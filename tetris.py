import pygame
import random

black = (0, 0, 0)
white = (255, 255, 255)
gray = (128, 128, 128)

yellow = (255, 215, 0)
red = (255, 0, 0)
blue = (0, 255, 255)
green = (0, 255, 0)
pink = (255, 20, 147)
orange = (255, 69, 0)
purple = (255, 0, 255)

colors = [yellow, red, blue, green, pink, orange, purple]

class Figure:
    figures = [
        [[1, 5, 9, 13], [4, 5, 6, 7]],
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
        [[1, 2, 5, 6]],
    ]
    x = 0
    y = 0
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.randint(0, len(self.figures) - 1)
        self.color = random.randint(1, len(colors) - 1)
        self.rotation = 0
    
    def image(self):
        return self.figures[self.type][self.rotation]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.figures[self.type])

class Tetris:
    level = 2
    score = 0
    matrix = []
    figure = None
    x = 150
    y = 100 - 2
    rows = 0
    cols = 0
    size = 30
    state = 'start'

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.matrix = [[0 for j in range(self.cols)] for i in range(self.rows)]
        # for i in range(rows):
        #     new_line = []
        #     for j in range(cols):
        #         new_line.append(0)
        #     self.matrix.append(new_line)

    def new_figure(self):
        self.figure = Figure(3, 0)

    def intersects(self):
        intersection = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    if i + self.figure.y > self.rows - 1 or \
                            j + self.figure.x > self.cols - 1 or \
                            j + self.figure.x < 0 or \
                            self.matrix[i + self.figure.y][j + self.figure.x] > 0:
                        
                        intersection = True

        return intersection

    def freeze(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    self.matrix[i + self.figure.y][j + self.figure.x] = self.figure.color

        self.break_lines()
        self.new_figure()
        if self.intersects():
            game.state = 'gameover'

    def break_lines(self):
        lines = 0
        for i in range(1, self.rows):
            zeros = 0
            for j in range(self.cols):
                if self.matrix[i][j] == 0:
                    zeros += 1
            if zeros == 0:
                lines += 1
                for i1 in range(i, 1, -1):
                    for j in range(self.cols):
                        self.matrix[i1][j] = self.matrix[i1 - 1][j]

        self.score += lines ** 2

    def go_space(self):
        while not self.intersects():
            self.figure.y += 1
        self.figure.y -= 1
        self.freeze()

    def go_down(self):
        self.figure.y += 1
        if self.intersects():
            self.figure.y -= 1
            self.freeze()

    def go_side(self, dx):
        old_x = self.figure.x
        self.figure.x += dx
        if self.intersects():
            self.figure.x = old_x

    def rotate(self):
        old_rotation = self.figure.rotation
        self.figure.rotate()
        if self.intersects():
            self.figure.rotation = old_rotation


pygame.init()

width, height = 600, 700
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('TETRIS')

def main():
    global game

    run = True
    clock = pygame.time.Clock()
    fps = 25
    counter = 0
    pressing_down = False
    game = Tetris(20, 10)

    while run:
        if game.figure is None:
            game.new_figure()
        counter += 1
        if counter > 100000:
            counter = 0

        if counter % (fps // game.level // 2) == 0 or pressing_down:
            if game.state == 'start':
                game.go_down()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game.go_side(-1)
                if event.key == pygame.K_RIGHT:
                    game.go_side(1)
                if event.key == pygame.K_UP:
                    game.rotate()
                if event.key == pygame.K_DOWN:
                    pressing_down = True
                if event.key == pygame.K_SPACE:
                    game.go_space()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    pressing_down = False

        screen.fill(black)

        for i in range(game.rows):
            for j in range(game.cols):
                pygame.draw.rect(screen, gray, (game.x+game.size*j, game.y+game.size*i, game.size, game.size), 1)
                if game.matrix[i][j] > 0:
                    pygame.draw.rect(screen, colors[game.matrix[i][j]],
                    [game.x+game.size*j, game.y+game.size*i, game.size-2, game.size-1])

        if game.figure is not None:
            for i in range(4):
                for j in range(4):
                    p = i * 4 + j
                    if p in game.figure.image():
                        pygame.draw.rect(screen, colors[game.figure.color], 
                        [game.x+game.size*(j+game.figure.x), game.y+game.size*(i+game.figure.y), game.size-2, game.size-2])

        font = pygame.font.SysFont('consolas', 25, True, False)
        font1 = pygame.font.SysFont('freesansbold.ttf', 70, True, False)
        text = font.render('SCORE: ' + str(game.score), True, white)
        text1 = font1.render('GAMEOVER' , True, red)
        text1_rect = text1.get_rect(center=(600//2, 700//2))
        
        screen.blit(text, (10, 10))
        if game.state == 'gameover':
            screen.blit(text1, text1_rect)
            run = False
        
        pygame.display.flip()
        clock.tick(fps)
        
    pygame.time.delay(2000)
    main_menu()

def main_menu():
    run = True
    while run:
        screen.fill(black)
        font1 = pygame.font.SysFont('comicsans', 60, True, False)
        text1 = font1.render('Press any key to begin...' , True, white)
        text1_rect = text1.get_rect(center=(600//2, 700//2))
        screen.blit(text1, text1_rect)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main()
    pygame.quit()

if __name__ == '__main__':
    main_menu()


            

        
    


                        


