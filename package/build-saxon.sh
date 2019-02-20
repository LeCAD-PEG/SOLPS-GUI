#!/bin/sh -x
set -e
BUILDROOT=${BUILDROOT:-$(cd ${0%/*} && echo ${PWD%/package})}
BUILD_DIR=${BUILDROOT}/build
DOWNLOAD_DIR=${BUILDROOT}/download
STAGING_DIR=${BUILDROOT}/staging
SAXON_VERSION=${SAXON_VERSION:-HE9-8-0-12J}

MAKE_JOBS=${MAKE_JOBS:-$(nproc)}

install -d ${BUILD_DIR}
install -d ${STAGING_DIR}
install -d ${DOWNLOAD_DIR}

# Download and extract SAXON
SAXON_SOURCE="Saxon${SAXON_VERSION}.zip"
SAXON_DOWNLOAD="https://sourceforge.net/projects/saxon/files/Saxon-HE/9.8/Saxon${SAXON_VERSION}.zip/download"

if [ ! -f ${DOWNLOAD_DIR}/${SAXON_SOURCE} ]; then
	wget -O ${DOWNLOAD_DIR}/${SAXON_SOURCE} ${SAXON_DOWNLOAD}
fi

if [ ! -e ${STAGING_DIR}/saxon/saxon9he.jar ]; then
	unzip ${DOWNLOAD_DIR}/${SAXON_SOURCE} -d ${STAGING_DIR}/saxon
fi
