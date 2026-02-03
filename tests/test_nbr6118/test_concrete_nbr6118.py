"""Tests for the concrete nbr6118."""

import math

import pytest

from structuralcodes.codes import nbr6118
from structuralcodes.materials.concrete import ConcreteNBR6118, create_concrete

# Series of tests using the factory function


@pytest.mark.parametrize(
    'design_code_to_set',
    ['nbr6118', 'NBR6118', 'Nbr6118'],
)
@pytest.mark.parametrize(
    'fck, expected_name',
    [(20, 'C20'), (25, 'C25'), (30, 'C30'), (35, 'C35'), (40, 'C40')],
)
def test_create_concrete(design_code_to_set, fck, expected_name):
    """Test creating a concrete with nbr6118."""
    # Arrange
    expected_density = 2400

    # Act
    c = create_concrete(fck=fck, design_code=design_code_to_set)

    # Assert
    assert isinstance(c, ConcreteNBR6118)
    assert c.name == expected_name
    assert c.density == expected_density


def test_create_concrete_wrong_code():
    """Test if a ValueError exception raises when passing the wrong code."""
    with pytest.raises(ValueError):
        create_concrete(fck=25, design_code='EN1995')


@pytest.mark.parametrize(
    'fck, fcm',
    [(20, 28), (35, 43), (55, 63), (90, 98)],
)
def test_update_attributes(fck, fcm):
    """Test update_attributes function."""
    c = ConcreteNBR6118(fck=fck, fcm=fcm)

    assert c.fcm is not None
    assert c.fcm == fcm


# Series of tests using ConcreteNBR6118 class


fck_parametrized = pytest.mark.parametrize('fck', [20, 25, 30, 35, 40])


@fck_parametrized
def test_fck_getter(fck):
    """Test fck getter."""
    c = ConcreteNBR6118(fck)

    assert c.fck == fck


@fck_parametrized
def test_fck_setter(fck):
    """Test fck setter."""
    c = ConcreteNBR6118(fck=fck + 5)

    assert c.fck == fck + 5


def test_properties_initialized_to_none():
    """Test if a ConcreteNBR6118 when created has the attributes set to None."""
    c = ConcreteNBR6118(fck=25)

    assert c._fcm is None
    assert c._fctm is None
    assert c._fctkinf is None
    assert c._fctksup is None
    assert c._Eci is None
    assert c._eps_c1 is None
    assert c._eps_cu1 is None
    assert c._k_sargin is None
    assert c._eps_c2 is None
    assert c._eps_cu is None
    assert c._n_parabolic_rectangular is None


fcm_parametrized = pytest.mark.parametrize(
    'test_input, expected',
    [(20, 28), (35, 43), (55, 63), (90, 98)],
)


@fcm_parametrized
def test_fcm_getter(test_input, expected):
    """Test the fcm getter."""
    c = ConcreteNBR6118(fck=test_input)
    assert math.isclose(c.fcm, expected)


@fcm_parametrized
def test_fcm_specified(test_input, expected):
    """Test specifying fcm."""
    c = ConcreteNBR6118(fck=test_input, fcm=expected)

    assert math.isclose(c.fcm, expected)


@pytest.mark.parametrize(
    'test_input',
    [20, 35, 55, 90],
)
def test_specify_fcm_exception(test_input):
    """Test specifying an invalid fcm."""
    with pytest.raises(ValueError):
        ConcreteNBR6118(fck=test_input, fcm=test_input - 1)


def test_Eci_getter():
    """Test the getter for Eci."""
    fck = 45
    fcm = nbr6118.fcm(fck=fck)
    expected = nbr6118.Eci(fck=fcm)
    assert ConcreteNBR6118(fck=fck).Eci == expected


def test_Eci_specified():
    """Test specifying a value for Eci."""
    fck = 45
    excepted = 30000
    assert ConcreteNBR6118(fck=fck, Eci=excepted).Eci == excepted


@pytest.mark.parametrize('Eci', (0.5e4, 2e5))
def test_Eci_specified_warning(Eci):
    """Test specifying Eci with a wrong value."""
    with pytest.warns(UserWarning):
        ConcreteNBR6118(fck=45, Eci=Eci)


