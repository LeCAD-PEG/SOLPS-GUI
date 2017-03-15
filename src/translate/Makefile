B2INPUT = ${HOME}/solps-iter/modules/B2.5/src/documentation/b2input.xml

all : ../widgets/b2_tooltips.py ../widgets/b2menu.py \
	../../doc/source/code/b2input.rst

../widgets/b2_tooltips.py : $(B2INPUT) create-tooltips.xslt
	xsltproc create-tooltips.xslt $(B2INPUT) > $@

../widgets/b2menu.py : $(B2INPUT) create-addmenu.xslt
	xsltproc create-addmenu.xslt $(B2INPUT) > $@

../../doc/source/code/b2input.rst : $(B2INPUT) create_b2input_rst.py
	python3 create_b2input_rst.py $(B2INPUT) > $@
