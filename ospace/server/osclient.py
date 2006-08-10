#!/usr/bin/env python2.2
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

# tweak PYTHONPATH
import sys, string
import os
sys.path.insert(0, 'lib')

from igeclient.IClient import IClient
import pprint, traceback
from getpass import getpass
from code import InteractiveConsole
from ige.ospace import Rules

levelTechs = {1: [
1000,
1100,
1101,
1102,
1104,
1106,
1107,
1110,
1112,
1400,
1401,
1402,
1403,
1404,
1500,
1510,
1511,
1800,
1801,
1802,
1803,
],
2: [
1105,
1111,
2001,
2006,
2400,
2401,
2403,
2404,
2405,
2406,
2407,
2408,
2409,
2800,
2801,
2802,
2803,
],
3: [
3000,
3010,
3013,
3401,
3402,
3403,
3404,
3405,
3406,
3407,
3409,
3410,
3450,
3451,
3800,
3802,
],
4: [
4000,
4004,
4005,
],
5: [
5000,
5001,
5002,
5800,
5801,
5802,
5803,
]}

levelTechsRaces = {
1: {'B': [], 'H': [], 'C': []},
2: {'B': [2003, 2005, 2007, 2804, 2805], 'H': [2000, 2004], 'C': [2002, 2004]},
3: {
'B': [3001, 3003, 3007, 3008, 3412, 3452, 3454, 3803, ],
'H': [3002, 3004, 3006, 3009, 3408, 3411, 3453, 3455, 3803, ],
'C': [3001, 3005, 3006, 3411, 3453, 3456, ]},
4: {
'B': [4003, 4400, 4401, 4402, 4403, 4404, 4405, 4406, 4458, 4460, 4476, ],
'H': [4002, 4407, 4408, 4409, 4410, 4411, 4412, 4413, 4459, 4461, 4477, 4479, 4480, ],
'C': [4001, 4414, 4415, 4416, 4417, 4418, 4419, 4420, 4459, 4462, 4477, 4479, ]},
5: {
'B': [5400, 5401, 5402, 5403, 5404, 5405, 5406, 5431, 5433, 5465, 5467, 5470, 5805, ],
'H': [5003, 5004, 5005, 5408, 5409, 5410, 5411, 5412, 5413, 5414, 5430, 5466, 5468, 5471, 5474, 5804, ],
'C': [5006, 5416, 5417, 5418, 5419, 5420, 5421, 5432, 5466, 5469, 5472, 5473, ]}
}

advTechLevel = {
1: {},
2: {"B" : 1990, "H" : 1991, "C" : 1992},
3: {"B" : 2990, "H" : 2991, "C" : 2992},
4: {"B" : 3990, "H" : 3991, "C" : 3992},
5: {"B" : 4990, "H" : 4991, "C" : 4992},
}

def msgHandler(id, data):
	if id >= 0:
		print 'Message', id, data

def getPlayer(name):
    u = s.getInfo(1)
    for playerID in u.players:
        pl = s.getInfo(playerID)
        if pl.name == name:
            return pl
    return None

def showPlayers():
	un = s.getInfo(1)
	players = []
	for playerID in un.players:
		player = s.getInfo(playerID)
		players.append((playerID, player.name))

	print
	print
	print "List of current players:"
	for pl in players:
		print "%5d: %s" % pl

	print
	print "Press Enter to continue"
	raw_input()

def showGalaxies():
	un = s.getInfo(1)
	galaxies = []
	for galaxyID in un.galaxies:
		galaxy = s.getInfo(galaxyID)
		galaxies.append((galaxyID, galaxy.name))

	print
	print
	print "List of current galaxies:"
	for gal in galaxies:
		print "%5d: %s" % gal

	print

def setCurrentObject():
	objId = raw_input("oid: ")
	newObjID = 0
	try:
		newObjID = int(objId)
	except:
		print "Invalid object"

	return newObjID

def giveTechs(objID):
	lvl = raw_input("level: ")
	level = 0
	try:
		level = int(lvl)
	except:
		print "Invalid level"
		return objId

	player = s.getInfo(objID)
	plTechs = player.techs
	for techId in levelTechs[level]:
		plTechs[techId] = 5

	if len(player.race) > 0:
		print "setting race dependent techs"
		for techId in levelTechsRaces[level][player.race]:
			plTechs[techId] = 5

	s.set(objID, "techs", plTechs)
	print "Techs at level %d added to player %d." % (level, objID)
	return objID

