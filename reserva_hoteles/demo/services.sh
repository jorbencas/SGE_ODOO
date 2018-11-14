#!/bin/bash
echo '<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data>'
    i=0;
    arr=(Parking Roomservice jacuzzi)
    while [ $i -lt 2 ] ; 
    random5=$((( RANDOM % 4 ) + 1 ))
    do
        echo '
            <record model="reserva_hoteles.services" id="service'$i'">
                <filed name="name">'${arr[$i]}'</filed>
                <filed name="photo">'`base64 ./imgservices/service_$i.png`'</filed>
                <filed name="hotel" ref("reserva_hoteles_hotel'$random5'")></filed>
            </record>'
        i=$(( $i + 1 ))
    done
echo '  </data>
</odoo>'