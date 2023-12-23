import random
from math import sin, pi

import pygame

W, H = 1200, 800
Floor = 200
graviti = 1200


class Point:
    def __init__(self, x, y, size) -> None:
        super().__init__()
        self.x, self.y = x, y
        self.size = size
        self.rect = pygame.Rect(self.x, self.y, size, size)
        self.image = None

    def draw(self, scr):
        if self.image is None:
            raise NotImplementedError()
        scr.blit(self.image, (self.x, self.y))


def dt(): return clock.get_time() / 1000


class Spike(Point):

    def __init__(self, x, y, rect_=False) -> None:
        super().__init__(x, y, 30)
        self.rect_ = rect_
        self.image = pygame.Surface((30, 30))
        pygame.draw.rect(self.image, "red", (0, 0, self.size, self.size), width=2)

    def draw(self, scr):
        p1 = (self.x - self.size // 3, self.y + self.size)
        p2 = (self.x + self.size // 2, self.y - self.size // 3)
        p3 = (self.x + self.size + self.size // 3, self.y + self.size)
        pygame.draw.line(scr, "purple", p1, p2, width=2)
        pygame.draw.line(scr, "purple", p2, p3, width=2)
        pygame.draw.line(scr, "purple", p1, p3, width=2)
        if self.rect_:
            return super().draw(scr)


class Spikes:

    def __init__(self) -> None:
        super().__init__()
        self.spikes = []

    def add(self, spike):
        self.spikes.append(spike)

    def draw(self, scr):
        for spike in self.spikes:
            spike.draw(scr)

    def update(self, player):
        for spike in self.spikes:
            if player.rect.colliderect(spike.rect):
                print("You Lose")
                global lose
                lose = True


class Player(Point):
    def __init__(self) -> None:
        super().__init__(W / 2, H / 2, 50)
        self.vx = 0.
        self.vy = 0.
        self.max = 300
        self.image = pygame.Surface((50, 50))
        pygame.draw.rect(self.image, "purple", (0, 0, self.size, self.size), width=2)
        self.stay = False

    def jump(self):
        if self.stay:
            self.y -= 3
            self.vy -= 500
            self.stay = False

    def left(self):
        self.vx = max(self.vx - 1200 * dt(), -self.max)

    def unleft(self):
        if self.vx < 0:
            self.vx /= 1.1

    def right(self):
        self.vx = min(self.vx + 1200 * dt(), self.max)

    def unright(self):
        if self.vx > 0:
            self.vx /= 1.1

    def calc_v(self):
        self.vy += graviti * dt()

    def floor(self):
        if self.y + self.rect.size[0] >= H - Floor:
            self.vy = 0
            self.y -= abs(self.y + self.rect.size[0]) - (H - Floor)
            self.stay = True

    def update(self):
        self.calc_v()
        self.x += self.vx * dt()
        self.y += self.vy * dt()
        self.floor()
        self.rect.x = self.x
        self.rect.y = self.y


pygame.init()
sc = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()
pl = Player()
spikes = Spikes()
for _ in range(4):
    spike = Spike(random.randint(0, W), H - Floor - 30, True)
    spikes.add(spike)
lose = False
N = 0
while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            quit()
    if not lose:
        pres = pygame.key.get_pressed()
        if pres[pygame.K_w] or pres[pygame.K_SPACE]:
            pl.jump()
        if pres[pygame.K_a]:
            pl.left()
        else:
            pl.unleft()

        if pres[pygame.K_d]:
            pl.right()
        else:
            pl.unright()

        pl.update()
        spikes.update(pl)
        sc.fill(0)
        pygame.draw.line(sc, "purple", (0, H - Floor), (W + 1, H - Floor), width=2)

        pl.draw(sc)
        spikes.draw(sc)
    else:
        sc.blit(pygame.font.Font(None, 57).render("You Lose", True, "purple"), (40, 100))
    pygame.display.flip()
    FPS = 20 + 40 * sin(N / 100 * 2 * pi) ** 2
    N += 1
    clock.tick(9999)
