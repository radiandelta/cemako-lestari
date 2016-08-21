# -*- coding: utf-8 -*-
from openerp import http

# class CliRealisasi(http.Controller):
#     @http.route('/cli_realisasi/cli_realisasi/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cli_realisasi/cli_realisasi/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('cli_realisasi.listing', {
#             'root': '/cli_realisasi/cli_realisasi',
#             'objects': http.request.env['cli_realisasi.cli_realisasi'].search([]),
#         })

#     @http.route('/cli_realisasi/cli_realisasi/objects/<model("cli_realisasi.cli_realisasi"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cli_realisasi.object', {
#             'object': obj
#         })