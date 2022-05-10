class Repository:
    def __init__(self) -> None:
        pass

    @classmethod
    def add_assets(cls, name, data):
        setattr(cls, name, data)