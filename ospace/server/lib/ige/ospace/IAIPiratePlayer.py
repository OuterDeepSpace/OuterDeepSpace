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
import math, time

class IAIPiratePlayer(IPlayer):

    typeID = T_AIPIRPLAYER
    resignTo = T_PIRPLAYER

    def init(self, obj):
        IPlayer.init(self, obj)
        #
        obj.name = u'Pirate'
        obj.login = '*'
        #
        obj.pirateFame = 0
    
    def register(self, tran, obj):
        log.debug("Registering player", obj.oid)
        counter = 1
        while 1:
            try:
                obj.name = u'Pirate faction %d' % counter
                obj.login = '*AIP*pirate%d' % counter
                tran.gameMngr.registerPlayer(obj.login, obj, obj.oid)
                tran.db[OID_UNIVERSE].players.append(obj.oid)
                return
            except CreatePlayerException:
                counter += 1
        # grant techs and so on
        self.cmd(obj).update(tran, obj)

    def reregister(self, tran, obj):
        self.cmd(obj).register(tran, obj)

    def processINITPhase(self, tran, obj, data):
        IPlayer.processINITPhase(self, tran, obj, data)
        # TODO -- remove following lines
        obj.lastLogin = time.time()
        # delete itself if there are no fleets and planets
        if not obj.fleets and not obj.planets:
            self.cmd(obj).delete(tran, obj)
        # "AI" behavior -> construct pirate bases on system AI owns
        for planetID in obj.planets:
            planet = tran.db[planetID]
            log.debug(obj.oid, "PIRATEAI - scanning", planetID, len(planet.prodQueue), len(planet.slots), planet.plSlots, planet.plMaxSlots)
            if planet.prodQueue:
                # something is in production queue
                continue
            if planet.plSlots > len(planet.slots):
                # build PIRBASE
                log.debug(obj.oid, "PIRATEAI - building pirate base", planet.oid)
                self.cmd(planet).startConstruction(tran, planet, Rules.Tech.PIRATEBASE, 1, planet.oid, False, False, OID_NONE)
                continue
            else:
                # no room
                # try to build on another planets
                system = tran.db[planet.compOf]
                build = False
                for targetID in system.planets:
                    target = tran.db[targetID]
                    if target.owner == OID_NONE and target.plSlots > 0:
                        log.debug(obj.oid, "PIRATEAI - colonizing planet", target.oid)
                        self.cmd(planet).startConstruction(tran, planet, Rules.Tech.PIRATEBASE, 1, targetID, False, False, OID_NONE)
                        build = True
                if build:
                    continue
                # try to expand slots
                if Rules.Tech.ADDSLOT3 in self.techs and planet.plSlots < planet.plMaxSlots:
                    log.debug(obj.oid, "PIRATEAI - building surface expansion", planet.oid)
                    self.cmd(planet).startConstruction(tran, planet, Rules.Tech.ADDSLOT3, 1, planet.oid, False, False, OID_NONE)
                    continue

    def update(self, tran, obj):
        # TODO: remove in 0.5.59
        if not hasattr(self, "techs"):
            self.techs = {}
        
        obj.techLevel = 3
        # grant technologies
        obj.techs[Rules.Tech.EMCANNONTUR] = Rules.techMaxImprovement
        obj.techs[Rules.Tech.SSROCKET2] = Rules.techMaxImprovement
        obj.techs[Rules.Tech.TORPEDO] = Rules.techMaxImprovement
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

    def getDiplomacyWith(self, tran, obj, playerID):
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

    def isPactActive(self, tran, obj, partnerID, pactID):
        return 0

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
