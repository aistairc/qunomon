#!/bin/bash

# define zipfile name
FILE_NAME=$(basename "$(realpath "$(dirname "$0")/../")").zip

# make zipfile
cd "$(dirname "$0")"/../deploy/container/
zip -r "../../$FILE_NAME" ./*
