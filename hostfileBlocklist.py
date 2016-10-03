#! /usr/bin/python
########################################################################
# Downloads and compiles a hostfile using multiple sources from the net.
# Copyright (C) 2016  Carl J Smith
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
########################################################################
import sys
# add the hostfile blocklist libary
sys.path.append('/usr/share/hostfileBlocklist/')
import hostfileblocklistLib
# launch the main program
hostfileblocklistLib.main(sys.argv)
