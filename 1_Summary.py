import streamlit as st
import plotly.express as px
import plotly.figure_factory as ff
import pandas as pd
import os
import base64
import warnings
warnings.filterwarnings('ignore')


st.set_page_config(page_title="Maintenance Summary" ,page_icon=":bar_chart:" ,layout="wide")

@st.cache_data
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


img = get_img_as_base64("dark.jpg")
img1 = get_img_as_base64("back1.jpg")

page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: url("data:image/png;base64,{img}");
background-size: 100%;
background-position: centered;
background-repeat: repeat;
background-attachment: local;
}}

[data-testid="stSidebar"] > div:first-child {{
background-image: url("data:image/png;base64,{img1}");
background-position: center; 
background-repeat: no-repeat;
background-attachment: fixed;
}}

[data-testid="stHeader"] {{
background: rgba(0,0,0,0);
}}

[data-testid="stToolbar"] {{
right: 2rem;
}}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)


st.title(":red[Maintenance Summary Page]")

df = pd.read_excel("Summary.xlsx")

#Monthly Data Calculation
option = st.selectbox(':rainbow[**Select** **Month**]',
    ('January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December' ))

dfM = df[(df['MONTH']==option)]

df_MON = df[(df['MONTH']==option)]
MON = df_MON.groupby(by = ["MONTH"], as_index = False)["MBDF"].sum()
MONT = int(MON["MBDF"].count())
#st.write(MONT)

if MONT > 0:
    MONC = MON["MONTH"].count()
else:
    MONC = 0

if MONT > 0:
    MOD = (":green[**YES**]")
else:
    MOD = (":red[**NO**]")

col3, col4 = st.columns((2))
with col3:
    st.write(':blue[**Month** **selected:**]'+ " ", option)
with col4:
    st.write(":blue[**Month** **Data** **Present** :]" + " " + str(MOD))

#Yealry & Date Filter Data Calculation

filterd = st.checkbox(":rainbow[**Click** **To** **Filter** **By** **Start** **&** **End** **Date**]")
FILTER =(":rainbow[**Year** **Till** **Date**]")
FILTERM =(":rainbow[**Month** **Till** **Date**]")
if filterd:
    #st.write("Yes")
    FILTER =(":rainbow[**Filter** **By** **Date** **Selected**]")
    col1, col2 = st.columns((2))
    df["Period"] = pd.to_datetime(df["Period"])

    startDate = pd.to_datetime(df["Period"]).min()
    endDate = pd.to_datetime(df["Period"]).max()

    with col1:
        date1 = pd.to_datetime(st.date_input(":rainbow[**YEAR** **START** **DATE**]", startDate))

    with col2:
        date2 = pd.to_datetime(st.date_input(":rainbow[**YEAR** **END** **DATE**]", endDate))

    df = df[(df["Period"] >= date1) & (df["Period"] <= date2)].copy()

#Calculations
#st.markdown("NUMBER OF V3 LINES")
V3TLA = int(df["V3TLA"].sum())
V3TLB = int(df["V3TLB"].sum())
V3TLC = int(df["V3TLC"].sum())

V3TLAM = int(dfM["V3TLA"].sum())
V3TLBM = int(dfM["V3TLB"].sum())
V3TLCM = int(dfM["V3TLC"].sum())

#st.markdown("NUMBER OF G3 LINES")
G3TLA = int(df["G3TLA"].sum())
G3TLB = int(df["G3TLB"].sum())
G3TLC = int(df["G3TLC"].sum())

G3TLAM = int(dfM["G3TLA"].sum())
G3TLBM = int(dfM["G3TLB"].sum())
G3TLCM = int(dfM["G3TLC"].sum())

#st.markdown("NUMBER OF GA LINES")
GATLA = int(df["GATLA"].sum())
GATLB = int(df["GATLB"].sum())
GATLC = int(df["GATLC"].sum())

