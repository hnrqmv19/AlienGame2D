import sys 
import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    """Gerencia o jogo e seus comportamentos."""

    def __init__(self):
        """Construtor da classe que inicializa o jogo e cria os recursos básicos"""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")
        
        # Instâncias principais
        self.ship = Ship(self.screen, self.settings)
        self.bg_color = self.settings.bg_color
        
        # Grupos de sprites
        self.bullets = pygame.sprite.Group() 
        self.aliens = pygame.sprite.Group() 
    
    def create_fleet(self):
        """Cria uma frota completa de alienígenas."""
        alien = Alien(self.screen, self.settings)
        alien_width = alien.rect.width
        alien_height = alien.rect.height
        
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)
        
        ship_height = self.ship.rect.height
        available_space_y = self.settings.screen_height - (3 * alien_height) - ship_height
        number_rows = available_space_y // (2 * alien_height)
        
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                alien = Alien(self.screen, self.settings)
                alien.x = alien_width + 2 * alien_width * alien_number
                alien.rect.x = alien.x
                alien.y = alien_height + 2 * alien_height * row_number
                alien.rect.y = alien.y
                self.aliens.add(alien)

    def _check_events(self):
        """Responde a eventos de pressionamento de teclas e de mouse."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.ship.moving_right = True
                elif event.key == pygame.K_LEFT:
                    self.ship.moving_left = True
                elif event.key == pygame.K_SPACE:
                    if len(self.bullets) < self.settings.bullet_allowed:
                        new_bullet = Bullet(self.screen, self.settings, self.ship)
                        self.bullets.add(new_bullet)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.ship.moving_right = False
                elif event.key == pygame.K_LEFT:
                    self.ship.moving_left = False

    def _update_bullets(self):
        """Atualiza a posição dos projéteis e descarta os antigos."""
        self.bullets.update()

        # Remove projéteis que saíram da tela
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        # Trata colisão entre projéteis e alienígenas
        pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        # Se toda a frota for destruída, limpa tiros e gera uma nova frota
        if len(self.aliens) == 0:
            self.bullets.empty()  # Remove projéteis restantes
            self.create_fleet()

    def _update_aliens(self):
        """Atualiza a posição de todos os alienígenas na frota."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                for a in self.aliens.sprites():
                    a.rect.y += self.settings.fleet_drop_speed
                self.settings.fleet_direction *= -1
                break

        self.aliens.update()

        # Verifica colisões entre alienígenas e a nave
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            print("A nave foi atingida!")
            sys.exit()

    def _update_screen(self):
        """Atualiza as imagens na tela e alterna para a nova tela."""
        self.screen.fill(self.bg_color)
        
        # Desenha a nave
        self.ship.blitme()
        
        # Desenha os projéteis
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
            
        # Desenha os alienígenas
        self.aliens.draw(self.screen)
        
        # Renderiza o frame atual na tela
        pygame.display.flip()

    def run_game(self):
        """Laço principal do jogo."""
        self.create_fleet()
        
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_aliens()
            self._update_screen()

if __name__ == '__main__':
    alien_invasion = AlienInvasion()
    alien_invasion.run_game()