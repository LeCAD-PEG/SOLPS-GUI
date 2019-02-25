
# Use realpath for the last time to remove trailing slash
BUILDROOT=$(realpath $(dir $(realpath $(firstword $(MAKEFILE_LIST)))))
STAGING_DIR ?= ${BUILDROOT}/staging

GLI_VERSION=4.5.30
GR_VERSION=0.0.94
OPENBLAS_VERSION=0.3.5
PYTHON_VERSION=3.6.8
PYTHON_MAINVERSION=3.6
NUMPY_VERSION=1.16.1
SCIPY_VERSION=1.2.1
GNUPLOT_VERSION=5.2.2
QT_VERSION=5.9.1
QT4_VERSION=4.8.7
PyQt_Version=5.9.1
SIP_VERSION=4.19.13
MDSPLUS_VERSION=stable_release-7-7-8
BLITZ_VERISON=1.0.0
LIBXML2_VERSION=2.9.1
SAXON_VERSION=HE9-8-0-12J
IMASDD_VERSION=3.21.0
IMASUAL_VERSION=3.8.4
GGD_VERSION=1.8.3
SOLPS_VERSION=3.0.7
MSCL_VERSION=1.1.1

#Paraview specific version
PARAVIEW_VERSION=5.4.1
PARAVIEW_QT_VERSION=4.8.7
CMAKE_VERSION=3.10.1

# Get module environment
#
MODULE_CMD:=${MODULE_CMD:-module}
SETUP_FILE="setupenv.sh"

.PHONY: gr gli OpenBLAS mscl ggd python libxml2 saxon blitz cmake mdsplus \
	imas solps-iter pyqt solps-gui

all: solps-iter solps-gui setupenv

gr:
	BUILDROOT=${BUILDROOT} GR_VERSION=${GR_VERSION} ./package/build-GR.sh

gli:
	BUILDROOT=${BUILDROOT} GLI_VERSION=${GLI_VERSION} ./package/build-GLI.sh

saxon:
	BUILDROOT=${BUILDROOT} \
	VERSION=${SAXON_VERSION} \
	./package/build-saxon.sh

blitz:
	BUILDROOT=${BUILDROOT} \
	./package/build-blitz.sh

cmake:
	BUILDROOT=${BUILDROOT} \
	VERSION=${CMAKE_VERSION} \
	./package/build-cmake.sh

mdsplus: libxml2
	BUILDROOT=${BUILDROOT} \
	LIBXML2_VERSION=${LIBXML2_VERSION} \
	VERSION=${MDSPLUS_VERSION} \
	./package/build-mdsplus.sh

OpenBLAS:
	BUILDROOT=${BUILDROOT}
	VERSION=${OPENBLAS_VERSION} \
	./package/build-OpenBLAS.sh

mscl:
	BUILDROOT=${BUILDROOT} \
	VERSION=${MSCL_VERSION} \
	./package/build-mscl.sh

python:
	BUILDROOT=${BUILDROOT} \
	VERSION=${PYTHON_VERSION} \
	./package/build-python.sh

matplotlib-numpy: python OpenBLAS
	VERSION=${NUMPY_VERSION} \
	./package/build-numpy.sh

scipy: python OpenBLAS
	VERSION=${SCIPY_VERSION} \
	./package/build-scipy.sh

sip: python
	VERSION=${SIP_VERSION} \
	./package/build-sip.sh

qt5:
	BUILDROOT=${BUILDROOT} \
	VERSION=${QT_VERSION} \
	./package/build-qt5.sh

qt4:
	BUILDROOT=${BUILDROOT} \
	VERSION=${PARAVIEW_QT_VERSION} \
	./package/build-qt4.sh

pyqt: python qt5 sip
	BUILDROOT=${BUILDROOT} \
	VERSION=${PyQt_Version} \
	PYTHON_VERSION=${PYTHON_VERSION} \
	QT_VERSION=${QT_VERSION} \
	SIP_VERSION=${SIP_VERSION} \
	./package/build-pyqt.sh

gnuplot: pyqt
	BUILDROOT=${BUILDROOT} \
	VERSION=${GNUPLOT_VERSION} \
	QT_VERSION=${QT_VERSION} \
	./package/build-gnuplot.sh

gnuplot-widget: gnuplot pyqt
	BUILDROOT=${BUILDROOT} \
	QT_VERSION=${QT_VERSION} \
	PYTHON_VERSION=${PYTHON_VERSION} \
	PyQt_Version=${PyQt_Version} \
	SIP_VERSION=${SIP_VERSION} \
	GNUPLOT_VERSION=${GNUPLOT_VERSION} \
	./package/build-gnuplot-widget.sh

