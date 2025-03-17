import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "libs"))

from src.libs.db.oracle_client import OracleConnection

def get_all_departments():
    """
    Obtiene todos los departamentos.
    
    Returns:
        dict: Lista de departamentos
    """
    db = OracleConnection()
    try:
        #se obtienen todos los departamentos
        query = "SELECT * FROM dim_departamentos"
        departments = db.execute_query(query)
        
        return {"departments": departments}
    finally:
        db.disconnect()

def get_department_by_id(num_departamento):
    """
    Obtiene un departamento por su ID.
    
    Args:
        num_departamento (str): ID del departamento
        
    Returns:
        dict: Datos del departamento
    """
    db = OracleConnection()
    try:
        # Opción 1: Ejecutar una consulta SQL directa
        query = "SELECT * FROM dim_departamentos WHERE num_departamento = :id"
        params = {"id": num_departamento}
        departments = db.execute_query(query, params)
        
        if not departments:
            return {"error": "No existe el departamento consultado", "status_code": 404}
            
        # Opción 2: Ejecutar un procedimiento almacenado
        # result = db.execute_procedure(
        #     "pkg_departments.get_department_by_id",
        #     {"p_num_departamento": num_departamento}
        # )
        
        return {"department": departments[0]}
    finally:
        db.disconnect()

def create_department(dic_departamento):
    """
    Crea un nuevo departamento.
    
    Args:
        dic_departamento (dict): Datos del departamento a crear
        
    Returns:
        dict: Resultado de la operación
    """
    if not dic_departamento:
        return {"error": "Datos del departamento son obligatorios", "status_code": 400}
        
    required_fields = ["num_departamento", "str_nombre_departamento"]
    for field in required_fields:
        if field not in dic_departamento:
            return {"error": f"El campo '{field}' es obligatorio", "status_code": 400}
    
    db = OracleConnection()
    try:
        result = db.execute_procedure(
            "pkg_dim_departamentos.insert_departamento",
            {
                "p_num_departamento": dic_departamento["num_departamento"],
                "p_nombre_departamento": dic_departamento["str_nombre_departamento"]
            }
        )
        
        if not result["success"]:
            return {"error": result["error"], "status_code": 400}
            
        return {"message": "Departmento creado", "num_departamento": dic_departamento["num_departamento"]}
    finally:
        db.disconnect()

def update_department(dic_departamento):
    """
    Actualiza un departamento existente.
    
    Args:
        dic_departamento (dict): Datos del departamento a actualizar
        
    Returns:
        dict: Resultado de la operación
    """
    if not dic_departamento:
        return {"error": "Datos del departamento son obligatorios", "status_code": 400}
    
    required_fields = ["id_departamento_sk","num_departamento", "str_nombre_departamento"]
    for field in required_fields:
        if field not in dic_departamento:
            return {"error": f"El campo '{field}' es obligatorio", "status_code": 400}
    
    db = OracleConnection()
    try:
        # Verificar si el departamento existe
        check_query = "SELECT 1 FROM dim_departamentos WHERE num_departamento = :id"
        exists = db.execute_query(check_query, {"id": dic_departamento["id_departamento_sk"]})
        
        if not exists:
            return {"error": "El departamento a actualizar no existe", "status_code": 404}
        
        result = db.execute_procedure(
            "pkg_dim_departamentos.update_departamento",
            {
                "p_departamento_id": dic_departamento["id_departamento_sk"],
                "p_num_departamento": dic_departamento["num_departamento"],
                "p_nombre_departamento": dic_departamento["str_nombre_departamento"]
            }
        )
        
        
        if not result["success"]:
            return {"error": result["error"], "status_code": 400}
        

        
        return {"message": "Department updated successfully"}
    finally:
        db.disconnect()

def delete_department(num_departamento):
    """
    Elimina un departamento.
    
    Args:
        num_departamento (str): ID del departamento a eliminar
        
    Returns:
        dict: Resultado de la operación
    """
    db = OracleConnection()
    try:
        # Verificar si el departamento existe
        check_query = "SELECT 1 FROM departments WHERE num_departamento = :id"
        exists = db.execute_query(check_query, {"id": num_departamento})
        
        if not exists:
            return {"error": "Department not found", "status_code": 404}
        
        # Opción 1: Ejecutar una consulta SQL directa
        query = "DELETE FROM departments WHERE num_departamento = :id"
        db.execute_query(query, {"id": num_departamento})
        
        # Opción 2: Ejecutar un procedimiento almacenado
        # result = db.execute_procedure(
        #     "pkg_departments.delete_department",
        #     {"p_num_departamento": num_departamento}
        # )
        
        return {"message": "Department deleted successfully"}
    finally:
        db.disconnect()