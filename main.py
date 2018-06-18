from pyglet import window, app, graphics, clock,gl
import object_main
import random

grid_size = [30,30]

UI = {
        'Main': {'size': [800, 600],   'position': [0, 0]},
        'Field': {'size': [600, 500],  'position': [150, 50]},
        'Grid': {'resolution': grid_size}
}

UI['Grid']['step'] = [UI['Field']['size'][0] / UI['Grid']['resolution'][0],
                      UI['Field']['size'][1] / UI['Grid']['resolution'][1]]

main_window = window.Window(width = UI['Main']['size'][0], height = UI['Main']['size'][1])
object_list = []

@main_window.event
def on_draw():
    main_window.clear()
    batch_actors.draw()
    graphics.draw(4,gl.GL_LINE_LOOP,('v2i',[
        UI['Field']['position'][0], UI['Field']['position'][1],
        UI['Field']['position'][0]+UI['Field']['size'][0], UI['Field']['position'][1],
        UI['Field']['position'][0]+UI['Field']['size'][0], UI['Field']['position'][1]+UI['Field']['size'][1],
        UI['Field']['position'][0], UI['Field']['position'][1]+UI['Field']['size'][1],
    ]))


def update(dt):
    for obj in object_list:
        obj.decision(grid,0)
        obj.move()


batch_actors = graphics.Batch()
foreground = graphics.OrderedGroup(1)

grid = {}
grid['size'] = grid_size
grid['resolution'] = UI['Grid']['resolution']


for x in range(0,grid_size[0]):
    grid[x]={}
    for y in range(0,grid_size[1]):
        grid[x][y]={'position':[int(x*UI['Grid']['step'][0] + UI['Field']['position'][0]),
                                int(y * UI['Grid']['step'][1] + UI['Field']['position'][1])]}
        grid[x][y]['contains']=[]


for team in range(0,2):
    for i in range (0,4):
        pos_x = random.randint(1, int((grid_size[0] / 4) -1)  + int(grid_size[0]*team/2 + grid_size[0] / 8))
        pos_y = random.randint(1, int((grid_size[1] / 4) -1)  + int(grid_size[1]*team/2 + grid_size[1] / 8))
        new_object = object_main.Basic(grid[pos_x][pos_y]['position'], [pos_x,pos_y], team, batch_actors, foreground)
        new_object.decision(grid,1)
        object_list.append(new_object)

clock.schedule_interval(update,1/30);

app.run()

