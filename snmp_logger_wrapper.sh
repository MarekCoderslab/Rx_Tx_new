#!/bin/bash

# Zaloguj čas spuštění skriptu
echo "$(date) — snmp_logger_wrapper.sh spuštěn" >> /Users/Marek/tableau_project/rx_tx_log.txt

# Čekej, dokud Docker daemon neběží
until docker info >/dev/null 2>&1; do
  echo "⏳ Čekám na Docker daemon..." >> /Users/Marek/tableau_project/rx_tx_log.txt
  sleep 5
done

# Spusť logger
/usr/local/bin/docker run --rm -v /Users/Marek/tableau_project/Rx_Tx_new:/app snmp-logger >> /Users/Marek/tableau_project/rx_tx_log.txt 2>> /Users/Marek/tableau_project/rx_tx_error.log
