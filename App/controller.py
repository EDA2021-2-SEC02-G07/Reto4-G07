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

# Funciones para la carga de datos
def loadAirports(catalog):
    """
    Carga los datos de los archivos y cargar los datos en la
    estructura de datos
    """
    airportsfile = 'airports_full.csv'
    airportsfile = cf.data_dir + airportsfile
    input_file = csv.DictReader(open(airportsfile, encoding="utf-8"),
                                delimiter=",")
    k = 0
    for airport in input_file:
        model.addAirport(catalog, model.createVertex(airport))
        model.addCity(catalog, airport)
        k+=1
    print(k)
    print(airport['City'], airport['IATA'])
    for airport in input_file:
        model.addCity(catalog, airport)
    return catalog
    
def loadRoutes(catalog):
    """
    Carga los datos de los archivos y cargar los datos en la
    estructura de datos
    """
    routesfile = 'routes_full.csv'
    routesfile = cf.data_dir + routesfile
    input_file = csv.DictReader(open(routesfile, encoding="utf-8"),
                                delimiter=",")
    
    for airport in input_file:
        model.addConnection(catalog, airport['Departure'], airport['Destination'], airport['distance_km'])
    return catalog
    
# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
