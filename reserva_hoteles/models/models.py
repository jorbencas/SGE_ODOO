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
    photoSmall = fields.Binary(compute='_get_resized_image_hotel',store=True)
    description = fields.Text()
    listRooms = fields.One2many('reserva_hoteles.rooms','name')
    valorations = fields.Selection([('1', '⭐'), ('2', '⭐⭐'), ('3', '⭐⭐⭐'), ('4', '⭐⭐⭐⭐'), ('5', '⭐⭐⭐⭐⭐')])
    listServices = fields.Many2many('reserva_hoteles.services')
    city = fields.Many2one('reserva_hoteles.citys','name')
    comments = fields.One2many('reserva_hoteles.comments','name')

    @api.depends('photoGallery')
    def _get_resized_image_hotel(self):
        for p in self:
               	if len(p.photoGallery) > 0:
                    data = tools.image_get_resized_images(p.photoGallery[0].photo)
                    p.photoSmall = data['image_small']
                else:
                    print("Este hotel no tiene fotos...")


class rooms (models.Model):
    _name = 'reserva_hoteles.rooms'
    name = fields.Integer()
    beds = fields.Selection([('0','Una Cama'),('1','Dos Camas'),('2','Cama de Matrimonio'),('3','Cama de matromonio mas cama infantil') ],'Type', default='1')
    photos = fields.One2many('reserva_hoteles.photogallery','photo')
    #photo_small = fields.Binary(compute='_get_resized_image',store=True)
    price = fields.Float(default=1)
    description = fields.Text(default="Habitación grande, espaciosa y con gran luminosidad.")
    hotel = fields.Many2one('reserva_hoteles.hotels','name')
    city = fields.Many2one('reserva_hoteles.citys', related='hotel.city', readonly=True)
   
    #@api.depends('photos')
    #def _get_resized_image(self):
	#    for p in self:
	#	    if len(p.photos) > 0:
    #            p.photo_small = tools.image_get_resized_images(p.photos[0].photo)
    #        else:
    #            print("Este hotel no tiene fotos...")



class reserve (models.Model):
    _name = 'reserva_hoteles.reserve'    
    name = fields.Char()
    datestart = fields.Date()
    dateend = fields.Date()
    client = fields.Many2one('res.partner','name')
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
    _name = 'reserva_hoteles.services'
    name = fields.Selection([("0","Parking"),("1","Roomservice"),("2","jacuzzi")],'Type', default='2')
    photo = fields.Binary()
    hotel = fields.Many2many('reserva_hoteles.hotels')

class comments (models.Model):
    _name = 'reserva_hoteles.comments'
    name = fields.Text()
    description = fields.Text()
    hotel = fields.Many2many('reserva_hoteles.hotels')
