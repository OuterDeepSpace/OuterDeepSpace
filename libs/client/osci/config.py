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

import os
import os.path

from ConfigParser import ConfigParser

class Config:
	"""Encapsulation of ConfigParser class.

	Attributes of this class represents sections
	of config file. If some want to assing value
	to section, an AttruteError is thrown, except
	None value, which removes section with given
	name. When asking for nonexisting section,
	section with same name is created. For
	existing section an instance of Section class
	is returned.
	"""
	def __init__(self, file):
		# We first check ~/.ospace for this file
		relative_dir = os.path.expanduser("~/.ospace")
		target_file = os.path.join(relative_dir, file)

		# If the file exists, target that one instead
		try:
			with open(target_file, "r") as handle:
				file = target_file
		except IOError:
			pass

		self.__dict__["_config"] = ConfigParser()
		self._config.read(file)

	def __getattr__(self, name):
		if not self._config.has_section(name):
			self._config.add_section(name)

		return Section(self._config, name)

	def __setattr__(self, name, value):
		if value == None:
			self._config.remove_section(name)
		else:
			raise AttributeError("Cannot assign value to config section")

	def save(self, file):
		# Just dump into ~/.ospace
		relative_dir = os.path.expanduser("~/.ospace")

		if (os.path.isdir(relative_dir) is False):
			os.mkdir(relative_dir)

			# Since we only ever seem to have single-depth paths for these configs
			# and we only ever seem to point into var, just create it
			os.mkdir(os.path.join(relative_dir, "var"))

		file = os.path.join(relative_dir, file)

		fh = open(file, 'w')
		self._config.write(fh)
		fh.close()

class Section:
	"""Represent section of ConfigParser class.

	Attributes of this class represents options
	of given section. when asking for option
	value None value is returned if given option
	does not exist, otherwise option value is
	returned.
	"""
	def __init__(self, config, name):
		self.__dict__["_config"] = config
		self.__dict__["section"] = name

	def __getattr__(self, name):
		if self._config.has_option(self.section, name):
			return self._config.get(self.section, name)
		else:
			return None

	def __setattr__(self, name, value):
		if value is None:
			self._config.remove_option(self.section, name)
			if not self._config.options(self.section):
				# no option -- delete me
				self._config.remove_section(self.section)
		else:
			self._config.set(self.section, name, str(value))
