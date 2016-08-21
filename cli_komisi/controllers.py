# -*- coding: utf-8 -*-
from openerp import http

# class CliKomisi(http.Controller):
#     @http.route('/cli_komisi/cli_komisi/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cli_komisi/cli_komisi/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('cli_komisi.listing', {
#             'root': '/cli_komisi/cli_komisi',
#             'objects': http.request.env['cli_komisi.cli_komisi'].search([]),
#         })

#     @http.route('/cli_komisi/cli_komisi/objects/<model("cli_komisi.cli_komisi"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cli_komisi.object', {
#             'object': obj
#         })