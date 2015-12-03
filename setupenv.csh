# source this csh file for local setup environment if PyQT is provided locally
setenv QTDIR "${PWD}/staging/qt/5.5.1"
setenv PATH "${PWD}/staging/bin:${QTDIR}/bin:${PATH}"

if !($?LD_LIBRARY_PATH) then
    setenv LD_LIBRARY_PATH "${PWD}/staging/lib:${QTDIR}/lib"
else
    setenv LD_LIBRARY_PATH "${PWD}/staging/lib:${QTDIR}/lib:${LD_LIBRARY_PATH}"
endif

if !($?PKG_CONFIG_PATH) then
    setenv PKG_CONFIG_PATH "${PWD}/staging/lib/pkgconfig"
else
    setenv PKG_CONFIG_PATH "${PWD}/staging/lib/pkgconfig:${PKG_CONFIG_PATH}"
endif

setenv PYQTDESIGNERPATH "${PWD}/src/plugins/python"
if !($?PYTHONPATH) then
    setenv PYTHONPATH "${PWD}/src/plugins/widget"
else
    setenv PYTHONPATH "${PWD}/src/plugins/widget:${PYTHONPATH}"
endif