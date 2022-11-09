uml_class(car).
uml_class_type(car,abstract).

uml_attr(car,color).
uml_attr_name(car,color,"color").
uml_attr_type(car,color,str).
uml_attr_visibility(car,color,protected).

uml_attr(car,doors).
uml_attr_name(car,doors,"doors").
uml_attr_type(car,doors,int).

uml_attr(car,serial_number).
uml_attr_name(car,serial_number,"serial number").
uml_attr_type(car,serial_number,int).
uml_attr_visibility(car,serial_number,private).

uml_op(car,paint).
uml_op_name(car,paint,paint).
uml_op_type(car,paint,void).
uml_op_visibility(car,paint,private).
uml_op_args(car,paint,((color,str),)).

uml_op(car,start).
uml_op_type(car,start,void).
uml_op_visibility(car,start,public).

uml_class(race_car).
uml_attr(race_car,max_speed).
uml_attr_type(race_car,max_speed,int).
uml_is_a(race_car,car).

uml_class(van).
uml_is_a(van,car).
uml_op(van,book).
uml_op_type(van,book,bool).
uml_op_args(van,book,((date,date),)).

uml_class(wheel).
uml_attr(wheel,size).
uml_attr_type(wheel,size,int).

uml_class(seat).
uml_attr(seat,material).
uml_attr_type(seat,material,str).

uml_assoc(car,wheel,car_wheels).
uml_assoc_type(car,wheel,car_wheels,agregation).
uml_assoc_cadinality(car,wheel,car_wheels,car,1,1).
uml_assoc_cadinality(car,wheel,car_wheels,wheel,4,4).
uml_assoc_name(car,wheel,car_wheels,wheel,wheels).
uml_assoc_name(car,wheel,car_wheels,car,car).

uml_assoc(car,seat,car_seat).
uml_assoc_type(car,seat,car_seat,agregation).
uml_assoc_cadinality(car,seat,car_seat,car,1,1).
uml_assoc_cadinality(car,seat,car_seat,seat,1,"*").
uml_assoc_name(car,seat,car_seat,seat,seats).
uml_assoc_name(car,seat,car_seat,car,car).


