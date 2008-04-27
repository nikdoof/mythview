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

from MythTV import *

class MythNowNext:

	def __init__(self,mythtv):
		if mythtv:
			self.db = mythtv.db
		else:
			self.db = MythDB()

	def get_nownext(self):
		c = self.db.cursor()

		c.execute("""   SELECT channel.chanid, channel.icon, cast(channel.channum as signed) as channum, 
				channel.name, program.title, 
				time_to_sec(timediff(time(program.endtime), time(now()) )) as timetoend
				FROM channel, program
				WHERE program.chanid = channel.chanid
				AND program.starttime <= NOW( )
				AND program.endtime >= NOW( )
				AND channum <> 0
				ORDER BY channum """)

		rows = c.fetchall()
		c.close()
		
		if rows:
			return rows
		else:
			return None
