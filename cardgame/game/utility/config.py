#coding:utf-8
#!/usr/bin/env python

from gclib.gcconfig import gcconfig


class config(gcconfig):
	@staticmethod 
	def getClientConfig(confname):
		conf = config.getConfig(confname)
		if confname == 'dungeon':
			conf = config.dungeonFilter(conf)
			return conf
		if confname == 'game':
			return conf
		return None
	
	
	@staticmethod 
	def getClientConfigMd5(confname):
		confobj = config.getClientConfig(confname)
		if confobj != None:
			return config.getMd5(confobj)
		return ''
		
		
		
			
	@staticmethod
	def dungeonFilter(conf):
		data = []
		for battle in conf:
			b = {}
			b['battleId'] = battle['battleId']
			b['rule'] = battle['rule']
			b['battleBigName'] = battle['battleBigName']
			b['battleBigNameEn'] = battle['battleBigNameEn']
			b['battleImageId'] = battle['battleImageId']
			b['field'] = []
			for field in battle['field']:
				f = {}
				f['FieldId'] = field['FieldId']
				f['battleSmallName'] = field['battleSmallName']
				f['battlePower'] = field['battlePower']
				f['totalRound'] = field['totalRound']
				f['degree'] = field['degree']
				b['field'].append(f)
			data.append(b)			
		return data
	
	
	@staticmethod
	def getMaxStamina(level):
		levelConf = config.getConfig('level')
		levelKey = str(level)
		if levelConf.has_key(levelKey):
			return levelConf[levelKey]['sp']
		return 0