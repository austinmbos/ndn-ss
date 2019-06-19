

key mgmt


### create pkcs8 keys

-  priv key
```
openssl genpkey -out rsakey.pem -algorithm RSA -pkeyopt rsa_keygen_bits:2048
```

- pub key
```
openssl rsa -in mykey.pem -pubout > mykey.pub
```


## Notes on key management

All key/certs/identies managed by KeyChain 
identies expressed by namespace ie /netflix/blackpanther
/<identity-name>/[key-id]
identies can have more than one key

Private part is stored in TPM
Public part is stred in PIB (public-key information base
most important of PIB is certs of public keys
the cert binds the pubkey to the name(identity)
a public key may have more than cert asscoiated with it.
 

### Key Management
- KeyChain manages all
```
KeyChain keyChain;
Name defaultCertName = keyChain.createIdentity(identity);
```
- Create keys manually
```
KeyChain keyChain;
Name alice("/ndn/test/alice");

Name aliceKeyName = keyChain.generateRsaKeyPair(alice);
keyChain.setDefaultKeyNameForIdentity(aliceKeyName);

Name aliceKeyName2 = keyChain.generateRsaKeyPairAsDefault(alice);
```


### Signing data









