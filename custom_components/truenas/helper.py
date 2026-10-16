"""Helper functions."""

from __future__ import annotations

from typing import Any


# ---------------------------
#   parse_update_status
# ---------------------------
def parse_update_status(result: Any) -> tuple[bool, str] | None:
    """Read an update.status response.

    Returns (update_available, new_version), or None when the response
    cannot be used (error code, API error, unexpected shape).
    """
    if not isinstance(result, dict) or result.get("code") != "NORMAL":
        return None

    status = result.get("status")
    if not isinstance(status, dict):
        return None

    new_version = status.get("new_version")
    if isinstance(new_version, dict) and new_version.get("version"):
        return True, str(new_version["version"])

    return False, ""


# ---------------------------
#   format_attribute
# ---------------------------
def format_attribute(attr: str) -> str:
    """Format attribute."""
    attr = attr.replace("_", " ")
    attr = attr.replace("-", " ")
    attr = attr.capitalize()
    attr = attr.replace("zfs", "ZFS")
    attr = attr.replace(" gib", " GiB")
    attr = attr.replace("Cpu ", "CPU ")
    attr = attr.replace("Vcpu ", "vCPU ")
    attr = attr.replace("Vmware ", "VMware ")
    attr = attr.replace("Ip4 ", "IP4 ")
    attr = attr.replace("Ip6 ", "IP6 ")
    return attr
