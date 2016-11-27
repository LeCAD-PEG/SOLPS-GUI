// Define the interface to the hello library.
#include <QtWidgets/QLabel>
#include <QtWidgets/QWidget>

#define HELLO_VERSION_STR "3.5"

class Hello : public QLabel {

 public:
    Hello(QWidget *parent = 0);

private:
    // Prevent instances from being copied.
    Q_DISABLE_COPY(Hello)
};
