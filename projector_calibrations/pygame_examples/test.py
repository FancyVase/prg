import pygame

class Disk:
    def __init__(self,color,pos,size): # initialze the properties of the object
        self.color=color
        self.pos=pos
        self.size=size
    
    def Render(self,screen):
        pygame.draw.circle(screen,self.color,self.pos,self.size, 5)

def main():
    screen=pygame.display.set_mode((1580,900))
    running=True
    RenderList=[] # list ofdisk
    MousePressed=False # Pressed down THIS FRAME
    MouseDown=False # mouse is held down
    MouseReleased=False # Released THIS FRAME
    Target=None # target of Drag/Drop
    colors = [(255,0,0),(0,255,0),(0,0,255),(255,0,255)] #purple, blue, green, red
    while running:
        screen.fill(0) # clear screen
        pos = pygame.mouse.get_pos()
        for Event in pygame.event.get():
            if Event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
                running = False
                break
            
            if Event.type == pygame.MOUSEBUTTONDOWN:
                MousePressed=True 
                MouseDown=True 
               
            if Event.type == pygame.MOUSEBUTTONUP:
                MouseReleased=True
                MouseDown=False
             
        if MousePressed==True:
            for item in RenderList: # search all items
                if (pos[0]>=(item.pos[0]-item.size) and 
                    pos[0]<=(item.pos[0]+item.size) and 
                    pos[1]>=(item.pos[1]-item.size) and 
                    pos[1]<=(item.pos[1]+item.size) ): # inside the bounding box
                    Target=item # "pick up" item
            
            if Target is None and len(RenderList) < 4: # didn't find any?
                Target=Disk(colors[-1],pos,10) # create a new one
                colors.insert(0,colors[-1])
                colors.pop()
                RenderList.append(Target) # add new disk to render list
            
        if MouseDown and Target is not None: # if we are dragging something
            Target.pos=pos                   # move the target with us
        
        if MouseReleased:
            Target=None # Drop item, if we have any
        
        vertices = []

        for item in RenderList:
            item.Render(screen) # Draw all items
            if item.pos not in vertices:
                vertices.append(item.pos)

        if len(RenderList) == 4:
            pygame.draw.polygon(screen,(255,255,255),vertices)
            
        MousePressed=False # Reset these to False
        MouseReleased=False # Ditto        
        pygame.display.flip()
    print vertices
    return # End of function
    
if __name__ == '__main__':
    main() # Execute our main function