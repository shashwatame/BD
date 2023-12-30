import streamlit as st
import plotly.express as px
import plotly.figure_factory as ff
import pandas as pd
import warnings
import os
import time
warnings.filterwarnings('ignore')
from pathlib import Path

st.set_page_config(page_title="Maintenance Dashboard-Pack" ,page_icon=":bar_chart:" ,layout="wide")

st.title(":bar_chart: :red[Himanshu Varshney]")

fl = st.file_uploader(":file_folder: Upload a file", type=(["xlsx"]))
if fl is not None:
    filename = fl.name
    st.write(filename)
    df = pd.read_excel(filename)#,sheet_name=None)
else:
   #st.image('group.jpg', caption='Advance Maintenance Engineering')
   exit()

col1, col2 = st.columns((2))

df["Date"] = pd.to_datetime(df["Date"])

startDate = pd.to_datetime(df["Date"]).min()
endDate = pd.to_datetime(df["Date"]).max()

#with col1:
#    date1 = pd.to_datetime(st.date_input("Start Date", startDate))

#with col2:
#    date2 = pd.to_datetime(st.date_input("End Date", endDate))

#df = df[(df["Date"] >= date1) & (df["Date"] <= date2)].copy()

st.title(":bar_chart: :red[Advance Maintenance Dashboard]")

st.sidebar.header("Choose your filter: ")
category = st.sidebar.multiselect("Pick Category", df["Category"].unique())
if not category:
    df2 = df.copy()
else:
    df2 = df[df["Category"].isin(category)]

type = st.sidebar.multiselect("Pick Line Type", df2["Type"].unique())
if not type:
    df3 = df2.copy()
else:
    df3 = df2[df2["Type"].isin(type)]

area = st.sidebar.multiselect("Pick Area", df3["Area"].unique())
if not area:
    df4 = df3.copy()
else:
    df4 = df3[df3["Area"].isin(area)]

#Filter the data

if not category and not type and not area:
    filtered_df = df
elif not type and not area:
    filtered_df = df[df["Category"].isin(category)]
elif not category and not area:
    filtered_df = df[df["Type"].isin(type)]
elif type and area:
    filtered_df = df3[df["Type"].isin(type) & df3["Area"].isin(area)]
elif category and area:
    filtered_df = df3[df["Category"].isin(category) & df3["Area"].isin(area)]
elif category and type:
    filtered_df = df3[df["Category"].isin(category) & df3["Type"].isin(type)]
elif area:
    filtered_df = df3[df["Area"].isin(area)]
else:
    filtered_df =  df3[df3["Category"].isin(category) & df3["Type"].isin(type) & df3["Area"].isin(area)]

category_df = filtered_df.groupby(by = ["Category"], as_index = False)["Time"].sum()

# Tabs
with st.expander(":red[**Issue** **Graphs**]"):
    tab1, tab2, tab3= st.tabs(["**Line** **Wise**", "**Type** **Wise**", "**Category** **Wise**"])

with tab1:
    col1, col2 = st.columns((2))
    with col1:
        st.subheader(":red[Line Wise Graph ]")
        area_df = filtered_df.groupby(by = ["Area"], as_index = False)["Time"].sum()
        area_df1 = df[(df['Category'] == 'MBD')]
        figsm = px.bar(area_df1, x = "Area", y = "Time", color='Area', text_auto=True)
        area_df2 = df[(df['Category'] == 'NBD')]
        figsn = px.bar(area_df2, x="Area", y="Time", color='Area', text_auto=True)
        area_df3 = df[(df['Category'] == 'RSD')]
        figsr = px.bar(area_df3, x="Area", y="Time", color='Area', text_auto=True)
        area_df4 = df[(df['Category'] == 'POKA-YOKE')]
        figsp = px.bar(area_df4, x="Area", y="Time", color='Area', text_auto=True)
       # figs.update_yaxes(tickfont=dict(size=20))
       # figs.update_xaxes(tickfont=dict(size=20))
        figsm.update_layout(height=400)
        figsm.update_layout(width=1000)
        #st.plotly_chart(figsm,use_container_width=False)

        figs = px.bar(area_df, x="Area", y="Time", color='Area', text_auto=True)
        # figs.update_yaxes(tickfont=dict(size=20))
        # figs.update_xaxes(tickfont=dict(size=20))
        figs.update_layout(height=400)
        figs.update_layout(width=1000)
        st.plotly_chart(figs, use_container_width=False)

