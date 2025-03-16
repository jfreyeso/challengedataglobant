/* Fecha de creación: 2025-03-15
-- Funcionalidad: Script de creación de la tabla de departamentos
-- Autor: Juan Felipe Reyes Ortiz
-- fecha Modificacion   Autor            Descripcion
--------------------------------------------------------------------------------
-- 2025-03-15          Juan Felipe      Creación de la tabla de departamentos
*/
create table dim_trabajo (
    num_id_trabajo_sk NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    num_id_trabajo int not null,
    str_nombre_trabajo varchar(50) not null
);
