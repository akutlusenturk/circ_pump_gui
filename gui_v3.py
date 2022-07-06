
import streamlit as st
import time
import numpy as np
import pandas as pd

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
    

    

st.set_page_config(
 page_title='Sirkülasyon Testi',
 layout="wide",
 initial_sidebar_state="expanded",
)

st.sidebar.markdown('''
### Sirkülasyon Testi
Yapılacak değişiklikler programı resetler.
''')

marka = st.sidebar.text_input("Pompa Markası:","Wilo")
model = st.sidebar.text_input("Pompa Modeli:","Yonos_25-80")
mod   = st.sidebar.text_input("Çalıştırma Modu:","dP5.0")
zamandamgasi = time.strftime("]_%Y%b%d_%H.%M.%S")
isim = marka+"_"+model+"_["+mod+zamandamgasi

i = 0
t = 0

st.sidebar.write("Otomatik Vana Modunda Deney")
Dint = st.sidebar.number_input("Başlangıç Noktası:",value=8.0)
Dfin = st.sidebar.number_input("Bitiş Noktası:",value=75.0)
ds = st.sidebar.number_input("Adım Aralığı",value=0.25)
dt = st.sidebar.number_input("Adımlar Arası Periyot",value=8)

if st.sidebar.button("Otomatik Modda Kayıt Başlat"):
    kaydet = 1
else:
    kaydet = 0,
    
st.sidebar.write("Manuel Vana Ayarı")
D = st.sidebar.number_input("Vana Açıklığı [0:Kapalı -90:Açık]",value=0.0)
if st.sidebar.button("Ayarla"): 
    yaz(64,[int(D*4)])
    

    
sozluk =[
    ['Date'                   ,"Tarih"                  ,"YMD"       ,""         ],
    ['Time'                   ,"Zaman"                  ,"HMS"       ,""         ],
    ['Temperature'            ,"Sıcaklık"               ,"T"         ,"°C"       ],
    ['Flow_Rate'              ,"Debi"                   ,"Q"         ,"m³/saat"  ],
    ['Valve_Aperture'         ,"Vana Açıklığı"          ,"D"         ,"°"        ],
    ['Static_Pressure'        ,"Durağan Basınç"         ,"P"         ,"Bar"      ],
    ['Suction_Pressure'       ,"Emme Basıncı"           ,"P1"        ,"Bar"      ],
    ['Discharge_Pressure'     ,"Basma Basıncı"          ,"P2"        ,"Bar"      ],
    ['Voltage'                ,"Gerilim"                ,"V"         ,"V"        ],
    ['Current'                ,"Akım"                   ,"I"         ,"A"        ],
    ['Measured_Frequency'     ,"Ölçülen Frekans"        ,"f"         ,"Hz"       ],
    ['Active_Power'           ,"Aktif Güç"              ,"PAP"       ,"W"        ],
    ['Reactive_Power'         ,"Reaktif Güç"            ,"QRP"       ,"VAr"      ],
    ['Apperent_Power'         ,"Görünür Güç"            ,"SAP"       ,"VA"       ],
    ['Phase_Voltage_Angle'    ,"Faz Gerilim Açısı"      ,"PVA"       ,"°"        ],
    ['Phase_Current_Angle'    ,"Faz Akım Açısı"         ,"PCA"       ,"°"        ],
    ['Cos_Phi'                ,"Cos_Phi"                ,"PHI"       ,""         ],
    ['Power_Factor'           ,"Güç Faktörü"            ,"PF"        ,""         ],
    ['Differential_Pressure'  ,"Fark Basıncı"           ,"DP"        ,"Bar"      ],
    ['Head'                   ,"Basma Yüksekliği"       ,"H"         ,"m"        ],
    ['Hydraulic_Power'        ,"Hidrolik Güç"           ,"PHYD"      ,"W"        ],
    ['Efficiency'             ,"Verimlilik"             ,"ETA"       ,"%"        ]
    ]
    
varis = []
for i in sozluk: varis.append(i[0])  #sozluk ilk sütun  (Türkçe için 0 yerine 1. sütun seçilebilir.)
df = pd.DataFrame(columns=varis)
buffy = pd.DataFrame(columns=varis)



col = st.columns(4)
 

###################################### G R A F İ K L E R #############################################

col[0].subheader("Debi & Basma Yüksekliği [m³/h,m]  \n Flow Rate & Head")
QHt = col[0].line_chart()

col[0].subheader("Hidrolik Güç & Verimlilik [W,%] \n Hydraulic Power & eta")
PHYDETAt = col[0].line_chart()

col[1].subheader("Emme & Basma Basınçları [Bar] \n Suction & Discharge Pressure")
P1P2t = col[1].line_chart()

col[1].subheader("Elektrik Güçleri [W, VA, VAr] \n Active, Reactive & Apperent Power" )
PAPQRPSAP = col[1].line_chart()

col[2].subheader("cos(φ) & Güç Faktörü \n cos(φ) & Power Factor")
PHIPFt = col[2].line_chart()

col[2].subheader("Faz Gerilim & Akım Açıları [°] \n Phase Voltage & Current Angles")
PVAPCAt = col[2].line_chart()

###################################### M E T R İ K L E R ##############################################

col[3].write(f"Deney Kimliği: \n {isim}")
YMDt = col[3].empty()
HMSt = col[3].empty()
Tt = col[3].empty()
Dt = col[3].empty()
Pt = col[3].empty()
Vt = col[3].empty()
ft = col[3].empty()

######################################### D Ö N G Ü ####################################################

while True:
    t=t+1
    buff = np.array(veri())
    df.loc[len(df)]=buff  
    
    if t%1==0:
        with Tt:
            st.metric("Hat Sıcaklığı",f"{buff[2]} °C")
        with YMDt:
            st.metric("Tarih",buff[0])
        with HMSt:
            st.metric("Saat",buff[1])
        with Dt:
            st.metric("Vana Açıklığı",f"{buff[4]} °")
        with Pt:
            st.metric("Durağan Basınç",f"{buff[5]} Bar")
        with Vt:
            st.metric("Gerilim",f"{buff[8]} v")
        with ft:
            st.metric("Ölçülen Frekans",f"{buff[10]} Hz")
        
        QHt.add_rows([[float(buff[3]),float(buff[19])]])
        PHYDETAt.add_rows([[float(buff[20]),float(buff[21])]])
        P1P2t.add_rows([[float(buff[6]),float(buff[7])]])
        PHIPFt.add_rows([[float(buff[16]),float(buff[17])]])
        PAPQRPSAP.add_rows([[float(buff[11]),float(buff[12]),float(buff[13])]])
        PVAPCAt.add_rows([[float(buff[14]),float(buff[15])]])
    

    if kaydet == 1:
        if t%dt==0 and Dint<Dfin:
            Dint=Dint+ds
            yaz(64,[int(Dint*4)])
        elif Dint>=Dfin:
            df.to_excel(f"{isim}.xlsx")
            kaydet=0
        


    
    
