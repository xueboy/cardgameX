from gclib.object import object
from gclib.utility import currentTime, is_same_day
from game.utility.config import config
from game.models.massyell import massyell

class network(object):
	
	def init(self):
		pass
		
	
	def __init__(self):
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
		self.user = None
		
	def install(self, roleid):
		object.install(self, roleid)
		
	def getData(self):
		data = object.getData(self)
		data['friend'] = self.friend
		data['message'] = self.message
		data['mail'] = self.mail
		data['email'] = self.email
		data['friend_request'] = self.email
		data['blacklist'] = self.blacklist
		data['sequenceid'] = self.sequenceid
		data['nt_info'] = self.nt_info
		data['request_list'] = self.request_list
		return data			
		
	def getClientMailData(self):
		
		data = {}
		for roleid in self.mail:
			 m = {}
			 m['name'] = self.nt_info[roleid]['name']
			 m['level'] = self.nt_info[roleid]['level']
			 m['sex'] = self.nt_info[roleid]['sex']
			 m['avatar_id'] = self.nt_info[roleid]['avatar_id']
			 m['last_login'] = self.nt_info[roleid]['last_login']
			 m['mail'] = self.mail[roleid]
			 data[roleid] = m
		return data
		
	
	def getClientData(self):	
		
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
		data['email'] = {}#self.email
		data['friend_request'] = self.email		
		#data['nt_info'] = self.nt_info
		return data			
		
	def load(self, roleid, data):
		object.load(self, roleid, data)
		self.friend = data['friend']
		self.message = data['message']
		self.mail = data['mail']
		self.email = data['email']
		self.sequenceid = data['sequenceid']
		self.nt_info = data['nt_info']
		self.request_list = data['request_list']
		
	def addFriendRequest(self, friend):
		
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
		friendNw.email[requestid] = data		
		friendNw.save()
		if not friend.notify.has_key('notify_friend_request'):
			friend.notify['notify_friend_request'] = {}
		friend.notify['notify_friend_request'][requestid] = data
		friend.save()
		self.save()
		return data
		
	def addFriend(self, friend):
		data = friend.getFriendData()
		self.friend[str(friend.roleid)] =  data
		return data
				
	def deleteFriend(self, friend):
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
		if self.friends.has_key(str(friendRoleid)):
			return friends[str(friendRoleid)]

	def sendMessage(self, toUser, msg):		
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
		if self.message.has_key(messageid):
			del self.message[messageid]
			self.save()
	
	def updateMessage(self):
		now = currentTime()
		gameConf = config.getConfig('game')
		expire = gameConf['message_expiry_period']
		self.message = dict((k, v) for k,v in self.message.items() if (v['send_time'] + expire) > now)		
		
	def sendMail(self, toUser, mail):
		toUserNw = toUser.getNetwork()					
		ntInfo = self.user.getNtInfoData()	
		requestid = str(toUserNw.sequenceid)
		toUserNw.sequenceid = toUserNw.sequenceid + 1
		fromUserId = str(self.user.roleid)
		msgData = {'mail':mail, 'send_time': currentTime(), 'id': requestid, 'roleid':fromUserId}	
		if not toUserNw.mail.has_key(fromUserId):
			toUserNw.mail[fromUserId] = []
		toUserNw.mail[fromUserId].append(msgData)
		toUserNw.nt_info[fromUserId] = ntInfo
		if not toUser.notify.has_key('notify_mail'):
			toUser.notify['notify_mail'] = {}
		toUser.notify['notify_mail'][fromUserId] = dict({'new_mail':msgData}, **ntInfo)
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
		fromUser.notify['notify_mail'][toUserId] = dict({'new_mail':msgData}, **toNtInfo)
		fromNw.save()
		fromUser.save()
		
	def deleteMail(self, friendid, mailid):		
		if not self.mail.has_key(friendid):
			return {'msg':'mail_not_exist'}		
		self.mail[friendid] = filter(lambda x : x['id'] != mailid, self.mail[friendid])
		if not self.mail[friendid]:
			del self.mail[friendid]
			del self.nt_info[friendid]
		self.save()
		return {}
		
	def deleteFriendMail(self, friendid):
		if not self.mail.has_key(friendid):
			return {'msg':'mail_not_exist'}		
		
		del self.mail[friendid]
		del self.nt_info[friendid]
		self.save()
		return {}
		
		
	def ban(self, ben_roleid, ben_name):
		self.blacklist.append({'roleid':ben_roleid, 'name':ben_name, 'create_time':currentTime()})
			
	def updateBlacklist(self):
		gameConf = config.getConfig('game')
		expire = gameConf['blacklist_expiry_period']
		now = currentTime()		
		self.blacklist = filter(lambda ban: ban['create_time'] + exp > now, self.blacklist)
			
	def isBan(self, ban_roleid):
		self.updateBlacklist()
		for ban in self.blacklist:
			if ban['roleid'] == ban_roleid:
				return True
		return False
		
	def emailAnswer(self, id, option):
		if not self.email.has_key(id):
			return {'msg':'request_not_exist'}
		email = self.email[id]
		#if email['type'] == 'firend_request':
		return self.emailAnswerFriendRequest(email, option)
			
	def updateFriendData(self):
		for friendid in self.friend:
			fNw = network.get(friendid)
			strRoleid = str(self.roleid)
			if fNw.friend.has_key(strRoleid):
				fNw.friend[strRoleid] = self.user.getFriendData()
				fNw.save()			
		
	def emailAnswerFriendRequest(self, email, option):
		if option == 'yes':
			friendid = email['roleid']
			if self.friend.has_key(friendid):
				return {'msg':'friend_not_exist'}
			friend = self.user.get(friendid)
			friendQt = friend.getQuest()

			friendData = self.addFriend(friend)
			usr = self.user
			qt = usr.getQuest()
			qt.udpateFinishFriendQuest(self )

			friendNw = friend.getNetwork()
			friendQt.udpateFinishFriendQuest(friendNw)
			friendNw.addFriend(self.user)
			
			emailid = [email['id']]
			del self.email[email['id']]
			
			for key, val in self.email.items():
				if val['roleid'] == friendid:
					del self.email[key]
					emailid.append(key)				
			self.save()
			friendNw.save()
			return {'friend_request_delete':emailid, 'friend_new':friendData}
		elif option == 'no':
			del self.email[email['id']]		
			self.save()
			return {'friend_request_delete':[email['id']]}
		return {}
	
	def emailMarkReaded(self, emailid):
		if not self.email.has_key(emailid):
			return {'msg':'email_not_exist'}
		self.email[emailid]['readed'] = True
		self.save()
		return self.email[emailid]		
		
	def emailDelete(self, emailid):
		if self.email.has_key(emailid):
			del self.email[emailid]
			self.save()
			return {'email_delete':emailid}
		return {'msg':'email_not_exist'}

	def yell(self, name, msg):
		ms = massyell.get(0)
		qt = self.user.getQuest()		
		qt.updateFinishYellQuest()
		return ms.yell(self.roleid, name, msg)
