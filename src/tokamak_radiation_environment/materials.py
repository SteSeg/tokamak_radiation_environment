import openmc

# PLASMA #############################
dt_plasma = openmc.Material(name='dt_plasma')
dt_plasma.add_nuclide('H2', 1.0)
dt_plasma.add_nuclide('H3', 1.0)
dt_plasma.set_density('g/cm3', 1e-5)

# METALS - ALLOSY #####################

# Tungsten (W) - pure
tungsten = openmc.Material(name='tungsten')
tungsten.add_element('W', 1.0, 'wo')
tungsten.set_density('g/cm3', 19.3)

# Beryllium (Be) - pure
beryllium = openmc.Material(name='beryllium')
beryllium.add_element('Be', 1.0)
beryllium.set_density('g/cm3', 1.85)

# Copper (Cu) - pure
copper = openmc.Material(name='Cu')
copper.add_element('Cu', 1.0)
copper.set_density('g/cm3', 8.96)

# Silver (Ag) - pure
silver = openmc.Material(name='Ag')
silver.add_element('Ag', 1.0)
silver.set_density('g/cm3', 10.49)

# PbSn - pure
pbsn = openmc.Material(name='PbSn Solder')
pbsn.add_element('Pb', 0.37, percent_type='wo')
pbsn.add_element('Sn', 0.63, percent_type='wo')
pbsn.set_density('g/cm3', 8.8)

# SS-304
ss304 = openmc.Material(name='ss304')
ss304.add_element('Cr', 0.19, 'wo')
ss304.add_element('Mn', 0.01, 'wo')
ss304.add_element('Fe', 0.71, 'wo')
ss304.add_element('Ni', 0.09, 'wo')
ss304.set_density('g/cm3', 7.80)

# Inconel 718 -
inconel718 = openmc.Material(name='inconel718')
inconel718.add_element('Ni', 53.0, 'wo')
inconel718.add_element('Cr', 19.06, 'wo')
inconel718.add_element('Nb', 5.08, 'wo')
inconel718.add_element('Mo', 3.04, 'wo')
inconel718.add_element('Ti', 0.93, 'wo')
inconel718.add_element('Al', 0.52, 'wo')
inconel718.add_element('Co', 0.11, 'wo')
inconel718.add_element('Cu', 0.02, 'wo')
inconel718.add_element('C', 0.021, 'wo')
inconel718.add_element('Fe', 18.15, 'wo')
inconel718.set_density('g/cm3', 8.19)

# Nitronic 50
# https://www.premiumalloys.com/products/nitronic_50
nitronic50 = openmc.Material(name='nitronic50')
nitronic50.add_element('Cr', 0.22, percent_type='wo')
nitronic50.add_element('Ni', 0.125, percent_type='wo')
nitronic50.add_element('Mo', 0.0225, percent_type='wo')
nitronic50.add_element('Nb', 0.002, percent_type='wo')
nitronic50.add_element('Mn', 0.05, percent_type='wo')
nitronic50.add_element('Si', 0.004, percent_type='wo')
nitronic50.add_element('C', 0.0003, percent_type='wo')
nitronic50.add_element('S', 0.0001, percent_type='wo')
nitronic50.add_element('P', 0.0004, percent_type='wo')
nitronic50.add_element('V', 0.0002, percent_type='wo')
nitronic50.add_element('N', 0.003, percent_type='wo')
nitronic50.add_element('Fe', 0.5725, percent_type='wo')
nitronic50.set_density('g/cm3', 7.88)

# Hastelloy C276
# https://www.haynesintl.com/docs/default-source/pdfs/new-alloy-brochures/corrosion-resistant-alloys/brochures/c-276.pdf?sfvrsn=6
hastelloy_c276 = openmc.Material(name='hastelloy_c276')
hastelloy_c276.add_element('Ni', 0.5456, percent_type='wo')
hastelloy_c276.add_element('Co', 0.025, percent_type='wo')
hastelloy_c276.add_element('Cr', 0.16, percent_type='wo')
hastelloy_c276.add_element('Mo', 0.16, percent_type='wo')
hastelloy_c276.add_element('Fe', 0.05, percent_type='wo')
hastelloy_c276.add_element('W', 0.04, percent_type='wo')
hastelloy_c276.add_element('Mn', 0.01, percent_type='wo')
hastelloy_c276.add_element('V', 0.0035, percent_type='wo')
hastelloy_c276.add_element('Si', 0.0008, percent_type='wo')
hastelloy_c276.add_element('C', 0.0001, percent_type='wo')
hastelloy_c276.add_element('Cu', 0.005, percent_type='wo')
hastelloy_c276.set_density('g/cm3', 8.89)

