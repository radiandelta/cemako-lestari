# -*- coding: utf-8 -*-
from openerp import http

# class CliOrder(http.Controller):
#     @http.route('/cli_order/cli_order/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cli_order/cli_order/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('cli_order.listing', {
#             'root': '/cli_order/cli_order',
#             'objects': http.request.env['cli_order.cli_order'].search([]),
#         })

#     @http.route('/cli_order/cli_order/objects/<model("cli_order.cli_order"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cli_order.object', {
#             'object': obj
#         })