with tab2:
    cl3, cl4 = st.columns(2)
    with cl3:
        st.subheader(":red[Type Wise Graph ]")
        type_df = filtered_df.groupby(by = ["Type"], as_index = False)["Time"].sum()
        fig2 = px.bar(type_df, x = "Type", y = "Time", text_auto=True)
        st.plotly_chart(fig2,use_container_width=True)

with tab3:
    with cl4:
        st.subheader("")
        st.subheader("")
        fig2 = px.pie(type_df, values = "Time", names = "Type", hole = 0.4)
        fig2.update_traces(text=type_df["Type"], textposition = "outside")
        st.plotly_chart(fig2,use_container_width=True, height = 200)

    col5, col6 = st.columns((2))

    with col5:
        st.subheader(":red[Category Wise Graph ]")
        fig1 = px.bar(category_df, x = "Category", y = "Time", text_auto=True)
        st.plotly_chart(fig1,use_container_width=True, height = 200)
        #fig1 = px.pie(category_df, values = "Time", names = "Category", hole = 0.2)
        #fig1.update_traces(text=category_df["Category"], textposition = "outside")
        #st.plotly_chart(fig1,use_container_width=True, height = 200)

    with col6:
        st.subheader("")
        st.subheader("")
        #fig2 = px.pie(filtered_df, values = "Time", names = "Type", hole = 0.2)
        #fig2.update_traces(text=filtered_df["Type"], textposition = "outside")
        #st.plotly_chart(fig2,use_container_width=True)
        fig1 = px.pie(category_df, values = "Time", names = "Category", hole = 0.4)
        fig1.update_traces(text=category_df["Category"], textposition = "outside")
        st.plotly_chart(fig1,use_container_width=True, height = 200)

col13, col14 = st.columns([10,1])
col13.header(":red[**BreakDown** **Details**]"+	":running:")

df_MBD = df[(df['Category']=='MBD')]
MBD = df_MBD.groupby(by = ["Type"], as_index = False)["Time"].sum()
MBDT = int(df_MBD["Time"].sum())


if MBDT > 0:
    MBDF = df['Category'].value_counts()["MBD"]
else:
    MBDF = 0


#Available Time

AT = int(420)

#Shift A
LIA = int(df["Lines in A"].sum())
#st.markdown("Total Running Lines in A Shift is : "+ str(LIA))
df_MBDA = df[(df['Category']=='MBD') & (df['Shift']=='A')]
MBDTA = int(df_MBDA["Time"].sum())

if LIA > 0:
    MBDAP = round(float(MBDTA/(LIA*AT)*100),2)
else:
    MBDAP = 0

#Shift B
LIB = int(df["Lines in B"].sum())
#st.markdown("Total Running Lines in B Shift is : "+ str(LIB))
df_MBDB = df[(df['Category']=='MBD') & (df['Shift']=='B')]
MBDTB = int(df_MBDB["Time"].sum())

if LIB > 0:
    MBDBP = round(float(MBDTB/(LIB*AT)*100),2)
else:
    MBDBP = 0

#Shift C
LIC = int(df["Lines in C"].sum())
#st.markdown("Total Running Lines in C Shift is : "+ str(LIC))
df_MBDC = df[(df['Category']=='MBD') & (df['Shift']=='C')]
MBDTC = int(df_MBDC["Time"].sum())

if LIC > 0:
    MBDCP = round(float(MBDTC/(LIC*AT)*100),2)
else:
    MBDCP = 0

#Type V3 A SHIFT
LIFV3A = df[(df['Type Of Line']=='V3') & (df['TShift']=='A')]
LIV3A = int(LIFV3A["Total"].sum())
df_MBDV3A = df[(df['Category']=='MBD') & (df['Type']=='V3') & (df['Shift']=='A')]
MBDTV3A = int(df_MBDV3A["Time"].sum())

if LIV3A > 0:
    MBDV3AP = round(float(MBDTV3A/(LIV3A*AT)*100),2)
else:
    MBDV3AP = 0
#st.markdown(LIV3A)
#st.markdown(MBDTV3A)
#st.markdown(MBDV3AP)

#Type V3 B SHIFT
LIFV3B = df[(df['Type Of Line']=='V3') & (df['TShift']=='B')]
LIV3B = int(LIFV3B["Total"].sum())
df_MBDV3B = df[(df['Category']=='MBD') & (df['Type']=='V3') & (df['Shift']=='B')]
MBDTV3B = int(df_MBDV3B["Time"].sum())

