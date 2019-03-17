#!/opt/Python/Python-3.7.2/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 27 15:30:18 2019

@author: christophirrenfried
"""

import subprocess,sys,os,copy,datetime

import numpy as np

import matplotlib.pyplot as plt
import matplotlib as mpl
#mpl.use("pgf")

import CoolProp.CoolProp as CP
from CoolProp.Plots import PropertyPlot
from CoolProp.Plots import SimpleCompressionCycle



def main():
    fluid="R1234yf"
    rrange=[10,20,50,100,200,300,400,500]
    prange=[1E5,2E5,4E5,6E5,8E5,10E5,12E5,16E5,20E5,25E5,30E5,40E5]

    plot_TS(fluid,rrange,prange)





def plot_TS(fluid,rrange,prange):
    ############### TS
    fig_x, fig_y = 14, 9
    fig=plt.figure(figsize=(fig_x, fig_y))
    ax = fig.gca()
    ax.set_ylim(240,400)
    ax.set_xlim(800,2000)

    qrange=np.linspace(0,1,10).tolist()
    ts = PropertyPlot(fluid, 'TS', unit_system='SI', tp_limits='ORC', axis=ax)#,reciprocal_density=True)
    ts.calc_isolines(CP.iQ, iso_range=qrange, num=10)

    ts.props[CP.iDmass]['color'] = 'red'
    ts.props[CP.iDmass]['lw'] = '0.5'
    ts.calc_isolines(CP.iDmass,iso_range=rrange, num=len(rrange),rounding=False)


    ## isobaric
    ts.props[CP.iP]['color'] = 'green'
    ts.props[CP.iP]['lw'] = '0.5'
    ts.calc_isolines(CP.iP, iso_range=prange, num=len(prange),rounding=False)


    ts.draw()

    axL=ts.get_axis_limits()

    ax.text(axL[0]+20, axL[3]-7,fluid,size=20) 


    t1=axL[3]-25
    t0=t1-5

    for p in prange:
        s1=CP.PropsSI("Smass","T",t1,"P",p,fluid)
        s0=CP.PropsSI("Smass","T",t0,"P",p,fluid)

        pA=np.array([s0,t0])
        pB=np.array([s1,t1])

        # Calculate the angle of the line
        dx, dy = pA-pB
        x_min, x_max = axL[0:2]
        y_min, y_max = axL[2:4]
        
        Dx = dx * fig_x / (x_max - x_min)
        Dy = dy * fig_y / (y_max - y_min)
        
        angle = (180/np.pi)*np.arctan( Dy / Dx)
        
        ax.text(s0, t0, str(format(p/1E5,'.0f'))+'bar', rotation = angle,
                horizontalalignment='left',
                verticalalignment='bottom', rotation_mode='anchor', color='green')


    t1=axL[3]-10
    t0=t1-5

    for r in rrange:
        s1=CP.PropsSI("Smass","T",t1,"Dmass",r,fluid)
        s0=CP.PropsSI("Smass","T",t0,"Dmass",r,fluid)
        
        pA=np.array([s0,t0])
        pB=np.array([s1,t1])
        
        # Calculate the angle of the line
        dx, dy = pA-pB
        x_min, x_max = axL[0:2]
        y_min, y_max = axL[2:4]
        
        Dx = dx * fig_x / (x_max - x_min)
        Dy = dy * fig_y / (y_max - y_min)
        
        angle = (180/np.pi)*np.arctan( Dy / Dx)
    
        ax.text(s0, t0, str(format(r,'.0f'))+'kg/m3', rotation = angle,
                horizontalalignment='left',
                verticalalignment='bottom', rotation_mode='anchor', color='red')


    t1=axL[2]
    t0=t1+8

    for q in qrange:
        s1=CP.PropsSI("Smass","T",t1,"Q",q,fluid)
        s0=CP.PropsSI("Smass","T",t0,"Q",q,fluid)

        pA=np.array([s0,t0])
        pB=np.array([s1,t1])

        # Calculate the angle of the line
        dx, dy = pA-pB
        x_min, x_max = axL[0:2]
        y_min, y_max = axL[2:4]

        Dx = dx * fig_x / (x_max - x_min)
        Dy = dy * fig_y / (y_max - y_min)

        angle = (180/np.pi)*np.arctan( Dy / Dx)
    
        ax.text(s0, t0, str(format(q,'.1f')), rotation = angle,
                horizontalalignment='left',
                verticalalignment='bottom', rotation_mode='anchor', color='gray')

    #fig.plot([s0,s1],[t0,t1],'ro')
    ## isobaric

    ax.grid()

    
    pgf_with_pdflatex = {
        "pgf.texsystem": "pdflatex",
        "pgf.preamble": [
            r"\usepackage[utf8x]{inputenc}",
            r"\usepackage[T1]{fontenc}",
        ]
    }
    mpl.rcParams.update(pgf_with_pdflatex)

    
    fig.savefig('TS.eps')
    fig.savefig("TS.pgf", bbox_inches="tight")
    ############### TS


# ############### ph
# ph = PropertyPlot(fluid, 'ph', unit_system='SI', tp_limits='ORC')

# ph.calc_isolines()



# ph.savefig('ph.eps')
# ph.show()
# ############### ph


# ############### pd
# pd = PropertyPlot(fluid, 'PD', unit_system='SI', tp_limits='ORC')


# pd.calc_isolines()


# pd.savefig('pv.eps')
# pd.show()
# ############### pv


# print('Zeichne kreisprozess')




# cycle = SimpleCompressionCycle(fluid, 'TS', unit_system='EUR')
# T0 = 300
# p0 = 5E5
# #pp.state.update(CoolProp.QT_INPUTS,0.0,T0-10)
# #p0 = pp.state.keyed_output(CoolProp.iP)
# T2 = 310
# p2 = 10E5
# #pp.state.update(CoolProp.QT_INPUTS,1.0,T2+15)
# #p2 = pp.state.keyed_output(CoolProp.iP)

# cycle.simple_solve(T0, p0, T2, p2, 0.7, SI=True)
# cycle.steps = 50
# sc = cycle.get_state_changes()
# pp.draw_process(sc)


# plt.close(cycle.figure)



# plt.show()


  
if __name__== "__main__":
  main()
