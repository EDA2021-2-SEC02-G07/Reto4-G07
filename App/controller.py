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
    airportsfile = 'airports-utf8-small.csv'
    airportsfile = cf.data_dir + airportsfile
    input_file = csv.DictReader(open(airportsfile, encoding="utf-8"),
                                delimiter=",")

    for airport in input_file:
        model.addAirport(catalog, airport)
        model.addIATA(catalog, airport)
        model.addIATACoordinates(catalog, airport)
    return catalog
    
def loadRoutes(catalog):
    """
    Carga los datos de las rutas.
    """
    routesfile = 'routes-utf8-small.csv'
    routesfile = cf.data_dir + routesfile
    input_file = csv.DictReader(open(routesfile, encoding="utf-8"),
                                delimiter=",")
    
    for airport in input_file:
        model.addConnection(catalog, airport['Departure'], airport['Destination'], airport['distance_km'])
        model.addRoute(catalog, airport['Departure'], airport['Destination'], airport['distance_km']) 
        model.addInRoute(catalog, airport['Departure'], airport['Destination'])
    return catalog

def loadCities(catalog):
    """
    Carga los datos de las ciudades.
    """
    citiesfile = 'worldcities-utf8.csv'
    citiesfile = cf.data_dir + citiesfile
    input_file = csv.DictReader(open(citiesfile, encoding="utf-8"),
                                delimiter=",")
    
    for city in input_file:
        model.addCity(catalog, city)
    return catalog
    
def loadSCC(catalog):
    catalog['SCC'] = scc.KosarajuSCC(catalog['directedAirports']) 
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

def affected_airports(catalog, Iatacode):
    data = model.affected_airports(catalog, Iatacode)
    return data