

_plasma_out = [[820, 0], [798, 105], [772, 178], [720, 243], [658, 301], [587, 335], [
    538, 338], [495, 317], [469, 285], [436, 191], [422, 80], [420, 0]]

_vessel_in = [[840, 0], [836, 80], [813, 162], [768, 246], [704, 322], [616, 383], [
    554, 398], [488, 380], [440, 322], [408, 222], [400, 109], [400, 0]]

# _tf_in = [[1053, 0], [1034, 109], [992, 222], [920, 335], [813, 436], [758, 470], [
#     666, 505], [560, 518], [488, 508], [408, 473], [345, 414], [317, 357], [308, 299], [308, 0]]

_tf_in = [[1050.,  118.],
          [1000.,  238.],
          [947.,  358.],
          [835.,  465.],
          [774.,  502.],
          [674.,  540.],
          [559.,  554.],
          [478.,  542.],
          [387.,  503.],
          [315.,  436.],
          [282.,  368.],
          [272.,  301.],
          [272.0, -301.0],
          [282.0, -368.0],
          [315.0, -436.0],
          [387.0, -503.0],
          [478.0, -542.0],
          [559.0, -554.0],
          [674.0, -540.0],
          [774.0, -502.0],
          [835.0, -465.0],
          [947.0, -358.0],
          [1000.0, -238.0],
          [1050.0, -118.0]
          ]


_pf_u1 = [[1230, 323], [1158, 323], [1158, 212], [1230, 212]]
_pf_u2 = [[862, 625], [798, 625], [798, 564], [862, 564]]
_pf_u3 = [[446, 746], [345, 746], [345, 650], [446, 650]]

_cs_u1 = [[202, 200], [132, 200], [132, 0], [202, 0]]
_cs_u2 = [[202, 400], [132, 400], [132, 200], [202, 200]]
_cs_u3 = [[202, 600], [132, 600], [132, 400], [202, 400]]


def _move_y(component, value):
    """points are provided 57cm shifted up in the z-direction

    Args:
        component (_type_): _description_

    Returns:
        _type_: _description_
    """

    new_component = [[0, 0] for _ in range(len(component))]
    for i, el in enumerate(component):
        new_component[i] = [el[0], el[1]+value]
        print(el[1]+value)

    return new_component


def _mirror_around_x(component, append: bool = False):
    """_summary_

    Args:
        component (_type_): _description_

    Returns:
        _type_: _description_
    """

    # if append:
    #     new_component = component.copy()
    # else:
    #     new_component = []

    new_component = []

    for el in component[::-1]:
        if el[1] != 0:
            new_component.append([el[0], -el[1]])
        else:
            if not append:
                new_component.append([el[0], 0])

    if append:
        new_component = component + new_component

    return new_component


plasma_out = _mirror_around_x(_plasma_out, append=True)
vessel_in = _mirror_around_x(_vessel_in, append=True)
tf_in = _mirror_around_x(_tf_in, append=True)
# pf_u1 = _pf_u1
# pf_u2 = _pf_u2
# pf_u3 = _pf_u3
# pf_l1 = _mirror_around_x(pf_u1)
# pf_l2 = _mirror_around_x(pf_u2)
# pf_l3 = _mirror_around_x(pf_u3)
# cs_u1 = _cs_u1
# cs_u2 = _cs_u2
# cs_u3 = _cs_u3
# cs_l1 = _mirror_around_x(_cs_u1)
# cs_l2 = _mirror_around_x(_cs_u2)
# cs_l3 = _mirror_around_x(_cs_u3)
