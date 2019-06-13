all: consumer producer mservice

consumer: consumer.cpp
	g++ -o c `pkg-config --cflags libndn-cxx` consumer.cpp `pkg-config --libs libndn-cxx`

producer: producer.cpp
	g++ -o p `pkg-config --cflags libndn-cxx` producer.cpp `pkg-config --libs libndn-cxx`

mservice: mservice.cpp
	g++ -o ms `pkg-config --cflags libndn-cxx` mservice.cpp `pkg-config --libs libndn-cxx`
