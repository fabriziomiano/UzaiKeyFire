#!/bin/bash
pip install --user --upgrade pip \
  && pip install --user virtualenv \
  && virtualenv venv -p python3 \
  && source venv/bin/activate \
  && pip install -r requirements.txt
