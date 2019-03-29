#!/bin/sh -x
set -e


# Variables
BUILDROOT=${BUILDROOT:-$(cd ${0%/*} && echo ${PWD%/package})}
MAKE_JOBS=${MAKE_JOBS:-$(nproc)}

# Buildroot directories
MODULE_DIR=${MODULE_DIR:-${BUILDROOT}/modules}
BUILD_DIR=${BUILDROOT}/build
STAGING_DIR=${STAGING_DIR:-${BUILDROOT}/staging}
DOWNLOAD_DIR=${BUILDROOT}/download

# Package variables
VERSION=${VERSION:-5.4.1}
SOURCE="ParaView-v${VERSION}.tar.gz"
DOWNLOAD="http://www.paraview.org/files/v${VERSION%.*}/${SOURCE}"
SRC_DIR="${BUILD_DIR}/ParaView-v${VERSION}"
INSTALL_DIR=${INSTALL_DIR:-${STAGING_DIR}/paraview/${VERSION}}


# Environment dependencies
FORTRAN_COMPILER_FOR_CATALYST=${FORTRAN_COMPILER_FOR_CATALYST:-ifort}
# Environment dependencies
if [ -e ${BUILDROOT}/package/setup.sh ]; then
    . ${BUILDROOT}/package/setup.sh
fi
# case $(hostname -f) in
#   *.iter.org)
#     module purge
#     module load GCCcore/6.4.0 binutils/2.28-GCCcore-6.4.0 intel/2018a GCC/6.4.0-2.28 Blitz++/0.10-GCCcore-6.4.0
#     module load Python/2.7.14-GCCcore-6.4.0-bare
#     # module load OpenSSL/1.0.2g-GCC-4.8.3
#     module load OpenSSL/1.0.2g-goolf-1.5.16
#     export CC=gcc
#     export CXX=g++
#         CMAKE_EXTRA_FLAGS=${CMAKE_EXTRA_FLAGS:-\
#           -DCMAKE_EXE_LINKER_FLAGS:STRING=-L${EBROOTOPENSSL}/lib}
#     #PARAVIEW_EXTRA_FLAGS=${PARAVIEW_EXTRA_FLAGS:-\
#         #          -DPARAVIEW_ENABLE_PYTHON:BOOL=OFF}
#     MAKE_JOBS=${MAKE_JOBS:-8}
#     ;;
#   *.marconi.cineca.it) # EU-IM Gateway with CentOS7.2
#     . /etc/profile.d.gw/modules.sh
#     module purge
#     module load cineca imasenv cmake/3.5.2
#     module switch itm-python/2.7
#     module unload matlab
#     QT_VERSION=${QT_VERSION:-4.8.7}
#     module load itm-qt/${QT_VERSION}
#     STAGING_QT=${QTDIR}
#     MAKE_JOBS=${MAKE_JOBS:-36}
#     export CXXFLAGS=-fpermissive
#     PARAVIEW_EXTRA_FLAGS=${PARAVIEW_EXTRA_FLAGS:-\
#                         -DPARAVIEW_USE_MPI:BOOL=ON}
#     ;;
#   *)
#     QT_VERSION=${QT_VERSION:-4.8.7}
#     STAGING_QT=${BUILDROOT}/staging/qt/${QT_VERSION}
#     CMAKE_VERSION=${CMAKE_VERSION:-3.10.1}
#     export PATH=${STAGING_DIR}/cmake/${CMAKE_VERSION}/bin:${PATH}
#     export PATH=${STAGING_QT}/bin:${PATH}
#     export LD_LIBRARY_PATH=${STAGING_DIR}/qt/${QT_VERSION}/lib:${LD_LIBRARY_PATH}

#     ;;
# esac

# Prepare directories for download and building
install -d ${BUILD_DIR}
install -d ${STAGING_DIR}
install -d ${DOWNLOAD_DIR}

# Download source
if [ ! -f ${DOWNLOAD_DIR}/${SOURCE} ]; then
    wget -O ${DOWNLOAD_DIR}/${SOURCE} --no-check-certificate ${DOWNLOAD}
fi

cd ${BUILD_DIR}

# Unpack sources
if [ ! -d ${BUILD_DIR}/${SOURCE%.tar*} ]; then
    tar xzf ${DOWNLOAD_DIR}/${SOURCE}
fi

# Configure
if [ ! -e ${SRC_DIR}/.configured ]; then
    rm -rf ${INSTALL_DIR}
    # Ignore git describe tags as we are building ParaView from tar.gz
    sed -i -e "/^determine_version/d" ${SRC_DIR}/CMakeLists.txt
    install -d ${BUILD_DIR}/paraview-${VERSION}
    cd ${BUILD_DIR}/paraview-${VERSION}

    if [ ${QT_VERSION%%.*} = 5 ]
        then VTK_RENDERING_BACKEND=OpenGL2
        else VTK_RENDERING_BACKEND=OpenGL
    fi

    cmake -DCMAKE_BUILD_TYPE:STRING=Release \
    -DVTK_RENDERING_BACKEND:STRING=${VTK_RENDERING_BACKEND} \
    -DPARAVIEW_QT_VERSION:STRING=${QT_VERSION%%.*} \
    -DVTK_QT_VERSION:STRING=${QT_VERSION%%.*} \
        -DBUILD_SHARED_LIBS:BOOL=ON  \
        -DPARAVIEW_INSTALL_DEVELOPMENT_FILES:BOOL=ON \
        -DBUILD_TESTING:BOOL=OFF \
        -DPARAVIEW_ENABLE_PYTHON:BOOL=ON \
        -DCMAKE_Fortran_COMPILER:STRING=${FORTRAN_COMPILER_FOR_CATALYST} \
        -DQT_QMAKE_EXECUTABLE:FILEPATH=${STAGING_DIR}/qt/${QT_VERSION}/bin/qmake \
        -DCMAKE_INSTALL_PREFIX:PATH=${INSTALL_DIR} \
    ${PARAVIEW_EXTRA_FLAGS} ${SRC_DIR}
    touch ${SRC_DIR}/.configured
fi


# Build
if [ ! -e ${SRC_DIR}/.built ]; then
    make -j${MAKE_JOBS} VERBOSE=0
    touch ${SRC_DIR}/.built
fi

# Install
if [ ! -d ${INSTALL_DIR} ]; then
    install -d ${INSTALL_DIR}
    make install
fi

# Post Installation
DOC_VERSION=${DOC_VERSION:-${VERSION%.*}.0}
INSTALL_DOC_DIR=${INSTALL_DIR}/share/paraview-${VERSION%.*}/doc
install -d ${INSTALL_DOC_DIR}
for file in ParaViewGettingStarted-${DOC_VERSION%-*}.pdf \
    ParaViewTutorial.pdf  ParaViewGuide-${DOC_VERSION%-*}.pdf \
    ParaViewCatalystGuide-${DOC_VERSION%-*}.pdf  ; do
    if [ ! -f ${DOWNLOAD_DIR}/${file} ]; then
         wget -O ${DOWNLOAD_DIR}/${file} --no-check-certificate \
             http://www.paraview.org/files/v${VERSION%.*}/${file}
    fi
    noParaView=${file#ParaView}
    noVersion=${noParaView%-*}
    noPdf=${noVersion%.pdf}
    target=${noPdf}.pdf
    install -m 444 ${DOWNLOAD_DIR}/${file} ${INSTALL_DOC_DIR}/${target}
done


# Generate Modulefile
if [ ! -d ${MODULE_DIR}/ParaView ]; then
    install -d ${MODULE_DIR}/ParaView
fi

cat << EOF > ${MODULE_DIR}/ParaView/${VERSION}
#%Module1.0#####################################################################
##
## \$name modulefile
##
proc ModulesHelp { } {
    puts stderr {

Description
===========
ParaView is a scientific parallel visualizer.


More information
================
 - Homepage: http://www.paraview.org
    }
}

module-whatis {Description: ParaView is a scientific parallel visualizer.}
module-whatis {Homepage: http://www.paraview.org}

if { ![ is-loaded Qt4/${QT_VERSION} ] } {
    module load Qt4/${QT_VERSION}
}

conflict ParaView
prepend-path CPATH              ${INSTALL_DIR}/include
prepend-path LD_LIBRARY_PATH    ${INSTALL_DIR}/lib
prepend-path LIBRARY_DIR        ${INSTALL_DIR}/lib
prepend-path PKG_CONFIG_PATH    ${INSTALL_DIR}/lib/pkgconfig
prepend-path PATH               ${INSTALL_DIR}/bin
EOF
