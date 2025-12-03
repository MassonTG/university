class GetOrder:
    def __init__(self, repo):
        self.repo = repo

    def execute(self, order_id: str):
        return self.repo.get_by_id(order_id)
