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
    
    def connect(self):
        """Método abstracto para establecer la conexión."""
        raise NotImplementedError("Debe implementarse en las clases hijas")
    
    def disconnect(self):
        """Método abstracto para cerrar la conexión."""
        raise NotImplementedError("Debe implementarse en las clases hijas")
    
    def execute_query(self, query, params=None):
        """Método abstracto para ejecutar consultas."""
        raise NotImplementedError("Debe implementarse en las clases hijas")
    
    def execute_procedure(self, procedure_name, params=None):
        """Método abstracto para ejecutar procedimientos almacenados."""
        raise NotImplementedError("Debe implementarse en las clases hijas")