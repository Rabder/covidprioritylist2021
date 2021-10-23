# -*- coding: utf-8 -*-
"""
Created on Wed May 12 17:14:10 2021

@author: rabde
"""


import pandas as pd
import seaborn as sns
import collections
import matplotlib.pyplot as plt
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
import spacy
nlp = spacy.load('es_core_news_sm')
spacy_stopwords = spacy.lang.es.stop_words.STOP_WORDS
import warnings
import sys
warnings.filterwarnings('ignore')
import re
from tqdm import tqdm, trange
import time
import csv
import math

casos = []
centros_vacunacion = []
centros_avancebajo = []
niveles_clasificados = []

dataset_casos = pd.read_csv(r'C:/Users/rabde/OneDrive/Documents/datos/positivos_covid.csv',encoding = 'utf8')
dataset_muertos = pd.read_csv(r'C:/Users/rabde/OneDrive/Documents/datos/fallecidos_covid.csv', encoding='ANSI')
dataset_vacunacion = pd.read_csv(r'C:/Users/rabde/OneDrive/Documents/datos/vacunados_minsa.csv', encoding='utf8')
dataset_poblacion = pd.read_csv(r'C:/Users/rabde/OneDrive/Documents/datos/dpto.csv', encoding='utf8')
dataset_camas = pd.read_csv(r'C:/Users/rabde/OneDrive/Documents/datos/Camas (1).csv', encoding='utf8')
dataset_65 = pd.read_csv(r'C:/Users/rabde/OneDrive/Documents/datos/pob65.csv', encoding='utf8')

dataset_centros = pd.read_csv(r'C:/Users/rabde/OneDrive/Documents/datos/IPRESS.csv', encoding='utf8')

# Conteo de casos por departamentos
what1 = dataset_muertos['DEPARTAMENTO'].value_counts()
what = dataset_casos['DEPARTAMENTO'].value_counts()
what3_u = dataset_vacunacion['Departamento'].value_counts()
what3_nivel = dataset_vacunacion['CategoriaNivel1'].value_counts()
what3_meta = dataset_vacunacion['Meta']
what3_logrados = dataset_vacunacion['Vacunados']
what_totalpob = dataset_poblacion['POBLACION']
what_nombres = dataset_poblacion['DPTO']

camas_disponibles = dataset_camas["CAMAS_ZC_DISPONIBLES"]
camas_total = dataset_camas["CAMAS_ZC_TOTAL"]

camas_no = camas_disponibles.value_counts()
camas_si = camas_total.value_counts()

i = 0

for j in camas_si.keys():
    i += int(j)
camas_totaln = i

i = 0
for j in camas_no.keys():
    i += int(j)
camas_dispn = i

camas_prom = camas_totaln / camas_dispn

print()




centros_tot_nacional = 23390
pob_nacional = 33035304
centros_prom = pob_nacional / centros_tot_nacional


for key in what.keys():
    casos_regiones = {"nombre": key, "casos": what[key]}
    nombre = {"nombre": key}
    casos.append(casos_regiones)


# Conteo de fallecidos por departamentos
for key in what1.keys():
    i = 0
    while True:
        if what[key] == what[what.keys()[i]]:
            casos[i]["muertos"] = what1[key]
            break
        else:
            i += 1





# Conteo de poblacion:
with open('C:/Users/rabde/OneDrive/Documents/datos/dpto.csv', "r") as data_file:
    reader = csv.reader(data_file)
    next(reader)
    for row in reader:
        i = 0
        tdict = {"nombre": row[0], "poblacion": int(row[1])}
        for key in what1.keys():
            j = 0
            while True:
                if j > 26:
                    break
                if row[0] == casos[j]['nombre']:
                    casos[j]["poblacion_total"] = int(row[1])
                    break
                else:
                    j += 1


# Conteo de centros de vacunación y clasificación por niveles
with open('C:/Users/rabde/OneDrive/Documents/datos/vacunados_minsa.csv', "r", encoding='utf8') as data_file1:
    reader1 = csv.reader(data_file1)
    next(reader1)
    for row in reader1:
        i = 0
        tdict = {'departamento': row[8], 'provincia': row[9], 'nivel': row[11], 'meta': int(row[13]),
                 'vacunados': int(row[14]), 'porcentaje': float(row[18])}
        centros_vacunacion.append(tdict)


#Separar aquellos centros en donde el avance sea menor al 50%
for center in centros_vacunacion:
    if center['porcentaje'] < 50.0:
        centros_avancebajo.append(center)


#Preparar la lista de niveles clasificados
i = 0
for names in what_nombres:
    niveles_clasificados.append({"departamento": "", "nivel_I": 0, "nivel_II": 0, "nivel_III": 0})
    niveles_clasificados[i]["departamento"] = names
    i += 1


# Clasificacion de niveles
for part in centros_vacunacion:
    for i in range(25):
        if part['departamento'] == niveles_clasificados[i]["departamento"]:
            if part['nivel'] == 'NIVEL I':
                niveles_clasificados[i]["nivel_I"] += 1
            elif  part['nivel'] == 'NIVEL II':
                niveles_clasificados[i]["nivel_II"] += 1
            elif part['nivel'] == 'NIVEL III':
                niveles_clasificados[i]["nivel_III"] += 1