libxml2: python
	BUILDROOT=${BUILDROOT} \
	VERSION=${LIBXML2_VERSION} \
	PYTHON_VERSION=${PYTHON_VERSION} \
	./package/build-libxml2.sh

paraview: cmake qt4
	BUILDROOT=${BUILDROOT} \
	VERSION=${PARAVIEW_VERSION} \
	QT_VERSION=${PARAVIEW_QT_VERSION} \
	PARAVIEW_VERSION=${PARAVIEW_VERSION} \
	./package/build-paraview.sh

paraview-plugin: imas cmake paraview blitz
	BUILDROOT=${BUILDROOT} \
	PARAVIEW_VERSION=${PARAVIEW_VERSION} \
	QT_VERSION=${PARAVIEW_QT_VERSION} \
	CMAKE_VERSION=${CMAKE_VERSION} \
	IMASDD_VERSION=${IMASDD_VERSION} \
	IMASUAL_VERSION=${IMASUAL_VERSION} \
	./package/build-paraview-plugin.sh

imasdd: saxon python
	VERSION=${IMASDD_VERSION} \
	PYTHON_VERSION=${PYTHON_VERSION} \
	SAXON_VERSION=${SAXON_VERSION} \
	./package/build-imasdd.sh

imas: python matplotlib-numpy scipy saxon mdsplus blitz libxml2 imasdd
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
	MSCL_VERSION=${MSCL_VERSION} \
	./package/build-imas.sh

ggd: imas
	BUILDROOT=${BUILDROOT} \
	VERSION=${GGD_VERSION} \
	IMASUAL_VERSION=${IMASUAL_VERSION} \
	IMASDD_VERSION=${IMASDD_VERSION} \
	MDSPLUS_VERSION=${MDSPLUS_VERSION} \
	./package/build-ggd.sh
	cp ${BUILDROOT}/imasdb ${STAGING_DIR}/imas/${IMASDD_VERSION}/solps/bin

solps-iter: imas gr gli OpenBLAS mscl ggd python
	# Copy imasdb script for setting up IMAS MDSPLUS_TREE environment
	IMASUAL_VERSION=${IMASUAL_VERSION} \
	IMASDD_VERSION=${IMASDD_VERSION} \
	GGD_VERSION=${GGD_VERSION} \
	MSCL_VERSION=${MSCL_VERSION} \
	GR_VERSION=${GR_VERSION} \
	GLI_VERSION=${GLI_VERSION} \
	MDSPLUS_VERSION=${MDSPLUS_VERSION} \
	OPENBLAS_VERSION=${OPENBLAS_VERSION} \
	./package/build-solps-iter.csh

solps-gui: imas pyqt gnuplot gnuplot-widget

