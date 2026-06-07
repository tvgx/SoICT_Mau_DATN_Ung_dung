#!/bin/bash
mkdir -p build
latexmk -pdf -interaction=nonstopmode -outdir=build main.tex
cp build/main.pdf main.pdf
echo "Build completed. All temporary files are in the build/ directory."
