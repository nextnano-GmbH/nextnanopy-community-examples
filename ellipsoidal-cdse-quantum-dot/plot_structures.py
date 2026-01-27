"""
nextnanopy: 1.0.3
nextnano++: 2.3.9
"""

import nextnanopy as nn
import pyvista as pv
import numpy as np
import os
import matplotlib.pyplot as plt
from nextnanopy.utils.plotting import NXT_BLUE_COLORMAP, NXT_COLORMAP, NXT_BLUE, GREEN
from plotting_utils import plot_isosurfaces, plot_isosurfaces_single_color, plot_grid_edges, plot_grid_volume, get_slice_at_x

ISO_VAL = 0.03  
VMIN = -0.08 # -0.002
VMAX = 0.08  # min and max values for the colormap


path_sphere = r"c:\Users\Heorhii\Documents\nextnano\Output\QD-CdSe-ellipsoidal_zb_II-IV_Ferreira_BJP_2006_3D_elipsoid_0"
path_ellips = r"c:\Users\Heorhii\Documents\nextnano\Output\QD-CdSe-ellipsoidal_zb_II-IV_Ferreira_BJP_2006_3D_elipsoid_1"

dfolder = nn.DataFolder(path_sphere)

material_path = dfolder.go_to("Structure", "materials.fld")
df_material_sphere = nn.DataFile(material_path)

dfolder = nn.DataFolder(path_ellips)
material_path = dfolder.go_to("Structure", "materials.fld")
df_material_ellips = nn.DataFile(material_path)






off_screen = True  # `True` to save, 'False' to display
plotter = pv.Plotter(shape=(1, 2), off_screen=off_screen, window_size=(1024, 600))  # Create a Plotter with a grid of 1x2 subplots

# plotter.camera_position = CAMERA_POSITION





plotter.subplot(0, 0)  # Set the current subplot to the first one
plot_isosurfaces_single_color(df_material_sphere, plotter, isosurfaces=[208], opacity=1.0)
plot_grid_edges(df_material_sphere, plotter, color="black", line_width=2)  # edges of the sim region
plot_grid_volume(df_material_sphere, plotter, color="grey", opacity=0.05)  # fill in the space with grey background

plotter.show_axes()
plotter.camera.zoom(0.9)
plotter.render()  # Update the plot with the new camera position

plotter.subplot(0, 1)  # Set the current subplot to the second one
plot_isosurfaces_single_color(df_material_ellips, plotter, isosurfaces=[208], opacity=1.0)
plot_grid_edges(df_material_ellips, plotter, color="black", line_width=2)  # edges of the sim region
plot_grid_volume(df_material_ellips, plotter, color="grey", opacity=0.05)
    # Show the plot interactively
# plotter.screenshot("pyramid/3D_pyramid_dot.png")  # Save the plot as a PNG file
# plotter.camera_position = CAMERA_POSITION
# plotter.camera.zoom(2.0)
# plotter.render()  # Update the plot with the new camera position
# plotter.screenshot("pyramid/3D_pyramid_dot_zoom.png")  # Save the plot as a PNG file

if off_screen:
    plotter.screenshot("tu_QD-CdSe-ellipsoidal_zb_II-IV_Ferreira_BJP_2006_3D_shape.png")  # Save the plot as a PNG file
else:   
    plotter.show() 

print(plotter.camera)
print(plotter.camera.zoom)