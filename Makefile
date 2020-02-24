
# Use realpath for the last time to remove trailing slash
BUILDROOT:=$(realpath $(dir $(realpath $(firstword $(MAKEFILE_LIST)))))
STAGING_DIR ?= ${BUILDROOT}/staging
MODULE_DIR ?= ${BUILDROOT}/modules

# SOLPS-GUI
SOLPS_GUI_VERSION=1.5.0

OPENBLAS_VERSION=0.3.8
PYTHON_VERSION=3.6.9
PYTHON_MAINVERSION=3.6
NUMPY_VERSION=1.17.3
SCIPY_VERSION=1.3.1
GNUPLOT_VERSION=5.2.7
QT_VERSION=5.13.0
PyQt_VERSION=5.13.0
SIP_VERSION=4.19.18
# ParaView specific version
PARAVIEW_VERSION=5.6.2
CMAKE_VERSION=3.15.4

# IMAS
BLITZ_VERSION=1.0.1
MDSPLUS_VERSION=stable_release-7-84-8
LIBXML2_VERSION=2.9.1
SAXON_VERSION=HE9-8-0-12J
IMASUAL_VERSION=4.5.0
IMASDD_VERSION=3.26.0
# Minor version is used for compatibility compiling.
IMAS_MINOR_VERSION=26

# SOLPS-ITER
GLI_VERSION=4.5.30
GR_VERSION=0.0.94
GGD_VERSION=1.9.1
SOLPS_VERSION=develop
MSCL_VERSION=1.1.1
CURL_VERSION=7.64.1
HDF5_VERSION=1.10.5
NETCDF_VERSION=4.6.0
NETCDF_FORTRAN_VERSION=4.4.4
FREETYPE_VERSION=2.10.0
NCL_VERSION=6.5.0
MOTIF_VERSION=2.3.8
OPENMPI_VERSION=4.0.0
FLEX_VERSION=v2.6.3

SETUP_FILE="setupenv.sh"
SOLPS_GUI_MOD=${MODULE_DIR}/solps-gui/1.5
SOLPS_ITER_MOD=${MODULE_DIR}/solps-iter/${SOLPS_VERSION}

.PHONY: gr gli OpenBLAS mscl ggd python libxml2 saxon blitz cmake mdsplus \
	imas solps-iter pyqt solps-gui curl hdf5 netcdf openmpi motif \
	solps-gui-mod paraview-plugin-iter

all: solps-iter solps-gui

package/setup.sh: configure
	./configure

config: package/setup.sh


${STAGING_DIR}/GR/${GR_VERSION}:
	sed -i -e "/^VERSION/s/:-[^}]*}/:-${GR_VERSION}}/" package/build-GR.sh

	./package/build-GR.sh

gr: ${STAGING_DIR}/GR/${GR_VERSION}

${STAGING_DIR}/GLI/${GLI_VERSION}:
	sed -i -e "/^VERSION/s/:-[^}]*}/:-${GLI_VERSION}}/" package/build-GLI.sh

	./package/build-GLI.sh

gli: ${STAGING_DIR}/GLI/${GLI_VERSION}

${STAGING_DIR}/saxon/${SAXON_VERSION}:
	sed -i -e "/^VERSION/s/:-[^}]*}/:-${SAXON_VERSION}}/" package/build-saxon.sh

	./package/build-saxon.sh

saxon: ${STAGING_DIR}/saxon/${SAXON_VERSION}

${STAGING_DIR}/blitz/${BLITZ_VERSION}:
	sed -i -e "/^VERSION/s/:-[^}]*}/:-${BLITZ_VERSION}}/" package/build-blitz.sh

	./package/build-blitz.sh

blitz: ${STAGING_DIR}/blitz/${BLITZ_VERSION}

${STAGING_DIR}/cmake/${CMAKE_VERSION}:
	sed -i -e "/^VERSION/s/:-[^}]*}/:-${CMAKE_VERSION}}/" package/build-cmake.sh

	./package/build-cmake.sh

