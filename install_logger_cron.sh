
#!/bin/bash

# Cesta k dockeru
DOCKER_PATH=$(which docker)

# Cesta k projektu
PROJECT_PATH="/Users/Marek/tableau_project/Rx_Tx_new"
LOG_PATH="/Users/Marek/tableau_project/rx_tx_log.txt"

# Cron řádek
CRON_LINE="0 * * * * $DOCKER_PATH run --rm -v $PROJECT_PATH:/app snmp-logger >> $LOG_PATH 2>&1"

# Přidání do crontabu (zachová existující úlohy)
(crontab -l 2>/dev/null; echo "$CRON_LINE") | crontab -

echo "✅ Cron úloha byla přidána:"
echo "$CRON_LINE"
