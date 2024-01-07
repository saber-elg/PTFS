import pygame
import os
import datetime
from authentication_manager import AuthenticationManager

ICONS_PATH = os.path.join(os.path.expanduser("~/ptfs"), "sys", "icons")
IMAGES_PATH = os.path.join(os.path.expanduser("~/ptfs"), "sys", "images")

class FileExplorer:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.background_color = (255, 255, 255)
        self.current_path = os.path.expanduser("~/ptfs")
        self.font = pygame.font.Font(None, 18)
        self.selected_index = 0

        self.update_file_list()

    def update_file_list(self):
        self.file_list = os.listdir(self.current_path)

    def draw(self):
        self.screen.fill(self.background_color)

        for i, file_name in enumerate(self.file_list):
            text_color = (0, 0, 0) if i != self.selected_index else (255, 0, 0)
            text = self.font.render(file_name, True, text_color)
            self.screen.blit(text, (50, 50 + i * 20))

        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_index = max(0, self.selected_index - 1)
                elif event.key == pygame.K_DOWN:
                    self.selected_index = min(len(self.file_list) - 1, self.selected_index + 1)
                elif event.key == pygame.K_RETURN:
                    selected_item = os.path.join(self.current_path, self.file_list[self.selected_index])
                    if os.path.isdir(selected_item):
                        self.current_path = selected_item
                        self.update_file_list()
                        self.selected_index = 0
                    else:
                        self.open_file(selected_item)

    def open_file(self, file_path):
        # Implement the logic to open or handle the selected file here
        print(f"Opening file: {file_path}")

    def run(self):
        while True:
            self.handle_events()
            self.draw()
            self.clock.tick(30)

class DesktopPage:
    def __init__(self, screen, auth_manager):
        self.screen = screen
        self.auth_manager = auth_manager
        self.clock = pygame.time.Clock()
        self.exit_icon = pygame.image.load(os.path.join(ICONS_PATH, "off.png"))
        self.exit_icon = pygame.transform.scale(self.exit_icon, (40, 40))
        self.exit_button_rect = self.exit_icon.get_rect(bottomright=(screen.get_width() - 20, screen.get_height() - 20))

        self.terminal_icon = pygame.image.load(os.path.join(ICONS_PATH, "terminal.png"))
        self.terminal_icon = pygame.transform.scale(self.terminal_icon, (40, 40))
        self.terminal_button_rect = self.terminal_icon.get_rect(topleft=(20, 20))

        self.explorer_icon = pygame.image.load(os.path.join(ICONS_PATH, "explorer.png"))
        self.explorer_icon = pygame.transform.scale(self.explorer_icon, (40, 40))
        self.explorer_button_rect = self.explorer_icon.get_rect(topleft=(80, 20))  # Adjusted position

        self.terminal_opened = False
        self.terminal_font = pygame.font.Font(None, 18)
        self.terminal_input = ""
        self.terminal_output = []

        self.file_explorer = None
        self.explorer_opened = False

    def draw(self):
        background_image = pygame.image.load(os.path.join(IMAGES_PATH, "background.jpg"))
        background_image = pygame.transform.scale(background_image, (self.screen.get_width(), self.screen.get_height()))
        self.screen.blit(background_image, (0, 0))

        self.screen.blit(self.exit_icon, self.exit_button_rect.topleft)
        self.screen.blit(self.terminal_icon, self.terminal_button_rect.topleft)
        self.screen.blit(self.explorer_icon, self.explorer_button_rect.topleft)

        self.draw_date_and_time()

        if self.terminal_opened:
            self.draw_terminal()

        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.exit_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    quit()
                elif self.terminal_button_rect.collidepoint(event.pos):
                    self.toggle_terminal()
                elif self.explorer_button_rect.collidepoint(event.pos):
                    self.toggle_file_explorer()

        if self.terminal_opened:
            self.handle_terminal_events()

        if self.explorer_opened:
            self.file_explorer.handle_events()

    def draw_terminal(self):
        pygame.draw.rect(self.screen, (0, 0, 0), (50, 50, self.screen.get_width() - 100, self.screen.get_height() - 100))

        for i, line in enumerate(self.terminal_output):
            text = self.terminal_font.render(line, True, (255, 255, 255))
            self.screen.blit(text, (60, 60 + i * 20))

        input_text = self.terminal_font.render(">" + self.terminal_input, True, (255, 255, 255))
        self.screen.blit(input_text, (60, self.screen.get_height() - 60))

    def handle_terminal_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.process_terminal_command()
                elif event.key == pygame.K_BACKSPACE:
                    self.terminal_input = self.terminal_input[:-1]
                elif event.key == pygame.K_ESCAPE:
                    self.toggle_terminal()
                else:
                    self.terminal_input += event.unicode

    def process_terminal_command(self):
        command = self.terminal_input
        self.terminal_output.append(f"> {command}")
        try:
            output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
            self.terminal_output.extend(output.splitlines())
        except subprocess.CalledProcessError as e:
            self.terminal_output.append(f"Error: {e.output}")

        self.terminal_input = ""

    def toggle_terminal(self):
        subprocess.run(["gnome-terminal", "--working-directory=" + os.path.expanduser("~/ptfs")])
        pygame.quit()
        quit()

    def toggle_file_explorer(self):
        if not self.explorer_opened:
            self.file_explorer = FileExplorer(self.screen)
            self.explorer_opened = True
        else:
            self.explorer_opened = False

    def draw_date_and_time(self):
        now = datetime.datetime.now()
        date_time_str = now.strftime("%a %d %b %Y %H:%M")
        date_time_font = pygame.font.Font(None, 20)
        date_time_text = date_time_font.render(date_time_str, True, (0, 0, 0))
        date_time_rect = date_time_text.get_rect(midbottom=(self.screen.get_width() // 2, self.screen.get_height() - 10))
        self.screen.blit(date_time_text, date_time_rect.topleft)

    def run(self):
        while True:
            self.handle_events()
            self.draw()
            self.clock.tick(30)

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600), pygame.FULLSCREEN)
    pygame.display.set_caption("Desktop Page")

    auth_manager = AuthenticationManager({})

    desktop_page = DesktopPage(screen, auth_manager)
    desktop_page.run()

