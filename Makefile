.PHONY: all clean

all: paper/main.pdf

paper/main.pdf: paper/main.tex paper/sections/*.tex paper/figures/*.tex paper/bibliography.bib
	mkdir -p paper/build
	cd paper && latexmk -pdf -interaction=nonstopmode -outdir=build main.tex
	mv paper/build/main.pdf paper/main.pdf

clean:
	rm -rf paper/build/
	rm -f paper/main.pdf
