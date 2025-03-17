import json

def format_response(status_code, body):
    """
    Formatea la respuesta para API Gateway.
    
    Args:
        status_code (int): Código de estado HTTP
        body (dict): Cuerpo de la respuesta
        
    Returns:
        dict: Respuesta formateada para API Gateway
    """
    # Si body contiene un status_code, usarlo en lugar del proporcionado
    if isinstance(body, dict) and "status_code" in body:
        status_code = body.pop("status_code")
    
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET,POST,PUT,DELETE,OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type,Authorization"
        },
        "body": json.dumps(body)
    }