# Tabla definitiva (dpto, poblacion, casos, muertos, centros_vacunacion (niveles),
#                   vacunados, meta, porcentaje_meta, vacunados_relacion_poblacion)

final = []

for dep in what_nombres:
    print(dep)

# DPTO, POBLACION, MUERTOS y CASOS TOTALES
for dep in what_nombres:
    dict_final = {"departamento": "", "casos": 0, "muertos": 0, "poblacion": 0, "centro_nivel1": 0, "centro_nivel2": 0, "centro_nivel3": 0, "vacunados": 0, "meta": 0}
    dict_final['departamento'] = dep
    for i in range(26):
        if casos[i]['nombre'] == dep:
            dict_final['casos'] = casos[i]['casos']
            dict_final["poblacion"] = casos[i]['poblacion_total']
            dict_final["muertos"] = casos[i]['muertos']
    final.append(dict_final)

centros = 0

for i in centros_vacunacion:
    centros += 1


# META Y VACUNADOS TOTALES

for wh in final:
    for dep in centros_vacunacion:
        if wh['departamento'] == dep['departamento']:
            wh['meta'] += dep['meta']
            wh['vacunados'] += dep['vacunados']
    wh['porcentaje'] = round((int(wh['vacunados']) / int(wh['meta'])) * 100.0, 2)


# NIVEL DE CENTROS
for i in range(len(final)):
    for dep in niveles_clasificados:
        if final[i]['departamento'] == dep['departamento']:
            final[i]['centro_nivel1'] = dep['nivel_I']
            final[i]['centro_nivel2'] = dep['nivel_II']
            final[i]['centro_nivel3'] = dep['nivel_III']

centros_dep = dataset_centros["Departamento"].value_counts()
newcentro = dict(centros_dep)
items = newcentro.items()
finalcentro = sorted(items)


for dep in final:
    for j in range(len(finalcentro)):
        if dep["departamento"] == finalcentro[j][0]:
            dep["centros_total"] = finalcentro[j][1]
            break


comorbilidad = [30.2, 34.9, 25.0, 39.0, 27.7, 27.4, 44.3, 31.3, 22.8, 28.1, 44.3, 26.4, 35.8, 36.0, 41.6, 35.4, 43.3, 43.8, 28.0, 38.7, 30.5, 33.9, 46.1, 42.0, 33.3]
i = 0
while i < 25:
    final[i]["camas_disp"] = camas_disponibles[i]
    final[i]["camas_total"] = camas_total[i]
    final[i]["comorbi"] = comorbilidad[i]
    final[i]["pob_65"] = dataset_65[" POBLACION"][i]
    i += 1

def div_zero(x, y):
    if x > 0 and y > 0:
        return x / y
    else:
        return 0




rank = []
# Algoritmo para priorizar
for dep in final:
    tdict = {"name": dep["departamento"], "score": 0, "cases": 0, "deaths/cases": 0, "comorbidity": 0, "icus": 0, "medcenters": 0}

    ratio = div_zero(float(dep["casos"]), float(dep["poblacion"]))
    tdict["cases"] = round(ratio*100, 2)
    ratio1 = div_zero(float(dep["muertos"]), float(dep["casos"]))
    tdict["deaths/cases"] = round(ratio1*100, 2)


    vac = div_zero(float(dep["vacunados"]), float(dep["pob_65"]))
    tdict["vacunados/pob65"] = round(vac*100, 2)

    centros = float(dep["centro_nivel1"]) + float(dep["centro_nivel2"]) + float(dep["centro_nivel3"])

    camas = div_zero(float(dep["camas_total"]), float(dep["camas_disp"]))


    if dep["camas_disp"] == 0:
        camas = (div_zero(dep["camas_total"], 1))

    cam = round(camas / camas_prom, 2)

    tdict["icu"] = cam

    #casos_pob es el porcentaje de la población con covid 19
    casos_pob = round(ratio*100, 2)

    #muertes_casos es el porcentaje de muertes por covid 19
    muertes_casos = round(ratio1*100, 2)

    #vac_pob es la relación entre vacunados y adultos mayores
    vac_pob65 = round(vac*100,2)

    # pob65: Porcentaje de adultos mayores de 65 años en el departamento
    pob65 = (dep["pob_65"]/dep["poblacion"]) * 100

    com = dep["comorbi"] / 10
    tdict["comorbidity"] = round(com*10, 2)



    # Centros por toda la población mayor a 65 años
    centros_pob  = ((dep["poblacion"]/dep["centros_total"]))

    centross = round(centros_pob / centros_prom, 2)
    tdict["medcenters"] = centross


    # Total de constantes 100.
    punt = ((casos_pob*10) + (muertes_casos*25) + (pob65*10) + (com*20) + (cam*5) + (centross*30))/100
    new_punt = round(punt*20, 2)
    tdict["score"] = new_punt
    rank.append(tdict)

newlist = sorted(rank, key=lambda k: k['score'])
for fin in reversed(newlist):
    print(fin)



keys = newlist[0].keys()

resultado = open("lista_final.csv", "w")
writer = csv.DictWriter(resultado, keys)
writer.writeheader()
writer.writerows(newlist)
resultado.close()


