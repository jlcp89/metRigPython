# -*- coding: utf-8 *-*
from carga_distribuida import CargaDistribuida
from carga_puntual import CargaPuntual
from nodo import Nodo
import math
import scipy
import numpy


class Elemento():

    def __init__(self):
        self.E = 0  # modulo de elasticidad del elemento en (ksi) kilolibras por pulgada cuadrada
        self.id_elemento = 0
        self.nodo_N = Nodo()
        self.nodo_F = Nodo()
        self.angulo_x = 0.00
        self.angulo_y = 0.00
        self.angulo_r_horizontal = 0.00  # angulo que el elemento forma con la horizontal
        self.longitud = 0.000  # en pies
        self.area_sec_tr = 0.00  # area de la seccion transversal del elemento, en pulgadas cuadradas (plg2)
        self.d_sec_tr = 0.0  # peralte de seccion transversal, en plg
        self.b_sec_tr = 0.0  # base de seccion transversal en plg
        self.cargas_puntuales = []  # lista que contiene las cargas puntuales en el elemento
        self.cargas_distribuidas = []  #lista que contiene las cargas puntuales en el elemento
        self.carga_actual_p = ''
        self.carga_actual_d = ''
        self.inercia_sec_tr = 0.00  # inercia de la seccion transversal para analisis estructural en pulgadas a la cuarta (plg4)
        self.tipo_elemento = ''
        self.matriz_k_local = [[0 for x in range(6)] for x in range(6)]   # matriz de rigidez, local del miembro    
        self.matriz_t_desp = [[0 for x in range(6)] for x in range(6)]
        self.matriz_t_fuer = [[0 for x in range(6)] for x in range(6)]
        self.matriz_k_global = []  # matriz de rigidez, global del miembro
        self.m_k_local = []
        self.m_t_des = []
        self.m_t_fue = []
        self.des2 = []
        self.q_nodos = []
        
    def calcular_propiedades(self, nodo1, nodo2):  # Calcula propiedades fisicas del elemento, en base a dados ingresados; importante que los nodos ingresados correspondan al elemento
        self.nodo_N = nodo1
        self.nodo_F = nodo2
        delta_x = self.nodo_F.co_x - self.nodo_N.co_x  # en pies
        delta_y = self.nodo_F.co_y - self.nodo_N.co_y  # en pies
        self.longitud = (((delta_x) ** 2) + ((delta_y) ** 2)) ** (0.5)  # en pies
        # self.area_sec_tr = self.d_sec_tr * self.b_sec_tr  # en plg2
        # self.inercia_sec_tr = (self.b_sec_tr * ((self.d_sec_tr) ** (3))) / 12  # en plg4
        self.angulo_x = (delta_x) / self.longitud
        self.angulo_y = (delta_y) / self.longitud
        if delta_x != 0:
            self.angulo_r_horizontal = math.atan(delta_y / delta_x)
        elif delta_x == 0 and self.nodo_N.co_y < self.nodo_F.co_y:
            self.angulo_r_horizontal = 2 * math.pi
        elif delta_x == 0 and self.nodo_N.co_y < self.nodo_F.co_y:
            self.angulo_r_horizontal = math.pi
        if self.angulo_x < self.angulo_y:
            self.tipo_elemento = 'columna'
        elif self.angulo_y < self.angulo_x:
            self.tipo_elemento = 'viga'
        else:
            self.tipo_elemento = 'elemento a 45 grados'
        a = self.area_sec_tr
        e = self.E
        i = self.inercia_sec_tr
        l_l = self.longitud * 12.00  # pasando la longitud de pies a pulgadas
        subp1 = (a * e) / l_l
        subp2 = (12 * e *  i) / (l_l ** 3)
        subp3 = (6 * e * i) / (l_l ** 2)
        subp4 = (4 * e * i) / l_l
        subp5 = (2 * e * i) / l_l
        self.matriz_k_local[0][0], self.matriz_k_local[0][1], self.matriz_k_local[0][2], self.matriz_k_local[0][3], self.matriz_k_local[0][4], self.matriz_k_local[0][5] = subp1, 0, 0, - subp1, 0, 0
        self.matriz_k_local[1][0], self.matriz_k_local[1][1], self.matriz_k_local[1][2], self.matriz_k_local[1][3], self.matriz_k_local[1][4], self.matriz_k_local[1][5] = 0, subp2, subp3, 0, - subp2, subp3
        self.matriz_k_local[2][0], self.matriz_k_local[2][1], self.matriz_k_local[2][2], self.matriz_k_local[2][3], self.matriz_k_local[2][4], self.matriz_k_local[2][5] = 0, subp3, subp4, 0, - subp3, subp5
        self.matriz_k_local[3][0], self.matriz_k_local[3][1], self.matriz_k_local[3][2], self.matriz_k_local[3][3], self.matriz_k_local[3][4], self.matriz_k_local[3][5] = - subp1, 0, 0, subp1, 0, 0
        self.matriz_k_local[4][0], self.matriz_k_local[4][1], self.matriz_k_local[4][2], self.matriz_k_local[4][3], self.matriz_k_local[4][4], self.matriz_k_local[4][5] = 0, - subp2, - subp3, 0, subp2, - subp3
        self.matriz_k_local[5][0], self.matriz_k_local[5][1], self.matriz_k_local[5][2], self.matriz_k_local[5][3], self.matriz_k_local[5][4], self.matriz_k_local[5][5] = 0, subp3,  subp5, 0, - subp3, subp4
        self.matriz_t_desp[0][0], self.matriz_t_desp[0][1], self.matriz_t_desp[0][2], self.matriz_t_desp[0][3], self.matriz_t_desp[0][4], self.matriz_t_desp[0][5] = self.angulo_x, self.angulo_y, 0, 0, 0, 0
        self.matriz_t_desp[1][0], self.matriz_t_desp[1][1], self.matriz_t_desp[1][2], self.matriz_t_desp[1][3], self.matriz_t_desp[1][4], self.matriz_t_desp[1][5] = - self.angulo_y, self.angulo_x, 0, 0, 0, 0
        self.matriz_t_desp[2][0], self.matriz_t_desp[2][1], self.matriz_t_desp[2][2], self.matriz_t_desp[2][3], self.matriz_t_desp[2][4], self.matriz_t_desp[2][5] = 0, 0, 1, 0, 0, 0
        self.matriz_t_desp[3][0], self.matriz_t_desp[3][1], self.matriz_t_desp[3][2], self.matriz_t_desp[3][3], self.matriz_t_desp[3][4], self.matriz_t_desp[3][5] = 0, 0, 0, self.angulo_x, self.angulo_y, 0
        self.matriz_t_desp[4][0], self.matriz_t_desp[4][1], self.matriz_t_desp[4][2], self.matriz_t_desp[4][3], self.matriz_t_desp[4][4], self.matriz_t_desp[4][5] = 0, 0, 0, - self.angulo_y, self.angulo_x, 0
        self.matriz_t_desp[5][0], self.matriz_t_desp[5][1], self.matriz_t_desp[5][2], self.matriz_t_desp[5][3], self.matriz_t_desp[5][4], self.matriz_t_desp[5][5] = 0, 0, 0, 0, 0, 1
        self.matriz_t_fuer[0][0], self.matriz_t_fuer[0][1], self.matriz_t_fuer[0][2], self.matriz_t_fuer[0][3], self.matriz_t_fuer[0][4], self.matriz_t_fuer[0][5] = self.angulo_x, - self.angulo_y, 0, 0, 0, 0
        self.matriz_t_fuer[1][0], self.matriz_t_fuer[1][1], self.matriz_t_fuer[1][2], self.matriz_t_fuer[1][3], self.matriz_t_fuer[1][4], self.matriz_t_fuer[1][5] = self.angulo_y, self.angulo_x, 0, 0, 0, 0
        self.matriz_t_fuer[2][0], self.matriz_t_fuer[2][1], self.matriz_t_fuer[2][2], self.matriz_t_fuer[2][3], self.matriz_t_fuer[2][4], self.matriz_t_fuer[2][5] = 0, 0, 1, 0, 0, 0
        self.matriz_t_fuer[3][0], self.matriz_t_fuer[3][1], self.matriz_t_fuer[3][2], self.matriz_t_fuer[3][3], self.matriz_t_fuer[3][4], self.matriz_t_fuer[3][5] = 0, 0, 0, self.angulo_x, - self.angulo_y, 0
        self.matriz_t_fuer[4][0], self.matriz_t_fuer[4][1], self.matriz_t_fuer[4][2], self.matriz_t_fuer[4][3], self.matriz_t_fuer[4][4], self.matriz_t_fuer[4][5] = 0, 0, 0, self.angulo_y, self.angulo_x, 0
        self.matriz_t_fuer[5][0], self.matriz_t_fuer[5][1], self.matriz_t_fuer[5][2], self.matriz_t_fuer[5][3], self.matriz_t_fuer[5][4], self.matriz_t_fuer[5][5] = 0, 0, 0, 0, 0, 1
        self.m_k_local = numpy.asmatrix(numpy.asarray(self.matriz_k_local))
        self.m_t_des = numpy.asmatrix(numpy.asarray(self.matriz_t_desp))
        self.m_t_fue = numpy.asmatrix(numpy.asarray(self.matriz_t_fuer))
        self.matriz_k_global= (self.m_t_fue * self.m_k_local) * self.m_t_des
        
    def agregar_carga_puntual(self, magnitud, dist):  # Guarda una nueva carga puntual en la lista de cargas puntuales
        self.carga_actual_p = CargaPuntual()
        self.cargas_puntuales.append(self.carga_actual_p)
        self.cargas_puntuales[- 1].magnitud = magnitud
        self.cargas_puntuales[- 1].x = dist

    def agregar_carga_distribuida(self, magnitud):  # Guarda una nueva carga Uniformemente ditribuida en la lista de cargas distribuidas
        self.carga_actual_d = CargaDistribuida()
        self.cargas_distribuidas.append(self.carga_actual_d)
        self.cargas_distribuidas[- 1].magnitud = magnitud   
        
        
    def calcular_fuerzas_para_analisis(self, nodos):  # En base a la condicion de carga ingresada, se calculan las acciones de empotramiento perfecto para analisis estructural.
        t_c_p = len(self.cargas_puntuales)  # total de cargas puntuales 
        t_c_d = len(self.cargas_distribuidas)  # total de cargas distribuidas
        t_fuerzas = 0.00  # magnitu total de las fuerzas aplicadas al elemento en kilolibras
        m_rea_N = 0.00  # suma de momentos respecto a N en kilolibras por pulgada kip-in
        m_rea_F = 0.00  # suma de momentos respecto a F en kip-in
        for puntuales in range(t_c_p):
            l = self.longitud
            p = self.cargas_puntuales[puntuales].magnitud
            a = self.cargas_puntuales[puntuales].x
            b = l - self.cargas_puntuales[puntuales].x
            t_fuerzas += p  # sumando aritmeticamente la carga actual al total de cargas, Sumatoria de Fuerzas en el Eje Y el elemento, recordando que X siempre esta de N a F.
            m_rea_N += (p * (b ** 2) * a) / l  # en kilolibras por pie, calculando momento y sumandolo al total, se calcula segun tabla pag 734 analisis estrutural Hibbeler 3ed.
            m_rea_F += (p * (a ** 2) * b) / l  # (Kip-ft) MOMENTOS DE EXTREMO FIJO, PARA ANALISIS ESTRUCTURAL
        for distribuidas in range(t_c_d):
            w = self.cargas_distribuidas[distribuidas].magnitud
            l = self.longitud
            t_fuerzas += w * l  # en kilolibras
            m_rea_N += (w * (l ** 2)) / 12  # en Kip-ft
            m_rea_F += (w * (l ** 2)) / 12  # en Kip-ft
        m_rea_N = (m_rea_N * 12)  # pasando momento de Kip-ft a Kip-in para analisis estructural, dejando momento en Kip-in
        m_rea_F = (m_rea_F * 12)  # dejando momento en Kip-in
        nodos[self.nodo_N.id_nodo].rb_1 += ((t_fuerzas / 2) * math.sin(self.angulo_r_horizontal))
        nodos[self.nodo_N.id_nodo].rb_2 -= (t_fuerzas / 2) * math.cos(self.angulo_r_horizontal)
        nodos[self.nodo_N.id_nodo].rb_3 -= m_rea_N
        nodos[self.nodo_N.id_nodo].rc_1 += (t_fuerzas / 2) * math.sin(self.angulo_r_horizontal)
        nodos[self.nodo_N.id_nodo].rc_2 += (t_fuerzas / 2) * math.cos(self.angulo_r_horizontal)
        nodos[self.nodo_N.id_nodo].rc_3 += m_rea_N
        nodos[self.nodo_F.id_nodo].rb_1 += (t_fuerzas / 2) * math.sin(self.angulo_r_horizontal)
        nodos[self.nodo_F.id_nodo].rb_2 -= (t_fuerzas / 2) * math.cos(self.angulo_r_horizontal)
        nodos[self.nodo_F.id_nodo].rb_3 += m_rea_F
        nodos[self.nodo_F.id_nodo].rc_1 += (t_fuerzas / 2) * math.sin(self.angulo_r_horizontal)
        nodos[self.nodo_F.id_nodo].rc_2 += (t_fuerzas / 2) * math.cos(self.angulo_r_horizontal)
        nodos[self.nodo_F.id_nodo].rc_3 -= m_rea_F
        self.nodo_N.cad = "N"
        self.nodo_F.cad = "F"
        #n_p_r = []
        #n_p_r.append(self.nodo_N)
        #n_p_r.append(self.nodo_F)
        return nodos
        
  