"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
from tabulate import tabulate
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT.graph import gr
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
assert cf
import time


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("0- Cargar información en el catálogo")
    print("1- : Encontrar puntos de interconexión aérea")
    print("2- : Encontrar clústeres de tráfico aéreo")
    print("3- : Encontrar la ruta más corta entre ciudades")
    print("4- : Utilizar las millas de viajero")
    print("5- : Cuantificar el efecto de un aeropuerto cerrado")
    print("6- : Comparar con servicio WEB externo")
    print("7- : Visualizar gráficamente los requerimientos")
catalog = None

def option0():
    print("Cargando información de los archivos ....")
    start_time = time.process_time()

    catalog = controller.initCatalog() # Inicializador del catálogo
    controller.loadData(catalog) # Carga de datos en el catálogo

    stop_time = time.process_time()
    elapsed_time_mseg = (stop_time - start_time)
    print('La carga demoró', elapsed_time_mseg, 'segundos')
    return catalog
"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 0:
        catalog = option0()
        numVertex = gr.numVertices(catalog['directedAirports'])
        numEdges= gr.numEdges(catalog['directedAirports'])
        print()
        print('En el grafo dirigido "directedAirports" de aeropuertos y las rutas entre aeropuertos hay',
         numVertex, 'aeropuertos y', numEdges, 'rutas.' )
        print()
        numVertex = gr.numVertices(catalog['notDirectedAirports'])
        numEdges= gr.numEdges(catalog['notDirectedAirports'])
        print()
        print('En el grafo dirigido "notDirectedAirports" de aeropuertos y las rutas no dirigidas entre aeropuertos hay',
         numVertex, 'aeropuertos y', numEdges, 'rutas.' )
        print()
        print('Hay', mp.size(catalog['cities']), 'nombres de ciudades registrados')
        aeropuerto = me.getValue(mp.get(catalog['IATAS'], 'GKA'))
        print('El primer aeropuerto cargado es el aeropuerto ' + aeropuerto['name'] + ' de la ciudad ' + aeropuerto['city'] 
        + ' del país ' + aeropuerto['country'] + ' y tiene latitid y longitud ' + aeropuerto['latitude'] + ',' 
        + aeropuerto['longitude'] + ' respectivamente.')
        print()
        city = lt.getElement(me.getValue(mp.get(catalog['cities'], 'Nordvik')), 1)
        print('La última ciudad cargada es Nordvik y tiene un población de ' + city['population'] + ' y tiene latitid y longitud ' + aeropuerto['latitude'] + ',' 
        + city['longitude'] + ' respectivamente.')

    elif int(inputs[0]) == 1:

        tabla1 = [['Iata', 'Conexiones', 'Nombre','Ciudad','País']]
        tabla2 = [['Iata', 'Conexiones', 'Nombre','Ciudad','País']]
        interconnected_airports = catalog['connected_airports']
        airports_directed = interconnected_airports[0]
        airports_no_directed = interconnected_airports[1]
        airports_map = catalog['IATAS']
        for key in  airports_directed:
            airport = me.getValue(mp.get(airports_map, key))
            line = [key, airports_directed[key], airport['name'], airport['city'], airport['country'] ]
            tabla1.append(line)
        for key in  airports_no_directed:
            airport = me.getValue(mp.get(airports_map, key))
            line = [key, airports_no_directed[key], airport['name'], airport['city'], airport['country'] ]
            tabla2.append(line)
        
        print('Los 10 aereopuertos que son los mayores puntos de interconexión aerea (grafo dirigido) son:')
        print(tabulate(tabla1 , headers='firstrow', tablefmt='fancy_grid'))
        print('Los 10 aereopuertos que son los mayores puntos de interconexión aerea (grafo no dirigido) son:')
        print(tabulate(tabla2 , headers='firstrow', tablefmt='fancy_grid'))


    elif int(inputs[0]) == 2:
        pass
    elif int(inputs[0]) == 3:
        origin = input('Por favor ingrese el nombre de la ciudad de origen: ')
        origin_data = controller.defineCity(catalog, origin)
        if origin_data == None:
            print('La ciudad ingresada no registra')
            pass
        destination = input('Por favor ingrese el nombre de la ciudad de destino: ')
        destination_data = controller.defineCity(catalog, destination)
        if destination_data == None:
            print('La ciudad ingresada no registra')
            pass

        pass

    
    elif int(inputs[0]) == 4:
        pass
    elif int(inputs[0]) == 5:
        pass
    elif int(inputs[0]) == 6:
        pass
    elif int(inputs[0]) == 7:
        pass

    else:
        sys.exit(0)
sys.exit(0)
