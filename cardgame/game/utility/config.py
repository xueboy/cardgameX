#coding:utf-8
#!/usr/bin/env python

from gclib.config import config as gcconfig


class config(gcconfig):
	@staticmethod 
	def getClientConfig(confname):
		conf = config.getConfig(confname)
		if confname == 'dungeon':
			return config.dungeonFilter(conf)			
		if confname == 'game':
			return conf
		if confname == 'pet':
			#return config.petFileter(conf)
			return conf
		if confname == 'monster':
			return conf
		if confname == 'skill':
			return conf
		if confname == 'pet_level':
			return conf
		if confname == 'level':
			return conf
		if confname == 'equipment':
			return conf
		if confname == 'prompt':
			return conf
		if confname == 'strength_price':
			return conf
		if confname == 'strength_probability':
			return conf
		if confname == 'luck':
			return conf
		if confname == 'stone':
			return conf
		if confname == 'stone_probability':
			return config.stoneProbabilityFilter(conf)
		if confname == 'stone_level':
			return conf
		if confname == 'educate':
			return conf
		if confname == 'educate_grade':
			return conf
		if confname == 'almanac_combination':
			return conf
		if confname == 'reborn':
			return conf
		return None
	
	
	@staticmethod 
	def getClientConfigMd5(confname):
		confobj = config.getClientConfig(confname)
		if confobj:
			return config.getMd5(confobj)
		return ''		
			
	@staticmethod
	def dungeonFilter(conf):
		data = []
		for battle in conf:
			b = {}
			b['battleId'] = battle['battleId']
			b['rule'] = battle['rule']
			b['battleName'] = battle['battleName']			
			b['imageId'] = battle['imageId']
			b['field'] = []
			for field in battle['field']:
				f = {}
				f['fieldId'] = field['fieldId']
				f['fieldName'] = field['fieldName']
				f['stamina'] = field['stamina']				
				f['difficult'] = field['difficult']
				b['field'].append(f)
			data.append(b)			
		return data
	
	@staticmethod	
	def petFileter(conf):
		data = {}
		for cardid in conf:
			c = {}
			c['imageId'] = conf[cardid]['imageId']
			c['icon'] = conf[cardid]['icon']			
			c['name'] = conf[cardid]['name']
			c['type'] = conf[cardid]['type']			
			c['leadership'] = conf[cardid]['leadership']
			c['nature'] = conf[cardid]['nature']
			c['maxLevel'] = conf[cardid]['maxLevel']
			c['hp'] = conf[cardid]['hp']
			c['attack'] = conf[cardid]['attack']
			c['recover'] = conf[cardid]['recover']
			c['agile'] = conf[cardid]['agile']			
			c['skillId'] = conf[cardid]['skillId']			
			c['evoPrice'] = conf[cardid]['evoPrice']
			c['evoId'] = conf[cardid]['evoId']
			c['evoMaterial'] = conf[cardid]['evoMaterial']
			c['describe'] = conf[cardid]['describe']
			data[cardid] = c
		return data
		
		
	@staticmethod
	def getMaxStamina(level):
		levelConf = config.getConfig('level')		
		return levelConf[level - 1]['sp']
		return 0
		

	@staticmethod
	def luckFilter(conf):
		data = {}
		for luckid in conf:
			l = {}
			l['name'] = conf[luckid]['name']
			l['luckid'] = conf[luckid]['luckid']
			l['value'] = conf[luckid]['value']
			l['type'] = conf[luckid]['type']
			l['valuetype'] = conf[luckid]['valuetype']			
			data[luckid] = l
		return data
			
	@staticmethod
	def stoneProbabilityFilter(conf):
		data = {}
		data['visitGold'] = conf['visitGold']
		data['visitGem'] = conf['visitGem']		
		return data