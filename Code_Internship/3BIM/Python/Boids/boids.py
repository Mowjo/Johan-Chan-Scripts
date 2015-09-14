import math
import numpy as np

#===============================================================================
# CLASS POPULATION
#===============================================================================


class Population :
#-------------------------------------------------------------------------------
	def __init__( self, p_id) :
		# General information
		# Population ID
		self.p_id = str(p_id)
		# Display name
		self.name = ""

		# Interactions with the other populations
		# List of all predator populations for this population
		self.predator_list = []
		# List of all prey populations for this population
		self.prey_list = []
		# List of all antagonist populations (territorial competition) with this population
		self.antagonist_list = []
		# List of all populations in neutral interaction with this population
		self.neutral_list = []

		# Cinetic parameters
		self.max_speed = 10.0
		self.max_acceleration = 100.00

		# Interaction coefficients
		# multiplication coefficient for the own, antagonist and neutral populations interactions
		self.coeff_social = 1.0

		# With own members
		self.coeff_cohesion = 1.0
		self.coeff_allignment= 1.0
		self.coeff_separation = 1.0
		# With neutral
		self.coeff_neutral_separation = 1.0
		# With predators
		self.coeff_predator_avoidance = 1.0
		# With prey
		self.coeff_prey_chase = 1.0
		# With antagonists
		self.coeff_antagonist_intimidation = 1.0
		self.coeff_antagonist_avoidance = 1.0

		# With the physical world
		self.coeff_obstacle_avoidance = 1.0
		
		self.normalize_coefficients()

		# World perception, radius and angle
		# For unique coordinates: r>=0, 0<=theta<=pi
		# Of own membersd 	
		self.friend_radius = 10.0
		self.friend_theta = math.pi

		# Of predators (however, when close, predators are perceived even when behind)
		self.evasion_radius = 10.0
		self.evasion_theta = math.pi

		# Of prey (however, when close, prey is perceived even when behind)
		self.hunt_radius = 10.0
		self.hunt_theta = math.pi

		# Of others (antagonist and neutral populations)
		self.social_radius = 10.0
		self.social_theta = math.pi

		# Of the physical world
		self.obstacle_radius = 2.0
		self.obstacle_theta = math.pi

		# Display parameters
		self.display_size = 1
		self.display_color_code = 0
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
	def normalize_coefficients( self ) :
		sum_coeffs = float( self.coeff_social*(self.coeff_cohesion + self.coeff_allignment + 
								self.coeff_separation + self.coeff_neutral_separation + 
								self.coeff_antagonist_intimidation + self.coeff_antagonist_avoidance) +
				self.coeff_predator_avoidance + self.coeff_prey_chase )
		self.coeff_predator_avoidance /= sum_coeffs
		self.coeff_prey_chase /= sum_coeffs
		self.coeff_social /= sum_coeffs

		self.coeff_obstacle_avoidance /= (self.coeff_obstacle_avoidance + sum_coeffs)
#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
	def load_data( self, label, name, predator_list, prey_list, antagonist_list, neutral_list,
				cinetic_params, interaction_coeffs, perception_params, display_params) :
		# Population ID
		self.p_id = str(label)
		# Display name
		self.name = str(name)

		# List of all predator populations for this population
		self.predator_list = predator_list
		# List of all prey populations for this population
		self.prey_list = prey_list
		# List of all antagonist populations (territorial competition) with this population
		self.antagonist_list = antagonist_list
		# List of all populations in neutral interaction with this population
		self.neutral_list = neutral_list

		# Cinetic parameters
		self.max_speed, self.max_acceleration = cinetic_params

		# Interaction coefficients
		(self.coeff_social, self.coeff_cohesion, self.coeff_allignment, self.coeff_separation, 
		self.coeff_neutral_separation, 
		self.coeff_predator_avoidance, self.coeff_prey_chase, 
		self.coeff_antagonist_intimidation, self.coeff_antagonist_avoidance, 
		self.coeff_obstacle_avoidance) = interaction_coeffs
		
		self.normalize_coefficients()

		# World perception parameters
		(self.friend_radius, self.friend_theta, self.evasion_radius, self.evasion_theta, 
		self.hunt_radius, self.hunt_theta, self.social_radius, self.social_theta, 
		self.obstacle_radius, self.obstacle_theta) = perception_params

		# Display parameters
		self.display_size, self.display_color_code = display_params
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
	def __repr__(self) :
		return str(self.p_id) + " " + str(self.name)
