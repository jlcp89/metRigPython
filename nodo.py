# -*- coding: utf-8 *-*

class Nodo():
    
    def __init__(self):
        self.apoyo = False 
        self.id_nodo = 0
        self.co_x = 0.000  # coordenadas en metros del nodo, en pies, en x
        self.co_y = 0.000  # en y en pies 
        self.r_1 = 0  # IDETIFICADORES NUMERICOS DE LAS REACCIONES EN EL NODO,  en x
        self.r_2 = 0  # en y
        self.r_3 = 0  # en  z
        self.rb_1 = 0.0000  # reaccion de extremos fijos para y de analisis estructural, en x
        self.rb_2 = 0.0000  # en y
        self.rb_3 = 0.0000  # en z
        self.rc_1 = 0.0000  # reacciones en apoyos + condicion de carga original, en x
        self.rc_2 = 0.0000  # en y
        self.rc_3 = 0.0000  # en z
        self.rt_1 = 0.0000  # reaccion total en el nodo, definido como rb + rc, en x 
        self.rt_2 = 0.0000  # en y
        self.rt_3 = 0.0000    # en z
        self.des_1 = 0.000  # desplazamiento 1 del nodo, en x
        self.des_2 = 0.000  # en y
        self.des_3 = 0.000  # en z
        self.cad = ""
              
   