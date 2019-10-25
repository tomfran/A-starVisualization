from math import sqrt, pow
from heapq import *
from Point import Point
from queue import Queue
import os, time, random


ROWS            = 30
COLUMNS         = 30
START           = Point(0,0,0)
END             = Point(ROWS-1, COLUMNS -1, 0)
STARCOEFFICENT  = 1
ENDCOEFFICENT   = 5
WALL            = 3
PATH            = 4


def makeBoards(n,m):
    a = []
    a = [[0 for j in range(n)] for i in range(m)]

    # random initalization
    for k in range(int(ROWS*COLUMNS//2.5)):
        i = 0
        j = 0
        while(((START.x == i and START.y == j) or (END.x == i and END.y == j)) or a[i][j] == 3):
            i = random.randint(0,ROWS-1)
            j = random.randint(0, COLUMNS-1)
        a[i][j] = 3

    # file initalization
    # with open ("input.txt") as f:
    #     for r in f:
    #         a.append([int(i) for i in r.split()])

    b = [[False for j in range(n)] for i in range(m)]
    return a,b

def printBoard(mat):
    for r in mat:
        for e in r:
            print("%2d" % e, end = " ")
        print("")

def printVisit(visit, board, rewrite):
    print("\n\n\t", end = "")
    # black border
    for i in range(len(visit)+2):
        print("\033[40;30m  \033[0m", end = "")
    print("\n\t", end = "")

    for i in range(len(visit)):
        print("\033[40;30m  \033[0m", end = "")
        for j in range(len(visit[0])):
            # if start print green
            if START.x == i and START.y == j:
                print("\033[42;30mS \033[0m", end = "")
            # if END print green
            elif END.x == i and END.y == j:
                print("\033[42;30mE \033[0m", end = "")
            # print wall
            elif board[i][j] == WALL:
                print("\033[40;30m  \033[0m", end = "")
            # print the shortest path in visit
            elif board[i][j] == PATH:
                print("\033[46;30m  \033[0m", end = "")
            # if visited print red
            elif visit[i][j]:
                print("\033[41;30m  \033[0m", end = "")
            # else print white
            else:
                print("\033[47;30m  \033[0m", end = "")

        # black border
        print("\033[40;30m  \033[0m\n\t", end = "")

    # black border
    for i in range(len(visit)+2):
        print("\033[40;30m  \033[0m", end = "")
    print("\n\n")
    # go back to the top of the matrix, to make the animation
    if(rewrite):
        print("\033[s\033[37A")

# Compute cost of cell, used to set visit priority
def computeCost(point, start, end):
    return sqrt((point.x-start.x)**2 + (point.y-start.y)**2)*STARCOEFFICENT + sqrt((point.x-end.x)**2 + (point.y-end.y)**2)*ENDCOEFFICENT

def visit(p, b):
    b[p.x][p.y] = True

def setPath(l, b):
    b[l[0]][l[1]] = PATH

def visited(p, b):
    return b[p.x][p.y]

def valid(i, j, board):
    return (i >= 0 and i < ROWS and j >= 0 and j < COLUMNS) and (board[i][j] != WALL)

def neighbours(p, board):
    ret = []
    for i in (p.y-1, p.y, p.y+1):
        for j in (p.x-1, p.x, p.x+1):
            if valid(j,i, board):
                r = Point(j,i,0)
                r.c = computeCost(r,START,END)
                ret.append(r)
    return ret

def highligthPath(board, visitBoard):
    # parent dict
    parent = dict()

    parent[START.convert()] = (0,0)
    currentVisitBoard = [[False for j in range(ROWS)] for i in range(COLUMNS)]

    q = Queue()
    q.put(START)
    finished = False
    while q and not finished:
        p = q.get()
        # visit only visited cells by A* algoritmh
        if(visited(p, visitBoard) and not visited(p,currentVisitBoard)):
            visit(p,currentVisitBoard)
            if(p == END):
                finished = True
            else:
                for n in neighbours(p, board):
                    if(visited(n, visitBoard) and not visited(n,currentVisitBoard)):

                        parent[n.convert()] = p.convert()
                        q.put(n)


    current = END.convert()
    while(current != START.convert()):
        setPath(current,board)
        current = parent[current]

# Run Astar algorithm, from start to end
def Astar():
    board, visitBoard = makeBoards(ROWS, COLUMNS);
    pq = [START]
    heapify(pq)
    endFound = False

    while pq and not endFound:
        p = heappop(pq)
        if(not visited(p, visitBoard)):
            if(p == END):
                visit(p, visitBoard)
                highligthPath(board, visitBoard);
                endFound = True
                printVisit(visitBoard, board, False)
            else:
                visit(p, visitBoard)
                printVisit(visitBoard, board, True)
                time.sleep(0.01)
                for n in neighbours(p, board):
                    if(not visited(n, visitBoard)):
                        heappush(pq, n)
    if not endFound:
        print("END NOT FOUND")

def main():
    print("\nA* Visualization")
    # Astar(board, start, end);
    Astar()
    # r = tk.Tk()
    # r.title('A* Visualization')
    # button = tk.Button(r, text='START', width=25, command=r.destroy)
    # button.pack()
    # r.mainloop()


if __name__ == '__main__':
    main()
