#!/usr/bin/env python
# coding: utf-8

# ## Requerimientos

# In[1]:


import pandas as pd
import numpy as np
import re
import os
import sys
import time
import os
import glob


# ## Archivo y directorio

# In[52]:


os.path.abspath('')
path = os.path.abspath('')


# In[53]:


print('Abriendo carpeta: '+ path +' ...')


# In[54]:


timestr = time.strftime("%Y%m%d")
timestr = timestr 
# sys.stdout=open(timestr + ".txt","w")


# In[55]:


def alerta(list):
    #Si no hay ningun falso -> mensaje positivo
    if all(list): print (mensaje_pos)
    else: print (mensaje_neg)


# In[56]:


#with open('default_cols.txt', 'w') as f:
#    for col in list(data.columns.values):
#        f.write("%s\n" % col)


# Cargar archivo a comprobar:

# In[58]:


extension = 'csv'
os.chdir(path)
result = glob.glob('*.{}'.format(extension))
print(result)


# In[59]:


folder = 'Raw_data/'
file_name = '02.01.21 MAF7-R1-2750-03-05-B'
extension = '.csv'
final_name = folder+file_name+extension
print('Cargando el archivo '+final_name+'...')
data = pd.read_csv(folder+file_name+extension, header=0)
df = data.copy()


# ## Pre-procesamiento de columnas

# In[8]:


#Listado de columnas totales por defecto:
with open('default_cols.txt', 'r') as f:
    default_cols = [str(line.strip()) for line in f]
    
#Listado de columnas obligatorias y necesarias:    
with open('required_cols.txt', 'r') as f:
    required_cols = [str(line.strip()) for line in f]
    
default_cols[3] = default_cols[3].replace('CARGA FONDO DISENO', 'CARGA FONDO DISENO ')
default_cols[4] = default_cols[4].replace('KG FONDO DISENO', 'KG FONDO DISENO ')
default_cols[5] = default_cols[5].replace('AIRE FONDO DISENO', 'AIRE FONDO DISENO ')
default_cols[8] = default_cols[8].replace('AIRE INTERMEDIO DISENO', 'AIRE INTERMEDIO DISENO ')
default_cols[9] = default_cols[9].replace('GRAVILLA INTERMEDIO DISENO', 'GRAVILLA INTERMEDIO DISENO ')
default_cols[11] = default_cols[11].replace('TACO GRAVILLA DISENO', 'TACO GRAVILLA DISENO ')
default_cols[14] = default_cols[14].replace('CARGA FONDO REAL', 'CARGA FONDO REAL ')
default_cols[15] = default_cols[15].replace('KG FONDO REAL', 'KG FONDO REAL ')
default_cols[16] = default_cols[16].replace('AIRE FONDO REAL', 'AIRE FONDO REAL ')
default_cols[19] = default_cols[19].replace('AIRE INTERMEDIO REAL', 'AIRE INTERMEDIO REAL ')
default_cols[20] = default_cols[20].replace('GRAVILLA INTERMEDIO REAL', 'GRAVILLA INTERMEDIO REAL ')
default_cols[22] = default_cols[22].replace('TACO GRAVILLA REAL', 'TACO GRAVILLA REAL ')


# ## Tratamiento de explosivos

# ### Pre procesamiento explosivos

# In[9]:


required_cols = ['MALLA', 'ID POZO', 'DIAMETRO PLG']
#Fondo
fondo_diseno = ['CARGA FONDO DISENO ', 'KG FONDO DISENO ']
fondo_real = ['CARGA FONDO REAL ', 'KG FONDO REAL ']
#Diseno
columna_diseno = ['CARGA COLUMNA  DISENO', 'KG COLUMNA DISENO']
columna_real = ['CARGA COLUMNA REAL', 'KG COLUMNA REAL']


necessary_cols_in_csv = []

if set(required_cols) <= set(default_cols) and (
(set(fondo_diseno) <= set(default_cols) and set(fondo_real) <= set(default_cols)) or
(set(columna_diseno) <= set(default_cols) and set(columna_real) <= set(default_cols))    
): print ("El archivo SI contiene las columnas necesarias")
else: 
    print ("El archivo NO contiene las columnas necesarias")

#imprimir cols necesarias:
print('De las columnas obligatorias, el archivo: ')
if set(required_cols) <= set(default_cols): print ('Contiene: ' + ' '.join(required_cols))
else: print ('No contiene: ' + ''.join(required_cols))
    
if (set(fondo_diseno) <= set(default_cols) and set(fondo_real) <= set(default_cols)): print ('Contiene: ' + ' '.join(fondo_diseno) + ' '.join(fondo_real))
else: print ('No contiene: ' + ' '.join(fondo_diseno) + ' '.join(fondo_real))
    
