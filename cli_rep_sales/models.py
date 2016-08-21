# -*- coding: utf-8 -*-

from openerp import models, fields, api
import xlsxwriter
import os
import base64

class cli_rep_sales(models.Model):
	_name = 'cli.rep.sales'
	
	@api.one
	def generate_data(self):
		tglawal = self.tgl_awal
		tglakhir = self.tgl_akhir+' 23:59:59'
		repid = str(self.id)
		if len(self.sales_id)== 0:
			if self.category=="Chemical":
				if self.pajak == 'PPN' :
					kriteria=['&','&','&','&',('date_order','>=',tglawal),('date_order','<=',tglakhir),('total_chem','>',0),('amount_tax','>',0),('cabang','=',0),'|',('state','=','manual'),('state','=','progress')]
				elif self.pajak == 'NON':
					kriteria=['&','&','&','&',('date_order','>=',tglawal),('date_order','<=',tglakhir),('total_chem','>',0),('amount_tax','=',0),('cabang','=',0),'|',('state','=','manual'),('state','=','progress')]
				else:
					kriteria=['&','&','&',('date_order','>=',tglawal),('date_order','<=',tglakhir),('total_chem','>',0),('cabang','=',0),'|',('state','=','manual'),('state','=','progress')]
			elif self.category == 'Lubricant':
				if self.pajak == 'PPN' :
					kriteria=['&','&','&','&',('date_order','>=',tglawal),('date_order','<=',tglakhir),('total_lubs','>',0),('amount_tax','>',0),('cabang','=',0),'|',('state','=','manual'),('state','=','progress')]
				elif self.pajak == 'NON':
					kriteria=['&','&','&','&',('date_order','>=',tglawal),('date_order','<=',tglakhir),('total_lubs','>',0),('amount_tax','=',0),('cabang','=',0),'|',('state','=','manual'),('state','=','progress')]
				else:
					kriteria=['&','&','&',('date_order','>=',tglawal),('date_order','<=',tglakhir),('total_lubs','>',0),('cabang','=',0),'|',('state','=','manual'),('state','=','progress')]
			else:
				if self.pajak == 'PPN' :
					kriteria=['&','&','&',('date_order','>=',tglawal),('date_order','<=',tglakhir),('amount_tax','>',0),('cabang','=',0),'|',('state','=','manual'),('state','=','progress')]
				elif self.pajak == 'NON':
					kriteria=['&','&','&',('date_order','>=',tglawal),('date_order','<=',tglakhir),('amount_tax','=',0),('cabang','=',0),'|',('state','=','manual'),('state','=','progress')]
				else:
					kriteria=['&','&',('date_order','>=',tglawal),('date_order','<=',tglakhir),('cabang','=',0),'|',('state','=','manual'),('state','=','progress')]
		else:
			salesid = self.sales_id.id
			if self.category=="Chemical":
				if self.pajak == 'PPN' :
					kriteria=['&','&','&','&','&',('date_order','>=',tglawal),('date_order','<=',tglakhir),('total_chem','>',0),('amount_tax','>',0),('cabang','=',0),('user_id','=',salesid),'|',('state','=','manual'),('state','=','progress')]
				elif self.pajak == 'NON' :
					kriteria=['&','&','&','&','&',('date_order','>=',tglawal),('date_order','<=',tglakhir),('total_chem','>',0),('amount_tax','=',0),('cabang','=',0),('user_id','=',salesid),'|',('state','=','manual'),('state','=','progress')]
				else:
					kriteria=['&','&','&','&',('date_order','>=',tglawal),('date_order','<=',tglakhir),('total_chem','>',0),('cabang','=',0),('user_id','=',salesid),'|',('state','=','manual'),('state','=','progress')]
			elif self.category == 'Lubricant':
				if self.pajak == 'PPN' :
					kriteria=['&','&','&','&','&',('date_order','>=',tglawal),('date_order','<=',tglakhir),('total_lubs','>',0),('amount_tax','>',0),('cabang','=',0),('user_id','=',salesid),'|',('state','=','manual'),('state','=','progress')]
				elif self.pajak == 'NON' :
					kriteria=['&','&','&','&','&',('date_order','>=',tglawal),('date_order','<=',tglakhir),('total_lubs','>',0),('amount_tax','=',0),('cabang','=',0),('user_id','=',salesid),'|',('state','=','manual'),('state','=','progress')]
				else:
					kriteria=['&','&','&','&',('date_order','>=',tglawal),('date_order','<=',tglakhir),('total_lubs','>',0),('cabang','=',0),('user_id','=',salesid),'|',('state','=','manual'),('state','=','progress')]
			else:
				if self.pajak == 'PPN' :
					kriteria=['&','&','&','&',('date_order','>=',tglawal),('date_order','<=',tglakhir),('amount_tax','>',0),('cabang','=',0),('user_id','=',salesid),'|',('state','=','manual'),('state','=','progress')]
				elif self.pajak == 'NON' :
					kriteria=['&','&','&','&',('date_order','>=',tglawal),('date_order','<=',tglakhir),('amount_tax','=',0),('cabang','=',0),('user_id','=',salesid),'|',('state','=','manual'),('state','=','progress')]
				else:
					kriteria=['&','&','&',('date_order','>=',tglawal),('date_order','<=',tglakhir),('cabang','=',0),('user_id','=',salesid),'|',('state','=','manual'),('state','=','progress')]
		self.env.cr.execute("DELETE FROM cli_rep_sales_lines WHERE rep_id = %s"%repid)
		orderraw=self.env['sale.order']
		order=orderraw.sorted(key=lambda r: r.user_id)
		ord_id=order.search(kriteria)
		xsumkomisi = xsumkomisi1 = xsumtotalkomisi = 0
		xsumnetto = 0
		xsumpd = 0
		xsumpd1 = 0
		xsumharga_jual = 0
		for val in ord_id:
			newline=True
			xharga=0
			xitem=''
			xnetto=0
			xharga_jual=0
			xdiskonrp=0
			xdisc=0
			xppn=0
			if self.category=="Chemical":
				criteria_prod=[4]
			elif self.category == 'Lubricant':
				criteria_prod=[3]
			else:
				criteria_prod=[3,4]
			for val2 in val.order_line:
				if val2.product_id.product_tmpl_id.categ_id.id in criteria_prod :
					if newline==False:
						xitem += "\r\n"
					xitem += str(int(val2.product_uom_qty))+' '+val2.product_uom.name+' '+val2.product_id.name+'('+"{:,}".format(int(val2.price_unit)).replace(',','.')+")"
					newline=False
					xharga += (val2.product_uom_qty * val2.price_unit)
					xnetto += (val2.product_uom_qty * val2.base_price)
					xdiskonrp += val2.diskonrp
					xdisc += (val2.product_uom_qty * int(val2.price_unit*(val2.discount/100)))
					if val2.tax_id.price_include == True:
						xppn += val2.price_subtotal - int(val2.price_subtotal/(1+val2.tax_id.amount))
					else:
						xppn += int(val2.price_subtotal*(val2.tax_id.amount))
					xharga_jual += val2.price_subtotal
			xpsn_kom = 0
			xkomisi = 0
			xharga_jual = xharga_jual - xdiskonrp
			xdisc = xdisc + xdiskonrp
			xpd = xharga - xdisc - xnetto
			xpd1 = int(xpd * (float(val.pd_rate)/100))
			if self.category=="Chemical":
				xpsn_kom = val.rate_chem
				xkomisi = int(val.komisi_chem)
			elif self.category=="Lubricant":
				xpsn_kom = val.rate_lubs
				xkomisi = int(val.komisi_lubs)
			else:
				if (val.komisi_lubs > 0 and val.komisi_chem > 0):
					xpsn_kom = 0
				else:
					xpsn_kom = val.rate_chem + val.rate_lubs
				xkomisi = int(val.komisi_chem)+int(val.komisi_lubs)
			xsumkomisi += xkomisi
			xsumkomisi1 += val.komisi1
			xsumtotalkomisi += val.grand_komisi
			xsumnetto += xnetto
			xsumpd1 += xpd1
			xsumpd += xpd
			xsumharga_jual += xharga_jual
			result={
				'rep_id': self.id,
				'tanggal': val.date_order,
				'no_inv': val.client_order_ref,
				'sales': val.user_id.name,
				'customer': val.partner_id.name,
				'item': xitem,
				'harga': xharga,
				'disc': xdisc,
				'harga_jual': val.amount_total,
				'ppn':xppn,
				'pd': val.pd1,
				'pd1': val.pd2,
				'netto': xnetto,
				'psn_kom': xpsn_kom,
				'komisi': xkomisi,
				'komisi1_rate':val.komisi_rate,
				'komisi1':val.komisi1,
				'total_komisi':val.grand_komisi,
				'ppn':xppn
			}
			self.env['cli.rep.sales.lines'].create(result)
			self.sumkomisi = xsumkomisi
			self.sumkomisi1 = xsumkomisi1
			self.sumtotalkomisi = xsumtotalkomisi
			self.sumnetto = xsumnetto
			self.sumpd = xsumpd
			self.sumpd1 = xsumpd1
			self.sumharga_jual = xsumharga_jual
			self.state= "draft"
		return
		
	@api.one
	def export_2_excel(self):
		if os.path.isfile("c:\\temp\\report_sales.xlsx"):
			os.remove("c:\\temp\\report_sales.xlsx")
		workbook = xlsxwriter.Workbook("c:\\temp\\report_sales.xlsx")
		worksheet = workbook.add_worksheet()
		worksheet.write('A1','Judul Laporan')
		worksheet.write('C1', self.name)
		worksheet.write('A2','Tanggal Awal')
		worksheet.write('C2',self.tgl_awal)
		worksheet.write('A3', 'Tanggal Akhir')
		worksheet.write('C3', self.tgl_akhir)
		worksheet.write('A4', 'Kategori')
		worksheet.write('C4', self.category)
		worksheet.write('A5', 'Pajak')
		worksheet.write('C5', self.pajak)
		worksheet.write('A6', 'Salesman')
		if self.sales_id.name != False :
			worksheet.write('C6', self.sales_id.name)
		worksheet.write('A8','Tanggal')
		worksheet.write('B8','No. Inv')
		worksheet.write('C8','Sales')
		worksheet.write('D8','Customer')
		worksheet.write('E8','Item')
		worksheet.write('F8','Harga')
		worksheet.write('G8','Disc')
		worksheet.write('H8','Harga Jual')
		worksheet.write('I8','PPN')
		worksheet.write('J8','PD')
		worksheet.write('K8','PD1')
		worksheet.write('L8','Netto')
		worksheet.write('M8','%Komisi')
		worksheet.write('N8','Komisi')
		worksheet.write('O8','% Komisi 1')
		worksheet.write('P8','Komisi 1')
		worksheet.write('Q8','Komisi Net')
		nrow1 = nrow = 7
		for line in self.report_line:
			nrow += 1
			worksheet.write(nrow, 0, line.tanggal)
			worksheet.write(nrow, 1, line.no_inv)
			worksheet.write(nrow, 2, line.sales)
			worksheet.write(nrow, 3, line.customer)
			worksheet.write(nrow, 4, line.item)
			worksheet.write(nrow, 5, line.harga)
			worksheet.write(nrow, 6, line.disc)
			worksheet.write(nrow, 7, line.harga_jual)
			worksheet.write(nrow, 8, line.ppn)
			worksheet.write(nrow, 9, line.pd)
			worksheet.write(nrow, 10, line.pd1)
			worksheet.write(nrow, 11, line.netto)
			worksheet.write(nrow, 12, line.psn_kom)
			worksheet.write(nrow, 13, line.komisi)
			worksheet.write(nrow, 14, line.komisi1_rate)
			worksheet.write(nrow, 15, line.komisi1)
			worksheet.write(nrow, 16, line.total_komisi)
		nrow += 1
		total_harga_jual='=SUM(H{}:H{})'.format(nrow1+2,nrow)
		total_pd = '=SUM(J{}:J{})'.format(nrow1+2,nrow)
		total_pd1 = '=SUM(K{}:K{})'.format(nrow1+2,nrow)
		total_netto = '=SUM(L{}:L{})'.format(nrow1+2,nrow)
		total_komisi = '=SUM(N{}:N{})'.format(nrow1+2,nrow)
		total_komisi1 = '=SUM(P{}:P{})'.format(nrow1+2,nrow)
		total_komisinet = '=SUM(Q{}:Q{})'.format(nrow1+2,nrow)
		worksheet.write(nrow, 7, total_harga_jual)
		worksheet.write(nrow, 9, total_pd)
		worksheet.write(nrow, 10, total_pd1)
		worksheet.write(nrow, 11, total_netto)
		worksheet.write(nrow, 13, total_komisi)
		worksheet.write(nrow, 15, total_komisi1)
		worksheet.write(nrow, 16, total_komisinet)
		nrow += 1
		worksheet.write(nrow, 7, self.sumharga_jual)
		worksheet.write(nrow, 9, self.sumpd)
		worksheet.write(nrow, 10, self.sumpd1)
		worksheet.write(nrow, 11, self.sumnetto)
		worksheet.write(nrow, 13, self.sumkomisi)
		worksheet.write(nrow, 15, self.sumkomisi1)
		worksheet.write(nrow, 16, self.sumtotalkomisi)
		workbook.close()
		with  open("c:\\temp\\report_sales.xlsx", "rb") as xlsx_file:
			encoded_string = base64.b64encode(xlsx_file.read())
		self.file = encoded_string
		self.filename = 'report_sales.xlsx'
		self.state = 'done'
		return 

	tgl_awal = fields.Date("Tanggal Awal")
	tgl_akhir = fields.Date("Tanggal Akhir")
	name = fields.Char("Nama Report :")
	category = fields.Selection([('Chemical','Chemical'),('Lubricant','Lubricant'),('Semua','Semua')],'Kategori',default='Chemical')
	pajak = fields.Selection([('PPN','PPN'),('NON','Non PPN'),('SEMUA','Semua')],'Pajak',default='SEMUA')
	report_line = fields.One2many('cli.rep.sales.lines','rep_id')
	lang = fields.Char("Language", default="en_US")
	sumkomisi = fields.Float("Total Komisi")
	sumkomisi1 = fields.Float("Total Komisi 1")
	sumtotalkomisi = fields.Float('Total Komisi Net')
	sumnetto = fields.Float("Total Netto")
	sumpd = fields.Float("Total PD")
	sumpd1 = fields.Float("Total PD1")
	sumharga_jual = fields.Float("Total Harga Jual")
	sales_id = fields.Many2one('res.users','Sales ID')
	file = fields.Binary('File')
	filename = fields.Char('File name', default='report_sales.xlsx')
	state = fields.Char('state',default='draft')




