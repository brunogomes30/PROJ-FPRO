def collide(a, b):
    return a.mask.overlap(b.mask, (int(b.origin[0] - a.origin[0]), int(b.origin[1] - a.origin[1])))