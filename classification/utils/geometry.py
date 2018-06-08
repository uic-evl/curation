from numpy import dot, sqrt


def union(a, b):
    """ Union of two rectangles (x, y, w, h) """
    x = min(a[0], b[0])
    y = min(a[1], b[1])
    w = max(a[0] + a[2], b[0] + b[2]) - x
    h = max(a[1] + a[3], b[1] + b[3]) - y
    return x, y, w, h


def intersection(a, b):
    """ Intersection of two rectangles (x, y, w, h) """
    x = max(a[0], b[0])
    y = max(a[1], b[1])
    w = min(a[0] + a[2], b[0] + b[2]) - x
    h = min(a[1] + a[3], b[1] + b[3]) - y
    if w < 0 or h < 0:
        return None
    return x, y, w, h


def contains(a, b):
    """ Find if a rectangle contains another rectangle """
    x, y, w, h = union(a, b)
    if (x == a[0] and y == a[1] and w == a[2] and h == a[3]) or (x == b[0] and y == b[1] and w == b[2] and h == b[3]):
        return True
    else:
        return False


# https://code.google.com/p/pythonxy/source/browse/src/python/OpenCV/DOC/samples/python2/squares.py?spec=svn.xy-27.cd6bf12fae7ae496d581794b32fd9ac75b4eb366&repo=xy-27&r=cd6bf12fae7ae496d581794b32fd9ac75b4eb366
def angle_cos(p0, p1, p2):
    d1, d2 = (p0 - p1).astype('float'), (p2 - p1).astype('float')
    return abs(dot(d1, d2) / sqrt(dot(d1, d1) * dot(d2, d2)))