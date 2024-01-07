#!/usr/bin/env python3
import pygame
import os
from desktop_page import DesktopPage


# Constants for paths
ICONS_PATH = os.path.join(os.path.expanduser("~/ptfs"), "sys", "icons")
IMAGES_PATH = os.path.join(os.path.expanduser("~/ptfs"), "sys", "images")

class LoginScreen:
    def __init__(self, screen, auth_manager):
        # Initialize Pygame screen, clock, and fonts
        self.screen = screen
        self.auth_manager = auth_manager
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 22)
        self.input_font = pygame.font.Font(None, 26)
        self.selected_account = None
        self.password = ""
        self.show_password_input = False
        self.state = "user_selection"  # Possible states: "user_selection", "login"

        # Load and scale the shutdown icon
        self.shutdown_icon = pygame.image.load(os.path.join(ICONS_PATH, "off.png"))
        self.shutdown_icon = pygame.transform.scale(self.shutdown_icon, (40, 40))
        self.shutdown_button_rect = self.shutdown_icon.get_rect(midbottom=(screen.get_width() // 2, screen.get_height() - 30))

    def draw(self):
        # Draw the background image
        background_image = pygame.image.load(os.path.join(IMAGES_PATH, "background1.jpg"))
        background_image = pygame.transform.scale(background_image, (self.screen.get_width(), self.screen.get_height()))
        self.screen.blit(background_image, (0, 0))

        if self.state == "user_selection":
            self.draw_user_selection()
        elif self.state == "login":
            self.draw_login()

        pygame.display.flip()

    def draw_user_selection(self):
        account_x = (self.screen.get_width() - (80 + 20) * len(self.auth_manager.users_data)) // 2
        account_y = self.screen.get_height() // 4
        user_icon_path = os.path.join(ICONS_PATH, "user.png")

        for username in self.auth_manager.users_data.keys():
            account_rect = pygame.Rect(account_x, account_y, 80, 80)
            background_color = (0, 255, 0) if self.selected_account == username else (255, 255, 255)
            pygame.draw.rect(self.screen, background_color, account_rect, border_radius=10)

            user_icon = pygame.image.load(user_icon_path)
            user_icon = pygame.transform.scale(user_icon, (30, 30))
            self.screen.blit(user_icon, (account_rect.centerx - 15, account_rect.y + 10))

            account_label = self.font.render(username, True, (0, 0, 0))
            self.screen.blit(account_label, (account_rect.centerx - account_label.get_width() // 2, account_rect.y + 50))

            account_x += 80 + 20

    def draw_login(self):
        account_rect = pygame.Rect((self.screen.get_width() - 80) // 2, self.screen.get_height() // 4, 80, 80)
        pygame.draw.rect(self.screen, (255, 255, 255), account_rect, border_radius=10)

        user_icon_path = os.path.join(ICONS_PATH, "user.png")
        user_icon = pygame.image.load(user_icon_path)
        user_icon = pygame.transform.scale(user_icon, (30, 30))
        self.screen.blit(user_icon, (account_rect.centerx - 15, account_rect.y + 10))

        account_label = self.font.render(self.selected_account, True, (0, 0, 0))
        self.screen.blit(account_label, (account_rect.centerx - account_label.get_width() // 2, account_rect.y + 50))

        password_label = self.font.render("Password:", True, (0, 0, 0))
        password_label_rect = password_label.get_rect(midleft=(self.screen.get_width() // 4 + 10, self.screen.get_height() // 2))
        self.screen.blit(password_label, password_label_rect.topleft)

        password_rect = pygame.Rect(self.screen.get_width() // 4 + 120, self.screen.get_height() // 2 - 10, 250, 40)
        pygame.draw.rect(self.screen, (255, 255, 255), password_rect, border_radius=10)
        password_input = self.input_font.render("*" * len(self.password), True, (50, 50, 50))
        self.screen.blit(password_input, (self.screen.get_width() // 4 + 130, self.screen.get_height() // 2 - 5))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.state == "user_selection":
                        if self.selected_account:
                            self.state = "login"
                    elif self.state == "login":
                        if self.selected_account and self.password:
                            if self.auth_manager.authenticate_user(self.selected_account, self.password):
                                desktop_page = DesktopPage(self.screen, self.auth_manager)
                                desktop_page.run()
                            else:
                                print("Invalid password.")
                elif event.key == pygame.K_TAB:
                    if self.state == "user_selection":
                        if self.selected_account is None:
                            self.selected_account = list(self.auth_manager.users_data.keys())[0]
                            self.show_password_input = True
                        elif self.show_password_input:
                            self.show_password_input = False
                        else:
                            self.selected_account = None
                    elif self.state == "login" and self.show_password_input:
                        self.show_password_input = False
                elif event.key == pygame.K_BACKSPACE:
                    if self.state == "login" and self.password:
                        self.password = self.password[:-1]
                else:
                    if event.unicode.isalnum() and self.show_password_input:
                        self.password += event.unicode

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.shutdown_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    quit()

                if self.state == "user_selection":
                    self.handle_user_selection_click(event.pos)
                elif self.state == "login":
                    pass

    def handle_user_selection_click(self, click_pos):
        account_x = (self.screen.get_width() - (80 + 20) * len(self.auth_manager.users_data)) // 2
        account_y = self.screen.get_height() // 4

        for username in self.auth_manager.users_data.keys():
            account_rect = pygame.Rect(account_x, account_y, 80, 80)
            if account_rect.collidepoint(click_pos):
                self.selected_account = username
                self.show_password_input = True
                self.state = "login"
                break
            account_x += 80 + 20

    def run(self):
        while True:
            self.handle_events()
            self.draw()
            self.clock.tick(30)

