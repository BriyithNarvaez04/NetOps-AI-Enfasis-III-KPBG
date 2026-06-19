HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 http://localhost:80)
if ! echo "$HTTP_CODE" | grep -qE "^[23][0-9][0-9]$"; then
    echo "ALERTA: Servicio web (Apache2) NO responde en localhost:80 - $(date)"
fi