if LIV3B > 0:
    MBDV3BP = round(float(MBDTV3B/(LIV3B*AT)*100),2)
else:
    MBDV3BP = 0
#st.markdown(LIV3B)
#st.markdown(MBDTV3B)
#st.markdown(MBDV3BP)

#Type V3 C SHIFT
LIFV3C = df[(df['Type Of Line']=='V3') & (df['TShift']=='C')]
LIV3C = int(LIFV3C["Total"].sum())
df_MBDV3C = df[(df['Category']=='MBD') & (df['Type']=='V3') & (df['Shift']=='C')]
MBDTV3C = int(df_MBDV3C["Time"].sum())

if LIV3C > 0:
    MBDV3CP = round(float(MBDTV3C/(LIV3C*AT)*100),2)
else:
    MBDV3CP = 0


#Type V3 TOTAL

if (LIV3A+LIV3B+LIV3C) > 0:
    MBDV3TP = round((((MBDTV3A+MBDTV3B+MBDTV3C)/((LIV3A+LIV3B+LIV3C)*AT))*100),2)
else:
    MBDV3TP = 0
#st.markdown(MBDV3TP)

#Type G3 A SHIFT
LIFG3A = df[(df['Type Of Line']=='G3') & (df['TShift']=='A')]
LIG3A = int(LIFG3A["Total"].sum())
df_MBDG3A = df[(df['Category']=='MBD') & (df['Type']=='G3') & (df['Shift']=='A')]
MBDTG3A = int(df_MBDG3A["Time"].sum())

if LIG3A > 0:
    MBDG3AP = round(float(MBDTG3A/(LIG3A*AT)*100),2)
else:
    MBDG3AP = 0


#Type G3 B SHIFT
LIFG3B = df[(df['Type Of Line']=='G3') & (df['TShift']=='B')]
LIG3B = int(LIFG3B["Total"].sum())
df_MBDG3B = df[(df['Category']=='MBD') & (df['Type']=='G3') & (df['Shift']=='B')]
MBDTG3B = int(df_MBDG3B["Time"].sum())

if LIG3B > 0:
    MBDG3BP = round(float(MBDTG3B/(LIG3B*AT)*100),2)
else:
    MBDG3BP = 0


#Type G3 C SHIFT
LIFG3C = df[(df['Type Of Line']=='G3') & (df['TShift']=='C')]
LIG3C = int(LIFG3C["Total"].sum())
df_MBDG3C = df[(df['Category']=='MBD') & (df['Type']=='G3') & (df['Shift']=='C')]
MBDTG3C = int(df_MBDG3C["Time"].sum())

if LIG3C > 0:
    MBDG3CP = round(float(MBDTG3C/(LIG3C*AT)*100),2)
else:
    MBDG3CP = 0
#st.markdown(LIG3C)
#st.markdown(MBDTG3C)
#st.markdown(MBDG3CP)

#Type G3 TOTAL

if (LIG3A+LIG3B+LIG3C) > 0:
    MBDG3TP = round((((MBDTG3A+MBDTG3B+MBDTG3C)/((LIG3A+LIG3B+LIG3C)*AT))*100),2)
else:
    MBDG3TP = 0


#Type GA A SHIFT
LIFGAA = df[(df['Type Of Line']=='GA') & (df['TShift']=='A')]
LIGAA = int(LIFGAA["Total"].sum())
df_MBDGAA = df[(df['Category']=='MBD') & (df['Type']=='GA') & (df['Shift']=='A')]
MBDTGAA = int(df_MBDGAA["Time"].sum())

if LIGAA > 0:
    MBDGAAP = round(float(MBDTGAA/(LIGAA*AT)*100),2)
else:
    MBDGAAP = 0


#Type GA B SHIFT
LIFGAB = df[(df['Type Of Line']=='GA') & (df['TShift']=='B')]
LIGAB = int(LIFGAB["Total"].sum())
df_MBDGAB = df[(df['Category']=='MBD') & (df['Type']=='GA') & (df['Shift']=='B')]
MBDTGAB = int(df_MBDGAB["Time"].sum())

if LIGAB > 0:
    MBDGABP = round(float(MBDTGAB/(LIGAB*AT)*100),2)
else:
    MBDGABP = 0


