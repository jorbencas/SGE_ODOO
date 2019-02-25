# -*- coding: utf-8 -*-
import json
from odoo import models, fields, api, tools
from odoo.exceptions import ValidationError
import datetime
import random

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
    grafic=fields.Float(compute='calcular_porcentaje',string='Ocupacion')
    ocupacionsemanal=fields.Char(compute='calcular_ocupacion')


    @api.multi
    def calcular_porcentaje(self):
        for hotel in self:
            hotel.grafic=len(hotel.futurereserve)+len(hotel.presentreserve)
            hotel.grafic=hotel.grafic/len(hotel.listRooms)
            hotel.grafic=hotel.grafic*100
            print(hotel.grafic)
   
    @api.multi
    def calcular_ocupacion(self):
        valores=[]
        for valor in self.presentreserve:
            reserves=valor.days
            valores.append({'label':str(valor.name),'value':str(reserves)})
        graph=[{'values':valores,'area':True,'title':'Reservas de esta semana','key':'Reservas','color':'#7c7bad'}]
        self.ocupacionsemanal=json.dumps(graph)

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

    @api.one
    def anyadir_comentario(self):
        reserva=self.env['reserva_hoteles.reserve'].search([('room.hotel','=',self.name),('dateend','<=',str(datetime.datetime.today()))])
        comentarios=['Me lo he pasado bien','Buenos efectos audivisuales y atencion al cliente','El baño me ha puesto nervioso', 'J**** donde m***** me he metido tio',"Tocará volver"]

        if len(reserva)!=0:
            cliente={'name':"Comantario nuevo",'description':"Descrippción de los comentarios creados genericamente",'valorations':str(random.randint(1,5)),'hotel':self.name,'clients':reserve[0].client.id}
            self.env['reserva_hoteles.comments'].create(cliente)
        else:
            print("/+++++++++++++++++++++++++++++++++++++++++++No se puede crear un comentario porque el hotel no tiene  clientes!")
            return {
                'warning': {
                    'title': "Algo ha ocurrido mal",
                    'message': "No puedes añadir un comentario aleatorio porque este hotel no tiene clientes",
                }
            }
    @api.one
    def anyadir_habitacion(self):
        hotel=self.env['reserva_hoteles.hotels'].search([('name','=',self.name)])
        print("/--***----****----***--**----****----**-/" + str(hotel.name))
        name=random.randint(1,1000)
        beds=str(random.randint(0,3))
        price=random.randint(100,1000)
        #photos=self.env['reserva_hoteles.photogallery'].search([('name','=',random.choice([self.env.ref('reserva_hoteles.photogallery').name,self.env.ref('reserva_hoteles.roomfoto2').id,self.env.ref('reserva_hoteles.roomfoto3').id,self.env.ref('reserva_hoteles.roomfoto4').id,self.env.ref('reserva_hoteles.roomfoto5').id]))])

        habitacion={'name':name,'beds':beds,'price':price,'description':"Es una habitación muy lumninosa",'hotel':hotel.id}
        hotel.listRooms.create(habitacion)
        print(habitacion)

