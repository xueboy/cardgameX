#coding:utf-8
#!/usr/bin/env python

from gclib.gcconfig import gcconfig


class config(gcconfig):
	@staticmethod 
	def getClientConfig(confname):
		conf = config.getConfig(confname)
		if confname == 'dungeon':
			return config.dungeonFilter(conf)			
		if confname == 'game':
			return conf
		if confname == 'card':
			return config.cardFileter(conf)
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
		
	def cardFileter(conf):
		data = {}
		for cardid in conf:
			c = {}
			c['imageId'] = conf[cardid]['imageId']
			c['icon'] = conf[cardid]['icon']
			c['job'] = conf[cardid]['job']
			c['name'] = conf[cardid]['name']
			c['type'] = conf[cardid]['type']
			c['attackTurn'] = conf[cardid]['attackTurn']
			c['leadership'] = conf[cardid]['leadership']
			c['nature'] = conf[cardid]['nature']
			c['maxLevel'] = conf[cardid]['maxLevel']
			c['hp'] = conf[cardid]['hp']
			c['attack'] = conf[cardid]['attack']
			c['recove'] = conf[cardid]['recove']
			c['agile'] = conf[cardid]['agile']			
			c['skillId'] = conf[cardid]['skillId']
			c['price'] = conf[cardid]['price']
			c['evoPrice'] = conf[cardid]['evoPrice']
			c['evoId'] = conf[cardid]['evoId']
			c['evoMaterial'] = conf[cardid]['evoMaterial']
			c['describe'] = conf[cardid]['describe']
			
			
			
			
	
	
	@staticmethod
	def getMaxStamina(level):
		levelConf = config.getConfig('level')
		levelKey = str(level)
		if levelConf.has_key(levelKey):
			return levelConf[levelKey]['sp']
		return 0