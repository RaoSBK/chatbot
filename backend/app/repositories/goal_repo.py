from sqlalchemy.orm import Session

class Goal_repo:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, id: int):
        return None
