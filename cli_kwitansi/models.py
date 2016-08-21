# -*- coding: utf-8 -*-

from openerp import models, fields, api
from openerp.tools import terbilang as tbl
from openerp.tools import tgltostr
from openerp.tools import ubahkoma
import os

class cli_kwitansi(models.Model):
	_name = 'cli_kwitansi'
	_inherit = 'account.invoice'

	name = fields.Char('Nomor Kwitansi')
	 
class account_invoice(models.Model):
	_name = "account.invoice"
	_inherit = "account.invoice"

	@api.one
	@api.depends('amount_total')
	def _proses_terbilang(self):
		self.terbilang = tbl.terbilang(self.amount_total)
		
	@api.one
	@api.depends('date_invoice')
	def _proses_tanggal(self):
		self.tanggal = tgltostr.tgltostr(self.date_invoice,1)
		
	nomor_po = fields.Char('Nomor PO/SPK')
	terbilang = fields.Char(compute='_proses_terbilang')
	tanggal = fields.Char(compute='_proses_tanggal')
	
class sale_order(models.Model):
	_name = "sale.order"
	_inherit = "sale.order"
	
	@api.v7
	def _prepare_invoice(self, cr, uid, order, lines, context=None):
		res=super(sale_order,self)._prepare_invoice(cr, uid, order, lines, context=context)
		res.update({'nomor_po':order.nomor_po})
		return res

	nomor_po = fields.Char('Nomor PO/SPK')