GATLAM = int(dfM["GATLA"].sum())
GATLBM = int(dfM["GATLB"].sum())
GATLCM = int(dfM["GATLC"].sum())


#st.markdown("NUMBER OF M LINES")
MTLA = int(df["MTLA"].sum())
MTLB = int(df["MTLB"].sum())
MTLC = int(df["MTLC"].sum())

MTLAM = int(dfM["MTLA"].sum())
MTLBM = int(dfM["MTLB"].sum())
MTLCM = int(dfM["MTLC"].sum())

#st.markdown("V3 MACHINE BREAKDOWN MINUTES")
V3BM = int(df["V3BM"].sum())

V3BMM = int(dfM["V3BM"].sum())
#st.markdown(str(V3BM)+ " Minutes")

#st.markdown("G3 MACHINE BREAKDOWN MINUTES")
G3BM = int(df["G3BM"].sum())

G3BMM = int(dfM["G3BM"].sum())
#st.markdown(str(G3BM)+ " Minutes")

#st.markdown("GA MACHINE BREAKDOWN MINUTES")
GABM = int(df["GABM"].sum())

GABMM = int(dfM["GABM"].sum())
#st.markdown(str(GABM)+ " Minutes")

#st.markdown("M MACHINE BREAKDOWN MINUTES")
MBM = int(df["MBM"].sum())

MBMM = int(dfM["MBM"].sum())
#st.markdown(str(MBM)+ " Minutes")

#st.markdown("NUMBER OF LINES")
LINES = int(V3TLA+G3TLA+GATLA+MTLA+V3TLB+G3TLB+GATLB+MTLB+V3TLC+G3TLC+GATLC+MTLC)

LINESM = int(V3TLAM+G3TLAM+GATLAM+MTLAM+V3TLBM+G3TLBM+GATLBM+MTLBM+V3TLCM+G3TLCM+GATLCM+MTLCM)
#st.markdown(LINES)

#st.markdown("MACHINE BREAKDOWN FREQUENCY")
MBDF = int(df["MBDF"].sum())

MBDFM = int(dfM["MBDF"].sum())
#st.markdown(MBDF)

#st.markdown("MACHINE BREAKDOWN MINUTES")
MBDTM = int(V3BM+G3BM+GABM+MBM)

MBDTMM = int(V3BMM+G3BMM+GABMM+MBMM)
#st.markdown(str(MBDTM)+ " Minutes")

#st.markdown("MACHINE BREAKDOWN HOURS")
MBDTH = round(float(MBDTM/60),2)

MBDTHM = round(float(MBDTMM/60),2)
#st.markdown(str(MBDTH)+ " Hours")

#st.markdown("Kaizen")
KAIZEN = int(df["KAIZEN"].sum())

KAIZENM = int(dfM["KAIZEN"].sum())
#st.markdown(KAIZEN)

#st.markdown("HSE")
HSE = int(df["HSE"].sum())

HSEM = int(dfM["HSE"].sum())
#st.markdown(HSE)

#st.markdown("LPA")
LPA = int(df["LPA"].sum())

LPAM = int(dfM["LPA"].sum())
#st.markdown(LPA)

#st.markdown("DQR")
DQR = int(df["DQR"].sum())

DQRM = int(dfM["DQR"].sum())
#st.markdown(DQR)

#st.markdown("RED-TAG")
REDTAG = int(df["REDTAG"].sum())

REDTAGM = int(dfM["REDTAG"].sum())
#st.markdown(REDTAG)

#st.markdown("CPI")
CPI = int(df["CPI"].sum())

CPIM = int(dfM["CPI"].sum())
#st.markdown(CPI)

#st.markdown("TOTAL AVAILABLE TIME")
ATA = int(428)
ATB = int(403)
ATC = int(458)
TAT = int(((V3TLA+G3TLA+GATLA+MTLA)*ATA)+((V3TLB+G3TLB+GATLB+MTLB)*ATB)+((V3TLC+G3TLC+GATLC+MTLC)*ATC))

