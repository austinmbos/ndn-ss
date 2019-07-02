FROM ubuntu
COPY test.sh /
WORKDIR /
# install the deps
RUN chmod +x test.sh

# run the install script for ndn-cxx && NFD
RUN bash test.sh

# specify the entry for the container
ENTRYPOINT ["/bin/bash"]

# pass in CMD [""] here for command to execute on container run

