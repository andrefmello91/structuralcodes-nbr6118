"""The concrete class for Model Code 2010 Reinforcement Material."""

import typing as t

from ...codes import nbr6118

from ..constitutive_laws import ConstitutiveLaw, create_constitutive_law
from ._reinforcement import Reinforcement


class ReinforcementNBR6118(Reinforcement):
    """Reinforcement implementation for ABNT NBR 6118 (2023)."""

    def __init__(
        self,
        fyk: float,
        Es: t.Optional[float] = 210e3,
        epsuk: float = 10e-3,
        gamma_s: t.Optional[float] = 1.15,
        name: t.Optional[str] = None,
        density: float = 7850.0,
        constitutive_law: t.Optional[
            t.Union[
                t.Literal[
                    'elastic',
                    'elasticperfectlyplastic',
                    'elasticplastic',
                ],
                ConstitutiveLaw,
            ]
        ] = 'elasticperfectlyplastic',
        initial_strain: t.Optional[float] = None,
        initial_stress: t.Optional[float] = None,
        strain_compatibility: t.Optional[bool] = None,
    ):
        """Initializes a new instance of Reinforcement for MC2010.

        Args:
            fyk (float): Characteristic yield strength in MPa.
            Es (Optional(float)): The Young's modulus in MPa. Default value is
                210000 MPa.
            epsuk (float): The characteristik strain at the ultimate stress
                level. Default value is 10e-3.
            gamma_s (Optional(float)): The partial factor for reinforcement.
                Default value is 1.15.

        Keyword Args:
            name (str): A descriptive name for the reinforcement.
            density (float): Density of material in kg/m3 (default: 7850).
            constitutive_law (ConstitutiveLaw | str): A valid ConstitutiveLaw
                object for reinforcement or a string defining a valid
                constitutive law type for reinforcement. (valid options for
                string: 'elastic', 'elasticplastic', or
                'elasticperfectlyplastic').
            initial_strain (Optional[float]): Initial strain of the material.
            initial_stress (Optional[float]): Initial stress of the material.
            strain_compatibility (Optional[bool]): Only relevant if
                initial_strain or initial_stress are different from zero. If
                True, the material deforms with the geometry. If False, the
                stress in the material upon loading is kept constant
                corresponding to the initial strain.

        Raises:
            ValueError: If the constitutive law name is not available for the
                material.
            ValueError: If the provided constitutive law is not valid for
                reinforcement.
        """
        if name is None:
            name = f'Reinforcement{round(fyk):d}'

        super().__init__(
            fyk=fyk,
            Es=Es,
            name=name,
            density=density,
            ftk=fyk,
            epsuk=epsuk,
            gamma_s=gamma_s,
            initial_strain=initial_strain,
            initial_stress=initial_stress,
            strain_compatibility=strain_compatibility,
        )
        self._gamma_eps = gamma_eps
        self._constitutive_law = (
            constitutive_law
            if isinstance(constitutive_law, ConstitutiveLaw)
            else create_constitutive_law(
                constitutive_law_name=constitutive_law, material=self
            )
        )
        if 'steel' not in self._constitutive_law.__materials__:
            raise ValueError(
                'The provided constitutive law is not valid for reinforcement.'
            )
        self._apply_initial_strain()

    def fyd(self) -> float:
        """The design yield strength."""
        return nbr6118.fyd(self.fyk, self.gamma_s)

    @property
    def gamma_s(self) -> float:
        """The partial factor for reinforcement."""
        return self._gamma_s or 1.15

    def ftd(self) -> float:
        """The design ultimate strength."""
        return self.fyd()

    def epsud(self) -> float:
        """The design ultimate strain."""
        return self._epsuk

    def __elastic__(self) -> dict:
        """Returns kwargs for creating an elastic constitutive law."""
        return {'E': self.Es}

    def __elasticperfectlyplastic__(self) -> dict:
        """Returns kwargs for ElasticPlastic constitutive law with no strain
        hardening.
        """
        return {
            'E': self.Es,
            'fy': self.fyd(),
            'eps_su': self.epsud(),
        }

    def __elasticplastic__(self) -> dict:
        """Returns kwargs for ElasticPlastic constitutive law with strain
        hardening.
        """
        raise NotImplementedError(
            'ElasticPlastic constitutive law with strain hardening is not '
            'implemented in ABNT NBR6118.'
        )
