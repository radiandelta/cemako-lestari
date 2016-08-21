# -*- coding: utf-8 -*-
from openerp import http

# class CliPl(http.Controller):
#     @http.route('/cli_pl/cli_pl/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cli_pl/cli_pl/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('cli_pl.listing', {
#             'root': '/cli_pl/cli_pl',
#             'objects': http.request.env['cli_pl.cli_pl'].search([]),
#         })

#     @http.route('/cli_pl/cli_pl/objects/<model("cli_pl.cli_pl"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cli_pl.object', {
#             'object': obj
#         })