# -*- coding: utf-8 -*-

from odoo import models, fields, api

class reserva_hoteles(models.Model):
     _name = 'reserva_hoteles.reserva_hoteles'

     name = fields.Char()
     value = fields.Integer()
     value2 = fields.Float(compute="_value_pc", store=True)
     description = fields.Text()

     @api.depends('value')
     def _value_pc(self):
         self.value2 = float(self.value) / 100

class citys(models.Model):
	_name = 'reserva_hoteles.citys'
	name_city = fields.Text()
	description = fields.Text()
	location = fields.Text()
	countrys = fields.Text()
	list_hotels = fields.Many2one('reserva_hoteles.hotels')

class hotels (models.Model):
    _name = 'reserva_hoteles.hotels'
    name_hotel = fields.Text()
    photo_gallery = fields.Binary()
    descripcio = fields.Text()
    list_rooms = fields.Many2one('reserva_hoteles.rooms')
    valorations = fields.Integer()
    list_service = fields.Text()
    city = fields.One2many('reserva_hoteles.citys')

class rooms(models.Model):
    _name = 'reserva_hoteles.rooms'
    name = fields.Integer()
    beds_distribution = fields.Integer()
    photos = fields.Binary()
    price = fields.Float()
    description = fields.Text()
    hotel = fields.One2many('reserva_hoteles.hotels',name_hotel)
    reserve = fields.Integer('reserva_hoteles.reserve',reserve)
    
class reserve (models.Model):
    _name = 'reserva_hoteles.reserve'    
    reserve = fields.Integer()
    date_reserve_start = fields.Date()
    date_reserve_end = fields.Date()
    hotel = fields.Many2one('reserva_hoteles.hotels')
    room = fields.Many2one('reserva_hoteles.rooms')
