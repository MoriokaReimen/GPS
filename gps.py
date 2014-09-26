from mpl_toolkits.basemap import Basemap
import StringIO
import numpy
import math
import os
import sys

class GPS(object):
    def __init__(self, filename):

        # Format x[m] y[m] z[m] travel distance[m]
        self.points = [[], [], [], []]

        with open(filename) as f:
            buf = f.read()

        # transform string to file object
        fbuf = StringIO.StringIO(buf)
        self.data = list(csv.reader(fbuf, quoting=csv.QUOTE_NONNUMERIC))


        for index, line in enumerate(self.data):
            # Get the latitude coordinate
            latitude_str = str(line[2])
            latitude_direction = str(line[3])

            # Get the longitude coordinate
            longitude_str = str(line[4])
            longitude_direction = str(line[5])


            # Convert the raw gps coordinates to the degrees-minutes format
            latitude = self.convertGPSData(latitude_str, latitude_direction)
            longitude = self.convertGPSData(longitude_str, longitude_direction)

            # Set up the projection to convert longitude/latitude to X/Y axis (local coordinates)
            if index == 0:
                map = Basemap(projection='aeqd', lon_0 = longitude, lat_0 = latitude,
                              resolution='c', width = 500, height = 500)

            # Convert the initial gps data to local coordinates
            x, y = map(longitude, latitude)

            # Get the altitude value
            z = float(line[9])

            # record initial position
            if index == 0:
                origin_x = x
                origin_y = y
                origin_z = z

            #off set data
            x = x - origin_x
            y = y - origin_y
            z = z - origin_z

            #calculate travel distance
            if index == 0:
                travel_distance = 0.0
            else:
                last_x = self.points[0][-1]
                last_y = self.points[1][-1]
                last_z = self.points[2][-1]
                travel_distance = travel_distance + sqrt((x - last_x) ** 2 + (y - last_y) ** 2 + (z - last_z) ** 2)
             self.points[0].append(x)
             self.points[1].append(y)
             self.points[2].append(z)
             self.points[3].append(travel_distance)

        # Function for converting a raw gps coordinate to a minute-degree format
        def convertGPSData (self, gpsCoordinates, gpsDirection):
            # Dictionnary for direction
            direction = {'N':1, 'S':-1, 'E': 1, 'W':-1}

            # Split the coordinates
            temporary = gpsCoordinates.split(".")[0]

            # Calculate the degrees and minutes coordinate
            degrees = int(gpsCoordinates[:(len(temporary)-2)])
            minutes = float(gpsCoordinates[(len(temporary)-2):])

            # Return the coordiante under degree and minutes format
            return ( degrees + minutes / 60.0 ) * direction[gpsDirection]

if __name__ == '__main__':
    # Check if the number of arguments passed as parameter match the expected
    if (len(sys.argv) != 2):
        # If not, print helf message to the user and kill the program
        print ("Usage: {} raw-gps-data-file".format(sys.argv[0]))
        sys.exit(2)

    gps = GPS(sys.argv[1])
    for i in xrange(len(gps.points[0])):
        print gps.points[0][i], gps.points[1][i], gps.points[2][i], gps.points[3][i]
