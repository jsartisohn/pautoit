import gtk.gdk
# TODO: Decide if we can hide away numpy here in region or if we should expose
#       colors as raw numpy types.

root_window = gtk.gdk.get_default_root_window()

class Region:
  def __init__(self, x, y, w, h):
    self.pb = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8, w, h)
    self.x = x
    self.y = y
    self._grab()

  def color_at(self, x, y):
    return self.arr[y, x]

  def update():
    w = self.pb.get_width()
    self._grab(self.x, self.y, self.pb.get_width(), self.pb.get_height())

  def _grab(self):
    self.pb = self.pb.get_from_drawable(root_window, root_window.get_colormap(),
                                        self.x, self.y, 0, 0,
                                        self.pb.get_width(),
                                        self.pb.get_height())
    self.arr = self.pb.get_pixels_array()

