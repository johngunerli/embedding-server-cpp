# c++ image embedding server

this project implements a web server in c++ that processes images and generates embeddings using the dino vit model.

## overview

the server provides a rest api endpoint that:
1. accepts image data as json
2. processes it through a vision transformer (vit) model
3. returns image embeddings

## components

- `server.cpp` - main c++ server using the crow framework
- `embed_image.py` - python script for generating image embeddings using dino vit
- `array_converter.py` - utility script for testing the api with sample images

## prerequisites

- c++ compiler with c++11 support
- python 3.x
- cmake
- pip packages:
  - torch
  - transformers
  - numpy
  - pillow
  - requests

## installation

1. clone the repository
2. build the project:
```sh
cmake .
make
```

## usage

1. start the server:
```sh
./server
```

2. the server will listen on port 8080

3. send post requests to `/embed` endpoint with json body in the format:
```json
{
    "image": [[[r,g,b], ...], ...]  // 3d array of rgb values
}
```

4. the server will return embeddings as json:
```json
{
    "embedding": [...]  // array of embedding values
}
```

## testing

you can use `array_converter.py` to test the api with a sample image:
```sh
python3 array_converter.py
```

this will:
1. download a sample image
2. convert it to the required format
3. send it to the server
4. print the resulting embeddings

## api endpoints

- `get /` - returns basic usage instructions
- `post /embed` - accepts image data and returns embeddings