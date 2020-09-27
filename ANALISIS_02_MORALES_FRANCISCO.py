# -*- coding: utf-8 -*-

import csv
import os   
import operator
    
    
diccionario_global=[]
with open("synergy_logistics_database.csv", "r") as archivo:
    lector = csv.DictReader(archivo)
    
    for linea in lector:
        diccionario_global.append(linea)
    
    # ï»¿register_id, direction, origin, destination, company_name, date, year, 
    # product, transport_mode, total_value


#Funciones********************************************************

#Función para obtener las rutas
def rutas(diccionario, llave_principal, llave_secundaria):
    lista = []
    for linea in diccionario:
        ruta = linea[llave_principal] + "-" + linea[llave_secundaria] 
        if ruta not in lista:
            lista.append(ruta)
            
    ceros = [0]*len(lista)
    ruta_suma = dict(zip(lista, ceros))
    ruta_contador = dict(zip(lista, ceros))
    for linea in diccionario:
        ruta_temp = linea[llave_principal] + "-" + linea[llave_secundaria]
        ruta_contador[ruta_temp] += 1 #int(linea["total_value"])
        ruta_suma[ruta_temp] += int(linea["total_value"])
    return ruta_suma,ruta_contador

#Función para obtener los valores distintos
def lista_distintos(diccionario, llave):
    lista_distintos = []
    
    for linea in diccionario:
        if linea[ llave ] not in lista_distintos:
            lista_distintos.append(linea[ llave ])
    return lista_distintos

#Funcion para filtrar el diccionario general
def filtro(diccionario, llave, valor):
    diccionario_filtrado = []
    for linea in diccionario:
        if linea[llave] == valor:
            diccionario_filtrado.append(linea)
    return diccionario_filtrado

#Funcion para sumar campos de una lista
def suma(lista, diccionario, llave):
    ceros = [0]*len(lista)
    suma = dict(zip(lista, ceros))
    for linea in diccionario:
        suma[linea[llave]] += int(linea["total_value"])
    return suma

#Funcion que cuenta los campos de una lista
def contador(lista, diccionario, llave):
    ceros = [0]*len(lista)
    contador = dict(zip(lista, ceros))
    for linea in diccionario:
        contador[linea[llave]] += 1
    return contador 

#Funcion porcentaje
def porcentaje(lista, total):
    porcentaje_exp = []
    for linea in lista:
        promedio = list(linea)
        promedio.append((int(promedio[1]) / total) * 100)
        porcentaje_exp.append(promedio)
    return porcentaje_exp
        
    
        
        
