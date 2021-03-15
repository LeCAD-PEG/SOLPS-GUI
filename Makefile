
# Use realpath for the last time to remove trailing slash
BUILDROOT:=$(realpath $(dir $(realpath $(firstword $(MAKEFILE_LIST)))))
STAGING_DIR ?= ${BUILDROOT}/staging
MODULE_DIR ?= ${BUILDROOT}/modules

# SOLPS-GUI
SOLPS_GUI_VERSION=1.5.0

OPENBLAS_VERSION=0.3.13
PYTHON_VERSION=3.9.2
FFI_VERSION=3.3
PYTHON_MAINVERSION=3.9
NUMPY_VERSION=1.20.1
SCIPY_VERSION=1.5.2
GNUPLOT_VERSION=5.2.8

QT_VERSION=5.15.2
# LLVM_VERSION=11.1.0
# PYSIDE2_VERSION=5.15.2

PyQt_VERSION=5.15.2
SIP_VERSION=4.19.25
# ParaView specific version
PARAVIEW_VERSION=5.8.1
CMAKE_VERSION=3.15.4

# IMAS
BLITZ_VERSION=1.0.2
MDSPLUS_VERSION=7.96.8
LIBXML2_VERSION=2.9.10
SAXON_VERSION=HE9-8-0-12J
IMASUAL_VERSION=4.8.7
IMASDD_VERSION=3.31.0
# Minor version is used for compatibility compiling.
IMAS_MINOR_VERSION=31

# SOLPS-ITER
GLI_VERSION=4.5.30
GR_VERSION=0.0.94
GGD_VERSION=1.9.1
SOLPS_VERSION=develop
MSCL_VERSION=1.1.1
CURL_VERSION=7.64.1
HDF5_VERSION=1.10.6
NETCDF_VERSION=4.7.4
NETCDF_FORTRAN_VERSION=4.5.3
FREETYPE_VERSION=2.10.0
NCL_VERSION=6.5.0
MOTIF_VERSION=2.3.8
OPENMPI_VERSION=4.0.0
FLEX_VERSION=2.6.3

SETUP_FILE="setupenv.sh"
SOLPS_ITER_MOD=${MODULE_DIR}/solps-iter/${SOLPS_VERSION}

.PHONY: gr gli openblas mscl ggd python libxml2 saxon blitz cmake mdsplus \
	imas solps-iter pyqt solps-gui curl hdf5 netcdf openmpi motif \
	llvm paraview-plugin-iter

all: solps-iter solps-gui

package/setup.sh: configure
	./configure

config: package/setup.sh

${STAGING_DIR}/llvm/${LLVM_VERSION}:
	sed -i -e "/^VERSION/s/:-[^}]*}/:-${LLVM_VERSION}}/" package/build-llvm.sh

	CMAKE_VERSION=${CMAKE_VERSION} \
	PYTHON_VERSION=${PYTHON_VERSION} \
	./package/build-llvm.sh

llvm : python cmake ${STAGING_DIR}/llvm/${LLVM_VERSION}

${STAGING_DIR}/GR/${GR_VERSION}:
	sed -i -e "/^VERSION/s/:-[^}]*}/:-${GR_VERSION}}/" package/build-gr.sh

	./package/build-gr.sh

gr: ${STAGING_DIR}/GR/${GR_VERSION}

${STAGING_DIR}/GLI/${GLI_VERSION}:
	sed -i -e "/^VERSION/s/:-[^}]*}/:-${GLI_VERSION}}/" package/build-gli.sh

	./package/build-gli.sh

gli: ${STAGING_DIR}/GLI/${GLI_VERSION}

${STAGING_DIR}/saxon/${SAXON_VERSION}:
	sed -i -e "/^VERSION/s/:-[^}]*}/:-${SAXON_VERSION}}/" package/build-saxon.sh

	./package/build-saxon.sh

saxon: ${STAGING_DIR}/saxon/${SAXON_VERSION}

${STAGING_DIR}/blitz/${BLITZ_VERSION}:
	sed -i -e "/^VERSION/s/:-[^}]*}/:-${BLITZ_VERSION}}/" package/build-blitz.sh

	CMAKE_VERSION=${CMAKE_VERSION} \
	./package/build-blitz.sh

blitz: cmake ${STAGING_DIR}/blitz/${BLITZ_VERSION}

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

${STAGING_DIR}/openblas/${OPENBLAS_VERSION}:
	sed -i -e "/^VERSION/s/:-[^}]*}/:-${OPENBLAS_VERSION}}/" package/build-openblas.sh

	./package/build-openblas.sh

openblas: ${STAGING_DIR}/openblas/${OPENBLAS_VERSION}

