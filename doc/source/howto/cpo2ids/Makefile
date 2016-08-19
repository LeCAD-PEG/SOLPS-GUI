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

crop:	# Calculates crop size for trimmed images from LaTeX file
	LANG=C awk 'BEGIN{FS=","; u=72/2.54}\
	/trim/ {trim=$$2; file=$$3;\
		gsub("cm", "", trim);\
		sub("trim=", "", trim);\
		sub(".*{", "", file);\
		sub("}.*", "", file);\
		file="images/" file ".png";\
		cmd = "identify -format \"%w %h\" " file;\
		cmd | getline;\
		split($$0, wh, " ");\
		close(cmd);\
		split(trim, p, " ");\
		if (trim == "0 0 0 0") {\
			print "Crop not needed for", file;\
			next;\
		}\
		printf("trim=%.0f %.0f %.0f %.0f size=%d %d\n",\
		  u*p[1] , u*p[2], u*p[3], u*p[4], wh[1], wh[2]);\
		printf("convert -crop %dx%d+%d+%d %s out.png\n",\
			 wh[1]-u*p[1]-u*p[3],\
			 wh[2]-u*p[2]-u*p[4], u*p[1], u*p[4], file);\
		}' cpo2ids.tex
