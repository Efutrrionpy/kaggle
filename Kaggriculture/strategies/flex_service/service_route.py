from collections import deque
MOVES={'NORTH':(0,-1),'SOUTH':(0,1),'EAST':(1,0),'WEST':(-1,0)}
def route(tiles,start,end):
    start=tuple(start);end=tuple(end);queue=deque([(start,[])]);seen={start};n=len(tiles)
    while queue:
        pos,path=queue.popleft()
        if pos==end:return path
        for name,(dx,dy) in MOVES.items():
            q=(pos[0]+dx,pos[1]+dy)
            if q not in seen and 0<=q[0]<n and 0<=q[1]<n and tiles[q[1]][q[0]]!='LOCKED':
                seen.add(q);queue.append((q,path+[[name]]))
    return None
