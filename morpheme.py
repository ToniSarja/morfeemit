import os
import pymunk
import pygame
from pymunk.vec2d import Vec2d
import json
import random
import pymunk.pygame_util
import sys
from prefixes_and_stems_in_dictionaries import *
from derivation_on_collision import *
# Main game loop

clock = pygame.time.Clock()

# Set the window size
WIDTH, HEIGHT = 1000, 800
window_size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption('Prefix')

# Initialize Pygame and PyMunk
pygame.init()
space = pymunk.Space()
space.gravity = (0, 900)  # Set the gravity

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

import os
import pygame
import pymunk
from pymunk.vec2d import Vec2d

class Stem:
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

        # Create a pivot joint body
    
    def draw(self, screen):
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

class Derivation:
    def __init__(self, space, radius, position, mass, elasticity, moment, image_path):
        self.body = pymunk.Body(mass, moment)
        self.body.position = position
        self.radius = radius 
        self.shape = pymunk.Circle(self.body, radius)
        
        self.image_path = image_path
        self.body.position = position
        
        # Only add the body and shape once
        space.add(self.body, self.shape)
        
        self.shape.elasticity = 0.7
        self.shape.friction = 0.2
        self.shape.color = (0, 255, 0, 0)
        
        # Load the image using Pygame
        self.image = pygame.image.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), self.image_path))

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

def collision_callback(arbiter, space, data):
    contact_points = arbiter.contact_point_set.points
    for contact_point in contact_points:
        collision_point = contact_point.point_a
        screen_point = (int(collision_point.x), int(collision_point.y))
        particle1.add_particles(screen_point)

derivations = []

def collision1(arbiter, space, data):
    mouse_position = pygame.mouse.get_pos()
    derive = Derivation(space, 40, mouse_position, 30, 30, 30, "morfeemit/deriv/za_pisat_derive.png")
    derivations.append(derive)
    derive.body.apply_impulse_at_local_point((10000, 0), (0, 0))
    contact_points = arbiter.contact_point_set.points
    for contact_point in contact_points:
        collision_point = contact_point.point_a
        screen_point = (int(collision_point.x), int(collision_point.y))
        for i in range(10):
            particle1.add_particles(screen_point)


    
def collision2(arbiter, space, data):
    mouse_position = pygame.mouse.get_pos()
    derive = Derivation(space, 40, mouse_position, 30, 30, 30, "morfeemit/deriv/do_pisat_derive.png")
    derivations.append(derive)
    derive.body.apply_impulse_at_local_point((10000, 0), (0, 0))
    contact_points = arbiter.contact_point_set.points
    for contact_point in contact_points:
        collision_point = contact_point.point_a
        screen_point = (int(collision_point.x), int(collision_point.y))
        for i in range(10):
            particle1.add_particles(screen_point)



handler0 = space.add_collision_handler(1, 2)
handler1 = space.add_collision_handler(3, 2)
handler2 = space.add_collision_handler(1, 4)
handler3 = space.add_collision_handler(1, 5)

handler0.post_solve = collision1
handler1.post_solve = collision2



def run(window, width, height):
    current_key = 'No prefix selected'
    running = True
    mouse_position = pygame.mouse.get_pos()

    current_key_index = 0
    keys = list(prefixes.keys())
    now = pygame.time.get_ticks()
    while running:
        
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
                    logo.body.apply_impulse_at_local_point((50000, 0), (0, 0))
                    
                except:
                    pass



        # Update PyMunk space
        space.step(1 / 60.0)
        
        # Clear the screen
        screen.fill(('white'))
        text = font.render(f'{current_key}', True, (0, 0, 0))
        screen.blit(text,(50, 50))
        particle1.emit()
        # Draw all Prefix objects
        for logo_shape in logos:
            logo_shape.draw(screen)
        for derivation in derivations:
            derivation.draw(screen)
        time_difference = pygame.time.get_ticks() - now
        if time_difference >= 1000:
            logo = Stem(space, 40, (500, 0), 30, 30, 30, "morfeemit/stem/pisat.png",2)
            logos.append(logo)
            now = pygame.time.get_ticks()
            

        
            

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60)

    # Quit Pygame
    pygame.quit()

if __name__ == "__main__":
	run(screen, WIDTH, HEIGHT)