${STAGING_DIR}/mscl/${MSCL_VERSION}:
	sed -i -e "/^VERSION/s/:-[^}]*}/:-${MSCL_VERSION}}/" package/build-mscl.sh

	./package/build-mscl.sh

mscl: ${STAGING_DIR}/mscl/${MSCL_VERSION}

${STAGING_DIR}/libffi/${FFI_VERSION}:
	sed -i -e "/^VERSION/s/:-[^}]*}/:-${FFI_VERSION}}/" package/build-ffi.sh
	./package/build-ffi.sh

ffi: config ${STAGING_DIR}/libffi/${FFI_VERSION}

${STAGING_DIR}/python/${PYTHON_VERSION}:
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

python: config openblas ${STAGING_DIR}/python/${PYTHON_VERSION}

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

${STAGING_DIR}/pyside2/${PYSIDE2_VERSION}:
	sed -i -e "/^VERSION/s/:-[^}]*}/:-${PYSIDE2_VERSION}}/" package/build-pyside2.sh

	LIBXML2_VERSION=${LIBXML2_VERSION} \
	LLVM_VERSION=${LLVM_VERSION} \
	PYTHON_VERSION=${PYTHON_VERSION} \
	QT_VERSION=${QT_VERSION} \
	CMAKE_VERSION=${CMAKE_VERSION} \
	./package/build-pyside2.sh

pyside2: config libxml2 python cmake llvm qt5 ${STAGING_DIR}/pyside2/${PYSIDE2_VERSION}

${STAGING_DIR}/pyqt5/${PyQt_VERSION}:
	sed -i -e "/^VERSION/s/:-[^}]*}/:-${PyQt_VERSION}}/" package/build-pyqt.sh

	PYTHON_VERSION=${PYTHON_VERSION} \
	QT_VERSION=${QT_VERSION} \
	SIP_VERSION=${SIP_VERSION} \
	./package/build-pyqt.sh

pyqt: config python qt5 sip ${STAGING_DIR}/pyqt5/${PyQt_VERSION}

${STAGING_DIR}/gnuplot/${GNUPLOT_VERSION}:
	sed -i -e "/^VERSION/s/:-[^}]*}/:-${GNUPLOT_VERSION}}/" package/build-gnuplot.sh

	QT_VERSION=${QT_VERSION} \
	./package/build-gnuplot.sh

gnuplot: config qt5 ${STAGING_DIR}/gnuplot/${GNUPLOT_VERSION}

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
	PYTHON_VERSION=${PYTHON_VERSION} \
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

motif: config freetype flex ${STAGING_DIR}/motif/${MOTIF_VERSION}

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

solps-gui: config imas pyqt gnuplot setupenv.sh

