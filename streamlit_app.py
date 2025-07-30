import streamlit as st
import plotly.graph_objects as go
import pandas as pd


import numpy as np
from scipy.signal import find_peaks

file_name="A-01.csv"

dg=pd.read_csv(file_name,  parse_dates=["Date"])

x=np.array(dg["Level"])
Max_Level=int(max(x))
y=Max_Level-x


peaks, _ = find_peaks(x)

print(f"Indices of peaks: {peaks}")

valley, _ = find_peaks(y)

print(f"Indices of valleys: {valley}")


print(f"Indices of peaks: {len(peaks)}")
print(f"Indices of valley: {len(valley)}")

for i in range (min(len(peaks),len(valley))):

      if(peaks[i]>valley[i]):
        print(i)
        print(peaks[i]-valley[i])
        print(peaks[i-1], peaks[i], peaks[i+1])
        print(valley[i-1], valley[i], valley[i+1])


target=[]
#hazen=min(len(peaks),len(valley))
for i in range (3150):
    if(abs(dg['Level'][peaks[i]]-dg['Level'][valley[i]])<0.5):
        #print(i)
        #print(dg['Level'][peaks[i]])
        #print(dg['Level'][valley[i]])
        target=np.append(target, i)
target = target.astype(int)
print(target)
print(len(target))


peaks=np.delete(peaks, target)
valley=np.delete(valley, target)
print(len(peaks))
print(len(valley))

dg.loc[peaks, 'Top'] = dg['Level']
dg.loc[valley,'Bottom']=dg['Level']
print(len(peaks))
print(len(valley))
print(dg)

dh=dg.iloc[peaks]


dg.loc[peaks, 'Top'] = dg['Level']
dg.loc[valley,'Bottom']=dg['Level']
print(len(peaks))
print(len(valley))
dg['id']=dg.index
print(dg)

fig = go.Figure()

fig.add_trace(
    go.Scatter(x=dg['Date'], y=dg['Level'], mode='lines', name='Level'),
    #secondary_y=False,
)
fig.add_trace(
    go.Scatter(x=dg['Date'], y=dg['Top'], mode='markers', text=dg['id'], name='Top'), 
    #secondary_y=False,
)
fig.add_trace(
    go.Scatter(x=dg['Date'], y=dg['Bottom'], mode='markers', text=dg['id'], name='Bottom')
)
fig.add_trace(
    go.Scatter(x=dg['Date'], y=dg['Pump01'], mode='lines', name="Pump 01"), 
    #secondary_y=True,
)
fig.add_trace(
    go.Scatter(x=dg['Date'], y=dg['Pump02'], mode='lines', name="Pump 02")
)

fig.update_layout(
    height=700,  # New height
    width=1400    # New width
)

st.plotly_chart(fig, config = {'scrollZoom': False})