opcion = 1
while opcion != 0: 
    os.system("cls")
    #print(os.name)
    print("Bienvenido. Presione: \n 1--Para análisis por rutas \n 2--Para análisis por transporte \n 3--Para análisis por país \n 0--Para salir")
    opcion = str(input("Seleccione una opción a analizar:"))
    
    #************Analisis de rutas***************
    if opcion == "1":
        os.system("cls")
        print("\nAnálisis de rutas:")
        
        #Exportaciones
        lista_exportacion = filtro(diccionario_global, "direction", "Exports")
        totales_rutas_exp, rutas_exp = rutas(lista_exportacion, "origin", "destination")
        suma_rutas_exp = sorted(rutas_exp.items(), key=operator.itemgetter(1), reverse=True)
            
        print("\nExportaciones\nLas 10 rutas principales son:\n")
        i = 0
        operaciones_ruta_exp = 0
        total_ruta_exp = 0
        for elemento in suma_rutas_exp:
            if i < 10:
                print(f"\t{i+1}.- '{elemento[0]}' empleada {elemento[1]} veces con ganancia de ${totales_rutas_exp[elemento[0]]}")
                total_ruta_exp += totales_rutas_exp[elemento[0]]
                operaciones_ruta_exp += elemento[1]
            i +=1
        print(f"\n El rendimiento general para exportaciones en las 10 rutas principales es:\n  En {operaciones_ruta_exp} se tuvo una ganancia de ${total_ruta_exp}")
        
        #Importaciones
        lista_importacion = filtro(diccionario_global, "direction", "Imports")
        totales_rutas_imp, rutas_imp = rutas(lista_importacion, "destination", "origin")
        suma_rutas_imp = sorted(rutas_imp.items(), key=operator.itemgetter(1), reverse=True)

        print("\nImportaciones\nLas 10 rutas principales son:\n")
        i = 0
        operaciones_ruta_imp = 0
        total_ruta_imp = 0
        for elemento in suma_rutas_imp:
            if i < 10:
                print(f"\t{i+1}.- '{elemento[0]}' empleada {elemento[1]} veces con ganancia de ${totales_rutas_imp[elemento[0]]}")
                total_ruta_imp += totales_rutas_imp[elemento[0]]
                operaciones_ruta_imp += elemento[1]
            i +=1
        print(f"\n El rendimiento general para importaciones en las 10 rutas principales es:\n  En {operaciones_ruta_imp} se tuvo una ganancia de ${total_ruta_imp}")


        
        
        regresar= input("\nPresione cualquier tecla para regresar")
    
    #************Analisis de transporte***************
    elif opcion == "2":
        os.system("cls")
        print("\nAnálisis de transporte")
        
        #Exportaciones
        lista_exportacion = filtro(diccionario_global, "direction", "Exports")        
        transportes_exp = lista_distintos(lista_exportacion, "transport_mode") 
        sum_exp =suma(transportes_exp, lista_exportacion, "transport_mode")
        suma_transportes_exp = sorted(sum_exp.items(), key=operator.itemgetter(1), reverse=True)
        contador_transportes_exp = contador(transportes_exp, lista_exportacion, "transport_mode")
        
        print("\nExportaciones\nLas 3 rutas principales son:")
        i = 0
        operaciones_transporte_exp = 0
        total__transporte_exp = 0
        for elemento in suma_transportes_exp:
            if i < 3:
                print(f"\t{i+1}.- '{elemento[0]}' con {contador_transportes_exp[elemento[0]]} exportaciones y ganancia de: ${elemento[1]}")
                operaciones_transporte_exp += contador_transportes_exp[elemento[0]]
                total__transporte_exp += elemento[1]
            i +=1
        print(f"\n El rendimiento general para exportaciones por país es:\n  En {operaciones_transporte_exp} se tuvo una ganancia de ${total__transporte_exp}")
        
        
        #Importaciones
        lista_importacion = filtro(diccionario_global, "direction", "Imports")
        transportes_imp = lista_distintos(lista_importacion, "transport_mode") 
        sum_imp = suma(transportes_imp, lista_importacion, "transport_mode")
        suma_transportes_imp =  sorted(sum_imp.items(), key=operator.itemgetter(1), reverse=True)
        contador_transportes_imp = contador(transportes_imp, lista_importacion, "transport_mode")
        
        print("\nImportaciones\nLas 3 rutas principales son:")
        i = 0
        operaciones_transporte_imp = 0
        total__transporte_imp = 0
        for elemento in suma_transportes_imp:
            if i < 3:
                print(f"\t{i+1}.- '{elemento[0]}' con {contador_transportes_imp[elemento[0]]} importaciones y una ganancia de: ${elemento[1]}")        
                operaciones_transporte_imp += contador_transportes_imp[elemento[0]]
                total__transporte_imp += elemento[1]
            i += 1
        print(f"\n El rendimiento general para importaciones por país es:\n  En {operaciones_transporte_imp} se tuvo una ganancia de ${total__transporte_imp}")

        regresar= input("\nPresione cualquier tecla para regresar")
        
        
    #************Analisis por país***************
    elif opcion == "3":
        os.system("cls")
        print("\nAnálisis por país")
        
        #Exportaciones
        lista_exportacion = filtro(diccionario_global, "direction", "Exports")
        paises_exp = lista_distintos(lista_exportacion, "origin")
        
        total_exp = 0
        count_exo = 0
        for linea in lista_exportacion:
            total_exp += int(linea["total_value"])
            count_exo += 1
        #print(total_exp)
        #print(count_exo)
        
        sum_pais_exp =suma(paises_exp, lista_exportacion, "origin")
        suma_paises_exp = sorted(sum_pais_exp.items(), key=operator.itemgetter(1), reverse=True)
        porcentaje_exp = porcentaje(suma_paises_exp, total_exp)
        contador_paises_exp = contador(paises_exp, lista_exportacion, "origin")
        
        print("Exportaciones \n Los paises que tienen el 80% de las exportaciones son:\n")
        porcentaje80 = 0
        operaciones_paises_exp = 0
        total__paises_exp = 0
        for linea in porcentaje_exp:
            porcentaje80 += linea[2]
            if porcentaje80 < 80 :
                print(f"\t '{linea[0]}' generó en {contador_paises_exp[linea[0]]} operaciones el {round(linea[2],2)} %")
                operaciones_paises_exp += contador_paises_exp[linea[0]]
                total__paises_exp += sum_pais_exp[linea[0]]
        print(f"\n El rendimiento general para exportaciones por país es:\n  En {operaciones_paises_exp} se tuvo una ganancia de ${total__paises_exp}")

        
        #Importaciones
        lista_importacion = filtro(diccionario_global, "direction", "Imports")
        paises_imp = lista_distintos(lista_importacion, "destination") 
        
        total_imp = 0
        count_imp = 0
        for linea in lista_importacion:
            total_imp += int(linea["total_value"])
            count_imp += 1
        #print(total_imp)
        #print(count_imp)
        
        sum_pais_imp = suma(paises_imp, lista_importacion, "destination")
        suma_paises_imp =  sorted(sum_pais_imp.items(), key=operator.itemgetter(1), reverse=True)
        porcentaje_imp = porcentaje(suma_paises_imp, total_imp)
        contador_paises_imp = contador(paises_imp, lista_importacion, "destination")
        
        print("\nImportaciones \n Los paises que tienen el 80% de las importaciones son: \n")
        porcentaje80 = 0
        operaciones_paises_imp = 0
        total__paises_imp = 0
        for linea in porcentaje_imp:
            porcentaje80 += linea[2]
            if porcentaje80 < 80 :
                print(f"\t '{linea[0]}' generó el {round(linea[2],2)} %")
                operaciones_paises_imp += contador_paises_imp[linea[0]]
                total__paises_imp += sum_pais_imp[linea[0]]
        print(f"\n El rendimiento general para importaciones por país es:\n  En {operaciones_paises_imp} se tuvo una ganancia de ${total__paises_imp}")
        
        
        regresar= input("\nPresione cualquier tecla para regresar")
        
        
    elif opcion == "0":
        os.system("cls")
        opcion = 0
    else:
        os.system("cls")
        print("Opcion inválida")

print("Final del ciclo")




    
    