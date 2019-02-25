
# Use realpath for the last time to remove trailing slash
BUILDROOT=$(realpath $(dir $(realpath $(firstword $(MAKEFILE_LIST)))))
STAGING_DIR ?= ${BUILDROOT}/staging
MODULE_DIR ?= ${BUILDROOT}/modules

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
BLITZ_VERSION=1.0.0
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
SETUP_FILE="setupenv.sh"
SOLPS_GUI_MOD=${MODULE_DIR}/solps-gui/1.5

.PHONY: gr gli OpenBLAS mscl ggd python libxml2 saxon blitz cmake mdsplus \
	imas solps-iter pyqt solps-gui

all: solps-iter solps-gui

${STAGING_DIR}/GR/${GR_VERSION}:
	BUILDROOT=${BUILDROOT} GR_VERSION=${GR_VERSION} ./package/build-GR.sh
gr: ${STAGING_DIR}/GR/${GR_VERSION}

${STAGING_DIR}/GLI/${GLI_VERSION}:
	BUILDROOT=${BUILDROOT} GLI_VERSION=${GLI_VERSION} ./package/build-GLI.sh

gli: ${STAGING_DIR}/GLI/${GLI_VERSION}

${STAGING_DIR}/saxon/${SAXON_VERSION}:
	BUILDROOT=${BUILDROOT} \
	VERSION=${SAXON_VERSION} \
	./package/build-saxon.sh

saxon: ${STAGING_DIR}/saxon/${SAXON_VERSION}

${STAGING_DIR}/blitz/${BLITZ_VERSION}:
	BUILDROOT=${BUILDROOT} \
	./package/build-blitz.sh

blitz: ${STAGING_DIR}/blitz/${BLITZ_VERSION}

${STAGING_DIR}/cmake/${CMAKE_VERSION}:
	BUILDROOT=${BUILDROOT} \
	VERSION=${CMAKE_VERSION} \
	./package/build-cmake.sh

cmake: ${STAGING_DIR}/cmake/${CMAKE_VERSION}

${STAGING_DIR}/mdsplus/${MDSPLUS_VERSION}:
	BUILDROOT=${BUILDROOT} \
	LIBXML2_VERSION=${LIBXML2_VERSION} \
	VERSION=${MDSPLUS_VERSION} \
	./package/build-mdsplus.sh

mdsplus: libxml2 ${STAGING_DIR}/mdsplus/${MDSPLUS_VERSION}

${STAGING_DIR}/OpenBLAS/${OPENBLAS_VERSION}:
	BUILDROOT=${BUILDROOT}
	VERSION=${OPENBLAS_VERSION} \
	./package/build-OpenBLAS.sh

OpenBLAS: ${STAGING_DIR}/OpenBLAS/${OPENBLAS_VERSION}

${STAGING_DIR}/mscl/${MSCL_VERSION}:
	BUILDROOT=${BUILDROOT} \
	VERSION=${MSCL_VERSION} \
	./package/build-mscl.sh

mscl: ${STAGING_DIR}/mscl/${MSCL_VERSION}

${STAGING_DIR}/Python/${PYTHON_VERSION}:
	BUILDROOT=${BUILDROOT} \
	VERSION=${PYTHON_VERSION} \
	./package/build-python.sh

python: ${STAGING_DIR}/Python/${PYTHON_VERSION}

${STAGING_DIR}/Python/${PYTHON_VERSION}/lib/python${PYTHON_MAINVERSION}/site-packages/numpy-${NUMPY_VERSION}-py${PYTHON_MAINVERSION}-linux-x86_64.egg:
	VERSION=${NUMPY_VERSION} \
	./package/build-numpy.sh

matplotlib-numpy: python OpenBLAS ${STAGING_DIR}/Python/${PYTHON_VERSION}/lib/python${PYTHON_MAINVERSION}/site-packages/numpy-${NUMPY_VERSION}-py${PYTHON_MAINVERSION}-linux-x86_64.egg

${STAGING_DIR}/Python/${PYTHON_VERSION}/lib/python${PYTHON_MAINVERSION}/site-packages/scipy-${SCIPY_VERSION}-py${PYTHON_MAINVERSION}-linux-x86_64.egg:
	VERSION=${SCIPY_VERSION} \
	./package/build-scipy.sh

scipy: python OpenBLAS ${STAGING_DIR}/Python/${PYTHON_VERSION}/lib/python${PYTHON_MAINVERSION}/site-packages/scipy-${SCIPY_VERSION}-py${PYTHON_MAINVERSION}-linux-x86_64.egg

${STAGING_DIR}/sip/${SIP_VERSION}:
	VERSION=${SIP_VERSION} \
	./package/build-sip.sh

sip: python ${STAGING_DIR}/sip/${SIP_VERSION}

${STAGING_DIR}/qt/${QT_VERSION}:
	BUILDROOT=${BUILDROOT} \
	VERSION=${QT_VERSION} \
	./package/build-qt5.sh

qt5: ${STAGING_DIR}/qt/${QT_VERSION}

