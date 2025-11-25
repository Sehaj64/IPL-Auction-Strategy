# IPL Auction Squad Optimizer

This project is a command-line interface (CLI) tool designed to assist in planning and simulating an IPL (Indian Premier League) auction. It provides functionalities to manage a player database, filter players based on various criteria, and build a provisional squad while respecting auction constraints like budget, squad size, and overseas player limits.

This project is a practical application of SQL and database management concepts, demonstrating how to build a data-centric application using Python and SQLite.

## Associated Presentation

This code project serves as the practical component for the "Decoding SQL: A Foundational Guide" presentation.

- **[View the Presentation](./docs/Final%20Project-SQL.pptx)**

## Features

- **Player Database**: Comes with a pre-populated database of sample IPL players with their roles, prices, and stats.
- **Initialize Database**: A one-step command to set up the database schema and load sample data.
- **Scout Players**:
  - `players list`: View all players in the database.
  - `players find <name>`: Search for a specific player by their full name.
  - `players filter`: Filter players by role, nationality, and price range.
- **Simulate Squad Building**:
  - `squad draft <player_id>`: Add a player to your provisional squad. The tool validates the draft against auction rules.
  - `squad undraft <player_id>`: Remove a player from your squad.
  - `squad view`: Display the list of players currently in your squad.
  - `squad summary`: Get a real-time summary of your squad's status (size, cost, remaining budget, etc.).

## Technology Stack

- **Backend**: Python 3
- **Database**: SQLite 3

## Setup and Installation

1.  **Clone the repository (or download the source code).**

2.  **Navigate to the project directory:**
    ```bash
    cd sql-project-presentation
    ```

3.  **Create and activate a virtual environment (recommended):**
    ```bash
    # For Windows
    python -m venv venv
    venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

4.  **Initialize the project database:**
    This command creates the `ipl_auction.db` file and populates it with sample player data.
    ```bash
    python -m src.main init
    ```

## Usage Examples

All commands are run from the root of the project directory.

**List all available bowlers:**
```bash
python -m src.main players filter --role Bowler
```

**Find a specific player:**
```bash
python -m src.main players find "Virat Kohli"
```

**Draft a player to your squad:**
```bash
python -m src.main squad draft 1
```

**View your current squad and budget summary:**
```bash
python -m src.main squad view
```

**Get a quick summary of your squad's status:**
```bash
python -m src.main squad summary
```

**Remove a player from your squad:**
```bash
python -m src.main squad undraft 1
```

## Running Tests

The project includes a suite of unit tests to verify the correctness of the database queries and squad management logic. To run the tests:
```bash
python -m unittest discover tests
```
