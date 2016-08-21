# -*- coding: utf-8 -*-
from openerp import http

# class RadianGlobalDiskon(http.Controller):
#     @http.route('/radian_global_diskon/radian_global_diskon/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/radian_global_diskon/radian_global_diskon/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('radian_global_diskon.listing', {
#             'root': '/radian_global_diskon/radian_global_diskon',
#             'objects': http.request.env['radian_global_diskon.radian_global_diskon'].search([]),
#         })

#     @http.route('/radian_global_diskon/radian_global_diskon/objects/<model("radian_global_diskon.radian_global_diskon"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('radian_global_diskon.object', {
#             'object': obj
#         })