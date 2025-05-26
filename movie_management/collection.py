from typing import Dict, List, Iterator, Set, Optional
from .movie import Movie
from .exceptions import (
    MovieNotFoundError,
    MovieAlreadyExistsError,
    CollectionNotFoundError,
    CollectionAlreadyExistsError
)

class MovieIterator:
    """
    Итератор для перебора фильмов в MovieCollection.
    """
    def __init__(self, movies_list: List[Movie]):
        # Сортируем фильмы по названию для единообразного порядка при переборе
        self._movies: List[Movie] = sorted(movies_list, key=lambda movie: movie.title)
        self._index: int = 0

    def __iter__(self) -> 'MovieIterator':
        """Возвращает сам объект итератора."""
        return self

    def __next__(self) -> Movie:
        """Возвращает следующий фильм в коллекции или вызывает StopIteration."""
        if self._index < len(self._movies):
            movie_to_return = self._movies[self._index]
            self._index += 1
            return movie_to_return
        else:
            raise StopIteration


class MovieCollection:
    """
    Класс для управления коллекцией фильмов.
    Хранит фильмы и позволяет выполнять различные операции с ними.
    """
    def __init__(self) -> None:
        # Основное хранилище фильмов.
        # Ключ: нормализованное название фильма.
        # Значение: объект Movie.
        self._movies: Dict[str, Movie] = {}

        self._named_collections: Dict[str, Set[str]] = {}

    def _normalize_title(self, title: str) -> str:
        """Приводит название фильма к единому формату (могут возникать коллизии, если фильмы имеют одинаковое название - Король лев(1994) и Король лев (2019))."""
        return title.strip().lower()

    def add_movie(self, movie: Movie) -> None:
        """Добавляет фильм в основную коллекцию."""
        norm_title = self._normalize_title(movie.title)
        if norm_title in self._movies:
            raise MovieAlreadyExistsError(f"Фильм '{movie.title}' уже есть в коллекции.")
        self._movies[norm_title] = movie
        print(f"Фильм '{movie.title}' добавлен.")

    def remove_movie(self, title: str) -> None:
        """
        Удаляет фильм из основной коллекции.
        Также удаляет его из всех именованных подборок, где он мог состоять.
        """
        norm_title = self._normalize_title(title)
        if norm_title not in self._movies:
            raise MovieNotFoundError(f"Фильм '{title}' не найден.")
        
        original_title = self._movies[norm_title].title
        del self._movies[norm_title]

        for collection_name in self._named_collections:
            if norm_title in self._named_collections[collection_name]:
                self._named_collections[collection_name].remove(norm_title)
        print(f"Фильм '{original_title}' удален из основной коллекции и всех подборок.")


    def get_movie(self, title: str) -> Movie:
        """Находит и возвращает фильм по его названию."""
        norm_title = self._normalize_title(title)
        if norm_title not in self._movies:
            raise MovieNotFoundError(f"Фильм '{title}' не найден.")
        return self._movies[norm_title]

    def create_named_collection(self, name: str) -> None:
        """Создает новую пустую именованную подборку."""
        if name in self._named_collections:
            raise CollectionAlreadyExistsError(f"Подборка '{name}' уже существует.")
        self._named_collections[name] = set()
        print(f"Подборка '{name}' создана.")

    def remove_named_collection(self, name: str) -> None:
        """Удаляет именованную подборку целиком."""
        if name not in self._named_collections:
            raise CollectionNotFoundError(f"Подборка '{name}' не найдена.")
        del self._named_collections[name]
        print(f"Подборка '{name}' удалена.")

    def add_movie_to_named_collection(self, movie_title: str, collection_name: str) -> None:
        """Добавляет существующий фильм в указанную именованную подборку."""
        norm_movie_title = self._normalize_title(movie_title)
        
        if norm_movie_title not in self._movies:
            raise MovieNotFoundError(f"Фильм '{movie_title}' не найден в основной коллекции.")
        if collection_name not in self._named_collections:
            raise CollectionNotFoundError(f"Подборка '{collection_name}' не найдена.")
        
        self._named_collections[collection_name].add(norm_movie_title)
        actual_movie_title = self._movies[norm_movie_title].title
        print(f"Фильм '{actual_movie_title}' добавлен в подборку '{collection_name}'.")

    def remove_movie_from_named_collection(self, movie_title: str, collection_name: str) -> None:
        """Удаляет фильм из указанной именованной подборки (но не из основной коллекции)."""
        norm_movie_title = self._normalize_title(movie_title)

        if collection_name not in self._named_collections:
            raise CollectionNotFoundError(f"Подборка '{collection_name}' не найдена.")
        
        if norm_movie_title not in self._named_collections[collection_name]:
            print(f"Фильма '{movie_title}' нет в подборке '{collection_name}'.")
            return
            
        self._named_collections[collection_name].remove(norm_movie_title)
        actual_movie_title = movie_title 
        if norm_movie_title in self._movies:
            actual_movie_title = self._movies[norm_movie_title].title
        print(f"Фильм '{actual_movie_title}' удален из подборки '{collection_name}'.")

    def get_movies_in_named_collection(self, collection_name: str) -> List[Movie]:
        """Возвращает список фильмов (объектов Movie) из указанной подборки."""
        if collection_name not in self._named_collections:
            raise CollectionNotFoundError(f"Подборка '{collection_name}' не найдена.")
        
        movie_titles_in_set = self._named_collections[collection_name]
        movies_list = []
        for title_key in movie_titles_in_set:
            if title_key in self._movies:
                movies_list.append(self._movies[title_key])
        return sorted(movies_list, key=lambda movie: movie.title)

    def search_movies(self,
                      title: Optional[str] = None,
                      director: Optional[str] = None,
                      year: Optional[int] = None,
                      genre: Optional[str] = None,
                      min_rating: Optional[float] = None) -> List[Movie]:
        """
        Ищет фильмы по заданным критериям.
        Критерии объединяются по "И" (фильм должен соответствовать всем указанным).
        Поиск по строковым полям (title, director, genre) - частичное совпадение без учета регистра.
        Поиск по году - точное совпадение.
        Поиск по min_rating - фильм должен иметь рейтинг не ниже указанного.
        """
        results: List[Movie] = []
        for movie_obj in self._movies.values():
            match = True

            if title:
                if title.lower() not in movie_obj.title.lower():
                    match = False
            if director and match:
                if director.lower() not in movie_obj.director.lower():
                    match = False
            
            if year and match:
                if movie_obj.year != year:
                    match = False
            
            if genre and match:
                if genre.lower() not in movie_obj.genre.lower():
                    match = False
            
            if min_rating and match:
                if movie_obj.rating is None or movie_obj.rating < min_rating:
                    match = False
            
            if match:
                results.append(movie_obj)
        
        return sorted(results, key=lambda movie: movie.title)


    def __iter__(self) -> MovieIterator:
        """Позволяет перебирать фильмы коллекции в цикле for."""
        return MovieIterator(list(self._movies.values()))

    def __len__(self) -> int:
        """Возвращает общее количество фильмов в основной коллекции."""
        return len(self._movies)

    def list_all_movies(self) -> List[Movie]:
        """Возвращает список всех фильмов в коллекции, отсортированных по названию."""
        return sorted(list(self._movies.values()), key=lambda movie: movie.title)

    def list_named_collections(self) -> List[str]:
        """Возвращает список названий всех именованных подборок, отсортированный по алфавиту."""
        return sorted(list(self._named_collections.keys()))