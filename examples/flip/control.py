import numpy as np
import math
import time

import logger

def control(t,state,prev):
	dt=0.05
	k_omega=2000
	k_alpha=300000

	#state=logger.state()
	gyrox=state[0]
	gyroy=state[1]
	gyroz=state[2]
	#q0=state[3]
	#q1=state[4]
	#q2=state[5]
	#q3=state[6]
	
	gyroxprev=prev[0]
	gyroyprev=prev[1]
	gyrozprev=prev[2]

	omega=matrix([[gyrox], [gyroy], [gyroz]])
	omegaprev=matrix([[gyroxprev], [gyroyprev], [gyrozprev]])
	alpha=(omega-omegaprev)/dt

	omega_d=matrix([[omega_dx(t)], [0], [0]])
	e_omega=omega-omega_d

	alpha_d=matrix([[omega_d_dotx(t)], [0], [0]])
	e_alpha=alpha-alpha_d
	
	torque=-k_omega*np.matmul(eye(3,dtype=float),e_omega) -k_alpha*np.matmul(eye(3,dtype=float),e_alpha)
	#phi_g=180/pi*arctan2(2*(q0*q1+q2*q3),1-2*(q2**2+q3**2))
	#if(phi_g<=180):
		#
	return torque

def omega_dx(t):
	r=0
	Phi_g1=180
	Phi_g3=180
	omega_max=1400
	gamma1=(1/omega_max)*Phi_g1
	gamma3=(1/omega_max)*Phi_g3
	beta1=-(3/4)*(1/gamma1**3)*omega_max
	beta3=-(3/4)*(1/gamma3**3)*omega_max
	delta=0.26
	if(t<delta):
		r=(beta1/3)*(t-gamma1)**3-beta1*gamma1**2*t+beta1*gamma1**3/3
	if(t>delta):		
		r=(beta3/3)*(gamma3+delta-t)**3-beta3*gamma3**2*(2*gamma3+delta-t)+beta3*gamma3**3/3
	return r


def omega_d_dotx(t):
	r=0
	Phi_g1=180
	Phi_g3=180
	omega_max=1400
	gamma1=(1/omega_max)*Phi_g1
	gamma3=(1/omega_max)*Phi_g3
	beta1=-(3/4)*(1/gamma1**3)*omega_max
	beta3=-(3/4)*(1/gamma3**3)*omega_max
	delta=0.26
	if(t<delta):
		r=beta1*(gamma1-t)**2-beta1*gamma1**2
	if(t>delta):
		r=beta3*gamma3**2-beta3*(delta+gamma3-t)**2
	return r
