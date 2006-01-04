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

import Rules
from ige import GameException
from ige.IDataHolder import IDataHolder
from Const import *
import log, random


def makeShipMinSpec(player, name, hullID, eqIDs, improvements,
	raiseExs = True):
	ship = makeShipFullSpec(player, name, hullID, eqIDs, improvements, raiseExs)
	# make 'real' ship spec
	spec = IDataHolder()
	spec.type = T_SHIP
	spec.name = ship.name
	spec.hullID = ship.hullID
	spec.level = ship.level
	spec.eqIDs = ship.eqIDs
	spec.improvements = ship.improvements
	spec.combatClass = ship.combatClass
	spec.signature = ship.signature
	spec.scannerPwr = ship.scannerPwr
	spec.speed = ship.speed
	spec.maxHP = ship.maxHP
	spec.shieldHP = ship.shieldHP
	spec.combatAtt = ship.combatAtt
	spec.combatDef = ship.combatDef
	spec.missileDef = ship.missileDef
	spec.storEn = ship.storEn
	spec.operEn = ship.operEn
	spec.buildProd = ship.buildProd
	spec.buildSRes = ship.buildSRes
	spec.weaponIDs = ship.weaponIDs
	spec.deployStructs = ship.deployStructs
	spec.built = 0
	spec.buildTurns = 1
	spec.upgradeTo = 0
	spec.isMilitary = ship.isMilitary
	spec.baseExp = ship.baseExp
	spec.combatPwr = ship.combatPwr
	spec.autoRepairFix = ship.autoRepairFix
	spec.autoRepairPerc = ship.autoRepairPerc
	spec.shieldRechargeFix = ship.shieldRechargeFix
	spec.shieldRechargePerc = ship.shieldRechargePerc
	return spec

def makeShipFullSpec(player, name, hullID, eqIDs, improvements, raiseExs = True):
	if not hullID:
		raise GameException("Ship's hull must be specified.")
	hull = Rules.techs[hullID]
	if not hull.isShipHull:
		raise GameException("Ship's hull must be specified.")
	ship = IDataHolder()
	ship.type = T_SHIP
	# initial values
	techEff = Rules.techImprEff[player.techs.get(hullID, Rules.techBaseImprovement)]
	ship.name = name
	ship.hullID = hullID
	ship.eqIDs = eqIDs
	ship.level = hull.level
	ship.combatClass = hull.combatClass
	ship.improvements = improvements
	ship.buildProd = hull.buildProd
	ship.buildSRes = hull.buildSRes[:] # we need copy
	ship.operEn = hull.operEn
	ship.storEn = hull.storEn * techEff
	ship.weight = hull.weight
	ship.signature = hull.signature
	ship.minSignature = hull.minSignature
	ship.combatAtt = hull.combatAtt * techEff
	ship.combatDef = hull.combatDef * techEff
	ship.missileDef = hull.missileDef * techEff
	ship.scannerPwr = max(hull.scannerPwr * techEff, Rules.scannerMinPwr)
	ship.autoRepairFix = hull.autoRepairFix
	ship.autoRepairPerc = hull.autoRepairPerc
	ship.shieldRechargeFix = hull.shieldRechargeFix
	ship.shieldRechargePerc = hull.shieldRechargePerc
	ship.engPwr = 0
	ship.slots = 0
	ship.upgradeTo = 0
	ship.shieldHP = 0
	ship.maxHP = int(hull.maxHP * techEff)
	ship.weaponIDs = []
	ship.deployStructs = []
	ship.isMilitary = 0
	ship.baseExp = 0
	shieldPerc = 0.0
	# add equipment
	counter = {}
	installations = {}
	for techID in eqIDs:
		tech = Rules.techs[techID]
		techEff = Rules.techImprEff[player.techs.get(techID, Rules.techBaseImprovement)]
		for i in xrange(0, eqIDs[techID]):
			counter[tech.subtype] = 1 + counter.get(tech.subtype, 0)
			installations[techID] = 1 + installations.get(techID, 0)
			# check min hull req
			if tech.minHull > ship.combatClass and raiseExs:
				log.warning("Cannot add tech", techID, tech.name)
				raise GameException("Minimum hull requirement not satisfied.")
			# check maximum installations
			if tech.maxInstallations and installations[tech.id] > tech.maxInstallations \
				and raiseExs:
				raise GameException("Maximum number of equipment installations exceeded.")
			# add values
			ship.level = max(ship.level, tech.level)
			ship.buildProd += tech.buildProd
			ship.buildSRes.extend(tech.buildSRes)
			ship.storEn += tech.storEn * techEff
			ship.weight += tech.weight
			ship.signature += tech.signature
			ship.minSignature = max(ship.minSignature, tech.minSignature)
			ship.combatDef += tech.combatDef * techEff
			ship.missileDef += tech.missileDef * techEff
			ship.slots += tech.slots
			ship.engPwr += tech.engPwr * techEff
			ship.maxHP += tech.maxHP * techEff
			shieldPerc += tech.shieldPerc * techEff
			ship.scannerPwr = max(ship.scannerPwr, tech.scannerPwr * techEff)
			ship.combatAtt += tech.combatAtt * techEff
			ship.operEn += tech.operEn
			ship.autoRepairFix = max(ship.autoRepairFix, tech.autoRepairFix * techEff)
			ship.autoRepairPerc = max(ship.autoRepairPerc, tech.autoRepairPerc * techEff)
			ship.shieldRechargeFix = max(ship.shieldRechargeFix, tech.shieldRechargeFix * techEff)
			ship.shieldRechargePerc = max(ship.shieldRechargePerc, tech.shieldRechargePerc * techEff)
			# if weapon - register only
			if tech.subtype == "seq_wpn":
				ship.weaponIDs.append(techID)
				ship.isMilitary = 1
				weapon = Rules.techs[techID]
				ship.baseExp += (weapon.weaponDmgMin + weapon.weaponDmgMax) / 2 * weapon.weaponROF
			if tech.unpackStruct != OID_NONE:
				ship.deployStructs.append(tech.unpackStruct)
	# check various conditions
	if counter.get("seq_ctrl", 0) == 0 and raiseExs:
		raise GameException("No control module in the ship.")
	if counter.get("seq_ctrl", 0) > 1 and raiseExs:
		raise GameException("Only one control module in the ship allowed.")
	if ship.slots > hull.slots and raiseExs:
		raise GameException("Hull does not have so many slots to hold all equipment.")
	if ship.weight > hull.maxWeight and raiseExs:
		raise GameException("Ship is too heavy.")
	# compute secondary paramaters
	ship.speed = float(ship.engPwr) / ship.weight
	ship.baseExp = int(ship.baseExp * Rules.shipBaseExpMod) + Rules.shipBaseExp[ship.combatClass]
	# compute base attack/defence
	ship.combatAtt += int(ship.speed)
	ship.combatDef += int(ship.speed)
	ship.missileDef += int(ship.speed / 2.0)
	# improvements
	if len(improvements) > Rules.shipMaxImprovements and raiseExs:
		raise GameException("Too many improvements.")
	for i in improvements:
		if i == SI_SPEED:
			ship.speed *= Rules.shipImprovementMod
		elif i == SI_TANKS:
			ship.storEn *= Rules.shipImprovementMod
		elif i == SI_ATT:
			ship.combatAtt *= Rules.shipImprovementMod
		elif i == SI_DEF:
			ship.combatDef *= Rules.shipImprovementMod
			ship.missileDef *= Rules.shipImprovementMod
		elif i == SI_HP:
			ship.maxHP *= Rules.shipImprovementMod
		elif i == SI_SHIELDS:
			ship.shieldHP *= Rules.shipImprovementMod
	# round values down
	ship.storEn = int(ship.storEn)
	ship.combatAtt = int(ship.combatAtt / (ship.combatClass + 1.0))
	ship.combatDef = int(ship.combatDef / (ship.combatClass + 1.0))
	ship.missileDef = int(ship.missileDef / (ship.combatClass + 1.0))
	ship.maxHP = int(ship.maxHP)
	ship.shieldHP = int(ship.maxHP * shieldPerc)
	ship.scannerPwr = int(ship.scannerPwr)
	ship.engPwr = int(ship.engPwr)
	ship.signature = int(ship.signature)
	ship.baseExp = int(ship.baseExp)
	# compute attack power
	attackPwr = 0.0
	refDefence = 10.0
	refAttack = 10.0
	refDmg = 10.0
	for weaponID in ship.weaponIDs:
		weapon = Rules.techs[weaponID]
		dmg = (weapon.weaponDmgMin + weapon.weaponDmgMax) / 2 * weapon.weaponROF
		att = ship.combatAtt + weapon.weaponAtt
		attackPwr += (att / float(att + refDefence) * dmg)
	# defence
	ship.combatPwr = int(attackPwr * (ship.maxHP + ship.shieldHP) / (refAttack / (refAttack + ship.combatDef) * refDmg))
	# fix signature
	ship.signature = max(1, ship.signature, ship.minSignature)
	#
	return ship

