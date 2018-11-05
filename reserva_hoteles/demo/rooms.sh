#!/bin/bash
echo "<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data>"
    let i=0;

    arrayString=("desagradable" "majestuosa" "primordial" "agradable" "fabulosa" "denigrante" "marginal")


    while [ $i -ge 399 ];
    do
     echo "
        <record model="{reserva_hoteles.hotels}" id="hotel_$i">
            <field name="name">Royald Resort</field>
            <field name="description">Es un habitación muy `$arrayString`</field>
            <field name="listRooms" ref('reserva_hoteles.hotel$i'/>
            <field name="valorations">2</field>
            <field name="listServices"></field>
            <field name="city" ref('reserva_hoteles.city$i'></field>
            <field name="comments"></field>
        </record>"
    done
echo "</data>
</odoo>";