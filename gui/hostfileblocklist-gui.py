#! /usr/bin/python
########################################################################
# GUI for editing Hostfile Blocklist config files
# Copyright (C) 2014  Carl J Smith
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
import os,tkMessageBox
from Tkinter import *
# main class for the program
class App:
	def __init__(self,master):
		# Top frame contains commands for working with config files
		buttonFrameRow1 = Frame(master)
		buttonFrameRow2 = Frame(master)
		buttonFrameRow3 = Frame(master)
		# below frame contains the exit and about buttons
		buttonFrameBottom = Frame(master)
		# align things to the right
		buttonFrameBottomRight = Frame(buttonFrameBottom)
		# first row for buttons really only has a label
		Label(buttonFrameRow1,text='You must Rebuild the Hosts File to see any changes.',justify=CENTER,wrap=400, width=80,height=3,anchor=N).pack(side=TOP)
		Button(buttonFrameRow1, text="Rebuild Hosts File", fg="Black", command=self.rebuildHostfile).pack(side=TOP)
		# start row 2 of buttons
		Button(buttonFrameRow2, text='Edit Protected Domains', command=self.editProtectedDomains).pack(side=LEFT)
		Button(buttonFrameRow2, text='Edit external Hosts lists', command=self.editExternalHosts).pack(side=LEFT)
		Button(buttonFrameRow2, text='Edit external Domains lists', command=self.editExternalDomains).pack(side=LEFT)
		# start row 3 of buttons
		Button(buttonFrameRow3, text='Edit unblock list', command=self.editUnblockList).pack(side=LEFT)
		Button(buttonFrameRow3, text='Edit Redirects', command=self.editRedirects).pack(side=LEFT)
		Button(buttonFrameRow3, text='Edit supplemental hosts file', command=self.editSupplementalHostsFile).pack(side=LEFT)
		Button(buttonFrameRow3, text='Edit config file (json formated)', command=self.editConfig).pack(side=LEFT)

		buttonFrameRow1.pack(side=TOP)
		buttonFrameRow2.pack(side=TOP)
		buttonFrameRow3.pack(side=TOP)
		#########################################################
		# a simple quit button
		Button(buttonFrameBottomRight, text='Quit', command=exit,justify=RIGHT).pack(side=RIGHT)
		# A button that brings up a popup about the program
		Button(buttonFrameBottomRight, text='About', command=self.showAbout,justify=RIGHT).pack(side=RIGHT)
		buttonFrameBottom.pack(side=RIGHT)
		buttonFrameBottomRight.pack(side=RIGHT)
		#########################################################
		# set the window title
		master.wm_title('Hostfile Blocklist Config Editor')
		# disable the user from resizing the window
		master.resizable(False,False)
	def rebuildHostfile(self):
		os.system('gksu \'xterm -T Rebuilding\ Hostfile\ Blocklist... -e "hostfileblocklist"\'')
		#~ print 'lol'
	def editProtectedDomains(self):
		os.system('gksu exo-open /etc/hostfileBlocklist/protectedDomains.source')
	def editExternalHosts(self):
		os.system('gksu exo-open /etc/hostfileBlocklist/hostfiles.source')
	def editExternalDomains(self):
		os.system('gksu exo-open /etc/hostfileBlocklist/domainLists.source')
	def editRedirects(self):
		os.system('gksu exo-open /etc/hostfileBlocklist/redirectList.source')
	def editUnblockList(self):
		os.system('gksu exo-open /etc/hostfileBlocklist/unblockList.source')
	def editSupplementalHostsFile(self):
		os.system('gksu exo-open /etc/hostfileBlocklist/supplementalBlocklist.host')
	def editConfig(self):
		os.system('gksu exo-open /etc/hostfileBlocklist/config.source')
	def showAbout(self):
		tkMessageBox.showinfo(title='About',message='This is a small program designed to be a interface to configuring the config files of the hostfile blocklist program.\n\nIt is very minimal and is likely to stay that way for quite a long time since the program is designed to be highly automated.')
# init code for class containing program
root = Tk()
app = App(root)
root.mainloop()
