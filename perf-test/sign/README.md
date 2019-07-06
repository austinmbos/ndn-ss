# signing data timing test

- If the docker image is already build
```
cp ../data/list_of_data.json .
python3 sign.py
docker run -d -v results:/app/results {image-name}
```

- To build the docker image
```
docker build -t {image-name} .
```
