# 导入所需的库和模块
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from subprocess import *
from threading import *
from time import *
import os
import random
import datetime



# 定义Move类，表示棋盘上的移动
class Move:
    NONE = 0
    BLACK = 1
    WHITE = 2
    EDGE = 19

    # 初始化方法，设置移动的初始状态
    def __init__(self, color=NONE, x1=-1, y1=-1, x2=-1, y2=-1):
        self.color = color
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    # 返回移动的字符串表示
    def __str__(self):
        return 'color: {0}, x1: {1}, y1: {2}, x2: {3}, y2: {4}'.format(self.color, self.x1, self.y1, self.x2, self.y2)

    # 从命令行字符串创建移动对象
    def fromCmd(cmd, color=None):
        # print(cmd);
        # print(self);
        cmd = cmd.strip()
        if cmd.startswith('move '):
            cmd = cmd[5:].upper()
            if len(cmd) == 2:
                cmd = cmd * 2
            m = Move(color)
            m.x1 = ord(cmd[0]) - ord('A')
            m.y1 = ord(cmd[1]) - ord('A')
            m.x2 = ord(cmd[2]) - ord('A')
            m.y2 = ord(cmd[3]) - ord('A')
            return m

        return None

    # 将移动对象转换为命令行字符串
    def toCmd(self):
        cmd = 'move ' + self.cmd() + '\n'
        print('Cmd:', cmd)
        return cmd

    # 将移动对象转换为放置命令行字符串
    def toPlaceCmd(self):
        if self.color == Move.BLACK:
            cmd = 'black '
        elif self.color == Move.WHITE:
            cmd = 'white '
        else:
            return 'None Place Cmd\n'
        cmd += self.cmd() + '\n'
        # print('Cmd:', cmd);
        return cmd

    # 获取移动的命令行表示
    def cmd(self):
        base = ord('A')
        return chr(base + self.x1) + chr(base + self.y1) + chr(base + self.x2) + chr(base + self.y2)

    # 使移动对象无效
    def invalidate(self):
        self.color = None
        self.x1 = -1
        self.y1 = -1
        self.x2 = -1
        self.y2 = -1

    # 验证移动是否有效
    def isValidated(self):
        if self.color != Move.BLACK and self.color != Move.WHITE:
            return False
        if Move.isValidPosition(self.x1, self.y1) and Move.isValidPosition(self.x2, self.y2):
            return True

        return False

    # 验证位置是否在棋盘内
    def isValidPosition(x, y):
        if 0 <= x < Move.EDGE and 0 <= y < Move.EDGE:
            return True
        return False


# 定义GameEngine类，处理游戏引擎的交互
class GameEngine:
    def __init__(self):
        self.fileName = GameEngine.getEngine()
        self.proc = None
        self.move = Move()
        self.color = Move.NONE
        self.setName('Unknown')

    # 获取默认引擎文件名
    def getEngine():
        defaultEngineFile = 'engines/Hblgxy_YQ.exe'
        return defaultEngineFile

    # 初始化游戏引擎
    def init(self, fileName=None, depth=None, vcf=None):
        self.release()

        if fileName is not None and fileName.strip() != '':
            self.fileName = fileName
        else:
            fileName = self.fileName
        if os.name == 'nt':
            # Windows NT hide
            startupinfo = STARTUPINFO()
            startupinfo.dwFlags |= STARTF_USESHOWWINDOW
            self.proc = Popen(fileName, stdin=PIPE, stdout=PIPE, bufsize=0, startupinfo=startupinfo)
        else:
            self.proc = Popen(fileName, stdin=PIPE, stdout=PIPE, bufsize=0)

        # game engine name
        self.setName(fileName)
        self.sendCmd('name\n')
        while True:
            msg = self.waitForNextMsg()
            if msg.startswith('name '):
                self.setName(msg.split(' ')[1])
                break

        if depth is not None:
            cmd = 'depth ' + str(depth) + '\n'
            # print(cmd);
            self.sendCmd(cmd)
        if vcf is not None:
            if vcf:
                cmd = 'vcf\n'
            else:
                cmd = 'unvcf\n'
            # print(cmd);
            self.sendCmd(cmd)

        self.move.invalidate()

        return True

    # 设置引擎名称
    def setName(self, name):
        self.name = self.shortName = name
        if len(self.shortName) > 10 and self.shortName.find('.') > -1:
            ls = self.shortName.split('.')
            for i in ls:
                if i != '':
                    self.shortName = i
                    break
        if len(self.shortName) > 10:
            self.shortName = self.shortName[:8] + '...'

    # 释放进程资源
    def release(self):
        while self.proc is not None:
            if self.proc.poll() == None:
                self.proc.terminate()
                # self.sendCmd('quit\n');
                # print('Release');
                sleep(0.2)
            else:
                self.proc = None
                break
        self.move.invalidate()

    # 发送'next'命令并处理移动列表
    def next(self, moveList=[]):
        if self.proc is not None:
            cmd = 'new xxx\n'
            self.sendCmd(cmd)
            for m in moveList:
                cmd = m.toPlaceCmd()
                self.sendCmd(cmd)

            cmd = 'next\n'
            self.sendCmd(cmd)

    # 向进程发送命令
    def sendCmd(self, cmd):
        if self.proc is not None:
            try:
                # print('sendCmd to stdin:', cmd);
                if len(cmd) < 1 or cmd[-1] != '\n':
                    # Add ret in the end;
                    cmd += '\n'
                self.proc.stdin.write(cmd.encode())
            except Exception as e:
                print('Error for sendCmd:', cmd, str(e))

    # 等待并获取进程的下一个消息
    def waitForNextMsg(self):
        if self.proc is not None:
            try:
                # print('Waiting');
                self.msg = self.proc.stdout.readline().decode()
                # print('out:', self.msg);
            except Exception as e:
                print('Error for waitForNextMsg:', str(e))
        return self.msg


