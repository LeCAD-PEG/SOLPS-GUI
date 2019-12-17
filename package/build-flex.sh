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
VERSION=${VERSION:-v2.6.3}
GIT="https://github.com/westes/flex.git"
SRC_DIR="${BUILD_DIR}/flex-${VERSION}"
INSTALL_DIR=${STAGING_DIR}/flex/${VERSION}


# Environment dependencies
if [ -e ${BUILDROOT}/package/setup.sh ]; then
    . ${BUILDROOT}/package/setup.sh
fi

# Prepare directories for download and building
install -d ${BUILD_DIR}
install -d ${STAGING_DIR}
install -d ${DOWNLOAD_DIR}

# Download source

# Unpack sources
if [ ! -d ${SRC_DIR} ]; then
    git clone --branch ${VERSION} --single-branch ${GIT} ${SRC_DIR}
fi

cd ${SRC_DIR}

# Configure
ln -sf /bin/true makeinfo
ln -sf /bin/true help2man
export PATH=${PWD}:${PATH}
if [ ! -e ${SRC_DIR}/.configured ]; then
    rm -rf ${INSTALL_DIR}
    ./autogen.sh
    ./configure --prefix=${INSTALL_DIR}
    touch ${SRC_DIR}/.configured
fi


# Build
if [ ! -e ${SRC_DIR}/.built ]; then
    # Texinfo is needed for compiling flex documenttion.
    # Since there is no way of saying no to compiling docs,
    # a disable check for job succession was performed.
    set +e
    make -j${MAKE_JOBS}
    # Create dummy doc files
    touch ${SRC_DIR}/doc/flex.1
    set -e
    touch ${SRC_DIR}/.built
fi

# Install
if [ ! -d ${INSTALL_DIR} ]; then
    make install
fi

# Generate Modulefile
if [ ! -d ${MODULE_DIR}/flex ]; then
    install -d ${MODULE_DIR}/flex
fi

cat << EOF > ${MODULE_DIR}/flex/${VERSION}
#%Module1.0#####################################################################
##
## \$name modulefile
##
proc ModulesHelp { } {
    puts stderr {

Description
===========
Flex is a fast lexical analyser generator. It is a tool for generating programs
that perform pattern-matching on text. Flex is a free (but non-GNU)
implementation of the original Unix lex program.


More information
================
 - Homepage: Homepage: https://www.gnu.org/software/flex/
    }
}


conflict flex
prepend-path LD_LIBRARY_PATH    ${INSTALL_DIR}/lib
prepend-path LIBRARY_PATH       ${INSTALL_DIR}/lib
prepend-path CPATH              ${INSTALL_DiR}/include
prepend-path PATH               ${INSTALL_DiR}/bin

EOF