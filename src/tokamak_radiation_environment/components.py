from abc import ABC
import openmc


def _add_boundaries(region, angle):

    if angle:
        _lower_bound = openmc.YPlane(
            y0=0, boundary_type='reflective').rotate([0, 0, angle[0]])
        _upper_bound = openmc.YPlane(
            y0=0, boundary_type='reflective').rotate([0, 0, angle[1]])

        region = region & +(_lower_bound) & -(_upper_bound)

    return region


class Component(ABC):
    """Implement common interface for components"""

    def __init__(self, exclude=True):
        self.exclude = exclude

    def __and__(self, other):
        return openmc.Intersection((self._hull_reg, other))

    def __or__(self, other):
        return openmc.Union((self._hull_reg, other))

    def __invert__(self):
        return ~self._hull_reg


class Plasma(Component):
    def __init__(self, outer_nodes, material: openmc.Material = None, surf_offset=0., angle=None):

        self.outer_nodes = outer_nodes
        self.material = material
        self.surf_offset = surf_offset
        self.angle = angle

    @property
    def surfaces(self):
        main_surf = openmc.model.Polygon(
            self.outer_nodes, basis="rz").offset(self.surf_offset)

        return main_surf

    @property
    def region(self):

        _region = -(self.surfaces)

        _region = _add_boundaries(_region, self.angle)

        return _region

    @property
    def cell(self):

        return openmc.Cell(region=self.region, fill=self.material)


class VacuumVessel(Component):
    def __init__(self, inner_nodes, thickness: float, material: openmc.Material, angle=None):
        super().__init__()

        self.inner_nodes = inner_nodes
        self.thickness = thickness
        self.material = material
        self.angle = angle

    @property
    def surfaces(self):

        inner_surface = openmc.model.Polygon(
            self.inner_nodes, basis="rz")
        outer_surface = openmc.model.Polygon(
            self.inner_nodes, basis="rz").offset(self.thickness)

        return inner_surface, outer_surface

    @property
    def region(self):

        _region = -(self.surfaces[1]) & +(self.surfaces[0])

        _region = _add_boundaries(_region, self.angle)

        return _region

    @property
    def cell(self):

        return openmc.Cell(region=self.region, fill=self.material)


class SOLVacuum(Component):

    def __init__(self, plasma: Plasma, vacuum_vessel: VacuumVessel, material: openmc.Material = None, angle=None):
        super().__init__()

        self.plasma = plasma
        self.vacuum_vessel = vacuum_vessel
        self.material = material
        self.angle = angle

    @property
    def surfaces(self):

        sol_inner_surface = self.plasma.surfaces
        sol_outer_surface = self.vacuum_vessel.surfaces[0]

        return sol_inner_surface, sol_outer_surface

    @property
    def region(self):

        _region = -(self.surfaces[1]) & +(self.surfaces[0])

        _region = _add_boundaries(_region, self.angle)

        return _region

    @property
    def cell(self):

        return openmc.Cell(region=self.region, fill=self.material)


class Blanket(Component):
    def __init__(self, vacuum_vessel: VacuumVessel, thickness: float, material: openmc.Material, nodes=None, angle=None):
        super().__init__()

        self.vacuum_vessel = vacuum_vessel
        self.thickness = thickness
        self.material = material
        self.nodes = nodes
        self.angle = angle

    @property
    def surfaces(self):

        inner_surface = self.vacuum_vessel.surfaces[1]

        if self.nodes:
            outer_surface = openmc.model.Polygon(self.nodes, basis="rz")
        else:
            outer_surface = self.vacuum_vessel.surfaces[1].offset(
                self.thickness)

        return inner_surface, outer_surface

    @property
    def region(self):

        _region = -(self.surfaces[1]) & +(self.surfaces[0])

        _region = _add_boundaries(_region, self.angle)

        return _region

    @property
    def cell(self):
        return openmc.Cell(region=self.region, fill=self.material)


class Shield(Component):
    def __init__(self, blanket: Blanket, thickness: float, material: openmc.Material, nodes=None, angle=None):
        super().__init__()

        self.blanket = blanket
        self.thickness = thickness
        self.material = material
        self.nodes = nodes
        self.angle = angle

    @property
    def surfaces(self):

        inner_surface = self.blanket.surfaces[1]

        if self.nodes:
            outer_surface = openmc.model.Polygon(self.nodes, basis="rz")
        else:
            outer_surface = self.blanket.surfaces[1].offset(
                self.thickness)

        return inner_surface, outer_surface

    @property
    def region(self):

        _region = -(self.surfaces[1]) & +(self.surfaces[0])

        _region = _add_boundaries(_region, self.angle)

        return _region

    @property
    def cell(self):
        return openmc.Cell(region=self.region, fill=self.material)


