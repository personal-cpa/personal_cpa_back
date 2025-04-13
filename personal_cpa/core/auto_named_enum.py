from enum import Enum
from typing import Any


class AutoNamedEnum(Enum):
    """
    Enum 멤버의 값으로 멤버의 이름 자체를 자동으로 설정하는 커스텀 Enum 클래스입니다.

    예시:
        class Color(AutoNamedEnum):
            RED = auto()
            GREEN = auto()

        위처럼 정의하면, Color.RED.value는 "RED", Color.GREEN.value는 "GREEN"이 됩니다.

    `_generate_next_value_`는 Python Enum에서 `auto()` 사용 시 자동으로 호출되는 메서드로,
    이 메서드를 오버라이드하여 각 멤버의 값을 멤버 이름으로 설정하도록 변경합니다.
    """

    @staticmethod
    def _generate_next_value_(name: str, start: int, count: int, last_values: list[Any]) -> Any:
        """
        auto()로 Enum 멤버를 생성할 때 호출되며, 멤버 값으로 멤버의 이름(name)을 그대로 반환합니다.

        Args:
            name (str): 현재 Enum 멤버의 이름.
            start (int): auto()가 사용할 시작 값 (사용되지 않음).
            count (int): 현재까지 정의된 멤버 수 (사용되지 않음).
            last_values (list[Any]): 이전에 정의된 값들의 리스트 (사용되지 않음).

        Returns:
            Any: 멤버 이름 그대로를 값으로 반환.
        """
        return name
