#!/bin/bash

# Dnešní datum
today=$(date +%Y-%m-%d)

# Zítřejší datum
tomorrow=$(date -v+1d +%Y-%m-%d)

# Dnešní časy
today_times=("14:58:00" "18:58:00" "22:58:00")

# Zítřejší časy
tomorrow_times=("02:58:00" "06:58:00" "10:58:00" "14:58:00" "18:58:00" "22:58:00")

# Vyčistit předchozí plán
sudo pmset schedule cancelall

# Naplánovat dnešní časy
for time in "${today_times[@]}"; do
  sudo pmset schedule wakeorpoweron "$today" "$time"
done

# Naplánovat zítřejší časy
for time in "${tomorrow_times[@]}"; do
  sudo pmset schedule wakeorpoweron "$tomorrow" "$time"
done

echo "✅ pmset schedule nastaven pro dnešek i zítřek."

