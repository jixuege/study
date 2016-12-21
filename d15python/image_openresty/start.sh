#!/bin/bash
docker build -t openresty:1.0 .
docker run -d -it openresty:1.0
