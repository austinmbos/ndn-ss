/*
 * Intended to be the microservice application
 * basically a proxy
 */


#include <ndn-cxx/face.hpp>
#include <ndn-cxx/security/key-chain.hpp>

#include <iostream>

namespace ndn {
namespace examples {

class Mservice : noncopyable
{
public:
  void
  run()
  {
    m_face.setInterestFilter("/ss/example/testApp",
                             bind(&Mservice::onInterest, this, _1, _2),
                             RegisterPrefixSuccessCallback(),
                             bind(&Mservice::onRegisterFailed, this, _1, _2));
    m_face.processEvents();
  }

  /* used to 'forward' an interest
   */
  void
  send_I()
  {
    Interest interest(Name("/example/testApp/randomData"));
    interest.setInterestLifetime(2_s); // 2 seconds
    interest.setMustBeFresh(true);

    m_face_I.expressInterest(interest,
                           bind(&Mservice::onData, this,  _1, _2),
                           bind(&Mservice::onNack, this, _1, _2),
                           bind(&Mservice::onTimeout, this, _1));

    //std::cout << "Sending " << interest << std::endl;
    m_face_I.processEvents();
  }


private:
  void
  onInterest(const InterestFilter& filter, const Interest& interest)
  {
    using namespace std;
    
    cout << "[SS] Received interest\n";
    cout << "[SS] Sending interest to main producer\n";
    send_I();

    // Create new name, based on Interest's name
    Name dataName(interest.getName());
    dataName
      .append("testAppss") // add "testApp" component to Interest name
      .appendVersion();  // add "version" component (current UNIX timestamp in milliseconds)

    static const std::string content = "HELLO KITTY";

    // Create Data packet
    shared_ptr<Data> data = make_shared<Data>();
    data->setName(dataName);
    data->setFreshnessPeriod(10_s); // 10 seconds
    data->setContent(reinterpret_cast<const uint8_t*>(content.data()), content.size());

    m_keyChain.sign(*data);

    //std::cout << ">> D: " << *data << std::endl;
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

/*************************************************************/
  void
  onData(const Interest& interest, const Data& data)
  {
    using namespace std;

    cout << "[*] Received data packet back (from main producer)\n";
  }

  void
  onNack(const Interest& interest, const lp::Nack& nack)
  {
    std::cout << "received Nack with reason " << nack.getReason()
              << " for interest " << interest << std::endl;
  }

  void
  onTimeout(const Interest& interest)
  {
    std::cout << "Timeout " << interest << std::endl;
  }

private:
  Face m_face_I;

/***************************************************************/

private:
  Face m_face;
  KeyChain m_keyChain;
};

} // namespace examples
} // namespace ndn

int
main(int argc, char** argv)
{
  ndn::examples::Mservice producer;
  try {
    producer.run();
  }
  catch (const std::exception& e) {
    std::cerr << "ERROR: " << e.what() << std::endl;
  }
  return 0;
}
