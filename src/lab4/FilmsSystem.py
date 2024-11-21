from math import isclose
import csv
from typing import Dict, List, Set, Optional


class Film:
    def __init__(self, name: str) -> None:
        self.__name: str = name

    @property
    def name(self) -> str:
        return self.__name

    def __str__(self) -> str:
        return f'Film "{self.__name}"'


class FilmBase:
    def __init__(self) -> None:
        self.__film_base: Dict[int, Film] = dict()

    def get_film(self, identifier: int) -> Film:
        if identifier not in self.__film_base:
            raise KeyError(f'Film with ID:{identifier} does not exist')

        return self.__film_base[identifier]

    def add_film(self, identifier: int, film: Film) -> None:
        if identifier in self.__film_base:
            raise KeyError(f'Film with ID:{identifier} already exists')

        self.__film_base[identifier] = film

    def upload_films_from_file(self, filename: str) -> None:
        with open(filename, encoding='utf-8') as file:
            reader = csv.reader(file)
            for identifier, name in reader:
                self.add_film(int(identifier), Film(name.strip()))

    def print(self):
        print("Available films:")
        for identifier, film in self.__film_base.items():
            print(f'ID:{identifier}   {film}')


class ViewersBase:
    def __init__(self, film_base: FilmBase) -> None:
        self.__film_base = film_base
        self.__viewers_base: List['ViewersBase._Viewer'] = list()
        self.__watch_data: Dict[Film, int] = dict()

    class _Viewer:
        def __init__(self) -> None:
            self.__watched_films_list: List[Film] = list()
            self.__watched_films_set: Set[Film] = set()

        def add_watched_film(self, film: Film) -> None:
            self.__watched_films_list.append(film)
            self.__watched_films_set.add(film)

        def get_match_index(self, other_viewer: 'ViewersBase._Viewer') -> float:
            if len(self.__watched_films_list) == 0:
                return 1
            match_number = len(self.__watched_films_set & other_viewer.__watched_films_set)
            return match_number / len(self.__watched_films_set)

        def get_mismatched_films(self, other_viewer: 'ViewersBase._Viewer') -> Set[Film]:
            return self.__watched_films_set - other_viewer.__watched_films_set

        def print(self) -> None:
            print("Watched films:")
            for watched_film in self.__watched_films_list:
                print(watched_film.name)

    def add_viewer(self, *film_identifies: int) -> None:
        new_viewer = self._Viewer()

        for film in map(self.__film_base.get_film, film_identifies):
            new_viewer.add_watched_film(film)
            self.__watch_data[film] = self.__watch_data.get(film, 0) + 1

        self.__viewers_base.append(new_viewer)

    def add_watched_films_to_viewer(self, viewer_index: int, *film_identifies: int) -> None:
        for film in map(self.__film_base.get_film, film_identifies):
            self.__viewers_base[viewer_index].add_watched_film(film)
            self.__watch_data[film] = self.__watch_data.get(film, 0) + 1

    def upload_views_from_file(self, filename: str) -> None:
        with open(filename, encoding='utf-8') as file:
            reader = csv.reader(file)
            for line in reader:
                if not line: continue
                self.add_viewer(*map(int, line))

    def recommend(self, index: int) -> Optional[Film]:
        other_viewer = self.__viewers_base[index]
        most_interesting_film = {"film": None, "index": 0}
        for viewer in self.__viewers_base:
            if viewer == other_viewer: continue
            index = other_viewer.get_match_index(viewer)
            if index > 0.5 or isclose(index, 0.5):
                for film in viewer.get_mismatched_films(other_viewer):
                    interesting_index = self.__watch_data[film] * index
                    if interesting_index > most_interesting_film["index"]:
                        most_interesting_film['film'] = film
                        most_interesting_film['index'] = interesting_index

        return most_interesting_film["film"]

    def print(self):
        self.__film_base.print()
        print()
        print("Watched films data:")
        for film, views in self.__watch_data.items():
            print(f'{film} has been viewed {views} times')
        print()
        print("Views data:")
        for viewer in self.__viewers_base:
            print("—————————————————")
            viewer.print()


if __name__ == '__main__':
    films = FilmBase()
    films.upload_films_from_file('FilmsBase.txt')
    views_data = ViewersBase(films)
    views_data.upload_views_from_file('ViewersBase.txt')
    views_data.add_viewer(2, 4)

    views_data.print()
    print(f'{views_data.recommend(-1)} recommended')


