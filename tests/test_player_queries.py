import unittest
import sqlite3
import os

# Adjust path for importing modules from src/
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src import player_queries, database

class TestPlayerQueries(unittest.TestCase):

    def setUp(self):
        """Set up a temporary in-memory database for each test."""
        self.conn = sqlite3.connect(":memory:")
        self.conn.row_factory = sqlite3.Row
        
        # Create schema
        schema_path = os.path.join(os.path.dirname(__file__), '..', 'database', 'schema.sql')
        with open(schema_path, 'r') as f:
            self.conn.executescript(f.read())
        
        # Load sample data
        data_path = os.path.join(os.path.dirname(__file__), '..', 'database', 'data.sql')
        with open(data_path, 'r') as f:
            self.conn.executescript(f.read())

    def tearDown(self):
        """Close the database connection after each test."""
        self.conn.close()

    def test_get_all_players(self):
        """Test retrieving all players."""
        players = player_queries.get_all_players(self.conn)
        self.assertEqual(len(players), 14) # Based on sample data

        drafted_players = player_queries.get_all_players(self.conn, drafted_only=True)
        self.assertEqual(len(drafted_players), 0) # Initially no players are drafted

    def test_get_player_by_id(self):
        """Test retrieving a player by ID."""
        player = player_queries.get_player_by_id(self.conn, 1) # Virat Kohli
        self.assertIsNotNone(player)
        self.assertEqual(player['name'], 'Virat Kohli')

        player_none = player_queries.get_player_by_id(self.conn, 999)
        self.assertIsNone(player_none)

    def test_get_player_by_name(self):
        """Test retrieving a player by name."""
        player = player_queries.get_player_by_name(self.conn, 'Rohit Sharma')
        self.assertIsNotNone(player)
        self.assertEqual(player['id'], 2)

        player_none = player_queries.get_player_by_name(self.conn, 'NonExistent Player')
        self.assertIsNone(player_none)

    def test_filter_players(self):
        """Test filtering players by various criteria."""
        # Filter by role
        batsmen = player_queries.filter_players(self.conn, role='Batsman')
        self.assertEqual(len(batsmen), 4) # Virat Kohli, Rohit Sharma, Shikhar Dhawan, David Warner

        # Filter by nationality
        indian_players = player_queries.filter_players(self.conn, nationality='Indian')
        self.assertEqual(len(indian_players), 8) # Virat, Rohit, Bumrah, Hardik, Dhoni, Rahul, Dhawan, Chahal (8 players, excluding foreign ones)

        # Filter by price range
        expensive_players = player_queries.filter_players(self.conn, min_price=1800000.00)
        # Kohli (2M), Bumrah (1.9M), Ben Stokes (1.9M), Rohit (1.8M) => 4
        # Ah, my count for sample data was off. Let's re-verify sample data.
        # Virat (2M), Rohit (1.8M), Bumrah (1.9M), Hardik (1.5M), Maxwell (1.7M), Rashid (1.6M), Dhoni (1.2M), Stokes (1.9M), Rahul (1.4M), Boult (1.5M), Dhawan (1M), Warner (1.6M), Chahal (1.1M), Buttler (1.7M)
        # >= 1.8M: Virat (2), Rohit (1.8), Bumrah (1.9), Stokes (1.9) => 4 players. My assertion was 5 before which was wrong based on actual data
        self.assertEqual(len(expensive_players), 4)

        # Combined filter
        indian_bowlers = player_queries.filter_players(self.conn, role='Bowler', nationality='Indian')
        self.assertEqual(len(indian_bowlers), 2) # Bumrah, Chahal

        # Filter drafted (initially none)
        drafted = player_queries.filter_players(self.conn, drafted_status=True)
        self.assertEqual(len(drafted), 0)

    def test_draft_undraft_player(self):
        """Test drafting and undrafting a player."""
        # Draft a player
        success_draft = player_queries.draft_player(self.conn, 1) # Virat Kohli
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
        self.assertEqual(player_queries.get_drafted_overseas_players_count(self.conn), 0)
        self.assertEqual(player_queries.get_total_squad_cost(self.conn), 0.0)

        # Draft Kohli (Indian) and Maxwell (Overseas)
        player_queries.draft_player(self.conn, 1) # Virat Kohli (2M)
        player_queries.draft_player(self.conn, 5) # Glenn Maxwell (1.7M)

        self.assertEqual(player_queries.get_drafted_players_count(self.conn), 2)
        self.assertEqual(player_queries.get_drafted_overseas_players_count(self.conn), 1)
        self.assertEqual(player_queries.get_total_squad_cost(self.conn), 3700000.00) # 2M + 1.7M

if __name__ == '__main__':
    unittest.main()
