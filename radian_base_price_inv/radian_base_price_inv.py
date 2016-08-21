from openerp.osv import orm, fields
from openerp import api
import openerp.addons.decimal_precision as dp

class account_invoice(orm.Model):
	_name = 'account.invoice'
	_inherit = "account.invoice"
	
	@api.one
	@api.depends('invoice_line.price_subtotal', 'invoice_line.diskonrp', 'invoice_line.pd_subtotal', 'invoice_line.net_subtotal', 'tax_line.amount')
	def _compute_amount(self):
		#res = super(account_invoice, self)._compute_amount(self)
		rpd = self.pd_rate
		self.amount_untaxed = sum(line.price_subtotal for line in self.invoice_line)
		self.amount_tax = sum(line.amount for line in self.tax_line)
		self.diskon = sum(line.diskonrp for line in self.invoice_line)
		self.pd1 = sum(line.pd_subtotal for line in self.invoice_line)
		self.pd2 = 0
		self.total_net = sum(line.net_subtotal for line in self.invoice_line)
		tot_lub = tot_chm = tot_oth = 0
		for line in self.invoice_line:
			vars = line.product_id.product_tmpl_id.categ_id.id
			if vars == 3:
				tot_lub += line.net_subtotal
			elif vars == 4:
				tot_chm += line.net_subtotal
			else:
				tot_oth += line.net_subtotal
		self.total_chem = tot_chm
		self.total_lubs = tot_lub
		self.total_othr = tot_oth
		self.komisi_chem = self.total_chem * float(self.rate_chem/100)
		self.komisi_lubs = self.total_lubs * float(self.rate_lubs/100)
		self.total_komisi = self.komisi_chem + self.komisi_lubs
		if self.amount_tax > 0:
			self.amount_tax = int((self.amount_untaxed - self.diskon)*0.1)
			self.komisi1 = int(self.total_komisi*float(self.rate_kom1)/100)
		self.pd2 = int(self.pd1*float(rpd)/100)
		self.total_pd = self.pd1 - self.pd2 - self.bonpd
		self.amount_total = self.amount_untaxed + self.amount_tax - self.diskon
	
	@api.one
	def compute_amount(self):
		self._compute_amount()
		
	_columns = {
		'diskon':fields.float(compute='_compute_amount', digits_compute=dp.get_precision('Account'), string='Diskon',
			help="Diskon Global", store=True, readonly=True, track_visibility='always'),
		'total_pd':fields.float(compute='_compute_amount', digits_compute=dp.get_precision('Account'), string='Total PD',
			store=True, readonly=True, help="Total PD", track_visibility='always'),
		'total_komisi':fields.float(compute='_compute_amount', digits_compute=dp.get_precision('Account'), string='Total Komisi',
			store=True, readonly=True, help="Total PD", track_visibility='always'),
		'total_net':fields.float(compute='_compute_amount', digits_compute=dp.get_precision('Account'), string='Total Net',
			store=True, readonly=True, help="Total Net", track_visibility='always'),
		'total_chem':fields.float(compute='_compute_amount', digits_compute=dp.get_precision('Account'), string='Total Chemical',
			store=True, readonly=True, help="Total Chemical", track_visibility='always'),
		'total_lubs':fields.float(compute='_compute_amount', digits_compute=dp.get_precision('Account'), string='Total Lubricant',
			store=True, readonly=True, help="Total Lubricant", track_visibility='always'),
		'total_othr':fields.float(compute='_compute_amount', digits_compute=dp.get_precision('Account'), string='Total Lain-2',
			store=True, readonly=True, help="Total Lain-2", track_visibility='always'),
		'pd1':fields.float(compute='_compute_amount', digits_compute=dp.get_precision('Account'), string='PD',
			store=True, readonly=True, help="PD 1", track_visibility='always'),
		'pd2':fields.float(compute='_compute_amount', digits_compute=dp.get_precision('Account'), string='PD 1',
			store=True, readonly=True, help="PD 1", track_visibility='always'),
		'bonpd':fields.float(string="Bon PD", onchange="_compute_amount", help='Bon PD'),
		'tanggal_pd':fields.date(string="Tanggal Cair", readonly=True),
		'nomor_fp':fields.char(string='Nomor FP', help='Masukkan nomor faktur pajak'),
		'estimasi':fields.boolean(string="Estimasi", help="Estimasi Komisi dan PD", default=False),
		'realisasi':fields.boolean(string="Realisasi", help="Realisasi Komisi dan PD", default=False),
		'rate_chem':fields.float(string="Rate Chemical", help="Rate komisi chemical", default=0),
		'rate_lubs':fields.float(string="Rate Lubricant", help="Rate komisi lubricant", default = 0),
		'komisi_chem':fields.float(string="Komisi Chemical", help="Komisi Chemical berdasarkan perhitungan per periode"),
		'komisi_lubs':fields.float(string="Komisi Lubricant", help="Komisi Lubricant berdasarkan perhitungan per periode"),
		'rate_kom1':fields.float(string="Rate Komisi 1(%)", help="Rate Komisi 1, diproses jika ada ppn"),
		'komisi1':fields.float(compute='_compute_amount', digits_compute=dp.get_precision('Account'), string='Komisi 1',
			store=True, readonly=True, help="Total PD", track_visibility='always'),
		'pd_rate':fields.float(string="Rate PD", default=0),
		'komisi_net':fields.float(compute='_compute_amount', digits_compute=dp.get_precision('Account'), string='Komisi Net',
			store=True, readonly=True, help="Komisi Net = Komisi - Komisi 1", track_visibility='always'),
	}

class account_invoice_line(orm.Model):
	_name = 'account.invoice.line'
	_inherit = 'account.invoice.line'
	
	@api.depends('quantity', 'base_price', 'subtotal_net')
	def _get_compute_netprice(self):
		self.subtotal_net=self.quantity*self.base_price
		
	def _amount_line_pd(self,cr,uid,ids,field_name,arg,context=None):
		res={}
		if context is None:
			context = {}
		for line in self.browse(cr,uid,ids,context=context):
			price1 = line.price_unit
			price2 = line.base_price
			qty = line.quantity
			pds = int(qty*(price1 - price2))
			res[line.id]= pds
		return res


	def _amount_line_net(self,cr,uid,ids,field_name,arg,context=None):
		res={}
		if context is None:
			context = {}
		for line in self.browse(cr,uid,ids,context=context):
			price1 = line.price_unit
			price2 = line.base_price
			qty = line.quantity
			net = int(qty*price2)
			res[line.id]= net
		return res

		
	_columns = {
		'base_price':fields.float('Base Price', required=True, digits_compute=dp.get_precision('Product Price'), default=0.00),
		'subtotal_net':fields.float('Amount(Net)', required=False, digits_compute=dp.get_precision('Account'), compute="_get_compute_netprice"),
		'pd':fields.float('pd', required=False, digits_compute=dp.get_precision('account')),
		'pd_bayar':fields.float('PD terbayar', required=False, digits_compute=dp.get_precision('account')),
		'cetak':fields.boolean('Cetak', default=True),
		'diskonrp':fields.float('Diskon(Rp)'),
		'label':fields.selection((('Seyton','Seyton'),('Saver','Saver'),('Lain2','Lain2')),'Label', default='Lain2'),
		'pd_subtotal':fields.function(_amount_line_pd, string='PD', digits_compute=dp.get_precision('Account'), store=True, readonly=True),
		'net_subtotal':fields.function(_amount_line_net, string='NET', digits_compute=dp.get_precision('Account'), store=True, readonly=True),


	}
	