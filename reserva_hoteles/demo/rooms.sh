#!/bin/bash
echo '<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data>'
    i=1;
    while [ $i -lt 400 ];
    random=$((( RANDOM % 2 ) + 1 ))
    random1=$((( RANDOM % 3 ) + 0 ))
    random5=$((( RANDOM % 4 ) + 1 ))
    do
     echo '
        <record model="reserva_hoteles.rooms" id="room_'$i'">
            <field name="name">1</field>
            <field name="beds" ref("reserva_hoteles.hotel'$random5'">'$random1'</field>
            <field name="price"></field>
            <field name="description">Es un habitación muy bonita</field>
            <field name="hotel" ref("reserva_hoteles.hotel'$random5'")></field>
            <field name="city" ref("reserva_hoteles.city'$random'")></field>
        </record>'
        i=$(( $i + 1 ))
    done
echo '  </data>
</odoo>';