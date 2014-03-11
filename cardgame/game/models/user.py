#coding:utf-8
#!/usr/bin/env python

from gclib.user import user as gcuser
from gclib.cache import cache
#from game.models.account import account
from game.models.dungeon import dungeon
from game.models.inventory import inventory
from game.models.network import network
from game.models.almanac import almanac
from game.models.quest import quest
from gclib.utility import currentTime, retrieval_object, is_expire
from game.utility.config import config
from game.models.massyell import massyell
from game.routine.luckycat import luckycat
from game.routine.garcha import garcha
from game.routine.educate import educate
from game.routine.stone import stone
from game.routine.signin import signin
from game.routine.levelup import levelup
from game.routine.arena import arena
from game.routine.tower import tower
from game.routine.medal import medal
from game.routine.pet import pet
from game.routine.practice import practice
from game.routine.pvp import pvp
from game.routine.slotmachine import slotmachine
from game.routine.vip import vip
from game.routine.invite import invite
from game.routine.infection import infection
from game.routine.explore import explore
from game.routine.arena import arena



class user(gcuser):
	
	def __init__(self):
		"""
		构造函数
		"""
		gcuser.__init__(self)
		self.id = 0
		self.roleid = 0
		self.name = ''
		self.level = 0
		self.stamina = 0
		self.gem = 0
		self.gold = 0
		self.exp = 0
		self.sp = 0
		self.stamina_last_recover = 0
		self.sp_last_recover = 0
		self.last_card_no = 0
		self.leader = ''		
		self.last_login = currentTime()
		self.dun = None
		self.inv = None
		self.network = None
		self.almanac = None
		self.quest = None
		self.garcha = garcha.make()
		self.notify = {}
		self.gender = 'male'
		self.equipment_strength_cooldown = 0
		self.equipment_strength_last_time = 0
		self.train_prd = {}
		self.fatigue = 0
		self.fatigue_last_time = 0		
		self.yell_hear_id = 0
		self.extend_columns.append({'name' :'avatar_id', 'value':''})
		self.luckycat = luckycat.make()
		self.educate = educate.make()
		self.signin = signin.make()
		self.levelup = levelup.make()
		self.trp = 0
		self.stv = stone.make_stv()
		self.stv_gem = stone.make_stv()
		self.arena = arena.make()
		self.avatar = ''
		self.longitude = 0.0
		self.latitude = 0.0
		self.tower = tower.make()
		self.medal = medal.make()
		self.practice = practice.make()
		self.slotmachine = slotmachine.make()
		self.vip = vip.make()
		self.invite = invite.make()
		self.infection = infection.make()
		self.born_card = pet.make_born_card()
		self.ip = 0
		self.ip_last_recover = 0
		self.explore = explore.make()
		
	
	def init(self, acc = None):
		"""
		初始化
		"""
		gcuser.init(self, acc)
		if acc:
			self.id = acc.roleid
			self.roleid = acc.roleid
			self.name = acc.nickname
			self.account = acc
		self.level = 1		
		levelConf = config.getConfig('level')		
		self.stamina = levelConf[0]['stamina']
		self.sp = levelConf[0]['sp']
		now = currentTime()
		self.stamina_last_recover = now
		self.sp_last_recover = now
		self.last_card_no = 0
		self.invite['make_time'] = now
		gameConf = config.getConfig('game')
		self.ip = gameConf['infection_point_max']
		self.ip_last_recover = now
		
	def install(self, roleid):
		"""
		安装
		"""
		gcuser.install(self, roleid)
	
	def getData(self):	
		"""
		得到数据
		"""
		data = gcuser.getData(self)
		data['name'] = self.name
		data['level'] = self.level
		data['stamina'] = self.stamina
		data['gem'] = self.gem
		data['gold'] = self.gold
		data['exp'] = self.exp
		data['vip'] = self.vip
		data['sp'] = self.sp
		data['gender'] = self.gender
		data['stamina_last_recover'] = self.stamina_last_recover
		data['sp_last_recover'] = self.sp_last_recover
		data['last_card_no'] = self.last_card_no
		data['last_login'] = self.last_login		
		data['leader'] = self.leader
		data['last_login'] = self.last_login
		data['garcha'] = self.garcha
		data['notify'] = self.notify
		data['train_prd'] = self.train_prd
		data['equipment_strength_cooldown'] = self.equipment_strength_cooldown
		data['equipment_strength_last_time'] = self.equipment_strength_last_time
		data['fatigue'] = self.fatigue
		data['fatigue_last_time'] = self.fatigue_last_time
		data['yell_hear_id'] = self.yell_hear_id
		data['luckycat'] = self.luckycat
		data['educate'] = self.educate
		data['trp'] = self.trp
		data['stv'] = self.stv
		data['stv_gem'] = self.stv_gem
		data['arena'] = self.arena
		data['avatar'] = self.avatar
		data['signin'] = self.signin
		data['levelup'] = self.levelup
		data['longitude'] = self.longitude
		data['latitude'] = self.latitude
		data['tower'] = self.tower
		data['medal'] = self.medal
		data['practice'] = self.practice
		data['slotmachine'] = self.slotmachine
		data['vip'] = self.vip
		data['invite'] = self.invite
		data['infection'] = self.infection
		data['born_card'] = self.born_card
		data['ip'] = self.ip
		data['ip_last_recover'] = self.ip_last_recover
		data['explore'] = self.explore
		return data
		
	def load(self, roleid, data):
		"""
		加载
		"""
		gcuser.load(self, roleid, data)
		self.name = data['name']
		self.level = data['level']
		self.stamina = data['stamina']
		self.gem = data['gem']
		self.gold = data['gold']
		self.exp = data['exp']		
		self.gender = data['gender']
		self.stamina_last_recover = data['stamina_last_recover']
		self.sp_last_recover = data['sp_last_recover']
		self.last_card_no = data['last_card_no']		
		self.last_login = data['last_login']		
		self.leader = data['leader']		 
		self.notify = data['notify']		
		self.train_prd = data['train_prd']
		self.equipment_strength_cooldown = data['equipment_strength_cooldown']
		self.equipment_strength_last_time = data['equipment_strength_last_time']		
		self.fatigue = data['fatigue']
		self.fatigue_last_time = data['fatigue_last_time']
		self.yell_hear_id = data['yell_hear_id']
		self.luckycat = (data['luckycat'])
		self.trp = data['trp']
		self.sp = data['sp']
		self.stv = data['stv']
		self.garcha = (data['garcha'])
		self.stv_gem = data['stv_gem']
		self.educate = data['educate']
		self.arena = (data['arena'])
		self.avatar = data['avatar']
		self.signin = data['signin']
		self.levelup = data['levelup']
		self.longitude = data['longitude']
		self.latitude = data['latitude']
		self.tower = data['tower']
		self.medal = (data['medal'])
		self.practice = data['practice']
		self.slotmachine = data['slotmachine']
		self.vip = (data['vip'])
		self.invite = (data['invite'])
		self.infection = (data['infection'])
		self.born_card = (data['born_card'])				
		self.ip = data['ip']
		self.ip_last_recover = data['ip_last_recover']
		self.explore = data['explore']
		
	def getClientData(self):
		"""
		得到client data
		"""
		now = currentTime()
		usrData = {}
		usrData['roleid'] = self.roleid
		usrData['name'] = self.name
		usrData['level'] = self.level
		usrData['stamina'] = self.stamina
		usrData['gem'] = self.gem
		usrData['gold'] = self.gold
		usrData['sp'] = self.sp
		usrData['exp'] = int(self.exp)
		usrData['vip'] = self.vip
		usrData['gender'] = self.gender
		usrData['stamina_last_recover_before'] = now - self.stamina_last_recover		
		usrData['sp_last_recover_before'] = now - self.sp_last_recover		
		usrData['avatar_id'] = self.avatar_id
		#if self.train_prd:
			#usrData['train_prd'] = self.train_prd		
		usrData['equipment_strength_cooldown'] = self.equipment_strength_cooldown - (now - self.equipment_strength_last_time)
		if usrData['equipment_strength_cooldown'] < 0:
			usrData['equipment_strength_cooldown'] = 0
		usrData['fatigue_last_time'] = self.fatigue_last_time		
		usrData['trp'] = self.trp
		usrData['stv'] = self.stv
		usrData['arena_time'] = self.arena['times']
		usrData['arena_award'] = self.arena['rank_award']
		usrData['avatar'] = self.avatar
		data = {}
		data['user'] = usrData
		gameConf = config.getConfig('game')
		if self.luckycat:
			data['luckycat'] = luckycat.getClientData(self, gameConf)
		data['educate'] = educate.getClientData(self, gameConf)
		
		data['levelup'] = self.levelup['record']
		data['tower'] = tower.getClientData(self)
		data['medal'] = medal.getClientData(self, gameConf)
		data['practice'] = practice.getClientData(self)
		data['slotmachine'] = slotmachine.getClientData(self)		
		data['invite'] = invite.getClientData(self)
		#data['infection'] = infection.getClientData(self)
		data['born_card'] = (self.born_card['cardid'] != '')
		data['ip'] = self.ip
		data['ip_last_recover_before'] = now - self.ip_last_recover
		data['explore'] = explore.getClientData(self)
		return data
		
	def getNtInfoData(self):
		"""
		得到network 数据
		"""
		ntInfo = {}
		ntInfo['roleid'] = self.roleid
		ntInfo['name'] = self.name
		ntInfo['level'] = self.level
		ntInfo['sex'] = self.gender
		ntInfo['avatar_id'] = self.avatar_id		
		#ntInfo['last_login'] = self.last_login
		return ntInfo
		
		
	def getFriendData(self):
		"""
		得到好友数据
		"""
		data = {}
		inv = self.getInventory()
		data['roleid'] = self.roleid
		data['name'] = self.name
		data['level'] = self.level		
		data['last_login'] = self.last_login
		#data['create_time'] = currentTime()
		data['avatar_id'] = self.avatar_id
		if self.gender == 'male':
			data['sex'] = 1
		else:
			data['sex'] = 0		
		if self.luckycat:
			data['luckycat_level'] = self.luckycat['level']
		#teamCardid = []
		#if inv.team[0]:
		#	teamCardid.append(inv.getCard(inv.team[0])['cardid'])
		#if inv.team[1]:
		#	teamCardid.append(inv.getCard(inv.team[1])['cardid'])
		#if inv.team[2]:
		#	teamCardid.append(inv.getCard(inv.team[2])['cardid'])
		#if inv.team[3]:
		#	teamCardid.append(inv.getCard(inv.team[3])['cardid'])
		#if inv.team[4]:
		#	teamCardid.append(inv.getCard(inv.team[4])['cardid'])
		#if inv.team[5]:
		#	teamCardid.append(inv.getCard(inv.gteam[5])['cardid'])		
		#data['member'] = teamCardid
		return data
		
	def getBattleData(self):
		"""
		得到战斗数据
		"""		
		data = {}
		inv = self.getInventory()
		data['roleid'] = self.roleid
		data['level'] = self.level
		data['name'] = self.name
		#data['team'] = inv.team
		data['team_card'] = []
		for cid in inv.team:
			if cid:
				data['team_card'].append(inventory.getClientCard(inv.getCard(cid)))																											
			else:
				data['team_card'].append({})
		data['slot'] = inv.getSlots()
		data['st_slot'] = inv.getStSlots()
		data['sk_slot'] = inv.getSkSlots()
		return data
		
	def getLoginData(self, gameConf):
		"""
		得到登陆数据
		"""
		data = {}		
		self.updateStamina()
		self.updateSp()
		self.updateIp()
		data.update(self.getClientData())
		dun = self.getDungeon()
		data['dungeon'] = dun.getClientData()
		inv = self.getInventory()
		data.update(inv.getClientData())		
		nw = self.getNetwork()
		data.update(nw.getClientData())
		data['user']['charm'] = nw.charm
		data['user']['tuhao'] = nw.tuhao
		al = self.getAlmanac()
		data.update(al.getClientData())
		data.update(garcha.getClientData(self, gameConf))
		qt = self.getQuest()
		data.update(qt.getClientData())
		return data
		
	def getSceneData(self):
		"""
		得到场景数据
		"""
		data = {}
		data['name'] = self.name
		data['gender'] = self.gender
		data['roleid'] = self.roleid
		data['avatar'] = self.avatar
		return data
		
	def getAccount(self):		
		"""
		得到帐号
		"""
		return self.getAccountCls().get(self.accountid)		
		
	def getAccountCls(self):
		"""
		得到帐号类
		"""
		return __import__('game.models.account', globals(), locals(), ['account']).account
	

	def getCardNo(self):
		"""
		卡牌编号
		"""
		self.last_card_no = self.last_card_no + 1
		return self.last_card_no
			
	@retrieval_object
	def getDungeon(self):
		"""
		得到地下城
		"""
		if self.dun:
			return self.dun			
		dun = dungeon.get(self.id)
		if not dun:	
			dun = dungeon()
			dun.init()
			dun.install(self.id)
		dun.user = self
		self.dun = dun
		return self.dun
	
	@retrieval_object
	def getInventory(self):
		"""
		得到玩家背包
		"""
		if self.inv:
			return self.inv
		inv = inventory.get(self.id)
		if not inv:
			inv = inventory()
			inv.init()
			inv.install(self.id)
		inv.user = self
		self.inv = inv
		return self.inv
		
	@retrieval_object
	def getNetwork(self):
		"""
		得到人脉
		"""
		if self.network:
			return self.network
		nt = network.get(self.id)
		if not nt:
			nt = network()
			nt.init()
			nt.install(self.id)
		nt.user = self
		self.network = nt
		return self.network
	
	@retrieval_object
	def getAlmanac(self):
		"""
		得到图鉴
		"""
		if self.almanac:
			return self.almanac
		al = almanac.get(self.id)
		if not al:
			al = almanac()
			al.init()
			al.install(self.id)
		al.user = self
		self.almanac = al
		return self.almanac
		
	@retrieval_object
	def getQuest(self):
		"""
		得到任务
		"""
		if self.quest:
			return self.quest
		qt = quest.get(self.id)
		if not qt:
			qt = quest()
			qt.init()
			qt.install(self.id)
		qt.user = self
		self.quest = qt
		return self.quest
	
	def updateStamina(self):
		"""
		ckeck and do if stamina recover.
		"""
		maxStamina = config.getMaxStamina(self.level)
		stamina_recover_before = currentTime() - self.stamina_last_recover
		stamina_recove_interval = config.getConfig('game')['statmina_recover_interval']
		if stamina_recover_before > stamina_recove_interval:
			point = stamina_recover_before // stamina_recove_interval
			self.stamina_last_recover = self.stamina_last_recover + (point * stamina_recove_interval)
			self.stamina = self.stamina + point
			if self.stamina > maxStamina:
				self.stamina = maxStamina
				
	def updateSp(self):
		"""
		更新sp
		"""
		levelConf = config.getConfig('level')
		gameConf = config.getConfig('game')
		maxSp = levelConf[self.level - 1]['sp']
		sp_recover_before = currentTime() - self.sp_last_recover
		if sp_recover_before > gameConf['sp_recover_interval']:
			point = sp_recover_before // gameConf['sp_recover_interval']
			self.sp_last_recover = self.sp_last_recover + (point * gameConf['sp_recover_interval'])
			self.sp = self.sp + point
			if self.sp > maxSp:
				self.sp = maxSp	
				
	def updateIp(self):
		"""
		更新ip
		"""
		gameConf = config.getConfig('game')
		
		maxIp = gameConf['infection_point_max']
		ip_recover_before = currentTime() - self.ip_last_recover
		ip_recover_interval = gameConf['infection_point_recover_interval']
		if ip_recover_before > ip_recover_interval:
			point = ip_recover_before // ip_recover_interval
			self.ip_last_recover = self.ip_last_recover + (point * gameConf['infection_point_recover_interval'])
			self.ip = self.ip + point
			if self.ip > maxIp:
				self.ip = maxIp
				
	def gainExp(self, exp):
		"""
		gain exp
		"""
		if exp <= 0:
			return
		self.exp = self.exp + exp
		levelConf = config.getConfig('level')
		isLevelup = False
		while self.exp > levelConf[self.level]['levelExp'] - levelConf[self.level - 1]['levelExp']:
			self.exp = self.exp - (levelConf[self.level]['levelExp'] - levelConf[self.level - 1]['levelExp'])
			self.level = self.level + 1
			isLevelup = True
			explore.on_user_levelup(self)
		if isLevelup:
			self.onLevelup()
			
	def update(self):
		"""
		更新
		"""
		return
		
	def onInit(self):
		"""
		初始化
		"""
		inv = self.getInventory()
		tc = inv.addCard('pet10111_3')
		inv.addCard('pet10001_4')
		inv.addCard('pet10001_3')
		inv.addCard('pet10001_4')
		deq = []
		dst = []
		dsk = []
		inv.setTeam(tc['id'], '', '', '', '', '', deq, dst, dsk)
		inv.save()	
		self.onLevelup()		

	def chargeStamina(self, point):
		"""
		补充体力
		"""
		self.stamina = self.stamina + point
		levelConf = config.getConfig('level')
		if levelConf[self.level - 1]['stamina'] < self.stamina:
			levelConf[self.level - 1]['stamina'] = self.stamina	
	
	def costStamina(self, point):
		"""
		消费体力
		"""
		if self.stamina < point:
			return -1
		self.updateStamina()
		maxStamina = config.getMaxStamina(sefl.level)
		self.stamina = self.stamina - point
		if maxStamina > self.stamina:
			self.stamina_last_recover = currentTime()		
		return 0
		
	def costSp(self, point):
		"""
		消费sp
		"""
		if self.sp < point:
			return -1
		self.updateSp()
		levelConf = config.getConfig('level')
		maxSp = levelConf[self.level - 1]
		self.sp = self.sp - point
		if maxSp > self.sp:
			self.sp_last_recover = currentTime()		
		return 0
		
	def costIp(self, point):
		"""
		消费ip
		"""
		if self.ip < point:
			return -1
		self.updateIp()
		gameConf = config.getConfig('game')
		maxIp = gameConf['infection_point_recover_interval']
		self.ip = self.ip - point
		if maxIp > self.ip:
			self.ip_last_recover = currentTime()
		return 0		
			
	def updateToFriend(self):
		"""
		更新好友
		"""
		for key in self.friends:
			friend = user.get(key)
			friend.addFreind(self)
			friend.save()
	
	def onLogin(self):
		"""
		登陆时
		"""
		gcuser.onLogin(self)
		gameConf = config.getConfig('game')
		educate.update_exp(self, gameConf)
		data = signin.login(self)
		arena.arena_update(self)
		invite.onLogin(self)
		return data
		
	def onLevelup(self):
		"""
		升级时
		"""
		gameConf = config.getConfig('game')
		if not self.luckycat:
			if gameConf['luckycat_open_level'] <= self.level:
				self.luckycat = luckycat.make()
				#self.notify['luckycat_notify'] = self.luckycat				
		nw = self.getNetwork()
		nw.updateFriendData()
		educate.levelup_update(self, gameConf)
		qt = self.getQuest()
		qt.updateQuest(True)
		
		if self.level > gameConf['arena_level'] and not self.arena.has_key('stand'):
			arena.stand_ladder(self)
			self.arena['stand'] = 1
	
	def updateFatigue(self):
		"""
		更新体力
		"""
		gameConf = config.getConfig('game')
		if is_expire(gameConf['fatigue_reset_time'], self.fatigue):
			self.fatigue = 0
			fatigue_last_time = currentTime()

	def updateEquipmentStrengthCooldown(self):
		"""
		更新强化装备冷却时间
		"""
		now = currentTime()
		elapse = now - self.equipment_strength_last_time
		self.equipment_strength_cooldown = self.equipment_strength_cooldown - elapse
		if self.equipment_strength_cooldown < 0:
			self.equipment_strength_cooldown = 0			

	def yell_listen(self):
		"""
		收到世界聊天
		"""		
		ms = massyell.get(0)
		yells = ms.listen(self)
		self.yell_hear_id = ms.sequenceid
		if yells:			
			return {'yell_notify':yells}
		return {}
		
	def delete(self):
		"""
		删除
		"""
		gcuser.delete(self)
		
	def clear(self):
		"""
		清除
		"""
		self.getInventory().delete()
		self.getNetwork().delete()
		self.getQuest().delete()
		self.getDungeon().delete()
		self.getAlmanac().delete()
		self.delete()
		
	def pvpProperty(self):
		"""
		pvp属性
		"""
		
		inv = self.getInventory()
		
		petConf = config.getConfig('pet')
		equipmentConf = config.getConfig('equipment')
		stoneConf = config.getConfig('stone')
		
		ppAlmanacData = pvp.almanacPvpProperty(self)
		ppMedalData = pvp.almanacPvpProperty(self)
		ppPracticeData = pvp.practicePvpProperty(self)
				
		data = []
		for tid in inv.team:
			if tid:
				card = inv.getCard(tid)
				ppData = pvp.pvpPetProperty(self, card, petConf)								
				for equip in card['slot']:
					if equip:
						data1 = pvp.pvpEquipmentProperty(equip, equipmentConf)
						ppData = pvp.mergePvpProperty(ppData, data1)	
				
				for st in card['st_slot']:
					if st:
						data1 = pvp.pvpStoneProperty(st, stoneConf)
						ppData = pet.mergePvpProperty(ppData, data1)	
				ppLuckData = pvp.luckPvpProperty(self, card)
				ppData = pvp.mergePvpProperty(ppData, ppLuckData)
				ppData = pvp.mergePvpProperty(ppData, ppAlmanacData)
				ppData = pvp.mergePvpProperty(ppData, ppMedalData)
				ppData = pvp.mergePvpProperty(ppData, ppPracticeData)
				ppData['critical_level'] = self.practice['critical_level']
				ppData['tenacity_level'] = self.practice['tenacity_level']
				ppData['block_level'] = self.practice['block_level']
				ppData['wreck_level'] = self.practice['wreck_level']
				data.append(ppData)
			else:
				data.append({})
				
		
		return data
		
	def notify_gold(self):
		"""
		提示金币
		"""
		self.notify['gold'] = self.gold