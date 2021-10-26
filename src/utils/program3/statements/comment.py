from src.utils.program3.statements.statement import Statement


class Comment(Statement):

    def __init__(self, comment_body: str):
        self.body = comment_body

    def __str__(self):
        return f"# {self.body}"

    def __repr__(self):
        return f"Comment(body=\"{self.body}\")"

    def __eq__(self, other):
        return self.body == other.body