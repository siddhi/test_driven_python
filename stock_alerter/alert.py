class Alert:
    """Maps a Rule to an Action, and triggers the action if the rule
    matches on any stock update"""

    def __init__(self, description, rule, action):
        self.description = description
        self.rule = rule
        self.action = action

    def connect(self, exchange):
        self.exchange = exchange
        dependent_stocks = self.rule.depends_on()
        for stock in dependent_stocks:
            exchange[stock].updated.connect(self.check_rule)

    def check_rule(self, stock):
        if self.rule.matches(self.exchange):
            self.action.execute(self.description)
