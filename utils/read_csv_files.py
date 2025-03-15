"""
Modulo para la lectura de archivos de tipo csv
:param:
archivo (str) : nombre del archivo
ruta (str) : ruta del archivo
:return: 
DataFrame con el contenido del archivo
"""
import os
import pandas as pd

class FileReader:
    """
    Clase que permite leer diferentes tipos de archivos
    :param:
    archivo (str) : nombre del archivo
    ruta (str) : ruta del archivo
    :return: 
    DataFrame con el contenido del archivo
    """
    def __init__(self, ruta, archivo):
        """
        Constructor de la clase
        """
        self.ruta = ruta
        self.archivo = archivo

    def read_file(self):
        """
        valida que el archivo sea de tipo csv
        :param archivo (str) : nombre del archivo
        :return: DataFrame con el contenido del archivo
        """
        file_extension = os.path.splitext(self.archivo)[1]
        print(f'{file_extension=}')
        if file_extension == '.csv':
            df_archivo = self.read_csv_file()
        else:
            df_archivo = 'invalide file type'
        return df_archivo

    def read_csv_file(self):
        """
        Leer archivos de tipo CSV
        :param:
        archivo (str) : nombre del archivo
        ruta (str) : ruta del archivo
        :return: 
        DataFrame con el contenido del archivo
        """
        path_file = os.path.join(self.ruta, self.archivo)
        df_archivo = pd.read_csv(path_file, sep=',', encoding='utf-8')
        #print(df_archivo)
        return df_archivo

# Usage example
#file_reader = FileReader('./data/input', 'departments.csv')
#file_content = file_reader.read_file()