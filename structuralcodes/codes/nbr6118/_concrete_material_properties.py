"""A collection of material properties for concrete."""

from __future__ import annotations  # To have clean hints of ArrayLike in docs

import math
from typing import Literal

import numpy as np
import numpy.typing as npt

aggregate_types = Literal['basalt', 'granite', 'limestone', 'sandstone']
"""Type alias for aggregate types used in concrete."""

cement_classes = Literal['CPI', 'CPII', 'CPIII', 'CPIV', 'CPV']
"""Type alias for cement classes used in concrete."""

# Values from Sec. 8.2.8.
ALPHA_E = {
    'basalt': 1.2,    # Basalto
    'granite': 1.0,   # Granito ou gnaisse
    'limestone': 0.9, # Calcário
    'sandstone': 0.7, # Arenito
}

# Values for normal strength concrete, from Table 5.1-9.
S_CEM = {
    'CPI':   0.25,
    'CPIII': 0.38,
    'CPV':   0.20,
}
S_CEM['CPII'] = S_CEM['CPI']
S_CEM['CPIV'] = S_CEM['CPIII']


def _fck(fck: float) -> float:
    """Ensure fck is positive and applicable for reinforced concrete, according
    to ABNT NBR 6118 (2023), Sec. 8.2.1.

    Args:
        fck (float): The characteristic compressive strength in MPa.
    Raises:
        ValueError: If fck is less than 20 MPa or greater than 90 MPa.
    Returns:
        float: The absolute value of fck in MPa
    """
    fck = abs(fck)
    if fck < 20 or fck > 90:
        raise ValueError(
            "fck must be between 20 MPa and 90 MPa for reinforced concrete,"
            "according to ABNT NBR 6118 (2023)."
            f"fck = {fck} MPa given."
        )
    return fck


def fcd(fck: float, gamma_c: float = 1.4) -> float:
    """The design compressive strength of concrete.

    ABNT NBR 6118 (2023), Sec. 12.3.3 and 12.4.1.

    Args:
        fck (float): The characteristic compressive strength in MPa.

    Keyword Args:
        gamma_c (float): The partial factor of concrete. Default value 1.4.

    Returns:
        float: The design compressive strength of concrete in MPa.
    """
    return _fck(fck) / abs(gamma_c)


def fctm(fck: float) -> float:
    """Compute the mean concrete tensile strength from the characteristic
    compressive strength.

    ABNT NBR 6118 (2023), Sec. 8.2.5.

    Args:
        fck (float): The characteristic compressive strength in MPa.

    Returns:
        float: The mean tensile strength in MPa.
    """
    fck = _fck(fck)
    return (
        0.3 * fck ** (2 / 3)
        if fck <= 50
        else 2.12 * math.log(1 + 0.1 * (fck + 8))
    )


def fctkinf(fctm: float) -> float:
    """Compute the lower bound value of the characteristic tensile strength
    from the mean tensile strength.

    ABNT NBR 6118 (2023), Sec. 8.2.5.

    Args:
        fctm (float): The mean tensile strength in MPa.

    Returns:
        float: Lower bound of the characteristic tensile strength in MPa.
    """
    return 0.7 * fctm


def fctksup(fctm: float) -> float:
    """Compute the upper bound value of the characteristic tensile strength
    from the mean tensile strength.

    ABNT NBR 6118 (2023), Sec. 8.2.5.

    Args:
        fctm (float): The mean tensile strength in MPa.

    Returns:
        float: Upper bound of the characteristic tensile strength in MPa.
    """
    return 1.3 * fctm


def Eci(
    fck: float,
    agg_type: aggregate_types = 'granite',
) -> float:
    """Calculate the modulus of elasticity for normal weight concrete at 28
    days.

    ABNT NBR 6118 (2023), Sec. 8.2.8.

    Args:
        fck (float): The characteristic compressive strength in MPa.

    Keyword Args:
        agg_type (str): Type of coarse grain aggregate used in the concrete.
            Choices are: 'basalt', 'granite', 'limestone', 'sandstone'.

    Returns:
        float: The modulus of elasticity for normal weight concrete at 28 days
        in MPa.
    """
    alpha_E = ALPHA_E[agg_type.lower()]
    fck = _fck(fck)
    return (
        alpha_E * 5600 * math.sqrt(fck)
        if fck <= 50
        else 21.5e3 * alpha_E * (fck / 10 + 1.25) ** (1 / 3)
    )

