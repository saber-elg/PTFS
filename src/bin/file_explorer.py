#!/usr/bin/env python3
import pygame
import os

class FileExplorer:
    def __init__(self, screen):
        self.screen = screen
        self.directory = os.path.expanduser("~/ptfs")
        self.icon_size = (64, 64)
        self.file_font = pygame.font.Font(None, 18)
        self.selected_file = None
        self.load_icons()

    def load_icons(self):
        self.folder_icon = pygame.image.load(os.path.join(self.directory, "sys", "icons", "folder.png"))
        self.folder_icon = pygame.transform.scale(self.folder_icon, self.icon_size)

        self.file_icon = pygame.image.load(os.path.join(self.directory, "sys", "icons", "file.png"))
        self.file_icon = pygame.transform.scale(self.file_icon, self.icon_size)

    def draw(self):
        files = os.listdir(self.directory)
        file_x, file_y = 50, 50
        gap = 10

        for file_name in files:
            file_rect = pygame.Rect(file_x, file_y, self.icon_size[0], self.icon_size[1])
            
            if os.path.isdir(os.path.join(self.directory, file_name)):
                self.screen.blit(self.folder_icon, file_rect.topleft)
            else:
                self.screen.blit(self.file_icon, file_rect.topleft)

            if file_rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(self.screen, (200, 200, 200), file_rect, width=2)

            file_label = self.file_font.render(file_name, True, (0, 0, 0))
            self.screen.blit(file_label, (file_x, file_y + self.icon_size[1] + gap))

            file_x += self.icon_size[0] + gap

            if file_x + self.icon_size[0] + gap > self.screen.get_width():
                file_x = 50
                file_y += self.icon_size[1] + gap + 20  # Adjusted vertical gap

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.handle_mouse_click()

    def handle_mouse_click(self):
        files = os.listdir(self.directory)
        file_x, file_y = 50, 50 + self.icon_size[1] + 30  # Adjusted starting position
        gap = 10

        for file_name in files:
            file_rect = pygame.Rect(file_x, file_y, self.icon_size[0], self.icon_size[1])

            if file_rect.collidepoint(pygame.mouse.get_pos()):
                selected_file_path = os.path.join(self.directory, file_name)

                if os.path.isdir(selected_file_path):
                    self.directory = selected_file_path
                else:
                    print(f"Selected file: {selected_file_path}")

                break

            file_x += self.icon_size[0] + gap

            if file_x + self.icon_size[0] + gap > self.screen.get_width():
                file_x = 50
                file_y += self.icon_size[1] + gap + 20  # Adjusted vertical gap

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("File Explorer")

    explorer = FileExplorer(screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        explorer.handle_events()
        explorer.draw()

        pygame.display.flip()

