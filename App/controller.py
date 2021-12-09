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
 """

import config as cf
import model
import csv
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import prim
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import list as lt
from DISClib.ADT.graph import gr
from DISClib.Algorithms.Graphs import dfs
from DISClib.ADT import queue as qe
"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros
def initCatalog():
    """
    Llama la funcion de inicializacion del catalogo del modelo.
    """
    catalog = model.newCatalog()
    return catalog

def loadData(catalog):

    loadAirports(catalog)
    loadRoutes(catalog)
    loadCities(catalog)
    loadConnectedAirports(catalog)
    loadSCC(catalog)
    loadMST(catalog)

# Funciones para la carga de datos

def loadConnectedAirports(catalog):
    '''
    Carga los aereopuertos más conectados al catálogo
    '''
    connected_airports = model.connected_airports(catalog)
    catalog['connected_airports'] = connected_airports

def loadAirports(catalog):
    """
    Carga los datos de los aeropuertos.
    """
    airportsfile = 'airports-utf8-large.csv'
    airportsfile = cf.data_dir + airportsfile
    input_file = csv.DictReader(open(airportsfile, encoding="utf-8"),
                                delimiter=",")
    
    firstAirport = True
    for airport in input_file:
        model.addAirport(catalog, airport)
        model.addIATA(catalog, airport)
        model.addIATACoordinates(catalog, airport)
        if firstAirport == True:
            firstAirport = airport
    catalog['initialAirport'] = firstAirport
    catalog['finalAirport'] = airport
        
    return catalog
    
def loadRoutes(catalog):
    """
    Carga los datos de las rutas.
    """
    routesfile = 'routes-utf8-large.csv'
    routesfile = cf.data_dir + routesfile
    input_file = csv.DictReader(open(routesfile, encoding="utf-8"),
                                delimiter=",")
    n = 0                            
    for route in input_file:
        n+= 1
        model.addConnection(catalog, route['Departure'], route['Destination'], float(route['distance_km']))
        model.addRoute(catalog, route['Departure'], route['Destination'], float(route['distance_km'])) 
        model.addInRoute(catalog, route['Departure'], route['Destination'])
    catalog['numRoutes'] = n
    
    return catalog

def loadCities(catalog):
    """
    Carga los datos de las ciudades.
    """
    citiesfile = 'worldcities-utf8.csv'
    citiesfile = cf.data_dir + citiesfile
    input_file = csv.DictReader(open(citiesfile, encoding="utf-8"),
                                delimiter=",")
    
    n = 0
    for city in input_file:
        if n == 0:
            firstCity = city
        model.addCity(catalog, city)
        n +=1
    catalog['firstCity'] = firstCity
    catalog['lastCity'] = city
    catalog['numCities'] = n
    return catalog
    
def loadSCC(catalog):
    catalog['SCC'] = scc.KosarajuSCC(catalog['directedAirports']) 

def loadMST(catalog):
    graph = catalog['notDirectedAirports']
    MST = prim.PrimMST(graph)
    edgesList = mp.valueSet(MST['edgeTo'])
    mstCost = 0
    for edge in lt.iterator(edgesList):
        model.addAirportToMST(catalog, edge['vertexA'])
        model.addAirportToMST(catalog, edge['vertexB'])
        model.addConnectionToMST(catalog, edge['vertexA'], edge['vertexB'], edge['weight'])
        mstCost += edge['weight']
    catalog['MST']['cost'] = mstCost
# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo

def defineCity(catalog, city_name): 
    city = None
    if model.mp.contains(catalog['cities'], city_name):
        cities_list = model.me.getValue(model.mp.get(catalog['cities'], city_name))
        if model.lt.size(cities_list) == 1:
            city = model.lt.getElement(cities_list, 1)
        else: 
            print('Por favor elija el número de la ciudad que quiere ingresar:')
            for i in range(1, model.lt.size(cities_list) + 1):
                homonym_city = model.lt.getElement(cities_list, i)
                print(i, '- Nombre: ', city_name , 'País: ', homonym_city['country'], 'Población: ', homonym_city['population'],
                'Latitud: ', homonym_city['latitude'], 'Longitud: ', homonym_city['longitude'] )
            number = input('Ingrese el número: ')
            number = int(number)
            city = model.lt.getElement(cities_list, number)
    return city

def findLargerRoute(catalog, km, IATA):
    mst = catalog['MST']
    vertices = dfs.DepthFirstSearch(mst, IATA)
    partitionCost = 0
    partition = vertices['visited']
    partitionTable = [['Departure', 'Destination', 'distance_km']]
    iatas = {}
    lat = 0
    nlat = 0
    lg = 0
    for vertex in lt.iterator(mp.keySet(partition)):
        vertexB = me.getValue(mp.get(partition, vertex))['edgeTo']
        if vertexB != None:
            edge = gr.getEdge(mst, vertex, vertexB)
            partitionCost += edge['weight']
            partitionTable.append([vertex, vertexB, edge['weight']])
        iatas[vertex] = me.getValue(mp.get(catalog['IATAS'], vertex))
        lat += float(iatas[vertex]['latitude'])
        lg += float(iatas[vertex]['longitude'])
        nlat +=1

    
    return partitionTable, partitionCost, iatas, lat, lg, nlat
    
def appendEdge(list, edge, mst, vertex, adjacents):
    n = False
    next = edge['vertexB']
    adjs = gr.adjacentEdges(mst, next)
    if lt.size(adjs) == 1:
        R = list
    else:
        rCopy = list
        for e in lt.iterator(adjs):
            if e['vertexB'] != vertex:
                if n == True:
                    appendEdge(rCopy, e, mst, e['vertexA'])
                else:
                    n = True
                    list.append(e)
                    appendEdge(list, e, mst, e['vertexA'])
            else: 
                lt.removeFirst(adjs)
            
    return R
    
def near_airport(catalog, city):
    
    return model.define_near_airport(catalog, city)

def minimumCostRoute(catalog, airport1, airport2):
     return model.minCostRoute(catalog, airport1, airport2)




def affected_airports(catalog, Iatacode):
    data = model.affected_airports(catalog, Iatacode)
    return data
