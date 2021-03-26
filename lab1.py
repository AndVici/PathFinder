"""
    author@ ij6984@rit.edu
    python lab1.py terrain.png mpp.txt [trail].txt [season] [dest].png
"""
from PIL import Image
import math
import re
from Point import Point
import sys
import pdb



SUMMER = {(248,148,18,255): 1, (255,192,0,255): 2.5, (255,255,255,255): 1.25, (2,208,60,255): 1.50, 
(2,136,40,255): 2.5, (5,73,24,255): "F", (0,0,255,255): "F", (71,51,3,255): 1, (0,0,0,255): 1.25, (205,0,101,255): "F"}

WINTER = {(248,148,18,255): 1, (255,192,0,255): 2.5, (255,255,255,255): 1.25, (2,208,60,255): 1.50, 
(2,136,40,255): 2.5, (5,73,24,255): "F", (0,0,255,255): "F", (71,51,3,255): 1, (0,0,0,255): 1.25, (205,0,101,255): "F",
(184,253,255,255): 2}

SPRING = {(248,148,18,255): 1, (255,192,0,255): 2.5, (255,255,255,255): 1.25, (2,208,60,255): 1.50, 
(2,136,40,255): 2.5, (5,73,24,255): "F", (0,0,255,255): "F", (71,51,3,255): 1, (0,0,0,255): 1.25, (205,0,101,255): "F"}

FALL = {(248,148,18,255): 1, (255,192,0,255): 2.5, (255,255,255,255): 1.25, (2,208,60,255): 1.50, 
(2,136,40,255): 2.5, (5,73,24,255): "F", (0,0,255,255): "F", (71,51,3,255): 1, (0,0,0,255): 1.75, (205,0,101,255): "F"}

season = SUMMER
lo = 10.29
la = 7.55

mapX = 395
mapY = 400

def neighbors(p,map):
    """returns list of adjacent pixels"""
    x = p.x
    y = p.y
    nb = []
    if x >0:
        nb.append(map[x-1][y])
        if y > 0:
            nb.append(map[x-1][y-1])
        if y < mapY-1:
            nb.append(map[x-1][y+1])
    if x < mapX-1:
        nb.append(map[x+1][y])
        if y > 0:
            nb.append(map[x+1][y-1])
        if y < mapY-1:
            nb.append(map[x+1][y+1])
    if y > 0:
        nb.append(map[x][y-1])
    if y < mapY-1:
        nb.append(map[x][y+1])
    return nb
    
def BFS(map, bank, seas):
    if len(bank) == 0:
        print("No water")
        return 0
    unseen = bank
    childQ=[]
    if seas == "winter":
        x = 7
    else:
        x = 15
    depth=0
    while(depth<x):
        if len(unseen)==0:
            if len(childQ)==0:
                return 0
            else:
                unseen = childQ
                childQ=[]
                depth+=1
        print(depth)
        current = unseen.pop(0)
        children=neighbors(map[current[0]][current[1]],map)
        ele = map[current[0]][current[1]].elev
        for child in children:
            if child not in unseen and child not in childQ:
                if seas == "winter":
                    if child.terrain == (0,0,255,255):
                        child.setTerrain((184,253,255,255))
                else:
                    if child.terrain!=(205,0,101,255) and ele - child.elev <= 1:
                        child.setTerrain((0,0,255,255))
                        
                childQ.append((child.x,child.y))
    

def distance(p1, p2):
    return math.sqrt(pow((p2.x-p1.x)*lo,2) + pow((p2.y-p1.y)*la,2))
        

def Tobler(e1, e2, d):
    if d == 0:
        return 0
    S = ((e2-e1)/d)

    i = -3.5 * abs(S+0.05)
    return 6*pow(math.e, i)
    
def cost(p1,p2,p3):
    if season[p2.terrain] == "F":
        return False
    d = distance(p1, p2)
    t = Tobler(p1.elev, p2.elev, d)
    if d==0 or t==0:
        gn = p1.gn
    else:
        gn = (d/(t*1000))+p1.gn            #g(n) *terrain[p2.terrain]
    hn = distance(p2, p3)/60000                            #h(n)
    return (gn, hn)

