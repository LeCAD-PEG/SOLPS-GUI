all: cpo2ids.pdf

%.pdf : %.tex
	pdflatex $*
	pdflatex $*

clean:
	rm -f cpo2ids.pdf 
	rm -f *.aux *.toc *.bbl *.toc *.out *.lof *.log *.synctex.gz

convert:
	pandoc --from=latex --to=rst --output=converted.txt cpo2ids.tex 	
	sed -f latex2rst.sed converted.txt > output.txt
