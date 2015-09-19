# source this file for local setup environment
export QTDIR="${PWD}/staging/qt/5.4.2"
export PATH="${PWD}/staging/bin:${QTDIR}/bin:${PATH}"
export LD_LIBRARY_PATH="${PWD}/staging/lib:${LD_LIBRARY_PATH}"
export PKG_CONFIG_PATH="${STAGING_DIR}/lib/pkgconfig:${PKG_CONFIG_PATH}"
