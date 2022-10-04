SOLPSTOP?=${HOME}/solps-iter
B2INPUT = ${SOLPSTOP}/modules/B2.5/src/documentation/b2input.xml
B2DTD = ${SOLPSTOP}/modules/B2.5/src/documentation/xhtml-symbol.ent

all : ../actors/b2_tooltips.py ../actors/b2menu.py \
	../../doc/source/code/b2input.rst

../actors/b2_tooltips.py : $(B2INPUT) create-tooltips.xslt
	xsltproc --nonet create-tooltips.xslt $(B2INPUT) > $@

../actors/b2menu.py : $(B2INPUT) create-addmenu.xslt
	xsltproc --nonet create-addmenu.xslt $(B2INPUT) > $@

../../doc/source/code/b2input.rst : $(B2INPUT) create_b2input_rst.py
	python3 create_b2input_rst.py $(B2INPUT) $(B2DTD) $@
