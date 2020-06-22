from typing import TypeVar, Type, Dict, Any, Set

from .policy import FeldPolicy
from .feld import Feld, FeldException

TargetType: TypeVar = TypeVar('TargetType')

_INCLUDED_POLICIES: Set[FeldPolicy] = {FeldPolicy.REQUIRE, FeldPolicy.OPTIONAL}


def construct_object(target_type: Type[TargetType], d: Dict[str, Any]) -> TargetType:
	args: Dict[str, Any] = {}

	for field_name, field_value in target_type.__dict__.items():
		if isinstance(field_value, Feld):
			field_value: Feld = field_value
			policy: FeldPolicy = field_value.policies().input_policy

			if policy in _INCLUDED_POLICIES:
				try:
					parsed_value: Any = field_value.parse_input(d)
					args[field_name] = parsed_value
				except FeldException:
					if policy == FeldPolicy.REQUIRE:
						raise

	return target_type(**args)


def deconstruct_object(target: TargetType) -> Dict[str, Any]:
	rv: Dict[str, Any] = {}
	target_type: Type[TargetType] = type(target)

	for field_name, field_value in target_type.__dict__.items():
		if isinstance(field_value, Feld):
			field_value: Feld = field_value
			policy: FeldPolicy = field_value.policies().output_policy

			if policy in _INCLUDED_POLICIES:
				try:
					parsed_value: Any = field_value.parse_output(target)
					rv[field_value.field_name()] = parsed_value
				except FeldException:
					if policy == FeldPolicy.REQUIRE:
						raise

	return rv
