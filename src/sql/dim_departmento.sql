/* Fecha de creación: 2025-03-15
-- Funcionalidad: Script de creación de la tabla de departamentos
-- Autor: Juan Felipe Reyes Ortiz
-- fecha Modificacion   Autor            Descripcion
--------------------------------------------------------------------------------
-- 2025-03-15          Juan Felipe      Creación de la tabla de departamentos
*/
create table dim_departamentos (
    id_departamento_sk serial primary key,
    num_departamento int not null,
    str_nombre_departamento varchar(50) not null
);