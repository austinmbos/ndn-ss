#include "func.h"


char *func::read_file(const char *file_name)
{
  using namespace std;
  struct stat res;
  int file_size = 0;
  if(stat(file_name,&res) == 0) {
    file_size = res.st_size;
  } else {
    cout << "Error reading file\n";
    exit(0);
  }

  FILE *fp = fopen(file_name,"r");

  char *buffer = (char*)malloc(file_size + 1);
  if(!buffer) {
    cout << "Erro allocating\n";
    exit(0);
  }

  char c;
  int i = 0;
  while((c = getc(fp)) != EOF) {
    buffer[i++] = c;
  }
  buffer[i] = '\0';

  fclose(fp);

  return buffer;

}

void func::handleErrors(void)
{
  ERR_print_errors_fp(stderr);
  abort();
}



int func::encrypt(unsigned char *plaintext, int plaintext_len, unsigned char *key,
            unsigned char *iv, unsigned char *ciphertext)
{

  EVP_CIPHER_CTX *ctx;

  int len;

  int ciphertext_len;

  if(!(ctx = EVP_CIPHER_CTX_new())) handleErrors();

  if( 1 != EVP_EncryptInit_ex(ctx, EVP_aes_256_cbc(),NULL,key,iv)) handleErrors();

  if( 1 != EVP_EncryptUpdate(ctx,ciphertext,&len,plaintext,plaintext_len)) handleErrors();
  ciphertext_len = len;

  if( 1 != EVP_EncryptFinal_ex(ctx,ciphertext + len, &len)) handleErrors();
  ciphertext_len += len;

  EVP_CIPHER_CTX_free(ctx);

  return ciphertext_len;

}

int func::decrypt(unsigned char *ciphertext, int ciphertext_len, unsigned char *key, unsigned char *iv, unsigned char *plaintext)
{

  EVP_CIPHER_CTX *ctx;

  int len;

  int plaintext_len;

  if(!(ctx = EVP_CIPHER_CTX_new())) handleErrors();

  if(1 != EVP_DecryptInit_ex(ctx, EVP_aes_256_cbc(), NULL, key, iv))
    handleErrors();

  if(1 != EVP_DecryptUpdate(ctx, plaintext, &len, ciphertext, ciphertext_len))
    handleErrors();
  plaintext_len = len;

  if(1 != EVP_DecryptFinal_ex(ctx, plaintext + len, &len)) handleErrors();
  plaintext_len += len;

  EVP_CIPHER_CTX_free(ctx);

  return plaintext_len;
  
  return 0;

}



int
func::envelope_seal(EVP_PKEY **pub_key, unsigned char *plaintext, int plaintext_len,
            unsigned char **encrypted_key, int *encrypted_key_len, unsigned char *iv,
            unsigned char *ciphertext)
{
  EVP_CIPHER_CTX *ctx;

  int ciphertext_len;

  int len;

  if(!(ctx = EVP_CIPHER_CTX_new())) handleErrors();

  if(1 != EVP_SealInit(ctx, EVP_aes_256_cbc(), encrypted_key, encrypted_key_len,
        iv, pub_key, 1))
    handleErrors();
  ciphertext_len = len;

  if(1 != EVP_SealUpdate(ctx,ciphertext, &len, plaintext, plaintext_len)) handleErrors();

  if( 1 != EVP_SealFinal(ctx, ciphertext + len, &len)) handleErrors();
  ciphertext_len += len;

  EVP_CIPHER_CTX_free(ctx);

  return ciphertext_len;


}


int
func::envelope_open(EVP_PKEY *priv_key, unsigned char *ciphertext, int ciphertext_len,
            unsigned char *encrypted_key, int encrypted_key_len, unsigned char *iv,
            unsigned char *plaintext)
{

  EVP_CIPHER_CTX *ctx;

  int len;
   int plaintext_len;

   if(!(ctx = EVP_CIPHER_CTX_new())) handleErrors();

   if(1 != EVP_OpenInit(ctx, EVP_aes_256_cbc(), encrypted_key, encrypted_key_len,
         iv,priv_key))
     handleErrors();

   if( 1 != EVP_OpenUpdate(ctx, plaintext, &len, ciphertext,ciphertext_len)) handleErrors();
   plaintext_len = len;

   if(1 != EVP_OpenFinal(ctx, plaintext+len, &len)) handleErrors();
   plaintext_len += len;

   EVP_CIPHER_CTX_free(ctx);

   return plaintext_len;

}


RSA* 
func::create_priv_RSA(const char *key)
{
  RSA *rsa= NULL;
  BIO *keybio = BIO_new_mem_buf((void*)key, -1);
  if(keybio == NULL) handleErrors();

  rsa = PEM_read_bio_RSAPrivateKey(keybio, &rsa, NULL,NULL);
  return rsa;
}

