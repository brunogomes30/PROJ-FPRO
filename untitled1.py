def check_collision(rect1, rect2):
    
    x1, x2, y1, y2 = rect1[0], rect1[0]+ rect1[2], rect1[1], rect1[1] + rect1[3]
    
    return (x1 < rect2[0] + rect2[2] and
   x2 > rect2[0] and
   y1 < rect2[1] + rect2[3] and
   y2 > rect2[1])
    print(rect1,"\n", rect2)
    print(not (x1 > rect2[0] + rect2[2] or x2 < rect2[0]) and (y1 > rect2[1] + rect2[3] or y2 < rect2[1]))
    #return not (x1 > rect2[0] + rect2[2] or x2 < rect2[0]) or (y1 > rect2[1] + rect2[3] or y2 < rect2[1])
        
    
    return not ((rect1[0] + rect1[2] < rect2[0] > rect1[0] or rect2[0] + rect2[2] < rect1[0]) and (rect1[1] + rect1[3] < rect2[1] > rect1[1] or rect2[1] + rect2[3] < rect1[1]))

collisions = set()

def divide_quad(rect):
    lst = []
    lst.append((rect[0],rect[1],rect[2]//2,rect[3]//2))
    lst.append((rect[0]+rect[2]//2,rect[1],rect[2]//2,rect[3]//2))
    lst.append((rect[0],rect[1]+rect[3]//2,rect[2]//2,rect[3]//2))
    lst.append((rect[0]+rect[2]//2,rect[1]+rect[3]//2,rect[2]//2,rect[3]//2))
    
    return tuple(lst)

def search_map(map, map_rectangle, search_rectangle):
    x, y, w, h = search_rectangle[0], search_rectangle[1], search_rectangle[2], search_rectangle[3]
    mx, my, mw, mh = map_rectangle[0], map_rectangle[1], map_rectangle[2], map_rectangle[3]
    halfx, halfy, halfmx, halfmy = x + w//2, y + h//2, mx + w//2, my + h//2
    global collisions
    
    #Try to insert into one quad
    divx1, divx2,divy1, divy2 = x//halfx, (x + w)//halfx, y//halfy, (y+h) // halfy
    if not(0<=divx1<=1 and 0<=divx2<=1 and 0<=divy1<=1 and 0<=divy2<=1):
        return collisions
    if  divx1 == divx2 and divy1 == divy2:
        #Can insert, then only searches in that quad
        collisions.union(search_map(map[divx1 + divy1*2], map_rectangle, search_rectangle))
        
    else:
        #Searchs in all quads
        rectangles = divide_quad(map_rectangle)
        for i, x in enumerate(map):
            if x == None:
                continue
            if type(x) == str:
                if x == 'C' and False:
                    print(x)
                    print(rectangles[i])
                    print("____")
                print(x)
                if check_collision(search_rectangle, rectangles[i]):
                    collisions.add(x)
                #print(collisions)
                
            elif type(x) == tuple:
                #print("BEFORE", collisions)
                collisions.union(search_map(map[i], rectangles[i], search_rectangle))
                #print("AFTER", collisions)
    #print("returning collisions...",collisions)
    return collisions

print(search_map(('A', (None, None, 'E', 'F'), ('D', None, None, 'B'), 'C'), (0, 0, 735, 959), (417, 697, 316, 238)))
input()