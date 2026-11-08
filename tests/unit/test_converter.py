"""Unit tests for the Unit Converter mode."""

import unittest

from kira_calculator.core.errors import IncompatibleUnitError, UnknownUnitError
from kira_calculator.modes.converter import UnitConverter


class TestUnitConverter(unittest.TestCase):
    def test_length_conversions(self):
        # 1 km = 1000 m
        self.assertAlmostEqual(UnitConverter.convert(1, "Kilometer (km)", "Meter (m)"), 1000.0)
        # 1 meter = 100 cm
        self.assertAlmostEqual(UnitConverter.convert(1, "Meter (m)", "Centimeter (cm)"), 100.0)
        # 1 foot = 0.3048 m
        self.assertAlmostEqual(UnitConverter.convert(1, "Foot (ft)", "Meter (m)"), 0.3048)
        # 1 mile = 1609.344 m
        self.assertAlmostEqual(UnitConverter.convert(1, "Mile (mi)", "Meter (m)"), 1609.344)

    def test_mass_conversions(self):
        # 1 kg = 1000 g
        self.assertAlmostEqual(UnitConverter.convert(1, "Kilogram (kg)", "Gram (g)"), 1000.0)
        # 1 lb = 0.45359237 kg
        self.assertAlmostEqual(UnitConverter.convert(1, "Pound (lb)", "Kilogram (kg)"), 0.45359237)

    def test_temperature_conversions(self):
        # 0 °C = 32 °F
        self.assertAlmostEqual(UnitConverter.convert(0, "Celsius (°C)", "Fahrenheit (°F)"), 32.0)
        # 100 °C = 212 °F
        self.assertAlmostEqual(UnitConverter.convert(100, "Celsius (°C)", "Fahrenheit (°F)"), 212.0)
        # -40 °C = -40 °F
        self.assertAlmostEqual(UnitConverter.convert(-40, "Celsius (°C)", "Fahrenheit (°F)"), -40.0)
        # 0 °C = 273.15 K
        self.assertAlmostEqual(UnitConverter.convert(0, "Celsius (°C)", "Kelvin (K)"), 273.15)
        # 300 K to Celsius
        self.assertAlmostEqual(UnitConverter.convert(300, "Kelvin (K)", "Celsius (°C)"), 26.85)

    def test_data_conversions(self):
        # 1 Kilobyte = 1000 Bytes
        self.assertAlmostEqual(UnitConverter.convert(1, "Kilobyte (KB)", "Byte (B)"), 1000.0)
        # 1 Kibibyte = 1024 Bytes
        self.assertAlmostEqual(UnitConverter.convert(1, "Kibibyte (KiB)", "Byte (B)"), 1024.0)
        # 1 Megabyte = 1e6 Bytes
        self.assertAlmostEqual(UnitConverter.convert(1, "Megabyte (MB)", "Byte (B)"), 1e6)
        # 1 Mebibyte = 1048576 Bytes
        self.assertAlmostEqual(UnitConverter.convert(1, "Mebibyte (MiB)", "Byte (B)"), 1048576.0)

    def test_time_conversions(self):
        # 1 hour = 3600 seconds
        self.assertAlmostEqual(UnitConverter.convert(1, "Hour (h)", "Second (s)"), 3600.0)
        # 1 day = 24 hours
        self.assertAlmostEqual(UnitConverter.convert(1, "Day (d)", "Hour (h)"), 24.0)

    def test_speed_conversions(self):
        # 100 km/h in m/s
        self.assertAlmostEqual(
            UnitConverter.convert(100, "Kilometer/hour (km/h)", "Meter/second (m/s)"),
            100.0 / 3.6,
        )

    def test_area_conversions(self):
        # 1 sq km = 1e6 sq m
        self.assertAlmostEqual(UnitConverter.convert(1, "Square Kilometer (km²)", "Square Meter (m²)"), 1e6)
        # 1 hectare = 10000 sq m
        self.assertAlmostEqual(UnitConverter.convert(1, "Hectare (ha)", "Square Meter (m²)"), 10000.0)
        # 1 sq ft = 0.09290304 sq m
        self.assertAlmostEqual(UnitConverter.convert(1, "Square Foot (ft²)", "Square Meter (m²)"), 0.09290304)
        # 1 acre in sq m
        self.assertAlmostEqual(UnitConverter.convert(1, "Acre (ac)", "Square Meter (m²)"), 4046.8564224)

    def test_volume_conversions(self):
        # 1 cubic meter = 1000 liters
        self.assertAlmostEqual(UnitConverter.convert(1, "Cubic Meter (m³)", "Liter (L)"), 1000.0)
        # 1 liter = 1000 ml
        self.assertAlmostEqual(UnitConverter.convert(1, "Liter (L)", "Milliliter (mL)"), 1000.0)
        # 1 US Gallon = 3.785411784 L
        self.assertAlmostEqual(UnitConverter.convert(1, "US Gallon (gal)", "Liter (L)"), 3.785411784)
        # 1 US Quart = 0.946352946 L
        self.assertAlmostEqual(UnitConverter.convert(1, "US Quart (qt)", "Liter (L)"), 0.946352946)

    def test_zero_and_negative_values(self):
        # Zero conversions
        self.assertEqual(UnitConverter.convert(0, "Meter (m)", "Kilometer (km)"), 0.0)
        self.assertEqual(UnitConverter.convert(0, "Celsius (°C)", "Kelvin (K)"), 273.15)
        self.assertEqual(UnitConverter.convert(0, "Byte (B)", "Megabyte (MB)"), 0.0)
        # Negative temperature
        self.assertAlmostEqual(UnitConverter.convert(-10, "Celsius (°C)", "Fahrenheit (°F)"), 14.0)

    def test_decimal_precision(self):
        # High precision preservation
        converted = UnitConverter.convert(1.23456789, "Meter (m)", "Centimeter (cm)")
        self.assertAlmostEqual(converted, 123.456789, places=6)

    def test_incompatible_categories(self):
        with self.assertRaises(IncompatibleUnitError):
            UnitConverter.convert(10, "Meter (m)", "Kilogram (kg)")

    def test_unknown_unit(self):
        with self.assertRaises((UnknownUnitError, IncompatibleUnitError)):
            UnitConverter.convert(5, "Furlong", "Meter (m)")


if __name__ == "__main__":
    unittest.main()

