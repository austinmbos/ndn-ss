

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



