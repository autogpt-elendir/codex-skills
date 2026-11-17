#!/usr/bin/env python3
"""Estimate maintained mean illuminance for identical luminaires in one zone."""

import argparse
import json
import math
from decimal import Decimal, InvalidOperation, ROUND_CEILING


def positive_number(value, name):
    """Read decimal inputs without silently accepting NaN, infinity or booleans."""
    try:
        if isinstance(value, bool):
            raise ValueError
        number = Decimal(str(value))
        if not number.is_finite() or number <= 0:
            raise ValueError
    except (InvalidOperation, ValueError) as error:
        raise ValueError(
            f"{name} doit être un nombre fini strictement positif"
        ) from error
    return number


def json_number(value):
    """Keep JSON interoperable: never emit nonstandard Infinity or NaN values."""
    try:
        result = float(value)
    except (OverflowError, ValueError) as error:
        raise ValueError(
            "résultat hors de la plage numérique JSON prise en charge"
        ) from error
    if not math.isfinite(result) or (value != 0 and result == 0):
        raise ValueError("résultat hors de la plage numérique JSON prise en charge")
    return result


def calculate(
    area_m2,
    lumens_per_fixture,
    utilization_factor,
    maintenance_factor,
    *,
    fixtures=None,
    target_lux=None,
):
    """Compute an average estimate, a required count, or both; no spatial simulation."""
    area = positive_number(area_m2, "surface")
    flux = positive_number(lumens_per_fixture, "flux par luminaire")
    utilization = positive_number(utilization_factor, "UF")
    maintenance = positive_number(maintenance_factor, "MF")
    if utilization > 1 or maintenance > 1:
        raise ValueError("UF et MF doivent être compris entre 0 exclu et 1 inclus")
    if fixtures is None and target_lux is None:
        raise ValueError("fournir --fixtures, --target-lux ou les deux")
    if fixtures is not None and (
        isinstance(fixtures, bool) or not isinstance(fixtures, int) or fixtures < 0
    ):
        raise ValueError("la quantité doit être un entier supérieur ou égal à zéro")

    result = {
        "method": "maintained-average-lumen-estimate",
        "inputs": {
            "area_m2": json_number(area),
            "lumens_per_fixture": json_number(flux),
            "utilization_factor": json_number(utilization),
            "maintenance_factor": json_number(maintenance),
        },
        "limitations": [
            "Moyenne estimée pour une zone et des luminaires identiques.",
            "UF et MF sont fournis par l’utilisateur, pas déduits par ce calcul.",
            "Ombres, éclairement minimal, uniformité et éblouissement non calculés.",
            "Ne constitue ni une simulation point par point ni une conformité.",
        ],
    }
    useful_flux_per_fixture = flux * utilization * maintenance
    target = None
    if target_lux is not None:
        target = positive_number(target_lux, "cible en lux")
        required_flux = target * area / (utilization * maintenance)
        result["target_lux"] = json_number(target)
        result["required_total_lumens_lm"] = json_number(required_flux)
        required_count = target * area / useful_flux_per_fixture
        result["minimum_fixture_count"] = int(
            required_count.to_integral_value(rounding=ROUND_CEILING)
        )
    count = fixtures if fixtures is not None else result["minimum_fixture_count"]
    maintained_lux = Decimal(count) * useful_flux_per_fixture / area
    result["fixtures"] = count
    result["total_lumens_lm"] = json_number(Decimal(count) * flux)
    result["estimated_maintained_average_lux"] = json_number(maintained_lux)
    if target is not None:
        result["average_estimate_reaches_target"] = maintained_lux >= target
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(
        description=(
            "Estime l’éclairement moyen par la méthode des lumens. "
            "UF et MF sont obligatoires et doivent être justifiés séparément. "
            "Ne calcule pas les ombres, l’uniformité ou l’éblouissement."
        ),
        epilog="Sortie JSON sur stdout ; erreur d’entrée : code 2, sans résultat partiel.",
    )
    parser.add_argument(
        "--area-m2", required=True, help="surface de la zone éclairée, en m²"
    )
    parser.add_argument(
        "--lumens-per-fixture",
        required=True,
        help="flux de sortie d’un luminaire, en lm",
    )
    parser.add_argument(
        "--utilization-factor", required=True, help="UF explicite : 0 < UF <= 1"
    )
    parser.add_argument(
        "--maintenance-factor", required=True, help="MF explicite : 0 < MF <= 1"
    )
    parser.add_argument(
        "--fixtures", type=int, help="quantité existante ou proposée, >= 0"
    )
    parser.add_argument("--target-lux", help="cible moyenne choisie, en lx")
    args = parser.parse_args(argv)
    try:
        result = calculate(
            args.area_m2,
            args.lumens_per_fixture,
            args.utilization_factor,
            args.maintenance_factor,
            fixtures=args.fixtures,
            target_lux=args.target_lux,
        )
    except (ValueError, InvalidOperation, OverflowError) as error:
        parser.error(str(error))
    print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
