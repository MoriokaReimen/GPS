blh2ecef.o: blh2ecef.cpp
	g++ -std=c++11 -Wall -fPIC -DPIC -I. -I /usr/include/python2.6/ -c blh2ecef.cpp

ecef.o: ecef.cpp
	g++ -std=c++11 -Wall -fPIC -DPIC -I. -I /usr/include/python2.6/ -c ecef.cpp

ecef.so: ecef.o blh2ecef.o
	g++ -shared -fPIC -DPIC ecef.o blh2ecef.o -L/usr/lib/ -lboost_python -L/usr/lib/python2.6/ -lpython2.6 -o ecef.so

all: ecef.so

clean:
	rm -f *.o *.so

.PHONY: all clean
