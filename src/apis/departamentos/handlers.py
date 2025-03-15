from src.libs.db.oracle_client import OracleConnection

def get_all_departments():
    """
    Obtiene todos los departamentos.
    
    Returns:
        dict: Lista de departamentos
    """
    db = OracleConnection()
    try:
        # Opción 1: Ejecutar una consulta SQL directa
        query = "SELECT * FROM departments"
        departments = db.execute_query(query)
        
        # Opción 2: Ejecutar un procedimiento almacenado
        # result = db.execute_procedure("pkg_departments.get_all_departments")
        # departments = result.get("departments", [])
        
        return {"departments": departments}
    finally:
        db.disconnect()

def get_department_by_id(department_id):
    """
    Obtiene un departamento por su ID.
    
    Args:
        department_id (str): ID del departamento
        
    Returns:
        dict: Datos del departamento
    """
    db = OracleConnection()
    try:
        # Opción 1: Ejecutar una consulta SQL directa
        query = "SELECT * FROM departments WHERE department_id = :id"
        params = {"id": department_id}
        departments = db.execute_query(query, params)
        
        if not departments:
            return {"error": "Department not found", "status_code": 404}
            
        # Opción 2: Ejecutar un procedimiento almacenado
        # result = db.execute_procedure(
        #     "pkg_departments.get_department_by_id",
        #     {"p_department_id": department_id}
        # )
        
        return {"department": departments[0]}
    finally:
        db.disconnect()

def create_department(department_data):
    """
    Crea un nuevo departamento.
    
    Args:
        department_data (dict): Datos del departamento a crear
        
    Returns:
        dict: Resultado de la operación
    """
    if not department_data:
        return {"error": "Department data is required", "status_code": 400}
        
    required_fields = ["department_name", "location_id"]
    for field in required_fields:
        if field not in department_data:
            return {"error": f"Field '{field}' is required", "status_code": 400}
    
    db = OracleConnection()
    try:
        # Opción 1: Ejecutar una consulta SQL directa
        query = """
            INSERT INTO departments (department_name, location_id) 
            VALUES (:name, :location_id) 
            RETURNING department_id INTO :department_id
        """
        params = {
            "name": department_data["department_name"],
            "location_id": department_data["location_id"],
            "department_id": None  # Salida
        }
        
        # Para inserciones con valores de retorno se necesita un approach específico
        # Esta es una versión simplificada, en la práctica se necesitaría adaptar
        # al uso específico de cx_Oracle para manejar variables de salida
        
        # Opción 2: Ejecutar un procedimiento almacenado (mejor opción)
        result = db.execute_procedure(
            "pkg_departments.create_department",
            {
                "p_department_name": department_data["department_name"],
                "p_location_id": department_data["location_id"]
            }
        )
        
        if not result["success"]:
            return {"error": result["error"], "status_code": 400}
            
        return {"message": "Department created successfully", "department_id": result.get("department_id")}
    finally:
        db.disconnect()

def update_department(department_id, department_data):
    """
    Actualiza un departamento existente.
    
    Args:
        department_id (str): ID del departamento a actualizar
        department_data (dict): Nuevos datos del departamento
        
    Returns:
        dict: Resultado de la operación
    """
    if not department_data:
        return {"error": "Department data is required", "status_code": 400}
    
    db = OracleConnection()
    try:
        # Verificar si el departamento existe
        check_query = "SELECT 1 FROM departments WHERE department_id = :id"
        exists = db.execute_query(check_query, {"id": department_id})
        
        if not exists:
            return {"error": "Department not found", "status_code": 404}
        
        # Opción 1: Ejecutar una consulta SQL directa
        update_fields = []
        params = {"id": department_id}
        
        if "department_name" in department_data:
            update_fields.append("department_name = :name")
            params["name"] = department_data["department_name"]
            
        if "location_id" in department_data:
            update_fields.append("location_id = :location_id")
            params["location_id"] = department_data["location_id"]
            
        if not update_fields:
            return {"message": "No fields to update"}
            
        query = f"UPDATE departments SET {', '.join(update_fields)} WHERE department_id = :id"
        db.execute_query(query, params)
        
        # Opción 2: Ejecutar un procedimiento almacenado
        # proc_params = {"p_department_id": department_id}
        # if "department_name" in department_data:
        #     proc_params["p_department_name"] = department_data["department_name"]
        # if "location_id" in department_data:
        #     proc_params["p_location_id"] = department_data["location_id"]
        #
        # result = db.execute_procedure(
        #     "pkg_departments.update_department",
        #     proc_params
        # )
        
        return {"message": "Department updated successfully"}
    finally:
        db.disconnect()

def delete_department(department_id):
    """
    Elimina un departamento.
    
    Args:
        department_id (str): ID del departamento a eliminar
        
    Returns:
        dict: Resultado de la operación
    """
    db = OracleConnection()
    try:
        # Verificar si el departamento existe
        check_query = "SELECT 1 FROM departments WHERE department_id = :id"
        exists = db.execute_query(check_query, {"id": department_id})
        
        if not exists:
            return {"error": "Department not found", "status_code": 404}
        
        # Opción 1: Ejecutar una consulta SQL directa
        query = "DELETE FROM departments WHERE department_id = :id"
        db.execute_query(query, {"id": department_id})
        
        # Opción 2: Ejecutar un procedimiento almacenado
        # result = db.execute_procedure(
        #     "pkg_departments.delete_department",
        #     {"p_department_id": department_id}
        # )
        
        return {"message": "Department deleted successfully"}
    finally:
        db.disconnect()