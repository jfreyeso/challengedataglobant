import sys
import os

# Agregar rutas para encontrar la capa y otras dependencias
sys.path.append("/opt")  # AWS Lambda usa `/opt` para capas

import json
import traceback
import logging
from handlers import (
    get_all_departments, 
    get_department_by_id, 
    create_department,
    update_department,
    delete_department
)
from src.libs.utils.response import format_response
from src.libs.utils.auth import validate_token , extract_token_from_header

# 🔹 Configuración de Logging
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Imprimir logs en consola
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)
logging.getLogger().addHandler(console_handler)

def lambda_handler(event, context):
    """
    Punto de entrada para la función Lambda de departamentos.
    Enruta las solicitudes a los controladores adecuados según el método HTTP y la ruta.
    """
    try:
        # Validar el token de autenticación
        if 'headers' not in event or 'Authorization' not in event['headers']:
            logging.warning("⚠️ Missing Authentication Token")
            return format_response(401, {"error": "Missing Authentication Token"})
        
        token = event['headers']['Authorization']
        token = extract_token_from_header(token)
        
        if not validate_token(token):
            logging.warning("❌ Invalid Authentication Token")
            return format_response(403, {"error": "Invalid Authentication Token"})
        
        http_method = event['httpMethod']
        path = event['path']
        
        
        # Obtener el ID del departamento si existe
        department_id = None
        if '{id}' in path or '/departamentos/' in path and path != '/departamentos':
            path_parts = path.split('/')
            department_id = path_parts[-1]
            
            
        # Obtener el cuerpo de la solicitud si existe
        body = None
        if 'body' in event and event['body']:
            body = json.loads(event['body'])
            logging.info("📦 Request Body: %s", body)
            
        # Enrutamiento basado en el método HTTP
        if http_method == 'GET':
            if department_id:
                logging.info(f"🔍 Fetching department with ID: {department_id}")
                result = get_department_by_id(department_id)
            else:
                logging.info("📋 Fetching all departments")
                result = get_all_departments()
                
        elif http_method == 'POST':
            logging.info("🆕 Creating a new department")
            result = create_department(body)
            
        elif http_method == 'PUT':
            if not department_id:
                logging.warning("⚠️ EL numero del Department es obligatorio para la actualización")
                return format_response(400, {"error": "El ID del Departamento es obligatorio para la actualización"})
            logging.info(f"♻️ Se actualizo el departamento numero: {department_id}")
            result = update_department(body)
            
        elif http_method == 'DELETE':
            if not department_id:
                logging.warning("⚠️ Department ID is required for deletion")
                return format_response(400, {"error": "El ID del Departamento es obligatorio para la eliminación"})
            logging.info(f"🗑️ Deleting department with ID: {department_id}")
            result = delete_department(department_id)
            
        else:
            logging.warning("🚫 Invalid HTTP method")
            return format_response(405, {"error": "Método inválido"})
            
        logging.info("✅ Response: %s", json.dumps(result))
        return format_response(200, result)
        
    except Exception as e:
        logging.error(f"🔥 Error processing request: {str(e)}")
        logging.error(traceback.format_exc())
        return format_response(500, {"error": "Internal server error"})
