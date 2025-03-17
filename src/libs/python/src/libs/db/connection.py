import os
import json
from ..auth.secrets import get_secret

class DatabaseConnection:
    """Clase para manejar conexiones a bases de datos."""
    
    def __init__(self):
        self.connection = None
        self.secret_arn = os.environ.get('DB_SECRET_ARN')
        self.db_config = None
     
    def get_connection_params(self):
        """Obtiene los parámetros de conexión desde AWS Secrets Manager."""
        if not self.db_config:
            secret_data = get_secret(self.secret_arn)
            self.db_config = json.loads(secret_data)
        return self.db_config