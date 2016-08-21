# -*- coding: utf-8 -*-
from openerp import http

# class CliInvoice(http.Controller):
#     @http.route('/cli_invoice/cli_invoice/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cli_invoice/cli_invoice/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('cli_invoice.listing', {
#             'root': '/cli_invoice/cli_invoice',
#             'objects': http.request.env['cli_invoice.cli_invoice'].search([]),
#         })

#     @http.route('/cli_invoice/cli_invoice/objects/<model("cli_invoice.cli_invoice"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cli_invoice.object', {
#             'object': obj
#         })