#-------------------------------------------------------------------------------







#===============================================================================
# CLASS OBSTACLE
#===============================================================================


class Obstacle :
#-------------------------------------------------------------------------------
	def __init__( self, o_id ) :
		# Obstacle id
		self.o_id = int(o_id)
		# Obstacle position
		self.position = np.array([0.0, 0.0, 0.0])
		# Obstacle size
		self.size = 1.0
		
		# Display parameters
		self.display_size = 1
		self.display_color_code = 0
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
	def load_data(self, o_id, position, size, display_params) :
		# Obstacle id
		self.o_id = int(o_id)
		# Obstacle position
		self.position = np.array(position)
		# Obstacle size
		self.size = float(size)
		
		# Display parameters
		self.display_size, self.display_color_code = display_params
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
	def __repr__(self) :
		return str(self.o_id) + "\t" + str(self.position)
#-------------------------------------------------------------------------------










#===============================================================================
# CLASS PHYSICALWORLD
#===============================================================================

class PhysicalWorld :
#-------------------------------------------------------------------------------
	def __init__(self, w_id, dimensions, nb_obstacles, obstacle_size_range) :
		self.w_id = int(w_id)
		self.dimensions = np.array([float(dimensions[0]), float(dimensions[1]),
									float(dimensions[2])]) 
		self.nb_obstacles = int(nb_obstacles)
		c = float(obstacle_size_range[0])
		self.os_min = float(obstacle_size_range[0])
		self.os_max = float(obstacle_size_range[1])
		self.all_obstacles = []

		for i in range(1, self.nb_obstacles+1) :
			new_obstacle = Obstacle(i)
			position = np.random.rand(3)
			size = self.os_min + (self.os_max - self.os_max)*np.random.rand()
			display_params = (1, 0)
			new_obstacle.load_data(i, position, size, display_params)
			self.all_obstacles.append(new_obstacle)
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
	def load_world_datafile( self, import_filename ) :
		input_file = open(str(import_filename), "r")

		wdimensions = []
		line_wdimensions = (input_file.readline().split())[1:]
		
		for i in range(0, 3):
			wdimensions.append(float(line_wdimensions[i]))
		
		self.dimensions = np.array(wdimensions)

		self.nb_obstacles = int((input_file.readline().split())[1])
		
		wosizerange = (input_file.readline().split())[1:]
		self.os_min = float(wosizerange[0])
		self.os_max = float(wosizerange[1])
		
		obstacle_labels = (input_file.readline().split())[1:]
		obstacles = []

		for label in obstacle_labels :
			input_file.readline()

			oid = int((input_file.readline().split())[1])

			oposition = []
			line_position = (input_file.readline().split())[1:]
			for i in range(0, 3) :
				oposition.append(float(line_position[i]))
			# print "***" + str(oposition)

			osize = float((input_file.readline().split())[1])
			# print "***" + str(osize)

			odisplay_params = []
			for i in range(0, 2) :
				odisplay_params.append(int((input_file.readline().split())[1]))
			# print "***" + str(odisplay_params)

			new_obstacle = Obstacle(oid)
			new_obstacle.load_data(oid, np.array(oposition), osize, odisplay_params)
			obstacles.append( new_obstacle )
			
		self.all_obstacles = obstacles
		input_file.close()
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
	def write_world_datafile( self, export_filename ) :
		output_file = open(str(export_filename), "w")
		print output_file

		wdimensions = ("W_DIMENSIONS"+"\t"+str(self.dimensions[0])+"\t"+
						str(self.dimensions[1])+"\t"+str(self.dimensions[2])+"\n") 
		output_file.write(wdimensions)

		wobstacles = "NB_OBSTACLES" + "\t" + str(self.nb_obstacles)+"\n"
		output_file.write(wobstacles)

		wosizerange = "O_SIZE_RANGE"+"\t"+str(self.os_min)+"\t"+str(self.os_max)+"\n"
		output_file.write(wosizerange)

		obstacle_labels = "ALL_OBSTACLES"+"\t"+"\t".join([str(i) for i in range(1, self.nb_obstacles+1)]) + "\n"
		output_file.write(obstacle_labels)

		for obstacle in self.all_obstacles :
			output_file.write("\n")

			oid = "O_ID"+"\t"+str(obstacle.o_id)+"\n"
			output_file.write(oid)

			print obstacle.position
			oposition = ("POSITION"+"\t"+str(obstacle.position[0])+"\t"+
						str(obstacle.position[1])+"\t"+str(obstacle.position[2])+"\n")
			output_file.write(oposition)

			osize = "SIZE"+"\t"+str(obstacle.size)+"\n"
			output_file.write(osize)

			odisplay_size = "SIZE"+"\t"+str(obstacle.display_size)+"\n"
			odisplay_color_code = "DISPLAY_COLOR_CODE"+"\t"+str(obstacle.display_color_code)+"\n"
			output_file.write(odisplay_size)
			output_file.write(odisplay_color_code) 
		output_file.close()
