# -*- coding: utf-8 -*-
from odoo import http

# class Pruebas1(http.Controller):
#     @http.route('/pruebas1/pruebas1/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/pruebas1/pruebas1/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('pruebas1.listing', {
#             'root': '/pruebas1/pruebas1',
#             'objects': http.request.env['pruebas1.pruebas1'].search([]),
#         })

#     @http.route('/pruebas1/pruebas1/objects/<model("pruebas1.pruebas1"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('pruebas1.object', {
#             'object': obj
#         })