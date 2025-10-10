


# %%
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime
import streamlit as st

# Load data
file_path = '/Users/Marek/tableau_project/Rx_Tx_new/traffic_log_dif.csv'
df = pd.read_csv(file_path)

# Convert 'Time' column to datetime
df['Time'] = pd.to_datetime(df['Time'])

# Filter rows from 7.10.2025 onwards and with positive values
start_date = datetime(2025, 10, 7)
filtered_df = df[(df['Time'] >= start_date) &
                 (df['Delta_LAN_OUT_MB'] > 0) &
                 (df['Delta_ISP_IN_MB'] > 0)]

# Plotting
plt.style.use('seaborn-v0_8')
fig, ax = plt.subplots(figsize=(12, 6))

x = filtered_df['Time']
lan = filtered_df['Delta_LAN_OUT_MB']
isp = filtered_df['Delta_ISP_IN_MB']

lan_sum = filtered_df["Delta_LAN_OUT_MB"].sum()
isp_sum = filtered_df["Delta_ISP_IN_MB"].sum()
total_sum = lan_sum + isp_sum

bar_width = 0.4
ax.bar(x - pd.Timedelta(hours=6), lan, width=bar_width, label='LAN OUT (MB)', color='steelblue', alpha=0.8)
ax.bar(x + pd.Timedelta(hours=6), isp, width=bar_width, label='ISP IN (MB)', color='orange', alpha=0.8)

# Fill under bars (approximate visual effect)
ax.fill_between(x, 0, lan, color='steelblue', alpha=0.2)
ax.fill_between(x, 0, isp, color='orange', alpha=0.2)

# Labels and title
ax.set_title('Spotřeba dat od 7.10.2025', fontsize=16)
ax.set_xlabel('Čas', fontsize=12)
ax.set_ylabel('Přenos dat (MB)', fontsize=12)
ax.legend()
plt.xticks(rotation=45)

# Add total summary text
summary_text = f"LAN = {lan_sum:.2f} MB\nISP = {isp_sum:.2f} MB\nCelkem = {total_sum:.2f} MB"
plt.text(0.99, 0.95, summary_text, transform=ax.transAxes,
         fontsize=12, verticalalignment='top', horizontalalignment='right',
         bbox=dict(facecolor='white', alpha=0.6, edgecolor='gray'))

# Save plot
output_path = '/Users/Marek/tableau_project/Rx_Tx_new/spotreba_dat_sloupcovy_graf.png'
os.makedirs(os.path.dirname(output_path), exist_ok=True)
plt.tight_layout()
plt.savefig(output_path)
plt.close()

st.pyplot(fig)


# %%
filtered_df[["Time", "Delta_LAN_OUT_MB", "Delta_ISP_IN_MB", "Delta_Time_hr"]]