#-------------------------------------------------------------------------------



#===============================================================================
# CLASS LIVE CREATURES
#===============================================================================
class LiveCreatures :
#-------------------------------------------------------------------------------
	def __init__(self, lc_id, input_filename, physical_world) :
		self.all_populations = {}
		self.all_boids = {}
		
		self.load_population_datafile(input_filename)
		current_id = 1
		for population, nb_boids in (self.all_populations).iteritems() :
			self.all_boids.update({population.p_id : []})
			for i in range(0, nb_boids) :
				new_boid = Boid(current_id, population, (self, physical_world))
				current_id+=1
				self.all_boids[population.p_id].append(new_boid)
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
	def __repr__( self ) :
		return str(self.all_boids)
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
	def load_population_datafile( self, filename ) :
		input_file = open(str(filename), "r")
		population_labels = (input_file.readline().split())[1:]
		populations = {}
		for label in population_labels :
			input_file.readline()

			p_label = (input_file.readline().split())[1]
			pname = (input_file.readline().split())[1]
			pnbagents = int(input_file.readline().replace("\n", "").split("\t")[1])
			pprey_list = (input_file.readline().split())[1:]
			# print "***" + str(pprey_list)
		
			ppredator_list = (input_file.readline().split())[1:]
			# print "***" + str(ppredator_list)
		
			pantagonist_list = (input_file.readline().split())[1:]
			# print "***" + str(pantagonist_list)
		
			pneutral_list = []
			for other_label in population_labels :
				if not(other_label==label or other_label in pprey_list or 
						other_label in ppredator_list or other_label in pantagonist_list) :
					pneutral_list.append(other_label)
			# print "***" + str(pneutral_list)

			pcinetic_params = []
			for i in range(0, 2) :
				pcinetic_params.append(float((input_file.readline().split())[1]))
			# print "***" + str(pcinetic_params)

			pinteraction_coeffs = []
			for i in range(0, 10) :
				pinteraction_coeffs.append(float((input_file.readline().split())[1]))
			# print "***" + str(pinteraction_coeffs)

			pperception_params = []
			for i in range(0, 10) :
				pperception_params.append(float((input_file.readline().split())[1]))
			# print "***" + str(pperception_params)

			pdisplay_params = []
			for i in range(0, 2) :
				pdisplay_params.append(int((input_file.readline().split())[1]))
			# print "***" + str(pdisplay_params)

			new_population = Population(p_label)
			new_population.load_data(p_label, pname, ppredator_list, pprey_list, 
									pantagonist_list, pneutral_list, pcinetic_params, 
									pinteraction_coeffs, pperception_params, pdisplay_params)
			populations.update( {new_population : pnbagents} )
		input_file.close()
		self.all_populations = populations
#-------------------------------------------------------------------------------












#===============================================================================
# CLASS BOID
#===============================================================================


class Boid :
#-------------------------------------------------------------------------------
	def __init__( self, b_id, population, universe):
		# General information
		# Agent ID
		self.b_id = b_id
		# Population the agent belongs to
		self.population = population
		
		# The universe in which this agent exists
		(self.animate_world, self.inanimate_world) = universe
		
		# Current cinetic parameters
		# Position
		xi = np.random.rand()*self.inanimate_world.dimensions[0]
		yi = np.random.rand()*self.inanimate_world.dimensions[1]
		zi = np.random.rand()*self.inanimate_world.dimensions[2]
		self.position = np.array([xi, yi, zi])
		# Instantaneous velocity
		self.velocity = np.random.rand()*self.population.max_speed*np.array([1.0, 1.0, 1.0])
		# Acceleration
		self.acceleration = np.array([0.0, 0.0, 0.0])

		# Current social environment (neighbourhood)
		self.close_predators = dict((predator_label, []) for predator_label in self.population.predator_list)
		self.close_prey = dict((prey_label, []) for prey_label in self.population.prey_list)
		self.close_antagonists = dict((antagonist_label, []) for antagonist_label in self.population.antagonist_list)
		self.close_neutrals = dict((neutral_label, []) for neutral_label in self.population.neutral_list)
		self.close_friends = []

		# Physical obstacles in proximity
		self.close_obstacles = []
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
	# Used to determine whever an animate or inanimate object can be perceived
