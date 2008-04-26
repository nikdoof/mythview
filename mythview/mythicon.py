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
	
	def __init__(self, id, h, w):
	
		self.loaded = False
		mythtv = MythTV()
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
		pixbufload.close()

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
