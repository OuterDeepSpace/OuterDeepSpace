import wx
from Gauge import Gauge

class DependencyPanel(wx.Panel):
	def __init__(self, parent, text, color, env, mineral, energy, nothing):
		wx.Panel.__init__(self, parent, -1)

		vertBox = wx.BoxSizer(wx.VERTICAL)
		
		gaugeWidth = 340
		gaugeHeight = 20
		gaugeBorders = (5, 0, 5, 5)
		
		minPanel = wx.Panel(self, -1)
		box = wx.BoxSizer(wx.HORIZONTAL)
		box.Add(wx.StaticText(minPanel, -1, text), 0, wx.NORTH | wx.SOUTH, 4)
		box.Fit(minPanel)
		minPanel.SetSizer(box)
		vertBox.Add(minPanel, 0, wx.EXPAND)

		minPanel = wx.Panel(self, -1)
		box = wx.BoxSizer(wx.HORIZONTAL)
		st = wx.StaticText(minPanel, -1, "Environment")
		size = st.GetSize()
		box.Add(st, 0, wx.EAST | wx.WEST, 4)
		self.env = Gauge(minPanel, color, gaugeWidth, gaugeHeight, gaugeBorders, env)
		box.Add(self.env, 1, wx.EXPAND)
		box.Fit(minPanel)
		minPanel.SetSizer(box)
		vertBox.Add(minPanel, 0, wx.EXPAND)
		
		minPanel = wx.Panel(self, -1)
		box = wx.BoxSizer(wx.HORIZONTAL)
		st = wx.StaticText(minPanel, -1, "Mineral")
		st.SetSize(size)
		box.Add(st, 0, wx.EAST | wx.WEST, 4)
		self.mineral = Gauge(minPanel, color, gaugeWidth, gaugeHeight, gaugeBorders, mineral)
		box.Add(self.mineral, 1, wx.EXPAND)
		box.Fit(minPanel)
		minPanel.SetSizer(box)
		vertBox.Add(minPanel, 0, wx.EXPAND)

		minPanel = wx.Panel(self, -1)
		box = wx.BoxSizer(wx.HORIZONTAL)
		st = wx.StaticText(minPanel, -1, "Energy")
		st.SetSize(size)
		box.Add(st, 0, wx.EAST | wx.WEST, 4)
		self.energy = Gauge(minPanel, color, gaugeWidth, gaugeHeight, gaugeBorders, energy)
		box.Add(self.energy, 1, wx.EXPAND)
		box.Fit(minPanel)
		minPanel.SetSizer(box)
		vertBox.Add(minPanel, 0, wx.EXPAND)

		minPanel = wx.Panel(self, -1)
		box = wx.BoxSizer(wx.HORIZONTAL)
		st = wx.StaticText(minPanel, -1, "Nothing")
		st.SetSize(size)
		box.Add(st, 0, wx.EAST | wx.WEST, 4)
		self.nothing = Gauge(minPanel, color, gaugeWidth, gaugeHeight, gaugeBorders, nothing)
		box.Add(self.nothing, 1, wx.EXPAND)
		box.Fit(minPanel)
		minPanel.SetSizer(box)
		vertBox.Add(minPanel, 0, wx.EXPAND)

		vertBox.Fit(self)
		self.SetSizer(vertBox)
	
	def SetEnv(self, percent):
		self.env.percent = percent
		self.Refresh()

	def SetMineral(self, percent):
		self.mineral.percent = percent
		self.Refresh()

	def SetEnergy(self, percent):
		self.energy.percent = percent
		self.Refresh()

	def SetNothing(self, percent):
		self.nothing.percent = percent
		self.Refresh()

	def Clear(self):
		self.nothing.percent = 0
		self.mineral.percent = 0
		self.env.percent = 0
		self.energy.percent = 0
		self.Refresh()

