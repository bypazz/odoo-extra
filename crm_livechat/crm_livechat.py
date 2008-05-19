from osv import fields,osv
from osv import orm
import pooler
import time

class crm_livechat_jabber(osv.osv):
	_name="crm_livechat.jabber"
	_description= "Livechat Account"
	_columns={
		'name': fields.char("Jabber Account", size=128, required=True),
		'server': fields.char('Jabber Server', size=40, required=True),
		'login': fields.char('Account Login', size=32, required=True),
		'password': fields.char('Account Password', size=16, required=True),
	}
crm_livechat_jabber()


#
# When a visitor wants to talk, he has to call start_session
# To know is there is a user available, you can call get_user
# Then close_session when it's finnished
#
class crm_livechat_livechat(osv.osv):
	_name="crm_livechat.livechat"
	_description= "LiveChat Account"
	_columns={
		'name': fields.char("Livechat Account", size=128, required=True),
		'state': fields.selection([('active','Active'),('notactive','Not Active')], "State"),
		'max_per_user': fields.integer('Maximum Customer per User'),
		'session_delay': fields.integer('Minutes to Close a session', help="Put here to number of minutes after which a session is considered as closed"),
		'user_ids': fields.one2many('crm_livechat.livechat.user', 'livechat_id', 'Users Accounts'),
		'partner_ids': fields.one2many('crm_livechat.livechat.partner', 'livechat_id', 'Visitors Accounts'),
	}
	_defaults = {
		'max_per_user': lambda *args: 5,
		'state': lambda *args: 'notactive'
	}
	def __init__(self, *args, **argv):
		self.session_count = 0
		self.sessions = {}
		return super(crm_livechat_livechat, self).__init__(*args, **argv)

	def get_chat_name(self,cr,uid,context={}):
		ids=self.search(cr,uid,[],context)
		res=self.browse(cr,uid,ids,context)
		result={}
		for r in res:
			result[str(r.id)]=r.name
		print "RESULT:::::::::::",result
		return result


	#
	# return { jabber_id, {jabber_connection_data} }
	# This is used by the web application to get information about jabber accounts
	# The web application put this in his session to now download it at each time
	#
	def get_configuration(self, cr, uid, ids, context={}):
		result = {}
		main_res={}
		print "Ids ",ids
		for lc in self.browse(cr, uid, ids, context):
			print "In loop",lc
			print "lc.user_ids + lc.partner_ids:",lc.user_ids ," dfdfdfdf          ",lc.partner_ids
			for u in lc.user_ids:
				result[str(u.id)] = {
					'name': u.name,
					'server': u.jabber_id.server,
					'login':  u.jabber_id.login,
					'password':  u.jabber_id.password,
					'state': u.state
				}
			main_res['user']=result
			result={}
			for u in lc.partner_ids:
				result[str(u.id)] = {
					'name': u.name,
					'server': u.jabber_id.server,
					'login':  u.jabber_id.login,
					'password':  u.jabber_id.password,
					'state': u.state
				}			
			main_res['partner']=result	
		print "This is result",main_res
		return main_res

	def get_user(self, cr, uid, id, context={}):
		minu = (9999999,False)
		print "This is id ",id
		livechat = self.browse(cr, uid, id,context)
		print "This is livechat",livechat
		for user in livechat[0].user_ids:
			print "users ",user
			if  user.state=='active':
