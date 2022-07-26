from bdb import Breakpoint
from random import randint
import os

import pygame as pg

from . import *
from .objects import BigAlienShip, BigAsteroid, EndGame2Texts, Explosion, Hit, InputBox, Planet, Scoreboard1, Scoreboard2, Shot, SmallAlienShip, SmallAsteroid, SpaceShip
from .records import DBManager


class Scene:
    def __init__(self, screen: pg.Surface):
        self.display = screen
        self.clock = pg.time.Clock()

    def main_loop(self):
        pass


class Front(Scene):

    def __init__(self, screen: pg.Surface):
        super().__init__(screen)
        image_background = pg.image.load(os.path.join(
            "resources", "background", "bg-preview-big.png"))
        self.background = pg.transform.scale2x(image_background)
        self.font_file = os.path.join(
            "resources", "fonts", "PublicPixel-z84yD.ttf")

    def main_loop(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        print("Exiting")
                        return
                    if event.key == pg.K_SPACE:
                        return

                if event.type == pg.QUIT:
                    print("Exiting!")
                    pg.quit()

            self.draw_background()
            self.draw_title()
            self.draw_text1()
            self.draw_text2()
            pg.display.flip()
            self.clock.tick(FPS)

    def draw_background(self):
        self.display.blit(self.background, (0, 0))

    def draw_title(self):
        # Título del juego
        typography = pg.font.Font(self.font_file, 100)
        message = "The Quest"
        text = pg.font.Font.render(typography, message, True, C_YELLOW)
        text_width = text.get_width()
        pos_x = (WIDTH-text_width)/2
        pos_y = 0.15 * HEIGHT
        self.display.blit(text, (pos_x, pos_y))

    def draw_text1(self):
        # Instrucciones del juego
        typography = pg.font.Font(self.font_file, 16)
        message = "¡Usa flecha arriba y abajo para esquivar los obstáculos!"
        text = pg.font.Font.render(typography, message, True, C_YELLOW)
        text_width = text.get_width()
        pos_x = (WIDTH-text_width)/2
        pos_y = 0.50 * HEIGHT
        self.display.blit(text, (pos_x, pos_y))

    def draw_text2(self):
        # Texto indicativo
        typography = pg.font.Font(self.font_file, 16)
        message = "Pulsa Espacio para empezar a jugar, ESC para salir, R si quieres reiniciar partida"
        text = pg.font.Font.render(typography, message, True, C_YELLOW)
        text_width = text.get_width()
        pos_x = (WIDTH-text_width)/2
        pos_y = 0.75 * HEIGHT
        self.display.blit(text, (pos_x, pos_y))


class Story(Scene):

    def __init__(self, screen: pg.Surface):
        super().__init__(screen)
        image_background = pg.image.load(os.path.join(
            "resources", "background", "bg-preview-big.png"))
        self.background = pg.transform.scale2x(image_background)
        self.font_file = os.path.join(
            "resources", "fonts", "PublicPixel-z84yD.ttf")

    def main_loop(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        print("Exiting")
                        return
                    if event.key == pg.K_SPACE:
                        return None
                if event.type == pg.QUIT:
                    print("Exiting!")
                    pg.quit()

            self.draw_background()
            self.draw_text()
            self.draw_text1()
            self.draw_text2()
            pg.display.flip()
            self.clock.tick(FPS)

    def draw_background(self):
        self.display.blit(self.background, (0, 0))

    def draw_text(self):
        # Historia
        typography = pg.font.Font(self.font_file, 18)
        message = "La Tierra es inhabitable y debemos abandonarla, para ello hemos construido una nave"
        text = pg.font.Font.render(typography, message, True, C_YELLOW)
        text_width = text.get_width()
        pos_x = (WIDTH-text_width)/2
        pos_y = 0.40 * HEIGHT
        self.display.blit(text, (pos_x, pos_y))

    def draw_text1(self):
        # Historia
        typography = pg.font.Font(self.font_file, 18)
        message = "En nuestro camino encontraremos muchos obstaculos y enemigos alienigenas"
        text = pg.font.Font.render(typography, message, True, C_YELLOW)
        text_width = text.get_width()
        pos_x = (WIDTH-text_width)/2
        pos_y = 0.50 * HEIGHT
        self.display.blit(text, (pos_x, pos_y))

    def draw_text2(self):
        # Texto indicativo
        typography = pg.font.Font(self.font_file, 16)
        message = "Pulsa Espacio para empezar, ESC para salir"
        text = pg.font.Font.render(typography, message, True, C_YELLOW)
        text_width = text.get_width()
        pos_x = (WIDTH-text_width)/2
        pos_y = 0.75 * HEIGHT
        self.display.blit(text, (pos_x, pos_y))


class Game1(Scene):

    def __init__(self, screen: pg.Surface):
        super().__init__(screen)
        self.game1 = True
        self.space_ship = SpaceShip()
        self.big_asteroid = BigAsteroid()
        self.small_asteroid = SmallAsteroid()
        self.score = Scoreboard1()
        image_background = pg.image.load(os.path.join(
            "resources", "background", "bg-preview-big.png"))
        self.background = pg.transform.scale2x(image_background)
        self.explosion_group = pg.sprite.Group()
        self.hit_group = pg.sprite.Group()
        self.small_enemy = SmallAlienShip()
        self.big_enemy = BigAlienShip()
        self.gamepoints = 0

    def draw_background(self):
        self.display.blit(self.background, (0, 0))

    def make_explosion(self):
        # animación explosion
        explosion = Explosion(self.space_ship.rect.x, self.space_ship.rect.y)
        self.explosion_group.add(explosion)

    def make_hit(self):
        # animación de golpe
        hit = Hit(self.space_ship.rect.x, self.space_ship.rect.y)
        self.hit_group.add(hit)

    def collide(self):
        # Funcion para detectar colisiones entre obstáculos y naves
        """
        Comprueba si el asteroide colisiona con la nave, resetea la posición del asteroide y resta un punto de vida
        """
        # colision entre asteroide grande y nave
        if pg.Rect.colliderect(self.big_asteroid.rect, self.space_ship.rect):
            self.space_ship.hit_hull()
            self.space_ship.hull_damage.ckeck_gameover_condition()
            if self.space_ship.hull_damage.points < 3:
                self.make_hit()
            else:
                self.make_explosion()

            if not self.space_ship.hull_damage.destroyed:
                if self.space_ship.hull_damage.points < 3:
                    self.make_hit()
                else:
                    self.make_explosion()
                self.big_asteroid.rect.x = WIDTH
                self.big_asteroid.rect.y = self.big_asteroid.rect.y = randint(
                    0, HEIGHT)
        # colision entre asteroide pequeño y nave
        if pg.Rect.colliderect(self.small_asteroid.rect, self.space_ship.rect):
            if self.space_ship.hull_damage.points < 3:
                self.make_hit()
            else:
                self.make_explosion()
            self.space_ship.hit_hull()
            self.space_ship.hull_damage.ckeck_gameover_condition()

            if not self.space_ship.hull_damage.destroyed:
                if self.space_ship.hull_damage.points < 3:
                    self.make_hit()
                else:
                    self.make_explosion()
                self.small_asteroid.rect.x = WIDTH
                self.small_asteroid.rect.y = self.small_asteroid.rect.y = randint(
                    0, HEIGHT)

        if pg.Rect.colliderect(self.big_enemy.rect, self.space_ship.rect):
            # colisión entre alien grande y nave
            if self.space_ship.hull_damage.points < 3:
                self.make_hit()
            else:
                self.make_explosion()
            self.space_ship.hit_hull()
            self.space_ship.hull_damage.ckeck_gameover_condition()

            if not self.space_ship.hull_damage.destroyed:
                if self.space_ship.hull_damage.points < 3:
                    self.make_hit()
                else:
                    self.make_explosion()
                self.big_enemy.rect.x = WIDTH
                self.big_enemy.rect.y = self.big_enemy.rect.y = randint(
                    0, HEIGHT)

        if pg.Rect.colliderect(self.small_enemy.rect, self.space_ship.rect):
            # colision entre alien pequeño y nave
            if self.space_ship.hull_damage.points < 3:
                self.make_hit()
            else:
                self.make_explosion()
            self.space_ship.hit_hull()
            self.space_ship.hull_damage.ckeck_gameover_condition()

            if not self.space_ship.hull_damage.destroyed:
                if self.space_ship.hull_damage.points < 3:
                    self.make_hit()
                else:
                    self.make_explosion()
                self.small_enemy.rect.x = WIDTH
                self.small_enemy.rect.y = self.small_enemy.rect.y = randint(
                    0, HEIGHT)

    def reset_and_score(self):
        # resetea la posición de los obstáculos al salir de la pantalla y añade puntuación
        if self.big_asteroid.rect.x <= 1:
            self.score.add_score()
            self.score.check_win_condition()
            if self.big_asteroid.rect.x <= 0:
                self.big_asteroid.rect.x = WIDTH
                self.big_asteroid.rect.y = randint(0, HEIGHT)

        if self.small_asteroid.rect.x <= 1:
            self.score.add_score()
            self.score.check_win_condition()
            if self.small_asteroid.rect.x <= 0:
                self.small_asteroid.speed = randint(7, 10)
                self.small_asteroid.rect.x = WIDTH
                self.small_asteroid.rect.y = randint(0, HEIGHT)

        if self.big_enemy.rect.x <= 1:
            self.score.add_score()
            self.score.check_win_condition()
            if self.big_enemy.rect.x <= 0:
                self.big_enemy.rect.x = WIDTH
                self.big_enemy.rect.y = randint(0, HEIGHT)

        if self.small_enemy.rect.x <= 1:
            self.score.add_score()
            self.score.check_win_condition()
            if self.small_enemy.rect.x <= 0:
                self.small_enemy.rect.x = WIDTH
                self.small_enemy.rect.y = randint(0, HEIGHT)

    def stop_obstacles_if_destroid(self):
        # para la generación de obstáculos
        self.big_asteroid.rect.x = WIDTH
        self.big_asteroid.rect.y = randint(0, HEIGHT)
        self.small_asteroid.rect.x = WIDTH
        self.small_asteroid.rect.y = randint(0, HEIGHT)
        self.big_enemy.rect.x = WIDTH
        self.big_enemy.rect.y = randint(0, HEIGHT)
        self.small_enemy.rect.x = WIDTH
        self.small_enemy.rect.y = randint(0, HEIGHT)

    def save_gamepoints_and_hits(self):
        # calcula los puntos de la partida, restando los golpes con la nave a los obstaculos
        self.gamepoints = self.score.points - self.space_ship.hull_damage.points

    def main_loop(self):
        print("Starting game!")

        while True:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        print("Exiting")
                        return
                    if event.key == pg.K_SPACE:
                        # if self.score.win == True:
                        return self.gamepoints
                    if event.key == pg.K_r:
                        self.score.initialize()
                        self.space_ship.hull_damage.initialize()

                if event.type == pg.QUIT:
                    print("Exiting")
                    pg.quit()

            # mueve asteroides y comprueba si chocan con la nave
            if self.space_ship.hull_damage.destroyed == False:
                self.big_asteroid.update()
                self.small_asteroid.update()
                self.small_enemy.update(self.game1)
                self.big_enemy.update(self.game1)
                if self.score.win == False:
                    self.collide()
            # para el asteroide
            else:
                self.stop_obstacles_if_destroid()

            # Resetea asteroides y marca si esquivados
            if self.score.win == False:
                self.reset_and_score()

            # dibuja el fondo
            self.draw_background()
            # dibuja la nave
            if not self.space_ship.hull_damage.destroyed:
                self.space_ship.update()
                self.display.blit(self.space_ship.image, self.space_ship.rect)
            # dibuja los asteroides
            self.display.blit(self.big_asteroid.image, self.big_asteroid.rect)
            self.display.blit(self.small_asteroid.image,
                              self.small_asteroid.rect)
            self.display.blit(self.big_enemy.image, self.big_enemy.rect)
            self.display.blit(self.small_enemy.image, self.small_enemy.rect)

            # dibuja explosion
            self.explosion_group.draw(self.display)
            self.explosion_group.update()

            # dibuja golpes a la nave
            self.hit_group.draw(self.display)
            self.hit_group.update()

            # dibuja puntuacion juego1
            if self.score.win == True:
                self.save_gamepoints_and_hits()

            # dibuja los puntos para ganar (asteroides esquivados)
            self.score.draw(self.display, self.gamepoints)
            # dibuja los puntos para perder (golpes a la nave)
            self.space_ship.hull_damage.draw(self.display)

            pg.display.flip()
            self.clock.tick(FPS)


class Story2(Scene):

    def __init__(self, screen: pg.Surface):
        super().__init__(screen)
        image_background = pg.image.load(os.path.join(
            "resources", "background", "layered", "bg-back.png"))
        image_background_stars = pg.image.load(os.path.join(
            "resources", "background", "layered", "bg-stars.png"))

        self.background = pg.transform.scale(image_background, (WIDTH, HEIGHT))
        self.background_stars = pg.transform.scale(
            image_background_stars, (WIDTH, HEIGHT))

        self.font_file = os.path.join(
            "resources", "fonts", "PublicPixel-z84yD.ttf")

    def main_loop(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        print("Exiting")
                        return
                    if event.key == pg.K_SPACE:
                        return None
                if event.type == pg.QUIT:
                    print("Exiting!")
                    pg.quit()

            self.display.fill(C_BLACK)
            self.draw_background()
            self.draw_text0()
            self.draw_text1()
            self.draw_text2()
            self.draw_text3()
            pg.display.flip()
            self.clock.tick(FPS)
        return None

    def draw_background(self):
        self.display.blit(self.background, (0, 0))
        self.display.blit(self.background_stars, (0, 0))

    def draw_text0(self):
        # Historia
        typography = pg.font.Font(self.font_file, 18)
        message = "Por fin hemos llegado a nuestro nuevo sol y nos aproximamos a nuestro nuevo hogar!"
        text = pg.font.Font.render(typography, message, True, C_YELLOW)
        text_width = text.get_width()
        pos_x = (WIDTH-text_width)/2
        pos_y = 0.30 * HEIGHT
        self.display.blit(text, (pos_x, pos_y))

    def draw_text1(self):
        # Historia
        typography = pg.font.Font(self.font_file, 18)
        message = "Tenemos un campo de asteroides enfrente y ... ESPERA!"
        text = pg.font.Font.render(typography, message, True, C_YELLOW)
        text_width = text.get_width()
        pos_x = (WIDTH-text_width)/2
        pos_y = 0.40 * HEIGHT
        self.display.blit(text, (pos_x, pos_y))

    def draw_text2(self):
        # Historia
        typography = pg.font.Font(self.font_file, 18)
        message = "Unas naves vienen hacia nosotros ¡Son los aliens! y están mas cabreados...¡Nos disparan!"
        text = pg.font.Font.render(typography, message, True, C_YELLOW)
        text_width = text.get_width()
        pos_x = (WIDTH-text_width)/2
        pos_y = 0.50 * HEIGHT
        self.display.blit(text, (pos_x, pos_y))

    def draw_text3(self):
        # Texto indicativo
        typography = pg.font.Font(self.font_file, 16)
        message = "Pulsa Espacio para empezar, ESC para Salir"
        text = pg.font.Font.render(typography, message, True, C_YELLOW)
        text_width = text.get_width()
        pos_x = (WIDTH-text_width)/2
        pos_y = 0.75 * HEIGHT
        self.display.blit(text, (pos_x, pos_y))


class Game2(Scene):

    def __init__(self, screen: pg.Surface):
        super().__init__(screen)
        self.game1 = False

        image_background = pg.image.load(os.path.join(
            "resources", "background", "layered", "bg-back.png"))
        image_background_stars = pg.image.load(os.path.join(
            "resources", "background", "layered", "bg-stars.png"))
        self.background = pg.transform.scale(image_background, (WIDTH, HEIGHT))
        self.background_stars = pg.transform.scale(
            image_background_stars, (WIDTH, HEIGHT))

        self.space_ship = SpaceShip()
        self.big_asteroid = BigAsteroid()
        self.small_asteroid = SmallAsteroid()
        self.big_enemy = BigAlienShip()
        self.small_enemy = SmallAlienShip()
        self.score = Scoreboard2()
        self.planet = Planet()
        self.endgame_text = EndGame2Texts()
        self.shot = Shot()

        self.explosion_group = pg.sprite.Group()
        self.hit_group = pg.sprite.Group()
        self.planet.planet_in_position = False
        self.landing_complete = False

    def draw_background(self):
        self.display.blit(self.background, (0, 0))
        self.display.blit(self.background_stars, (0, 0))

    def make_explosion(self):
        # animacion de explosión
        explosion = Explosion(self.space_ship.rect.x, self.space_ship.rect.y)
        self.explosion_group.add(explosion)

    def make_hit(self):
        # animación de golpe
        hit = Hit(self.space_ship.rect.x, self.space_ship.rect.y)
        self.hit_group.add(hit)

    def collide(self):
        # Detecta colision entre obstáculos y nave
        """
        Comprueba si el asteroide colisiona con la nave, resetea la posición del asteroide y resta un punto de vida
        """
        # colision entre asteroide grande y nave
        if pg.Rect.colliderect(self.big_asteroid.rect, self.space_ship.rect):
            self.space_ship.hit_hull()
            self.space_ship.hull_damage.ckeck_gameover_condition()
            if self.space_ship.hull_damage.points < 3:
                self.make_hit()
            else:
                self.make_explosion()

            if not self.space_ship.hull_damage.destroyed:
                if self.space_ship.hull_damage.points < 3:
                    self.make_hit()
                else:
                    self.make_explosion()
                self.big_asteroid.rect.x = WIDTH
                self.big_asteroid.rect.y = self.big_asteroid.rect.y = randint(
                    0, HEIGHT)
        # colision entre asteroide pequeño y nave
        if pg.Rect.colliderect(self.small_asteroid.rect, self.space_ship.rect):
            if self.space_ship.hull_damage.points < 3:
                self.make_hit()
            else:
                self.make_explosion()
            self.space_ship.hit_hull()
            self.space_ship.hull_damage.ckeck_gameover_condition()

            if not self.space_ship.hull_damage.destroyed:
                if self.space_ship.hull_damage.points < 3:
                    self.make_hit()
                else:
                    self.make_explosion()
                self.small_asteroid.rect.x = WIDTH
                self.small_asteroid.rect.y = self.small_asteroid.rect.y = randint(
                    0, HEIGHT)

        # colision con alien grande
        if pg.Rect.colliderect(self.big_enemy.rect, self.space_ship.rect):
            if self.space_ship.hull_damage.points < 3:
                self.make_hit()
            else:
                self.make_explosion()
            self.space_ship.hit_hull()
            self.space_ship.hull_damage.ckeck_gameover_condition()

            if not self.space_ship.hull_damage.destroyed:
                if self.space_ship.hull_damage.points < 3:
                    self.make_hit()
                else:
                    self.make_explosion()
                self.big_enemy.rect.x = WIDTH
                self.big_enemy.rect.y = self.big_enemy.rect.y = randint(
                    0, HEIGHT)

        # colision con alien pequeño
        if pg.Rect.colliderect(self.small_enemy.rect, self.space_ship.rect):
            if self.space_ship.hull_damage.points < 3:
                self.make_hit()
            else:
                self.make_explosion()
            self.space_ship.hit_hull()
            self.space_ship.hull_damage.ckeck_gameover_condition()

            if not self.space_ship.hull_damage.destroyed:
                if self.space_ship.hull_damage.points < 3:
                    self.make_hit()
                else:
                    self.make_explosion()
                self.small_enemy.rect.x = WIDTH
                self.small_enemy.rect.y = self.small_enemy.rect.y = randint(
                    0, HEIGHT)
        # colision con disparo
        if pg.Rect.colliderect(self.shot.rect, self.space_ship.rect):
            if self.space_ship.hull_damage.points < 3:
                self.make_hit()
            else:
                self.make_explosion()
            self.space_ship.hit_hull()
            self.space_ship.hull_damage.ckeck_gameover_condition()

            if not self.space_ship.hull_damage.destroyed:
                if self.space_ship.hull_damage.points < 3:
                    self.make_hit()
                else:
                    self.make_explosion()
                self.shot.rect.x = WIDTH
                self.shot.rect.y = self.small_enemy.rect.y = randint(
                    0, HEIGHT)

    def reset_and_score(self):
        # resgenera los obstáculos y marca puntuación
        if self.big_asteroid.rect.x <= 1:
            self.score.add_score()
            self.score.check_win_condition()
            if self.big_asteroid.rect.x <= 0:
                self.big_asteroid.rect.x = WIDTH
                self.big_asteroid.rect.y = randint(0, HEIGHT)

        if self.small_asteroid.rect.x <= 1:
            self.score.add_score()
            self.score.check_win_condition()
            if self.small_asteroid.rect.x <= 0:
                self.small_asteroid.speed = randint(7, 10)
                self.small_asteroid.rect.x = WIDTH
                self.small_asteroid.rect.y = randint(0, HEIGHT)

        if self.big_enemy.rect.x <= 1:
            self.score.add_score()
            self.score.check_win_condition()
            if self.big_enemy.rect.x <= 0:
                self.big_enemy.rect.x = WIDTH
                self.big_enemy.rect.y = randint(0, HEIGHT)

        if self.small_enemy.rect.x <= 1:
            self.score.add_score()
            self.score.check_win_condition()
            if self.small_enemy.rect.x <= 0:
                self.small_enemy.rect.x = WIDTH
                self.small_enemy.rect.y = randint(0, HEIGHT)

        if self.shot.rect.x <= 1:
            self.score.add_score()
            self.score.check_win_condition()
            if self.shot.rect.x <= 0:
                self.shot.rect.x = WIDTH
                self.shot.rect.y = randint(0, HEIGHT)

    def stop_obstacles_if_destroid(self):
        # para la generacion de obstáculos si la nave se destruye
        self.big_asteroid.rect.x = WIDTH
        self.big_asteroid.rect.y = randint(0, HEIGHT)
        self.small_asteroid.rect.x = WIDTH
        self.small_asteroid.rect.y = randint(0, HEIGHT)
        self.big_enemy.rect.x = WIDTH
        self.big_enemy.rect.y = randint(0, HEIGHT)
        self.small_enemy.rect.x = WIDTH
        self.small_enemy.rect.y = randint(0, HEIGHT)
        self.shot.rect.x = WIDTH
        self.shot.rect.y = randint(0, HEIGHT)

    def ship_landing(self):
        # empieza el evento de aterrizaje
        self.space_ship.rot_center()
        if self.space_ship.rect.y > HEIGHT/2:
            self.space_ship.rect.y -= self.space_ship.speed
        if self.space_ship.rect.y < HEIGHT/2:
            self.space_ship.rect.y += self.space_ship.speed
        if self.space_ship.rect.x <= PLANET_WIDTH+349:
            self.space_ship.rect.x += self.space_ship.speed*3
        if self.space_ship.rect.x >= PLANET_WIDTH+349:
            self.landing_complete = True

    def calculate_points(self):
        # Calcula la puntuación restando los golpes a la nave con los obstáculos esquivados
        self.gamepoints = self.score.points - self.space_ship.hull_damage.points

    def main_loop(self):
        print("Starting game!")

        while True:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        print("Exiting")
                        return
                    if event.key == pg.K_SPACE:
                        if self.score.win == True and self.landing_complete == True:
                            return self.gamepoints
                    if event.key == pg.K_r and self.score.win != True:
                        self.score.initialize()
                        self.space_ship.hull_damage.initialize()

                if event.type == pg.QUIT:
                    print("Exiting")
                    pg.quit()

            # mueve obstaculos y comprueba si chocan con la nave
            if self.space_ship.hull_damage.destroyed == False:
                self.big_asteroid.update()
                self.small_asteroid.update()
                self.big_enemy.update(self.game1)
                self.small_enemy.update(self.game1)
                self.shot.update()

                if self.score.win == False:
                    self.collide()

            # para obstaculos si se pierde partida
            else:
                self.stop_obstacles_if_destroid()
                # Resetea obstaculos y marca si esquivados
            if self.score.win == False:
                self.reset_and_score()

                # dibuja el fondo
            self.draw_background()
            # dibuja la nave
            if not self.space_ship.hull_damage.destroyed:
                self.display.blit(self.space_ship.image, self.space_ship.rect)
                self.space_ship.update()
            # dibuja los obstaculos
            self.display.blit(self.big_asteroid.image, self.big_asteroid.rect)
            self.display.blit(self.small_asteroid.image,
                              self.small_asteroid.rect)
            self.display.blit(self.big_enemy.image, self.big_enemy.rect)
            self.display.blit(self.small_enemy.image, self.small_enemy.rect)
            self.display.blit(self.shot.image, self.shot.rect)

            # dibuja explosion
            self.explosion_group.draw(self.display)
            self.explosion_group.update()

            # dibuja golpes a la nave
            self.hit_group.draw(self.display)
            self.hit_group.update()

            # dibuja los puntos ganados
            self.score.draw(self.display)
            # dibuja los puntos para perder (golpes a la nave)
            self.space_ship.hull_damage.draw(self.display)

            # dibuja planeta
            if self.score.win == True:
                self.calculate_points()
                self.display.blit(self.planet.image, self.planet.rect)
                self.planet.update()
                # textos final de partida
                self.endgame_text.draw_text1(self.display, self.gamepoints)

            # aterrizaje de la nave
            if self.planet.planet_in_position == True:
                self.ship_landing()
            # si se completa la animación de aterrizaje aparece un texto de historia
            if self.landing_complete == True:
                self.endgame_text.draw_text2(self.display)

            pg.display.flip()
            self.clock.tick(FPS)


class HallOfFame(Scene):
    def __init__(self, screen: pg.Surface):
        super().__init__(screen)
        image_background = pg.image.load(os.path.join(
            "resources", "background", "bg-preview-big.png"))
        self.background = pg.transform.scale2x(image_background)
        pg.font.init()
        font_file = os.path.join("resources", "fonts", "PublicPixel-z84yD.ttf")
        self.typography_title = pg.font.Font(font_file, 30)
        self.typography_records = pg.font.Font(font_file, 18)
        self.total_gamepoints = 0  # puntos metidos para poder trabajar con db

        self.database = DBManager(DB_ROUTE)
        self.records = []

        self.names = []
        self.points = []
        self.names_render = []
        self.points_render = []

    def draw_background(self):
        self.display.blit(self.background, (0, 0))

    def draw_text(self):
        text = pg.font.Font.render(
            self.typography_records, "¡Pulsa ESC para salir, Adios!", True, C_YELLOW)

        pos_x1 = (WIDTH - text.get_width())/2
        pos_y1 = HEIGHT * 0.75

        pg.surface.Surface.blit(self.display, text, (pos_x1, pos_y1))

    def load(self):
        # carga records desde la base de datos
        self.records = self.database.load()
        for record in self.records:
            record.pop("id")
            for value in record.values():
                if isinstance(value, str):
                    self.names.append(value)
                else:
                    self.points.append(value)

    def draw_records(self, name, points, render_names, render_points):
        # pintado de titulos:
        text_title_name = pg.font.Font.render(
            self.typography_title, "NOMBRE", True, C_YELLOW)
        pos_x_title_name = (WIDTH - text_title_name.get_width())/4
        pos_y_title_name = LATERAL_MARGIN
        self.display.blit(
            text_title_name, (pos_x_title_name, pos_y_title_name))

        text_title_score = pg.font.Font.render(
            self.typography_title, "PUNTOS", True, C_YELLOW)
        pos_x_title_score = (
            (WIDTH - text_title_score.get_width())/4) + WIDTH / 2
        pos_y_title_score = LATERAL_MARGIN
        self.display.blit(
            text_title_score, (pos_x_title_score, pos_y_title_score))

        # pintado de records:
        begin_lines = 200

        for a in range(len(name)):
            pos_x = (WIDTH - render_names.get_width()) / 4
            pos_y = a * render_names.get_height() + begin_lines
            self.display.blit(name[a], (pos_x, pos_y))

        for b in range(len(points)):
            pos_x1 = ((WIDTH - render_points.get_width())/4) + WIDTH / 2
            pos_y1 = b * render_points.get_height() + begin_lines
            self.display.blit(points[b], (pos_x1, pos_y1))

    def check_if_top10(self):
        # comprueba si la puntuacion alcanzada esta en el top 10 de récords
        lowest = self.database.lowest_top10_score()
        # puede entrar un 0 desde la funcion de database, dejando entrar cualquier puntuacion
        if self.total_gamepoints > lowest:
            return True
        else:
            return False

    def main_loop(self):

        if self.check_if_top10() == True:
            inputbox = InputBox(self.display)
            name = inputbox.get_text()

            self.database.save(name, self.total_gamepoints)

        self.load()

        for name in self.names:
            rendertext = self.typography_records.render(name, True, C_YELLOW)
            self.names_render.append(rendertext)

        for score in self.points:
            rendertext2 = self.typography_records.render(
                str(score), True, C_YELLOW)
            self.points_render.append(rendertext2)
            pass

        while True:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        print("Exiting")
                        return
                    if event.key == pg.K_SPACE:
                        return

                if event.type == pg.QUIT:
                    print("Exiting")
                    pg.quit()
            self.display.fill(C_BLUE)
            self.draw_background()

            # Pinta los récords
            self.draw_records(self.names_render,
                              self.points_render, rendertext, rendertext2)

            self.draw_text()

            pg.display.flip()
            self.clock.tick(FPS)