class GameState:
    Exit = -1

    Idle = 0
    AI2Human = 2

    WaitForEngine = 1
    WaitForHumanFirst = 2
    WaitForHumanSecond = 3

    Win = 4


# 定义游戏状态类
def create_left_side_labels(frame):
    BOARD_SIZE = 19
    for i in range(BOARD_SIZE):
        label = Label(frame, text=str(i + 1), width=3, pady=7, anchor=E)
        label.pack(side=BOTTOM, fill=X)

        # 创建底部坐标标签方法


def create_bottom_side_labels(frame):
    BOARD_SIZE = 19
    for i in range(BOARD_SIZE):
        label = Label(frame, text=chr(ord('A') + i), width=3, padx=6, anchor=W)
        label.pack(side=LEFT, fill=Y)


class App(Frame):

    # 窗口初始化
    def __init__(self, master=None):
        Frame.__init__(self, master, width=640, height=700)
        self.pack()

        self.gameMode = GameState.Idle
        self.gameState = GameState.Idle

        self.initResource()
        self.createBoard()

        self.initBoard()

    # 控制模块的创建
    def initResource(self):
        # Images sets.
        self.images = {}
        im = self.images
        im['go_u'] = PhotoImage(file='imgs/go_u.gif')
        im['go_ul'] = PhotoImage(file='imgs/go_ul.gif')
        im['go_ur'] = PhotoImage(file='imgs/go_ur.gif')
        im['go'] = PhotoImage(file='imgs/go.gif')
        im['go_l'] = PhotoImage(file='imgs/go_l.gif')
        im['go_r'] = PhotoImage(file='imgs/go_r.gif')
        im['go_d'] = PhotoImage(file='imgs/go_d.gif')
        im['go_dl'] = PhotoImage(file='imgs/go_dl.gif')
        im['go_dr'] = PhotoImage(file='imgs/go_dr.gif')
        im['go_-'] = PhotoImage(file='imgs/go_-.gif')
        im['go_b'] = PhotoImage(file='imgs/go_b.gif')
        im['go_w'] = PhotoImage(file='imgs/go_w.gif')
        im['go_bt'] = PhotoImage(file='imgs/go_bt.gif')
        im['go_wt'] = PhotoImage(file='imgs/go_wt.gif')

        # 设置行和列的权重
        self.grid_rowconfigure(0, weight=0)  # 设置第0行的权重为0，使其不可伸缩
        self.grid_rowconfigure(1, weight=1)  # 设置第1行的权重为1，使其可伸缩
        self.grid_rowconfigure(2, weight=0)  # 设置第2行的权重为0，使其不可伸缩
        self.grid_columnconfigure(0, weight=0)  # 设置第0列的权重为0，使其不可伸缩
        self.grid_columnconfigure(1, weight=1)  # 设置第1列的权重为1，使其可伸缩

        self.gameEngine = GameEngine()
        self.searchThread = Thread(target=self.searching)
        self.searchThread.start()

        # 创建Canvas
        self.canvas = Canvas(self, width=640, height=640, bg='white')
        self.canvas.grid(row=1, column=1, sticky=NSEW)

        # 在Canvas的左边放置坐标
        self.left_frame = Frame(self, width=40, height=640)  # 设置Frame的宽度和高度
        self.left_frame.grid(row=1, column=0, sticky=NS)
        create_left_side_labels(self.left_frame)

        # 在Canvas的下边放置坐标
        self.bottom_frame = Frame(self, height=40)  # 设置Frame的高度
        self.bottom_frame.grid(row=2, column=1, sticky=EW)
        create_bottom_side_labels(self.bottom_frame)

        # 创建控制框架并放置在棋盘下方
        self.controlFrame = Frame(self)
        self.controlFrame.grid(row=2, column=0, sticky=EW)

        # 在控制框架中创建先后手选择框
        labelframe = LabelFrame(self.controlFrame, text='先后手')
        labelframe.pack(side=LEFT, fill=BOTH, expand=1)

        self.aiSelected = StringVar(value='xianshou')
        labelframe.humanRBtn = Radiobutton(labelframe, text="AI后手", variable=self.aiSelected, value='xianshou')
        labelframe.humanRBtn.select()
        labelframe.humanRBtn.pack(anchor=W)
        labelframe.engineRBtn = Radiobutton(labelframe, text="AI先手", variable=self.aiSelected, value='houshou', )
        labelframe.engineRBtn.pack(anchor=W)

        # 在控制框架中创建控制模块
        labelframe = LabelFrame(self.controlFrame, text='控制模块')
        labelframe.pack(side=LEFT, fill=BOTH, expand=1)

        labelframe.newBtn = Button(labelframe, text='开始对局', command=self.newGame)
        labelframe.newBtn.pack(side=TOP, fill=X)
        labelframe.backBtn = Button(labelframe, text='悔棋', command=self.backMove)
        labelframe.backBtn.pack(fill=X)
        labelframe.quitBtn = Button(labelframe, text='结束对局', command=self.master.destroy)
        labelframe.quitBtn.pack(fill=X)

    # 创建左侧坐标标签方法

    # 初始化游戏引擎方法
    def initGameEngine(self, fileName=''):
        self.gameEngine.init(fileName, 6, 1)

    # 创建棋盘单元格方法
    def createBoardUnit(self, x, y, imageKey):
        lb = Label(self.canvas, height=32, width=32)
        lb.x = x
        lb.y = y
        lb['image'] = self.images[imageKey]
        lb.initImage = self.images[imageKey]
        lb.bind('<Button-1>', self.onClickBoard)
        self.gameBoard[x][y] = lb
        return lb

    # 棋盘的创建与初始化
    def createBoard(self):
        self.gameBoard = [[0 for i in range(Move.EDGE)] for i in range(Move.EDGE)]
        self.moveList = []
        gameBoard = self.gameBoard

        self.createBoardUnit(0, 0, 'go_ul')
        for j in range(1, 18):
            self.createBoardUnit(0, j, 'go_u')
        self.createBoardUnit(0, 18, 'go_ur')

        for i in range(1, 18):
            gameBoard[i][0] = self.createBoardUnit(i, 0, 'go_l')
            for j in range(1, 18):
                gameBoard[i][j] = self.createBoardUnit(i, j, 'go')

            gameBoard[i][18] = self.createBoardUnit(i, 18, 'go_r')

        self.createBoardUnit(3, 3, 'go_-')
        self.createBoardUnit(3, 9, 'go_-')
        self.createBoardUnit(3, 15, 'go_-')
        self.createBoardUnit(9, 3, 'go_-')
        self.createBoardUnit(9, 9, 'go_-')
        self.createBoardUnit(9, 15, 'go_-')
        self.createBoardUnit(15, 3, 'go_-')
        self.createBoardUnit(15, 9, 'go_-')
        self.createBoardUnit(15, 15, 'go_-')

        self.createBoardUnit(18, 0, 'go_dl')
        for j in range(1, 18):
            self.createBoardUnit(18, j, 'go_d')
        self.createBoardUnit(18, 18, 'go_dr')

    # 悔棋方法
    def backMove(self):
        if self.gameMode == GameState.AI2Human:
            if self.gameState == GameState.WaitForHumanFirst:
                if self.gameMode == GameState.AI2Human and len(self.moveList) > 1:
                    self.unmakeTopMove()
                    self.unmakeTopMove()
                elif len(self.moveList) > 0:
                    self.unmakeTopMove()
            elif self.gameState == GameState.WaitForHumanSecond:
                self.unplaceColor(self.move.x1, self.move.y1)
                self.toGameState(GameState.WaitForHumanFirst)

    # 初始化棋盘方法
    def initBoard(self):
        self.moveList = []
        for i in range(Move.EDGE):
            for j in range(Move.EDGE):
                self.unplaceColor(i, j)

    # 移除颜色方法
    def unplaceColor(self, i, j):
        gameBoard = self.gameBoard
        gameBoard[i][j]['image'] = gameBoard[i][j].initImage
        gameBoard[i][j].color = 0
        gameBoard[i][j].grid(row=i, column=j)

    # 检查连接方向方法
    def connectedByDirection(self, x, y, dx, dy):
        gameBoard = self.gameBoard
        cnt = 1
        xx = dx
        yy = dy
        while Move.isValidPosition(x + xx, y + yy) and gameBoard[x][y].color == gameBoard[x + xx][y + yy].color:
            xx += dx
            yy += dy
            cnt += 1
        xx = -dx
        yy = -dy
        while Move.isValidPosition(x + xx, y + yy) and gameBoard[x][y].color == gameBoard[x + xx][y + yy].color:
            xx -= dx
            yy -= dy
            cnt += 1
        if cnt >= 6:
            return True
        return False

    # 检查连接方法
    def connectedBy(self, x, y):
        # Four direction
        if self.connectedByDirection(x, y, 1, 1):
            return True
        if self.connectedByDirection(x, y, 1, -1):
            return True
        if self.connectedByDirection(x, y, 1, 0):
            return True
        if self.connectedByDirection(x, y, 0, 1):
            return True
        return False

    # 检查胜利方法
    def isWin(self, move):
        if move.isValidated():
            return self.connectedBy(move.x1, move.y1) or self.connectedBy(move.x2, move.y2)
        return False

    # 获取下一个颜色方法
    def nextColor(self):
        color = Move.BLACK
        if len(self.moveList) % 2 == 1:
            color = Move.WHITE
        return color

    # 等待移动方法
    def waitForMove(self):
        color = self.nextColor()
        while True:
            msg = self.gameEngine.waitForNextMsg()
            move = Move.fromCmd(msg, color)
            if move is not None:
                break

        return move

    # 搜索方法
    def searching(self):
        while True:
            try:
                if self.gameState == GameState.Exit:
                    break
                if self.gameMode == GameState.AI2Human:
                    if self.gameState == GameState.WaitForEngine:
                        self.gameEngine.next(self.moveList)
                        move = self.waitForMove()
                        self.gameEngine.color = move.color
                        self.makeMove(move)
                        if self.gameState == GameState.WaitForEngine and self.gameMode == GameState.AI2Human:
                            self.toGameState(GameState.WaitForHumanFirst)
                    else:
                        sleep(0.1)
                else:
                    sleep(0.2)
            except Exception as e:
                print('Exception when searching: ' + str(e))
                sleep(0.5)

    # 获取相反颜色方法
    def otherColor(self, color):
        if color == Move.BLACK:
            return Move.WHITE
        elif color == Move.WHITE:
            return Move.BLACK
        return Move.NONE

    # 新游戏方法
    def newGame(self):
        self.gameEngine.release()
        self.initBoard()
        self.initGameEngine()
        self.toGameMode(GameState.AI2Human)
        if self.aiSelected.get().strip() == 'xianshou':
            self.toGameState(GameState.WaitForHumanFirst)
        else:
            self.toGameState(GameState.WaitForEngine)

    # 添加到移动列表方法
    def addToMoveList(self, move):
        n = len(self.moveList)
        if n > 0:
            m = self.moveList[n - 1]
            self.placeColor(m.color, m.x1, m.y1)
            self.placeColor(m.color, m.x2, m.y2)

        self.moveList.append(move)

    # 取消顶部移动方法
    def unmakeTopMove(self):
        if len(self.moveList) > 0:
            m = self.moveList[-1]
            self.moveList = self.moveList[:-1]
            self.unplaceColor(m.x1, m.y1)
            self.unplaceColor(m.x2, m.y2)
            if len(self.moveList) > 0:
                m = self.moveList[-1]
                self.placeColor(m.color, m.x1, m.y1, 't')
                self.placeColor(m.color, m.x2, m.y2, 't')

    # 制作移动方法
    def makeMove(self, move):
        if move.isValidated():
            self.placeStone(move.color, move.x1, move.y1)
            self.placeStone(move.color, move.x2, move.y2)
            self.addToMoveList(move)
        return move

    # 放置颜色方法
    def placeColor(self, color, x, y, extra=''):
        if color == Move.BLACK:
            imageKey = 'go_b'
        elif color == Move.WHITE:
            imageKey = 'go_w'
        else:
            return
        imageKey += extra
        self.gameBoard[x][y].color = color
        self.gameBoard[x][y]['image'] = self.images[imageKey]
        self.gameBoard[x][y].grid(row=x, column=y)

    # 检查指定位置是否为空（没有棋子）
    def isNoneStone(self, x, y):
        return self.gameBoard[x][y].color == Move.NONE

    # 设置游戏模式
    def toGameMode(self, mode):
        self.gameMode = mode

    def toGameState(self, state):
        self.gameState = state
        if state == GameState.Win:
            # 游戏结束时打印棋谱
            self.printMoveList(self)

    def printMoveList(self, color):
        moveListStr = ""
        for move in self.moveList:
            if move.color == Move.BLACK:
                color_str = "B"
            else:
                color_str = "W"
            # 将坐标转换为大写字母和数字的表示形式
            x1 = chr(move.x1 + ord('A'))
            y1 = str(move.y1 + 1)
            if move.x2 != -1 and move.y2 != -1:  # 如果有第二个坐标，表示是移动
                x2 = chr(move.x2 + ord('A'))
                y2 = str(move.y2 + 1)
                moveListStr += f"{color_str}({x1},{y1});{color_str}({x2},{y2}); "
            else:  # 否则，只打印一个坐标
                moveListStr += f"{color_str}({x1},{y1}); "
                # 终端输出棋谱坐标
                print(moveListStr)
        # 指定文件名和内容
        now = datetime.datetime.now()
        filename = "棋谱.txt"
        unicode_str=u"先手参赛队 后手参赛队 后手胜 先手胜"
        gb2312_bytes=unicode_str.encode('gb2312')

        # 使用'w'模式打开文件，'utf-8'指定编码格式
        with open(filename, 'w', encoding='GB2312') as file:
            file.write('{[C6][先手参赛队 B][后手参赛队 W][' + ('先手胜' if color == Move.BLACK else '后手胜') + ']' +
                       '[' + now.strftime('%Y.%m.%d %H:%M %S') + ' 淮北][2024 CCGC];')
            file.write(moveListStr)

        # 文件会在with语句结束时自动关闭

    def placeStone(self, color, x, y):
        self.placeColor(color, x, y, 't')  # 假设 't' 是用于标记特殊移动的参数
        if self.connectedBy(x, y):
            self.winner = color
            self.toGameState(GameState.Win)  # 使用正确的方法名
            if color == Move.BLACK:
                messagebox.showinfo("黑棋胜利", "黑棋 胜利!")
            else:
                messagebox.showinfo("白棋胜利", "白棋 胜利!")

    # 处理棋盘上的点击事件
    def onClickBoard(self, event):
        x = event.widget.x
        y = event.widget.y
        if not self.isNoneStone(x, y):
            return

            # 人机对战
        if self.gameMode == GameState.AI2Human:
            color = self.nextColor()
            if len(self.moveList) == 0 and self.gameState == GameState.WaitForHumanFirst:
                self.move = Move(color, x, y, x, y)
                self.addToMoveList(self.move)
                self.placeStone(self.move.color, x, y)
                self.toGameState(GameState.WaitForEngine)

            elif self.gameState == GameState.WaitForHumanFirst:
                self.move = Move(color, x, y)
                self.placeStone(self.move.color, x, y)
                if self.gameState == GameState.WaitForHumanFirst:
                    self.toGameState(GameState.WaitForHumanSecond)

            elif self.gameState == GameState.WaitForHumanSecond:
                self.move.x2 = x
                self.move.y2 = y
                self.placeStone(self.move.color, x, y)
                self.addToMoveList(self.move)
                if self.gameState == GameState.WaitForHumanSecond:
                    self.toGameState(GameState.WaitForEngine)

        return

# 主函数，启动GUI应用程序
def main():
    root = Tk()
    app = App(root)
    app.master.title('   ')
    app.mainloop()


if __name__ == '__main__':
    main()
