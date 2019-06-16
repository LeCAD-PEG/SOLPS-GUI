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
VERSION=${VERSION:-7.64.1}
GIT="https://github.com/curl/curl.git"
SRC_DIR="${BUILD_DIR}/curl-${VERSION}"
INSTALL_DIR=${STAGING_DIR}/curl/${VERSION}


# Environment dependencies


# Prepare directories for download and building
install -d ${BUILD_DIR}
install -d ${STAGING_DIR}
install -d ${DOWNLOAD_DIR}

# Download source

# Unpack sources
if [ ! -d ${SRC_DIR} ]; then
    git clone --branch "curl-$(tr '.' '_' <<< ${VERSION})" --single-branch ${GIT} ${SRC_DIR}
fi

cd ${SRC_DIR}

# Configure
if [ ! -e ${SRC_DIR}/.configured ]; then
    rm -rf ${INSTALL_DIR}
    #LDFLAGS="-L/usr/lib64" CFLAGS="-I/usr/include"
    autoreconf -i
    ./configure --prefix=${INSTALL_DIR}
    touch ${SRC_DIR}/.configured
fi

# Build
if [ ! -e ${SRC_DIR}/.built ]; then
    make -j${MAKE_JOBS}
    touch ${SRC_DIR}/.built
fi

# Install
if [ ! -d ${INSTALL_DIR} ]; then
    make install
fi

# Generate Modulefile
if [ ! -d ${MODULE_DIR}/cURL ]; then
    install -d ${MODULE_DIR}/cURL
fi

cat << EOF > ${MODULE_DIR}/cURL/${VERSION}
#%Module1.0#####################################################################
##
## \$name modulefile
##
proc ModulesHelp { } {
    puts stderr {

Description
===========
A command line tool and library for transferring data with URL syntax,
supporting HTTP, HTTPS, FTP, FTPS, GOPHER, TFTP, SCP, SFTP, SMB, TELNET, DICT,
LDAP, LDAPS, FILE, IMAP, SMTP, POP3, RTSP and RTMP. libcurl offers a myriad of
powerful features.

More information
================
 - Homepage: https://curl.haxx.se/
    }
}

module-whatis {Description:
A command line tool and library for transferring data with URL syntax,
supporting HTTP, HTTPS, FTP, FTPS, GOPHER, TFTP, SCP, SFTP, SMB, TELNET, DICT,
LDAP, LDAPS, FILE, IMAP, SMTP, POP3, RTSP and RTMP. libcurl offers a myriad of
powerful features.
}
module-whatis {Homepage: https://curl.haxx.se/}

conflict cURL
prepend-path CPATH              ${INSTALL_DIR}/inclue
prepend-path LD_LIBRARY_PATH    ${INSTALL_DIR}/lib
prepend-path LIBRARY_PATH       ${INSTALL_DIR}/lib
prepend-path PATH               ${INSTALL_DIR}/bin
prepend-path PKG_CONFIG_PATH    ${INSTALL_DIR}/lib/pkg-config
EOF