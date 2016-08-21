# -*- coding: utf-8 -*-

from openerp import models, fields, api
import os

class cli_order(models.Model):
     _name = 'cli_order.cli_order'

     name = fields.Char()
	 
class sale_order(models.Model):
	_name = 'sale.order'
	_inherit = 'sale.order'
	

	@api.onchange('client_order_ref')
	def _check_client_order_ref(self):
		if self.client_order_ref != False :
			if len(self.client_order_ref)>0 and self.state == 'draft':
				so = self.env['sale.order']
				hasil = so.search([('client_order_ref','=',self.client_order_ref)])
				if len(hasil) > 0:
					return {'value':{},'warning':{'title':'warning','message':'Kode referensi sudah terpakai'}}
				return
	#peringatan = fields.Char('Peringatan')
		
	#_constraint = [(_check_client_order_ref,'Kode referensi sudah dipergunakan',['client_order_ref'])]