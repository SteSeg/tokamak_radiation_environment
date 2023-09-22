# %%
import openmc
import components_nodes as cn
import tokamak_radiation_environment as tre
# %%
# define materials

flibe = openmc.Material(name='FLiBe')
flibe.add_elements_from_formula('F4Li2Be')
flibe.set_density('g/cm3', 1.94)

wc = openmc.Material(name='WC')
wc.add_element('W', 0.5, percent_type='ao')
wc.add_element('C', 0.5, percent_type='ao')
wc.set_density('g/cm3', 15.63)

b4c = openmc.Material(name='B4C')
b4c.add_element('B', 0.8, percent_type='ao')
b4c.add_element('C', 0.2, percent_type='ao')
b4c.set_density('g/cm3', 2.52)

# https://doi.org/10.1007/s10853-014-8281-5
eurofer = openmc.Material(name='Eurofer')
eurofer.add_element('C', 0.0011, percent_type='wo')
eurofer.add_element('Cr', 0.087, percent_type='wo')
eurofer.add_element('W', 0.01, percent_type='wo')
eurofer.add_element('Ta', 0.001, percent_type='wo')
eurofer.add_element('V', 0.0019, percent_type='wo')
eurofer.add_element('Mn', 0.0044, percent_type='wo')
eurofer.add_element('S', 0.00004, percent_type='wo')
eurofer.add_element('Fe', 0.89456, percent_type='wo')
eurofer.set_density('g/cm3', 7.80)

materials = openmc.Materials([flibe, wc, b4c, eurofer])

materials.export_to_xml()

# %%

# geometry

# surfaces

reflective_lower = openmc.YPlane(
    y0=0, boundary_type='reflective').rotate([0, 0, -10])
reflective_upper = openmc.YPlane(
    y0=0, boundary_type='reflective').rotate([0, 0, 10])

tf_poloidal_lower = openmc.YPlane(y0=-38)
tf_poloidal_upper = openmc.YPlane(y0=38)
tf_right = openmc.XPlane(x0=0)

plasma_out = openmc.model.Polygon(cn.plasma_out, basis='rz')

vessel_in = openmc.model.Polygon(cn.vessel_in, basis='rz')
blanket_in = openmc.model.Polygon(cn.vessel_in, basis='rz').offset(5)
shield_in = openmc.model.Polygon(cn.vessel_in, basis='rz').offset(60)
shield_out = openmc.model.Polygon(cn.vessel_in, basis='rz').offset(90)

# tf_case_in =
# tf_case_out =

tf_in = openmc.model.Polygon(cn.tf_in, basis='rz')
tf_out = openmc.model.Polygon(cn.tf_in, basis='rz').offset(89)

pf_u1_case = openmc.model.Polygon(cn.pf_u1, basis='rz')
pf_u2_case = openmc.model.Polygon(cn.pf_u2, basis='rz')
pf_u3_case = openmc.model.Polygon(cn.pf_u3, basis='rz')
pf_l1_case = openmc.model.Polygon(cn.pf_l1, basis='rz')
pf_l2_case = openmc.model.Polygon(cn.pf_l2, basis='rz')
pf_l3_case = openmc.model.Polygon(cn.pf_l3, basis='rz')

pf_u1_insulation = openmc.model.Polygon(cn.pf_u1, basis='rz').offset(-7)
pf_u2_insulation = openmc.model.Polygon(cn.pf_u2, basis='rz').offset(-7)
pf_u3_insulation = openmc.model.Polygon(cn.pf_u3, basis='rz').offset(-7)
pf_l1_insulation = openmc.model.Polygon(cn.pf_l1, basis='rz').offset(-7)
pf_l2_insulation = openmc.model.Polygon(cn.pf_l2, basis='rz').offset(-7)
pf_l3_insulation = openmc.model.Polygon(cn.pf_l3, basis='rz').offset(-7)

pf_u1_magnet = openmc.model.Polygon(cn.pf_u1, basis='rz').offset(-14)
pf_u2_magnet = openmc.model.Polygon(cn.pf_u2, basis='rz').offset(-14)
pf_u3_magnet = openmc.model.Polygon(cn.pf_u3, basis='rz').offset(-14)
pf_l1_magnet = openmc.model.Polygon(cn.pf_l1, basis='rz').offset(-14)
pf_l2_magnet = openmc.model.Polygon(cn.pf_l2, basis='rz').offset(-14)
pf_l3_magnet = openmc.model.Polygon(cn.pf_l3, basis='rz').offset(-14)

