#! /bin/python
# -*- coding: utf-8 -*-
""" gps.py
Convert *.000 file and Output as a tsb file.
USAGE:
    $ python gps.py hogehoge.000 > Outputfile.tsb
"""
import mpl_toolkits.basemap as mpl
import StringIO
import scipy.signal as sp
import math
import csv
import sys


def to_ddmm(gps_coordinates, gps_direction):
    """
    Private function for converting a raw gps coordinate to a
    minute-degree format
    Args:
        gps_coordinates (float): coordinate of gps data
        gps_direction (float): direction of gps data

    Returns:
        float: coordinate in degree and minutes format
    """
    # Dictionnary for direction
    direction = {'N': 1, 'S': -1, 'E': 1, 'W': -1}

    # Split the coordinates
    temporary = gps_coordinates.split(".")[0]

    # Calculate the degrees and minutes coordinate
    degrees = int(gps_coordinates[:(len(temporary) - 2)])
    minutes = float(gps_coordinates[(len(temporary) - 2):])

    # Return the coordiante under degree and minutes format
    return (degrees + minutes / 60.0) * direction[gps_direction]


class GPS(object):

    """ *.000 file manupilating class.
    read *.000 file and convert to list self.points
    Format of self.points is
    [[x positions], [y positions], [y positions]]
    """

    def __init__(self, filename):
        """
        Constructor of GPS class.
        Args:
            filename (str): path of *.000 file.
        """
        # Format x[m] y[m] z[m]
        self.points = [[], [], []]

        with open(filename) as file000:
            buf = StringIO.StringIO(file000.read())

        # transform file object to list
        self.data = list(csv.reader(buf, delimiter=','))

        for index, line in enumerate(filter(lambda line: not '' in line,self.data)):
            # Get the latitude coordinate
            latitude_str = str(line[2])
            latitude_direction = str(line[3])

            # Get the longitude coordinate
            longitude_str = str(line[4])
            longitude_direction = str(line[5])

            # Convert the raw gps coordinates to the degrees-minutes format
            latitude = to_ddmm(latitude_str, latitude_direction)
            longitude = to_ddmm(longitude_str, longitude_direction)

            # Set up the projection to convert longitude/latitude to X/Y axis
            if index == 0:
                projection = mpl.Basemap(projection='aeqd', lon_0=longitude,
                                         lat_0=latitude, resolution='c',
                                         width=500, height=500)

            # Convert the initial gps data to local coordinates
            # list "point" point of xyz coordinate
            # Format:
            #   [xposition, ypostion zposition]
            point = list(projection(longitude, latitude))
            point += [float(line[9])]

            # record initial position
            if index == 0:
                origin = [point[0], point[1], point[2]]

            # off set data
            point = [point[i] - origin[i] for i in range(len(point))]

            self.points[0].append(point[0])
            self.points[1].append(point[1])
            self.points[2].append(point[2])

    def filt_points(self, cut_off):
        """
        smooth data with butterworth filter.
        Args:
            cut_off (float): cutoff frequency of filter ranged 0 to 1.
        """
        num, den = sp.butter(2, cut_off, 'low')
        for point in self.points:
            buff = sp.filtfilt(num, den, point)
            point = buff

    def calc_travel_distance(self):
        """
        calculate net taravel distance.
        Returns:
            float: net travel distance [m]
        """
        for num in range(len(self.points[0])):
            if num == 0:
                travel_distance = 0.0
            else:
                new_x = self.points[0][num]
                new_y = self.points[1][num]
                new_z = self.points[2][num]
                last_x = self.points[0][num - 1]
                last_y = self.points[1][num - 1]
                last_z = self.points[2][num - 1]
                travel_distance = travel_distance + \
                    math.sqrt(
                        (new_x - last_x) ** 2 +
                        (new_y - last_y) ** 2 +
                        (new_z - last_z) ** 2)
        return travel_distance

if __name__ == '__main__':
    # Check if the number of arguments passed as parameter match the expected
    if (len(sys.argv) != 2):
        # If not, print helf message to the user and kill the program
        print ("Usage: {} raw-gps-data-file".format(sys.argv[0]))
        sys.exit(2)

    DATA = GPS(sys.argv[1])
    print "X[m]\tY[m]\tZ[m]\tTravel Distance[m]\tSlope Angle[degree]"
    for i in xrange(len(DATA.points[0])):
        # Format X[m] Y[m] Z[m]
        print "%4.5f\t%4.5f\t%4.5f" % \
            (DATA.points[0][i], DATA.points[1][i], DATA.points[2][i])