# ROF tables
rofTable = {}
for i in xrange(0, 100):
	line = []
	level = i
	for j in xrange(0, 100):
		if level >= 100:
			line.append(1)
			level -= 100
		else:
			line.append(0)
		level += i
	# check
	sum = 0
	for e in line:
		sum += e
	#@log.debug("ROF %02d %2.2f" % (i, sum / 10.0), line)
	assert i == sum, "Bad ROF table sum for %d" % i
	rofTable[i] = line

def getRounds(rof, counter):
	rof = int(rof * 100)
	return rof / 100 + rofTable[rof % 100][counter % 100]

# damage
def computeDamage(wpnCls, trgtCls, dmgMin, dmgMax):
	"""Compute damage that causes weapon to the target with specified combat
	   class."""
	assert trgtCls >= wpnCls
	dmg = random.uniform(dmgMin, dmgMax) * Rules.weaponDmgDegrade[trgtCls - wpnCls]
	#@log.debug("Difference", trgtCls, wpnCls, dmg)
	intDmg = int(dmg)
	if random.random() >= dmg - intDmg:
		intDmg += 1
	return intDmg

def sortShips(ships):
	# TODO: remove in 0.6
	origShips = ships[:]

	# split them
	types = {}
	for ship in ships:
		t = ship[SHIP_IDX_DESIGNID]
		if t not in types:
			types[t] = []
		types[t].append(ship)

	# sort them by HP, init counter
	incrs = {}
	counters = {}
	for t in types:
		# take shield into account
		types[t].sort(lambda a, b: cmp(a[SHIP_IDX_HP] + a[SHIP_IDX_SHIELDHP], b[SHIP_IDX_HP] + b[SHIP_IDX_SHIELDHP]))
		incrs[t] = 1.0 / (float(len(types[t])) / len(ships))
		counters[t] = incrs[t]

	# rearrange them
	ships = []

	while types:
		# find minimum
		minCounter = 1e100
		minType = None
		for t in counters:
			if minCounter > counters[t]:
				minType = t
				minCounter = counters[t]
		# pick ship, increase counter
		ships.append(types[minType].pop(0))
		counters[minType] += incrs[minType]
		if not types[minType]:
			del types[minType]
			del counters[minType]

	# check result
	# TODO: remove in 0.6
	for ship in ships:
		origShips.remove(ship)
	assert origShips == []

	return ships