def Ecs(
    fck: float,
    agg_type: aggregate_types = 'granite',
) -> float:
    """Calculate the secant modulus of elasticity for normal weight concrete
    at 28 days.

    ABNT NBR 6118 (2023), Sec. 8.2.8.

    Args:
        fck (float): The characteristic compressive strength in MPa.

    Keyword Args:
        agg_type (str): Type of coarse grain aggregate used in the concrete.
            Choices are: 'basalt', 'granite', 'limestone', 'sandstone'.

    Returns:
        float: The modulus of elasticity for normal weight concrete at 28 days
        in MPa.
    """
    fck = _fck(fck)
    alpha_i = min(0.8 + 0.2 * fck / 80, 1)
    return alpha_i * Eci(fck, agg_type)


def beta_1(
    time: npt.ArrayLike,
    cem_class: cement_classes,
) -> np.ndarray:
    """Calculate multiplication factor beta_1, used to determine the
    compressive strength at an arbitrary time.

    Defined in ABNT NBR 6118 (2023), Sec. 12.3.3.

    Args:
        time (numpy.typing.ArrayLike): The time in days at which the
            compressive strength is to be determined.
        cem_class (str): The cement strength class that is used. The choices
            are: 'CPI', 'CPII', 'CPIII', 'CPIV' and 'CPV'.

    Returns:
        numpy.ndarray: Multiplication factor beta_1.
    """
    s = S_CEM[cem_class.upper()]
    return np.exp(s * (1 - np.sqrt(28 / np.asarray(time))))


def fckj(
    fck: float,
    time: npt.ArrayLike,
    cem_class: cement_classes,
) -> np.ndarray:
    """Calculate the characteristic compressive strength of concrete at an
    arbitrary time.

    Defined in ABNT NBR 6118 (2023), Sec. 12.3.3.

    Args:
        fck (float): The characteristic compressive strength at 28 days, in
            MPa.
        time (numpy.typing.ArrayLike): The time in days at which the
            compressive strength is to be determined.
        cem_class (str): The cement strength class that is used. The choices
            are: 'CPI', 'CPII', 'CPIII', 'CPIV' and 'CPV'.
    Returns:
        numpy.ndarray: The characteristic compressive strength at the desired
            'time', in MPa.
    """
    return beta_1(time, cem_class) * _fck(fck)


def fcdj(
    fck: float,
    time: npt.ArrayLike,
    cem_class: cement_classes,
    gamma_c: float = 1.4,
) -> np.ndarray:
    """Calculate the design compressive strength of concrete at an arbitrary
    time.

    Defined in ABNT NBR 6118 (2023), Sec. 12.3.3.

    Args:
        fck (float): The characteristic compressive strength at 28 days, in
            MPa.
        time (numpy.typing.ArrayLike): The time in days at which the
            compressive strength is to be determined.
        cem_class (str): The cement strength class that is used. The choices
            are: 'CPI', 'CPII', 'CPIII', 'CPIV' and 'CPV'.
    Keyword Args:
        gamma_c (float): The partial factor of concrete. Default value 1.4.
    Returns:
        numpy.ndarray: The design compressive strength at the desired 'time',
            in MPa.
    """
    return fckj(fck, time, cem_class) / abs(gamma_c)


def Eci_t(
    fck: float,
    time: npt.ArrayLike,
    cem_class: cement_classes,
    agg_type: aggregate_types = 'granite',
) -> np.ndarray:
    """Calculate the modulus of elasticity for normal weight concrete at time
    'time' (not 28 days).

    Defined in ABNT NBR 6118 (2023), Sec. 8.2.8.

    Args:
        fck (float): The characteristic compressive strength at 28 days, in MPa.
        time (numpy.typing.ArrayLike): The time in days at which the
            compressive strength is to be determined.
        cem_class (str): The cement strength class that is used. The choices
            are: 'CPI', 'CPII', 'CPIII', 'CPIV' and 'CPV'.
    Keyword Args:
        agg_type (str): Type of coarse grain aggregate used in the concrete.
            Choices are: 'basalt', 'granite', 'limestone', 'sandstone'.
    Returns:
        numpy.ndarray: The modulus of elasticity for normal weight concrete at
        time 'time' (not 28 days) in MPa.
    """
    fck = _fck(fck)
    e = 0.5 if fck <= 50 else 0.3
    return (fckj(fck, time, cem_class) / fck) ** e * Eci(fck, agg_type)


