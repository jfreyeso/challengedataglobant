CREATE OR REPLACE PACKAGE pkg_dim_departamentos AS
/* Fecha de creación: 2025-03-15
-- Funcionalidad: Paquete para realizar CRUD de departamentos
-- Autor: Juan Felipe Reyes Ortiz
-- fecha Modificacion   Autor            Descripcion
--------------------------------------------------------------------------------
-- 2025-03-15          Juan Felipe      Creación del paquete
*/
    -- Procedimiento para insertar un nuevo departamento
    PROCEDURE insert_departamento(
        p_num_departamento IN VARCHAR2,
        p_nombre_departamento IN VARCHAR2
    );

    -- Procedimiento para actualizar un departamento existente
    PROCEDURE update_departamento(
        p_departamento_id IN NUMBER,
        p_num_departamento IN VARCHAR2,
        p_nombre_departamento IN VARCHAR2
    );

    -- Procedimiento para eliminar un departamento existente
    PROCEDURE delete_departamento(
        p_departamento_id IN NUMBER
    );
END pkg_dim_departamentos;
/

CREATE OR REPLACE PACKAGE BODY pkg_dim_departamentos AS
    -- Implementación del procedimiento para insertar un nuevo departamento
    PROCEDURE insert_departamento(
        p_num_departamento IN VARCHAR2,
        p_nombre_departamento IN VARCHAR2
    ) IS
    BEGIN
        BEGIN
            INSERT INTO dim_departamentos (num_departamento, str_nombre_departamento)
            VALUES (p_num_departamento, p_nombre_departamento);
        EXCEPTION
            WHEN OTHERS THEN
                RAISE_APPLICATION_ERROR(-20001, 'Error al insertar el departamento: ' || SQLERRM);
        END;
    END insert_departamento;

    -- Implementación del procedimiento para actualizar un departamento existente
    PROCEDURE update_departamento(
        p_departamento_id IN NUMBER,
        p_num_departamento IN VARCHAR2,
        p_nombre_departamento IN VARCHAR2
    ) IS
    BEGIN
        BEGIN
            UPDATE dim_departamentos
            SET num_departamento = p_num_departamento,
                str_nombre_departamento = p_nombre_departamento
            WHERE num_departamento = p_departamento_id;

            IF SQL%ROWCOUNT = 0 THEN
                RAISE_APPLICATION_ERROR(-20002, 'El departamento con ID ' || p_departamento_id || ' no existe.');
            END IF;
        EXCEPTION
            WHEN OTHERS THEN
                RAISE_APPLICATION_ERROR(-20003, 'Error al actualizar el departamento: ' || SQLERRM);
        END;
    END update_departamento;

    -- Implementación del procedimiento para eliminar un departamento existente
    PROCEDURE delete_departamento(
        p_departamento_id IN NUMBER
    ) IS
    BEGIN
        BEGIN
            DELETE FROM dim_departamentos
            WHERE num_departamento = p_departamento_id;

            IF SQL%ROWCOUNT = 0 THEN
                RAISE_APPLICATION_ERROR(-20004, 'El departamento con ID ' || p_departamento_id || ' no existe.');
            END IF;
        EXCEPTION
            WHEN OTHERS THEN
                RAISE_APPLICATION_ERROR(-20005, 'Error al eliminar el departamento: ' || SQLERRM);
        END;
    END delete_departamento;
END pkg_dim_departamentos;
/