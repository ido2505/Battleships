import pygame
import pygame_gui
import ipaddress


class MenuUI:
    MENU_WINDOW_HEIGHT = 600
    MENU_WINDOW_WIDTH = 220

    TEXT_BOX_X_POSITION = 10
    TEXT_BOX_Y_POSITION = 110
    TEXT_BOX_WIDTH = 200
    TEXT_BOX_HEIGHT = 40

    UI_CLOCK_TICKS = 30
    UI_REFRESH_RATE = UI_CLOCK_TICKS / 1000

    BACKGROUND_COLOR = (255, 255, 255)

    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((self.MENU_WINDOW_WIDTH, self.MENU_WINDOW_WIDTH))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 30)

        self.menu_buttons = {Button(self.screen, self.font, 'Server', 200, 40, (10, 10), 5): False,
                             Button(self.screen, self.font, 'Connect', 200, 40, (10, 60), 5): False}

        self.text_box_ui_manager = pygame_gui.UIManager((self.MENU_WINDOW_WIDTH, self.MENU_WINDOW_HEIGHT))
        self.text_box = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(
            (self.TEXT_BOX_X_POSITION, self.TEXT_BOX_Y_POSITION),
            (self.TEXT_BOX_WIDTH, self.TEXT_BOX_HEIGHT)),
            manager=self.text_box_ui_manager,
            object_id='#ip_text_entry'
        )

        self.run_menu()

    def run_menu(self):
        """
        this function is the main menu loop
        """
        menu_running = True
        count_until_quit = 10
        text_box_ip_address = ""

        while menu_running:
            # fill background
            self.screen.fill(self.BACKGROUND_COLOR)

            self.draw_buttons()

            self.check_buttons_click()

            events = pygame.event.get()

            # check for events
            for event in events:
                if event.type == pygame.QUIT:
                    menu_running = False
                if event.type == pygame_gui.UI_TEXT_ENTRY_CHANGED:
                    text_box_ip_address = str(event.text)

                self.text_box_ui_manager.process_events(event)

            for button_pressed in self.menu_buttons.values():
                if button_pressed:
                    count_until_quit -= 1
                    if count_until_quit == 0:
                        print(text_box_ip_address)
                        menu_running = False
                        break

            self.text_box_ui_manager.update(self.UI_REFRESH_RATE)
            self.text_box_ui_manager.draw_ui(self.screen)

            pygame.display.update()
            self.clock.tick(self.UI_CLOCK_TICKS)

        pygame.quit()

    def draw_buttons(self):
        for button in self.menu_buttons:
            button.draw()

    def check_buttons_click(self):
        for button in self.menu_buttons:
            if button.check_click():
                self.menu_buttons[button] = True

    def check_connection_address(self) -> bool:


        try:
            ipaddress.ip_address(ip_address)
        except ValueError:
            return False
        return True


class Button:
    def __init__(self, screen, gui_font, text, width, height, pos, elevation):
        self.screen = screen
        self.gui_font = gui_font

        # Core attributes
        self.pressed = False
        self.elevation = elevation
        self.dynamic_elevation = elevation
        self.original_y_pos = pos[1]

        # top rectangle
        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = '#475F77'

        # bottom rectangle
        self.bottom_rect = pygame.Rect(pos, (width, height))
        self.bottom_color = '#354B5E'
        # text
        self.text = text
        self.text_surf = gui_font.render(text, True, '#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

    def change_text(self, new_text):
        self.text_surf = self.gui_font.render(new_text, True, '#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

    def draw(self):
        # elevation logic
        self.top_rect.y = self.original_y_pos - self.dynamic_elevation
        self.text_rect.center = self.top_rect.center

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elevation

        pygame.draw.rect(self.screen, self.bottom_color, self.bottom_rect, border_radius=12)
        pygame.draw.rect(self.screen, self.top_color, self.top_rect, border_radius=12)
        self.screen.blit(self.text_surf, self.text_rect)
        # self.check_click()

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = '#D74B4B'
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elevation = 0
                self.pressed = True
                self.change_text(f"{self.text}")
            else:
                self.dynamic_elevation = self.elevation
                if self.pressed:
                    self.pressed = False
                    self.change_text(self.text)
                    return True
        else:
            self.dynamic_elevation = self.elevation
            self.top_color = '#475F77'

        return False
