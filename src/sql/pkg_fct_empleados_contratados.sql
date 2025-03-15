CREATE OR REPLACE PACKAGE pkg_fct_empleados_contratados AS
/* Fecha de creación: 2023-10-01
-- Funcionalidad: Paquete para realizar CRUD de fct_empleados_contratados contratados
-- Autor: Juan Felipe Reyes Ortiz
-- fecha Modificacion   Autor            Descripcion
--------------------------------------------------------------------------------
-- 2023-10-01           Juan Felipe      Creación del paquete
*/
    -- Procedimiento para insertar un empleado
    PROCEDURE insert_empleado(
        p_id IN NUMBER,
        p_nombre IN VARCHAR2,
        p_fecha_contratacion IN DATE,
        p_id_departamento IN NUMBER,
        p_id_trabajo IN NUMBER
    );

    -- Procedimiento para hacer merge de un empleado
    PROCEDURE merge_empleado(
        p_id IN NUMBER,
        p_nombre IN VARCHAR2,
        p_fecha_contratacion IN DATE,
        p_id_departamento IN NUMBER,
        p_id_trabajo IN NUMBER
    );

    -- Procedimiento para eliminar un empleado
    PROCEDURE delete_empleado(
        p_id IN NUMBER
    );
END pkg_fct_empleados_contratados;
/

CREATE OR REPLACE PACKAGE BODY pkg_fct_empleados_contratados AS
    -- Procedimiento para insertar un empleado
    PROCEDURE insert_empleado(
        p_id IN NUMBER,
        p_nombre IN VARCHAR2,
        p_fecha_contratacion IN DATE,
        p_id_departamento IN NUMBER,
        p_id_trabajo IN NUMBER
    ) IS
    BEGIN
        INSERT INTO fct_empleados_contratados (id_emp_contatado_sk, str_nombre_empleado, dtm_fecha_contratacion, str_status, id_departamento_sk, id_trabajo_sk)
        VALUES (p_id, p_nombre, p_fecha_contratacion, 'activo', p_id_departamento, p_id_trabajo);
    EXCEPTION
        WHEN NO_DATA_FOUND THEN
            DBMS_OUTPUT.PUT_LINE('Error: Departamento o Trabajo no encontrado.');
        WHEN OTHERS THEN
            DBMS_OUTPUT.PUT_LINE('Error en insert_empleado: ' || SQLERRM);
    END insert_empleado;

    -- Procedimiento para hacer merge de un empleado
    PROCEDURE merge_empleado(
        p_id IN NUMBER,
        p_nombre IN VARCHAR2,
        p_fecha_contratacion IN DATE,
        p_id_departamento IN NUMBER,
        p_id_trabajo IN NUMBER
    ) IS
    BEGIN
        MERGE INTO fct_empleados_contratados e
        USING (SELECT p_id AS id_emp_contatado_sk, p_nombre AS str_nombre_empleado, p_fecha_contratacion AS dtm_fecha_contratacion, p_id_departamento AS id_departamento_sk, p_id_trabajo AS id_trabajo_sk FROM dual) src
        ON (e.id_emp_contatado_sk = src.id_emp_contatado_sk)
        WHEN MATCHED THEN
            UPDATE SET e.str_nombre_empleado = src.str_nombre_empleado, e.dtm_fecha_contratacion = src.dtm_fecha_contratacion, e.id_departamento_sk = src.id_departamento_sk, e.id_trabajo_sk = src.id_trabajo_sk
        WHEN NOT MATCHED THEN
            INSERT (id_emp_contatado_sk, str_nombre_empleado, dtm_fecha_contratacion, id_departamento_sk, id_trabajo_sk)
            VALUES (src.id_emp_contatado_sk, src.str_nombre_empleado, src.dtm_fecha_contratacion, src.id_departamento_sk, src.id_trabajo_sk);
    EXCEPTION
        WHEN NO_DATA_FOUND THEN
            DBMS_OUTPUT.PUT_LINE('Error: Departamento o Trabajo no encontrado.');
        WHEN OTHERS THEN
            DBMS_OUTPUT.PUT_LINE('Error en merge_empleado: ' || SQLERRM);
    END merge_empleado;

    -- Procedimiento para eliminar un empleado (borrado lógico)
    PROCEDURE delete_empleado(
        p_id IN NUMBER
    ) IS
    BEGIN
        UPDATE fct_empleados_contratados
        SET str_status = 'inactivo'
        WHERE id_emp_contatado_sk = p_id;
    EXCEPTION
        WHEN OTHERS THEN
            DBMS_OUTPUT.PUT_LINE('Error en delete_empleado: ' || SQLERRM);
    END delete_empleado;
END pkg_fct_empleados_contratados;
/