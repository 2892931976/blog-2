#!/bin/bash
 
export LD_LIBRARY_PATH=/opt/python3/lib 
 
rm -rf build/
rm -rf dist/

pyinstaller3  --clean  blog.py  --additional-hooks-dir=. 
 
rm -rf build/
  