if (set(columna_diseno) <= set(default_cols) and set(columna_real) <= set(default_cols)): print ('Contiene: ' + ' '.join(columna_diseno) + ' '.join(columna_real))
else: print ('No contiene: ' + ' '.join(columna_diseno) + ' '.join(columna_real))
    
    
#Crear lista de columnas necesarias que si tiene el archvo:
if set(required_cols) <= set(default_cols): necessary_cols_in_csv.extend(required_cols)
if (set(fondo_diseno) <= set(default_cols) and set(fondo_real) <= set(default_cols)): necessary_cols_in_csv.extend(fondo_diseno+fondo_real)
if (set(columna_diseno) <= set(default_cols) and set(columna_real) <= set(default_cols)): necessary_cols_in_csv.extend(columna_diseno+columna_real)


#Armar la lista de [valores required_cols] + [explisvo real] +  [explosivo planificado]


# ### Explosivo caso 1: Carga de Fondo

# Conservar solo las que son posibles de cargar con explosivos de fondo o mas

# In[10]:


fondo_cols = ['CARGA FONDO DISENO ','KG FONDO DISENO ','CARGA FONDO REAL ','KG FONDO REAL ']


# In[11]:


df_fondo_ready = df.dropna(subset=['CARGA FONDO DISENO ','KG FONDO DISENO ','CARGA FONDO REAL ','KG FONDO REAL '])
df_fondo_ready[fondo_cols].head(5)


# ### Explosivo caso 2: Carga de Columna

# Conservar solo las que son posibles de cargar con explosivos de columna o mas

# In[12]:


columna_cols = ['CARGA COLUMNA  DISENO','KG COLUMNA DISENO','CARGA COLUMNA REAL','KG COLUMNA REAL']


# In[13]:


df_columna_ready = df.dropna(subset=['CARGA COLUMNA  DISENO','KG COLUMNA DISENO','CARGA COLUMNA REAL','KG COLUMNA REAL'])
(df_columna_ready[columna_cols]).head(5)
# df_columna_ready.to_csv('columna' + ".csv", index=False)


# ### Explosivo caso 3: Carga de Fondo y Columna

# In[14]:


cols = fondo_cols+columna_cols
df_both_explosives = df.dropna(subset=['CARGA COLUMNA  DISENO',
                                       'KG COLUMNA DISENO',
                                       'CARGA COLUMNA REAL',
                                       'KG COLUMNA REAL',
                                       'CARGA FONDO DISENO ',
                                       'KG FONDO DISENO ',
                                       'CARGA FONDO REAL ',
                                       'KG FONDO REAL '])
df_both_explosives[cols].head(5)


# ### Consolidaci??n explosivos

# In[15]:


#Valido pero solo con fondo
df_only_fondo = pd.concat([df_fondo_ready,df_both_explosives]).drop_duplicates(keep=False)
#Valido pero solo con columna
df_only_columna = pd.concat([df_columna_ready,df_both_explosives]).drop_duplicates(keep=False)


# In[16]:


filtered_aux = pd.concat([df_only_columna,df_only_fondo])
filtered_df = pd.concat([filtered_aux,df_both_explosives])
# filtered_df.to_csv(timestr + ".csv", index=False)


# In[17]:


df_not_ready = pd.concat([df,filtered_df]).drop_duplicates(keep=False)
# df_not_ready = union[union.isnull().any(axis=1)]
# not_ready_name = "NoParaCargar" + timestr
# df_not_ready.to_csv(not_ready_name + ".csv", index=False)


# In[18]:


# df_len = int(len(df))
# filtered_len = int(len(filtered_df))
# outer_len = int(len(df_not_ready))
# print(df_len)
# print(filtered_len)
# print(outer_len)


# Comprobar si el archivo contiene el n??mero total de columnas que podr??a tener:

# ## Tratamiento de Mallas

# In[19]:


df = filtered_df.copy()
df['MALLA']


# In[20]:


print("Comprobando si el nombre de las mallas contiene prefijo v??lido:")
#Comprobar que el prefijo sea el correcto:
check = []
mensaje_neg = "-> ERROR!, El nombre de las mallas NO cumple el formato de prefijos"
mensaje_pos = "-> BIEN!, El nombre de las mallas SI cumple el formato de prefijos"

#lista de prefijos:
# prefix_mallas = ['MAF07-R1', 'MAF09-SE', 'MAF10-N', 'MAF11-W', 'MAF9-SE','MAF7']

# for m in range(0, len(df['MALLA'])):
#     malla_contiene_prefijo = any(prefix_mallas in df['MALLA'][0] for prefix_mallas in prefix_mallas)
#     check.append(malla_contiene_prefijo)
# alerta(check)


# In[21]:


print('Revisando si existen mallas con sufijo "_vm":')
suffix = '_vm'
suffix_count = sum(1 for s in df['MALLA'] if s.endswith(suffix))
print ('-> Se han econtrado '+ str(suffix_count)+' mallas con sufijo "_vm"')


