import pytest
from movie_management.movie import Movie

def test_movie_creation():
    """Тест создания объекта Movie и доступа к атрибутам."""
    movie = Movie("Начало", "Кристофер Нолан", 2010, "Научная фантастика", 8.8)
    assert movie.title == "Начало"
    assert movie.director == "Кристофер Нолан"
    assert movie.year == 2010
    assert movie.genre == "Научная фантастика"
    assert movie.rating == 8.8

def test_movie_creation_no_rating():
    """Тест создания фильма без рейтинга."""
    movie = Movie("Дюна", "Дени Вильнёв", 2021, "Научная фантастика")
    assert movie.title == "Дюна"
    assert movie.rating is None

def test_movie_str_representation():
    """Тест строкового представления фильма."""
    movie = Movie("Начало", "Кристофер Нолан", 2010, "Научная фантастика", 8.8)
    expected_str = "'Начало' (2010) - Реж: Кристофер Нолан, Жанр: Научная фантастика, Рейтинг: 8.8"
    assert str(movie) == expected_str

    movie_no_rating = Movie("Дюна", "Дени Вильнёв", 2021, "Научная фантастика")
    expected_str_no_rating = "'Дюна' (2021) - Реж: Дени Вильнёв, Жанр: Научная фантастика"
    assert str(movie_no_rating) == expected_str_no_rating


def test_movie_repr_representation():
    """Тест repr представления фильма."""
    movie = Movie("Начало", "Кристофер Нолан", 2010, "Научная фантастика", 8.8)
    expected_repr = ("Movie(title='Начало', director='Кристофер Нолан', "
                     "year=2010, genre='Научная фантастика', rating=8.8)")
    assert repr(movie) == expected_repr

def test_movie_equality():
    """Тест сравнения фильмов."""
    movie1 = Movie("Начало", "Кристофер Нолан", 2010, "Научная фантастика", 8.8)
    movie2 = Movie("начало", "Кто-то Другой", 2010, "Боевик")
    movie3 = Movie("Темный рыцарь", "Кристофер Нолан", 2008, "Боевик", 9.0)
    
    assert movie1 == movie2
    assert movie1 != movie3
    assert movie1 != "Не объект фильма"

def test_movie_hash():
    """Тест хеширования фильмов."""
    movie1 = Movie("Начало", "Кристофер Нолан", 2010, "Научная фантастика", 8.8)
    movie2 = Movie("начало", "Кто-то Другой", 2010, "Боевик")
    
    assert hash(movie1) == hash(movie2)
    
    movie_set = {movie1, movie2}
    assert len(movie_set) == 1 

def test_movie_empty_title():
    """Тест создания фильма с пустым названием."""
    with pytest.raises(ValueError, match="Название фильма не может быть пустым."):
        Movie("", "Режиссер", 2000, "Жанр")