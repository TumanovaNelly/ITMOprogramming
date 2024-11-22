from math import isclose
import csv
from typing import Dict, List, Set, Optional


class Film:
    def __init__(self, identify: int, name: str) -> None:
        self.__name: str = name
        self.__identify: int = identify

    @property
    def name(self) -> str:
        return self.__name

    @property
    def identify(self) -> int:
        return self.__identify

    def __str__(self) -> str:
        return f'Film (ID: {self.__identify}) "{self.__name}"'


class FilmBase:
    def __init__(self) -> None:
        self.__film_base: Dict[int, Film] = dict()

    def __getitem__(self, identifier: int) -> Film:
        return self.__film_base[identifier]

    def __contains__(self, identify: int):
        return identify in self.__film_base

    def add_film(self, film: Film) -> None:
        if film.identify in self.__film_base:
            raise KeyError(f'Film with ID:{film.identify} already exists')

        self.__film_base[film.identify] = film

    def upload_films_from_file(self, filename: str) -> None:
        with open(filename, encoding='utf-8') as file:
            reader = csv.reader(file)
            for identifier, name in reader:
                self.add_film(Film(int(identifier), name.strip()))

    def print(self):
        print("Available films:")
        for film in self.__film_base.values():
            print(film)


class Films:
    def __init__(self) -> None:
        self.__watched_films_list: List[Film] = list()
        self.__watched_films_set: Set[Film] = set()

    def __getitem__(self, identifier: int) -> Film:
        return self.__watched_films_list[identifier]

    def __and__(self, other: 'Films') -> Set[Film]:
        return set(self.__watched_films_set) & set(other.__watched_films_set)

    def __sub__(self, other: 'Films') -> Set[Film]:
        return self.__watched_films_set - other.__watched_films_set

    def __len__(self) -> int:
        return len(self.__watched_films_list)

    def set_len(self) -> int:
        return len(self.__watched_films_set)

    def add(self, film: Film) -> None:
        self.__watched_films_list.append(film)
        self.__watched_films_set.add(film)

    def print(self):
        for film in self.__watched_films_list:
            print(film)


class Viewer:
    def __init__(self, *films: Film) -> None:
        self.watched_films: Films = Films()
        for film in films:
            self.watched_films.add(film)

    def get_match_index(self, other_viewer: 'Viewer') -> float:
        if len(self.watched_films) == 0:
            return 1
        match_number = len(self.watched_films & other_viewer.watched_films)
        return match_number / self.watched_films.set_len()

    def get_mismatched_films(self, other_viewer: 'Viewer') -> Set[Film]:
        return self.watched_films - other_viewer.watched_films

    def print(self) -> None:
        print("Watched films:")
        self.watched_films.print()


class ViewersBase:
    def __init__(self, film_base: FilmBase) -> None:
        self.__film_base = film_base
        self.__viewers_base: List[Viewer] = list()
        self.__watch_data: Dict[Film, int] = dict()

    def __getitem__(self, identifier: int) -> Viewer:
        return self.__viewers_base[identifier]

    def add_viewer(self, viewer: Viewer) -> None:
        for film in viewer.watched_films:
            if film.identify not in self.__film_base or self.__film_base[film.identify] != film:
                raise ValueError("Unknown film")
            self.__watch_data[film] = self.__watch_data.get(film, 0) + 1

        self.__viewers_base.append(viewer)

    def upload_views_from_file(self, filename: str) -> None:
        with open(filename, encoding='utf-8') as file:
            reader = csv.reader(file)
            for line in reader:
                if not line: continue
                self.add_viewer(Viewer(*map(self.__film_base.__getitem__, map(int, line))))

    def recommend(self, viewer: Viewer) -> Optional[Film]:
        most_interesting_film = {"film": None, "index": 0}
        for other_viewer in self.__viewers_base:
            if viewer == other_viewer: continue
            index = viewer.get_match_index(other_viewer)
            if index > 0.5 or isclose(index, 0.5):
                for film in other_viewer.get_mismatched_films(viewer):
                    interesting_index = self.__watch_data[film] * index
                    if interesting_index > most_interesting_film["index"]:
                        most_interesting_film['film'] = film
                        most_interesting_film['index'] = interesting_index

        return most_interesting_film["film"]

    def print(self):
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
    films.add_film(Film(5, "Matrix"))
    viewers = ViewersBase(films)
    viewers.upload_views_from_file('ViewersBase.txt')
    viewers.add_viewer(Viewer(films[1], films[2], films[5], films[5]))

    viewers.print()

    print("==============================================")
    new_viewer = Viewer(films[2], films[4])
    print("New viewer data:")
    new_viewer.print()
    print(f"=> {viewers.recommend(new_viewer)} recommended for new viewer")