from dataclasses import dataclass
from enum import Enum
from typing import Set


class FeldPolicy(Enum):
	REQUIRE = 'REQUIRE'  # Field is required, field if rejected
	OPTIONAL = 'OPTIONAL'  # Field is optional, ignore if rejected
	IGNORE = 'IGNORE'  # Field if excluded, always ignore


@dataclass
class FeldPolicies:
	input_policy: FeldPolicy
	output_policy: FeldPolicy

	@classmethod
	def default_policies(cls) -> 'FeldPolicies':
		return cls(FeldPolicy.REQUIRE, FeldPolicy.REQUIRE)
