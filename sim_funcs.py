import numpy as np
import math #for sqrt

# -- Complex number multiplication --
#this is used because I don't use trig functions in this project
#complex number perform rotation quite well
#(a + bi)(c + di)
#ac + adi + bci - bd
#((ac - bd) + (ad + bc)
def mult_complex(c1, c2):
	return (c1[0]*c2[0] - c1[1]*c2[1], c1[0]*c2[1] + c1[1]*c2[0])
	
# -- Simple projection --
#numpy might do but I couldn't find it
def project(a, b):
	numerator = np.dot(a, b)
	denom = np.dot(b, b)
	scaler = numerator/denom
	return np.multiply(b, scaler)
	
# -- Local Translations of the limb segments -- 
#limbs profiles are defined globaly so this is needed for applying rotations
def get_local_trans(profile_global):
	local_vectors = np.zeros((profile_global.shape[0] - 1, profile_global.shape[1]))
	for n, vector in enumerate(local_vectors):
		local = profile_global[n+1] - profile_global[n]
		local_vectors[n] = local		
	return local_vectors
	
# -- Find the point where the sting contacts the limb --
#as best as i can tell, this is the simplest way to find the contact pointing
#calc vectors from the nocking point to each of the discretized limb points
#the point with the lagest x component
def find_string_contact(profile_global, nocking_point):
	nock2limb = np.subtract(profile_global, nocking_point)
	norms = np.linalg.norm(nock2limb, axis = -1)
	norms = np.expand_dims(norms, axis = -1)
	nock2limb = np.divide(nock2limb, norms)
	nock2limb_abs = np.absolute(nock2limb)
	indx = np.argmax(nock2limb[:,0])
	indy = np.argmax(nock2limb_abs[:,1])
	if indx != indy:
		print("derp")
		print(nock2limb)
		print(indx)
		print(indy)
		print("something above went wonky")
	return indx
	
# -- Calculate the stringing force -- 
# take a force and apply it in the same direction as the stringing vector
# this is used to bend the bow into brace or to a certain string length
def calc_string_force_vector(string_vector, force):
	string_norm = np.linalg.norm(string_vector)
	string_vector_normed = np.divide(string_vector, string_norm)
	force_vector = np.multiply(string_vector_normed, force)
	return force_vector
	
# -- Calculate compression and shear forces in the limb --
# these calculation may not be right (need to revisit).  Should we project instead
# vectors point in because I want compression to be position
def calc_comp_shear(profile_global, force_vector, contact_indx, forces):
	for n, elem in enumerate(forces):
		if n >= contact_indx:
			forces[n][0] = np.linalg.norm(force_vector)
			forces[n][1] = 0.0
		else:
			vec = profile_global[n] - profile_global[n+1]
			norm_vec = np.multiply(vec, 1 / np.linalg.norm(vec))
			compression = np.dot(norm_vec, force_vector)
			shear = np.linalg.norm(force_vector) - np.linalg.norm(compression)
			forces[n][0] = compression
			forces[n][1] = shear
	
# -- Calculate the rotational moments --
#set moments to zero if the string is in contact
#really this would be proportional to the tickness of the limb segment 
#The vectors don't point in the same direction as those in the compression calculation
#because I want right hand bending to be positive (as if this were sinTheta)
#need to project onto limb tangent
#np.cross with 2d inputs returns an array of length 1; just the z components 
#not using np.cross might be faster
def calc_rot_moment(profile_global, contact_indx, force_vector, moments):
	contact_point = profile_global[contact_indx]
	for n, moment in enumerate(moments):
		if n >= contact_indx:
			moments[n] = 0
		else:
			'''
			vec = profile_global[i+1] - profile_global[i]
			tangent = np.multiply(vec, 1 / np.linalg.norm(vec))
			joint2contact = np.subtract(profile_global[i], contact_point)
			arm = project(joint2contact, tangent)
			moments[i] = force_vector[0]*arm[1] - force_vector[1]*arm[0] #np.cross(force_vector, arm)
			'''
			arm = np.subtract(profile_global[n], contact_point)
			moments[n] = force_vector[0]*arm[1] - force_vector[1]*arm[0] #np.cross(force_vector, arm)
			#testing
			arm2 = np.subtract(profile_global[n+1], contact_point)
			m2 = force_vector[0]*arm2[1] - force_vector[1]*arm2[0]
			A = np.array( [ [arm[1], - arm[0]], [arm2[1], - arm2[0]] ])
			#print(moments[i], m2)
			#print(A.dot(force_vector))
			if A[0][0]*A[1][1] - A[0][1]*A[1][0] != 0.0:
				A_inv = np.linalg.inv(A)
				f_est = A_inv.dot((moments[n], m2))

# -- Calculate the force that the limbs apply to the string --		
def calc_forces(P_global, moments, stringing_vector, contact_index):
	contact_point = P_global[contact_index]
	sum = 0.0
	for n, P in enumerate(P_global):
		if n < contact_index:
			m = moments[n]
			S = np.divide(stringing_vector, np.linalg.norm(stringing_vector))
			arm = np.subtract(P, contact_point)
			S_cross_arm = arm[1]*S[0] - arm[0]*S[1]
			force = m / S_cross_arm
			sum += force
	return sum / contact_index
								

# -- From the rotation moments calculate the local rotations --
# using Hooke's equation x = F / k
# modified to b = Frot / K where b is the imaginary component of a complex number used for rotation
# in this way as we have a descent approximation for small rotations only
# we shouldn't ever have large rotations.  If we do the script will complain so the failure can be identified
# a = sqrt(1 - bb)
def calc_local_rotations(moments, K, local_rotations):
	if K.shape[0] != moments.shape[0] + 1:
		print("moment and stiffness shape mismatch")
	#local_rotations = np.full((moments.shape[0], 2), (1,0))
	for n, moment in enumerate(moments):
		moment = moment.item() #it's currently an array
		b = moment / K[n]
		if b > 1 or b < -1:
			print("as assumption about small moment is broken")
		a = math.sqrt(1 - b*b)
		local_rotations[n] = (a, b)

# -- Calculate Hierarchical, global rotations --
#Rotations are calculated locally so we need to calculate the global rotations
#later rotations are products of previous rotations
#this function contains a check for the magnitude of the rotation
def calc_global_rotations(local_rotations, global_rotations):
	global_rotations[0] = local_rotations[0]
	n = 1
	while n < local_rotations.shape[0]:
		rot = mult_complex(local_rotations[n], global_rotations[n -1])
		global_rotations[n] = rot
		n += 1
		norm = np.linalg.norm(rot)
		if norm > 1.01 or norm < .99:
			print("rotations are not normalized")
		
# -- Calculate and return the global profile --
#rotations are applied first, then translations
#this is performed hierarchically from the riser to the tip of the limb		
def calc_global_profile(T_local, R_globabl, P_global):
	for n, vec in enumerate(T_local):
		rotated = mult_complex(R_globabl[n], vec)
		new = np.add(rotated, P_global[n])
		P_global[n+1] = new

#def calc_string_length(contact
		