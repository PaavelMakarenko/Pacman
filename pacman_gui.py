from tkinter import *
import pacman_logic as pm


class GUIMovingObject(pm.MovingObject):
    """
    Adds a method draw_inplace() to the MovingObject, that subclasses
    should redefine in an appropriate manner..
    """

    def __init__(self, x, y, x_size, y_size, dx, dy, cnv, obj_type="default"):
        """
        Added cnv parameter for GameApp Canvas.
        """
        super().__init__(x, y, x_size, y_size, dx, dy, obj_type)
        self.cnv = cnv
        self.id = self.draw_inplace()

    def move(self, dx=0, dy=0):
        super().move(dx, dy)
        self.draw_move(dx, dy)

    def draw_inplace(self):
        """
        Draw the shape to canvas according to x, y, x_size, y_size attributes.
        Return the shape id.
        """
        return None
    
    def draw_move(self, dx, dy):
        """
        Move the shape on canvas by dx, dy.
        """ 
        self.cnv.move(self.id, dx, dy)



class GUIPacMan(GUIMovingObject, pm.PacMan):

    def draw_inplace(self):
        return self.cnv.create_oval(self.x - self.x_size,
                                    self.y - self.y_size,
                                    self.x + self.x_size,
                                    self.y + self.y_size,
                                    fill = "yellow")

    def lose_life(self):
        super().lose_life()
        self.cnv.lose_life()
   

   # Näidata lõuendil skoori kui see muutub
        
class GUIGhost(GUIMovingObject, pm.Ghost):

    def draw_inplace(self):
        return self.cnv.create_oval(self.x - self.x_size,
                                    self.y - self.y_size,
                                    self.x + self.x_size,
                                    self.y + self.y_size,
                                    fill = "cyan")


class GameApp(Canvas):

    def __init__(self, root, *args, **kwargs):
        super().__init__(root, width=500, height=500, bg="blue", *args, **kwargs)
        self.root = root
        self.SPEED = 2
        self.pacman = GUIPacMan(100, 100, 10, 10, 0, 0, self, obj_type="pacman")
        self.world = self.create_world()
        root.bind("<KeyPress>", self.keypress) # Seome klahvid wasd vastavate callback funktsioonidega, kasutades Tk meetodi bind
        self.ticking = True

    def keypress(self, event):
        c = event.char
        if c == "w":
            self.pacman.set_heading(0, -self.SPEED)
        if c == "s":
            self.pacman.set_heading(0, self.SPEED)
        if c == "a":
            self.pacman.set_heading(-self.SPEED, 0)
        if c == "d":
            self.pacman.set_heading(self.SPEED, 0)

    def create_world(self):
        # Create walls
        wall_data = [(200, 30, 5, 50),
                     (70, 30, 30, 5),
                     (170, 130, 30, 5),
                     (100, 230, 50, 5),
                     (5, 200, 5, 200),
                     (400, 200, 5, 200),
                     (200, 5, 200, 5),
                     (200, 400, 200, 5)]
        walls = []
        for x, y, x_s, y_s in wall_data:
            self.create_rectangle(x-x_s, y-y_s, x+x_s, y+y_s, fill="white")
            walls.append(pm.GameObject(x, y, x_s, y_s, obj_type="wall"))

        # Create pellets
        P_SIZE = 3
        pellet_data = [(100, 120), (300, 200), (120, 45)]
        pellets = []
        for x, y in pellet_data:
            p_id = self.create_oval(x-P_SIZE, y-P_SIZE, x+P_SIZE, y+P_SIZE, fill="white")
            def eat(p, gui_id = p_id): #gui_id=p_id: trikk, et siduda callback f-niga p_id
                pellets.remove(p)
                self.delete(gui_id)                
            pellets.append(pm.Pellet(x, y, P_SIZE, P_SIZE, obj_type="pellet", eaten_callback=eat))
            
        ghosts = [GUIGhost(gx, gy, 10, 10, 3, 0, self, obj_type="ghost") for gx, gy in [(100, 200), (120, 200), (140, 200)]]
        return pm.World(pellets, walls, [self.pacman] + ghosts)
             
    def timer_tick(self, ms=50): # Reageerime kella tiksumisele ja registreerib järgmise tiksumise
        self.world.tick()
        if self.ticking:
            self.after(ms, self.timer_tick)

    def lose_life(self):
        self.delete(ALL)
        self.create_text(200, 200, fill="yellow", text="Game Over!")
        self.ticking = False


if __name__ == "__main__":
    root = Tk()
    app = GameApp(root)
    app.grid()
    app.timer_tick()
    root.mainloop()
    