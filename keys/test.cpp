/*
 * how to use the rsa functions
 */


#include <ndn-cxx/face.hpp>
#include <ndn-cxx/security/key-chain.hpp>
#include <ndn-cxx/security/signing-info.hpp>
#include <ndn-cxx/security/v2/key-chain.hpp>

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

  char *priv_key = func::read_file((char*)"privkey_a.pem");
  char *pub_key  = func::read_file((char*)"pubkey_a.pub");

  bool is_good;

  char *data = (char*)"hello";
  
  char *sig = func::sign_message(priv_key,data);

  is_good = func::verify_sig(pub_key,data,sig);

  cout << is_good << endl;
    

}