# cs_case_central1 =
# cs_case_u2 =
# cs_case_u3 =
# cs_case_l2 =
# cs_case_l3 =

cs_u1 = openmc.model.Polygon(cn.cs_u1, basis='rz')
cs_u2 = openmc.model.Polygon(cn.cs_u2, basis='rz')
cs_u3 = openmc.model.Polygon(cn.cs_u3, basis='rz')
cs_l1 = openmc.model.Polygon(cn.cs_l1, basis='rz')
cs_l2 = openmc.model.Polygon(cn.cs_l2, basis='rz')
cs_l3 = openmc.model.Polygon(cn.cs_l3, basis='rz')

enclosure = openmc.Sphere(x0=0, y0=0, z0=0, r=1500, boundary_type='vacuum')

# regions
plasma_region = -plasma_out & +reflective_lower & -reflective_upper
sol_region = +plasma_out & -vessel_in & +reflective_lower & -reflective_upper
vessel_region = +vessel_in & -blanket_in & +reflective_lower & -reflective_upper
blanket_region = +blanket_in & -shield_in & +reflective_lower & -reflective_upper
shield_region = +shield_in & -shield_out & +reflective_lower & -reflective_upper

tf_region = +tf_in & -tf_out & +tf_poloidal_lower & -tf_poloidal_upper & +tf_right

pf_u1_case_region = -pf_u1_case & +pf_u1_insulation & + \
    reflective_lower & -reflective_upper
pf_u2_case_region = -pf_u2_case & +pf_u2_insulation & + \
    reflective_lower & -reflective_upper
pf_u3_case_region = -pf_u3_case & +pf_u3_insulation & + \
    reflective_lower & -reflective_upper
pf_l1_case_region = -pf_l1_case & +pf_l1_insulation & + \
    reflective_lower & -reflective_upper
pf_l2_case_region = -pf_l2_case & +pf_l2_insulation & + \
    reflective_lower & -reflective_upper
pf_l3_case_region = -pf_l3_case & +pf_l3_insulation & + \
    reflective_lower & -reflective_upper

pf_u1_insulation_region = -pf_u1_insulation & + \
    pf_u1_magnet & +reflective_lower & -reflective_upper
pf_u2_insulation_region = -pf_u2_insulation & + \
    pf_u2_magnet & +reflective_lower & -reflective_upper
pf_u3_insulation_region = -pf_u3_insulation & + \
    pf_u3_magnet & +reflective_lower & -reflective_upper
pf_l1_insulation_region = -pf_l1_insulation & + \
    pf_l1_magnet & +reflective_lower & -reflective_upper
pf_l2_insulation_region = -pf_l2_insulation & + \
    pf_l2_magnet & +reflective_lower & -reflective_upper
pf_l3_insulation_region = -pf_l3_insulation & + \
    pf_l3_magnet & +reflective_lower & -reflective_upper

pf_u1_magnet_region = -pf_u1_magnet & +reflective_lower & -reflective_upper
pf_u2_magnet_region = -pf_u2_magnet & +reflective_lower & -reflective_upper
pf_u3_magnet_region = -pf_u3_magnet & +reflective_lower & -reflective_upper
pf_l1_magnet_region = -pf_l1_magnet & +reflective_lower & -reflective_upper
pf_l2_magnet_region = -pf_l2_magnet & +reflective_lower & -reflective_upper
pf_l3_magnet_region = -pf_l3_magnet & +reflective_lower & -reflective_upper

cs_u1_region = -cs_u1 & +reflective_lower & -reflective_upper
cs_u2_region = -cs_u2 & +reflective_lower & -reflective_upper
cs_u3_region = -cs_u3 & +reflective_lower & -reflective_upper
cs_l1_region = -cs_l1 & +reflective_lower & -reflective_upper
cs_l2_region = -cs_l2 & +reflective_lower & -reflective_upper
cs_l3_region = -cs_l3 & +reflective_lower & -reflective_upper


