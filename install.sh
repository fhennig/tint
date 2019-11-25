#!/bin/bash
mkdir -p ~/opt
cd ~/opt
git clone https://github.com/fhennig/tint.git
cd tint
./setup-venv.sh
ln -s tint ~/bin/tint
