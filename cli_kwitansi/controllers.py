# -*- coding: utf-8 -*-
from openerp import http

# class CliKwitansi(http.Controller):
#     @http.route('/cli_kwitansi/cli_kwitansi/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cli_kwitansi/cli_kwitansi/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('cli_kwitansi.listing', {
#             'root': '/cli_kwitansi/cli_kwitansi',
#             'objects': http.request.env['cli_kwitansi.cli_kwitansi'].search([]),
#         })

#     @http.route('/cli_kwitansi/cli_kwitansi/objects/<model("cli_kwitansi.cli_kwitansi"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cli_kwitansi.object', {
#             'object': obj
#         })