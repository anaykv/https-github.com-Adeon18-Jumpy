# Game by - Adeon18(Trush Ostap)
# Sound and Music - @diiienow
# Art from Kenney.nl

from sprites import *
from os import path


class Game:
    def __init__(self):
        # initialize game window, etc
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.mixer.init()
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.font_name = pygame.font.match_font(FONT_NAME)
        self.menu = pygame.sprite.Group()
        self.load_data()

    def load_data(self):
        # Load high score
        coin_file = open(COIN_FILE, "w+")
        coin_file.close()
        saves_file = open(SAVES_FILE, "w+")
        saves_file.close()
        self.dir = path.dirname(__file__)
        with open(path.join(self.dir, SAVES_FILE), 'r') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0

        with open(path.join(self.dir, COIN_FILE), 'r') as f:
            try:
                self.coin_amount = int(f.read())
            except:
                self.coin_amount = 0

        # Load spritesheet image
        self.spritesheet1 = Spritesheet1(path.join(self.dir, SPRITESHEET1))
        img_dir = path.join(self.dir, 'graphics')
        # Bg images
        self.bg_menu = pygame.image.load('bg_menu.png')
        # Button images
        self.menu_b1 = Button(self, WIDTH // 2, HEIGHT // 2 + 56)
        self.menu_b2 = Button(self, WIDTH // 2, HEIGHT // 2 + 56 * 2)
        self.menu_b3 = Button(self, WIDTH // 2, HEIGHT // 2 + 56 * 3)
        self.tut_b = Button(self, WIDTH // 2, HEIGHT // 2 + 56 * 3)
        # Cloud images
        self.cloud_images = []
        for i in range(1, 4):
            self.cloud_images.append(pygame.image.load(path.join(img_dir, 'cloud_bg{}.png'.format(i))).convert())
        # Load Sound
        self.sound_dir = path.join(self.dir, 'Sounds')
        self.jump_sound = pygame.mixer.Sound(path.join(self.sound_dir, 'jump.wav'))
        self.jump_sound.set_volume(0.2)
        self.boost_sound = pygame.mixer.Sound(path.join(self.sound_dir, 'boost.wav'))
        self.boost_sound.set_volume(0.7)
        self.bubble_sound = pygame.mixer.Sound(path.join(self.sound_dir, 'bubble.wav'))
        self.bubble_pop_sound = pygame.mixer.Sound(path.join(self.sound_dir, 'bubble_pop.wav'))
        self.coin_sound = pygame.mixer.Sound(path.join(self.sound_dir, 'coin.wav'))
        self.wings_sound = pygame.mixer.Sound(path.join(self.sound_dir, 'wings.wav'))
        self.wings_sound.set_volume(0.3)
        self.flyman_sound = pygame.mixer.Sound(path.join(self.sound_dir, 'flyman.wav'))
        self.flyman_sound.set_volume(0.4)
        self.jetpack_sound = pygame.mixer.Sound(path.join(self.sound_dir, 'jetpack.wav'))
        self.jetpack_sound.set_volume(0.3)
        self.lightining_sound = pygame.mixer.Sound(path.join(self.sound_dir, 'lightning.wav'))
        self.lightining_sound.set_volume(0.3)
        self.button_sound = pygame.mixer.Sound(path.join(self.sound_dir, 'button.wav'))
        self.button_sound.set_volume(0.5)

    def new(self):
        # start a new game
        self.score = 0
        self.bubble_score = 0
        self.jetpack_score = 0
        self.wings_score = 0
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.platforms = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.mobs = pygame.sprite.Group()
        self.passive_mobs = pygame.sprite.Group()
        self.flying_mobs = pygame.sprite.Group()
        self.clouds = pygame.sprite.Group()
        self.lightinings = pygame.sprite.Group()
        self.player = Player(self)
        for plat in PLATFORM_LIST:
            Platform(self, *plat)
        self.mob_timer = 0
        self.has_flyman = False
        self.has_sun = False
        # Fade properties
        self.R = 136
        self.G = 202
        self.B = 255
        self.first_fade = False
        self.second_fade = False
        self.third_fade = False
        self.color_change = False
        # Sounds
        self.wings_sound.set_volume(0.3)
        for i in range(6):
            c = CloudBG(self)
            c.rect.y += 500
        self.run()

    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()

        pygame.mixer.music.fadeout(500)

    def update(self):
        # Game Loop - Update
        self.draw()
        self.all_sprites.update()

        # Spawn a Flyman
        time_passed = pygame.time.get_ticks()
        if time_passed - self.mob_timer > FLYMAN_FREQ + random.choice([-1000, -500, 0, 500, 1000]) and self.player.pos.y\
                < HEIGHT - 50 and not self.has_flyman and SUN_SPAWN_SCORE > self.score > FLYMAN_SPAWN_SCORE:
            self.mob_timer = time_passed
            if random.randrange(100) < FLYMAN_SPAWN_RATIO:
                self.flyman_sound.play()
                Flyman(self)
                self.has_flyman = True
        # Spawn a Sun without wing powerup
        if not self.player.has_wings:
            if time_passed - self.mob_timer > SUN_FREQ + random.choice([-1000, -500, 0, 500, 1000]) \
                    and self.player.pos.y < HEIGHT - 50 and not self.has_sun and self.score > SUN_SPAWN_SCORE:
                self.mob_timer = time_passed
                if random.randrange(100) < SUN_SPAWN_RATIO:
                    Sun(self)
                    self.has_sun = True
        # Spawn a sun when the wings are initiated
        else:
            if time_passed - self.mob_timer > 1000 and not self.player.losing_wings:
                self.mob_timer = time_passed
                Sun(self)
                self.has_sun = True

        # Hit mobs
        mob_hits = pygame.sprite.spritecollide(self.player, self.mobs, False)
        if mob_hits and not self.player.has_bubble and not self.player.has_jetpack:
            if pygame.sprite.spritecollide(self.player, self.mobs, False, pygame.sprite.collide_mask):
                # We stop the wing sound
                self.wings_sound.set_volume(0)
                self.playing = False
        # Hit flying mobs
        f_mob_hits = pygame.sprite.spritecollide(self.player, self.flying_mobs, False)
        if f_mob_hits and not self.player.has_bubble and not self.player.has_jetpack:
            if pygame.sprite.spritecollide(self.player, self.flying_mobs, False, pygame.sprite.collide_mask):
                self.wings_sound.set_volume(0)
                self.playing = False

        # check if player hits a platform - only if falling
        if self.player.vel.y > 0:
            hits = pygame.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                lowest_plat = hits[0]
                for hit in hits:
                    if hit.rect.bottom > lowest_plat.rect.bottom:
                        lowest_plat = hit
                # Applying the plat borders where you can walk
                if lowest_plat.rect.left - 10 < self.player.pos.x < lowest_plat.rect.right + 10:
                    if self.player.pos.y < lowest_plat.rect.centery - 3:
                        self.player.pos.y = lowest_plat.rect.top
                        self.player.vel.y = 0
                        self.player.jumping = False
                        # If it is the snow platform then we change the friction
                        if lowest_plat.type == 'icy':
                            self.player.friction = PLAYER_FRICTION_ON_SNOW
                        elif lowest_plat.type == 'sand':
                            self.player.friction = PLAYER_FRICTION_ON_SAND
                        else:
                            self.player.friction = PLAYER_FRICTION
        # We move everything further down at a rate which depends on the wings pow being initiated or no
        if self.player.has_wings:
            SCR_CHANGE_H = SCR_CHANGE_H_FLY
        else:
            SCR_CHANGE_H = HEIGHT / 2 - 80
        # If player reaches the 1/4 of the screen
        if self.player.rect.top <= SCR_CHANGE_H:
            if random.randrange(100) < CLOUD_BG_SPAWN_RATIO:
                CloudBG(self)
            self.player.pos.y += max(abs(self.player.vel.y), 3)
            # Move the clouds further down
            for cloud in self.clouds:
                cloud.rect.y += max(abs(self.player.vel.y / 2), 1.5)
            # Move the platforms further down
            for plat in self.platforms:
                plat.rect.y += max(abs(self.player.vel.y), 3)
                # Respawn the platforms
                if plat.rect.top >= HEIGHT:
                    plat.respawn = True
                    # We kill the plat and spawn a new one
                    if plat.respawn:
                        p = Platform(self, random.randrange(0, WIDTH), plat.rect.y - 1.1 * HEIGHT)
                        plat.kill()
                        # Stop respawn
                        plat.respawn = False
                        # Kepping the plat fully on the screen
                        if p.rect.right > WIDTH:
                            p.rect.right = WIDTH - 5
                        elif p.rect.left < 0:
                            p.rect.left = 5
                    # Increasing the score
                    self.score += random.randrange(10, 16)
                    # We add values to this score so we can monitor the powerups
                    if self.player.has_bubble:
                        self.bubble_score += 10
                    if self.player.has_jetpack:
                        self.jetpack_score += 10
                    if self.player.has_wings:
                        self.wings_score += 10
                    # The variable at which we change fade
                    self.color_change = True

            # Move the powerups further down(code differs because their vel is always changing)
            for pow in self.powerups:
                pow.rect.y += max(abs(self.player.vel.y), 3) + pow.jumpCount
            # Move the mobs further down
            for mob in self.mobs:
                mob.rect.y += max(abs(self.player.vel.y), 3)
            for f_mob in self.flying_mobs:
                f_mob.rect.y += max(abs(self.player.vel.y), 3) + f_mob.vel_y
            for passive_mob in self.passive_mobs:
                passive_mob.rect.y += max(abs(self.player.vel.y), 3)

        # Player/Coin hits
        for coin in self.coins:
            coin_hits = pygame.sprite.spritecollide(self.player, self.coins, True)
            if coin_hits:
                self.coin_sound.play()
                if coin.type == 'bronze':
                    self.coin_amount += 1
                elif coin.type == 'silver':
                    self.coin_amount += 3
                elif coin.type == 'gold':
                    self.coin_amount += 5

        # Player/Powerup hits
        powerup_hits = pygame.sprite.spritecollide(self.player, self.powerups, True)
        for hit in powerup_hits:
            # Only 1 pow can be taken at a time
            if hit.type == 'boost' and not (self.player.has_jetpack or self.player.has_bubble or self.player.has_wings):
                self.boost_sound.play()
                self.player.vel.y = -BOOST_POWER
                self.player.jumping = False
            elif hit.type == 'bubble' and not (self.player.has_jetpack or self.player.has_wings):
                self.bubble_sound.play()
                self.player.has_bubble = True
                self.player.jumping = False
                self.bubble_score = 0
            elif hit.type == 'jetpack' and not (self.player.has_bubble or self.player.has_wings):
                self.player.has_jetpack = True
                self.jetpack_score = 0
            elif hit.type == 'wings' and not (self.player.has_bubble or self.player.has_jetpack):
                self.player.has_wings = True
                self.wings_score = 0

        # Wings mechanics
        if self.player.has_wings:
            self.wings_sound.play()
            # We accelerate
            self.player.vel.y -= BUBBLE_ACC
            # Keeping the speed once we accelerated
            if self.player.vel.y <= -WING_SPEED:
                self.player.vel.y = -WING_SPEED
            # Slowing down
            if WINGS_END_SCORE > self.wings_score > 350:
                self.player.vel.y += BUBBLE_ACC
                # Moving the player up the screen var = true
                self.player.losing_wings = True
            # Wings are gone
            if self.wings_score >= WINGS_END_SCORE:
                self.player.losing_wings = False
                self.player.has_wings = False

        # Bubble mechanics
        if self.player.has_bubble:
            # We accelerate
            self.player.vel.y -= BUBBLE_ACC
            if self.player.vel.y <= -BUBBLE_SPEED:
                self.player.vel.y = -BUBBLE_SPEED
            # Keeping the speed once we accelerated
            if BUBBLE_END_SCORE > self.bubble_score > 180:
                self.player.vel.y += BUBBLE_ACC
            # Slowing down
            if self.bubble_score >= BUBBLE_END_SCORE:
                self.bubble_pop_sound.play()
                self.player.has_bubble = False

        # Jetpack mechanics:
        if self.player.has_jetpack:
            self.jetpack_sound.play()
            # We accelerate
            self.player.acceleration = True
            self.player.vel.y -= JETPACK_ACC
            # Keeping the speed once we accelerated
            if self.player.vel.y <= -JETPACK_SPEED:
                self.player.acceleration = False
                self.player.still = True
                self.player.vel.y = -JETPACK_SPEED
            # Slowing down
            if JETPACK_END_SCORE >= self.jetpack_score >= 460:
                self.player.acceleration = True
                self.player.still = False
                self.player.vel.y += JETPACK_DEACC
            # Stopping the jetpack
            if self.jetpack_score > JETPACK_END_SCORE:
                self.player.acceleration = False
                self.player.has_jetpack = False


        # Game over
        if self.player.rect.bottom > HEIGHT:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
                if sprite.rect.bottom < 0:
                    sprite.kill()
        if len(self.platforms) == 0:
            self.playing = False

    def events(self):
        # Game Loop - events
        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.player.jump()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    self.player.jump_cut()

    def draw(self):
        # Game Loop - draw
        # Screen color change
        self.fade()
        self.all_sprites.draw(self.screen)
        self.draw_text(str(self.score), 32, BLACK, WIDTH / 2, 15)
        self.draw_text('Coins: ' + str(self.coin_amount), 32, BLACK, 60, 15)
        # *after* drawing everything, flip the display
        pygame.display.flip()

    def show_start_screen(self):
        # game splash/start screen
        pygame.mixer.music.load(path.join(self.sound_dir, 'bg_music.ogg'))
        pygame.mixer.music.play(loops=-1)
        pygame.mixer.music.set_volume(0.1)
        self.screen.blit(self.bg_menu, (0, 0))
        self.draw_text(TITLE, 68, ALMOST_WHITE, WIDTH / 2, HEIGHT / 4)
        self.menu.draw(self.screen)
        self.menu_b1.draw_txt('Play', 32, ALMOST_WHITE)
        self.menu_b2.draw_txt('Tutorial', 32, ALMOST_WHITE)
        self.menu_b3.draw_txt('Exit', 32, ALMOST_WHITE)
        self.draw_text('High score :' + str(self.highscore), 32, ALMOST_WHITE, WIDTH / 2, 15)

        def wait_for_key_startscr():
            pygame.mouse.set_visible(True)
            waiting = True
            while waiting:
                self.clock.tick(FPS)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        waiting = False
                        self.running = False
                    # Getting the mouse pos and checking the button clicks
                    pos = pygame.mouse.get_pos()
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if self.menu_b1.rect.collidepoint(pos):
                            waiting = False
                            pygame.mouse.set_visible(False)
                            self.button_sound.play()
                        elif self.menu_b2.rect.collidepoint(pos):
                            self.show_tutorial_screen()
                            self.button_sound.play()
                        elif self.menu_b3.rect.collidepoint(pos):
                            waiting = False
                            self.running = False
                        elif self.tut_b.rect.collidepoint(pos):
                            waiting = False
                            self.tut_b.kill()
                            self.show_start_screen()
        pygame.display.flip()
        wait_for_key_startscr()
        pygame.mixer.music.fadeout(1000)

    def show_tutorial_screen(self):
        self.screen.blit(self.bg_menu, (0, 0))
        # Giving tutorial
        self.draw_text('Jumpy!', 72, ALMOST_WHITE, WIDTH / 2, HEIGHT / 10)
        self.draw_text('A/D to move, W to jump', 32, (0, 102, 133), WIDTH / 2, HEIGHT / 3)
        self.draw_text('Avoid mobs and collect coins', 32, (0, 102, 133), WIDTH / 2, HEIGHT / 3 + 36)
        self.draw_text('Use powerups to get the highest score!', 32, (0, 102, 133), WIDTH / 2, HEIGHT / 3 + 36 * 2)
        self.draw_text('Good Luck!:)', 32, (0, 102, 133), WIDTH / 2, HEIGHT / 2 + 10)
        # Creating a button
        self.tut_b = Button(self, WIDTH // 2, HEIGHT // 2 + 56 * 4)
        self.tut_b.draw_txt('Go back', 32, ALMOST_WHITE)
        pygame.display.flip()

    def show_go_screen(self):
        # game over/continue
        if not self.running:
            return
        pygame.mixer.music.load(path.join(self.sound_dir, 'bg_music.ogg'))
        pygame.mixer.music.play(loops=-1)
        self.screen.blit(self.bg_menu, (0, 0))
        self.draw_text('GAME OVER', 68, ALMOST_WHITE, WIDTH / 2, HEIGHT / 5)
        self.draw_text('Score :' + str(self.score), 32, ALMOST_WHITE, WIDTH / 2, HEIGHT / 5 + 50)
        # Adjusting the buttons
        self.goscr_b1 = Button(self, WIDTH // 2, HEIGHT // 2 + 56)
        self.goscr_b2 = Button(self, WIDTH // 2, HEIGHT // 2 + 56 * 2)
        self.goscr_b3 = Button(self, WIDTH // 2, HEIGHT // 2 + 56 * 3)
        self.goscr_b1.draw_txt('Play again', 32, ALMOST_WHITE)
        self.goscr_b2.draw_txt('Return to menu', 32, ALMOST_WHITE)
        self.goscr_b3.draw_txt('Exit', 32, ALMOST_WHITE)
        # Draw the highscore count
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text('New high score!', 32, ALMOST_WHITE, WIDTH / 2, HEIGHT / 5 + 45 * 2)
            with open(path.join(self.dir, SAVES_FILE), 'w',) as f:
                f.write(str(self.score))
        else:
            self.draw_text('High score :' + str(self.highscore), 32, ALMOST_WHITE, WIDTH / 2, HEIGHT / 5 + 45 * 2)

        with open(path.join(self.dir, COIN_FILE), 'w',) as f:
            f.write(str(self.coin_amount))

        def wait_for_key_goscr():
            pygame.mouse.set_visible(True)
            waiting = True
            while waiting:
                self.clock.tick(FPS)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        waiting = False
                        self.running = False
                    # Getting the pos and checking the button clicks
                    pos = pygame.mouse.get_pos()
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if self.goscr_b1.rect.collidepoint(pos):
                            waiting = False
                            pygame.mouse.set_visible(False)
                            self.button_sound.play()
                        if self.goscr_b2.rect.collidepoint(pos):
                            waiting = False
                            self.button_sound.play()
                            self.show_start_screen()
                        elif self.goscr_b3.rect.collidepoint(pos):
                            waiting = False
                            self.running = False
                            self.button_sound.play()
        pygame.display.flip()
        wait_for_key_goscr()
        pygame.mixer.music.fadeout(1000)

    def draw_text(self, text, size, color, x, y):
        font = pygame.font.Font('fonts/AmaticSC-Bold.ttf', size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

    def fade(self):
        # Filling the screen with our start colour
        self.screen.fill((self.R, self.G, self.B))
        # slowly changing the start colour as platforms get killed
        if self.B > 169 and self.color_change and not self.first_fade and not self.second_fade:
            self.B -= 1
            if self.G > 169 and self.color_change:
                self.G -= 1
                self.color_change = False
            self.color_change = False
        self.screen.fill((self.R, self.G, self.B))
        # As we fill the first fade we set it to true so the first if statement is false
        if self.B == 169 and self.G == 169:
            self.first_fade = True
        # We can begin second fade now
        if self.R < 255 and self.color_change:
            self.R += 1
            if self.B < 255 and self.color_change :
                self.B += 1
                self.color_change = False
            self.color_change = False
        self.screen.fill((self.R, self.G, self.B))
        # Second fade is finished so we set it to true; 1st and 2nd ifs are false now
        if self.B == 255 and self.R == 255:
            self.second_fade = True
        # We begin the thind fade
        if self.G < 250 and self.color_change and self.second_fade and not self.third_fade:
            self.G += 1
            self.color_change = False
        # Third fade is finished so we set all the ifs to false now and stop the fade
        if self.G == 250:
            self.third_fade = True


g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pygame.quit()
