from . import player_queries

MAX_SQUAD_SIZE = 25
MAX_OVERSEAS_PLAYERS = 8
TOTAL_BUDGET_USD = 10000000.00 # 10 Million USD, or approx 10 Crores INR

def can_draft_player(conn, player_id):
    """
    Checks if a player can be drafted based on current squad rules.
    Returns (True, "reason") if allowed, (False, "reason") otherwise.
    """
    player = player_queries.get_player_by_id(conn, player_id)
    if not player:
        return False, "Player not found."

    if player['is_drafted'] == 1:
        return False, f"{player['name']} is already drafted."

    current_squad_size = player_queries.get_drafted_players_count(conn)
    if current_squad_size >= MAX_SQUAD_SIZE:
        return False, "Maximum squad size reached."

    current_total_cost = player_queries.get_total_squad_cost(conn)
    if (current_total_cost + player['base_price_usd']) > TOTAL_BUDGET_USD:
        return False, f"Adding {player['name']} would exceed the total budget. Remaining budget: ${TOTAL_BUDGET_USD - current_total_cost:.2f}"

    if player['nationality'] == 'Overseas':
        current_overseas_players = player_queries.get_drafted_overseas_players_count(conn)
        if current_overseas_players >= MAX_OVERSEAS_PLAYERS:
            return False, "Maximum overseas players limit reached."
    
    return True, f"{player['name']} can be drafted."

def get_squad_summary(conn):
    """Returns a summary of the current drafted squad."""
    squad_size = player_queries.get_drafted_players_count(conn)
    overseas_count = player_queries.get_drafted_overseas_players_count(conn)
    total_cost = player_queries.get_total_squad_cost(conn)
    remaining_budget = TOTAL_BUDGET_USD - total_cost

    summary = {
        "squad_size": squad_size,
        "overseas_count": overseas_count,
        "total_cost": total_cost,
        "remaining_budget": remaining_budget,
        "max_squad_size": MAX_SQUAD_SIZE,
        "max_overseas_players": MAX_OVERSEAS_PLAYERS,
        "total_budget": TOTAL_BUDGET_USD
    }
    return summary
