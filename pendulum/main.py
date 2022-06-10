import pygame
import math
import button
import graph
import matplotlib.pyplot as plt

class ball(object):

    def __init__(self, XY, radius, balance):
        self.x = XY[0]
        self.y = XY[1]
        
        self.old_x = XY[0]
        self.old_y = XY[1]

        self.radius = radius

        self.balance = balance

        self.vel = 0

        self.angacc = 0

    def angle_length(self):
        self.length = math.sqrt(math.pow(self.x - self.balance, 2)
                            + math.pow(self.y - 50, 2))
        self.angle = math.asin((self.x - self.balance) / self.length)

    def update_position(self):
        self.x = round(self.balance + self.length * math.sin(self.angle))
        self.y = round(50 + self.length * math.cos(self.angle))

    def draw(self, bg, bg2, color_line, 
             color_border_circle, color_fill_circle):

        # Pendulum
        pygame.draw.lines(bg, color_line, False, 
                          [(self.balance, 50), (self.x, self.y)], 2)
        pygame.draw.circle(bg, color_border_circle, 
                           (self.x, self.y), self.radius)
        
        # Path
        pygame.draw.line(bg2, color_fill_circle, 
                         (self.old_x, self.old_y), 
                         (self.x, self.y), 2)
        bg.blit(bg2, (0, 0))

        # Fill circle
        pygame.draw.circle(bg, color_fill_circle, 
                           (self.x, self.y), self.radius - 2)


