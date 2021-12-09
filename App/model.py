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
import math 
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.ADT.graph import gr
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
assert cf
from DISClib.Algorithms.Sorting import mergesort as merge

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

        catalog['LatitudesTree'] = om.newMap(omaptype= 'RBT', comparefunction= cmpValues)

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
        gr.addEdge(catalog['directedAirports'], Departure, Destination, float(distance_km))
    else:
        outdegreeList = me.getValue(mp.get(catalog['directedAirports']['vertices'], edge['vertexA']))
        outdegreeList['size'] += 1
        indegree = me.getValue(mp.get(catalog['directedAirports']['indegree'], edge['vertexB'])) 
        mp.put(catalog['directedAirports']['indegree'], edge['vertexB'], indegree + 1)
    
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



def addIATACoordinates(catalog, airport):
    """
    Adiciona un aereopuerto al arbol RBT
    """
    Iatacode = airport['IATA']
    latitude = float(airport['Latitude'])
    longitude = float(airport['Longitude'])
    latitudes = catalog['LatitudesTree']

    try:
        longitudes = om.get(latitudes, latitude)
        om.put(longitudes, longitude, Iatacode)
    except:
        longitudes = om.newMap(omaptype= 'RBT', comparefunction= cmpValues)
        om.put(longitudes, longitude, Iatacode)
        om.put(latitudes, latitude, longitudes)

    

      
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

def hav(x):
    ''' retorna la función hav de un dato'''
    result = (math.sin(x/2))**2
    return result

def invhav(x):
    ''' retorna la inversa de la función hav'''
    result = 2*(math.asin((x**0.5)))
    return result

def havDistance(lon1, lon2, lat1, lat2):
    r = 6371
    x = hav(lat2-lat1)+((1-hav(lat1-lat2)-hav(lat1+lat2))*hav(lon2-lon1))
    d = 2*r*(math.asin(x**0.5))
    return d

def latitudeUpDown(latitude, d):
    r = 6371
    k = invhav(math.sin(d/(2*r))**2)
    l1 = k + latitude
    l2 = latitude - k
    
    if l1 > l2:
        return l1, l2
    else: 
        return l2, l1

def longitudeUpDown(longitude, latitude, d):
    r = 6371
    div = (math.sin(d/(2*r))**2)/(1-hav(2*latitude))
    k = invhav(div)
    l1 = k+longitude
    l2 = longitude-k

    if l1 > l2: 
        return l1, l2
    else:
        return l2, l1


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
    airports_list = gr.adjacents(directed_graph, Iatacode)
    airports_list2 = catalog['InRoutes'][Iatacode]

    return (airports_list, airports_list2)



def search_connected_airports(vertices, graph,catalog):
    '''
    Busca los aereopuertos más interconectados
    '''
    selected_airports = {}
    min_connections = -1
    for i in range(1, lt.size(vertices)+1):
        airport = lt.getElement(vertices, i)
        connections = vertexDegree(graph, airport) 
        if len(selected_airports) < 5:
            selected_airports[airport] = connections
            min_connections, min_key = minimum(selected_airports)
        elif connections > min_connections:
            selected_airports.pop(min_key)
            selected_airports[airport] = connections
            min_connections, min_key = minimum(selected_airports)

    AirportsList = lt.newList('ARRAY_LIST')      
    for x in selected_airports:
        lt.addLast(AirportsList, (x, selected_airports[x]))
    orderedAirports = sortAirports(AirportsList, compareAirportsDegree)
    return orderedAirports        

def connected_airports(catalog):
    '''
    Define los aereopuertos conectados de los dos grafos
    '''
    airports1 = catalog['directedAirports']
    airports1_vertices = gr.vertices(airports1)
    connected_airports1 = search_connected_airports(airports1_vertices, airports1, catalog)
    return connected_airports1


def search_near_airports(catalog, city, d):
    latitudes = catalog['LatitudesTree']
    near_airports = []
    latitude = float(city['latitude']) * 0.0174533
    longitude = float(city['longitude']) * 0.0174533
    latup,latdown = latitudeUpDown(latitude, d)
    lonup,londown = longitudeUpDown(longitude, latitude, d)
    latitudes_list = om.values(latitudes, latdown/0.0174533, latup/0.0174533)
    list_size = lt.size(latitudes_list)

    for i in range(1, list_size + 1):
        longitudes = lt.getElement(latitudes_list, i)
        longitudes_list = om.values(longitudes, londown/0.0174533, lonup/0.0174533)
        longitudes_size = lt.size(longitudes_list)
        for j in range(1, longitudes_size + 1):
            airport = lt.getElement(longitudes_list, j)
            near_airports.append(airport)    
    if len(near_airports) > 0:
        return near_airports

    else: 
        return search_near_airports(catalog, city, d+10)


def define_near_airport(catalog, city):
    city_latitude = float(city['latitude'])*0.0174533
    city_longitude = float(city['longitude'])*0.0174533
    selected_airport = None
    mindist = -1
    airports = search_near_airports(catalog, city, 10)
    if len(airports) == 1: 
        selected_airport = airports[0]
        airport = selected_airport
        airport_data = me.getValue(mp.get(catalog['IATAS'], airport)) 
        airport_latitude = float(airport_data['latitude'])*0.0174533
        airport_longitude = float(airport_data['longitude'])*0.0174533
        distance = havDistance(airport_longitude, city_longitude, airport_latitude, city_latitude)
        mindist = distance
    else: 
        for airport in airports:
            airport_data = me.getValue(mp.get(catalog['IATAS'], airport)) 
            airport_latitude = float(airport_data['latitude'])*0.0174533
            airport_longitude = float(airport_data['longitude'])*0.0174533
            distance = havDistance(airport_longitude, city_longitude, airport_latitude, city_latitude)
            if selected_airport == None or distance < mindist:
                selected_airport = airport
                mindist = distance
    return selected_airport, mindist


def minCostRoute(catalog, airport1, airport2):
    routes = djk.Dijkstra(catalog['directedAirports'], airport1)
    
    return djk.pathTo(routes, airport2)

   
def vertexDegree(graph, vertex):
    return gr.degree(graph, vertex) + gr.indegree(graph, vertex)

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

def compareAirportsDegree(Airport1, Airport2):
    degree1 = Airport1[1]
    degree2 = Airport2[1]
    return degree1  > degree2 
    
def cmpValues(value1, value2):
    """
    Compara dos valores numéricos o str cualquiera
    """
    if value1 == value2:
        return 0
    elif value1 > value2:
        return 1
    else: 
        return -1

# Funciones de ordenamiento
def sortAirports(list, cmpfunction):
    size=lt.size(list)
    sub_list = lt.subList(list, 1, size)
    sub_list = sub_list.copy()
    sorted_list = merge.sort(sub_list, cmpfunction)      
    
    return sorted_list