${STAGING_DIR}/qt/${QT4_VERSION}:
	BUILDROOT=${BUILDROOT} \
	VERSION=${PARAVIEW_QT_VERSION} \
	./package/build-qt4.sh

qt4: ${STAGING_DIR}/qt/${QT4_VERSION}

${STAGING_DIR}/PyQt5/${PyQt_Version}:
	BUILDROOT=${BUILDROOT} \
	VERSION=${PyQt_Version} \
	PYTHON_VERSION=${PYTHON_VERSION} \
	QT_VERSION=${QT_VERSION} \
	SIP_VERSION=${SIP_VERSION} \
	./package/build-pyqt.sh

pyqt: python qt5 sip ${STAGING_DIR}/PyQt5/${PyQt_Version}

${STAGING_DIR}/gnuplot/${GNUPLOT_VERSION}:
	BUILDROOT=${BUILDROOT} \
	VERSION=${GNUPLOT_VERSION} \
	QT_VERSION=${QT_VERSION} \
	./package/build-gnuplot.sh

gnuplot: pyqt ${STAGING_DIR}/gnuplot/${GNUPLOT_VERSION}

${STAGING_DIR}/gnuplot-widget/python-${PYTHON_VERSION}-qt-${QT_VERSION}:
	BUILDROOT=${BUILDROOT} \
	QT_VERSION=${QT_VERSION} \
	PYTHON_VERSION=${PYTHON_VERSION} \
	PyQt_Version=${PyQt_Version} \
	SIP_VERSION=${SIP_VERSION} \
	GNUPLOT_VERSION=${GNUPLOT_VERSION} \
	./package/build-gnuplot-widget.sh

gnuplot-widget: gnuplot pyqt ${STAGING_DIR}/gnuplot-widget/python-${PYTHON_VERSION}-qt-${QT_VERSION}

${STAGING_DIR}/libxml2/${LIBXML2_VERSION}:
	BUILDROOT=${BUILDROOT} \
	VERSION=${LIBXML2_VERSION} \
	PYTHON_VERSION=${PYTHON_VERSION} \
	./package/build-libxml2.sh

libxml2: python ${STAGING_DIR}/libxml2/${LIBXML2_VERSION}

${STAGING_DIR}/paraview/${PARAVIEW_VERSION}:
	BUILDROOT=${BUILDROOT} \
	VERSION=${PARAVIEW_VERSION} \
	QT_VERSION=${PARAVIEW_QT_VERSION} \
	PARAVIEW_VERSION=${PARAVIEW_VERSION} \
	./package/build-paraview.sh

paraview: cmake qt4 ${STAGING_DIR}/paraview/${PARAVIEW_VERSION}

${STAGING_DIR}/ReadUALEdge-Plugin/1.5.0:
	BUILDROOT=${BUILDROOT} \
	PARAVIEW_VERSION=${PARAVIEW_VERSION} \
	QT_VERSION=${PARAVIEW_QT_VERSION} \
	CMAKE_VERSION=${CMAKE_VERSION} \
	IMASDD_VERSION=${IMASDD_VERSION} \
	IMASUAL_VERSION=${IMASUAL_VERSION} \
	./package/build-paraview-plugin.sh

paraview-plugin: imas cmake paraview blitz ${STAGING_DIR}/ReadUALEdge-Plugin/1.5.0

${BUILDROOT}/build/data-dictionary-${IMASDD_VERSION}/.installed:
	@echo ${BUILDROOT}/data-dictionary-${IMASDD_VERSION}/.installed
	VERSION=${IMASDD_VERSION} \
	PYTHON_VERSION=${PYTHON_VERSION} \
	SAXON_VERSION=${SAXON_VERSION} \
	./package/build-imasdd.sh

imasdd: saxon python ${BUILDROOT}/build/data-dictionary-${IMASDD_VERSION}/.installed

${STAGING_DIR}/imas/${IMASDD_VERSION}/solps:
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
	cp ${BUILDROOT}/imasdb ${STAGING_DIR}/imas/${IMASDD_VERSION}/solps/bin

imas: python matplotlib-numpy scipy saxon mdsplus blitz libxml2 imasdd ${STAGING_DIR}/imas/${IMASDD_VERSION}/solps

${STAGING_DIR}/GGD/${GGD_VERSION}:
	BUILDROOT=${BUILDROOT} \
	VERSION=${GGD_VERSION} \
	IMASUAL_VERSION=${IMASUAL_VERSION} \
	IMASDD_VERSION=${IMASDD_VERSION} \
	MDSPLUS_VERSION=${MDSPLUS_VERSION} \
	./package/build-ggd.sh

ggd: imas ${STAGING_DIR}/GGD/${GGD_VERSION}

