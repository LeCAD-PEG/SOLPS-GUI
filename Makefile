BUILDROOT=$(dir $(realpath $(firstword $(MAKEFILE_LIST))))

GLI_VERSION=4.5.30
OPENBLAS_VERSION=0.3.5
PYTHON_VERSION=3.6.8
NUMPY_VERSION=1.16.1
SCIPY_VERSION=1.2.1
GNUPLOT_VERSION=5.2.2
QT_VERSION=5.9.1
PyQT_VERSION=5.9.1
SIP_VERSION=4.19.13
MDSPLUS_VERSION=stable_release-7-7-8
BLITZ_VERISON=1.0.0
LIBXML2_VERSION=2.9.1
SAXON_VERSION=HE9-8-0-12J
IMASDD_VERSION=3.21.0
IMASUAL_VERSION=3.8.4
GGD_VERSION=1.8.3
SOLPS_VERSION=3.0.7

#Paraview specific version
PARAVIEW_VERSION=5.4.1
PARAVIEW_QT_VERSION=4.8.7
CMAKE_VERSION=3.10.1


.PHONY: gr gli OpenBLAS mscl ggd python libxml2 saxon blitz cmake mdsplus \
	imas solps-iter pyqt solps-gui

all: solps-iter solps-gui

gr:
	BUILDROOT=${BUILDROOT} ./package/build-GR.sh

gli:
	BUILDROOT=${BUILDROOT} GLI_VERSION=${GLI_VERSION} ./package/build-GLI.sh

saxon:
	BUILDROOT=${BUILDROOT} \
	SAXON_VERSION=${SAXON_VERSION} \
	./package/build-saxon.sh

blitz:
	BUILDROOT=${BUILDROOT} \
	./package/build-blitz.sh

cmake:
	BUILDROOT=${BUILDROOT} \
	CMAKE_VERSION=${CMAKE_VERSION} \
	./package/build-cmake.sh

mdsplus: libxml2
	BUILDROOT=${BUILDROOT} \
	./package/build-mdsplus.sh

OpenBLAS:
	BUILDROOT=${BUILDROOT} OPENBLAS_VERSION=${OPENBLAS_VERSION} \
	./package/build-OpenBLAS.sh

mscl:
	BUILDROOT=${BUILDROOT} ./package/build-mscl.sh

python: OpenBLAS
	BUILDROOT=${BUILDROOT} \
	PYTHON_VERSION=${PYTHON_VERSION} \
	NUMPY_VERSION=${NUMPY_VERSION} \
	SCIPY_VERSION=${SCIPY_VERSION} \
	./package/build-python.sh

pyqt: python
	BUILDROOT=${BUILDROOT} \
	PYTHON_VERSION=${PYTHON_VERSION} \
	QT_VERSION=${QT_VERSION} \
	PyQT_VERSION=${PyQT_VERSION} \
	SIP_VERSION=${SIP_VERSION} \
	./package/build-pyqt.sh

gnuplot: pyqt
	BUILDROOT=${BUILDROOT} \
	GNUPLOT_VERSION=${GNUPLOT_VERSION} \
	QT_VERSION=${QT_VERSION} \
	./package/build-gnuplot.sh

gnuplot-widget: gnuplot
	BUILDROOT=${BUILDROOT} \
	QT_VERSION=${QT_VERSION} \
	PYTHON_VERSION=${PYTHON_VERSION} \
	./package/build-gnuplot-widget.sh

libxml2: python
	BUILDROOT=${BUILDROOT} \
	LIBXML2_VERSION=${LIBXML2_VERSION} \
	./package/build-libxml2.sh

paraview: cmake
	BUILDROOT=${BUILDROOT} \
	CMAKE_VERSION=${CMAKE_VERSION} \
	QT_VERSION=${PARAVIEW_QT_VERSION} \
	PARAVIEW_VERSION=${PARAVIEW_VERSION} \
	./package/build-paraview.sh

paraview-plugin: imas cmake paraview
	BUILDROOT=${BUILDROOT} \
	PARAVIEW_VERSION=${PARAVIEW_VERSION} \
	QT_VERSION=${PARAVIEW_QT_VERSION} \
	CMAKE_VERSION=${CMAKE_VERSION} \
	IMASDD_VERSION=${IMASDD_VERSION} \
	IMASUAL_VERSION=${IMASUAL_VERSION} \
	./package/build-paraview-plugin.sh

imas: python OpenBLAS saxon mdsplus blitz libxml2
	BUILDROOT=${BUILDROOT} \
	PYTHON_VERSION=${PYTHON_VERSION} \
	NUMPY_VERSION=${NUMPY_VERSION} \
	SCIPY_VERSION=${SCIPY_VERSION} \
	MDSPLUS_VERSION=${MDSPLUS_VERSION} \
	BLITZ_VERSION=${BLITZ_VERSION} \
	LIBXML2_VERSION=${LIBXML2_VERSION} \
	SAXON_VERSION=${SAXON_VERSION} \
	IMASDD_VERSION=${IMASDD_VERSION} \
	IMASUAL_VERSION=${IMASUAL_VERSION} \
	./package/build-imas.sh

ggd: imas
	BUILDROOT=${BUILDROOT} \
	GGD_VERSION=${GGD_VERSION} \
	IMASUAL_VERSION=${IMASUAL_VERSION} \
	IMASDD_VERSION=${IMASDD_VERSION} \
	MDSPLUS_VERSION=${MDSPLUS_VERSION} \
	./package/build-ggd.sh

solps-iter: imas gr gli OpenBLAS mscl ggd python
	# Copy imasdb script for setting up IMAS MDSPLUS_TREE environment
	cp ${BUILDROOT}/imasdb ${BUILDROOT}/staging/bin
	IMASUAL_VERSION=${IMASUAL_VERSION} \
	IMASDD_VERSION=${IMASDD_VERSION} \
	./package/build-solps-iter.csh

solps-gui: imas pyqt gnuplot gnuplot-widget

query-%:
	@echo $($(*))
deep-clean:
	rm -rf ${BUILDROOT}/download ${BUILDROOT}/build ${BUILDROOT}/staging
