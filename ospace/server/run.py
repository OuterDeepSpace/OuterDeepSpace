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

import sys

# setup system path
sys.path.insert(0,"lib")

import os, atexit
import getopt

#configure gc
#import gc
#gc.set_debug(gc.DEBUG_STATS | gc.DEBUG_COLLECTABLE | gc.DEBUG_UNCOLLECTABLE |
#	gc.DEBUG_INSTANCES | gc.DEBUG_OBJECTS)

# legacy logger
from ige import log
log.setMessageLog('var/logs/messages.log')
log.setErrorLog('var/logs/errors.log')

#~ # standard logger
#~ import logging, logging.handlers
#~ log = logging.getLogger()
#~ log.setLevel(logging.DEBUG)
#~ # file handler
#~ h = logging.handlers.RotatingFileHandler('var/log/server.log', 'a', 16 * 1024 * 1024, 5)
#~ h.setLevel(logging.INFO)
#~ h.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(name)s %(message)s'))
#~ log.addHandler(h)
#~ # stdout handler (TODO: disable in productin server)
#~ h = logging.StreamHandler(sys.stdout)
#~ h.setLevel(logging.DEBUG)
#~ h.setFormatter(logging.Formatter('%(created)d %(levelname)-5s %(name)-8s %(message)s'))
#~ log.addHandler(h)

# options
# parse arguments
log.message('Parsing arguments...')
options = ('reset', 'upgrade', 'devel', 'restore=', "config=")

opts, args = getopt.getopt(sys.argv[1:], '', options)

optReset = 0
optUpgrade = 0
optDevel = 0
optRestore = 0
optConfig = "var/config.ini"

for opt, arg in opts:
	if opt == '--reset':
		optReset = 1
	elif opt == '--upgrade':
		optUpgrade = 1
	elif opt == '--devel':
		optDevel = 1
	elif opt == '--restore':
		optRestore = arg
	elif opt == "--config":
		optConfig = arg

# record my pid

# pid
pidFd = os.open("var/server.pid", os.O_CREAT | os.O_EXCL | os.O_WRONLY)
os.write(pidFd, str(os.getpid()))
# TODO: check if server.pid points to the running process

game = None
msgMngr = None
clientMngr = None
issueMngr = None

# define and register exit function
def cleanup():
# shut down game
	try:
		if game:
			log.message('Shutting down game...')
			game.shutdown()

		if msgMngr:
			log.message('Shutting down message manager...')
			msgMngr.shutdown()

		if clientMngr:
			log.message('Shutting down client manager...')
			clientMngr.shutdown()

		if issueMngr:
			log.message('Shutting down issue manager...')
			issueMngr.shutdown()
	except:
		log.exception("Shutdown of the server failed")

	log.message('Shutted down')
	log.message("Cleaning up...")
	# delete my pid
	os.close(pidFd)
	os.remove("var/server.pid")

atexit.register(cleanup)

#~fh = open(pidFilename, 'w')
#~print >> fh, os.getpid()
#~fh.close()

# read configuration
from ige.Config import Config
log.message("Reading configuration from", optConfig)
config = Config(optConfig)

# set ruleset
from  ige.ospace import Rules

Rules.initRules("res/rules/standard")

# startup game
log.debug('Importing IGE modules...')

import ige.RPCServer as server
import ige
from ige.ClientMngr import ClientMngr
from ige.MsgMngr import MsgMngr
from ige.IssueMngr import IssueMngr
from ige.ospace.GameMngr import GameMngr

# set runtime mode
ige.setRuntimeMode(not optDevel)

gameName = 'Alpha'

# open database
from ige.MetakitDatabase import MetakitDatabase, MetakitDatabaseString

log.debug("Creating databases...")
gameDB = MetakitDatabase("var/db_data", "game_%s" % gameName, cache = 15000)
clientDB = MetakitDatabaseString("var/db_data", "accounts", cache = 100)
msgDB = MetakitDatabaseString("var/db_data", "messages", cache = 1000)

if optRestore:
	gameDB.restore("var/%s-game_Alpha.osbackup" % optRestore)
	clientDB.restore("var/%s-accounts.osbackup" % optRestore)
	# TODO: remove afer fix of the message database
	# the following code imports to the message database only valid entries
        # and forces mailbox scan
	incl = [1]
	incl.extend(gameDB[1].galaxies)
	incl.extend(gameDB[1].players)
	def include(k, l = incl):
		for i in l:
			if k.startswith("Alpha-%d-" % i) or (k == "Alpha-%d" % i):
				return True
		return False
	msgDB.restore("var/%s-messages.osbackup" % optRestore, include = include)

# initialize game
log.message('Initializing game \'%s\'...' % gameName)

log.debug("Initializing issue manager")
issueMngr = IssueMngr()
log.debug("Initializing client manager")
clientMngr = ClientMngr(clientDB)
log.debug("Initializing message manager")
msgMngr = MsgMngr(msgDB)

log.debug("Initializing game manager")
game = GameMngr(gameName, config, clientMngr, msgMngr, gameDB)

if optReset:
	# reset game
	log.message('Resetting game \'%s\'...' % gameName)
	game.reset()
else:
	# normal operations
	game.init()

	if optUpgrade:
		game.upgrade()
		msgMngr.upgrade()

	game.start()

	server.init(clientMngr)
	server.register(game)

	server.xmlrpcPublish('clientmngr', clientMngr)
	server.xmlrpcPublish('issuemngr', issueMngr)

	log.message('Initialized. Starting server...')

	try:
		import psyco
		psyco.full()
		log.message("Using psyco with full acceleration")
	except ImportError:
		log.message("NOT using psyco")
	server.start()
