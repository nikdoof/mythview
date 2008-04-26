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
