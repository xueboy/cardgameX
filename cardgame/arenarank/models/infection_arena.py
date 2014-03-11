#coding:utf-8
#!/usr/bin/env python

from gclib.facility import facility
from gclib.utility import currentTime, is_same_day, randint
from game.utility.config import config
from game.utility.email import email

class infection_arena(facility):
		
	def __init__(self):
		"""
		初始化
		"""
		facility.__init__(self)
		self.battle = {}		
		self.user = {}
		self.prestige_ladder = {}
		self.damage_ladder = {}
		self.last_update_time = 0
	
	def getData(self):
		"""
		得到 data
		"""
		data = {}
		data['battle'] = self.battle
		data['user'] = self.user
		data['prestige_ladder'] = self.prestige_ladder
		data['damage_ladder'] = self.damage_ladder
		data['last_update_time'] = self.last_update_time
		return data
		
	def load(self, name, data):
		"""
		加载
		"""
		facility.load(self, name, data)
		self.battle = data['battle']
		self.user = data['user']
		self.prestige_ladder = data['prestige_ladder']
		self.damage_ladder = data['damage_ladder']
		self.last_update_time = data['last_update_time']		
	
	@staticmethod
	def make_user(name):
		"""
		制造玩家
		"""
		return {'prestige':0, 'last_hit_time': 0, 'damage':0, 'level':1, 'infection_list':[], 'name': name, 'prestige_score': 0 ,'last_award_prestige_score' : 0}
						
	@staticmethod
	def make_relief(battle):
		"""
		制造援军
		"""
		data = {}
		data['roleid'] = battle['roleid']
		data['rolename'] = battle['rolename']
		data['create_time'] = battle['create_time']
		data['quality'] = battle['quality']
		data['level'] = battle['level']
		return data		
		
	@staticmethod
	def battle_total_hp(battle):
		"""
		总hp
		"""
		totalhp = 0
		for mon in battle['monster']:
			totalhp = totalhp + mon['hp']
		return totalhp
		
	@staticmethod
	def battle_is_finish(battle, now, gameConf):
		"""
		战斗完成
		"""
		return infection_arena.battle_is_escape(battle, now, gameConf) or infection_arena.battle_is_clear(battle)
		
	@staticmethod
	def battle_is_clear(battle):
		"""
		战斗全清
		"""
		return battle.has_key('last_hit')
		
	@staticmethod
	def battle_clear_time(battle):
		"""
		全清时间
		"""
		return battle[battle['last_hit']]['last_hit_time']
		
	@staticmethod
	def battle_is_escape(battle, now, gameConf):
		"""
		是否逃跑
		"""
		quality = battle['quality']
		escape_time = gameConf['infection_quality'][quality]['escape_time']
		if battle['create_time'] + escape_time < now:			
			return True		
		return False		
		
	@staticmethod
	def battle_escapse_time(battle, now, gameConf):
		"""
		逃跑时间
		"""
		quality = battle['quality']
		escape_time = gameConf['infection_quality'][quality]['escape_time']
		return battle['create_time'] + escape_time			
				
	def encounter(self, roleid, name):		
		"""
		遇敌
		"""
		gameConf = config.getConfig('game')
		now = currentTime()		
		self.update_battle(now, gameConf)
		if self.battle.has_key(roleid):
			battle = self.battle[roleid][-1]
			if battle and (not infection_arena.battle_is_finish(battle, now, gameConf)):
				return {'msg': 'infection_battle_not_finish'}
			
		rd = randint()
		quality = -1
		for (i, qualityInfo) in enumerate(gameConf['infection_quality']):
			if rd > qualityInfo['probability']:
				rd = rd - qualityInfo['probability']
			else:
				quality = i
				
		if quality < 0:
			return {'msg':'infection_bad_quality'}
		
		if not self.user.has_key(roleid):
			self.user[roleid] = infection_arena.make_user(name)		
				
		level = self.user[roleid]['level']		
		self.update_prestige(roleid, now)
				
		infectionBattleConf = config.getConfig('infection_battle')
		infectionBattleInfo = infectionBattleConf[str(quality)][level - 1]
		if not infectionBattleInfo:
			return {'msg':'infection_battle_not_exist'}
		
		battle = {}
		battle['monster'] = []
		
		totalhp = 0
		monsterConf = config.getConfig('monster')		
		for monsterid in infectionBattleInfo['monster']:
			monsterInfo = monsterConf[monsterid]			
			monster = {}
			monster['monsterid'] = monsterid
			monster['hp'] = monsterInfo['hp']
			totalhp = totalhp + monsterInfo['hp']
			battle['monster'].append(monster)
		battle['monster_total_hp'] = totalhp
		battle['quality'] = quality
		battle['level'] = level
		battle['roleid'] = roleid
		battle['create_time'] = now
		battle['user'] = {}
		battle['rolename'] = name
		self.battle[roleid] = []
		self.battle[roleid].append(battle)
		
		self.user[roleid]['infection_list'].append(infection_arena.make_relief(battle))
		self.save()
		return {'battle':self.battle[roleid]}
		
			
	def beat(self, roleid, rolelevel, rolename, battleRoleid, damage):
		"""
		击败
		"""
		
		if not self.battle.has_key(battleRoleid):
			return {'msg': 'infection_battle_not_exist'}
		
		if not self.battle[battleRoleid]:
			return {'msg': 'infection_battle_not_exist'}		
		
		now = currentTime()		
		gameConf = config.getConfig('game')		
		battle = self.battle[battleRoleid][-1]
		if infection_arena.battle_is_finish(battle, now, gameConf):
			return {'msg': 'infection_battle_finish'}		
		
		self.update_battle(now, gameConf)
		
		canCall = False
		if battle['monster_total_hp'] == infection_arena.battle_total_hp(battle):
			canCall = True
		
		totaldamage = sum(damage)
		lefthp = 0
		for (i, monster) in enumerate(battle['monster']):
			monster['hp'] = monster['hp'] - damage[i]
			if monster['hp'] < 0:
				totaldamage = totaldamage + monster['hp']				
				monster['hp'] = 0
			lefthp = lefthp + monster['hp']
				
		if not battle['user'].has_key(roleid):
			battle['user'][roleid] = {}
		
		if not battle['user'][roleid].has_key('damage'):
			battle['user'][roleid]['damage'] = 0
		
		battle['user'][roleid]['damage'] = battle['user'][roleid]['damage'] + totaldamage
		battle['user'][roleid]['last_hit_time'] = now
		infectionBattleConf = config.getConfig('infection_battle')
		infectionBattleInfo = infectionBattleConf[str(battle['quality'])][battle['level'] - 1]
		prestige = int((float(totaldamage) / battle['monster_total_hp'] * infectionBattleInfo['prestige']) * gameConf['infection_quality'][battle['quality']]['prestige_rate'])
		
		if not self.user.has_key(roleid):
				self.user[roleid] = infection_arena.make_user(rolename)
		now = currentTime()
		self.update_prestige(roleid, now)
		self.user[roleid]['last_hit_time'] = now
		self.user[roleid]['prestige'] = self.user[roleid]['prestige'] + prestige
		self.user[roleid]['prestige_score'] = self.user[roleid]['prestige_score'] + prestige
		prestige_ladder_position = self.update_prestige_ladder(roleid, rolelevel, self.user[roleid]['prestige'], gameConf)		
		if battle['user'][roleid]['damage'] > self.user[roleid]['damage']:
			self.user[roleid]['damage'] = battle['user'][roleid]['damage']
			self.update_damage_ladder(roleid, rolelevel, self.user[roleid]['damage'], gameConf)
			
		data = {}
		if lefthp == 0:
			if roleid == battleRoleid and self.user[roleid]['level'] <= len(infectionBattleConf['0']):
				self.user[roleid]['level'] = self.user[roleid]['level'] + 1						
				battle['last_hit'] = roleid
		self.save()
		data['total_damage'] = totaldamage
		data['left_hp'] = lefthp
		data['prestige'] = prestige
		data['prestige_score'] = self.user[roleid]['prestige_score']
		data['prestige_ladder_position'] = prestige_ladder_position
		data['can_call'] = canCall
		return data
		
	
						
	def update_prestige_ladder(self, roleid, rolelevel, prestige, gameConf):
		"""
		更新声望排行榜
		"""
		levelGroup = gameConf['infection_ladder_level_group'][-1]
		for lg in gameConf['infection_ladder_level_group']:
			if rolelevel < lg:
				levelGroup = lg
			if not self.prestige_ladder.has_key(lg):
				self.prestige_ladder[lg] = []
			else:
				if roleid in self.prestige_ladder[lg]:
					self.prestige_ladder[lg].remove(roleid)			
		
		prestige_position = -1
		for(i, rid) in enumerate(self.prestige_ladder[levelGroup]):
			if self.user[rid]['prestige'] < prestige:
				prestige_position = i
		if prestige_position < 0 and (len(self.prestige_ladder[levelGroup]) < gameConf['infection_ladder_max_size']):
			self.prestige_ladder[levelGroup].append(roleid)
			prestige_position = len(self.prestige_ladder[levelGroup]) - 1
		elif prestige_position >= 0:
			self.prestige_ladder[levelGroup].insert(prestige_position, roleid)
		return prestige_position
		
	def update_damage_ladder(self, roleid, rolelevel, damage, gameConf):
		"""
		更新伤害排行
		"""
		levelGroup = gameConf['infection_ladder_level_group'][-1]
		for lg in gameConf['infection_ladder_level_group']:
			if rolelevel < lg:
				levelGroup = lg
			if not self.damage_ladder.has_key(lg):
				self.damage_ladder[lg] = []
			else:			
				if roleid in self.damage_ladder[lg]:
					self.damage_ladder[lg].remove(roleid)
			
		damage_position = -1
		for (i, rid) in enumerate(self.damage_ladder[levelGroup]):
			if self.user[rid]['damage'] < damage:
				damage_position = i
		if damage_position < 0 and (len(self.damage_ladder[levelGroup]) < gameConf['infection_ladder_max_size']):
			self.damage_ladder[levelGroup].append(roleid)
		elif damage_position >=0:
			self.damage_ladder[levelGroup].insert(damage_position, roleid)
			
	def update_prestige(self, roleid, now):
		"""
		更新声望
		"""
		if not is_same_day(self.user[roleid]['last_hit_time'], now):
			self.user[roleid]['prestige'] = 0
			self.user[roleid]['prestige_score'] = 0
						
	def call_relief(self, roleid, friend):
		"""
		招唤援军
		"""
		if not self.battle.has_key(roleid):
			return {'msg': 'infection_battle_not_exist'}
							
		if not self.battle[roleid]:
			return {'msg': 'infection_battle_not_exist'}
				
		now = currentTime()		
		gameConf = config.getConfig('game')		
		battle = self.battle[roleid][-1]
		if infection_arena.battle_is_finish(battle, now, gameConf):
			return {'msg': 'infection_battle_finish'}		
				
		for f in friend:
			if not self.user.has_key(f[0]):
				self.user[f[0]] = infection_arena.make_user(f[1])
			reliefBattle = infection_arena.make_relief(battle)			
			self.user[f[0]]['infection_list'].append(reliefBattle)
		self.save()
		return {}
	
	def get_infection_battle(self, roleid):
		"""
		得到援军
		"""
		if not self.user.has_key(roleid):
			return {'msg': 'infection_not_exist'}
				
		now = currentTime()		
		gameConf = config.getConfig('game')
		
		self.update_battle(now, gameConf)
		
		data = {}
		data['battle'] = []
		
		for inf in self.user[roleid]['infection_list']:
			battleRoleid = inf['roleid']
			b = {}
			if self.battle.has_key(battleRoleid):
				for battle in self.battle[battleRoleid]:					
					if battle['create_time'] == inf['create_time']:
						b['monster'] = battle['monster']
						b['create_time'] = battle['create_time']
						b['roleid'] = battle['roleid']
						b['rolename'] = battle['rolename']
						b['quality'] = battle['quality']
						b['level'] = battle['level']
			if not b:
				b['total_hp'] = 0
				b['create_time'] = 0
				b['roleid'] = inf['roleid']
				b['rolename'] = inf['rolename']
				b['quality'] = inf['quality']
				b['level'] = inf['level']
			data['battle'].append(b)					
						
		return data
						
	def get_battle_award(self, roleid, battleRoleid, create_time):
		"""
		得到战斗奖励
		"""
			
		if not self.battle.has_key(battleRoleid):
			return {'msg': 'infection_battle_not_exist'}
		
		if not self.battle[battleRoleid]:
			return {'msg': 'infection_battle_not_exist'}
		
		now = currentTime()		
		gameConf = config.getConfig('game')		
		self.update_battle(now, gameConf)				
		battle = {}
		for  b in self.battle[battleRoleid]:
			if b['create_time'] == create_time:
				battle = b
				break
		if not battle:
			return {'msg': 'infection_battle_not_exist'}		
				
		if infection_arena.battle_total_hp(battle) > 0:
			return {'msg': 'infection_battle_not_finish'}
				
		callerDropid = ''
		lastHitDropid = ''
		hitDropid = ''
		
		quality = battle['quality']
		level = battle['level']
		
		infectionBattleConf = config.getConfig('infection_battle')		
		infectionBattleInfo = infectionBattleConf[str(quality)][level - 1]
		
		if battle['roleid'] == roleid:
			if (not battle.has_key('caller_award')) or ( not battle['caller_award']):				
				callerDropid = infectionBattleInfo['caller_dropid']
				battle['caller_award'] = {'roleid':roleid, 'dropid':callerDropid}
		
		if battle['last_hit'] == roleid:
			if (not battle.has_key('last_hit_award')) or ( not battle['last_hit_award']):				
				lastHitDropid = infectionBattleInfo['last_hit_dropid']
				battle['last_hit_award'] = {'roleid':roleid, 'dropid':lastHitDropid}
					
		if battle['user'].has_key(roleid):
			if not battle['user'][roleid].has_key('hit_award'):
				hitDropid = infectionBattleInfo['hit_dropid']
				battle['user'][roleid]['hit_award'] = {'roleid':roleid, 'dropid':hitDropid}
					
		if (not callerDropid) or (not lastHitDropid) or (not hitDropid):
			return {'msg': 'infection_battle_no_award'}
					
		self.save()
		data = {}
		if callerDropid:
			data['call_dropid'] = callerDropid
		if lastHitDropid:
			data['last_hit_dropid'] = lastHitDropid
		if hitDropid:
			data['hit_dropid'] = hitDropid			
		return data
		
	def get_prestige_award(self, roleid, rolelevel):
		"""
		得到声望奖励
		"""
		infectionPrestigePriceConf = config.getConfig('infection_prestige_price')
		gameConf = config.getConfig('game')		
		
		levelGroup = gameConf['infection_ladder_level_group'][-1]
		for lg in gameConf['infection_ladder_level_group']:
			if rolelevel < lg:
				levelGroup = lg
				break
		infectionPrestigePriceInfo = infectionPrestigePriceConf[str(levelGroup)]
		
		last_award_prestige_score = self.user[roleid]['last_award_prestige_score']
		prestige_score = self.user[roleid]['prestige_score']
		
		award = []
		next_awrd_score = last_award_prestige_score
		for key in infectionPrestigePriceInfo:
			pp = int(key)
			if pp > last_award_prestige_score and pp <= prestige_score:
				award.append(key)
				if next_awrd_score < pp:
					next_awrd_score = pp
					
		self.user[roleid]['last_award_prestige_score'] = next_awrd_score
		
		data = {}
		data['award'] = award		
		
		return data	
				
	def update_battle(self, now, gameConf):		
		"""
		更新战斗
		"""
		if is_same_day(self.last_update_time, now):
			return
	
		email.send_ladder_email(self.damage_ladder, '4')
		email.send_ladder_email(self.prestige_ladder, '4')
		for roleid in self.battle.keys():
			battleRemoveList = []
			for battle in self.battle[roleid]:
				quality = battle['quality']
				if infection_arena.battle_is_escape(battle, now, gameConf):					
					if not is_same_day(battle['create_time'] + gameConf['infection_quality'][quality]['escape_time'], now):
						battleRemoveList.append(battle)
				elif infection_arena.battle_is_clear(battle):
					hit_time = battle['user'][battle['last_hit']]['last_hit_time']
					if not is_same_day(hit_time, now):
						battleRemoveList.append(battle)						
			for rb in battleRemoveList:
				self.battle[roleid].remove(rb)			
			if not self.battle[roleid]:
				del self.battle[roleid]
		self.last_update_time = now
					
	def prestige_ladder_list(self, rolelevel):
		"""
		声望排行榜
		"""
		gameConf = config.getConfig('game')
		
		levelGroup = gameConf['infection_ladder_level_group'][-1]
		for lg in gameConf['infection_ladder_level_group']:
			if rolelevel < lg:
				levelGroup = lg
				break
		
		data = {}
		data['prestige_ladder'] = []		
		for (i, roleid) in enumerate(self.prestige_ladder[str(levelGroup)]):
			item = {}
			item['position'] = i
			item['name'] = self.user[roleid]['name']
			item['prestige'] = self.user[roleid]['prestige']
			data['prestige_ladder'].append(item)			
		return data
	
	def damdage_ladder_list(self, rolelevel):
		"""
		伤害排行榜
		"""
		gameConf = config.getConfig('game')		
		levelGroup = gameConf['infection_ladder_level_group'][-1]
		for lg in gameConf['infection_ladder_level_group']:
			if rolelevel < lg:
				levelGroup = lg			
		
		data = {}
		data['damdage_ladder'] = []
		for (i, roleid) in enumerate(self.damage_ladder[str(levelGroup)]):
			item = {}
			item['position'] = i
			item['name'] = self.user[roleid]['name']
			item['prestige'] = self.user[roleid]['prestige']
			data['damdage_ladder'].append(item)
			
		return data
		
	def user_info(self, roleid):
		"""
		玩家信息
		"""
		if self.user.has_key(roleid):			
			data = {}
			data['prestige'] = self.user[roleid]['prestige']
			data['prestige_score'] = self.user[roleid]['prestige_score']			
			data['prestige_ladder_position'] = -1
			if roleid in self.prestige_ladder:
				data['prestige_ladder_position'] = self.prestige_ladder.index(roleid)
			return data
		else:
			data = {}
			data['prestige'] = 0
			data['prestige_score'] = 0
			data['prestige_ladder_position'] = -1
			return data
			
	def breset_prestige_score(self, roleid):
		"""
		声望分数
		"""
		if not self.user.has_key(roleid):
			return {'prestige_score':0}				
		self.user[roleid]['prestige_score'] = 0		
		return {'prestige_score':0}