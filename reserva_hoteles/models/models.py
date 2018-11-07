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
	countrys = fields.Many2one('res.country','Pais')
	listHotels = fields.One2many('reserva_hoteles.hotels', 'name')

class hotels (models.Model):
    _name = 'reserva_hoteles.hotels'
    name = fields.Text()
    photoGallery = fields.One2many('reserva_hoteles.hotelgallery','photo')
    description = fields.Text()
    listRooms = fields.One2many('reserva_hoteles.rooms','name')
    valorations = fields.Selection([('1', '⭐'), ('2', '⭐⭐'), ('3', '⭐⭐⭐'), ('4', '⭐⭐⭐⭐'), ('5', '⭐⭐⭐⭐⭐')])
    listServices = fields.Many2many('reserva_hoteles.service')
    city = fields.Many2one('reserva_hoteles.citys','name')
    comments = fields.One2many('reserva_hoteles.comments','name')

class rooms (models.Model):
    _name = 'reserva_hoteles.rooms'
    name = fields.Integer()
    beds = fields.Selection([('1','Una Cama'),('2','Dos Camas'),('3','Cama de Matrimonio'),('4','Cama de matromonio mas cama infantil') ],'Type', default='1')
    photos = fields.One2many('reserva_hoteles.photogallery','photo')
    price = fields.Float(default=1)
    description = fields.Text(default="Habitación grande, espaciosa y con gran luminosidad.")
    hotel = fields.Many2one('reserva_hoteles.hotels','name')
    city = fields.Many2one('reserva_hoteles.citys', related='hotel.city', readonly=True)

class reserve (models.Model):
    _name = 'reserva_hoteles.reserve'    
    name = fields.Char()
    datestart = fields.Date()
    dateend = fields.Date()
    client = fields.Many2many('res.partner')
    room = fields.Many2one('reserva_hoteles.rooms','name')
    hotel = fields.Many2one('reserva_hoteles.hotels', related='room.hotel', readonly=True)
    city = fields.Many2one('reserva_hoteles.citys', related='hotel.city', readonly=True)

class photoHotel (models.Model):
    _name='reserva_hoteles.hotelgallery'
    name = fields.Text()
    photo = fields.Binary()
    hotel = fields.Many2one('reserva_hoteles.hotels','name')

class photoGallery (models.Model):
    _name = 'reserva_hoteles.photogallery'
    name = fields.Text()
    photo = fields.Binary()
    room = fields.Many2one('reserva_hoteles.rooms','name')

class services (models.Model):
    _name = 'reserva_hoteles.service'
    name = fields.Selection([("1","Parking"),("2","Roomservice"),("3","Sauna")],'Type', default='2')
    photo = fields.Binary()
    hotel = fields.One2many('reserva_hoteles.hotels','name')

class comments (models.Model):
    _name = 'reserva_hoteles.comments'
    name = fields.Text()
    description = fields.Text()
    hotel = fields.Many2one('reserva_hoteles.hotels','name')