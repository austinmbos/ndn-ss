/*
 * the producer application
 */


#include <ndn-cxx/face.hpp>
#include <ndn-cxx/security/key-chain.hpp>
#include <ndn-cxx/security/signing-info.hpp>
#include <ndn-cxx/security/v2/key-chain.hpp>

#include <iostream>
#include <string>
#include <fstream>
#include <algorithm>


using namespace ndn;
using namespace std;


class Producer : noncopyable
{
public:

	void run()
	{
		m_face.setInterestFilter("/ndn-ss/ss-entry",
				bind(&Producer::onInterest, this, _1, _2),
				RegisterPrefixSuccessCallback(),
				bind(&Producer::onRegisterFailed, this, _1, _2));
		
		m_face.processEvents();
	}

	void sendToNext(const Interest& interest)
	{
		// change the name
		Name name = Name("/ndn-ss/sig-ver");
		Name n = interest.getName();
		auto it = n.begin();
		it++;
		it++;
		while(it != n.end()) {
			cout << "getting name\n";
			name.append(*it);
			it++;
		}

		cout << "New name: " << name << "\n";

		// create the new interest with the name for the next service
		Interest inter(name);
		inter.setInterestLifetime(2_s); // 2 seconds
		inter.setMustBeFresh(true);
		m_face.expressInterest(inter,
							   bind(&Producer::onData, this,  _1, _2),
							   bind(&Producer::onNack, this, _1, _2),
							   bind(&Producer::onTimeout, this, _1));

		std::cout << "Sending " << inter << std::endl;

		// processEvents will block until the requested data received or timeout occurs
		m_face.processEvents();
	}

private:

	Data onData(const Interest& interest, const Data& data)
	{
		using namespace std;
		cout << "[*] Received data packet back\n";
		//cout << "[*] Content\n" << data.getContent().value() << "\n";
		return data;
	}

	void onNack(const Interest& interest, const lp::Nack& nack)
	{
		std::cout << "received Nack with reason " << nack.getReason()
				  << " for interest " << interest << std::endl;
	}

	void onTimeout(const Interest& interest)
	{
		std::cout << "Timeout " << interest << std::endl;
	}


	void onInterest(const InterestFilter& filter, const Interest& interest)
	{
		cout << "[*] Recieved interest\n";

		this->sendToNext(interest);
		
		Name name(interest.getName());
		name.append("testing").appendVersion();

		char *content = (char*)"HELLO";

		shared_ptr<Data> data = make_shared<Data>();
		data->setName(name);
		data->setFreshnessPeriod(1_s);
		data->setContent(reinterpret_cast<const uint8_t*>(content),strlen(content));

		m_keyChain.sign(*data);
		m_face.put(*data);
	}

	void onRegisterFailed(const Name& prefix, const string& reason)
	{
		cout << "[*] Failed to register prefix: " << reason << "\n";
		m_face.shutdown();
	}


private:
	Face m_face;
	Face m_sendFace;
	KeyChain m_keyChain;

};



int main(int argc, char *argv[])
{
	cout << "=== starting nfd-entry ===\n";

	Producer producer;

	try {
		producer.run();
	} catch (const std::exception& e) {
		cout << "[!] Error: " << e.what() << "\n";
	}
	return 0;
}
