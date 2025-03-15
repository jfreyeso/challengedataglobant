CREATE OR REPLACE PACKAGE pkg_dim_trabajos AS
/* Fecha de creación: 2025-03-15
-- Funcionalidad: Paquete para realizar CRUD de dim_trabajo
-- Autor: Juan Felipe Reyes Ortiz
-- fecha Modificacion   Autor            Descripcion
--------------------------------------------------------------------------------
-- 2025-03-15           Juan Felipe      Creación del paquete
*/

-- Procedimiento para insertar un trabajo
PROCEDURE insertar_trabajo(p_id IN NUMBER, p_nombre IN VARCHAR2);

-- Procedimiento para actualizar un trabajo
PROCEDURE actualizar_trabajo(p_id IN NUMBER, p_nombre IN VARCHAR2);

-- Procedimiento para eliminar un trabajo
PROCEDURE eliminar_trabajo(p_id IN NUMBER);

END pkg_dim_trabajos;
/

CREATE OR REPLACE PACKAGE BODY pkg_dim_trabajos AS

-- Procedimiento para insertar un trabajo
PROCEDURE insertar_trabajo(p_id IN NUMBER, p_nombre IN VARCHAR2) IS
BEGIN
    INSERT INTO dim_trabajo (num_id_trabajo, str_nombre_trabajo) VALUES (p_id, p_nombre);
    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        RAISE_APPLICATION_ERROR(-20001, 'Error al insertar trabajo: ' || SQLERRM);
END insertar_trabajo;

-- Procedimiento para actualizar un trabajo
PROCEDURE actualizar_trabajo(p_id IN NUMBER, p_nombre IN VARCHAR2) IS
BEGIN
    UPDATE dim_trabajo SET str_nombre_trabajo = p_nombre WHERE num_id_trabajo = p_id;
    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        RAISE_APPLICATION_ERROR(-20002, 'Error al actualizar trabajo: ' || SQLERRM);
END actualizar_trabajo;

-- Procedimiento para eliminar un trabajo
PROCEDURE eliminar_trabajo(p_id IN NUMBER) IS
BEGIN
    DELETE FROM dim_trabajo WHERE num_id_trabajo = p_id;
    COMMIT;
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        RAISE_APPLICATION_ERROR(-20003, 'Error al eliminar trabajo: ' || SQLERRM);
END eliminar_trabajo;

END pkg_dim_trabajos;
/