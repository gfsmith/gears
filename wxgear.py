import wx
from gears import Gear, InternalGear

class GearPanel(wx.Panel):
    def __init__(self, parent, gear=None, margin=10):
        self.gear = gear
        wx.Panel.__init__(self, parent, -1)
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.Bind(wx.EVT_SIZE, self.on_size)
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.margin = margin

    def on_size(self, evt):
        evt.Skip()
        self.Refresh()

    def on_paint(self, evt):
        dc = wx.AutoBufferedPaintDC(self)
        self.draw(dc)

    def save(self, dc, filename):
        # based largely on code posted to wxpython-users by Andrea Gavana 2006-11-08
        size = dc.Size

        bmp = wx.EmptyBitmap(size.width, size.height)

        memDC = wx.MemoryDC()

        memDC.SelectObject(bmp)

        memDC.Blit( 0, # Copy to this X coordinate
            0, # Copy to this Y coordinate
            size.width, # Copy this width
            size.height, # Copy this height
            dc, # From where do we copy?
            0, # What's the X offset in the original DC?
            0  # What's the Y offset in the original DC?
            )

        memDC.SelectObject(wx.NullBitmap)

        img = bmp.ConvertToImage()
        img.SaveFile(filename, wx.BITMAP_TYPE_PNG)

    def scaled_gear(self,w,h):
        gear = self.gear
        if gear:
            w,h = self.GetSize()
            cx,cy = w/2.0,h/2.0
            gear_diameter = gear.D_outside
            xscale = (w-self.margin)/gear_diameter
            yscale = (h-self.margin)/gear_diameter
            retval = []
            for x,y,z in gear.geom:
                retval.append((cx+(x*xscale), cy+(y*yscale)))
            return retval
        return None

    def draw(self, dc):
        w,h = dc.GetSize()
        # Paint the background black
        dc.SetBrush(wx.BLACK_BRUSH)
        dc.DrawRectangle(0,0,w,h)

        # Generate the scaled gear
        points = self.scaled_gear(w,h)
        cx,cy = w/2.0,h/2.0
        dc.SetPen(wx.WHITE_PEN)
        for i in range(len(points)-1):
            (x1,y1),(x2,y2) = points[i],points[i+1]
            dc.DrawLine(x1,y1,x2,y2)

    def set_gear(self, g):
        self.gear = g
        self.Refresh()

if __name__ == "__main__":
    gear = Gear(15)
    app = wx.App(False)
    frame = wx.Frame(None)
    panel = GearPanel(frame, gear)
    
    frame.SetSize((400,400))
    frame.SetTitle("WxGear Example")
    frame.Show(True)
    
    app.MainLoop()