enclosure_region = -enclosure & ~(plasma_region | sol_region | vessel_region | blanket_region | shield_region |
                                  tf_region |
                                  pf_u1_case_region | pf_u2_case_region | pf_u3_case_region | pf_l1_case_region | pf_l2_case_region | pf_l3_case_region |
                                  pf_u1_insulation_region | pf_u2_insulation_region | pf_u3_insulation_region | pf_l1_insulation_region | pf_l2_insulation_region | pf_l3_insulation_region |
                                  pf_u1_magnet_region | pf_u2_magnet_region | pf_u3_magnet_region | pf_l1_magnet_region | pf_l2_magnet_region | pf_l3_magnet_region |
                                  cs_u1_region | cs_u2_region | cs_u3_region | cs_l1_region |
                                  cs_l2_region | cs_l3_region)

# cells
plasma_cell = openmc.Cell(region=plasma_region, fill=None)
sol_cell = openmc.Cell(region=sol_region, fill=None)
vessel_cell = openmc.Cell(region=vessel_region, fill=None)
blanket_cell = openmc.Cell(region=blanket_region, fill=None)
shield_cell = openmc.Cell(region=shield_region, fill=None)

tf_cell = openmc.Cell(region=tf_region, fill=None)

pf_u1_case_cell = openmc.Cell(region=pf_u1_case_region, fill=None)
pf_u2_case_cell = openmc.Cell(region=pf_u2_case_region, fill=None)
pf_u3_case_cell = openmc.Cell(region=pf_u3_case_region, fill=None)
pf_l1_case_cell = openmc.Cell(region=pf_l1_case_region, fill=None)
pf_l2_case_cell = openmc.Cell(region=pf_l2_case_region, fill=None)
pf_l3_case_cell = openmc.Cell(region=pf_l3_case_region, fill=None)

pf_u1_insulation_cell = openmc.Cell(region=pf_u1_insulation_region, fill=None)
pf_u2_insulation_cell = openmc.Cell(region=pf_u2_insulation_region, fill=None)
pf_u3_insulation_cell = openmc.Cell(region=pf_u3_insulation_region, fill=None)
pf_l1_insulation_cell = openmc.Cell(region=pf_l1_insulation_region, fill=None)
pf_l2_insulation_cell = openmc.Cell(region=pf_l2_insulation_region, fill=None)
pf_l3_insulation_cell = openmc.Cell(region=pf_l3_insulation_region, fill=None)

pf_u1_magnet_cell = openmc.Cell(region=pf_u1_magnet_region, fill=None)
pf_u2_magnet_cell = openmc.Cell(region=pf_u2_magnet_region, fill=None)
pf_u3_magnet_cell = openmc.Cell(region=pf_u3_magnet_region, fill=None)
pf_l1_magnet_cell = openmc.Cell(region=pf_l1_magnet_region, fill=None)
pf_l2_magnet_cell = openmc.Cell(region=pf_l2_magnet_region, fill=None)
pf_l3_magnet_cell = openmc.Cell(region=pf_l3_magnet_region, fill=None)

cs_u1_cell = openmc.Cell(region=cs_u1_region, fill=None)
cs_u2_cell = openmc.Cell(region=cs_u2_region, fill=None)
cs_u3_cell = openmc.Cell(region=cs_u3_region, fill=None)
cs_l1_cell = openmc.Cell(region=cs_l1_region, fill=None)
cs_l2_cell = openmc.Cell(region=cs_l2_region, fill=None)
cs_l3_cell = openmc.Cell(region=cs_l3_region, fill=None)

enclosure_cell = openmc.Cell(cell_id=999, region=enclosure_region, fill=None)


geometry = openmc.Geometry(
    [plasma_cell, sol_cell, vessel_cell, blanket_cell, shield_cell, tf_cell,
     pf_u1_case_cell, pf_u2_case_cell, pf_u3_case_cell, pf_l1_case_cell, pf_l2_case_cell, pf_l3_case_cell,
     pf_u1_insulation_cell, pf_u2_insulation_cell, pf_u3_insulation_cell, pf_l1_insulation_cell, pf_l2_insulation_cell, pf_l3_insulation_cell,
     pf_u1_magnet_cell, pf_u2_magnet_cell, pf_u3_magnet_cell, pf_l1_magnet_cell, pf_l2_magnet_cell, pf_l3_magnet_cell,
     cs_u1_cell, cs_u2_cell, cs_u3_cell, cs_l1_cell, cs_l2_cell, cs_l3_cell,
     enclosure_cell])

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
