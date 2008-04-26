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
		
		#Get the Main Window, and connect the "destroy" event
		self.window = self.wTree.get_widget("MainWindow")
		if (self.window):
			self.window.connect("destroy", gtk.main_quit)

		self.channelStore = gtk.ListStore(int, gtk.gdk.Pixbuf, str)

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
		addTreeColumn("Channel", gtk.CellRendererText(), False,64)
		addTreeColumn("Icon", gtk.CellRendererPixbuf(), True, 0)
		addTreeColumn("Now", gtk.CellRendererText(), True, 0)

		self.UpdateTree()

		self.window.show()
	
	def UpdateTree(self):
		# Test Data
		#self.channelStore.append([1,MythIcon(1805,64,64).pixbuf,"BBC One"])
                #self.channelStore.append([2,MythIcon(1172,64,64).pixbuf,"BBC Two"])

		rows = MythNowNext(self.mythtv).get_nownext()
		
		for row in rows:

			if row[1]:
				self.channelStore.append([row[0], MythIcon(self.mythtv, row[0], 64, 64).pixbuf, row[3]])
			else:
				self.channelStore.append([row[0], None, row[3]])

			print row[0]

		self.channelTree.set_model(self.channelStore)

	def FillCellIcon(self, column, cell, model, iter):

		if column.get_title() == 'Icon':
		        cell.set_property('pixbuf', model.get_value(iter, 1) )
		if column.get_title() == 'Now':
			cell.set_property('text', model.get_value(iter, 2))
        	return

	def main(self):
		gtk.main()

print __name__
if __name__ == "__main__":
	base = MythViewUI()
	base.main()
