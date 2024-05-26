#!/bin/bash

set -euf

python /bot/core/database/init_tables.py

python /bot/core/main.py
