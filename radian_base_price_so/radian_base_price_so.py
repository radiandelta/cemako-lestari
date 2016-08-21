import logging
from openerp.osv import orm, fields
from openerp import api
import openerp.addons.decimal_precision as dp

_logger=logging.getLogger(__name__)

class res_partner(orm.Model):
	_name = "res.partner"
	_inherit = "res.partner"
	
	_columns = {
		'npwp':fields.char('NPWP', help='Diisi dengan nomor NPWP rekanan'),
	}
	
class res_users(orm.Model):
	_name = "res.users"
	_inherit = "res.users"
	
	_columns = {
		'rate_pd':fields.float('Rate PD(%)', help='Nilai rate untuk potongan PD 2', default=10.0),
	}
	

class sale_order_line(orm.Model):
	_name = 'sale.order.line'
	_inherit = 'sale.order.line'
	
	def _amount_line_pd(self, cr, uid, ids, field_name, arg, context=None):
		cur_obj = self.pool.get('res.currency')
		res = {}
		if context is None :
			context = {}
		for line in self.browse(cr, uid, ids, context=context):
			price1 = line.price_unit - int(line.price_unit*(line.discount/100))
			price2 = line.base_price
			qty = line.product_uom_qty
			pds = int(qty*(price1 - price2))
			cur = line.order_id.pricelist_id.currency_id
			res[line.id] = cur_obj.round(cr, uid, cur, pds)
		return res

	def _amount_line_net(self, cr, uid, ids, field_name, arg, context=None):
		cur_obj = self.pool.get('res.currency')
		res = {}
		if context is None :
			context = {}
		for line in self.browse(cr, uid, ids, context=context):
			price1 = line.price_unit - int(line.price_unit*(line.discount/100))
			price2 = line.base_price
			qty = line.product_uom_qty
			net = int(qty*price2)
			cur = line.order_id.pricelist_id.currency_id
			res[line.id] = cur_obj.round(cr, uid, cur, net)
		return res
		
	def _prepare_order_line_invoice_line(self, cr, uid, line, account_id=False, context=None):
		ret=super(sale_order_line,self)._prepare_order_line_invoice_line(cr, uid, line, account_id=False, context=context)
		if line.product_id:
			ret['base_price']=line.base_price
			ret['cetak']=line.cetak
			ret['diskonrp']=line.diskonrp
			ret['label']=line.label
		return ret
	
	_columns = {
		'base_price':fields.float('Base Price', required=True, digits_compute=dp.get_precision('Product Price'), readonly=True, states={'draft':[('readonly', False)]}),
		'pd_subtotal':fields.function(_amount_line_pd, string='PD', digits_compute=dp.get_precision('Account'), store=True),
		'net_subtotal':fields.function(_amount_line_net, string='NET', digits_compute=dp.get_precision('Account'), store=True),
		'cetak':fields.boolean('Cetak', default=True),
		'label':fields.selection((('Seyton','Seyton'),('Saver','Saver'),('Lain2','Lain2')),'Label', default='Lain2')
		}
	_default = {
		'base_price': 0.0,
	}

