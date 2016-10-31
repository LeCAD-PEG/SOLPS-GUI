%.pdf : %.tex
	pdflatex $*
	pdflatex $*

clean:
	rm -f cpo2ids.pdf converted.txt output.txt
	rm -f *.aux *.toc *.bbl *.toc *.out *.lof *.log *.synctex.gz

convert:
	# pandoc --from=latex --to=rst --output=converted.txt main.tex 	
	sed -f latex2rst.sed converted.txt > output.txt
