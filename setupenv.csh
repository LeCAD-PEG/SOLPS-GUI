# source this csh file for local setup environment if PyQT is provided locally
setenv QTDIR "${PWD}/staging/qt/5.9.1"
setenv PARAVIEW_PREFIX ${PWD}/staging/paraview/5.4.1

setenv PATH "${PWD}/staging/bin:${QTDIR}/bin:${PARAVIEW_PREFIX}/bin:${PATH}"
setenv SOLPSGUI "${PWD}/src/gui"

if !($?LD_LIBRARY_PATH) then
    setenv LD_LIBRARY_PATH "${PWD}/staging/lib:${QTDIR}/lib"
else
    setenv LD_LIBRARY_PATH "${PWD}/staging/lib:${QTDIR}/lib:${LD_LIBRARY_PATH}"
    setenv LD_LIBRARY_PATH "${PWD}/staging/qt/5.9.1/lib:${LD_LIBRARY_PATH}"
endif

if !($?PKG_CONFIG_PATH) then
    setenv PKG_CONFIG_PATH "${PWD}/staging/lib/pkgconfig"
else
    setenv PKG_CONFIG_PATH "${PWD}/staging/lib/pkgconfig:${PKG_CONFIG_PATH}"
endif

setenv PYQTDESIGNERPATH "${PWD}/src/plugins/designer"
if !($?PYTHONPATH) then
    setenv PYTHONPATH "${PWD}/src/widgets"
    setenv PYTHONPATH "${PWD}/staging/lib/site-packages:${PYTHONPATH}"
else
    setenv PYTHONPATH "${PWD}/src/widgets:${PYTHONPATH}"
    setenv PYTHONPATH "${PWD}/staging/lib/site-packages:${PYTHONPATH}"
endif


alias solps "${PWD}/staging/bin/python3 ${PWD}/src/gui/solps.py"
alias solps_doc xdg-open "${PWD}/doc/build/html/index.html"
alias solps_help assistant -collectionFile "${PWD}/doc/build/qthelp/SOLPSGUI.qhc"
alias eirene "python3 ${PWD}/src/widgets/eirene.py"
alias b2 "python3 ${PWD}/src/widgets/b2.py"
