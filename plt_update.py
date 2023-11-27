import matplotlib.pyplot as plt 
import numpy as np 

class Immediate_Plotter(object):
    def __init__(self):
        plt.ion()                          # interactive mode
        self.fig = plt.figure()
        self.ax  = self.fig.add_subplot(1,1,1)
    def __del__(self):
        plt.close(self.fig)
    def draw(self, track_list: list):
        self.ax.clear()
        for track in track_list:
            self.ax.plot(track[:,0], track[:,1], color='r')
            circle = plt.Circle((track[-1,0], track[-1,1]), 0.01, color='r', fill=False)
            self.ax.add_patch(circle)
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

if __name__ == "__main__":
    import random
    im_pltr = Immediate_Plotter()
    
    frames = 100
    print("plotting for", frames, "frames")

    for frame in range(frames):
        track_list = []
        for trck_ndx in range(random.randint(1,10)):
                track = np.random.rand(random.randint(1,10), 2)  # shape = (time, xy)
                track_list.append(track)
        print("Plotting", len(track_list), "tracks")
        im_pltr.draw(track_list = track_list)

    print("done i guess")

'''
x = np.linspace(0, 10*np.pi, 100) 
y = np.sin(x) 
  
plt.ion() 
fig = plt.figure() 
ax = fig.add_subplot(111) 
line1, = ax.plot(x, y, 'b-') 
  
for phase in np.linspace(0, 10*np.pi, 100): 
    line1.set_ydata(np.sin(0.5 * x + phase)) 
    fig.canvas.draw() 
    fig.canvas.flush_events() 
'''
