import unittest
from typing import Set
from src.lab4.FilmsSystem import Film, Films, FilmBase, Viewer, ViewersBase


class TestFilm(unittest.TestCase):
    def test_film_creation_and_properties(self):
        film = Film(1, "Inception")
        self.assertEqual(film.identify, 1)
        self.assertEqual(film.name, "Inception")
        self.assertEqual(str(film), 'Film (ID: 1) "Inception"')


class TestFilmBase(unittest.TestCase):
    def setUp(self):
        self.films = FilmBase()

    def test_add_and_get_film(self):
        film1 = Film(1, "Inception")
        film2 = Film(2, "Matrix")
        self.films.add_film(film1)
        self.films.add_film(film2)
        self.assertEqual(self.films[1], film1)
        self.assertEqual(self.films[2], film2)

    def test_add_duplicate_film(self):
        self.films.add_film(Film(1, "Inception"))
        self.assertRaises(KeyError, self.films.add_film, Film(1, "Inception"))


class TestFilms(unittest.TestCase):
    def setUp(self):
        self.film1 = Film(1, "Inception")
        self.film2 = Film(2, "Titanic")
        self.films = Films()

    def test_add_and_access_film(self):
        self.films.add(self.film1)
        self.assertEqual(self.films[0], self.film1)
        self.assertEqual(len(self.films), 1)

    def test_intersection_and_difference(self):
        self.films.add(self.film1)
        other_films = Films()
        other_films.add(self.film1)
        other_films.add(self.film2)
        intersection: Set[Film] = self.films & other_films
        difference: Set[Film] = other_films - self.films
        self.assertEqual(len(intersection), 1)
        self.assertEqual(len(difference), 1)
        self.assertIn(self.film2, difference)


class TestViewer(unittest.TestCase):
    def setUp(self):
        self.film1 = Film(1, "Inception")
        self.film2 = Film(2, "Titanic")
        self.film3 = Film(3, "Avatar")
        self.viewer1 = Viewer(self.film1, self.film2)
        self.viewer2 = Viewer(self.film2, self.film3)

    def test_match_index(self):
        match_index = self.viewer1.get_match_index(self.viewer2)
        self.assertAlmostEqual(match_index, 0.5)

    def test_mismatched_films(self):
        mismatched = self.viewer1.get_mismatched_films(self.viewer2)
        self.assertEqual({film.name for film in mismatched}, {"Inception"})


class TestViewersBase(unittest.TestCase):
    def setUp(self):
        self.films = FilmBase()
        self.films.add_film(Film(1, "Inception"))
        self.films.add_film(Film(2, "Titanic"))
        self.films.add_film(Film(3, "Avatar"))
        self.viewers_base = ViewersBase(self.films)

    def test_add_and_recommend(self):
        viewer1 = Viewer(self.films[1], self.films[2])
        viewer2 = Viewer(self.films[2], self.films[3])
        self.viewers_base.add_viewer(viewer1)
        self.viewers_base.add_viewer(viewer2)
        self.assertEqual(self.viewers_base.recommend(viewer1), self.films[3])
        self.assertEqual(self.viewers_base.recommend(viewer2), self.films[1])

    def test_add_unknown_film(self):
        viewer1 = Viewer(Film(99, "Unknown"))
        viewer2 = Viewer(Film(1, "Avatar"))
        self.assertRaises(ValueError, self.viewers_base.add_viewer, viewer1)
        self.assertRaises(ValueError, self.viewers_base.add_viewer, viewer2)


if __name__ == "__main__":
    unittest.main()

