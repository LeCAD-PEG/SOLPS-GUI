convert:
	pandoc --from=latex --to=rst --output=converted.txt \
		 --reference-links --bibliography=References.bib \
		--csl ieee.csl ids.tex         
	sed -e 's/\\ :sub:`\([0-9A-Za-z ]\)`/-\1/g' \
	    -e 's/\\ //g' \
	    -e 's/:math:`\([^`]*\)`/``\1``/g' \
	    -e 's/\\-/-/g' \
	    -e 's/\\_/_/g' \
	    -e 's/ / /g' \
	    -e 's/ / /g' \
	    -e 's/“/"/g' \
	    -e 's/”/"/g' \
	    -e 's/:math:`\([^`]*\)`/``\1``/g' \
	    -e 's/\\-/-/g' \
	    -e 's/\\_/_/g' \
	    -e 's/Table[ \\]\{1,\}`\[tbl:\([a-zA-Z0-9_-]\{1,\}\)\]`_/:numref:`fig-\1`/g' \
	    -e 's/Fig.[ \\]\{1,\}`\[fig:\([a-zA-Z0-9_-]\{1,\}\)\]`_/:numref:`fig-\1`/g' \
	    -e 's/Listing[ \\]\{1,\}`\[lst:\([a-zA-Z0-9_-]\{1,\}\)\]`_/:numref:`lst-\1`/g' \
	    -e 's/^\[fig:\([a-zA-Z0-9_-]\{1,\}\)\]/.. _fig-\1:/' \
	    -e 's/^\[tbl:\([a-zA-Z0-9_-]\{1,\}\)\]/.. _tbl-\1:/' \
	    -e 's/^\[lst:\([a-zA-Z0-9_-]\{1,\}\)\]/.. _lst-\1:/' \
	    -e 's/figure:: \(.*\)/figure:: \1.png/' \
	    -e 's,images/CPO/,images/,' -e 's,images/IDS/,images/,' \
	    -e 's/.png.png/.png/' -e 's/.pdf.png/.*/' \
	    -e 's/Iter/ITER/g' \
	    -e 's/\to/-->/g' \
	    -e 's/\*\*\([a-zA-Z ]\{1,\}\)\*\* button/:guilabel:`\1` button/g' \
	    -e '/\.\. raw/,+3d' \
	    -e 's/^\.\. subsec:\(.*\)/.. _subsec-\1/' \
	    -e 's/^\.\. sec:\(.*\)/.. _sec-\1/' \
	    -e 's/\$$\([^$$]\{1,\}\)\$$/:math:`\1`/g' \
	    	converted.txt > output.txt
