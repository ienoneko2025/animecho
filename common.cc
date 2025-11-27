#include <string.h>

#include <qapplication.h>

#include "common.h"

QApplication *
create_qapplication ()
{
  static int unused_0;
  static char unused_1[16];
  static char *unused_2[2];

  unused_0 = 1;
  unused_2[0] = strcpy(unused_1, "./this.program");
  unused_2[1] = nullptr;

  return new QApplication(unused_0, unused_2);
}
