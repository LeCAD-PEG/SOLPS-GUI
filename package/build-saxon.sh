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

#Package variables
VERSION=${VERSION:-HE9-8-0-12J}
SOURCE="Saxon${VERSION}.zip"
DOWNLOAD="https://sourceforge.net/projects/saxon/files/Saxon-HE/9.8/Saxon${VERSION}.zip/download"
INSTALL_DIR=${STAGING_DIR}/saxon/${VERSION}

# Environment dependencies

# Prepare directories for download and building
install -d ${BUILD_DIR}
install -d ${STAGING_DIR}
install -d ${DOWNLOAD_DIR}


# Download source
if [ ! -f ${DOWNLOAD_DIR}/${SOURCE} ]; then
    wget --insecure --no-check-certificate -O ${DOWNLOAD_DIR}/${SOURCE} \
        ${DOWNLOAD}
fi

cd ${BUILD_DIR}

# Unpack sources

# Configure

# Build

# Install
if [ ! -d ${INSTALL_DIR} ]; then
    install -d ${INSTALL_DIR}
    unzip ${DOWNLOAD_DIR}/${SOURCE} -d ${INSTALL_DIR}
fi

if [ ! -d ${MODULE_DIR}/saxon ]; then
    install -d ${MODULE_DIR}/saxon
fi

cat << EOF > ${MODULE_DIR}/saxon/${VERSION}
#%Module1.0#####################################################################
##
## \$name modulefile
##
proc ModulesHelp { } {
    puts stderr { Open Source SAXON XSLT processor developed by Saxonica Limited. - Homepage: http://saxon.sourceforge.net
    }
}

module-whatis {Description: Open Source SAXON XSLT processor developed by Saxonica Limited. - Homepage: http://saxon.sourceforge.net}

conflict saxon
prepend-path    CLASSPATH               ${INSTALL_DIR}/saxon9-test.jar
prepend-path    CLASSPATH               ${INSTALL_DIR}/saxon9-xqj.jar
prepend-path    CLASSPATH               ${INSTALL_DIR}/saxon9he.jar
EOF
