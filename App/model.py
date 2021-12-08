"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.ADT.graph import gr
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Utils import error as error
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def newCatalog():
    """
    Inicializa el catálogo. Crea una diccionario vacío para guardar
    todos las estructuras de datos.
    """
    try:
        catalog = {'directedAirports': None,
                   'notDirectedAirports': None,
                   'cities': None,
                   'IATAS': None,
                   'routes': None,
                   'SCC': None,
                   'MST': None,
                   'connected_airports': None
                    }

        catalog['directedAirports'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=21400,
                                              comparefunction=compareAirports)

        catalog['notDirectedAirports'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=False,
                                              size=60,
                                              comparefunction=compareAirports)

        catalog['MST'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=False,
                                              size=60,
                                              comparefunction=compareAirports)

        catalog['cities'] = mp.newMap(numelements= 20000,
                                      maptype= 'PROBING',
                                      loadfactor= 0.5)
        catalog['IATAS'] = mp.newMap(numelements= 20000,
                                      maptype= 'PROBING',
                                      loadfactor= 0.5) 
        catalog['routes'] = mp.newMap(numelements= 20000,
                                      maptype= 'PROBING',
                                      loadfactor= 0.5)  
        catalog['connected_airports'] = None        

        catalog['SCC'] = None    

        catalog['InRoutes'] = {}
        
        return catalog
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')
    
# Funciones para agregar informacion al catalogo

def addAirport(catalog, airport):
    """
    Adiciona un aeropuerto como un vertice del grafo
    """
    try: 
        gr.insertVertex(catalog['directedAirports'], airport['IATA'])
    except Exception as exp:
        error.reraise(exp, 'model:addAirport')

def addConnection(catalog, Departure, Destination, distance_km):
    """
    Adiciona un arco entre dos aeropuertos.
    """
    edge = gr.getEdge(catalog['directedAirports'], Departure, Destination)
    if edge is None:
        gr.addEdge(catalog['directedAirports'], Departure, Destination, distance_km)
    
def addCity(catalog, city):
    """
    Adiciona una ciudad al mapa de ciudades
    """
    try: 
        cityData = {'population': city['population'],
                'latitude': city['lat'],
                'longitude': city['lng'], 'country': city['country']}
        if mp.contains(catalog['cities'], city['city_ascii']):
            homonyms_cities = me.getValue(mp.get(catalog['cities'], city['city_ascii']))
            lt.addLast(homonyms_cities, cityData)
        else: 
            homonyms_cities = lt.newList('ARRAY_LIST')
            lt.addLast(homonyms_cities, cityData)
            mp.put(catalog['cities'], city['city_ascii'], homonyms_cities)
    except Exception as exp:
        error.reraise(exp, 'model:addCity')

def addIATA(catalog, airport):
    """
    Adiciona un aeropuerto como un vertice del grafo
    """
    try: 
        airportData = {'name': airport['Name'],
                'country': airport['Country'],
                'city': airport['City'],
                'latitude': airport['Latitude'],
                'longitude': airport['Longitude']}
        mp.put(catalog['IATAS'], airport['IATA'], airportData)
    except Exception as exp:
        error.reraise(exp, 'model:addCity')

      
def addRoute(catalog, Departure, Destination, distance_km):
    """
    Adiciona un arco entre dos aeropuertos.
    """
    inverse = mp.get(catalog['routes'], Destination + '-' + Departure)
    if inverse is not None: 
        if not gr.containsVertex(catalog['notDirectedAirports'], Destination):
            gr.insertVertex(catalog['notDirectedAirports'], Destination)
        if not gr.containsVertex(catalog['notDirectedAirports'], Departure):
            gr.insertVertex(catalog['notDirectedAirports'], Departure)
        edge = gr.getEdge(catalog['notDirectedAirports'], Departure, Destination)
        if edge is None:
            gr.addEdge(catalog['notDirectedAirports'], Departure, Destination, distance_km)
        mp.put(catalog['routes'], Departure + '-' + Destination, True)
    else: 
        mp.put(catalog['routes'], Departure + '-' + Destination, True)

def addAirportToMST(catalog, airport):
    """
    Adiciona un aeropuerto como un vertice del grafo
    """
    try: 
        if not gr.containsVertex(catalog['MST'], airport):
            gr.insertVertex(catalog['MST'], airport)
    except Exception as exp:
        error.reraise(exp, 'model:addAirport')

def addConnectionToMST(catalog, Departure, Destination, distance_km):
    """
    Adiciona un arco entre dos aeropuertos.
    """
    edge = gr.getEdge(catalog['MST'], Departure, Destination)
    if edge is None:
        gr.addEdge(catalog['MST'], Departure, Destination, distance_km)
        

def addInRoute(catalog,V_origin, V_destination):
    routes_map = catalog['InRoutes']
    if V_destination not in routes_map:
        routes_map[V_destination] = lt.newList('ARRAY_LIST')
        lt.addLast(routes_map[V_destination], V_origin)
    else:
        lt.addLast(routes_map[V_destination],V_origin) 
    

# Funciones para creacion de datos
def createVertex(airport):
    """
    A partir de la información de un aeropuerto se crea el nombre que tendrá su vértice en el grafo
    """
    name = airport['IATA'] + '-'
    name = name + airport['City']
    return name

# Funciones de consulta
def minimum(dictionary):
    '''
    Determina la llave y el valor mínimo de un diccionario
    '''
    minimum = None
    min_key = None
    for key in dictionary:
        value = dictionary[key]
        if minimum == None or value < minimum:
            minimum = value
            min_key = key
    return minimum, min_key

        
def affected_airports(catalog, Iatacode):
    directed_graph = catalog['directedAirports']
    affected_airpots_directed = gr.degree(directed_graph, Iatacode)
    airports_list = gr.adjacents(directed_graph, Iatacode)
    airports_list2 = catalog['InRoutes'][Iatacode]
    return (airports_list, airports_list2, affected_airpots_directed)



def search_connected_airports(vertices, graph):
    '''
    Busca los aereopuertos más interconectados
    '''
    selected_airports = {}
    min_connections = -1
    for i in range(1, lt.size(vertices)+1):
        airport = lt.getElement(vertices, i)
        connections = gr.degree(graph, airport)
        if len(selected_airports) < 10:
            selected_airports[airport] = connections
            min_connections, min_key = minimum(selected_airports)
        elif connections > min_connections:
            selected_airports.pop(min_key)
            selected_airports[airport] = connections
            min_connections, min_key = minimum(selected_airports)

    return selected_airports        

def connected_airports(catalog):
    '''
    Define los aereopuertos conectados de los dos grafos
    '''
    airports1 = catalog['directedAirports']
    airports2 = catalog['notDirectedAirports']
    airports1_vertices = gr.vertices(airports1)
    airports2_vertices = gr.vertices(airports2)
    connected_airports1 = search_connected_airports(airports1_vertices, airports1)
    connected_airports2 = search_connected_airports(airports2_vertices, airports2)
    return connected_airports1, connected_airports2

# Funciones de comparación

def compareAirports(Airport, keyvalueAirport):
    """
    Compara dos estaciones
    """
    Airportcode = keyvalueAirport['key']
    if (Airport == Airportcode):
        return 0
    elif (Airport < Airportcode):
        return 1
    else:
        return -1

# Funciones de ordenamiento
