class MovieNotFoundError(Exception):
    """Исключение, когда фильм не найден."""
    pass

class MovieAlreadyExistsError(Exception):
    """Исключение, когда фильм уже существует в коллекции."""
    pass

class CollectionNotFoundError(Exception):
    """Исключение, когда именованная коллекция не найдена."""
    pass

class CollectionAlreadyExistsError(Exception):
    """Исключение, когда именованная коллекция уже существует."""
    pass