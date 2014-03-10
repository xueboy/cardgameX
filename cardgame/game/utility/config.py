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
			return config.gameFilter(conf)
		if confname == 'pet':
			#return config.petFileter(conf)
			return conf
		if confname == 'monster':
			return conf
		if confname == 'skill':
			return conf
		if confname == 'skill_effect':
			return conf
		if confname == 'skill_level':
			return conf
		if confname == 'pet_level':
			return conf
		if confname == 'level':
			return conf
		if confname == 'equipment':
			return conf
		if confname == 'item':
			return conf
		if confname == 'prompt':
			return conf
		if confname == 'strength_price':
			return conf
		if confname == 'strength_probability':
			return config.strengthProbabilityFilter(conf)
		if confname == 'luckycat_bless':
			return conf
		if confname == 'luckycat_profit':
			return conf
		if confname == 'luck':
			return conf
		if confname == 'stone':
			return conf
		if confname == 'stone_probability':
			return config.stoneProbabilityFilter(conf)
		if confname == 'educate':
			return conf
		if confname == 'educate_grade':
			return conf
		if confname == 'almanac_combination':
			return conf
		if confname == 'reborn':
			return conf
		if confname == 'trp':
			return conf
		if confname == 'trp_price':
			return conf
		if confname == 'language':
			return conf
		if confname == 'drop':
			return config.dropFilter(conf)
		if confname == 'dialog':
			return conf
		if confname == 'drama':
			return conf
		if confname == 'quest':
			return config.questFilter(conf)
		if confname == 'signin':
			return conf
		if confname == 'levelup':
			return conf
		if confname == 'open_award':
			return conf
		if confname == 'ladder_score':
			return conf
		if confname == 'arena_loot':
			return conf
		if confname == 'tower_monster':
			return conf
		if confname == 'tower_markup':
			return conf
		if confname == 'tower_award':
			return conf
		if confname == 'medal':
			return config.medalFilter(conf)
		if confname == 'medal_loot':
			return conf
		if confname == 'medal_level':
			return config.medalLevelFilter(conf)
		if confname == 'mall_price':
			return conf
		if confname == 'practice_property':
			return conf
		if confname == 'practice_level':
			return conf
		if confname == 'slotmachine':
			return conf
		if confname == 'vip':
			return conf
		if confname == 'potential_price':
			return conf
		if confname == 'email':
			return config.emailFilter(conf)
		if confname == 'gift':
			return conf
		if confname == 'ladder_score':
			return conf
		return None
	
	
	@staticmethod 
	def getClientConfigMd5(confname):
		confobj = config.getClientConfig(confname)
		if confobj:
			return config.getMd5(confobj)
		return ''		
	
	@staticmethod
	def gameFilter(conf):
		data = conf.copy()		
		del data['dungeon_medal_probablity']
		del data['medal_holder_relate_level_at_last']
		del data['medal_holder_count']
		del data['medal_holder_appear_member_position']
		del data['medal_grab_probablity']		
		del data['scene_player_count']
		del data['equipment_strength_critical_probability']
		del data['garcha_10_dropid1']
		del data['garcha_100_dropid1']
		del data['garcha_100_dropid2']
		del data['garcha_100_dropid3']
		del data['garcha_10000_dropid1']
		del data['garcha_10000_dropid2']
		del data['garcha_10000_dropid3']
		del data['garcha_skill_10_dropid1']
		del data['garcha_skill_10_dropid2']
		del data['garcha_skill_dropid']
		del data['gift_record_max_count']
		del data['gift_ladder_max_size']
		del data['invite_max_count']
		del data['infection_ladder_level_group']
		del data['infection_dungeon_probability']
		del data['infection_quality']
		del data['infection_ladder_max_size']
		del data['medal_levelup_wink_finish_count']
		del data['infection_explore_probability']
		del data['explore_max_times']
		del data['explore_times_on_levelup']
		del data['explore_friend_count']
		del data['explore_extra_times_probability']
		del data['explore_gold_and_exp_revision']
		del data['explore_critical_probability_growth']
		del data['explore_critical_income_rate']		
		return data
	
			
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
				f['dayCount'] = field['dayCount']
				f['exp'] = field['exp']
				f['mayDrop'] = field['mayDrop']
				f['waveCount'] = len(field['wave'])
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
		return levelConf[level - 1]['stamina']
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
		
		
	@staticmethod
	def questFilter(conf):
		data = {}
		for questid in conf:
			q = conf[questid].copy()			
			if isinstance(q['finishValue'], list):
				q['finishValue'] = []			
				for e in conf[questid]['finishValue']:
					q['finishValue'].append(str(e))
			else: 
				q['finishValue'] = [str(conf[questid]['finishValue'])]
					
			data[questid] = q
		return data
		
	@staticmethod
	def strengthProbabilityFilter(conf):
		data = {}
		for item in conf:
			data[str(item[0])] = item[1]		
		return data
		
	@staticmethod
	def dropFilter(conf):
		data = {}
		
		for (dropid, d) in conf.items():
			if d['isClient']:
				data[dropid] = d['drop']
		return data
		
	@staticmethod
	def emailFilter(conf):
		data = {}
		
		for (emailid, email) in conf.items():
			d = email.copy()
			del d['optype']
			del d['opvaule']
			data[emailid] = d
			
		return data
	
	@staticmethod
	def medalFilter(conf):
		data = {}
		for (medalid, medal) in conf.items():
			d = medal.copy()
			del d['medalid']
			data[medalid] = d			
		return data
	
	@staticmethod
	def medalLevelFilter(conf):
		data = {}
		for (medalid, levelInfo) in conf.items():
			d = []
			for l in levelInfo:
				i = l.copy()
				del i['typestr']
				d.append(i)
			
			data[medalid] = d			
		return data