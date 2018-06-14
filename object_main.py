from pyglet import sprite, image
import random

images = [image.load('./images/circle.png')]
time_scale = 1


class Basic:
    def __init__(self,position, target, team, batch_set, order_group):
        self.position = position
        self.team = team
        self.speed = 1
        self.target_position = self.position
        self.target_grid = target
        self.sprite = sprite.Sprite(images[0], batch=batch_set, group=order_group, x=position[0], y=position[1])
        print (self.target_position)

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
        if self.position == self.target_position or interrupt == 1:

            self.target_grid[0] += random.randint(-1,  1)
            self.target_grid[1] += random.randint(-1, 1)
            print(self.target_grid)
            self.target_position = grid[self.target_grid[0]][self.target_grid[1]]['position']