class rooms (models.Model):
    _name = 'reserva_hoteles.rooms'
    name = fields.Integer('Numero de Habitación')
    beds = fields.Selection([('0','Una Cama'),('1','Dos beds'),('2','Cama de Matrimonio'),('3','Cama de matromonio mas cama infantil') ],'Numero de beds', default='1')
    price = fields.Float(default=1)
    description = fields.Text(default="Habitación grande, espaciosa y con gran luminosidad.")
    hotel = fields.Many2one('reserva_hoteles.hotels','Lista de habitaciones')
    photos = fields.Many2many('reserva_hoteles.photogallery')
    photomainroom = fields.Binary(compute='_get_resized_image',store=True)
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
                print("Esta habitación no tiene fotos...")

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
    reserve = fields.Many2one('reserva_hoteles.reserve', 'Linea de Venta', store=True)
    hotel = fields.Many2one('reserva_hoteles.hotel', related='reserve.hotel', readOnly=True)
    room_sale_order_line_inherit = fields.Integer(related='reserve.room.name');
    datestart_inherit = fields.Date(related='reserve.datestart', readOnly=True);
    dateend_inherit = fields.Date(related='reserve.dateend', readOnly=True);
    quantity = fields.Integer(compute='get_reserve_quantity', store=True);

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
                    print(record.dateend)
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
        id_producto = self.env.ref('reserva_hoteles.product2')
        sale_id = self.env['sale.order'].create({'partner_id': self.client.id})
        print(sale_id)
        venta = {'product_id': id_producto.id, 'order_id': sale_id.id, 'name': self.name,'reserve':self.id,
                     'product_uom_qty': self.days, 'qty_delivered': 1, 'qty_invoiced': 1,
                     'price_unit': self.room.price}
        print(venta)
        self.env['sale.order.line'].create(venta)



