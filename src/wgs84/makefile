#
# Makefile for wgs84
# author: Kei Nakata
# Date: Nov. 11.21.2014
# Compiler: gcc4.7.2
# python: python2.7
#
wgs84.o: wgs84.cpp wgs84.hpp
	g++ -std=c++11 -Wall -Ofast -fPIC -DPIC -I. -I /usr/include/python2.6/ -c wgs84.cpp

python_wgs84.o: python_wgs84.cpp wgs84.hpp
	g++ -std=c++11 -Wall -Ofast -fPIC -DPIC -I. -I /usr/include/python2.6/ -c python_wgs84.cpp

wgs84.so: python_wgs84.o wgs84.o
	g++ -shared -fPIC -Ofast -DPIC python_wgs84.o wgs84.o -L/usr/lib/ -lboost_python -L/usr/lib/python2.6/ -lpython2.6 -o wgs84.so

all: wgs84.so wgs84.o

python: wgs84.so

clean:
	rm -f *.o *.so

.PHONY: all clean python
