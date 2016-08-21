# -*- coding: utf-8 -*-
from openerp.osv import orm, fields
import openerp.addons.decimal_precision as dp
#from openerp.osv import osv

class sale_order(orm.Model):
	_name = 'sale.order'
	_inherit = 'sale.order'
	
	
	def _amount_all(self, cr, uid, ids, field_name, arg, context=None):
		cur_obj = self.pool.get('res.currency')
		res = super(sale_order, self)._amount_all(cr, uid, ids, field_name, arg, context)
		for order in self.browse(cr, uid, ids, context=context):
			res[order.id] = {
				'amount_untaxed': 0.0,
				'amount_tax':0.0,
				'amount_total': 0.0,
				'diskon':0.0,
				'total_pd':0.0,
				'total_chem':0.0,
				'total_lubs':0.0,
				'total_othr':0.0,
				'total_net':0.0,
				'pd2':0.0,
			}
			val = val1 = val2 = val3 = val4 = val5 = val7 = val8 = val9 = val10= val11 = val13= val14= 0.0
			cur = order.pricelist_id.currency_id
			rpd = float(order.pd_rate)
			for line in order.order_line :
				vars = line.product_id.product_tmpl_id.categ_id.id
				if vars == 3:
					val7 += line.net_subtotal
				elif vars == 4:
					val8 += line.net_subtotal
				else:
					val9 += line.net_subtotal
				val1 += line.price_subtotal
				val2 += line.diskonrp
				val3 += line.pd_subtotal
				val4 += line.net_subtotal
				val += self._amount_line_tax(cr, uid, line, context=context)
			if val>0 :
				val = int((val1-val2)*0.1)
			val3 = val1 - val2 - val4
			val5 = int(val3*float(rpd)/100)
			val6 = val3-val5
			if order.iskomisi == True:
				val10 = order.komisi_lubs_man
				val11 = order.komisi_chem_man
			else:
				val10 = int(val7 * (order.rate_lubs/100))
				val11 = int(val8 * (order.rate_chem/100))
			val12 = val10+val11
			val13 = int(val12 * (float(order.komisi_rate)/100))
			val14 = val12 - val13
			res[order.id]['amount_tax'] = cur_obj.round(cr, uid, cur, val)
			res[order.id]['diskon']=cur_obj.round(cr, uid, cur, val2)
			res[order.id]['total_pd']=cur_obj.round(cr, uid, cur, val6)
			res[order.id]['total_lubs']=cur_obj.round(cr,uid,cur, val7)
			res[order.id]['komisi_lubs']=cur_obj.round(cr,uid,cur, val10)
			res[order.id]['total_chem']=cur_obj.round(cr,uid,cur, val8)
			res[order.id]['komisi_chem']=cur_obj.round(cr,uid,cur, val11)
			res[order.id]['total_komisi']=cur_obj.round(cr,uid,cur, val12)
			res[order.id]['total_othr']=cur_obj.round(cr,uid,cur, val9)
			res[order.id]['total_net']=cur_obj.round(cr, uid, cur, val4)
			res[order.id]['pd1']=cur_obj.round(cr, uid, cur, val3)
			res[order.id]['pd2']=cur_obj.round(cr, uid, cur, val5)
			res[order.id]['amount_untaxed'] = cur_obj.round(cr, uid, cur, val1)
			res[order.id]['amount_total'] = res[order.id]['amount_untaxed']+res[order.id]['amount_tax']-res[order.id]['diskon']
			res[order.id]['komisi1'] = cur_obj.round(cr,uid, cur, val12)
			res[order.id]['grand_komisi'] = cur_obj.round(cr, uid, cur, val13)
		return res
		
	def _get_order(self, cr, uid, ids, context=None):
		result = {}
		for line in self.pool.get('sale.order.line').browse(cr, uid, ids, context=context):
			result[line.order_id.id] = True
		return result.keys()
		 
	_columns = {
		'diskon':fields.function(_amount_all, digits_compute=dp.get_precision('Account'), string='Diskon',
			store={'sale.order.line':(_get_order, None, 10),}, multi="sums", help="Diskon Global", 
			track_visibility='always'),
		'total_pd':fields.function(_amount_all, digits_compute=dp.get_precision('Account'), string='Total PD',
			store={'sale.order.line':(_get_order, None, 10),}, multi="sums", help="Total PD",
			track_visibility='always'),
		'total_net':fields.function(_amount_all, digits_compute=dp.get_precision('Account'), string='Total Net',
			store={'sale.order.line':(_get_order, None, 10),}, multi="sums", help="Total Net",
			track_visibility='always'),
		'total_chem':fields.function(_amount_all, digits_compute=dp.get_precision('Account'), string='Total Chemical',
			store={'sale.order.line':(_get_order, None, 10),}, multi="sums", help="Total Net Chemical",
			track_visibility='always'),
		'total_lubs':fields.function(_amount_all, digits_compute=dp.get_precision('Account'), string='Total Lubricant',
			store={'sale.order.line':(_get_order, None, 10),}, multi="sums", help="Total Net Lubricant",
			track_visibility='always'),
		'total_othr':fields.function(_amount_all, digits_compute=dp.get_precision('Account'), string='Total Lain-2',
			store={'sale.order.line':(_get_order, None, 10),}, multi="sums", help="Total Net Lain2",
			track_visibility='always'),
		'pd1':fields.function(_amount_all, digits_compute=dp.get_precision('Account'), string='PD',
			store={'sale.order.line':(_get_order, None, 10),}, multi="sums", help="PD",
			track_visibility='always'),
		'pd2':fields.function(_amount_all, digits_compute=dp.get_precision('Account'), string='PD 1',
			store={'sale.order.line':(_get_order, None, 10),}, multi="sums", help="PD 1",
			track_visibility='always'),
		'pd_rate':fields.selection((('0','0'),('5','5'),('10','10')),'Rate PD(%)',default='10'),
		'komisi_rate':fields.selection((('0','0'),('5','5'),('10','10')),'Rate Komisi1(%)',default='10'),
		'tanggal_pd':fields.date(string="Tanggal Cair", readonly=True),
		'nomor_fp':fields.char(string='Nomor FP', help='Masukkan nomor faktur pajak'),
		'rate_chem':fields.float(string="Rate Chemical", help="Rate komisi chemical", default=0),
		'rate_lubs':fields.float(string="Rate Lubricant", help="Rate komisi lubricant", default = 0),
		'komisi_chem':fields.function(_amount_all, digits_compute=dp.get_precision('Account'), string="Komisi Chemical",
			store={'sale.order.line':(_get_order, None, 10),}, multi='sums', help="Komisi Chemical", track_visibility="always"),
		'komisi_chem_man':fields.float(string='Komisi Chemical', default = 0),
		'komisi_lubs':fields.function(_amount_all, digits_compute=dp.get_precision('Account'), string="Komisi Lubricants",
			store={'sale.order.line':(_get_order, None, 10),}, multi='sums', help="Komisi Lubricants", track_visibility="always"),
		'komisi_lubs_man':fields.float(string='Komisi Lubricants', default=0),
		'total_komisi':fields.function(_amount_all, digits_compute=dp.get_precision('Account'), string="Komisi",
			store={'sale.order.line':(_get_order, None, 10),}, multi="sums", help="Total Komisi", track_visibility="always"),
		'komisi1':fields.function(_amount_all,digits_compute=dp.get_precision('Account'), string='Komisi 1',
			store={'sale.order.line':(_get_order, None, 10),}, multi="sums", help="Total Komisi", track_visibility="always"),
		'grand_komisi':fields.function(_amount_all,digits_compute=dp.get_precision('Account'), string='Total Komisi',
			store={'sale.order.line':(_get_order, None, 10),}, multi="sums", help="Total Komisi", track_visibility="always"),
		'cabang':fields.boolean("Penjualan Cabang", default=False),
		'dsp_total_chem': fields.related('total_chem',type="float", string="Total Net Chem"),
		'dsp_total_lubs': fields.related('total_lubs',type="float", string="Total Net Lubs"),
		'dsp_total_othr': fields.related('total_othr',type="float", string="Total Net Lain-2"),
		'dsp_total_net': fields.related('total_net',type="float", string="Total Net"),
		}

		

class sale_order_line(orm.Model):
	_name = 'sale.order.line'
	_inherit = 'sale.order.line'
	
	_columns = {
		'diskonrp':fields.float('Diskon(Rp)'),
	}

