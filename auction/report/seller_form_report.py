##############################################################################
#
# Copyright (c) 2005 TINY SPRL. (http://tiny.be) All Rights Reserved.
#
# $Id$
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
##############################################################################


import pooler
import time
from report import report_sxw
from osv import osv

class seller_form_report(report_sxw.rml_parse):
	def __init__(self, cr, uid, name, context):
		super(seller_form_report, self).__init__(cr, uid, name, context)
		lot=self.pool.get('auction.lots').browse(cr,uid,uid)
		#address=lot.bord_vnd_id.address_get(self.cr,self.uid,[partner.id])
	#	partner=lot.bord_vnd_id.partner_id
	#	address=partner.address and partner.address[0] or ""
	#	street = address and address.street or ""
	

			
		self.localcontext.update({
			'time': time,
			'sum_taxes': self.sum_taxes,
	#		'street':street,
	#		'address':address,
})

		
	def sum_taxes(self, auction_id,obj_price):
		 seller_cost = self.pool.get('auction.dates').read(self.cr,self.uid,[auction_id],['seller_costs'])[0]
		 total_amount = 0.0
		 for id in seller_cost['seller_costs'] :
		 	amount = self.pool.get('account.tax').read(self.cr,self.uid,[id],['amount'])[0]['amount']
		 	total_amount += (amount*obj_price)
		 return total_amount


report_sxw.report_sxw('report.seller_form_report', 'auction.lots', 'addons/auction/report/seller_form_report.rml', parser=seller_form_report)

