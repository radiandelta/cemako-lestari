# -*- coding: utf-8 -*-

from openerp import models, fields, api
import re
from mako.template import Template
from mako.lookup import TemplateLookup
import time
import os
import locale
import datetime

tpl_lookup = TemplateLookup('D:\Odoo addons\cli_do_dot')

cetak_fields = {'teks': {'type': 'text', 'default': 'Pencetakan sedang berlangsung.', 'readonly': True }}

cetak_form = '''<?xml version="1.0"?>
<form string="Cetak ke printer dotmatrix">
    <field name="teks" />
</form>'''

class stock_picking(models.Model):    
    _inherit = 'stock.picking'
  
    def cetak(self, cr, uid, ids, context):
        # Mendefinikan template report berdasarkan path modul terkait 
        tpl = tpl_lookup.get_template('picking.txt')
        tpl_line = tpl_lookup.get_template('picking_line.txt')
 
        # Mempersiapkan data-data yang diperlukan                
        user = self.pool.get('res.users').browse(cr, uid, uid)
        order = self.browse(cr, uid, ids)[0]            
        date = time.strftime('%d/%m/%Y %H:%M', time.strptime(order.date,'%Y-%m-%d %H:%M:%S'))   
        tglo=order.date        
        no = 0
        rows = []
        for line in order.move_lines:
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
                       do=order.no_pesan,
					   tglp=order.tgl_pesan,
					   nmp=order.nama_pesan,
                       user='('+ user.name +')')
                 
 
        # Membuat temporary file yang akan dicetak beserta pathnya   
        filename = 'c:/temp/%s.txt' % uid
        filename2 = '"c:\\temp\%s.txt"' % uid
        filename3 = '"c:\\temp\\text.txt"'
         
        # Mengisi file tersebut dengan data yang telah dirender
        f = open(filename, 'w')
        f.write(s)
        f.close()
         
        # Proses cetak dijalankan dan pastikan variabel nama_printer adalah nama printer yang anda setting atau tambahkan dengan webmin diatas
        os.system('type %s > %s' % (filename2,filename3))
         
        # Hapus file yang telah dicetak
        #os.remove(filename)
       
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
  
  
stock_picking()

