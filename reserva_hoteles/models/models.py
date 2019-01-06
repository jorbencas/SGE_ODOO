# -*- coding: utf-8 -*-
from odoo import models, fields, api, tools
# from odoo.exceptions import ValnameationError
import datetime

class citys(models.Model):
	_name = 'reserva_hoteles.citys'
	name = fields.Text()
	description = fields.Text()
	location = fields.Text()
	countrys = fields.Many2one('res.country','Pais')
	listHotels = fields.One2many('reserva_hoteles.hotels', 'city')
    # active_id_hotel = fields.Id(related='listHotels.name', readOnly=True)

class hotels (models.Model):
    _name = 'reserva_hoteles.hotels'
    name = fields.Text()
    photoGallery = fields.Many2many('reserva_hoteles.hotelgallery')
    photomainhotel = fields.Binary(compute='_get_resized_image_hotel',store=True)
    description = fields.Text()
    listRooms = fields.One2many('reserva_hoteles.rooms','name')
    active_id_room = fields.Id(related='listRooms.name', readOnly=True)
    valorations = fields.Selection([('1', '⭐'), ('2', '⭐⭐'), ('3', '⭐⭐⭐'), ('4', '⭐⭐⭐⭐'), ('5', '⭐⭐⭐⭐⭐')])
    listServices = fields.Many2many('reserva_hoteles.services')
    city = fields.Many2one('reserva_hoteles.citys','name')
    countrys = fields.Char(related='city.countrys.name', store=True, readOnly=True)
    comments = fields.One2many('reserva_hoteles.comments','name')
    # active_id_coment = fields.Id(related='comments.name', readOnly=True)

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
        reserve=self.env['reserva_hoteles.reserve'].search([('room.hotel','=',self.name),('dateend','<=',str(datetime.datetime.today()))])
        #el self.env se usa para recuperar una tabla de la bbdd
        #el search es como usn elect
        comments=['Me lo he pasado bien','Buenos efectos audivisuales y atencion al cliente','El baño me ha puesto nervioso', 'J**** donde m***** me he metnameo tio',"Tocará volver"]

        if len(reserve)!=0:
            client={'clientes':reserve[random.randint(0,len(reserve)-1)].client.name,'hoteles':self.name,'descripcion':comentarios[random.randint(0,len(comentarios)-1)],'valoracion':str(random.randint(1,5))}
            self.env['reserva_hoteles.comments'].create(client)
        else:
            print("No se puede crear un comentario porque el hotel no tiene  clientes!")
            return {
                'warning': {
                    'title': "Algo ha ocurrnameo mal",
                    'message': "No puedes añadir un comentario aleatorio porque este hotel no tiene clientes",
                }
            }
    @api.one
    def anyadir_habitacion(self):
        hotel=self.env['reserva_hoteles.hotel'].search([('name','=',self.name)])
        name="Habitacion " + str(hotel.name) + str(random.randint(1,1000))
        beds=str(random.randint(1,5))
        price=random.randint(100,1000)
        photos=self.env['reserva_hoteles.photogallery'].search([('name','=',random.choice([self.env.ref('reserva_hoteles.roomfoto1').name,self.env.ref('reserva_hoteles.roomfoto2').name,self.env.ref('reserva_hoteles.roomfoto3').name,self.env.ref('reserva_hoteles.roomfoto4').name,self.env.ref('reserva_hoteles.roomfoto5').name]))])

        room={'hotel':hotel.name,'name':name,'beds':beds,'price':price,'photos':[(6,0,photos.name)]}
        hotel.roomlist.create(room)
        #print(habitacion)



class rooms (models.Model):
    _name = 'reserva_hoteles.rooms'
    name = fields.Integer()
    beds = fields.Selection([('0','Una Cama'),('1','Dos Camas'),('2','Cama de Matrimonio'),('3','Cama de matromonio mas cama infantil') ],'Type', default='1')
    photos = fields.Many2many('reserva_hoteles.photogallery')
    photomainroom = fields.Binary(compute='_get_resized_image',store=True)
    price = fields.Float(default=1)
    description = fields.Text(default="Habitación grande, espaciosa y con gran luminosnamead.")
    hotel = fields.Many2one('reserva_hoteles.hotels','listRooms')
    city = fields.Many2one('reserva_hoteles.citys', related='hotel.city', readOnly=True)
    reserve = fields.One2many('reserva_hoteles.reserve','name')
    # active_id = fields.Id(related='reserve.name')
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

class reserve (models.Model):
    _name = 'reserva_hoteles.reserve'
    name = fields.Text(string="Nombre de la reserva")
    datestart = fields.Date()
    dateend = fields.Date()
    client = fields.Many2one('res.partner', 'Nombre del cliente')
    room = fields.Many2one('reserva_hoteles.rooms','reserve')
    hotel = fields.Many2one('reserva_hoteles.hotels', related='room.hotel', readonly=True,store=True)
    city = fields.Many2one('reserva_hoteles.citys', related='hotel.city', readonly=True)
    fotoclient=fields.Binary(compute='_get_imagen_cliente',store=True)

    @api.depends('client')
    def _get_imagen_cliente(self):
        if self.cliente:
            if(self.client.image):
                self.photoclient = self.client.image
            if(self.client.image_small):
                self.photoclient = self.client.image_small
            if (self.client.image_medium):
                self.photoclient = self.client.image_medium


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
                            'title': "Algo ha ocurrnameo mal",
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
            variable = self.search_count([('name', '!=', record.name),('room.name', '=', record.room.name) ,('dateend', '>=', record.datestart), ('datestart','<=', record.dateend)])
            variable2 = self.search([('name', '!=', record.name),('room.name', '=', record.room.name), ('dateend', '>=', record.datestart), ('datestart','<=', record.dateend)])

            for valor in variable2:
                print(self.name)
                print(valor.name)

            if variable > 0:
                raise ValnameationError("Se solapan las 2 fechas \n"+ self.name + "com " + valor.name)

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