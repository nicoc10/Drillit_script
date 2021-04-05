#!/usr/bin/env python
# coding: utf-8

# In[247]:


import pandas as pd
import numpy as np
import re
import os 


# In[234]:


print('Abriendo carpeta: '+ os.getcwd()+' ...')


# In[195]:


def alerta(list):
    #Si no hay ningun falso -> mensaje positivo
    if all(list): print (mensaje_pos)
    else: print (mensaje_neg)


# In[261]:


#with open('default_cols.txt', 'w') as f:
#    for col in list(data.columns.values):
#        f.write("%s\n" % col)


# Cargar archivo a comprobar:

# In[262]:


file_name = 'MAFXX-banco-malla_error.csv'
print('Cargando el archivo '+file_name+'...')
data = pd.read_csv(file_name)


# In[263]:


#Comprobar nombre del archivo
print("Comprobando nombre del archivo:")
print("-> Por definir ...")


# In[264]:


with open('default_cols.txt', 'r') as f:
    default_cols = [str(line.strip()) for line in f]


# In[265]:


#Columnas
print("Comprobando columnas:")
check = []
mensaje_neg = "-> ERROR!, El archivo NO contiene las columnas necesarias"
mensaje_pos = "-> BIEN!, El archivo SI contiene las columnas necesarias"

#Comprueba si tienen el mismo numero de cols:
file_cols = list(data.columns.values)
col_numb = len(file_cols)==len(default_cols)
check.append(col_numb)
#Comprueba si esas columnas son iguales:
for n in range(0,len(default_cols)):
    c = default_cols[n].split() == file_cols[n].split()
    check.append(c)
#Ejecutar alerta si es necesario
alerta(check)


# In[266]:


print("Comprobando si el nombre de las mallas contiene prefijo válido:")
#Comprobar que el prefijo sea el correcto:
check = []
mensaje_neg = "-> ERROR!, El nombre de las mallas NO cumple el formato de prefijos"
mensaje_pos = "-> BIEN!, El nombre de las mallas SI cumple el formato de prefijos"

#lista de prefijos:
prefix_mallas = ['MAF07-R1', 'MAF09-SE', 'MAF10-N', 'MAF11-W']

for m in range(0, len(data['MALLA'])):
    malla_contiene_prefijo = any(prefix_mallas in data['MALLA'][0] for prefix_mallas in prefix_mallas)
    check.append(malla_contiene_prefijo)
alerta(check)


# In[267]:


print('Revisando si existen mallas con sufijo "_vm":')
suffix = '_vm'
suffix_count = sum(1 for s in data['MALLA'] if s.endswith(suffix))
print ('-> Se han econtrado '+ str(suffix_count)+' mallas con sufijo "_vm"')


# In[268]:


#Identificador de Pozo en la malla de perforacion
print('Revisando identificador de pozo en la malla de perforación:')
id_pozo = pd.to_numeric(data['ID POZO'], errors='coerce')
print ('-> Existen '+ str(id_pozo.isna().sum()) + ' pozos que no podrán ser importador por ser AUX o vacio')


# In[276]:


print('Asegurando exactitud valores numericos:')
data['DIAMETRO PLG'] = np.around(list(map(float, data['DIAMETRO PLG'])),5)
data['GRAVILLA INTERMEDIO DISENO '] = np.around(list(map(float, data['GRAVILLA INTERMEDIO DISENO '])),5)
data['AIRE INTERMEDIO REAL '] = np.around(list(map(float, data['AIRE INTERMEDIO REAL '])),5)
data['TACO GRAVILLA REAL '] = np.around(list(map(float, data['TACO GRAVILLA REAL '])),5)
print( '... falta guardar archivo como .csv ...')
# data['DIAMETRO PLG']


# In[286]:


print ('Asegurando formato de valores ...')
print ('1. Asegurando columnas formato texto:')
data['MALLA'] = list(map(str, data['MALLA']))
data['CARGA FONDO DISENOlo '] = list(map(str, data['CARGA FONDO DISENOlo ']))
data['CARGA COLUMNA  DISENO'] = list(map(str, data['CARGA COLUMNA  DISENO']))
data['CARGA FONDO REAL '] = list(map(str, data['CARGA FONDO REAL ']))
data['CARGA COLUMNA REAL'] = list(map(str, data['CARGA COLUMNA REAL']))
print ('-> Formato texto asegurado')
print ('2. Asegurando columnas formato numero:')
# data['ID POZO'] = list(map(float, data['ID POZO']))
# data['DIAMETRO PLG'] = list(map(float, data['DIAMETRO PLG']))
data['KG FONDO DISENO '] = list(map(float, data['KG FONDO DISENO ']))
data['AIRE FONDO DISENO '] = list(map(float, data['AIRE FONDO DISENO ']))
data['KG COLUMNA DISENO'] = list(map(float, data['KG COLUMNA DISENO']))
data['AIRE FONDO DISENO '] = list(map(float, data['AIRE FONDO DISENO ']))
data['AIRE SUPERIOR DISENO'] = list(map(float, data['AIRE SUPERIOR DISENO']))
data['TACO GRAVILLA DISENO '] = list(map(float, data['TACO GRAVILLA DISENO ']))
data['SECUENCIA DETONACION DISENO'] = list(map(float, data['SECUENCIA DETONACION DISENO']))
data['PROFUNDIDAD REAL'] = list(map(float, data['PROFUNDIDAD REAL']))
data['KG FONDO REAL '] = list(map(float, data['KG FONDO REAL ']))
data['AIRE FONDO REAL '] = list(map(float, data['AIRE FONDO REAL ']))
data['KG COLUMNA REAL'] = list(map(float, data['KG COLUMNA REAL']))
data['AIRE SUPERIOR REAL'] = list(map(float, data['AIRE SUPERIOR REAL']))
data['SECUENCIA DETONACION REAL'] = list(map(float, data['SECUENCIA DETONACION REAL']))
data['AGUA'] = list(map(float, data['AGUA']))
print ('-> Formato numérico asegurado')


# In[306]:


print ('Comprobando información mínima de carga:')
print ('Existen '+ str(len(data['MALLA']))+' mallas válidas')
print ('Existen '+ str(len(data['ID POZO']))+' id_pozo válidos')
print ('Existen '+ str(len(data['DIAMETRO PLG']))+' diámetros PGL válidos')


# In[278]:


list(data.columns.values)


# In[307]:


#Nombre archivo
#Comprobar demas digitos de la MALLA
#Comprobar explosivo diseño y real


# In[ ]:




