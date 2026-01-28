"""Material properties for reinforcement steel."""

import typing as t

def fyd(fyk: float, gamma_s: float = 1.15) -> float:
    """Calculate the design value of the reinforcement yield strength.

    ABNT NBR 6118 (2023), Sec. 12.3 and 12.4.1.

    Args:
        fyk (float): The characteristic yield strength in MPa.
        gamma_s (float): The partial factor. Default value 1.15.

    Returns:
        float: The design yield strength in MPa.

    Raises:
        ValueError: If fyk is less than 0.
        ValueError: If gamma_s is less than 1.
    """
    if fyk < 0:
        raise ValueError(f'fyk={fyk} cannot be less than 0')
    if gamma_s < 1:
        raise ValueError(f'gamma_s={gamma_s} must be larger or equal to 1')
    return fyk / gamma_s