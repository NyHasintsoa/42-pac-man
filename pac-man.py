from src.graphic import MainWindow


def main() -> None:
    print("Hello from pacman!")
    window = MainWindow(1000, 1000, "Pacman")
    window.add_event()
    window.render()


if __name__ == "__main__":
    main()
