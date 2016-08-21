# -*- coding: utf-8 -*-
from openerp import http

# class CliInvDot(http.Controller):
#     @http.route('/cli_inv_dot/cli_inv_dot/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cli_inv_dot/cli_inv_dot/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('cli_inv_dot.listing', {
#             'root': '/cli_inv_dot/cli_inv_dot',
#             'objects': http.request.env['cli_inv_dot.cli_inv_dot'].search([]),
#         })

#     @http.route('/cli_inv_dot/cli_inv_dot/objects/<model("cli_inv_dot.cli_inv_dot"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cli_inv_dot.object', {
#             'object': obj
#         })