#Type GA C SHIFT
LIFGAC = df[(df['Type Of Line']=='GA') & (df['TShift']=='C')]
LIGAC = int(LIFGAC["Total"].sum())
df_MBDGAC = df[(df['Category']=='MBD') & (df['Type']=='GA') & (df['Shift']=='C')]
MBDTGAC = int(df_MBDGAC["Time"].sum())

if LIGAC > 0:
    MBDGACP = round(float(MBDTGAC/(LIGAC*AT)*100),2)
else:
    MBDGACP = 0


#Type GA TOTAL

if (LIGAA+LIGAB+LIGAC) > 0:
    MBDGATP = round((((MBDTGAA+MBDTGAB+MBDTGAC)/((LIGAA+LIGAB+LIGAC)*AT))*100),2)
else:
    MBDGATP = 0


#Type M A SHIFT
LIFMA = df[(df['Type Of Line']=='M') & (df['TShift']=='A')]
LIMA = int(LIFMA["Total"].sum())
df_MBDMA = df[(df['Category']=='MBD') & (df['Type']=='M') & (df['Shift']=='A')]
MBDTMA = int(df_MBDMA["Time"].sum())

if LIMA > 0:
    MBDMAP = round(float(MBDTMA/(LIMA*AT)*100),2)
else:
    MBDMAP = 0


#Type M B SHIFT
LIFMB = df[(df['Type Of Line']=='M') & (df['TShift']=='B')]
LIMB = int(LIFMB["Total"].sum())
df_MBDMB = df[(df['Category']=='MBD') & (df['Type']=='M') & (df['Shift']=='B')]
MBDTMB = int(df_MBDMB["Time"].sum())

if LIMB > 0:
    MBDMBP = round(float(MBDTMB/(LIMB*AT)*100),2)
else:
    MBDMBP = 0


#Type M C SHIFT
LIFMC = df[(df['Type Of Line']=='M') & (df['TShift']=='C')]
LIMC = int(LIFMC["Total"].sum())
df_MBDMC = df[(df['Category']=='MBD') & (df['Type']=='M') & (df['Shift']=='C')]
MBDTMC = int(df_MBDMC["Time"].sum())

if LIMC > 0:
    MBDMCP = round(float(MBDTMC/(LIMC*AT)*100),2)
else:
    MBDMCP = 0


#Type M TOTAL

if (LIMA+LIMB+LIMC) > 0:
    MBDMTP = round((((MBDTMA+MBDTMB+MBDTMC)/((LIMA+LIMB+LIMC)*AT))*100),2)
else :
    MBDMTP = 0


#st.markdown(":green[*Line* *Running* *Shift* *Wise* *:* "+" *A* - "+str(LIA)+",  *B* - "+str(LIB)+",  *C* - "+str(LIC)+ "]")
#st.markdown(":blue[*Downtime* *Shift* *Wise* *:* "+" *A* - "+str(MBDTA)+" min"+",  *B* - "+str(MBDTB)+" min"+",  *C* - "+str(MBDTC)+" min]")
#st.markdown(":red[*Downtime* *Percent* *Shift* *Wise* *:* "+" *A* - "+str(MBDAP)+"%  "+", *B* - "+str(MBDBP)+"%  "+", *C* - "+str(MBDCP)+"% ]")

MBDS=int(LIA+LIB+LIC)
#st.markdown(":green[*Total* *Line* *Running* *(* *A* + *B* + *C* *)* *is* *:* "+ str(MBDS)+"]")
#st.markdown(":blue[*Machine* *Downtime*  *(* *A* + *B* + *C* *)* *is* *:* "+ str(MBDT) + " min]")

if MBDS > 0:
    MBDTP = round(float(MBDT/(MBDS*AT)*100),2)
else:
    MBDTP = 0
#st.markdown(":red[*Downtime* *Percent*  *(* *A* + *B* + *C* *)* *is* *:* "+ str(MBDTP) + " %]")

#DAY TOTAL

TAT = (AT*MBDS)
#st.markdown(LIA)
#st.markdown(LIB)
#st.markdown(LIC)
#st.markdown(":orange[Total Available Time In Minutes : "+ str(TAT)+" min]")

#MTBF & MTTR
if MBDF > 0:
    MTBF1 = int((TAT-MBDT)/MBDF)
    MTBF = round(int(MTBF1/60),0)
    MTTR = round(int(MBDT/MBDF),0)
else:
    MTBF1 = int(TAT-MBDT)
    MTBF = round(int(MTBF1/60),0)
    MTTR = 0

