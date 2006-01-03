#
#  Copyright 2001 - 2006 Ludek Smid [http://www.ospace.net/]
#
#  This file is part of Pygame.UI.
#
#  Pygame.UI is free software; you can redistribute it and/or modify
#  it under the terms of the Lesser GNU General Public License as published by
#  the Free Software Foundation; either version 2.1 of the License, or
#  (at your option) any later version.
#
#  Pygame.UI is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  Lesser GNU General Public License for more details.
#
#  You should have received a copy of the Lesser GNU General Public License
#  along with Pygame.UI; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#

from pygame.locals import *
from Const import *
from Window import Window
from SimpleGridLM import SimpleGridLM
from Title import Title
from ActiveLabel import ActiveLabel

class Menu(Window):

	def __init__(self, parent, **kwargs):
		Window.__init__(self, parent)
		# data
		self.__dict__["title"] = None
		self.__dict__["items"] = None
		self.__dict__["looseFocusClose"] = 1
		self.__dict__["decorated"] = 0
		self.__dict__["layoutManager"] = SimpleGridLM()
		self.__dict__["width"] = 10
		self.__dict__["_labels"] = []
		self.processKWArguments(kwargs)
		# subscribe action
		# add title
		Title(self, id = "_menuTitle")

	def show(self, pos = None):
		self._menuTitle.layout = (0, 0, self.width, 1)
		self._menuTitle.text = self.title
		if not pos:
			pos = pygame.mouse.get_pos()
		index = 0
		for item in self.items:
			if len(self._labels) <= index:
				label = ActiveLabel(self, align = ALIGN_W)
				label.subscribeAction("*", self.actionHandler)
				self._labels.append(label)
			label = self._labels[index]
			label.layout = (0, index + 1, self.width, 1)
			label.text = item.text
			if hasattr(item, "action"):
				label.action = item.action
			else:
				label.action = None
			if hasattr(item, "data"):
				label.data = item.data
			else:
				label.data = None
			index += 1
		rowSize, colSize = self.app.theme.getGridParams()
		self.rect = Rect(pos[0], pos[1], self.width * colSize, (index + 1) * rowSize)
		return Window.show(self)

	def actionHandler(self, widget, action, data):
		self.hide()
		self.processAction(action, widget.data)