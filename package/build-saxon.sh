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
install -d ${STAGING_DIR}/saxon/${SAXON_VERSION}

# Download and extract SAXON
SAXON_SOURCE="Saxon${SAXON_VERSION}.zip"
SAXON_DOWNLOAD="https://sourceforge.net/projects/saxon/files/Saxon-HE/9.8/Saxon${SAXON_VERSION}.zip/download"

if [ ! -f ${DOWNLOAD_DIR}/${SAXON_SOURCE} ]; then
	wget -O ${DOWNLOAD_DIR}/${SAXON_SOURCE} ${SAXON_DOWNLOAD}
fi

if [ ! -e ${STAGING_DIR}/saxon/${SAXON_VERSION}/saxon9he.jar ]; then
	unzip ${DOWNLOAD_DIR}/${SAXON_SOURCE} -d ${STAGING_DIR}/saxon/${SAXON_VERSION}
fi

MODULE_DIR=${MDULE_DIR:-${BUILDROOT}/modules}
if [ ! -d ${MODULE_DIR}/saxon ]; then
	install -d ${MODULE_DIR}/saxon
fi

cat << EOF > ${MODULE_DIR}/saxon/${SAXON_VERSION}
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
prepend-path    CLASSPATH               ${STAGING_DIR}/saxon/${SAXON_VERSION}/saxon9-test.jar
prepend-path    CLASSPATH               ${STAGING_DIR}/saxon/${SAXON_VERSION}/saxon9-xqj.jar
prepend-path    CLASSPATH               ${STAGING_DIR}/saxon/${SAXON_VERSION}/saxon9he.jar
EOF
