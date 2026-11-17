class BusinessRuleException(Exception):

    def __init__(self, message: str = 'operation not allowed') -> None:
        super().__init__(message)