setupenv.sh: Makefile
	@echo "Writing environemnt to ${BUILDROOT}/${SETUP_FILE}"
	@echo "ROOT_DIR=${BUILDROOT}" > ${SETUP_FILE}
	@echo "#Setting versions" >> ${SETUP_FILE}
	@echo "if [ \$$# -eq 0 ]; then" >> ${SETUP_FILE}
	@echo "    echo 'Skipping version setting!'" >> ${SETUP_FILE}
	@echo "else" >> ${SETUP_FILE}
	@echo "    export BUILDROOT=\$${ROOT_DIR}" >> ${SETUP_FILE}
	@echo "    export STAGING_DIR=\$${ROOT_DIR}/staging" >> ${SETUP_FILE}
	@echo "    export SOLPS_GUI_VERSION=${SOLPS_GUI_VERSION}" >> ${SETUP_FILE}
	@echo "    export OPENBLAS_VERSION=${OPENBLAS_VERSION}" >> ${SETUP_FILE}
	@echo "    export PYTHON_VERSION=${PYTHON_VERSION}" >> ${SETUP_FILE}
	@echo "    export PYTHON_MAINVERSION=${PYTHON_MAINVERSION}" >> ${SETUP_FILE}
	@echo "    export NUMPY_VERSION=${NUMPY_VERSION}" >> ${SETUP_FILE}
	@echo "    export SCIPY_VERSION=${SCIPY_VERSION}" >> ${SETUP_FILE}
	@echo "    export GNUPLOT_VERSION=${GNUPLOT_VERSION}" >> ${SETUP_FILE}
	@echo "    export QT_VERSION=${QT_VERSION}" >> ${SETUP_FILE}
	@echo "    export PyQt_VERSION=${PyQt_VERSION}" >> ${SETUP_FILE}
	@echo "    export SIP_VERSION=${SIP_VERSION}" >> ${SETUP_FILE}
	@echo "    export PARAVIEW_VERSION=${PARAVIEW_VERSION}" >> ${SETUP_FILE}
	@echo "    export CMAKE_VERSION=${CMAKE_VERSION}" >> ${SETUP_FILE}
	@echo "    export BLITZ_VERSION=${BLITZ_VERSION}" >> ${SETUP_FILE}
	@echo "    export MDSPLUS_VERSION=${MDSPLUS_VERSION}" >> ${SETUP_FILE}
	@echo "    export LIBXML2_VERSION=${LIBXML2_VERSION}" >> ${SETUP_FILE}
	@echo "    export SAXON_VERSION=${SAXON_VERSION}" >> ${SETUP_FILE}
	@echo "    export IMASUAL_VERSION=${IMASUAL_VERSION}" >> ${SETUP_FILE}
	@echo "    export IMASDD_VERSION=${IMASDD_VERSION}" >> ${SETUP_FILE}
	@echo "    export IMAS_MINOR_VERSION=${IMAS_MINOR_VERSION}" >> ${SETUP_FILE}
	@echo "    export GLI_VERSION=${GLI_VERSION}" >> ${SETUP_FILE}
	@echo "    export GR_VERSION=${GR_VERSION}" >> ${SETUP_FILE}
	@echo "    export GGD_VERSION=${GGD_VERSION}" >> ${SETUP_FILE}
	@echo "    export SOLPS_VERSION=${SOLPS_VERSION}" >> ${SETUP_FILE}
	@echo "    export MSCL_VERSION=${MSCL_VERSION}" >> ${SETUP_FILE}
	@echo "    export CURL_VERSION=${CURL_VERSION}" >> ${SETUP_FILE}
	@echo "    export HDF5_VERSION=${HDF5_VERSION}" >> ${SETUP_FILE}
	@echo "    export NETCDF_VERSION=${NETCDF_VERSION}" >> ${SETUP_FILE}
	@echo "    export NETCDF_FORTRAN_VERSION=${NETCDF_FORTRAN_VERSION}" >> ${SETUP_FILE}
	@echo "    export FREETYPE_VERSION=${FREETYPE_VERSION}" >> ${SETUP_FILE}
	@echo "    export NCL_VERSION=${NCL_VERSION}" >> ${SETUP_FILE}
	@echo "    export MOTIF_VERSION=${MOTIF_VERSION}" >> ${SETUP_FILE}
	@echo "    export OPENMPI_VERSION=${OPENMPI_VERSION}" >> ${SETUP_FILE}
	@echo "    export FLEX_VERSION=${FLEX_VERSION}" >> ${SETUP_FILE}
	@echo "fi" >> ${SETUP_FILE}
	@echo "source \$${ROOT_DIR}/package/setup.sh" >> ${SETUP_FILE}
	@echo "INSTALL_DIR=\$${ROOT_DIR}/staging" >> ${SETUP_FILE}
	@echo "" >> ${SETUP_FILE}
	@echo "# Setting PATH:" >> ${SETUP_FILE}
	@echo "PATH=\$${INSTALL_DIR}/Python/${PYTHON_VERSION}/bin:\$${PATH}" >> ${SETUP_FILE}
	@echo "PATH=\$${INSTALL_DIR}/sip/${SIP_VERSION}/bin:\$${PATH}" >> ${SETUP_FILE}
	@echo "PATH=\$${INSTALL_DIR}/qt/${QT_VERSION}/bin:\$${PATH}" >> ${SETUP_FILE}
	@echo "PATH=\$${INSTALL_DIR}/cmake/${CMAKE_VERSION}/bin:\$${PATH}" >> ${SETUP_FILE}
	@echo "PATH=\$${INSTALL_DIR}/paraview/${PARAVIEW_VERSION}/bin:\$${PATH}" >> ${SETUP_FILE}
	@echo "PATH=\$${INSTALL_DIR}/openmpi/${OPENMPI_VERSION}/bin:\$${PATH}" >> ${SETUP_FILE}
	@echo "PATH=\$${INSTALL_DIR}/gnuplot/${GNUPLOT_VERSION}/bin:\$${PATH}" >> ${SETUP_FILE}
	@echo "" >> ${SETUP_FILE}
	@echo "# Setting LD_LIBRARY_PATH:" >> ${SETUP_FILE}
	@echo "LD_LIBRARY_PATH=\$${INSTALL_DIR}/Python/${PYTHON_VERSION}/lib:\$${LD_LIBRARY_PATH}" >> ${SETUP_FILE}
	@echo "LD_LIBRARY_PATH=\$${INSTALL_DIR}/blitz/${BLITZ_VERSION}/lib:\$${LD_LIBRARY_PATH}" >> ${SETUP_FILE}
	@echo "LD_LIBRARY_PATH=\$${INSTALL_DIR}/qt/${QT_VERSION}/lib:\$${LD_LIBRARY_PATH}" >> ${SETUP_FILE}
	@echo "LD_LIBRARY_PATH=\$${INSTALL_DIR}/pyqt5/${PyQt_VERSION}/lib:\$${LD_LIBRARY_PATH}" >> ${SETUP_FILE}
	@echo "LD_LIBRARY_PATH=\$${INSTALL_DIR}/mdsplus/${MDSPLUS_VERSION}/lib:\$${LD_LIBRARY_PATH}" >> ${SETUP_FILE}
	@echo "LD_LIBRARY_PATH=\$${INSTALL_DIR}/imas/${IMASDD_VERSION}/solps/lib:\$${LD_LIBRARY_PATH}" >> ${SETUP_FILE}
	@echo "LD_LIBRARY_PATH=\$${INSTALL_DIR}/libxml2/${LIBXML2_VERSION}/solps/lib:\$${LD_LIBRARY_PATH}" >> ${SETUP_FILE}
	@echo "LD_LIBRARY_PATH=\$${INSTALL_DIR}/hdf5/${HDF5_VERSION}/lib:\$${LD_LIBRARY_PATH}" >> ${SETUP_FILE}
	@echo "LD_LIBRARY_PATH=\$${INSTALL_DIR}/curl/${CURL_VERSION}/lib:\$${LD_LIBRARY_PATH}" >> ${SETUP_FILE}
	@echo "LD_LIBRARY_PATH=\$${INSTALL_DIR}/openmpi/${OPENMPI_VERSION}/lib:\$${LD_LIBRARY_PATH}" >> ${SETUP_FILE}
	@echo "LD_LIBRARY_PATH=\$${INSTALL_DIR}/motif/${MOTIF_VERSION}/lib:\$${LD_LIBRARY_PATH}" >> ${SETUP_FILE}
	@echo "LD_LIBRARY_PATH=\$${INSTALL_DIR}/freetype/${FREETYPE_VERSION}/lib:\$${LD_LIBRARY_PATH}" >> ${SETUP_FILE}
	@echo "LD_LIBRARY_PATH=\$${INSTALL_DIR}/ncl/${NCL_VERSION}/lib:\$${LD_LIBRARY_PATH}" >> ${SETUP_FILE}
	@echo "LD_LIBRARY_PATH=\$${INSTALL_DIR}/netcdf/${NETCDF_VERSION}/lib:\$${LD_LIBRARY_PATH}" >> ${SETUP_FILE}
	@echo "LD_LIBRARY_PATH=\$${INSTALL_DIR}/netcdf/${NETCDF_VERSION}/lib64:\$${LD_LIBRARY_PATH}" >> ${SETUP_FILE}
	@echo "" >> ${SETUP_FILE}
	@echo "# Setting PYTHONPATH:" >> ${SETUP_FILE}
	@echo "PYTHONPATH=\$${ROOT_DIR}/src/widgets:\$${PYTHONPATH}" >> ${SETUP_FILE}
	@echo "PYTHONPATH=\$${INSTALL_DIR}/imas/${IMASDD_VERSION}/solps/python/lib.linux-x86_64-${PYTHON_MAINVERSION}:\$${PYTHONPATH}" >> ${SETUP_FILE}
	@echo "PYTHONPATH=\$${INSTALL_DIR}/pyqt5/${PyQt_VERSION}/lib/python${PYTHON_MAINVERSION}/site-packages:\$${PYTHONPATH}" >> ${SETUP_FILE}
	@echo "PYTHONPATH=\$${INSTALL_DIR}/sip/${SIP_VERSION}/lib:\$${PYTHONPATH}" >> ${SETUP_FILE}
	@echo "PYTHONPATH=\$${INSTALL_DIR}/gnuplot-widget/python-${PYTHON_VERSION}-qt-${QT_VERSION}:\$${PYTHONPATH}" >> ${SETUP_FILE}
	@echo "" >> ${SETUP_FILE}
	@echo "# Exporting variables" >> ${SETUP_FILE}
	@echo "export PATH" >> ${SETUP_FILE}
	@echo "export LD_LIBRARY_PATH" >> ${SETUP_FILE}
	@echo "export PYTHONPATH" >> ${SETUP_FILE}
	@echo "export QTDIR=${BUILDROOT}/staging/qt/5.9.1" >> ${SETUP_FILE}
	@echo "export QT_QPA_FONTDIR=/usr/share/fonts/dejavu" >> ${SETUP_FILE}
	@echo "export QT_QPA_PLATFORM_PLUGIN_PATH=\$${QTDIR}/plugins" >> ${SETUP_FILE}
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

query-%:
	@echo $($(*))
deep-clean:
	rm -rf ${BUILDROOT}/download ${BUILDROOT}/build ${BUILDROOT}/staging
	rm -rf ${BUILDROOT}/package/setup.sh ${BUILDROOT}/package/setup.csh
