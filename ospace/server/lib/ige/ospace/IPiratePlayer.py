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
from IPlayer import IPlayer
from ige.IDataHolder import IDataHolder
import Rules, Utils
from Const import *
import log, math, time, sys, random

class IPiratePlayer(IPlayer):

	typeID = T_PIRPLAYER
	resignTo = T_AIPIRPLAYER

	def init(self, obj):
		IPlayer.init(self, obj)
		obj.pirateFame = 0

	def XXXgetDiplomacyWith(self, tran, obj, playerID):
		if obj.oid == playerID:
			return REL_UNITY
		# this AI battles with overyone
		# make default
		dipl = IDataHolder()
		dipl.type = T_DIPLREL
		dipl.pacts = {}
		dipl.relation = REL_ENEMY
		dipl.relChng = 0
		dipl.lastContact = tran.db[OID_UNIVERSE].turn
		dipl.contactType = CONTACT_NONE
		dipl.stats = None
		return dipl

	def XXXisPactActive(self, tran, obj, partnerID, pactID):
		return 0

	def update(self, tran, obj):
		# call super method
		IPlayer.update(self, tran, obj)
		#
		obj.techLevel = 99
		# grant special technologies
		obj.techs[Rules.Tech.PIRATEBASE] = Rules.techMaxImprovement
		obj.techs[Rules.Tech.PIRATEDEN] = Rules.techMaxImprovement
		obj.techs[Rules.Tech.PIRATESD] = Rules.techMaxImprovement
		obj.techs[Rules.Tech.PIRATEFTLENG] = Rules.techMaxImprovement
		obj.techs[Rules.Tech.PIRCOLONYMOD] = Rules.techMaxImprovement
		# TODO: enable?
		#@obj.techs[Rules.Tech.PIRGOVERNMENT] = Rules.techMaxImprovement
		# grant all TL1 ship techs except for colony module(s)
		for techID in Rules.techs:
			tech = Rules.techs[techID]
			if tech.level == 1 and (tech.isShipEquip or tech.isShipHull) and not tech.unpackStruct:
				obj.techs[techID] = Rules.techMaxImprovement
		# convert enslavedPop
		if hasattr(obj, "enslavedPop"):
			obj.pirateFame = int(obj.enslavedPop * 0.0005)
			log.debug(obj.oid, "New pirate fame is", obj.pirateFame, obj.enslavedPop)
			del obj.enslavedPop

	def processFINALPhase(self, tran, obj, data):
		obj.govPwr = Rules.pirateGovPwr
		IPlayer.processFINALPhase(self, tran, obj, data)
		# get fame every 1:00 turns
		if tran.db[OID_UNIVERSE].turn % Rules.turnsPerDay == 0:
			Utils.sendMessage(tran, obj, MSG_GAINED_FAME, obj.oid, Rules.pirateSurvivalFame)
			obj.pirateFame += Rules.pirateSurvivalFame
		# fix goverment power
		obj.govPwrCtrlRange = 10000
		# bonus for gained fame
		obj.prodEff += obj.pirateFame / 100.0

	processFINALPhase.public = 1
	processFINALPhase.accLevel = AL_ADMIN

	def processRSRCHPhase(self, tran, obj, data):
		# do not research anything
		return

	processRSRCHPhase.public = 1
	processRSRCHPhase.accLevel = AL_ADMIN

	def capturePlanet(self, tran, obj, planet):
		# find distance to closes pirate's planet
		dist = sys.maxint
		for objID in obj.planets:
			pirPl = tran.db[objID]
			d = math.hypot(planet.x - pirPl.x, planet.y - pirPl.y)
			if d < dist:
				dist = d
		if random.random() <= Rules.pirateGainFamePropability(dist):
			log.debug(obj.oid, "Pirate captured planet + fame", dist, planet.oid)
			obj.pirateFame += Rules.pirateCaptureInRangeFame
			Utils.sendMessage(tran, obj, MSG_GAINED_FAME, planet.oid, Rules.pirateCaptureInRangeFame)
		elif random.random() <= Rules.pirateLoseFameProbability(dist):
			log.debug(obj.oid, "Pirate captured planet OUT OF range", dist, planet.oid)
			obj.pirateFame += Rules.pirateCaptureOutOfRangeFame
			Utils.sendMessage(tran, obj, MSG_LOST_FAME, planet.oid, Rules.pirateCaptureOutOfRangeFame)

	def stealTechs(self, tran, obj, playerID):
		if playerID == OID_NONE:
			return
		log.debug(obj.oid, "IPiratePlayer stealing techs")
		player = tran.db[playerID]
		canSteal = Rules.pirateCanStealImprovements
		for techID in player.techs:
			tech = Rules.techs[techID]
			if player.techs[techID] <= obj.techs.get(techID, 0):
				# skip techs that are already stealed
				continue
			if (tech.isShipEquip or tech.isShipHull) and not tech.unpackStruct:
				obj.techs[techID] = min(obj.techs.get(techID, 0) + 1, player.techs[techID])
				canSteal -= 1
				if canSteal == 0:
					break
				# TODO message to (both?) players
			if (tech.isProject):
				obj.techs[techID] = min(obj.techs.get(techID, 0) + 1, player.techs[techID])
				break
		# update techs
		self.cmd(obj).update(tran, obj)
		return
