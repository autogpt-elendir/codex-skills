"""Numerical and CLI checks with synthetic data; no real room or product inputs."""

import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "lumen_method.py"
SPEC = importlib.util.spec_from_file_location("lumen_method", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class LumenMethodTests(unittest.TestCase):
    def estimate(self, **changes):
        values = dict(
            area_m2=24,
            lumens_per_fixture=2400,
            utilization_factor=0.6,
            maintenance_factor=0.8,
            fixtures=4,
        )
        values.update(changes)
        return MODULE.calculate(**values)

    def test_existing_quantity_includes_both_losses(self):
        result = self.estimate()
        self.assertEqual(result["total_lumens_lm"], 9600)
        self.assertEqual(result["estimated_maintained_average_lux"], 192)

    def test_required_flux_divides_by_both_factors(self):
        result = self.estimate(fixtures=None, target_lux=200)
        self.assertEqual(result["required_total_lumens_lm"], 10000)
        self.assertEqual(result["minimum_fixture_count"], 5)
        self.assertEqual(result["estimated_maintained_average_lux"], 240)

    def test_existing_quantity_is_not_replaced_by_target_count(self):
        result = self.estimate(target_lux=200)
        self.assertEqual(result["fixtures"], 4)
        self.assertEqual(result["minimum_fixture_count"], 5)
        self.assertFalse(result["average_estimate_reaches_target"])

    def test_exact_decimal_boundary_does_not_add_an_extra_fixture(self):
        result = MODULE.calculate(1, 10, "0.1", 1, target_lux=1)
        self.assertEqual(result["minimum_fixture_count"], 1)
        self.assertTrue(result["average_estimate_reaches_target"])

    def test_rounding_up_is_minimal_for_various_targets(self):
        for target in (1, 199, 200, 201, 500, 750):
            with self.subTest(target=target):
                result = self.estimate(fixtures=None, target_lux=target)
                count = result["minimum_fixture_count"]
                self.assertGreaterEqual(
                    result["estimated_maintained_average_lux"], target
                )
                previous = self.estimate(fixtures=count - 1)
                self.assertLess(previous["estimated_maintained_average_lux"], target)

    def test_poorer_factors_increase_required_count(self):
        base = self.estimate(fixtures=None, target_lux=200)["minimum_fixture_count"]
        for change in ({"utilization_factor": 0.3}, {"maintenance_factor": 0.4}):
            with self.subTest(change=change):
                count = self.estimate(fixtures=None, target_lux=200, **change)[
                    "minimum_fixture_count"
                ]
                self.assertGreater(count, base)

    def test_double_area_halves_mean_lux(self):
        self.assertEqual(
            self.estimate(area_m2=48)["estimated_maintained_average_lux"], 96
        )

    def test_zero_existing_luminaires_is_a_valid_baseline(self):
        result = self.estimate(fixtures=0, target_lux=200)
        self.assertEqual(result["estimated_maintained_average_lux"], 0)
        self.assertEqual(result["minimum_fixture_count"], 5)
        self.assertFalse(result["average_estimate_reaches_target"])

    def test_reject_invalid_photometric_inputs(self):
        for key in (
            "area_m2",
            "lumens_per_fixture",
            "utilization_factor",
            "maintenance_factor",
            "target_lux",
        ):
            for value in (0, -1, "NaN", "Infinity", "-Infinity", "not-a-number", True):
                with self.subTest(key=key, value=value):
                    with self.assertRaises(ValueError):
                        self.estimate(**{key: value})

    def test_reject_factors_above_one(self):
        for key in ("utilization_factor", "maintenance_factor"):
            with self.subTest(key=key):
                with self.assertRaises(ValueError):
                    self.estimate(**{key: 1.01})

    def test_reject_fractional_negative_or_boolean_quantities(self):
        for count in (1.5, -1, True, "2"):
            with self.subTest(count=count):
                with self.assertRaises(ValueError):
                    self.estimate(fixtures=count)

    def test_reject_missing_quantity_and_target(self):
        with self.assertRaises(ValueError):
            self.estimate(fixtures=None)

    def test_reject_json_overflow_instead_of_emitting_infinity(self):
        with self.assertRaises(ValueError):
            self.estimate(area_m2="1e300", fixtures=None, target_lux="1e300")


class CliTests(unittest.TestCase):
    args = [
        "--area-m2",
        "24",
        "--lumens-per-fixture",
        "2400",
        "--utilization-factor",
        "0.6",
        "--maintenance-factor",
        "0.8",
    ]

    def run_cli(self, *args):
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            capture_output=True,
            text=True,
            check=False,
        )

    def test_help(self):
        result = self.run_cli("--help")
        self.assertEqual(result.returncode, 0)
        self.assertIn("--target-lux", result.stdout)

    def test_successful_json_output(self):
        result = self.run_cli(*self.args, "--target-lux", "200")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["minimum_fixture_count"], 5)

    def test_factors_are_required_without_defaults(self):
        result = self.run_cli(
            "--area-m2", "24", "--lumens-per-fixture", "2400", "--target-lux", "200"
        )
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")

    def test_invalid_input_has_no_partial_json_or_traceback(self):
        for extra in (("--fixtures", "-1"), ("--target-lux", "NaN"), ()):
            with self.subTest(extra=extra):
                result = self.run_cli(*self.args, *extra)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(result.stdout, "")
                self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
