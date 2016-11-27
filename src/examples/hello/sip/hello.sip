// Define the SIP wrapper to the hello library.

%Module hello

%Import QtGui/QtGuimod.sip
%Import QtWidgets/QtWidgetsmod.sip

class Hello : public QLabel {

%TypeHeaderCode
#include <hello.h>
%End

public:
    Hello(QWidget *parent /TransferThis/ = 0);

private:
    Hello(const Hello &);
};
