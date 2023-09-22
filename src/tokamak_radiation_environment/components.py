from abc import ABC
import openmc


def _add_boundary_surfaces(region, boundary_1, boundary_2):

    if boundary_1:
        region = region & +(boundary_1)
    if boundary_2:
        region = region & -(boundary_2)

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
    def __init__(self, nodes, material: openmc.Material = None, surf_offset=0., boundary_1: openmc.Surface = None, boundary_2: openmc.Surface = None):

        self.nodes = nodes
        self.material = material
        self.surf_offset = surf_offset
        self.boundary_1 = boundary_1
        self.boundary_2 = boundary_2

    @property
    def surfaces(self):
        return openmc.model.Polygon(self.nodes, basis="rz").offset(self.surf_offset)

    @property
    def region(self):

        _region = -(self.surfaces)

        _region = _add_boundary_surfaces(
            _region, self.boundary_1, self.boundary_2)

        return _region

    @property
    def cell(self):

        return openmc.Cell(region=self.region, fill=self.material)


class VacuumVessel(Component):
    def __init__(self, nodes, thickness: float, material: openmc.Material, boundary_1: openmc.Surface = None, boundary_2: openmc.Surface = None):
        super().__init__()

        self.nodes = nodes
        self.thickness = thickness
        self.material = material
        self.boundary_1 = boundary_1
        self.boundary_2 = boundary_2

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

        _region = _add_boundary_surfaces(
            _region, self.boundary_1, self.boundary_2)

        return _region

    @property
    def cell(self):

        return openmc.Cell(region=self.region, fill=self.material)


class SOLVacuum(Component):

    def __init__(self, plasma: Plasma, vacuum_vessel: VacuumVessel, material: openmc.Material = None, boundary_1: openmc.Surface = None, boundary_2: openmc.Surface = None):
        super().__init__()

        self.plasma = plasma
        self.vacuum_vessel = vacuum_vessel
        self.material = material
        self.boundary_1 = boundary_1
        self.boundary_2 = boundary_2

    @property
    def surfaces(self):

        sol_inner_surface = self.plasma.surfaces
        sol_outer_surface = self.vacuum_vessel.surfaces[0]

        return sol_inner_surface, sol_outer_surface

    @property
    def region(self):

        _region = -(self.surfaces[1]) & +(self.surfaces[0])

        _region = _add_boundary_surfaces(
            _region, self.boundary_1, self.boundary_2)

        return _region

    @property
    def cell(self):

        return openmc.Cell(region=self.region, fill=self.material)


class Blanket(Component):
    def __init__(self, vacuum_vessel: VacuumVessel, thickness: float, material: openmc.Material, nodes=None, boundary_1: openmc.Surface = None, boundary_2: openmc.Surface = None):
        super().__init__()

        self.vacuum_vessel = vacuum_vessel
        self.thickness = thickness
        self.material = material
        self.nodes = nodes
        self.boundary_1 = boundary_1
        self.boundary_2 = boundary_2

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

        _region = _add_boundary_surfaces(
            _region, self.boundary_1, self.boundary_2)

        return _region

    @property
    def cell(self):
        return openmc.Cell(region=self.region, fill=self.material)


class Shield(Component):
    def __init__(self, blanket: Blanket, thickness: float, material: openmc.Material, nodes=None, boundary_1: openmc.Surface = None, boundary_2: openmc.Surface = None):
        super().__init__()

        self.blanket = blanket
        self.thickness = thickness
        self.material = material
        self.nodes = nodes
        self.boundary_1 = boundary_1
        self.boundary_2 = boundary_2

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

        _region = _add_boundary_surfaces(
            _region, self.boundary_1, self.boundary_2)

        return _region

    @property
    def cell(self):
        return openmc.Cell(region=self.region, fill=self.material)


class PFCoilMagnet(Component):
    def __init__(self, centroid: float, height: float, radial_thickness: float, material: openmc.Material, boundary_1: openmc.Surface = None, boundary_2: openmc.Surface = None):
        super().__init__()

        self.centroid = centroid
        self.height = height
        self.radial_thickness = radial_thickness
        self.material = material
        self.boundary_1 = boundary_1
        self.boundary_2 = boundary_2

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

        _region = _add_boundary_surfaces(
            _region, self.boundary_1, self.boundary_2)

        return _region

    @property
    def cell(self):

        return openmc.Cell(region=self.region, fill=self.material)


class PFCoilInsulation(Component):
    def __init__(self, pf_coil_magnet: PFCoilMagnet, thickness: float, material: openmc.Material, boundary_1: openmc.Surface = None, boundary_2: openmc.Surface = None):
        super().__init__()

        self.pf_coil_magnet = pf_coil_magnet
        self.thickness = thickness
        self.material = material
        self.boundary_1 = boundary_1
        self.boundary_2 = boundary_2

    @property
    def surfaces(self):

        return self.pf_coil_magnet.surfaces.offset(self.thickness)

    @property
    def region(self):

        _region = -(self.surfaces) & ~(self.pf_coil_magnet.region)

        _region = _add_boundary_surfaces(
            _region, self.boundary_1, self.boundary_2)

        return _region

    @property
    def cell(self):

        return openmc.Cell(region=self.region, fill=self.material)


class PFCoilCase(Component):
    def __init__(self, pf_coil_magnet: PFCoilMagnet, thickness: float, material: openmc.Material, pf_coil_insulation: PFCoilInsulation = None, boundary_1: openmc.Surface = None, boundary_2: openmc.Surface = None):
        super().__init__()

        self.pf_coil_magnet = pf_coil_magnet
        self.pf_coil_insulation = pf_coil_insulation
        self.material = material
        self.thickness = thickness
        self.boundary_1 = boundary_1
        self.boundary_2 = boundary_2

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

        _region = _add_boundary_surfaces(
            _region, self.boundary_1, self.boundary_2)

        return _region

    @property
    def cell(self):

        return openmc.Cell(region=self.region, fill=self.material)


class TFCoilMagnet(Component):
    def __init__(self, nodes=None, centroid: float = None, height: float = None, radial_thickness: float = None, boundary_1: openmc.Surface = None, boundary_2: openmc.Surface = None):
        super().__init__()

        self.nodes = nodes
        self.centroid = centroid
        self.height = height
        self.radial_thickness = radial_thickness
        self.boundary_1 = boundary_1
        self.boundary_2 = boundary_2

    @property
    def surface(self):
        pass

    @property
    def region(self):
        pass

    @property
    def cell(self):
        pass


class TFCoilCase(Component):
    def __init__(self, plasma: Plasma, vacuum_vessel: VacuumVessel, boundary_1: openmc.Surface = None, boundary_2: openmc.Surface = None):
        super().__init__()
        pass

    @property
    def surface(self):
        pass

    @property
    def region(self):
        pass

    @property
    def cell(self):
        pass


class TFCoilInsulation(Component):
    def __init__(self, plasma: Plasma, vacuum_vessel: VacuumVessel, boundary_1: openmc.Surface = None, boundary_2: openmc.Surface = None):

        super().__init__()

    @property
    def surface(self):
        pass

    @property
    def region(self):
        pass

    @property
    def cell(self):
        pass


class NewComponent(ABC):
    def __init__(self, nodes, material, exclude=None):
        self.nodes = nodes
        self.material = material
        self.exclude = exclude

    def surfaces(self):
        pass

    def region(self):
        pass

    def cell(self):
        pass
