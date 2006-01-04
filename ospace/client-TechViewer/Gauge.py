import wx

class Gauge(wx.Panel):
	"""
	borders = (left, right, top, bottom)
	"""
	def __init__(self, parent, color, width, height = 20, borders = (5, 5, 5, 5), percent = 100):
		wx.Panel.__init__(self, parent, -1)
		
		self.percent = percent
		self.borders = borders
		self.color = color
		self.height = height
		self.width = width
		
		wx.EVT_SIZE(self, self.OnSize)
		wx.EVT_PAINT(self, self.OnPaint)
	
	def OnSize(self, event):
		self.SetSize(wx.Size(self.width, self.height))
	
	def OnPaint(self, event):
		dc = wx.PaintDC(self)
		dc.BeginDrawing()
		dc.SetPen(wx.Pen(self.color, 1))
		dc.SetBrush(wx.Brush(self.color))
		size = self.GetClientSize()
		if self.percent > 0:
			dc.DrawRectangle(
				self.borders[0],
				self.borders[2],
				(size.width * self.percent / 100) - (self.borders[0] + self.borders[1]),
				size.height - (self.borders[2] + self.borders[3])
			)
		dc.EndDrawing()
