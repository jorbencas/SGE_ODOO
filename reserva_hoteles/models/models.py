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
	name = fields.Text()
	description = fields.Text()
	location = fields.Text()
	countrys = fields.Many2many('res.country','Pais')
	listHotels = fields.Many2one('reserva_hoteles.hotels')

class hotels (models.Model):
    _name = 'reserva_hoteles.hotels'
    name = fields.Text()
    photoGallery = fields.One2many('reserva_hoteles.photogallery','photo')
    descripcio = fields.Text()
    listRooms = fields.Many2one('reserva_hoteles.rooms')
    valorations = fields.Integer()
    listServices = fields.Many2many('reserva_hoteles.reserve')
    city = fields.One2many('reserva_hoteles.citys','name')

class rooms (models.Model):
    _name = 'reserva_hoteles.rooms'
    name = fields.Integer()
    beds = fields.Integer()
    photos = fields.Many2many('reserva_hoteles.photogallery')
    price = fields.Float()
    description = fields.Text()
    hotel = fields.One2many('reserva_hoteles.hotels','name')
    services = fields.Many2one('reserva_hoteles.reserve')
    
class reserve (models.Model):
    _name = 'reserva_hoteles.reserve'    
    name = fields.Integer()
    datestart = fields.Date()
    dateend = fields.Date()
    hotel = fields.Many2one('reserva_hoteles.hotels')
    room = fields.Many2one('reserva_hoteles.rooms')

class photoGallery (models.Model):
    _name = 'reserva_hoteles.photogallery'
    photo = fields.Binary()