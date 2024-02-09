from abc import ABC
import typing
import openmc


def _add_boundaries(region, angle):
    """Include two reflective surfaces perpendicular to the xy plane
    in order to slice the tokamak according to the values given in the
    angle argument. The initial region has to be axysymmetric around z.
    The result is an openmc.Region that is symmetric 
    with respect the xz plane

    Parameters
    ----------
    region : openmc.Region 
        Region to slice
    angle : tuple of two floats
        The first float is the angle in deg to cut with respect the x axis
        The second float is the angle in deg to finish the cut

    Returns
    -------
    openmc.Region
        The region subtended by the two angles provided in the angle argument
    """

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
    def __init__(self, outer_nodes, material: openmc.Material = None, surf_offset: float = 0., angle=None):
        """Plasma component described by its outer surface. The outer surface is an openmc

        Parameters
        ----------
        outer_nodes : iterable of tuples with (r,z) coordinates and describing a closed polygon
            _description_
        material : openmc.Material, optional
            material to fill the plasma with, by default None
        surf_offset : float, optional
            offset the surfaces decribed by the nodes by this value (cm)
            if positive it offsets outwards,
            if negative it offsets inwards, by default 0.
        angle : tuple of two floats, optional
        The first float is the angle in deg to cut with respect the x axis
        The second float is the angle in deg to finish the cut, by default None
        """

        self.outer_nodes = outer_nodes
        self.material = material
        self.surf_offset = surf_offset
        self.angle = angle

    @property
    def surfaces(self):
        """openmc.Surface generator

        Returns
        -------
        openmc.Surface
            Rurfaces necessary to build the plasma component
        """
        main_surf = openmc.model.Polygon(
            self.outer_nodes, basis="rz").offset(self.surf_offset)

        return main_surf

    @property
    def region(self):
        """openmc.Region generator

        Returns
        -------
        openmc.Region
            Regions that define the bodies in the openmc simulation
        """

        _region = -(self.surfaces)

        _region = _add_boundaries(_region, self.angle)

        return _region

    @property
    def cell(self):
        """openmc.Cell generator

        Returns
        -------
        openmc.Cell
            Final component cell for the openmc simulation
        """

        return openmc.Cell(region=self.region, fill=self.material)


class FirstWall(Component):
    def __init__(self, inner_nodes, thickness: str, material: openmc.Material, angle=None):
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

    def __init__(self, plasma: Plasma, first_wall: FirstWall, material: openmc.Material = None, angle=None):
        super().__init__()

        self.plasma = plasma
        self.first_wall = first_wall
        self.material = material
        self.angle = angle

    @property
    def surfaces(self):

        sol_inner_surface = self.plasma.surfaces
        sol_outer_surface = self.first_wall.surfaces[0]

        return sol_inner_surface, sol_outer_surface

    @property
    def region(self):

        _region = -(self.surfaces[1]) & +(self.surfaces[0])

        _region = _add_boundaries(_region, self.angle)

        return _region

    @property
    def cell(self):

        return openmc.Cell(region=self.region, fill=self.material)


class VesselInnerStructure(Component):
    def __init__(self, first_wall: FirstWall, thickness: str, material: openmc.Material, angle=None):
        super().__init__()

        self.first_wall = first_wall
        self.thickness = thickness
        self.material = material
        self.angle = angle

    @property
    def surfaces(self):

        inner_surface = self.first_wall.surfaces[-1]
        outer_surface = inner_surface.offset(self.thickness)

        return inner_surface, outer_surface

    @property
    def region(self):

        _region = -(self.surfaces[1]) & +(self.surfaces[0])

        _region = _add_boundaries(_region, self.angle)

        return _region

    @property
    def cell(self):

        return openmc.Cell(region=self.region, fill=self.material)


class VesselCoolingChannel(Component):
    def __init__(self, vessel_inner_structure: VesselInnerStructure, thickness: str, material: openmc.Material, angle=None):
        super().__init__()

        self.vessel_inner_structure = vessel_inner_structure
        self.thickness = thickness
        self.material = material
        self.angle = angle

    @property
    def surfaces(self):

        inner_surface = self.vessel_inner_structure.surfaces[-1]
        outer_surface = inner_surface.offset(self.thickness)

        return inner_surface, outer_surface

    @property
    def region(self):

        _region = -(self.surfaces[1]) & +(self.surfaces[0])

        _region = _add_boundaries(_region, self.angle)

        return _region

    @property
    def cell(self):

        return openmc.Cell(region=self.region, fill=self.material)


