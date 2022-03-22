import numpy as np
import stddraw
from Board import Board
import stdrandom
import color
import matplotlib.pyplot as plt
import math
from point2DMatrix import point2DMatrix
from queue import PriorityQueue

class Element:
    def __init__(self,r,c,des):
        self.r=r
        self.c=c
        self.des=des
        self.move=0

    def Manhattan(self):
        manhattan=abs(self.des[0]-self.r)+abs(self.des[1]-self.c)
        return manhattan

    def __eq__(self, other):
        if self.r==other.r and self.c==other.c:
            return True
        return False

    def __lt__(self, other):
        return self.Manhattan() +self.move < other.Manhattan()+other.move

    # board的邻居，若不存在则输出-1
    def neighbors(self):
        neighbors = []

        # 若邻居存在，则构建新的邻居board并存入neighbors列表

        element = Element(self.r, self.c - 1, self.des)
        element.move=self.move
        neighbors.append(element)


        element = Element(self.r, self.c + 1, self.des)
        element.move = self.move
        neighbors.append(element)


        element = Element(self.r + 1, self.c, self.des)
        element.move = self.move
        neighbors.append(element)


        element = Element(self.r - 1, self.c, self.des)
        element.move = self.move
        neighbors.append(element)

        return neighbors
    #重构哈希，为之后通过根节点寻找父节点做准备
    def __hash__(self):
        return hash(id(self))

# class Box(Box):
#     def Manhattan(self):
#         manhattan=abs(self.des[0]-self.r)+abs(self.des[1]-self.c)
#         return manhattan