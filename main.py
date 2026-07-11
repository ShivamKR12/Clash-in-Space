# /// script
# dependencies = [
#     "pygame-ce",
# ]
# ///

import pygame, sys, asyncio
from random import randint, uniform

async def main():
    class Player(pygame.sprite.Sprite):
        def __init__(self, groups, game):
            super().__init__(groups)
            self.game = game
            self.image = pygame.image.load('assets/player.png').convert_alpha()
            self.rect = self.image.get_frect(center = (self.game.WINDOW_WIDTH / 2, self.game.WINDOW_HEIGHT / 2))
            self.direction = pygame.Vector2()
            self.speed = 300
    
            # cooldown 
            self.can_shoot = True
            self.laser_shoot_time = 0
            self.cooldown_duration = 400
    
            # mask 
            self.mask = pygame.mask.from_surface(self.image)
    
        def laser_timer(self):
            if not self.can_shoot:
                current_time = pygame.time.get_ticks()
                if current_time - self.laser_shoot_time >= self.cooldown_duration:
                    self.can_shoot = True
    
        def update(self, dt):
            keys = pygame.key.get_pressed()
            self.direction.x = (int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])) or (int(keys[pygame.K_d]) - int(keys[pygame.K_a]))
            self.direction.y = (int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])) or (int(keys[pygame.K_s]) - int(keys[pygame.K_w]))
            self.direction = self.direction.normalize() if self.direction else self.direction 
            self.rect.center += self.direction * self.speed * dt
    
            recent_keys = pygame.key.get_just_pressed()
            if recent_keys[pygame.K_SPACE] and self.can_shoot:
                Laser(self.game.laser_surf, self.rect.midtop, (self.game.all_sprites, self.game.laser_sprites)) 
                self.can_shoot = False
                self.laser_shoot_time = pygame.time.get_ticks()
                self.game.laser_sound.play()
    
            self.laser_timer()
    
    class Star(pygame.sprite.Sprite):
        def __init__(self, groups, surf):
            super().__init__(groups)
            self.image = surf
            self.rect = self.image.get_frect(center = (randint(0, 1280),randint(0, 720))) # Use fixed values or pass game object
    
    class Laser(pygame.sprite.Sprite):
        def __init__(self, surf, pos, groups):
            super().__init__(groups)
            self.image = surf 
            self.rect = self.image.get_frect(midbottom = pos)
    
        def update(self, dt):
            self.rect.centery -= 400 * dt
            if self.rect.bottom < 0:
                self.kill()
    
    class Meteor(pygame.sprite.Sprite):
        def __init__(self, surf, pos, groups):
            super().__init__(groups)
            self.original_surf = surf
            self.image = surf
            self.rect = self.image.get_frect(center = pos)
            self.start_time = pygame.time.get_ticks()
            self.lifetime = 3000
            self.direction = pygame.Vector2(uniform(-0.5, 0.5),1)
            self.speed = randint(400,500)
            self.rotation_speed = randint(40,80)
            self.rotation = 0
    
        def update(self, dt):
            self.rect.center += self.direction * self.speed * dt
            if pygame.time.get_ticks() - self.start_time >= self.lifetime:
                self.kill()
            self.rotation += self.rotation_speed * dt
            self.image = pygame.transform.rotozoom(self.original_surf, self.rotation, 1)
            self.rect = self.image.get_frect(center = self.rect.center)
    
    class AnimatedExplosion(pygame.sprite.Sprite):
        def __init__(self, frames, pos, groups, explosion_sound):
            super().__init__(groups)
            self.frames = frames
            self.frame_index = 0
            self.image = self.frames[self.frame_index]
            self.rect = self.image.get_frect(center = pos)
            explosion_sound.play()
     
        def update(self, dt):
            self.frame_index += 20 * dt
            if self.frame_index < len(self.frames):
                self.image = self.frames[int(self.frame_index)]
            else:
                self.kill()
    
    class Game:
        def __init__(self):
            # general setup 
            pygame.init()
            self.WINDOW_WIDTH, self.WINDOW_HEIGHT = 1280, 720
            self.display_surface = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
            pygame.display.set_caption('Clash in Space')
            self.clock = pygame.time.Clock()
            self.running = True
            self.game_state = "menu" # menu, play, game_over
    
            # assets
            self.star_surf = pygame.image.load('assets/star.png').convert_alpha()
            self.meteor_surf = pygame.image.load('assets/meteor.png').convert_alpha()
            self.laser_surf = pygame.image.load('assets/laser.png').convert_alpha()
            self.font = pygame.font.Font('assets/Oxanium-Bold.ttf', 40)
            self.explosion_frames = [pygame.image.load(f'assets/explosion/{i}.png').convert_alpha() for i in range(21)]
    
            # sounds
            self.laser_sound = pygame.mixer.Sound('assets/laser.ogg')
            self.laser_sound.set_volume(0.5)
            self.explosion_sound = pygame.mixer.Sound('assets/explosion.ogg')
            self.game_music = pygame.mixer.Sound('assets/game_music.ogg')
            self.game_music.set_volume(0.4)
    
            # high score
            self.high_score = 0
    
        def reset_game(self):
            # sprites 
            self.all_sprites = pygame.sprite.Group()
            self.meteor_sprites = pygame.sprite.Group()
            self.laser_sprites = pygame.sprite.Group()
            for i in range(20):
                Star(self.all_sprites, self.star_surf) 
            self.player = Player(self.all_sprites, self)
    
            # custom events -> meteor event
            self.meteor_event = pygame.event.custom_type()
            self.meteor_timer_interval = 400 # Start with a slower spawn rate
            pygame.time.set_timer(self.meteor_event, self.meteor_timer_interval)
            self.game_start_time = pygame.time.get_ticks()
    
        def collisions(self):
            if pygame.sprite.spritecollide(self.player, self.meteor_sprites, True, pygame.sprite.collide_mask):
                self.game_state = "game_over"
                if self.score > self.high_score:
                    self.high_score = self.score
    
            for laser in self.laser_sprites:
                if pygame.sprite.spritecollide(laser, self.meteor_sprites, True):
                    laser.kill()
                    AnimatedExplosion(self.explosion_frames, laser.rect.midtop, self.all_sprites, self.explosion_sound)
    
        def display_score(self):
            self.score = (pygame.time.get_ticks() - self.game_start_time) // 100
            text_surf = self.font.render(str(self.score), True, (240,240,240))
            text_rect = text_surf.get_frect(midbottom = (self.WINDOW_WIDTH / 2, self.WINDOW_HEIGHT - 50))
            self.display_surface.blit(text_surf, text_rect)
            pygame.draw.rect(self.display_surface, (240,240,240), text_rect.inflate(20,10).move(0,-8), 5, 10)
    
        def update_difficulty(self):
            # Increase meteor spawn rate over time
            if self.meteor_timer_interval > 150 and self.score % 100 == 0 and self.score > 0:
                self.meteor_timer_interval -= 25
                pygame.time.set_timer(self.meteor_event, self.meteor_timer_interval)
    
        def main_menu(self, events):
            self.display_surface.fill('#3a2e3f')
            title_surf = self.font.render("Clash in Space", True, 'white')
            title_rect = title_surf.get_frect(center=(self.WINDOW_WIDTH / 2, self.WINDOW_HEIGHT / 2 - 100))
    
            instr_surf = self.font.render("Press SPACE to Play", True, 'white')
            instr_rect = instr_surf.get_frect(center=(self.WINDOW_WIDTH / 2, self.WINDOW_HEIGHT / 2))
    
            high_score_surf = self.font.render(f"High Score: {self.high_score}", True, 'white')
            high_score_rect = high_score_surf.get_frect(center=(self.WINDOW_WIDTH / 2, self.WINDOW_HEIGHT / 2 + 100))
    
            self.display_surface.blit(title_surf, title_rect)
            self.display_surface.blit(instr_surf, instr_rect)
            self.display_surface.blit(high_score_surf, high_score_rect)
    
            for event in events:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.game_state = "play"
                    self.reset_game()
    
        def play_game(self, dt, events):
            for event in events:
                if event.type == self.meteor_event:
                    x, y = randint(0, self.WINDOW_WIDTH), randint(-200, -100)
                    Meteor(self.meteor_surf, (x, y), (self.all_sprites, self.meteor_sprites))
            self.all_sprites.update(dt)
            self.collisions()
            self.display_surface.fill('#3a2e3f')
            self.all_sprites.draw(self.display_surface)
            self.display_score()
    
        def game_over_screen(self, events):
            self.display_surface.fill('#3a2e3f')
            title_surf = self.font.render("Game Over", True, 'white')
            title_rect = title_surf.get_frect(center=(self.WINDOW_WIDTH / 2, self.WINDOW_HEIGHT / 2 - 150))
    
            score_surf = self.font.render(f"Your Score: {self.score}", True, 'white')
            score_rect = score_surf.get_frect(center=(self.WINDOW_WIDTH / 2, self.WINDOW_HEIGHT / 2 - 50))
    
            high_score_surf = self.font.render(f"High Score: {self.high_score}", True, 'white')
            high_score_rect = high_score_surf.get_frect(center=(self.WINDOW_WIDTH / 2, self.WINDOW_HEIGHT / 2 + 50))
    
            instr_surf = self.font.render("Press SPACE to Play Again", True, 'white')
            instr_rect = instr_surf.get_frect(center=(self.WINDOW_WIDTH / 2, self.WINDOW_HEIGHT / 2 + 150))
    
            self.display_surface.blit(title_surf, title_rect)
            self.display_surface.blit(score_surf, score_rect)
            self.display_surface.blit(high_score_surf, high_score_rect)
            self.display_surface.blit(instr_surf, instr_rect)
    
            for event in events:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.game_state = "play"
                    self.reset_game()
    
        async def run(self):
            self.game_music.play(loops=-1)
            while self.running:
                dt = self.clock.tick() / 1000
                events = pygame.event.get()
                for event in events:
                    if event.type == pygame.QUIT or \
                       (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                        self.running = False
    
                if self.game_state == "menu":
                    self.main_menu(events)
                elif self.game_state == "play":
                    self.play_game(dt, events)
                elif self.game_state == "game_over":
                    self.game_over_screen(events)
    
                pygame.display.update()
                await asyncio.sleep(0)
    
            pygame.quit()
            sys.exit()
    
    game = Game()
    await game.run()


asyncio.run(main())
