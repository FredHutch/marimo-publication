#!/bin/bash
set -e

rm -rf test_build

marimo export html-wasm app.py -o test_build --mode run --no-show-code

python -m http.server --directory test_build