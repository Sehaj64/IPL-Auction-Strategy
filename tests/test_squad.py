import unittest
import sqlite3
import os
import sys

# Adjust path for importing modules from src/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src import squad, player_queries


class TestSquad(unittest.TestCase):

    def setUp(self):
        """Set up a temporary in-memory database for each test."""
        self.conn = sqlite3.connect(":memory:")
        self.conn.row_factory = sqlite3.Row

        # Create schema and load data
        schema_path = os.path.join(os.path.dirname(__file__), '..',
                                   'database', 'schema.sql')
        with open(schema_path, 'r') as f:
            self.conn.executescript(f.read())
        data_path = os.path.join(os.path.dirname(__file__), '..',
                                 'database', 'data.sql')
        with open(data_path, 'r') as f:
            self.conn.executescript(f.read())

        # Store original values to reset them in tearDown
        self.original_max_squad_size = squad.MAX_SQUAD_SIZE
        self.original_max_overseas = squad.MAX_OVERSEAS_PLAYERS
        self.original_total_budget = squad.TOTAL_BUDGET_USD

    def tearDown(self):
        """Close the database connection and reset constants after each test."""
        self.conn.close()
        squad.MAX_SQUAD_SIZE = self.original_max_squad_size
        squad.MAX_OVERSEAS_PLAYERS = self.original_max_overseas
        squad.TOTAL_BUDGET_USD = self.original_total_budget

    def test_can_draft_player_success(self):
        """Test that a valid player can be drafted."""
        can_draft, reason = squad.can_draft_player(self.conn, 1)  # Virat Kohli
        self.assertTrue(can_draft)
        self.assertEqual(reason, "Virat Kohli can be drafted.")

    def test_can_draft_player_already_drafted(self):
        """Test that a player who is already drafted cannot be drafted again."""
        player_queries.draft_player(self.conn, 1)  # Draft Kohli
        can_draft, reason = squad.can_draft_player(self.conn, 1)
        self.assertFalse(can_draft)
        self.assertEqual(reason, "Virat Kohli is already drafted.")

    def test_can_draft_player_squad_full(self):
        """Test that a player cannot be drafted if the squad is full."""
        squad.MAX_SQUAD_SIZE = 1  # Temporarily reduce for testing
        player_queries.draft_player(self.conn, 1)  # Draft one player
        can_draft, reason = squad.can_draft_player(self.conn, 2)
        self.assertFalse(can_draft)
        self.assertEqual(reason, "Maximum squad size reached.")

    def test_can_draft_player_overseas_full(self):
        """Test drafting an overseas player when the overseas limit is full."""
        squad.MAX_OVERSEAS_PLAYERS = 1  # Temporarily reduce for testing
        player_queries.draft_player(self.conn, 5)  # Draft Maxwell (Overseas)
        can_draft, reason = squad.can_draft_player(self.conn, 6)
        self.assertFalse(can_draft)
        self.assertEqual(reason, "Maximum overseas players limit reached.")

    def test_can_draft_player_budget_exceeded(self):
        """Test that a player cannot be drafted if it exceeds the budget."""
        squad.TOTAL_BUDGET_USD = 2000000.00  # Temporarily reduce for testing
        player_queries.draft_player(self.conn, 1)  # Draft Kohli (2M)
        can_draft, reason = squad.can_draft_player(self.conn, 2)
        self.assertFalse(can_draft)
        self.assertIn("exceed the total budget", reason)

    def test_get_squad_summary(self):
        """Test that the squad summary is accurate."""
        summary_initial = squad.get_squad_summary(self.conn)
        self.assertEqual(summary_initial['squad_size'], 0)
        self.assertEqual(summary_initial['overseas_count'], 0)
        self.assertEqual(summary_initial['total_cost'], 0.0)
        self.assertEqual(summary_initial['remaining_budget'],
                         squad.TOTAL_BUDGET_USD)

        player_queries.draft_player(self.conn, 1)  # Draft Kohli (Indian, 2M)
        player_queries.draft_player(self.conn, 5)  # Maxwell (Overseas, 1.7M)

        summary_updated = squad.get_squad_summary(self.conn)
        self.assertEqual(summary_updated['squad_size'], 2)
        self.assertEqual(summary_updated['overseas_count'], 1)
        self.assertEqual(summary_updated['total_cost'], 3700000.00)
        self.assertEqual(summary_updated['remaining_budget'],
                         squad.TOTAL_BUDGET_USD - 3700000.00)


if __name__ == '__main__':
    unittest.main()