with col13:

    col20, col21, col22, col23, col24 = st.columns([1.2,1.2,1.2,1.2,1.2])
    col20.metric(label=":green[**Total** **V3** **Lines**]", value=str(LIV3A + LIV3B + LIV3C))
    col21.metric(label=":green[**Total** **G3** **Lines**]", value=str(LIG3A + LIG3B + LIG3C))
    col22.metric(label=":green[**Total** **GA** **Lines**]", value=str(LIGAA + LIGAB + LIGAC))
    col23.metric(label=":green[**Total** **M** **Lines**]", value=str(LIMA + LIMB + LIMC))
    col24.metric(label=":green[**Total** **Running** **Lines**]", value=str(MBDS))

    col20, col21, col22, col23, col24 = st.columns([1.2,1.2,1.2,1.2,1.2])
    col20.metric(label=":violet[**Total** **V3** **Downtime**]", value=str(MBDTV3A + MBDTV3B + MBDTV3C) + " Min")
    col21.metric(label=":violet[**Total** **G3** **Downtime**]", value=str(MBDTG3A + MBDTG3B + MBDTG3C) + " Min")
    col22.metric(label=":violet[**Total** **GA** **Downtime**]", value=str(MBDTGAA + MBDTGAB + MBDTGAC) + " Min")
    col23.metric(label=":violet[**Total** **M** **Downtime**]", value=str(MBDTMA + MBDTMB + MBDTMC) + " Min")
    col24.metric(label=":violet[**Total** **Downtime**]", value=str(MBDT) + " Min")

    col30, col31, col32, col33, col34 = st.columns([1.2,1.2,1.2,1.2,1.2])
    DIFFV3 = float(1.2 - MBDV3TP)
    col30.metric(label=":red[**Total** **Percentage** **V3**]", value=str(MBDV3TP) + " %", delta=round(DIFFV3,2))
    DIFFG3 = float(1.2 - MBDG3TP)
    col31.metric(label=":red[**Total** **Percentage** **G3**]", value=str(MBDG3TP) + " %", delta=round(DIFFG3,2))
    DIFFGA = float(1.2 - MBDGATP)
    col32.metric(label=":red[**Total** **Percentage** **GA**]", value=str(MBDGATP) + " %", delta=round(DIFFGA,2))
    DIFFM = float(1.2 - MBDMTP)
    col33.metric(label=":red[**Total** **Percentage** **M**]", value=str(MBDMTP) + " %", delta=round(DIFFM,2))
    DIFFT = float(1.2 - MBDTP)
    col34.metric(label=":red[**BreakDown** **Percentage**]", value=str(MBDTP) + " % ", delta=round(DIFFT,2))

with col14:
    INA = df["INAC"].sum()
    if INA == 1:
        st.image('1.jpg', caption="A Shift", width=100)
    elif INA == 2:
        st.image('2.jpg', caption="A Shift", width=100)
    elif INA == 3:
        st.image('3.jpg', caption="A Shift", width=100)
    elif INA == 4:
        st.image('4.jpg', caption="A Shift", width=100)
    elif INA == 5:
        st.image('5.jpg', caption="A Shift", width=100)
    elif INA == 6:
        st.image('6.jpg', caption="A Shift", width=100)
    elif INA == 7:
        st.image('7.jpg', caption="A Shift", width=100)
    elif INA == 8:
        st.image('8.jpg', caption="A Shift", width=100)
    elif INA == 9:
        st.image('9.jpg', caption="A Shift", width=100)
    elif INA == 10:
        st.image('10.jpg', caption="A Shift", width=100)

    INB = df["INBC"].sum()
    if INB == 1:
        st.image('1.jpg', caption="B Shift", width=100)
    elif INB == 2:
        st.image('2.jpg', caption="B Shift", width=100)
    elif INB == 3:
        st.image('3.jpg', caption="B Shift", width=100)
    elif INB == 4:
        st.image('4.jpg', caption="B Shift", width=100)
    elif INB == 5:
        st.image('5.jpg', caption="B Shift", width=100)
    elif INB == 6:
        st.image('6.jpg', caption="B Shift", width=100)
    elif INB == 7:
        st.image('7.jpg', caption="B Shift", width=100)
    elif INB == 8:
        st.image('8.jpg', caption="B Shift", width=100)
    elif INB == 9:
        st.image('9.jpg', caption="B Shift", width=100)
    elif INB == 10:
        st.image('10.jpg', caption="B Shift", width=100)

    INC = df["INCC"].sum()
    if INC == 1:
        st.image('1.jpg', caption="C Shift", width=100)
    elif INC == 2:
        st.image('2.jpg', caption="C Shift", width=100)
    elif INC == 3:
        st.image('3.jpg', caption="C Shift", width=100)
    elif INC == 4:
        st.image('4.jpg', caption="C Shift", width=100)
    elif INC == 5:
        st.image('5.jpg', caption="C Shift", width=100)
    elif INC == 6:
        st.image('6.jpg', caption="C Shift", width=100)
    elif INC == 7:
        st.image('7.jpg', caption="C Shift", width=100)
    elif INC == 8:
        st.image('8.jpg', caption="C Shift", width=100)
    elif INC == 9:
        st.image('9.jpg', caption="C Shift", width=100)
    elif INC == 10:
        st.image('10.jpg', caption="C Shift", width=100)


