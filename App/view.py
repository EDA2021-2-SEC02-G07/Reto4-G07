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
from DISClib.ADT import stack
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import prim
assert cf
import time
default_limit = 1000
sys.setrecursionlimit(default_limit*10)

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
        

    elif int(inputs[0]) == 1:
        print('=============== Req 1. answer ===============')
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
        try:
            graph = catalog['directedAirports']
            comps = catalog['SCC']
            print('=============== Req 2. inputs ===============')
            a1 = input('Inserte el código IATA del aeropuerto 1: ')
            a2 = input('Inserte el código IATA del aeropuerto 2: ')
            print()
            print('=============== Req 2. answer ===============')
            conected = scc.stronglyConnected(comps, a1, a2)
            print('Número de componentes fuertemente conectados:', scc.connectedComponents(comps))
            print('¿Están el aeropuerto con código "' + a1 + '" y el aeropuerto con código "' + a2 + '" fuertemente conectados?:', conected)
        except:
            print('Inserte valores válidos compa.') #XD



    elif int(inputs[0]) == 3:
        print('=============== Req 3. inputs ===============')
        origin = input('Por favor ingrese el nombre de la ciudad de origen: ')
        origin_data = controller.defineCity(catalog, origin)
        if origin_data == None:
            print('La ciudad ingresada no registra')
            continue
        destination = input('Por favor ingrese el nombre de la ciudad de destino: ')
        destination_data = controller.defineCity(catalog, destination)
        if destination_data == None:
            print('La ciudad ingresada no registra')
            continue

        
        origin_airport = controller.near_airport(catalog, origin_data)
        destination_airport = controller.near_airport(catalog, destination_data)
        origin_dist = origin_airport[1]
        destination_dist = destination_airport[1]
        origin_airport = origin_airport[0]
        destination_airport = destination_airport[0]
        path = controller.minimumCostRoute(catalog, origin_airport, destination_airport)
        if path == None:
            print('No hay ruta entre las dos ciudades seleccionadas')
            continue



        table1 = [['IATA', 'Nombre', 'País', 'Ciudad']]
        origin_airport_info = me.getValue(mp.get(catalog['IATAS'], origin_airport))
        table1.append([origin_airport, origin_airport_info['name'],origin_airport_info['country'],origin_airport_info['city']])
        table2 = [['IATA', 'Nombre', 'País', 'Ciudad']]
        destination_airport_info = me.getValue(mp.get(catalog['IATAS'], destination_airport))
        table2.append([destination_airport, destination_airport_info['name'],destination_airport_info['country'],destination_airport_info['city']])        
        table3 = [['Origen', 'Destino', 'Distancia (km)']]
        table4 = [['IATA', 'Nombre', 'País', 'Ciudad']]
        aereopuertos = []
        distance = origin_dist+destination_dist
        while (not stack.isEmpty(path)):
            triproute = stack.pop(path)
            table3.append([triproute['vertexA'], triproute['vertexB'],triproute['weight']])
            aereopuertos.append(triproute['vertexA'])
            aereopuertos.append(triproute['vertexB'])
            distance += float(triproute['weight'])
        result = []
        for aereopuerto in aereopuertos:
            if aereopuerto not in result:
                result.append(aereopuerto)
        for iata in result:
            airport_info = me.getValue(mp.get(catalog['IATAS'], iata))
            table4.append([iata, airport_info['name'],airport_info['country'],airport_info['city']])
                
        print('=============== Req 2. answer ===============')
        print('El viaje cubre una distancia de:', round(distance,3), 'Km' )
        print('Para ir desde', origin, 'hasta', destination, 'se debe trasladar desde el aereopuerto:')
        print(tabulate(table1 , headers='firstrow', tablefmt='fancy_grid'))

        print('Hasta el aereopuerto:')
        print(tabulate(table2 , headers='firstrow', tablefmt='fancy_grid'))

        print('Los trayectos que debe seguir son: ')
        print(tabulate(table3 , headers='firstrow', tablefmt='fancy_grid'))

        print('En la tabla se brinda información de las paradas: ')
        print(tabulate(table4 , headers='firstrow', tablefmt='fancy_grid'))
        


        
    
    elif int(inputs[0]) == 4:
        pass
    elif int(inputs[0]) == 5: 
        Iatacode = input('Ingrese el código IATA del aereopuerto que está cerrado: ')
        data = controller.affected_airports(catalog, Iatacode)
        affected_airports = []
        list1 = data[0]
        list2 = data[1]
        for i in range(1,lt.size(list1)+1):
            airport = lt.getElement(list1, i)
            affected_airports.append(airport)
        for i in range(1, lt.size(list2)+1):
            airport = lt.getElement(list2, i)
            affected_airports.append(airport)
        result = []
        for airport in affected_airports:
            if airport not in result:
                result.append(airport)
        print('El cierre afecta a', len(result), 'aereopuerto(s)')
        if len(result) <= 6:
            pass
        else: 
            result = result[0:3]+result[len(result)-4:]
        
        tablita = [['IATA', 'Nombre', 'País', 'Ciudad']]
        for iata in result:
            airport_info = me.getValue(mp.get(catalog['IATAS'], iata))
            tablita.append([iata, airport_info['name'],airport_info['country'],airport_info['city']])
        
        print('Los primeros 3 y los últimos 3 aereopuertos afectados son: ')
        print(tabulate(tablita , headers='firstrow', tablefmt='fancy_grid'))
        
    elif int(inputs[0]) == 6:
        pass
    elif int(inputs[0]) == 7:
        pass

    else:
        sys.exit(0)
sys.exit(0)