TATM = int(((V3TLAM+G3TLAM+GATLAM+MTLAM)*ATA)+((V3TLBM+G3TLBM+GATLBM+MTLBM)*ATB)+((V3TLCM+G3TLCM+GATLCM+MTLCM)*ATC))
#st.markdown(TAT)

if TAT > 0:
    #st.markdown("BREAKDOWN PERCENTAGE")
    MBDP = round(float((MBDTM/TAT)*100),2)
    #st.markdown(str(MBDP) +" %")
else:
    MBDP = 0

if TAT > 0:
    #st.markdown("BREAKDOWN PERCENTAGE")
    MBDPM = round(float((MBDTMM/TAT)*100),2)
    #st.markdown(str(MBDP) +" %")
else:
    MBDPM = 0

#MTBF & MTTR

if MBDF > 0:
    MTTR = round(float(MBDTM/MBDF),2)
    MTBF1 = float((TAT-MBDTM)/MBDF)
    MTBF = round(round(float(MTBF1/60),2),2)
else:
    MTTR = 0
    MTBF = round(float(TAT/60),2)

if MBDFM > 0:
    MTTRM = round(float(MBDTMM/MBDFM),2)
    MTBF1M = float((TATM-MBDTMM)/MBDFM)
    MTBFM = round(float(MTBF1M/60),2)
else:
    MTTRM = 0
    MTBFM = round(float(TATM/60),2)


if (V3TLA+V3TLB+V3TLC) > 0:
    #st.markdown("V3 MACHINE BREAKDOWN %")
    V3BP = round(float((V3BM/(V3TLA*ATA+V3TLB*ATB+V3TLC*ATC))*100),2)
    #st.markdown(str(V3BP)+ "  %")
else:
    V3BP = 0

if (V3TLAM+V3TLBM+V3TLCM) > 0:
    #st.markdown("V3 MACHINE BREAKDOWN %")
    V3BPM = round(float((V3BMM/(V3TLAM*ATA+V3TLBM*ATB+V3TLCM*ATC))*100),2)
    #st.markdown(str(V3BPM)+ "  %")
else:
    V3BPM = 0

if (G3TLA+G3TLB+G3TLC) > 0:
    #st.markdown("G3 MACHINE BREAKDOWN %")
    G3BP = round(float((G3BM/(G3TLA*ATA+G3TLB*ATB+G3TLC*ATC))*100),2)
    #st.markdown(str(G3BP)+ "  %")
else:
    G3BP = 0

if (G3TLAM+G3TLBM+G3TLCM) > 0:
    #st.markdown("G3 MACHINE BREAKDOWN %")
    G3BPM = round(float((G3BMM/(G3TLAM*ATA+G3TLBM*ATB+G3TLCM*ATC))*100),2)
    #st.markdown(str(G3BPM)+ "  %")
else:
    G3BPM = 0

if (GATLA+GATLB+GATLC) > 0:
    #st.markdown("GA MACHINE BREAKDOWN %")
    GABP = round(float((GABM/(GATLA*ATA+GATLB*ATB+GATLC*ATC))*100),2)
    #st.markdown(str(GABP)+ "  %")
else:
    GABP = 0

if (GATLAM+GATLBM+GATLCM) > 0:
    #st.markdown("GA MACHINE BREAKDOWN %")
    GABPM = round(float((GABMM/(GATLAM*ATA+GATLBM*ATB+GATLCM*ATC))*100),2)
    #st.markdown(str(GABPM)+ "  %")
else:
    GABPM = 0

if (MTLA+MTLB+MTLC) > 0:
    #st.markdown("M MACHINE BREAKDOWN %")
    MBP = round(float((MBM/(MTLA*ATA+MTLB*ATB+MTLC*ATC))*100),2)
    #st.markdown(str(MBP)+ "  %")
else:
    MBP = 0

