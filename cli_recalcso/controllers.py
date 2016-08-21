# -*- coding: utf-8 -*-
from openerp import http

# class CliRecalcso(http.Controller):
#     @http.route('/cli_recalcso/cli_recalcso/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cli_recalcso/cli_recalcso/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('cli_recalcso.listing', {
#             'root': '/cli_recalcso/cli_recalcso',
#             'objects': http.request.env['cli_recalcso.cli_recalcso'].search([]),
#         })

#     @http.route('/cli_recalcso/cli_recalcso/objects/<model("cli_recalcso.cli_recalcso"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cli_recalcso.object', {
#             'object': obj
#         })