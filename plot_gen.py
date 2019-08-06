import dill
import numpy as np
import numexpr as ne
import matplotlib.pyplot as plt
from matplotlib import animation
from pathos.multiprocessing import ProcessingPool as Pool

func_raw = open('func_plot.pkl','rb')
func = dill.load(func_raw)

x_array = np.linspace(0, 1, 50, endpoint=False)

def func_points_gen(i):
    local = []
    for j in range(len(func[i])):
        local_points = func[i][j](x_array)
        for k in local_points:
            local.append(k)
    print(f'Generated {i+1}/{len(func)} points')
    return local

p = Pool(12)
R = [i for i in range(len(func))]
func_points = p.map(func_points_gen, R)

xlim = (0, 20)
ylim = (0, 6)
x_axis = np.linspace(0, 20, 1000, endpoint=False)

fig = plt.figure()
ax = plt.axes(xlim=xlim, ylim=ylim)

line, = ax.plot([], [], lw=2)

def inite():
    line.set_data([], [])
    return line,

def animate(i):
    x = x_axis
    y = func_points[i]
    line.set_data(x, y)
    return line,

anim = animation.FuncAnimation(fig, animate, init_func=inite, frames=3290, interval=20, blit=True)

anim.save(f'aircraft_model.mp4', fps=30, extra_args=['-vcodec', 'libx264'])

plt.show()