from abc import ABC
import openmc


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
    def __init__(self, nodes, material=None, surf_offset=0., boundary_1=None, boundary_2=None, exclude=True):
        super().__init()

        self.nodes = nodes
        self.material = material
        self.surf_offset = surf_offset
        self.boundary_1 = boundary_1
        self.boundary_2 = boundary_2
        self.exclude = exclude

    @property
    def surfaces(self):
        return openmc.model.Polygon(self.nodes, basis="rz").offset(self.surf_offset)

    @property
    def region(self):

        region = -(self.surfaces)

        if self.boundary_1:
            region = region & +(self.boundary_1)
        if self.boundary_2:
            region = region & -(self.boundary_2)

        return region

    def cell(self):

        return openmc.Cell(region=self.region, fill=self.material)


class VacuumVessel(Component):
    def __init__(self, nodes, thickness: float, material, surf_offset=0., boundary_1=None, boundary_2=None, exclude=True):
        super().__init__()

        self.nodes = nodes
        self.thickness = thickness
        self.material = material
        self.surf_offset = surf_offset
        self.boundary_1 = boundary_1
        self.boundary_2 = boundary_2
        self.exclude = exclude

    @property
    def surfaces(self):

        inner_surface = openmc.model.Polygon(
            self.nodes, basis="rz").offset(self.surf_offset)
        outer_surface = openmc.model.Polygon(
            self.nodes, basis="rz").offset(self.surf_offset+self.thickness)

        return inner_surface, outer_surface

    @property
    def region(self):

        region = -(self.surfaces[1]) & +(self.surfaces[0])

        if self.boundary_1:
            region = region & +(self.boundary_1)
        if self.boundary_2:
            region = region & -(self.boundary_2)

        return region

    def cell(self):

        return openmc.Cell(region=self.region, fill=self.material)


class SOLVacuum(Component):

    def __init__(self):
        super().__init__()
        pass

    def __init__(self, plasma: Plasma, vacuum_vessel: VacuumVessel):
        pass


class Blanket(Component):
    def __init__(self, exclude=True):
        pass


class Shield(Component):
    def __init__(self, exclude=True):
        pass


class PFCoilCase(Component):
    def __init__(self, exclude=True):
        pass


class PFCoilInsulation(Component):
    def __init__(self, exclude=True):
        pass


class TFCoilMagnet(Component):
    def __init__(self, exclude=True):
        pass


class TFCoilCase(Component):
    def __init__(self, exclude=True):
        pass


class TFCoilInsulation(Component):
    def __init__(self, exclude=True):
        pass
