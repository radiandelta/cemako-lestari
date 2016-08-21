# -*- coding: utf-8 -*-

from openerp import models, fields, api

class sales_order(models.Model):
	_name = 'sale.order'
	_inherit = 'sale.order'


	@api.one
	@api.depends('order_line.product_id', 'order_line.net_subtotal')
	def update_pd(self):
		tot_lub=tot_chm=tot_oth = 0
		for line in self.order_line:
			vars = line.product_id.product_tmpl_id.categ_id.id
			if vars == 3:
				tot_lub += line.net_subtotal
			elif vars == 4:
				tot_chm += line.net_subtotal
			else:
				tot_oth += line.net_subtotal	
		self.env.cr.execute("update sale_order set total_chem=%s, total_lubs=%s, total_othr=%s WHERE id=%s" % (tot_chm, tot_lub, tot_oth, self.id))
		self.env.cr.execute("update sale_order set pd2 = trunc(pd1*cast(pd_rate as integer)/100) WHERE id=%s" % self.id)
		self.env.cr.execute("update sale_order set total_pd = pd1 - pd2 WHERE id=%s" % self.id)