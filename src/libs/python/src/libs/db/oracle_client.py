import os
import oracledb
from .connection import DatabaseConnection

# Definir variables de entorno necesarias
os.environ["NLS_LANG"] = "AMERICAN_AMERICA.AL32UTF8"

class OracleConnection(DatabaseConnection):
    """Clase específica para conexiones a Oracle."""
    
    def connect(self):
        """Establece la conexión con la base de datos Oracle."""
        if self.connection is None:
            config = self.get_connection_params()
            
            # Configuración de la conexión
            host = config['host']
            port = config['port']
            service_name = config.get('service_name', config.get('dbname', ''))
            
            dsn = f"(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST={host})(PORT={port}))(CONNECT_DATA=(SERVICE_NAME={service_name})))"
            print(f"dsn: {dsn}")
            
            self.connection = oracledb.connect(
                user=config['username'],
                password=config['password'],
                dsn=dsn
            )
            print("coenctado a la db")
        return self.connection
    
    def disconnect(self):
        """Cierra la conexión con la base de datos."""
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def execute_query(self, query, params=None):
        """
        Ejecuta una consulta SQL y devuelve los resultados.
        
        Args:
            query (str): Consulta SQL a ejecutar
            params (dict, optional): Parámetros para la consulta
            
        Returns:
            list: Lista de diccionarios con los resultados
        """
        conn = self.connect()
        cursor = conn.cursor()
        
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
                
            # Obtener nombres de columnas
            columns = [col[0].lower() for col in cursor.description]
            
            # Convertir resultados a lista de diccionarios
            results = []
            for row in cursor:
                results.append(dict(zip(columns, row)))
                
            return results
            
        finally:
            cursor.close()
    
    def execute_procedure(self, procedure_name, params=None):
        """
        Ejecuta un procedimiento almacenado en Oracle.
        
        Args:
            procedure_name (str): Nombre del procedimiento
            params (dict, optional): Parámetros para el procedimiento
            
        Returns:
            dict: Resultados del procedimiento
        """
        conn = self.connect()
        cursor = conn.cursor()
        
        try:
            # Construir la llamada al procedimiento
            if params:
                placeholders = ", ".join([f":{key}" for key in params.keys()])
                call_statement = f"BEGIN {procedure_name}({placeholders}); END;"
                cursor.execute(call_statement, params)
            else:
                call_statement = f"BEGIN {procedure_name}; END;"
                cursor.execute(call_statement)
            
            conn.commit()
            return {"success": True}
            
        except oracledb.DatabaseError as e:
            conn.rollback()
            error, = e.args
            return {"success": False, "error": error.message}
            
        finally:
            cursor.close()