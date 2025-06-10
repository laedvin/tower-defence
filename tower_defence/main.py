from pathlib import Path

import pygame

PROJECT_PATH = Path(__file__).parent
ASSETS_PATH = PROJECT_PATH / "assets"


class Unit:
    def __init__(self):
        self.radius = 10.0
        self.max_speed = 30.0
        self.x = self.radius
        self.y = self.radius
        self._vx = 1.0
        self._vy = 1.0

    @property
    def vx(self) -> float:
        return self._vx

    @vx.setter
    def vx(self, value):
        self._vx = min(max(value, -self.max_speed), self.max_speed)

    @property
    def vy(self) -> float:
        return self._vy

    @vy.setter
    def vy(self, value):
        self._vy = min(max(value, -self.max_speed), self.max_speed)

    def move(self, canvas_height, canvas_width) -> None:
        self.x += self.vx
        self.y += self.vy
        if self.x + self.radius >= canvas_width:
            self.vx = min(-self.vx, 0) * 0.9
            self.x = canvas_width - self.radius
        elif self.x - self.radius <= 0:
            self.vx = max(-self.vx, 0) * 0.9
            self.x = self.radius
        if self.y + self.radius >= canvas_height:
            self.vy = min(-self.vy, 0) * 0.9
            self.y = canvas_height - self.radius
        elif self.y - self.radius <= 0:
            self.vy = max(-self.vy, 0) * 0.9
            self.y = self.radius


class InputState:
    def __init__(self):
        self.k_left_held = False
        self.k_right_held = False
        self.k_up_held = False
        self.k_down_held = False


class UserInterface:
    def __init__(self) -> None:
        self.canvas_width = 640
        self.canvas_height = 480
        pygame.init()
        pygame.display.set_caption("Tower Defence")
        pygame.display.set_icon(pygame.image.load(ASSETS_PATH / "icon.png"))
        self.window = pygame.display.set_mode((self.canvas_width, self.canvas_height))
        self.clock = pygame.time.Clock()

        self.player = Unit()
        self.input_state = InputState()
        self.running = True

    def process_input(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                break
            if event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_RIGHT:
                        self.input_state.k_right_held = True
                    case pygame.K_LEFT:
                        self.input_state.k_left_held = True
                    case pygame.K_UP:
                        self.input_state.k_up_held = True
                    case pygame.K_DOWN:
                        self.input_state.k_down_held = True
            if event.type == pygame.KEYUP:
                match event.key:
                    case pygame.K_RIGHT:
                        self.input_state.k_right_held = False
                    case pygame.K_LEFT:
                        self.input_state.k_left_held = False
                    case pygame.K_UP:
                        self.input_state.k_up_held = False
                    case pygame.K_DOWN:
                        self.input_state.k_down_held = False

    def update(self) -> None:
        self.player.vx += self.input_state.k_right_held - self.input_state.k_left_held
        self.player.vy += self.input_state.k_down_held - self.input_state.k_up_held
        self.player.move(self.canvas_height, self.canvas_width)

    def render(self) -> None:
        self.window.fill((110, 170, 110))
        pygame.draw.circle(
            self.window,
            (200, 110, 110),
            (self.player.x, self.player.y),
            self.player.radius,
        )
        pygame.display.update()

    def run(self) -> None:
        while self.running:
            self.process_input()
            self.update()
            self.render()
            self.clock.tick(60)


if __name__ == "__main__":
    ui = UserInterface()
    ui.run()