#-------------------------------------------------------------------------------
	def is_in_proximity( self, point, angle, radius ) :
		point = np.array(point)
		difference_vector = point - self.position
		distance = np.linalg.norm(difference_vector)
		
		if distance > radius :
			return False		
		# Close objects are perceived even if they are behind, 0.1 is arbitrary
		if distance < 0.1*radius :
			return True
		
		# Defining a unit vector oriented along the velocity
		speed = np.linalg.norm(self.velocity)
		epsilon = 0.0001
		if not((speed - 0.0) < epsilon) :
			unit_velocity = self.velocity/float(np.linalg.norm(self.velocity))
			unit_difference = difference_vector/float(np.linalg.norm(difference_vector))
			scalar_product = np.dot(unit_difference, unit_velocity)
			if ( scalar_product > 1.0 ) :
				scalar_product = 1.0
			else :
				if ( scalar_product < -1.0 ) :
					scalar_product = -1.0
			vector_angle = math.acos(scalar_product)
			return math.fabs(vector_angle) < math.fabs(angle)
		else :
			return (distance<=radius)
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
	def find_neighbours( self ) :
		# Resetting values
		self.close_friends = []
		self.close_obstacles = []

		for antagonist_label in self.close_antagonists.keys() :
			self.close_antagonists[antagonist_label] = []
		for neutral_label in self.close_neutrals.keys() :
			self.close_neutrals[neutral_label] = []
		for predator_label in self.close_predators.keys() :
			self.close_predators[predator_label] = []
		for prey_label in self.close_prey.keys() :
			self.close_prey[prey_label] = []

		# Find physical obstacles
		for obstacle in self.inanimate_world.all_obstacles :
			if self.is_in_proximity( obstacle.position, self.population.obstacle_theta, 
							obstacle.size * self.population.obstacle_radius ) : 
				self.close_obstacles.append(obstacle)

		# Find close antagonists
		if len(self.population.antagonist_list) > 0 :
			for antagonist_label in self.population.antagonist_list :
				for antagonist in self.animate_world.all_boids[antagonist_label] :
					if self.is_in_proximity( antagonist.position, self.population.social_theta, 
								self.population.social_radius ) : 
						self.close_antagonists[antagonist_label].append(antagonist)

		# Find close friends
			for friend in self.animate_world.all_boids[self.population.p_id] :
				if (self.is_in_proximity( friend.position, self.population.friend_theta, 
							self.population.friend_radius ) and
					not (friend.b_id == self.b_id) ): 
					self.close_friends.append(friend)

		# Find close neutral agents
		if len(self.population.neutral_list) > 0 :
			for neutral_label in self.population.neutral_list :
				for neutral in self.animate_world.all_boids[neutral_label] :
					if self.is_in_proximity( neutral.position, self.population.social_theta, 
								self.population.social_radius ) : 
						self.close_neutrals[neutral_label].append(neutral)

		# Find close predators
		if len(self.population.predator_list) > 0 :
			for predator_label in self.population.predator_list :
				for predator in self.animate_world.all_boids[predator_label] :
					if self.is_in_proximity( predator.position, self.population.evasion_theta, 
								self.population.evasion_radius ) : 
						self.close_predators[predator_label].append(predator)

		# Find close prey
		if len(self.population.prey_list) > 0 :
			for prey_label in self.population.prey_list :
				for prey in self.animate_world.all_boids[prey_label] :
					if self.is_in_proximity( prey.position, self.population.hunt_theta, 
								self.population.hunt_radius ) : 
						self.close_prey[prey_label].append(prey)
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
	def normalize_vector( self, vector, max_module ) :
		v_module = np.linalg.norm(vector)
		if v_module >= max_module :
			vector=vector*max_module/v_module
		return vector
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
	def rebound( self ) :
		xmax, ymax, zmax = self.inanimate_world.dimensions
		xmin, ymin, zmin = [0.0, 0.0, 0.0]
		
		if self.position[0] > xmax :
			self.position[0] = xmax
			if self.velocity[0] > 0 :
				self.velocity[0] *= -1
		if self.position[0] < xmin :
			self.position[0] = xmin
			if self.velocity[0] < 0 :
				self.velocity[0] *= -1

		if self.position[1] > ymax :
			self.position[1] = ymax
			if self.velocity[1] > 0 :
				self.velocity[1] *= -1

		if self.position[1] < ymin :
			self.position[1] = ymin
			if self.velocity[1] < 0 :
				self.velocity[1] *= -1


		if self.position[2] > zmax :
			self.position[2] = zmax
			if self.velocity[2] > 0 :
				self.velocity[2] *= -1

		if self.position[2] < zmin :
			self.position[2] = zmin
			if self.velocity[2] < 0 :
				self.velocity[2] *= -1