${STAGING_DIR}/solps-iter/${SOLPS_VERSION}:
	# Copy imasdb script for setting up IMAS MDSPLUS_TREE environment
	SOLPS_VERSION=${SOLPS_VERSION} \
	IMASUAL_VERSION=${IMASUAL_VERSION} \
	IMASDD_VERSION=${IMASDD_VERSION} \
	GGD_VERSION=${GGD_VERSION} \
	MSCL_VERSION=${MSCL_VERSION} \
	GR_VERSION=${GR_VERSION} \
	GLI_VERSION=${GLI_VERSION} \
	MDSPLUS_VERSION=${MDSPLUS_VERSION} \
	OPENBLAS_VERSION=${OPENBLAS_VERSION} \
	./package/build-solps-iter.csh

solps-iter: imas gr gli OpenBLAS mscl ggd python ${STAGING_DIR}/solps-iter/${SOLPS_VERSION}

solps-gui: imas pyqt gnuplot gnuplot-widget setupenv.sh ${MODULE_DIR}/solps-gui/1.5

setupenv.sh:
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
	@echo "export PV_PLUGIN_PATH=\$${INSTALL_DIR}/ReadUALEdge-Plugin/1.5.0" >> ${SETUP_FILE}
	@echo "" >> ${SETUP_FILE}
	@echo "# Setting aliases" >> ${SETUP_FILE}
	@echo "alias solps=\"python3 ${BUILDROOT}/src/gui/solps.py\"" >> ${SETUP_FILE}
	@echo "alias solps_doc=\"xdg-open ${BUILDROOT}/doc/build/html/index.html\"" >> ${SETUP_FILE}
	@echo "alias solps_help=\"assistant -collectionFile ${BUILDROOT}/doc/build/qthelp/SOLPSGUI.qhc\"" >> ${SETUP_FILE}
	@echo "alias eirene=\"python3 ${BUILDROOT}/src/widgets/eirene.py\"" >> ${SETUP_FILE}
	@echo "alias b2=\"python3 ${BUILDROOT}/src/widgets/b2.py\"" >> ${SETUP_FILE}

# Solps GUI module file
${MODULE_DIR}/solps-gui/1.5:
	@echo "Writing solps-gui module file to ${MODULE_DIR}/solps-gui/1.5"
	@install -d ${MODULE_DIR}/solps-gui
	@echo "#%Module1.0###################################################################" > ${SOLPS_GUI_MOD}
	@echo "##" >> ${SOLPS_GUI_MOD}
	@echo "## \$$name modulefile" >> ${SOLPS_GUI_MOD}
	@echo "##" >> ${SOLPS_GUI_MOD}
	@echo "proc ModulesHelp { } {" >> ${SOLPS_GUI_MOD}
	@echo "puts stderr "\tThis module sets the environment for $name v$ver"" >> ${SOLPS_GUI_MOD}
	@echo "}" >> ${SOLPS_GUI_MOD}
	@echo "conflict $name" >> ${SOLPS_GUI_MOD}
	@echo "module-whatis "Graphical user interface for interacting with SOLPS-ITER and its output"" >> ${SOLPS_GUI_MOD}
	@echo "if { ! [ is-loaded imas ] } {" >> ${SOLPS_GUI_MOD}
	@echo "    module load imas/${IMASDD_VERSION}/solps" >> ${SOLPS_GUI_MOD}
	@echo "}" >> ${SOLPS_GUI_MOD}
	@echo "" >> ${SOLPS_GUI_MOD}
	@echo "if { ![ is-loaded Python/${PYTHON_VERSION} ] } {" >> ${SOLPS_GUI_MOD}
	@echo "    module load Python/${PYTHON_VERSION}" >> ${SOLPS_GUI_MOD}
	@echo "}" >> ${SOLPS_GUI_MOD}
	@echo "" >> ${SOLPS_GUI_MOD}
	@echo "if { ![ is-loaded PyQt5/${PyQt_Version} ] } {" >> ${SOLPS_GUI_MOD}
	@echo "    module load PyQt5/${PyQt_Version}" >> ${SOLPS_GUI_MOD}
	@echo "}" >> ${SOLPS_GUI_MOD}
	@echo "" >> ${SOLPS_GUI_MOD}
	@echo "prepend-path PYTHONPATH         ${BUILDROOT}/src/widgets" >> ${SOLPS_GUI_MOD}
	@echo "prepend-path PYQTDESIGNER       ${BUILDROOT}/src/plugins/designer" >> ${SOLPS_GUI_MOD}
	@echo "" >> ${SOLPS_GUI_MOD}
	@echo "set-alias solps {python3 ${BUILDROOT}/src/gui/solps.py $*}" >> ${SOLPS_GUI_MOD}
	@echo "set-alias solps_doc \"xdg-open ${BUILDROOT}/doc/build/html/index.html\"" >> ${SOLPS_GUI_MOD}
	@echo "set-alias eirene \"python3 -m eirene $*\"" >> ${SOLPS_GUI_MOD}
	@echo "set-alias b2 \"python3 -m b2 $*\"" >> ${SOLPS_GUI_MOD}

query-%:
	@echo $($(*))
deep-clean:
	rm -rf ${BUILDROOT}/download ${BUILDROOT}/build ${BUILDROOT}/staging
