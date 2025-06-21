def fill_place():
    place = []
    c = 0
    for i in range(4):
        line = []
        for j in range(4):
            line.append(c)
            c += 1
        place.append(line)
    return place


class Place:
    
    def __init__(self):
        self.place: list[list[int]] = fill_place()
            
    def print_place(self):
        for i in range(4):
            line = ''
            for j in range(4):
                N = self.place[i][j]
                line += f'{N} ' if N>9 else f'{N}  '
            print(line)
            
            
if __name__ == '__main__':
    Place().print_place()