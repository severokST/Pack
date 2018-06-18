import random
import numpy
from pyglet import image, sprite


images = [image.load('./images/circle.png')]
time_scale = 1


class Basic:
    def __init__(self,position, target, team, batch_set, order_group):
        self.position = position
        self.team = team
        self.speed = 1
        self.range = 5
        self.target_position = self.position
        self.target_grid = target
        self.sprite = sprite.Sprite(images[0], batch=batch_set, group=order_group, x=position[0], y=position[1])

    def move(self):
        if self.position[0] != self.target_position[0] and self.position[1] != self.target_position[1] :
            direction = random.randint(0,1)
        else:
            if self.position[0] != self.target_position[0]: direction = 0
            else: direction = 1
        if self.position[direction] > self.target_position[direction]:
            self.position[direction] -= self.speed/time_scale
        else:
            self.position[direction] += self.speed / time_scale

        self.sprite.position = self.position

    def decision(self, grid, interrupt):
        # current_target_pos = self.target_grid.copy()
        if self.position == self.target_position or interrupt == 1:
            decision = []
            decision_weight = []
            total_weight = 0
            for x in range (self.target_grid[0] + self.range * -1, self.target_grid[0] + self.range):
                if x < 0 or x >= grid['resolution'][0]:
                    print('Hit x bound')
                    continue
                for y in range (self.target_grid[1] + self.range * -1, self.target_grid[1] + self.range):
                    if y < 0 or y >= grid['resolution'][1]:
                        print('Hit y bound')
                        continue
                    weight = 0.3

                    if len(grid[x][y]['contains']) > 0: continue

                    for choice_x in range ( x-3, x+3):
                        if choice_x < 0 or choice_x >= grid['resolution'][0]:
                            continue
                        for choice_y in range(y - 3, y + 3):
                            if choice_y < 0 or choice_y >= grid['resolution'][1]:
                                continue
                            for item in grid[choice_x][choice_y]['contains']:
                                if item.team == 0:
                                    weight += 0.5
                                else:
                                    if self.team == item.team:
                                        weight += 0.2
                                    else:
                                        weight -= 0.2
                            total_weight += weight

                    #for prob in range(0,len(decision_weight)):
                    #    decision_weight[prob] = decision_weight[prob] / total_weight
                    decision.append([x,y])
                    decision_weight.append(weight)

            normalise_factor = sum(decision_weight)
            decision_weight = list(map(lambda x:x/normalise_factor, decision_weight))
            choice = numpy.random.choice(range(0,len(decision)),1, p=decision_weight)
            choice = decision[choice[0]]

            print(self.target_grid, choice, len(grid[self.target_grid[0]][self.target_grid[1]]['contains']))
            for item in range(0, len(grid[self.target_grid[0]][self.target_grid[1]]['contains'])):
                if grid[self.target_grid[0]][self.target_grid[1]]['contains'][item] == self:
                    grid[self.target_grid[0]][self.target_grid[1]]['contains'].remove(self)
            self.target_grid = choice

            print(self.target_grid)
            grid[self.target_grid[0]][self.target_grid[1]]['contains'].append(self)


            self.target_position = grid[self.target_grid[0]][self.target_grid[1]]['position']