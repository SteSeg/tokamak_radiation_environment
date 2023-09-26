# %%
import openmc
import math
import numpy as np
import components_nodes as cn
import tokamak_radiation_environment as tre
# %%
# define materials

dt_plasma = tre.materials.dt_plasma
eurofer = tre.materials.eurofer97
flibe = tre.materials.flibe
ss304 = tre.materials.ss304
ss316L = tre.materials.ss316L
b4c = tre.materials.b4c
wc = tre.materials.wc

nb3sn = tre.materials.nb3sn
fiberglass = tre.materials.fiberglass
hastelloy = tre.materials.hastelloy_c276

materials = openmc.Materials(
    [dt_plasma, flibe, wc, eurofer, ss304, nb3sn, fiberglass, hastelloy])

# %%

# geometry

# boundary surfaces
reflective_lower = openmc.YPlane(y0=0, boundary_type='reflective').rotate([
    0, 0, -10])  # -10 degrees
reflective_upper = openmc.YPlane(y0=0, boundary_type='reflective').rotate([
    0, 0, 10])  # +10 degress

# components

# core
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

# tf coil
tf_coil_magnet = tre.components.TFCoilMagnet(
    nodes=cn._tf_in, thickness=25, material=nb3sn, boundary_1=reflective_lower, boundary_2=reflective_upper)
tf_coil_insulation = tre.components.TFCoilInsulation(
    tf_coil_magnet=tf_coil_magnet, thickness=18, material=fiberglass, boundary_1=reflective_lower, boundary_2=reflective_upper)
tf_coil_case = tre.components.TFCoilCase(
    tf_coil_magnet=tf_coil_magnet, tf_coil_insulation=tf_coil_insulation, thickness=18, material=ss316L, boundary_1=reflective_lower, boundary_2=reflective_upper)

# pf coils
pf_u1_magnet = tre.components.PFCoilMagnet(centroid=[
                                           1130, 210], height=30, radial_thickness=30, material=nb3sn, boundary_1=reflective_lower, boundary_2=reflective_upper)
pf_u1_insulation = tre.components.PFCoilInsulation(
    pf_coil_magnet=pf_u1_magnet, thickness=10, material=fiberglass, boundary_1=reflective_lower, boundary_2=reflective_upper)
pf_u1_case = tre.components.PFCoilCase(pf_coil_magnet=pf_u1_magnet, pf_coil_insulation=pf_u1_insulation,
                                       thickness=10, material=ss316L, boundary_1=reflective_lower, boundary_2=reflective_upper)

pf_u2_magnet = tre.components.PFCoilMagnet(centroid=[
                                           870, 580], height=21, radial_thickness=24, material=nb3sn, boundary_1=reflective_lower, boundary_2=reflective_upper)
pf_u2_insulation = tre.components.PFCoilInsulation(
    pf_coil_magnet=pf_u2_magnet, thickness=10, material=fiberglass, boundary_1=reflective_lower, boundary_2=reflective_upper)
pf_u2_case = tre.components.PFCoilCase(pf_coil_magnet=pf_u2_magnet, pf_coil_insulation=pf_u2_insulation,
                                       thickness=10, material=ss316L, boundary_1=reflective_lower, boundary_2=reflective_upper)


pf_u3_magnet = tre.components.PFCoilMagnet(centroid=[
                                           400, 650], height=40, radial_thickness=45, material=nb3sn, boundary_1=reflective_lower, boundary_2=reflective_upper)
pf_u3_insulation = tre.components.PFCoilInsulation(
    pf_coil_magnet=pf_u3_magnet, thickness=14, material=fiberglass, boundary_1=reflective_lower, boundary_2=reflective_upper)
pf_u3_case = tre.components.PFCoilCase(pf_coil_magnet=pf_u3_magnet, pf_coil_insulation=pf_u3_insulation,
                                       thickness=14, material=ss316L, boundary_1=reflective_lower, boundary_2=reflective_upper)

pf_l1_magnet = tre.components.PFCoilMagnet(centroid=[
                                           1130, -210], height=30, radial_thickness=30, material=nb3sn, boundary_1=reflective_lower, boundary_2=reflective_upper)
pf_l1_insulation = tre.components.PFCoilInsulation(
    pf_coil_magnet=pf_l1_magnet, thickness=10, material=fiberglass, boundary_1=reflective_lower, boundary_2=reflective_upper)
pf_l1_case = tre.components.PFCoilCase(pf_coil_magnet=pf_l1_magnet, pf_coil_insulation=pf_l1_insulation,
                                       thickness=10, material=ss316L, boundary_1=reflective_lower, boundary_2=reflective_upper)

pf_l2_magnet = tre.components.PFCoilMagnet(centroid=[
                                           870, -580], height=21, radial_thickness=24, material=nb3sn, boundary_1=reflective_lower, boundary_2=reflective_upper)
pf_l2_insulation = tre.components.PFCoilInsulation(
    pf_coil_magnet=pf_l2_magnet, thickness=10, material=fiberglass, boundary_1=reflective_lower, boundary_2=reflective_upper)