class VesselNeutronMultiplier(Component):
    def __init__(self, vessel_cooling_channel: VesselCoolingChannel, thickness: str, material: openmc.Material, angle=None):
        super().__init__()

        self.vessel_cooling_channel = vessel_cooling_channel
        self.thickness = thickness
        self.material = material
        self.angle = angle

    @property
    def surfaces(self):

        inner_surface = self.vessel_cooling_channel.surfaces[-1]
        outer_surface = inner_surface.offset(self.thickness)

        return inner_surface, outer_surface

    @property
    def region(self):

        _region = -(self.surfaces[1]) & +(self.surfaces[0])

        _region = _add_boundaries(_region, self.angle)

        return _region

    @property
    def cell(self):

        return openmc.Cell(region=self.region, fill=self.material)


class VesselOuterStructure(Component):
    def __init__(self, vessel_neutron_multiplier: typing.Union[VesselNeutronMultiplier, VesselCoolingChannel], thickness: str, material: openmc.Material, angle=None):
        super().__init__()

        self.vessel_neutron_multiplier = vessel_neutron_multiplier
        self.thickness = thickness
        self.material = material
        self.angle = angle

    @property
    def surfaces(self):

        inner_surface = self.vessel_neutron_multiplier.surfaces[-1]
        outer_surface = inner_surface.offset(self.thickness)

        return inner_surface, outer_surface

    @property
    def region(self):

        _region = -(self.surfaces[1]) & +(self.surfaces[0])

        _region = _add_boundaries(_region, self.angle)

        return _region

    @property
    def cell(self):

        return openmc.Cell(region=self.region, fill=self.material)


