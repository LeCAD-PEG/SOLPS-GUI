# source this bash file for local environment if PyQT is provided locally
export QTDIR="${PWD}/staging/qt/5.5.1"
export PATH="${PWD}/staging/bin:${QTDIR}/bin:${PATH}"
export LD_LIBRARY_PATH="${PWD}/staging/lib:${QTDIR}/lib:${LD_LIBRARY_PATH}"
export PKG_CONFIG_PATH="${PWD}/staging/lib/pkgconfig:${PKG_CONFIG_PATH}"
export PYTHONPATH="${PWD}/src/plugins/widgets:${PYTHONPATH}"
export PYQTDESIGNERPATH="${PWD}/src/plugins/python:${PYQTDESIGNERPATH}"
