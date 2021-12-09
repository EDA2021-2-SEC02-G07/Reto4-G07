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
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import prim
from DISClib.Algorithms.Graphs import dfs
assert cf
import time
sys.setrecursionlimit(50000)

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
        print('=============== Req 1. answer ===============')
        tabla1 = [['Iata', 'Conexiones', 'inbound', 'outbound', 'Nombre','Ciudad','País']]
        airports_directed = catalog['connected_airports']
        airports_map = catalog['IATAS']
        for key in  lt.iterator(airports_directed):
            airport = me.getValue(mp.get(airports_map, key[0]))
            line = [key[0], key[1], gr.indegree(catalog['directedAirports'], key[0]), gr.degree(catalog['directedAirports'],key[0]),
             airport['name'], airport['city'], airport['country'] ]
            tabla1.append(line)
        print('Los 5 aereopuertos que son los mayores puntos de interconexión aerea (grafo dirigido) son:')
        print(tabulate(tabla1 , headers='firstrow', tablefmt='fancy_grid'))

    elif int(inputs[0]) == 2:
        try:
            graph = catalog['directedAirports']
            comps = catalog['SCC']

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
        try:
            mst = catalog['MST']
            print('=============== Req 4. inputs ===============')
            IATa = input('Inserte el código IATA del aeropuerto de inicio: ')
            miles = float(input('Inserte el número de millas acumuladas por el viajero: '))
            km = miles *1.6

            print()
            print('=============== Req 4. answer ===============')
            table, cost = controller.findLargerRoute(catalog, km, IATa)
            print('  - Número de posibles aeropuertos:', gr.numVertices(mst))
            print('  - Suma de la distancia de viaje entre aeropuertos:', round(mst['cost'],2), '(km)')
            print('  - Millas disponibles del pasajero:', miles * 1.6, '(km)')

            print()
            print("+++ Posible ruta más larga que pasa por el aeropuerto '" + IATa + "'")
            print('  - Distancia del posible camino más largo:', round(cost,2), '(km)')
            print('  - Detalles del camino posible más largo:')
            print(tabulate(table , headers='firstrow', tablefmt='fancy_grid'))

            print('-----')
            print('El pasajero necesita', (cost*2)/1.6 - 19850, 'millas para poder completar el recorrido más largo posible.')
            print('-----')
        except:
            print('Inserte valores válidos compa.')
        
    elif int(inputs[0]) == 5: 
        Iatacode = input('Ingrese el código IATA del aereopuerto que está cerrado: ')
        data = controller.affected_airports(catalog, Iatacode)
        affected_airports = []
        list1 = data[0]
        list2 = data[1]
        total = data[2]
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
        print(result)

    elif int(inputs[0]) == 6:
        pass
    elif int(inputs[0]) == 7:
        pass

    else:
        sys.exit(0)
sys.exit(0)
