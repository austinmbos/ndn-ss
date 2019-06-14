

all: consumer producer mservice

consumer: consumer.cpp func.o
	g++ -o c func.o `pkg-config --cflags libndn-cxx` consumer.cpp `pkg-config --libs libndn-cxx`

producer: producer.cpp func.o
	g++ -o p func.o `pkg-config --cflags libndn-cxx` producer.cpp `pkg-config --libs libndn-cxx`

mservice: mservice.cpp func.o
	g++ -o ms func.o `pkg-config --cflags libndn-cxx` mservice.cpp `pkg-config --libs libndn-cxx`

func.o: func.cpp func.h
	g++ -c func.cpp

clean:
	rm c
	rm p
	rm ms
	rm *.o
