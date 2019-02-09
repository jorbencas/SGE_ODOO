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
        print("/****************************************************************************/" + str(self.oldreserve))
    @api.one
    @api.depends('reserve')
    def get_present_reserve(self):
        self.presentreserve = self.env['reserva_hoteles.reserve'].search([('hotel', '=', self.name), ('datestart', '>',  datetime.datetime.now()), ('dateend', '<',  datetime.datetime.now())])      
        print("/****************************************************************************/" + str(self.presentreserve))
    @api.one
    @api.depends('reserve')
    def get_future_reserve(self):
        self.futurereserve = self.env['reserva_hoteles.reserve'].search([('hotel', '=', self.name), ('datestart', '>',  datetime.datetime.now()), ('dateend', '>',  datetime.datetime.now())])
        print("/****************************************************************************/" + str(self.futurereserve))
    
    @api.depends('photoGallery')
    def _get_resized_image_hotel(self):
        for p in self:
            print(p.city.name)
            if len(p.photoGallery) > 0:
                 p.photomainhotel = p.photoGallery[0].photo
            else:
                 print("Este hotel no tiene fotos...")

    # @api.one
    # def anyadir_comentario(self):
    #     reserva=self.env['hotels_be_bago.reserva'].search([('habitaciones.hotel','=',self.id),('fechaFinal','<=',str(datetime.datetime.today()))])
    #     #el self.env se usa para recuperar una tabla de la bbdd
        #el search es como usn elect
    #     comentarios=['Me lo he pasado bien','Buenos efectos audivisuales y atencion al cliente','El baño me ha puesto nervioso', 'J**** donde m***** me he metido tio',"Tocará volver"]

    #     if len(reserva)!=0:
    #         cliente={'clientes':reserva[random.randint(0,len(reserva)-1)].clientes.id,'hoteles':self.id,'descripcion':comentarios[random.randint(0,len(comentarios)-1)],'valoracion':str(random.randint(1,5))}
    #         self.env['hotels_be_bago.comentarios'].create(cliente)
    #     else:
    #         print("No se puede crear un comentario porque el hotel no tiene  clientes!")
    #         return {
    #             'warning': {
    #                 'title': "Algo ha ocurrido mal",
    #                 'message': "No puedes añadir un comentario aleatorio porque este hotel no tiene clientes",
    #             }
    #         }
    # @api.one
    # def anyadir_habitacion(self):
    #     hotel=self.env['hotels_be_bago.hotel'].search([('id','=',self.id)])
    #     name="Habitacion " + str(hotel.name) + str(random.randint(1,1000))
    #     camas=str(random.randint(1,5))
    #     precios=random.randint(100,1000)
    #     fotos=self.env['hotels_be_bago.roomfotos'].search([('id','=',random.choice([self.env.ref('hotels_be_bago.roomfoto1').id,self.env.ref('hotels_be_bago.roomfoto2').id,self.env.ref('hotels_be_bago.roomfoto3').id,self.env.ref('hotels_be_bago.roomfoto4').id,self.env.ref('hotels_be_bago.roomfoto5').id]))])

    #     habitacion={'hotel':hotel.id,'name':name,'camas':camas,'precios':precios,'fotos':[(6,0,fotos.ids)]}
    #     hotel.roomlist.create(habitacion)
        #print(habitacion)

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
    days = fields.Float(default=1, compute="get_days_reserve")

    @api.one
    @api.depends('datestart','dateend')
    def get_days_reserve(self):
        for record in self:
            if (record.datestart and record.dateend):
                DATE_FORMAT="%Y-%m-%d"
                datestart=datetime.datetime.strptime(str(record.datestart),DATE_FORMAT)
                dateend=datetime.datetime.strptime(str(record.dateend),DATE_FORMAT)
                resu = dateend - datestart
                resu_day = resu.days + float(resu.seconds) / 86400
                record.days = resu_day

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
        sale_id = self.env['sale.order'].create({'partner_id': self.client.id})
        print(sale_id)
        venta={'product_id':self.id,'order_id':sale_id,'name':self.name,'reservas':self.id,'product_uom_qty':self.days,'qty_delivered':1,'qty_invoiced':1,'price_unit':self.room.price}
        print(venta)

    @api.one
    def crear_venta_todos(self):
        print( "/************************************************************************/")
        reservasCliente=self.client.reserve
        print(reservasCliente)
        id_producto = self.env.ref('reserva_hoteles.product2')
        sale_id = self.env['sale.order'].create({'partner_id': self.client.id})
        for reserva in reservasCliente:
            print(reserva.room);
            venta = {'product_id': id_producto.id, 'order_id': sale_id.id, 'name': reserva.name,'reserve':self.id,
                     'product_uom_qty': reserva.days, 'qty_delivered': 1, 'qty_invoiced': 1,
                     'price_unit': reserva.room.price}
            
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