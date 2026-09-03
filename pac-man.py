from src.graphic.main_window import MainWindow


def main() -> None:
    window = MainWindow(1500, 1000, "Pacman")
    window.add_event()
    window.load_page()
    window.render()


if __name__ == "__main__":
    main()
