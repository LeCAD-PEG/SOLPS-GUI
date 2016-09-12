all: paraview_UAL_tutorial.pdf

.tex.pdf:
	pdflatex $*
	pdflatex $*

clean:
	rm -f *.aux *.toc *.bbl *.toc *.out

convert:
	pandoc --from=latex --to=rst --output=converted.txt \
			paraview_UAL_tutorial.tex         
	sed -e '/\[fig:[a-zA-Z0-9_]*/y/_/-/' \
	    -e 's/:math:`\([^`]*\)`/``\1``/g' \
	    -e 's/\\-/-/g' \
	    -e 's/\\_/_/g' \
	    -e 's/\[fig:\([a-zA-Z0-9_-]\{1,\}\)\]/:num:`Fig. #\1`/g' \
	    -e 's/Fig. :num:/:num:/g' \
	    -e 's/figure:: \(.*\)/figure:: images\/\1.png/' \
	    -e 's/Iter/ITER/g' \
	    -e 's/\to/-->/g' \
	    -e 's/\*\*\([a-zA-Z ]\{1,\}\)\*\* button/:guilabel:`\1` button/g' \
	    	converted.txt > output.txt
	


