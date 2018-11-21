#!/bin/bash
echo '<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data>'
    i=0;
    while [ $i -lt 399 ];
    #random=$((( RANDOM % 2 ) + 1 ))
    #random1=$((( RANDOM % 3 ) + 0 ))
    #random5=$((( RANDOM % 4 ) + 1 ))
    do
        echo '
        <record model="reserva_hoteles.rooms" id="room_'$i'">
            <field name="name">'$i'</field>
            <field name="beds">2</field>
            <field name="price">4.52</field>
            <field name="description">Es un habitación muy bonita</field>
            <field name="hotel" ref="reserva_hoteles.hotel4"></field>
            <field name="city" ref="reserva_hoteles.city2"></field>
        </record>'
        i=$(( $i + 1 ))
    done
echo '  </data>
</odoo>';