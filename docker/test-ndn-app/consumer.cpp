/*
 * the consumer application:
 * run this on the host machine
 *
 * It should be pointed to the service chain NOT the intended end point
 *
 * The data will be process all the way to the producer, then returned here
 *
 */

#include <ndn-cxx/face.hpp>
#include <iostream>

using namespace ndn;
using namespace std;

class Consumer : noncopyable 
{
public:
	void run()
	{
		Interest interest(Name("/ndn-ss/example/testApp"));
		interest.setInterestLifetime(2_s);
		interest.setMustBeFresh(true);

		m_face.expressInterest(interest,
				bind(&Consumer::onData, this, _1, _2),
				bind(&Consumer::onNack, this, _1, _2),
				bind(&Consumer::onTimeout, this, _1));

		cout << "Sending: " << interest << "\n";
		m_face.processEvents();
	}

private:

	void onData(const Interest& interest, const Data& data)
	{
		cout << "[*] Recieved Data packet back\n";
	}

	void onNack(const Interest& interest, const lp::Nack& nack)
	{
		cout << "[!] Recieved nack: " << nack.getReason() << "\n";
	}

	void onTimeout(const Interest& interest)
	{
		cout << "[!] Timeout !!\n";
	}

private:
	Face m_face;


};

int main(int argc, char *argv[])
{
	Consumer consumer;

	try {
		consumer.run();
	} catch (const std::exception& e) {
		cerr << "[!] Error: " << e.what() << "\n";
	}
	return 0;
}


