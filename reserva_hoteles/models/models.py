# -*- coding: utf-8 -*-
from odoo import models, fields, api, tools
from odoo.exceptions import ValidationError
import datetime

class citys(models.Model):
	_name = 'reserva_hoteles.citys'
	name = fields.Text('Ciudad')
	description = fields.Text('Descripcion')
	location = fields.Text('Localización')
	countrys = fields.Many2one('res.country','Pais')
	listHotels = fields.One2many('reserva_hoteles.hotels', 'city')

class hotels (models.Model):
    _name = 'reserva_hoteles.hotels'
    name = fields.Text('Hotel')
    photoGallery = fields.Many2many('reserva_hoteles.hotelgallery')
    photomainhotel = fields.Binary(compute='_get_resized_image_hotel',store=True)
    description = fields.Text('Dscripción')
    listRooms = fields.One2many('reserva_hoteles.rooms','name')
    valorations = fields.Selection([('1', '⭐'), ('2', '⭐⭐'), ('3', '⭐⭐⭐'), ('4', '⭐⭐⭐⭐'), ('5', '⭐⭐⭐⭐⭐')])
    listServices = fields.Many2many('reserva_hoteles.services')
    city = fields.Many2one('reserva_hoteles.citys','Ciudad')
    countrys = fields.Char(related='city.countrys.name', store=True, readOnly=True)
    comments = fields.One2many('reserva_hoteles.comments','name')
    reserve = fields.One2many('reserva_hoteles.reserve','hotel')
    oldreserve = fields.One2many('reserva_hoteles.reserve','hotel', compute='get_old_reserve')
    presentreserve = fields.One2many('reserva_hoteles.reserve','hotel', compute='get_present_reserve')
    futurereserve = fields.One2many('reserva_hoteles.reserve','hotel', compute='get_future_reserve')

    @api.one
    @api.depends('reserve')
    def get_old_reserve(self):
        self.oldreserve = self.env['reserva_hoteles.reserve'].search([('hotel', '=', self.name), ('datestart',  '<',  datetime.datetime.now()), ('dateend', '<',  datetime.datetime.now())])     
    
    @api.one
    @api.depends('reserve')
    def get_present_reserve(self):
        self.presentreserve = self.env['reserva_hoteles.reserve'].search([('hotel', '=', self.name), ('datestart', '>',  datetime.datetime.now()), ('dateend', '<',  datetime.datetime.now())])      
    
    @api.one
    @api.depends('reserve')
    def get_future_reserve(self):
        self.futurereserve = self.env['reserva_hoteles.reserve'].search([('hotel', '=', self.name), ('datestart', '>',  datetime.datetime.now()), ('dateend', '>',  datetime.datetime.now())])

    @api.depends('photoGallery')
    def _get_resized_image_hotel(self):
        for p in self:
            print(p.city.name)
            if len(p.photoGallery) > 0:
                 p.photomainhotel = p.photoGallery[0].photo
            else:
                 print("Este hotel no tiene fotos...")

class rooms (models.Model):
    _name = 'reserva_hoteles.rooms'
    name = fields.Integer('Numero de Habitación')
    beds = fields.Selection([('0','Una Cama'),('1','Dos Camas'),('2','Cama de Matrimonio'),('3','Cama de matromonio mas cama infantil') ],'Numero de camas', default='1')
    photos = fields.Many2many('reserva_hoteles.photogallery')
    photomainroom = fields.Binary(compute='_get_resized_image',store=True)
    price = fields.Float(default=1)
    description = fields.Text(default="Habitación grande, espaciosa y con gran luminosidad.")
    hotel = fields.Many2one('reserva_hoteles.hotels','Lista de habitaciones')
    city = fields.Many2one('reserva_hoteles.citys', related='hotel.city',readOnly=True)
    reserve = fields.One2many('reserva_hoteles.reserve','name')
    avaible = fields.Char(string="Estado", compute='_getestado', readOnly=True)

    @api.depends('photos')
    def _get_resized_image(self):
        for record in self:
            print(len(record.photos))
            if len(record.photos) > 0:
                record.photomainroom = record.photos[0].photo
            else:
                print("Este hotel no tiene fotos...")

    @api.depends('reserve')
    def _getestado(self):
        for record in self:
            if len(record.reserve) > 0:
                for valorreserve in record.reserve:
                    if(valorreserve.dateend < str(datetime.datetime.today())):
                        record.avaible="Libre"
                    else:
                        record.avaible="Ocupado"
            else:
                record.avaible="Libre"

