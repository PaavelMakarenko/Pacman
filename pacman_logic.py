import random

class GameObject:
    """
    GameObject has:
    x,y coordinates, positive integers, zero point is at upper left corner
    x, y sizes as positive integers, object rectangle is defined by x +/- x_size and  y +/- y_size
    collision detection/reaction
    """

    def __init__(self, x, y, x_size, y_size, obj_type="default"):   # __init__ tekitab klassi eksemplari,
                                                # väljakutse mo=MovingObject(x,y,x_s,y_s)
                                                # NB! Väljakutsel jääb self argumendina ära 
        """ Initialize coordinates and sizes"""
        self.x = x # Tekitab ja väärtustab meie objektil atribuudi x
        self.y = y
        self.x_size = x_size
        self.y_size = y_size
        self.obj_type = obj_type

    def collides(self, other):
        """ Detect if our size rect. overlaps with other GameObjects """
        x_overlaps = abs(self.x - other.x) < self.x_size + other.x_size
        y_overlaps = abs(self.y - other.y) < self.y_size + other.y_size
        return x_overlaps and y_overlaps

    def collision_react(self, other):
        """ React to collision with other GameObject """
        pass


class Pellet(GameObject):
    def __init__(self, x, y, x_size, y_size, obj_type="default", eaten_callback=None):
        super().__init__(x, y, x_size, y_size, obj_type="default")
        self.eaten_callback = eaten_callback
        
    def collision_react(self, other):
        if other.obj_type == "pacman" and self.eaten_callback != None:
            self.eaten_callback(self)


class MovingObject(GameObject): # Kuna MovingObject on GameObjecti alamklass, siis
                                # võtab see kõik GameObjecti meetodid vaikimisi üle.                
    """
    MovingObject is a GameObject with additional movement methods and heading (dx, dy)
    It calls a callback function when moves.
    """

    def __init__(self, x, y, x_size, y_size, dx, dy, obj_type="default"):
        """ dx, dy: heading, change of x,y coordinates """
        super().__init__(x, y, x_size, y_size, obj_type) # Ülemklassi meetodi väljakutse
        self.dx = dx
        self.dy = dy
 
    def set_heading(self, dx, dy):
        self.dx = dx
        self.dy = dy

    def tick(self):
        """ React to timer tick by moving """
        self.move(self.dx, self.dy)

    def move(self, dx=0, dy=0):
        """ Move the object by dx, dy """
        self.x += dx
        self.y += dy

        
class PacMan(MovingObject): # MovingObject on PacMani ülemklass
    """
    Represents the PacMan moving object.
    """

    def __init__(self, x, y, x_size, y_size, dx, dy, obj_type="pacman"):
        super().__init__(x, y, x_size, y_size, dx, dy, obj_type)
        self.score = 0

    def collision_react(self, other):
        if other.obj_type == "wall":
            self.move(-self.dx, -self.dy)
        elif other.obj_type == "ghost":
            self.lose_life()
        elif other.obj_type == "pellet":
            self.score += 1
            self.change_score(self)

    def lose_life(self):
        pass

    def change_score(self):
        pass
        
    
class Ghost(MovingObject):
    """
    Represents the Ghost moving object.
    """
        
    def collision_react(self, other):
        if other.obj_type == "wall":
            self.move(-self.dx, -self.dy)
            speed = abs(self.dx + self.dy)
            dx, dy = random.choice([(-speed, 0), (speed, 0), (0, -speed), (0, speed)])
            self.set_heading(dx, dy)
        
  
    

class World:
    """
    A collection of all objects in the game.
    It forwards tick messages and detects collisions.
    """

    def __init__(self, pellets, walls, moving_objs):
        """
        static_objs: list of static GameObjects
        moving_objs: list of MovingObjects
        """

        self.pellets = pellets
        self.walls = walls
        self.moving_objs = moving_objs

    def tick(self):
        """
        Forwards tick to all moving objects
        """
        for mo in self.moving_objs:
            mo.tick()
            # Kontrolli kokkupõrkeid
            for other_obj in self.pellets + self.walls + self.moving_objs:
                if mo != other_obj and mo.collides(other_obj):
                    # Saada sõnumid
                    mo.collision_react(other_obj)
                    other_obj.collision_react(mo)

    

if __name__ == "__main__":
    def eaten(pellet):
        pellets.remove(pellet)
        print("eaten!")
    pellets = []
    p1 = Pellet(100, 100, 10, 10, "pellet", eaten_callback=eaten)
    pm = PacMan(115, 115, 10, 10, 0, 10, "pacman")
    g = Ghost(115, 115, 10, 10, 0, -10, "ghost")
    #print(mo1.collides(mo2), mo2.collides(mo1))
    p2 = Pellet(115, 200, 10, 10, "pellet", eaten_callback=eaten)
    w1 = GameObject(115, 25, 30, 5, "wall")
    pellets.append(p1)
    pellets.append(p2)
    w = World(pellets , [w1], [pm, g])
    #print(mo3.collides(mo2), mo2.collides(mo3))
    for step in range(14):
        w.tick()
        #mo2.tick()
        #mo2.set_heading(0, 10)
        print("step", step,  pm.x, pm.y, g.x, g.y)
        