import argparse
from contextlib import closing
from . import database, player_queries, squad


# --- Handler Functions ---

def handle_init_db(args):
    """Initializes the DB and loads sample data."""
    database.init_db()
    database.load_sample_data()


def print_player_table(players):
    """Prints a formatted table of players."""
    if not players:
        print("No players found.")
        return

    hdr = (f"{'ID':<4} {'Name':<20} {'Role':<15} {'Nationality':<12} "
           f"{'Base Price (USD)':<20} {'Drafted':<8}")
    print(hdr)
    print("-" * len(hdr))
    for player in players:
        is_drafted_str = "Yes" if player['is_drafted'] else "No"
        price_str = f"${player['base_price_usd']:<19,.2f}"
        row = (f"{player['id']:<4} {player['name']:<20} {player['role']:<15} "
               f"{player['nationality']:<12} {price_str} {is_drafted_str:<8}")
        print(row)


def handle_players_list(args):
    """Handles listing all players."""
    with closing(database.get_db_connection()) as conn:
        players = player_queries.get_all_players(conn)
        print_player_table(players)


def handle_players_find(args):
    """Handles finding a player by name."""
    with closing(database.get_db_connection()) as conn:
        player = player_queries.get_player_by_name(conn, args.name)
        if player:
            print_player_table([player])
        else:
            print(f"Player '{args.name}' not found.")


def handle_players_filter(args):
    """Handles filtering players."""
    with closing(database.get_db_connection()) as conn:
        players = player_queries.filter_players(
            conn,
            role=args.role,
            nationality=args.nationality,
            min_price=args.min_price,
            max_price=args.max_price
        )
        print_player_table(players)


def handle_squad_view(args):
    """Handles viewing the current squad."""
    with closing(database.get_db_connection()) as conn:
        print("--- Current Drafted Squad ---")
        drafted_players = player_queries.get_all_players(conn,
                                                         drafted_only=True)
        print_player_table(drafted_players)
        print("\n--- Squad Summary ---")
        handle_squad_summary(args)


def handle_squad_draft(args):
    """Handles drafting a player."""
    with closing(database.get_db_connection()) as conn:
        can_draft, reason = squad.can_draft_player(conn, args.player_id)
        if can_draft:
            success = player_queries.draft_player(conn, args.player_id)
            if success:
                player = player_queries.get_player_by_id(conn, args.player_id)
                print(f"Successfully drafted {player['name']}.")
            else:
                # This case is unlikely if can_draft is True
                print("An unexpected error occurred during drafting.")
        else:
            print(f"Error: Could not draft player. Reason: {reason}")


def handle_squad_undraft(args):
    """Handles undrafting a player."""
    with closing(database.get_db_connection()) as conn:
        success = player_queries.undraft_player(conn, args.player_id)
        if success:
            player = player_queries.get_player_by_id(conn, args.player_id)
            print(f"Successfully undrafted {player['name']}.")
        else:
            print(f"Error: Could not find player with ID "
                  f"{args.player_id} to undraft.")


def handle_squad_summary(args):
    """Handles showing the squad summary."""
    with closing(database.get_db_connection()) as conn:
        summary = squad.get_squad_summary(conn)
        print(f"Squad Size:           {summary['squad_size']} / "
              f"{summary['max_squad_size']}")
        print(f"Overseas Players:     {summary['overseas_count']} / "
              f"{summary['max_overseas_players']}")
        print(f"Total Cost:           ${summary['total_cost']:,.2f}")
        print(f"Remaining Budget:     ${summary['remaining_budget']:,.2f}")
        print(f"Total Budget:         ${summary['total_budget']:,.2f}")


# --- Main Parser Setup ---

def main():
    """Main function to configure and run the CLI."""
    parser = argparse.ArgumentParser(
        description="IPL Auction Squad Optimizer CLI")
    subparsers = parser.add_subparsers(dest="command", required=True,
                                     help="Main command")

    # `init` command
    init_parser = subparsers.add_parser(
        "init", help="Initialize the database with schema and sample data.")
    init_parser.set_defaults(func=handle_init_db)

    # `players` command group
    players_parser = subparsers.add_parser(
        "players", help="Commands related to viewing players.")
    players_subparsers = players_parser.add_subparsers(dest="subcommand",
                                                     required=True)

    players_list_parser = players_subparsers.add_parser(
        "list", help="List all available players.")
    players_list_parser.set_defaults(func=handle_players_list)

    players_find_parser = players_subparsers.add_parser(
        "find", help="Find a specific player by name.")
    players_find_parser.add_argument(
        "name", type=str, help="Full name of the player to find.")
    players_find_parser.set_defaults(func=handle_players_find)

    players_filter_parser = players_subparsers.add_parser(
        "filter", help="Filter players by criteria.")
    players_filter_parser.add_argument(
        "--role", type=str, help="Filter by player role (e.g., Batsman).")
    players_filter_parser.add_argument(
        "--nationality", type=str, help="Filter by nationality (e.g., Indian).")
    players_filter_parser.add_argument(
        "--min-price", type=float, help="Minimum base price.")
    players_filter_parser.add_argument(
        "--max-price", type=float, help="Maximum base price.")
    players_filter_parser.set_defaults(func=handle_players_filter)

    # `squad` command group
    squad_parser = subparsers.add_parser(
        "squad", help="Commands related to managing your squad.")
    squad_subparsers = squad_parser.add_subparsers(dest="subcommand",
                                                 required=True)

    squad_view_parser = squad_subparsers.add_parser(
        "view", help="View your current drafted squad and summary.")
    squad_view_parser.set_defaults(func=handle_squad_view)

    squad_draft_parser = squad_subparsers.add_parser(
        "draft", help="Draft a player to your squad.")
    squad_draft_parser.add_argument(
        "player_id", type=int, help="The ID of the player to draft.")
    squad_draft_parser.set_defaults(func=handle_squad_draft)

    squad_undraft_parser = squad_subparsers.add_parser(
        "undraft", help="Remove a player from your squad.")
    squad_undraft_parser.add_argument(
        "player_id", type=int, help="The ID of the player to undraft.")
    squad_undraft_parser.set_defaults(func=handle_squad_undraft)

    squad_summary_parser = squad_subparsers.add_parser(
        "summary", help="Show a summary of your squad's status.")
    squad_summary_parser.set_defaults(func=handle_squad_summary)

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