class sale_order_line_inherit(models.Model):
    _name='sale.order.line'
    _inherit='sale.order.line'
    reserve = fields.Many2one('reserva_hoteles.reserve', 'Linea de Venta', Store=True)
    hotel = fields.Many2one('reserva_hoteles.hotel', related='reserve.hotel', readOnly=True)
    room_sale_order_line_inherit = fields.Integer(related='reserve.room.name');
    datestart_inherit = fields.Date(related='reserve.datestart', readOnly=True);
    dateend_inherit = fields.Date(related='reserve.dateend', readOnly=True);
    quantity = fields.Float(compute='get_reserve_quantity');

    @api.one
    @api.depends('reserve')
    def get_reserve_quantity(self):
        for record in self:
	        record.quantity = len(record.reserve)

class reserve (models.Model):
    _name = 'reserva_hoteles.reserve'
    name = fields.Text(string="Nombre de la reserva")
    datestart = fields.Date('Fecha de Inicio')
    dateend = fields.Date('Fecha de fin')
    client = fields.Many2one('res.partner', 'Nombre del cliente')
    room = fields.Many2one('reserva_hoteles.rooms','Habitacion')
    hotel = fields.Many2one('reserva_hoteles.hotels','Hotel', related='room.hotel', readonly=True,store=True)
    city = fields.Many2one('reserva_hoteles.citys','Ciudad', related='hotel.city', readonly=True)
    sale_line = fields.One2many('sale.order.line','reserve')
    days = fields.Text(default=1, compute="get_days_reserve")

    @api.one
    @api.depends('datestart','dateend')
    def get_days_reserve(self):
        for r in self:
            date_format = "%Y-%m-%d";
            d_start = datetime.datetime.strptime(r.datestart,date_format)
            d_end = datetime.datetime.strptime(r.dateend,date_format)
            r.days = d_end - d_start

    @api.onchange('datestart','dateend')
    def _manyana(self):
        for record in self:
            if record.dateend and record.datestart:

                fmt='%Y-%m-%d'
                datestart=datetime.datetime.strptime(str(record.datestart),fmt)
                dateend=datetime.datetime.strptime(str(record.dateend),fmt)
                if dateend < datestart:
                    record.dateeend = datestart + datetime.timedelta(days=1)
                    print(record.fechaFinal)
                    return {
                        'warning': {
                            'title': "Algo ha ocurrido mal",
                            'message': "No puedes insertar un dia antes de la fecha de inicio",
                        }
                    }
                else:
                    print(" No hay error!")
            elif record.datestart:
                fmt = '%Y-%m-%d'
                data = datetime.datetime.strptime(str(record.datestart), fmt)
                record.dateend = data + datetime.timedelta(days=1)

    @api.constrains('datestart','dateend')
    def _comprobar_reserva(self):
        for record in self:
            variable = self.search_count([('id', '!=', record.id),('room.id', '=', record.room.id) ,('dateend', '>=', record.datestart), ('datestart','<=', record.dateend)])
            variable2 = self.search([('id', '!=', record.id),('room.id', '=', record.room.id), ('dateend', '>=', record.datestart), ('datestart','<=', record.dateend)])

            for valor in variable2:
                print(self.name)
                print(valor.name)

            if variable > 0:
                raise ValidationError("Se solapan las 2 fechas \n"+ self.name + "com " + valor.name)

    @api.one
    def crear_venta(self):
        sale_id = self.env['sale.order'].create({'partner_id': self.clientes.id})
        print(sale_id)
        #venta={'product_id':self.id,'order_id':sale_id,'name':self.name,'reservas':self.id,'product_uom_qty':self.dias,'qty_delivered':1,'qty_invoiced':1,'price_unit':self.habitaciones.precios}
        #print(venta)

    @api.one
    def crear_venta_todos(self):
        print(self.clientes)
        reservasCliente=self.clientes.reserve
        print(reservasCliente)
        id_producto = self.env.ref('reserva_hoteles.product2')
        sale_id = self.env['sale.order'].create({'partner_id': self.clientes.id})
        for reserva in reservasCliente:
            venta = {'product_id': id_producto.id, 'order_id': sale_id.id, 'name': reserve.name,'reserve':self.id,
                     'product_uom_qty': reserve.days, 'qty_delivered': 1, 'qty_invoiced': 1,
                     'price_unit': reserva.habitaciones.precios}
            
            self.env['sale.order.line'].create(venta)




class my_clients (models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'
    reserve = fields.One2many('reserva_hoteles.reserve', 'client')
    comments = fields.One2many('reserva_hoteles.comments', 'clients')

class photoHotel (models.Model):
    _name='reserva_hoteles.hotelgallery'
    name = fields.Text(string="Galeria de fotos del hotel")
    photo = fields.Binary()

class photoGallery (models.Model):
    _name = 'reserva_hoteles.photogallery'
    name = fields.Text(string="Galeria de fotos de la habitación")
    photo = fields.Binary()

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