def insertP(p1,p2,p3,Q,flag):
    """insert for priority queue on f(n)"""
    if flag==True:
        tup = p3
    else:
        tup = cost(p1,p2,p3)
        if tup==False:
            return 0
    if p1!=p2:
        p2.setParent(p1)
    p2.setgn(tup[0])
    p2.sethn(tup[1])
    fn = tup[0]+tup[1]

    index = 0
    for p in Q:
        fi = p.gn+p.hn
        if fi < fn:
            index+=1
    Q.insert(index, p2)
    
def pathFinder(p, start):
    cost = 0
    length = 0
    path = [p]
    while(True):
        length+=distance(p.parent,p)
        path.insert(0,p.parent)
        cost+=p.parent.gn
        p=p.parent
        if(p==start):
            path.insert(0, length)
            break
    return path
        
    
def Astr(start, end, map):
    if(start == end):
        return start
    unseen = []
    c = cost(start, start, end)
    c = (start.gn, c[1])
    insertP(start, start, c, unseen,True)
    seen = []
    childQ = []
    count = 0
    while(True):
        count+=1
        if len(unseen)==0:
            if len(childQ) == 0:
                return ("No solution")
            unseen = childQ
            childQ = []
            
        current = unseen.pop(0)
        seen.append(current)
        if current == end:
            return pathFinder(current,start)
        children = neighbors(current, map)
        for child in children:
            if child not in seen and child not in unseen and child not in childQ:               #no f(n) 
                insertP(current,child,end,childQ,False)    
            elif child in unseen:
                c = cost(current,child,end)
                if c!= False and c[0]+c[1] < child.gn+child.hn:
                    unseen.remove(child)
                    insertP(current,child,c,childQ,True)

def main():

    map = []
    bank = []
    if sys.argv[4] == "summer":
        season = SUMMER
    elif sys.argv[4] == "winter":
        season = WINTER
    elif sys.argv[4] == "spring":
        season = SPRING
    else:
        season = FALL
    readfile = open(sys.argv[2])
    temp = readfile.readline().strip()
    ele = re.split('\s+',temp)
    
    with Image.open(sys.argv[1]) as im:
        mapX = im.size[0]
        mapY = min(im.size[1],len(ele))
        for i in range(mapX):
            map.append([])
            for j in range(mapY):
                map[i].append(Point(i,j,float(ele[j]),im.getpixel((i,j))))
                if im.getpixel((i,j))!=(0,0,255,255) and im.getpixel((i,j))!=(205,0,101,255):
                    if i<mapX-1 and im.getpixel((i+1,j))==(0,0,255,255):
                        bank.append((i,j))
                    elif j<mapY-1 and im.getpixel((i,j+1))==(0,0,255,255):
                        bank.append((i,j))
                elif im.getpixel((i,j))==(0,0,255,255):
                    if i<mapX-1 and im.getpixel((i+1,j))!=(0,0,255,255) and im.getpixel((i+1,j))!=(205,0,101,255):
                        bank.append((i+1,j))
                    elif j<mapY-1 and im.getpixel((i,j+1))!=(0,0,255,255) and im.getpixel((i,j+1))!=(205,0,101,255):
                        bank.append((i,j+1))
            t = readfile.readline().strip()
            ele = re.split('\s+',temp)
    readfile.close()
    if sys.argv[4]=="winter":
        BFS(map,bank,"winter")
    if sys.argv[4]=="spring":
        BFS(map,bank,"spring")
    
    gates = []
    with open(sys.argv[3]) as f:
        data = f.readlines()
        for line in data:
            line = line.strip('\n').split(' ')
            gates.append(map[int(line[0])][int(line[1])])
    p = []
    length = 0
    for i in range(1,len(gates)):
        p1 = gates[i-1]
        p2 = gates[i]
        tem = Astr(p1, p2, map)
        length+=tem.pop(0)
        for j in tem:
            p.append(j)
        
    print(length)
    for pnt in p:
        pnt.setTerrain((165,42,42,255))
    icy = Image.new("RGBA", (mapX,mapY))
    icyim = icy.load()
    for i in range(mapX):
        for j in range(mapY):
            icyim[i,j] = map[i][j].terrain
    icy = icy.save(sys.argv[5])
    
    
main()