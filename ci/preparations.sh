#!/bin/bash

mkdir -p ~/.cache
cp -r ./.cache/pip ~/.cache/pip
pip install -r requirements.txt
