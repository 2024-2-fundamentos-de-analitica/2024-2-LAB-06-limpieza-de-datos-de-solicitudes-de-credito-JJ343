"""
Escriba el codigo que ejecute la accion solicitada en la pregunta.
"""


def pregunta_01():
    """
    Realice la limpieza del archivo "files/input/solicitudes_de_credito.csv".
    El archivo tiene problemas como registros duplicados y datos faltantes.
    Tenga en cuenta todas las verificaciones discutidas en clase para
    realizar la limpieza de los datos.

    El archivo limpio debe escribirse en "files/output/solicitudes_de_credito.csv"

    """
import pandas as pd
import re
import os 
# Cargar el archivo
df = pd.read_csv('files/input/solicitudes_de_credito.csv', delimiter =";")

# Eliminar duplicados
df.drop('Unnamed: 0', axis=1, inplace=True)
est=[]
com=[]
for item in df['estrato']:
    stra=int(item)
    est.append(stra)
df["estrato"]=est
for item in df['comuna_ciudadano']:
    co=int(item)
    com.append(co)
df["comuna_ciudadano"]=com

#lower
df['sexo']= df['sexo'].str.lower()
df['tipo_de_emprendimiento']=df['tipo_de_emprendimiento'].str.lower()
df['idea_negocio']=df['idea_negocio'].str.lower()
df['barrio']=df['barrio'].str.lower()
df['línea_credito']=df['línea_credito'].str.lower()
#replace
df['línea_credito']=df['línea_credito'].str.replace('-','_').str.replace('_'," ").str.replace(' ','').str.replace('.','').str.rstrip()
df['barrio']=df['barrio'].str.replace('-','_').str.replace('_'," ").str.replace(' ','').str.rstrip()
df['idea_negocio']=df['idea_negocio'].str.replace('-','_').str.replace('_'," ").str.replace(' ','').str.replace('.',"").str.rstrip()
df['monto_del_credito']=df['monto_del_credito'].str.replace(',','').str.replace(' ', '').str.replace('$','').str.lstrip().str.split('.').str[0]

#numbre

y=[]
for items in  df['idea_negocio']:
  palabra_sin_numero= re.sub(r'\d+', '', items)

  y.append(palabra_sin_numero)
df['idea_negocio']=y



fechas=[]
# Convertir fechas erróneas con un formato alternativo

for items in df['fecha_de_beneficio']:
    
    def convertir_fecha_cadenas(fecha):
        if '/' in fecha:  # Verifica si se utiliza '/' como separador
            partes = fecha.split('/')
            if len(partes[0]) == 4:  # Caso: formato 'yyyy/mm/dd'
                anio, mes, dia = partes

            else:  # Caso: formato 'dd/mm/yy'
                dia, mes, anio = partes
            # Retorna en formato estándar 'yyyy-mm-dd'
            date= f"{anio}/{mes}/{dia}"
            date=pd.to_datetime(date, format="%Y/%m/%d")
            return date
      
    fechas.append(convertir_fecha_cadenas(items))
df['fecha_de_beneficio']  = fechas



df = df.drop_duplicates()
df = df.dropna()

print()



filtered_df=df[df['línea_credito']=="credioportuno"]

output_directory = 'files/output'
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Guardar el archivo limpio
df.to_csv('files/output/solicitudes_de_credito.csv', sep=";", index=False)


print(df["barrio"].value_counts().to_list())
