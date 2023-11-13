#!/bin/bash
sudo apt-get -y install texlive-latex-base texlive-fonts-recommended texlive-fonts-extra biber 
cd doc/
pdflatex -interaction=nonstopmode proyecto  
biber proyecto
makeglossaries proyecto
pdflatex -interaction=nonstopmode proyecto
cd ..
invoke clean     