# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import date
import random

class cli_komisi(models.Model):
	_name = 'cli.komisi'
	

	@api.one	
	def generate_est(self):
		id_komisi = self.id
		tgl_awal=tglawal = self.periode_awal
		tglakhir = self.periode_akhir
		self.env.cr.execute("DELETE from cli_komisi_line WHERE komisi_id = %s" % id_komisi)
		self.env.cr.execute("SELECT user_id from sale_order WHERE sale_order.date_order >= '%s' AND sale_order.date_order < ('%s'::date + '1 day'::interval) AND sale_order.cabang=False GROUP BY sale_order.user_id" % (tglawal, tglakhir))
		# users = self.env['res.users']
		#ids = users.search([['komisi','=',True]])
		result = self.env.cr.dictfetchall()
		vals = {}
		for val in result:
			vals = {
				'komisi_id': self.id,
				'user_id': val['user_id'],
			}
			self.env['cli.komisi.line'].create(vals)
		for line in self.komisi_line:
			ids = line.user_id.id
			isflat = line.user_id.komisiflat
			self.env.cr.execute("SELECT sum(total_othr) as total_othr, sum(total_chem) as total_chem, sum(total_lubs) as total_lubs, sum(total_pd) as total_pd FROM sale_order WHERE sale_order.user_id = %d  AND sale_order.date_order >= '%s' AND sale_order.date_order < ('%s'::date + '1 day'::interval) AND sale_order.cabang = False AND (state!='draft' AND state!='cancel')" % (ids, tglawal, tglakhir))
			result = self.env.cr.dictfetchall()
			tot_chm = tot_lub = tot_oth = tot_pd = 0
			for val in result:
				tot_chm = val['total_chem']
				tot_lub = val['total_lubs']
				tot_oth = val['total_othr']
				tot_pd = val['total_pd']
			line.est_tot_chem = tot_chm
			line.est_tot_lubs = tot_lub
			line.est_tot_othr = tot_oth
			line.est_total_pd = tot_pd
			vars = line.est_tot_chem
			rate = 15
			if not isflat:
				if vars <= 5000000:
					rate = 0
				elif vars > 5000000 and vars <= 7500000:
					rate = 5
				elif vars > 7500000 and vars <= 10000000:
					rate = 7.5
				elif vars > 10000000 and vars <= 15000000:
					rate = 10
				elif vars > 15000000 and vars <= 20000000:
					rate = 12.5
				elif vars > 20000000:
					rate = 15
			vars2 = line.est_tot_lubs
			rate2 = 15
			if not isflat:
				if vars2 <= 5000000:
					rate2 = 0
				elif vars2 > 5000000 and vars2 <= 7500000:
					rate2 = 5
				elif vars2 > 7500000 and vars2 <= 10000000:
					rate2 = 7.5
				elif vars2 > 10000000 and vars2 <= 15000000:
					rate2 = 10
				elif vars2 > 15000000 and vars2 <= 20000000:
					rate2 = 12.5
				elif vars2 > 20000000:
					rate2 = 15
			line.rate_chem = rate
			line.rate_lubs = rate2
			ratechem = line.rate_chem
			ratelubs = line.rate_lubs
			self.env.cr.execute("UPDATE sale_order SET rate_chem=%f, rate_lubs=%f, komisi_line_id=%d WHERE user_id=%d AND date_order >= '%s' AND date_order < ('%s'::date + '1 day'::interval) AND state!='draft' AND state!='cancel'" % (ratechem, ratelubs, line.id, ids, tgl_awal, tglakhir))
			self.env.cr.execute("UPDATE sale_order SET komisi_chem = (total_chem * (rate_chem/100)), komisi_lubs = (total_lubs*(rate_lubs/100)) WHERE (iskomisi is false OR iskomisi is null) AND user_id=%d AND date_order >= '%s' AND date_order < ('%s'::date + '1 day'::interval) AND state!='draft' AND state!='cancel'" % (ids, tgl_awal, tglakhir))
			self.env.cr.execute("UPDATE sale_order SET komisi_chem = komisi_chem_man, komisi_lubs = komisi_lubs_man WHERE iskomisi is true AND user_id=%d AND date_order >= '%s' AND date_order < ('%s'::date + '1 day'::interval) AND state!='draft' AND state!='cancel'" % (ids, tgl_awal, tglakhir))
			self.env.cr.execute("SELECT sum(komisi_chem) as komisi_chem, sum(komisi_lubs) as komisi_lubs FROM sale_order WHERE sale_order.user_id = %d  AND sale_order.date_order >= '%s' AND sale_order.date_order < ('%s'::date + '1 day'::interval) AND sale_order.cabang = False AND (state!='draft' AND state!='cancel')" % (ids, tglawal, tglakhir))
			result = self.env.cr.dictfetchall()
			for val in result:
				tot_chm = val['komisi_chem']
				tot_lub = val['komisi_lubs']
			line.est_kom_chem = tot_chm
			line.est_kom_lubs = tot_lub
			line.est_total_kom = line.est_kom_chem + line.est_kom_lubs
		self.env.cr.execute("UPDATE account_invoice t2 set rate_chem=t1.rate_chem, rate_lubs=t1.rate_lubs, pd_rate=cast(t1.pd_rate as float), rate_kom1=cast(t1.komisi_rate as float) FROM sale_order t1 WHERE t2.origin=t1.name")
		self.env.cr.execute("UPDATE account_invoice SET komisi_chem = (total_chem * (rate_chem/100)), komisi_lubs = (total_lubs*(rate_lubs/100))")
		self.env.cr.execute("UPDATE sale_order SET total_komisi = komisi_chem + komisi_lubs")
		self.env.cr.execute("UPDATE account_invoice SET total_komisi = komisi_chem + komisi_lubs")
		self.env.cr.execute("UPDATE sale_order SET komisi1 = total_komisi * (cast(komisi_rate as float)/100) WHERE amount_tax > 0")
		self.env.cr.execute("UPDATE account_invoice SET komisi1 = total_komisi * (cast(rate_kom1 as float)/100) WHERE amount_tax > 0")
		self.env.cr.execute("UPDATE sale_order SET komisi1 = 0 WHERE amount_tax = 0")
		self.env.cr.execute("UPDATE account_invoice SET komisi1 = 0 WHERE amount_tax = 0")
		self.env.cr.execute("UPDATE sale_order SET grand_komisi = total_komisi - komisi1")
		self.env.cr.execute("UPDATE account_invoice SET komisi_net = total_komisi - komisi1")
		self.env.cr.execute("UPDATE sale_order SET pd2 = pd1 * (pd_rate/100)")
		self.env.cr.execute("UPDATE sale_order SET total_pd = pd1 - pd2")
		self.env.cr.execute("UPDATE account_invoice SET pd2 = pd1 * (pd_rate/100)")
		self.env.cr.execute("UPDATE account_invoice SET total_pd = pd1 - pd2 - bonpd")


		

	@api.one
	@api.depends("komisi_line.est_kom_chem", "komisi_line.est_kom_lubs", "komisi_line.est_total_pd")
	def _compute_komisi(self):
		kom_chem = kom_lubs = total_pd = 0
		self.est_kom_chem = sum(line.est_kom_chem for line in self.komisi_line)
		self.est_kom_lubs = sum(line.est_kom_lubs for line in self.komisi_line)
		self.est_total_pd = sum(line.est_total_pd for line in self.komisi_line)
		self.est_total_kom = self.est_kom_chem + self.est_kom_lubs
				
	periode_awal = fields.Date("Periode Awal")
	periode_akhir = fields.Date("Periode Akhir")
	est_kom_chem = fields.Float(compute="_compute_komisi",string="Est. komisi Chemical", store=True, readonly=True)
	est_kom_lubs = fields.Float(compute="_compute_komisi",string="Est. komisi Lubricants", store=True, readonly=True)
	est_kom_othr = fields.Float("Est. komisi Lain2", readonly=True)
	est_total_pd = fields.Float(compute="_compute_komisi",string="Est. Total PD", store=True, readonly=True)
	est_total_kom = fields.Float(compute="_compute_komisi", string="Est. Total Komisi", store=True, readonly=True)
	tgl_est = fields.Date("Tanggal Estimasi",readonly=True)
	komisi_line = fields.One2many("cli.komisi.line", "komisi_id")
	estimated = fields.Boolean("Estimated")
	realised = fields.Boolean("Realisasi")

