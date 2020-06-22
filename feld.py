from typing import TypeVar, Callable, Optional, Generic, Dict, Union, Any

from policy import FeldPolicies

FeldInputType: TypeVar = TypeVar('FeldInputType')
FeldParsedType: TypeVar = TypeVar('FeldParsedType')
FeldOutputType: TypeVar = TypeVar('FeldOutputType')

InputParser: TypeVar = Callable[[bool, Optional[FeldInputType]], FeldParsedType]
OutputParser: TypeVar = Callable[[bool, FeldParsedType], FeldOutputType]


class FeldException(Exception):
	_msg: str
	_cause: BaseException

	def __init__(self, msg: str, cause: BaseException):
		super().__init__(msg, cause)
		self._msg = msg
		self._cause = cause

	def __repr__(self) -> str:
		return f"{type(self).__name__}({self._msg!r}, {self._cause!r})"


class Feld(Generic[FeldInputType, FeldParsedType, FeldOutputType]):
	_field_name: str
	_input_parser: InputParser
	_output_parser: OutputParser
	_policies: FeldPolicies

	def __init__(
			self,
			field_name: str,
			input_parser: InputParser, output_parser: OutputParser,
			policies: FeldPolicies
	):
		self._field_name = field_name
		self._input_parser = input_parser
		self._output_parser = output_parser
		self._policies = policies

	def parse_input(self, d: Dict[str, Union[FeldInputType, Any]]) -> FeldParsedType:
		value: Optional[FeldInputType]
		value_present: bool
		try:
			value = d[self._field_name]
			value_present = True
		except KeyError:
			value = None
			value_present = False

		try:
			return self._input_parser(value_present, value)
		except Exception as e:
			raise FeldException(f"Field {self._field_name} rejected on input", e)

	def parse_output(self, target: object) -> FeldOutputType:
		value_present: bool = hasattr(target, self._field_name)
		value: Optional[FeldParsedType] = getattr(target, self._field_name, None)

		try:
			return self._output_parser(value_present, value)
		except Exception as e:
			raise FeldException(f"Field {self._field_name} rejected on output", e)

	def policies(self) -> FeldPolicies:
		return self._policies

	def field_name(self) -> str:
		return self._field_name
