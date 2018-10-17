# -*- coding: utf-8 -*-
from odoo import http

# class ReservaHoteles(http.Controller):
#     @http.route('/reserva_hoteles/reserva_hoteles/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/reserva_hoteles/reserva_hoteles/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('reserva_hoteles.listing', {
#             'root': '/reserva_hoteles/reserva_hoteles',
#             'objects': http.request.env['reserva_hoteles.reserva_hoteles'].search([]),
#         })

#     @http.route('/reserva_hoteles/reserva_hoteles/objects/<model("reserva_hoteles.reserva_hoteles"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('reserva_hoteles.object', {
#             'object': obj
#         })