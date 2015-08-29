import pygame
from pygame.locals import *
from mapping import *

class Disk:
    def __init__(self,color,pos,size): # initialize the properties of the object
        self.color = color
        self.pos = pos
        self.size = size
    
    def Render(self,screen):
        pygame.draw.circle(screen,self.color,self.pos,self.size, 3)

class Grid:
    def __init__(self, color, world_width, world_height, numcells, transform, transform_reverse, bounds, modify=False):
        self.color = color;
        self.width = world_width
        self.height = world_height
        self.numcells = numcells
        self.transform = transform
        self.transform_reverse = transform_reverse
        self.bounds = bounds
        self.dx = 0
        self.dy = 0


    def Render(self, screen):
        cw = self.width/float(self.numcells) # cell width
        ch = self.height/float(self.numcells) # cell height

        for i in range(self.numcells): 
            for j in range(self.numcells):
                world_vertices = [[i*cw + self.dx, (1+i)*cw + self.dx, (1+i)*cw + self.dx,i*cw + self.dx],[(1+j)*ch - self.dy,(1+j)*ch - self.dy, j*ch - self.dy, j*ch - self.dy]]
                lines = Lines("grid " + str(i) + ", " + str(j),self.color,world_vertices,self.transform,self.transform_reverse,self.bounds,self.dx,self.dy)
                lines.Render(screen)
                # print str(i) + "," + str(j) + " " + str(world_vertices)

    def Rainbow(self): # for looping colorful displays
        r, g, b = self.color
        if b == 50 and r < 150:
            r += 1
        if r == 150 and g < 150:
            g += 1
        if g == 150 and b < 150:
            b += 1
        if b == 150 and r > 50:
            r -= 1
        if r == 50 and g > 50:
            g -= 1
        if g == 50 and b > 50:
            b -= 1 

        self.color = (r, g, b)

class Lines:
    def __init__(self, name, color, world_vertices, transform, transform_reverse, bounds, dx=0, dy=0):
        self.name = name;
        self.color = color;
        self.world_vertices = world_vertices
        self.p = [] # projector coordinates
        self.transform = transform
        self.transform_reverse = transform_reverse
        self.bounds = bounds
        self.dx = dx
        self.dy = dy

    def Render(self, screen):
        moved = [[x + self.dx for x in self.world_vertices[0]], [y - self.dy for y in self.world_vertices[1]]]
        self.world_vertices = moved
        self.p = perspective_transform(self.world_vertices, self.transform)

        # pygame.draw.polygon(screen,(255,255,255),self.p)

        for i in range(len(self.p)):
            if i == len(self.p) - 1:
                draw_line(screen, self.color, self.p[i], self.p[0], self.bounds)
            else:
                draw_line(screen, self.color, self.p[i], self.p[i+1], self.bounds)
 