pf_l2_case = tre.components.PFCoilCase(pf_coil_magnet=pf_l2_magnet, pf_coil_insulation=pf_l2_insulation,
                                       thickness=10, material=ss316L, boundary_1=reflective_lower, boundary_2=reflective_upper)

pf_l3_magnet = tre.components.PFCoilMagnet(centroid=[
                                           400, -650], height=40, radial_thickness=45, material=nb3sn, boundary_1=reflective_lower, boundary_2=reflective_upper)
pf_l3_insulation = tre.components.PFCoilInsulation(
    pf_coil_magnet=pf_l3_magnet, thickness=14, material=fiberglass, boundary_1=reflective_lower, boundary_2=reflective_upper)
pf_l3_case = tre.components.PFCoilCase(pf_coil_magnet=pf_l3_magnet, pf_coil_insulation=pf_l3_insulation,
                                       thickness=14, material=ss316L, boundary_1=reflective_lower, boundary_2=reflective_upper)


# central solenoid
cs_u1_magnet = tre.components.PFCoilMagnet(centroid=[
                                           167, 100], height=160, radial_thickness=40, material=nb3sn, boundary_1=reflective_lower, boundary_2=reflective_upper)
cs_u1_insulation = tre.components.PFCoilInsulation(
    pf_coil_magnet=cs_u1_magnet, thickness=10, material=fiberglass, boundary_1=reflective_lower, boundary_2=reflective_upper)
cs_u1_case = tre.components.PFCoilCase(pf_coil_magnet=cs_u1_magnet, pf_coil_insulation=cs_u1_insulation,
                                       thickness=10, material=ss316L, boundary_1=reflective_lower, boundary_2=reflective_upper)

cs_u2_magnet = tre.components.PFCoilMagnet(centroid=[
                                           167, 300], height=160, radial_thickness=40, material=nb3sn, boundary_1=reflective_lower, boundary_2=reflective_upper)
cs_u2_insulation = tre.components.PFCoilInsulation(
    pf_coil_magnet=cs_u2_magnet, thickness=10, material=fiberglass, boundary_1=reflective_lower, boundary_2=reflective_upper)
cs_u2_case = tre.components.PFCoilCase(pf_coil_magnet=cs_u2_magnet, pf_coil_insulation=cs_u2_insulation,
                                       thickness=10, material=ss316L, boundary_1=reflective_lower, boundary_2=reflective_upper)

cs_u3_magnet = tre.components.PFCoilMagnet(centroid=[
                                           167, 500], height=160, radial_thickness=40, material=nb3sn, boundary_1=reflective_lower, boundary_2=reflective_upper)
cs_u3_insulation = tre.components.PFCoilInsulation(
    pf_coil_magnet=cs_u3_magnet, thickness=10, material=fiberglass, boundary_1=reflective_lower, boundary_2=reflective_upper)
cs_u3_case = tre.components.PFCoilCase(pf_coil_magnet=cs_u3_magnet, pf_coil_insulation=cs_u3_insulation,
                                       thickness=10, material=ss316L, boundary_1=reflective_lower, boundary_2=reflective_upper)

cs_l1_magnet = tre.components.PFCoilMagnet(centroid=[
                                           167, -100], height=160, radial_thickness=40, material=nb3sn, boundary_1=reflective_lower, boundary_2=reflective_upper)
cs_l1_insulation = tre.components.PFCoilInsulation(
    pf_coil_magnet=cs_l1_magnet, thickness=10, material=fiberglass, boundary_1=reflective_lower, boundary_2=reflective_upper)
cs_l1_case = tre.components.PFCoilCase(pf_coil_magnet=cs_l1_magnet, pf_coil_insulation=cs_l1_insulation,
                                       thickness=10, material=ss316L, boundary_1=reflective_lower, boundary_2=reflective_upper)

cs_l2_magnet = tre.components.PFCoilMagnet(centroid=[
                                           167, -300], height=160, radial_thickness=40, material=nb3sn, boundary_1=reflective_lower, boundary_2=reflective_upper)
cs_l2_insulation = tre.components.PFCoilInsulation(
    pf_coil_magnet=cs_l2_magnet, thickness=10, material=fiberglass, boundary_1=reflective_lower, boundary_2=reflective_upper)
cs_l2_case = tre.components.PFCoilCase(pf_coil_magnet=cs_l2_magnet, pf_coil_insulation=cs_l2_insulation,
                                       thickness=10, material=ss316L, boundary_1=reflective_lower, boundary_2=reflective_upper)

cs_l3_magnet = tre.components.PFCoilMagnet(centroid=[
                                           167, -500], height=160, radial_thickness=40, material=nb3sn, boundary_1=reflective_lower, boundary_2=reflective_upper)
cs_l3_insulation = tre.components.PFCoilInsulation(
    pf_coil_magnet=cs_l3_magnet, thickness=10, material=fiberglass, boundary_1=reflective_lower, boundary_2=reflective_upper)
cs_l3_case = tre.components.PFCoilCase(pf_coil_magnet=cs_l3_magnet, pf_coil_insulation=cs_l3_insulation,
                                       thickness=10, material=ss316L, boundary_1=reflective_lower, boundary_2=reflective_upper)


