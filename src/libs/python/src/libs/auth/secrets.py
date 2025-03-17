import boto3
from botocore.exceptions import ClientError

def get_secret(secret_arn):
    """
    Obtiene un secreto desde AWS Secrets Manager.
    
    Args:
        secret_arn (str): ARN del secreto a recuperar
        
    Returns:
        str: Valor del secreto en formato JSON
        
    Raises:
        Exception: Si ocurre un error al obtener el secreto
    """
    client = boto3.client('secretsmanager')
    
    try:
        response = client.get_secret_value(SecretId=secret_arn)
        
        # El secreto puede estar en SecretString o SecretBinary
        if 'SecretString' in response:
            return response['SecretString']
        else:
            return response['SecretBinary']
            
    except ClientError as e:
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']
        raise Exception(f"Error retrieving secret: {error_code} - {error_message}")