# V-4Cr-4Ti - pure - NIFS-HEAT2
v4cr4ti = openmc.Material(name='v4cr4ti')
v4cr4ti.add_element('V', 0.92, 'wo')
v4cr4ti.add_element('Cr', 0.04, 'wo')
v4cr4ti.add_element('Ti', 0.04, 'wo')
v4cr4ti.set_density('g/cm3', 6.06)
#
# Eurofer97 -
eurofer97 = openmc.Material(name='eurofer97')
eurofer97.add_element('Cr', 8.99866, 'wo')
eurofer97.add_element('C', 0.109997, 'wo')
eurofer97.add_element('W', 1.5, 'wo')
eurofer97.add_element('V', 0.2, 'wo')
eurofer97.add_element('Ta', 0.07, 'wo')
eurofer97.add_element('B', 0.001, 'wo')
eurofer97.add_element('N', 0.03, 'wo')
eurofer97.add_element('O', 0.01, 'wo')
eurofer97.add_element('S', 0.001, 'wo')
eurofer97.add_element('Fe', 88.661, 'wo')
eurofer97.add_element('Mn', 0.4, 'wo')
eurofer97.add_element('P', 0.005, 'wo')
eurofer97.add_element('Ti', 0.01, 'wo')
eurofer97.set_density('g/cm3', 7.798)

# MOLTEN SALTS & LIQUID METALS #####################
#
# FLiBe - natural - pure
flibe = openmc.Material(name='flibe')
flibe.add_element('F', 4.0)
flibe.add_element('Li', 2.0)
flibe.add_element('Be', 1.0)
flibe.set_density('g/cm3', 1.960)

# FLiNaK - natural - pure
flinak = openmc.Material(name='flinak')
flinak.add_element('F', 50, 'ao')
flinak.add_element('Li', 23.25, 'ao')
flinak.add_element('Na', 5.75, 'ao')
flinak.add_element('K', 21, 'ao')
flinak.set_density('g/cm3', 2.020)

# FLiNaBe - natural - pure
flinabe = openmc.Material(name='flinabe')
flinabe.add_element('F', 57.14, 'ao')
flinabe.add_element('Li', 14.29, 'ao')
flinabe.add_element('Na', 14.29, 'ao')
flinabe.add_element('Be', 14.29, 'ao')
flinabe.set_density('g/cm3', 2.030)

# Lithium - natural - pure
lithium = openmc.Material(name='lithium')
lithium.add_element('Li', 100, 'ao')
lithium.set_density('g/cm3', 0.4728)

# PbLi - natural - pure
pbli = openmc.Material(name='pbli')
pbli.add_element('Pb', 84.2, 'ao')
pbli.add_element('Li', 15.2, 'ao')
pbli.set_density('g/cm3', 11)

# LiF-LiBr-NaBr - natural - pure (20:73:7)
liflibrnabr = openmc.Material(name='liflibrnabr')
liflibrnabr.add_element('Li', 46.5, 'ao')
liflibrnabr.add_element('F', 36.5, 'ao')
liflibrnabr.add_element('Br', 40, 'ao')
liflibrnabr.add_element('Na', 3.5, 'ao')
liflibrnabr.set_density('g/cm3', 3.16)  # approximated

# LiF-LiBr-NaF - natural - pure (14:79:7)
liflibrnaf = openmc.Material(name='liflibrnaf')
liflibrnaf.add_element('Li', 46.5, 'ao')
liflibrnaf.add_element('F', 10.5, 'ao')
liflibrnaf.add_element('Br', 49.5, 'ao')
liflibrnaf.add_element('Na', 3.5, 'ao')
liflibrnaf.set_density('g/cm3', 3.20)  # approximated