with st.expander(":red[Shift-Wise Details]"):
    col20, col21, col22, col23, col24,col25 = st.columns([1.2,1.2,1.2,1.2,1.2,1.2])
    DIFFT = float(1.2 - MBDTP)
    col20.metric(label=":green[**V3-A** **Lines**]", value=str(LIV3A))
    DIFFV3 = float(1.2 - MBDV3TP)
    col21.metric(label=":green[**V3-B** **Lines**]", value=str(LIV3B))
    DIFFG3 = float(1.2 - MBDG3TP)
    col22.metric(label=":green[**V3-C** **Lines**]", value=str(LIV3C))
    DIFFGA = float(1.2 - MBDGATP)
    col23.metric(label=":green[**G3-A** **Lines**]", value=str(LIG3A))
    DIFFM = float(1.2 - MBDMTP)
    col24.metric(label=":green[**G3-B** **Lines**]", value=str(LIG3B))
    DIFFM = float(1.2 - MBDMTP)
    col25.metric(label=":green[**G3-C** **Lines**]", value=str(LIG3C))

    col20, col21, col22, col23, col24,col25 = st.columns([1.2,1.2,1.2,1.2,1.2,1.2])
    DIFFT = float(1.2 - MBDTP)
    col20.metric(label=":violet[**V3-A** **Downtime**]", value=str(MBDTV3A))
    DIFFV3 = float(1.2 - MBDV3TP)
    col21.metric(label=":violet[**V3-B** **Downtime**]", value=str(MBDTV3B))
    DIFFG3 = float(1.2 - MBDG3TP)
    col22.metric(label=":violet[**V3-C** **Downtime**]", value=str(MBDTV3C))
    DIFFGA = float(1.2 - MBDGATP)
    col23.metric(label=":violet[**G3-A** **Downtime**]", value=str(MBDTG3A))
    DIFFM = float(1.2 - MBDMTP)
    col24.metric(label=":violet[**G3-B** **Downtime**]", value=str(MBDTG3B))
    DIFFM = float(1.2 - MBDMTP)
    col25.metric(label=":violet[**G3-C** **Downtime**]", value=str(MBDTG3C))

    col20, col21, col22, col23, col24,col25 = st.columns([1.2,1.2,1.2,1.2,1.2,1.2])
    DIFFT = float(1.2 - MBDTP)
    col20.metric(label=":green[**GA-A** **Lines**]", value=str(LIGAA))
    DIFFV3 = float(1.2 - MBDV3TP)
    col21.metric(label=":green[**GA-B** **Lines**]", value=str(LIGAB))
    DIFFG3 = float(1.2 - MBDG3TP)
    col22.metric(label=":green[**GA-C** **Lines**]", value=str(LIGAC))
    DIFFGA = float(1.2 - MBDGATP)
    col23.metric(label=":green[**M-A** **Lines**]", value=str(LIMA))
    DIFFM = float(1.2 - MBDMTP)
    col24.metric(label=":green[**M-B** **Lines**]", value=str(LIMB))
    DIFFM = float(1.2 - MBDMTP)
    col25.metric(label=":green[**M-C** **Lines**]", value=str(LIMC))

    col20, col21, col22, col23, col24,col25 = st.columns([1.2,1.2,1.2,1.2,1.2,1.2])
    DIFFT = float(1.2 - MBDTP)
    col20.metric(label=":violet[**GA-A** **Downtime**]", value=str(MBDTGAA))
    DIFFV3 = float(1.2 - MBDV3TP)
    col21.metric(label=":violet[**GA-B** **Downtime**]", value=str(MBDTGAB))
    DIFFG3 = float(1.2 - MBDG3TP)
    col22.metric(label=":violet[**GA-C** **Downtime**]", value=str(MBDTGAC))
    DIFFGA = float(1.2 - MBDGATP)
    col23.metric(label=":violet[**M-A** **Downtime**]", value=str(MBDTMA))
    DIFFM = float(1.2 - MBDMTP)
    col24.metric(label=":violet[**M-B** **Downtime**]", value=str(MBDTMB))
    DIFFM = float(1.2 - MBDMTP)
    col25.metric(label=":violet[**M-C** **Downtime**]", value=str(MBDTMC))

    col30, col31, col32, col33, col34, col35 = st.columns([1.2,1.2,1.2,1.2,1.2,1.2])
    DIFFV3A = float(1.2 - MBDV3AP)
    col30.metric(label=":red[**V3-A** **Percentage**]", value=str(MBDV3AP) + " % ", delta=round(DIFFV3A, 2))
    DIFFV3B = float(1.2 - MBDV3BP)
    col31.metric(label=":red[**V3-B** **Percentage**]", value=str(MBDV3BP) + " % ", delta=round(DIFFV3B, 2))
    DIFFV3C = float(1.2 - MBDV3CP)
    col32.metric(label=":red[**V3-C** **Percentage**]", value=str(MBDV3CP) + " % ", delta=round(DIFFV3C, 2))
    DIFFG3A = float(1.2 - MBDG3AP)
    col33.metric(label=":red[**G3-A** **Percentage**]", value=str(MBDG3AP) + " % ", delta=round(DIFFG3A, 2))
    DIFFG3B = float(1.2 - MBDG3BP)
    col34.metric(label=":red[**G3-B** **Percentage**]", value=str(MBDG3BP) + " % ", delta=round(DIFFG3B, 2))
    DIFFG3C = float(1.2 - MBDG3CP)
    col35.metric(label=":red[**G3-C** **Percentage**]", value=str(MBDG3CP) + " % ", delta=round(DIFFG3C, 2))

    col30, col31, col32, col33, col34, col35 = st.columns([1.2,1.2,1.2,1.2,1.2,1.2])
    DIFFGAA = float(1.2 - MBDGAAP)
    col30.metric(label=":red[**GA-A** **Percentage**]", value=str(MBDGAAP) + " % ", delta=round(DIFFGAA, 2))
    DIFFGAB = float(1.2 - MBDGABP)
    col31.metric(label=":red[**GA-B** **Percentage**]", value=str(MBDGABP) + " % ", delta=round(DIFFGAB, 2))
    DIFFGAC = float(1.2 - MBDGACP)
    col32.metric(label=":red[**GA-C** **Percentage**]", value=str(MBDGACP) + " % ", delta=round(DIFFGAC, 2))
    DIFFMA = float(1.2 - MBDMAP)
    col33.metric(label=":red[**M-A** **Percentage**]", value=str(MBDMAP) + " % ", delta=round(DIFFMA, 2))
    DIFFMB = float(1.2 - MBDMBP)
    col34.metric(label=":red[**M-B** **Percentage**]", value=str(MBDMBP) + " % ", delta=round(DIFFMB, 2))
    DIFFMC = float(1.2 - MBDMCP)
    col35.metric(label=":red[**M-C** **Percentage**]", value=str(MBDMCP) + " % ", delta=round(DIFFMC, 2))

