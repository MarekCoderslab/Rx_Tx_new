
#!/bin/bash

# Cílové časy probuzení (5 minut před loggerem)
wake_times=("02:55:00" "06:55:00" "10:55:00" "14:55:00" "18:55:00" "22:55:00")

# Vyčistit předchozí plán
sudo pmset schedule cancelall

# Naplánovat nové probuzení
for time in "${wake_times[@]}"; do
  sudo pmset schedule wakeorpoweron "$(date +%Y-%m-%d)" "$time"
done

echo "✅ pmset schedule aktualizován pro zítřejší běhy."