cmake: ${STAGING_DIR}/cmake/${CMAKE_VERSION}

${STAGING_DIR}/mdsplus/${MDSPLUS_VERSION}:
	sed -i -e "/^VERSION/s/:-[^}]*}/:-${MDSPLUS_VERSION}}/" package/build-mdsplus.sh
	LIBXML2_VERSION=${LIBXML2_VERSION} \
	FLEX_VERSION=${FLEX_VERSION} \
	MOTIF_VERSION=${MOTIF_VERSION} \
	./package/build-mdsplus.sh

mdsplus: config motif libxml2 ${STAGING_DIR}/mdsplus/${MDSPLUS_VERSION}

${STAGING_DIR}/OpenBLAS/${OPENBLAS_VERSION}:
	sed -i -e "/^VERSION/s/:-[^}]*}/:-${OPENBLAS_VERSION}}/" package/build-OpenBLAS.sh

	./package/build-OpenBLAS.sh

OpenBLAS: ${STAGING_DIR}/OpenBLAS/${OPENBLAS_VERSION}

${STAGING_DIR}/mscl/${MSCL_VERSION}:
	sed -i -e "/^VERSION/s/:-[^}]*}/:-${MSCL_VERSION}}/" package/build-mscl.sh

	./package/build-mscl.sh

mscl: ${STAGING_DIR}/mscl/${MSCL_VERSION}

${STAGING_DIR}/Python/${PYTHON_VERSION}:
	sed -i -e "/^VERSION/s/:-[^}]*}/:-${PYTHON_VERSION}}/" package/build-python.sh

	PYTHON_VERSION=${PYTHON_VERSION} \
	OPENBLAS_VERSION=${OPENBLAS_VERSION} \
	./package/build-python.sh

	# Install numpy, matplotib and scipy
	sed -i -e "/^VERSION/s/:-[^}]*}/:-${NUMPY_VERSION}}/" package/build-numpy.sh
	PYTHON_VERSION=${PYTHON_VERSION} \
	OPENBLAS_VERSION=${OPENBLAS_VERSION} \
	./package/build-numpy.sh

	sed -i -e "/^VERSION/s/:-[^}]*}/:-${SCIPY_VERSION}}/" package/build-scipy.sh
	PYTHON_VERSION=${PYTHON_VERSION} \
	OPENBLAS_VERSION=${OPENBLAS_VERSION} \
	./package/build-scipy.sh

python: config OpenBLAS ${STAGING_DIR}/Python/${PYTHON_VERSION}

${STAGING_DIR}/sip/${SIP_VERSION}:
	sed -i -e "/^VERSION/s/:-[^}]*}/:-${SIP_VERSION}}/" package/build-sip.sh

	PYTHON_VERSION=${PYTHON_VERSION} \
	./package/build-sip.sh

sip: config python ${STAGING_DIR}/sip/${SIP_VERSION}

${STAGING_DIR}/qt/${QT_VERSION}:
	sed -i -e "/^VERSION/s/:-[^}]*}/:-${QT_VERSION}}/" package/build-qt5.sh

	PYTHON_VERSION=${PYTHON_VERSION} \
	./package/build-qt5.sh

qt5: config ${STAGING_DIR}/qt/${QT_VERSION}

${STAGING_DIR}/PyQt5/${PyQt_VERSION}:
	sed -i -e "/^VERSION/s/:-[^}]*}/:-${PyQt_VERSION}}/" package/build-pyqt.sh

	PYTHON_VERSION=${PYTHON_VERSION} \
	QT_VERSION=${QT_VERSION} \
	SIP_VERSION=${SIP_VERSION} \
	./package/build-pyqt.sh

pyqt: config python qt5 sip ${STAGING_DIR}/PyQt5/${PyQt_VERSION}