#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
	def avoid_predators( self ) :	# May be optimized : higher priority to the closest one - (chase mode?)
		nb_predators = 0
		distance_vector = np.array([0.0, 0.0, 0.0])
		sum_vector = np.array([0.0, 0.0, 0.0])
		for predator_label, predator_list in self.close_predators.iteritems() :
			for predator in predator_list :
				distance_vector = predator.position - self.position
				distance = np.linalg.norm(distance_vector)
				sum_vector -= distance_vector/distance
				nb_predators+=1
		if nb_predators > 0 :
			sum_vector /= nb_predators
		acceleration = self.population.coeff_predator_avoidance*sum_vector
		#acceleration = normalize_vector(acceleration, self.population.max_acceleration)
		return acceleration
#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
	def chase_prey( self ) :
		distance_vector = np.array([0.0, 0.0, 0.0])
		min_distance = float("inf")
		closest_prey_position = np.array([0.0, 0.0, 0.0])
		
		for prey_label, prey_list in self.close_prey.iteritems() :
			for prey in prey_list :
				distance_vector = prey.position - self.position
				distance = np.linalg.norm(distance_vector)
				if distance < min_distance :
					min_distance = distance
					closest_prey_position = prey.position

		acceleration = self.population.coeff_prey_chase*(closest_prey_position-self.position)
		if min_distance > 0 :
			acceleration/= min_distance
		#acceleration = normalize_vector(acceleration, self.population.max_acceleration)
		return acceleration
#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
	def react_to_neutral( self ) :
		nb_neutral = len(self.close_neutrals)
		distance_vector = np.array([0.0, 0.0, 0.0])
		sum_vector = np.array([0.0, 0.0, 0.0])
		
		for neutral_label, neutral_list in self.close_neutrals.iteritems() :
			for neutral in neutral_list :
				distance_vector = neutral.position - self.position
				sum_vector -= distance_vector
		if nb_neutral > 0 :
			sum_vector /= nb_neutral
		acceleration = self.population.coeff_neutral_separation*sum_vector
		#acceleration = normalize_vector(acceleration, self.population.max_acceleration)
		return acceleration
#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
	def react_to_friends( self ) :
		nb_friends = len(self.close_friends)
		nb_too_close = 0

		distance_vector = np.array([0.0, 0.0, 0.0])
		diff_velocity_vector = np.array([0.0, 0.0, 0.0])

		sum_allignment_vector = np.array([0.0, 0.0, 0.0])
		sum_cohesion_vector = np.array([0.0, 0.0, 0.0])
		sum_separation_vector = np.array([0.0, 0.0, 0.0])
		
		for friend in self.close_friends :
			distance_vector = friend.position - self.position
			diff_velocity_vector = friend.velocity - self.velocity
			
			sum_allignment_vector+=diff_velocity_vector
			sum_cohesion_vector+=distance_vector
			
			if self.is_in_proximity( friend.position, self.population.obstacle_theta, self.population.obstacle_radius) :
				sum_separation_vector -= distance_vector
				nb_too_close+=1


		ac = self.population.coeff_allignment
		cc = self.population.coeff_cohesion
		sc = self.population.coeff_separation
		if nb_friends > 0 :
			sum_allignment_vector/=nb_friends
			sum_cohesion_vector/=nb_friends
		if nb_too_close > 0 :
			sum_separation_vector/=nb_too_close
		sum_vector = ac*sum_allignment_vector + cc*sum_cohesion_vector + sc*sum_separation_vector
		acceleration = self.population.coeff_social*sum_vector
		#acceleration = normalize_vector(acceleration, self.population.max_acceleration)
		return acceleration
