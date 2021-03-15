#!/bin/sh
set -e
BUILDROOT=${BUILDROOT:-$( cd "$( dirname "${BASH_SOURCE[0]:-$0}" )" &> /dev/null && echo ${PWD%/package} )}
PACKAGE="saxon"
VERSION=${VERSION:-HE9-8-0-12J}
MAJOR_VERSION=${VERSION%.*}
DOWNLOAD_LINK="https://sourceforge.net/projects/saxon/files/Saxon-HE/9.8/Saxon${VERSION}.zip/download"
FILENAME="${PACKAGE}-${VERSION}.zip"

if  [ -e ${BUILDROOT}/package/solps_gui_utils.sh ]; then
    source ${BUILDROOT}/package/solps_gui_utils.sh
fi
if  [ -e ${BUILDROOT}/package/setup.sh ]; then
    source ${BUILDROOT}/package/setup.sh
fi

# Download source
if [ ! -f ${DOWNLOAD_DIR}/${FILENAME} ]; then
    wget --no-check-certificate -O ${DOWNLOAD_DIR}/${FILENAME} \
        ${DOWNLOAD_LINK}
fi
# Install
if [ ! -d ${PACKAGE_INSTALL_DIR} ]; then
    install -d ${PACKAGE_INSTALL_DIR}
    unzip ${DOWNLOAD_DIR}/${FILENAME} -d ${PACKAGE_INSTALL_DIR}
fi
