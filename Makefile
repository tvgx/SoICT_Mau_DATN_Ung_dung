.PHONY: all clean

all:
	mkdir -p build
	latexmk -pdf -outdir=build main.tex
	cp build/main.pdf main.pdf

clean:
	latexmk -C -outdir=build
	rm -rf build/
	find . -type d -name "build" -exec rm -rf {} +
	find . -type f -name "*.aux" -delete
	find . -type f -name "*.log" -delete
	find . -type f -name "*.fls" -delete
	find . -type f -name "*.fdb_latexmk" -delete
	find . -type f -name "*.synctex.gz" -delete
	find . -type f -name "*-blx.bib" -delete
	find . -type f -name "*.run.xml" -delete
	find . -type f -name "*.bbl" -delete
	find . -type f -name "*.blg" -delete
	rm -f main.pdf
