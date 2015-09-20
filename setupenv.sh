# source this bash file for local setup environment
export QTDIR="${PWD}/staging/qt/5.5.0"
export PATH="${PWD}/staging/bin:${QTDIR}/bin:${PATH}"
export LD_LIBRARY_PATH="${PWD}/staging/lib:${QTDIR}/lib:${LD_LIBRARY_PATH}"
export PKG_CONFIG_PATH="${STAGING_DIR}/lib/pkgconfig:${PKG_CONFIG_PATH}"
