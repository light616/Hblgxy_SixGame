# 淮北理工学院----重生之我在淮理下棋
# 作者：杜良轩、夏炎 
# 程序主要由Hblgxy.py文件构成，于2024_11_16号晚上18:30分完成
# 声明
Copyright (c) 2014, Liang Li <ll@lianglee.org; liliang010@gmail.com>.
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * Neither the name of the copyright holders nor the
      names of its contributors may be used to endorse or promote products
      derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


# Hblgxy.py
主要由Move类、App类、GaemState类、GameEngine类组成

## Move类
Move 类用于表示棋盘上的移动。这个类包含了多个方法，用于初始化移动、转换为字符串、从命令行字符串创建移动对象、转换为命令行字符串等。以下是对类中各个方法的简要说明：
1. __init__：构造函数，初始化 Move 对象。它设置移动的初始状态，包括颜色和坐标。
2. __str__：特殊方法，返回移动的字符串表示，便于打印和调试。
3. fromCmd：类方法，从命令行字符串创建移动对象。它解析字符串，提取坐标信息，并创建一个新的 Move 对象。
4. toCmd：将移动对象转换为命令行字符串，用于发送给游戏引擎。
5. toPlaceCmd：将移动对象转换为放置命令行字符串，用于在游戏引擎中放置棋子。
6. cmd：获取移动的命令行表示，不包括 'move ' 前缀。
7. invalidate：使移动对象无效，重置所有属性。
8. isValidated：验证移动是否有效，检查颜色和位置是否在有效范围内。
9. isValidPosition：静态方法，验证给定的位置是否在棋盘内。

## App类
App 类它继承自 Frame 类，用于创建一个图形用户界面（GUI）应用程序。这个类用于管理一个棋盘游戏的状态和行为，包括初始化游戏资源、创建棋盘、处理游戏逻辑等。以下是对类中各个方法的简要说明：
1. __init__：构造函数，初始化 App 对象。它设置游戏模式和状态，初始化游戏资源，创建棋盘，并初始化棋盘。
2. initResource：初始化游戏资源，如加载图像资源和设置布局权重。
3. createBoard：创建棋盘单元格，并将它们放置在 Canvas 上。
4. backMove：悔棋方法，允许玩家撤销上一步操作。
5. initBoard：初始化棋盘，清除所有棋子。
6. unplaceColor：移除指定位置的棋子颜色。
7. connectedByDirection：检查指定方向上是否有连续的棋子。
8. connectedBy：检查是否有连续的棋子。
9. isWin：检查是否有玩家赢得了游戏。
10. nextColor：获取下一个玩家的颜色。
11. waitForMove：等待引擎或玩家的下一步移动。
12. searching：搜索方法，用于AI思考和决策。
13. otherColor：获取相反颜色的玩家。
14. newGame：开始新游戏，重置游戏状态。
15. addToMoveList：将移动添加到移动列表中。
16. unmakeTopMove：撤销移动列表中的最后一步。
17. makeMove：在棋盘上执行移动。
18. placeStone：在棋盘上放置棋子。
19. placeColor：在棋盘上放置棋子颜色。
20. isNoneStone：检查指定位置是否为空。
21. toGameMode：设置游戏模式。
22. toGameState：设置游戏状态。
23. printMoveList：打印棋谱列表到文件。
24. onClickBoard：处理棋盘上的点击事件

## GaemState类
用于表示游戏的不同状态。这个类使用了类变量来定义各种状态，这些状态通常用于游戏逻辑中判断当前游戏处于哪个阶段。以下是每个状态的含义：
1. Exit = -1：表示游戏退出状态。
2. Idle = 0：表示游戏处于空闲状态，没有进行任何操作。
3. AI2Human = 2：表示游戏处于人工智能对人类玩家的状态，可能是AI已经下过棋，现在轮到人类玩家。
4. WaitForEngine = 1：表示游戏正在等待引擎（可能是AI）的响应或动作。
5. WaitForHumanFirst = 2：表示游戏正在等待人类玩家的第一次操作。
6. WaitForHumanSecond = 3：表示游戏正在等待人类玩家的第二次操作，这可能是在某种特定的游戏规则下，人类玩家需要进行两次操作。
4. Win = 4：表示游戏胜利状态，可能是AI或人类玩家赢得了游戏。

