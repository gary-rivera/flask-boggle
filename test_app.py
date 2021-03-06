from unittest import TestCase

from app import app, games

# Make Flask errors be real errors, not HTML pages with error info
app.config["TESTING"] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config["DEBUG_TB_HOSTS"] = ["dont-show-debug-toolbar"]


class BoggleAppTestCase(TestCase):
    """Test flask app of Boggle."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config["TESTING"] = True

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""

        with self.client as client:
            response = client.get("/")
            ...
            # test that you're getting a template
            html = response.get_data(as_text=True)
            # top view verification that route works
            self.assertEqual(response.status_code, 200)
            # verify unique html is loading
            self.assertIn('<table class="board">', html)

    def test_api_new_game(self):
        """Test starting a new game."""

        with self.client as client:
            # write a test for this route
            # save response from get reqeust to route
            resp = client.get("/api/new-game")
            data = resp.json

            # top view cert
            self.assertEqual(resp.status_code, 200)

            # is game id a string in json respo
            self.assertIsInstance(data["gameId"], str)
            # is board a list on json respo
            self.assertIsInstance(data["board"], list)
            # is games in json respon
            self.assertIn(data["gameId"], games)

    def test_score_word(self):
        """ the way a word is validated with defined class methods """
        with self.client as client:
            resp = client.get("api/new-game")
            # get the json from resp
            data = resp.json

            # generate mock board (5x5)
            gameId = data["gameId"]
            game = games[gameId]

            # mock board hard code
            game.board[0] = ["W", "O", "R", "D", "S"]
            game.board[1] = ["S", "H", "O", "E", "S"]
            game.board[2] = ["L", "I", "G", "H", "T"]
            game.board[3] = ["K", "I", "D", "S", "A"]
            game.board[4] = ["I", "R", "A", "W", "R"]

            # high level cert
            self.assertEqual(resp.status_code, 200)

            # verify post request from /score-word

            resp = client.post(
                "/api/score-word", json={"gameId": gameId, "word": "AXYSB"}
            )

            self.assertEqual(resp.json, {"result": "not_a_word"})

            # not on board
            resp = client.post(
                "/api/score-word", json={"gameId": gameId, "word": "ROCKS"}
            )
            self.assertEqual(resp.json, {"result": "not_on_board"})

            # valid
            resp = client.post(
                "/api/score-word", json={"gameId": gameId, "word": "WORDS"}
            )
            self.assertEqual(resp.json, {"result": "word_OK"})
