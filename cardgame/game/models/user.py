#coding:utf-8
#!/usr/bin/env python

from gclib.user import user as gcuser
from game.models.dungeon import dungeon
from game.models.inventory import inventory
from game.models.network import network
from game.models.almanac import almanac
from gclib.utility import currentTime, retrieval_object, is_expire
from game.utility.config import config
from game.models.massyell import massyell
from game.routine.luckycat import luckycat
from game.routine.garcha import garcha
from game.routine.educate import educate
from game.routine.stone import stone


class user(gcuser):
	
	def __init__(self):
		gcuser.__init__(self)
		self.id = 0
		self.roleid = 0
		self.name = ''
		self.level = 0
		self.stamina = 0
		self.gem = 0
		self.gold = 0
		self.exp = 0
		self.vip = 0		
		self.stamina_last_recover = currentTime()
		self.last_card_no = 0
		self.leader = ''		
		self.last_login = currentTime()
		self.dun = None
		self.inv = None
		self.network = None
		self.almanac = None
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
		self.luckycat = {}
		self.educate = educate.make()
		self.trp = 0
		self.stv = stone.make_stv()
		self.stv_gem = stone.make_stv()
		
	
	def init(self, acc):
		gcuser.init(self, acc)
		self.id = acc.roleid
		self.roleid = acc.roleid
		self.name = acc.nickname
		self.level = 1
		self.stamina = 100				
		self.vip = 0
		self.stamina_last_recover = currentTime()
		self.last_card_no = 0

	
	def getData(self):	
		data = {}
		data['name'] = self.name
		data['level'] = self.level
		data['stamina'] = self.stamina
		data['gem'] = self.gem
		data['gold'] = self.gold
		data['exp'] = self.exp
		data['vip'] = self.vip
		data['stamina_last_recover'] = self.stamina_last_recover
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
		return data
		
	def getClientData(self):
		usrData = {}
		usrData['roleid'] = self.roleid
		usrData['name'] = self.name
		usrData['level'] = self.level
		usrData['stamina'] = self.stamina
		usrData['gem'] = self.gem
		usrData['gold'] = self.gold
		usrData['exp'] = self.exp
		usrData['vip'] = self.vip
		usrData['stamina_last_recover_before'] = currentTime() - self.stamina_last_recover		
		usrData['avatar_id'] = self.avatar_id
		#if self.train_prd:
			#usrData['train_prd'] = self.train_prd		
		usrData['equipment_strength_cooldown'] = self.equipment_strength_cooldown
		usrData['fatigue_last_time'] = self.fatigue_last_time
		usrData['equipment_strength_last_time'] = self.equipment_strength_last_time
		usrData['trp'] = self.trp
		usrData['stv'] = self.stv
		data = {}
		data['user'] = usrData
		gameConf = config.getConfig('game')
		if self.luckycat:
			data['luckycat'] = luckycat.getClientData(self, gameConf)
		data['educate'] = educate.getClientData(self, gameConf)
		return data
		
		
	def getFriendData(self):
		data = {}
		inv = self.getInventory()
		data['roleid'] = self.roleid
		data['name'] = self.name
		data['level'] = self.level		
		data['last_login'] = self.last_login
		data['create_time'] = currentTime()
		data['avatar_id'] = self.avatar_id
		data['luckycat_level'] = self.luckycat['level']
		teamCardid = []
		if self.team[0]:
			teamCardid.append(inv.getCard(self.team[0])['cardid'])
		if self.team[1]:
			teamCardid.append(inv.getCard(self.team[1])['cardid'])
		if self.team[2]:
			teamCardid.append(inv.getCard(self.team[2])['cardid'])
		if self.team[3]:
			teamCardid.append(inv.getCard(self.team[3])['cardid'])
		if self.team[4]:
			teamCardid.append(inv.getCard(self.team[4])['cardid'])
		if self.team[5]:
			teamCardid.append(inv.getCard(self.team[5])['cardid'])		
		data['member'] = teamCardid
		return data
		
	def getLoginData(self):
		data = {}
		self.updateStamina()
		data.update(self.getClientData())
		dun = self.getDungeon()
		data['dungeon'] = dun.getClientData()
		inv = self.getInventory()
		data.update(inv.getClientData())		
		nw = self.getNetwork()
		data.update(nw.getClientData())
		al = self.getAlmanac()
		data.update(al.getClientData())
		return data
		
	def load(self, roleid, data):
		gcuser.load(self, roleid, data)
		self.name = data['name']
		self.level = data['level']
		self.stamina = data['stamina']
		self.gem = data['gem']
		self.gold = data['gold']
		self.exp = data['exp']
		self.vip = data['vip']		
		self.stamina_last_recover = data['stamina_last_recover']		
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
		self.luckycat = data['luckycat']
		self.trp = data['trp']
		self.stv = data['stv']
		self.stv_gem = data['stv_gem']
		self.educate = data['educate']
			 		
	def getCardNo(self):
		self.last_card_no = self.last_card_no + 1
		return self.last_card_no		
	
	@retrieval_object
	def getDungeon(self):
		if self.dun != None:
			return self.dun
			
		dun = dungeon.get(self.id)
		if dun == None:	
			dun = dungeon()
			dun.init()
			dun.install(self.id)
		dun.user = self
		self.dun = dun
		return self.dun
	
	@retrieval_object
	def getInventory(self):
		if self.inv != None:
			return self.inv		
		inv = inventory.get(self.id)
		if inv == None:
			inv = inventory()
			inv.init()
			inv.install(self.id)
		inv.user = self
		self.inv = inv
		return self.inv
		
	@retrieval_object
	def getNetwork(self):
		if self.network != None:
			return self.network
		nt = network.get(self.id)
		if nt == None:
			nt = network()
			nt.init()
			nt.install(self.id)
		nt.user = self
		self.network = nt
		return self.network
	
	@retrieval_object
	def getAlmanac(self):
		if self.almanac != None:
			return self.almanac
		al = almanac.get(self.id)
		if al == None:
			al = almanac()
			al.init()
			al.install(self.id)
		al.user = self
		self.almanac = al
		return self.almanac
	
	def updateStamina(self):
		"""
		ckeck and do if stamina recover.
		"""
		maxStamina = config.getMaxStamina(self.level)
		stamina_recover_before = currentTime() - self.stamina_last_recover
		stamina_recove_interval = config.getConfig('game')['statmina_recove_interval']
		if maxStamina > self.stamina and stamina_recover_before > stamina_recove_interval:
			point = stamina_recover_before // stamina_recove_interval
			self.stamina_last_recover += point * stamina_recove_interval
			self.stamina += point
			if self.stamina > maxStamina:
				self.stamina = maxStamina
				
	def gainExp(self, exp):
		"""
		gain exp
		"""
		self.exp = self.exp + exp
		levelConf = config.getConfig('level')
		isLevelup = False
		while self.exp > levelConf[self.level - 1]['levelExp']:
			self.exp = self.exp - levelConf[self.level - 1]['levelExp']			
			self.level = self.level + 1
			isLevelup = True
		if isLevelup:
			self.onLevelup()
			
	def update(self):
		return
		
	def onInit(self):
		self.onLevelup()		

	def costStamina(self, point):
		maxStamina = config.getMaxStamina(sefl.level)
		if maxStamina == self.stamina:
			self.stamina_last_recover = currentTime()
		self.stamina -= point
			
	def updateToFriend(self):
		for key in self.friends:
			friend = user.get(key)
			friend.addFreind(self)
			friend.save()
	
	def onLogin(self):
		gameConf = config.getConfig('game')
		educate.update_exp(self, gameConf)
		
	def onLevelup(self):
		gameConf = config.getConfig('game')
		if not self.luckycat:
			if gameConf['luckycat_open_level'] <= self.level:
				self.luckycat = luckycat.make()
				self.notify['luckycat_notify'] = self.luckycat				
		nw = self.getNetwork()
		nw.updateFriendData()
		educate.levelup_update(self, gameConf)		
	
	def updateFatigue(self):
		gameConf = config.getConfig('game')
		if is_expire(gameConf['fatigue_reset_time'], self.fatigue):
			self.fatigue = 0
			fatigue_last_time = currentTime()

	def updateEquipmentStrengthCooldown(self):
		now = currentTime()
		elapse = now - self.equipment_strength_last_time
		self.equipment_strength_cooldown = self.equipment_strength_cooldown - elapse
		if self.equipment_strength_cooldown < 0:
			self.equipment_strength_cooldown = 0			

	def yell_listen(self):		
		ms = massyell.get(0)
		yells = ms.listen(self.yell_hear_id)
		self.yell_hear_id = ms.sequenceid
		if yells:			
			return {'yell':ms.listen()}
		return {}
		