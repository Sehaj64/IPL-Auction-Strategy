import unittest
import sqlite3
import os
import sys

# Adjust path for importing modules from src/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src import player_queries


class TestPlayerQueries(unittest.TestCase):

    def setUp(self):
        """Set up a temporary in-memory database for each test."""
        self.conn = sqlite3.connect(":memory:")
        self.conn.row_factory = sqlite3.Row

        # Create schema
        schema_path = os.path.join(os.path.dirname(__file__), '..', 'database',
                                   'schema.sql')
        with open(schema_path, 'r') as f:
            self.conn.executescript(f.read())

        # Load sample data
        data_path = os.path.join(os.path.dirname(__file__), '..', 'database',
                                 'data.sql')
        with open(data_path, 'r') as f:
            self.conn.executescript(f.read())

    def tearDown(self):
        """Close the database connection after each test."""
        self.conn.close()

    def test_get_all_players(self):
        """Test retrieving all players."""
        players = player_queries.get_all_players(self.conn)
        self.assertEqual(len(players), 14)  # Based on sample data

        drafted_players = player_queries.get_all_players(self.conn,
                                                         drafted_only=True)
        # Initially no players are drafted
        self.assertEqual(len(drafted_players), 0)

    def test_get_player_by_id(self):
        """Test retrieving a player by ID."""
        player = player_queries.get_player_by_id(self.conn, 1)  # Virat Kohli
        self.assertIsNotNone(player)
        self.assertEqual(player['name'], 'Virat Kohli')

        player_none = player_queries.get_player_by_id(self.conn, 999)
        self.assertIsNone(player_none)

    def test_get_player_by_name(self):
        """Test retrieving a player by name."""
        player = player_queries.get_player_by_name(self.conn, 'Rohit Sharma')
        self.assertIsNotNone(player)
        self.assertEqual(player['id'], 2)

        player_none = player_queries.get_player_by_name(self.conn,
                                                        'NonExistent Player')
        self.assertIsNone(player_none)

    def test_filter_players(self):
        """Test filtering players by various criteria."""
        # Filter by role
        batsmen = player_queries.filter_players(self.conn, role='Batsman')
        self.assertEqual(len(batsmen), 4)

        # Filter by nationality
        ind_players = player_queries.filter_players(self.conn,
                                                    nationality='Indian')
        self.assertEqual(len(ind_players), 8)

        # Filter by price range
        exp_players = player_queries.filter_players(self.conn,
                                                    min_price=1800000.00)
        self.assertEqual(len(exp_players), 4)

        # Combined filter
        ind_bowlers = player_queries.filter_players(self.conn, role='Bowler',
                                                    nationality='Indian')
        self.assertEqual(len(ind_bowlers), 2)  # Bumrah, Chahal

        # Filter drafted (initially none)
        drafted = player_queries.filter_players(self.conn, drafted_status=True)
        self.assertEqual(len(drafted), 0)

    def test_draft_undraft_player(self):
        """Test drafting and undrafting a player."""
        # Draft a player
        success_draft = player_queries.draft_player(self.conn, 1)  # Virat Kohli
        self.assertTrue(success_draft)
        player_drafted = player_queries.get_player_by_id(self.conn, 1)
        self.assertEqual(player_drafted['is_drafted'], 1)

        # Undraft the player
        success_undraft = player_queries.undraft_player(self.conn, 1)
        self.assertTrue(success_undraft)
        player_undrafted = player_queries.get_player_by_id(self.conn, 1)
        self.assertEqual(player_undrafted['is_drafted'], 0)

        # Test drafting non-existent player
        success_non_existent = player_queries.draft_player(self.conn, 999)
        self.assertFalse(success_non_existent)

    def test_drafted_player_counts_and_cost(self):
        """Test getting counts and total cost of drafted players."""
        self.assertEqual(player_queries.get_drafted_players_count(self.conn), 0)
        self.assertEqual(
            player_queries.get_drafted_overseas_players_count(self.conn), 0)
        self.assertEqual(player_queries.get_total_squad_cost(self.conn), 0.0)

        # Draft Kohli (Indian) and Maxwell (Overseas)
        player_queries.draft_player(self.conn, 1)  # Virat Kohli (2M)
        player_queries.draft_player(self.conn, 5)  # Glenn Maxwell (1.7M)

        self.assertEqual(player_queries.get_drafted_players_count(self.conn), 2)
        self.assertEqual(
            player_queries.get_drafted_overseas_players_count(self.conn), 1)
        self.assertEqual(player_queries.get_total_squad_cost(self.conn),
                         3700000.00)  # 2M + 1.7M


if __name__ == '__main__':
    unittest.main()
