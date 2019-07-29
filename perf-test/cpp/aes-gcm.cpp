#include <iostream>
#include <cstring>
#include <fstream>
#include <vector>


#include <openssl/conf.h>
#include <openssl/evp.h>
#include <openssl/err.h>

void quit() { std::cout << "Quitting\n"; exit(0); }

int aes_gcm_enc(unsigned char *plaintext, int plaintext_len,
			unsigned char *aad, int aad_len,
			unsigned char *key,
			unsigned char *iv, int iv_len,
			unsigned char *ciphertext,
			unsigned char *tag)
{
	EVP_CIPHER_CTX *ctx;
	int len;
	int ciphertext_len;

	if(!(ctx = EVP_CIPHER_CTX_new())) quit();
	if(1 != EVP_EncryptInit_ex(ctx,EVP_aes_256_gcm(),NULL,NULL,NULL)) quit();
	if(1 != EVP_CIPHER_CTX_ctrl(ctx,EVP_CTRL_GCM_SET_IVLEN,iv_len,NULL)) quit();
	if(1 != EVP_EncryptInit_ex(ctx,NULL,NULL,key,iv)) quit();
	if(1 != EVP_EncryptUpdate(ctx,NULL,&len,aad,aad_len)) quit();
	if(1 != EVP_EncryptUpdate(ctx,ciphertext,&len,plaintext,plaintext_len)) quit();
	ciphertext_len = len;
	if(1 != EVP_EncryptFinal_ex(ctx,ciphertext + len, &len)) quit();
	ciphertext_len += len;
	if(1 != EVP_CIPHER_CTX_ctrl(ctx,EVP_CTRL_GCM_GET_TAG,16,tag)) quit();
	EVP_CIPHER_CTX_free(ctx);
	return ciphertext_len;
}

int aes_gcm_dec(unsigned char *ciphertext, int ciphertext_len,
				unsigned char *aad, int aad_len,
				unsigned char *tag,
				unsigned char *key,
				unsigned char *iv, int iv_len,
				unsigned char *plaintext)
{
	EVP_CIPHER_CTX *ctx;
	int len;
	int pt_len;
	int ret;

	if(!(ctx = EVP_CIPHER_CTX_new())) quit();
	if(!EVP_DecryptInit_ex(ctx,EVP_aes_256_gcm(),NULL,NULL,NULL)) quit();
	if(!EVP_CIPHER_CTX_ctrl(ctx,EVP_CTRL_GCM_SET_IVLEN,iv_len,NULL)) quit();
	if(!EVP_DecryptInit_ex(ctx,NULL,NULL,key,iv)) quit();
	if(!EVP_DecryptUpdate(ctx,NULL,&len,aad,aad_len)) quit();
	if(!EVP_DecryptUpdate(ctx,plaintext,&len,ciphertext,ciphertext_len)) quit();
	pt_len = len;
	if(!EVP_CIPHER_CTX_ctrl(ctx,EVP_CTRL_GCM_SET_TAG,16,tag)) quit();
	ret = EVP_DecryptFinal_ex(ctx,plaintext + len,&len);
	EVP_CIPHER_CTX_free(ctx);
	if(ret > 0) {
		pt_len += len;
		return pt_len;
	} else {
		return -1;
	}

}

int main(int argc, char *argv[])
{
	if(argc < 2) quit();	

	std::string line;
	std::vector<std::string> list_of_data;
	std::ifstream in_file;
	in_file.open("data/list_of_data.txt",std::ios::in);

	while( in_file >> line) {
		list_of_data.push_back(line);
	}
	in_file.close();


	unsigned char *key = (unsigned char *)"01234567890123456789012345678901";
	unsigned char *iv = (unsigned char *)"1123456789012345";
	size_t iv_len = 16;

	unsigned char *pt = (unsigned char *)"this is the plaintext, here";
	unsigned char *aad = (unsigned char *)"not to be encrypted";
	unsigned char ct[128];
	unsigned char f_pt[128];
	unsigned char tag[16];
	int ct_len;
	int pt_len;



	std::cout << "Running for encryption\n";
	auto it = list_of_data.begin();
	while(it != list_of_data.end()) {
		ct_len = aes_gcm_enc((unsigned char*)(*it).c_str(),(*it).length(),
				aad,strlen((char*)aad),key,iv,iv_len,ct,tag);
		it++;
	}

	list_of_data.clear();
	exit(0);
}