${STAGING_DIR}/gnuplot/${GNUPLOT_VERSION}:
	sed -i -e "/^VERSION/s/:-[^}]*}/:-${GNUPLOT_VERSION}}/" package/build-gnuplot.sh

	QT_VERSION=${QT_VERSION} \
	./package/build-gnuplot.sh

gnuplot: config pyqt ${STAGING_DIR}/gnuplot/${GNUPLOT_VERSION}

${STAGING_DIR}/gnuplot-widget/python-${PYTHON_VERSION}-qt-${QT_VERSION}:

	QT_VERSION=${QT_VERSION} \
	PYTHON_VERSION=${PYTHON_VERSION} \
	PyQt_VERSION=${PyQt_VERSION} \
	SIP_VERSION=${SIP_VERSION} \
	GNUPLOT_VERSION=${GNUPLOT_VERSION} \
	./package/build-gnuplot-widget.sh

gnuplot-widget: config gnuplot pyqt ${STAGING_DIR}/gnuplot-widget/python-${PYTHON_VERSION}-qt-${QT_VERSION}

${STAGING_DIR}/libxml2/${LIBXML2_VERSION}:
	sed -i -e "/^VERSION/s/:-[^}]*}/:-${LIBXML2_VERSION}}/" package/build-libxml2.sh

	PYTHON_VERSION=${PYTHON_VERSION} \
	./package/build-libxml2.sh

libxml2: config python ${STAGING_DIR}/libxml2/${LIBXML2_VERSION}

${STAGING_DIR}/paraview/${PARAVIEW_VERSION}:
	sed -i -e "/^VERSION/s/:-[^}]*}/:-${PARAVIEW_VERSION}}/" package/build-paraview.sh

	QT_VERSION=${QT_VERSION} \
	CMAKE_VERSION=${CMAKE_VERSION} \
	PYTHON_VERSION=${PYTHON_VERSION} \
	LIBXML2_VERSION=${LIBXML2_VERSION} \
	./package/build-paraview.sh

paraview: config cmake qt5 ${STAGING_DIR}/paraview/${PARAVIEW_VERSION}

${STAGING_DIR}/ReadUALEdge-Plugin/1.5.0:
	QT_VERSION=${QT_VERSION} \
	PARAVIEW_VERSION=${PARAVIEW_VERSION} \
	CMAKE_VERSION=${CMAKE_VERSION} \
	IMASDD_VERSION=${IMASDD_VERSION} \
	IMASUAL_VERSION=${IMASUAL_VERSION} \
	BLITZ_VERSION=${BLITZ_VERSION} \
	MDSPLUS_VERSION=${MDSPLUS_VERSION} \
	./package/build-paraview-plugin.sh

paraview-plugin: config imas cmake paraview blitz ${STAGING_DIR}/ReadUALEdge-Plugin/1.5.0

${STAGING_DIR}/ReadUALEdge-Plugin/1.5.0-iter:
	./package/build-paraview-plugin-iter.sh

paraview-plugin-iter: ${STAGING_DIR}/ReadUALEdge-Plugin/1.5.0-iter

${BUILDROOT}/build/data-dictionary-${IMASDD_VERSION}/.installed:
	@echo ${BUILDROOT}/data-dictionary-${IMASDD_VERSION}/.installed
	sed -i -e "/^VERSION/s/:-[^}]*}/:-${IMASDD_VERSION}}/" package/build-imasdd.sh

	PYTHON_VERSION=${PYTHON_VERSION} \
	SAXON_VERSION=${SAXON_VERSION} \
	./package/build-imasdd.sh

imasdd: config saxon python ${BUILDROOT}/build/data-dictionary-${IMASDD_VERSION}/.installed

