#!/usr/bin/env python3

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np

# Test simple 3D visualization
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Draw a single cube
vertices = [
    [0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0],  # bottom face
    [0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1]   # top face
]

faces = [
    [vertices[0], vertices[1], vertices[5], vertices[4]],  # front face
    [vertices[1], vertices[2], vertices[6], vertices[5]],  # right face  
    [vertices[2], vertices[3], vertices[7], vertices[6]],  # back face
    [vertices[3], vertices[0], vertices[4], vertices[7]],  # left face
    [vertices[4], vertices[5], vertices[6], vertices[7]],  # top face
    [vertices[0], vertices[3], vertices[2], vertices[1]]   # bottom face
]

cube = Poly3DCollection(faces, facecolors='cyan', edgecolors='black', alpha=0.7)
ax.add_collection3d(cube)

ax.set_xlim(0, 2)
ax.set_ylim(0, 2) 
ax.set_zlim(0, 2)

print("Test 3D visualization successful")