import numpy as np
import matplotlib.pyplot as plt
from sim_funcs import *
from bow import create_bow

def draw_bow(model, x_step = .01, force_step = 0.001, max_opt_iter = 1000):
	# -- CONSTANT --
	T_top_local		= get_local_trans(model["P_top_global_unbraced"])
	T_bottom_local	= get_local_trans(model["P_bottom_global_unbraced"])

	# -- NEED TO TRACK THESE
	R_top_local		= np.copy(model["R_top_local_braced"])
	R_bottom_local	= np.copy(model["R_bottom_local_braced"])
	
	
	# -- Calculate global profile --
	R_top_global	= np.copy(R_top_local)
	R_bottom_global	= np.copy(R_bottom_local)
	calc_global_rotations(R_top_local, R_top_global)
	calc_global_rotations(R_bottom_local, R_bottom_global)
	
	P_top_global	= np.copy(model["P_top_global_unbraced"])
	P_bottom_global	= np.copy(model["P_bottom_global_unbraced"])
	calc_global_profile(T_top_local, R_top_global, P_top_global)
	calc_global_profile(T_bottom_local, R_bottom_global, P_bottom_global)
	
	# -- Calculate Moments --

	contact_top_indx			= find_string_contact(P_top_global, model["bracepoint"])
	contact_bottom_indx			= find_string_contact(P_bottom_global, model["bracepoint"])
	stringing_vector_top		= model["bracepoint"] - P_top_global[contact_top_indx]
	stringing_vector_bottom		= model["bracepoint"] - P_bottom_global[contact_bottom_indx]
	force_top					= calc_string_force_vector(stringing_vector_top, model["f_string"])
	force_bottom				= calc_string_force_vector(stringing_vector_bottom, model["f_string"])
	
	moments_top					= np.zeros((P_top_global.shape[0] - 1, 1))
	moments_bottom				= np.zeros((P_top_global.shape[0] - 1, 1))
	calc_rot_moment(P_top_global, contact_top_indx, force_top, moments_top)
	calc_rot_moment(P_bottom_global, contact_bottom_indx, force_bottom, moments_bottom)
	
	print(model["bracepoint"] - P_top_global[contact_top_indx])
	print(stringing_vector_top)
	f_top = calc_forces(P_top_global, moments_top, stringing_vector_top, contact_top_indx)
	f_bottom = calc_forces(P_bottom_global, moments_bottom, stringing_vector_bottom, contact_bottom_indx)
	f = (f_top + f_bottom) /2
	print(model["f_string"], f)
	force_top		= calc_string_force_vector(stringing_vector_top, model["f_string"])
	force_bottom	= calc_string_force_vector(stringing_vector_bottom, model["f_string"])
	print(force_top, force_bottom)
	force_top		= calc_string_force_vector(stringing_vector_top, f)
	force_bottom	= calc_string_force_vector(stringing_vector_bottom, f)
	print(force_top, force_bottom)
	

