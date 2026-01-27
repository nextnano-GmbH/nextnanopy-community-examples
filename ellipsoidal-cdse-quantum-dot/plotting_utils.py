"""
nextnanopy: 1.0.3
"""

import pyvista as pv
import numpy as np
import nextnanopy as nn
from nextnanopy.utils.plotting import NXT_BLUE
import matplotlib.pyplot as plt

def plot_isosurfaces(dfile, plotter, 
                     isosurfaces: list[float] = None, opacity: float = 0.5, 
                     cmap="viridis", var_name="envelopes", clim=None, var_file_name=None,
                     show_scalar_bar=True, scalar_bar_args=None):
    """Visualize the isosurfaces"""
    if scalar_bar_args is None:
        scalar_bar_args = {}
    x = dfile.coords['x'].value
    y = dfile.coords['y'].value
    z = dfile.coords['z'].value
    X, Y, Z = np.meshgrid(x, y, z, indexing='ij')
    if var_file_name is None:
        var = dfile.variables[0].value
    else:
        var = dfile.variables[var_file_name].value
    

    grid = pv.StructuredGrid(X, Y, Z)
    grid[var_name] = var.flatten(order="F")  # Fortran order


    # plotter.add_mesh(grid.outline(), color='grey') 
    isosurface = grid.contour(isosurfaces=isosurfaces)
    plotter.add_mesh(isosurface, scalars=var_name, opacity=opacity, cmap=cmap, 
                     clim=clim, show_scalar_bar=show_scalar_bar, scalar_bar_args=scalar_bar_args)
    return grid
    
def plot_isosurfaces_single_color(dfile, plotter, isosurfaces: list[float] = None, opacity: float = 0.5, color=NXT_BLUE):
    """Visualize the probabilities of a quantum dot in a cubic structure with a single isosurface."""
    x = dfile.coords['x'].value
    y = dfile.coords['y'].value
    z = dfile.coords['z'].value
    X, Y, Z = np.meshgrid(x, y, z, indexing='ij')
    var = dfile.variables[0].value

    grid = pv.StructuredGrid(X, Y, Z)
    grid["probability"] = var.flatten(order="F")  # Fortran order

    # plotter.add_mesh(grid.outline(), color="blue") # slid outline

    isosurface = grid.contour(isosurfaces=isosurfaces)
    plotter.add_mesh(isosurface, opacity=opacity, color=color)
    return grid

def plot_grid_edges(dfile, plotter, color="black", line_width=2, opacity=1.0):
    """Plot the contour (edges) of a grid"""
    x = dfile.coords['x'].value
    y = dfile.coords['y'].value
    z = dfile.coords['z'].value
    X, Y, Z = np.meshgrid(x, y, z, indexing='ij')
    grid = pv.StructuredGrid(X, Y, Z)
    plotter.add_mesh(grid.outline(), color=color, line_width=line_width) # slid outline

def plot_grid_volume(dfile, plotter, color="grey", opacity=0.05):
    """Plot the volume of a grid"""
    x = dfile.coords['x'].value
    y = dfile.coords['y'].value
    z = dfile.coords['z'].value
    X, Y, Z = np.meshgrid(x, y, z, indexing='ij')
    grid = pv.StructuredGrid(X, Y, Z)
    plotter.add_mesh(grid, opacity=opacity, color=color) # fill in the space with grey background


def get_slice_at_x(dfile, x_slice_pos, var_name=0):
    x = dfile.coords['x'].value
    y = dfile.coords['y'].value
    z = dfile.coords['z'].value
    X, Y, Z = np.meshgrid(x, y, z, indexing='ij')
    ix = np.where(np.abs(x-x_slice_pos)<1e-2)[0][0]
    
    Y, Z = np.meshgrid(y, z, indexing='ij') # for return
    var = dfile.variables[var_name].value
    var_slice= var[ix, :, :]
    print(Y.shape, Z.shape)
    print(var_slice.shape)

    return Y, Z, var_slice


def get_slice_at_y(dfile, y_slice_pos, var_name=0):
    x = dfile.coords['x'].value
    y = dfile.coords['y'].value
    z = dfile.coords['z'].value
    X, Y, Z = np.meshgrid(x, y, z, indexing='ij')
    iy = np.where(np.abs(y-y_slice_pos)<1e-2)[0][0]
    
    X, Z = np.meshgrid(x, z, indexing='ij') # for return
    var = dfile.variables[var_name].value
    var_slice= var[:, iy, :]
    
    return X, Z, var_slice


def get_slice_at_z(dfile, z_slice_pos, var_name=0):
    x = dfile.coords['x'].value
    y = dfile.coords['y'].value
    z = dfile.coords['z'].value
    X, Y, Z = np.meshgrid(x, y, z, indexing='ij')
    iz = np.where(np.abs(z-z_slice_pos)<1e-2)[0][0]
    
    X, Y = np.meshgrid(x, y, indexing='ij') # for return
    var = dfile.variables[var_name].value
    var_slice= var[:, :, iz]
    
    return X, Y, var_slice

def set_up_ybroken_axes(ymin, ybreak_low, ybreak_high, ymax):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6), sharex=True)
    fig.subplots_adjust(hspace=0.05)
    ax2.set_ylim(ymin, ybreak_low)
    ax1.set_ylim(ybreak_high, ymax)

    ax1.spines.bottom.set_visible(False)
    ax2.spines.top.set_visible(False)
    ax1.xaxis.tick_top()
    ax1.tick_params(labeltop=False)  # don't put tick labels at the top
    ax2.xaxis.tick_bottom()

    d = .5  # proportion of vertical to horizontal extent of the slanted line
    kwargs = dict(marker=[(-1, -d), (1, d)], markersize=12,
              linestyle="none", color='k', mec='k', mew=1, clip_on=False)
    ax1.plot([0, 1], [0, 0], transform=ax1.transAxes, **kwargs)
    ax2.plot([0, 1], [1, 1], transform=ax2.transAxes, **kwargs)

    return fig, ax1, ax2


def plot_isovolume_single_color(dfile, plotter, threshold, opacity: float = 0.5, color=NXT_BLUE):
    """Visualize the probabilities of a quantum dot in a cubic structure with a single isosurface."""
    x = dfile.coords['x'].value
    y = dfile.coords['y'].value
    z = dfile.coords['z'].value
    X, Y, Z = np.meshgrid(x, y, z, indexing='ij')
    var = dfile.variables[0].value

    grid = pv.StructuredGrid(X, Y, Z)
    grid["probability"] = var.flatten(order="F")  # Fortran order

    # plotter.add_mesh(grid.outline(), color="blue") # slid outline

    isovolume = grid.threshold(threshold, scalars="probability")
    plotter.add_mesh(isovolume, opacity=opacity, color=color)
    return grid