class PFCoilMagnet(Component):
    def __init__(self, nodes, material: openmc.Material, angle=None):
        super().__init__()

        self.nodes = nodes
        self.material = material
        self.angle = angle

    @property
    def surfaces(self):

        return openmc.model.Polygon(self.nodes, basis="rz")

    @property
    def region(self):
        _region = -(self.surfaces)

        _region = _add_boundaries(_region, self.angle)

        return _region

    @property
    def cell(self):

        return openmc.Cell(region=self.region, fill=self.material)


class PFCoilInsulation(Component):
    def __init__(self, pf_coil_magnet: PFCoilMagnet, thickness: float, material: openmc.Material, angle=None):
        super().__init__()

        self.pf_coil_magnet = pf_coil_magnet
        self.thickness = thickness
        self.material = material
        self.angle = angle

    @property
    def surfaces(self):

        return self.pf_coil_magnet.surfaces.offset(self.thickness)

    @property
    def region(self):

        _region = -(self.surfaces) & ~(self.pf_coil_magnet.region)

        _region = _add_boundaries(_region, self.angle)

        return _region

    @property
    def cell(self):

        return openmc.Cell(region=self.region, fill=self.material)


class PFCoilCase(Component):
    def __init__(self, pf_coil_magnet: PFCoilMagnet, thickness: float, material: openmc.Material, pf_coil_insulation: PFCoilInsulation = None, angle=None):
        super().__init__()

        self.pf_coil_magnet = pf_coil_magnet
        self.pf_coil_insulation = pf_coil_insulation
        self.material = material
        self.thickness = thickness
        self.angle = angle

    @property
    def surfaces(self):

        if self.pf_coil_insulation:
            return self.pf_coil_insulation.surfaces.offset(self.thickness)
        else:
            return self.pf_coil_magnet.surfaces.offset(self.thickness)

    @property
    def region(self):

        _region = -(self.surfaces) & ~(self.pf_coil_magnet.region)

        if self.pf_coil_insulation:
            _region = _region & ~(self.pf_coil_insulation.region)

        _region = _add_boundaries(_region, self.angle)

        return _region

    @property
    def cell(self):

        return openmc.Cell(region=self.region, fill=self.material)


class TFCoilMagnet(Component):
    def __init__(self, inner_nodes, thickness: float, material: openmc.Material, angle=None, rotation_angle: float = 0):
        super().__init__()

        self.inner_nodes = inner_nodes
        self.thickness = thickness
        self.material = material
        self.angle = angle
        self.rotation_angle = rotation_angle

    @property
    def surfaces(self):

        main_surface_in = openmc.model.Polygon(self.inner_nodes, basis="rz")
        main_surface_out = openmc.model.Polygon(
            self.inner_nodes, basis="rz").offset(self.thickness)
        lower_bound = openmc.YPlane(
            y0=-self.thickness).rotate((0, 0, self.rotation_angle))
        upper_bound = openmc.YPlane(y0=self.thickness).rotate(
            (0, 0, self.rotation_angle))
        left_bound = openmc.XPlane(x0=0).rotate((0, 0, self.rotation_angle))

        return main_surface_in, main_surface_out, lower_bound, upper_bound, left_bound

    @property
    def region(self):

        _region = +(self.surfaces[0]) & -(self.surfaces[1]) & + \
            (self.surfaces[2]) & -(self.surfaces[3]) & +(self.surfaces[4])

        _region = _add_boundaries(_region, self.angle)

        return _region

    @property
    def cell(self):

        return openmc.Cell(region=self.region, fill=self.material)


class TFCoilInsulation(Component):
    def __init__(self, tf_coil_magnet: TFCoilMagnet, thickness: float, material: openmc.Material, angle=None):
        super().__init__()

        self.tf_coil_magnet = tf_coil_magnet
        self.thickness = thickness
        self.material = material
        self.angle = angle
        self.rotation_angle = tf_coil_magnet.rotation_angle

    @property
    def surfaces(self):

        lb_y0 = self.tf_coil_magnet.surfaces[2].d - self.thickness
        ub_y0 = self.tf_coil_magnet.surfaces[3].d + self.thickness

        main_surface_in = self.tf_coil_magnet.surfaces[0].offset(
            -self.thickness)
        main_surface_out = self.tf_coil_magnet.surfaces[1].offset(
            +self.thickness)
        lower_bound = openmc.YPlane(y0=lb_y0).rotate(
            (0, 0, self.rotation_angle))
        upper_bound = openmc.YPlane(y0=ub_y0).rotate(
            (0, 0, self.rotation_angle))
        left_bound = openmc.XPlane(x0=0).rotate((0, 0, self.rotation_angle))

        return main_surface_in, main_surface_out, lower_bound, upper_bound, left_bound

    @property
    def region(self):

        _region = +(self.surfaces[0]) & -(self.surfaces[1]) & + \
            (self.surfaces[2]) & -(self.surfaces[3]) & + \
            (self.surfaces[4]) & ~(self.tf_coil_magnet.region)

        _region = _add_boundaries(_region, self.angle)

        return _region

    @property
    def cell(self):
        return openmc.Cell(region=self.region, fill=self.material)


