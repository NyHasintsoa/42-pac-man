import math
from typing import TYPE_CHECKING, Dict

import pyray as pr

from src.graphic.component import GhostCharacter, PacmanCharacter, PageFrame
from src.graphic.page.parent import ParentPage
from src.model.enums import PageState

if TYPE_CHECKING:
    from src.graphic.main_window import MainWindow


class HowToPlayPage(ParentPage):
    def __init__(self, window: MainWindow) -> None:
        super().__init__(window)
        self.state = PageState.HELP_MENU
        self.page_frame = PageFrame(window.width, window.height)
        self.font_path = "assets/fonts/emulogic.ttf"
        self.font = pr.load_font(self.font_path)

        self.color_title = pr.Color(249, 44, 114, 255)
        self.color_headers = pr.Color(27, 199, 233, 255)
        self.color_text = pr.Color(255, 255, 255, 255)
        self.color_shadow = pr.Color(0, 0, 0, 255)
        self.color_accent = pr.Color(255, 255, 0, 255)
        self.color_footer = pr.Color(249, 44, 114, 255)

        self.sections = [
            {
                "header": "CONTROLS",
                "body": "USE THE KEYBOARD BUTTONS TO\nNAVIGATE THE MAZE.",
            },
            {
                "header": "OBJECTIVE",
                "body": "EAT ALL PELLETS IN THE MAZE\nWHILE AVOIDING GHOSTS.",
            },
            {
                "header": "POWER PELLET",
                "body": "EAT LARGE PELLETS TO WEAKEN\nGHOSTS AND EAT THEM.",
            },
            {
                "header": "SCORING",
                "body": """PELLETS: 10 PTS
POWER PELLETS: 50 PTS
GHOSTS: 200 PTS.
""",
            },
        ]

        dummy_maze = [[0]]
        self.pacman_preview = PacmanCharacter(
            maze_data=dummy_maze,
            pos_x=0,
            pos_y=0,
            speed=0.0,
            animation_speed=0.15,
            window=self.window,
        )
        self.ghost_preview = GhostCharacter(
            maze_data=dummy_maze,
            pos_x=0,
            pos_y=0,
            speed=0.0,
            animation_speed=0.15,
            window=self.window,
            score=200,
        )

    def unload(self) -> None:
        pr.unload_font(self.font)
        self.pacman_preview.unload()
        self.ghost_preview.unload()

    def _draw_text_with_shadow_ex(
        self,
        text: str,
        x: int,
        y: int,
        font_size: int,
        spacing: float,
        text_color: pr.Color,
        shadow_color: pr.Color,
        offset: int = 2,
    ) -> None:
        pr.draw_text_ex(
            self.font,
            text,
            pr.Vector2(x + offset, y + offset),
            font_size,
            spacing,
            shadow_color,
        )
        pr.draw_text_ex(
            self.font, text, pr.Vector2(x, y), font_size, spacing, text_color
        )

    def _draw_key_button(self, text: str, x: int, y: int, size: int) -> None:
        pr.draw_rectangle_rounded(
            pr.Rectangle(x, y + 4, size, size), 0.2, 8, pr.DARKGRAY
        )
        pr.draw_rectangle_rounded(
            pr.Rectangle(x, y, size, size), 0.2, 8, pr.LIGHTGRAY
        )
        pr.draw_rectangle_rounded_lines(
            pr.Rectangle(x, y, size, size), 0.2, 8, pr.WHITE
        )

        font_size = int(size * 0.4)
        text_size = pr.measure_text_ex(self.font, text, font_size, 2)
        tx = x + (size - text_size.x) / 2
        ty = y + (size - text_size.y) / 2
        pr.draw_text_ex(
            self.font, text, pr.Vector2(tx, ty), font_size, 2, pr.BLACK
        )

    def _draw_component_pacman(
        self,
        x: int,
        y: int,
        size: int,
        frame_index: int,
        rotation: float = 0.0,
    ) -> None:
        self.pacman_preview.scale = size
        self.pacman_preview.pixel_pos = pr.Vector2(x, y)
        self.pacman_preview.frame_index = frame_index
        self.pacman_preview.rotation = rotation
        self.pacman_preview.is_dead = False
        self.pacman_preview.render()

    def _draw_component_ghost(
        self,
        x: int,
        y: int,
        size: int,
        frame_index: int,
        is_edible: bool = False,
        look_id: int = 1,
    ) -> None:
        self.ghost_preview.scale = size
        self.ghost_preview.pixel_pos = pr.Vector2(x, y)
        self.ghost_preview.frame_index = frame_index
        self.ghost_preview.is_edible = is_edible
        self.ghost_preview.look_id = look_id
        self.ghost_preview.render()

    def _event_listener(self) -> None:
        if pr.is_key_pressed(pr.KeyboardKey.KEY_ESCAPE) or pr.is_key_pressed(
            pr.KeyboardKey.KEY_ENTER
        ):
            self.next_state = PageState.MAIN_MENU

    def _render_section_card(
        self,
        sec: Dict[str, str],
        box_x: int,
        box_y: int,
        cell_width: int,
        cell_height: int,
        header_font_size: int,
        body_font_size: int,
        spacing: float,
    ) -> None:
        pr.draw_rectangle_rounded(
            pr.Rectangle(box_x, box_y, cell_width, cell_height),
            0.08,
            8,
            pr.Color(15, 15, 40, 255),
        )
        pr.draw_rectangle_rounded_lines(
            pr.Rectangle(box_x, box_y, cell_width, cell_height),
            0.08,
            8,
            pr.Color(27, 199, 233, 100),
        )

        header_size_vec = pr.measure_text_ex(
            self.font, sec["header"], header_font_size, spacing
        )
        header_x = box_x + (cell_width - header_size_vec.x) // 2
        self._draw_text_with_shadow_ex(
            sec["header"],
            int(header_x),
            box_y + int(cell_height * 0.1),
            header_font_size,
            spacing,
            self.color_headers,
            self.color_shadow,
        )

        padding_left = int(cell_width * 0.05)
        self._draw_text_with_shadow_ex(
            sec["body"],
            box_x + padding_left,
            box_y + int(cell_height * 0.27),
            body_font_size,
            spacing,
            self.color_text,
            self.color_shadow,
        )

    def _render_section_visuals(
        self,
        header: str,
        box_x: int,
        box_y: int,
        cell_width: int,
        cell_height: int,
        total_time: float,
        global_frame_tick: int,
        spacing: float,
    ) -> None:
        visual_area_y = box_y + int(cell_height * 0.72)
        sprite_size = int(cell_height * 0.18)

        if header == "CONTROLS":
            key_size = int(cell_height * 0.12)
            offset_k = int(key_size * 1.15)

            wasd_center_x = box_x + int(cell_width * 0.30)
            self._draw_key_button(
                "W",
                wasd_center_x - (key_size // 2),
                visual_area_y - offset_k,
                key_size,
            )
            self._draw_key_button(
                "A",
                wasd_center_x - (key_size // 2) - offset_k,
                visual_area_y,
                key_size,
            )
            self._draw_key_button(
                "S", wasd_center_x - (key_size // 2), visual_area_y, key_size
            )
            self._draw_key_button(
                "D",
                wasd_center_x - (key_size // 2) + offset_k,
                visual_area_y,
                key_size,
            )

            arrows_center_x = box_x + int(cell_width * 0.70)
            self._draw_key_button(
                "^",
                arrows_center_x - (key_size // 2),
                visual_area_y - offset_k,
                key_size,
            )
            self._draw_key_button(
                "<",
                arrows_center_x - (key_size // 2) - offset_k,
                visual_area_y,
                key_size,
            )
            self._draw_key_button(
                "v", arrows_center_x - (key_size // 2), visual_area_y, key_size
            )
            self._draw_key_button(
                ">",
                arrows_center_x - (key_size // 2) + offset_k,
                visual_area_y,
                key_size,
            )

        elif header == "OBJECTIVE":
            track_width = int(cell_width * 0.7)
            track_start_x = box_x + (cell_width - track_width) // 2

            raw_progress = (total_time * (track_width * 0.4)) % (
                track_width * 2
            )
            if raw_progress > track_width:
                pac_x = track_start_x + (track_width * 2 - raw_progress)
                rotation_angle = 180.0
            else:
                pac_x = track_start_x + raw_progress
                rotation_angle = 0.0

            for dot_idx in range(6):
                dot_x = (
                    track_start_x
                    + int(track_width * 0.05)
                    + (dot_idx * int(track_width * 0.18))
                )
                if (rotation_angle == 0.0 and dot_x > pac_x) or (
                    rotation_angle == 180.0 and dot_x < pac_x
                ):
                    pr.draw_circle(
                        int(dot_x),
                        int(visual_area_y),
                        4,
                        pr.Color(255, 255, 255, 255),
                    )

            self._draw_component_pacman(
                int(pac_x),
                int(visual_area_y),
                sprite_size,
                global_frame_tick,
                rotation_angle,
            )

        elif header == "POWER PELLET":
            track_width = int(cell_width * 0.7)
            track_start_x = box_x + (cell_width - track_width) // 2

            animation_duration = 4.0
            timer_seq = total_time % animation_duration
            normalized_progress = timer_seq / animation_duration

            pac_x = track_start_x + (normalized_progress * track_width)
            pellet_x = track_start_x + int(track_width * 0.35)
            ghost_x = track_start_x + int(track_width * 0.75)

            is_past_pellet = pac_x >= pellet_x
            is_ghost_eaten = pac_x >= ghost_x

            if not is_past_pellet:
                pellet_pulse = 6 + int(abs(math.sin(total_time * 6.0)) * 3)
                pr.draw_circle(
                    int(pellet_x),
                    int(visual_area_y),
                    pellet_pulse,
                    self.color_accent,
                )

            distance_to_ghost = abs(pac_x - ghost_x)

            if not is_ghost_eaten:
                if distance_to_ghost > 15:
                    ghost_scared = is_past_pellet
                    self._draw_component_ghost(
                        int(ghost_x),
                        int(visual_area_y),
                        sprite_size,
                        global_frame_tick,
                        is_edible=ghost_scared,
                        look_id=1,
                    )
            else:
                self._draw_text_with_shadow_ex(
                    str(self.context.config.points_per_ghost),
                    int(ghost_x),
                    int(visual_area_y - (sprite_size // 2)),
                    10,
                    spacing,
                    pr.Color(0, 255, 255, 255),
                    self.color_shadow,
                )

            self._draw_component_pacman(
                int(pac_x),
                int(visual_area_y),
                sprite_size,
                global_frame_tick,
                rotation=0.0,
            )

        elif header == "SCORING":
            scoring_center_x = box_x + (cell_width // 2)
            offset_w = int(cell_width * 0.18)

            pr.draw_circle(
                int(scoring_center_x - offset_w),
                int(visual_area_y),
                4,
                pr.WHITE,
            )
            self._draw_text_with_shadow_ex(
                str(self.context.config.points_per_pacgum),
                int(scoring_center_x - offset_w + 20),
                int(visual_area_y - 6),
                12,
                spacing,
                self.color_text,
                self.color_shadow,
            )

            pr.draw_circle(
                int(scoring_center_x), int(visual_area_y), 8, self.color_accent
            )
            self._draw_text_with_shadow_ex(
                str(self.context.config.points_per_super_pacgum),
                int(scoring_center_x + 20),
                int(visual_area_y - 6),
                12,
                spacing,
                self.color_text,
                self.color_shadow,
            )

            self._draw_component_ghost(
                int(scoring_center_x + offset_w),
                int(visual_area_y),
                sprite_size,
                global_frame_tick,
                is_edible=True,
            )
            self._draw_text_with_shadow_ex(
                str(self.context.config.points_per_ghost),
                int(scoring_center_x + offset_w + int(sprite_size * 0.6)),
                int(visual_area_y - 6),
                12,
                spacing,
                self.color_text,
                self.color_shadow,
            )

    def render(self) -> None:
        self._event_listener()
        self.page_frame.render()
        total_time = pr.get_time()
        spacing = 2
        global_frame_tick = int(total_time / 0.15)

        width = self.window.width
        height = self.window.height

        title_font_size = int(width * 0.035)
        header_font_size = int(width * 0.015)
        body_font_size = int(width * 0.010)

        title_text = "HOW TO PLAY"
        title_size_vec = pr.measure_text_ex(
            self.font, title_text, title_font_size, spacing
        )
        title_x = (width - title_size_vec.x) // 2
        pr.draw_text_ex(
            self.font,
            title_text,
            pr.Vector2(title_x, int(height * 0.06)),
            title_font_size,
            spacing,
            self.color_title,
        )

        grid_cols = 2
        gap_x = int(width * 0.04)
        gap_y = int(height * 0.04)

        total_grid_w = int(width * 0.82)
        total_grid_h = int(height * 0.58)

        cell_width = (total_grid_w - gap_x) // grid_cols
        cell_height = (total_grid_h - gap_y) // grid_cols

        start_x = (width - total_grid_w) // 2
        start_y = int(height * 0.18) + (int(height * 0.66) - total_grid_h) // 2

        for i, sec in enumerate(self.sections):
            col = i % grid_cols
            row = i // grid_cols

            box_x = start_x + col * (cell_width + gap_x)
            box_y = start_y + row * (cell_height + gap_y)

            self._render_section_card(
                sec,
                box_x,
                box_y,
                cell_width,
                cell_height,
                header_font_size,
                body_font_size,
                spacing,
            )

            self._render_section_visuals(
                sec["header"],
                box_x,
                box_y,
                cell_width,
                cell_height,
                total_time,
                global_frame_tick,
                spacing,
            )

        alpha_pulse = int(130 + 125 * math.cos(total_time * 4.5))
        footer_color = pr.Color(
            self.color_footer.r,
            self.color_footer.g,
            self.color_footer.b,
            alpha_pulse,
        )

        footer_text = "PRESS [ESC] OR [ENTER] TO RETURN TO MENU"
        footer_font_size = int(width * 0.012)
        footer_size_vec = pr.measure_text_ex(
            self.font, footer_text, footer_font_size, spacing
        )
        footer_x = (width - footer_size_vec.x) // 2
        pr.draw_text_ex(
            self.font,
            footer_text,
            pr.Vector2(footer_x, height - int(height * 0.08)),
            footer_font_size,
            spacing,
            footer_color,
        )
