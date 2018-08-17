#!/bin/bash

cd "$(dirname "$0")"
python app.py runserver -h 0.0.0.0 -p 80

