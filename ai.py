import math
import heapq

import util

def manhattan(p1,p2):
    x1, y1 = p1
    x2, y2 = p2
    return math.fabs(x1-x2) + math.fabs(y1-y2)

class Point:
    def __init__(self, parent, x, y, f, g, dir):
        self.parent = parent
        self.p = x,y
        self.f = f
        self.s = f + g
        self.dir = dir

    def __lt__(self, other):
        return self.s < other.s

    def __repr__(self):
        return "{0}: {1}".format(str(self.p), self.s)

def astar(start, end, is_passable):
    def unwind(p):
        if p.p == start:
            return []
        else:
            return unwind(p.parent) + [(p.dir, p.p)]

    fringe = [Point(None, start[0], start[1], 0, manhattan(start, end), None)]
    visited = {start: True}
    while fringe:
        #print("fringe = {0}".format(fringe))
        next = heapq.heappop(fringe)
        visited[next.p] = True
        if next.p == end:
            return unwind(next)
        for (d, (x, y)) in [('North', (-1,0)),
                            ('South', (1,0)),
                            ('West', (0, -1)),
                            ('East', (0, 1))]:
            currp = next.p[0] + x, next.p[1] + y
            if currp == end:
                return unwind(next) + [(d, (next.p[0] + x, next.p[1] + y))]
            if currp not in visited and currp not in fringe and is_passable(currp):
                heapq.heappush(fringe, Point(next, currp[0], currp[1], next.f + 1, manhattan(currp, end), d))
    return [] # no path found
