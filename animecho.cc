#include <stdlib.h>

#include <qapplication.h>

// include after Qt to avoid conflicts
#ifdef BACKEND_IS_X11
# include <X11/Xlib.h>
#endif

#include "common.h"
#include "first.h"

int
main ()
{
  QApplication *app;
  scr_first *first;

#if defined(BACKEND_IS_X11) && defined(BACKEND_IS_LIBVLC)
  // on XWayland, avoid picking up Wayland as LibVLC doesn't support
  setenv("QT_QPA_PLATFORM", "xcb", /* overwrite */ 1);

  // as per LibVLC documentation
  XInitThreads();
#endif

  app = create_qapplication();

  app->setApplicationName("animecho");

  first = new scr_first();
  first->show();

  app->exec();

  delete first;
  delete app;

  return 0;
}
