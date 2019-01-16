# SGE_ODOO
Example of odoo module
Eevrethink to do odoo start will be comment in my blog: https://jorgeblogbeneyto.wordpress.com/

Moduls ODOO: compra ventas factura crm

sudo nano /etc/netplan/50-cloud-init.yaml 

# This file is generated from information provided by
# the datasource.  Changes to it will not persist across an instance.
# To disable cloud-init's network configuration capabilities, write a file
# /etc/cloud/cloud.cfg.d/99-disable-network-config.cfg with the following:
# network: {config: disabled}
network:
        version: 2
        ethernets:
                 eth1:
                        dhcp4: false
                        addresses: [10.100.23.201/23]
                        gateway4: 10.100.22.1
                        nameservers:
                               addresses: [10.100.22.250]





sudo netplan apply

Seguir comandos de la pagina:

sudo nano /etc/passwd

buscar usuari odoo i cambiar li el terminal a /bin/bash

Paaswd oboo

su odoo

cd

mkdir modules
crear repositori


////////////////////////////////////////////////////Crear Modul Odoo////////////////////////////////////////////////////////
Para odoo

ser root

service odoo stop

ps aux | grep odoo
despres su odoo

crear module: 

odoo scaffold pruebas1 .

odoo --addons-path="/var/lib/odoo/modules,/usr/lib/python3/dist-packages/odoo/addons" --save

///////////////////////////////////////////////////Iniciar Odoo//////////////////////////////////////////////////////////////
Iniciar ODOO: odoo --config /var/lib/odoo/.odoorc


/////////////////////////////////////////////////Acedir a la ba se de datos/////////////////


su passwd postgres

su postgres

psql sge

\dt


/////////////////////////////////////////////////Afegir el modul a una vista////////////////////////////////////////////////////

su odoo

cd 

cd modules/pruebas1

cd views

nano views.xml

Descomentar la part de la vista, el primer paragraf de actions, els menus, excepte la ultima linea, que te que estar comentada

odoo>
  <data>
    <!-- explicit list view definition -->
    
    <record model="ir.ui.view" id="pruebas1.list">
      <field name="name">pruebas1 list</field>
      <field name="model">pruebas1.pruebas1</field>
      <field name="arch" type="xml">
        <tree>
          <field name="name"/>
          <field name="value"/>
          <field name="value2"/>
        </tree>
      </field>
    </record>
    

    <!-- actions opening views on models -->
    
    <record model="ir.actions.act_window" id="pruebas1.action_window">
      <field name="name">pruebas1 window</field>
      <field name="res_model">pruebas1.pruebas1</field>
      <field name="view_mode">tree,form</field>
    </record>
    

    <!-- server action to the one above -->
    <!--
    <record model="ir.actions.server" id="pruebas1.action_server">
      <field name="name">pruebas1 server</field>
      <field name="model_id" ref="model_pruebas1_pruebas1"/>
      <field name="state">code</field>
      <field name="code">
        action = {
          "type": "ir.actions.act_window",
          "view_mode": "tree,form",
          "res_model": self._name,
        }
      </field>
    </record>
    -->

    <!-- Top menu item -->
    
    <menuitem name="pruebas1" id="pruebas1.menu_root"/>
    
    <!-- menu categories -->
    
    <menuitem name="Menu 1" id="pruebas1.menu_1" parent="pruebas1.menu_root"/>
    <menuitem name="Menu 2" id="pruebas1.menu_2" parent="pruebas1.menu_root"/>
    
    <!-- actions -->
    
    <menuitem name="List" id="pruebas1.menu_1_list" parent="pruebas1.menu_1"
              action="pruebas1.action_window"/>
    <!--<menuitem name="Server to list" id="pruebas1" parent="pruebas1.menu_2"
              action="pruebas1.action_server"/>-->
    
  </data>
</odoo>




cd ../modules

nano modules.py

Descomentar totes les linies (la linea de class, te que estar apegada al margue)

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