if (MTLAM+MTLBM+MTLCM) > 0:
    #st.markdown("M MACHINE BREAKDOWN %")
    MBPM = round(float((MBMM/(MTLAM*ATA+MTLBM*ATB+MTLCM*ATC))*100),2)
    #st.markdown(str(MBPM)+ "  %")
else:
    MBPM = 0

dfk = pd.DataFrame({
        "Key Performance Indicators(TPM)": ["Mean Time Between Failure(MTBF)","Mean Time To Repair(MTTR)","Total BreakDown Percentage"
        ,"Total BreakDown Frequency","Total BreakDown Minutes","V3 BreakDown Time","V3 BreakDown Percentage","G3 BreakDown Time",
        "G3 BreakDown Percentage","GA BreakDown Time","GA BreakDown Percentage","GA BreakDown Time","GA BreakDown Percentage","Kaizen Done"],

        "TO BE": ["240","15","1.2 %"
        ,"30","-","-","-","-",
        "-","-","-","-","-","54"],

        "AS IS": [str(MTBF)+ " hour",str(MTTR)+" min",str(MBDP)+ " %"
        ,str(MBDF),str(MBDTM)+ " Minutes",str(V3BM)+ " Minutes",str(V3BP)+ "  %",str(G3BM)+ " Minutes",
        str(G3BP)+ "  %",str(GABM)+ " Minutes",str(GABP)+ "  %",str(MBM)+ " Minutes",str(MBP)+ "  %",str(KAIZEN)]


})
#st.subheader(" ")
#st.subheader("Other Details : ")
#st.markdown(dfk.style.hide(axis="index").to_html(), unsafe_allow_html=True)

#st.markdown("NUMBER OF HSE POINTS")
HSE = int(df["HSE"].sum())
HSEM = int(dfM["HSE"].sum())
#st.markdown(HSE)
#st.markdown("NUMBER OF HSE OPEN POINTS")
HSEO = int(df["HSEO"].sum())
HSEOM = int(dfM["HSEO"].sum())
#st.markdown(HSEO)

#st.markdown("NUMBER OF CPI POINTS")
CPI = int(df["CPI"].sum())
CPIM = int(dfM["CPI"].sum())
#st.markdown(CPI)
#st.markdown("NUMBER OF CPI OPEN POINTS")
CPIO = int(df["CPIO"].sum())
CPIOM = int(dfM["CPIO"].sum())
#st.markdown(CPIO)

#st.markdown("NUMBER OF LPA POINTS")
LPA = int(df["LPA"].sum())
LPAM = int(dfM["LPA"].sum())
#st.markdown(LPA)
#st.markdown("NUMBER OF LPA OPEN POINTS")
LPAO = int(df["LPAO"].sum())
LPAOM = int(dfM["LPAO"].sum())
#st.markdown(LPAO)

#st.markdown("NUMBER OF DQR POINTS")
DQR = int(df["DQR"].sum())
DQRM = int(dfM["DQR"].sum())
#st.markdown(DQR)
#st.markdown("NUMBER OF DQR OPEN POINTS")
DQRO = int(df["DQRO"].sum())
DQROM = int(dfM["DQRO"].sum())
#st.markdown(DQRO)

#st.markdown("NUMBER OF RED TAGS")
RED = int(df["REDTAG"].sum())
REDM = int(dfM["REDTAG"].sum())
#st.markdown(RED)
#st.markdown("NUMBER OF OPEN RED TAGS")
REDO = int(df["REDTAGO"].sum())
REDOM = int(dfM["REDTAGO"].sum())
#st.markdown(REDO)

#st.markdown("NUMBER OF F006C")
F006C = int(df["F006C"].sum())
F006CM = int(dfM["F006C"].sum())
#st.markdown(F006C)

#st.markdown("NUMBER OF F098")
F098 = int(df["F098"].sum())
F098M = int(dfM["F098"].sum())
#st.markdown(F098)

