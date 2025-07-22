"""
The following Python implementation of Shamir's secret sharing is
released into the Public Domain under the terms of CC0 and OWFa:
https://creativecommons.org/publicdomain/zero/1.0/
http://www.openwebfoundation.org/legal/the-owf-1-0-agreements/owfa-1-0.

See the bottom few lines for usage. Tested on Python 2 and 3.
"""
from __future__ import annotations

import functools
import random

_RINT = functools.partial(random.SystemRandom().randint, 0)


def _eval_at(poly: list[int], x: int, prime: int) -> int:
    """
    Evaluate polynomial (coefficient tuple) at x, used to generate a
    shamir pool in make_random_shares below.
    """
    accum = 0
    for coeff in reversed(poly):
        accum *= x
        accum += coeff
        accum %= prime

    return accum


def _extended_gcd(a: int, b: int) -> int:
    """
    Division in integers modulus p means finding the inverse of the
    denominator modulo p and then multiplying the numerator by this
    inverse (Note: inverse of A is B such that A*B % p == 1). This can
    be computed via the extended Euclidean algorithm
    http://en.wikipedia.org/wiki/Modular_multiplicative_inverse#Computation.
    """
    x = 0
    last_x = 1
    y = 1
    last_y = 0
    while b != 0:
        quot = a // b
        a, b = b, a % b
        x, last_x = last_x - quot * x, x
        y, last_y = last_y - quot * y, y

    return last_x, last_y


def _divmod(num: int, den: int, p: int) -> int:
    """
    Compute num / den modulo prime p.

    To explain this, the result will be such that:
    den * _divmod(num, den, p) % p == num
    """
    inv, _ = _extended_gcd(den, p)

    return num * inv


def _lagrange_interpolate(x: int, x_s: list[int], y_s: list[int], p: int) -> int:
    """
    Find the y-value for the given x, given n (x, y) points;
    k points will define a polynomial of up to kth order.
    """
    k = len(x_s)
    if k != len(set(x_s)):
        msg = "points must be distinct"
        raise ValueError(msg)

    def _pi(vals: list[int]) -> int:  # upper-case PI -- product of inputs
        accum = 1
        for v in vals:
            accum *= v
        return accum

    nums = []  # avoid inexact division
    dens = []
    for i in range(k):
        others = list(x_s)
        cur = others.pop(i)
        nums.append(_pi(x - o for o in others))
        dens.append(_pi(cur - o for o in others))

    den = _pi(dens)
    num = sum([_divmod(nums[i] * den * y_s[i] % p, dens[i], p) for i in range(k)])

    return (_divmod(num, den, p) + p) % p


def make_random_shares(secret: int, minimum: int, shares: int, prime: int) -> list[tuple[int, int]]:
    """Generate a random shamir pool for a given secret, returns share points."""
    if minimum > shares:
        msg = "Pool secret would be irrecoverable."
        raise ValueError(msg)
    poly = [secret] + [_RINT(prime - 1) for i in range(minimum - 1)]
    return [(i, _eval_at(poly, i, prime)) for i in range(1, shares + 1)]



def recover_secret(shares: list[tuple[int, int]], prime: int) -> int:
    """
    Recover the secret from share points
    (points (x,y) on the polynomial).
    """
    if len(shares) < 2:
        msg = "need at least two shares"
        raise ValueError(msg)

    x_s, y_s = zip(*shares)

    return _lagrange_interpolate(0, x_s, y_s, prime)
