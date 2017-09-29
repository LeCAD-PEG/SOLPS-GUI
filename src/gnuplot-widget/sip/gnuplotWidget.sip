%Module pyQtGnuplot

%Import QtGui/QtGuimod.sip
%Import QtCore/QtCoremod.sip
%Import QtWidgets/QtWidgetsmod.sip

class gnuplotWidget : public QWidget{
%TypeHeaderCode
#include "gnuplotWidget.h"
%End

public:
    gnuplotWidget(QWidget *parent /TransferThis/ = 0);

public slots:
    void cmd(const QString command);

signals:
    void output(const QString output);
};
