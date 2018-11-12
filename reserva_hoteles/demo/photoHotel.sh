#!/bin/bash
echo '<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data>'
    i=1;
    while [ $i -le 4 ] ; 
    do
        echo ' 
        <record model="reserva_hoteles.photoHotel" id="photoHotel_'$1'">
            <field name="name">img_hotel'$i'</field>
            <field name="photo">`base64 ./img/Hotel'$i'.jpg`</field>
            <field name="hotel" ref=("reserva_hoteles.hotel'$i'")></field>
        </record>'
       i=$(( $i + 1 ))
    done
echo '  </data>
</odoo>'