import pygame
import random
import sys
import time
import sqlite3 as sq 


class Game:
    pygame.init()
 
    def __init__(self):
        self.attempt = 1
        self.l = 750
        self.h = 500
        self.start = True
        self.end = False
        self.font = 35
        self.input = ""
        self.words = ""
        self.msg = "SPEED TYPING TEST"
        self.x_pos = None
        self.string_length = None
        self.current_word = ""
        self.time_start = 0
        self.total_time = 0
        self.accuracy = 0
        self.wpm = 0

        pygame.init()
        self.surface = pygame.display.set_mode((self.l, self.h))
        self.restart_icon = pygame.image.load('restart.png')
        pygame.display.set_caption('Typing Speed Test')

        pygame.display.update()

    def para(self):
        self.words = open("text.txt").read()
        self.words = self.words.split('.')
        self.words = random.choice(self.words)
        self.words = self.words.split(' ')[1:12]
        self.words = ' '.join([str(elem) for elem in self.words])
        self.draw_text(self.surface, self.words, 26, self.l / 2, 220, (250, 250, 250))
        self.string_length = int(len(self.words) / 2)

        pygame.display.update()

    def draw_text(self, surface, inputText, f, l, y, colour):
        font = pygame.font.Font(None, f)
        text = font.render(inputText, 2, colour)
        text_rect = text.get_rect(center=(int(l), y))
        surface.blit(text, text_rect)
        pygame.display.update()

    def run(self):
        self.reset()
        self.end = False
        clock = pygame.time.Clock()
        while True:
            self.surface.fill((0, 0, 0), (50, 250, 650, 50))
            pygame.draw.rect(self.surface, (250, 250, 250), (50, 250, 650, 50), 2)
            self.draw_text(self.surface, self.input, 28, self.l / 2, 290, (250, 250, 250))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()
                    # input box
                    if 50 <= x <= 700 and 250 <= y <= 300:
                        self.start = True
                        self.time_start = time.time()
                    # reset button
                    elif 250 <= x <= 300 and 400 <= y <= 450:
                        self.reset()
                        self.run()
                    # stop practice
                    elif 450 <= x <= 650 and 400 <= y <= 450:
                        self.surface.fill((0,0,0))
                        self.start_protocal()

                elif event.type == pygame.KEYDOWN:
                    if self.start == True and self.end == False:
                        if event.key == pygame.K_BACKSPACE:
                            self.input = self.input[:-1]
                        elif event.key == pygame.K_RETURN:
                            self.calculation(self.surface)
                            self.database()
                            self.end = True

                        else:
                            try:
                                self.current_word = event.unicode
                                self.input += self.current_word
                            except:
                                pass
                        self.recon()

                pygame.display.update()
            clock.tick(60)
            # self.attempt+=1

    def reset(self):
        self.surface.fill((0, 0, 0))
        self.surface.fill((0, 0, 0), (0, 200, 750, 49))
        self.attempt = 0
        self.para()
        self.surface.blit(self.restart_icon, (250, 400))
        pygame.draw.rect(self.surface, (250, 250, 250), (450, 400, 200, 50), 2)
        self.draw_text(self.surface, 'STOP PRACTICE', 30, 550, 425, (250, 250, 250))
        self.draw_text(self.surface, self.msg, 80, self.l / 2, 70, (250, 250, 250))
        self.start = False
        self.end = True
        self.input = ""
        self.time_start = 0
        self.total_time = 0
        self.wpm = 0
        pygame.display.update()

    def recon(self):
        self.x_pos = (375 - self.string_length * 8)
        for i, c in enumerate(self.input):
            if c != self.words[i]:
                self.surface.fill((250, 0, 0), (self.x_pos + (i * 8), 230, 10, 2))
            elif c == self.words[i]:
                self.surface.fill((0, 0, 0), (self.x_pos + (i * 8), 230, 10, 2))

        pygame.display.update()

    def calculation(self, surface):
        if not self.end:
            self.total_time = time.time() - self.time_start
            count = 0
            for i, c in enumerate(self.words):
                try:
                    if self.input[i] == c:
                        count += 1
                except:
                    pass
            self.accuracy = count / len(self.words) * 100
            # Calculate words per minute
            self.wpm = len(self.input) * 60 / (5 * self.total_time)
            self.end = True

    def database(self):
        conn = sq.connect('save_db.sqlite')
        cur = conn.cursor()
        cur.execute(
            '''CREATE TABLE IF NOT EXISTS data (attempt VARCHAR, wpm VARCHAR, accuracy VARCHAR, time VARCHAR)''')
        cur.execute('SELECT * FROM data ORDER BY attempt DESC LIMIT 1')
        row = cur.fetchone()
        try:
            self.attempt = int(row[0]) + 1
        except:
            self.attempt = 1
        cur.execute('INSERT INTO data (attempt, wpm, accuracy, time) values (?, ?, ?, ?)',
                    (self.attempt, self.wpm, self.accuracy, self.total_time))
        conn.commit()

    ############

    def start_protocal(self):

        while True:

            self.draw_text(self.surface, self.msg, 100, self.l / 2, 100, (250, 250, 250))
            # Start
            pygame.draw.rect(self.surface, (250, 250, 250), (325, 300, 100, 50), 2)
            self.draw_text(self.surface, 'START', 30, 375, 325, (250, 250, 250))
            # Stats
            pygame.draw.rect(self.surface, (250, 250, 250), (50, 300, 100, 50), 2)
            self.draw_text(self.surface, 'STATS', 30, 100, 325, (250, 250, 250))
            # Exit
            pygame.draw.rect(self.surface, (250, 250, 250), (600, 300, 100, 50), 2)
            self.draw_text(self.surface, 'EXIT', 30, 650, 325, (250, 250, 250))
            # Instructions
            pygame.draw.rect(self.surface, (250, 250, 250), (250, 425, 250, 50), 2)
            self.draw_text(self.surface, 'INSTRUCTIONS', 30, 375, 450, (250, 250, 250))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()
                    # start button
                    if 325 <= x <= 425 and 300 <= y <= 350:
                        self.run()
                        # exit button
                    elif 600 <= x <= 700 and 300 <= y <= 350:
                        sys.exit()

            pygame.display.update()
    def statistics(self):
        # page 1
        #self.surface.fill((0,0,0))
        self.wpm = []
        self.attempt = []
        self.accuracy = []
        self.total_time = []
        con = sq.connect('save_db.sqlite')
        cur = con.cursor()
        cur.execute('SELECT attempt FROM data')
        temp_row1 = cur.fetchall()
        cur.execute('SELECT wpm FROM data')
        temp_row2 = cur.fetchall()
        cur.execute('SELECT accuracy FROM data')
        temp_row3 = cur.fetchall()
        cur.execute('SELECT time FROM data')
        temp_row4 = cur.fetchall()
        for i,j,k,l in temp_row1,temp_row2,temp_row3,temp_row4:
            self.attempt.append(int(i[0]))
            self.wpm.append(int(j[0]))
            self.accuracy.append(int(k[0]))
            self.accuracy.append(int(l[0]))





Game().statistics()#start_protocal()