with st.expander(":red[**All** **Issues** **Details**]"):
   df_issue=filtered_df[["Shift", "Area", "Date", "Time", "Description", "Action"]]
   st.dataframe((df_issue.set_index(df.columns[0]).sort_values(by=["Shift"], ascending=True)), width=2220, height=400)

col15, col16= st.columns([5, 15])

#NBD Calculation
df_NBD = df[(df['Category']=='NBD')]
NBD = df_MBD.groupby(by = ["Type"], as_index = False)["Time"].sum()
NBDT = int(df_NBD["Time"].sum())


if NBDT > 0:
    NBDF = df['Category'].value_counts()["NBD"]
else:
    NBDF = 0


#RSD Calculation
df_RSD = df[(df['Category']=='RSD')]
RSD = df_RSD.groupby(by = ["Type"], as_index = False)["Time"].sum()
RSDT = int(df_RSD["Time"].sum())


if RSDT > 0:
    RSDF = df['Category'].value_counts()["RSD"]
else:
    RSDF = 0

#PKF Calculation
df_PKF = df[(df['Category']=='POKA-YOKE')]
PKF = df_PKF.groupby(by = ["Type"], as_index = False)["Time"].sum()
PKFT = int(df_PKF["Time"].sum())


if PKFT > 0:
    PKFF = df['Category'].value_counts()["RSD"]
