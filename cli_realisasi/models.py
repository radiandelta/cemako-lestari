from openerp import models, api, fields

class komisi_realisasi(models.Model):
	_name = "komisi.realisasi"

	@api.one
	@api.depends("real_line.real_kom_chem", "real_line.real_kom_lubs", "real_line.real_total_pd")
	def _compute_komisi(self):
		self.real_kom_chem = sum(line.real_kom_chem for line in self.real_line)
		self.real_kom_lubs = sum(line.real_kom_lubs for line in self.real_line)
		self.real_total_pd = sum(line.real_total_pd for line in self.real_line)
		self.real_total_kom = self.real_kom_chem + self.real_kom_lubs
		
	@api.multi
	def generate_date(self):
		return
		
	name = fields.Char('Name', default='Realisasi Komisi dan PD')
	periode_awal = fields.Date("Periode Awal")
	periode_akhir = fields.Date("Periode Akhir")
	real_kom_chem = fields.Float("Real. komisi Chemical", readonly=True)
	real_kom_lubs = fields.Float("Real. komisi Lubricants",readonly=True)
	real_kom_othr = fields.Float("Real. komisi Lain2",readonly=True)
	real_total_kom = fields.Float(compute="_compute_komisi", string="Real. Total Komisi", readonly=True)
	real_total_pd = fields.Float(compute="_compute_komisi", string="Real. Total PD", readonly=True)
	tgl_real = fields.Date("Tanggal Realisasi", readonly=True)
	real_line = fields.One2many("komisi.realisasi.lines", "real_id")
	
class komisi_realisasi_lines(models.Model):
	_name = "komisi.realisasi.lines"
	
	user_id = fields.Many2one('res.users', string="User")
	real_id = fields.Many2one('komisi.realisasi', string="realisasi")
	invoice_line = fields.One2many("account.invoice", "real_ids")
	real_kom_chem = fields.Float("Real. komisi Chemical", readonly=True)
	real_kom_lubs = fields.Float("Real. komisi Lubricants", readonly=True)
	real_kom_othr = fields.Float("Real. komisi Lain2", readonly=True)
	real_total_kom = fields.Float("Real. Total Komisi", readonly=True)
	real_total_pd = fields.Float("Real. Total PD", readonly=True)
	tgl_real = fields.Date("Tanggal Realisasi", readonly=True)
	
class account_invoice(models.Model):
	_name = 'account.invoice'
	_inherit = 'account.invoice'
	
	real_ids=fields.Many2one('komisi.realisasi.lines', string='realisasi id')
	