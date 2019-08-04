#include <ndn-cxx/face.hpp>
#include <ndn-cxx/security/key-chain.hpp>
#include <ndn-cxx/security/signing-info.hpp>
#include <ndn-cxx/security/v2/key-chain.hpp>
#include <iostream>
#include <string>
#include <fstream>
#include <unistd.h>
using namespace ndn;
using namespace std;


static void resetFiles()
{
	ofstream o_file;
	
	o_file.open("shared/sig-ver.sem");
	o_file << "1";
	o_file.close();

	o_file.open("shared/sym-dec.sem");
	o_file << "1";
	o_file.close();

	o_file.open("shared/final.sem");
	o_file << "1";
	o_file.close();
}

static void setLock(string filename,char lock_status)
{
	ofstream o_file;
	o_file.open(filename);
	o_file << lock_status;
	o_file.close();
}


class Producer : noncopyable
{
public:

	void run()
	{
		this->m_switch = 1;
		m_face.setInterestFilter("/ndn-ss",
				bind(&Producer::onInterest, this, _1, _2),
				RegisterPrefixSuccessCallback(),
				bind(&Producer::onRegisterFailed, this, _1, _2));
		
		m_face.processEvents();
	}

private:

	void onInterest(const InterestFilter& filter, const Interest& interest)
	{
		cout << "[*] Recieved interest\n";

		Name n = interest.getName();
		ofstream o_file;
		o_file.open("shared/data.first.txt");

		// dump the data for the micro service 
		for(auto it = n.begin(); it != n.end(); it++) {
			//cout << *it << "\n";
			o_file << *it << "\n";
		}
		o_file.close();

		// alert the sig-ver
		// 2 for sig-ver-1 and 3 for sig-ver-2
		if(m_switch) {
			setLock("shared/sig-ver.sem",'2');
		} else {
			setLock("shared/sig-ver.sem",'3');
		}
		m_switch = !m_switch; // switch between 1 and 0
		cout << "[*] Wrote switch for sig-ver\n";

		// wait here for microservice chain to complete
		// while final.sem == 1 { wait }
		int lock_status = 1;
		ifstream in_file;
		in_file.open("shared/final.sem");

		// wait for the service chain to finish here
		while(lock_status) {
			in_file.clear();
			in_file.seekg(0,ios::beg);
			in_file >> lock_status;
			usleep(100);
		}
		

		// should read in final data here, for now return HELLO

		resetFiles();
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
	int m_switch; // switch between two sig-ver services
};



int main(int argc, char *argv[])
{
	cout << "=== starting nfd-entry ===\n";
	resetFiles();

	Producer producer;

	try {
		producer.run();
	} catch (const std::exception& e) {
		cout << "[!] Error: " << e.what() << "\n";
	}
	return 0;
}