# LiI - natural - pure (20:80)
liflii = openmc.Material(name='lii')
liflii.add_element('Li', 50, 'ao')
liflii.add_element('F', 10, 'ao')
liflii.add_element('I', 40, 'ao')
liflii.set_density('g/cm3', 3.68)  # approximated

# LiF-NaF-ZrF4 - natural - pure (55:22:23)
lifnafzrf4 = openmc.Material(name='lifnafrzf4')
lifnafzrf4.add_element('Li', 20.36, 'ao')
lifnafzrf4.add_element('F', 62.54, 'ao')
lifnafzrf4.add_element('Na', 8.15, 'ao')
lifnafzrf4.add_element('Zr', 8.51, 'ao')
lifnafzrf4.set_density('g/cm3', 2.72)  # approximated

# CERAMICS - SHIELDS ################################

# Boron Carbide (B4C) - pure
b4c = openmc.Material(name='b4c')
b4c.add_element('B', 4.0)
b4c.add_element('C', 1.0)
b4c.set_density('g/cm3', 2.51)

# Zirconium Hydride (ZrH2) - pure
zrh2 = openmc.Material(name='zrh2')
zrh2.add_element('Zr', 1.0)
zrh2.add_element('H', 2.0)
zrh2.set_density('g/cm3', 5.56)

# Zirconium Boride (ZrB) - pure
zrb2 = openmc.Material(name='zrb')
zrb2.add_element('Zr', 1.0)
zrb2.add_element('B', 2.0)
zrb2.set_density('g/cm3', 6.09)

# Tungsten Borides
# WB - pure
wb = openmc.Material(name='wb')
wb.add_element('W', 1.0)
wb.add_element('B', 1.0)
wb.set_density('g/cm3', 15.3)
# WB4 - pure
wb4 = openmc.Material(name='wb4')
wb4.add_element('W', 1.0)
wb4.add_element('B', 4.0)
wb4.set_density('g/cm3', 8.46)
# W2B5 - pure
w2b5 = openmc.Material(name='w2b4')
w2b5.add_element('W', 2.0)
w2b5.add_element('B', 4.0)
w2b5.set_density('g/cm3', 13.5)

# Tungsten Carbide (WC) - pure
wc = openmc.Material(name='wc')
wc.add_element('W', 1.0)
wc.add_element('C', 1.0)
wc.set_density('g/cm3', 15.63)

# SIMPLIFIED MAGNETS

# fiberglass insulation
fiberglass = openmc.Material(name='Fiberglass_type_e')
fiberglass.add_element('B', 0.022803, percent_type='wo')
fiberglass.add_element('O', 0.471950, percent_type='wo')
fiberglass.add_element('F', 0.004895, percent_type='wo')
fiberglass.add_element('Na', 0.007262, percent_type='wo')
fiberglass.add_element('Mg', 0.014759, percent_type='wo')
fiberglass.add_element('Al', 0.072536, percent_type='wo')
fiberglass.add_element('Si', 0.247102, percent_type='wo')
fiberglass.add_element('K', 0.008127, percent_type='wo')
fiberglass.add_element('Ca', 0.143428, percent_type='wo')
fiberglass.add_element('Ti', 0.004400, percent_type='wo')
fiberglass.add_element('Fe', 0.002739, percent_type='wo')
fiberglass.set_density('g/cm3', 2.57)

# Nb3Sn - LTS
nb3sn = openmc.Material(name='ybco')
nb3sn.add_elements_from_formula('Nb3Sn')
nb3sn.set_density('g/cm3', 8.74)

# YBCO - HTS
ybco = openmc.Material(name='ybco')
ybco.add_elements_from_formula('YBa2Cu3O7')
ybco.set_density('g/cm3', 6.3)

# mixes
# https://doi.org/10.1038/s41598-021-81559-z. Assuming 50um hastelloy.
tape = openmc.Material.mix_materials([copper, silver, hastelloy_c276, ybco], [
                                     10/65.35, 3/65.35, 50/65.35, 2.35/65.35], percent_type='vo')
windingpack = openmc.Material.mix_materials([copper, nitronic50, pbsn, tape], [
                                            0.163333, 0.603333, 0.030967, 0.202367], percent_type='vo', name="Winding pack")  # Volume fractions based on talks with magnet team
