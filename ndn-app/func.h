#ifndef func_h
#define func_h
#include <iostream>
#include <fstream>
#include <openssl/conf.h>
#include <openssl/evp.h>
#include <openssl/err.h>
#include <openssl/rsa.h>
#include <openssl/pem.h>
#include <string.h>
#include <sys/stat.h>

class func
{
  private:

  public:
  static char *read_file(const char *file_name);
  
  static void handleErrors(void);

  static int encrypt(unsigned char *plaintext, int plaintext_len, unsigned char *key,
              unsigned char *iv, unsigned char *ciphertext);


  static int decrypt(unsigned char *ciphertext, int ciphertext_len, unsigned char *key,
               unsigned char *iv, unsigned char *plaintext);


  static int envelope_seal(EVP_PKEY **pub_key, unsigned char *plaintext, int plaintext_len,
              unsigned char **encrypted_key, int *encrypted_key_len, unsigned char *iv,
              unsigned char *ciphertext);

  static int envelope_open(EVP_PKEY *priv_key, unsigned char *ciphertext, int ciphertext_len,
              unsigned char *encrypted_key, int encrypted_key_len, unsigned char *iv,
              unsigned char *plaintext);

  static RSA *create_priv_RSA(const char *key);

  static bool RSA_sign(RSA* rsa, const unsigned char *plaintext, size_t plaintext_len, 
            unsigned char **ciphertext, size_t *ciphertext_len);

  static void base64_encode(const unsigned char *buffer, size_t length, char **base64_text);

  static char *sign_message(const char* priv_key,const char* plaintext);

  static size_t calc_decode_len(const char* base64_input);

  static void base64_decode(const char* base64_text, unsigned char** buffer, size_t* length);

  static RSA *create_pub_RSA(const char* key);

  static bool RSA_verify_sig(RSA* rsa, unsigned char* msg_hash, size_t hash_len,
      const char* msg, size_t msg_len, bool* is_auth);

  static bool verify_sig(const char* pub_key, const char* plaintext, 
      char* base64_sig);

};

#endif
