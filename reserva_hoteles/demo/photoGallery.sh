#!/bin/bash
echo '<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data>'
    i=1;
    while [ $i -le 4 ] ;do 
     random=$((( RANDOM % 399 ) + 0 ))
        echo ' 
        <record model="reserva_hoteles.photogallery" id="roomfoto'$i'">
            <field name="name">img_room'$i'</field>
            <field name="photo">'`base64 ./img/Hotel$i.jpg`'</field>
        </record>'
       i=$(( $i + 1 ))
    done
echo '  </data>
</odoo>'