class cli_komisi_line(models.Model):
	_name = "cli.komisi.line"
	
	@api.one
	@api.depends('est_tot_chem', 'est_tot_lubs')
	def _compute_rate_chem(self):
		vars = self.est_tot_chem
		rate = 0
		if vars <= 5000000:
			rate = 0
		elif vars > 5000000 and vars <= 7500000:
			rate = 5
		elif vars > 7500000 and vars <= 10000000:
			rate = 7.5
		elif vars > 10000000 and vars <= 15000000:
			rate = 10
		elif vars > 15000000 and vars <= 20000000:
			rate = 12.5
		elif vars > 20000000:
			rate = 15
		self.rate_chem = rate
		self.est_kom_chem = self.est_tot_chem * float(self.rate_chem/100)
		vars2 = self.est_tot_lubs
		rate2 = 0
		if vars2 <= 5000000:
			rate2 = 0
		elif vars2 > 5000000 and vars2 <= 7500000:
			rate2 = 5
		elif vars2 > 7500000 and vars2 <= 10000000:
			rate2 = 7.5
		elif vars2 > 10000000 and vars2 <= 15000000:
			rate2 = 10
		elif vars2 > 15000000 and vars2 <= 20000000:
			rate2 = 12.5
		elif vars > 20000000:
			rate2 = 15
		self.rate_lubs = rate2
		self.est_kom_lubs = self.est_tot_lubs * float(self.rate_lubs/100)
		self.est_total_kom = self.est_kom_chem + self.est_kom_lubs
		
	komisi_id = fields.Many2one("cli.komisi", string="Komisi reference")
	user_id = fields.Many2one('res.users', string="User")
	est_tot_chem = fields.Float("Est. Total Chemical", readonly=True)
	rate_chem = fields.Float(compute="_compute_rate_chem",string="Rate Chemical", store=True, readonly=True)
	est_kom_chem = fields.Float(compute="_compute_rate_chem",string="Est. komisi Chemical",store=True, readonly=True)
	est_tot_lubs = fields.Float("Est. Total Lubricants", readonly=True)
	rate_lubs = fields.Float(compute="_compute_rate_chem",string="Rate Lubricants", store=True, readonly=True)
	est_kom_lubs = fields.Float(compute="_compute_rate_chem",string="Est. komisi Lubricants",store=True, readonly=True)
	est_tot_othr = fields.Float("Est. Total Lain2", readonly=True)
	rate_othr = fields.Float("Rate Lain2", readonly=True, default=0)
	est_kom_othr = fields.Float("Est. komisi Lain2", readonly=True)
	est_total_kom = fields.Float(compute="_compute_rate_chem", string="Est. Total Komisi", store=True, readonly=True )
	est_total_pd = fields.Float("Est. Total PD", readonly=True)
	tgl_est = fields.Date("Tanggal Estimasi", readonly=True)
	komisi_order_line = fields.One2many("sale.order","komisi_line_id")
	
class cli_komisi_user(models.Model):
	_name = "res.users"
	_inherit = "res.users"
	
	komisi = fields.Boolean("Komisi", default=False)
	komisiflat = fields.Boolean("Komisi Flat", default = False)
	
class sale_order(models.Model):
	_name = "sale.order"
	_inherit = "sale.order"
	
	komisi_line_id = fields.Many2one("cli.komisi.line","komisi line id")
	iskomisi = fields.Boolean("Komisi Manual", default=False)