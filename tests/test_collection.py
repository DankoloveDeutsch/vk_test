import pytest
from movie_management.movie import Movie
from movie_management.collection import MovieCollection
from movie_management.exceptions import (
    MovieNotFoundError,
    MovieAlreadyExistsError,
    CollectionNotFoundError,
    CollectionAlreadyExistsError
)
#AAS
@pytest.fixture
def empty_collection() -> MovieCollection:
    return MovieCollection()

@pytest.fixture
def populated_collection() -> MovieCollection:
    collection = MovieCollection()
    collection.add_movie(Movie("Начало", "Кристофер Нолан", 2010, "Научная фантастика", 8.8))
    collection.add_movie(Movie("Темный рыцарь", "Кристофер Нолан", 2008, "Боевик", 9.0))
    collection.add_movie(Movie("Интерстеллар", "Кристофер Нолан", 2014, "Научная фантастика", 8.6))
    collection.add_movie(Movie("Криминальное чтиво", "Квентин Тарантино", 1994, "Криминал", 8.9))
    collection.add_movie(Movie("Матрица", "Вачовски", 1999, "Научная фантастика", 8.7))
    return collection

def test_add_movie(empty_collection: MovieCollection):
    """Тест добавления фильма."""
    movie = Movie("Паразиты", "Пон Джун-хо", 2019, "Триллер", 8.5)
    empty_collection.add_movie(movie)
    assert empty_collection.get_movie("Паразиты") == movie
    assert len(empty_collection) == 1

def test_add_movie_case_insensitivity(empty_collection: MovieCollection):
    """Тест добавления фильма с учетом нечувствительности к регистру."""
    movie1 = Movie("Паразиты", "Пон Джун-хо", 2019, "Триллер", 8.5)
    empty_collection.add_movie(movie1)
    assert empty_collection.get_movie("паразиты") == movie1
    assert empty_collection.get_movie(" ПАРАЗИТЫ ") == movie1

def test_add_duplicate_movie(empty_collection: MovieCollection):
    """Тест добавления дублирующего фильма."""
    movie = Movie("Паразиты", "Пон Джун-хо", 2019, "Триллер", 8.5)
    empty_collection.add_movie(movie)
    with pytest.raises(MovieAlreadyExistsError):
        empty_collection.add_movie(Movie("Паразиты", "Другой Режиссер", 2020, "Комедия"))
    with pytest.raises(MovieAlreadyExistsError):
        empty_collection.add_movie(Movie("паразиты", "Пон Джун-хо", 2019, "Триллер", 8.5))

def test_remove_movie(populated_collection: MovieCollection):
    """Тест удаления фильма."""
    initial_len = len(populated_collection)
    populated_collection.remove_movie("Начало")
    assert len(populated_collection) == initial_len - 1
    with pytest.raises(MovieNotFoundError):
        populated_collection.get_movie("Начало")

def test_remove_movie_case_insensitivity(populated_collection: MovieCollection):
    """Тест удаления фильма с учетом нечувствительности к регистру."""
    initial_len = len(populated_collection)
    populated_collection.remove_movie("начало") 
    with pytest.raises(MovieNotFoundError):
        populated_collection.get_movie("Начало")
    assert len(populated_collection) == initial_len - 1

def test_remove_non_existent_movie(empty_collection: MovieCollection):
    """Тест удаления несуществующего фильма."""
    with pytest.raises(MovieNotFoundError):
        empty_collection.remove_movie("Несуществующий Фильм")

def test_get_movie(populated_collection: MovieCollection):
    """Тест получения фильма."""
    movie = populated_collection.get_movie("Темный рыцарь")
    assert movie.director == "Кристофер Нолан"
    assert movie.year == 2008

def test_get_non_existent_movie(empty_collection: MovieCollection):
    """Тест получения несуществующего фильма."""
    with pytest.raises(MovieNotFoundError):
        empty_collection.get_movie("Несуществующий Фильм")

def test_collection_iteration(populated_collection: MovieCollection):
    """Тест итерации по коллекции."""
    titles = [movie.title for movie in populated_collection]
    expected_titles = sorted([
        "Начало", "Темный рыцарь", "Интерстеллар", 
        "Криминальное чтиво", "Матрица"
    ])
    assert titles == expected_titles
    assert len(titles) == 5 

def test_collection_len(populated_collection: MovieCollection, empty_collection: MovieCollection):
    """Тест получения длины коллекции."""
    assert len(populated_collection) == 5
    assert len(empty_collection) == 0

