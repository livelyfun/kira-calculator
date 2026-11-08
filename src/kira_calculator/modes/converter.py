"""Unit conversion engine supporting length, mass, temperature, data, area, speed, time, and volume."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from ..core.errors import IncompatibleUnitError, UnknownUnitError


@dataclass(frozen=True)
class UnitDefinition:
    name: str
    symbol: str
    to_base: Callable[[float], float]
    from_base: Callable[[float], float]


# Conversion functions
def _linear(factor: float) -> tuple[Callable[[float], float], Callable[[float], float]]:
    return (lambda x, f=factor: x * f), (lambda x, f=factor: x / f)


CATEGORIES: dict[str, dict[str, UnitDefinition]] = {
    "Length": {
        "Meter (m)": UnitDefinition("Meter", "m", *_linear(1.0)),
        "Kilometer (km)": UnitDefinition("Kilometer", "km", *_linear(1000.0)),
        "Centimeter (cm)": UnitDefinition("Centimeter", "cm", *_linear(0.01)),
        "Millimeter (mm)": UnitDefinition("Millimeter", "mm", *_linear(0.001)),
        "Micrometer (µm)": UnitDefinition("Micrometer", "µm", *_linear(1e-6)),
        "Nanometer (nm)": UnitDefinition("Nanometer", "nm", *_linear(1e-9)),
        "Mile (mi)": UnitDefinition("Mile", "mi", *_linear(1609.344)),
        "Yard (yd)": UnitDefinition("Yard", "yd", *_linear(0.9144)),
        "Foot (ft)": UnitDefinition("Foot", "ft", *_linear(0.3048)),
        "Inch (in)": UnitDefinition("Inch", "in", *_linear(0.0254)),
        "Nautical Mile (nmi)": UnitDefinition("Nautical Mile", "nmi", *_linear(1852.0)),
    },
    "Mass": {
        "Kilogram (kg)": UnitDefinition("Kilogram", "kg", *_linear(1.0)),
        "Gram (g)": UnitDefinition("Gram", "g", *_linear(0.001)),
        "Milligram (mg)": UnitDefinition("Milligram", "mg", *_linear(1e-6)),
        "Metric Ton (t)": UnitDefinition("Metric Ton", "t", *_linear(1000.0)),
        "Pound (lb)": UnitDefinition("Pound", "lb", *_linear(0.45359237)),
        "Ounce (oz)": UnitDefinition("Ounce", "oz", *_linear(0.028349523125)),
        "Stone (st)": UnitDefinition("Stone", "st", *_linear(6.35029318)),
    },
    "Temperature": {
        "Celsius (°C)": UnitDefinition(
            "Celsius",
            "°C",
            to_base=lambda c: c,
            from_base=lambda c: c,
        ),
        "Fahrenheit (°F)": UnitDefinition(
            "Fahrenheit",
            "°F",
            to_base=lambda f: (f - 32.0) * 5.0 / 9.0,
            from_base=lambda c: (c * 9.0 / 5.0) + 32.0,
        ),
        "Kelvin (K)": UnitDefinition(
            "Kelvin",
            "K",
            to_base=lambda k: k - 273.15,
            from_base=lambda c: c + 273.15,
        ),
    },
    "Data": {
        "Byte (B)": UnitDefinition("Byte", "B", *_linear(1.0)),
        "Kilobyte (KB)": UnitDefinition("Kilobyte", "KB", *_linear(1000.0)),
        "Megabyte (MB)": UnitDefinition("Megabyte", "MB", *_linear(1e6)),
        "Gigabyte (GB)": UnitDefinition("Gigabyte", "GB", *_linear(1e9)),
        "Terabyte (TB)": UnitDefinition("Terabyte", "TB", *_linear(1e12)),
        "Petabyte (PB)": UnitDefinition("Petabyte", "PB", *_linear(1e15)),
        "Kibibyte (KiB)": UnitDefinition("Kibibyte", "KiB", *_linear(1024.0)),
        "Mebibyte (MiB)": UnitDefinition("Mebibyte", "MiB", *_linear(1024.0**2)),
        "Gibibyte (GiB)": UnitDefinition("Gibibyte", "GiB", *_linear(1024.0**3)),
        "Tebibyte (TiB)": UnitDefinition("Tebibyte", "TiB", *_linear(1024.0**4)),
    },
    "Area": {
        "Square Meter (m²)": UnitDefinition("Square Meter", "m²", *_linear(1.0)),
        "Square Kilometer (km²)": UnitDefinition("Square Kilometer", "km²", *_linear(1e6)),
        "Square Foot (ft²)": UnitDefinition("Square Foot", "ft²", *_linear(0.09290304)),
        "Square Mile (mi²)": UnitDefinition("Square Mile", "mi²", *_linear(2589988.110336)),
        "Acre (ac)": UnitDefinition("Acre", "ac", *_linear(4046.8564224)),
        "Hectare (ha)": UnitDefinition("Hectare", "ha", *_linear(10000.0)),
    },
    "Speed": {
        "Meter/second (m/s)": UnitDefinition("Meter/second", "m/s", *_linear(1.0)),
        "Kilometer/hour (km/h)": UnitDefinition("Kilometer/hour", "km/h", *_linear(1.0 / 3.6)),
        "Mile/hour (mph)": UnitDefinition("Mile/hour", "mph", *_linear(0.44704)),
        "Knot (kn)": UnitDefinition("Knot", "kn", *_linear(1852.0 / 3600.0)),
        "Foot/second (ft/s)": UnitDefinition("Foot/second", "ft/s", *_linear(0.3048)),
    },
    "Time": {
        "Millisecond (ms)": UnitDefinition("Millisecond", "ms", *_linear(0.001)),
        "Second (s)": UnitDefinition("Second", "s", *_linear(1.0)),
        "Minute (min)": UnitDefinition("Minute", "min", *_linear(60.0)),
        "Hour (h)": UnitDefinition("Hour", "h", *_linear(3600.0)),
        "Day (d)": UnitDefinition("Day", "d", *_linear(86400.0)),
        "Week (wk)": UnitDefinition("Week", "wk", *_linear(604800.0)),
        "Year (yr)": UnitDefinition("Year", "yr", *_linear(31557600.0)),  # 365.25 days
    },
    "Volume": {
        "Liter (L)": UnitDefinition("Liter", "L", *_linear(1.0)),
        "Milliliter (mL)": UnitDefinition("Milliliter", "mL", *_linear(0.001)),
        "Cubic Meter (m³)": UnitDefinition("Cubic Meter", "m³", *_linear(1000.0)),
        "US Gallon (gal)": UnitDefinition("US Gallon", "gal", *_linear(3.785411784)),
        "US Quart (qt)": UnitDefinition("US Quart", "qt", *_linear(0.946352946)),
        "US Pint (pt)": UnitDefinition("US Pint", "pt", *_linear(0.473176473)),
        "US Cup (cup)": UnitDefinition("US Cup", "cup", *_linear(0.2365882365)),
        "US Fluid Ounce (fl oz)": UnitDefinition(
            "US Fluid Ounce", "fl oz", *_linear(0.0295735295625)
        ),
        "Imperial Gallon (imp gal)": UnitDefinition(
            "Imperial Gallon", "imp gal", *_linear(4.54609)
        ),
    },
}


class UnitConverter:
    """Provides high-accuracy unit conversions across supported physical domains."""

    @staticmethod
    def get_categories() -> list[str]:
        return list(CATEGORIES.keys())

    @staticmethod
    def get_units(category: str) -> list[str]:
        if category not in CATEGORIES:
            raise UnknownUnitError(f"Category '{category}' is not recognized.")
        return list(CATEGORIES[category].keys())

    @classmethod
    def convert(
        cls,
        value: float,
        from_unit: str,
        to_unit: str,
        category: str | None = None,
    ) -> float:
        """Convert a numerical value from one unit to another.

        Args:
            value: The scalar input value.
            from_unit: The source unit name.
            to_unit: The target unit name.
            category: Optional explicit category name. If omitted, inferred.

        Returns:
            The converted float value.
        """
        # Resolve category
        cat_dict = None
        if category and category in CATEGORIES:
            cat_dict = CATEGORIES[category]
        else:
            for _cat_name, units in CATEGORIES.items():
                if from_unit in units and to_unit in units:
                    cat_dict = units
                    break

        if cat_dict is None:
            raise IncompatibleUnitError(
                f"Units '{from_unit}' and '{to_unit}' belong to incompatible categories."
            )

        if from_unit not in cat_dict:
            raise UnknownUnitError(f"Source unit '{from_unit}' is unknown.")
        if to_unit not in cat_dict:
            raise UnknownUnitError(f"Target unit '{to_unit}' is unknown.")

        unit_from = cat_dict[from_unit]
        unit_to = cat_dict[to_unit]

        base_val = unit_from.to_base(value)
        return unit_to.from_base(base_val)
