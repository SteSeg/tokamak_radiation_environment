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

materials = openmc.Materials(
    [dt_plasma, flibe, wc, eurofer, ss304, nb3sn, fiberglass, ss316L])

# %%

# geometry

# boundary surfaces
angle = (-10, 10)

# components

# core
plasma, sol, vacuum_vessel, blanket, shield = tre.components.core_group(
    plasma_outer_nodes=cn.plasma_out, plasma_material=dt_plasma,
    vessel_inner_nodes=cn.vessel_in, vessel_thickness=5., vessel_material=eurofer,
    blanket_thickness=55, blanket_material=flibe,
    shield_thickness=30, shield_material=ss304,
    angle=angle)

# tf coil
tf_coil_magnet, tf_coil_insulation, tf_coil_case = tre.components.tfcoil_group(
    magnet_inner_nodes=cn.tf_in, magnet_thickness=22, magnet_material=nb3sn,
    insulation_thickness=14, insulation_material=fiberglass,
    case_thickness=14, case_material=ss316L,
    angle=angle)

# pf coils
# u1
pf_u1_magnet, pf_u1_insulation, pf_u1_case = tre.components.pfcoil_group(
    magnet_nodes=cn.pf_u1, magnet_material=nb3sn,
    insulation_thickness=10, insulation_material=fiberglass,
    case_thickness=10, case_material=ss316L,
    angle=angle)

# u2
pf_u2_magnet, pf_u2_insulation, pf_u2_case = tre.components.pfcoil_group(
    magnet_nodes=cn.pf_u2, magnet_material=nb3sn,
    insulation_thickness=10, insulation_material=fiberglass,
    case_thickness=10, case_material=ss316L,
    angle=angle)

# u3
pf_u3_magnet, pf_u3_insulation, pf_u3_case = tre.components.pfcoil_group(
    magnet_nodes=cn.pf_u3, magnet_material=nb3sn,
    insulation_thickness=14, insulation_material=fiberglass,
    case_thickness=14, case_material=ss316L,
    angle=angle)

# l1
pf_l1_magnet, pf_l1_insulation, pf_l1_case = tre.components.pfcoil_group(
    magnet_nodes=cn.pf_l1, magnet_material=nb3sn,
    insulation_thickness=10, insulation_material=fiberglass,
    case_thickness=10, case_material=ss316L,
    angle=angle)

# l2
pf_l2_magnet, pf_l2_insulation, pf_l2_case = tre.components.pfcoil_group(
    magnet_nodes=cn.pf_l2, magnet_material=nb3sn,
    insulation_thickness=10, insulation_material=fiberglass,
    case_thickness=10, case_material=ss316L,
    angle=angle)

# l3
pf_l3_magnet, pf_l3_insulation, pf_l3_case = tre.components.pfcoil_group(
    magnet_nodes=cn.pf_l3, magnet_material=nb3sn,
    insulation_thickness=14, insulation_material=fiberglass,
    case_thickness=14, case_material=ss316L,
    angle=angle)

# central solenoid
# u1
cs_u1_magnet, cs_u1_insulation, cs_u1_case = tre.components.pfcoil_group(
    magnet_nodes=cn.cs_u1, magnet_material=nb3sn,
    insulation_thickness=10, insulation_material=fiberglass,
    case_thickness=10, case_material=ss316L,
    angle=angle)

# u2
cs_u2_magnet, cs_u2_insulation, cs_u2_case = tre.components.pfcoil_group(
    magnet_nodes=cn.cs_u2, magnet_material=nb3sn,
    insulation_thickness=10, insulation_material=fiberglass,
    case_thickness=10, case_material=ss316L,
    angle=angle)

# u3
cs_u3_magnet, cs_u3_insulation, cs_u3_case = tre.components.pfcoil_group(
    magnet_nodes=cn.cs_u3, magnet_material=nb3sn,
    insulation_thickness=10, insulation_material=fiberglass,
    case_thickness=10, case_material=ss316L,
    angle=angle)

# l1
cs_l1_magnet, cs_l1_insulation, cs_l1_case = tre.components.pfcoil_group(
    magnet_nodes=cn.cs_l1, magnet_material=nb3sn,
    insulation_thickness=10, insulation_material=fiberglass,
    case_thickness=10, case_material=ss316L,
    angle=angle)

# l2
cs_l2_magnet, cs_l2_insulation, cs_l2_case = tre.components.pfcoil_group(
    magnet_nodes=cn.cs_l2, magnet_material=nb3sn,
    insulation_thickness=10, insulation_material=fiberglass,
    case_thickness=10, case_material=ss316L,
    angle=angle)

# l3
cs_l3_magnet, cs_l3_insulation, cs_l3_case = tre.components.pfcoil_group(
    magnet_nodes=cn.cs_l3, magnet_material=nb3sn,
    insulation_thickness=10, insulation_material=fiberglass,
    case_thickness=10, case_material=ss316L,
    angle=angle)


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
settings = openmc.Settings(run_mode='fixed source')
settings.photon_transport = False
settings.source = source
settings.batches = 100
settings.particles = int(1e6)
settings.output = {'tallies': False}

# %%

# filters
particle_filter = openmc.ParticleFilter(
    ['neutron', 'photon', 'electron', 'positron'])

# mesh
# regular mesh
mesh = openmc.RegularMesh()
mesh.dimension = [175, 66, 140]
mesh.lower_left = [122, -165, -700]
mesh.upper_right = [1178, 165, 700]
globalmesh_filter = openmc.MeshFilter(mesh)
# cylindrical mesh
mesh = openmc.CylindricalMesh()
mesh.r_grid = [267, 272]
mesh.z_grid = [-2.5, 2.5]
mesh.phi_grid = (0, math.radians(360))
mesh.origin = (0., 0., 0.)
localmesh_filter = openmc.MeshFilter(mesh)

# energyfilter
tripoli315 = openmc.mgxs.GROUP_STRUCTURES['TRIPOLI-315']
energy_filter = openmc.EnergyFilter(tripoli315)

# tallies
# mesh tally - flux
tally1 = openmc.Tally(tally_id=1, name="nflux_mesh")
tally1.filters = [particle_filter, globalmesh_filter]
tally1.scores = ["flux"]

# mesh tally - heating
tally2 = openmc.Tally(tally_id=2, name="heating_mesh")
tally2.filters = [particle_filter, globalmesh_filter]
tally2.scores = ["heating"]

# mesh tally - gas production
tally3 = openmc.Tally(tally_id=3, name="heating_mesh")
tally3.filters = [globalmesh_filter]
tally3.scores = ["H1-production", "H2-production", "H3-production",
                 "He3-production", "He4-production"]

# mesh tally - flux
tally4 = openmc.Tally(tally_id=4, name="nflux_mesh_spectrum")
tally4.filters = [particle_filter, localmesh_filter, energy_filter]
tally4.scores = ["flux"]

tallies = openmc.Tallies([tally1, tally2, tally3, tally4])


# %%

model = openmc.Model(materials=materials, geometry=geometry,
                     settings=settings, tallies=tallies)

model.export_to_model_xml()

# model.run(threads=12)
