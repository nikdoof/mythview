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
import os.path

try:
	import gtk
except:
	print "GTK/GDK binding not found, exiting..."
	sys.exit(1)

from urllib import urlopen
from MythTV import *

class MythIcon:
	
	def __init__(self, mythtv, id, h=None, w=None):
	
		self.loaded = False
		pixbufload = gtk.gdk.PixbufLoader()

		if os.path.isfile("/tmp/mythtv/%d.jpg" % id):
			# File has been cached before, reload from cache
			urlstr = 'file:///tmp/mythtv/%d.jpg' % id
		else:
			urlstr = 'http://%s:%d/Myth/GetChannelIcon?ChanId=%s' % (mythtv.master_host, mythtv.master_port + 1, id)

		url = urlopen(urlstr)
		for data in url:
			pixbufload.write(data)
		if pixbufload.get_pixbuf() != None:
			self.pixbuf = pixbufload.get_pixbuf()
		self.loaded = True		
		
		if os.path.exists('/tmp/mythtv') == False:	
			os.mkdir('/tmp/mythtv')
		self.save('/tmp/mythtv/%d.jpg' % id, "jpeg", {})

		if h or w:
			self.resize(h,w)

	def resize(self, h, w):
		if self.loaded:
			self.pixbuf = self.pixbuf.scale_simple(w,h,gtk.gdk.INTERP_BILINEAR)

	def save(self, filename, type, opt):
		if filename and self.loaded:
			self.pixbuf.save(filename, type, opt)
