#! /usr/bin/python3

import random
import time
import multiprocessing as mp

samples= 10**7  # REDUCED! 10^9 would need about 4 hours on this old hardware

def riggedDice():
  if random.random() < 0.25:
    return 6
  else:
    return random.randint( 1, 5 )


def myTestProcess( n ):
  count= [n,0,0,0,0,0,0]
  for _ in range( n ):
    count[ riggedDice() ]+= 1
  return count


if __name__ == "__main__":
  mp.set_start_method("spawn", force=True)

  cores= mp.cpu_count()
  jobsPerCore= samples // cores
  remaining= samples % cores
  joblist= [jobsPerCore] * cores
  joblist[0]+= remaining

  # test riggedDice() in parallel
  t0= time.time()
  with mp.Pool(cores) as pool:
    result= pool.map( myTestProcess, joblist )
  duration= time.time() - t0

  count= [0] * 7
  for cpu in range( cores ):
    for throw in range( 1, 7 ):
      count[throw]+= result[cpu][throw]

  # print results and time
  print( f'{samples} samples:\n' )

  for n in range( 1, 7 ):
    percent= ( count[n] / samples ) * 100
    print( f'{n}: {count[n]} {percent:.3f}%' )

  print( f'\nduration: {duration:.3f}s' )