# ## Tratamiento de pozos

# In[22]:


#Identificador de Pozo en la malla de perforacion
print('Revisando identificador de pozo en la malla de perforaci??n:')
id_pozo = pd.to_numeric(df['ID POZO'], errors='coerce')
print ('-> Existen '+ str(id_pozo.isna().sum()) + ' pozos que no podr??n ser importador por ser AUX o vacio')


# In[23]:


df_id_pozo = df.dropna(subset=['ID POZO'])
df_id_pozo['ID POZO'] = list(map(str, df_id_pozo['ID POZO']))
# df_id_pozo = df[~df['ID POZO'].contains("AUX")]
# df_id_pozo['ID POZO']


# In[24]:


df_id_pozo['ID POZO']


# ## Formato de valores 

# In[25]:


df = df_id_pozo.copy()


# In[26]:


print('Asegurando exactitud valores numericos:')
df['DIAMETRO PLG'] = np.around(list(map(float, df['DIAMETRO PLG'])),5)
df['GRAVILLA INTERMEDIO DISENO '] = np.around(list(map(float, df['GRAVILLA INTERMEDIO DISENO '])),5)
df['AIRE INTERMEDIO REAL '] = np.around(list(map(float, df['AIRE INTERMEDIO REAL '])),5)
df['TACO GRAVILLA REAL '] = np.around(list(map(float, df['TACO GRAVILLA REAL '])),5)
# data['DIAMETRO PLG']


# In[27]:


print ('Asegurando formato de valores ...')
print ('1. Asegurando columnas formato texto:')
df['MALLA'] = list(map(str, df['MALLA']))
df['CARGA FONDO DISENOlo '] = list(map(str, df['CARGA FONDO DISENO ']))
df['CARGA COLUMNA  DISENO'] = list(map(str, df['CARGA COLUMNA  DISENO']))
df['CARGA FONDO REAL '] = list(map(str, df['CARGA FONDO REAL ']))
df['CARGA COLUMNA REAL'] = list(map(str, df['CARGA COLUMNA REAL']))
print ('-> Formato texto asegurado')
print ('2. Asegurando columnas formato numero:')
# df['ID POZO'] = list(map(float, df['ID POZO']))
# df['DIAMETRO PLG'] = list(map(float, df['DIAMETRO PLG']))
df['KG FONDO DISENO '] = list(map(float, df['KG FONDO DISENO ']))
df['AIRE FONDO DISENO '] = list(map(float, df['AIRE FONDO DISENO ']))
df['KG COLUMNA DISENO'] = list(map(float, df['KG COLUMNA DISENO']))
df['AIRE FONDO DISENO '] = list(map(float, df['AIRE FONDO DISENO ']))
df['AIRE SUPERIOR DISENO'] = list(map(float, df['AIRE SUPERIOR DISENO']))
df['TACO GRAVILLA DISENO '] = list(map(float, df['TACO GRAVILLA DISENO ']))
df['SECUENCIA DETONACION DISENO'] = list(map(float, df['SECUENCIA DETONACION DISENO']))
df['PROFUNDIDAD REAL'] = list(map(float, df['PROFUNDIDAD REAL']))
df['KG FONDO REAL '] = list(map(float, df['KG FONDO REAL ']))
df['AIRE FONDO REAL '] = list(map(float, df['AIRE FONDO REAL ']))
df['KG COLUMNA REAL'] = list(map(float, df['KG COLUMNA REAL']))
df['AIRE SUPERIOR REAL'] = list(map(float, df['AIRE SUPERIOR REAL']))
df['SECUENCIA DETONACION REAL'] = list(map(float, df['SECUENCIA DETONACION REAL']))
df['AGUA'] = list(map(float, df['AGUA']))
print ('-> Formato num??rico asegurado')


# In[28]:


print ('Comprobando informaci??n m??nima de carga:')
print ('Existen '+ str(len(df['MALLA']))+' mallas v??lidas')
print ('Existen '+ str(len(df['ID POZO']))+' id_pozo v??lidos')
print ('Existen '+ str(len(df['DIAMETRO PLG']))+' di??metros PGL v??lidos')


# ## Exportaci??n

# In[45]:


from pathlib import Path


# In[46]:


Path(file_name).mkdir(parents=True, exist_ok=True)


# In[47]:


export_dir = file_name+"/"


# In[48]:


export_dir+export_name


# In[49]:


export_name = 'Valid-' + file_name
df.to_csv(export_dir+export_name + ".csv", index=False)
print ('Archivo v??lido exportado: ' + export_name)


# In[50]:


not_ready_name = "Invalid-" + file_name
df_not_ready.to_csv(export_dir+not_ready_name + ".csv", index=False)
print ('Archivo NO v??lido exportado: ' + not_ready_name)


# In[60]:


sys.stdout.close()


# In[62]:


# !jupyter nbconvert --to script script.ipynb


# In[ ]:




