# %%
import openmc
import math
import components_nodes as cn
import tokamak_radiation_environment as tre
# %%
# define materials

dt_plasma = tre.materials.dt_plasma
eurofer = tre.materials.eurofer97
flibe = tre.materials.flibe
ss304 = tre.materials.ss304
b4c = tre.materials.b4c
wc = tre.materials.wc

materials = openmc.Materials([dt_plasma, flibe, wc, eurofer, ss304])

materials.export_to_xml()

# %%

# geometry

# boundary surfaces
reflective_lower = openmc.YPlane(y0=0, boundary_type='reflective').rotate([
    0, 0, -10])  # -10 degrees
reflective_upper = openmc.YPlane(y0=0, boundary_type='reflective').rotate([
    0, 0, 10])  # +10 degress

# components
plasma = tre.components.Plasma(
    nodes=cn.plasma_out, material=dt_plasma, boundary_1=reflective_lower, boundary_2=reflective_upper)
vacuum_vessel = tre.components.VacuumVessel(
    nodes=cn.vessel_in, thickness=5, material=eurofer, boundary_1=reflective_lower, boundary_2=reflective_upper)
sol = tre.components.SOLVacuum(plasma=plasma, vacuum_vessel=vacuum_vessel,
                               boundary_1=reflective_lower, boundary_2=reflective_upper)
blanket = tre.components.Blanket(vacuum_vessel=vacuum_vessel, thickness=55,
                                 material=flibe, boundary_1=reflective_lower, boundary_2=reflective_upper)
shield = tre.components.Shield(blanket=blanket, thickness=30, material=ss304,
                               boundary_1=reflective_lower, boundary_2=reflective_upper)

reactor_components = [plasma, sol, vacuum_vessel, blanket, shield]

# building enclosure
enclosure_surf = openmc.Sphere(r=1000, boundary_type='vacuum')
enclosure_region = -enclosure_surf
for rc in reactor_components:
    enclosure_region = enclosure_region & ~(rc.region)
enclosure_cell = openmc.Cell(region=enclosure_region, fill=None)

# surfaces

geometry = openmc.Geometry(
    [plasma.cell, vacuum_vessel.cell, sol.cell, blanket.cell, shield.cell, enclosure_cell])

geometry.export_to_xml()


# %%

# %%
# settings

settings = openmc.Settings()

settings.photon_transport = False
settings.run_mode = 'fixed source'
# source definition
source = openmc.Source()
source.particle = 'neutron'
radius = openmc.stats.Discrete([620], [1])
z_values = openmc.stats.Discrete([0], [1])
angle = openmc.stats.Uniform(a=math.radians(0), b=math.radians(360))
source.space = openmc.stats.CylindricalIndependent(
    r=radius, phi=angle, z=z_values, origin=(0., 0., 0.))
source.angle = openmc.stats.Isotropic()
source.energy = openmc.stats.Discrete(14.1e6, 1)

# settings' settings
# weight windows from wwinp
settings.source = source
settings.survival_biasing = False
settings.batches = 100
settings.particles = int(1e6)
settings.output = {
    'tallies': False,
    'path': 'results'
}

settings.export_to_xml()