reactor_components = [plasma, sol, vacuum_vessel, blanket, shield,
                      cs_u1_magnet, cs_u1_insulation, cs_u1_case, cs_u2_magnet, cs_u2_insulation, cs_u2_case, cs_u3_magnet, cs_u3_insulation, cs_u3_case,
                      cs_l1_magnet, cs_l1_insulation, cs_l1_case, cs_l2_magnet, cs_l2_insulation, cs_l2_case, cs_l3_magnet, cs_l3_insulation, cs_l3_case,
                      pf_u1_magnet, pf_u1_insulation, pf_u1_case, pf_u2_magnet, pf_u2_insulation, pf_u2_case, pf_u3_magnet, pf_u3_insulation, pf_u3_case,
                      pf_l1_magnet, pf_l1_insulation, pf_l1_case, pf_l2_magnet, pf_l2_insulation, pf_l2_case, pf_l3_magnet, pf_l3_insulation, pf_l3_case,
                      tf_coil_magnet, tf_coil_insulation, tf_coil_case]

# building enclosure
enclosure_surf = openmc.Sphere(r=5000, boundary_type='vacuum')
enclosure_region = -enclosure_surf
for rc in reactor_components:
    enclosure_region = enclosure_region & ~(rc.region)
enclosure_cell = openmc.Cell(region=enclosure_region, fill=None)

# surfaces

root = [plasma.cell, vacuum_vessel.cell, sol.cell, blanket.cell, shield.cell,
        cs_u1_magnet.cell, cs_u1_insulation.cell, cs_u1_case.cell, cs_u2_magnet.cell, cs_u2_insulation.cell, cs_u2_case.cell,
        cs_u3_magnet.cell, cs_u3_insulation.cell, cs_u3_case.cell, cs_l1_magnet.cell, cs_l1_insulation.cell, cs_l1_case.cell,
        cs_l2_magnet.cell, cs_l2_insulation.cell, cs_l2_case.cell, cs_l3_magnet.cell, cs_l3_insulation.cell, cs_l3_case.cell,
        pf_u1_magnet.cell, pf_u1_insulation.cell, pf_u1_case.cell, pf_u2_magnet.cell, pf_u2_insulation.cell, pf_u2_case.cell,
        pf_u3_magnet.cell, pf_u3_insulation.cell, pf_u3_case.cell, pf_l1_magnet.cell, pf_l1_insulation.cell, pf_l1_case.cell,
        pf_l2_magnet.cell, pf_l2_insulation.cell, pf_l2_case.cell, pf_l3_magnet.cell, pf_l3_insulation.cell, pf_l3_case.cell,
        tf_coil_magnet.cell, tf_coil_insulation.cell, tf_coil_case.cell,
        enclosure_cell]

geometry = openmc.Geometry(root=root)

geometry.merge_surfaces = True

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
angle = openmc.stats.Uniform(a=math.radians(-10), b=math.radians(10))
source.space = openmc.stats.CylindricalIndependent(
    r=radius, phi=angle, z=z_values, origin=(0., 0., 0.))
source.angle = openmc.stats.Isotropic()
source.energy = openmc.stats.muir(e0=14.08e6, m_rat=5, kt=20000)

# settings' settings
settings.source = source
settings.photon_transport = False
settings.batches = 100
settings.particles = int(1e2)
settings.output = {'tallies': False}

# %%

# filters
particle_filter = openmc.ParticleFilter(
    ['neutron', 'photon', 'electron', 'positron'])

# mesh

mesh = openmc.RegularMesh()
mesh.dimension = [175, 66, 140]
mesh.lower_left = [122, -165, -700]
mesh.upper_right = [1178, 165, 700]

# mesh = openmc.CylindricalMesh()
# mesh.r_grid = np.arange(122, 1178, 6)  # 175 steps
# mesh.z_grid = np.arange(-700, 710, 10)  # 140 steps
# mesh.phi_grid = (0, math.radians(360))
# mesh.origin = (0., 0., 0.)
mesh_filter = openmc.MeshFilter(mesh)

# energyfilter
tripoli315 = openmc.mgxs.GROUP_STRUCTURES['TRIPOLI-315']
energy_filter = openmc.EnergyFilter(tripoli315)

# tallies
# mesh tally - flux
tally1 = openmc.Tally(tally_id=1, name="nflux_mesh")
tally1.filters = [particle_filter, mesh_filter]
tally1.scores = ["flux"]

# mesh tally - heating
tally2 = openmc.Tally(tally_id=2, name="heating_mesh")
tally2.filters = [particle_filter, mesh_filter]
tally2.scores = ["heating"]

# mesh tally - gas production
tally3 = openmc.Tally(tally_id=3, name="heating_mesh")
tally3.filters = [mesh_filter]
tally3.scores = ["H1-production", "H2-production", "H3-production"
                 "He3-production", "He4-production"]

tallies = openmc.Tallies([tally1, tally2, tally3])


# %%

model = openmc.Model(materials=materials, geometry=geometry,
                     settings=settings, tallies=tallies)

model.run(threads=12)
