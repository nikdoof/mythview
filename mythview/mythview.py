#!/usr/bin/env python
#
#    Myth View - Now/Next Viewer for MythTV
#    Copyright (C) 2008 Andrew Williams
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA

import sys
try:
 	import pygtk
  	pygtk.require("2.0")
except:
  	pass
try:
	import gtk
  	import gtk.glade
except:
	sys.exit(1)

import time
import datetime

from mythicon import MythIcon
from mythnownext import MythNowNext
from MythTV import *

class MythViewUI:
	def __init__(self):

		#Set the Glade file
		self.gladefile = "mythview.glade"  
	        self.wTree = gtk.glade.XML(self.gladefile) 

		self.mythtv = MythTV()
		self.icon_size = 32
		
		#Get the Main Window, and connect the "destroy" event
		self.window = self.wTree.get_widget("MainWindow")
		if (self.window):
			self.window.connect("destroy", gtk.main_quit)
			self.wTree.signal_autoconnect({"on_btnRefresh_clicked" : self.btnRefresh_clicked})
		
		self.statusbar = self.wTree.get_widget("MainStatusBar")
		self.channelStore = gtk.ListStore(int, int, gtk.gdk.Pixbuf, str, str, str)

		# Setup the TreeView
    		def addTreeColumn(title, ctype, visible,size):
        		column = gtk.TreeViewColumn(title, ctype)
			column.set_cell_data_func(ctype, self.FillCellIcon)
        		column.set_resizable(True)
        		column.set_expand(True)
			column.set_visible(visible)
			if size > 0:
				column.set_fixed_width(size)
        		self.channelTree.append_column(column)

		self.channelTree = self.wTree.get_widget("ChannelView")
		addTreeColumn("Channel ID", gtk.CellRendererText(), False,self.icon_size)
		addTreeColumn("Channel #", gtk.CellRendererText(), True, 0)
		addTreeColumn("Icon", gtk.CellRendererPixbuf(), True, 0)
		addTreeColumn("Name", gtk.CellRendererText(), True, 0)
		addTreeColumn("Now", gtk.CellRendererText(), True, 0)
		addTreeColumn("Next", gtk.CellRendererText(), True, 0)

		self.UpdateTree()

		self.window.show()
	
	def UpdateTree(self):

		self.statusbar.push(0,"Refreshing...")

		rows = MythNowNext(self.mythtv).get_all()
		
		self.channelStore.clear()

		for row in rows:

			if row[1]:
				icon = MythIcon(self.mythtv, row[0], self.icon_size, self.icon_size).pixbuf
			else:
				icon = None
			
			# http://www.goldb.org/goldblog/2008/02/06/PythonConvertSecsIntoHumanReadableTimeStringHHMMSS.aspx
			def humanize_time(secs):
				mins, secs = divmod(secs, 60)
				hours, mins = divmod(mins, 60)
				return '%02d:%02d:%02d' % (hours, mins, secs)

			now = "%s\n%s remaning" % (row[4], humanize_time(row[6]))


			t = datetime.datetime.now()
			next_starttime = t + datetime.timedelta(seconds=row[6])

			next = "%s\nStarts: %s" % (row[5], next_starttime.strftime("%I:%M%P"))

			self.channelStore.append([row[0], row[2], icon, row[3], now, next])

		self.statusbar.pop(0)
		self.channelTree.set_model(self.channelStore)

	def FillCellIcon(self, column, cell, model, iter):

		if column.get_title() == 'Channel ID':
			cell.set_property('text', model.get_value(iter, 0))
		if column.get_title() == 'Channel #':
			cell.set_property('text', model.get_value(iter, 1))
		if column.get_title() == 'Icon':
		        cell.set_property('pixbuf', model.get_value(iter, 2))
		if column.get_title() == 'Name':
			cell.set_property('text', model.get_value(iter, 3))
		if column.get_title() == 'Now':
			cell.set_property('text', model.get_value(iter, 4))
		if column.get_title() == 'Next':
			cell.set_property('text', model.get_value(iter, 5))
        	return


	#### Events

	def btnRefresh_clicked(self, *args):
		self.UpdateTree()

	def main(self):
		gtk.main()

print __name__
if __name__ == "__main__":
	base = MythViewUI()
	base.main()
