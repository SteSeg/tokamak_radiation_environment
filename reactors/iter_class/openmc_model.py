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

nb3sn = tre.materials.nb3sn
fiberglass = tre.materials.fiberglass
hastelloy = tre.materials.hastelloy_c276

materials = openmc.Materials(
    [dt_plasma, flibe, wc, eurofer, ss304, nb3sn, fiberglass, hastelloy])

materials.export_to_xml()

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
    nodes=cn._tf_in, thickness=25, material=nb3sn)
tf_coil_insulation = tre.components.TFCoilInsulation(
    tf_coil_magnet=tf_coil_magnet, thickness=18, material=fiberglass)
tf_coil_case = tre.components.TFCoilCase(
    tf_coil_magnet=tf_coil_magnet, tf_coil_insulation=tf_coil_insulation, thickness=18, material=hastelloy)

# pf coils
pf_u1_magnet = tre.components.PFCoilMagnet(centroid=[
                                           1130, 210], height=30, radial_thickness=30, material=nb3sn, boundary_1=reflective_lower, boundary_2=reflective_upper)
pf_u1_insulation = tre.components.PFCoilInsulation(
    pf_coil_magnet=pf_u1_magnet, thickness=10, material=fiberglass, boundary_1=reflective_lower, boundary_2=reflective_upper)
pf_u1_case = tre.components.PFCoilCase(pf_coil_magnet=pf_u1_magnet, pf_coil_insulation=pf_u1_insulation,
                                       thickness=10, material=hastelloy, boundary_1=reflective_lower, boundary_2=reflective_upper)

pf_u2_magnet = tre.components.PFCoilMagnet(centroid=[
                                           870, 580], height=21, radial_thickness=24, material=nb3sn, boundary_1=reflective_lower, boundary_2=reflective_upper)
pf_u2_insulation = tre.components.PFCoilInsulation(
    pf_coil_magnet=pf_u2_magnet, thickness=10, material=fiberglass, boundary_1=reflective_lower, boundary_2=reflective_upper)
pf_u2_case = tre.components.PFCoilCase(pf_coil_magnet=pf_u2_magnet, pf_coil_insulation=pf_u2_insulation,
                                       thickness=10, material=hastelloy, boundary_1=reflective_lower, boundary_2=reflective_upper)


pf_u3_magnet = tre.components.PFCoilMagnet(centroid=[
                                           400, 650], height=40, radial_thickness=45, material=nb3sn, boundary_1=reflective_lower, boundary_2=reflective_upper)
pf_u3_insulation = tre.components.PFCoilInsulation(
    pf_coil_magnet=pf_u3_magnet, thickness=14, material=fiberglass, boundary_1=reflective_lower, boundary_2=reflective_upper)
pf_u3_case = tre.components.PFCoilCase(pf_coil_magnet=pf_u3_magnet, pf_coil_insulation=pf_u3_insulation,
                                       thickness=14, material=hastelloy, boundary_1=reflective_lower, boundary_2=reflective_upper)

pf_l1_magnet = tre.components.PFCoilMagnet(centroid=[
                                           1130, -210], height=30, radial_thickness=30, material=nb3sn, boundary_1=reflective_lower, boundary_2=reflective_upper)
pf_l1_insulation = tre.components.PFCoilInsulation(
    pf_coil_magnet=pf_l1_magnet, thickness=10, material=fiberglass, boundary_1=reflective_lower, boundary_2=reflective_upper)
pf_l1_case = tre.components.PFCoilCase(pf_coil_magnet=pf_l1_magnet, pf_coil_insulation=pf_l1_insulation,
                                       thickness=10, material=hastelloy, boundary_1=reflective_lower, boundary_2=reflective_upper)

pf_l2_magnet = tre.components.PFCoilMagnet(centroid=[
                                           870, -580], height=21, radial_thickness=24, material=nb3sn, boundary_1=reflective_lower, boundary_2=reflective_upper)
pf_l2_insulation = tre.components.PFCoilInsulation(
    pf_coil_magnet=pf_l2_magnet, thickness=10, material=fiberglass, boundary_1=reflective_lower, boundary_2=reflective_upper)
pf_l2_case = tre.components.PFCoilCase(pf_coil_magnet=pf_l2_magnet, pf_coil_insulation=pf_l2_insulation,
                                       thickness=10, material=hastelloy, boundary_1=reflective_lower, boundary_2=reflective_upper)

pf_l3_magnet = tre.components.PFCoilMagnet(centroid=[
                                           400, -650], height=40, radial_thickness=45, material=nb3sn, boundary_1=reflective_lower, boundary_2=reflective_upper)
pf_l3_insulation = tre.components.PFCoilInsulation(
    pf_coil_magnet=pf_l3_magnet, thickness=14, material=fiberglass, boundary_1=reflective_lower, boundary_2=reflective_upper)
pf_l3_case = tre.components.PFCoilCase(pf_coil_magnet=pf_l3_magnet, pf_coil_insulation=pf_l3_insulation,
                                       thickness=14, material=hastelloy, boundary_1=reflective_lower, boundary_2=reflective_upper)

reactor_components = [plasma, sol, vacuum_vessel, blanket,
                      shield, pf_u1_magnet, pf_u1_insulation, pf_u1_case, pf_u2_magnet, pf_u2_insulation, pf_u2_case, pf_u3_magnet, pf_u3_insulation, pf_u3_case,
                      pf_l1_magnet, pf_l1_insulation, pf_l1_case, pf_l2_magnet, pf_l2_insulation, pf_l2_case, pf_l3_magnet, pf_l3_insulation, pf_l3_case,
                      tf_coil_magnet, tf_coil_insulation, tf_coil_case]

# building enclosure
enclosure_surf = openmc.Sphere(r=5000, boundary_type='vacuum')
enclosure_region = -enclosure_surf
for rc in reactor_components:
    enclosure_region = enclosure_region & ~(rc.region)
enclosure_cell = openmc.Cell(region=enclosure_region, fill=None)

# surfaces

geometry = openmc.Geometry(root=[plasma.cell, vacuum_vessel.cell, sol.cell,
                           blanket.cell, shield.cell, pf_u1_magnet.cell, pf_u1_insulation.cell,
                           pf_u1_case.cell, pf_u2_magnet.cell, pf_u2_insulation.cell, pf_u2_case.cell,
                           pf_u3_magnet.cell, pf_u3_insulation.cell, pf_u3_case.cell, pf_l1_magnet.cell,
                           pf_l1_insulation.cell, pf_l1_case.cell, pf_l2_magnet.cell, pf_l2_insulation.cell,
                           pf_l2_case.cell, pf_l3_magnet.cell, pf_l3_insulation.cell, pf_l3_case.cell,
                           tf_coil_magnet.cell, tf_coil_insulation.cell, tf_coil_case.cell,
                           enclosure_cell])

geometry.merge_surfaces = True

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
