#!/bin/bash -e
cd "$(dirname "$0")"

python3 -m venv venv &&
  source venv/bin/activate &&
  pip install --upgrade pip &&
  pip install -r requirements.txt &&
  deactivate