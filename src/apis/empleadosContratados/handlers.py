import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "libs"))

from src.libs.db.oracle_client import OracleConnection

def get_all_employees():
    """
    Obtiene todos los departamentos.
    
    Returns:
        dict: Lista de departamentos
    """
    db = OracleConnection()
    try:
        #se obtienen todos los departamentos
        query = "SELECT * FROM fct_empleados_contratados"
        employees = db.execute_query(query)
        
        return {"employees": employees}
    finally:
        db.disconnect()

def get_employee_by_id(num_id_empleado):
    """
    Obtiene un empleado por su ID.
    
    Args:
        num_id_empleado (num): ID del empleado
        
    Returns:
        dict: Datos del empleado
    """
    db = OracleConnection()
    try:
        # Opción 1: Ejecutar una consulta SQL directa
        query = "SELECT * FROM fct_empleados_contratados WHERE id_emp_contatado_sk = :id"
        params = {"id": num_id_empleado}
        employees = db.execute_query(query, params)
        
        if not employees:
            return {"error": "No existe el empleado consultado", "status_code": 404}
        
        return {"EmpleadoContratado": employees[0]}
    finally:
        db.disconnect()

def create_employee(dic_empleado):
    """
    Crea un nuevo empleado.
    
    Args:
        dic_empleado (dict): Datos del empleado a crear
        
    Returns:
        dict: Resultado de la operación
    """
    if not dic_empleado:
        return {"error": "Datos del empleado son obligatorios", "status_code": 400}
        
    required_fields = ["num_id_empleado", "str_nombre_empleado","dtm_fecha_contratacion","id_departamento_sk","num_id_trabajo_sk"]
    for field in required_fields:
        if field not in dic_empleado:
            return {"error": f"El campo '{field}' es obligatorio", "status_code": 400}
    
    db = OracleConnection()
    try:
        result = db.execute_procedure(
            "pkg_fct_empleados_contratados.insert_empleado",
            {
                "num_id_empleado":dic_empleado["num_id_empleado"],
                "str_nombre_empleado": dic_empleado["str_nombre_empleado"],
                "dtm_fecha_contratacion": dic_empleado["dtm_fecha_contratacion"],
                "id_departamento_sk": dic_empleado["id_departamento_sk"],
                "num_id_trabajo_sk": dic_empleado["num_id_trabajo_sk"]
            }
        )
        
        if not result["success"]:
            return {"error": result["error"], "status_code": 400}
            
        return {"message": "Empleado creado", "num_id_empleado": dic_empleado["num_id_empleado"]}
    finally:
        db.disconnect()

def update_employee(dic_empleado):
    """
    Actualiza un empleado existente.
    
    Args:
        dic_empleado (dict): Datos del empleado a actualizar
        
    Returns:
        dict: Resultado de la operación
    """
    if not dic_empleado:
        return {"error": "Datos del empleado son obligatorios", "status_code": 400}
    
    required_fields = ["num_id_empleado", "str_nombre_empleado","dtm_fecha_contratacion","id_departamento_sk","num_id_trabajo_sk"]
    for field in required_fields:
        if field not in dic_empleado:
            return {"error": f"El campo '{field}' es obligatorio", "status_code": 400}
    
    db = OracleConnection()
    try:
        # Verificar si el empleado existe
        check_query = "SELECT 1 FROM fct_empleados_contratados WHERE num_id_empleado = :id"
        exists = db.execute_query(check_query, {"id": dic_empleado["num_id_empleado"]})
        
        if not exists:
            return {"error": "El empleado a actualizar no existe", "status_code": 404}
        
        result = db.execute_procedure(
            "pkg_fct_empleados_contratados.merge_empleado",
            {
                "num_id_empleado":dic_empleado["num_id_empleado"],
                "str_nombre_empleado": dic_empleado["str_nombre_empleado"],
                "dtm_fecha_contratacion": dic_empleado["dtm_fecha_contratacion"],
                "id_departamento_sk": dic_empleado["id_departamento_sk"],
                "num_id_trabajo_sk": dic_empleado["num_id_trabajo_sk"]
            }
        )
        
        
        if not result["success"]:
            return {"error": result["error"], "status_code": 400}
        
        return {"message": "Empleado actualizado exitosamente"}
    finally:
        db.disconnect()

def delete_employee(num_id_empleado):
    """
    Elimina un empleado.
    
    Args:
        num_id_empleado (str): ID del empleado a eliminar
        
    Returns:
        dict: Resultado de la operación
    """
    db = OracleConnection()
    try:
        # Verificar si el empleado existe
        check_query = "SELECT 1 FROM fct_empleados_contratados WHERE num_id_empleado = :id"
        exists = db.execute_query(check_query, {"id": num_id_empleado})
        
        if not exists:
            return {"error": "Empleado no encontrado", "status_code": 404}
        
        # Ejecutar un procedimiento almacenado
        result = db.execute_procedure(
             "pkg_fct_empleados_contratados.delete_empleado",
             {"p_num_id_empleado": num_id_empleado}
         )
        if not result["success"]:
            return {"error": result["error"], "status_code": 400}
        
        return {"message": "Empleado eliminado exitosamente"}
    finally:
        db.disconnect()