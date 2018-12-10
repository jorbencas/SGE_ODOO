#!/bin/bash
echo '<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data>'
    i=0;
    while [[ $i -lt 399 ]];do
    random=$((( RANDOM % 4 ) + 1 ))
        echo '
        <record model="reserva_hoteles.rooms" id="room_'$i'">
            <field name="name">'$i'</field>
            <field name="beds">2</field>
            <field name="price">4.52</field>
            <field name="description">Es un habitación muy bonita</field>
            <field name="hotel" ref="reserva_hoteles.hotel'$random'"></field>
        </record>'
        i=$(( $i + 1 ))
    done
echo '  </data>
</odoo>';