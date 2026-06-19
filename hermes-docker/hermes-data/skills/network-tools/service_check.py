#!/usr/bin/env python3
"""
Verifica el estado de servicios en la máquina: Apache (puerto 80) y SSH (puerto 22).
Uso: service_check.py [apache|ssh|all]
"""
import subprocess
import sys


def check_port(host: str, port: int, timeout: int = 3) -> bool:
    result = subprocess.run(
        ["nc", "-z", "-w", str(timeout), host, str(port)],
        capture_output=True
    )
    return result.returncode == 0


def check_apache() -> dict:
    alive = check_port("localhost", 80)
    details = {}
    if not alive:
        # Diagnóstico automático cuando Apache no responde
        checks = {
            "proceso": ["pgrep", "-a", "apache2"],
            "puerto_ocupado": ["ss", "-tlnp"],
            "systemctl": ["systemctl", "status", "apache2", "--no-pager", "-l"],
        }
        for key, cmd in checks.items():
            r = subprocess.run(cmd, capture_output=True, text=True)
            details[key] = r.stdout.strip() or r.stderr.strip() or "(sin salida)"
    return {"servicio": "Apache (puerto 80)", "activo": alive, "diagnostico": details}


def check_ssh() -> dict:
    alive = check_port("localhost", 22)
    details = {}
    if not alive:
        r = subprocess.run(["ss", "-tlnp"], capture_output=True, text=True)
        details["puertos_activos"] = r.stdout.strip()
    return {"servicio": "SSH (puerto 22)", "activo": alive, "diagnostico": details}


def format_result(res: dict) -> str:
    estado = "✅ ACTIVO" if res["activo"] else "❌ NO RESPONDE"
    lines = [f"{res['servicio']}: {estado}"]
    if res["diagnostico"]:
        lines.append("\n🔍 Diagnóstico automático:")
        for k, v in res["diagnostico"].items():
            lines.append(f"\n[{k}]\n{v}")
        lines.append("\n💡 Recomendación:")
        if "apache" in res["servicio"].lower():
            lines.append("  → sudo systemctl start apache2")
            lines.append("  → sudo systemctl enable apache2")
        else:
            lines.append("  → sudo systemctl start ssh")
    return "\n".join(lines)


def main():
    target = sys.argv[1].lower() if len(sys.argv) > 1 else "all"
    if target == "apache":
        print(format_result(check_apache()))
    elif target == "ssh":
        print(format_result(check_ssh()))
    else:
        print(format_result(check_apache()))
        print("\n" + "─" * 40 + "\n")
        print(format_result(check_ssh()))


if __name__ == "__main__":
    main()
