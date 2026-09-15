"""Define shared movement and rendering behavior for characters."""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, List

import pyray as pr

from src.graphic.utils import ResourceManager

if TYPE_CHECKING:
    from src.graphic.main_window import MainWindow


class CharacterComponent(ABC):
    """Provide shared state and behavior for moving characters."""

    def __init__(
        self,
        maze_data: List[List[int]],
        pos_x: int,
        pos_y: int,
        speed: float,
        animation_speed: float,
        window: "MainWindow",
        margin_top: int = 80,
        margin_bottom: int = 30,
        padding_x: int = 20,
    ) -> None:
        """Initialize the CharacterComponent instance.

        Args:
            maze_data: The maze grid encoded with wall bit flags.
            pos_x: The horizontal position or grid coordinate.
            pos_y: The vertical position or grid coordinate.
            speed: The movement speed in pixels per frame.
            animation_speed: The interval between animation frames.
            window: The application window owning the component.
            margin_top: The top layout margin in pixels.
            margin_bottom: The bottom layout margin in pixels.
            padding_x: The horizontal layout padding in pixels.

        Returns:
            The requested result.
        """
        self.maze_data = maze_data
        self.grid_cols = len(maze_data[0]) if maze_data else 0
        self.grid_rows = len(maze_data) if maze_data else 0
        self.animation_speed = animation_speed
        self.assets_path: str
        self._loaded_textures: List[pr.Texture] = []
        self._is_unloaded = False
        available_width = float(window.width - (padding_x * 2))
        available_height = float(
            window.height - margin_top - (padding_x * 2) - margin_bottom
        )
        scale_x = (
            available_width / self.grid_cols if self.grid_cols > 0 else 1.0
        )
        scale_y = (
            available_height / self.grid_rows if self.grid_rows > 0 else 1.0
        )
        self.scale = min(scale_x, scale_y)

        self.offset_x = (window.width - (self.grid_cols * self.scale)) / 2.0
        self.offset_y = (
            margin_top
            + (available_height - (self.grid_rows * self.scale)) / 2.0
        )
        self.speed = speed
        self.grid_pos = pr.Vector2(pos_x, pos_y)
        self.pixel_pos = self.get_pixel_position(self.grid_pos)
        self.direction = pr.Vector2(0, 0)
        self.next_direction = pr.Vector2(0, 0)
        self.frame_index = 0
        self.frame_timer = 0.0
        self.load_textures()

    def get_pixel_position(self, grid_pos: pr.Vector2) -> pr.Vector2:
        """Convert a grid coordinate to the corresponding pixel center.

        Args:
            grid_pos: The grid position to convert.

        Returns:
            The pixel center corresponding to the grid position.
        """
        return pr.Vector2(
            grid_pos.x * self.scale + self.offset_x + (self.scale / 2.0),
            grid_pos.y * self.scale + self.offset_y + (self.scale / 2.0),
        )

    def load_tex(self, filename: str, fallback_color: pr.Color) -> pr.Texture:
        """Load an asset texture or create a colored fallback texture.

        Args:
            filename: The asset or score filename.
            fallback_color: The color used when an asset is unavailable.

        Returns:
            The loaded or fallback texture.
        """
        path = ResourceManager.path(self.assets_path, filename)
        size = int(self.scale) if int(self.scale) > 0 else 1

        img = pr.load_image(path)
        pr.image_resize(img, size, size)
        tex = pr.load_texture_from_image(img)
        pr.unload_image(img)
        self._loaded_textures.append(tex)
        return tex

    def check_wall_collision(self, gx: int, gy: int, dx: int, dy: int) -> bool:
        """Return whether a movement step is blocked by maze walls.

        Args:
            gx: The current grid x coordinate.
            gy: The current grid y coordinate.
            dx: The horizontal movement delta in tiles.
            dy: The vertical movement delta in tiles.

        Returns:
            True when movement is blocked; otherwise False.
        """
        if not (0 <= gx < self.grid_cols and 0 <= gy < self.grid_rows):
            return True
        cell = self.maze_data[int(gy)][int(gx)]
        if cell == 15:
            return True
        if dy == -1 and (cell & 1):
            return True
        if dx == 1 and (cell & 2):
            return True
        if dy == 1 and (cell & 4):
            return True
        if dx == -1 and (cell & 8):
            return True

        nx, ny = int(gx + dx), int(gy + dy)
        if 0 <= nx < self.grid_cols and 0 <= ny < self.grid_rows:
            next_cell = self.maze_data[ny][nx]
            if next_cell == 15:
                return True
            if dy == 1 and (next_cell & 1):
                return True
            if dx == -1 and (next_cell & 2):
                return True
            if dy == -1 and (next_cell & 4):
                return True
            if dx == 1 and (next_cell & 8):
                return True
            return False
        return True

    def update_movement_and_grid(self) -> None:
        """Move the component and synchronize its grid position.

        Returns:
            The requested result.
        """
        center = self.get_pixel_position(self.grid_pos)
        if (
            abs(self.pixel_pos.x - center.x) < self.speed
            and abs(self.pixel_pos.y - center.y) < self.speed
        ):
            if not self.check_wall_collision(
                int(self.grid_pos.x),
                int(self.grid_pos.y),
                int(self.next_direction.x),
                int(self.next_direction.y),
            ):
                self.direction = self.next_direction
                self.on_direction_changed()
            if self.check_wall_collision(
                int(self.grid_pos.x),
                int(self.grid_pos.y),
                int(self.direction.x),
                int(self.direction.y),
            ):
                self.direction = pr.Vector2(0, 0)
                self.pixel_pos = center

        self.pixel_pos.x += self.direction.x * self.speed
        self.pixel_pos.y += self.direction.y * self.speed

        self.grid_pos.x = int((self.pixel_pos.x - self.offset_x) // self.scale)
        self.grid_pos.y = int((self.pixel_pos.y - self.offset_y) // self.scale)

    def update_animation_timer(self) -> None:
        """Advance the animation frame timer.

        Returns:
            The requested result.
        """
        self.frame_timer += pr.get_frame_time()
        if self.frame_timer >= self.animation_speed:
            self.frame_timer = 0.0
            self.frame_index += 1

    def unload(self) -> None:
        """Release graphical resources owned by the component.

        Returns:
            The requested result.
        """
        if self._is_unloaded:
            return
        for texture in list(self._loaded_textures):
            pr.unload_texture(texture)
        self._loaded_textures.clear()
        self._is_unloaded = True

    @abstractmethod
    def load_textures(self) -> None:
        """Load textures required by the concrete character.

        Returns:
            The requested result.
        """
        pass

    @abstractmethod
    def render(self) -> None:
        """Render the component for the current frame.

        Returns:
            The requested result.
        """
        pass

    @abstractmethod
    def on_direction_changed(self) -> None:
        """Update direction-dependent visual state.

        Returns:
            The requested result.
        """
        pass
