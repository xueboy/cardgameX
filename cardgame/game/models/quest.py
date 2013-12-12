#coding:utf-8
#!/usr/bin/env python


class quest(object):
	
	def __init__(self):
		object.__init__(self)
		self.finish = []
		self.current = []
		
	@staticmethod
	def makeQuest(questid):
		return {'questid':questid, 'count':0}
		
		
	def levelUpdate(self):
		questConf = config.getConfig('quest')
		usr = self.user
		for questid ,questInfo in questConf:
			alreadyAccept = False
			if questInfo['level'] <= usr.level:
				for q in self.finish:
					if q['questid'] == questid:
						alreadyAccept = True
						break
				if alreadyAccept:
					continue
				for q in self.current:
					if q['questid'] == questid:
						alreadyAccept = True
						break
				if alreadyAccept:
					continue
				self.accept(questid)
			
	def accept(questid):
		q = quest.makeQuest(questid)
		self.current.append(q)
		
