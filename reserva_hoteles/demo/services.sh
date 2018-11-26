#!/bin/bash
echo '<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data>'
   i=0;
    arr=(0 1 2)
    while [ $i -le 2 ]; 
    random=$((( RANDOM % 4 ) + 1 ))
    do
        echo '  
        <record model="reserva_hoteles.services" id="service'$i'">
            <field name="name">'${arr[$i]}'</field>
            <field name="photo">'`base64 ./imgservices/service_$i.png`'</field>
            <field name="hotel"  eval="[(6,0[ref(reserva_hoteles.hotel'$random')])]"/>
        </record>'
        i=$(( $i + 1 ))
    done
echo '  </data>
</odoo>'
