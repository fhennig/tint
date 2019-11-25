#!/bin/bash
mkdir -p ~/.virtualenvs/
python3 -m venv ~/.virtualenvs/tint
source ~/.virtualenvs/tint/bin/activate
pip install -r requirements.txt