def test_list_all_movies(populated_collection: MovieCollection):
    """Тест получения списка всех фильмов."""
    all_movies = populated_collection.list_all_movies()
    assert len(all_movies) == 5
    assert all_movies[0].title == "Начало"

def test_search_movies_by_director(populated_collection: MovieCollection):
    """Тест поиска фильмов по режиссеру."""
    results = populated_collection.search_movies(director="Кристофер Нолан")
    assert len(results) == 3
    assert all(movie.director == "Кристофер Нолан" for movie in results)
    
    results_partial = populated_collection.search_movies(director="нолан") # Частичное совпадение, регистр
    assert len(results_partial) == 3

def test_search_movies_by_title(populated_collection: MovieCollection):
    """Тест поиска фильмов по названию."""
    results = populated_collection.search_movies(title="Матрица")
    assert len(results) == 1
    assert results[0].title == "Матрица"

    results_partial = populated_collection.search_movies(title="емный рыц")
    assert len(results_partial) == 1
    assert results_partial[0].title == "Темный рыцарь"

def test_search_movies_by_year(populated_collection: MovieCollection):
    """Тест поиска фильмов по году выпуска."""
    results = populated_collection.search_movies(year=2010)
    assert len(results) == 1
    assert results[0].title == "Начало"

def test_search_movies_by_genre(populated_collection: MovieCollection):
    """Тест поиска фильмов по жанру."""
    results = populated_collection.search_movies(genre="Научная фантастика")
    # Начало, Интерстеллар, Матрица
    assert len(results) == 3 
    titles = sorted([m.title for m in results])
    assert titles == ["Интерстеллар", "Матрица", "Начало"]
    
    results_partial = populated_collection.search_movies(genre="научная фант") # Частичное совпадение
    assert len(results_partial) == 3

def test_search_movies_by_min_rating(populated_collection: MovieCollection):
    """Тест поиска фильмов по минимальному рейтингу."""
    populated_collection.add_movie(Movie("Довод", "Кристофер Нолан", 2020, "Научная фантастика")) # Фильм без рейтинга
    
    results = populated_collection.search_movies(min_rating=8.8) 
    # Начало (8.8), Темный рыцарь (9.0), Криминальное чтиво (8.9)
    assert len(results) == 3
    titles = sorted([m.title for m in results])
    assert titles == ["Криминальное чтиво", "Начало", "Темный рыцарь"]

    results_higher = populated_collection.search_movies(min_rating=9.0)
    assert len(results_higher) == 1
    assert results_higher[0].title == "Темный рыцарь"
    
    results_no_match = populated_collection.search_movies(min_rating=9.5)
    assert len(results_no_match) == 0
    
    results_with_none = populated_collection.search_movies(min_rating=7.0)
    assert "Довод" not in [m.title for m in results_with_none]


def test_search_movies_multiple_criteria(populated_collection: MovieCollection):
    """Тест поиска фильмов по нескольким критериям."""
    results = populated_collection.search_movies(director="Нолан", genre="Научная фантастика")
    assert len(results) == 2 
    titles = sorted([m.title for m in results])
    assert titles == ["Интерстеллар", "Начало"]

    results_specific = populated_collection.search_movies(director="Нолан", year=2010, genre="Научн", min_rating=8.0)
    assert len(results_specific) == 1
    assert results_specific[0].title == "Начало"

def test_search_movies_no_results(populated_collection: MovieCollection):
    """Тест поиска фильмов без результатов."""
    results = populated_collection.search_movies(director="Стивен Спилберг")
    assert len(results) == 0
    results_2 = populated_collection.search_movies(year=1000)
    assert len(results_2) == 0
    results_3 = populated_collection.search_movies(title="НесуществующийФильм", director="Любой")
    assert len(results_3) == 0

def test_create_named_collection(empty_collection: MovieCollection):
    """Тест создания именованной коллекции."""
    empty_collection.create_named_collection("Мои любимые")
    assert "Мои любимые" in empty_collection.list_named_collections()
    with pytest.raises(CollectionAlreadyExistsError):
        empty_collection.create_named_collection("Мои любимые")

def test_remove_named_collection(empty_collection: MovieCollection):
    """Тест удаления именованной коллекции."""
    empty_collection.create_named_collection("Посмотреть")
    empty_collection.remove_named_collection("Посмотреть")
    assert "Посмотреть" not in empty_collection.list_named_collections()
    with pytest.raises(CollectionNotFoundError):
        empty_collection.remove_named_collection("Несуществующая")

