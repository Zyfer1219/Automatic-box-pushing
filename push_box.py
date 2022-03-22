from PointGrid2D import PointGrid2D
import stddraw
import color
import numpy as np
from queue import PriorityQueue
from Element import Element
class Game:
    def __init__(self,n=15):
        # 设置stdDraw窗口尺寸
        stddraw.setCanvasSize(600, 600)
        # 设置stdDraw的坐标范围
        stddraw.setXscale(0, 10)
        stddraw.setYscale(0, 10)

        self.n=n

        self.me=(3,1)
        self.box=(1,2)
        self.des=(self.n-1,self.n-1)
        self.kidTree = {}
        self.path_me={}

        self.pg=PointGrid2D(5,5,10,10,n,n)
        #2是人，3是box,4是目的地

        self.draw_grid()
        self.draw_other()

    def draw_grid(self):
        for i in range(self.n):
            for j in range(self.n):
                point=self.pg.pos(i,j)
                value=self.pg.get_attr(i,j)
                if value==1:
                    stddraw.setPenColor(color.LIGHT_GRAY)
                    stddraw.filledSquare(point[0],point[1],self.pg.dx() / 2 - 0.01)
                else:
                    stddraw.setPenColor(color.BLACK)
                    stddraw.filledSquare(point[0], point[1], self.pg.dx() / 2 - 0.01)

    def draw_other(self):
        stddraw.setPenColor(color.RED)
        pos=self.pg.pos(self.me[0],self.me[1])
        stddraw.filledCircle(pos[0],pos[1],self.pg.dx()/2-0.2)

        pos=self.pg.pos(self.box[0],self.box[1])
        stddraw.filledSquare(pos[0],pos[1],self.pg.dx()/2-0.2)

        pos=self.pg.pos(self.des[0],self.des[1])
        stddraw.filledRectangle(pos[0],pos[1],self.pg.dx(),self.pg.dx()/2)

        stddraw.setFontSize(20)
        stddraw.text(2,9.5,"w:up s:down a:left d:right")
        stddraw.text(2, 9, "S:save map L:load map A:auto")
    def isvisited(self,r,c):
        if r>=0 and r< self.n and c>=0 and c<self.n and self.pg.get_attr(r,c)==1:
            return True
        return False

    def move(self,op):
        if op == 'w' and self.isvisited(self.me[0] + 1, self.me[1]):
            if self.box == (self.me[0] + 1, self.me[1]):
                if self.isvisited(self.box[0] + 1, self.box[1]):
                    self.box = (self.box[0] + 1, self.box[1])
                    self.me = (self.me[0] + 1, self.me[1])
            else:
                self.me = (self.me[0] + 1, self.me[1])

        elif op == 's' and self.isvisited(self.me[0] - 1, self.me[1]):
            if self.box == (self.me[0] - 1, self.me[1]):
                if self.isvisited(self.box[0] - 1, self.box[1]):
                    self.box = (self.box[0] - 1, self.box[1])
                    self.me = (self.me[0] - 1, self.me[1])
            else:
                self.me = (self.me[0] - 1, self.me[1])

        elif op == 'd' and self.isvisited(self.me[0], self.me[1] + 1):
            if self.box == (self.me[0], self.me[1] + 1):
                if self.isvisited(self.box[0], self.box[1] + 1):
                    self.box = (self.box[0], self.box[1] + 1)
                    self.me = (self.me[0], self.me[1] + 1)
            else:
                self.me = (self.me[0], self.me[1] + 1)

        elif op == 'a' and self.isvisited(self.me[0], self.me[1] - 1):
            if self.box == (self.me[0], self.me[1] - 1):
                if self.isvisited(self.box[0], self.box[1] - 1):
                    self.box = (self.box[0], self.box[1] - 1)
                    self.me = (self.me[0], self.me[1] - 1)
            else:
                self.me = (self.me[0], self.me[1] - 1)
        self.draw_grid()
        self.draw_other()

    def save_map(self):
        file = open('homework_11.txt', 'w+')
        for i in reversed(range(self.n)):
            for j in range(self.n):
                value = self.pg.get_attr(i, j)
                file.write(str(value) + ' ')
            file.write('\n')
        file.close()

    def load_map(self):
        file = open('homework_11.txt', 'r')
        arr = []
        for line in file:
            line = list(map(float, line.split()))
            self.n = len(line)
            arr.append(line)

        self.pg = PointGrid2D(5, 5, 10, 10, self.n, self.n)
        arr = np.array(arr)
        arr =list(np.flip(arr, 0).reshape(1,self.n*self.n)[0])
        keys = list(range(0, self.n*self.n, 1))
        dicts = dict(zip(keys, arr))
        self.pg.set_attrs(dicts)

        self.draw_grid()
        self.draw_other()

    def click_grid(self,x,y):
        x_ = int(x // self.pg.dx())
        y_ = int(y // self.pg.dy())

        if self.pg.get_attr(y_,x_)==1:
            stddraw.setPenColor(color.BLACK)
            self.pg.set_attr(y_, x_, 0)
            pos = self.pg.pos(y_, x_)
            stddraw.filledSquare(pos[0], pos[1], self.pg.dx() / 2 - 0.01)
        else:
            stddraw.setPenColor(color.LIGHT_GRAY)
            self.pg.set_attr(y_, x_, 1)
            pos = self.pg.pos(y_, x_)
            stddraw.filledSquare(pos[0], pos[1], self.pg.dx() / 2 - 0.01)
        stddraw.show(20)

    def auto_me(self,me,box,op):
        kidTree={}
        visited = set()
        pq = PriorityQueue()
        if op=='left':
            des=(box[0],box[1]+1)
        elif op=='right':
            des = (box[0], box[1] - 1)
        elif op=='up':
            des = (box[0]-1, box[1])
        else:
            des = (box[0] + 1, box[1])

        me = Element(me[0], me[1], des)
        kidTree[me] = me
        visited.add((me.r, me.c))

        while me.r != des[0] or me.c != des[1]:
            neighbors = me.neighbors()
            left, right, up, down = neighbors

            if (right.r, right.c) not in visited and self.isvisited(right.r, right.c) and (right.r, right.c)!=box:
                right.move = right.move + 1
                pq.put(right)
                kidTree[right] = me
                visited.add((right.r, right.c))

            if (up.r, up.c) not in visited and self.isvisited(up.r, up.c) and (up.r, up.c)!=box:
                up.move = up.move + 1
                pq.put(up)
                kidTree[up] = me
                visited.add((up.r, up.c))

            if (down.r, down.c) not in visited and self.isvisited(down.r, down.c) and (down.r, down.c)!=box:
                down.move = down.move + 1
                pq.put(down)
                kidTree[down] = me
                visited.add((down.r, down.c))
            if (left.r, left.c) not in visited and self.isvisited(left.r, left.c) and (left.r, left.c)!=box:
                left.move = left.move + 1
                pq.put(left)
                kidTree[left] = me
                visited.add((left.r, left.c))
            me = pq.get()
            if pq.qsize()==0:
                return False

        path = self.goBack(me,kidTree)
        path.insert(0,Element(box[0],box[1],box))
        return path

    def auto(self):
        self.visited = set()
        self.pq = PriorityQueue()
        box = Element(self.box[0], self.box[1], self.des)
        self.kidTree[box] = box
        self.visited.add((box.r, box.c))

        while box.r != self.des[0] or box.c != self.des[1]:
            neighbors = box.neighbors()
            left, right, up, down = neighbors

            if (right.r, right.c,self.me) not in self.visited and self.isvisited(right.r, right.c) and self.isvisited(right.r,right.c - 2):
                res=self.auto_me(self.me,(box.r,box.c),'right')
                if res!=False:
                    self.path_me[right] = res
                    right.move = right.move + 1
                    self.pq.put(right)
                    self.kidTree[right] = box
                    self.visited.add((right.r, right.c,self.me))

            if (up.r, up.c,self.me) not in self.visited and self.isvisited(up.r, up.c) and self.isvisited(up.r - 2, up.c):
                res=self.auto_me(self.me,(box.r,box.c),'up')
                if res!=False:
                    self.path_me[up] = res
                    up.move = up.move + 1
                    self.pq.put(up)
                    self.kidTree[up] = box
                    self.visited.add((up.r, up.c,self.me))

            if (left.r, left.c,self.me) not in self.visited and self.isvisited(left.r, left.c) and self.isvisited(left.r, left.c + 2):
                res=self.auto_me(self.me,(box.r,box.c),'left')
                if res!=False:
                    self.path_me[left]=res
                    left.move = left.move + 1
                    self.pq.put(left)
                    self.kidTree[left] = box
                    self.visited.add((left.r, left.c,self.me))

            if (down.r, down.c,self.me) not in self.visited and self.isvisited(down.r, down.c) and self.isvisited(down.r + 2,down.c):
                res=self.auto_me(self.me,(box.r,box.c),'down')
                if res!=False:
                    self.path_me[down] = res
                    down.move = down.move + 1
                    self.pq.put(down)
                    self.kidTree[down] = box
                    self.visited.add((down.r, down.c,self.me))
            if self.pq.qsize() == 0:
                print("无解")
                return False
            box = self.pq.get()
            # print(self.path_me[box])
            self.me=(self.path_me[box][0].r,self.path_me[box][0].c)

        path = self.goBack(box,self.kidTree)
        self.draw(path)

    def draw(self, path):

        path.pop()

        for t in reversed(path):
            path_me=self.path_me[t]
            for p in reversed(path_me):
                self.me=(p.r, p.c)
                if self.me!=self.box:
                    self.draw_grid()
                    self.draw_other()
                    stddraw.show(100)
            self.me=self.box
            self.box = (t.r, t.c)
            self.draw_grid()
            self.draw_other()
            stddraw.show(100)
        print("通关成功")

    def goBack(self, box,kidTree):
        path = []
        path.append(box)
        while kidTree[box] != box:
            path.append(kidTree[box])
            box = kidTree[box]
        return path

    def run(self):

        while True:
            if stddraw.hasNextKeyTyped():
                temp = stddraw.nextKeyTyped()
                if temp=='a' or temp=='d' or temp=='w' or temp=='s':
                    self.move(temp)
                    if self.box==self.des:
                        print("恭喜通关")

                elif temp=='S':
                    self.save_map()
                elif temp=='L':
                    self.load_map()
                elif temp=='A':
                    self.auto()
            if stddraw.mousePressed():
                x = stddraw.mouseX()
                y = stddraw.mouseY()
                self.click_grid(x,y)

            stddraw.show(20)

if __name__ == '__main__':

    print("请输入迷宫的长度")
    n=eval(input())
    g=Game(n)
    g.run()
