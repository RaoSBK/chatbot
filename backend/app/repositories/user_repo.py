from sqlalchemy.orm import Session

class User_repo:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, id: int):
        return None
