#coding:utf-8
#!/usr/bin/env python

import random
from gclib.utility import is_same_day, currentTime
from gclib.json import json
from gclib.curl import curl
from game.utility.config import config
from game.routine.drop import drop

from cardgame.settings import ARENE_SERVER, SIGLE_SERVER


class tower:
		
	@staticmethod
	def make():
		"""
		制做
		"""
		return {'tiems':0, 'last_update':0, 'record':[], 'current':{}, 'floor_score':[], 'floor_point':[], 'max_floor':0, 'max_point':0, 'last_max_floor':0, 'last_max_point':0, 'ladder_position':0, 'ladder_rank_level':0}

	@staticmethod			
	def make_data():
		"""
		制做当前数据
		"""
		return {'floor':0, 'point':0, 'energy':0, 'score':0, 'strength':0, 'intelligence':0, 'artifice':0}
				
	@staticmethod
	def getClientData(usr):
		"""
		得到client data
		"""
		now = currentTime()
		tower.dayUpdate(usr, now)		
		gameConf = config.getConfig('game')
		data = {}
		
		data['tower_floor'] = -1	
		if usr.tower['current']:
			data['tower_floor'] = usr.tower['current']['floor']
			data['tower_point'] = usr.tower['current']['point']
			data['tower_energy'] = usr.tower['current']['energy']
			data['tower_strength'] = usr.tower['current']['strength']
			data['tower_intelligence'] = usr.tower['current']['intelligence']
			data['tower_artifice'] = usr.tower['current']['artifice']
		else:			
			data['tower_point'] = 0
			data['tower_energy'] = 0
			data['tower_strength'] = 0
			data['tower_intelligence'] = 0
			data['tower_artifice'] = 0
		if usr.tower.has_key('ladder_position'):
			data['tower_ladder_position'] = usr.tower['ladder_position']
		else:
			data['tower_ladder_position'] = -1
			
			
		if (not usr.tower.has_key('ladder_position') or usr.tower['ladder_position'] > gameConf['tower_no_markup_ladder_position']) and usr.tower['max_floor']:
			towerMarkupConf = config.getConfig('tower_markup')
			data['tower_markup'] = towerMarkupConf[usr.tower['max_floor']]
			
		data['tower_max_point'] = usr.tower['max_point']
		data['tower_max_floor'] = usr.tower['max_floor']
		data['tower_last_max_floor'] = usr.tower['last_max_floor']
		#data['tower_last_max_point'] = usr.tower['last_max_point']
		
		data['tower_times'] = tower.times(usr, gameConf)
		if usr.tower['current'].has_key('enhance'):
			data['tower_enhance'] = usr.tower['current']['enhance']
		else:
			data['tower_enhance'] = []
				
		return data
			
	@staticmethod
	def start(usr, markup):
		"""
		开始
		"""
		if usr.tower['current']:
			return {'msg':'tower_not_finished'}
				
		gameConf = config.getConfig('game')
		
		if gameConf['tower_times'] - len(usr.tower['record']) <= 0:
			return {'msg':'tower_max_times'}
		
		usr.tower['current'] = tower.make_data()
		markup = int(markup)
		
		tower.do_markup(usr, markup)		
		usr.save()
		
		data = {}
		data['tower_point'] = usr.tower['current']['point']
		data['tower_energy'] = usr.tower['current']['energy']
		data['tower_strength'] = usr.tower['current']['strength']
		data['tower_intelligence'] = usr.tower['current']['intelligence']
		data['tower_artifice'] = usr.tower['current']['artifice']
		data['tower_times'] = tower.times(usr, gameConf)
		data['tower_floor'] = 0

			
		return data
		
	@staticmethod
	def beat(usr, difficulty, star, dp, ehc):
		"""
		战胜
		"""
		if not usr.tower['current']:
			return {'msg':'tower_not_start'}
				
		if usr.tower['current'].has_key('enhance') and (ehc == -1):
			return {'msg':'tower_enhance_required'}
				
		gameConf = config.getConfig('game')
		towerAwardConf = config.getConfig('tower_award')
		towerMonster = config.getConfig('tower_monster')
						
		usr.tower['current']['point'] = usr.tower['current']['point'] + star * difficulty
		usr.tower['current']['energy'] = usr.tower['current']['energy'] + star * difficulty
		usr.tower['current']['score'] = usr.tower['current']['score'] + star * difficulty		
		usr.tower['current']['floor'] = usr.tower['current']['floor'] + 1
		
		if usr.tower['max_point'] < usr.tower['current']['point']:
			usr.tower['max_point'] = usr.tower['current']['point']
		
		while len(usr.tower['floor_score']) < usr.tower['current']['floor']:
			usr.tower['floor_score'].append(0)
		while len(usr.tower['floor_point']) < usr.tower['current']['floor']:
			usr.tower['floor_point'].append(0)
				
		newPoint = False
		if usr.tower['floor_point'][usr.tower['current']['floor'] - 1] < usr.tower['current']['point']:
			newPoint = True			
		
		newScore = False
		if usr.tower['floor_score'][usr.tower['current']['floor'] - 1] < usr.tower['current']['score']:
			newScore = True
		print usr.tower['floor_score'][usr.tower['current']['floor'] - 1], usr.tower['current']['score']
		
		data = {}		
					
		if ehc != -1:
			if not usr.tower['current'].has_key('enhance'):
				return {'msg':'tower_enhance_not_exsit'}
			tower.do_enhance(usr, ehc)
				
		enhance = []
		if usr.tower['current']['floor'] % gameConf['tower_enhance_interval_floor'] == 0:
			enhance = tower.make_enhance_list()
			usr.tower['current']['enhance'] = enhance
		
		
			
		if usr.tower['current']['floor'] % gameConf['tower_award_interval_floor'] == 0:
			towerAwardInfo = towerAwardConf[str(usr.tower['current']['floor'])]
			if newPoint:
				awd = {}
				awd = drop.open(usr, towerAwardInfo[1], awd)
				data = drop.makeData(awd, data,'top_drop')
				usr.tower['floor_point'][usr.tower['current']['floor'] - 1] = usr.tower['current']['point']
			if newScore:				
				if usr.tower['current']['score'] > 45:
					awd = {}
					awd = drop.open(usr, towerAwardInfo[3], awd)
					data = drop.makeData(awd, data, 'record_drop')
				if usr.tower['current']['score'] > 30:
					awd = {}
					awd = drop.open(usr, towerAwardInfo[2], awd)
					data = drop.makeData(awd, data, 'record_drop')
				usr.tower['floor_score'][usr.tower['current']['floor'] - 1] = usr.tower['current']['score']
			usr.tower['current']['score'] = 0

		if usr.tower['max_floor'] < usr.tower['current']['floor']:
			 usr.tower['max_floor'] = usr.tower['current']['floor']				

		if dp:
			awd = {}
			awd = drop.open(usr, towerMonster[usr.tower['current']['floor']]['dropid'], awd)
			data = drop.makeData(awd, data, 'random_drop')		
		
		usr.save()
		if enhance:
			data['tower_enhance'] = enhance
		data['tower_point'] = usr.tower['current']['point']
		data['tower_energy'] = usr.tower['current']['energy']
		data['tower_strength'] = usr.tower['current']['strength']
		data['tower_intelligence'] = usr.tower['current']['intelligence']
		data['tower_artifice'] = usr.tower['current']['artifice']
		data['tower_floor'] = usr.tower['current']['floor']
		data['tower_max_floor'] = usr.tower['max_floor']
		data['tower_max_point'] = usr.tower['max_point']
		return data		
		
	@staticmethod
	def do_enhance(usr, ehc, gameConf):
		"""
		加强属性
		"""
		
		
			
		point = 0
		if ehc == 0:
			usr.tower['current']['strength'] = usr.tower['current']['strength'] + usr.tower['current']['enhance'][0]
			point = usr.tower['current']['enhance'][0]
		elif ehc == 1:
			usr.tower['current']['intelligence'] = usr.tower['current']['intelligence'] + usr.tower['current']['enhance'][1]
			point = usr.tower['current']['enhance'][1]
		elif ehc == 2:
			usr.tower['current']['artifice'] = usr.tower['current']['artifice'] + usr.tower['current']['enhance'][2]
			point = usr.tower['current']['enhance'][2]
		del usr.tower['current']['enhance']
		
		for item in gameConf['tower_enhance_probability']:
			if item['point'] == point:
				usr.tower['current']['point'] = usr.tower['current']['point'] - point
		
	@staticmethod
	def do_markup(usr, mkp):
		"""
		加强属性
		"""
		if mkp == 0:
			return
		if usr.tower['max_floor'] == 0:
			return
		
		towerMarkupConf = config.getConfig('tower_markup')
		markup = towerMarkupConf[usr.tower['max_floor']]
		
		if mkp == 'strength':
			usr.tower['current']['strength'] = usr.tower['current']['strength'] + usr.tower['last_max_floor']
		if mkp == 'intelligence':
			usr.tower['current']['intelligence'] = usr.tower['current']['intelligence'] + usr.tower['last_max_floor']
		if mkp == 'artifice':
			usr.tower['current']['artifice']= usr.tower['current']['artifice'] + usr.tower['last_max_floor']
		
	@staticmethod
	def fail(usr):
		"""
		爬塔失败
		"""
		if not usr.tower['current']:
			return {'msg':'tower_not_start'}		
				
		res = tower.stand(usr)
		if usr.tower['max_floor'] < usr.tower['current']['floor']:
			 usr.tower['max_floor'] = usr.tower['current']['floor']
		usr.tower['record'].append(usr.tower['current'])
		usr.tower['current'] = {}
		usr.save()		
		
		if not res.has_key('msg'):
			if usr.tower['ladder_position'] < res['position']:
				usr.tower['ladder_position'] = res['position']
			if usr.tower['ladder_rank_level'] < res['rank_level']:
				usr.tower['ladder_rank_level'] = res['rank_level']		
		
		return {'tower_max_floor': usr.tower['max_floor'], 'tower_max_point':usr.tower['max_point'], 'tower_times': usr.tower['times']}	
		
	@staticmethod
	def make_enhance_list():
		"""
		制做强化列表
		"""
		
		point = []
		for i in range(3):			
			point.extend(random.sample([2, 10, 20], 1))
		
		if 2 not in point:
			idx = random.randint(0, 2)
			point[idx] = 2
		return point		
		
	@staticmethod
	def current_floor(usr):
		"""
		当前层数
		"""
		if usr.tower['current']:
			return usr.tower['current']['floor']
		return 0
		
	@staticmethod
	def dayUpdate(usr, now):
		"""
		每日更新
		"""
		if not is_same_day(usr.tower['last_update'], now):
			if usr.tower['current']:
				usr.tower['record'].append(usr.tower['current'])
			usr.tower['max_floor'] = 0
			floor = 0
			point = 0
			for rd in usr.tower['record']:
				if rd['floor'] > floor:
					usr.tower['last_max_floor'] = rd['floor']
				if rd['point'] > point:
					usr.tower['last_max_point'] = rd['point']
			usr.tower['current'] = {}
			usr.tower['record'] = []				
			usr.tower['times'] = 0
			usr.tower['max_floor'] = 0
			usr.tower['last_update'] = now
			usr.tower['floor_point'] = []
			
	@staticmethod
	def stand(usr):
		"""
		加入排行榜
		"""
		if SIGLE_SERVER:
			from arenarank.routine.tower import tower as towerR
			return towerR.stand(str(usr.roleid), usr.name, usr.level, usr.tower['current']['point'], tower.current_floor(usr))
		else: 
			return json.loads(curl.url(ARENE_SERVER +  '/arena/tower_stand/', None, {'roleid': usr.roleid, 'level': usr.level, 'point':  usr.tower['current']['point'], 'name':usr.name, 'floor':tower.current_floor(usr)}))
			
	@staticmethod
	def show_ladder(usr):
		"""
		显示楼梯
		"""
		if SIGLE_SERVER:
			from arenarank.routine.tower import tower as towerR
			return {'tower_ladder':towerR.show_ladder()}
		else:
			return {'tower_ladder':json.loads(curl.url(ARENE_SERVER +  '/arena/tower_show/', None, {'roleid': usr.roleid, 'level': usr.level}))}
			
	@staticmethod
	def times(usr, gameConf):
		"""
		剩余次数
		"""
		towerTimes = gameConf['tower_times'] - len(usr.tower['record'])
		if usr.tower['current']:
			towerTimes = towerTimes - 1
		return towerTimes
		