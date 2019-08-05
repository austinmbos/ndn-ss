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
	o_file << '1';
	o_file.close();

	o_file.open("shared/sym-dec.sem");
	o_file << '1';
	o_file.close();

	o_file.open("shared/final.sem");
	o_file << '1';
	o_file.close();

	o_file.open("shared/in-progress.sem");
	o_file << '0';
	o_file.close();
}



class Producer : noncopyable
{
public:

	Producer(fstream &inProgress,
				fstream &sigVer,
				fstream &finalF,
				fstream &data) :
		inProgressFile(inProgress),
		sigVerFile(sigVer),
		finalFile(finalF),
		dataFile(data)

	{
		cout << "[*] initialize Producer\n";
	}

	void setLock(fstream &str, int lock_status)
	{
		str.clear();
		str.seekg(0);
		str << lock_status;
	}

	int readLock(fstream &str)
	{
		str.clear();
		str.seekg(0);
		int x;
		str >> x;
		return x;
	}

	void run()
	{
		this->sigVerFile << "lksdjflsfjksjfdj";
		this->m_switch = 1;
		this->m_count = 1;
		this->m_lock_status = 0;
		m_face.setInterestFilter("/ndn-ss",
				bind(&Producer::onInterest, this, _1, _2),
				RegisterPrefixSuccessCallback(),
				bind(&Producer::onRegisterFailed, this, _1, _2));
		
		m_face.processEvents();
	}


private:

	void onInterest(const InterestFilter& filter, const Interest& interest)
	{
		cout << "[*] Recieved interest count: " << this->m_count++ << "\n";
		
		Name n = interest.getName();

		// dump the data for the micro service 
		dataFile.clear();
		dataFile.seekg(0);
		for(auto it = n.begin(); it != n.end(); it++) 
			dataFile << *it << "\n";
		
		// alert the sig-ver
		// 2 for sig-ver-1 and 3 for sig-ver-2
		if(m_switch) 
			setLock(sigVerFile,2);
		else 
			setLock(sigVerFile,3);

		m_switch = !m_switch; // switch between 1 and 0
#ifdef SINGLE
		m_switch = 1;
#endif

		// wait here for microservice chain to complete
		// while final.sem == 1 { wait }

		// wait for the service chain to finish here
		m_lock_status = readLock(finalFile);
		while(m_lock_status) {
			m_lock_status = readLock(finalFile);
			usleep(100);
		}
		
		cout << "asdassdfafd\n";

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
	int m_count;
	int m_lock_status;

	fstream &inProgressFile;
	fstream &sigVerFile;
	fstream &finalFile;
	fstream &dataFile;

};



int main(int argc, char *argv[])
{

	std::fstream tt("test.txt");
	tt << "lskjdldsjf";
	exit(0);

	cout << "=== starting nfd-entry ===\n";
#ifdef SINGLE
	cout << "!!! routing to a single signature verifier !!!\n";
#endif
	resetFiles();




	cout << "[*] Opening file's\n";
	fstream inP("shared/in-progress.sem",fstream::in|fstream::out);
	fstream sV("shared/sig-ver.sem",fstream::in | fstream::out);
	fstream fF("shared/final.sem",fstream::in|fstream::out);
	fstream dF("shared/data.first.txt",fstream::in|fstream::out);
	cout << "[*] files opened\n";

	sV.flush();
	sV.clear();
	sV.seekp(0);
	sV << "lskjfkldsfjds";
	exit(0);


	Producer producer(inP,sV,fF,dF);

	try {
		//producer.init();
		producer.run();
		//producer.setLock(producer.sigVerFile,2);
	} catch (const std::exception& e) {
		cout << "[!] Error: " << e.what() << "\n";
	}
	return 0;
}
