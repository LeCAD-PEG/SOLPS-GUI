
#define gnuplotWidget_VERSION_STR "1.0"

#include "QtGnuplotInstance.h"

#include <QtCore>
#include <QtGui>
#include <QtWidgets>
#include <QWidget>

class gnuplotWidget;

class gnuplotWidget : public QWidget
{
Q_OBJECT

public:
    gnuplotWidget(QWidget *parent = 0);

public slots:
    void cmd(const QString command);
    void _output_delegate(const QString output);

signals:
    void gnuplotOutput(const QString output);

private:
    QtGnuplotInstance gp;
    QtGnuplotWidget* widget;

};