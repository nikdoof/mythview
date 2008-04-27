#!/usr/bin/env python
# example base.py

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
		
		self.channelStore = gtk.ListStore(int, int, gtk.gdk.Pixbuf, str, str)

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

		self.UpdateTree()

		self.window.show()
	
	def UpdateTree(self):

		print "Refresh Fired"

		rows = MythNowNext(self.mythtv).get_nownext()
		
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

			now = "%s\n%s remaning" % (row[4], humanize_time(row[5]))

			self.channelStore.append([row[0], row[2], icon, row[3], now])

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