def test_add_movie_to_named_collection(populated_collection: MovieCollection):
    """Тест добавления фильма в именованную коллекцию."""
    populated_collection.create_named_collection("Лучшее от Нолана")
    # Используем фильмы, которые точно есть в populated_collection
    inception_title = "Начало"
    dk_title = "Темный рыцарь"

    populated_collection.add_movie_to_named_collection(inception_title, "Лучшее от Нолана")
    populated_collection.add_movie_to_named_collection(dk_title.lower() + " ", "Лучшее от Нолана") # Проверка нормализации

    movies_in_coll = populated_collection.get_movies_in_named_collection("Лучшее от Нолана")
    assert len(movies_in_coll) == 2
    titles = sorted([m.title for m in movies_in_coll])
    assert inception_title in titles
    assert dk_title in titles

    with pytest.raises(MovieNotFoundError):
        populated_collection.add_movie_to_named_collection("Несуществующий Фильм", "Лучшее от Нолана")
    with pytest.raises(CollectionNotFoundError):
        populated_collection.add_movie_to_named_collection(inception_title, "Несуществующая Коллекция")

def test_remove_movie_from_named_collection(populated_collection: MovieCollection):
    """Тест удаления фильма из именованной коллекции."""
    sci_fi_coll = "Научная фантастика: Классика"
    inception_title = "Начало"
    interstellar_title = "Интерстеллар"
    
    populated_collection.create_named_collection(sci_fi_coll)
    populated_collection.add_movie_to_named_collection(inception_title, sci_fi_coll)
    populated_collection.add_movie_to_named_collection(interstellar_title, sci_fi_coll)
    
    populated_collection.remove_movie_from_named_collection(inception_title, sci_fi_coll)
    movies_in_coll = populated_collection.get_movies_in_named_collection(sci_fi_coll)
    assert len(movies_in_coll) == 1
    assert movies_in_coll[0].title == interstellar_title

    pulp_fiction_title = "Криминальное чтиво"
    populated_collection.remove_movie_from_named_collection(pulp_fiction_title, sci_fi_coll)
    movies_in_coll_after = populated_collection.get_movies_in_named_collection(sci_fi_coll)
    assert len(movies_in_coll_after) == 1

    with pytest.raises(CollectionNotFoundError):
        populated_collection.remove_movie_from_named_collection(interstellar_title, "Несуществующая Коллекция")

def test_get_movies_in_named_collection(populated_collection: MovieCollection):
    """Тест получения фильмов из именованной коллекции."""
    test_coll_name = "Тестовая коллекция"
    pulp_fiction_movie = populated_collection.get_movie("Криминальное чтиво") # Получаем существующий фильм
    
    populated_collection.create_named_collection(test_coll_name)
    populated_collection.add_movie_to_named_collection(pulp_fiction_movie.title, test_coll_name)
    
    retrieved_movies = populated_collection.get_movies_in_named_collection(test_coll_name)
    assert len(retrieved_movies) == 1
    assert retrieved_movies[0].title == pulp_fiction_movie.title 

    with pytest.raises(CollectionNotFoundError):
        populated_collection.get_movies_in_named_collection("Несуществующая")

def test_remove_movie_also_removes_from_named_collections(populated_collection: MovieCollection):
    """Тест удаления фильма из всех именованных коллекций."""
    nolan_fans_coll = "Фанаты Нолана"
    scifi_hits_coll = "Хиты научной фантастики"
    inception_title = "Начало"
    interstellar_title = "Интерстеллар"

    populated_collection.create_named_collection(nolan_fans_coll)
    populated_collection.create_named_collection(scifi_hits_coll)

    populated_collection.add_movie_to_named_collection(inception_title, nolan_fans_coll)
    populated_collection.add_movie_to_named_collection(inception_title, scifi_hits_coll)
    populated_collection.add_movie_to_named_collection(interstellar_title, nolan_fans_coll)
    populated_collection.add_movie_to_named_collection(interstellar_title, scifi_hits_coll)

    assert len(populated_collection.get_movies_in_named_collection(nolan_fans_coll)) == 2
    assert len(populated_collection.get_movies_in_named_collection(scifi_hits_coll)) == 2
    
    populated_collection.remove_movie(inception_title) # Удаляем из основной коллекции
    
    nolan_movies = populated_collection.get_movies_in_named_collection(nolan_fans_coll)
    scifi_movies = populated_collection.get_movies_in_named_collection(scifi_hits_coll)
    
    assert len(nolan_movies) == 1
    assert nolan_movies[0].title == interstellar_title
    
    assert len(scifi_movies) == 1
    assert scifi_movies[0].title == interstellar_title

    with pytest.raises(MovieNotFoundError):
        populated_collection.get_movie(inception_title)