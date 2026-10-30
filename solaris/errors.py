"""Errores del núcleo Solaris."""

from __future__ import annotations


class SolarisError(Exception):
    """Error base del proyecto."""


class SchemaError(SolarisError):
    """Dato que no cumple el contrato."""


class AdapterError(SolarisError):
    """Fallo de un adaptador de modelo."""


class AdapterNotConfigured(AdapterError):
    """El adaptador requiere configuración ausente."""


class KillSwitchActive(SolarisError):
    """El kill switch está activo y el sistema no debe ejecutarse."""
