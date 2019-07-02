/*
 * the producer application
 *
 * This is to be run on the host machine
 *
 */


#include <ndn-cxx/face.hpp>
#include <ndn-cxx/security/key-chain.hpp>
#include <ndn-cxx/security/signing-info.hpp>
#include <ndn-cxx/security/v2/key-chain.hpp>

#include <iostream>
#include <string>


using namespace ndn;
using namespace std;

class Producer : noncopyable
{
public:

	void run()
	{
		m_face.setInterestFilter("/example/endPoint",
				bind(&Producer::onInterest, this, _1, _2),
				RegisterPrefixSuccessCallback(),
				bind(&Producer::onRegisterFailed, this, _1, _2));
		
		m_face.processEvents();
	}

private:

	void onInterest(const InterestFilter& filter, const Interest& interest)
	{
		cout << "[*] Recieved interest\n";
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
	KeyChain m_keyChain;

};



int main(int argc, char *argv[])
{
	Producer producer;

	try {
		producer.run();
	} catch (const std::exception& e) {
		cout << "[!] Error: " << e.what() << "\n";
	}
	return 0;
}