${STAGING_DIR}/imas/${IMASDD_VERSION}/solps:
	sed -i -e "/^VERSION/s/:-[^}]*}/:-${IMASUAL_VERSION}}/" package/build-imas.sh

	PYTHON_VERSION=${PYTHON_VERSION} \
	MDSPLUS_VERSION=${MDSPLUS_VERSION} \
	BLITZ_VERSION=${BLITZ_VERSION} \
	LIBXML2_VERSION=${LIBXML2_VERSION} \
	SAXON_VERSION=${SAXON_VERSION} \
	IMASDD_VERSION=${IMASDD_VERSION} \
	IMASUAL_VERSION=${IMASUAL_VERSION} \
	MSCL_VERSION=${MSCL_VERSION} \
	OPENBLAS_VERSION=${OPENBLAS_VERSION} \
	./package/build-imas.sh
	cp ${BUILDROOT}/imasdb ${STAGING_DIR}/imas/${IMASDD_VERSION}/solps/bin

imas: config python saxon mdsplus blitz libxml2 imasdd ${STAGING_DIR}/imas/${IMASDD_VERSION}/solps

${STAGING_DIR}/GGD/${GGD_VERSION}:
	sed -i -e "/^VERSION/s/:-[^}]*}/:-${GGD_VERSION}}/" package/build-ggd.sh

	IMASUAL_VERSION=${IMASUAL_VERSION} \
	IMASDD_VERSION=${IMASDD_VERSION} \
	MDSPLUS_VERSION=${MDSPLUS_VERSION} \
	./package/build-ggd.sh

ggd: config imas ${STAGING_DIR}/GGD/${GGD_VERSION}


${STAGING_DIR}/curl/${CURL_VERSION}:
	sed -i -e "/^VERSION/s/:-[^}]*}/:-${CURL_VERSION}}/" package/build-curl.sh

	./package/build-curl.sh


curl: config ${STAGING_DIR}/curl/${CURL_VERSION}

${STAGING_DIR}/hdf5/${HDF5_VERSION}:
	sed -i -e "/^VERSION/s/:-[^}]*}/:-${HDF5_VERSION}}/" package/build-hdf5.sh

	CMAKE_VERSION=${CMAKE_VERSION} \
	OPENMPI_VERSION=${OPENMPI_VERSION} \
	./package/build-hdf5.sh

hdf5: config cmake ${STAGING_DIR}/hdf5/${HDF5_VERSION}

${STAGING_DIR}/netcdf/${NETCDF_VERSION}:
	sed -i -e "/^VERSION/s/:-[^}]*}/:-${NETCDF_VERSION}}/" package/build-netCDF.sh

	VERSION=${NETCDF_VERSION} \
	HDF5_VERSION=${HDF5_VERSION} \
	CURL_VERSION=${CURL_VERSION} \
	CMAKE_VERSION=${CMAKE_VERSION} \
	./package/build-netCDF.sh

	sed -i -e "/^VERSION/s/:-[^}]*}/:-${NETCDF_FORTRAN_VERSION}}/" package/build-netCDF-Fortran.sh

	VERSION=${NETCDF_FORTRAN_VERSION} \
	NETCDF_VERSION=${NETCDF_VERSION} \
	CMAKE_VERSION=${CMAKE_VERSION}	\
	HDF5_VERSION=${HDF5_VERSION} \
	CURL_VERSION=${CURL_VERSION} \
	./package/build-netCDF-Fortran.sh

netcdf: config hdf5 curl ${STAGING_DIR}/netcdf/${NETCDF_VERSION}

${STAGING_DIR}/freetype/${FREETYPE_VERSION}:
	sed -i -e "/^VERSION/s/:-[^}]*}/:-${FREETYPE_VERSION}}/" package/build-freetype.sh

	./package/build-freetype.sh

freetype: ${STAGING_DIR}/freetype/${FREETYPE_VERSION}

${STAGING_DIR}/ncl/${NCL_VERSION}:
	sed -i -e "/^VERSION/s/:-[^}]*}/:-${NCL_VERSION}}/" package/build-ncl.sh

	FLEX_VERSION=${FLEX_VERSION} \
	FREETYPE_VERSION=${FREETYPE_VERSION} \
	OPENBLAS_VERSION=${OPENBLAS_VERSION} \
	NETCDF_VERSION=${NETCDF_VERSION} \
	./package/build-ncl.sh