fctm_parmetrized = pytest.mark.parametrize(
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


@fctm_parmetrized
def test_fctm_getter(test_input, expected):
    """Test the fctm getter function."""
    c = ConcreteNBR6118(fck=test_input)
    assert math.isclose(c.fctm, expected, rel_tol=0.02)


@fctm_parmetrized
def test_fctm_specified(test_input, expected):
    """Test specifying fctm."""
    c = ConcreteNBR6118(fck=test_input, fctm=expected)

    assert math.isclose(c.fctm, expected)


@pytest.mark.parametrize('test_input', [20, 25, 30, 35, 40, 45])
def test_specifying_fctm_warning(test_input):
    """Test specifying fctm . Check that a warning is raised when trying to set
    a value higher than 0.5 times fck.
    """
    with pytest.warns(UserWarning):
        ConcreteNBR6118(fck=test_input, fctm=test_input * 0.5 + 1)


fctkmin_parametrized = pytest.mark.parametrize(
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


@fctkmin_parametrized
def test_fctkmin_getter(test_input, expected):
    """Test the fctkmin getter function."""
    c = ConcreteNBR6118(fck=test_input)
    assert math.isclose(c.fctkmin, expected, rel_tol=0.031)


@fctkmin_parametrized
def test_fctkmin_specified(test_input, expected):
    """Test specifying fctkmin."""
    c = ConcreteNBR6118(fck=test_input, fctkmin=expected)

    assert math.isclose(c.fctkmin, expected)


fctkmax_parmetrized = pytest.mark.parametrize(
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


@fctkmax_parmetrized
def test_fctkmax_getter(test_input, expected):
    """Test the fctkmax getter function."""
    c = ConcreteNBR6118(fck=test_input)
    assert math.isclose(c.fctkmax, expected, rel_tol=0.028)


@fctkmax_parmetrized
def test_fctkmax_specified(test_input, expected):
    """Test specifying fctkmax."""
    c = ConcreteNBR6118(fck=test_input, fctkmax=expected)

    assert math.isclose(c.fctkmax, expected)


def test_gamma_c():
    """Test the gamma_c property."""
    # Arrange
    concrete = ConcreteNBR6118(45)

    # Assert
    assert math.isclose(concrete.gamma_c, 1.4)


@pytest.mark.parametrize(
    'fck, expected',
    [
        (35, 25),
        (45, 32.14),
        (90, 64.29),
    ],
)
def test_fcd(fck, expected):
    """Test calculating the design compressive strength."""
    # Arrange
    concrete = ConcreteNBR6118(fck)

    # Act
    fcd = concrete.fcd()

    # Assert
    assert math.isclose(fcd, expected, rel_tol=10e-5)


@fck_parametrized
def test_eps_c1_getter(fck):
    """Test eps_c1 getter."""
    c = ConcreteNBR6118(fck=fck)
    expected = nbr6118.eps_c1(fck=fck)
    assert math.isclose(c.eps_c1, expected, rel_tol=1e-6)


eps_c1_parametrized = pytest.mark.parametrize(
    'test_input, expected',
    [
        (20, 1.966604e-3),
        (35, 2.24633e-3),
        (50, 2.46468e-3),
        (60, 2.58926e-3),
        (80, 2.8e-3),
        (90, 2.8e-3),
    ],
)


@eps_c1_parametrized
def test_eps_c1_specified(test_input, expected):
    """Test specifying eps_c1."""
    c = ConcreteNBR6118(fck=test_input, eps_c1=expected)

    assert math.isclose(c.eps_c1, expected)


@fck_parametrized
def test_eps_cu1_getter(fck):
    """Test eps_cu1 getter."""
    c = ConcreteNBR6118(fck=fck)
    expected = nbr6118.eps_cu1(fck=fck)
    assert math.isclose(c.eps_cu1, expected, rel_tol=1e-6)


eps_cu1_parametrized = pytest.mark.parametrize(
    'test_input, expected',
    [
        (20, 3.5e-3),
        (35, 3.5e-3),
        (50, 3.5e-3),
        (60, 3.0187e-3),
        (80, 2.8027e-3),
        (90, 2.8e-3),
    ],
)


@eps_cu1_parametrized
def test_eps_cu1_specified(test_input, expected):
    """Test specifying eps_cu1."""
    c = ConcreteNBR6118(fck=test_input, eps_cu1=expected)

    assert math.isclose(c.eps_cu1, expected)


@fck_parametrized
def test_k_getter(fck):
    """Test k getter."""
    c = ConcreteNBR6118(fck=fck)
    expected = nbr6118.k_sargin(fck=fck)
    assert math.isclose(c.k_sargin, expected, rel_tol=1e-6)


def test_k_specified_warning():
    """Test specifying k_sargin with a wrong value."""
    with pytest.raises(ValueError):
        ConcreteNBR6118(fck=45, k_sargin=-1.0)


@fck_parametrized
def test_eps_c2_getter(fck):
    """Test eps_c2 getter."""
    c = ConcreteNBR6118(fck=fck)
    expected = nbr6118.eps_c2(fck=fck)
    assert math.isclose(c.eps_c2, expected, rel_tol=1e-6)


eps_c2_parametrized = pytest.mark.parametrize(
    'test_input, expected',
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


@eps_c2_parametrized
def test_eps_c2_specified(test_input, expected):
    """Test specifying eps_c2."""
    c = ConcreteNBR6118(fck=test_input, eps_c2=expected)

    assert math.isclose(c.eps_c2, expected)


@fck_parametrized
def test_eps_cu_getter(fck):
    """Test eps_cu getter."""
    c = ConcreteNBR6118(fck=fck)
    expected = nbr6118.eps_cu(fck=fck)
    assert math.isclose(c.eps_cu, expected, rel_tol=1e-6)


eps_cu_parametrized = pytest.mark.parametrize(
    'test_input, expected',
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


@eps_cu_parametrized
def test_eps_cu_specified(test_input, expected):
    """Test specifying eps_cu."""
    c = ConcreteNBR6118(fck=test_input, eps_cu=expected)

    assert math.isclose(c.eps_cu, expected)


@fck_parametrized
def test_n_getter(fck):
    """Test n getter."""
    c = ConcreteNBR6118(fck=fck)
    expected = nbr6118.n_parabolic_rectangular(fck=fck)
    assert math.isclose(c.n_parabolic_rectangular, expected, rel_tol=1e-6)


n_parametrized = pytest.mark.parametrize(
    'test_input, expected',
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


@n_parametrized
def test_n_specified(test_input, expected):
    """Test specifying n_parabolic_rettangular."""
    c = ConcreteNBR6118(fck=test_input, n_parabolic_rectangular=expected)

    assert math.isclose(c.n_parabolic_rectangular, expected)


def test_n_specified_error():
    """Test specifying n_parabolic_rectangular with a wrong value."""
    with pytest.raises(ValueError):
        ConcreteNBR6118(fck=45, n_parabolic_rectangular=-1)


def test_n_specified_warning():
    """Test specifying n_parabolic_rectangular with a wrong value."""
    with pytest.warns(UserWarning):
        ConcreteNBR6118(fck=45, n_parabolic_rectangular=6)