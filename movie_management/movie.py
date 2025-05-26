from typing import Optional

class Movie:
    """
    Класс для представления одного фильма.
    Содержит информацию о названии, режиссере, годе выпуска, жанре и рейтинге.
    """
    def __init__(self, title: str, director: str, year: int, genre: str, rating: Optional[float] = None):
        if not title: 
            raise ValueError("Название фильма не может быть пустым.")
        self.title: str = title
        self.director: str = director
        self.year: int = year
        self.genre: str = genre
        self.rating: Optional[float] = rating

    def __str__(self) -> str:
        """Возвращает строковое представление фильма для пользователя."""
        rating_str = f", Рейтинг: {self.rating}" if self.rating is not None else ""
        return f"'{self.title}' ({self.year}) - Реж: {self.director}, Жанр: {self.genre}{rating_str}"

    def __repr__(self) -> str:
        """Возвращает строковое представление, удобное для отладки."""
        return (f"Movie(title='{self.title}', director='{self.director}', "
                f"year={self.year}, genre='{self.genre}', rating={self.rating})")

    def __eq__(self, other: object) -> bool:
        """
        Сравнивает два фильма. Фильмы считаются равными, если их названия совпадают
        (без учета регистра). Это полезно, чтобы не добавлять "один и тот же" фильм
        с разным регистром в названии как два разных.
        """
        if not isinstance(other, Movie):
            return NotImplemented # Не сравниваем с объектами других типов
        return self.title.lower() == other.title.lower()

    def __hash__(self) -> int:
        """
        Возвращает хеш фильма, основанный на названии.
        """
        return hash(self.title.lower())