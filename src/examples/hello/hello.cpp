#include "hello.h"
#include "stdio.h"

Hello::Hello(QWidget *parent):QLabel(parent)
{
    printf("Hello, SOLPS\n");
}

Hello::Hello(const Hello &)
{

}

Hello &Hello::operator=(const Hello &)
{
    return *this;
}
