#coding:utf-8
#!/usr/bin/env python

from game.utility.config import config


class email:
	
	@staticmethod
	def send_ladder_email(ladder, emailType):
		emailConf = config.getConfig('email')
		
		for emailid in emailConf:
			emailInfo = emailConf[emailid]
			if emailInfo['optype'] == emailType:
				begin, end, levelGroup = emailInfo['opvaule']
				if ladder.has_key(levelGroup):
					last_position = len(ladder[levelGroup]) - 1
					if last_position < begin:
						continue
					if last_position < end:
						end = last_position
					if begin > end:
						continue
					for i in range(begin, end + 1):
						usr = user.get(ladder[levelGroup][i])
						if usr:
							nw = usr.getNetwork()
							nw.appendMail(emailid, str(i))
							
		
		