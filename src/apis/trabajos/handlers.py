import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "libs"))

from src.libs.db.oracle_client import OracleConnection

def get_all_jobs():
    """
    Obtiene todos los empleados.
    
    Returns:
        dict: Lista de empleados
    """
    db = OracleConnection()
    try:
        #se obtienen todos los empleados
        query = "SELECT * FROM dim_trabajo"
        jobs = db.execute_query(query)
        
        return {"Empleados": jobs}
    finally:
        db.disconnect()

def get_job_by_id(num_id_trabajo):
    """
    Obtiene un trabajo por su ID.
    
    Args:
        num_id_trabajo (str): ID del trabajo
        
    Returns:
        dict: Datos del trabajo
    """
    db = OracleConnection()
    try:
        # Ejecutar una consulta SQL directa
        query = "SELECT * FROM dim_trabajo WHERE num_id_trabajo = :id"
        params = {"id": num_id_trabajo}
        jobs = db.execute_query(query, params)
        
        if not jobs:
            return {"error": "No existe el trabajo consultado", "status_code": 404}
        
        return {"Trabajo": jobs[0]}
    finally:
        db.disconnect()

def create_job(dic_trabajo):
    """
    Crea un nuevo trabajo.
    
    Args:
        dic_trabajo (dict): Datos del trabajo a crear
        
    Returns:
        dict: Resultado de la operación
    """
    if not dic_trabajo:
        return {"error": "Datos del trabajo son obligatorios", "status_code": 400}
        
    required_fields = ["num_id_trabajo","str_nombre_trabajo"]
    for field in required_fields:
        if field not in dic_trabajo:
            return {"error": f"El campo '{field}' es obligatorio", "status_code": 400}
    
    db = OracleConnection()
    try:
        result = db.execute_procedure(
            "pkg_dim_trabajos.insertar_trabajo",
            {
                "p_id": dic_trabajo["num_id_trabajo"],
                "p_nombre": dic_trabajo["str_nombre_trabajo"]
            }
        )
        
        if not result["success"]:
            return {"error": result["error"], "status_code": 400}
            
        return {"message": "Trabajo creado", "num_id_trabajo": dic_trabajo["num_id_trabajo"]}
    finally:
        db.disconnect()

def update_job(dic_trabajo):
    """
    Actualiza un trabajo existente.
    
    Args:
        dic_trabajo (dict): Datos del trabajo a actualizar
        
    Returns:
        dict: Resultado de la operación
    """
    if not dic_trabajo:
        return {"error": "Datos del trabajo son obligatorios", "status_code": 400}
    
    required_fields = ["num_id_trabajo","str_nombre_trabajo"]
    for field in required_fields:
        if field not in dic_trabajo:
            return {"error": f"El campo '{field}' es obligatorio", "status_code": 400}
    
    db = OracleConnection()
    try:
        # Verificar si el trabajo existe
        check_query = "SELECT 1 FROM dim_trabajo WHERE num_id_trabajo = :id"
        exists = db.execute_query(check_query, {"id": dic_trabajo["num_id_trabajo"]})
        
        if not exists:
            return {"error": "El trabajo a actualizar no existe", "status_code": 404}
        
        result = db.execute_procedure(
            "pkg_dim_trabajos.actualizar_trabajo",
            {
                "p_id": dic_trabajo["num_id_trabajo"],
                "p_nombre": dic_trabajo["str_nombre_trabajo"]
            }
        )
        
        
        if not result["success"]:
            return {"error": result["error"], "status_code": 400}

        return {"message": "Trabajo actualizado exitosamente"}
    finally:
        db.disconnect()

def delete_job(num_id_trabajo):
    """
    Elimina un trabajo.
    
    Args:
        num_id_trabajo (num): ID del trabajo a eliminar
        
    Returns:
        dict: Resultado de la operación
    """
    db = OracleConnection()
    try:
        
        if not num_id_trabajo:
            return {"error": "Body vacio se requiere el id del trabajo", "status_code": 400}
        
        required_fields = ["num_id_trabajo"]
        for field in required_fields:
            if field not in num_id_trabajo:
             return {"error": f"El campo '{field}' es obligatorio", "status_code": 400}
        
        # Verificar si el trabajo existe
        check_query = "SELECT 1 FROM dim_trabajo WHERE num_id_trabajo = :num_id_trabajo"
        exists = db.execute_query(check_query, {"num_id_trabajo": num_id_trabajo})
        
        if not exists:
            return {"error": "Trabajo no encontrado", "status_code": 404}
        
        # Ejecutar un procedimiento almacenado
        result = db.execute_procedure(
             "pkg_dim_trabajos.eliminar_trabajo",
             {"p_id": num_id_trabajo}
         )
        if not result["success"]:
            return {"error": result["error"], "status_code": 400}
        
        return {"message": "Trabajo eliminado exitosamente"}
    finally:
        db.disconnect()