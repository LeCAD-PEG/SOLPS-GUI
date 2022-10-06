SOLPS_GUI_VERSION=$(shell git describe)

pyqt := $(shell package/pyqt.sh --prefix)
pyside6 := $(shell package/pyside6.sh --prefix)
gnuplot-widget := $(shell package/gnuplot-widget.sh --prefix)
gnuplot := $(shell package/gnuplot.sh --prefix)

.PHONY: doc gnuplot-widget gnuplot

solps-gui: doc # $(pyqt) $(pyside6) setupenv.sh # imas paraview ggd-plugin


doc:
	make -C doc latexpdf 
	make -C doc html

clean:
	make -C doc clean

$(pyqt):
	package/pyqt.sh --rebuild

gnuplot-widget : $(gnuplot-widget)
$(gnuplot-widget) :
	package/gnuplot-widget.sh --rebuild

gnuplot : $(gnuplot)
$(gnuplot) :
	package/gnuplot.sh --rebuild

$(pyside6) :
	package/pyside6.sh --rebuild

setupenv.sh: Makefile
	package/environment.sh > $@

query-%:
	@echo $($(*))

deep-clean:
	-chmod -R a+rw staging/imas
	rm -rf build staging

