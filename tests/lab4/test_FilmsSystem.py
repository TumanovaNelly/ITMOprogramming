import unittest
from unittest.mock import patch, mock_open
from src.lab4.FilmsSystem import Film, FilmBase, ViewersBase


class TestFilm(unittest.TestCase):
    def test_film_initialization(self):
        film = Film("Inception")
        self.assertEqual(film.name, "Inception")
        self.assertEqual(str(film), 'Film "Inception"')


class TestFilmBase(unittest.TestCase):
    def setUp(self):
        self.film_base = FilmBase()

    def test_add_and_get_film(self):
        film = Film("Matrix")
        self.film_base.add_film(1, film)
        self.assertEqual(self.film_base.get_film(1).name, "Matrix")

    def test_add_existing_film(self):
        self.film_base.add_film(1, Film("Matrix"))
        with self.assertRaises(KeyError):
            self.film_base.add_film(1, Film("Inception"))

    def test_get_nonexistent_film(self):
        with self.assertRaises(KeyError):
            self.film_base.get_film(99)

    @patch("builtins.open", new_callable=mock_open, read_data="1,Matrix\n2,Inception\n")
    def test_upload_films_from_file(self, mock_file):
        self.film_base.upload_films_from_file("dummy.txt")
        self.assertEqual(self.film_base.get_film(1).name, "Matrix")
        self.assertEqual(self.film_base.get_film(2).name, "Inception")


class TestViewersBase(unittest.TestCase):
    def setUp(self):
        self.film_base = FilmBase()
        self.film_base.add_film(1, Film("Matrix"))
        self.film_base.add_film(2, Film("Inception"))
        self.film_base.add_film(3, Film("Avatar"))
        self.viewers_base = ViewersBase(self.film_base)

    def test_add_viewer(self):
        self.viewers_base.add_viewer(1, 2)
        viewer = self.viewers_base._ViewersBase__viewers_base[0]
        self.assertEqual(len(viewer._Viewer__watched_films_list), 2)
        self.assertEqual(viewer._Viewer__watched_films_list[0].name, "Matrix")
        self.assertEqual(viewer._Viewer__watched_films_list[1].name, "Inception")

    def test_add_watched_films_to_viewer(self):
        self.viewers_base.add_viewer(1)
        self.viewers_base.add_watched_films_to_viewer(0, 2, 3)
        viewer = self.viewers_base._ViewersBase__viewers_base[0]
        self.assertEqual(len(viewer._Viewer__watched_films_list), 3)
        self.assertEqual(viewer._Viewer__watched_films_list[0].name, "Matrix")
        self.assertEqual(viewer._Viewer__watched_films_list[1].name, "Inception")
        self.assertEqual(viewer._Viewer__watched_films_list[2].name, "Avatar")

    @patch("builtins.open", new_callable=mock_open, read_data="1,2\n2,3\n")
    def test_upload_views_from_file(self, mock_file):
        self.viewers_base.upload_views_from_file("dummy.txt")
        viewer1 = self.viewers_base._ViewersBase__viewers_base[0]
        self.assertEqual(len(viewer1._Viewer__watched_films_list), 2)

    def test_recommend(self):
        self.viewers_base.add_viewer(1, 2)  # Viewer 0: Watched "Matrix" and "Inception"
        self.viewers_base.add_viewer(1, 3)  # Viewer 1: Watched "Matrix" and "Avatar"
        recommended_film = self.viewers_base.recommend(0)
        self.assertEqual(recommended_film.name, "Avatar")

    def test_no_recommendations(self):
        self.viewers_base.add_viewer(1)  # Viewer 0
        self.viewers_base.add_viewer(1)  # Viewer 1
        recommended_film = self.viewers_base.recommend(0)
        self.assertIsNone(recommended_film)

    def test_match_index(self):
        viewer1 = self.viewers_base._Viewer()
        viewer2 = self.viewers_base._Viewer()
        viewer1.add_watched_film(self.film_base.get_film(1))
        viewer1.add_watched_film(self.film_base.get_film(2))
        viewer2.add_watched_film(self.film_base.get_film(1))
        viewer2.add_watched_film(self.film_base.get_film(3))
        self.assertAlmostEqual(viewer1.get_match_index(viewer2), 0.5)


if __name__ == "__main__":
    unittest.main()
