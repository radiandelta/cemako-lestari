# -*- coding: utf-8 -*-

from openerp import models, fields, api
import re
from mako.template import Template
from mako.lookup import TemplateLookup
import time
import os
import locale
import datetime

tpl_lookup = TemplateLookup('D:\modul Odoo\cli_do_dot')

cetak_fields = {'teks': {'type': 'text', 'default': 'Pencetakan sedang berlangsung.', 'readonly': True }}

cetak_form = '''<?xml version="1.0"?>
<form string="Cetak ke printer dotmatrix">
    <field name="teks" />
</form>'''

class account_invoice(models.Model):    
    _inherit = 'account.invoice'
	
	def terbilang(angka):
		hasil = ""
		if angka < 12:
			if angka == 1:
				hasil += "satu "
			elif angka == 2:
				hasil += "dua "
			elif angka == 3:
				hasil += "tiga "
			elif angka == 4:
				hasil += "empat "
			elif angka == 5:
				hasil += "lina "
			elif angka == 6:
				hasil += "enam "
			elif angka == 7:
				hasil += "tujuh "
			elif angka == 8:
				hasil += "delapan "
			elif angka == 9:
				hasil += "sembilan "
			elif angka == 10:
				hasil += "sepuluh "
			elif angka == 11:
				hasil += "sebelas "
		elif angka < 100:
			if angka < 20:
				hasil += terbilang(angka%10)+"belas "
			else:
				hasil += terbilang(int(angka/10))+"puluh "+terbilang(angka%10)
		elif angka < 1000:
			if angka < 200:
				hasil += "seratus "+terbilang(angka%100)
			else:
				hasil += terbilang(int(angka/100))+"ratus "+terbilang(angka%100)
		elif angka < 1000000:
			if angka < 2000:
				hasil += "seribu "+terbilang(angka%1000)
			else:
				hasil += terbilang(int(angka/1000))+"ribu "+terbilang(angka%1000)
		elif angka < 1000000000:
			hasil += terbilang(int(angka/1000000))+"juta "+terbilang(angka%1000000)
		elif angka < 1000000000000:
			hasil += terbilang(int(angka/1000000000))+"miliar "+terbilang(angka%1000000000)
		else:
			hasil = "Angka lebih dari 999999999"

		return hasil


            

  
    def cetak(self, cr, uid, ids, context):
        # Mendefinikan template report berdasarkan path modul terkait 
        tpl = tpl_lookup.get_template('picking.txt')
        tpl_line = tpl_lookup.get_template('picking_line.txt')
 
        # Mempersiapkan data-data yang diperlukan                
        user = self.pool.get('res.users').browse(cr, uid, uid)
        invoice = self.browse(cr, uid, ids)[0]            
        date = time.strftime('%d/%m/%Y %H:%M', time.strptime(order.date,'%Y-%m-%d %H:%M:%S'))   
        tglo=order.date        
        no = 0
        rows = []
        for line in invoice.invoice_lines:
            no += 1
            s = tpl_line.render(no=str(no),
                                code="Kode Barang", #line.product_id.code,
								uom=line.product_uom.name,
                                name=line.product_id.name_template, #line.product_id.name_template,
								desk = line.product_tmpl_id.description.strip()[:49],
                                qty="{:,.0f}".format(line.product_uom_qty).replace(",","."))
            rows.append(s)
         
        # Merender data yang telah disiapkan ke dalam template report text

        s = tpl.render(id=order.nomor_do, #order.name,
                       tgl=tglo[8:10]+"-"+tglo[5:7]+"-"+tglo[:4],
                       pelanggan=order.partner_id.name,
					   alamat=order.partner_id.street,
					   kota=order.partner_id.city,
                       rows=rows,
                       po=order.origin,
                       do=order.nomor_do,
                       user='('+ user.name +')')
                 
 
        # Membuat temporary file yang akan dicetak beserta pathnya   
        filename = 'c:/temp/%s.txt' % uid
         
        # Mengisi file tersebut dengan data yang telah dirender
        f = open(filename, 'w')
        f.write(s)
        f.close()
         
        # Proses cetak dijalankan dan pastikan variabel nama_printer adalah nama printer yang anda setting atau tambahkan dengan webmin diatas
        os.system('lpr -S 192.168.1.7 -P ip2700 %s' % filename)
         
        # Hapus file yang telah dicetak
        os.remove(filename)
       
        return True
  
    states = {
        'init': {
            'actions': [cetak],
            'result': {'type':'form',
                       'arch':cetak_form,
                       'fields': cetak_fields,
                       'state':[]
                      }
            },
        }
  
  
account_invoice()

# class cli_inv_dot(models.Model):
#     _name = 'cli_inv_dot.cli_inv_dot'

#     name = fields.Char()