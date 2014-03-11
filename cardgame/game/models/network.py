from gclib.object import object
from gclib.utility import currentTime, is_same_day
from game.utility.config import config
from game.models.massyell import massyell
from game.routine.drop import drop
from game.routine.gift import gift


class network(object):
	
	def init(self):
		pass
		
	
	def __init__(self):
		"""
		初始化
		"""
		object.__init__(self)
		self.message = {}
		self.mail = {}
		self.email = {}			
		self.gift = {}						#{roleid:'#depend'}
		self.jail = {}						#[{'roleid':'', 'name':'abc'}]
		self.friend = {}
		self.friend_request = {}
		self.request_list = {}
		self.blacklist = []
		self.sequenceid = 1
		self.nt_info = {}
		self.gift = {}
		self.tuhao = 0
		self.charm = 0
		self.send_gift_record = []
		self.receive_gift_record = []
		self.user = None
		
	def install(self, roleid):
		"""
		安装
		"""
		object.install(self, roleid)
		
	def getData(self):
		"""
		得到 data
		"""
		data = object.getData(self)
		data['friend'] = self.friend
		data['message'] = self.message
		data['mail'] = self.mail
		data['email'] = self.email
		data['friend_request'] = self.friend_request
		data['blacklist'] = self.blacklist
		data['sequenceid'] = self.sequenceid
		data['nt_info'] = self.nt_info
		data['request_list'] = self.request_list
		data['gift'] = self.gift
		data['tuhao'] = self.tuhao
		data['charm'] = self.charm
		data['send_gift_record'] = self.send_gift_record
		data['receive_gift_record'] = self.receive_gift_record
		return data			
		
	def getClientMailData(self):
		"""
		得到client mail data
		"""
		
		data = {}
		for roleid in self.mail:
			 m = {}
			 m['name'] = self.nt_info[roleid]['name']
			 m['level'] = self.nt_info[roleid]['level']
			 m['sex'] = self.nt_info[roleid]['sex']
			 m['avatar_id'] = self.nt_info[roleid]['avatar_id']
			 #m['last_login'] = self.nt_info[roleid]['last_login']
			 m['mail'] = self.mail[roleid]
			 data[roleid] = m
		return data
		
	
	def getClientData(self):	
		"""
		得到client data
		"""
		
		avatarmap = {}		
		for key in self.message:
			otherid = self.message[key]['roleid']
			if not avatarmap.has_key(otherid):
				usr = self.user.__class__.get(otherid)
				if usr:
					avatarmap[otherid] = usr.avatar_id
			self.message[key]['avatar_id'] = avatarmap[otherid]				
		data = {}
		data['friend'] = self.friend	
		data['message'] = self.message
		data['mail'] = self.getClientMailData()
		data['email'] = self.email
		data['friend_request'] = self.friend_request				
		data['send_gift_record'] = self.send_gift_record
		data['receive_gift_record'] = self.receive_gift_record
		#data['nt_info'] = self.nt_info
		return data			
		
	def load(self, roleid, data):
		"""
		加载
		"""
		object.load(self, roleid, data)
		self.friend = data['friend']
		self.message = data['message']
		self.mail = data['mail']
		self.email = data['email']
		self.sequenceid = data['sequenceid']
		self.nt_info = data['nt_info']
		self.request_list = data['request_list']
		self.friend_request = data['friend_request']
		self.gift = data['gift']
		self.tuhao = data['tuhao']
		self.charm = data['charm']
		self.send_gift_record = data['send_gift_record']
		self.receive_gift_record = data['receive_gift_record']
		
	def addFriendRequest(self, friend):
		"""
		添加好友请求
		"""
		
		friendRoleid = str(friend.roleid)
		if self.request_list.has_key(friendRoleid):
			if is_same_day(currentTime(), self.request_list[friendRoleid]):
				return {'msg':'friend_already_request'}
		self.request_list[friendRoleid] = currentTime()
		
		data = self.user.getFriendData()
		friendNw = friend.getNetwork()
		requestid = str(friendNw.sequenceid)
		friendNw.sequenceid = friendNw.sequenceid + 1
		data.update({'id':requestid})		
		friendNw.friend_request[requestid] = data		
		friendNw.save()
		if not friend.notify.has_key('notify_friend_request'):
			friend.notify['notify_friend_request'] = {}
		friend.notify['notify_friend_request'][requestid] = data
		friend.save()
		self.save()
		return data
		
	def addFriend(self, friend):
		"""
		添加好友
		"""
		data = friend.getFriendData()
		self.friend[str(friend.roleid)] =  data
		return data
				
	def deleteFriend(self, friend):
		"""
		删除好友
		"""
		if self.friend.has_key(friend.roleid):
			del self.friend[friend.roleid]
			self.save()
		else:
			return {'msg':'friend_not_exist'}
		otherNw = friend.getNetwork()
		selfroleid = str(self.roleid)
		if otherNw.friend.has_key(selfroleid):
			del otherNw.friend[str(selfroleid)]			
			otherNw.save()
			return {'friend_delete':friend.roleid}		
			
	def getFriend(self, friendRoleid):
		"""
		得到好友
		"""
		if self.friends.has_key(str(friendRoleid)):
			return friends[str(friendRoleid)]

	def sendMessage(self, toUser, msg):
		"""
		发送消息
		"""
		self.updateMessage()
		toUserNw = toUser.getNetwork()
		fromUserId = str(self.roleid)		
		requestid = str(toUserNw.sequenceid)
		toUserNw.sequenceid = toUserNw.sequenceid + 1
		msgData = self.user.getFriendData()		
		msgData.update({'message':msg, 'send_time': currentTime(), 'id':requestid})
		toUserNw.message[requestid] = msgData
		if not toUser.notify.has_key('notify_message'):
			toUser.notify['notify_message'] = {}
		toUser.notify['notify_message'][requestid] = msgData		
		toUser.save()
		toUserNw.save()
	
	def deleteMessage(self, messageid):
		"""
		删除消息
		"""		
		if self.message.has_key(messageid):
			del self.message[messageid]
			self.save()
	
	def updateMessage(self):
		"""
		更新消息
		"""
		now = currentTime()
		gameConf = config.getConfig('game')
		expire = gameConf['message_expiry_period']
		self.message = dict((k, v) for k,v in self.message.items() if (v['send_time'] + expire) > now)		
		
	def sendMail(self, toUser, mail):
		"""
		发送邮件
		"""
		toUserNw = toUser.getNetwork()					
		ntInfo = self.user.getNtInfoData()	
		requestid = str(toUserNw.sequenceid)
		toUserNw.sequenceid = toUserNw.sequenceid + 1
		fromUserId = str(self.user.roleid)
		msgData = {'mail':mail, 'send_time': currentTime(), 'id': str(requestid) + str(fromUserId), 'roleid':fromUserId}	
		if not toUserNw.mail.has_key(fromUserId):
			toUserNw.mail[fromUserId] = []
		toUserNw.mail[fromUserId].append(msgData)
		toUserNw.nt_info[fromUserId] = ntInfo
		if not toUser.notify.has_key('notify_mail'):
			toUser.notify['notify_mail'] = {}
		toUser.notify['notify_mail'][str(requestid) + str(fromUserId)] = dict({'new_mail':msgData}, **ntInfo)
		toUser.save()
		toUserNw.save()
				
		fromUser = self.user
		fromNw = self
		toNtInfo = toUser.getNtInfoData()
		toUserId = str(toUser.roleid)
		fromNw.nt_info[toUserId] = toNtInfo
		if not fromNw.mail.has_key(toUserId):
			fromNw.mail[toUserId] = []
		fromNw.mail[toUserId].append(msgData)
		if not fromUser.notify.has_key('notify_mail'):
			fromUser.notify['notify_mail'] = {}
		fromUser.notify['notify_mail'][str(requestid) + str(fromUserId)] = dict({'new_mail':msgData}, **toNtInfo)
		fromNw.save()
		fromUser.save()
		
	def deleteMail(self, friendid, mailid):		
		"""
		删除邮件
		"""
		if not self.mail.has_key(friendid):
			return {'msg':'mail_not_exist'}		
		self.mail[friendid] = filter(lambda x : x['id'] != mailid, self.mail[friendid])
		if not self.mail[friendid]:
			del self.mail[friendid]
			del self.nt_info[friendid]
		self.save()
		return {}
		
	def deleteFriendMail(self, friendid):
		"""
		删除好友的邮件
		"""
		if not self.mail.has_key(friendid):
			return {'msg':'mail_not_exist'}
		
		del self.mail[friendid]
		del self.nt_info[friendid]
		self.save()
		return {}
			
	def ban(self, ben_roleid, ben_name):
		"""
		阻止玩家
		"""
		self.blacklist.append({'roleid':ben_roleid, 'name':ben_name, 'create_time':currentTime()})
			
	def updateBlacklist(self):
		"""
		更新好友列表
		"""
		gameConf = config.getConfig('game')
		expire = gameConf['blacklist_expiry_period']
		now = currentTime()		
		self.blacklist = filter(lambda ban: ban['create_time'] + exp > now, self.blacklist)
			
	def isBan(self, ban_roleid):
		"""
		是否禁用
		"""
		self.updateBlacklist()
		for ban in self.blacklist:
			if ban['roleid'] == ban_roleid:
				return True
		return False
				
	def updateFriendData(self):
		"""
		更新好友数据
		"""
		for friendid in self.friend:
			fNw = network.get(friendid)
			strRoleid = str(self.roleid)
			if fNw.friend.has_key(strRoleid):
				fNw.friend[strRoleid] = self.user.getFriendData()
				fNw.save()			
		
	def friendRequestAnswer(self, requestid, option):
		"""
		回应好友请求
		"""
		if not self.friend_request.has_key(requestid):
			return {'msg':'request_not_exist'}
		friendRequest = self.friend_request[requestid]
		if option == 'yes':
			friendid = friendRequest['roleid']
			if self.friend.has_key(friendid):
				return {'msg':'friend_not_exist'}
			friend = self.user.__class__.get(friendid)
			friendQt = friend.getQuest()

			friendData = self.addFriend(friend)
			usr = self.user
			qt = usr.getQuest()
			qt.udpateFinishFriendQuest(self )

			friendNw = friend.getNetwork()
			friendQt.udpateFinishFriendQuest(friendNw)
			selfData = friendNw.addFriend(self.user)
			if not friend.notify.has_key('notify_add_friend'):
				friend.notify['notify_add_friend'] = {}
			friend.notify['notify_add_friend'][self.roleid] = selfData		
			requestid = [friendRequest['id']]
			del self.friend_request[friendRequest['id']]
			
			for key, val in self.friend_request.items():
				if val['roleid'] == friendid:
					del self.friend_request[key]
					requestid.append(key)				
			self.save()
			friendNw.save()
			friend.save()
			return {'friend_request_delete':requestid, 'friend_new':friendData}
		elif option == 'no':
			del self.friend_request[requestid]		
			self.save()
			return {'friend_request_delete':requestid}
		return {}
	
	def emailMarkReaded(self, id):
		"""
		将邮件标记为已读
		"""
		if not self.email.has_key(id):
			return {'msg':'email_not_exist'}
		if not self.email.has_key(id):
			return {'msg':'email_not_exist'}
		self.email[id]['read'] = True
		self.save()
		self.email[id]['read'] = True
		return self.email[id]
		
	def emailOpen(self, id):
		"""
		打开邮件
		"""
		
		if not self.email.has_key(id):
			return {'msg':'email_not_exist'}
		
		if self.email[id]['open']:
			return {'msg':'email_already_open'}
		
		usr = self.user
		emailConf = config.getConfig('email')
		emailInfo = emailConf[self.email[id]['emailid']]
		if emailInfo:
			awd = {}
			awd = drop.open(usr, emailInfo['dropid'], awd)
			awd = drop.makeData(awd, {})
		self.email[id]['open'] = True
		
		self.save()
		
		data = awd
		data['email_update'] = self.email[id]
		return data
		
		
	def emailDelete(self, emailid):
		"""
		删除邮件
		"""
		if self.email.has_key(emailid):
			del self.email[emailid]
			self.save()
			return {'email_delete':emailid}
		return {'msg':'email_not_exist'}

	def yell(self, name, msg):
		"""
		世界聊天
		"""
		ms = massyell.get(0)
		qt = self.user.getQuest()		
		qt.updateFinishYellQuest()
		return ms.yell(self.roleid, name, msg)

	def appendEmail(self, emailid, parameter):
		"""
		加入 email
		"""
		usr = self.user
		requestid = str(self.sequenceid)		
		email = {'emailid' : emailid, 'read' : False, 'open' : False, 'send_time' : currentTime(), 'roleid':0, 'id':requestid, 'parameter':parameter}
		self.email[requestid] = email
		self.sequenceid = self.sequenceid + 1
		self.notify_add_email(email)
		usr.save()
		self.save()
		
	def notify_add_email(self, email):
		"""
		提示新的邮件
		"""
		usr = self.user
		if not usr.notify.has_key('notify_add_email'):
			usr.notify['notify_add_email'] = {}
		usr.notify['notify_add_email'][email['id']] = email
		
	
