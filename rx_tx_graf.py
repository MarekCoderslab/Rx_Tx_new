


# %%
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime
import streamlit as st

# --- Načtení dat ---
df = pd.read_csv('traffic_log_dif.csv')
df['Time'] = pd.to_datetime(df['Time'], errors='coerce')
# --- Filtrování od 21. října ---
df = df[df['Time'] >= '2025-10-21']

# --- Výpočet součtů bez filtrace ---
lan_sum = df["Delta_LAN_OUT_MB"].sum()
isp_sum = df["Delta_ISP_IN_MB"].sum()
total_sum = lan_sum + isp_sum

# --- Vykreslení grafu ---
plt.style.use('seaborn-v0_8')
fig, ax = plt.subplots(figsize=(12, 6))

x = df['Time']
bar_width = 0.2

ax.bar(x - pd.Timedelta(hours=6), df['Delta_LAN_OUT_MB'], width=bar_width,
       label='LAN OUT (MB)', color='steelblue', alpha=0.8)
ax.bar(x + pd.Timedelta(hours=6), df['Delta_ISP_IN_MB'], width=bar_width,
       label='ISP IN (MB)', color='orange', alpha=0.8)

# --- Popisky a souhrn ---
ax.set(title='Spotřeba dat (všechny záznamy)', xlabel='Čas', ylabel='Přenos dat (MB)')
ax.set_ylim(0, 1000)
ax.legend()
plt.xticks(rotation=45)

summary = f"LAN = {lan_sum:.2f} MB\nISP = {isp_sum:.2f} MB\nCelkem = {total_sum:.2f} MB"
plt.text(0.99, 0.95, summary, transform=ax.transAxes,
         fontsize=12, ha='right', va='top',
         bbox=dict(facecolor='white', alpha=0.6, edgecolor='gray'))


st.pyplot(fig)



