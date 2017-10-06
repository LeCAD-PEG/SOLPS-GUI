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
    gridLayout->setSpacing(0);
    gridLayout->setMargin(0);
    widget = new QtGnuplotWidget();
    //widget->setFixedSize(400, 250);
    gp.setWidget(widget);
    connect(&gp, SIGNAL(gnuplotOutput(const QString&)), this, SLOT(_output_delegate(const QString&)));

    connect(widget, SIGNAL(plotDone()), this, SLOT(_plotDone()));

    gridLayout->addWidget(widget, 0, 0);

    QVBoxLayout* layout = new QVBoxLayout(this);
    layout->setSpacing(0);
    layout->setMargin(0);
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

void gnuplotWidget::_plotDone()
{
    emit this->plotDone();
}