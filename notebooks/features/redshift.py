# From Ken Smith
# https://github.com/genghisken/gkutils/blob/master/gkutils/commonutils/generalutils.py#L1825

import math

def redshiftToDistance(z, H0 = 70.0):
   """redshiftToDistance.

   Args:
        z:
        H0: Hubble constant (km s-1 Mpc-1, default = 70.0)
   """

   # Cosmological Parameters (to be changed if required)
   WM = 0.3           # Omega_matter
   WV = 0.7           # Omega_vacuum
   #H0 = 70.0           # Hubble constant (km s-1 Mpc-1)

   # Other variables
   h = H0/100.0
   WR = 4.165E-5/(h*h)     # Omega_radiation
   WK = 1.0-WM-WV-WR       # Omega_curvature = 1 - Omega(Total)
   c = 299792.458          # speed of light (km/s)

   # Arbitrarily set the values of these variables to zero just so we can define them.

   DCMR  = 0.0             # comoving radial distance in units of c/H0
   DCMR_Mpc = 0.0          # comoving radial distance in units of Mpc
   DA = 0.0                # angular size distance in units of c/H0
   DA_Mpc = 0.0            # angular size distance in units of Mpc
   DA_scale = 0.0          # scale at angular size distance in units of Kpc / arcsec
   DL = 0.0                # luminosity distance in units of c/H0
   DL_Mpc = 0.0            # luminosity distance in units of Mpc
   DMOD = 0.0              # Distance modulus determined from luminosity distance
   a = 0.0                 # 1/(1+z), the scale factor of the Universe

   az = 1.0/(1.0+z)        # 1/(1+z), for the given redshift

   # Compute the integral over a=1/(1+z) from az to 1 in n steps
   n = 1000
   for i in range(n):
      a = az+(1.0-az)*(i+0.5)/n
      adot = math.sqrt(WK+ (WM/a) + (WR/(math.pow(a,2))) +(WV*math.pow(a,2)))
      DCMR = DCMR + 1.0/(a*adot)

   DCMR = (1.0-az)*DCMR/n           # comoving radial distance in units of c/H0
   DCMR_Mpc = (c/H0)*DCMR           # comoving radial distance in units of Mpc

   # Tangental comoving radial distance
   x = math.sqrt(abs(WK))*DCMR
   if x > 0.1:
      if WK > 0.0:
         ratio = 0.5*(math.exp(x)-math.exp(-x))/x
      else:
         ratio = math.sin(x)/x
   else:
      y = math.pow(x,2)
      if WK < 0.0:
         y=-y
      ratio = 1 + y/6.0 + math.pow(y,2)/120.0

   DA = az*ratio*DCMR               #angular size distance in units of c/H0
   DA_Mpc = (c/H0)*DA               #angular size distance in units of Mpc
   DA_scale = DA_Mpc/206.264806     #scale at angular size distance in units of Kpc / arcsec
   DL = DA/math.pow(az,2)                #luminosity distance in units of c/H0
   DL_Mpc = (c/H0)*DL               #luminosity distance in units of Mpc
   DMOD = 5*math.log10(DL_Mpc*1e6)-5     #Distance modulus determined from luminosity distance


   results = \
   {
      "dcmr_mpc": DCMR_Mpc,
      "da_mpc": DA_Mpc,
      "da_scale": DA_scale,
      "dl_mpc": DL_Mpc,
      "dmod": DMOD,
      "z" : z
   }

   return results