ncl: config flex freetype ${STAGING_DIR}/ncl/${NCL_VERSION}

${STAGING_DIR}/openmpi/${OPENMPI_VERSION}:
	sed -i -e "/^VERSION/s/:-[^}]*}/:-${OPENMPI_VERSION}}/" package/build-openmpi.sh

	./package/build-openmpi.sh

openmpi: ${STAGING_DIR}/openmpi/${OPENMPI_VERSION}

${STAGING_DIR}/flex/${FLEX_VERSION}:
	sed -i -e "/^VERSION/s/:-[^}]*}/:-${FLEX_VERSION}}/" package/build-flex.sh

	./package/build-flex.sh

flex: ${STAGING_DIR}/flex/${FLEX_VERSION}

${STAGING_DIR}/motif/${MOTIF_VERSION}:
	sed -i -e "/^VERSION/s/:-[^}]*}/:-${MOTIF_VERSION}}/" package/build-motif.sh

	FLEX_VERSION=${FLEX_VERSION} \
	FREETYPE_VERSION=${FREETYPE_VERSION} \
	./package/build-motif.sh

motif: config flex ${STAGING_DIR}/motif/${MOTIF_VERSION}

${STAGING_DIR}/solps-iter/${SOLPS_VERSION}/.installed:
	# Copy imasdb script for setting up IMAS MDSPLUS_TREE environment

	SOLPS_VERSION=${SOLPS_VERSION} \
	IMASUAL_VERSION=${IMASUAL_VERSION} \
	IMAS_MINOR_VERISON=${IMAS_MINOR_VERSION} \
	IMASDD_VERSION=${IMASDD_VERSION} \
	GGD_VERSION=${GGD_VERSION} \
	MSCL_VERSION=${MSCL_VERSION} \
	GR_VERSION=${GR_VERSION} \
	GLI_VERSION=${GLI_VERSION} \
	MDSPLUS_VERSION=${MDSPLUS_VERSION} \
	OPENBLAS_VERSION=${OPENBLAS_VERSION} \
	NCL_VERSION=${NCL_VERSION} \
	NETCDF_VERSION=${NETCDF_VERSION} \
	NETCDF_FORTRAN_VERSION=${NETCDF_FORTRAN_VERSION} \
	OPENMPI_VERSION=${OPENMPI_VERSION} \
	MOTIF_VERSION=${MOTIF_VERSION} \
	HDF5_VERSION=${HDF5_VERSION} \
	CURL_VERSION=${CURL_VERSION} \
	FLEX_VERSION=${FLEX_VERSION} \
	FREETYPE_VERSION=${FREETYPE_VERSION} \
	PYTHON=${PYTHON_VERSION} \
	./package/build-solps-iter.sh

solps-iter: config imas gr gli OpenBLAS mscl ggd python netcdf ncl openmpi motif ${STAGING_DIR}/solps-iter/${SOLPS_VERSION}/.installed

solps-gui-mod:
	sed -i -e "/^VERSION/s/:-[^}]*}/:-${SOLPS_GUI_VERSION}}/" package/build-solps-gui.sh
	VERSION=${SOLPS_GUI_VERSION} \
	IMASDD_VERSION=${IMASDD_VERSION} \
	PYTHON_VERSION=${PYTHON_VERSION} \
	QT_VERSION=${QT_VERSION} \
	PyQt_VERSION=${PyQt_VERSION} \
	GNUPLOT_VERSION=${GNUPLOT_VERSION} \
	./package/build-solps-gui.sh


solps-gui: config imas pyqt gnuplot gnuplot-widget setupenv.sh solps-gui-mod

