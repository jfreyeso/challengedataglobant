/* Fecha de creación: 2025-03-15
-- Funcionalidad: Script de creación de la tabla de departamentos
-- Autor: Juan Felipe Reyes Ortiz
-- fecha Modificacion   Autor            Descripcion
--------------------------------------------------------------------------------
-- 2025-03-15          Juan Felipe      Creación de la tabla de departamentos
*/
CREATE TABLE dim_departamentos (
    id_departamento_sk NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    num_departamento NUMBER NOT NULL,
    str_nombre_departamento VARCHAR2(50) NOT NULL
);