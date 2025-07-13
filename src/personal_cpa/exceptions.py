class PersonalCPAError(Exception):
    """
    개인 CPA 애플리케이션 예외
    """


class ChartOfAccountAlreadyExistsError(PersonalCPAError):
    """
    계정과목이 이미 존재할 경우 발생하는 예외
    """