class TFCoilCase(Component):
    def __init__(self, tf_coil_magnet: TFCoilMagnet, thickness: float, material: openmc.Material, tf_coil_insulation: PFCoilInsulation = None, angle=None):
        super().__init__()

        self.tf_coil_magnet = tf_coil_magnet
        self.thickness = thickness
        self.material = material
        self.tf_coil_insulation = tf_coil_insulation
        self.angle = angle
        self.rotation_angle = tf_coil_magnet.rotation_angle

    @property
    def surfaces(self):

        if self.tf_coil_insulation:
            insulation_thickness = self.tf_coil_insulation.thickness
        else:
            insulation_thickness = 0.

        lb_y0 = self.tf_coil_magnet.surfaces[2].d - \
            self.thickness - insulation_thickness
        ub_y0 = self.tf_coil_magnet.surfaces[3].d + \
            self.thickness + insulation_thickness

        main_surface_in = self.tf_coil_magnet.surfaces[0].offset(
            -(self.thickness+insulation_thickness))
        main_surface_out = self.tf_coil_magnet.surfaces[1].offset(
            +(self.thickness+insulation_thickness))
        lower_bound = openmc.YPlane(y0=lb_y0).rotate(
            (0, 0, self.rotation_angle))
        upper_bound = openmc.YPlane(y0=ub_y0).rotate(
            (0, 0, self.rotation_angle))
        left_bound = openmc.XPlane(x0=0).rotate((0, 0, self.rotation_angle))

        return main_surface_in, main_surface_out, lower_bound, upper_bound, left_bound

    @property
    def region(self):

        _region = +(self.surfaces[0]) & -(self.surfaces[1]) & + \
            (self.surfaces[2]) & -(self.surfaces[3]) & + \
            (self.surfaces[4]) & ~(self.tf_coil_magnet.region)

        if self. tf_coil_insulation:
            _region = _region & ~(self.tf_coil_insulation.region)

        _region = _add_boundaries(_region, self.angle)

        return _region

    @property
    def cell(self):

        return openmc.Cell(region=self.region, fill=self.material)


def core_group(plasma_outer_nodes, plasma_material: openmc.Material,
               vessel_inner_nodes, vessel_thickness: float, vessel_material: openmc.Material,
               blanket_thickness: float, blanket_material: openmc.Material,
               shield_thickness: float, shield_material: openmc.Material,
               angle=None):

    plasma = Plasma(outer_nodes=plasma_outer_nodes,
                    material=plasma_material, angle=angle)

    vacuum_vessel = VacuumVessel(inner_nodes=vessel_inner_nodes, thickness=vessel_thickness,
                                 material=vessel_material, angle=angle)

    sol = SOLVacuum(
        plasma=plasma, vacuum_vessel=vacuum_vessel, angle=angle)

    blanket = Blanket(vacuum_vessel=vacuum_vessel, thickness=blanket_thickness,
                      material=blanket_material, angle=angle)

    shield = Shield(blanket=blanket, thickness=shield_thickness,
                    material=shield_material, angle=angle)

    return plasma, sol, vacuum_vessel, blanket, shield


def pfcoil_group(magnet_nodes, magnet_material: openmc.Material,
                 insulation_thickness: float, insulation_material: openmc.Material,
                 case_thickness: float, case_material: openmc.Material,
                 angle=None):

    pf_magnet = PFCoilMagnet(
        nodes=magnet_nodes, material=magnet_material, angle=angle)

    pf_insulation = PFCoilInsulation(pf_coil_magnet=pf_magnet,
                                     thickness=insulation_thickness,
                                     material=insulation_material, angle=angle)
    pf_case = PFCoilCase(pf_coil_magnet=pf_magnet, pf_coil_insulation=pf_insulation,
                         thickness=case_thickness, material=case_material, angle=angle)

    return pf_magnet, pf_insulation, pf_case


def tfcoil_group(magnet_inner_nodes, magnet_thickness: float, magnet_material: openmc.Material,
                 insulation_thickness: float, insulation_material: openmc.Material,
                 case_thickness: float, case_material: openmc.Material,
                 angle=None, rotation_angle: float = 0):

    tf_coil_magnet = TFCoilMagnet(inner_nodes=magnet_inner_nodes, thickness=magnet_thickness,
                                  material=magnet_material, angle=angle, rotation_angle=rotation_angle)

    tf_coil_insulation = TFCoilInsulation(tf_coil_magnet=tf_coil_magnet, thickness=insulation_thickness,
                                          material=insulation_material, angle=angle)

    tf_coil_case = TFCoilCase(tf_coil_magnet=tf_coil_magnet, tf_coil_insulation=tf_coil_insulation,
                              thickness=case_thickness, material=case_material, angle=angle)

    return tf_coil_magnet, tf_coil_insulation, tf_coil_case
