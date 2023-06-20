# -*- coding: utf-8 *-*

import os
import sys

import numpy
from scipy import linalg

from nodo import Nodo
from elemento import Elemento

def main():
    os.system("mode con cols=125 lines=25")
    os.system("cls")
    numero_nodos = int(sys.argv[1])
    numero_apoyos = int(sys.argv[2])
    numero_elementos = int(sys.argv[3])
    modulo_elasticidad = float(sys.argv[4])
    inercia_sec_tr = float(sys.argv[5])
    area_sec_tr = float(sys.argv[6])
    nodos = []
    contador_nodos = 0
    contador_reacciones = 0
    for contador_nodos in range(numero_nodos + numero_apoyos):  # Ingereso de coordenadas de nodos
        nodo_actual = Nodo()
        nodos.append(nodo_actual)
        os.system("cls")
        print
        print
        if contador_nodos < numero_nodos:
            cadenita = "NO"
            nodos[contador_nodos].apoyo = False
        else:
            cadenita = "SI"
            nodos[contador_nodos].apoyo = True
        print "Ingresando datos del nodo ",(contador_nodos)," que ",cadenita, " es un Apoyo."
        nodos[contador_nodos].co_x = (int(raw_input("Ingrese Coordenada X del Nodo (en pies): ")))
        nodos[contador_nodos].co_y = (int(raw_input("Ingrese Coordenada Y del Nodo (en pies): ")))
        nodos[contador_nodos].id_nodo = contador_nodos
        nodos[contador_nodos].r_1 = int(contador_reacciones)
        contador_reacciones += 1
        nodos[contador_nodos].r_2 = int(contador_reacciones)
        contador_reacciones += 1
        nodos[contador_nodos].r_3 = int(contador_reacciones)
        contador_reacciones += 1
    
##########################################################    
    elementos = []
    contador_elementos = 0
    for contador_elementos in range(numero_elementos):  # Ingreso de nodos por elemento
        elemento_actual = Elemento()
        elementos.append(elemento_actual)
        os.system("cls")
        print
        print
        print "Ingresando datos del elemento numero: ", contador_elementos
        elementos[contador_elementos].id_elemento = contador_elementos
        id_nodo_N = (int(raw_input("Ingrese el numero de identificacion del nodo cercano (N): ")))    
        id_nodo_F = (int(raw_input("Ingrese el numero de identificacion del nodo alejado (F): ")))
        # elementos[contador_elementos].d_sec_tr = (int(raw_input("Ingrese el peralte del elemento (en cm): ")))
        # elementos[contador_elementos].b_sec_tr = (int(raw_input("Ingrese la base del elemento (en cm)   : ")))
        elementos[contador_elementos].E = modulo_elasticidad
        elementos[contador_elementos].inercia_sec_tr = inercia_sec_tr
        elementos[contador_elementos].area_sec_tr = area_sec_tr
        elementos[contador_elementos].calcular_propiedades(nodos[id_nodo_N], nodos[id_nodo_F])
        print
        respuesta_1 = raw_input("Este elemento esta afectado por alguna fuerza puntual? s/n: ")
        if respuesta_1 == "s" or respuesta_1 == "S":
            n_car_pun = int(raw_input("Cuantas cargas puntuales tiene?  : "))
            contador_1 = 0
            for contador_1 in range(n_car_pun):
                print
                print "Ingreso de datos de la fuerza puntual ", contador_1
                magnitud = (float(raw_input("Ingrese valor de carga puntual (en Kip): ")))
                dist = (float(raw_input("Ingrese la distanca, del nodo N al punto de aplicacion de la fuerza (en ft.): ")))
                elementos[contador_elementos].agregar_carga_puntual(magnitud, dist)
        else:
            pass
        print   
        respuesta_2 = raw_input("Este elemento esta afectado por alguna fuerza uniformemente distribuida? s/n: ")
        if respuesta_2 == "s" or respuesta_2 == "S":
            n_car_dis = int(raw_input("Cuantas cargas distribuidas tiene?: "))
            contador_2 = 0
            for contador_2 in range(n_car_dis):
                print
                print "Ingreso de datos de la fuerza uniformemente distribuida", contador_2
                magnitud = float(raw_input("Ingrese magnitud de fuerza uniformemente distribuida (en Kip/ft.): "))
                elementos[contador_elementos].agregar_carga_distribuida(magnitud)
        else:
            pass
        nodos = elementos[contador_elementos].calcular_fuerzas_para_analisis(nodos)
    
