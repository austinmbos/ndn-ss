/*
 * how to use the rsa functions
 */


#include <ndn-cxx/face.hpp>
#include <ndn-cxx/security/key-chain.hpp>
#include <ndn-cxx/security/signing-info.hpp>
#include <ndn-cxx/security/v2/key-chain.hpp>
#include <ndn-cxx/security/pib/pib-sqlite3.hpp>

#include <iostream>
#include <fstream>
#include <stdio.h>
#include <sys/stat.h>
#include <stdlib.h>

#include "func.h"


using namespace std;
using namespace ndn;
using namespace security;
using namespace pib;


int main(int argc, char** argv)
{
  cout << "[*] Testing keys\n";
  Name key_name = "/priv-key";
  Name n_name = "/test";
  Name i_name ="/name";

  PibSqlite3 pib;

  char *priv_key = func::read_file((char*)"privkey_a.pem");
  char *pub_key  = func::read_file((char*)"pubkey_a.pub");

  /* create and init a pib */
  pib.addKey(i_name,key_name,(uint8_t*)priv_key,strlen(priv_key));
  pib.setTpmLocator("/home/abos/.ndn");

  KeyChain k_chain;
  Identity i = k_chain.createIdentity(n_name);
  pib.addIdentity(n_name);

}
