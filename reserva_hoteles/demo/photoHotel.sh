echo "<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data>"
    i=1;
    while [ $i -ge 4 ]; 
    do
        echo " <record model="{reserva_hoteles.photoGallery}" id="hotel1">
            <field name="name">img_hotel$i</field>
           "
    done
echo "</data>
</odoo>"