def main():
    # Parameters
    cont = True # game continue?
    count_loop = 0
    times_loop = []
    graph_check = False
    arr_X = [] # Store position for graph
    acceleration = False
    angacc_change = 0
    vel_change = 0

    width, height = 950, 600

    # Balance position
    balance = int(width / 2)
    pendulum = ball((balance, -10), 2, balance)

    # Set screen
    pygame.init()

    background = pygame.display.set_mode((width, height))
    background2 = pygame.Surface([width, height], pygame.SRCALPHA, 32)
    background2 = background2.convert_alpha()

    # Background images
    bg_img = pygame.image.load(r'assets/background.png').convert()

    # Button images
    gravity_img = pygame.image.load(r'assets/velocity.png').convert()
    damping_img = pygame.image.load(r'assets/damping.png').convert()
    graph_img = pygame.image.load(r'assets/graph.png').convert()

    plus1_img = pygame.image.load(r'assets/plus.png').convert()
    plus2_img = pygame.image.load(r'assets/plus.png').convert()
    minus1_img = pygame.image.load(r'assets/minus.jpg').convert()
    minus2_img = pygame.image.load(r'assets/minus.jpg').convert()

    # Buttons
    plus_gravity = button.Button(723, 120, plus1_img, 0.08)
    minus_gravity = button.Button(860, 119, minus1_img, 0.05)
    
    plus_damping = button.Button(718, 168, plus2_img, 0.08)
    minus_damping = button.Button(858, 168, minus2_img, 0.05)

    graph_button = button.Button(780, 230, graph_img, 1)
    gravity_button = button.Button(750, 100, gravity_img, 0.05)
    damping_button = button.Button(750, 150, damping_img, 0.05)

    # Color
    white = (255, 255, 255)
    black = (0, 0, 0)
    gray = (150, 150, 150)
    dark_red = (150, 0, 0)

    # Game loop
    clock = pygame.time.Clock()

    fig, ax = plt.subplots()
    plt.ion()
    plt.show()

    while cont:
        
        clock.tick(120)
        check_click = 0

        for event in pygame.event.get():
            # Increase gravity
            if plus_gravity.draw(background):
                angacc_change += 0.0003

                print(angacc_change)
                check_click += 1

            # Decrease gravity
            elif minus_gravity.draw(background):
                angacc_change -= 0.0003

                print(angacc_change)
                check_click += 1

            # Increase damping
            elif plus_damping.draw(background):
                vel_change -= 0.0005

                print(vel_change)
                check_click += 1

            # Decrease damping
            elif minus_damping.draw(background):
                vel_change += 0.0005

                print(vel_change)
                check_click += 1

            # Draw graph
            elif graph_button.draw(background):
               if graph_check == False:
                   graph_check = True
               else:
                   graph_check = False

               print("Done!!!!")
               check_click += 1

            if event.type == pygame.QUIT:
                cont = False
            elif check_click == 0:
                if (event.type == pygame.MOUSEBUTTONDOWN):

                    background2 = pygame.Surface([width, height], 
                                                 pygame.SRCALPHA, 32)
                    background2 = background2.convert_alpha()

                    # Create the pendulum
                    pendulum = ball(pygame.mouse.get_pos(), 15, balance)

                    # Caculate angle and length
                    pendulum.angle_length()

                    # Move pendulum
                    acceleration = True           

        # Increase gravity
        if plus_gravity.draw(background):
            angacc_change += 0.0003
            
            print(angacc_change)
            check_click += 1

        # Decrease gravity
        elif minus_gravity.draw(background):
            angacc_change -= 0.0003

            print(angacc_change)
            check_click += 1

        # Increase damping
        elif plus_damping.draw(background):
           vel_change -= 0.0005
               
           print(vel_change)
           check_click += 1

        # Decrease damping
        elif minus_damping.draw(background):
           vel_change += 0.0005
               
           print(vel_change)
           check_click += 1

        # Draw graph
        elif graph_button.draw(background):
           if graph_check == False:
               graph_check = True
           else:
               graph_check = False

           print("Done!!!!")
           check_click += 1

        # Pendulum moving 
        if acceleration:

            times_loop.append(str(count_loop))

            # Save x, y
            pendulum.old_x = pendulum.x
            pendulum.old_y = pendulum.y 
            
            # Possition with respect to balance position
            arr_X.append(str(pendulum.x - pendulum.balance))

            # Angular acceleration
            pendulum.angacc = -(0.0005 + angacc_change) * math.sin(pendulum.angle)
            
            # Velocity
            pendulum.vel += pendulum.angacc

            # Damping
            pendulum.vel *= (1 + vel_change)

            # New angle
            pendulum.angle += pendulum.vel

            # New x, y
            pendulum.update_position()

            count_loop += 1

        # Graph
        if graph_check == True:
            position_x, position_y = graph.coordinates_process()

            ax.plot(position_y, position_x)
            ax.set_title('Pendulum Graph')
            ax.set_xlabel('Position update instance')
            ax.set_ylabel('Position with respect to balance')
            
            plt.gcf().canvas.draw()        

        coordinates = 'coordinates.txt'
        with open(coordinates, 'w') as c:
            c.write(' '.join(arr_X))
        c.close()
        
        times = 'times.txt'
        with open(times, 'w') as t:
            t.write(' '.join(times_loop))
        t.close()
        
        # Draw
        background.fill(white)
 
        background.blit(pygame.transform.scale(
                    bg_img, (955, 555)), (0, 0))
    
        background.blit(pygame.transform.scale(
                    gravity_img, (100, 55)), (750, 100))
        background.blit(pygame.transform.scale(
                    damping_img, (100, 55)), (750, 150 ))
        background.blit(pygame.transform.scale(
                    plus1_img, (20, 20)), (720, 116))
        background.blit(pygame.transform.scale(
                    minus1_img, (23, 15)), (860, 119))
        background.blit(pygame.transform.scale(
                    plus2_img, (20, 20)), (720, 170))
        background.blit(pygame.transform.scale(
                    minus2_img, (23, 15)), (860, 170))
        background.blit(pygame.transform.scale(
                    graph_img, (100, 55)), (780, 230))

        pendulum.draw(background, background2, black, black, dark_red)
        pygame.display.update()

    # End game
    pygame.quit()


if __name__ == '__main__':
    main()
