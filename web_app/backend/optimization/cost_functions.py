import matplotlib.pyplot as plt
import numpy as np

def hour_cost(q,gxp,d,Xb,Ce,Cv):
  if gxp > d: # is the generation higher than the demand?
    s = gxp - d 
    if s > Xb-q: # is the overgeneration capable of filling the batteries
      qn = Xb
      dc = -Cv*(s-(Xb-q))
      case = 1
      e_r = -(s-(Xb-q)) # electricity from the network
      e_s = d           # electricity from the solar panels
      e_b = Xb-q        # electricity to the battery
    else:
      qn = q + s # load the batteries
      dc = 0
      case = 2
      e_r = 0
      e_s = d
      e_b = s
  else:
    if d - gxp > q: # is the leftover demand higher than the load in the batteries?
      qn = 0
      dc = Ce*(d-gxp-q)
      case = 3
      e_r = d-gxp-q
      e_s = gxp
      e_b = -q
    else:
      qn = q - (d-gxp)
      dc = 0
      case = 4
      e_r = 0
      e_s = gxp
      e_b = -(d-gxp)
  #print(f"demmand {d}, power {gxp}, batttery {q}, {qn}, case {case}")
  return dc, qn, case, e_r, e_s, e_b

def electricity_cost(Xp,Xb,gv, dv, N, Ce, Cv, qinit):
  c = 0
  q = qinit
  if q>Xb:
    q = Xb
  qv = []
  casev = []
  e_rv, e_sv, e_bv = [],[],[]
  for i in range(N):
    [dc, q, case, e_r, e_s, e_b] = hour_cost(q, Xp*gv[i], dv[i], Xb, Ce, Cv)
    c += dc
    qv.append(q)
    casev.append(case)
    e_sv.append(e_s)
    e_bv.append(e_b)
    e_rv.append(e_r)
  return c, qv, casev, e_rv, e_sv, e_bv

def total_cost(Xp,Xb,irradiance, demand, N, Ce, Cv, qinit, Cb, Vb, Cp, Vp, Ninit = 2):
  ecost, battery_charge, casev, e_rv, e_sv, e_bv = electricity_cost(Xp,Xb,irradiance, demand, N, Ce, Cv, qinit)
  for i in range(Ninit):
    ecost, battery_charge, casev, e_rv, e_sv, e_bv = electricity_cost(Xp,Xb,irradiance, demand, N, Ce, Cv, battery_charge[-1]) # call it twice to use a better init battery charge

  fixcost = Xb*Cb/Vb + Xp*Cp/Vp
  npe_rv = np.asarray(e_rv) 
  rcost = npe_rv[npe_rv> 0].sum() # electricity from the network
  total_cost = ecost + fixcost
  return total_cost, rcost

  