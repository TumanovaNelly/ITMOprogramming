import unittest
from io import StringIO
import sys
from src.lab4.FilmsSystem import Film, Films, FilmBase, Viewer, ViewersBase


class TestFilmSystem(unittest.TestCase):
    def setUp(self):
        self.films = FilmBase()
        self.films.add_film(Film(1, "Inception"))
        self.films.add_film(Film(2, "Titanic"))
        self.films.add_film(Film(3, "Avatar"))
        self.films.add_film(Film(4, "The Matrix"))
        self.viewers_base = ViewersBase(self.films)

    def test_add_and_get_film(self):
        self.assertRaises(KeyError, self.films.add_film, Film(1, "The Matrix 2"))
        self.assertRaises(KeyError, self.films.__getitem__, 5)
        new_film = Film(5, "The Matrix 2")
        self.films.add_film(new_film)
        self.assertEqual(self.films.__getitem__(5), new_film)

    def test_add_viewer(self):
        viewer1 = Viewer(self.films[1], self.films[2], self.films[2])
        viewer2 = Viewer(self.films[2], self.films[3], self.films[4])
        viewer3 = Viewer(self.films[3], self.films[3])
        self.viewers_base.add_viewer(viewer1)
        self.viewers_base.add_viewer(viewer2)
        self.viewers_base.add_viewer(viewer3)
        self.assertEqual(self.viewers_base[0], viewer1)
        self.assertEqual(self.viewers_base[1], viewer2)
        self.assertEqual(self.viewers_base[2], viewer3)
        viewer_bad = Viewer(self.films[4], Film(9, "Smeshariki"))
        self.assertRaises(ValueError, self.viewers_base.add_viewer, viewer_bad)

    def test_viewer_creation_and_match_index(self):
        viewer1 = Viewer(self.films[1], self.films[2], self.films[2])
        viewer2 = Viewer(self.films[2], self.films[3], self.films[4])
        viewer3 = Viewer(self.films[3], self.films[3])
        self.assertAlmostEqual(viewer1.get_match_index(viewer2), 1 / 2)
        self.assertAlmostEqual(viewer2.get_match_index(viewer1), 1 / 3)
        self.assertAlmostEqual(viewer1.get_match_index(viewer3), 0)
        self.assertAlmostEqual(viewer3.get_match_index(viewer1), 0)
        self.assertAlmostEqual(viewer2.get_match_index(viewer3), 1 / 3)
        self.assertAlmostEqual(viewer3.get_match_index(viewer2), 1)

        viewer_empty = Viewer()
        self.assertAlmostEqual(viewer_empty.get_match_index(viewer1), 1)
        self.assertAlmostEqual(viewer1.get_match_index(viewer_empty), 0)

    def test_get_mismatched_films(self):
        viewer1 = Viewer(self.films[1], self.films[2])
        viewer2 = Viewer(self.films[2], self.films[3])
        mismatched = viewer1.get_mismatched_films(viewer2)
        self.assertEqual(mismatched, {self.films[1]})

    def test_recommendation(self):
        viewer1 = Viewer(self.films[1], self.films[2])
        viewer2 = Viewer(self.films[2], self.films[3])
        viewer3 = Viewer(self.films[3], self.films[4])
        self.viewers_base.add_viewer(viewer1)
        self.viewers_base.add_viewer(viewer2)
        recommended_film = self.viewers_base.recommend(viewer3)
        self.assertEqual(recommended_film, self.films[2])


if __name__ == "__main__":
    unittest.main()
