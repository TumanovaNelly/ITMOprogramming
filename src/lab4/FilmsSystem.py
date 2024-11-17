from math import isclose
from typing import Dict, List, Set


class Film:
    def __init__(self, name: str) -> None:
        self.__name: str = name
        self.__views: int = 0

    @property
    def name(self) -> str:
        return self.__name

    @property
    def views(self) -> int:
        return self.__views

    @views.setter
    def views(self, value: int) -> None:
        self.__views = value

    def __str__(self) -> str:
        return f'Film "{self.__name}" has been viewed {self.__views} times'


class FilmBase:
    def __init__(self) -> None:
        self.__film_base: Dict[int, Film] = dict()

    def get_film(self, identifier: int) -> Film:
        if identifier not in self.__film_base:
            raise ValueError(f'Film with ID:{identifier} does not exist')

        return self.__film_base[identifier]

    def add_film(self, identifier: int, film: Film) -> None:
        if identifier in self.__film_base:
            raise ValueError(f'Film with ID:{identifier} already exists')

        self.__film_base[identifier] = film

    def upload_films_from_file(self, filename: str) -> None:
        with open(filename, encoding='utf-8') as file:
            for line in file.readlines():
                if not line: continue
                identifier, name = line.split(',')
                self.add_film(int(identifier), Film(name.strip()))

    def print(self):
        print("Available films:")
        for identifier, film in self.__film_base.items():
            print(f'ID:{identifier}   {film}')


class Base:
    def __init__(self, film_base: FilmBase) -> None:
        self.__film_base = film_base
        self.__viewers_base: List['Base._Viewer'] = list()

    class _Viewer:
        def __init__(self) -> None:
            self.__watched_films_list: List[Film] = list()
            self.__watched_films_set: Set[Film] = set()

        def add_watched_film(self, film: Film) -> None:
            self.__watched_films_list.append(film)
            self.__watched_films_set.add(film)
            film.views += 1

        def get_match_index(self, other_viewer: 'Base._Viewer') -> float:
            match_number = len(self.__watched_films_set & other_viewer.__watched_films_set)
            return match_number / len(other_viewer.__watched_films_set)

        def get_mismatched_films(self, other_viewer: 'Base._Viewer') -> Set[Film]:
            return self.__watched_films_set - other_viewer.__watched_films_set

        def print(self) -> None:
            print("Watched films:")
            for watched_film in self.__watched_films_list:
                print(watched_film.name)

    def add_viewer(self, *identifies: int) -> None:
        new_viewer = self._Viewer()
        for film in map(self.__film_base.get_film, identifies):
            new_viewer.add_watched_film(film)
        self.__viewers_base.append(new_viewer)

    def add_watched_film_to_viewer(self, viewer_index: int, film_identify: int) -> None:
        self.__viewers_base[viewer_index].add_watched_film(self.__film_base.get_film(film_identify))

    def get_viewer(self, index: int) -> 'Base._Viewer':
        return self.__viewers_base[index]

    def upload_views_from_file(self, filename: str) -> None:
        with open(filename, encoding='utf-8') as file:
            for line in file.readlines():
                if not line: continue
                self.add_viewer(*map(int, line.split(',')))

    def recommend(self, index: int) -> Film:
        other_viewer = self.__viewers_base[index]
        most_interesting_film = {"film": None, "index": 0}
        for viewer in self.__viewers_base:
            if viewer == other_viewer: continue
            index = viewer.get_match_index(other_viewer)
            if index > 0.5 or isclose(index, 0.5):
                for film in viewer.get_mismatched_films(other_viewer):
                    interesting_index = film.views * index
                    if interesting_index > most_interesting_film["index"]:
                        most_interesting_film['film'] = film
                        most_interesting_film['index'] = interesting_index

        return most_interesting_film["film"] if most_interesting_film["film"] is not None else Film('unknown')

    def print(self):
        self.__film_base.print()
        print()
        print("Views data:")
        for viewer in self.__viewers_base:
            print("—————————————————")
            viewer.print()


if __name__ == '__main__':
    films = FilmBase()
    films.upload_films_from_file('FilmsBase.txt')
    views_data = Base(films)
    views_data.upload_views_from_file('ViewersBase.txt')
    views_data.add_watched_film_to_viewer(0, 1)
    views_data.print()