#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
	def avoid_obstacles(self) :
		nb_obstacles = len(self.close_obstacles)
		distance_vector = np.array([0.0, 0.0, 0.0])
		sum_vector = np.array([0.0, 0.0, 0.0])

		for obstacle in self.close_obstacles :
			distance_vector = obstacle.position - self.position
			sum_vector -= distance_vector
		if nb_obstacles > 0 :
			sum_vector /= nb_obstacles
		acceleration = self.population.coeff_obstacle_avoidance*sum_vector
		return acceleration
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
	# TO DO !!!!!!!!!!!!!! ALSO ANTAGONISTS
	def advance( self, dt) :
		self.find_neighbours()

		acceleration = (self.avoid_predators() + self.chase_prey() + self.react_to_friends() + 
						self.react_to_neutral() + self.avoid_obstacles())
		self.acceleration = self.normalize_vector(acceleration, self.population.max_acceleration)

		self.velocity += dt*self.acceleration
		self.velocity = self.normalize_vector(self.velocity, self.population.max_speed)
		self.position+=dt*self.velocity
		self.rebound()

#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
	def __repr__( self ) :
		return "B: " + str(self.b_id) +" P: " + str(self.population.p_id) + " position: " + str(self.position) + " velocity: " + str(self.velocity) + "\n"

#-------------------------------------------------------------------------------






import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D

def f_range( start, end, step ) : 
	while start <= end :
		yield start
		start += step



'''
#===============================================================================
# CLASS ANIMATION
#===============================================================================

class AnimatedScatter(object):
	def __init__(self, numpoints=5):

		pw = PhysicalWorld(1, (100, 60, 90), 5, (1, 2))
		lc = LiveCreatures(1, "population.data", pw)

		self.xmin = 0
		self.xmax = 100
		self.ymin = 0
		self.ymax = 60
		self.zmin = 0
		self.zmax = 90

		self.numpoints = numpoints
		self.stream = self.data_stream()

		self.fig = plt.figure()
		self.ax = self.fig.add_subplot(111,projection = '3d')
		self.ani = animation.FuncAnimation(self.fig, self.update, init_func=self.setup_plot, blit=True)

	def setup_plot(self):
		X = next(self.stream)
		c = ['b', 'r', 'g', 'y', 'm']
		self.scat = self.ax.scatter(X[:,0], X[:,1], X[:,2] , c=c, s=1, animated=True)

		self.ax.set_xlim3d(self.xmin, self.xmax)
		self.ax.set_ylim3d(self.ymin, self.ymax)
		self.ax.set_zlim3d(self.zmin, self.zmax)

		return self.scat,

	def data_stream(self):
		data = np.zeros(( self.numpoints , 3 ))
		xyz = data[:,:3]
		while True:
			xyz += 2 * (np.random.random(( self.numpoints,3)) - 0.5)
			yield data

	def update(self, i):
		for population, liste_boids in lc.all_boids.iteritems() :
		for boid in liste_boids :
			boid.advance(dt)

	
	
		data = next(self.stream)
		data = np.transpose(data)

		self.scat._offsets3d = ( np.ma.ravel(data[:,0]) , np.ma.ravel(data[:,0]) , np.ma.ravel(data[:,0]) )

		plt.draw()
		return self.scat,

	def show(self):
		plt.show()

if __name__ == '__main__':
	a = AnimatedScatter()
	a.show()





'''














def simulation (t_final, dt) :
	pw = PhysicalWorld(1, (50, 60, 10), 5, (1, 2))
	pw.write_world_datafile("pc.data")
	pw.load_world_datafile("pc.data")
	lc = LiveCreatures(1, "population.data", pw)
	print lc.all_populations
	print lc.all_boids
	
	for t in f_range(0, t_final, dt) :
		for population, liste_boids in lc.all_boids.iteritems() :
			for boid in liste_boids :
				boid.advance(dt)
				print boid
		print "*****************************************************************"


print "Hello world"
simulation(100, 0.1)
