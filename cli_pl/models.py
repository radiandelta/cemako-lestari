# -*- coding: utf-8 -*-

from openerp import models, fields, api
from openerp.tools import tgltostr

class stock_picking(models.Model):
	_name = "stock.picking"
	_inherit = "stock.picking"
	
	@api.one
	@api.depends('date')
	def _proses_tanggal(self):
		self.tgl_cetak = tgltostr.tgltostr(self.date,1)
	
	nomor_do = fields.Char("Nomor DO",default="-")
	no_pesan = fields.Char("Nomor Pesanan",default=" ")
	tgl_pesan = fields.Char("Tanggal Pesanan")
	nama_pesan = fields.Char("Nama Pemesan",default=" ")
	tgl_cetak = fields.Char(compute='_proses_tanggal')