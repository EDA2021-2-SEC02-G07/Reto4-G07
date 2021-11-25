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
                   'cities': None 
                    }

        catalog['directedAirports'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=21400,
                                              comparefunction=compareAirports)

        catalog['notDirectedAirports'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=False,
                                              size=21400,
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
    Adiciona un aeropuerto como un vertice del grafo
    """
    try: 
        cityData = {'population': city['population'],
                'latitude': city['lat'],
                'longitude': city['lng']}
        mp.put(catalog['cities'], city['city'], cityData)
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

# Funciones para creacion de datos
def createVertex(airport):
    """
    A partir de la información de un aeropuerto se crea el nombre que tendrá su vértice en el grafo
    """
    name = airport['IATA'] + '-'
    name = name + airport['City']
    return name
# Funciones de consulta

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
