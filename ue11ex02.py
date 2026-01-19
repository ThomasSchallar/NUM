#! /usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt
import time
import math
import multiprocessing as mp

xmin, xmax= 0.0, 1.0
ymin, ymax= 0.0, 1.0

centerX= ( xmax - xmin ) / 2
centerY= ( ymax - ymin ) / 2
R=       ( xmax - xmin ) / 2

def myPi( P ):
  x= np.random.uniform( xmin, xmax, P )
  y= np.random.uniform( ymin, ymax, P )

  inside= (x - centerX)**2 + (y - centerY)**2 <= R**2

  return inside.sum()


if __name__ == "__main__":
  mp.set_start_method("spawn", force=True)

  np.random.seed( 8325876 )

  for P in [ 10**5, 10**6, 10**7, 10**8 ]:
    cores= mp.cpu_count()
    jobsPerCore= P // cores
    remaining= P % cores
    joblist= [jobsPerCore] * cores
    joblist[0]+= remaining

    t0= time.time()
    with mp.Pool(cores) as pool:
      result= pool.map( myPi, joblist )
    duration= time.time() - t0

    inside= 0
    for cpu in range( cores ):
      inside+= result[cpu]

    pi_est= ( 4.0 * inside ) / P
    err= abs( math.pi - pi_est )
    print( f'P={P} ⇒ π~{pi_est:.7f}, Δ={err:.7f}, time= {duration:.3f}s' )

  print( 'done' )

#EOF