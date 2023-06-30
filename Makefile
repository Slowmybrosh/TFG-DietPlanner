all: pdf clean
pdf:
	cd doc && pdflatex -interaction=nonstopmode proyecto.tex
	cd doc && biber proyecto
	cd doc && pdflatex -interaction=nonstopmode proyecto.tex
	cd doc && pdflatex -interaction=nonstopmode proyecto.tex
clean:
	rm -f doc/*.aux doc/*.bbl doc/*.bcf doc/*.blg doc/*.log doc/*.out doc/*.run.xml doc/*.toc
.PHONY: latex clean