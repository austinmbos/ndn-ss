
#include <ndn-cxx/face.hpp>
#include <ndn-cxx/security/key-chain.hpp>
#include <ndn-cxx/security/signing-info.hpp>
#include <ndn-cxx/security/v2/key-chain.hpp>

#include <iostream>
#include <string>

#include "func.h"

namespace ndn {
namespace examples {

class Producer : noncopyable
{
public:

  void
  init()
  {
    priv_key_a = func::read_file((char*)"keys/privkey_a.pem");
    priv_key_b = func::read_file((char*)"keys/privkey_b.pem");
    pub_key_a  = func::read_file((char*)"keys/pubkey_a.pub");
  }

  void
  run()
  {
    m_face.setInterestFilter("/example/testApp",
                             bind(&Producer::onInterest, this, _1, _2),
                             RegisterPrefixSuccessCallback(),
                             bind(&Producer::onRegisterFailed, this, _1, _2));
    m_face.processEvents();
  }

private:
  void
  onInterest(const InterestFilter& filter, const Interest& interest)
  {
    using namespace std;
    cout << "[*] REcieved interest\n";
    

    Name dataName(interest.getName());
    dataName
      .append("testApp") // add "testApp" component to Interest name
      .appendVersion();  // add "version" component (current UNIX timestamp in milliseconds)

    char *content = (char*)"HELLO";

    char *sig = func::sign_message(priv_key_a,content);
    size_t sig_len = strlen(sig);

    char *c_data = (char*)malloc(5 + sig_len + 1);

    // combine the content and the sig
    sprintf(c_data,"%s%s",content,sig);

    bool is_good = func::verify_sig(pub_key_a,content,sig);

    shared_ptr<Data> data = make_shared<Data>();
    data->setName(dataName);
    data->setFreshnessPeriod(1_s); 
    data->setContent(reinterpret_cast<const uint8_t*>(c_data), sig_len + 6);

    m_keyChain.sign(*data);
    
    m_face.put(*data);
  }


  void
  onRegisterFailed(const Name& prefix, const std::string& reason)
  {
    std::cerr << "ERROR: Failed to register prefix \""
              << prefix << "\" in local hub's daemon (" << reason << ")"
              << std::endl;
    m_face.shutdown();
  }

private:
  char *priv_key_a;
  char *pub_key_a;
  char *priv_key_b;
  Face m_face;
  KeyChain m_keyChain;
};

} // namespace examples
} // namespace ndn

int
main(int argc, char** argv)
{
  ndn::examples::Producer producer;
  producer.init();

  try {
    producer.run();
  }
  catch (const std::exception& e) {
    std::cerr << "ERROR: " << e.what() << std::endl;
  }
  return 0;
}
