import json
import traceback
from handlers import (
    get_all_departamentos, 
    get_department_by_id, 
    create_department,
    update_department,
    delete_department
)
from src.libs.utils.response import format_response

def lambda_handler(event, context):
    """
    Punto de entrada para la función Lambda de departamentos.
    Enruta las solicitudes a los controladores adecuados según el método HTTP y la ruta.
    """
    try:
        http_method = event['httpMethod']
        path = event['path']
        
        # Obtener el ID del departamento desde la ruta si existe
        department_id = None
        if '{id}' in path or '/departamentos/' in path and path != '/departamentos':
            path_parts = path.split('/')
            department_id = path_parts[-1]
            
        # Obtener el cuerpo de la solicitud si existe
        body = None
        if 'body' in event and event['body']:
            body = json.loads(event['body'])
            
        # Enrutamiento basado en el método HTTP
        if http_method == 'GET':
            if department_id:
                # GET /departamentos/{id}
                result = get_department_by_id(department_id)
            else:
                # GET /departamentos
                result = get_all_departamentos()
                
        elif http_method == 'POST':
            # POST /departamentos
            result = create_department(body)
            
        elif http_method == 'PUT':
            # PUT /departamentos/{id}
            if not department_id:
                return format_response(400, {"error": "El ID del Departmento es obligatorio para la actualización"})
            result = update_department(department_id, body)
            
        elif http_method == 'DELETE':
            # DELETE /departamentos/{id}
            if not department_id:
                return format_response(400, {"error": "El ID del Departmento es obligatorio para la eliminación"})
            result = delete_department(department_id)
            
        else:
            return format_response(405, {"error": "Metodo invalido"})
            
        # Formatear y devolver la respuesta
        return format_response(200, result)
        
    except Exception as e:
        print(f"Error processing request: {str(e)}")
        print(traceback.format_exc())
        return format_response(500, {"error": "Internal server error"})