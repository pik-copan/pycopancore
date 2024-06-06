
# This file is part of pycopancore.
#
# Copyright (C) 2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>


#import model:
from pycopancore.models import BBC

# standard runner for simulating any model:
from pycopancore.runners.runner import Runner

#needed packages:
import numpy as np
import pandas as pd
import os

#Loop for runing several experiments

#directors with the model imputs
directory = 'C:/Users/hhpra/Desktop/Ausbildung/Hu_Berlin/INRM/Masterarbeit/Model_input/SN_PBC_CC' # adopt!
sfile = 0
print(sfile)
for savefile in os.scandir(directory):
    f = os.path.join(directory, savefile)
    print(f)
    para = pd.read_excel(f)
    sfile = sfile + 1
    sfiles = str(sfile)
    print(sfiles)
    for index, row in para.iterrows():
        # instantiate the model and have it analyse its own structure:
        model = BBC.Model()


        # simulation parameters
        t_max = 2100  # interval for which the model will be simulated
        dt = 1  # desired temporal resolution of the resulting output.
        Emissions = pd.read_csv('C:/Users/hhpra/Desktop/Ausbildung/Hu_Berlin/INRM/Masterarbeit/Model_input/Emissions85.csv') # adopt to RCP szenario
        Emissions_array = Emissions.to_numpy()
        LUC = pd.read_csv('C:/Users/hhpra/Desktop/Ausbildung/Hu_Berlin/INRM/Masterarbeit/Model_input/LUC85.csv') # adopt to RCP szenario
        LUC_array = LUC.to_numpy()


        # instantiate process taxa:
        environment = BBC.Environment(
            #K_c = para["K_c"][index],
            #K_A = para["K_A"][index],
            #NPP = para["NPP"][index],
            #Q_R = para["Q_R"][index],
            #tau = para["tau"][index],
            #lam = para["lam"][index],
            #I_CC = para["I_CC"][index],
            #teta = para["teta"][index],
            #v_max = para["v_max"][index],
            #r_g = para["r_g"][index],
            #p_T = para["p_T"][index],
            #Dd = para["Dd"][index],
            #r = para["r"][index],
            #D_T = para["D_T"][index],
            #B_0 = para["B_0"][index],
            #B_T = para["B_T"][index],
            #B_TB = para["B_TB"][index],
            #B_A = para["B_A"][index],
            #w_0 = para["w_0"][index],
            #w_T = para["w_T"][index],
            #c_a0 = para["ca0"][index],
            #c_t0 = para["ct0"][index],
            #c_m0 = para["cm0"][index],
        )

        metabolism = BBC.Metabolism(
            emission_array=Emissions_array,
            LUC_array=LUC_array,
            #R_max_BD = para["R_max_BD"][index],
            #R_max_CC=para["R_max_CC"][index],
            #e_min=para["emin"][index],
            #i_min = para["imin"][index],
        )

        culture = BBC.Culture(
            #Ef_BD = para["Ef_BD"][index],
            #Ef_CC=para["Ef_CC"][index],
            #PBC_BD = para["PBC_BD"][index],
            PBC_CC=para["PBC_CC"][index],
            SN_CC=para["SN_CC"][index],
            #SN_BD = para["SN_BD"][index],
            #alp=para["alp"][index],
            #w1=para["w1"][index],
            #w2=para["w2"][index],
            #wA=para["wA"][index],
            #wN=para["wN"][index],
            #wC=para["wC"][index],
            TPB=para["TBP"][index],
            PR=para["PR"][index]
        )

        world = BBC.World(culture=culture, metabolism=metabolism, environment=environment)
        runner = Runner(model=model)
        traj = runner.run(t_0=1765, t_1=t_max, dt=dt)


        #get variables for saving
        temp = list(traj[BBC.Environment.temperature].values())
        temp = (temp[0])
        biodiv = list(traj[BBC.Environment.J].values())
        biodiv = (biodiv[0])
        SNCC = list(traj[BBC.Culture.SN_CC].values())
        SNCC = (SNCC[0])
        SNBD = list(traj[BBC.Culture.SN_BD].values())
        SNBD = (SNBD[0])
        PBCCC = list(traj[BBC.Culture.PBC_CC].values())
        PBCCC = (PBCCC[0])
        PBCBD = list(traj[BBC.Culture.PBC_BD].values())
        PBCBD = (PBCBD[0])
        filename = str(index+10)

        #choose variables for model output
        output_sensitivity = pd.DataFrame(np.column_stack([traj['t'], temp, biodiv, SNCC, PBCCC]),
                            columns=['time', 'Temperature' + filename, 'Biosiv_loss' + filename, "SN_CC"+filename, "PBC_CC"+filename])

        #save model outfut to file (for each run, a file with its number must be created prior to the runs)
        pd.DataFrame(output_sensitivity).to_csv(
            "C:/Users/hhpra/Desktop/Ausbildung/Hu_Berlin/INRM/Masterarbeit/Model_output/RCP_85/SN_PBC_runs/Non-Cum/CC/" + sfiles + "/" + filename + ".csv")

        #pd.DataFrame(output_sensitivity).to_csv(
            #"C:/Users/hhpra/Desktop/Ausbildung/Hu_Berlin/INRM/Masterarbeit/Model_output/RCP_45/monte_carlo_runs/MC_b/CC/try/" + filename + ".csv")

        #delete all entities and taxa so that they can be initiated again
        environment.delete()
        metabolism.delete()
        culture.delete()
        world.delete()
        print("taxonomies deleted!")

