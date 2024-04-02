
import pygame  
from pygame.locals import *  
import sys     
from itertools import cycle               
SCREENWIDTH = 822  
SCREENHEIGHT = 399  
FPS = 30  


# 定義一個移動地圖class
class MyMap():

    def __init__(self, x, y):
        # 載入背景圖片
        self.bg = pygame.image.load("image/bg.png").convert_alpha()
        self.x = x
        self.y = y

    def map_rolling(self):
        if self.x < -790:  # 小於-790說明地圖已經完全移動完畢
            self.x = 800  # 給地圖一個新的座標點
        else:
            self.x -= 5  #元向左移動

    # 更新地圖
    def map_update(self):
        SCREEN.blit(self.bg, (self.x, self.y))

# 背景音樂按鈕
class Music_Button():
    is_open = True   # 背景音的標記
    def __init__(self):
        self.open_img = pygame.image.load('image/btn_open.png').convert_alpha()
        self.close_img = pygame.image.load('image/btn_close.png').convert_alpha()
        self.bg_music = pygame.mixer.Sound('audio/bg_music.mp3')  # 載入背景音樂
    # 判斷滑鼠是否在按鈕的範圍內
    def is_select(self):
        # 獲取滑鼠的座標
        point_x, point_y = pygame.mouse.get_pos()
        w, h = self.open_img.get_size()             # 獲取按鈕圖片的大小
        # 判斷滑鼠是否在按鈕範圍內
        in_x = point_x > 20 and point_x < 20 + w
        in_y = point_y > 20 and point_y < 20 + h
        return in_x and in_y







# 瑪麗類
class Marie():
    def __init__(self):
        # 初始化小瑪麗長方形
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.jumpState = False  # 跳躍的狀態
        self.jumpHeight = 90  # 跳躍的高度
        self.lowest_y = 323  # 最低座標
        self.jumpValue = 0  # 跳躍增變數
        # 小瑪麗動圖索引
        self.marieIndex = 0
        self.marieIndexGen = cycle([0, 1, 2])
        # 載入小瑪麗圖片
        self.adventure_img = (
            pygame.image.load("image/adventure1.png").convert_alpha(),
            pygame.image.load("image/adventure1.png").convert_alpha(),
            pygame.image.load("image/adventure1.png").convert_alpha(),
        )
        self.jump_audio = pygame.mixer.Sound('audio/jump.ogg')  # 跳音效
        self.rect.size = self.adventure_img[0].get_size()
        self.x = 50;  # 繪製小瑪麗的X座標
        self.y = self.lowest_y;  # 繪製小瑪麗的Y座標
        self.rect.topleft = (self.x, self.y)

    # 跳狀態
    def jump(self):
        self.jumpState = True

    # 小瑪麗移動
    def move(self):
        if self.jumpState:  # 當起跳的時候
            if self.rect.y >= self.lowest_y:  # 如果站在地上
                self.jumpValue = -4  # 以5個圖元值向上移動
            if self.rect.y <= self.lowest_y - self.jumpHeight:  # 小瑪麗到達頂部回落
                self.jumpValue = 4  # 以5個圖元值向下移動
            self.rect.y += self.jumpValue  # 通過迴圈改變瑪麗的Y座標
            if self.rect.y >= self.lowest_y:  # 如果小瑪麗回到地面
                self.jumpState = False  # 關閉跳躍狀態

    # 繪製小瑪麗
    def draw_marie(self):
        # 匹配小瑪麗動圖
        marieIndex = next(self.marieIndexGen)
        # 繪製小瑪麗
        SCREEN.blit(self.adventure_img[marieIndex],
                    (self.x, self.rect.y))

import random  # 亂數
# 障礙物類
class Obstacle():
    score = 1  # 分數
    move = 5   # 移動距離
    obstacle_y = 336  # 障礙物y座標
    def __init__(self):
        # 初始化障礙物矩形
        self.rect = pygame.Rect(0, 0, 0, 0)
        # 載入障礙物圖片
        self.missile = pygame.image.load("image/missile.png").convert_alpha()
        self.pipe = pygame.image.load("image/pipe2.png").convert_alpha()
        # 載入分數圖片
        self.numbers = (pygame.image.load('image/0.png').convert_alpha(),
                        pygame.image.load('image/1.png').convert_alpha(),
                        pygame.image.load('image/2.png').convert_alpha(),
                        pygame.image.load('image/3.png').convert_alpha(),
                        pygame.image.load('image/4.png').convert_alpha(),
                        pygame.image.load('image/5.png').convert_alpha(),
                        pygame.image.load('image/6.png').convert_alpha(),
                        pygame.image.load('image/7.png').convert_alpha(),
                        pygame.image.load('image/8.png').convert_alpha(),
                        pygame.image.load('image/9.png').convert_alpha())
        # 載入加分音效
        self.score_audio = pygame.mixer.Sound('audio/score.wav')  # 加分
        # 0和1亂數
        r = random.randint(0, 1)
        if r == 0:  # 如果亂數為0顯示導彈障礙物相反顯示管道
            self.image = self.missile   # 顯示導彈障礙
            self.move = 15              # 移動速度加快
            self.obstacle_y = 100       # 導彈座標在天上
        else:
            self.image = self.pipe      # 顯示管道障礙
        # 根據障礙物點陣圖的寬高來設置矩形
        self.rect.size = self.image.get_size()
        # 獲取點陣圖寬高
        self.width, self.height = self.rect.size
        # 障礙物繪製座標
        self.x = 800
        self.y = self.obstacle_y
        self.rect.center = (self.x, self.y)

    # 障礙物移動
    def obstacle_move(self):
        self.rect.x -= self.move

    # 繪製障礙物
    def draw_obstacle(self):
        SCREEN.blit(self.image, (self.rect.x, self.rect.y))

    # 獲取分數
    def getScore(self):
        self.score
        tmp = self.score;
        if tmp == 1:
            self.score_audio.play()  # 播放加分音樂
        self.score = 0;
        return tmp;

    # 顯示分數
    def showScore(self, score):
        # 獲取得分數字
        self.scoreDigits = [int(x) for x in list(str(score))]
        totalWidth = 0  # 要顯示的所有數位的總寬度
        for digit in self.scoreDigits:
            # 獲取積分圖片的寬度
            totalWidth += self.numbers[digit].get_width()
        # 分數橫向位置
        Xoffset = (SCREENWIDTH - (totalWidth+30))
        for digit in self.scoreDigits:
            # 繪製分數
            SCREEN.blit(self.numbers[digit], (Xoffset, SCREENHEIGHT * 0.1))
            # 隨著數字增加改變位置
            Xoffset += self.numbers[digit].get_width()

