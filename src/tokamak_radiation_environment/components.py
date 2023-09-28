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
    def __init__(self, nodes, material: openmc.Material = None, surf_offset=0., angle=None):

        self.nodes = nodes
        self.material = material
        self.surf_offset = surf_offset
        self.angle = angle

    @property
    def surfaces(self):
        main_surf = openmc.model.Polygon(
            self.nodes, basis="rz").offset(self.surf_offset)

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
    def __init__(self, nodes, thickness: float, material: openmc.Material, angle=None):
        super().__init__()

        self.nodes = nodes
        self.thickness = thickness
        self.material = material
        self.angle = angle

    @property
    def surfaces(self):

        inner_surface = openmc.model.Polygon(
            self.nodes, basis="rz")
        outer_surface = openmc.model.Polygon(
            self.nodes, basis="rz").offset(self.thickness)

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
    def __init__(self, centroid, height: float, radial_thickness: float, material: openmc.Material, angle=None):
        super().__init__()

        self.centroid = centroid
        self.height = height
        self.radial_thickness = radial_thickness
        self.material = material
        self.angle = angle

    @property
    def surfaces(self):

        lower_left = [self.centroid[0]-self.radial_thickness /
                      2, self.centroid[1]-self.height/2]
        lower_right = [self.centroid[0]+self.radial_thickness /
                       2, self.centroid[1]-self.height/2]
        upper_right = [self.centroid[0]+self.radial_thickness /
                       2, self.centroid[1]+self.height/2]
        upper_left = [self.centroid[0]-self.radial_thickness /
                      2, self.centroid[1]+self.height/2]
        nodes = [lower_left, lower_right, upper_right, upper_left]

        return openmc.model.Polygon(nodes, basis="rz")

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
    def __init__(self, nodes, thickness: float, material: openmc.Material, angle=None):
        super().__init__()

        self.nodes = nodes
        self.thickness = thickness
        self.material = material
        self.angle = angle

    @property
    def surfaces(self):

        main_surface_in = openmc.model.Polygon(self.nodes, basis="rz")
        main_surface_out = openmc.model.Polygon(
            self.nodes, basis="rz").offset(self.thickness)
        lower_bound = openmc.YPlane(y0=-self.thickness)
        upper_bound = openmc.YPlane(y0=self.thickness)
        left_bound = openmc.XPlane(x0=0)

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

    @property
    def surfaces(self):

        lb_y0 = self.tf_coil_magnet.surfaces[2].y0 - self.thickness
        ub_y0 = self.tf_coil_magnet.surfaces[3].y0 + self.thickness

        main_surface_in = self.tf_coil_magnet.surfaces[0].offset(
            -self.thickness)
        main_surface_out = self.tf_coil_magnet.surfaces[1].offset(
            +self.thickness)
        lower_bound = openmc.YPlane(y0=lb_y0)
        upper_bound = openmc.YPlane(y0=ub_y0)
        left_bound = openmc.XPlane(x0=0)

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

    @property
    def surfaces(self):

        if self.tf_coil_insulation:
            insulation_thickness = self.tf_coil_insulation.thickness
        else:
            insulation_thickness = 0.

        lb_y0 = self.tf_coil_magnet.surfaces[2].y0 - \
            self.thickness - insulation_thickness
        ub_y0 = self.tf_coil_magnet.surfaces[3].y0 + \
            self.thickness + insulation_thickness

        main_surface_in = self.tf_coil_magnet.surfaces[0].offset(
            -(self.thickness+insulation_thickness))
        main_surface_out = self.tf_coil_magnet.surfaces[1].offset(
            +(self.thickness+insulation_thickness))
        lower_bound = openmc.YPlane(y0=lb_y0)
        upper_bound = openmc.YPlane(y0=ub_y0)
        left_bound = openmc.XPlane(x0=0)

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
