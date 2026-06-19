#!/usr/bin/env python3
import subprocess
import sys

def run(cmd, timeout=10):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return r.stdout.strip() or r.stderr.strip() or "(sin salida)"
    except Exception as e:
        return f"[ERROR] {e}"

def show_routes(router="router1"):
    result = run(["docker", "exec", router, "vtysh", "-c", "show ip route"])
    return f"=== Tabla de rutas en {router} ===\n{result}"

def apply_alternate(router="router1", metric="50"):
    if not metric.isdigit():
        return "[ERROR] La métrica debe ser un número"
    
    run(["docker", "exec", router, "vtysh",
         "-c", "configure terminal",
         "-c", "no ip route 10.0.1.0/24 172.30.0.20",
         "-c", "no ip route 192.168.100.0/24 172.30.0.20",
         "-c", f"ip route 10.0.1.0/24 172.30.0.20 {metric}",
         "-c", f"ip route 192.168.100.0/24 172.30.0.20 {metric}",
         "-c", "end"])
    
    tabla = run(["docker", "exec", router, "vtysh", "-c", "show ip route"])
    return (
        f"Política de enrutamiento alternativo aplicada\n"
        f"  Router: {router}\n"
        f"  Nueva metrica: {metric}\n"
        f"=== Tabla de rutas actualizada ===\n{tabla}"
    )

def restore_default(router="router1"):
    run(["docker", "exec", router, "vtysh",
         "-c", "configure terminal",
         "-c", "no ip route 10.0.1.0/24 172.30.0.20",
         "-c", "no ip route 192.168.100.0/24 172.30.0.20",
         "-c", "ip route 10.0.1.0/24 172.30.0.20 10",
         "-c", "ip route 192.168.100.0/24 172.30.0.20 10",
         "-c", "end"])
    
    tabla = run(["docker", "exec", router, "vtysh", "-c", "show ip route"])
    return (
        f"Rutas restauradas a configuración por defecto\n"
        f"=== Tabla de rutas actualizada ===\n{tabla}"
    )

def main():
    if len(sys.argv) < 2:
        print("Uso: routing_policy.py <show|apply|restore> [router] [metrica]")
        sys.exit(1)
    action = sys.argv[1].lower()
    router = sys.argv[2] if len(sys.argv) > 2 else "router1"
    metric = sys.argv[3] if len(sys.argv) > 3 else "50"
    
    if action == "show":
        print(show_routes(router))
    elif action == "apply":
        print(apply_alternate(router, metric))
    elif action == "restore":
        print(restore_default(router))
    else:
        print(f"[ERROR] Acción desconocida: {action}")
        sys.exit(1)

if __name__ == "__main__":
    main()
