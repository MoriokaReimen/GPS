#
# Makefile for wgs84
# author: Kei Nakata
# Date: Nov. 11.21.2014
# Compiler: gcc4.7.2
# python: python2.7
CXX = g++
RELEASE_FLAG = -std=c++11 -Wall -Ofast -fPIC -DPIC
DEBUG_FLAG = -std=c++11 -Wall -g -fPIC -DPIC

#relase
./build/wgs84-release.o: ./src/wgs84.cpp ./include/wgs84.hpp
	g++ $(RELEASE_FLAG) -I./include/ -I/usr/include/ -c ./src/wgs84.cpp -o ./build/wgs84-release.o

./build/python_wgs84-release.o: ./src/python_wgs84.cpp ./include/wgs84.hpp
	g++ $(RELEASE_FLAG) -I./include/ -I/usr/include/python2.6/ -c ./src/python_wgs84.cpp -o ./build/python_wgs84-release.o

./lib/wgs84.so: ./build/python_wgs84-release.o ./build/wgs84-release.o
	g++ -shared -fPIC -Ofast -DPIC ./build/python_wgs84-release.o ./build/wgs84-release.o -L/usr/lib/ -lboost_python -L/usr/lib/python2.6/ -lpython2.6 -o ./lib/wgs84.so

release: ./lib/wgs84.so ./build/wgs84-release.o ./build/wgs84-release.o

#debug
./build/wgs84-debug.o: ./src/wgs84.cpp ./include/wgs84.hpp
	g++ $(DEBUG_FLAG) -I./include/ -I/usr/include/ -c ./src/wgs84.cpp -o ./build/wgs84-debug.o

./build/python_wgs84-debug.o: ./src/python_wgs84.cpp ./include/wgs84.hpp
	g++ $(debug_FLAG) -I./include/ -I/usr/include/python2.6/ -c ./src/python_wgs84.cpp -o ./build/python_wgs84-debug.o

./lib/wgs84d.so: ./build/python_wgs84-debug.o ./build/wgs84-debug.o
	g++ -shared -fPIC -Ofast -DPIC ./build/python_wgs84-debug.o ./build/wgs84-debug.o -L/usr/lib/ -lboost_python -L/usr/lib/python2.6/ -lpython2.6 -o ./lib/wgs84.so

debug: ./lib/wgs84d.so ./build/wgs84-debug.o ./build/wgs84-debug.o

all: release debug

clean:
	rm -f ./build/*.o *.so

.PHONY: all clean python
