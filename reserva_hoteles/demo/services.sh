#!/bin/bash
echo '<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data>'
   i=0;
    arr=(Parking Roomservice jacuzzi)
    while [ $i -le 2 ]; 
    do
        echo '  
        <record model="reserva_hoteles.services" id="service'$i'">
            <field name="name">'${arr[$i]}'</field>
            <field name="photo">'`base64 ./imgservices/service_$i.png`'</field>
            <field name="hotel"  eval="[(6,0[ref(reserva_hoteles.hotel1),ref(reserva_hoteles.hotel3)])]"/>
        </record>'
        i=$(( $i + 1 ))
    done
echo '  </data>
</odoo>'