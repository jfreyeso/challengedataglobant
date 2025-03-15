/* Fecha de creación: 2025-03-15
-- Funcionalidad: Script de creación de la tabla de fct_empleados_contratados
-- Autor: Juan Felipe Reyes Ortiz
-- fecha Modificacion   Autor            Descripcion
--------------------------------------------------------------------------------
-- 2025-03-15          Juan Felipe      Creación de la tabla
*/
create table fct_empleados_contratados (
id_emp_contatado_sk int primary key,
str_nombre_empleado varchar2(150) not null,
dtm_fecha_contratacion data is not null,
id_departamento_sk int not null,
num_id_trabajo_sk int not null,
str_status varchar2(50),
foreign key (id_departamento_sk) references departamento(id_departamento_sk),
foreign key (num_id_trabajo_sk) references trabajo(num_id_trabajo_sk)
);