else:
    PKFF = 0

# Tabs
tab11, tab12, tab13, tab14 = st.tabs(["**Machine** **BreakDown**", "**No-BreakDown**", "**RSD Issues**", "**Poka-Yoke** **Issues**"])

with tab11:
    st.header(":red[**Machine** **Breakdown**]" + ":rage:")
    if MBDT == 0:
        st.info("**Zero** **Breakdown**")
        if st.button(":smiley:"):
            st.toast('Hip!')
            time.sleep(.5)
            st.toast('Hip!')
            time.sleep(.5)
            st.toast('Hooray!', icon='🎉')
            st.balloons()
    else:
        st.plotly_chart(figsm, use_container_width=False)
        with st.expander(":red[**MBD-Details**]"):
            df_MBDI = df_MBD[["Shift", "Area", "Time", "Description", "Action"]]
            st.dataframe((df_MBDI.set_index(df.columns[0]).sort_values(by=["Shift"], ascending=True)), width=2220, height=300)


with tab12:
    col17, col18= st.columns([5, 15])

    col17.header(":red[**No-BreakDown**]"+":disappointed_relieved:")
    df_NBD = df[(df['Category']=='NBD')]# & (df['Plan']=='No')]
    NBD = df_NBD.groupby(by = ["Type"], as_index = False)["Time"].sum()
    NBDT = int(df_NBD["Time"].sum())
    st.markdown("*Total* *Unplanned* *Work* *is* *:* "+ str(NBDT) + " min")

    if NBDT == 0:
        st.info("**Zero** **Unplanned** **Work**"+":smiley:")
    else:
        #st.header(":red[**No-BreakDown-Graph**]")
        st.plotly_chart(figsn, use_container_width=False)
        with st.expander(":red[**NBD-Details**]"):
            df_NBDI = df_NBD[["Shift", "Area", "Time", "Description", "Action"]]
            st.dataframe((df_NBDI.set_index(df.columns[0]).sort_values(by=["Shift"], ascending=True)), width=2220, height=300)


with tab13:
    col19, col20 = st.columns([5, 15])

    col19.header(":red[**RSD** **Issues**]"+"	:rotating_light:")
    df_RSD = df[(df['Category']=='RSD')]# & (df['Plan']=='No')]
    RSD = df_RSD.groupby(by = ["Type"], as_index = False)["Time"].sum()
    RSDT = int(df_RSD["Time"].sum())
    st.markdown("*Total* *RSD* *issue* *time* *is* *:* "+ str(RSDT) + " min")

    if RSDT == 0:
        st.info("**Zero** **RSD**" + ":smiley:")
    else:
        st.plotly_chart(figsr, use_container_width=False)
        with st.expander(":red[**RSD-Details**]"):
            df_RSDI = df_RSD[["Shift", "Area", "Time", "Description", "Action"]]
            st.dataframe((df_RSDI.set_index(df.columns[0]).sort_values(by=["Shift"], ascending=True)), width=2220, height=300)

with tab14:
    col21, col22 = st.columns([5,5])

    col21.header(":red[POKA-YOKE Issues]"+":alarm_clock:")
    df_PK = df[(df['Category']=='POKA-YOKE')]# & (df['Plan']=='No')]
    PK = df_PK.groupby(by = ["Type"], as_index = False)["Time"].sum()
    PKT = int(df_PK["Time"].sum())
    st.markdown("*Total* *Poka-Yoke* *issue* *time* *is* *:* "+ str(PKT) + " min")

    if PKT == 0:
        st.info("**Zero** **Failure**" + ":smiley:")
    else:
        st.plotly_chart(figsp, use_container_width=False)
        with st.expander(":red[**POKA-YOKE** **Details**]"):
            df_PKI = df_PK[["Shift", "Area", "Time", "Description", "Action"]]
            st.dataframe((df_PKI.set_index(df.columns[0]).sort_values(by=["Shift"], ascending=True)), width=2220, height=300)




