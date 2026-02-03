"""Tests for the _concrete_material_properties module."""

import math

import numpy as np
import pytest

from structuralcodes.codes.nbr6118 import _concrete_material_properties


@pytest.mark.parametrize(
    'test_input, expect',
    [(20, 28), (35, 43), (55, 63), (90, 98)],
)
def test_fcm(test_input, expect):
    """Test the fcm function."""
    assert math.isclose(_concrete_material_properties.fcm(test_input), expect)


@pytest.mark.parametrize(
    'test_input, expected',
    [
        (20, 2.21),
        (25, 2.56),
        (30, 2.90),
        (35, 3.21),
        (40, 3.51),
        (45, 3.80),
        (50, 4.07),
        (55, 4.21),
        (60, 4.35),
        (70, 4.61),
        (80, 4.84),
        (90, 5.04),
    ],
)
def test_fctm(test_input, expected):
    """Test the fctm function."""
    assert math.isclose(
        _concrete_material_properties.fctm(test_input), expected, rel_tol=0.02
    )


@pytest.mark.parametrize(
    'test_input, expected',
    [
        (20, 1.55),
        (25, 1.79),
        (30, 2.03),
        (35, 2.25),
        (40, 2.46),
        (45, 2.66),
        (50, 2.85),
        (55, 2.95),
        (60, 3.04),
        (70, 3.23),
        (80, 3.39),
        (90, 3.53)
    ],
)
def test_fctkinf(test_input, expected):
    """Test the fctkinf function."""
    assert math.isclose(
        _concrete_material_properties.fctkinf(
            _concrete_material_properties.fctm(test_input)
        ),
        expected,
        rel_tol=0.031,
    )


@pytest.mark.parametrize(
    'test_input, expected',
    [
        (20, 2.87),
        (25, 3.33),
        (30, 3.77),
        (35, 4.17),
        (40, 4.56),
        (45, 4.94),
        (50, 5.29),
        (55, 5.47),
        (60, 5.65),
        (70, 5.99),
        (80, 6.29),
        (90, 6.55)
    ],
)
def test_fctksup(test_input, expected):
    """Test the fctksup function."""
    assert math.isclose(
        _concrete_material_properties.fctksup(
            _concrete_material_properties.fctm(test_input)
        ),
        expected,
        rel_tol=0.028,
    )


@pytest.mark.parametrize(
    '_fcm, agg_type, expected',
    [
        (20, 'granite', 25043.96),
        (40, 'granite', 35417.51),
        (70, 'granite', 43443.33),
        (20, 'basalt', 30052.75),
        (20, 'Limestone', 22539.565),
        (20, 'SANDSTONE', 17530.77),
    ],
)
def test_Eci(_fcm, agg_type, expected):
    """Test Eci function."""
    assert np.isclose(
        _concrete_material_properties.Eci(_fcm, agg_type),
        expected,
        rtol=1e-5,
    )


@pytest.mark.parametrize(
    'time, cem_class, expected',
    [
        (10, 'CPIV', 0.77425),
        (10, 'cpii', 0.84507),
        (10, 'cpv', 0.87401),
        (
            np.array([10, 20, 40]),
            'CPii',
            np.array([0.845075 , 0.95523, 1.04168]),
        ),
    ],
)
def test_beta_1(time, cem_class, expected):
    """Test beta_cc function."""
    assert np.isclose(
        _concrete_material_properties.beta_1(time, cem_class),
        expected,
        rtol=1e-5,
    ).all()  # all() is required to test numpy array.



@pytest.mark.parametrize(
    'fck, gamma_c, expected',
    [
        (35, 1.4, 25),
        (45, 1.4, 32.14),
        (90, 1.4, 64.29),
    ],
)
def test_fcd(fck, gamma_c, expected):
    """Test fcd function."""
    assert math.isclose(
        _concrete_material_properties.fcd(fck, gamma_c),
        expected,
        rel_tol=10e-5,
    )


@pytest.mark.parametrize(
    'fck, expected',
    [
        (20, 1.966604e-3),
        (35, 2.24633e-3),
        (50, 2.46468e-3),
        (60, 2.58926e-3),
        (80, 2.8e-3),
        (90, 2.8e-3),
    ],
)
def test_eps_c1(fck, expected):
    """Test eps_c1 function."""
    assert math.isclose(
        _concrete_material_properties.eps_c1(fck), expected, rel_tol=1e-6
    )


@pytest.mark.parametrize(
    'test_input, expect',
    [
        (20, 3.5e-3),
        (35, 3.5e-3),
        (50, 3.5e-3),
        (60, 3.0187e-3),
        (80, 2.8027e-3),
        (90, 2.8e-3),
    ],
)
def test_eps_cu1(test_input, expect):
    """Test the eps_cu1 function."""
    assert math.isclose(
        _concrete_material_properties.eps_cu1(test_input),
        expect,
        rel_tol=1e-6,
    )


@pytest.mark.parametrize(
    'test_input, expect',
    [
        (20, 2.0e-3),
        (35, 2.0e-3),
        (50, 2.0e-3),
        (60, 2.29e-3),
        (70, 2.42e-3),
        (80, 2.52e-3),
        (90, 2.6e-3),
    ],
)
def test_eps_c2(test_input, expect):
    """Test the eps_c2 function."""
    assert math.isclose(
        _concrete_material_properties.eps_c2(test_input),
        expect,
        rel_tol=1e-2,
    )


@pytest.mark.parametrize(
    'test_input, expect',
    [
        (20, 3.5e-3),
        (35, 3.5e-3),
        (50, 3.5e-3),
        (60, 2.88e-3),
        (70, 2.66e-3),
        (80, 2.6e-3),
        (90, 2.6e-3),
    ],
)
def test_eps_cu(test_input, expect):
    """Test the eps_cu2 function."""
    assert math.isclose(
        _concrete_material_properties.eps_cu(test_input),
        expect,
        rel_tol=4e-2,
    )


# With 100 1.3 -> not working because table is 1.3 but equation gives 1.4
@pytest.mark.parametrize(
    'test_input, expect',
    [
        (20, 2.0),
        (35, 2.0),
        (50, 2.0),
        (60, 1.589),
        (70, 1.437),
        (80, 1.402),
        (90, 1.4),
    ],
)
def test_n(test_input, expect):
    """Test the n function."""
    assert math.isclose(
        _concrete_material_properties.n_parabolic_rectangular(test_input),
        expect,
        rel_tol=9e-3,
    )