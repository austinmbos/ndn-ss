#include <iostream>
#include <curl/curl.h>

using namespace std;

class CurlWrapper {

	private:
		CURL *curl;
		CURLcode res;

	public:
		void send_curl();

}; // end class

void CurlWrapper::send_curl()
{
	curl = curl_easy_init();
	if(curl) {
		curl_easy_setopt(curl,CURLOPT_URL,"http://localhost:5000/sign");
		curl_easy_setopt(curl,CURLOPT_POSTFIELDS,"");

		res = curl_easy_perform(curl);
		cout <<  << "\n";
		/*
		if(res != CURLE_OK) {
			cout << "perform failed\n";
			cout << curl_easy_strerror(res);
		}

		curl_easy_cleanup(curl);
		*/
	}
	curl_global_cleanup();
}

int main(void)
{
	CurlWrapper c;
	c.send_curl();

}