setupenv.sh:
	@echo "Writing environemnt to ${BUILDROOT}/${SETUP_FILE}"
	@echo "ROOT_DIR=\$${PWD}" > ${SETUP_FILE}
	@echo "INSTALL_DIR=\$${ROOT_DIR}/staging" >> ${SETUP_FILE}
	@echo "" >> ${SETUP_FILE}
	@echo "# Setting PATH:" >> ${SETUP_FILE}
	@echo "PATH=\$${INSTALL_DIR}/Python/${PYTHON_VERSION}/bin:\$${PATH}" >> ${SETUP_FILE}
	@echo "PATH=\$${INSTALL_DIR}/sip/${SIP_VERSION}/bin:\$${PATH}" >> ${SETUP_FILE}
	@echo "PATH=\$${INSTALL_DIR}/qt/${QT_VERSION}/bin:\$${PATH}" >> ${SETUP_FILE}
	@echo "PATH=\$${INSTALL_DIR}/cmake/${CMAKE_VERSION}/bin:\$${PATH}" >> ${SETUP_FILE}
	@echo "PATH=\$${INSTALL_DIR}/paraview/${PARAVIEW_VERSION}/bin:\$${PATH}" >> ${SETUP_FILE}
	@echo "PATH=\$${INSTALL_DIR}/openmpi/${OPENMPI_VERSION}/bin:\$${PATH}" >> ${SETUP_FILE}
	@echo "" >> ${SETUP_FILE}
	@echo "# Setting LD_LIBRARY_PATH:" >> ${SETUP_FILE}
	@echo "LD_LIBRARY_PATH=\$${INSTALL_DIR}/Python/${PYTHON_VERSION}/lib:\$${LD_LIBRARY_PATH}" >> ${SETUP_FILE}
	@echo "LD_LIBRARY_PATH=\$${INSTALL_DIR}/blitz/${BLITZ_VERSION}/lib:\$${LD_LIBRARY_PATH}" >> ${SETUP_FILE}
	@echo "LD_LIBRARY_PATH=\$${INSTALL_DIR}/qt/${QT_VERSION}/lib:\$${LD_LIBRARY_PATH}" >> ${SETUP_FILE}
	@echo "LD_LIBRARY_PATH=\$${INSTALL_DIR}/PyQt5/${PyQt_VERSION}/lib:\$${LD_LIBRARY_PATH}" >> ${SETUP_FILE}
	@echo "LD_LIBRARY_PATH=\$${INSTALL_DIR}/mdsplus/${MDSPLUS_VERSION}/lib:\$${LD_LIBRARY_PATH}" >> ${SETUP_FILE}
	@echo "LD_LIBRARY_PATH=\$${INSTALL_DIR}/imas/${IMASDD_VERSION}/solps/lib:\$${LD_LIBRARY_PATH}" >> ${SETUP_FILE}
	@echo "LD_LIBRARY_PATH=\$${INSTALL_DIR}/libxml2/${LIBXML2_VERSION}/solps/lib:\$${LD_LIBRARY_PATH}" >> ${SETUP_FILE}
	@echo "LD_LIBRARY_PATH=\$${INSTALL_DIR}/hdf5/${HDF5_VERSION}/lib:\$${LD_LIBRARY_PATH}" >> ${SETUP_FILE}
	@echo "LD_LIBRARY_PATH=\$${INSTALL_DIR}/curl/${CURL_VERSION}/lib:\$${LD_LIBRARY_PATH}" >> ${SETUP_FILE}
	@echo "LD_LIBRARY_PATH=\$${INSTALL_DIR}/openmpi/${OPENMPI_VERSION}/lib:\$${LD_LIBRARY_PATH}" >> ${SETUP_FILE}
	@echo "LD_LIBRARY_PATH=\$${INSTALL_DIR}/motif/${MOTIF_VERSION}/lib:\$${LD_LIBRARY_PATH}" >> ${SETUP_FILE}
	@echo "LD_LIBRARY_PATH=\$${INSTALL_DIR}/freetype/${FREETYPE_VERSION}/lib:\$${LD_LIBRARY_PATH}" >> ${SETUP_FILE}
	@echo "LD_LIBRARY_PATH=\$${INSTALL_DIR}/ncl/${NCL_VERSION}/lib:\$${LD_LIBRARY_PATH}" >> ${SETUP_FILE}
	@echo "" >> ${SETUP_FILE}
	@echo "# Setting PYTHONPATH:" >> ${SETUP_FILE}
	@echo "PYTHONPATH=\$${ROOT_DIR}/src/widgets:\$${PYTHONPATH}" >> ${SETUP_FILE}
	@echo "PYTHONPATH=\$${INSTALL_DIR}/imas/${IMASDD_VERSION}/solps/python/lib.linux-x86_64-${PYTHON_MAINVERSION}:\$${PYTHONPATH}" >> ${SETUP_FILE}
	@echo "PYTHONPATH=\$${INSTALL_DIR}/PyQt5/${PyQt_VERSION}/lib/python${PYTHON_MAINVERSION}/site-packages:\$${PYTHONPATH}" >> ${SETUP_FILE}
	@echo "PYTHONPATH=\$${INSTALL_DIR}/sip/${SIP_VERSION}/lib/python${PYTHON_MAINVERSION}/site-packages:\$${PYTHONPATH}" >> ${SETUP_FILE}
	@echo "PYTHONPATH=\$${INSTALL_DIR}/gnuplot-widget/python-${PYTHON_VERSION}-qt-${QT_VERSION}:\$${PYTHONPATH}" >> ${SETUP_FILE}
	@echo "" >> ${SETUP_FILE}
	@echo "# Exporting variables" >> ${SETUP_FILE}
	@echo "export PATH" >> ${SETUP_FILE}
	@echo "export LD_LIBRARY_PATH" >> ${SETUP_FILE}
	@echo "export PYTHONPATH" >> ${SETUP_FILE}
	@echo "export QTDIR=${BUILDROOT}/staging/qt/5.9.1" >> ${SETUP_FILE}
	@echo "export QT_QPA_FONTDIR=/usr/share/fonts/dejavu" >> ${SETUP_FILE}
	@echo "export QT_QPA_PLATFORM_PLUGIN_PATH=$${QTDIR}/plugins" >> ${SETUP_FILE}
	@echo "export PARAVIEW_PREFIX=${BUILDROOT}/staging/paraview/5.4.1" >> ${SETUP_FILE}
	@echo "export ids_path=\$${INSTALL_DIR}/imas/${IMASDD_VERSION}/solps/models/mdsplus" >> ${SETUP_FILE}
	@echo "export SOLPSGUI=${BUILDROOT}/src/gui" >> ${SETUP_FILE}
	@echo "export PYQTDESIGNERPATH=${BUILDROOT}/src/plugins/designer:\$${PYQTDESIGNERPATH}" >> ${SETUP_FILE}
	@echo "export IMAS_VERSION=${IMASDD_VERSION}" >> ${SETUP_FILE}
	@echo "export UAL_VERSION=${IMASUAL_VERSION}" >> ${SETUP_FILE}
	@echo "export PV_PLUGIN_PATH=\$${INSTALL_DIR}/ReadUALEdge-Plugin/1.5.0" >> ${SETUP_FILE}
	@echo "" >> ${SETUP_FILE}
	@echo "# Setting aliases" >> ${SETUP_FILE}
	@echo "alias solps=\"python3 \$${ROOT_DIR}/src/gui/solps.py\"" >> ${SETUP_FILE}
	@echo "alias solps_doc=\"xdg-open \$${ROOT_DIR}/doc/build/html/index.html\"" >> ${SETUP_FILE}
	@echo "alias solps_help=\"assistant -collectionFile \$${ROOT_DIR}/doc/build/qthelp/SOLPSGUI.qhc\"" >> ${SETUP_FILE}
	@echo "alias eirene=\"python3 \$${ROOT_DIR}/src/widgets/eirene.py\"" >> ${SETUP_FILE}
	@echo "alias b2=\"python3 \$${ROOT_DIR}/src/widgets/b2.py\"" >> ${SETUP_FILE}

