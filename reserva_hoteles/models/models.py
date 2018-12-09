# -*- coding: utf-8 -*-
from odoo import models, fields, api, tools
from odoo.exceptions import ValidationError
import datetime

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
    photoGallery = fields.Many2many('reserva_hoteles.hotelgallery')
    photomainhotel = fields.Binary(compute='_get_resized_image_hotel',store=True)
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
                 p.photomainhotel = p.photoGallery[0].photo
            else:
                 print("Este hotel no tiene fotos...")


class rooms (models.Model):
    _name = 'reserva_hoteles.rooms'
    name = fields.Integer()
    beds = fields.Selection([('0','Una Cama'),('1','Dos Camas'),('2','Cama de Matrimonio'),('3','Cama de matromonio mas cama infantil') ],'Type', default='1')
    photos = fields.Many2many('reserva_hoteles.photogallery')
    # photomainroom = fields.Binary(compute='_get_resized_image',store=True)
    price = fields.Float(default=1)
    description = fields.Text(default="Habitación grande, espaciosa y con gran luminosidad.")
    hotel = fields.Many2one('reserva_hoteles.hotels','name')
    city = fields.Many2one('reserva_hoteles.citys', related='hotel.city', readOnly=True)
    reserve = fields.One2many('reserva_hoteles.reserve','name')
    avaible = fields.Char(string="Estado", compute='_getestado', readOnly=True)

    # @api.depends('photos')
    # def _get_resized_image(self):
	#     for record in self:
	#  	    if len(record.photos) > 0:
    #             # record.photomainroom = record.photos[0].photo
    #             print("Este hotel no tiene fotos...")
    #         else:
    #             print("Este hotel no tiene fotos...")

    @api.depends('reserve')
    def _getestado(self):
        for record in self:
            # print(len(record.reserve))
            if len(record.reserve) > 0:
                for valorreserve in record.reserve:
                    if(valorreserve.dateend < str(datetime.datetime.today())):
                        record.avaible="Libre"
                    else:
                        record.avaible="Ocupado"
            else:
                record.avaible="Libre"

class reserve (models.Model):
    _name = 'reserva_hoteles.reserve'
    name = fields.Text(string="Nombre de la reserva")
    datestart = fields.Date()
    dateend = fields.Date()
    client = fields.Many2one('res.partner', 'Nombre del cliente')
    room = fields.Many2one('reserva_hoteles.rooms','reserve')
    hotel = fields.Many2one('reserva_hoteles.hotels', related='room.hotel', readonly=True,store=True)
    city = fields.Many2one('reserva_hoteles.citys', related='hotel.city', readonly=True)

    @api.constrains('datestart','dateend')
    def _comprobar_reserva(self):
        for record in self:
            variable = self.search_count([('id','!=',record.id),('dateend','>=',record.datestart),('dateend','<=',record.dateend)])
            variable2 = self.search([('id','!=',record.id),('dateend','>=',record.datestart)('datestart','<=',record.dateend)])
            for valor in variable2:
                print(self.name)
                print(valor.name)

            if variable > 0:
                raise ValidationError("Se solapan las 2 fechas \n"+ self.name + "com " + valor.name)

class photoHotel (models.Model):
    _name='reserva_hoteles.hotelgallery'
    name = fields.Text()
    photo = fields.Binary()
    # hotel = fields.Many2one('reserva_hoteles.hotels','name')

class photoGallery (models.Model):
    _name = 'reserva_hoteles.photogallery'
    name = fields.Text()
    photo = fields.Binary()
    # room = fields.Many2one('reserva_hoteles.rooms','name')

class services (models.Model):
    _name = 'reserva_hoteles.services'
    name = fields.Selection([("0","Parking"),("1","Roomservice"),("2","jacuzzi")],'Type', default='2')
    photo = fields.Binary()

class comments (models.Model):
    _name = 'reserva_hoteles.comments'
    name = fields.Text()
    description = fields.Text()
    clients = fields.Many2one("res.partner", "Nombre del cliente")
    photoclient = fields.Binary(related='clients.image',store=True)
    nameclient = fields.Char(related='clients.name')
    valorations = fields.Selection([('1', '⭐'), ('2', '⭐⭐'), ('3', '⭐⭐⭐'), ('4', '⭐⭐⭐⭐'), ('5', '⭐⭐⭐⭐⭐')],default='5')
    hotel = fields.Many2one('reserva_hoteles.hotels',"comments")