bool
func::RSA_sign(RSA *rsa, const unsigned char *plaintext, size_t plaintext_len,
    unsigned char **ciphertext, size_t *ciphertext_len)
{
  EVP_MD_CTX * RSA_sign_CTX = EVP_MD_CTX_create();
  EVP_PKEY * priv_key = EVP_PKEY_new();
  EVP_PKEY_assign_RSA(priv_key, rsa);

  if(EVP_DigestSignInit(RSA_sign_CTX, NULL, EVP_sha256(),NULL,priv_key)<=0)
    return false;

  if(EVP_DigestSignUpdate(RSA_sign_CTX,plaintext,plaintext_len)<=0)
    return false;

  if(EVP_DigestSignFinal(RSA_sign_CTX,NULL,ciphertext_len)<=0)
    return false;

  *ciphertext = (unsigned char*)malloc(*ciphertext_len);
  if(EVP_DigestSignFinal(RSA_sign_CTX, *ciphertext,ciphertext_len)<=0)
    return false;

  EVP_MD_CTX_free(RSA_sign_CTX);
  return true;


}

void
func::base64_encode(const unsigned char *buffer, size_t length, char **base64_text)
{

  BIO *bio, *b64;
  BUF_MEM *bufferPtr;

  b64 = BIO_new(BIO_f_base64());
  bio = BIO_new(BIO_s_mem());
  bio = BIO_push(b64, bio);


  BIO_write(bio, buffer, length);
  BIO_flush(bio);
  BIO_get_mem_ptr(bio, &bufferPtr);
  BIO_set_close(bio, BIO_NOCLOSE);
  BIO_free_all(bio);

  *base64_text=(*bufferPtr).data;
}

char*
func::sign_message(const char* priv_key,const char* plaintext)
{

  RSA* priv_RSA = create_priv_RSA(priv_key);
  unsigned char* ciphertext;
  char* base64_text;
  size_t ciphertext_len;
  RSA_sign(priv_RSA,(unsigned char*) plaintext, strlen(plaintext), &ciphertext, &ciphertext_len);
  base64_encode(ciphertext, ciphertext_len, &base64_text);
  free(ciphertext);
  return base64_text;

}

size_t
func::calc_decode_len(const char* base64_input)
{

  size_t len = strlen(base64_input), padding = 0;

  if(base64_input[len-1] == '=' && base64_input[len-2] == '=')
    padding = 2;
  else if(base64_input[len-1] == '=')
    padding = 1;
  return(len*3)/4 - padding;
  
}

void
func::base64_decode(const char* base64_text, unsigned char** buffer, size_t* length)
{

  BIO *bio, *b64;

  int decode_len = calc_decode_len(base64_text);
  *buffer = (unsigned char*)malloc(decode_len + 1);
  (*buffer)[decode_len] = '\0';

  bio = BIO_new_mem_buf(base64_text, -1);
  b64 = BIO_new(BIO_f_base64());
  bio = BIO_push(b64,bio);

  *length = BIO_read(bio,*buffer, strlen(base64_text));
  BIO_free_all(bio);


}

RSA*
func::create_pub_RSA(const char* key)
{

  RSA* rsa = NULL;
  BIO* keybio;

  keybio = BIO_new_mem_buf((void*)key, -1);
  if(keybio==NULL) return 0;

  rsa = PEM_read_bio_RSA_PUBKEY(keybio, &rsa,NULL,NULL);
  return rsa;

}

bool
func::RSA_verify_sig(RSA* rsa, unsigned char* msg_hash, size_t hash_len,
      const char* msg, size_t msg_len, bool* is_auth)
{

  *is_auth = false;
  EVP_PKEY* pub_key = EVP_PKEY_new();
  EVP_PKEY_assign_RSA(pub_key,rsa);
  EVP_MD_CTX* RSA_verify_CTX = EVP_MD_CTX_create();

  if(EVP_DigestVerifyInit(RSA_verify_CTX, NULL, EVP_sha256(),NULL,pub_key)<=0) 
    return false;

  if(EVP_DigestVerifyUpdate(RSA_verify_CTX,msg,msg_len)<=0)
    return false;

  int auth_status = EVP_DigestVerifyFinal(RSA_verify_CTX,msg_hash,hash_len);
  if(auth_status == 1)
  {
    *is_auth = true;
    EVP_MD_CTX_free(RSA_verify_CTX);
    return true;
  }
  else if(auth_status == 0)
  {
    *is_auth = false;
    EVP_MD_CTX_free(RSA_verify_CTX);
    return true;
  }
  else
  {
    *is_auth = false;
    EVP_MD_CTX_free(RSA_verify_CTX);
    return false;
  }
}

bool
func::verify_sig(const char* pub_key, const char* plaintext, char* base64_sig)
{

  RSA* pub_rsa = create_pub_RSA(pub_key);
  unsigned char* ciphertext;
  size_t ciphertext_len;
  bool is_auth;
  base64_decode(base64_sig,&ciphertext,&ciphertext_len);
  bool res = RSA_verify_sig(pub_rsa,ciphertext,ciphertext_len,
      plaintext,strlen(plaintext),&is_auth);
  return (res & is_auth);

}




