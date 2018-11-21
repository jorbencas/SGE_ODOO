#!/bin/bash
echo '<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data>'
    i=1;
    while [ $i -le 4 ] ; 
     #random1=$((( RANDOM % 399 ) + 0 ))
    do
        echo ' 
        <record model="reserva_hoteles.photogallery" id="photo'$i'">
            <field name="name">img_hotel'$i'</field>
            <field name="photo">'`base64 ./img/Hotel$i.jpg`'</field>
            <field name="room" ref="reserva_hoteles.room_'$i'" ></field>
        </record>'
       i=$(( $i + 1 ))
    done
echo '  </data>
</odoo>'