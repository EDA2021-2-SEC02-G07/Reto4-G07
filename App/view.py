﻿"""
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
from DISClib.Algorithms.Graphs import dfs
assert cf
import time
import folium
import webbrowser
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
        start_time = time.process_time()
        catalog = option0()
        stop_time = time.process_time()
        elapsed_time_mseg = (stop_time - start_time)
        print('La carga duró', elapsed_time_mseg, 'segundos')

        numVertex = gr.numVertices(catalog['directedAirports'])
        numEdges= gr.numEdges(catalog['directedAirports'])
        print('=== Aeropuertos-Rutas Grafo Dirigido===')
        print('Vertices:', numVertex, ' vertices de', numVertex, 'aeropuetos cargados.' )
        print('Arcos:', numEdges, ' arcos de', catalog['numRoutes'], 'rutas cargadas.' )
        graphTable = [['IATA','Name', 'City', 'Country', 'Latitude', 'Longitude']]
        initialAirport = catalog['initialAirport']
        finalAirport = catalog['finalAirport']
        graphTable.append([initialAirport['IATA'], initialAirport['Name'], initialAirport['Country'],
         round(float(initialAirport['Latitude']), 4), round(float(initialAirport['Longitude']), 4)])
        graphTable.append([finalAirport['IATA'], finalAirport['Name'], finalAirport['Country'],
         round(float(finalAirport['Latitude']), 4), round(float(finalAirport['Longitude']), 4)])
        print(tabulate(graphTable , headers='firstrow', tablefmt='fancy_grid'))
        print()
        numVertex = gr.numVertices(catalog['notDirectedAirports'])
        numEdges= gr.numEdges(catalog['notDirectedAirports'])

        print()
        numVertex = gr.numVertices(catalog['notDirectedAirports'])
        numEdges= gr.numEdges(catalog['notDirectedAirports'])
        print('=== Aeropuertos-Rutas Grafo No Dirigido===')
        print('Vertices:', numVertex, ' vertices de', numVertex, 'aeropuetos cargados.' )
        print('Arcos:', numEdges, ' arcos de', catalog['numRoutes'], 'rutas cargadas.' )
        graphTable = [['IATA','Name', 'City', 'Country', 'Latitude', 'Longitude']]
        initialAirport = catalog['initialAirport']
        finalAirport = catalog['finalAirport']
        graphTable.append([initialAirport['IATA'], initialAirport['Name'], initialAirport['Country'],
         round(float(initialAirport['Latitude']), 4), round(float(initialAirport['Longitude']), 4)])
        graphTable.append([finalAirport['IATA'], finalAirport['Name'], finalAirport['Country'],
         round(float(finalAirport['Latitude']), 4), round(float(finalAirport['Longitude']), 4)])
        print(tabulate(graphTable , headers='firstrow', tablefmt='fancy_grid'))
        print()
        numVertex = gr.numVertices(catalog['notDirectedAirports'])
        numEdges= gr.numEdges(catalog['notDirectedAirports'])

        print()
        print('=== Ciudades cargadas===')
        print('Hay', catalog['numCities'], 'nombres de ciudades registrados')
        citiesTable = [['City', 'Country', 'Latitude', 'Longitude', 'population']]
        firstCity = catalog['firstCity']
        lastCity = catalog['lastCity']
        citiesTable.append([firstCity['city'], firstCity['country'], firstCity['lat'], firstCity['lng'], firstCity['population']])
        citiesTable.append([lastCity['city'], lastCity['country'], lastCity['lat'], lastCity['lng'], lastCity['population']])
        print('La primera y última ciudad cargada son:')
        print(tabulate(citiesTable , headers='firstrow', tablefmt='fancy_grid'))
        print()

    elif int(inputs[0]) == 1:
        try:
            print('=============== Req 1. answer ===============')
            start_time = time.process_time()
            tabla1 = [['Iata', 'Conexiones', 'inbound', 'outbound', 'Nombre','Ciudad','País']]
            airports_directed = catalog['connected_airports']
            airports_map = catalog['IATAS']
            iatas = {}
            lat = 0
            lg = 0
            for key in  lt.iterator(airports_directed):
                iatas[key[0]] = me.getValue(mp.get(catalog['IATAS'], key[0]))
                lat += float(iatas[key[0]]['latitude'])
                lg += float(iatas[key[0]]['longitude'])
                airport = me.getValue(mp.get(airports_map, key[0]))
                line = [key[0], key[1], gr.indegree(catalog['directedAirports'], key[0]), gr.degree(catalog['directedAirports'],key[0]),
                airport['name'], airport['city'], airport['country'] ]
                tabla1.append(line)
            stop_time = time.process_time()
            elapsed_time_mseg = (stop_time - start_time)
            print('La carga duró', elapsed_time_mseg, 'segundos')
            print('Los 5 aereopuertos que son los mayores puntos de interconexión aerea (grafo dirigido) son:')
            print(tabulate(tabla1 , headers='firstrow', tablefmt='fancy_grid'))


            print()
            print('¿Desea visualizar los aeropuertos relacionados con la consulta en un mapa?')
            print('1. Sí.')
            print('2. No.')
            mapeo = input('Ingrese la opción que desee: ')
            if mapeo == '1':
                mi_mapa = folium.Map(location=(lat/5,lg/5), zoom_start=2)
                for iata in iatas:
                    latitude = float(iatas[iata]['latitude'])
                    longitude = float(iatas[iata]['longitude'])
                    marcador = folium.Marker(location=(latitude, longitude))
                    marcador.add_to(mi_mapa)
                    
                mi_mapa.save("mapa.html")
                webbrowser.open_new('mapa.html')
        except:
            print('Inserte valores válidos compa.') 

    elif int(inputs[0]) == 2:
        try:
            graph = catalog['directedAirports']
            comps = catalog['SCC']

            a1 = input('Inserte el código IATA del aeropuerto 1: ')
            a2 = input('Inserte el código IATA del aeropuerto 2: ')
            print()
            print('=============== Req 2. answer ===============')
            start_time = time.process_time()
            conected = scc.stronglyConnected(comps, a1, a2)
            stop_time = time.process_time()
            elapsed_time_mseg = (stop_time - start_time)
            print('La carga duró', elapsed_time_mseg, 'segundos')
            print('Número de componentes fuertemente conectados:', scc.connectedComponents(comps))

            print('¿Están el aeropuerto con código "' + a1 + '" y el aeropuerto con código "' + a2 + '" fuertemente conectados?:', conected)
            airp1 = me.getValue(mp.get(catalog['IATAS'], a1))
            airp2 = me.getValue(mp.get(catalog['IATAS'], a2))
            iatas = {a1: airp1, a2: airp2}
            lati = float(airp1['latitude']) + float(airp2['latitude'])
            lang = float(airp1['longitude']) + float(airp2['longitude'])

            print()
            print('¿Desea visualizar los aeropuertos relacionados con la consulta en un mapa?')
            print('1. Sí.')
            print('2. No.')
            mapeo = input('Ingrese la opción que desee: ')
            if mapeo == '1':
                mi_mapa = folium.Map(location=(lati/2,lang/2), zoom_start=2)
                for iata in iatas:
                    latitude = float(iatas[iata]['latitude'])
                    longitude = float(iatas[iata]['longitude'])
                    marcador = folium.Marker(location=(latitude, longitude))
                    marcador.add_to(mi_mapa)
                
                mi_mapa.save("mapa.html")
                webbrowser.open_new('mapa.html')

        except:
            print('Inserte valores válidos compa.') #XD



    elif int(inputs[0]) == 3:
        try:
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

            start_time = time.process_time()
            origin_airport = controller.near_airport(catalog, origin_data)
            destination_airport = controller.near_airport(catalog, destination_data)
            origin_dist = origin_airport[1]
            destination_dist = destination_airport[1]
            origin_airport = origin_airport[0]
            destination_airport = destination_airport[0]
            path = controller.minimumCostRoute(catalog, origin_airport, destination_airport)
            stop_time = time.process_time()
            elapsed_time_mseg = (stop_time - start_time)
            print('La carga duró', elapsed_time_mseg, 'segundos')

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
            iatas = {}
            lat = 0
            nlat = 0
            lg = 0
            distance = origin_dist+destination_dist
            while (not stack.isEmpty(path)):
                triproute = stack.pop(path)
                table3.append([triproute['vertexA'], triproute['vertexB'],triproute['weight']])
                aereopuertos.append(triproute['vertexA'])
                aereopuertos.append(triproute['vertexB'])
                distance += float(triproute['weight'])
                
            result = []
            for aereopuerto in aereopuertos:
                iatas[aereopuerto] = me.getValue(mp.get(catalog['IATAS'], aereopuerto))
                lat += float(iatas[aereopuerto]['latitude'])
                lg += float(iatas[aereopuerto]['longitude'])
                nlat +=1
                if aereopuerto not in result:
                    result.append(aereopuerto)
            for iata in result:
                airport_info = me.getValue(mp.get(catalog['IATAS'], iata))
                table4.append([iata, airport_info['name'],airport_info['country'],airport_info['city']])
                    
            print('=============== Req 3. answer ===============')
            print('El viaje cubre una distancia de:', round(distance,3), 'Km' )
            print('Para ir desde', origin, 'hasta', destination, 'se debe trasladar desde el aereopuerto:')
            print(tabulate(table1 , headers='firstrow', tablefmt='fancy_grid'))

            print('Hasta el aereopuerto:')
            print(tabulate(table2 , headers='firstrow', tablefmt='fancy_grid'))

            print('Los trayectos que debe seguir son: ')
            print(tabulate(table3 , headers='firstrow', tablefmt='fancy_grid'))

            print('En la tabla se brinda información de las paradas: ')
            print(tabulate(table4 , headers='firstrow', tablefmt='fancy_grid'))
            
            print()
            print('¿Desea visualizar los aeropuertos relacionados con la consulta en un mapa?')
            print('1. Sí.')
            print('2. No.')
            mapeo = input('Ingrese la opción que desee: ')
            if mapeo == '1':
                mi_mapa = folium.Map(location=(lat/nlat,lg/nlat), zoom_start=2)
                for iata in iatas:
                    latitude = float(iatas[iata]['latitude'])
                    longitude = float(iatas[iata]['longitude'])
                    marcador = folium.Marker(location=(latitude, longitude))
                    marcador.add_to(mi_mapa)
                
                mi_mapa.save("mapa.html")
                webbrowser.open_new('mapa.html')
        except:
            print('Inserte valores válidos compa.') 
        
        
    elif int(inputs[0]) == 4:
        try:
            mst = catalog['MST']
            print('=============== Req 4. inputs ===============')
            IATa = input('Inserte el código IATA del aeropuerto de inicio: ')
            miles = float(input('Inserte el número de millas acumuladas por el viajero: '))
            km = miles *1.6

            print()
            print('=============== Req 4. answer ===============')

            start_time = time.process_time()
            table, cost, iatas, lat, lg, nlat = controller.findLargerRoute(catalog, km, IATa)
            stop_time = time.process_time()
            elapsed_time_mseg = (stop_time - start_time)
            print('La carga duró', elapsed_time_mseg, 'segundos')
            print('  - Número de posibles aeropuertos:', gr.numVertices(mst))
            print('  - Suma de la distancia de viaje entre aeropuertos:', round(mst['cost'],2), '(km)')
            print('  - Millas disponibles del pasajero:', miles * 1.6, '(km)')

            print()
            print("+++ Posible ruta más larga que pasa por el aeropuerto '" + IATa + "'")
            print('  - Distancia del posible camino más largo:', round(cost,2), '(km)')
            print('  - Detalles del camino posible más largo:')
            print(tabulate(table , headers='firstrow', tablefmt='fancy_grid'))

            print('-----')
            if (cost*2)/1.6 - 19850 > 0:
                print('El pasajero necesita', (cost*2)/1.6 - 19850, 'millas para poder completar el recorrido más largo posible.')
            else: print('El pasajero no necesita más millas para poder hacer el recorrido.')
            print('-----')

            print()
            print('¿Desea visualizar los aeropuertos relacionados con la consulta en un mapa?')
            print('1. Sí.')
            print('2. No.')
            mapeo = input('Ingrese la opción que desee: ')
            if mapeo == '1':
                mi_mapa = folium.Map(location=(lat/nlat,lg/nlat), zoom_start=2)
                for iata in iatas:
                    latitude = float(iatas[iata]['latitude'])
                    longitude = float(iatas[iata]['longitude'])
                    marcador = folium.Marker(location=(latitude, longitude))
                    marcador.add_to(mi_mapa)
                
                mi_mapa.save("mapa.html")
                webbrowser.open_new('mapa.html')
        except:
            print('Inserte valores válidos compa.')
        
    elif int(inputs[0]) == 5: 
        try:
            print('=============== Req 5. inputs ===============')
            Iatacode = input('Ingrese el código IATA del aereopuerto que está cerrado: ')
            start_time = time.process_time()
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
            print('=============== Req 5. answer ===============')
            stop_time = time.process_time()
            elapsed_time_mseg = (stop_time - start_time)
            print('La carga duró', elapsed_time_mseg, 'segundos')
            print('El cierre afecta a', len(result), 'aereopuerto(s)')
            if len(result) <= 6:
                pass
            else: 
                result = result[0:3]+result[len(result)-4:]
            iatas = {}
            lat = 0
            nlat = 0
            lg = 0
            tablita = [['IATA', 'Nombre', 'País', 'Ciudad']]
            for iata in result:
                airport_info = me.getValue(mp.get(catalog['IATAS'], iata))
                tablita.append([iata, airport_info['name'],airport_info['country'],airport_info['city']])
                iatas[iata] = me.getValue(mp.get(catalog['IATAS'], iata))
                lat += float(iatas[iata]['latitude'])
                lg += float(iatas[iata]['longitude'])
                nlat +=1
            print('Los primeros 3 y los últimos 3 aereopuertos afectados son: ')
            print(tabulate(tablita , headers='firstrow', tablefmt='fancy_grid'))
            print()
            print('¿Desea visualizar los aeropuertos relacionados con la consulta en un mapa?')
            print('1. Sí.')
            print('2. No.')
            mapeo = input('Ingrese la opción que desee: ')
            if mapeo == '1':
                mi_mapa = folium.Map(location=(lat/nlat,lg/nlat), zoom_start=2)
                for iata in iatas:
                    latitude = float(iatas[iata]['latitude'])
                    longitude = float(iatas[iata]['longitude'])
                    marcador = folium.Marker(location=(latitude, longitude))
                    marcador.add_to(mi_mapa)
                
                mi_mapa.save("mapa.html")
                webbrowser.open_new('mapa.html')
        except:
            print('Inserte valores válidos compa.')
    elif int(inputs[0]) == 6:
        pass

    else:
        sys.exit(0)
sys.exit(0)
