# A test ndn app to test the service chain

- There should be a consumer and producer. Both run on the host, so start the
  producer first, then the client, on the same machine. The final NFD container
  will send an interest for the producer on the host. 

- The producer on the host system is the end point.

- An example to think of is the consumer is me, wanting to watch a movie, and
  the producer is netflix, with my movie. and the docker containers are the
  service chain that will process data going both ways.

- Should be a simple ndn application, send an interest, get back a data

- The purpose of this application is to test data is flowing through the service
  chain



