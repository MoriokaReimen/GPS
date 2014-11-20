wgs84.o: wgs84.cpp
	g++ -std=c++11 -Wall -fPIC -DPIC -I. -I /usr/include/python2.6/ -c wgs84.cpp

python_wgs84.o: python_wgs84.cpp
	g++ -std=c++11 -Wall -fPIC -DPIC -I. -I /usr/include/python2.6/ -c python_wgs84.cpp

wgs84.so: python_wgs84.o wgs84.o
	g++ -shared -fPIC -DPIC python_wgs84.o wgs84.o -L/usr/lib/ -lboost_python -L/usr/lib/python2.6/ -lpython2.6 -o wgs84.so

all: wgs84.so

clean:
	rm -f *.o *.so

.PHONY: all clean