# 遊戲結束的方法
def game_over():
    bump_audio = pygame.mixer.Sound('audio/bump.wav')  # 撞擊
    bump_audio.play()  # 播放撞擊音效
    # 獲取表單寬、高
    screen_w = pygame.display.Info().current_w
    screen_h = pygame.display.Info().current_h
    # 載入遊戲結束的圖片
    over_img = pygame.image.load('image/gameover.png').convert_alpha()
    # 將遊戲結束的圖片繪製在表單的中間位置
    SCREEN.blit(over_img, ((screen_w - over_img.get_width()) / 2,
                                       (screen_h - over_img.get_height()) / 2))


def mainGame():
    score = 0  # 得分
    over = False  # 遊戲結束標記
    global SCREEN, FPSCLOCK
    pygame.init()  # 經過初始化以後我們就可以盡情地使用pygame了。

    # 使用Pygame時鐘之前，必須先創建Clock物件的一個實例，
    # 控制每個迴圈多長時間運行一次。
    FPSCLOCK = pygame.time.Clock()
    SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))  # 通常來說我們需要先創建一個視窗，方便我們與程式的交互。
    pygame.display.set_caption('超級瑪麗')  # 設置視窗標題

    # 創建地圖對象
    bg1 = MyMap(0, 0)
    bg2 = MyMap(800, 0)

    # 創建小瑪麗對象
    marie = Marie()

    addObstacleTimer = 0  # 添加障礙物的時間
    list = []  # 障礙物對象清單

    music_button = Music_Button()     # 創建背景音樂按鈕物件
    btn_img  = music_button.open_img  # 設置背景音樂按鈕的預設圖片
    music_button.bg_music.play(-1)    # 迴圈播放背景音樂

    while True:
        # 獲取按一下事件
        for event in pygame.event.get():

            if event.type == pygame.MOUSEBUTTONUP:  # 判斷滑鼠事件
                if music_button.is_select():        # 判斷滑鼠是否在靜音按鈕範圍
                    if music_button.is_open:        # 判斷背景音樂狀態
                        btn_img = music_button.close_img # 按一下後顯示關閉狀態的圖片
                        music_button.is_open = False    # 關閉背景音樂狀態
                        music_button.bg_music.stop()    # 停止背景音樂的播放
                    else:
                        btn_img = music_button.open_img
                        music_button.is_open = True
                        music_button.bg_music.play(-1)
            # 如果按一下了關閉視窗就將視窗關閉
            if event.type == QUIT:
                pygame.quit()  # 退出窗口
                sys.exit()  # 關閉窗口

            # 按一下鍵盤空白鍵，開啟跳的狀態
            if event.type == KEYDOWN and event.key == K_UP:
                if marie.rect.y >= marie.lowest_y:  # 如果小瑪麗在地面上
                    marie.jump_audio.play()  # 播放小瑪麗跳躍音效
                    marie.jump()  # 開啟小瑪麗跳的狀態

                if over == True:  # 判斷遊戲結束的開關是否開啟
                    mainGame()  # 如果開啟將調用mainGame方法重新啟動遊戲




        if over == False:
            # 繪製地圖起到更新地圖的作用
            bg1.map_update()
            # 地圖移動
            bg1.map_rolling()
            bg2.map_update()
            bg2.map_rolling()

            # 小瑪麗移動
            marie.move()
            # 繪製小瑪麗
            marie.draw_marie()

            # 計算障礙物間隔時間
            if addObstacleTimer >= 1300:
                r = random.randint(0, 100)
                if r > 40:
                    # 創建障礙物對象
                    obstacle = Obstacle()
                    # 將障礙物對象添加到清單中
                    list.append(obstacle)
                # 重置添加障礙物時間
                addObstacleTimer = 0

            # 迴圈遍歷障礙物
            for i in range(len(list)):
                # 障礙物移動
                list[i].obstacle_move()
                # 繪製障礙物
                list[i].draw_obstacle()

                # 判斷小瑪麗與障礙物是否碰撞
                if pygame.sprite.collide_rect(marie, list[i]):
                    over = True  # 碰撞後開啟結束開關
                    game_over()  # 調用遊戲結束的方法
                    music_button.bg_music.stop()
                else:
                    # 判斷小瑪麗是否躍過了障礙物
                    if (list[i].rect.x + list[i].rect.width) < marie.rect.x:
                        # 加分
                        score += list[i].getScore()
                # 顯示分數
                list[i].showScore(score)

        addObstacleTimer += 20  # 增加障礙物時間
        SCREEN.blit(btn_img, (20, 20)) # 繪製背景音樂按鈕
        pygame.display.update()  # 更新整個視窗
        FPSCLOCK.tick(FPS)  # 迴圈應該多長時間運行一次


if __name__ == '__main__':
    mainGame()
