from enum import auto

from personal_cpa.core.auto_named_enum import AutoNamedEnum


class AccountType(AutoNamedEnum):
    """
    복식부기 회계 시스템에서 사용되는 계정의 기본 유형(Enum)입니다.

    각 항목은 계정의 '성격'을 구분하는 데 사용되며,
    Enum 멤버의 값은 이름 자체를 그대로 사용합니다
    (예: AccountType.ASSET.value == "ASSET").

    ✅ 사용 예:
        - 계정 생성 시 유형을 이 Enum으로 지정
        - 대차대조표(BS), 손익계산서(PL) 등의 보고서 작성 시 분류 기준

    -------------------------
    계정 유형 및 예시 계정:
    -------------------------
    - ASSET (자산): 현금, 예금, 주식, 부동산 등 개인이 보유한 가치 있는 항목
        현금, 보통예금, 증권계좌, 코인지갑, 부동산, 차량, 선급금 등

    - LIABILITY (부채): 대출, 미지급금 등 미래에 상환해야 할 금전적 의무
        신용카드, 마이너스통장, 학자금대출, 전세보증금, 미지급세금 등

    - EQUITY (자본): 자산에서 부채를 뺀 순자산, 혹은 자기자본
        자기자본, 자본금, 순이익 누계, 인출금, 유보이익 등

    - REVENUE (수익): 배당금, 이자수익, 급여 등 유입되는 수익 항목
        급여, 배당수익, 이자수익, 임대료, 주식매각차익, 코인매매이익 등

    - EXPENSE (비용): 생활비, 수수료, 세금 등 자산 유출에 해당하는 항목
        식비, 교통비, 통신비, 보험료, 수수료, 세금, 대출이자, 생활비 등
    """

    ASSET = auto()
    LIABILITY = auto()
    EQUITY = auto()
    REVENUE = auto()
    EXPENSE = auto()