def eta_c(fck: float) -> float:
    """The coefficient eta_c for parabola-rectangle diagram.

    Defined in ABNT NBR 6118 (2023), Sec. 8.2.10.1.

    Args:
        fck (float): The characteristic compressive strength in MPa.

    Returns:
        float: The coefficient eta_c, no unit.
    """
    fck = _fck(fck)
    return (
        1.0 if fck <= 40
        else (40 / fck) ** (1 / 3)
    )


def eps_c2(fck: float) -> float:
    """The compressive yield strain of concrete for parabolic-rectangular diagram.
    Occurs when compressive stress reaches 0.85 * eta_c * fcd.

    Defined in ABNT NBR 6118 (2023), Sec. 8.2.10.1.

    Args:
        fck (float): The characteristic compressive strength in MPa.

    Returns:
        float: The yield strain of concrete, absolute value, no unit.
    """
    fck = _fck(fck)
    return (
        2e-3 if fck <= 50
        else 2e-3 + 0.085e-3 * (fck - 50) ** 0.53
    )


def eps_cu(fck: float) -> float:
    """The ultimate strain of concrete for parabolic-rectangular diagram.

    Defined in ABNT NBR 6118 (2023), Sec. 8.2.10.1.

    Args:
        fck (float): The characteristic compressive strength in MPa.

    Returns:
        float: The ultimate strain of concrete, absolute value, no unit.
    """
    fck = _fck(fck)
    return (
        3.5e-3 if fck <= 50
        else 2.6e-3 + 35e-3 * ((90 - fck) / 100) ** 4
    )


def n_parabolic_rectangular(fck: float) -> float:
    """The exponent in the parabolic-rectangular law.

    Defined in ABNT NBR 6118 (2023), Sec. 8.2.10.1.

    Args:
        fck (float): The characteristic compressive strength of concrete in
            MPa.

    Returns:
        float: The exponent n, absolute value, no unit.
    """
    fck = _fck(fck)
    return (
        2.0 if fck <= 50
        else (1.4 + 23.4 * ((90 - fck) / 100) ** 4)
    )


def fcm(fck: float) -> float:
    """Compute the mean concrete compressive strength from the characteristic
    strength. Used for nonlinear analysis (Sargin constitutive law).

    ABNT NBR 6118 (2023), Sec. 8.2.10.1 - Fig. 8.3.

    Args:
        fck (float): The characteristic compressive strength in MPa.

    Returns:
        float: The mean compressive strength in MPa.
    """
    return _fck(fck) + 8


def eps_c1(fck: float) -> float:
    """The strain at maximum compressive stress of concrete (fcm) for the
    Sargin constitutive law.

    ABNT NBR 6118 (2023), Sec. 8.2.10.1 - Fig. 8.3.

    Args:
        fck (float): The characteristic compressive strength of concrete in
            MPa.

    Returns:
        float: The strain at maximum compressive stress, absolute value, no
        unit.
    """
    return min(0.7 * fcm(fck) ** 0.31, 2.8e-3)


def eps_cu1(fck: float) -> float:
    """The ultimate strain for the Sargin constitutive law.

    ABNT NBR 6118 (2023), Sec. 8.2.10.1 - Fig. 8.3.

    Args:
        fck (float): The characteristic compressive strength of concrete in
            MPa.

    Returns:
        float: The ultimate compressive strain of concrete, absolute value,
        no unit.
    """
    fck = _fck(fck)
    return (
        eps_cu(fck) if fck <= 50
        else 2.8e-3 + 27e-3 * ((98 - fcm(fck)) / 100) ** 4
    )

def k_sargin(
    fck: float,
    agg_type: aggregate_types = 'granite',
) -> float:
    """The plasticity number k for Sargin constitutive Law.

    ABNT NBR 6118 (2023), Sec. 8.2.10.1 - Fig. 8.3.

    Args:
        fck (float): The characteristic compressive strength of concrete in
            MPa.
    Keyword Args:
        agg_type (str): Type of coarse grain aggregate used in the concrete.
            Choices are: 'basalt', 'granite', 'limestone', 'sandstone'.

    Returns:
        float: The coefficient k for nonlinear constitutive law.
    """
    return 1.05 * Eci(fck, agg_type) * eps_c1(fck) / fcm(fck)