import pyray as rl
import os
from mazegenerator import MazeGenerator


def main() -> None:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    assets_path = os.path.join(script_dir, "..", "assets", "tiles")

    maze_width = 20
    maze_height = 15
    gen = MazeGenerator(size=(maze_width, maze_height), perfect=True)
    maze_data = gen.maze

    tile_size = 40
    screen_w = maze_width * tile_size
    screen_h = maze_height * tile_size
    rl.init_window(screen_w, screen_h, "Pacman Maze Renderer")
    rl.set_target_fps(60)

    # 3. Load Textures
    textures = {}
    for i in range(16):
        # We match the bitmask values (1,2,4,8) to your filenames
        # bin(i) creates the string "0000" through "1111"
        filename = f"{bin(i)[2:].zfill(4)}.png"
        full_image_path = os.path.join(assets_path, filename)

        if os.path.exists(full_image_path):
            image = rl.load_image(full_image_path)
            rl.image_resize(image, tile_size, tile_size)
            textures[i] = rl.load_texture_from_image(image)
            rl.unload_image(image)
        else:
            # Fallback: if 1111.png is missing, use 0000.png or a colored square
            print(f"Warning: File not found at {full_image_path}. Using fallback.")
            if 0 in textures:  # Use the empty/solid tile as fallback
                textures[i] = textures[0]

    while not rl.window_should_close():
        rl.begin_drawing()
        rl.clear_background(rl.BLACK)

        for y in range(len(maze_data)):
            for x in range(len(maze_data[y])):
                cell_value = maze_data[y][x]
                lookup_value = cell_value & 15
                if lookup_value in textures:
                    rl.draw_texture(
                        textures[lookup_value], x * tile_size, y * tile_size, rl.WHITE
                    )
                else:
                    rl.draw_rectangle(
                        x * tile_size + 10, y * tile_size + 10, 20, 20, rl.RED
                    )
        rl.draw_text("MAZE GENERATED", 10, screen_h - 25, 20, rl.YELLOW)
        rl.end_drawing()

    # 5. Cleanup
    for tex in textures.values():
        rl.unload_texture(tex)
    rl.close_window()


if __name__ == "__main__":
    main()
