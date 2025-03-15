"""
Modulo para la guardar archivos en formato avro a partir de un dataframe
:param:
 df_archivo (dataframe) : nombre del dataframe de entrada
 ruta (str) : ruta del archivo
:return: 
 resultado (str) : mensaje de exito o error
"""
import os
import pandas as pd
from fastavro import writer, parse_schema

class saveAvroFile:
    """
    Clase que permite guardar archivos de tipo Avro en una ruta especifica
    :param:
     df_archivo (dataframe) : nombre del dataframe de entrada
     ruta (str) : ruta del archivo
    :return: 
     resultado (str) : mensaje de exito o error
    """
    def __init__(self, ruta, df_archivo):
        """
        Constructor de la clase
        """
        self.ruta = ruta
        self.df_archivo = df_archivo

    def save_avro_file(self):
        """
        guardar archivos de tipo avro.
        :param:
         df_archivo (dataframe) : nombre del dataframe de entrada
         ruta (str) : ruta del archivo
        :return: 
         resultado (str) : mensaje de exito o error
        """
        try:
            # Define Avro schema
            schema = {
                "type": "record",
                "name": "DataFrameRecord",
                "fields": [{"name": col, "type": ["null", "string"]} for col in self.df_archivo.columns]
            }
            parsed_schema = parse_schema(schema)

            # Convert DataFrame to records
            records = self.df_archivo.to_dict(orient='records')

            # Write records to Avro file
            with open(self.ruta, 'wb') as out:
                writer(out, parsed_schema, records)

            resultado = "Archivo Avro guardado exitosamente."
        except Exception as e:
            resultado = f"Error al guardar el archivo Avro: {e}"
        
        return resultado


# Usage example
#df = pd.DataFrame({'col1': ['value1', 'value2'], 'col2': ['value3', 'value4']})
#avro_saver = saveAvroFile('./data/output/departments.avro', df)
#result = avro_saver.save_avro_file()
#print(result)