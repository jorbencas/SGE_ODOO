#!/bin/bash
echo '<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data>'
    i=1;
    while [ $i -le 400 ];
    do
     echo '
        <record model="{reserva_hoteles.rooms}" id="room_'$i'">
            <field name="name">1</field>
            <field name="beds" ref("`reserva_hoteles.hotel'$i'`"/>
            <field name="photos" eval="[(6,0,[ref(reserva_hoteles.photoGallery)] )]"></field>
            <field name="price"></field>
            <field name="description">Es un habitación muy bonita</field>
            <field name="hotel" ref("reserva_hoteles.hotel1")></field>
            <field name="city" ref("reserva_hoteles.city1")></field>
        </record>'
        i=$(( $i + 1 ))
    done
echo '  </data>
</odoo>';