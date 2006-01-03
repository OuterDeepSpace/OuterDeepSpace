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

import gdata, client
import glob, math
import pygame, pygame.image
from ige.ospace.Const import *

whiteShift = 80000
redShift = 90000

smallStarImgs = None
techImgs = None
bigStarImgs = None
planetImgs = None
cmdInProgressImg = None
loginLogoImg = None
structProblemImg = None
structOffImg = None
icons = {}

def initialize():
	# needed for progress dlg
	global loginLogoImg
	loginLogoImg = pygame.image.load('res/logo-login.png').convert_alpha()

def loadResources():
	import dialog
	dlg = dialog.ProgressDlg(gdata.app)
	curr = 0
	max = len(glob.glob('res/galaxy/*.png')) + len(glob.glob('res/techs/*.png')) + \
		len(glob.glob('res/system/*.png')) + len(glob.glob('res/icons/*.png'))
	dlg.display(_('Loading resources'), 0, max)
	# load star imgs
	global smallStarImgs
	smallStarImgs = {}
	for filename in glob.glob('res/galaxy/star_*.png'):
		curr += 1
		if curr % 10 == 0:
			dlg.setProgress(_('Loading resources...'), curr)
		name = filename[16:-4]
		smallStarImgs[name] = pygame.image.load(filename).convert_alpha()
	# load tech imgs
	global techImgs
	techImgs = {}
	white = pygame.Surface((37,37))
	white.fill((255, 255, 255))
	white.set_alpha(64)
	red = pygame.Surface((37,37))
	red.fill((255, 0, 0))
	red.set_alpha(64)
	for filename in glob.glob('res/techs/????.png'):
		curr += 1
		if curr % 10 == 0:
			dlg.setProgress(_('Loading resources...'), curr)
		name = filename[10:14]
		imgID = int(name)
		techImgs[imgID] = pygame.image.load(filename).convert_alpha()
		copyImg = techImgs[imgID].convert_alpha()
		copyImg.blit(white, (0,0))
		techImgs[imgID + whiteShift] = copyImg
		copyImg = techImgs[imgID].convert_alpha()
		copyImg.blit(red, (0,0))
		techImgs[imgID + redShift] = copyImg
	# load big star imgs
	global bigStarImgs
	bigStarImgs = {}
	for filename in glob.glob('res/system/star_*.png'):
		curr += 1
		if curr % 10 == 0:
			dlg.setProgress(_('Loading resources...'), curr)
		name = filename[16:-4]
		bigStarImgs[name] = pygame.image.load(filename).convert_alpha()
	# load planet images
	global planetImgs
	planetImgs = {}
	for filename in glob.glob('res/system/planet_*.png'):
		curr += 1
		if curr % 10 == 0:
			dlg.setProgress(_('Loading resources...'), curr)
		name = filename[18:-4]
		planetImgs[name] = pygame.image.load(filename).convert_alpha()
	# load ship imgs
	global shipImgs
	shipImgs = {}
	for filename in glob.glob('res/ships/??.png'):
		curr += 1
		if curr % 10 == 0:
			dlg.setProgress(_('Loading resources...'), curr)
		name = filename[10:-4]
		shipImgs[int(name)] = pygame.image.load(filename).convert_alpha()
	# load star imgs
	global icons
	icons = {}
	for filename in glob.glob('res/icons/*.png'):
		curr += 1
		if curr % 10 == 0:
			dlg.setProgress(_('Loading resources...'), curr)
		name = filename[10:-4]
		icons[name] = pygame.image.load(filename).convert_alpha()
	# other icons
	global cmdInProgressImg
	cmdInProgressImg = pygame.image.load('res/cmdInProgress.png').convert_alpha()
	global structProblemImg
	structProblemImg = pygame.image.load('res/struct_problem.png').convert_alpha()
	global structOffImg
	structOffImg = pygame.image.load('res/struct_off.png').convert_alpha()
	dlg.hide()

def getTechImg(techID):
	return techImgs.get(techID, techImgs[0])

def getShipImg(combatClass, isMilitary):
	return shipImgs.get(int(combatClass) * 10 + int(isMilitary), shipImgs[99])

def getSmallStarImg(name):
	return smallStarImgs[name]

def getBigStarImg(name):
	return bigStarImgs[name]

def getPlanetImg(name):
	return planetImgs[name]

def getUnknownName():
	return _('[Unknown]')

def getNA():
	return _('N/A')

def OLDgetFFColorCode(relationship):
	if relationship < 0:
		return (0xff, 0x00, 0xff)
	elif relationship < 500 and relationship >= 0:
		rel = relationship / 500.0
		r = 0xff
		g = int(0xff * rel)
		b = 0x00
		return (r, g, b)
	elif relationship >= 500 and relationship <= 1000:
		rel = (relationship - 500) / 500.0
		#r = int(0xff * (1 - rel))
		#g = 0xff
		#b = int(0xff * rel)
		r = 0xff
		g = 0xff
		b = int(0xff * rel)
		return (r, g, b)
	elif relationship == 1250:
		return (0x00, 0xff, 0x00)
	else:
		return (0xc0, 0xc0, 0xc0)

def getFFColorCode(relationship):
	if relationship < 0:
		return (0xff, 0x00, 0xff)
	elif relationship < REL_UNFRIENDLY_LO:
		return (0xff, 0x80, 0x80)
	elif relationship < REL_NEUTRAL_LO:
		return (0xff, 0x90, 0x01)
	elif relationship < REL_FRIENDLY_LO:
		return (0xff, 0xff, 0x00)
	elif relationship < REL_ALLY_LO:
		return (0xb0, 0xb0, 0xff)
	elif relationship <= REL_ALLY_HI:
		return (0x80, 0xff, 0xff)
	elif relationship == 1250:
		return (0x00, 0xff, 0x00)
	else:
		return (0xc0, 0xc0, 0xc0)

def getPlayerColor(owner):
	if owner == OID_NONE:
		return getFFColorCode(REL_UNDEF)
	if gdata.config.defaults.highlights == 'yes':
		if gdata.playersHighlightColors.has_key(owner):
			return gdata.playersHighlightColors[owner]
	rel = min(REL_UNDEF,client.getRelationTo(owner))
	return getFFColorCode(rel)


def formatTime(time):
	time = int(math.ceil(time))
	sign = ''
	if time < 0:
		time = - time
		sign = '-'
	days = time / 24
	hours = time % 24
	return '%s%d:%02d' % (sign, days, hours)

def formatBE(b, e):
	return '%d / %d' % (b, e)