## GameEngine类
GameEngine类用于处理与游戏引擎的交互。这个类包含了多个方法，用于初始化引擎、发送命令、等待消息等。以下是对类中各个方法的简要说明：
1. __init__：构造函数，初始化 GameEngine 对象。它设置默认的引擎文件名，初始化进程对象 proc，创建一个 Move 对象用于存储移动信息，设置颜色为 NONE，并设置引擎名称为 'Unknown'。
2. getEngine：类方法，返回默认的引擎文件名。
3. init：初始化游戏引擎。如果提供了 fileName，则使用提供的文件名；否则，使用默认文件名。根据操作系统类型，使用不同的方式启动进程。然后，发送 'name' 命令以获取引擎名称，并根据返回的消息设置引擎名称。如果提供了 depth 或 vcf 参数，还会发送相应的命令来设置引擎的搜索深度或是否使用 VCF（胜利条件评估）。
4. setName：设置引擎名称，并根据名称的长度进行截断或处理，以便于显示。
5. release：释放进程资源。如果进程正在运行，将其终止，并等待进程结束。然后，将 proc 设置为 None 并使 move 对象失效。
6. next：发送 'new' 命令以开始新游戏，然后发送移动列表中的所有移动命令，最后发送 'next' 命令以继续游戏。
7. sendCmd：向进程发送命令。如果进程存在，将命令写入进程的标准输入流。如果命令末尾没有换行符，则添加一个。
8. waitForNextMsg：等待并获取进程的下一个消息。如果进程存在，从进程的标准输出流中读取一行文本。

## 算法说明

1. Tkinter库
    在游戏界面的设计上，我们使用了Tkinter库，构建一了个简洁且直观的棋盘界面，让玩家和对手可以获得更好的体验，另外，由于Tkinter 采用事件驱动编程模型，所以我们使用事件驱动的方法处理用户输入，提高了界面的响应性。同时在定义了onClickBoard方法处理用户的棋盘点击事件，将点击转换为棋盘上的移动，并更新游戏状态，使得用户可以更加清晰的看清棋盘上的局势。
2. DFS算法
    我们使用了深度优先算法(Depth First Search即DFS)，DFS算法一种用于遍历或搜索树或图的算法。沿着树的深度遍历树的节点，尽可能深的搜索树的分支。当节点v的所在边都己被探寻过或者在搜寻时结点不满足条件，搜索将回溯到发现节点v的那条边的起始节点。整个进程反复进行直到所有节点都被访问为止。属于盲目搜索,最糟糕的情况算法时间复杂度为O(!n)。
    基本思想如下：
    1.	选择起始点：选择图中的一个点作为起始点。
    2.	访问节点：标记起始节点为已访问，并将该节点加入递归或栈中。
    3.	探索邻接节点：从该点周围取出一个点，检查它的所有未访问的邻接节点。
    4.	递归或迭代：对每个未访问的邻接节点，将其标记为已访问，然后将其推入递归或栈中。
    5.	回溯：当当前节点的所有邻接节点都被访问后，递归中回溯/从栈中弹出该节点，继续搜索上一个点的其他分支。
    6.	结束条件：当栈为空或找到目标节点时，搜索结束。
3. 快速排序
    通过一趟排序算法把所需要排序的序列的元素分割成两大块，其中，一部分的元素都要小于或等于另外一部分的序列元素，然后仍根据该种方法对划分后的这两块序列的元素分别再次实行快速排序算法，排序实现的整个过程可以是递归的来进行调用，最终能够实现将所需排序的无序序列元素变为一个有序的序列。快速排序有三种划分数组的方法，挖洞法、双指针法、经典霍尔法。我们在程序中实现了一个基于评分的排序算法，用于对生成的棋步进行排序，以便优先搜索评分较高的棋步。
4. 动态规划
    动态规划（Dynamic Programming,DP）算法通常用于求解某种具有最优性质的问题。在这类问题中，可能会有许多可行解，每一个解都对应一个值，我们希望找到具有最优值的解。
    动态规划算法与分治法类似，其基本思想也是将待求解的问题分解成若干个子问题，先求解子问题，然后从这些子问题的解中 得到原有问题的解。与分治法不同的是，动态规划经分解后得到的子问题往往不是相互独立的。我们通过动态规划的方法生成所有可能的棋步，并为每一步棋计算一个评分，用于后续的搜索和评估。
5. VCS算法
    VCF为五子棋引入的英文名称，对于黑方即利用连续不断地活三，直至最终通过四三取得胜利。对于白方最后还可通过双三、双四、长连或逼迫黑方禁手而取胜。也就是，利用连续不断地利用活三、冲四、做VCF三种攻击手段，最终获胜的战术技巧。VCT中的Three并不仅仅指活三，而是指与活三相同先手等级的攻击方法（包括活三、做VCF）。我们基于VCF算法进行了修改，加强了活四的权重，通过递归搜索VCF机会或防御VCF威胁增强了VCS算法强度。        

