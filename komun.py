from pyModbusTCP.client import ModbusClient
import numpy as np
import time

np.set_printoptions(suppress=True)


##############################################################################

SERVER_HOST = "192.168.1.15"
SERVER_PORT = 502
SERVER_U_ID = 1

c = ModbusClient()

c.host(SERVER_HOST)
c.port(SERVER_PORT)
c.unit_id(SERVER_U_ID)

us=np.arange(1,24)
taban=np.full((23),2)
maske=1/np.power(taban,us)

##############################################################################

def oku(reg=100,n=10):
    if not c.is_open():
        if not c.open():
            print("unable to connect to "+SERVER_HOST+":"+str(SERVER_PORT))
    if c.is_open():
        regs = c.read_holding_registers(reg,n)
        #print(f"Register {reg} to {reg+n-1} is read.")
    return regs

##############################################################################

def yaz(reg,n):
    if not c.is_open():
        if not c.open():
            print("unable to connect to "+SERVER_HOST+":"+str(SERVER_PORT))
    if c.is_open():
        c.write_multiple_registers(reg,n)   
        

##############################################################################

def veri():
    YMD = time.strftime("%Y/%m/%d")
    HMS = time.strftime("%H:%M:%S")
    T = np.round(ieee_con(oku(36,2)),1) 
    Q = np.round(ieee_con(oku(40,2)),3) 
    D = np.round((oku(64,1)[0])/4,2)
    P = np.round(ieee_con(oku(30,2)),2)
    P1 = np.round(ieee_con(oku(32,2)),3) 
    P2 = np.round(ieee_con(oku(34,2)),3)   
    V = np.round(oku(43,1)[0]*0.1,1)               
    I = np.round(oku(45,1)[0]*0.001,2)
    f = np.round(oku(47,1)[0]*0.01,2)
    PAP = np.round(ieee_con(oku(38,2)),2)
    QRP = np.round(ieee_con(oku(48,2)),2)
    SAP = np.round(ieee_con(oku(56,2)),2) 
    PVA = np.round(oku(59,1)[0]*0.1,2)                         
    PCA = np.round(oku(55,1)[0]*0.1,2)                         
    PHI = np.round((2**16-oku(52,1)[0])*0.001,2)           
    PF = np.round((2**16-oku(50,1)[0])*0.001,2)        
    DP = np.round(P2-P1,3)
    H = np.round(DP*100.000/9.807,3)
    PHYD = np.round(2.72*Q*H,2)
    ETA = np.round(PHYD/PAP*100,2)
    
    return([YMD,HMS,T,Q,D,P,P1,P2,V,I,f,PAP,QRP,SAP,PVA,PCA,PHI,PF,DP,H,PHYD,ETA])


##############################################################################
    
def ieee_con(n):
    sol="{0:016b}".format(int(n[1]))
    sag="{0:016b}".format(int(n[0]))
    ikili=sol+sag
    
    isaret=int(ikili[0]) #0 ise +; 1 ise -
    eksp=ikili[1:9]
    mantissa=ikili[9:]

    exb=int(eksp,2)-127 #127 is the bias for single precision
    manti=np.array(list(mantissa))
    frac=np.sum(manti.astype(int)*maske)
    sonuc=((-1)**isaret)*(1+frac)*(2**exb)

    return sonuc
    



        
        
    
    
    
    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    