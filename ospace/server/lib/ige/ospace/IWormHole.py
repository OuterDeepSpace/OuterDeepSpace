#
#  Copyright 2001 - 2006 Ludek Smid [http://www.ospace.net/]
#
#  This file is part of IGE - Outer Space.
#
#  IGE - Outer Space is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  IGE - Outer Space is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with IGE - Outer Space; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#

from ige import *
from xml.dom.minidom import Node
from ISystem import ISystem
from Const import *

class IWormHole(ISystem):

    typeID = T_WORMHOLE

    def init(self, obj):
        ISystem.init(self, obj)
        #
        obj.destinationOid = OID_NONE
        obj.destination = u'---'
        obj.starClass = u'wW0'

    def loadDOMNode(self, tran, obj, xoff, yoff, node):
        obj.x = float(node.getAttribute('x')) + xoff
        obj.y = float(node.getAttribute('y')) + yoff
        for elem in node.childNodes:
            if elem.nodeType == Node.ELEMENT_NODE:
                name = elem.tagName
                if name == 'properties':
                    self.loadDOMAttrs(obj, elem)
                else:
                    raise GameException('Unknown element %s' % name)
        return SUCC
