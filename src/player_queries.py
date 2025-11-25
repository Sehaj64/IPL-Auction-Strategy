def get_all_players(conn, drafted_only=False):
    """Retrieves all players or only drafted players from the database."""
    cursor = conn.cursor()
    if drafted_only:
        cursor.execute("SELECT * FROM players WHERE is_drafted = 1 ORDER BY name")
    else:
        cursor.execute("SELECT * FROM players ORDER BY name")
    players = cursor.fetchall()
    return players

def get_player_by_id(conn, player_id):
    """Retrieves a single player by their ID."""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM players WHERE id = ?", (player_id,))
    player = cursor.fetchone()
    return player

def get_player_by_name(conn, name):
    """Retrieves a single player by their name."""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM players WHERE name = ?", (name,))
    player = cursor.fetchone()
    return player

def filter_players(conn, role=None, nationality=None, min_price=None, max_price=None, drafted_status=None):
    """Filters players based on various criteria."""
    cursor = conn.cursor()
    query = "SELECT * FROM players WHERE 1=1"
    params = []

    if role:
        query += " AND role = ?"
        params.append(role)
    if nationality:
        query += " AND nationality = ?"
        params.append(nationality)
    if min_price is not None:
        query += " AND base_price_usd >= ?"
        params.append(min_price)
    if max_price is not None:
        query += " AND base_price_usd <= ?"
        params.append(max_price)
    if drafted_status is not None:
        query += " AND is_drafted = ?"
        params.append(1 if drafted_status else 0)

    query += " ORDER BY name"
    cursor.execute(query, params)
    players = cursor.fetchall()
    return players

def draft_player(conn, player_id):
    """Marks a player as drafted."""
    cursor = conn.cursor()
    cursor.execute("UPDATE players SET is_drafted = 1 WHERE id = ?", (player_id,))
    conn.commit()
    return cursor.rowcount > 0

def undraft_player(conn, player_id):
    """Marks a player as not drafted."""
    cursor = conn.cursor()
    cursor.execute("UPDATE players SET is_drafted = 0 WHERE id = ?", (player_id,))
    conn.commit()
    return cursor.rowcount > 0

def get_drafted_players_count(conn):
    """Returns the count of currently drafted players."""
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM players WHERE is_drafted = 1")
    count = cursor.fetchone()[0]
    return count

def get_drafted_overseas_players_count(conn):
    """Returns the count of currently drafted overseas players."""
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM players WHERE is_drafted = 1 AND nationality = 'Overseas'")
    count = cursor.fetchone()[0]
    return count

def get_total_squad_cost(conn):
    """Returns the total cost of currently drafted players."""
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(base_price_usd) FROM players WHERE is_drafted = 1")
    total_cost = cursor.fetchone()[0]
    return total_cost if total_cost else 0.0