class cli_rep_sales_line(models.Model):
	_name= "cli.rep.sales.lines"
	_order="no_inv"
	
	@api.one
	def _compute_kategori(self):
		if self.no_inv == 'C':
			return 'Chemical'
		else:
			return 'Lubricant'
			
	@api.one
	def _compute_ppn(self):
		if self.ppn > 0:
			return 'PPN'
		else:
			return 'NON'
	
	rep_id = fields.Many2one('cli.rep.sales')
	tanggal = fields.Date('Tanggal')
	no_inv = fields.Char('No.Inv',select=True)
	sales = fields.Char('Sales')
	customer = fields.Char('Customer')
	item = fields.Text('Item')
	harga = fields.Float('Harga')
	disc = fields.Float('Disc')
	harga_jual = fields.Float('Harga Jual')
	pd = fields.Float('PD')
	pd1 = fields.Float('PD1')
	netto = fields.Float('Netto')
	psn_kom = fields.Float('%KOM')
	komisi = fields.Float('Komisi')
	ppn = fields.Float('PPN')
	category=fields.Char(string='Kategori',compute='_compute_kategori',store=True)
	isppn = fields.Char(string='PPN/Non', compute='_compute_ppn',store=True)
	komisi1_rate = fields.Float('% Komisi 1')
	komisi1 = fields.Float('Komisi 1')
	total_komisi = fields.Float('Total Komisi')