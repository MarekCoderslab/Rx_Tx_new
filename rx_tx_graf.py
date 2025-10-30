import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime
import matplotlib.dates as mdates
import streamlit as st

# --- Načtení dat ---
df = pd.read_csv('traffic_log_dif.csv')
df['Time'] = pd.to_datetime(df['Time'], errors='coerce')

# --- Filtrování od 21. října ---
df = df[df['Time'] >= '2025-10-21']

# --- Výpočet součtů bez filtrace ---
df['ISP_Speed_MB_per_hr'] = (df['Delta_ISP_IN_MB'] / df['Delta_Time_hr']).round(2)
lan_sum = df["Delta_LAN_OUT_MB"].sum()
isp_sum = df["Delta_ISP_IN_MB"].sum()
total_sum = lan_sum + isp_sum

# --- Vykreslení grafu ---
plt.style.use('seaborn-v0_8')
fig, ax1 = plt.subplots(figsize=(12, 6))

x = df['Time']
bar_width = 0.2
offset = pd.Timedelta(minutes=15)

# Sloupcový graf na hlavní ose
ax1.bar(x - offset, df['Delta_LAN_OUT_MB'], width=bar_width, label='LAN OUT (MB)', color='steelblue', alpha=0.5)
ax1.bar(x + offset, df['Delta_ISP_IN_MB'], width=bar_width, label='ISP IN (MB)', color='orange', alpha=0.5)

ax1.set_ylabel('Přenos dat (MB)', fontsize=12)
ax1.legend(loc='upper left')

# Vedlejší osa pro rychlost
ax2 = ax1.twinx()
ax2.plot(x, df['ISP_Speed_MB_per_hr'], color='green', marker='o', linewidth=2, label='Rychlost ISP (MB/h)')
ax2.set_ylabel('Rychlost ISP (MB/h)', fontsize=12)
ax2.legend(loc='upper right')

# Doplnění hodnot nad markery
for i in range(len(df)):
    ax2.annotate(
        f"{df['ISP_Speed_MB_per_hr'].iloc[i]:.1f}",
        (df['Time'].iloc[i], df['ISP_Speed_MB_per_hr'].iloc[i]),
        textcoords="offset points",
        xytext=(0, 8),
        ha='center',
        fontsize=9,
        color='green'
    )

# Popisky a souhrn
ax1.set_title('Přenos dat a rychlost ISP v čase', fontsize=16)
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.'))
ax1.set_xlabel('Čas', fontsize=12)
ax1.tick_params(axis='x', rotation=45, labelsize=10)

# Shrnutí v rohu grafu
summary = f"OUT = {lan_sum:.2f} MB\nIN = {isp_sum:.2f} MB\nCelkem = {total_sum:.2f} MB"
ax1.text(0.99, 0.92, summary, transform=ax1.transAxes,
         fontsize=12, ha='right', va='top',
         bbox=dict(facecolor='white', alpha=0.6, edgecolor='gray'))

# Osy a mřížky
ax1.set_ylim(0, 1000)
ax2.set_ylim(0, 100)
ax1.grid(True, color='dimgray', linestyle='--', linewidth=0.7)
ax2.grid(False)

# Výstup do Streamlit
st.pyplot(fig)