def brace_bow(model, force_step = 0.001, max_opt_iter = 1000):
	if len(model["K_top"]) != np.copy(model["P_top_global_unbraced"]).shape[0] or len(model["K_bottom"]) != model["P_bottom_global_unbraced"].shape[0]:
		print("invalid model")

	# -- CONSTANT --
	T_top_local		= get_local_trans(model["P_top_global_unbraced"])
	T_bottom_local	= get_local_trans(model["P_bottom_global_unbraced"])

	# -- NEED TO TRACK THESE
	R_top_local		= np.full((T_top_local.shape[0], 2), (1.0, 0.0))
	R_bottom_local	= np.full((T_bottom_local.shape[0], 2), (1, 0.0))

	# -- Don't need to track these --
	#but I will to reduce memory creation and freeing overhead
	#not sure if this is really a good idea or not
	comp_shear_top		= np.zeros((model["P_top_global_unbraced"].shape[0] - 1, 2))
	comp_shear_bottom	= np.zeros((model["P_bottom_global_unbraced"].shape[0] - 1, 2))
	moments_top			= np.zeros((model["P_top_global_unbraced"].shape[0] - 1, 1))
	moments_bottom		= np.zeros((model["P_bottom_global_unbraced"].shape[0] - 1, 1))
	R_top_global		= np.copy(R_top_local)
	R_bottom_global		= np.copy(R_bottom_local)
	P_top_global		= np.copy(model["P_top_global_unbraced"])
	P_bottom_global		= np.copy(model["P_bottom_global_unbraced"])


	iter = 0
	f_string = 0.0
	contact_top_indx = find_string_contact(P_top_global, model["bracepoint"])

	while P_top_global[contact_top_indx][0] < model["bracepoint"][0] and iter < max_opt_iter:		
		#1.) -- find a stringing vectors to pull the limbs back
		contact_top_indx			= find_string_contact(P_top_global, model["bracepoint"])
		contact_bottom_indx			= find_string_contact(P_bottom_global, model["bracepoint"])
		stringing_vector_top		= model["bracepoint"] - P_top_global[contact_top_indx]
		stringing_vector_bottom		= model["bracepoint"] - P_bottom_global[contact_bottom_indx]
		
		#2.1) -- recalculate forces --
		#in the case that went down do to new contact point or change in leverage
		'''
		f_top = calc_forces(P_top_global, moments_top, stringing_vector_top, contact_top_indx)
		f_bottom = calc_forces(P_bottom_global, moments_bottom, stringing_vector_bottom, contact_bottom_indx)
		f = (f_top + f_bottom) /2
		print(f_string, f)'''
				
		#2.2) -- calculate the force we will use to begin to brace the bow
		f_string		= f_string + force_step
		force_top		= calc_string_force_vector(stringing_vector_top, f_string)
		force_bottom	= calc_string_force_vector(stringing_vector_bottom, f_string)
		
		#3.) -- Calculate compression and shear forces
		calc_comp_shear(P_top_global, force_top, contact_top_indx, comp_shear_top)
		calc_comp_shear(P_bottom_global, force_bottom, contact_bottom_indx, comp_shear_bottom)
		
		#4) -- calculate the rotational moments on the bending elements of tf he bow
		calc_rot_moment(P_top_global, contact_top_indx, force_top, moments_top)
		calc_rot_moment(P_bottom_global, contact_bottom_indx, force_bottom, moments_bottom)

		#5.1) -- Calculate local rotations
		calc_local_rotations(moments_top, model["K_top"], R_top_local)
		calc_local_rotations(moments_bottom, model["K_bottom"], R_bottom_local)
		
		#5.2) -- Apply these rotations hierarchically to get global orientations
		calc_global_rotations(R_top_local, R_top_global)
		calc_global_rotations(R_bottom_local, R_bottom_global)

		#5.3) apply these bending momements to update the global profile of the bow
		calc_global_profile(T_top_local, R_top_global, P_top_global)
		calc_global_profile(T_bottom_local, R_bottom_global, P_bottom_global)

		
		#6) -- Updates for stopping conditions	
		iter +=1

	#print(R_top_local)
	#print(R_top_global)

	print("Iterations: %i" % (iter))
	print("String tension: %f" % (f_string))
	
	model["T_top_local"] = T_top_local 
	model["T_bottom_local"] = T_bottom_local 
	model["R_top_local_braced"] = R_top_local 
	model["R_bottom_local_braced"] = R_bottom_local 
	model["f_string"] = f_string
	
	contact_top_indx			= find_string_contact(P_top_global, model["bracepoint"])
	contact_bottom_indx			= find_string_contact(P_bottom_global, model["bracepoint"])
	stringing_vector_top		= model["bracepoint"] - P_top_global[contact_top_indx]
	stringing_vector_bottom		= model["bracepoint"] - P_bottom_global[contact_bottom_indx]
	
	print(model["bracepoint"] - P_top_global[contact_top_indx])
	print(stringing_vector_top)
	f_top = calc_forces(P_top_global, moments_top, stringing_vector_top, contact_top_indx)
	f_bottom = calc_forces(P_bottom_global, moments_bottom, stringing_vector_bottom, contact_bottom_indx)
	f = (f_top + f_bottom) /2
	print(f_string, f)
	force_top		= calc_string_force_vector(stringing_vector_top, f_string)
	force_bottom	= calc_string_force_vector(stringing_vector_bottom, f_string)
	print(force_top, force_bottom)
	force_top		= calc_string_force_vector(stringing_vector_top, f)
	force_bottom	= calc_string_force_vector(stringing_vector_bottom, f)
	print(force_top, force_bottom)


model = create_bow()
brace_bow(model)

print("do the thing")
draw_bow(model)

# -- VISUALIZATION and SUCH -- 
#recalculate the global profile
R_top_global = np.copy(model["R_top_local_braced"])
R_bottom_global = np.copy(model["R_bottom_local_braced"])
calc_global_rotations(model["R_top_local_braced"], R_top_global)
calc_global_rotations(model["R_bottom_local_braced"], R_bottom_global)

P_top_global_braced = np.copy(model["P_top_global_unbraced"])
P_bottom_global_braced = np.copy(model["P_bottom_global_unbraced"])
calc_global_profile(model["T_top_local"], R_top_global, P_top_global_braced)
calc_global_profile(model["T_bottom_local"], R_bottom_global, P_bottom_global_braced)


fig, ax = plt.subplots(nrows = 1, ncols = 2)

#before bracing
ax[0].plot(model["P_top_global_unbraced"][:,0], model["P_top_global_unbraced"][:,1], '-o')
ax[0].plot(model["P_bottom_global_unbraced"][:,0], model["P_bottom_global_unbraced"][:,1], '-o')

#after bracing
ax[0].plot(P_top_global_braced[:,0], P_top_global_braced[:,1], '-o')
ax[0].plot(P_bottom_global_braced[:,0], P_bottom_global_braced[:,1], '-o')

top_contact = P_top_global_braced[find_string_contact(P_top_global_braced, model["bracepoint"])]
bottom_contact = P_bottom_global_braced[find_string_contact(P_bottom_global_braced, model["bracepoint"])]
string = np.array([top_contact, model["bracepoint"], bottom_contact]) 

ax[0].plot(string[:,0], string[:,1], '-o')


plt.show()