setupenv:
	@echo "Writing environemnt to ${BUILDROOT}/${SETUP_FILE}"
	@echo "INSTALL_DIR=${STAGING_DIR}" > ${SETUP_FILE}
	@echo "" >> ${SETUP_FILE}
	@echo "# Setting PATH:" >> ${SETUP_FILE}
	@echo "PATH=\$${INSTALL_DIR}/Python/${PYTHON_VERSION}/bin:\$${PATH}" >> ${SETUP_FILE}
	@echo "PATH=\$${INSTALL_DIR}/sip/${SIP_VERSION}/bin:\$${PATH}" >> ${SETUP_FILE}
	@echo "PATH=\$${INSTALL_DIR}/qt/${QT_VERSION}/bin:\$${PATH}" >> ${SETUP_FILE}
	@echo "PATH=\$${INSTALL_DIR}/cmake/${CMAKE_VERSION}/bin:\$${PATH}" >> ${SETUP_FILE}
	@echo "PATH=\$${INSTALL_DIR}/paraview/${PARAVIEW_VERSION}/bin:\$${PATH}" >> ${SETUP_FILE}
	@echo "" >> ${SETUP_FILE}
	@echo "# Setting LD_LIBRARY_PATH:" >> ${SETUP_FILE}
	@echo "LD_LIBRARY_PATH=\$${INSTALL_DIR}/Python/${PYTHON_VERSION}/lib:\$${LD_LIBRARY_PATH}" >> ${SETUP_FILE}
	@echo "LD_LIBRARY_PATH=\$${INSTALL_DIR}/qt/${QT_VERSION}/lib:\$${LD_LIBRARY_PATH}" >> ${SETUP_FILE}
	@echo "LD_LIBRARY_PATH=\$${INSTALL_DIR}/qt/${QT4_VERSION}/lib:\$${LD_LIBRARY_PATH}" >> ${SETUP_FILE}
	@echo "LD_LIBRARY_PATH=\$${INSTALL_DIR}/PyQt5/${PyQt_Version}/lib:\$${LD_LIBRARY_PATH}" >> ${SETUP_FILE}
	@echo "LD_LIBRARY_PATH=\$${INSTALL_DIR}/mdsplus/${MDSPLUS_VERSION}/lib:\$${LD_LIBRARY_PATH}" >> ${SETUP_FILE}
	@echo "LD_LIBRARY_PATH=\$${INSTALL_DIR}/imas/${IMASDD_VERSION}/solps/lib:\$${LD_LIBRARY_PATH}" >> ${SETUP_FILE}
	@echo "LD_LIBRARY_PATH=\$${INSTALL_DIR}/libxml2/${LIBXML2_VERSION}/solps/lib:\$${LD_LIBRARY_PATH}" >> ${SETUP_FILE}
	@echo "" >> ${SETUP_FILE}
	@echo "# Setting PYTHONPATH:" >> ${SETUP_FILE}
	@echo "PYTHONPATH=${BUILDROOT}/src/widgets:\$${PYTHONPATH}" >> ${SETUP_FILE}
	@echo "PYTHONPATH=\$${INSTALL_DIR}/imas/${IMASDD_VERSION}/solps/lib.linux-x86_64-${PYTHON_MAINVERSION}:\$${PYTHONPATH}" >> ${SETUP_FILE}
	@echo "PYTHONPATH=\$${INSTALL_DIR}/PyQt5/${PyQt_Version}/lib/python${PYTHON_MAINVERSION}/site-packages:\$${PYTHONPATH}" >> ${SETUP_FILE}
	@echo "PYTHONPATH=\$${INSTALL_DIR}/sip/${SIP_VERSION}/lib/python/site-packages:\$${PYTHONPATH}" >> ${SETUP_FILE}
	@echo "PYTHONPATH=\$${INSTALL_DIR}/gnuplot-widget/python-${PYTHON_VERSION}-qt-${QT_VERSION}:\$${PYTHONPATH}" >> ${SETUP_FILE}
	@echo "" >> ${SETUP_FILE}
	@echo "# Exporting variables" >> ${SETUP_FILE}
	@echo "export PATH" >> ${SETUP_FILE}
	@echo "export LD_LIBRARY_PATH" >> ${SETUP_FILE}
	@echo "export PYTHONPATH" >> ${SETUP_FILE}
	@echo "export QTDIR=${BUILDROOT}/staging/qt/5.9.1" >> ${SETUP_FILE}
	@echo "export QT_QPA_FONTDIR=/usr/share/fonts/dejavu" >> ${SETUP_FILE}
	@echo "export PARAVIEW_PREFIX=${BUILDROOT}/staging/paraview/5.4.1" >> ${SETUP_FILE}
	@echo "export ids_path=\$${INSTALL_DIR}/imas/${IMASDD_VERSION}/solps/models/mdsplus" >> ${SETUP_FILE}
	@echo "export SOLPSGUI=${BUILDROOT}/src/gui" >> ${SETUP_FILE}
	@echo "export PYQTDESIGNERPATH=${BUILDROOT}/src/plugins/designer:\$${PYQTDESIGNERPATH}" >> ${SETUP_FILE}
	@echo "export IMAS_VERSION=${IMASDD_VERSION}" >> ${SETUP_FILE}
	@echo "export UAL_VERSION=${IMASUAL_VERSION}" >> ${SETUP_FILE}
	@echo "" >> ${SETUP_FILE}
	@echo "# Setting aliases" >> ${SETUP_FILE}
	@echo "alias solps=\"python3 ${BUILDROOT}/src/gui/solps.py\"" >> ${SETUP_FILE}
	@echo "alias solps_doc=\"xdg-open ${BUILDROOT}/doc/build/html/index.html\"" >> ${SETUP_FILE}
	@echo "alias solps_help=\"assistant -collectionFile ${BUILDROOT}/doc/build/qthelp/SOLPSGUI.qhc\"" >> ${SETUP_FILE}
	@echo "alias eirene=\"python3 ${BUILDROOT}/src/widgets/eirene.py\"" >> ${SETUP_FILE}
	@echo "alias b2=\"python3 ${BUILDROOT}/src/widgets/b2.py\"" >> ${SETUP_FILE}


query-%:
	@echo $($(*))
deep-clean:
	rm -rf ${BUILDROOT}/download ${BUILDROOT}/build ${BUILDROOT}/staging