######################################################################    
    cont_reac = 0    
    Qk = [[0 for x in range(1)] for x in range(numero_nodos * 3)]   
    Qk = numpy.reshape(numpy.matrix(numpy.asanyarray(Qk)),((numero_nodos * 3),1))
    for contador_nodos in range(numero_nodos):
        Qk[cont_reac, 0] = nodos[contador_nodos].rb_1
        cont_reac += 1        
        Qk[cont_reac, 0] = nodos[contador_nodos].rb_2
        cont_reac += 1        
        Qk[cont_reac, 0] = nodos[contador_nodos].rb_3
        cont_reac += 1
    matriz_k_marco =  [[0 for x in range(contador_reacciones)] for x in range(contador_reacciones)]
    m_k_marco = numpy.asmatrix(numpy.asarray(matriz_k_marco))     
    for contador_elementos in range(numero_elementos):
        m_k_marco[elementos[contador_elementos].nodo_N.r_1,elementos[contador_elementos].nodo_N.r_1] += elementos[contador_elementos].matriz_k_global[0,0]     
        m_k_marco[elementos[contador_elementos].nodo_N.r_1,elementos[contador_elementos].nodo_N.r_2] += elementos[contador_elementos].matriz_k_global[0,1]
        m_k_marco[elementos[contador_elementos].nodo_N.r_1,elementos[contador_elementos].nodo_N.r_3] += elementos[contador_elementos].matriz_k_global[0,2]
        m_k_marco[elementos[contador_elementos].nodo_N.r_1,elementos[contador_elementos].nodo_F.r_1] += elementos[contador_elementos].matriz_k_global[0,3]
        m_k_marco[elementos[contador_elementos].nodo_N.r_1,elementos[contador_elementos].nodo_F.r_2] += elementos[contador_elementos].matriz_k_global[0,4]
        m_k_marco[elementos[contador_elementos].nodo_N.r_1,elementos[contador_elementos].nodo_F.r_3] += elementos[contador_elementos].matriz_k_global[0,5]
        m_k_marco[elementos[contador_elementos].nodo_N.r_2,elementos[contador_elementos].nodo_N.r_1] += elementos[contador_elementos].matriz_k_global[1,0]     
        m_k_marco[elementos[contador_elementos].nodo_N.r_2,elementos[contador_elementos].nodo_N.r_2] += elementos[contador_elementos].matriz_k_global[1,1]
        m_k_marco[elementos[contador_elementos].nodo_N.r_2,elementos[contador_elementos].nodo_N.r_3] += elementos[contador_elementos].matriz_k_global[1,2]
        m_k_marco[elementos[contador_elementos].nodo_N.r_2,elementos[contador_elementos].nodo_F.r_1] += elementos[contador_elementos].matriz_k_global[1,3]
        m_k_marco[elementos[contador_elementos].nodo_N.r_2,elementos[contador_elementos].nodo_F.r_2] += elementos[contador_elementos].matriz_k_global[1,4]
        m_k_marco[elementos[contador_elementos].nodo_N.r_2,elementos[contador_elementos].nodo_F.r_3] += elementos[contador_elementos].matriz_k_global[1,5]
        m_k_marco[elementos[contador_elementos].nodo_N.r_3,elementos[contador_elementos].nodo_N.r_1] += elementos[contador_elementos].matriz_k_global[2,0]     
        m_k_marco[elementos[contador_elementos].nodo_N.r_3,elementos[contador_elementos].nodo_N.r_2] += elementos[contador_elementos].matriz_k_global[2,1]
        m_k_marco[elementos[contador_elementos].nodo_N.r_3,elementos[contador_elementos].nodo_N.r_3] += elementos[contador_elementos].matriz_k_global[2,2]
        m_k_marco[elementos[contador_elementos].nodo_N.r_3,elementos[contador_elementos].nodo_F.r_1] += elementos[contador_elementos].matriz_k_global[2,3]
        m_k_marco[elementos[contador_elementos].nodo_N.r_3,elementos[contador_elementos].nodo_F.r_2] += elementos[contador_elementos].matriz_k_global[2,4]
        m_k_marco[elementos[contador_elementos].nodo_N.r_3,elementos[contador_elementos].nodo_F.r_3] += elementos[contador_elementos].matriz_k_global[2,5]
        m_k_marco[elementos[contador_elementos].nodo_F.r_1,elementos[contador_elementos].nodo_N.r_1] += elementos[contador_elementos].matriz_k_global[3,0]     
        m_k_marco[elementos[contador_elementos].nodo_F.r_1,elementos[contador_elementos].nodo_N.r_2] += elementos[contador_elementos].matriz_k_global[3,1]
        m_k_marco[elementos[contador_elementos].nodo_F.r_1,elementos[contador_elementos].nodo_N.r_3] += elementos[contador_elementos].matriz_k_global[3,2]
        m_k_marco[elementos[contador_elementos].nodo_F.r_1,elementos[contador_elementos].nodo_F.r_1] += elementos[contador_elementos].matriz_k_global[3,3]
        m_k_marco[elementos[contador_elementos].nodo_F.r_1,elementos[contador_elementos].nodo_F.r_2] += elementos[contador_elementos].matriz_k_global[3,4]
        m_k_marco[elementos[contador_elementos].nodo_F.r_1,elementos[contador_elementos].nodo_F.r_3] += elementos[contador_elementos].matriz_k_global[3,5]
        m_k_marco[elementos[contador_elementos].nodo_F.r_2,elementos[contador_elementos].nodo_N.r_1] += elementos[contador_elementos].matriz_k_global[4,0]     
        m_k_marco[elementos[contador_elementos].nodo_F.r_2,elementos[contador_elementos].nodo_N.r_2] += elementos[contador_elementos].matriz_k_global[4,1]
        m_k_marco[elementos[contador_elementos].nodo_F.r_2,elementos[contador_elementos].nodo_N.r_3] += elementos[contador_elementos].matriz_k_global[4,2]
        m_k_marco[elementos[contador_elementos].nodo_F.r_2,elementos[contador_elementos].nodo_F.r_1] += elementos[contador_elementos].matriz_k_global[4,3]
        m_k_marco[elementos[contador_elementos].nodo_F.r_2,elementos[contador_elementos].nodo_F.r_2] += elementos[contador_elementos].matriz_k_global[4,4]
        m_k_marco[elementos[contador_elementos].nodo_F.r_2,elementos[contador_elementos].nodo_F.r_3] += elementos[contador_elementos].matriz_k_global[4,5]
        m_k_marco[elementos[contador_elementos].nodo_F.r_3,elementos[contador_elementos].nodo_N.r_1] += elementos[contador_elementos].matriz_k_global[5,0]     
        m_k_marco[elementos[contador_elementos].nodo_F.r_3,elementos[contador_elementos].nodo_N.r_2] += elementos[contador_elementos].matriz_k_global[5,1]
        m_k_marco[elementos[contador_elementos].nodo_F.r_3,elementos[contador_elementos].nodo_N.r_3] += elementos[contador_elementos].matriz_k_global[5,2]
        m_k_marco[elementos[contador_elementos].nodo_F.r_3,elementos[contador_elementos].nodo_F.r_1] += elementos[contador_elementos].matriz_k_global[5,3]
        m_k_marco[elementos[contador_elementos].nodo_F.r_3,elementos[contador_elementos].nodo_F.r_2] += elementos[contador_elementos].matriz_k_global[5,4]
        m_k_marco[elementos[contador_elementos].nodo_F.r_3,elementos[contador_elementos].nodo_F.r_3] += elementos[contador_elementos].matriz_k_global[5,5]
    matriz_k11_marco = [[0 for x in range(numero_nodos * 3)] for x in range(numero_nodos * 3)]
    m_k11_marco = numpy.asmatrix(numpy.asarray(matriz_k11_marco))
    for i in range(numero_nodos * 3):
        for j in range (numero_nodos *3):
            m_k11_marco[i,j] = m_k_marco[i,j]
    m_inv_k11_marco = linalg.inv(m_k11_marco)
    Du = m_inv_k11_marco * Qk
    matriz_k21_marco = [[0 for x in range(numero_nodos * 3)] for x in range(numero_apoyos * 3)]
    m_k21_marco = numpy.asmatrix(numpy.asanyarray(matriz_k21_marco))
    for i in range((numero_nodos * 3), ((numero_nodos + numero_apoyos) * 3)):
        for j in range (numero_nodos *3):
            m_k21_marco[i-(numero_nodos * 3),j] = m_k_marco[i,j]
    Qu = m_k21_marco * Du
    numpy.set_printoptions(precision=5)      
    print Du
    print Du[2,0]
    for eli in range(len(elementos)):
        elementos[eli].des2 = [[0 for x in range(1)] for x in range(6)]   
        if elementos[eli].nodo_N.apoyo:        
            elementos[eli].des2[0][0] = 0
            elementos[eli].des2[1][0] = 0
            elementos[eli].des2[2][0] = 0
        else:
            elementos[eli].des2[0][0] = Du[elementos[eli].nodo_N.r_1, 0]
            elementos[eli].des2[1][0] = Du[elementos[eli].nodo_N.r_2, 0]
            elementos[eli].des2[2][0] = Du[elementos[eli].nodo_N.r_3, 0]   
        if elementos[eli].nodo_F.apoyo:        
            elementos[eli].des2[3][0] = 0
            elementos[eli].des2[4][0] = 0
            elementos[eli].des2[5][0] = 0
        else:
            elementos[eli].des2[3][0] = Du[elementos[eli].nodo_F.r_1, 0]
            elementos[eli].des2[4][0] = Du[elementos[eli].nodo_F.r_2, 0]
            elementos[eli].des2[5][0] = Du[elementos[eli].nodo_F.r_3, 0]
        elementos[eli].des2 = numpy.matrix(numpy.asanyarray(elementos[eli].des2))
        elementos[eli].q_nodos = (elementos[eli].m_k_local * elementos[eli].m_t_des) * elementos[eli].des2
        
    raw_input("presione la ultima tecla enter para continuar... Este es el final progrado del script, con fines de identificacion.")


if __name__ == "__main__":
    main()