def giveTech(objID):
	tid = raw_input("techId: ")
	try:
		techId = int(tid)
	except:
		print "Invalid techId"
		return objId

	player = s.getInfo(objID)
	plTechs = player.techs
	plTechs[techId] = 5

	s.set(objID, "techs", plTechs)
	print "Tech %d added to player %d." % (techId, objID)
	return objID

def advanceLevel(objID):
	lvl = raw_input("level: ")
	try:
		level = int(lvl)
	except:
		print "Invalid level"
		return objId

	race = string.upper(raw_input("race: "))
	player = s.getInfo(objID)
	plTechs = player.techs
	plTechs[advTechLevel[level][race]] = 5

	s.set(objID, "techs", plTechs)
	s.set(objID, "techLevel", level)
	s.set(objID, "race", race)
	print "Tech %d added, techLevel advance to %d to player %d." % (advTechLevel[level][race], level, objID)
	return objID

def promoteToImperator(objID):
	galID = raw_input("galaxy id: ")
	try:
		galaxyID = int(galID)
	except:
		print "Invalid galaxy id"
		return objId

	s.set(objID, "imperator", 3)
	s.set(galaxyID, "imperator", objID)
	print "Galaxy %d has now imperator %d." % (galaxyID, objID)
	return objID

def giveStratRes(objID):
	resID = raw_input("strategy resource: ")
	try:
		stratResID = int(resID)
	except:
		print "Invalid strategy resource"
		return objId

	qty = raw_input("qty: ")
	try:
		quantity = int(qty)
	except:
		print "Invalid quantity"
		return objId

	plQty = 0
	player = s.getInfo(objID)
	if stratResID in player.stratRes:
		plQty = player.stratRes[stratResID]

	stratRes = player.stratRes
	stratRes[stratResID] = plQty + quantity
	s.set(objID, "stratRes", stratRes)
	print "Player %d has now %d pieces of %d." % (objID, stratRes[stratResID], stratResID)
	return objID

def showMenu(objID):
	print
	print "----- OSPace admin console menu -----"
	print "Current object: %s" % objID
	print
	print "1. Show players"
	print "2. Set current object"
	print "3. Give techs"
	print "4. Give particular tech"
	print "5. Advance to level"
	print "6. Show Galaxies"
	print "7. Promote current object to imperator"
	print "8. Give current object Strategic Resource"
	print "9. Finish production queue"
	print "C. Interactive console"
	print "T. Process turn"
	print "R. Process X turns"
	print
	print "Ctrl+Z to End"
	print

def processTurns():
	numT = raw_input("Number of turns: ")
	try:
		num = int(numT)
	except:
		print "invalid number of turns"

	for i in range(1, num + 1):
		s.processTurn()

def finishProdQueue(objId):
	p = s.get(objId)
	for i in p.prodQueue:
		i.currProd = 38400
	s.set(p.oid, "prodQueue", p.prodQueue)

def processMenu(inp, objId, s):
	if inp == "1":
		showPlayers()
	elif inp == "2":
		return setCurrentObject()
	elif inp == "3":
		giveTechs(objId)
	elif inp == "4":
		giveTech(objId)
	elif inp == "5":
		advanceLevel(objId)
	elif inp == "6":
		showGalaxies()
	elif inp == "7":
		promoteToImperator(objId)
	elif inp == "8":
		giveStratRes(objId)
	elif inp == "9":
		finishProdQueue(objId)
	elif string.upper(inp) == "R":
		processTurns()
	elif string.upper(inp) == "T":
		s.processTurn()
	elif string.upper(inp) == "C":
		console = InteractiveConsole(locals())
		console.interact()

	return objId

#s = IClient('ospace.net:9080', None, msgHandler, None, 'IClient/osc')
s = IClient('localhost:9080', None, msgHandler, None, 'IClient/osc')

if len(sys.argv) != 2:
	print "Usage: osclient LOGIN"
	sys.exit(1)

login = sys.argv[1]

if login == "admin":
	# get admin login from var/token
	password = open(os.path.join("var", "token"), "r").read()
else:
	password = getpass("Password: ")

s.connect(login)
s.login('Alpha', login, password)

try:
	objID = 0
	while True:
		showMenu(objID)
		objID = processMenu(raw_input(), objID, s)
except EOFError:
	pass

s.logout()
