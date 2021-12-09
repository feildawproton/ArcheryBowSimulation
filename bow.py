import numpy as np

def create_bow():
	L_brace 	= 1/3					#brace height
	bracepoint	= (0.0, 0.0)			#the nocking point at brace

	o_topLimb = [-L_brace, 0]
	'''
	p_topLimb = [[0.0, 0.0],
				[0.0, .25],
				[0.0, 0.5],
				[0.0, 0.75],
				[0.0, 1.0],
				[0.0, 1.25],
				[-0.0, 1.5],
				[-0.0, 1.75]]
	K_top = np.array([1, 1, 1, 1, 1, 1, 1, 1])
	
	p_topLimb = [[0.0, 0.0],
				[0.0, .25],
				[0.0, 0.5],
				[0.0, 0.75],
				[0.0, 1.0],
				[0.0, 1.25],
				[-0.0, 1.5],
				[-0.0, 1.75]]
	K_top = np.array([2, 1.75, 1.5, 1.25, 1, 1, 1, 1])
	'''
	p_topLimb = [[0.0, 0.0],
				[0.0, .25],
				[0.0, 0.5],
				[0.0, 0.75],
				[0.0, 1.0],
				[0.0, 1.25],
				[-0.075, 1.5],
				[-0.125, 1.6]]
	K_top = np.array([1, 1, 1, 1, 1, 1, 1, 1])
	'''
	p_topLimb = [[0.0, 0.0],
				[0.0, .25],
				[0.0, 0.5],
				[0.0, 0.75],
				[0.0, 1.0],
				[0.0, 1.25],
				[-0.1, 1.5],
				[-0.2, 1.6]]
	K_top = np.array([1, 1, 1, 1, 1, 1, 1, 1])
	
	p_topLimb = [[0.0, 0.0],
				[0.01, .25],
				[0.02, 0.5],
				[0.03, 0.75],
				[0.04, 1.0],
				[0.03, 1.25],
				[0.01, 1.5],
				[-0.02, 1.75]]
	K_top = np.array([1, 1, 1, 1, 1, 1, 1, 1])
	'''
	o_bottomLimb = o_topLimb
	p_bottomLimb = np.copy(p_topLimb)  #copy just in case
	p_bottomLimb = np.multiply(p_bottomLimb, (1, -1))
	K_bottom = np.copy(K_top)

	P_top_global = np.add(p_topLimb, o_topLimb)
	P_bottom_global = np.add(p_bottomLimb, o_bottomLimb)
	
	return {"P_top_global_unbraced": P_top_global, "K_top": K_top, "P_bottom_global_unbraced" : P_bottom_global, "K_bottom": K_bottom, "bracepoint": bracepoint}