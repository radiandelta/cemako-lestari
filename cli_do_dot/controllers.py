# -*- coding: utf-8 -*-
from openerp import http

# class CliDoDot(http.Controller):
#     @http.route('/cli_do_dot/cli_do_dot/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cli_do_dot/cli_do_dot/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('cli_do_dot.listing', {
#             'root': '/cli_do_dot/cli_do_dot',
#             'objects': http.request.env['cli_do_dot.cli_do_dot'].search([]),
#         })

#     @http.route('/cli_do_dot/cli_do_dot/objects/<model("cli_do_dot.cli_do_dot"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cli_do_dot.object', {
#             'object': obj
#         })