# -*- coding: utf-8 -*-

from openerp import models, fields, api
from openerp.tools import terbilang as tbl

class cli_invoice(models.Model):
	_name = 'cli.invoice'
	 
	name = fields.Char("Name")
	 
	 
class account_invoice(models.Model):
	_name = 'account.invoice'
	_inherit = 'account.invoice'
	
	@api.one
	@api.depends('amount_total')
	def _proses_terbilang(self):
		self.tottext = tbl.terbilang(self.amount_total)

	tottext = fields.Char(compute="_proses_terbilang",string="Terbilang")
	Note = fields.Text('Note')
	date_invoice = fields.Date(string='Invoice Date',
		readonly=False, index=True, help="Keep empty to use the current date", copy=False)
	payment_term = fields.Many2one('account.payment.term', string='Payment Terms', readonly=False,
		help="If you use payment terms, the due date will be computed automatically at the generation "
			"of accounting entries. If you keep the payment term and the due date empty, it means direct payment. "
			"The payment term may compute several due dates, for example 50% now, 50% in one month.")
	partner_bank_id = fields.Many2one('res.partner.bank', string='Bank Account', readonly=False,
		help='Bank Account Number to which the invoice will be paid. A Company bank account if this is a Customer Invoice or Supplier Refund, otherwise a Partner bank account number.')
