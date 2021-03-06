# -*- coding: utf-8 -*-

from odoo import models, fields, api

class pruebas1(models.Model):
	_name = 'pruebas1.pruebas1'
	name = fields.Char()
	value = fields.Integer()
	value2 = fields.Float(compute="_value_pc", store=True)
	description = fields.Text()

	@api.depends('value')
	def _value_pc(self):
		self.value2 = float(self.value) / 100

class coches(models.Model):
	_name = 'pruebas1.coches'
	nombre = fields.Char()
	model = fields.Text()
	description = fields.Text()
	codclient = fields.Many2one('pruebas1.client','modelcar')

class client(models.Model):
	_name='pruebas1.client'
	codclient = fields.Integer()
	nombre = fields.Text()
	subname = fields.Text()
	country = fields.Many2one('res.country')
	currency = fields.Char(related='country.currency_id.symbol',store=False,readonly=True)
	a = fields.Integer(default='0')
	b = fields.Integer(default='0')
	ab = fields.Integer(compute='_get_ab')
	modelcar = fields.One2many('pruebas1.coches','codclient')

	@api.depends('a','b')
	def _get_ab(self):
		for r in self:
			r.ab = r.a+r.b

class concessionario(models.Model):
	_name='pruebas1.concessionario'
	codconfessionario = fields.Integer()
	nameconfessionario = fields.Text()
	model = fields.Many2many('pruebas1.coches')
