class MaxAmountException(Exception):
    def __init__(self, amount, message="Amount requested is not in (0, 2000) range"):
        self.amount = amount
        self.message = message
        super().__init__(self.message)


class IlleagalMoneyException(Exception):
    def __init__(self, message=f'unknown bill'):
        self.message = message
        super().__init__(self.message)


class OutOfCashException(Exception):
    def __init__(self,  message="Machine remporeraly out of order"):
        self.message = message
        super().__init__(self.message)


class MaxCoinsExceededException(Exception):
    def __init__(self,  message="Machine remporeraly out of order"):
        self.message = message
        super().__init__(self.message)
