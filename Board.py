from PointGrid import PointGrid
from queue import PriorityQueue
import numpy as np
import stddraw
from point2DMatrix import point2DMatrix
import color

class Board(PointGrid):
    def __init__(self,m,n,sqtiles=[],moves=0):
        PointGrid.__init__(self,m,n)
        # A_np是一个n*n，从上到下，从左到右的数组形式
        self.A_np = []
        self.m=m
        self.n=n
        # 移动次数
        self.moves=moves

        #处理输入的数组，使其变成从下到上，从左到右的形式
        if sqtiles!=[]:
            self.sqtiles=sqtiles
            self.arr=np.array(sqtiles).reshape(self.m,self.n)
            self.arr=np.flip(self.arr,0).reshape(1, self.n * self.n)
            temp=list(self.arr[0])
            keys = list(range(0, m * n, 1))
            dicts = dict(zip(keys, temp))
            self.set_attrs(dicts)


#重构函数
    def set_attrs(self, dict):
        self._A = dict
        for value in dict.values():
            self.A_np.append(value)
        self.A_np = np.array(self.A_np).reshape(self.m, self.n)
        self.A_np = np.flip(self.A_np, 0)

    def _get_keybyvalue(self,value):
        for key in self._A.keys():
            if self._A[key]==value:
                return key

    def tileAt(self,r,c):
        key = r * self.n + c
        return self._A[key]

    def size(self):
        return len(self.sqtiles)

    def Hamming(self):
        hamming = 0
        attrs=self.A_np[:].reshape(1, self.n * self.n)[0]
        for i in range(len(attrs)):
            if attrs[i] != i + 1 and attrs[i] != 0:
                hamming += 1
        return hamming

    def Manhattan(self):
        manhattan=0

        for i in range(self.m):
            for j in range(self.n):
                if i!=self.m-1 or j != self.n-1:
                    target = i * self.n + j+1
                    point=np.where(self.A_np ==target)
                    manhattan=manhattan+abs(i-point[0][0])+abs(j-point[1][0])
        return manhattan

    def isGoal(self):
        if self.Hamming()==0:
            return True
        return False

    def __eq__(self, other):
        if (self.A_np==other.A_np).all():
            return True
        return False
    #重构哈希，为之后通过根节点寻找父节点做准备
    def __hash__(self):
        return hash(id(self))

    #board的邻居，若不存在则输出-1
    def neighbors(self):
        neighbors=[]
        for key, value in self.get_attrs().items():
            if value==0:
                ix=key
        # print(self.A_np)
        left, right, up, down=self.neighors_keys(ix)
        temp=[self.get_attrs().copy() for _ in range(4)]

        #若邻居存在，则构建新的邻居board并存入neighbors列表
        if left!=-1:
            temp[0][ix],temp[0][left]=temp[0][left],temp[0][ix]
            board=Board(self.m,self.n)
            board.set_attrs(temp[0])
            neighbors.append(board)

        if right!=-1:
            temp[1][ix], temp[1][right] = temp[1][right], temp[1][ix]
            board = Board(self.m, self.n)
            board.set_attrs(temp[1])
            neighbors.append(board)

        if up != -1:
            temp[2][ix], temp[2][up] = temp[2][up], temp[2][ix]
            board = Board(self.m, self.n)
            board.set_attrs(temp[2])
            neighbors.append(board)

        if down != -1:
            temp[3][ix], temp[3][down] = temp[3][down], temp[3][ix]
            board = Board(self.m, self.n)
            board.set_attrs(temp[3])
            neighbors.append(board)
        return neighbors

    def __lt__(self, other):
        return self.Manhattan()+self.moves<other.Manhattan()+other.moves

    #计算逆序对
    def Inversions(self):
        inversions=0
        arr=self.sqtiles[:]
        arr.remove(0)
        for i in range(len(arr)-1):
            for j in range(i+1,len(arr)):
                if arr[j]<arr[i]:
                    inversions+=1
        return inversions
    #通过逆序对判断是否可解
    def isSolvable(self):
        if self.n%2==1 and self.Inversions()%2==0:
            return True
        if self.n%2==0:
            point = np.where(self.A_np == 0)
            blank_row=point[0][0]
            if blank_row+self.Inversions()%2==1:
                return True
        return False

#下面开始解决问题
class solution:
    def __init__(self,arr,m,n):
        #已访问的节点
        self.visited=[]
        #key是孩子，value是父亲
        self.kidTree={}
        self.m=m
        self.n=n
        self.b = Board(m, n, arr)
        self.pq = PriorityQueue()
        self.pq.put(self.b)
        # 根节点的父节点是自己
        self.kidTree[self.b]=self.b
        stddraw.setCanvasSize(600, 600)
        stddraw.setXscale(-100, 100)
        stddraw.setYscale(-100, 100)

    #找出最短路径后进行回溯，通过子节点找到父节点，直到找到根节点为止
    def goBack(self,board):
        path=[]
        path.append(board)
        while self.kidTree[board]!=board:
            path.append(self.kidTree[board])
            board=self.kidTree[board]
        return path
    #绘画函数
    def draw(self, path):
        for t in reversed(path):
            pm = point2DMatrix(0, 0, 200, 200, self.m, self.n)
            arr = []
            for value in t.get_attrs().values():
                arr.append(value)
            pm.set_values(np.array(arr).reshape(self.m, self.n))
            stddraw.clear()
            for i in range(self.m):
                for j in range(self.n):
                    stddraw.setPenColor(color.BLACK)
                    stddraw.setFontSize(50)
                    pos = pm.pos(i, j)
                    t = pm.get_value(i, j)
                    if (t != 0):
                        stddraw.text(pos[0], pos[1], str(int(t)))
            # TODO 通过调整show中的数字可以改变图像中的移动速度
            stddraw.show(300)
    #运行函数
    def run(self):
        #从优先队列中取出一个board
        board=self.pq.get()
        # 在已访问列表中添加属性
        # self.visited.append(board.get_attrs())
        #如果不可解则打印无解
        if board.isSolvable()==False:
            return print("无解")
        #如可解，则在解出前一直进行循环
        while board.isGoal()==False:
            # 找出取出的board的邻居
            neighbors=board.neighbors()
            #对每一个另据，如果未被访问，则进入优先队列，并且在kidTree列表中记录它的父节点
            for n in neighbors:
                if  n not in self.kidTree:
                    n.moves=n.moves+1
                    self.pq.put(n)
                    self.kidTree[n]=board
                    # print(self.kidTree)
            #取出优先队列中优先值最小的
            board=self.pq.get()
            # self.visited.append(board.get_attrs())
        #最后得出的board是目标board，通过回溯找到它移动的正确路径
        path=self.goBack(board)
        self.draw(path)
        print("恭喜通过")
        stddraw.show()
# 1 4 7
# 2 5 8
# 3 6 0
if __name__ == '__main__':
    arr=[0,1,3,4,2,5,7,8,9,6,12,10,11,15,13,14]
    # arr=[1,7,6,2,4,5,0,8,3]
    s=solution(arr, 4, 4)
    s.run()
    # arr=[8,1,3,4,0,2,7,6,5]
    # arr=[1,2,3,4,5,6,0,8,9,10,7,11,13,14,15,12]
    # b=Board(3,3,arr)

#[1,2,3,4,5,6,0,8,7]
    # print(b.Hamming())
    # b.Manhattan()
    # b.isGoal()
    # print(b.Manhattan())
    # print(b.Hamming())
    # print(b.neighbors())
    # print(b.isSolvable())
    #
    # print(b.Inversions())
    #
    # print(b.tileAt(0,0))
    # print(b.neighbors())
