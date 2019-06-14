all: test

test: test.cpp func.o
	g++ -o test func.o `pkg-config --cflags libndn-cxx` test.cpp `pkg-config --libs libndn-cxx`

func.o: func.cpp func.h
	g++ -c func.cpp

clean:
	rm test
	rm *.o
