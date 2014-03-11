
from gclib.utility import currentTime
from gclib.cacheable import cacheable
from game.utility.config import config
import copy

class massyell(cacheable):
	
	def __init__(self):
		"""
		构造函数
		"""
		cacheable.__init__(self)
		self.record = []
		self.sequenceid = 0	
		
		
	def yell(self, roleid, name, msg):		
		"""
		世界聊天
		"""		
		self.updatemass()
		y = {}
		self.sequenceid = self.sequenceid + 1
		y['roleid'] = roleid
		y['name'] = name
		y['yell'] = msg
		y['create_time'] = currentTime()
		y['id'] = str(self.sequenceid)
		self.record.append(y)
		self.save()		
		return y
		
	def getData(self):
		"""
		得到data
		"""
		data = cacheable.getData(self)
		data['record'] = self.record
		data['sequenceid'] = self.sequenceid		
		return data
	
	def load(self, cacheid, data):
		"""
		加载
		"""
		cacheable.load(self, cacheid, data)
		self.record = data['record']
		self.sequenceid = data['sequenceid']
		return 0
		
	def updatemass(self):
		"""
		刷新世界聊天
		"""
		gameConf = config.getConfig('game')		
		expire = gameConf['yell_expiry_period']
		now = currentTime()
		self.record = filter(lambda r: r['create_time'] + expire >= now, self.record)
		
	def listen(self, usr):
		"""
		收听世界聊天
		"""
		record = copy.copy(self.record)		
		for key in record:
			if key < usr.yell_hear_id:
				del record[key]		
		return record