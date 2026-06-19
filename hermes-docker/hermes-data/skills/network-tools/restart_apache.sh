#!/bin/bash
echo "🔧 Intentando reiniciar Apache2..."

# Verificar si ya está activo
if curl -s -o /dev/null -w "%{http_code}" --max-time 3 http://localhost:80 | grep -qE "^[2-3][0-9][0-9]$"; then
    echo "✅ Apache ya está activo en el puerto 80. No es necesario reiniciarlo."
    exit 0
fi

# Usar el servidor de control de la VM host
RESULTADO=$(curl -s --max-time 10 http://127.0.0.1:9999/restart_apache)

if [ $? -ne 0 ]; then
    echo "⚠️ No se pudo conectar al servidor de control."
    echo "💡 Ejecuta manualmente en la VM: sudo systemctl start apache2"
    exit 1
fi

sleep 3

# Verificar resultado
if curl -s -o /dev/null -w "%{http_code}" --max-time 3 http://localhost:80 | grep -qE "^[2-3][0-9][0-9]$"; then
    echo "✅ Apache2 reiniciado correctamente. Puerto 80 activo."
else
    echo "⚠️ Apache2 no respondió después del reinicio."
    echo "📋 Salida del comando:"
    echo "$RESULTADO"
fi