#st.markdown("NUMBER OF F099")
F099 = int(df["F099"].sum())
F099M = int(dfM["F099"].sum())
#st.markdown(F099)

#st.markdown("NUMBER OF DENT ON PARTS")
DENT = int(df["DENT"].sum())
DENTM = int(dfM["DENT"].sum())
#st.markdown(DENT)

#st.markdown("NUMBER OF DROP PARTS")
DROP = int(df["DROP"].sum())
DROPM = int(dfM["DROP"].sum())
#st.markdown(DROP)

#st.markdown("SPARE")

SPARED = round(float(df["SPARE"].sum()),2)

if SPARED == 0:
    SPARE = 0
else:
    SPARE = round(float(df["SPARE"].mean()),2)

SPAREMD = round(float(dfM["SPARE"].sum()),2)

if SPAREMD == 0:
    SPAREM = 0
else:
    SPAREM = round(float(dfM["SPARE"].mean()),2)

#st.markdown(SPARE)

st.header(":blue[**TPM** **STATUS**]")
st.subheader(FILTER)
col10, col11, col12, col13, col14 = st.columns(5)
with col10:
    st.subheader(":red[**MTBF**]")
col10.metric(label=":orange[**Mean** **Time** **Between** **Failure**]", value=str(MTBF)+ " Hrs", delta=round((MTBF-240),2))
with col11:
    st.subheader(":red[**MTTR**]")
col11.metric(label=":orange[**Mean** **Time** **To** **Repair**]", value=str(MTTR)+ " Min", delta=round((15-MTTR),2))
with col12:
    st.subheader(":red[**BREAKDOWN**]")
col12.metric(label=":orange[**Percentage**]", value=str(MBDP)+ " %", delta=round((1.2-MBDP),2))
with col13:
    st.subheader(":red[**BREAKDOWN**]")
col13.metric(label=":orange[**Frequency**]", value=str(MBDF), delta=(30-MBDF))
with col14:
    st.subheader(":red[**KAIZEN**]")
col14.metric(label=":orange[**Numbers**]", value=str(KAIZEN), delta=(KAIZEN-54))

if MONT > 0:
    st.subheader(":rainbow[**Month** **Till** **Date**]")
    col10, col11, col12, col13, col14 = st.columns(5)
    with col10:
        st.subheader(":red[**MTBF**]")
    col10.metric(label=":orange[**Mean** **Time** **Between** **Failure**]", value=str(MTBFM)+ " Hrs", delta=round((MTBFM-240),2))
    with col11:
        st.subheader(":red[**MTTR**]")
    col11.metric(label=":orange[**Mean** **Time** **To** **Repair**]", value=str(MTTRM)+ " Min", delta=round((15-MTTRM),2))
    with col12:
        st.subheader(":red[**BREAKDOWN**]")
    col12.metric(label=":orange[**Percentage**]", value=str(MBDPM)+ " %", delta=round((1.2-MBDPM),2))
    with col13:
        st.subheader(":red[**BREAKDOWN**]")
    col13.metric(label=":orange[**Frequency**]", value=str(MBDFM), delta=(30-MBDFM))
    with col14:
        st.subheader(":red[**KAIZEN**]")
    col14.metric(label=":orange[**Numbers**]", value=str(KAIZENM), delta=(KAIZENM-54))




st.header(":blue[**KEY** **PERFORMANCE** **INDICATORS(KPI)**]")
st.subheader(FILTER)
col15, col16, col17, col18, col19 = st.columns(5)
with col15:
    st.subheader(":red[**V3**]")
col15.metric(label=":orange[**DownTime**]", value=str(V3BM)+" Min")
with col16:
    st.subheader(":red[**G3**]")
col16.metric(label="", value=str(G3BM)+" Min")
with col17:
    st.subheader(":red[**GA**]")
col17.metric(label="", value=str(GABM)+" Min")
with col18:
    st.subheader(":red[**Manual**]")
