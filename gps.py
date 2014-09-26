from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy
import math
import os
import pickle
import sys

# Function for converting a raw gps coordinate to a minute-degree format
def convertGPSData (gpsCoordinates, gpsDirection):
    # Dictionnary for direction
    direction = {'N':1, 'S':-1, 'E': 1, 'W':-1}

    # Split the coordinates
    temporary = gpsCoordinates.split(".")[0]

    # Calculate the degrees and minutes coordinate   
    degrees = int(gpsCoordinates[:(len(temporary)-2)])
    minutes = float(gpsCoordinates[(len(temporary)-2):])

    # Return the coordiante under degree and minutes format
    return ( degrees + minutes / 60.0 ) * direction[gpsDirection]



# Check if the number of arguments passed as parameter match the expected
if (len(sys.argv) != 2):
    # If not, print helf message to the user and kill the program
    print ("Usage: {} raw-gps-data-file".format(sys.argv[0]))
    sys.exit(2)

# Define lists to store the gps data
x_list = []
y_list = []
z_list = []
movement_estimation_list = []

movementEstimation = 0.0


# Open the gps data file
with open(sys.argv[1], "r") as f:
    # Read the first line of gps data and split it
    data = f.readline().split(",")
   
    # Get the latitude coordinate
    latitudeStr = str(data[2])
    latitudeDirection = str(data[3])
  
    # Get the longitude coordinate
    longitudeStr = str(data[4])
    longitudeDirection = str(data[5])
   
    # Get the altitude value
    altitude = float(data[9])

    # Convert the raw gps coordinates to the degrees-minutes format
    latitude = convertGPSData(latitudeStr, latitudeDirection)
    longitude = convertGPSData(longitudeStr, longitudeDirection)
   
    # Set up the projection to convert longitude/latitude to X/Y axis (local coordinates)
    plt.figure(5)
    map = Basemap(projection='aeqd', lon_0 = longitude, lat_0 = latitude,
                  resolution='c', width = 500, height = 500)
                 
    # Convert the initial gps data to local coordinates
    frameOriginX,frameOriginY = map(longitude, latitude)
    frameOriginZ = altitude
   
    # Add the initial gps data to the lists
    x_list.append(frameOriginX)
    y_list.append(frameOriginY)
    z_list.append(frameOriginZ)
    movement_estimation_list.append(0)

    # Read every line in the file
    for line in f:
       # Split the data line
       data = line.split(",")
      
       # Get the latitude coordinate
       latitudeStr = str(data[2])
       latitudeDirection = str(data[3])

       # Get the longitude coordinate
       longitudeStr = str(data[4])
       longitudeDirection = str(data[5])
       
       # Get the altitude value
       altitude = float(data[9])
   
       # Convert the raw gps coordinates to the degrees-minutes format
       latitude = convertGPSData(latitudeStr, latitudeDirection)
       longitude = convertGPSData(longitudeStr, longitudeDirection)
      
       # Convert the initial gps data to local coordinates
       gpsNewRoverX, gpsNewRoverY = map(longitude, latitude)
       gpsNewRoverZ = altitude
      
       # Update the motion estimation
       movementEstimation += math.sqrt(math.pow(gpsNewRoverX - x_list[-1], 2) + math.pow(gpsNewRoverY - y_list[-1], 2) + math.pow(gpsNewRoverZ - z_list[-1], 2))

       # Add the current gps data to the lists
       x_list.append(gpsNewRoverX)
       y_list.append(gpsNewRoverY)
       z_list.append(gpsNewRoverZ)
       movement_estimation_list.append(movementEstimation)

# Close the file
f.close()
print("Done GPS plotting")
print("Motion estimated: {}m".format(round(movement_estimation_list[-1], 3)))

# Plot the data
plt.figure(1)
plt.plot(x_list, y_list)

plt.figure(2)
plt.plot(movement_estimation_list, z_list)

# Pickle and store the gps data
pickle.dump( ["GPS", x_list, y_list, z_list, movement_estimation_list], open( "map.p", "wb" ) )
print ('pickled')

# Show the graph
plt.show()
