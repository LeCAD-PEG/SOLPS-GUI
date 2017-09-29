#include "gnuplotWidget.h"
#include "QtGnuplotWidget.h"
#include <QtCore>
#include <QtGui>
#include <QtWidgets>
#include <QWidget>

gnuplotWidget::gnuplotWidget(QWidget *parent = 0)
    : QWidget(parent)
{
    QGridLayout* gridLayout = new QGridLayout();
    widget = new QtGnuplotWidget();
    //widget->setFixedSize(400, 250);
    gp.setWidget(widget);
    connect(&gp, SIGNAL(gnuplotOutput(const QString&)), this, SLOT(_output_delegate(const QString&)));

    gridLayout->addWidget(widget, 0, 0);

    QVBoxLayout* layout = new QVBoxLayout(this);
    layout->addLayout(gridLayout);
    setLayout(layout);
}

void gnuplotWidget::cmd(const QString command)
{
    gp << command + '\n';
}

void gnuplotWidget::_output_delegate(const QString output)
{
    emit this->gnuplotOutput(output);
}