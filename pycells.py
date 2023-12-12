import os
import pymunk
import pygame
from pymunk.vec2d import Vec2d
import json
import random
import pymunk.pygame_util
import sys
from derivation_on_collision import *
# Main game loop
running = True
clock = pygame.time.Clock()

# Set the window size
WIDTH, HEIGHT = 1000, 800
window_size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption('Prefix')

# Initialize Pygame and PyMunk
pygame.init()
space = pymunk.Space()
space.gravity = (0, 1000)  # Set the gravity

PARTICLE_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(PARTICLE_EVENT,40)

current_parameter_set = 0
current_stem_parameter_set = 0
current_derive_parameter_set = 0

font = pygame.font.Font(None, 24)

# List to store Prefix objects
logos = []


class Morpheme:
    def __init__(self, space, radius, position, mass, elasticity, moment,  image_path, collision_type):
        # Create a PyMunk body and circle shape for the ball
        self.body = pymunk.Body(mass, moment)
        self.body.position = position
        self.radius = radius 
        self.shape = pymunk.Circle(self.body, radius)
        self.image_path = image_path # List of image paths
        self.shape.collision_type = collision_type
        self.shape.elasticity = 1
        # Load the image using Pygame
        self.image = pygame.image.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), self.image_path))

        # Add the ball to the space
        space.add(self.body, self.shape)

    def get_position(self):
        return self.body.position
    
    def draw(self, window):
        # Get the position of the body
        p = self.body.position
        p = Vec2d(p.x, p.y)

        # Calculate the offset for drawing
        offset = Vec2d(*self.image.get_size()) / 2
        p = p - offset

        # Draw the image on the screen
        rect = self.image.get_rect()
        rect.topleft = p
        screen.blit(self.image, rect.topleft)


class ParticlePrinciple:
	def __init__(self):
		self.particles = []

	def emit(self):
		if self.particles:
			self.delete_particles()
			for particle in self.particles:
				particle[0][1] += particle[2][0]
				particle[0][0] += particle[2][1]
				particle[1] -= 0.2
				pygame.draw.circle(screen,pygame.Color('Red'),particle[0], int(particle[1]))

	def add_particles(self, pos):
		pos_x = pos[0]
		pos_y = pos[1] 
		radius = 10
		direction_x = random.randint(-3,3)
		direction_y = random.randint(-3,3)
		particle_circle = [[pos_x,pos_y],radius,[direction_x,direction_y]]
		self.particles.append(particle_circle)

	def delete_particles(self):
		particle_copy = [particle for particle in self.particles if particle[1] > 0]
		self.particles = particle_copy
          

particle1 = ParticlePrinciple()

def create_boundaries(space, width, height):
	rects = [
		[(width/2, height - 10), (width, 20)],
		[(width/2, 10), (width, 20)],
		[(10, height/2), (20, height)],
		[(width - 10, height/2), (20, height)]
	]

	for pos, size in rects:
		body = pymunk.Body(body_type=pymunk.Body.STATIC)
		body.position = pos
		shape = pymunk.Poly.create_box(body, size)
		shape.collision_type = 2
		shape.friction = 0.5
		space.add(body, shape)

derivations = []

def collision_handler(arbiter, space, data):
    # Get the total impulse applied during the collision
    impulse = arbiter.total_impulse
    force_x, force_y = impulse.x, impulse.y
    print(force_y)
    if force_y <= -10000:
        print("He's dead")
 
current_prefix_index = 0
mouse_position = pygame.mouse.get_pos()
prefixes = {
     "za":{"image_path":"morfeemit/prefix/za.png","collision_type":1}
            } 

current_key_index = 0
keys = list(prefixes.keys())

handler = space.add_collision_handler(1, 2)
handler.post_solve = collision_handler

def create_missile(space, position):
    mass = 1
    moment = pymunk.moment_for_circle(mass, 0, 10)  # Inertia for a circle
    body = pymunk.Body(mass, moment)
    body.position = position
    shape = pymunk.Circle(body, 10)
    shape.elasticity = 0.8
    shape.friction = 1.0
    space.add(body, shape)
    return body

def update_missile(missile, target):
    direction = target.get_position() - missile.position
    missile.velocity = 200 * direction.normalized()

current_key = 'No prefix selected'

def run(window, width, height):
    current_key = 'No prefix selected'
    running = True
    launch_missile = False
    mouse_position = pygame.mouse.get_pos()
    create_boundaries(space, width, height)
    current_key_index = 0
    keys = list(prefixes.keys())
    missile = None
    

    now = pygame.time.get_ticks()
    pygame.key.set_repeat(0, 0) 

    while running:
        launch_missile = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEWHEEL:
                current_key_index = (current_key_index + 1) % len(keys)
                current_key = keys[current_key_index]
                current_value = prefixes[current_key]
                print(current_value)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                try:
                    mouse_position = pygame.mouse.get_pos()
                    # Get the image path based on the current_prefix_index
                    para = current_value
                    # Create a Morpheme object and add it to the logos list
                    logo = Morpheme(space, 40, mouse_position, 30, 30, 30, **para)
                    logos.append(logo)
                except:
                    pass
            if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                logo.body.apply_impulse_at_local_point((0, -15000), (0, 0))
                for i in range(10):
                    particle1.add_particles(logo.body.position)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                logo.body.apply_impulse_at_local_point((0, 15000), (0, 0))                 
            if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                logo.body.apply_impulse_at_local_point((10000, 0), (0, 0))
            if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                logo.body.apply_impulse_at_local_point((-10000, 0), (0, 0))
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                logo.body.apply_impulse_at_local_point((0, 100000), (0, 0))
                for i in range(100):
                    particle1.add_particles(logo.body.position)                  
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LSHIFT:
                logo.body.apply_impulse_at_local_point((100000, 0), (0, 0))         
             
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:
            # Left mouse button clicked, launch the missile
                launch_missile = True
        if launch_missile:
            print("missile launch")
            # Create the missile at the mouse click position
            missile = create_missile(space, pygame.mouse.get_pos())
            launch_missile = False


        # Update PyMunk space
        space.step(1 / 60.0)
 
        # Clear the screen
        screen.fill(('white'))
        if missile:
            # Update missile's position based on the target
            update_missile(missile, logo)
        if missile:
            pygame.draw.circle(screen, (255, 0, 0), missile.position.int_tuple, 10)

        particle1.emit()
        # Draw all Prefix objects
        for logo_shape in logos:
            logo_shape.draw(screen)

        if missile:
            # Update missile's position based on the target
            update_missile(missile, logo_shape)
        if missile:
            pygame.draw.circle(screen, (255, 0, 0), missile.position.int_tuple, 10)            

        
            

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

    # Quit Pygame
    pygame.quit()

if __name__ == "__main__":
	run(screen, WIDTH, HEIGHT)
