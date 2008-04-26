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

class MythViewUI:
	def __init__(self):

		#Set the Glade file
		self.gladefile = "mythview.glade"  
	        self.wTree = gtk.glade.XML(self.gladefile) 
		
		#Get the Main Window, and connect the "destroy" event
		self.window = self.wTree.get_widget("MainWindow")
		if (self.window):
			self.window.connect("destroy", gtk.main_quit)

		self.channelStore = gtk.ListStore(int, gtk.gdk.Pixbuf, str)

		# Setup the TreeView
    		def addTreeColumn(tree, title, ctype, datafunc, visible,size):
        		column = gtk.TreeViewColumn(title, ctype)
			if datafunc: column.set_cell_data_func(ctype, datafunc)
        		column.set_resizable(False)
        		column.set_expand(True)
			column.set_visible(visible)
			#if size:
			#	column.set_width(size)
        		tree.append_column(column)

		self.channelTree = self.wTree.get_widget("ChannelView")
		addTreeColumn(self.channelTree, "Channel", gtk.CellRendererText(), None, False,64)
		addTreeColumn(self.channelTree, "Icon", gtk.CellRendererPixbuf(), self.FillChanIcon, True, 0)
		addTreeColumn(self.channelTree, "Now", gtk.CellRendererText(), None, True, 0)

		# Test Data
		self.channelStore.append([1,MythIcon(1126,64,64).pixbuf,"test 1"])
                self.channelStore.append([2,None,"test 2"])

		self.channelTree.set_model(self.channelStore)

		self.window.show()
	
	def FillChanIcon(self, column, cell, model, iter):
	        cell.set_property('pixbuf', model.get_value(iter, 1) )
        	return

	def main(self):
		gtk.main()

print __name__
if __name__ == "__main__":
	base = MythViewUI()
	base.main()
