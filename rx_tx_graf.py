import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime
import matplotlib.dates as mdates
import streamlit as st

st.title("Analýza přenosu dat")

# --- Výběr souboru ---
uploaded_file = st.file_uploader("Vyber CSV soubor", type=["csv"])

if uploaded_file is not None:
    # Načtení dat
    st.cache_data.clear() # <<< VYMAZÁNÍ CACHE
    df = pd.read_csv(uploaded_file)
    df['Time'] = pd.to_datetime(df['Time'], errors='coerce')


    # --- Výpočet součtů ---
    df['ISP_Speed_MB_per_hr'] = (df['Delta_ISP_IN_MB'] / df['Delta_Time_hr']).round(2)
    lan_sum = df["Delta_LAN_OUT_MB"].sum()
    isp_sum = df["Delta_ISP_IN_MB"].sum()
    total_sum = lan_sum + isp_sum

    # --- Vykreslení grafu ---
    plt.style.use('seaborn-v0_8')
    fig, ax1 = plt.subplots(figsize=(12, 6))

    x = df['Time']
    bar_width = 0.03
    offset = pd.Timedelta(minutes=5)

    ax1.bar(x - offset, df['Delta_LAN_OUT_MB'], width=bar_width, label='LAN OUT (MB)', color='steelblue', alpha=0.5)
    ax1.bar(x + offset, df['Delta_ISP_IN_MB'], width=bar_width, label='ISP IN (MB)', color='orange', alpha=0.5)

    ax1.set_ylabel('Přenos dat (MB)', fontsize=12)
    ax1.legend(loc='upper left')

    ax2 = ax1.twinx()
    ax2.plot(x, df['ISP_Speed_MB_per_hr'], color='green', marker='o', linewidth=2, label='Rychlost ISP (MB/h)')
    ax2.set_ylabel('Rychlost ISP (MB/h)', fontsize=12)
    ax2.legend(loc='upper right')

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

    ax1.set_title('Přenos dat a rychlost ISP v čase', fontsize=16)
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.'))
    ax1.set_xlabel('Čas', fontsize=12)
    ax1.tick_params(axis='x', rotation=45, labelsize=10)

    summary = f"OUT = {lan_sum:.2f} MB\nIN = {isp_sum:.2f} MB\nCelkem = {total_sum:.2f} MB"
    ax1.text(0.99, 0.92, summary, transform=ax1.transAxes,
             fontsize=12, ha='right', va='top',
             bbox=dict(facecolor='white', alpha=0.6, edgecolor='gray'))

    ax1.set_ylim(0, 2000)
    ax2.set_ylim(0, 200)
    ax1.grid(True, color='dimgray', linestyle='--', linewidth=0.7)
    ax2.grid(False)

    st.pyplot(fig)
    
    st.subheader("Posledních 10 záznamů")
    df_sorted = df.sort_values(by="Time", ascending=False)
    last_10 = df_sorted.head(10)
    st.dataframe(last_10)

else:
    st.info("Vyber CSV soubor pro zobrazení grafu.")