col18.metric(label="", value=str(MBM)+" Min")
with col19:
    st.subheader(":red[**TOTAL**]")
col19.metric(label="", value=str(MBDTM)+" Min")

col15.metric(label=":orange[**Percentage**]", value=str(V3BP)+" %", delta=round((1.2-V3BP),2))
col16.metric(label="", value=str(G3BP)+" %", delta=round((1.2-G3BP),2))
col17.metric(label="", value=str(GABP)+" %", delta=round((1.2-GABP),2))
col18.metric(label="", value=str(MBP)+" %", delta=round((1.2-MBP),2))
col19.metric(label="", value=str(MBDP)+ " %", delta=round((1.2-MBDP),2))

if MONT > 0:
    st.subheader(":rainbow[**Month** **Till** **Date** ]")
    col15, col16, col17, col18, col19 = st.columns(5)
    with col15:
        st.subheader(":red[**V3**]")
    col15.metric(label=":orange[**DownTime**]", value=str(V3BMM)+" Min")
    with col16:
        st.subheader(":red[**G3**]")
    col16.metric(label="", value=str(G3BMM)+" Min")
    with col17:
        st.subheader(":red[**GA**]")
    col17.metric(label="", value=str(GABMM)+" Min")
    with col18:
        st.subheader(":red[**Manual**]")
    col18.metric(label="", value=str(MBMM)+" Min")
    with col19:
        st.subheader(":red[**TOTAL**]")
    col19.metric(label="", value=str(MBDTMM)+" Min")

    col15.metric(label=":orange[**Percentage**]", value=str(V3BPM)+" %", delta=round((1.2-V3BPM),2))
    col16.metric(label="", value=str(G3BPM)+" %", delta=round((1.2-G3BPM),2))
    col17.metric(label="", value=str(GABPM)+" %", delta=round((1.2-GABPM),2))
    col18.metric(label="", value=str(MBPM)+" %", delta=round((1.2-MBPM),2))
    col19.metric(label="", value=str(MBDPM)+ " %", delta=round((1.2-MBDPM),2))

st.header(":blue[**INCIDENT** **DETAILS**]")
st.subheader(FILTER)
col20, col21, col22, col23, col24 = st.columns(5)
with col20:
    st.subheader(":red[**LEAKAGE**]")
col20.metric(label=":orange[**F006C**]", value=str(F006C))
with col21:
    st.subheader(":red[**SMOKE**]")
col21.metric(label=":orange[**F098**]", value=str(F098))
with col22:
    st.subheader(":red[**FIRE**]")
col22.metric(label=":orange[**F099**]", value=str(F099))
with col23:
    st.subheader(":red[**DROP** **PARTS**]")
col23.metric(label=":orange[**Numbers**]", value=str(DROP))
with col24:
    st.subheader(":red[**DENT**]")
col24.metric(label=":orange[**Numbers**]", value=str(DENT))

if MONT > 0:
    st.subheader(":rainbow[**Month** **Till** **Date** ]")
    col20, col21, col22, col23, col24 = st.columns(5)
    with col20:
        st.subheader(":red[**LEAKAGE**]")
    col20.metric(label=":orange[**F006C**]", value=str(F006CM))
    with col21:
        st.subheader(":red[**SMOKE**]")
    col21.metric(label=":orange[**F098**]", value=str(F098M))
    with col22:
        st.subheader(":red[**FIRE**]")
    col22.metric(label=":orange[**F099**]", value=str(F099M))
    with col23:
        st.subheader(":red[**DROP** **PARTS**]")
    col23.metric(label=":orange[**Numbers**]", value=str(DROPM))
    with col24:
        st.subheader(":red[**DENT**]")
    col24.metric(label=":orange[**Numbers**]", value=str(DENTM))

col25, col26 = st.columns(2)

with col25:
    st.header(":blue[**SPARE** **COST**]")
    st.subheader(FILTER)
    st.metric(label=":red[**INR /** **PART**]", value=str(SPARE), delta=round((0.11 - SPARE), 2))