#				continue
				c = 0
				for s in self.sessions:
					if s[0]==user.user_id.id:
						c+=1
				if c<minu[0]:
					if c<livechat[0].max_per_user:
						minu = (c, user.id)
			else:
				print "Not active"
				continue
		return minu[1]

	"""
		IN:
			livechat_id
			user_id : False (auto-detect) or force a particular user
			partner_ip: IP Address of the partner
			lang: language of the partner (False for unknown)
		OUT:
			False if no available users or partners
			(session_id, user_jabber_id, partner_jabber_id) if available
	"""
	def start_session(self, cr, uid, livechat_id, user_id=False, partner_ip='Unknown', lang=False, context={}):
		print "In session srtart", livechat_id," User id ", user_id
		if not user_id:
			user_id = self.get_user(cr, uid, livechat_id, context)
		if not user_id:
			return False

		partner_id=False
		for p in self.browse(cr, uid, livechat_id, context)[0].partner_ids:
			print "partner ids::::::::::::::::",p.id,p.state
			if p.state=='active':
				print "In if",p.id
				partner_id = p.id
				break
		if not partner_id:
			return False
		print "Parnter id",partner_id
		self.pool.get('crm_livechat.livechat.partner').write(cr, uid, [partner_id], {
			'available': partner_ip,
			'available_date': time.strftime('%Y-%m-%d %H:%M:%S')
		})
		self.session_count+=1
		self.sessions[self.session_count] = (user_id, partner_id, livechat_id)
		print "self.session",self.sessions
		return self.session_count
	"""
		IN:
			livechat_id
			session_id : The ID of a session
		OUT:
			True
	"""
	def stop_session(self, cr, uid, id, session_id, log=True, context={}):
		print "session_id"
		print "session id ",session_id," data it have ",self.sessions
		self.pool.get('crm_livechat.livechat.partner').write(cr, uid, [self.sessions[session_id][1]], {
			'available': 'notactive',
		})
		print "This is self session",self.sessions
		if session_id in self.sessions:
			print "This is log ",session_id
			print " Value of log ",log
			if log:
				print "In logging"
				self.pool.get('crm_livechat.log').create(cr, uid, {
					'note': log,
					'user_id': self.sessions[session_id][1],
					'livechat_id':self.sessions[session_id][2][0],
				})
				print "LOG COMPLTERD::::::::::::::"
			del self.sessions[session_id]
		return True

crm_livechat_livechat()

#
# The available jabber accounts for the visitors of the website
#
class crm_livechat_livechat_partner(osv.osv):
	_name="crm_livechat.livechat.partner"
	_description= "LiveChat Visitors"
	_columns={
		'name': fields.char("Account Name", size=128, required=True),
		'jabber_id': fields.many2one('crm_livechat.jabber', "Jabber Account", required=True),
		'livechat_id': fields.many2one("crm_livechat.livechat", "Livechat", required=True),
		'available': fields.char('Available IP', size=64, help="If empty, the acount is available/not used"),
		'available_date': fields.datetime('Available Date'),
		'state': fields.selection([('active','Active'),('notactive','Not Active')], "State", required=True),
	}
	_defaults = {
		'state': lambda *args: 'notactive'
	}
crm_livechat_livechat_partner()

class crm_livechat_livechat_user(osv.osv):
	_name="crm_livechat.livechat.user"
	_description= "LiveChat Users"
	_columns={
		'name': fields.char("User Name", size=128, required=True),
		'user_id': fields.many2one('res.users', "User", required=True),
		'jabber_id': fields.many2one('crm_livechat.jabber', "Jabber Account", required=True),
		'livechat_id': fields.many2one("crm_livechat.livechat", "Livechat", required=True),
		'languages': fields.char('Language Regex', size=128),
		'state': fields.selection([('active','Active'),('notactive','Not Active')], "State", required=True),
	}
	_defaults = {
		'state': lambda *args: 'notactive'
	}
crm_livechat_livechat_user()

class crm_livechat_livechat_log(osv.osv):
	_name="crm_livechat.log"
	_description= "LiveChat Log"
	_order = 'id desc'
	_columns={
		'name': fields.datetime("Date and Time", required=True),
		'user_id': fields.many2one('crm_livechat.livechat.user', "User"),
		'livechat_id': fields.many2one("crm_livechat.livechat", "Livechat", required=True, ondelete='cascade'),
		'note': fields.text('History')
	}
	_defaults = {
		'name': lambda *args: time.strftime('%Y-%m-%d %H:%M:%S')
	}
crm_livechat_livechat_log()