class my_clients (models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'
    reserve = fields.One2many('reserva_hoteles.reserve', 'client')
    comments = fields.One2many('reserva_hoteles.comments', 'clients')
    reservewithoutpaying = fields.One2many('reserva_hoteles.reserve', 'client', compute='generate_reserve_without_paying')
    reservepaying = fields.One2many('reserva_hoteles.reserve', 'client', compute='generate_reserve_paying')
    slopereserves = fields.Boolean(compute="get_slope_reserves")

    #Obtenemos si el cliente tiene reservas sin pagar, osea son reservas pendinetes

    @api.depends('reserve','reservewithoutpaying')
    def get_slope_reserves(self):
        for record in self:
            if(len(record.reservewithoutpaying) > 0 ):
                print(len(record.reservewithoutpaying))
                record.slopereserves=True
            else:
                record.slopereserves=False

    @api.depends('reserve')
    def generate_reserve_without_paying(self):
        for record in self:
            if(record.reserve):
                reservaPagada = self.env['sale.order.line'].search([]).mapped('reserve')  # obtengo las reservas que tiene una linea de factura
                record.reservewithoutpaying=record.reserve
                for pagada in reservaPagada: # me dispongo a recorrer las reservas que estan pagadas para ver si son todas las que tiene el usuario self.id
                    if(pagada.client.id==record.id):
                        record.reservewithoutpaying = record.reservewithoutpaying-pagada

    @api.depends('reserve')
    def generate_reserve_paying(self):
        for record in self:
            if(record.reserve ):
                    print(len(record.reservepaying))
                    if (len(record.reservewithoutpaying)==0):
                        record.reservepaying=record.reserve
                    else:
                        record.reservepaying=record.reserve-record.reservewithoutpaying

    @api.one
    def crear_venta_todos(self):
        print( "/************************************************************************/")
        id_producto = self.env.ref('reserva_hoteles.product2')
        print(id_producto)
        sale_id = self.env['sale.order'].create({'partner_id': self.id})
        print(sale_id)
        for reserva in self.reservewithoutpaying:
            venta = {'product_id': id_producto.id, 'order_id': sale_id.id, 'name': reserva.name,'reserve':reserva.id,
                     'product_uom_qty': reserva.days, 'qty_delivered': 1, 'qty_invoiced': 1,
                     'price_unit': reserva.room.price}
            print(venta)
            self.env['sale.order.line'].create(venta)
        self.reservewithoutpaying=self.reservewithoutpaying-reserva

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
    valorations = fields.Selection([('1', '⭐'), ('2', '⭐⭐'), ('3', '⭐⭐⭐'), ('4', '⭐⭐⭐⭐'), ('5', '⭐⭐⭐⭐⭐')],default='5')
    hotel = fields.Many2one('reserva_hoteles.hotels',"comments")
    clients = fields.Many2one("res.partner", "Nombre del cliente")
    photoclient = fields.Binary(related='clients.image',store=True)
    nameclient = fields.Char(related='clients.name')
   

class wizard_selection_reserve(models.TransientModel):
    _name='reserva_hoteles.selection_wizard'

    def _default_cliente(self):
        return self.env['res.partner'].browse(self._context.get('active_id'))

    def _default_pendientes(self):
        return self.env['res.partner'].browse(self._context.get('active_id')).reservewithoutpaying

    cli = fields.Many2one('res.partner', default=_default_cliente , string="Cliente actual")
    cliReservasPendientesMany = fields.Many2many('reserva_hoteles.reserve',default=_default_pendientes, string="Reservas por pagar")
    #name=fields.Char(name="Nombre de la reserva" , related='cliReservasPendientesMany.name')
    datestart=fields.Date(name="Inicio de la reserva",related='cliReservasPendientesMany.datestart')
    dateend = fields.Date(name="Final de la reserva", related='cliReservasPendientesMany.dateend')
    days=fields.Float(name="Numero de dias" , related='cliReservasPendientesMany.days')

    @api.multi
    def launch(self):
        id_producto = self.env.ref('reserva_hoteles.product2')
        sale_id = self.env['sale.order'].create({'partner_id': self.cli.id})

        for reserva in self.cliReservasPendientesMany:
            venta = {'product_id': id_producto.id, 'order_id': sale_id.id, 'name': reserva.name, 'reserva': reserva.id,
                     'product_uom_qty': reserva.days, 'qty_delivered': 1, 'qty_invoiced': 1,
                     'price_unit': reserva.room.price}

            self.env['sale.order.line'].create(venta)
            self.cliReservasPendientesMany = self.cliReservasPendientesMany - reserva
        return {}

class reserva_wizard(models.TransientModel):   # La classe és transientModel
    _name = 'reserva_hoteles.reserve_wizard'

    def _default_servicios(self):
        return self.env['reserva_hoteles.services'].search([])

    def default_hoteles(self):
        return self.env['reserva_hoteles.hotels'].search([])

    def default_paises_con_hoteles(self):
        return self.env['reserva_hoteles.hotels'].search([]).mapped('city').mapped('countrys').ids

    def default_habitaciones(self):
        print(self.hotel.search([]))
        return self.hotel.search([]).mapped('listRooms').ids

    clientes = fields.Many2one("res.partner", "Nombre del cliente")
    city=fields.Many2one("reserva_hoteles.citys","Ciudad")
    countries=fields.Many2many("res.country",default=default_paises_con_hoteles)
    country=fields.Many2one("res.country")

    hotel=fields.Many2many("reserva_hoteles.hotels","Hotel",default=default_hoteles)
    descripcion=fields.Text(related='hotel.description')
    fotoprincipalhotel=fields.Binary(related='hotel.photomainhotel')
    servicis=fields.Many2many("reserva_hoteles.services", default=_default_servicios)
    estrellasMax = fields.Selection([('1', '⭐'), ('2', '⭐⭐'), ('3', '⭐⭐⭐'), ('4', '⭐⭐⭐⭐'), ('5', '⭐⭐⭐⭐⭐')],string ="Maximo estrell",default='5')
    estrellasMin = fields.Selection([('1', '⭐'), ('2', '⭐⭐'), ('3', '⭐⭐⭐'), ('4', '⭐⭐⭐⭐'), ('5', '⭐⭐⭐⭐⭐')], string="Minimo rellas",default='1')
    beds = fields.Selection([('0','Una Cama'),('1','Dos beds'),('2','Cama de Matrimonio'),('3','Cama de matromonio mas cama infantil') ])
    precios=fields.Integer()
    #es posible que alguien queira hacer varias reservas
    rooms=fields.Many2many("reserva_hoteles.rooms",default=default_habitaciones,limit=10)

    fechaInicio = fields.Date()
    fechaFinal = fields.Date()

    state = fields.Selection([  # El camp state és per a crear l'assistent.
        ('localizacion', "Selecciona Localización"),
        ('habitacion', "Selecciona el hotel"),
        ('reserva', "Selecciona la habitación"),
        ('fin', "Fin"),
    ], default='localizacion')

    @api.onchange('city','clientes')
    def _oc_city(self):
        if (self.city and self.clientes):
            self.aplicar_filtros()
            #self.state
            return {}

    @api.onchange('country')
    def _oc_country(self):
        if (self.country):
            self.aplicar_filtros()
            # self.state
            return {}

    @api.onchange('beds')
    def _oc_beds(self):
        if(self.beds):
            self.aplicar_filtros()
            return {}

    @api.onchange('precios')
    def _oc_prices(self):
        if (self.precios):
            self.aplicar_filtros()
            return {}

    @api.onchange('estrellasMin')
    def _oc_min_stars(self):
        if(self.estrellasMin):
            self.aplicar_filtros()
            return {}

    @api.onchange('estrellasMax')
    def _oc_max_stars(self):
        if (self.estrellasMax):
            self.aplicar_filtros()
            return {}

    @api.onchange('fechaInicio','fechaFinal')
    def _on_dates(self):
        if(self.fechaFinal and self.fechaFinal):
            self.aplicar_filtros()
            return {}


    def aplicar_filtros(self):
        domains=[]
        if len(self.city)!=0:
            domains.append(('city.id','=',str(self.city.id)))

        if len(self.country)!=0:
            domains.append(('city.countrys.id','=',str(self.country.id)))

        if self.beds:
            domains.append(('listRooms.beds','=',str(self.beds)))

        if self.precios != 0:
            domains.append(('listRooms.price','=',self.precios))

        if self.estrellasMin!=0:
            domains.append(('valorations','>=',self.estrellasMin))

        if self.estrellasMax!=0:
            domains.append(('valorations','<=',self.estrellasMax))

        
        

        # print(domains)
        # listaTMPHotel=self.env['reserva_hoteles.hotels'].search(domains)

        # if len(self.servicis)>0:
        #     servicios=self.servicis
        #     listaTMPHotel=listaTMPHotel.filtered(lambda r:len(r.listServices & servicios) == len(servicios))

        # self.hotel=listaTMPHotel

        # if(self.fechaInicio and self.fechaFinal):
        #     self.rooms=self.env['reserva_hoteles.rooms'].search([('hotel.name','in',self.hotel.name)])


        # print(domains)
        # listaTMPHotel=self.env['reserva_hoteles.hotels'].search(domains)
        # self.rooms=self.hotel.mapped('listRooms').ids

        # if len(self.servicis)>0:
        #     servicios=self.servicis
        #     listaTMPHotel=listaTMPHotel.filtered(lambda r:len(r.listServices & servicios) == len(servicios))

        # self.hotel=listaTMPHotel

        # print(self.hotel)

        # if self.fechaInicio and self.fechaFinal:
        #     habitacionesLibres=self.rooms.search([('avaible','=','Libre')])
        #     if self.beds != '0':
        #         habitacionesLibres=habitacionesLibres.filtered(lambda r:r.beds==self.beds)
        #     self.hotel=habitacionesLibres.mapped('hotel').sorted(key=lambda r: r.valorations,reverse=True).ids

        #     if self.precios != 0:
        #         habitacionesLibres=habitacionesLibres.filtered(lambda r:r.price <= self.precios)
        #     self.rooms=habitacionesLibres


    @api.multi
    def siguiente_paso(self):
        if (self.state == "localizacion") :
            self.state = "habitacion"
            return {"type": "ir.actions.do_nothing", }

        elif(self.state == "habitacion"):
            self.state="reserva"
            return {"type": "ir.actions.do_nothing", }
        elif(self.state=="reserva"):
            self.state="fin"
            return {"type": "ir.actions.do_nothing", }




