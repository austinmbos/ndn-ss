# if ndn-cxx and NFD installed locally, need to run these commands first
#
# place the below in ~/.bashrc
# export PKG_CONFIG_PATH=$HOME/ndn/ndn-cxx-lib/lib/pkgconfig
# export PATH=$PATH:$HOME/ndn/ndn-NFD-lib/bin



all: producer 

producer: producer.cpp 
	g++ -o p  `pkg-config --cflags libndn-cxx` producer.cpp `pkg-config --libs libndn-cxx`

clean:
	rm p
