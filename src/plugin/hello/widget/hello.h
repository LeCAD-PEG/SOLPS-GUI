// Define the interface to the hello library.
#include <QLabel>
#include <QWidget>
#include <QString>

class Hello : public QLabel {
    // This is needed by the Qt Meta-Object Compiler.
    Q_OBJECT

public:
    Hello(QWidget *parent = 0);

private:
    // Prevent instances from being copied.
    Hello(const Hello &);
    Hello &operator=(const Hello &);
};
#if !defined(Q_OS_WIN)
void setDefault(const QString &def);
#endif
