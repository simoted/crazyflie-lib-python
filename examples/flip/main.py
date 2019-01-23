import logging
import time
from threading import Timer
from threading import Thread

import cflib.crtp  # noqa
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
#from cflib.crazyflie.log import LogConfig

import numpy as np

# Only output errors from the logging framework
logging.basicConfig(level=logging.ERROR)

if __name__ == '__main__':
	uri = 'radio://0/80/2M'
	# Initialize the low-level drivers (don't list the debug drivers)
	cflib.crtp.init_drivers(enable_debug_driver=False)
	# Scan for Crazyflies and use the first one found
#	le = Logger(uri)

	# The Crazyflie lib doesn't contain anything to keep the application alive,
	# so this is where your application should do something. In our case we
	# are just waiting until we are disconnected.
	#while le.is_connected:
		
	# Initialize the low-level drivers (don't list the debug drivers)
	cflib.crtp.init_drivers(enable_debug_driver=False)
	dt=0.05
	tfin=0.52

	with SyncCrazyflie(uri, cf=Crazyflie(rw_cache='./cache')) as scf:
		cf = scf.cf

		cf.param.set_value('kalman.resetEstimation', '1')
		time.sleep(0.1)
		cf.param.set_value('kalman.resetEstimation', '0')
		time.sleep(2)

		#for y in range(10):
		#	cf.commander.send_hover_setpoint(0, 0, 0, y / 25)
		#	time.sleep(0.1)
		
		#for _ in range(20):
		#	cf.commander.send_hover_setpoint(0, 0, 0, 0.4)
		#	time.sleep(0.1)
		
		t0=time.time()
		t=t0
		while(t<=t0+tfin):
			pre=t
			t=time.time()
			if(t>=pre+dt):
				#prev=state
				#state=logger.state()
				#torque=control(t,state,prev)
				cf.commander.send_angular_velocity_setpoint(omega_dx(t), 0, 0, 32767)#32767
				#cf.commander.send_angular_velocity_setpoint(100000, 100000, 100000, 40000)#32767
				time.sleep(0.1)

		#for _ in range(20):
		#	cf.commander.send_hover_setpoint(0, 0, 0, 0.4)
		#	time.sleep(0.1)

		#for y in range(10):
		#	cf.commander.send_hover_setpoint(0, 0, 0, (10 - y) / 25)
		#	time.sleep(0.1)
