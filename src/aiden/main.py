try:
    # Prefer package-relative import when run as a module (python -m aiden.main)
    from aiden.game import AdventureGame
except Exception:
    # Fallback for direct execution contexts
    from game import AdventureGame  # type: ignore


def main():
    game = AdventureGame()
    game.run()


if __name__ == "__main__":
    main()
