#!/bin/bash
pyinstaller --onefile --add-data "assets:assets" --add-data "sounds:sounds" src/main.py
