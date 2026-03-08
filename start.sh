#!/bin/bash
# Aktywuj środowisko i uruchom aplikację
source .venv/bin/activate
export $(grep -v '^#' .env | xargs)
python src/main.py
