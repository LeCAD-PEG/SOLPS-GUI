B2INPUT = ${HOME}/solps-iter/modules/B2.5/src/documentation/b2input.xml

all : b2_tooltips.py b2menu.py

b2_tooltips.py : $(B2INPUT)
	xsltproc create-tooltips.xslt $(B2INPUT) > b2_tooltips.py

b2menu.py : $(B2INPUT)
	xsltproc create-addmenu.xslt $(B2INPUT) > b2menu.py
