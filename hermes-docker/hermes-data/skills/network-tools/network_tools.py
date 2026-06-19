#!/usr/bin/env python3
"""
Network diagnostic tools skill for Hermes Agent.
Usage: network_tools.py <action> [target]
Actions: ping, traceroute, arp, snmp
"""
import subprocess
import sys
import shlex
import ipaddress
import re


def is_valid_target(target: str) -> bool:
    """Allow only IPs or simple hostnames to avoid command injection."""
    try:
        ipaddress.ip_address(target)
        return True
    except ValueError:
        pass
    return bool(re.match(r'^[a-zA-Z0-9.-]+$', target))


def run(cmd: list, timeout: int = 15) -> str:
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout
        )
        output = result.stdout.strip()
        if result.returncode != 0:
            output += f"\n[exit code {result.returncode}] {result.stderr.strip()}"
        return output or "(sin salida)"
    except subprocess.TimeoutExpired:
        return f"[ERROR] Comando excedió el tiempo límite de {timeout}s"
    except FileNotFoundError:
        return f"[ERROR] Comando no encontrado: {cmd[0]}"


def do_ping(target: str) -> str:
    return run(["ping", "-c", "4", target])


def do_traceroute(target: str) -> str:
    return run(["traceroute", "-m", "15", target], timeout=30)


def do_arp(_target: str = None) -> str:
    return run(["arp", "-a"])


def do_snmp(target: str, community: str = "public", oid: str = "1.3.6.1.2.1.1.1.0") -> str:
    return run(["snmpget", "-v2c", "-c", community, target, oid], timeout=10)


def main():
    if len(sys.argv) < 2:
        print("Uso: network_tools.py <ping|traceroute|arp|snmp> [target] [community]")
        sys.exit(1)

    action = sys.argv[1].lower()
    target = sys.argv[2] if len(sys.argv) > 2 else None

    if action in ("ping", "traceroute", "snmp") and not target:
        print(f"[ERROR] La acción '{action}' requiere un target (IP u hostname)")
        sys.exit(1)

    if target and not is_valid_target(target):
        print(f"[ERROR] Target inválido o potencialmente peligroso: {target}")
        sys.exit(1)

    if action == "ping":
        print(do_ping(target))
    elif action == "traceroute":
        print(do_traceroute(target))
    elif action == "arp":
        print(do_arp())
    elif action == "snmp":
        community = sys.argv[3] if len(sys.argv) > 3 else "public"
        print(do_snmp(target, community))
    else:
        print(f"[ERROR] Acción desconocida: {action}")
        sys.exit(1)


if __name__ == "__main__":
    main()