if MONT > 0:
    with col26:
        st.subheader("")
        st.subheader("")
        st.subheader("")
        st.subheader(":rainbow[**Month** **Till** **Date** ]")
        st.metric(label=":red[**INR /** **PART**]", value=str(SPAREM), delta=round((0.11 - SPAREM), 2))

col30, col31 = st.columns([1,2])

with col30:
    dfi = pd.DataFrame({
        "Audit Observations": ["HSE","CPI","LPA/RSD","DQR","RED-TAG"],

        "Total": [str(HSE),str(CPI),str(LPA),str(DQR),str(REDTAG)],

        "Open": [str(HSEO),str(CPIO),str(LPAO),str(DQRO),str(REDO)],

        "Closed": [str(HSE-HSEO),str(CPI-CPIO),str(LPA-LPAO),str(DQR-DQRO),str(RED-REDO)]


    })
    st.subheader("")
    st.header(":blue[AUDIT DETAILS]")
    st.subheader(FILTER)
    st.markdown(dfi.style.hide(axis="index").to_html(), unsafe_allow_html=True)
if MONT > 0:
    with col31:
        dfi = pd.DataFrame({
            "Audit Observations": ["HSE","CPI","LPA/RSD","DQR","RED-TAG"],

            "Total": [str(HSEM),str(CPIM),str(LPAM),str(DQRM),str(REDTAGM)],

            "Open": [str(HSEOM),str(CPIOM),str(LPAOM),str(DQROM),str(REDOM)],

            "Closed": [str(HSEM-HSEOM),str(CPIM-CPIOM),str(LPAM-LPAOM),str(DQRM-DQROM),str(REDM-REDOM)]


        })
        st.subheader("")
        st.header(":blue[AUDIT DETAILS]")
        st.subheader(":rainbow[**Month** **Till** **Date** ]")
        st.markdown(dfi.style.hide(axis="index").to_html(), unsafe_allow_html=True)

st.subheader("")
with st.expander(":red[**CUSTOMER** **AUDIT** **OBSERVATIONS-**]" +" " + FILTER):
    st.header(" ")
    df_details = df[
        ["Period", "Customer", "Observations"]]
    st.dataframe((df_details.set_index(df.columns[0]).sort_values(by=["Period"], ascending=True)), width=2220,
                 height=400)
if MONT > 0:
    with st.expander(":red[**CUSTOMER** **AUDIT** **OBSERVATIONS-**]" +" " + FILTERM):
        st.header(" ")
        df_details = dfM[
            ["Period", "Customer", "Observations"]]
        st.dataframe((df_details.set_index(df.columns[0]).sort_values(by=["Period"], ascending=True)), width=2220,
                     height=400)

st.header(":blue[INFORMATION]")
with st.expander(":rainbow[**Click** **To** **Expand-**]" +" " + FILTER):
    st.header(" ")
    df_details=df[["Period", "Preventive Maintenance","PM Status", "Changeover","CH Status", "ESD Plan","ESD Status", "LUX Level Plan","LUX Status"]]
    st.dataframe((df_details.set_index(df.columns[0]).sort_values(by=["Period"], ascending=True)), width=2220,
                 height=400)
    #st.markdown(df_details.style.hide(axis="index").to_html(), unsafe_allow_html=True)

if MONT > 0:
    with st.expander(":rainbow[**Click** **To** **Expand-**]" +" " + FILTERM):
        st.header(" ")
        df_detailsm=dfM[["Period", "Preventive Maintenance","PM Status", "Changeover","CH Status", "ESD Plan","ESD Status", "LUX Level Plan","LUX Status"]]
        st.dataframe((df_detailsm.set_index(df.columns[0]).sort_values(by=["Period"], ascending=True)), width=2220,
                     height=400)
        #st.markdown(df_details.style.hide(axis="index").to_html(), unsafe_allow_html=True)