class Blanket(Component):
    def __init__(self, vacuum_vessel: typing.Union[VesselInnerStructure, VesselOuterStructure],
                 thickness: float, material: openmc.Material, nodes=None, angle=None):
        super().__init__()

        self.vacuum_vessel = vacuum_vessel
        self.thickness = thickness
        self.material = material
        self.nodes = nodes
        self.angle = angle

    @property
    def surfaces(self):

        inner_surface = self.vacuum_vessel.surfaces[-1]

        if self.nodes:
            outer_surface = openmc.model.Polygon(self.nodes, basis="rz")
        else:
            outer_surface = self.vacuum_vessel.surfaces[-1].offset(
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
    def __init__(self, tf_coil_magnet: TFCoilMagnet, thickness: float, material: openmc.Material, tf_coil_insulation: TFCoilInsulation = None, angle=None):
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

        if self.tf_coil_insulation:
            _region = _region & ~(self.tf_coil_insulation.region)

        _region = _add_boundaries(_region, self.angle)

        return _region

    @property
    def cell(self):

        return openmc.Cell(region=self.region, fill=self.material)


def core_group(plasma_outer_nodes, plasma_material: openmc.Material,
               firstwall_inner_nodes, firstwall_thickness: float, firstwall_material: openmc.Material,
               vv_stri_thickness: float, vv_stri_material: openmc.Material,
               vv_channel_thickness: float, vv_channel_material: openmc.Material,
               vv_multiplier_thickness: float, vv_multiplier_material: openmc.Material,
               vv_stro_thickness: float, vv_stro_material: openmc.Material,
               blanket_thickness: float, blanket_material: openmc.Material,
               shield_thickness: float, shield_material: openmc.Material,
               angle=None):
    """This function allows do directly generate all the Core components in one call

    Parameters
    ----------
    plasma_outer_nodes : Iterable of tuples
        List of (r,z) coordinates for the plasma cell outer surface
    plasma_material : openmc.Material
        Material to fill the plasma with
    vessel_inner_nodes : Iterable of tuples
        List of (r,z) coordinates for the vessel cell inner surface
    vessel_thickness : float
        number (cm) for offsetting the vessel nodes outwards and get the vessel outer surface
    vessel_material : openmc.Material
        Material to fill the vessel with
    blanket_thickness : float
        number (cm) for offsetting the vessel nodes further outwards other than the vessel
        thickness itself and get the blanket outer surface
    blanket_material : openmc.Material
        Material to fill the blanket with
    shield_thickness : float
        number (cm) for offsetting the vessel nodes further outwards other than the vessel
        and blanket thickness itself and get the shield outer surface
    shield_material : openmc.Material
        Material to fill the shield with
    angle : tuple of two floats, optional
        The first float is the angle in deg to cut with respect the x axis
        The second float is the angle in deg to finish the cut, by default None

    Returns
    -------
    Four Component types
        Plasma, VacuumVessel, SOLVacuum, Blanket, Shield
    """

    plasma = Plasma(outer_nodes=plasma_outer_nodes,
                    material=plasma_material, angle=angle)

    first_wall = FirstWall(inner_nodes=firstwall_inner_nodes,
                           thickness=firstwall_thickness, material=firstwall_material, angle=angle)
    vessel_inner_structure = VesselInnerStructure(
        first_wall=first_wall, thickness=vv_stri_thickness, material=vv_stri_material, angle=angle)
    vessel_cooling_channel = VesselCoolingChannel(
        vessel_inner_structure=vessel_inner_structure, thickness=vv_channel_thickness, material=vv_channel_material, angle=angle)
    vessel_neutron_multiplier = VesselNeutronMultiplier(
        vessel_cooling_channel=vessel_cooling_channel, thickness=vv_multiplier_thickness, material=vv_multiplier_material, angle=angle)
    vessel_outer_structure = VesselOuterStructure(
        vessel_neutron_multiplier=vessel_neutron_multiplier, thickness=vv_stro_thickness, material=vv_stro_material, angle=angle)

    sol = SOLVacuum(plasma=plasma, first_wall=first_wall,
                    material=None, angle=angle)

    blanket = Blanket(vacuum_vessel=vessel_outer_structure, thickness=blanket_thickness,
                      material=blanket_material, nodes=None, angle=angle)

    shield = Shield(blanket=blanket, thickness=shield_thickness,
                    material=shield_material, angle=angle)

    return plasma, sol, first_wall, vessel_inner_structure, vessel_cooling_channel, vessel_neutron_multiplier, vessel_outer_structure, blanket, shield


def pfcoil_group(magnet_nodes, magnet_material: openmc.Material,
                 insulation_thickness: float, insulation_material: openmc.Material,
                 case_thickness: float, case_material: openmc.Material,
                 angle=None):
    """This function allows do directly generate all the PFCoil components in one call

    Parameters
    ----------
    magnet_nodes : Iterable of tuples
        List of (r,z) coordinates for the superconductor cell
    magnet_material : openmc.Material
        Material to fill the magnet with
    insulation_thickness : float
        number (cm) for offsetting the magnet nodes outwards and get the insulation
        outer surface
    insulation_material : openmc.Material
        Material to fill the insulation with
    case_thickness : float
        number (cm) for offsetting the magnet nodes further outwards other than the 
        insulation thickness and get the case outer surface
    case_material : openmc.Material
        Material to fill the case with
    angle : tuple of two floats, optional
        The first float is the angle in deg to cut with respect the x axis
        The second float is the angle in deg to finish the cut, by default None

    Returns
    -------
    Three Component types
    PFCoilMagnet, PFCoilInsulation, PFCoilCase
    """

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
    """This function allows do directly generate all the TFCoil components in one call

    Parameters
    ----------
    magnet_inner_nodes : Iterable of tuples
        List of (r,z) coordinates for the superconductor cell inner surface
    magnet_thickness : float
        number (cm) for offsetting the magnet nodes outwards in poloidal direction
        and to extrude the magnet in the toroidal direction with the xz plane being
        the midplane
    magnet_material : openmc.Material
        Material to fill the magnet with
    insulation_thickness : float
        number (cm) for offsetting the magnet nodes outwards in both poloidal
        and toroidal directions and get the insulation
        outer surface
    insulation_material : openmc.Material
        Material to fill the insulation with
    case_thickness : float
        number (cm) for offsetting the magnet nodes further outwards in both poloidal
        and toroidal directions other than the  insulation thickness and get the case
        outer surface
    case_material : openmc.Material
        Material to fill the case with
    angle : tuple of two floats, optional
        The first float is the angle in deg to cut with respect the x axis
        The second float is the angle in deg to finish the cut, by default None
    rotation_angle : float, optional
        number (deg) for rotating the magnet counterclockwise around the z-axis,
        by default 0

    Returns
    -------
    Three Component types
        TFCoilMagnet, TFCoilInsulation, TFCoilCase
    """

    tf_coil_magnet = TFCoilMagnet(inner_nodes=magnet_inner_nodes, thickness=magnet_thickness,
                                  material=magnet_material, angle=angle, rotation_angle=rotation_angle)

    tf_coil_insulation = TFCoilInsulation(tf_coil_magnet=tf_coil_magnet, thickness=insulation_thickness,
                                          material=insulation_material, angle=angle)

    tf_coil_case = TFCoilCase(tf_coil_magnet=tf_coil_magnet, tf_coil_insulation=tf_coil_insulation,
                              thickness=case_thickness, material=case_material, angle=angle)

    return tf_coil_magnet, tf_coil_insulation, tf_coil_case