def main():
    disks = False # turn on/off calibrating disks
    screen = pygame.display.set_mode((3072,768), pygame.FULLSCREEN)
    running = True
    DiskList = []
    LinesList = []
    GridList = []
    MousePressed = False # Pressed down THIS FRAME
    MouseDown = False # mouse is held down
    MouseReleased = False # Released THIS FRAME
    Target = None # target of Drag/Drop
    index = None
    LinesTarget = None
    colors = [(255,0,0),(0,255,0),(0,0,255),(255,0,255)] #purple, blue, green, red
    colors = [(255,255,255),(255,255,255)]
    p1bounds = [(0,0),(1023,768)]
    p2bounds = [(1024,0),(2048,768)]
    p3bounds = [(2048,0),(3072,768)]

    # LinesList.append(Lines("projector 1 lines", (0, 0, 0), tcmb_p3, p1transform,p1transform_reverse,p1bounds))
    # LinesList.append(Lines("projector 2 lines", (0, 0, 0), tcmb_p3, p2transform,p2transform_reverse,p2bounds))
    # LinesList.append(Lines("projector 3 lines", (0, 0, 0), tcmb_p3, p3transform,p3transform_reverse,p3bounds))

    world_width = 140
    world_height = 220
    numcells = 10

    GridList.append(Grid((150,50,50), world_width, world_height, numcells, p1transform, p1transform_reverse, p1bounds))
    GridList.append(Grid((150,50,50), world_width, world_height, numcells, p2transform, p2transform_reverse, p2bounds))
    GridList.append(Grid((150,50,50), world_width, world_height, numcells, p3transform, p3transform_reverse, p3bounds, True))

    dx = 750
    dy = 500
    
    img_orig = pygame.image.load('vision/img/dropline.png')
    img = img_orig.copy()
    colorkey = img.get_at((0,0))
    img_orig.set_colorkey(colorkey, RLEACCEL)
    img_rect = img.get_rect(center=(dx,dy))
    angle = 0

    while running:
        screen.fill(0) # clear screen

        pos = pygame.mouse.get_pos()
        for Event in pygame.event.get():
            if Event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
                running = False
                break

            if pygame.key.get_pressed()[pygame.K_SPACE]:
                pygame.display.toggle_fullscreen()

            if pygame.key.get_pressed()[pygame.K_a]:
                angle += 60

            if pygame.key.get_pressed()[pygame.K_d]:
                angle -= 60

            if pygame.key.get_pressed()[pygame.K_RIGHT]:
                for lines in LinesList:
                    lines.dx += .1
                
                for grid in GridList:
                    grid.dx += 1

                dx += 10


            if pygame.key.get_pressed()[pygame.K_LEFT]:
                for lines in LinesList:
                    lines.dx -= .1

                for grid in GridList:
                    grid.dx -= 1

                dx -= 10

            if pygame.key.get_pressed()[pygame.K_UP]:
                for lines in LinesList:
                    lines.dy -= 0.1

                for grid in GridList:
                    grid.dy -= 1

                dy -= 10

            if pygame.key.get_pressed()[pygame.K_DOWN]:
                for lines in LinesList:
                    lines.dy += 0.1

                for grid in GridList:
                    grid.dy += 1

                dy += 10

            if Event.type == pygame.MOUSEBUTTONDOWN:
                MousePressed=True 
                MouseDown=True 
               
            if Event.type == pygame.MOUSEBUTTONUP:
                MouseReleased=True
                MouseDown=False
             
        if MousePressed==True:
            for lines in LinesList:
                for vertex in lines.p:
                    if (pos[0]>=(vertex[0]-10) and 
                    pos[0]<=(vertex[0]+10) and 
                    pos[1]>=(vertex[1]-10) and 
                    pos[1]<=(vertex[1]+10) ): # inside the bounding box
                        LinesTarget=lines # select lines object
                        index=lines.p.index(vertex) 
            if disks:
                for disk in DiskList: # search all disks
                    if (pos[0]>=(disk.pos[0]-disk.size) and 
                        pos[0]<=(disk.pos[0]+disk.size) and 
                        pos[1]>=(disk.pos[1]-disk.size) and 
                        pos[1]<=(disk.pos[1]+disk.size) ): # inside the bounding box
                        Target=disk # "pick up" disk
                
                if Target is None and len(DiskList) < 100: # didn't find any?
                    Target=Disk(colors[-1],pos,4) # create a new one
                    colors.insert(0,colors[-1])
                    colors.pop()
                    DiskList.append(Target) # add new disk to render list
            
        if MouseDown and Target is not None:
            Target.pos=pos

        if MouseDown and LinesTarget is not None:
            LinesTarget.p[index] = pos
            LinesTarget.world_vertices = projector_to_world(LinesTarget.p, LinesTarget.transform_reverse)

        if MouseReleased:
            if LinesTarget is not None:
                v0 = LinesTarget.world_vertices[:2]
                v1 = coords_to_list(LinesTarget.p)[:2]
                LinesTarget.transform = get_transform_matrix(v0, v1)[0]

            v0 = None
            v1 = None
            Target=None # Drop disk, if we have any
            LinesTarget=None
            index=None
        
        vertices = []

        for disk in DiskList:
            disk.Render(screen) # Draw all disks
            if disk.pos not in vertices:
                vertices.append(disk.pos)

        for grid in GridList:
            grid.Render(screen)
            grid.Rainbow()

        if len(DiskList) == 100:
            polygon = pygame.draw.polygon(screen,(255,255,255),vertices)
            
        for lines in LinesList:
            lines.Render(screen)
        
        MousePressed=False # Reset these to False
        MouseReleased=False      

        # img = pygame.transform.rotate(img_orig, angle)
        # img_rect = img.get_rect(center=(dx,dy))
        # screen.blit(img, img_rect)

        pygame.display.flip()

    for lines in LinesList:
        print lines.name
        print "real coords: " + str(lines.world_vertices)
        print "virtual coords: " + str(coords_to_list(perspective_transform(lines.world_vertices,lines.transform)))
        print "----------------------------------"
    
    if disks:
        print "vertices: " + str([[x[0] for x in vertices],[x[1] for x in vertices]])
        print "cardboard is 64cm x 40 cm"

    return # End of function
    
if __name__ == '__main__':
    main() # Execute our main function
