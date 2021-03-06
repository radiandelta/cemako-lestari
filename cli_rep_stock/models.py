# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import timedelta
import os
import base64
import xlsxwriter
from werkzeug.wrappers import Response


class rep_stock(models.Model):
	_name = 'cli_rep_stock.rep_stock'

	@api.one
	def isi_data(self):
		repid = str(self.id)
		xtglakhir = self.tglakhir+' 23:59:59'
		xtglawal = self.tglawal
		self.env.cr.execute('Delete from cli_rep_stock_rep_stock_line WHERE report_id = %s' % repid)
		produk = self.env['product.product']
		prod_id = produk.search([('product_tmpl_id.categ_id.id','=',self.category.id)])
		sawal = self.env['stock.inventory.line']
		mutasi = self.env['stock.move']
		for hasil in prod_id:
			result={
				'report_id':self.id,
				'product_id':hasil.id,
				'product_name':hasil.name_template,
				'product_uom':hasil.product_tmpl_id.uom_id.name,
				'stock_awal':0,
				'stock_akhir':0,
				'mutasi_in':0,
				'mutasi_out':0,
			}
			self.env['cli_rep_stock.rep_stock_line'].create(result)
		test = ""
		for line in self.report_line:
			xproduct_id = line.product_id.id
			xlocation_id = line.report_id.location_id.id
			sawal_val=sawal.search([('product_id','=',xproduct_id),('location_id','=',xlocation_id),('inventory_id.initial_inv','=',1)])
			line.stock_awal=sawal_val.product_qty
			xsawal_id = sawal_val.inventory_id.id
			xsawal_tgl = sawal_val.inventory_id.date
			if xsawal_tgl == False:
				xsawal_tgl = '01/05/2016'
			xmutasi_in = xmutasi_inl = xmutasi_out = xmutasi_outl = 0
			self.env.cr.execute("select id,product_qty,location_id,location_dest_id,inventory_id,date,state from stock_move WHERE product_id=%d and date >= '%s' AND date < '%s' AND (inventory_id <> %d or inventory_id is Null) AND state in ('done','complete')" % (xproduct_id, xsawal_tgl, xtglakhir, xsawal_id))
			result = self.env.cr.dictfetchall()
			for hasil in result:
				if hasil['date'] < xtglawal :
					if hasil['location_id'] == xlocation_id :
						xmutasi_outl += hasil['product_qty']
					if hasil['location_dest_id'] == xlocation_id:
						xmutasi_inl += hasil['product_qty']
				else:
					if hasil['location_id'] == xlocation_id :
						xmutasi_out += hasil['product_qty']
					if hasil['location_dest_id'] == xlocation_id:
						xmutasi_in += hasil['product_qty']
				if xproduct_id == 3418 and hasil['location_dest_id'] == xlocation_id:
					test += "test:"+str(hasil['id'])+' '+str(hasil['product_qty'])+' '+hasil['date']+"\r\n"
			line.stock_awal += (xmutasi_inl - xmutasi_outl)
			line.mutasi_in = xmutasi_in
			line.mutasi_out = xmutasi_out
			line.stock_akhir = line.stock_awal + line.mutasi_in - line.mutasi_out
		f=open("c:\\temp\\move.txt","w")
		f.write(test)
		f.close()
		self.state='draft'
		if self.isnol == 0:
			self.env.cr.execute("Delete FROM cli_rep_stock_rep_stock_line WHERE stock_akhir = 0 AND report_id =%s" % repid)
		return
		
	@api.one	
	def export_2_excel(self):
		if os.path.isfile("c:\\temp\\report_stock.xlsx"):
			os.remove("c:\\temp\\report_stock.xlsx")
		workbook = xlsxwriter.Workbook('c:\\temp\\report_stock.xlsx')
		worksheet = workbook.add_worksheet()
		worksheet.set_column('A:A',25)
		worksheet.write('A1','Judul Laporan')
		worksheet.write('B1',self.name)
		worksheet.write('A2','Tanggal Awal')
		worksheet.write('B2',self.tglawal)
		worksheet.write('A3','Tanggal Akhir')
		worksheet.write('B3',self.tglakhir)
		worksheet.write('A4','Kategori')
		worksheet.write('B4',self.category.name)
		worksheet.write('A5','Lokasi')
		worksheet.write('B5',self.location_id.name)
		worksheet.write('A7','Produk')
		worksheet.write('B7','Satuan')
		worksheet.write('C7','Stock Awal')
		worksheet.write('D7','Mutasi Masuk')
		worksheet.write('E7','Mutasi Keluar')
		worksheet.write('F7','Stock Akhir')
		nrow = 6
		for line in self.report_line:
			nrow += 1
			worksheet.write(nrow, 0, line.product_name)
			worksheet.write(nrow, 1, line.product_uom)
			worksheet.write(nrow, 2, line.stock_awal)
			worksheet.write(nrow, 3, line.mutasi_in)
			worksheet.write(nrow, 4, line.mutasi_out)
			worksheet.write(nrow, 5, line.stock_akhir)
		workbook.close()
		with  open("c:\\temp\\report_stock.xlsx", "rb") as xlsx_file:
			encoded_string = base64.b64encode(xlsx_file.read())
		self.file = encoded_string
		self.filename = 'report_stock.xlsx'
		self.state = 'done'
		return 

	name = fields.Char('Judul Laporan')
	tglawal = fields.Date('Tanggal awal laporan')
	tglakhir = fields.Date('Tanggal akhir laporan')
	report_line = fields.One2many('cli_rep_stock.rep_stock_line','report_id','Report Line')
	#category = fields.Selection([('4','Chemical'),('3','Lubricant')],'Kategori',default='4')
	category = fields.Many2one('product.category','Kategori')
	isnol = fields.Boolean('Cetak saldo 0',default=False)
	lang = fields.Char('language',default='en-US')
	location_id = fields.Many2one('stock.location','Lokasi')
	file = fields.Binary('File')
	filename = fields.Char('File name', default='report_stock.xlsx')
	report_name = fields.Char('Report Name', default='reportstock.xlsx')
	state = fields.Char('state',default='draft')
	
class rep_stock_line(models.Model):
	_name = "cli_rep_stock.rep_stock_line"
	_order = 'product_name'
	
	report_id = fields.Many2one('cli_rep_stock.rep_stock','Report Id')
	product_id = fields.Many2one('product.product','Product Id')
	product_name = fields.Char('Produk')
	product_uom = fields.Char('Satuan')
	stock_awal = fields.Float('Stock Awal')
	mutasi_out = fields.Float('Mutasi keluar')
	mutasi_in =  fields.Float('Mutasi masuk')
	stock_akhir = fields.Float('Stock Akhir')
	
class stock_inventory(models.Model):
	_name = "stock.inventory"
	_inherit = "stock.inventory"
	
	initial_inv= fields.Boolean('Initial_inv', default=False)
	