B2INPUT = ${HOME}/solps-iter/modules/B2.5/src/documentation/b2input.xml
B2DTD = $(HOME)/solps-iter/modules/B2.5/src/documentation/xhtml-symbol.ent

all : ../widgets/b2_tooltips.py ../widgets/b2menu.py \
	../../doc/source/code/b2input.rst

../widgets/b2_tooltips.py : $(B2INPUT) create-tooltips.xslt
	xsltproc --nonet create-tooltips.xslt $(B2INPUT) > $@

../widgets/b2menu.py : $(B2INPUT) create-addmenu.xslt
	xsltproc --nonet create-addmenu.xslt $(B2INPUT) > $@

../../doc/source/code/b2input.rst : $(B2INPUT) create_b2input_rst.py
	python3 create_b2input_rst.py $(B2INPUT) $(B2DTD)> $@