# Solps GUI module file
${SOLPS_GUI_MOD}:
	@echo "Writing solps-gui module file to ${MODULE_DIR}/solps-gui/1.5"
	@install -d ${MODULE_DIR}/solps-gui
	@echo "#%Module1.0###################################################################" > ${SOLPS_GUI_MOD}
	@echo "##" >> ${SOLPS_GUI_MOD}
	@echo "## \$$name modulefile" >> ${SOLPS_GUI_MOD}
	@echo "##" >> ${SOLPS_GUI_MOD}
	@echo "proc ModulesHelp { } {" >> ${SOLPS_GUI_MOD}
	@echo "puts stderr "\tThis module sets the environment for $name v$ver"" >> ${SOLPS_GUI_MOD}
	@echo "}" >> ${SOLPS_GUI_MOD}
	@echo "conflict solps-gui" >> ${SOLPS_GUI_MOD}
	@echo "module-whatis "Graphical user interface for interacting with SOLPS-ITER and its output"" >> ${SOLPS_GUI_MOD}
	@echo "if { ! [ is-loaded imas ] } {" >> ${SOLPS_GUI_MOD}
	@echo "    module load imas/${IMASDD_VERSION}/solps" >> ${SOLPS_GUI_MOD}
	@echo "}" >> ${SOLPS_GUI_MOD}
	@echo "" >> ${SOLPS_GUI_MOD}
	@echo "if { ![ is-loaded Python/${PYTHON_VERSION} ] } {" >> ${SOLPS_GUI_MOD}
	@echo "    module load Python/${PYTHON_VERSION}" >> ${SOLPS_GUI_MOD}
	@echo "}" >> ${SOLPS_GUI_MOD}
	@echo "" >> ${SOLPS_GUI_MOD}
	@echo "if { ![ is-loaded PyQt5/${PyQt_VERSION} ] } {" >> ${SOLPS_GUI_MOD}
	@echo "    module load PyQt5/${PyQt_VERSION}" >> ${SOLPS_GUI_MOD}
	@echo "}" >> ${SOLPS_GUI_MOD}
	@echo "if { ![ is-loaded gnuplot-widget ] } {" >> ${SOLPS_GUI_MOD}
	@echo "    module load gnuplot-widget" >> ${SOLPS_GUI_MOD}
	@echo "}" >> ${SOLPS_GUI_MOD}
	@echo "" >> ${SOLPS_GUI_MOD}
	@echo "prepend-path PYTHONPATH         ${BUILDROOT}/src/widgets" >> ${SOLPS_GUI_MOD}
	@echo "prepend-path PYQTDESIGNERPATH   ${BUILDROOT}/src/plugins/designer" >> ${SOLPS_GUI_MOD}
	@echo "" >> ${SOLPS_GUI_MOD}
	@echo "set-alias solps {python3 ${BUILDROOT}/src/gui/solps.py $*}" >> ${SOLPS_GUI_MOD}
	@echo "set-alias solps_doc \"xdg-open ${BUILDROOT}/doc/build/html/index.html\"" >> ${SOLPS_GUI_MOD}
	@echo "set-alias eirene \"python3 -m eirene $*\"" >> ${SOLPS_GUI_MOD}
	@echo "set-alias b2 \"python3 -m b2 $*\"" >> ${SOLPS_GUI_MOD}

query-%:
	@echo $($(*))
deep-clean:
	rm -rf ${BUILDROOT}/download ${BUILDROOT}/build ${BUILDROOT}/staging
	rm -rf ${BUILDROOT}/package/setup.sh ${BUILDROOT}/package/setup.csh
