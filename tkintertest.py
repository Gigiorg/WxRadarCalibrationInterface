import tkinter
from tkinter import *
import tkinter.ttk as ttk
import datetime
from tkinter import filedialog, Variable

from PIL import Image, ImageTk

import os
import h5py
import argparse
import sys
from datetime import  timedelta
import numpy as np
import math
import simplekml
from geopy import distance, location
import pandas as pd
#from sciṕy.constants import speed_of_light
import matplotlib.pyplot as plt

class RadarInterface():
    def __init__(self, master):
        self.master = master
        self.master.title("Radar Interface")
        self.master.geometry("1200x650+100+100")
        self.master.resizable(0, 0)

        self.sys_time = StringVar()
        self.sys_time.set(datetime.datetime.now().strftime("%H:%M:%S"))

        self.idx_min_range_bin = 94  # Indice del primer range bin de deteccion
        self.idx_t_conm = 87  # Indice del range bin de t/conmutacion
        self.idx_file = 0
        self.idx_exp_ele = 20


        #variables
        self.list_items = []
        self.list_box_items = Variable(value = self.list_items)


        frm_base = Frame(self.master, padx = 10, pady = 10)
        frm_base.pack(side = TOP)

        notebook = ttk.Notebook(frm_base)
        notebook.pack(pady=10, expand=True)


        frm = Frame(self.master, padx=10, pady=10)
        frm_param = Frame(self.master, padx=10, pady=10)

        notebook.add(frm, text='Interfaz Principal')
        notebook.add(frm_param, text='Parametros')

        #canvas = Canvas(frm_param)
        #canvas.pack(side=TOP, fill=BOTH, expand=True)

        img = Image.open('123431.png')
        img1 = PhotoImage('123431.png')
        img2 = ImageTk.PhotoImage(img)

        '''  
        img = PhotoImage(file="bd-sophy.png")
        canvas.create_image(5,5, image=img)
        '''
        img_label = Label(frm_param, image=img2)
        img_label.pack()
        #canvas.create_image(40, 20, image=img)

        frm1 = Frame(frm, padx=10, pady=10)
        frm1.grid(row=0, column=0, sticky='n')

        frm2 = Frame(frm, padx=10, pady=10)
        frm2.grid(row=0, column=1, rowspan=2)

        frm3 = Frame(frm, padx=10, pady=10)
        frm3.grid(row=0, column=2, rowspan=2)

        frm4 = Frame(frm, padx=10, pady=10)
        frm4.grid(row=3, column=0, sticky='n')

        #frm5 = Frame(frm, padx=10, pady=10)
        #frm5.grid(row=3, column=1, sticky='w')

        frm6 = Frame(frm, padx=10, pady=10)
        frm6.grid(row=3, column=1, columnspan= 2)

        lblFrameExperiments = ttk.Labelframe(frm1, text="Experimentos")
        lblFrameExperiments.pack()

        lblFrameHardConstant = ttk.Labelframe(frm2, text="Constante de Hard Targets")
        lblFrameHardConstant.pack()

        lblFrameSoftConstant = ttk.Labelframe(frm3, text="Constante de Soft Targets")
        lblFrameSoftConstant.pack()

        lblFrameButtons = ttk.LabelFrame(frm4, text="Acciones", height = 80, width = 100)
        lblFrameButtons.pack()
        #lblFrameButtons.grid_propagate(False)

        #lblFrameParameters = ttk.LabelFrame(frm5, text="Parámetros de Radar")
        #lblFrameParameters.pack()

        lblFrameChannels = ttk.Labelframe(frm6, text="Constantes de Calibacion")
        lblFrameChannels.pack()

        #------------------LBLFRMEXPERIMENTS--------------------------------------------------

        self.lstBoxExperiments = tkinter.Listbox(lblFrameExperiments, listvariable=self.list_box_items, width= 40, height= 12)
        self.lstBoxExperiments.pack()


        #------------------LBLFRMHARDTARGETS--------------------------------------------------

        self.lstBoxHardConstant = tkinter.Listbox(lblFrameHardConstant, width= 40, height = 18)
        self.lstBoxHardConstant.pack()


        #------------------LBLFRMSOFTTARGETS--------------------------------------------------

        self.lstBoxSoftConstant = tkinter.Listbox(lblFrameSoftConstant, width= 40, height = 18)

        self.lstBoxSoftConstant.pack()


        #------------------LBLFRMBUTTONS--------------------------------------------------

        self.btnAddExperiment = tkinter.Button(lblFrameButtons, text="Añadir experimento", width=35, command = self.loadExperiment)
        self.btnCalculateHard = tkinter.Button(lblFrameButtons, text="Calcular constante de hard-targets", width=35, command = self.calculateHardConstant,
                                               pady=5)
        self.btnCalculateSoft = tkinter.Button(lblFrameButtons, text="Calcular constante de soft-targets", width=35,
                                               pady=5)
        self.btnCalculateChannels = tkinter.Button(lblFrameButtons, text="Calcular constantes de ambos canales",
                                                   width=35, pady=5)

        self.btnAddExperiment.grid(row=0, column=0, rowspan=1)
        self.btnCalculateHard.grid(row=1, column=0, rowspan=1)
        self.btnCalculateSoft.grid(row=2, column=0, rowspan=1)
        self.btnCalculateChannels.grid(row=3, column=0, rowspan=1)

        #------------------LBLFRMPARAMETERS--------------------------------------------------
        '''
        self.lblRadarFrequency = ttk.Label(lblFrameParameters, text="Frecuencia operativa de radar: ")
        self.lblPulseWidth= ttk.Label(lblFrameParameters, text="Ancho de Pulso: ")
        self.lblPowerThreshold= ttk.Label(lblFrameParameters, text="Umbral de Potencia: ")
        self.lblTransmittedPower = ttk.Label(lblFrameParameters, text="Potencia de Transmisión: ")
        self.lblLnaGain = ttk.Label(lblFrameParameters, text="Ganancia de LNA: ")
        #
        self.powerThreshold = DoubleVar(value=-45.2)
        self.transmittedPower = DoubleVar(value=44)
        self.pulseWidth = DoubleVar(value=0.1)
        self.radarFrequency = DoubleVar(value=9.375)
        self.lnaGain = DoubleVar(value=70)

        #unidades
        self.lblGHz = ttk.Label(lblFrameParameters, text="GHz")
        self.lblDbm = ttk.Label(lblFrameParameters, text="dBm")
        self.lblDbPower = ttk.Label(lblFrameParameters, text="dB")
        self.lblDbLna = ttk.Label(lblFrameParameters, text="dB")
        self.lblUs = ttk.Label(lblFrameParameters, text="us")

        self.entryRadarFrequency = ttk.Entry(lblFrameParameters, width=8, textvariable=self.radarFrequency)
        self.entryPulseWidth = ttk.Entry(lblFrameParameters, width=8, textvariable=self.pulseWidth)
        self.entryPowerThreshold = ttk.Entry(lblFrameParameters, width=8, textvariable=self.powerThreshold)
        self.entryTransmittedPower = ttk.Entry(lblFrameParameters, width=8, textvariable=self.transmittedPower)
        self.entryLnaGain = ttk.Entry(lblFrameParameters, width=8, textvariable=self.lnaGain)

        #


        self.lblRadarFrequency.grid(row= 0, column=0, pady = 3)
        self.lblPulseWidth.grid(row= 1, column=0, pady = 3)
        self.lblPowerThreshold.grid(row= 2, column=0, pady = 3)
        self.lblTransmittedPower.grid(row= 3, column=0, pady = 6)
        self.lblLnaGain.grid(row=4, column=0, padx=25, pady=6)

        self.entryRadarFrequency.grid(row= 0, column=1, padx = 25, pady = 3)
        self.entryPulseWidth.grid(row= 1, column=1, padx = 25, pady = 3)
        self.entryPowerThreshold.grid(row= 2, column=1, padx = 25, pady = 6)
        self.entryTransmittedPower.grid(row= 3, column=1, padx = 25, pady = 6)
        self.entryLnaGain.grid(row=4, column=1, padx=25, pady=6)


        self.lblGHz.grid(row= 0, column=2, padx = 3, pady = 6)
        self.lblUs.grid(row= 1, column=2, padx = 3, pady = 6)
        self.lblDbPower.grid(row= 2, column=2, padx = 3, pady = 6)
        self.lblDbm.grid(row= 3, column=2, padx = 3, pady = 6)
        self.lblDbLna.grid(row=4, column=2, padx=3, pady=6)
        '''

        #------------------LBLFRMCHANNELS--------------------------------------------------

        self.lblChannel1 = ttk.Label(lblFrameChannels, text="Canal H: ")
        self.lblChannel2 = ttk.Label(lblFrameChannels, text="Canal V: ")

        self.entryChannel1 = ttk.Entry(lblFrameChannels, width=8)
        self.entryChannel2 = ttk.Entry(lblFrameChannels, width=8)

        self.lblChannel1.grid(row= 0, column=0,padx = 20)
        self.lblChannel2.grid(row= 0, column=2,padx = 20)
        self.entryChannel1.grid(row= 0, column=1, pady= 23, padx = 70)
        self.entryChannel2.grid(row= 0, column=3, pady= 23, padx = 70)

        # master.after(10, self.update_time)

    # def update_time(self):
    #     self.change_time()
    #
    # def change_time(self):
    #     self.sys_time.set(datetime.datetime.now().strftime("%H:%M:%S"))
    #     self.master.after(10, self.update_time)




    def loadExperiment(self):
            filepath = filedialog.askdirectory()
            experiment = filepath.split('/')[-1]
            self.list_items.append(filepath)
            self.lstBoxExperiments.insert(self.lstBoxExperiments.size(),experiment)
            #print(self.list_items)


    def calculateHardConstant(self):

        def get_sphere_drone_echoes(power):
            print(power)


        def get_time_for_hdf5(file):
            utc_time = datetime.datetime.fromtimestamp(file['Data']['time'][0]).replace(microsecond=0)
            return utc_time

        def get_powerH(file):
            #hPower = np.array(h5f['Data']['power']['H'])  # Canal H
            hPower = np.array(file['Data']['data_param']['channel00'])  # Canal H
            return hPower

        def get_powerV(file):
            #vPower = np.array(h5f['Data']['power']['V'])  # Canal V
            vPower = np.array(file['Data']['data_param']['channel01'])  # Canal H
            return vPower

        def get_elevation_h5f(file):
            elevation = np.array(file['Metadata']['elevation'])  # Elevacion
            return elevation

        def get_range_h5f(file):
            range = np.array(file['Metadata']['range'])  # Rango
            return range

        def get_azimuth_h5f(file):
            azimuth = np.array(file['Metadata']['azimuth']).mean()
            return azimuth

        def remove_failed_profiles(dPower):

            '''
            Remueve los perfiles fallados (perfiles con un valor atipico de potencia en todos los range bins).
            Entrada --> Dataset original
            Salida --> Dataset filtrado

            '''

            first_from_row = dPower[:, 0]
            idx_fail = np.where(np.isnan(first_from_row) == False)

            for idx in idx_fail[0]:
                dPower[idx, :] = 1e-7

            idx_wrong = np.where(np.isnan(first_from_row) == False)
            return dPower

        def is_sphere_drone_detected(dPower):

            """
            Retorna True si del dataset se reconocen ecos correspondientes al drone y la esfera separados por un espacio
            (ecos de potencia menor). Retorna False si no se reconoce el patron ecos fuertes - espacio de ecos debiles - ecos fuertes
            dentro del dataset.
            """

            n_gaps = 0
            end = False

            dPowerdB = 10 * np.log10(dPower)  # dataset en dBm

            x, y = np.where(dPowerdB[self.idx_exp_ele:,
                            self.idx_min_range_bin:self.idx_min_range_bin + 4] > self.powerThreshold.get())  # filtro de valores de potencia

            x += self.idx_exp_ele
            y += self.idx_min_range_bin

            x = list(sorted(set(x)))  # se guardan los perfiles con valores de potencia sospechosos (drone y esfera)

            for i in range(len(x)):

                try:
                    # si hay perfiles consecutivos con valores de potencia reconocibles
                    if (x[i] + 1) == x[i + 1]:
                        # print("next")
                        if n_gaps >= 1:
                            end = True
                    else:
                        # Se detecta el espacio entre el drone y la esfera
                        # print("gap")
                        n_gaps += 1

                except:
                    pass

            return end

        for exp in self.list_items:

            path_hdf5 =  exp + '/param-0.5km-0/' + os.listdir(exp + '/param-0.5km-0')[0]

            for file in sorted(os.listdir(path_hdf5)):

                h5_file = h5py.File(path_hdf5 + '/' + file, 'r')

                powerH = get_powerH(h5_file)
                powerV = get_powerV(h5_file)

                elevation_arr = get_elevation_h5f(h5_file)
                range_arr = get_range_h5f(h5_file)
                azimuth_arr = get_azimuth_h5f(h5_file)
                tmstamp = get_time_for_hdf5(h5_file)

                # Eliminando los perfiles fallidos
                powerH_corr = remove_failed_profiles(powerH)
                powerV_corr = remove_failed_profiles(powerV)

                powerV_corr_power = 10 * np.log10(powerV_corr)
                powerV_corr_power = 10 ** (powerV_corr_power / 10)

                #Si se detectan ecos correspondientes al drone y a la esfera:
                if(is_sphere_drone_detected(powerH_corr)):
                    print("SI")
                else:
                    print("NO")






root = Tk()
app = RadarInterface(root)
root.mainloop()
