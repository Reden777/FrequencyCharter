#!/usr/bin/env python3
"""Find products shared by two or more of the supplied base numbers.

Examples:
    python find_coincident_multiples.py
    python find_coincident_multiples.py --max-factor 300

The bases and products are handled as exact fractions, so decimal values such
as 731.35 and 1.618 do not suffer floating-point rounding errors.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from fractions import Fraction


BASES = (
    "174",
    "285",
    "396",
    "417",
    "528",
    "639",
    "852",
    "963",
    "731.35",
    "360",
    "7.83",
    "1.618",
)


def display(value: Fraction) -> str:
    """Use a tidy exact representation for a product."""
    if value.denominator == 1:
        return str(value.numerator)
    return f"{float(value):.12g} ({value.numerator}/{value.denominator})"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Print products reached by two or more base numbers."
    )
    parser.add_argument(
        "--max-factor", type=int, default=120,
        help="test every integer multiplier from 1 through this value (default: 120)",
    )
    parser.add_argument(
        "--min-factor", type=int, default=1,
        help="first integer multiplier to test (default: 1)",
    )
    args = parser.parse_args()
    if args.min_factor < 1 or args.max_factor < args.min_factor:
        parser.error("factors must be positive and max-factor must be at least min-factor")

    products: dict[Fraction, list[tuple[str, int]]] = defaultdict(list)
    for label in BASES:
        base = Fraction(label)
        for factor in range(args.min_factor, args.max_factor + 1):
            products[base * factor].append((label, factor))

    matches = [
        (product, sources) for product, sources in products.items() if len(sources) >= 2
    ]
    matches.sort(key=lambda item: item[0])

    print(
        f"Shared products for factors {args.min_factor}–{args.max_factor}: "
        f"{len(matches)} results\n"
    )
    for product, sources in matches:
        calculations = " = ".join(f"{base} × {factor}" for base, factor in sources)
        print(f"N={len(sources)}  {display(product)}: {calculations}")


if __name__ == "__main__":
    main()
