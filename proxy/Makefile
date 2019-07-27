# if ndn-cxx and NFD installed locally, need to run these commands first
#
# export PKG_CONFIG_PATH=$HOME/ndn/ndn-cxx-lib/lib/pkgconfig
# export PATH=$PATH:$HOME/ndn/ndn-NFD-lib/bin



all: consumer producer 

consumer: consumer.cpp 
	g++ -o c `pkg-config --cflags libndn-cxx` consumer.cpp `pkg-config --libs libndn-cxx`

producer: producer.cpp 
	g++ -o p  `pkg-config --cflags libndn-cxx` producer.cpp `pkg-config --libs libndn-cxx`

clean:
	rm c
	rm p
