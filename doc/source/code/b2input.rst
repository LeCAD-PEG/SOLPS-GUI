.. _b2input:

##########
B2.5 input
##########


.. highlight:: csh

.. solps-gui-switches:


.. note::

	This is a generated reST file from b2input.xml.
	It covers switches and parameters.

.. role:: latex(raw)
   :format: latex

********
b2ai.dat
********
.. index:: b2ai params

b2ai params
===========
.. index:: dimens

``dimens``    type: ``None``    default: ``None``
    the number of charge states
    

.. index:: label

``label``    type: ``None``    default: ``None``
    a label

.. index:: specs

``specs``    type: ``None``    default: ``None``
    atomic charge, nuclear charge, atomic mass and atomic charge squared for each charge state, minimum atomic charge of the stage, maximum atomic charge of the stage, nuclear charge, and atomic mass; this data should match that given in b2ah.dat
    

.. index:: naini

``naini``    type: ``None``    default: ``None``
    initial densities for each of the charge states, in m^-3`
    

.. index:: ttini

``ttini``    type: ``None``    default: ``None``
    initial ion and electron temperatures, in eV
    

.. index:: 
   single: b2ai params; dimens
   single: b2ai params; label
   single: b2ai params; specs
   single: b2ai params; naini
   single: b2ai params; ttini

********
b2ah.dat
********
.. index:: b2ah params

b2ah params
===========
.. index:: dimens

``dimens``    default: ``None``
    the number of charge states
    

.. index:: label

``label``    default: ``None``
    specifies, on the next line, a label for the run
    

.. index:: b2cmpa

``b2cmpa``    default: ``None``
    specifies a block of basic parameters.
    

.. index:: b2cmpb

``b2cmpb``    default: ``None``
    specifies a block of boundary conditions
    

.. index:: b2cmpt

``b2cmpt``    default: ``None``
    specifies a block of transport coefficients
    

.. index:: specs

``specs``
    atomic charge, nuclear charge, atomic mass and atomic charge squared; this data should match that given in b2ai.dat. Starting with code version 01.001.024, an alternative means of describing the plasma species and filling out the b2cmpa block is provided, in order to allow for bundling of charge states, when running cases with high-Z species. The relevant description is then minimum atomic charge of the stage, maximum atomic charge of the stage, nuclear charge, and atomic mass; this data should match that given in b2ai.dat The code can accept indifferently both types of input and makes the appropriate self-consistency checks. It is not permitted to bundle neutral and ionized species together.
    

.. index:: cbregs

``cbregs``    default: ``None``
    specifies the number of regions where boundary conditions will be specified the 'south' boundary is broken into three pieces with one quarter of the cells in the first region, half of the cells in the second, and the remaining quarter in the third region (Western target private flux, core, Eastern target private flux). This is geometry-dependent information the code will check against the mesh connectivity and return an error if the two do not match the 'north', 'west' and 'east' are not broken up, and correspond to the SOL boundary, inner (outer) target and outer (inner) target, respectively for lower (upper) single-null topologies. For double-null cases, the north boundary should be split into two sections.
    

.. index:: region

``region``    default: ``None``
    one block for each of the regions containing; the immediately following line being the region dentifier
    

.. index:: cbsna

``cbsna``    default: ``None``
    boundary conditions for density (1 line per species)
    

.. index:: cbsmo

``cbsmo``    default: ``None``
    boundary conditions for parallel momentum (1 line per species)
    

.. index:: cbshi

``cbshi``    default: ``None``
    ion/neutral (or "atomic") temperature/energy boundary condition (1 line per species)
    

.. index:: cbshe

``cbshe``    default: ``None``
    electron temperature/heat flux boundary condition
    

.. index:: cbsch

``cbsch``    default: ``None``
    boundary condition for the electric potential equation
    

.. index:: cbrec

``cbrec``    default: ``None``
    recycling coefficients (1 line per species)
    

.. index:: cbmsa

``cbmsa``    default: ``None``
    [unused]
    

.. index:: cbmsb

``cbmsb``    default: ``None``
    [unused] (1 line per species)
    

.. index:: 
   single: b2ah params; dimens
   single: b2ah params; label
   single: b2ah params; b2cmpa
   single: b2ah params; b2cmpb
   single: b2ah params; b2cmpt
   single: b2ah params; specs
   single: b2ah params; cbregs
   single: b2ah params; region
   single: b2ah params; cbsna
   single: b2ah params; cbsmo
   single: b2ah params; cbshi
   single: b2ah params; cbshe
   single: b2ah params; cbsch
   single: b2ah params; cbrec
   single: b2ah params; cbmsa
   single: b2ah params; cbmsb

********
b2ag.dat
********
.. index:: b2ag params

b2ag params
===========
.. index:: dimens

``dimens``    type: ``None``    default: ``None``
    specifies the size of the grid first pair is NX & NY of the grid you want to produce second pair is the size of the grid that was originally created each needs to be an integer multiple of the corresponding entry of the first pair. Note that for double-null cases, the interior guard cells corresponding to the top divertor boundaries should not be multiplied.
    

.. index:: param

``param``    type: ``None``    default: ``None``
    at least 100 additional numbers, of which only the first is relevant, unless using an analytic formulation for the grid.
    A value of -1.0 asks to read the mesh data using the "simplified" Carre format.
    A value of -2.0 asks to read the mesh data using the Sonnet format.
    

.. index:: 
   single: b2ag params; dimens
   single: b2ag params; param

********
b2mn.dat
********
.. index:: Geometry

Geometry
========
.. index:: b2agfs_geometry

``b2agfs_geometry``    type: ``string``    default: ``upgrade.geometry``
    contains the file name of the geometry file to be read.
    The file will be looked for in the run directory, in the ../baserun directory, in $SOLPSTOP/data.local/meshes, and in $SOLPSTOP/modules/Carre/meshes/$DEVICE. To be used in b2ag.dat.
    

.. index:: b2mwti_jxa

``b2mwti_jxa``    type: ``integer``    default: ``See description (integer)``
    Cell index, on the basis mesh, of the outer midplane. Default value depends on geometry:
    Lower Single-null  : jxa=rightcut(1)-(rightcut(1)-leftcut(1))/4, i.e. three quarters of the way between the two cuts.
    Upper Single-null  : jxa=leftcut(1)+(rightcut(1)-leftcut(1))/4, i.e. one quarter of the way between the two cuts.
    Stellarator island : jxa=leftcut(1)+(rightcut(1)-leftcut(1))/2, i.e. midway between the two cuts.
    Double-null        : jxa=(rightcut(1)+rightcut(2))/2, i.e. halfway between the two outer cuts.
    Limiter geometry   : jxa=nx/2
    Straight geometry  : jxa=nx/2
    Superseded by the RZOMP definition from b2.user.parameters.
    

.. index:: b2mwti_jxi

``b2mwti_jxi``    type: ``integer``    default: ``See description (integer)``
    Cell index, on the basis mesh, of the inner midplane. Default value depends on geometry:
    Lower Single-null  : jxi=leftcut(1)+(rightcut(1)-leftcut(1))/4, i.e. one quarter of the way between the two cuts.
    Upper Single-null  : jxi=rightcut(1)-(rightcut(1)-leftcut(1))/4, i.e. three quarters of the way between the two cuts.
    Stellarator island : jxi=leftcut(1)+(rightcut(1)-leftcut(1))/4, i.e. one quarter of the way between the two cuts.
    Double-null        : jxi=(leftcut(1)+leftcut(2))/2, i.e. halfway between the two inner cuts.
    Limiter geometry   : jxi=nx/4
    Straight geometry  : jxi=nx/4
    Superseded by the RZIMP definition from b2.user.parameters.
    

.. index:: b2mwti_jsep

``b2mwti_jsep``    type: ``integer``    default: ``See description (integer)``
    Flux surface index, on the basis mesh, of the active separatrix. Can only be provided for slab geometries, otherwise deduced from geometry.
    

.. index:: b2agmx_pbs_from_basis_mesh

``b2agmx_pbs_from_basis_mesh``    type: ``integer``    default: ``1``
    If pbs\_from\_basis\_mesh.eq.0, the pbs array is computed from values on the actual working mesh (old treatment).
    If pbs\_from\_basis\_mesh.eq.1, the pbs array is computed from values on the (possibly) finer basis mesh from the geometry file and the contributions from each basis cell are added to obtain the value on the working mesh.
    In both cases, mind the value of 'b2news\_area\_fix', which should be also declared in b2ag.dat if the non-default behaviour is wanted.
    

.. index:: b2agdr_redef_pbs

``b2agdr_redef_pbs``    type: ``integer``    default: ``1``
    When b2agdr\_redef\_pbs.eq.1, geometrical quantities are adjusted so as to ensure that the poloidal flux between two flux surfaces remains constant.
    

.. index:: b2mndr_redef_pbs

``b2mndr_redef_pbs``    type: ``integer``    default: ``0``
    Obsolete. Should use b2agdr\_redef\_pbs instead.
    

.. index:: b2agfs_periodic_bc

``b2agfs_periodic_bc``    type: ``integer``    default: ``0``
    periodic\_bc specifies if this is either an island or limiter geometry.
    If periodic\_bc.eq.1 then island/limiter treatment is turned on. We differentiate between the two case through nncut:
    nncut.eq.0 = limiter case
    nncut.ge.1 = island divertor case (there should be nncut islands then)
    The case periodic\_bc.eq.-1 is used to remove tranverse physics in 1-D cases.
    If periodic\_bc.eq.0 then we have the usual treatment. No other values are currently allowed. To be used in b2ag.dat.
    

.. index:: b2agsi_isymm

``b2agsi_isymm``    type: ``integer``    default: ``1``
    isymm specifies the type of symmetry of the geometry: isymm.eq.0 implies a slab geometry,
    isymm.eq.1.or.isymm.eq.2 imply rotational symmetry about the crx=0 axis, and isymm.eq.3.or.isymm.eq.4 indicate rotational symmetry about the cry=0 axis.
    Other values are not allowed.
    isymm.eq.1.or.isymm.eq.3 mean a toroidal geometry case, i.e. with a toroidal (out-of-plane) magnetic field component.
    isymm.eq.2.or.isymm.eq.4 mean a cylindrical geometry case, i.e. no toroidal magnetic field component. To be used in b2ag.dat.
    

.. index:: b2stbc_coreregn*

.. index:: b2stbc_coreregno, b2stbc_coreregn2
.. c

``b2stbc_coreregn*``

  - ``b2stbc_coreregno``  -     type: ``integer``    default: ``1``

  - ``b2stbc_coreregn2``  -     type: ``integer``    default: ``4``


    coreregno is the boundary index of the core boundary in the input files b2ah.dat and b2mn.dat. For standard single-null and double-null cases, the default value of coreregno is 1. For a straight geometry or limiter case, the default value of coreregno is 0.
    coreregn2 is the boundary index of the second core boundary in case of a double-null geometry, and is not used otherwise.
    
.. index::
   single: b2stbc_coreregn*; b2stbc_coreregno
   single: b2stbc_coreregn*; b2stbc_coreregn2


.. index:: b2stbc_pfrregno*

.. index:: b2stbc_pfrregno1, b2stbc_pfrregno2
.. c

``b2stbc_pfrregno*``

  - ``b2stbc_pfrregno1``  -     type: ``integer``    default: ``0``

  - ``b2stbc_pfrregno2``  -     type: ``integer``    default: ``2``


    pfrregno1 is the boundary index of the first half of the private flux region boundary on which feedback is being applied (through b2stbc\_ndes or b2stbc\_private\_flux\_puff) in the input files b2ah.dat and b2mn.dat. pfrregno2 is the second half of the same private flux region. For a standard single null, the pair should be (0,2). For a standard double-null, the lower private flux region is labelled with the pair (0,5), and the upper private flux region with the pair (2,3). One can use only one private flux region by setting pfrregno1.eq.pfrregno2.
    
.. index::
   single: b2stbc_pfrregno*; b2stbc_pfrregno1
   single: b2stbc_pfrregno*; b2stbc_pfrregno2


.. index:: b2stbc_solregno

``b2stbc_solregno``    type: ``integer``    default: ``3``
    solregno is the boundary index of the SOL North boundary in the input files b2ah.dat and b2mn.dat. For a standard single-null case, solregno is 3. For a standard double-null case, solregno for the outer SOL North boundary would be 7.
    

.. index:: b2agmt_1d_width

``b2agmt_1d_width``    type: ``real``    default: ``1.0``
    For 1-D cases, gives the width of the domain (in m) in the third (toroidal) dimension.
    

.. index:: b2stbr_first_flight_no_of_start_points

``b2stbr_first_flight_no_of_start_points``    type: ``integer``    default: ``2*(nx+2)+2*max(nncut,1)*(ny+2)``
    When the first flight model is turned on, this number must be greater than or equal to the num
    ber of boundary cells on the mesh. Only in cases with special geometries (i.e. limiters, islands, ...) need it be increased beyond the default value above. This variable is only used within the first flight module.
    

.. index:: b2agfs_geom_match_dist

``b2agfs_geom_match_dist``    type: ``real``    default: ``1.0e-6``
    Distance used as the matching criterion when reading the geometry file.
    

.. index:: b2agfs_Bt_adjust

``b2agfs_Bt_adjust``    type: ``integer``    default: ``0``
    If the mesh is offset (See b2agfs\_xoffset, b2agfs\_yoffset below) and Bt\_adjust.eq.1, then the magnetic field is recomputed for toroidal geometries, keeping the pitch constant but changing the toroidal field magnitude according to Bt = Bt0/R. To be used in b2ag.dat.
    

.. index:: b2agfs_Bt_rescale

``b2agfs_Bt_rescale``    type: ``real``    default: ``1.0``
    The magnetic field will be multiplied by Bt\_rescale. All components of the field are scaled together. To be used in b2ag.dat.
    

.. index:: b2agfs_pit_rescale

``b2agfs_pit_rescale``    type: ``real``    default: ``1.0``
    The magnetic field line pitch will be multiplied by pit\_rescale.
    This means that the poloidal field component is multiplied by pit\_rescale, while the toroidal field component is left unchanged. To reverse the plasma current direction, set pit\_rescale to -1.0.
    The sign convention used is that a positive poloidal field points in the direction of increasing <ix>. Be mindful however that, when inverting the sign of the poloidal magnetic field, you are also inverting the direction of the parallel velocity. You will then need to use the 'b2mndr\_inverse\_ua' switch to correct for that. To be used in b2ag.dat.
    

.. index:: b2agfs_Bt_reversal

``b2agfs_Bt_reversal``    type: ``integer``    default: ``0``
    If Bt\_reversal.eq.1, then the sign of the toroidal field component only is reversed. The sign convention used is that a positive toroidal field leads to a Bx(grad(B)) direction pointing down, so B is out of the page when looking at the usual view of the poloidal plane with the center line on the left. To be used in b2ag.dat.
    

.. index:: b2agfs_min_pitch

``b2agfs_min_pitch``    type: ``real``    default: ``1.0``
    Minimum allowed value for the pitch angle (in degrees) at the plates.
    

.. index:: b2agfs_.offset

.. index:: b2agfs_xoffset, b2agfs_yoffset
.. c

``b2agfs_.offset``

  - ``b2agfs_xoffset``  -     type: ``real``    default: ``0.0``

  - ``b2agfs_yoffset``  -     type: ``real``    default: ``0.0``


    xoffset and yoffset are offsets of the basis mesh in the x- and y-direction respectively. The mesh will be translated by (xoffset,yoffset) if any of the two is non-zero from its position given in the local\_sonnet (See 'b2agfs\_geometry' above) file.
    To be used in b2ag.dat.
    
.. index::
   single: b2agfs_.offset; b2agfs_xoffset
   single: b2agfs_.offset; b2agfs_yoffset


.. index:: b2agfs_.rescale

.. index:: b2agfs_xrescale, b2agfs_yrescale
.. c

``b2agfs_.rescale``

  - ``b2agfs_xrescale``  -     type: ``real``    default: ``1.0``

  - ``b2agfs_yrescale``  -     type: ``real``    default: ``1.0``


    Rescaling factors of the x- and y- coordinates of the basis mesh.
    To be used in b2ag.dat.
    
.. index::
   single: b2agfs_.rescale; b2agfs_xrescale
   single: b2agfs_.rescale; b2agfs_yrescale


.. index:: b2agfs_nncut

``b2agfs_nncut``    type: ``integer``    default: ``See description (integer)``
    Number of topological cuts in geometry. Needed only to force a different value from the one computed automatically by b2ag.
    

.. index:: b2agfs_*cut

.. index:: b2agfs_leftcut, b2agfs_rightcut, b2agfs_bottomcut, b2agfs_topcut
.. c

``b2agfs_*cut``

  - ``b2agfs_leftcut``  -     type: ``integer``    default: ``See description (integer)``

  - ``b2agfs_rightcut``  -     type: ``integer``    default: ``See description (integer)``

  - ``b2agfs_bottomcut``  -     type: ``integer``    default: ``See description (integer)``

  - ``b2agfs_topcut``  -     type: ``integer``    default: ``See description (integer)``


    Parameters describing the position and extent of the first topological cut, i.e. corresponding to the first X-point. Needed only to force different values from the ones computed automatically by b2ag.
    leftcut is the poloidal index of cells directly to the RIGHT of the left branch of the cut.
    rightcut is the poloidal index of cells directly to the RIGHT of the right branch of the cut.
    bottomcut is the radial index of cells directly below the cut.
    topcut is the radial index of cells directly above the cut.
    
.. index::
   single: b2agfs_*cut; b2agfs_leftcut
   single: b2agfs_*cut; b2agfs_rightcut
   single: b2agfs_*cut; b2agfs_bottomcut
   single: b2agfs_*cut; b2agfs_topcut


.. index:: b2agfs_*cut2

.. index:: b2agfs_leftcut2, b2agfs_rightcut2, b2agfs_bottomcut2, b2agfs_topcut2
.. c

``b2agfs_*cut2``

  - ``b2agfs_leftcut2``  -     type: ``integer``    default: ``See description (integer)``

  - ``b2agfs_rightcut2``  -     type: ``integer``    default: ``See description (integer)``

  - ``b2agfs_bottomcut2``  -     type: ``integer``    default: ``See description (integer)``

  - ``b2agfs_topcut2``  -     type: ``integer``    default: ``See description (integer)``


    Parameters describing the position and extent of the second topological cut, i.e. corresponding to the second X-point. Needed only to force different values from the ones computed automatically by b2ag.
    leftcut2 is the poloidal index of cells directly to the RIGHT of the left branch of the second cut.
    rightcut2 is the poloidal index of cells directly to the RIGHT of the right branch of the second cut.
    bottomcut is the radial index of cells directly below the second cut.
    topcut is the radial index of cells directly above the second cut.
    
.. index::
   single: b2agfs_*cut2; b2agfs_leftcut2
   single: b2agfs_*cut2; b2agfs_rightcut2
   single: b2agfs_*cut2; b2agfs_bottomcut2
   single: b2agfs_*cut2; b2agfs_topcut2


.. index:: b2agdr_n.iso.

.. index:: b2agdr_nxiso1, b2agdr_nxiso2, b2agdr_nyiso1, b2agdr_nyiso2
.. c

``b2agdr_n.iso.``

  - ``b2agdr_nxiso1``  -     type: ``integer``    default: ``-2``

  - ``b2agdr_nxiso2``  -     type: ``integer``    default: ``-2``

  - ``b2agdr_nyiso1``  -     type: ``integer``    default: ``-2``

  - ``b2agdr_nyiso2``  -     type: ``integer``    default: ``-2``


    Range of an optional isolated region to be included in the geometry.
    The isolated region will extend over the cell range spanned by (nxiso1:nxiso2,nyiso1:nyiso2).
    If only some of the four coordinates are given, the region is made to extent from the given coordinates to the end of the grid.
    Neighbourhood arrays and region indices are automatically adjusted.
    
.. index::
   single: b2agdr_n.iso.; b2agdr_nxiso1
   single: b2agdr_n.iso.; b2agdr_nxiso2
   single: b2agdr_n.iso.; b2agdr_nyiso1
   single: b2agdr_n.iso.; b2agdr_nyiso2


.. index:: b2us_write_b2fgmtry_us

``b2us_write_b2fgmtry_us``    type: ``integer``    default: ``1``
    Switch for conversion with b2us; can be specified in the b2mn.dat file read by b2us during case conversion to unstructured format. When set to 1, unstructured b2fgmtry\_us file is written by b2us. When set to 0, it is not.
    

.. index:: b2us_write_b2fstati_us

``b2us_write_b2fstati_us``    type: ``integer``    default: ``1``
    Switch for conversion with b2us; can be specified in the b2mn.dat file read by b2us during case conversion to unstructured format. When set to 1, unstructured b2fstati\_us file is written by b2us. When set to 0, it is not.
    

.. index:: conv_triangles_old_co

``conv_triangles_old_co``    type: ``integer``    default: ``0``
    Switch for conversion with b2us; can be specified in the b2mn.dat file read by b2us during case conversion to unstructured format. When converting a structured case with b2us and conv\_triangles\_old\_co = 1, the coordinates of the nodes of the triangles from the original fort.33 file will be used in the unstructured format. Otherwise, the triangular mesh will be exactly matched to the B2.5 grid.  Setting the switch to 1 may be required when converting triangle grids that include extreme slender/skewed triangles (typically manifested through FOLNEUT errors at runtime after case conversion).
    

.. index:: b2us_auto_midplane_det

``b2us_auto_midplane_det``    type: ``integer``    default: ``1``
    Switch for conversion with b2us; can be specified in the b2mn.dat file read by b2us during case conversion to unstructured format. When set to 1, b2us will automatically try to reconstruct outer and inner midplane from the geometry (magnetic field and cell coordinates), and write the corresponding coordinates in b2.user.parameters. When set to 0, the IMP and OMP definition will be based on the values of b2mwti\_jxi, b2mwti\_jxa, b2mwti\_jsep.
    

.. index:: b2us_prep_Qalfmin

``b2us_prep_Qalfmin``    type: ``real``    default: ``1e-3``
    If abs(cos(alpha)\*bx).ge.b2us\_prep\_Qalfmin, the beta angle is assigned to zero during writing of b2fgmtry.
    If abs(cos(alpha)\*bx).lt.b2us\_prep\_Qalfmin, boundary faces are treated like field-aligned faces in BCMOM=13, BCCON=14, BCENE=15 (style=1), BCENI=15 (style=0) and BCPOT=11. Leakage coefficients (if they are needed) are set equal to b2us\_prep\_Qalfmax.
    

.. index:: b2us_prep_Qalfmax

``b2us_prep_Qalfmax``    type: ``real``    default: ``1e-3``
    If abs(cos(alpha)\*bx).ge.b2us\_prep\_Qalfmin .and. abs(cos(alpha)\*bx).lt.b2us\_prep\_Qalfmax, fcPbs is set equal to b2us\_prep\_Qalfmax\*fcS for boundary faces during writing of b2fgmtry.
    

.. index:: b2us_prep_mod_hc

``b2us_prep_mod_hc``    type: ``integer``    default: ``0``
    If b2us\_prep\_mod\_hc.eq.1 then the length between cell face center and neighboring cell centers (fcHc) will be modified.	It will be the same for neighboring boundary faces belonging to the same flux tube. For all boundary faces it will be recalculated to decrease the distance between boundary face and guard cell centers.
    

.. index:: b2us_prep_set_beta_0

``b2us_prep_set_beta_0``    type: ``integer``    default: ``0``
    If b2us\_prep\_set\_beta\_0.eq.1, the beta angle will be assigned to zero for faces between boundary cells belonging to same shaved flux tube.
    

.. index:: 
   single: Geometry; b2agfs_geometry
   single: Geometry; b2mwti_jxa
   single: Geometry; b2mwti_jxi
   single: Geometry; b2mwti_jsep
   single: Geometry; b2agmx_pbs_from_basis_mesh
   single: Geometry; b2agdr_redef_pbs
   single: Geometry; b2mndr_redef_pbs
   single: Geometry; b2agfs_periodic_bc
   single: Geometry; b2agsi_isymm
   single: Geometry; b2stbc_coreregn*
   single: Geometry; b2stbc_pfrregno*
   single: Geometry; b2stbc_solregno
   single: Geometry; b2agmt_1d_width
   single: Geometry; b2stbr_first_flight_no_of_start_points
   single: Geometry; b2agfs_geom_match_dist
   single: Geometry; b2agfs_Bt_adjust
   single: Geometry; b2agfs_Bt_rescale
   single: Geometry; b2agfs_pit_rescale
   single: Geometry; b2agfs_Bt_reversal
   single: Geometry; b2agfs_min_pitch
   single: Geometry; b2agfs_.offset
   single: Geometry; b2agfs_.rescale
   single: Geometry; b2agfs_nncut
   single: Geometry; b2agfs_*cut
   single: Geometry; b2agfs_*cut2
   single: Geometry; b2agdr_n.iso.
   single: Geometry; b2us_write_b2fgmtry_us
   single: Geometry; b2us_write_b2fstati_us
   single: Geometry; conv_triangles_old_co
   single: Geometry; b2us_auto_midplane_det
   single: Geometry; b2us_prep_Qalfmin
   single: Geometry; b2us_prep_Qalfmax
   single: Geometry; b2us_prep_mod_hc
   single: Geometry; b2us_prep_set_beta_0

.. index:: Run

Run
===
.. index:: b2mndr_id

.. index:: b2mndr_ids_path, b2mndr_pulse_number, b2mndr_shot_number, b2mndr_run_number, b2mndr_database, b2mndr_device, b2mndr_user
.. c

``b2mndr_id``

  - ``b2mndr_ids_path``  -     type: ``character*256``    default: ``See description``

  - ``b2mndr_pulse_number``  -     type: ``integer``    default: ``0``

  - ``b2mndr_shot_number``  -     type: ``integer``    default: ``0``

  - ``b2mndr_run_number``  -     type: ``integer``    default: ``0``

  - ``b2mndr_database``  -     type: ``string``    default: ``$(DEVICE)``

  - ``b2mndr_device``  -     type: ``string``    default: ``$(DEVICE)``

  - ``b2mndr_user``  -     type: ``string``    default: ``$(USER)``


    These switches serve as identification for the simulation. They can be inherited from the SOLPS-GUI:
    IDS path : Only available if using IMAS Access Layer 5. The directory path where the IMAS data entry will be saved. Supersedes the pulse (previously shot) and run numbers. May begin with "$HOME", "$IMASDIR", or "$SOLPSTOP", that will be parsed by the code. If it begins with a '/', is understood as an absolute path, otherwise will be prefixed with the $IMASDIR environment variable. Defaults to the last line in the 'shotnumber.history' file if present, and to $IMASDIR/${pulse\_number}/${run\_number} otherwise or if $IMASDIR is modified from its default value by the switches below.
    Pulse number : Pulse number identifying the run (supersedes b2mndr\_shot\_number). Defaults to the last number found in shotnumber.history, or 0 if the file is not found. Must be positive and non-zero if an IMAS data entry is requested. If using IMAS Access Layer 4, cannot exceed 214748.
    Run number : The number of the run. Must be positive or zero. If using IMAS Access Layer 4, limited to 5 digits (i.e. span from 0 to 99999).
    Database : IMAS IDS database name (supersedes b2mndr\_device). Defaults to 'solps-iter' if $DEVICE if undefined. If $DEVICE is 'iter', the code internally changes it to 'ITER' to follow the IMAS convention. Can be used to rebuild the IMASDIR path.
    User : The user who ran the simulation. Can be used to rebuild the IMASDIR path.
    
.. index::
   single: b2mndr_id; b2mndr_ids_path
   single: b2mndr_id; b2mndr_pulse_number
   single: b2mndr_id; b2mndr_shot_number
   single: b2mndr_id; b2mndr_run_number
   single: b2mndr_id; b2mndr_database
   single: b2mndr_id; b2mndr_device
   single: b2mndr_id; b2mndr_user


.. index:: b2aidr_read_b2fstate

``b2aidr_read_b2fstate``    type: ``integer``    default: ``0``
    If read\_b2fstate.ne.0, b2aidr will read an existing b2fstate file and append to it a flat state description for additional new species being introduced in the run.
    

.. index:: b2mndr_ntim

``b2mndr_ntim``    type: ``integer``    default: ``1``
    Number of timesteps desired in this run. If ntim.eq.0, the code simply reads the input file and creates the b2fplasma and b2fstate files corresponding to the present plasma state.
    

.. index:: b2mndr_dtim

``b2mndr_dtim``    type: ``real``    default: ``1.0``
    Timestep (in seconds).
    

.. index:: b2mndr_d*

.. index:: b2mndr_delta_max, b2mndr_delta_min, b2mndr_dt_change_dec, b2mndr_dt_change_inc, b2mndr_dt_max, b2mndr_dt_min
.. c

``b2mndr_d*``

  - ``b2mndr_delta_max``  -     type: ``real``    default: ``0.0``

  - ``b2mndr_delta_min``  -     type: ``real``    default: ``0.0``

  - ``b2mndr_dt_change_dec``  -     type: ``real``    default: ``1.0``

  - ``b2mndr_dt_change_inc``  -     type: ``real``    default: ``1.0``

  - ``b2mndr_dt_max``  -     type: ``real``    default: ``1.0e+01``

  - ``b2mndr_dt_min``  -     type: ``real``    default: ``1.0e-30``


    One of the dynamic timestep control parameters. Only active if both delta\_max and delta\_min are nonzero. The timestep is increased by a factor dt\_change\_inc or decreased by a factor dt\_change\_dec, within the bounds [dt\_min, dt\_max], according to whether the largest instantaneous change in all equations is smaller than delta\_min or larger than delta\_max, respectively.
    
.. index::
   single: b2mndr_d*; b2mndr_delta_max
   single: b2mndr_d*; b2mndr_delta_min
   single: b2mndr_d*; b2mndr_dt_change_dec
   single: b2mndr_d*; b2mndr_dt_change_inc
   single: b2mndr_d*; b2mndr_dt_max
   single: b2mndr_d*; b2mndr_dt_min


.. index:: b2mndr_stim

``b2mndr_stim``    type: ``real``    default: ``0.0``
    stim specifies the initial time --- default 0.
    If set to a positive or zero value, this overwrites the time value read from b2fstati.
    If set to a negative value, the run continues from the time read in b2fstati. In that case, the tracing data is appended to the existing files, otherwise the tracing files are overwritten.
    

.. index:: b2mndr_etim

``b2mndr_etim``    type: ``real``    default: ``0.0``
    etim specifies the end time. Only active if etim > stim.
    

.. index:: b2mndt_nstg.

.. index:: b2mndt_nstg0, b2mndt_nstg1, b2mndt_nstg2
.. c

``b2mndt_nstg.``

  - ``b2mndt_nstg0``  -     type: ``integer``    default: ``1``

  - ``b2mndt_nstg1``  -     type: ``integer``    default: ``1``

  - ``b2mndt_nstg2``  -     type: ``integer``    default: ``1``


    Time-dependent mode and iterative mode switches. The basic code timestep proceeds as follows:

    | ..test input arguments
    | ..compute auxiliary quantities
    | ..prepare source computation
    | ..do i0=1,nstg0
    |  ..compute log-log linearised rate coefficients
    |  ..do i1=1,nstg1
    |   ..compute source linearisation (Eirene call)
    |   ..do i2=1,nstg2
    |    ..perform one inner iteration (on fluid equations)
    |    ..re-compute auxiliary quantities
    |    ..produce monitoring output
    |   ..enddo
    |  ..enddo
    | ..enddo

    This can be completed by the the 'b2mndt\_nstg\_ares??' switches. See 'Numerics' section for details.
    It is recommended to use these inner iterations when running in time-dependent mode (b2mndt\_style=2) to make residuals converge within each time-step.
    
.. index::
   single: b2mndt_nstg.; b2mndt_nstg0
   single: b2mndt_nstg.; b2mndt_nstg1
   single: b2mndt_nstg.; b2mndt_nstg2


.. index:: b2news_no_solve

``b2news_no_solve``    type: ``integer``    default: ``0``
    If no\_solve.eq.1, then the code is run without actually solving any equations. All secondary and dependent data is computed.
    The nstg(0:2) array is overwritten to '1's. The simulation time will not be updated. The code will compute fluxes, sources, transport coefficients, etc... 'ntim' times but not update the basic plasma quantities. Additionally, if no\_solve is set to a negative value, then only some equations are solved (simulation time and nstg arrays will behave normally).
    no\_solve.eq.-1 will activate the parallel momentum equations only.
    no\_solve.eq.-2 will activate the density equations only.
    no\_solve.eq.-4 will activate the potential equation only. (Active only if poteq.eq.1, otherwise, the behaviour dictated by the poteq setting applies).
    no\_solve.eq.-8 will activate the heat equations only. These can be combined. For example, no\_solve.eq.-3 will activate the parallel momentum and particle conservation equations.
    If the no\_solve switch requires an equation not to be solved, the settings in the corresponding solvexx arrays from b2.numerics.parameters are moot.
    The latter are reserved for fine-tuning numerical diagnostics.
    If wishing to toggle whether to solve or not to solve each equation separately, one should set, in the b2.numerics.parameters input file, the SOLVEMO, SOLVEMT, SOLVECO, SOLVEE, SOLVEEI, SOLVEET and SOLVEPO arrays, respectively, for each of the parallel momentum equations, the total momentum equation, each density equation, the electron and ion heat equations, and the total energy equation.
    When running in time-dependent mode, the total energy and total momentum equations are not solved.
    The table below shows which combination of equations will be solved	depending on the value of switch 'b2news\_no\_solve'
    \*----------------------------------------------------
    \*        | value |  co  |  mo  |  he  |  hi  |  po  |
    \*----------------------------------------------------
    \*        |   0   |  +   |  +   |  +   |  +   |  +   |
    \*----------------------------------------------------
    \*        |   1   |  -   |  -   |  -   |  -   |  -   |
    \*----------------------------------------------------
    \*        |  -1   |  -   |  +   |  -   |  -   |  -   |
    \*----------------------------------------------------
    \*        |  -2   |  +   |  -   |  -   |  -   |  -   |
    \*----------------------------------------------------
    \*        |  -3   |  +   |  +   |  -   |  -   |  -   |
    \*----------------------------------------------------
    \*        |  -4   |  -   |  -   |  -   |  -   |  +   |
    \*----------------------------------------------------
    \*        |  -5   |  -   |  +   |  -   |  -   |  +   |
    \*----------------------------------------------------
    \*        |  -6   |  +   |  -   |  -   |  -   |  +   |
    \*----------------------------------------------------
    \*        |  -7   |  +   |  +   |  -   |  -   |  +   |
    \*----------------------------------------------------
    \*        |  -8   |  -   |  -   |  +   |  +   |  -   |
    \*----------------------------------------------------
    \*        |  -9   |  -   |  +   |  +   |  +   |  -   |
    \*----------------------------------------------------
    \*        | -10   |  +   |  -   |  +   |  +   |  -   |
    \*----------------------------------------------------
    \*        | -11   |  +   |  +   |  +   |  +   |  -   |
    \*----------------------------------------------------
    \*        | -12   |  -   |  -   |  +   |  +   |  +   |
    \*----------------------------------------------------
    \*        | -13   |  -   |  +   |  +   |  +   |  +   |
    \*----------------------------------------------------
    \*        | -14   |  +   |  -   |  +   |  +   |  +   |
    \*----------------------------------------------------
    

.. index:: b2mndr_cpu

``b2mndr_cpu``    type: ``real``    default: ``0.0``
    CPU limit. If cpu.eq.0.0, no CPU limit is enforced. Otherwise, the code stops smoothly after it has been running for at least 'cpu' CPU seconds.
    

.. index:: b2mndr_elapsed

``b2mndr_elapsed``    type: ``real``    default: ``0.0``
    Elapsed time limit. Is elapsed.eq.0.0, no time limit is enforced.
    Otherwise, the code stops smoothly after is has been running for at least 'elapsed' wall clock seconds.
    

.. index:: b2mndr_savecpu

``b2mndr_savecpu``    type: ``real``    default: ``3600.0``
    If savecpu.gt.0.0, CPU time interval after which save files plasmastate.xxxx are written. Other additional options for writing of the checkpointing files are available by means of the b2mndt\_ntim\_save and/or b2mndr\_plasmatim switches.
    These can be used, in conjunction with the b2co.exe instruction, to recover a crashed run.
    

.. index:: b2mndr_ismain

``b2mndr_ismain``    type: ``real``    default: ``1``
    ismain identifies the index of the main plasma species.
    It must hold that ismain is not a neutral species.
    

.. index:: b2news_facdrift*

.. index:: b2news_facdrift_dec, b2news_facdrift_inc, b2news_facdrift_start, b2news_facdrift_target
.. c

``b2news_facdrift*``

  - ``b2news_facdrift_dec``  -     type: ``real``    default: ``0.0``

  - ``b2news_facdrift_inc``  -     type: ``real``    default: ``1.0``

  - ``b2news_facdrift_start``  -     type: ``real``    default: ``0.0``

  - ``b2news_facdrift_target``  -     type: ``real``    default: ``0.0``


    Ramping parameters for facdrift, which multiplies the diamagnetic terms as well as the ion inertia current. The code is started on the first time step with facdrift=facdrift\_start. If facdrift\_target.ne.facdrift\_start, then, on each time step, facdrift is multiplied by facdrift\_inc. If the code does not converge on the timestep, facdrift is decreased by facdrift\_dec. A facdrift profile is also possible, see Numerics section for details.
    The ion-neutral friction current requires either facdrift or fac\_ExB to be turned on as well.
    
.. index::
   single: b2news_facdrift*; b2news_facdrift_dec
   single: b2news_facdrift*; b2news_facdrift_inc
   single: b2news_facdrift*; b2news_facdrift_start
   single: b2news_facdrift*; b2news_facdrift_target


.. index:: b2news_facExB_*

.. index:: b2news_facExB_dec, b2news_facExB_inc, b2news_facExB_start, b2news_facExB_target
.. c

``b2news_facExB_*``

  - ``b2news_facExB_dec``  -     type: ``real``    default: ``0.0``

  - ``b2news_facExB_inc``  -     type: ``real``    default: ``1.0``

  - ``b2news_facExB_start``  -     type: ``real``    default: ``0.0``

  - ``b2news_facExB_target``  -     type: ``real``    default: ``0.0``


    Ramping parameters for facExB, which multiplies the ExB terms. Same treatment as above for facdrift. Can be superseded by b2news\_ExB to set a constant value throughout the run.
    
.. index::
   single: b2news_facExB_*; b2news_facExB_dec
   single: b2news_facExB_*; b2news_facExB_inc
   single: b2news_facExB_*; b2news_facExB_start
   single: b2news_facExB_*; b2news_facExB_target


.. index:: b2news_facvis_*

.. index:: b2news_facvis_dec, b2news_facvis_inc, b2news_facvis_start, b2news_facvis_target
.. c

``b2news_facvis_*``

  - ``b2news_facvis_dec``  -     type: ``real``    default: ``0.0``

  - ``b2news_facvis_inc``  -     type: ``real``    default: ``1.0``

  - ``b2news_facvis_start``  -     type: ``real``    default: ``0.0``

  - ``b2news_facvis_target``  -     type: ``real``    default: ``0.0``


    Ramping parameters for facvis, which multiplies the drift viscosity terms. Same treatment as above for facdrift. Can be superseded by b2news\_vis to set a constant value throughout the run.
    
.. index::
   single: b2news_facvis_*; b2news_facvis_dec
   single: b2news_facvis_*; b2news_facvis_inc
   single: b2news_facvis_*; b2news_facvis_start
   single: b2news_facvis_*; b2news_facvis_target


.. index:: b2srdt_*_namelist

.. index:: b2stbc_boundary_namelist, b2stbr_neutrals_namelist, b2srdt_numerics_namelist, b2tqna_transport_namelist, b2optim_namelist
.. c

``b2srdt_*_namelist``

  - ``b2stbc_boundary_namelist``  -     type: ``integer``    default: ``See description``

  - ``b2stbr_neutrals_namelist``  -     type: ``integer``    default: ``0``

  - ``b2srdt_numerics_namelist``  -     type: ``integer``    default: ``0``

  - ``b2tqna_transport_namelist``  -     type: ``integer``    default: ``0``

  - ``b2optim_namelist``  -     type: ``integer``    default: ``0``


    Namelist file indicators. If xxx\_namelist.eq.1, then the code looks for the file b2.xxx.parameters, in which it expects to find the xxx namelist.
    In the case of boundary\_namelist, defaults to 1 for double-null and snowflake geometries, 0 otherwise.
    
.. index::
   single: b2srdt_*_namelist; b2stbc_boundary_namelist
   single: b2srdt_*_namelist; b2stbr_neutrals_namelist
   single: b2srdt_*_namelist; b2srdt_numerics_namelist
   single: b2srdt_*_namelist; b2tqna_transport_namelist
   single: b2srdt_*_namelist; b2optim_namelist


.. index:: b2sral_inputfile

``b2sral_inputfile``    default: ``0``
    Profiles file indicator. If b2sral\_inputfile.eq.1, then the code looks for the file b2.sources.profile in which it expects to find the 'profile' namelist.
    This namelist will contain profiles of sources measured from the outer midplane separatrix location, which is set with the [RZ]OMP variables in b2.user.parameters.
    

.. index:: b2tqna_inputfile

``b2tqna_inputfile``    type: ``integer``    default: ``0``
    Profiles file indicator. If b2tqna\_inputfile.eq.1, then the code looks for the file b2.transport.inputfile, in which it expects to find the transport namelist.
    This namelist will contain profiles of transport parameters measured from the outer midplane separatrix location, which is set with the [RZ]OMP variables in b2.user.parameters.
    

.. index:: b2mndr_eirene

``b2mndr_eirene``    type: ``integer``    default: ``0``
    Turns on coupling with the Eirene Monte Carlo neutral code if nonzero.
    To be used, the code must be compiled with the -DB25\_EIRENE option.
    

.. index:: b2mndr_astra

``b2mndr_astra``    type: ``integer``    default: ``0``
    Turns on coupling with the ASTRA core transport code if nonzero.
    To be used, the code must be compiled with the -DASTRA option.
    

.. index:: b2mndr_rescale_neutrals_sources

``b2mndr_rescale_neutrals_sources``    type: ``real``    default: ``1.0``
    Multiplier to the neutral sources (either computed by Eirene or the corresponding rate coefficients).
    

.. index:: b2mndr_rescale_neutrals

``b2mndr_rescale_neutrals``    type: ``real``    default: ``1.0``
    Multiplier to the neutral density on the first timestep.
    

.. index:: b2mndr_density_rescale

``b2mndr_density_rescale``    type: ``real``    default: ``1.0``
    Multiplier of all densities on the first timestep.
    

.. index:: b2stbr_core_sources_rescale

``b2stbr_core_sources_rescale``    type: ``real``    default: ``1.0``
    Multiplier to the totally ionised species sources at the core boundary.
    

.. index:: b2mndt_density_control

``b2mndt_density_control``    type: ``integer``    default: ``0``
    Feedback on the total heavy particle density. If density\_control.ne.0, the sum of all densities is kept constant.
    

.. index:: b2stbc_feedback

``b2stbc_feedback``    type: ``integer``    default: ``0``
    If feedback.eq.1, turns on feedback mode for the boundary conditions.
    See Physics section for more details. Equivalent to LFEEDBACK=.true. in the b2.boundary.parameters namelist.
    

.. index:: b2stbc_ncallfeedback

``b2stbc_ncallfeedback``    type: ``integer``    default: ``0``
    Timestep index after which the feedback in b2stbc is activated. NOT YET CONVERTED IN WG CODE
    

.. index:: b2stbr_first_flight

``b2stbr_first_flight``    type: ``integer``    default: ``0``
    If first\_flight.ne.0, turns on the first flight model. See Physics section for additional details.
    

.. index:: b2ytdr_ns

``b2ytdr_ns``    type: ``integer``    default: ``ns``
    New number of species desired when creating a new initial state file using b2yt.exe. Must be specified within b2yt.dat.
    

.. index:: b2ytdr_jsep1

``b2ytdr_jsep1``    type: ``integer``    default: ``nx1/2``
    Radial index of separatrix in the converted grid. Must be specified within b2yt.dat. Only applies when converting linear geometries.
    

.. index:: b2ytdr_ndepth1

``b2ytdr_ndepth1``    type: ``integer``    default: ``ndepth_nml``
    New resolution of target depth desired when creating a new initial state file using b2yt.exe. Must be specified within b2yt.dat.
    

.. index:: b2ytdr_rescale_neutrals

``b2ytdr_rescale_neutrals``    type: ``real``    default: ``1.0``
    Rescaling of neutral densities by rescale\_neutrals when creating a new initial state file using b2yt.exe. Must be specified within b2yt.dat.
    

.. index:: b2ytdr_non_commensurate

``b2ytdr_non_commensurate``    type: ``integer``    default: ``0``
    When set to 1, b2yt will attempt to interpolate a plasma solution and create new input files for a new grid which is not commensurate to the original grid, but still has the same topology.
    Must be specified within b2yt.dat.
    

.. index:: 
   single: Run; b2mndr_id
   single: Run; b2aidr_read_b2fstate
   single: Run; b2mndr_ntim
   single: Run; b2mndr_dtim
   single: Run; b2mndr_d*
   single: Run; b2mndr_stim
   single: Run; b2mndr_etim
   single: Run; b2mndt_nstg.
   single: Run; b2news_no_solve
   single: Run; b2mndr_cpu
   single: Run; b2mndr_elapsed
   single: Run; b2mndr_savecpu
   single: Run; b2mndr_ismain
   single: Run; b2news_facdrift*
   single: Run; b2news_facExB_*
   single: Run; b2news_facvis_*
   single: Run; b2srdt_*_namelist
   single: Run; b2sral_inputfile
   single: Run; b2tqna_inputfile
   single: Run; b2mndr_eirene
   single: Run; b2mndr_astra
   single: Run; b2mndr_rescale_neutrals_sources
   single: Run; b2mndr_rescale_neutrals
   single: Run; b2mndr_density_rescale
   single: Run; b2stbr_core_sources_rescale
   single: Run; b2mndt_density_control
   single: Run; b2stbc_feedback
   single: Run; b2stbc_ncallfeedback
   single: Run; b2stbr_first_flight
   single: Run; b2ytdr_ns
   single: Run; b2ytdr_jsep1
   single: Run; b2ytdr_ndepth1
   single: Run; b2ytdr_rescale_neutrals
   single: Run; b2ytdr_non_commensurate

.. index:: Physics

Physics
=======
.. index:: b2siav_addvis

``b2siav_addvis``    type: ``real``    default: ``1.0``
    Multiplier to heat flux contribution to divergence of viscosity tensor in the momentum equation.
    

.. index:: b2siav_addvis1

``b2siav_addvis1``    type: ``real``    default: ``1.0``
    When not equal to '0.0', adds contribution to divergence of viscosity tensor coming from x-variations in B.
    

.. index:: b2siav_style_qip

``b2siav_style_qip``    type: ``integer``    default: ``0``
    If style\_qip.eq.1, adds a classical ion heat conductivity term to the heat flux used to compute the heat viscosity current (see manual for full details).
    

.. index:: b2npmo_b2sifr_

``b2npmo_b2sifr_``    type: ``integer``    default: ``1``
    If b2sigp\_style is set to '2', this switch has no effect.
    When set to '1', the new correct form of the friction force is used, applicable for non-hydrogenic plasmas or hydrogenic mixtures.
    The value '0' corresponds to the old SOLPS5.0 treatment. Not recommended unless wanting to recover older 5.0 results.
    

.. index:: b2sihs_istyle_Joule_heating

``b2sihs_istyle_Joule_heating``    type: ``integer``    default: ``1``
    When set to '1', there is no radial contribution in Joule heating because there are no physical reasons to take it into account.
    The value '0' corresponds to the old SOLPS5.0 treatment.
    

.. index:: b2sian_phm0

``b2sian_phm0``    type: ``real``    default: ``1.0``
    Multiplier to the parallel momentum source term associated with the anomalous current. It is recommended '1.0'. Only active if both the ExB and diamagnetic drifts are turned on.
    The value '0.0' corresponds to the old SOLPS5.0 treatment.
    

.. index:: b2sicf_phm0

``b2sicf_phm0``    type: ``real``    default: ``1.0``
    Multiplier of the centrifugal force term. It is recommended '1.0'.
    The value '0.0' corresponds to the old SOLPS5.0 treatment.
    

.. index:: b2sicf_phm1

``b2sicf_phm1``    type: ``real``    default: ``1.0``
    Multiplier of the centrifugal force correction term due to linearization.
    It is recommended '1.0'.
    The value '0.0' corresponds to the old SOLPS5.0 treatment.
    

.. index:: b2t*_anomalous

.. index:: b2tfhe_anomalous, b2tanml_anomalous
.. c

``b2t*_anomalous``

  - ``b2tfhe_anomalous``  -     type: ``real``    default: ``1.0``

  - ``b2tanml_anomalous``  -     type: ``real``    default: ``1.0``


    Real parameter which determines anomalous current.
    Both b2tfhe\_anomalous and b2tanml\_anomalous point to the same switch (backward compatibility with SOLPS5.2): b2tfhe\_anomalous is checked first and only if it is not found is b2tanml\_anomalous looked for.
    If b2tfhe\_anomalous is 0 then anomalous current is switched off otherwise anomalous current is switched on, and the numerical value of b2tfhe\_anomalous acts as a multiplier to the anomalous electrical conductivity and thermo-electric coefficients provided.
    
.. index::
   single: b2t*_anomalous; b2tfhe_anomalous
   single: b2t*_anomalous; b2tanml_anomalous


.. index:: b2news_ExB

``b2news_ExB``    type: ``real``    default: ``0.0``
    Real parameter which multiplies ExB flows. If b2news\_ExB.eq.0 and b2news\_facExB\_start.eq.0 then ExB flows are switched off. If b2news\_ExB is nonzero, then ExB flows are multiplied by that constant throughout the run.
    See also Run section on switches b2news\_facExB\_... for more details. A spatial fac\_ExB profile is also possible, see Numerics section for details.
    

.. index:: b2news_vis

``b2news_vis``    type: ``real``    default: ``0.0``
    Real parameter which multiplies the viscous drift flows. If b2news\_vis.eq.0 and b2news\_facvis\_start.eq.0 then the viscous drift flows are switched off. If b2news\_vis is nonzero, then the viscous drift flows are multiplied by that constant throughout the run.
    See also Run section on switches b2news\_facvis\_... for more details. A spatial fac\_vis profile is also possible, see Numerics section for details.
    

.. index:: b2tiner_inert

``b2tiner_inert``    type: ``real``    default: ``1.0``
    Real parameter which multiplies the ion inertial current.
    

.. index:: b2tfhe_dia_cur

``b2tfhe_dia_cur``    type: ``real``    default: ``1.0``
    Real parameter which multiplies the diamagnetic current.
    

.. index:: b2tfhe_vdia_par

``b2tfhe_vdia_par``    type: ``real``    default: ``1.0``
    Real parameter which multiplies the convective heat flux due to grad B-drift of guiding centers in non-modified heat fluxes of electrons and ions.
    

.. index:: b2tfhe_neutral

``b2tfhe_neutral``    type: ``real``    default: ``0.0``
    Real parameter which multiplies the ion-neutral current.
    If b2tfhe\_neutral is 0 then the ion-neutral current is switched off otherwise the ion-neutral current is switched on.
    The ion-neutral current also requires either the diamagnetic or ExB drifts to be turned on as well.
    

.. index:: b2tinnt_fchin_in_core

``b2tinnt_fchin_in_core``    type: ``integer``    default: ``0``
    Integer switch to turn off or on the ion-neutral current in the core region (applies to coupled runs only). This is recommended in cases where the neutral densities are very low in the core region and the ion-neutral current is likely to vary widely from one iteration to the next as a result of Monte Carlo noise.
    If fchin\_in\_core.eq.0 (default), then fchin is set to zero in the core.
    If fchin\_in\_core.eq.1, then fchin is unchanged.
    fchin\_in\_core.eq.1 not yet available for WG.
    

.. index:: b2tfhe_PSch

``b2tfhe_PSch``    type: ``real``    default: ``1.0``
    Real parameter which multiplies the Pfirsch-Schlueter electron heat flux and conductivity.
    

.. index:: b2tfhe_vis_par

``b2tfhe_vis_par``    type: ``real``    default: ``0.0``
    Real parameter which multiplies the current driven by parallel viscosity.
    If b2tfhe\_vis\_par is 0 then the viscosity-driven current is switched off otherwise the viscosity-driven current is switched on.
    

.. index:: b2tfhe_vis_q

``b2tfhe_vis_q``    type: ``real``    default: ``1.0``
    Real parameter which multiplies the current driven by heat viscosity effects.
    

.. index:: b2tfhe_stochastic

``b2tfhe_stochastic``    type: ``real``    default: ``0.0``
    Real parameter which turns on stochastic current.
    If b2tfhe\_stochastic is 0 then stochastic current is switched off otherwise stochastic current is switched on.
    Not yet available for WG.
    

.. index:: b2tstch_delta

``b2tstch_delta``    type: ``real``    default: ``0.0``
    Width of the stochastic current layer (in metres), measured from the separatrix inward, along the poloidal index ixref (given by b2tqna\_ixref).
    If b2tfhe\_stochastic.ne.0, then b2tstch\_delta must be greater than zero.
    Not yet available for WG.
    

.. index:: b2tstch_sig

``b2tstch_sig``    type: ``real``    default: ``1.0``
    Multiplier to the magnetic field line stochastic diffusion coefficient, describing the stochastic conductivity.
    Not yet available for WG.
    

.. index:: b2trno_con_e_stochastic

``b2trno_con_e_stochastic``    type: ``real``    default: ``1.0``
    Multiplier to the stochastic conductivity.
    Not yet available for WG.
    

.. index:: b2trcl_lluciani

``b2trcl_lluciani``    type: ``integer``    default: ``3``
    If lluciani.ne.0, then transport coefficients on cells belonging to closed field lines are modified according to the Luciani model.
    If lluciani.eq.1, the standard connection length formulation is used.
    If lluciani.eq.2, the old SOLPS4.0 formulation is used for backward compatibility.
    If lluciani.eq.3, Spb's new form Luciani's coefficient.
    

.. index:: b2trcl_lthf21

``b2trcl_lthf21``    type: ``integer``    default: ``0``
    If lthf21.ne.0, then the heat transfer model is modified according to the 21-moment approach. This should only be used for multi-fluid runs.
    Not yet available for WG.
    

.. index:: b2trcl_lvis21

``b2trcl_lvis21``    type: ``integer``    default: ``0``
    If lvis21.ne.0, then the viscosities are modified according to the 21-moment approach. This should only be used for multi-fluid runs. This switch should not be used along with 'b2tfhe\_vis\_par' to avoid double-counting of classical viscosity effects.
    Not yet available for WG.
    

.. index:: b2tral_Zhdanov_closure

``b2tral_Zhdanov_closure``    type: ``integer``    default: ``0``
    If b2tral\_Zhdanov\_closure.eq.1, the Zhdanov-Grad module is enabled, and fully multi-ion collisional closure for the components along the magnetic field of the vector and tensor moments of the distribution function is applied for all the ions (without specifying main ions and impurities) based on the works of Zhdanov [V. M. Zhdanov, 2002] and Makarov et al. [S. O. Makarov et al., PoP 2021]. Otherwise the standard SOLPS-ITER model is applied.
    

.. index:: b2tral_zh_imp_analyt

``b2tral_zh_imp_analyt``    type: ``integer``    default: ``0``
    If b2tral\_zh\_imp\_analyt.eq.0, the Zhdanov-Grad closure method is applied by means of the explicit matrix inversion methed (EMIM).
    If b2tral\_zh\_imp\_analyt.eq.1, the improved analytical method (IAM) is applied. See [S. O. Makarov et al., PoP 2021] for details.
    This switch is subservient to b2tral\_Zhdanov\_closure.
    

.. index:: b2tral_zh_analyt_mdf

``b2tral_zh_analyt_mdf``    type: ``integer``    default: ``0``
    If b2tral\_zh\_analyt\_mdf.eq.1, the MDF friction force calculation is applied. See [S. O. Makarov et al., PoP 2021] for details.
    This switch is subservient to b2tral\_Zhdanov\_closure.
    

.. index:: b2tral_Zhdanov_cond

``b2tral_Zhdanov_cond``    type: ``integer``    default: ``1``
    If b2tral\_Zhdanov\_cond.eq.0, the Braginskii expression for the ion conductivity is used.
    This switch is subservient to b2tral\_Zhdanov\_closure.
    

.. index:: b2tral_Zhdanov_vish

``b2tral_Zhdanov_vish``    type: ``integer``    default: ``1``
    If b2tral\_Zhdanov\_vish.eq.0, the Braginskii expression for the heat flux dependent viscous stress is used.
    This switch is subservient to b2tral\_Zhdanov\_closure.
    

.. index:: b2tral_Zhdanov_visu

``b2tral_Zhdanov_visu``    type: ``integer``    default: ``1``
    If b2tral\_Zhdanov\_visu.eq.0, the Braginskii expression for the velocity-dependent viscous stress is used.
    This switch is subservient to b2tral\_Zhdanov\_closure.
    

.. index:: b2tral_zhflcorr

``b2tral_zhflcorr``    type: ``real``    default: ``3.0``
    Flux-limiting coefficient multiplier.
    

.. index:: b2tral_zhflcorrh

``b2tral_zhflcorrh``    type: ``real``    default: ``0.4``
    Additional flux-limiting coefficient multiplier for the heat flux.
    

.. index:: b2tral_zhd_corr

``b2tral_zhd_corr``    type: ``integer``    default: ``1``
    Multiplier to the corrections due to the difference in definition for temperature and Joule heating between Zhdanov and Braginskii.
    This switch is subservient to b2tral\_Zhdanov\_closure.
    

.. index:: b2tral_zhd_corrT

``b2tral_zhd_corrT``    type: ``integer``    default: ``1``
    Multiplier to the corrections due to the difference in definition for temperature between Zhdanov and Braginskii in the thermal force calculation.
    This switch is subservient to b2tral\_Zhdanov\_closure.
    

.. index:: b2tral_zhcscorr

``b2tral_zhcscorr``    type: ``integer``    default: ``1``
    If b2tral\_zhcscorr.eq.0, the corrections for each individual ion charge state from the isonuclear sequence value are disabled.
    This switch is subservient to b2tral\_Zhdanov\_closure.
    

.. index:: b2tral_zhcscorr_vq

``b2tral_zhcscorr_vq``    type: ``integer``    default: ``1``
    If b2tral\_zhcscorr\_vq.eq.0, the corrections for each individual ion charge state from the isonuclear sequence value are disabled for the heat stress-viscosity.
    This switch is subservient to b2tral\_Zhdanov\_closure.
    

.. index:: b2sifr_Zhdanov_tf_fr

``b2sifr_Zhdanov_tf_fr``    type: ``integer``    default: ``1``
    If b2sifr\_Zhdanov\_tf\_fr.eq.1, the Zhdanov expressions for the thermal and friction forces are used.
    This switch is subservient to b2tral\_Zhdanov\_closure.
    

.. index:: b2sifr_Zhdanov_test

``b2sifr_Zhdanov_test``    type: ``integer``    default: ``0``
    If b2sifr\_Zhdanov\_test.eq.1, the Zhdanov-Grad calculation takes place, but is not used. To be used for testing purposes.
    

.. index:: b2tfhi_Zhdanov_vel_heat

``b2tfhi_Zhdanov_vel_heat``    type: ``integer``    default: ``1``
    If b2tfhi\_Zhdanov\_vel\_heat.eq.1, the Zhdanov velocity-dependent ion heat flux is used.
    This switch is subservient to b2tral\_Zhdanov\_closure.
    

.. index:: b2tral_zh_tf_toff

``b2tral_zh_tf_toff``    type: ``string``    default: ``0``
    String of integers with (nspecies\*(nspecies+1))/2-nspecies digits. If a digit is {\tt 1}, turn off the thermal force between corresponding species starting from 1 and 2; 1 and 3;....; up to nspecies-1 and nspecies.
    This switch is subservient to b2tral\_Zhdanov\_closure.
    

.. index:: b2tral_zh_vis_type

``b2tral_zh_vis_type``    type: ``integer``    default: ``0``
    If b2tral\_zh\_vis\_type.eq.0, the Braginskii-like velocity-dependent stress-viscosity is used.
    If b2tral\_zh\_vis\_type.eq.1, the Zhdanov-like velocity-dependent stress-viscosity is used.
    If b2tral\_zh\_vis\_type.eq.2, the Makarov-like velocity-dependent stress-viscosity is used.
    

.. index:: b2npmo_smbvi_factor

``b2npmo_smbvi_factor``    type: ``real``    default: ``1.0``
    This switch defines the fraction of the cross-ion part of the stress-viscosity term which is applied. The cross-ion part of the stress-viscosity term can lead to numerical problems. If so, it is recommended to start from '0.0' and increase it step by step.
    This switch is subservient to b2tral\_Zhdanov\_closure.
    

.. index:: b2tral_amfact_on

``b2tral_amfact_on``    type: ``integer``    default: ``0``
    If b2tral\_amfact\_on.eq.1, the mass correction for the thermal and friction force calculation is applied.
    

.. index:: b2tral_amfact_***

``b2tral_amfact_***``    type: ``real``    default: ``1.0``
    If b2tral\_amfact\_on.eq.1, this multiplier is applied for the mass of the species corresponding to isonuclear sequence number '\*\*\*'. Recall the sequence numbering starts at zero (e.g. b2tral\_amfact\_000, b2tral\_amfact\_001, ...).
    

.. index:: b2npmo_impr_form_fr

``b2npmo_impr_form_fr``    type: ``integer``    default: ``0``
    If b2npmo\_impr\_form\_fr.eq.1, an improved analytical form for the friction force is computed instead of the form corrresponding to b2sigp\_style.eq.2.
    Used only if b2tral\_Zhdanov\_closure is equal to 0.
    

.. index:: b2npmo_impr_form_tf

``b2npmo_impr_form_tf``    type: ``integer``    default: ``0``
    If b2npmo\_impr\_form\_tf.eq.1, an improved analytical form for the thermal force is computed instead of the form corresponding to b2sigp\_style.eq.2.
    Used only if b2tral\_Zhdanov\_closure is equal to 0.
    

.. index:: b2npmo mass multiplicator

``b2npmo mass multiplicator``    type: ``real``    default: ``1.0``
    Using this number the impurity mass can be artificialy increased.
    Used only if b2tral\_Zhdanov\_closure is equal to 0.
    

.. index:: b2sqel_artificial_radiation

``b2sqel_artificial_radiation``    type: ``real``    default: ``0.0``
    If art\_rad.ne.0, then an artificial radiation loss term is added to the electron cooling rate. Art\_rad represents the percent fraction of impurities in the plasma.
    

.. index:: b2stbc_*

.. index:: b2stbc_fheycore, b2stbc_fhiycore, b2stbc_fhiycore_kinetic_energy, b2stbc_fchycore, b2stbc_fnaycore, b2stbc_isfeedback, b2stbc_iyped, b2stbc_ndes, b2stbc_ndes_sol, b2stbc_nepedm_sol, b2stbc_nesepm, b2stbc_nesepm_overshoot, b2stbc_nesepm_pfr, b2stbc_nesepm_sol, b2stbc_private_flux_puff, b2stbc_volrec, b2stbc_volrec_overshoot, b2stbc_nesepm_minpuff, b2stbc_nesepm_maxpuff, eirene_nesepm_istra
.. c

``b2stbc_*``

  - ``b2stbc_fheycore``  -     type: ``real``    default: ``0.0``

  - ``b2stbc_fhiycore``  -     type: ``real``    default: ``0.0``

  - ``b2stbc_fhiycore_kinetic_energy``  -     type: ``integer``    default: ``0``

  - ``b2stbc_fchycore``  -     type: ``real``    default: ``-1.0e30``

  - ``b2stbc_fnaycore``  -     type: ``real``    default: ``-1.0e30``

  - ``b2stbc_isfeedback``  -     type: ``integer``    default: ``0``

  - ``b2stbc_iyped``  -     type: ``real``    default: ``jsep/2``

  - ``b2stbc_ndes``  -     type: ``real``    default: ``0.0``

  - ``b2stbc_ndes_sol``  -     type: ``real``    default: ``0.0``

  - ``b2stbc_nepedm_sol``  -     type: ``real``    default: ``0.0``

  - ``b2stbc_nesepm``  -     type: ``real``    default: ``0.0``

  - ``b2stbc_nesepm_overshoot``  -     type: ``real``    default: ``0.0``

  - ``b2stbc_nesepm_pfr``  -     type: ``real``    default: ``0.0``

  - ``b2stbc_nesepm_sol``  -     type: ``real``    default: ``0.0``

  - ``b2stbc_private_flux_puff``  -     type: ``real``    default: ``0.0``

  - ``b2stbc_volrec``  -     type: ``real``    default: ``0.0``

  - ``b2stbc_volrec_overshoot``  -     type: ``real``    default: ``0.0``

  - ``b2stbc_nesepm_minpuff``  -     type: ``real``    default: ``0.0``

  - ``b2stbc_nesepm_maxpuff``  -     type: ``real``    default: ``0.0``

  - ``eirene_nesepm_istra``  -     type: ``integer``    default: ``-1``


    The 20 switches above are all feedback switches and require that b2stbc\_feedback.ne.0 (See Run section for details) or that lfeedback=.true. in b2.boundary.parameters. Feedback schemes are now all applied in the same way in a dedicated module b2us\_feedback (see FEEDBACK\_CONTROL namelist). Switches in b2mn.dat are still available and will override whatever is specified in b2.feedback\_control.parameters, but it is recommended to not use switches anymore. This will allow more flexibility in applying such schemes.
    The feedback is done as a boundary condition and is under-relaxed using the b2stbc\_....\_alpha switches (See Numerics section for details).
    fheycore is the radial electron heat flow entering the core boundary.  Will apply fb\_type=11, fb\_rescale=1, fb\_actuator=4 on region defined by coreregno.
    fhiycore is the radial ion heat flow entering the core boundary. Will apply fb\_type=12, fb\_rescale=1, fb\_actuator=5 on region defined by coreregno.
    fchycore is the radial current entering the core boundary. Will apply fb\_type=13, fb\_rescale=1, fb\_actuator=4 on region defined by coreregno.
    fnaycore is the radial flux of species "isfeedback" entering the core boundary. Will apply fb\_type=10, fb\_rescale=1, fb\_actuator=3 on region defined by coreregno.
    If fhiycore\_kinetic\_energy.eq.1, the parallel kinetic energy flux is counted as part of the ion energy flux.
    For double-null cases, the f..ycore variables contain the total flow through both core boundaries taken together (to be checked for WG code!).
    The core boundaries are identified by the coreregno and coreregn2 switches (see Geometry section). These switches need to be manually adjusted for WG cases as now they indicate the boundary where the feedback is applied. For switches like b2stbc\_xxxycore or private\_gas\\_puff the user has to specify in b2.feedback\_control.parameters} where the feedback is calculated (see b2us.regions.parameters produced at conversion), while coreregno still indicates where it is applied. pfrregno and solregno lose meaning in kinetic cases if the actuator is the gas puff. Coreregn2 and pfrregno2 are not yet converted/used.
    The other seven switches are density feedback switches: nesepm is the outer midplane separatrix electron density. (See rzomp switch in b2.user.parameters for setting of midplane position). This is controlled through particle input of main plasma species isfeedback through the core boundary (See Geometry section for the core boundary indices coreregno and coreregn2).
    nesepm\_sol is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the SOL region. (See b2mwti\_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the SOL North boundary (See Geometry section for the SOL North boundary index solregno). If nesepm\_overshoot.gt.1.0, the gas puff is turned off when the midplane separatrix density reaches nesepm\*nesepm\_overshoot. Minimum and maximum values of the feedback gas puff can be set using b2stbc\_nesepm\_minpuff and b2stbc\_nesepm\_maxpuff. It will apply fb\_type=3, fb\_rescale=1, fb\_actuator=1 on region defined by solregno.
    nepedm\_sol is similar to nesepm\_sol but the feedback is exerted on the electron density at the top of the pedestal, along the outer midplane, at the icped-th ring (where icped=iyped+2) counting from the inner core boundary. It will apply fb\_type=16, fb\_rescale=1, fb\_actuator=1 on region defined by solregno.
    ndes\_sol is the total particle content from the isonuclear sequence of species 'isfeedback' over the entire simulation domain. It is governed, like nesepm\_sol, by nesepm\_overshoot and nesepm\_alpha and corresponds to a SOL boundary feedback. Will apply fb\_type=14, fb\_rescale=1, fb\_actuator=1 on region defined by solregno. WARNING: in the structured code this switch was asking for BCCON=12, so density BC for fluid neutrals feedback but then it switches to gas  puff for kinetic neutrals. Now it is ONLY gaspuff.
    volrec\_sol is the total particle source due to volume recombination coming from Eirene. Its feedback is governed by volrec\_overshoot and volrec\_alpha and volrec\_beta parameters (See Numerics section for the latter two). Will apply fb\_type=15, fb\_rescale=1, fb\_actuator=1 on region defined by pfrregno1. WARNING: not available yet for fluid neutrals.
    nesepm\_pfr is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the PFR region. (See b2mwti\_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the PFR South boundary indices pfrregno1 and pfrregno2). will apply fb\_type=3, fb\_rescale=1, fb\_actuator=1 on region defined pfrregno1
    ndes is the total particle (neutrals + ions) content of the species whose neutral species has index isfeedback. This is controlled through particle input of neutrals species isfeedback through the	private flux boundaries (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2). will apply fb\_type=14, fb\_rescale=1, fb\_actuator=1 on region defined by pfrregno1. WARNING: in the structured code this switch was asking for BCCON=12, so density BC for fluid neutrals feedback but then it switches to gas puff for kinetic neutrals. Now it is ONLY gas puff.
    private\_flux\_puff NOT YET CONVERTED TO WG CODE! is the particle flow of species isfeedback through the private flux region boundary. This is controlled through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2).
    All but the first of these feedback schemes ("nesepm") can also be run though an Eirene neutral gas puff. In that case, one should set an appropriate gas puffing stratum in the Eirene input file input.dat, as well as in the b2.neutrals.parameters file. The code will assume, unless told otherwise through the use of "eirene\_nesepm\_istra", that the first stratum of type 'C' found in b2.neutrals.parameters is the stratum used for the feedback. If "eirene\_nesepm\_istra" is set to a positive number, the code will consider the feedback stratum to be the stratum in the "eirene\_nesepm\_istra"-th position in b2.neutrals.parameters.
    b2stbc\_iyped is the index in the OMP CV list (defined with RZOMP in b2.user.parameters) of the pedestal cell (defaults to icsepomp/2).
    
.. index::
   single: b2stbc_*; b2stbc_fheycore
   single: b2stbc_*; b2stbc_fhiycore
   single: b2stbc_*; b2stbc_fhiycore_kinetic_energy
   single: b2stbc_*; b2stbc_fchycore
   single: b2stbc_*; b2stbc_fnaycore
   single: b2stbc_*; b2stbc_isfeedback
   single: b2stbc_*; b2stbc_iyped
   single: b2stbc_*; b2stbc_ndes
   single: b2stbc_*; b2stbc_ndes_sol
   single: b2stbc_*; b2stbc_nepedm_sol
   single: b2stbc_*; b2stbc_nesepm
   single: b2stbc_*; b2stbc_nesepm_overshoot
   single: b2stbc_*; b2stbc_nesepm_pfr
   single: b2stbc_*; b2stbc_nesepm_sol
   single: b2stbc_*; b2stbc_private_flux_puff
   single: b2stbc_*; b2stbc_volrec
   single: b2stbc_*; b2stbc_volrec_overshoot
   single: b2stbc_*; b2stbc_nesepm_minpuff
   single: b2stbc_*; b2stbc_nesepm_maxpuff
   single: b2stbc_*; eirene_nesepm_istra


.. index:: b2stbc_type13..21*

.. index:: b2stbc_type13_ref, b2stbc_type16_ref, b2stbc_type20_ref, b2stbc_type21_ref, b2stbc_type16_kinetic_energy
.. c

``b2stbc_type13..21*``

  - ``b2stbc_type13_ref``  -     type: ``integer``    default: ``1``

  - ``b2stbc_type16_ref``  -     type: ``integer``    default: ``1``

  - ``b2stbc_type20_ref``  -     type: ``integer``    default: ``1``

  - ``b2stbc_type21_ref``  -     type: ``integer``    default: ``1``

  - ``b2stbc_type16_kinetic_energy``  -     type: ``integer``    default: ``0``


    These switches are associated with the boundary condition of type 13, 16, 17, 20 or 21 for particle flux, or electron and ion energy fluxes, i.e. constant density or temperature giving a prescribed flux through a radial surface, located type13\_ref or type16\_ref radial steps away from the boundary of the computational domain, respectively, and applied type20\_ref steps away. See code and description in b2cdcn for details.
    Type 21 also applies to the electric potential boundary condition.
    It scales the feedback strength according to the value of the variable on the ring type21\_ref steps inside.
    When type16\_ref.gt.1, then the position where the core flux tallies are computed moves along with the boundary condition.
    If type16\_kinetic\_energy.eq.1, then the parallel kinetic energy flux is included in the ion heat flux component of type 16 and 17 boundary conditions.
    
.. index::
   single: b2stbc_type13..21*; b2stbc_type13_ref
   single: b2stbc_type13..21*; b2stbc_type16_ref
   single: b2stbc_type13..21*; b2stbc_type20_ref
   single: b2stbc_type13..21*; b2stbc_type21_ref
   single: b2stbc_type13..21*; b2stbc_type16_kinetic_energy


.. index:: b2stbc_bcene_15_style

``b2stbc_bcene_15_style``    type: ``integer``    default: ``1``
    If bcene\_15\_style.eq.0, the electron sheath boundary condition computes the electron current as the difference between the ion flow and the poloidal current.
    If bcene\_15\_style.eq.1 (recommended, default), the electron current at the sheath is computed directly from the sheath potential drop. This method has proven numerically more stable, especially in cases with drifts.
    

.. index:: b2stbc_bceni_15_style

``b2stbc_bceni_15_style``    type: ``integer``    default: ``0``
    If bceni\_15\_style.eq.0 (default), use the ion sheath transmission factor specified by ENIPAR(IB,1).
    If bceni\_15\_style.eq.1, use the self-consistent ion sheath transmission factor implied by the truncated drifting Maxwellian ion distribution determined by the Eirene sheath model (ENIPAR(IB,1) is not used). See Eirene manual Section 1.5.1 for the detailed expression.
    

.. index:: b2stbc_bcene_16_style

``b2stbc_bcene_16_style``    type: ``integer``    default: ``0``
    If bcene\_16\_style.eq.1, the boundary condition is enforced using the modified fluxes fhe\_mdf. Recommended when running cases with drifts.
    bcene\_16\_style.eq.1 not yet available for WG.
    

.. index:: b2stbc_bceni_16_style

``b2stbc_bceni_16_style``    type: ``integer``    default: ``0``
    If bceni\_16\_style.eq.1, the boundary condition is enforced using the modified fluxes fhi\_mdf. Recommended when running cases with drifts.
    bceni\_16\_style.eq.1 not yet available for WG.
    

.. index:: b2stbc_secmodel

``b2stbc_secmodel``    type: ``integer``    default: ``0``
    If secmodel.eq.1, then the secondary electron emission coefficient at the plates is computed locally according to a kinetic model, otherwise the default values of cbsch(7,ireg) and/or gammae are used.
    Not yet available for WG.
    

.. index:: b2mndr_boundary_sources

``b2mndr_boundary_sources``    type: ``integer``    default: ``0``
    If boundary\_sources.ne.0, allow for the specification of boundary values for all equations, using BC type 7, provided in the bv\_na.dat, bv\_ua.dat, bv\_te.dat, bv\_ti.dat, and bv\_po.dat files. Only the files corresponding to the solved equations must be provided. For time-dependent MMS (use\_mms.eq.2), boundary values must be provided for each time-step: bv\_XX0001.dat, bv\_XX0002.dat, bv\_XX0003.dat, and so on.
    

.. index:: b2mndr_equation_sources

``b2mndr_equation_sources``    type: ``integer``    default: ``0``
    If equation\_sources.ne.0, allow for the specification of source term values for all equations, per unit volume, provided in the art\_sna.dat, art\_smo.dat, art\_she.dat, art\_shi.dat, and art\_sch.dat files. Only the files corresponding to the solved equations must be provided. For time-dependent MMS (use\_mms.eq.2), artifical sources must be provided for each time-step: art\_sXX0001.dat, art\_sXX0002.dat, art\_sXX0003.dat, and so on.
    

.. index:: b2mndr_mms_...

.. index:: b2mndr_use_mms, b2mndr_set_na_numerical, b2mndr_set_ua_numerical, b2mndr_set_te_numerical, b2mndr_set_ti_numerical, b2mndr_set_tn_numerical, b2mndr_set_po_numerical
.. c

``b2mndr_mms_...``

  - ``b2mndr_use_mms``  -     type: ``integer``    default: ``0``

  - ``b2mndr_set_na_numerical``  -     type: ``integer``    default: ``0``

  - ``b2mndr_set_ua_numerical``  -     type: ``integer``    default: ``0``

  - ``b2mndr_set_te_numerical``  -     type: ``integer``    default: ``0``

  - ``b2mndr_set_ti_numerical``  -     type: ``integer``    default: ``0``

  - ``b2mndr_set_tn_numerical``  -     type: ``integer``    default: ``0``

  - ``b2mndr_set_po_numerical``  -     type: ``integer``    default: ``0``


    If use\_mms.eq.1, specifies a run using the Method of Manufactured Solutions in steady-state mode (b2mndt\_style.eq.1). If use\_mms.eq.2, specifies a run using the Method of Manufactured Solutions in time-dependent mode (b2mndt\_style.eq.2). The exact solutions to match are provided by the b2mndr\_set\_XX\_numerical switches.
    An exact solution is available for comparison if the corresponding b2mndr\_set\_XX\_numerical switch is nonzero. The exact solutions for steady-state are provided, respectively, in the exact\_na.dat and exact\_ne.dat, exact\_ua.dat, exact\_te.dat, exact\_ti.dat, and exact\_po.dat files. The exact solutions for time-dependent must be provided for each time-step: exact\_XX0001.dat, exact\_XX0002.dat, exact\_XX0003.dat, and so on.
    The exact\_na.dat and exact\_ne.dat files must be provided simultaneously.
    
.. index::
   single: b2mndr_mms_...; b2mndr_use_mms
   single: b2mndr_mms_...; b2mndr_set_na_numerical
   single: b2mndr_mms_...; b2mndr_set_ua_numerical
   single: b2mndr_mms_...; b2mndr_set_te_numerical
   single: b2mndr_mms_...; b2mndr_set_ti_numerical
   single: b2mndr_mms_...; b2mndr_set_tn_numerical
   single: b2mndr_mms_...; b2mndr_set_po_numerical


.. index:: b2stbr_sputtering...

.. index:: b2stbr_plate_model, b2stbr_plate_option, b2stbr_sput_chem_model, b2stbr_sput_chem_cutoff_alpha, b2stbr_sput_chem_cutoff_beta, b2stbr_sput_mixed_alpha, b2stbr_sput_mixed_beta, b2stbr_sput_phys_model, b2stbr_sputter_energy_on, b2stbr_sput_res, b2stbr_therm_evap, b2stbr_sput_dst, b2stbr_sput_dst2, b2stbr_sput_dst3, b2stbr_sput_frac_flag, b2stbr_sput_frc, b2stbr_sput_phys, b2stbr_sput_src, b2stbr_sput_phys_col, b2stbr_alpha, b2stbr_plate_temp, b2stbr_plate_thick, b2stbr_redep_alpha
.. c

``b2stbr_sputtering...``

  - ``b2stbr_plate_model``  -     type: ``integer``    default: ``0``

  - ``b2stbr_plate_option``  -     type: ``integer``    default: ``3``

  - ``b2stbr_sput_chem_model``  -     type: ``integer``    default: ``0``

  - ``b2stbr_sput_chem_cutoff_alpha``  -     type: ``real``    default: ``1.0``

  - ``b2stbr_sput_chem_cutoff_beta``  -     type: ``real``    default: ``3.0``

  - ``b2stbr_sput_mixed_alpha``  -     type: ``real``    default: ``1.0``

  - ``b2stbr_sput_mixed_beta``  -     type: ``real``    default: ``1.0``

  - ``b2stbr_sput_phys_model``  -     type: ``integer``    default: ``1``

  - ``b2stbr_sputter_energy_on``  -     type: ``integer``    default: ``1``

  - ``b2stbr_sput_res``  -     type: ``real``    default: ``0.0``

  - ``b2stbr_therm_evap``  -     type: ``real``    default: ``0.0``

  - ``b2stbr_sput_dst``  -     type: ``integer``    default: ``-1``

  - ``b2stbr_sput_dst2``  -     type: ``integer``    default: ``-1``

  - ``b2stbr_sput_dst3``  -     type: ``integer``    default: ``-1``

  - ``b2stbr_sput_frac_flag``  -     type: ``integer``    default: ``0``

  - ``b2stbr_sput_frc``  -     type: ``real``    default: ``0.0``

  - ``b2stbr_sput_phys``  -     type: ``real``    default: ``0.0``

  - ``b2stbr_sput_src``  -     type: ``integer``    default: ``1``

  - ``b2stbr_sput_phys_col``  -     type: ``integer``    default: ``3``

  - ``b2stbr_alpha``  -     type: ``real``    default: ``0.25``

  - ``b2stbr_plate_temp``  -     type: ``real``    default: ``300.0``

  - ``b2stbr_plate_thick``  -     type: ``real``    default: ``0.00``

  - ``b2stbr_redep_alpha``  -     type: ``real``    default: ``0.00``


    Sputtering model switches. Not yet available for WG. See the code in b2stbr and the b2mod\_sputter module for specific implementation details and references.
    The default values represent the case of Graphite plates. Sput\_src is the atomic number of the plasma species which causes chemical sputtering.
    Sput\_dst (when .ge.0) is the species index of the destination species produced by physical sputtering, chemical sputtering and/or RES. If either of the latter two processes are included, the chemical sputtering and RES production rate calculations provided in the code assume that sput\_dst points to a Carbon species.
    Sput\_dst2 and sput\_dst3 (when .ge.0) represent other species produced by wall interactions for mixed materials scenarios.
    Sput\_frac\_flag is the switch to turn on mixed materials scenarios (when sput\_frac\_flag.eq.1).
    Plate\_model.eq.0 means the 0-D time-independent plate heating model while plate\_model.eq.1 indicates the 1-D time-dependent plate heating treatment. Plate\_model.eq.2 gives acces to a 2-D time-dependent model. Plate\_option chooses the initialisation of the plate temperature profile. If plate\_option.eq.1, the profile is set to the constant given in plate\_temp. If plate\_option.eq.2, the profile is computed to be the 0-D equilibrium profile. If plate\_option.eq.3, the profile is read from results of the previous run.
    Sput\_phys\_model is a switch for choosing between the TRIM tables (model 1, default) or an empirical formula (model 0). When TRIM data is not available, the empirical formula is automatically used. Extrapolations of low and high energy ranges beyond the TRIM table data is done using the same physical dependencies as the empirical formula. Sput\_chem\_model is a switch for the chemical sputtering model used.
    If sput\_chem\_model.eq.0 (default), the empirical formula is used.
    If sput\_chem\_model.eq.1, a constant with a low energy cut-off is used.
    The cutoff occurs at approximately sput\_chem\_cutoff\_alpha and the width is determined by sput\_chem\_cutoff\_beta (the larger the value, the narrower the width over which the transition from 0 to 1 occurs).
    For model 0, sput\_frc is a multiplier to the empirical formula, while for model 1, sput\_frc is the constant chemical sputtering yield.
    Sput\_frc is superseded by the chem\_sput array from b2.neutrals.namelist if the latter is used.
    For neutrals species, we add a factor of α\*na\*vbar to the particle flux to the plate (used to compute chemical and RES sputtering), where vbar is the average neutral particle speed.
    Sput\_phys turns on physical sputtering when sput\_phys.gt.0.0 and contains a (real) multiplier for the physical sputtering rate looked up in the TRIM tables. It is superseded by the phys\_sput array in b2.neutrals.parameters if the latter is used.
    sput\_phys\_col indicates which column to use in the TRIM table; the default (3) corresponds to 30 degrees incidence. The columns are for

    |  0 15 30 45 55 65 75 80 85

    degrees. This angle is also used in the empirical formula. Plate\_temp is the temperature (in Kelvin) of the COOLED end of the divertor plates. The surface temperature is computed self-consistently (using a 1-D description) according to the incident heat fluxes from the plasma. The plate is assumed to have a thickness of plate\_thick, measured in metres. When plate\_thick.eq.0 (default), the plate surface temperature is assumed to be the same as plate\_temp. Sput\_res turns on radiation enhanced sublimation (RES) when .gt.0.0 and is a multiplier to the RES rate.
    The switch sputter\_energy\_on turns on the energy contribution from the sputtered particles (physical and chemical). If sputter\_energy\_on.eq.0, the particles are sputtered cold, with no energy contribution to the ion heat equation.
    If sputter\_energy\_on.ne.0 (default), the chemically sputtered particles are re-introduced into the plasma with the thermal energy corresponding to the surface temperature of the material, while physically sputtered particles are re-introduced with the TRIM-calculated energy sputtering yield (if the TRIM model is used).
    Therm\_evap turns on thermal evaporation when .gt.0.0 and is a multiplier to the thermal evaporation rate.
    Redep\_alpha is the multiplier to the reduction of the sputtering yield due to prompt redeposition. The promptly redeposited species is counted as eroded-then-deposited species.
    
.. index::
   single: b2stbr_sputtering...; b2stbr_plate_model
   single: b2stbr_sputtering...; b2stbr_plate_option
   single: b2stbr_sputtering...; b2stbr_sput_chem_model
   single: b2stbr_sputtering...; b2stbr_sput_chem_cutoff_alpha
   single: b2stbr_sputtering...; b2stbr_sput_chem_cutoff_beta
   single: b2stbr_sputtering...; b2stbr_sput_mixed_alpha
   single: b2stbr_sputtering...; b2stbr_sput_mixed_beta
   single: b2stbr_sputtering...; b2stbr_sput_phys_model
   single: b2stbr_sputtering...; b2stbr_sputter_energy_on
   single: b2stbr_sputtering...; b2stbr_sput_res
   single: b2stbr_sputtering...; b2stbr_therm_evap
   single: b2stbr_sputtering...; b2stbr_sput_dst
   single: b2stbr_sputtering...; b2stbr_sput_dst2
   single: b2stbr_sputtering...; b2stbr_sput_dst3
   single: b2stbr_sputtering...; b2stbr_sput_frac_flag
   single: b2stbr_sputtering...; b2stbr_sput_frc
   single: b2stbr_sputtering...; b2stbr_sput_phys
   single: b2stbr_sputtering...; b2stbr_sput_src
   single: b2stbr_sputtering...; b2stbr_sput_phys_col
   single: b2stbr_sputtering...; b2stbr_alpha
   single: b2stbr_sputtering...; b2stbr_plate_temp
   single: b2stbr_sputtering...; b2stbr_plate_thick
   single: b2stbr_sputtering...; b2stbr_redep_alpha


.. index:: b2stbr_refl*

.. index:: b2stbr_refl_model, b2stbr_reflection_on
.. c

``b2stbr_refl*``

  - ``b2stbr_refl_model``  -     type: ``integer``    default: ``1``

  - ``b2stbr_reflection_on``  -     type: ``integer``    default: ``1``


    Reflection model switches. If the recycling coefficients (particle and energy) are set to zero, then the code attempts to use, for surfaces in contact with walls, the TRIM reflection data for particle and energy reflection coefficients, when refl\_model.eq.1. If refl\_model.eq.0, an empirical formula is used instead. The model switch is subservient to reflection\_on.ne.0. If reflection\_on.eq.0, then no reflection is used.
    If reflection\_on.eq.1 (default), then the incident species is reflected unchanged. Otherwise, the reflected flux is of the associated neutral species to the incident particles.
    Not converted for WG. It is recommended to use the advanced fluid neutral (AFN) models instead.
    
.. index::
   single: b2stbr_refl*; b2stbr_refl_model
   single: b2stbr_refl*; b2stbr_reflection_on


.. index:: b2mndr_coronal_model

``b2mndr_coronal_model``    type: ``integer``    default: ``0``
    Turns on the coronal model if coronal.ne.0. I.e., the reaction rates of all reactions are made density-independent, and the value computed at the lowest density (given in b2ar.dat) is used.
    

.. index:: b2mndr_hz

``b2mndr_hz``    type: ``real``    default: ``1.0``
    hz has been introduced into the new form of the parallel momentum balance equation. If fac\_hz = 0.0 then hz = 1 and old form of equations is used. If fac\_hz = 1.0 then new form of equations is used.
    

.. index:: b2tfhe_alfTeEh

``b2tfhe_alfTeEh``    type: ``real``    default: ``0.0``
    When set to '1.0', the old form of the electron heat flux calculation is used and b2tfhe\_fch\_pTe should be set to '0.0'. It is recommended to use 0.0.
    Cannot be set to 1.0 when using the SOLPS5.2 physics model.
    

.. index:: b2tfhe_fch_pTe

``b2tfhe_fch_pTe``    type: ``real``    default: ``1.0``
    When set to '1.0', the new form of the electron heat flux calculation is used and b2tfhe\_alfTeEh should be set to '0.0'. It is recommended to use 1.0.
    Cannot be set to 0.0 when using the SOLPS5.2 physics model.
    

.. index:: b2tfnb_xcur

``b2tfnb_xcur``    type: ``real``    default: ``0.0``
    Xcur is a multiplier to the parallel viscosity, perpendicular viscosity, heat viscosity, ion inertial and anomalous current contributions to the ion poloidal flows (particle and energy).
    If set to 0 (default), these currents are carried by electrons. If set to 1, these poloidal currents are carried by the main hydrogenic ions. The latter option can only be used if the plasma has a single majority hydrogenic species. Otherwise, an error will be returned.
    

.. index:: b2tfnb_ycur

``b2tfnb_ycur``    type: ``real``    default: ``1.0``
    Ycur is a multiplier to the parallel viscosity, perpendicular viscosity, heat viscosity, ion inertial and anomalous current contributions to the ion radial flows (particle and energy).
    If set to 0, these currents are carried by electrons. If set to 1 (default), these radial currents are carried by the main hydrogenic ions. The latter option can only be used if the plasma has a single majority hydrogenic species. Otherwise, an error will be returned.
    

.. index:: b2tfnb_vis_per

``b2tfnb_vis_per``    type: ``real``    default: ``0.0``
    vis\_per is a multiplier to the perpendicular viscosity current contributions to the ion poloidal flows (particle and energy). Subservient to b2tfnb\_xcur and b2tfnb\_ycur.
    Cannot be used in conjunction with the 9-point stencil numerical treatment. If used with the 5-point stencil treatment and with fluid neutrals, must be equal to b2tfhe\_vis\_per for numerical stability reasons.
    

.. index:: b2tfnb_vis_q

``b2tfnb_vis_q``    type: ``real``    default: ``1.0``
    vis\_q is a multiplier to the heat viscosity current contributions to the ion poloidal flows (particle and energy). Subservient to b2tfnb\_xcur and b2tfnb\_ycur.
    

.. index:: b2tqce_fke_Zhdanov

``b2tqce_fke_Zhdanov``    type: ``integer``    default: ``1``
    When set to '1', the Zhdanov expression is used in the electron thermal conductivity. It is recommended to use 'b2tqce\_fke\_Zhdanov' '1'.
    This switch is only active if, simultaneously, one has b2tqce\_model.eq.1 and b2tfhe\_fch\_pTe.eq.1.0.
    

.. index:: b2tqce_style_guard_cells

``b2tqce_style_guard_cells``    type: ``integer``    default: ``0``
    When set to '0', b2tqce calculates all classical contributions to the electron transport coefficients on all cells.
    When set to '1', the electrical conductivity (sig) and the thermo-electric coefficient (alf) are not calculated in the guard cells that lie on open flux surfaces.
    

.. index:: b2tqna_user_transport...

.. index:: b2tqna_user_transport, set_transport_eta, set_transport_eta_alpha, set_transport_eta_floor, set_transport_eta_ceiling, set_transport_iyref, set_transport_required_te_gradient
.. c

``b2tqna_user_transport...``

  - ``b2tqna_user_transport``  -     type: ``integer``    default: ``0``

  - ``set_transport_eta``  -     type: ``real``    default: ``2.0``

  - ``set_transport_eta_alpha``  -     type: ``real``    default: ``0.5``

  - ``set_transport_eta_floor``  -     type: ``real``    default: ``0.1``

  - ``set_transport_eta_ceiling``  -     type: ``real``    default: ``10.0``

  - ``set_transport_iyref``  -     type: ``integer``    default: ``See description (integer)``

  - ``set_transport_required_te_gradient``  -     type: ``real``    default: ``5.0e4``


    The last switch is subservient to b2tqna\_user\_transport, and only used if user\_transport.ne.0. When this is the case, the electron perpendicular heat diffusivity and anomalous perpendicular particle transport coefficient are scaled so as to maintain the required\_te\_gradient (in units of eV/m), at the iyref-th radial ring along the outer midplane. By default, this is the ring immediately inside the separatrix.
    The transport\_eta switches are activated when user\_transport.eq.3 and allow modifications of the electron heat conductivity according to a constant eta (Grad Te / Grad Ne) model. See routine set\_transport\_eta code for details.
    A model for disruption transport coefficients is available with user\_transport.eq.7. See routine set\_transport\_disruption code for details. Not yet available for WG.
    The value user\_transport.eq.8 activates the neoclassical model for computation of the transport coefficients in the core. See routine set\_transport\_neo and subroutines called for details. Implemented from the NEOART package.
    
.. index::
   single: b2tqna_user_transport...; b2tqna_user_transport
   single: b2tqna_user_transport...; set_transport_eta
   single: b2tqna_user_transport...; set_transport_eta_alpha
   single: b2tqna_user_transport...; set_transport_eta_floor
   single: b2tqna_user_transport...; set_transport_eta_ceiling
   single: b2tqna_user_transport...; set_transport_iyref
   single: b2tqna_user_transport...; set_transport_required_te_gradient


.. index:: b2tqna_m*

.. index:: b2tqna_max_df0, b2tqna_min_df0
.. c

``b2tqna_m*``

  - ``b2tqna_max_df0``  -     type: ``real``    default: ``1e30``

  - ``b2tqna_min_df0``  -     type: ``real``    default: ``0.0``


    Upper and lower limits of the diffusivity coefficients df0 computed in b2tqna for each neutral species.
    
.. index::
   single: b2tqna_m*; b2tqna_max_df0
   single: b2tqna_m*; b2tqna_min_df0


.. index:: b2tqna_new_df0

``b2tqna_new_df0``    type: ``integer``    default: ``0``
    When new\_df0.eq.1, the neutral diffusivity is computed according to the local charge exchange, ionisation and elastic collision rates, instead of the standard form with constant cross-sections.
    

.. index:: b2tqna_ballooning

.. index:: b2tqna_ballooning, b2tqna_ballooning_rescale, b2tqna_bb_ref, b2tqna_ballooning_sig
.. c

``b2tqna_ballooning``

  - ``b2tqna_ballooning``  -     type: ``real``    default: ``0.0``

  - ``b2tqna_ballooning_rescale``  -     type: ``real``    default: ``1.0``

  - ``b2tqna_bb_ref``  -     type: ``real``    default: ``See description (real)``

  - ``b2tqna_ballooning_sig``  -     type: ``integer``    default: ``1``


    Ballooning model switches. If ballooning.ne.0, then all transport coefficients in cell (i) are rescaled by a factor of ballooning\_rescale\*abs(bb\_ref/bb(i))\*\*ballooning .
    The default value for bb\_ref is the arithmetic average of the total magnetic field strength over the entire computational domain. If b2tqna\_ballooning\_sig.ne.0 (default), the ballooning factor is also applied to the anomalous radial electrical conductivity and the anomalous radial thermo-electric coefficient.
    
.. index::
   single: b2tqna_ballooning; b2tqna_ballooning
   single: b2tqna_ballooning; b2tqna_ballooning_rescale
   single: b2tqna_ballooning; b2tqna_bb_ref
   single: b2tqna_ballooning; b2tqna_ballooning_sig


.. index:: b2tqna_pfr_rescale

``b2tqna_pfr_rescale``    type: ``real``    default: ``1.0``
    Scaling factor for all ion and electron transport coefficients inside private flux regions.
    

.. index:: b2tqna_divsol_rescale

``b2tqna_divsol_rescale``    type: ``real``    default: ``1.0``
    Scaling factor for all ion and electron transport coefficients inside divertor SOL regions.
    

.. index:: b2sifr_phm0

``b2sifr_phm0``    type: ``real``    default: ``1.0``
    Multiplier of the friction term between charged species (only ions in case b2sigp\_style.eq.2).
    

.. index:: b2sifr_phm1

``b2sifr_phm1``    type: ``real``    default: ``1.0``
    If b2sigp\_style.eq.2, multiplier to the friction force term between electrons and ions.
    Otherwise, multiplier of the ehxp term in the older expression for the thermal force.
    

.. index:: b2sifr_phm2

``b2sifr_phm2``    type: ``real``    default: ``1.0``
    Multiplier of the electron thermal gradient term in the thermal force term and parallel current
    

.. index:: b2sifr_phm3

``b2sifr_phm3``    type: ``real``    default: ``1.0``
    Multiplier of the ion thermal gradient term in the thermal force term.
    

.. index:: b2sifr_limth*

.. index:: b2sifr_limthee, b2sifr_limthii
.. c

``b2sifr_limth*``

  - ``b2sifr_limthee``  -     type: ``real``    default: ``0.3``

  - ``b2sifr_limthii``  -     type: ``real``    default: ``0.3``


    Parameters for the computation of the thermal force term.
    
.. index::
   single: b2sifr_limth*; b2sifr_limthee
   single: b2sifr_limth*; b2sifr_limthii


.. index:: b2trcl_cth*

.. index:: b2trcl_cthe, b2trcl_cthi
.. c

``b2trcl_cth*``

  - ``b2trcl_cthe``  -     type: ``real``    default: ``0.0``

  - ``b2trcl_cthi``  -     type: ``real``    default: ``2.65``


    Parameters for the computation of the thermal force term.
    
.. index::
   single: b2trcl_cth*; b2trcl_cthe
   single: b2trcl_cth*; b2trcl_cthi


.. index:: b2tlnl_*

.. index:: b2trcl_lambda, b2tlnl_ee, b2tlnl_ei, b2tlnl_ii
.. c

``b2tlnl_*``

  - ``b2trcl_lambda``  -     type: ``real``    default: ``-5.0``

  - ``b2tlnl_ee``  -     type: ``integer``    default: ``0``

  - ``b2tlnl_ei``  -     type: ``integer``    default: ``0``

  - ``b2tlnl_ii``  -     type: ``integer``    default: ``0``


    If lambda is positive, the Coulomb logarithm is set to lambda.
    If lambda is negative, then abs(lambda) is the lower bound to be used when computing the Coulomb logarithm according to the NRL formulae.
    The computation of the Coulomb logarithm takes place in b2tlnl.
    The default formula is to use the Braginskii formulation, which will give the same answer for electron-electron (ee), electron-ion (ei), and ion-ion (ii) collisions. Respectively, non-default values of '1', '2' and '3' for b2tlnl\_ii, \_ee, and \_ei, respectively, make use of the calculation according to Wesson.
    
.. index::
   single: b2tlnl_*; b2trcl_lambda
   single: b2tlnl_*; b2tlnl_ee
   single: b2tlnl_*; b2tlnl_ei
   single: b2tlnl_*; b2tlnl_ii


.. index:: b2tfnb_PSch

``b2tfnb_PSch``    type: ``real``    default: ``1.0``
    Multiplier to the Pfirsch-Schlueter flows.
    

.. index:: b2news_BoRiS

``b2news_BoRiS``    type: ``real``    default: ``0.0``
    The poloidal convective heat flux contains a prefactor of (3/2+BoRiS). The default gives us the internal energy equation. The value BoRiS = 1.0 gives us the total energy equation.
    Only for use to benchmark with codes using the total energy equation. When used, the meaning of fhe and fhi changes from internal energy fluxes to total energy fluxes.
    

.. index:: b2tfhe_conduction_only

``b2tfhe_conduction_only``    type: ``integer``    default: ``0``
    When conduction\_only.eq.1, convective heat transfer terms are turned off. Only to be used when benchmarking against pure conduction cases.
    

.. index:: b2tfnb_flux...

.. index:: b2tfnb_alpha, b2tfnb_gamma, b2tfnb_flux_limit_min_ti
.. c

``b2tfnb_flux...``

  - ``b2tfnb_alpha``  -     type: ``real``    default: ``0.0``

  - ``b2tfnb_gamma``  -     type: ``real``    default: ``2.0``

  - ``b2tfnb_flux_limit_min_ti``  -     type: ``real``    default: ``0.0``


    Parameters for the flux limit to the convective neutral flow.
    Alpha is a multiplier to the classical flux limit value.
    The larger α is, the weaker the flux limit is.
    γ is the exponent used in the flux-limiting formula.
    The smaller γ is, the stronger the flux limit is.
    If alpha.eq.0, no flux limit is applied.
    flux\_limit\_min\_ti specifies the minimum ti to be used (in eV).
    
.. index::
   single: b2tfnb_flux...; b2tfnb_alpha
   single: b2tfnb_flux...; b2tfnb_gamma
   single: b2tfnb_flux...; b2tfnb_flux_limit_min_ti


.. index:: b2tlc0_*

.. index:: b2tlc0_alpha, b2tlc0_gamma
.. c

``b2tlc0_*``

  - ``b2tlc0_alpha``  -     type: ``real``    default: ``0.0 (if b2mn_afn = 0); 1.0 (otherwise)``

  - ``b2tlc0_gamma``  -     type: ``real``    default: ``2.0``


    Parameters for the flux limit to dpa0 - pressure driven neutral diffusion.
    Alpha is a multiplier to the classical flux limit value.
    γ is the exponent used in the flux-limiting formula. If alpha.eq.0, no flux limit is applied.
    
.. index::
   single: b2tlc0_*; b2tlc0_alpha
   single: b2tlc0_*; b2tlc0_gamma


.. index:: b2tlh0_*

.. index:: b2tlh0_alpha, b2tlh0_gamma, b2tlh0_flux_limit_min_ti
.. c

``b2tlh0_*``

  - ``b2tlh0_alpha``  -     type: ``real``    default: ``0.0 (if b2mn_afn = 0); 1.0 (otherwise)``

  - ``b2tlh0_gamma``  -     type: ``real``    default: ``2.0``

  - ``b2tlh0_flux_limit_min_ti``  -     type: ``real``    default: ``0.0``


    Parameters for the flux limit to the heat conductivity of the neutrals. Alpha is a multiplier to the classical flux limit value.
    The larger α is, the weaker the flux limit is.
    γ is the exponent used in the flux-limiting formula.
    The smaller γ is, the stronger the flux limit is.
    If alpha.eq.0, no flux limit is applied.
    flux\_limit\_min\_ti specifies the minimum ti to be used (in eV).
    
.. index::
   single: b2tlh0_*; b2tlh0_alpha
   single: b2tlh0_*; b2tlh0_gamma
   single: b2tlh0_*; b2tlh0_flux_limit_min_ti


.. index:: b2tlv0_*

.. index:: b2tlv0_alpha, b2tlv0_gamma
.. c

``b2tlv0_*``

  - ``b2tlv0_alpha``  -     type: ``real``    default: ``0.0 (if b2mn_afn = 0); 1.0 (otherwise)``

  - ``b2tlv0_gamma``  -     type: ``real``    default: ``2.0``


    Parameters for the flux limit to the viscosity of the neutrals. Alpha is a multiplier to the classical flux limit value.
    The larger α is, the weaker the flux limit is.
    γ is the exponent used in the flux-limiting formula.
    The smaller γ is, the stronger the flux limit is.
    If alpha.eq.0, no flux limit is applied.
    
.. index::
   single: b2tlv0_*; b2tlv0_alpha
   single: b2tlv0_*; b2tlv0_gamma


.. index:: b2tlmv_style

``b2tlmv_style``    type: ``integer``    default: ``1``
    If style = 0 then the original form of the viscosity flux limit is used, otherwise the SPb flux limit is used.
    

.. index:: b2tlhe_far_sol

``b2tlhe_far_sol``    type: ``integer``    default: ``0``
    EXPERIMENTAL SWITCH GROUP, USE WITH CARE.
    If set to 1, enables gradual modification of the electron heat flux limiter towards low density regions. Above b2tlhe\_ne\_max (default 1.0e18 m^{-3}), the standard value cflme is used. Below b2tlhe\_ne\_min (default 1.0e17 m^{-3}), the value b2tlhe\_cflme\_min is used (default 0.2). For densities in between b2tlhe\_ne\_min and b2tlhe\_ne\_max, the heat flux limiter is computed based on linear interpolation between the limiting values.
    

.. index:: b2tlhi_far_sol

``b2tlhi_far_sol``    type: ``integer``    default: ``0``
    EXPERIMENTAL SWITCH GROUP, USE WITH CARE.
    If set to 1, enables gradual modification of the ion heat flux limiter towards low density regions. Above b2tlhi\_ni\_max (default 1.0e18 m^{-3}), the standard value cflmi is used. Below b2tlhi\_ni\_min (default 1.0e17 m^{-3}), the value b2tlhi\_cflmi\_min is used (default 1.0e1). For densities in between b2tlhi\_ni\_min and b2tlhi\_ni\_max, the heat flux limiter is computed based on linear interpolation between the limiting values.
    

.. index:: b2tlmv_far_sol

``b2tlmv_far_sol``    type: ``integer``    default: ``0``
    EXPERIMENTAL SWITCH GROUP, USE WITH CARE.
    If set to 1, enables gradual modification of the parallel viscosity flux limiter towards low density regions. Above b2tlmv\_ni\_max  (default 1.0e18 m^{-3}), the standard value cflmv is used. Below b2tlmv\_ni\_min (default 1.0e17 m^{-3}), the value b2tlmv\_cflmv\_min is used (default 0.5). For densities in between b2tlmv\_ni\_min and b2tlmv\_ni\_max, the flux limiter is computed based on linear interpolation between the limiting values.
    

.. index:: b2sihs_phm0

``b2sihs_phm0``    type: ``real``    default: ``1.0``
    Multiplier of the contribution to electron heat sources from divergence(ue,ve). This term is superseded by the BoRiS switch if invoked.
    

.. index:: b2sihs_phm1

``b2sihs_phm1``    type: ``real``    default: ``1.0``
    Multiplier of the contribution to ion heat sources from divergence(ua,va). This term is superseded by the BoRiS switch if invoked.
    

.. index:: b2sihs_phm2

``b2sihs_phm2``    type: ``real``    default: ``1.0``
    Multiplier of the contribution to ion heat sources from viscous heating due to poloidal velocity differences. This term is superseded by the BoRiS switch if invoked.
    

.. index:: b2sihs_phm3

``b2sihs_phm3``    type: ``real``    default: ``1.0``
    Multiplier of the contribution to electron heat sources from Joule heating (electron-ion friction).
    

.. index:: b2sihs_phm4

``b2sihs_phm4``    type: ``real``    default: ``1.0``
    Multiplier of the contribution to ion heat sources from atom-atom friction. This term is superseded by the BoRiS switch if invoked.
    

.. index:: b2sihs_phm5

``b2sihs_phm5``    type: ``real``    default: ``1.0``
    Multiplier of the contribution to electron heat sources from divergence of the electrical drift. That contribution is also multiplied by facExB.
    

.. index:: b2sihs_phm6

``b2sihs_phm6``    type: ``real``    default: ``1.0``
    Multiplier of the contribution to ion heat sources from divergence of the electrical drift. That contribution is also multiplied by facExB.
    

.. index:: b2sihs_phm7

``b2sihs_phm7``    type: ``real``    default: ``0.0``
    Multiplier of the contribution to heat sources from friction due to diamagnetic velocities. Normally already included in 'phm3' term above.
    

.. index:: b2sihs_phm8

``b2sihs_phm8``    type: ``real``    default: ``1.0``
    Multiplier of the contribution to heat sources from viscous heating due to radial velocity differences. This term is only included when using b2nph9\_style.eq.1 or b2npht\_style.eq.1 (defaults). This term is superseded by the BoRiS switch if invoked.
    

.. index:: b2sdia_facgt

``b2sdia_facgt``    type: ``real``    default: ``0.0``
    Multiplier of the contribution to electron and ion heat sources from divergence of the gradTxB heat flux. That contribution is also multiplied by facdrift. This term is no longer needed as it has been transferred from being a source to being included in the flows.
    

.. index:: b2sral_style

``b2sral_style``    type: ``integer``    default: ``2``
    When set to '0' or '2', the code calls the standard b2stbc routine, which uses the particle flux with drift terms included in the expression of the electron particle flux (fne). Option '1' is obsolete. It is recommended '2'.
    

.. index:: b2sqcx_phm.

.. index:: b2sqcx_styl0, b2sqcx_phm0
.. c

``b2sqcx_phm.``

  - ``b2sqcx_styl0``  -     type: ``integer``    default: ``0``

  - ``b2sqcx_phm0``  -     type: ``real``    default: ``1.0``


    phm0 : Multiplier to the charge exchange rate coefficient. Subservient to styl0: only used if styl0.eq.0 or is.lt.2. If styl0.ne.0, the charge exchange rate coefficients for species of index 2 and above are set to zero.
    
.. index::
   single: b2sqcx_phm.; b2sqcx_styl0
   single: b2sqcx_phm.; b2sqcx_phm0


.. index:: b2sqel_phm0

``b2sqel_phm0``    type: ``real``    default: ``1.0``
    Multiplier to the ionisation rate coefficient.
    

.. index:: b2sqel_phm1

``b2sqel_phm1``    type: ``real``    default: ``1.0``
    Multiplier to the recombination rate coefficient.
    

.. index:: b2sqel_phm2

``b2sqel_phm2``    type: ``real``    default: ``1.0``
    Multiplier to the heat loss rate coefficient.
    

.. index:: b2stel_phm0

``b2stel_phm0``    type: ``real``    default: ``1.0``
    Multiplier of the sources due to atomic physics.
    

.. index:: b2tfhe_lim_flux

``b2tfhe_lim_flux``    type: ``integer``    default: ``0``
    If '0', flux limit is not applied directly to the electron heat flux but is applied through transport coefficients if 'b2trcl\_conductive\_limit' is '1'. It is recommended '0'.
    b2tfhe\_lim\_flux.eq.1 not yet available for WG.
    

.. index:: b2tfhi_lim_flux

``b2tfhi_lim_flux``    type: ``integer``    default: ``0``
    If '0', flux limit is not applied directly to the ion heat flux but is applied through transport coefficients if 'b2trcl\_conductive\_limit' is '1'. It is recommended '0'.
    b2tfhi\_lim\_flux.eq.1 not yet available for WG.
    

.. index:: b2treq_phm0

``b2treq_phm0``    type: ``real``    default: ``1.0``
    Multiplier to the temperature equipartition term.
    

.. index:: b2tqca_phm0

``b2tqca_phm0``    type: ``real``    default: ``1.0``
    Multiplier for the classical parallel viscosity.
    

.. index:: b2tqca_model

``b2tqca_model``    type: ``integer``    default: ``1``
    If model.eq.1, use the Balescu formulation from SOLPS5.2 classical parallel ion heat diffusivity.
    If model.eq.2, use the older Braginskii SOLPS4.0 model.
    Note: old option model.eq.3 removed, replaced with model.eq.1., but numerical treatment w.r.t. factor 4/3 according to old model.eq.3.
    

.. index:: b2tqce_model

``b2tqce_model``    type: ``integer``    default: ``1``
    If model.eq.1, use the fitted Balescu formulation from SOLPS5.0 classical parallel electron heat diffusivity.
    If model.eq.2, use the older Braginskii SOLPS4.0 model.
    If model.eq.3, use the 21-moment Balescu results.
    

.. index:: b2tqna_model_sig

``b2tqna_model_sig``    type: ``integer``    default: ``0``
    If '1', use constant density in core region to calculate anomalous conductivity sig0=dfsig\*qe\*ne(nmdpl,-1), nmdpl - number of midplane cell. If '0', use sig0=dfsig\*qe\*ne(x,y)
    

.. index:: b2trno_csig_an_style

``b2trno_csig_an_style``    type: ``integer``    default: ``1``
    If '1', the anomalous contributions in the parallel direction to the electrical conductivity csig and the thermo-electric coefficient calf are zeroed out.
    

.. index:: b2tqin_csigin_style

``b2tqin_csigin_style``    type: ``integer``    default: ``0``
    Integer switch to choose the expression for the ion-neutral conductivity.
    If '1', the ion-neutral conductivity is computed from hydrogen gas diffusivity (SOLPS5.2 treatment).
    If '0' (default), it is computed from the local CX rate (SOLPS5.0/5.1 and AFN treatments).
    

.. index:: b2trno_pol_anom_scale

``b2trno_pol_anom_scale``    type: ``real``    default: ``1.0``
    If pol\_anom\_scale.ne.1, the poloidal anomalous transport coefficients are scaled by the number. To get the same treatment as setting the old switch (radial\_only) to 1, set the new switch to 0.0.
    This multiplication is to only take place for charged species.
    

.. index:: eirene_l*

.. index:: eirene_lhalpha, eirene_lvib
.. c

``eirene_l*``

  - ``eirene_lhalpha``  -     type: ``integer``    default: ``1``

  - ``eirene_lvib``  -     type: ``integer``    default: ``1``


    Deprecated. Use "DEFINE\_LINES" in block 12 of Eirene input file instead.
    
.. index::
   single: eirene_l*; eirene_lhalpha
   single: eirene_l*; eirene_lvib


.. index:: eirene_repeat_first_call

``eirene_repeat_first_call``    type: ``integer``    default: ``1``
    If > 0 then repeats the first call to Eirene in eirene\_mc so many times.
    Useful if a density feedback gas puff is being used because the flux passed to Eirene on its first call is ignored (instead the value in the Eirene input file is used).
    

.. index:: eirene_use_recyceir

``eirene_use_recyceir``    type: ``integer``    default: ``1``
    If > 0 use recyceir (non species dependent) to specify the recycling coefficients, else if 0 use recyc (species dependent).
    

.. index:: eirene_ionising_core

``eirene_ionising_core``    type: ``integer``    default: ``0``
    If <> 0 then recycles the neutral flux having crossed the core boundary within Eirene as ions. The recycling is modulated as per the poloidal density distribution of the ions, and neutrals come back as fully-stripped ions.
    'eirene\_ionizing\_core' is an alias for this switch.
    If the value = 1, then the flux is added by direct modification of the sources in the guard cells --- this will only work if a standard flux boundary condition is applied at that boundary.
    If the value is < 0, then the absolute value specifies which boundary in b2.boundary.parameters is to be used. This will only work for the BCCON = 13 type boundary condition, for which a negative value for ionizing\_core is required.
    Cannot be used in conjunction with 'eirene\_ank\_mods'.
    Use of this switch is not allowed if the core boundary condition is not of a flux type. Moreover, certain boundary conditions expressly include the flux of neutrals already (BCCON = 6, 19, 21, 23, 26, or 27), in which case use of this switch is redundant and should be avoided.
    

.. index:: eirene_background

``eirene_background``    type: ``integer``    default: ``1``
    If eirene\_background.eq.0, the ion velocities passed to Eirene to be used for the collisions are based on grad-B and ExB drifts (vadia + vaecrb).
    If eirene\_background.eq.1, these velocities contain the full diamagnetic and ExB drifts (wadia + vaecrb).
    Note: recycling fluxes are always computed based on grad-B and ExB drifts only (and are not affected by this switch), because diamagnetic drift flows largely close within the sheath.
    

.. index:: eirene_sheath_pot

``eirene_sheath_pot``    type: ``integer``    default: ``1``
    If eirene\_sheath\_pot.eq.1, the sheath potential drop as computed by B2.5 (i.e. including effects of parallel currents, secondary electron emission, etc.) is passed to EIRENE to compute ion acceleration in the sheath.
    If eirene\_sheath\_pot.eq.0, the sheath potential drop is	recomputed by EIRENE, usually assuming zero current and secondary electron emission.
    

.. index:: b2mndr_atomic_physics_rescale

``b2mndr_atomic_physics_rescale``    type: ``integer``    default: ``0``
    If atomic\_physics\_rescale is not 0, then the code will rescale the rates stored in b2frates according to the multipliers given in the b2.atomic\_physics\_rescale.parameters inputfile before making use of them.
    

.. index:: neoclassical_ic

``neoclassical_ic``    type: ``integer``    default: ``3``
    ..set the contribution ic in NEOART
    0 --- classical particle flux
    1 --- banana plateau contribution
    2 --- Pfirsch-Schlueter contribution
    3 --- both banana and PS
    4 --- all contributions
    mind that B2.5 already calculates the classical transport !
    avoid double transport, 0+4 for cross-checks only !
    

.. index:: b2mndr_solve_keps

``b2mndr_solve_keps``    type: ``integer``    default: ``0``
    Main switch controlling the use of the k(-eps)-model. In this model, anomalous transport coefficients are determined self-consistently through the solution of an additional transport equation for the turbulent kinetic energy k (variable "kt" in the code) and possibly the turbulent enstrophy zeta (variable "zt" in the code). Note that both the k and k-eps models are currently under active development/testing, and should be used with care. In particular, the k-eps model (option '2') is not suitable for routine testing yet.
    If '0': k(-eps)-model not used.
    If '1': one additional transport equation solved for k.
    If '2': two additional transport equations solved for k and zeta. Warning: under development - expert use only!
    Note: solutions to these equations are only used to compute the transport coefficients if the switch b2tqna\_transport\_keps is set.
    

.. index:: b2tqna_transport_keps

``b2tqna_transport_keps``    type: ``integer``    default: ``0``
    Compute transport coefficients based on k(-eps)-model.
    If '0': transport coefficients not computed based on k(-eps)-model.
    If '1': transport coefficients computed using k-model (i.e. based on kt).
    If '2': transport coefficients computed using k-eps model (i.e. based on kt and zt). Warning: under development - expert use only!
    

.. index:: b2tqna_keps_local

``b2tqna_keps_local``    type: ``integer``    default: ``1``
    If '0': use Larmor radius at OMP separatrix in k(-eps)-model.
    If '1': use local Larmor radius for each cell in k(-eps)-model.
    

.. index:: b2tqna_keps_iout

``b2tqna_keps_iout``    type: ``integer``    default: ``0``
    If '1': print output for k(-eps)-model.
    

.. index:: b2tqna_keps_cd

``b2tqna_keps_cd``    type: ``real``    default: ``0.1``
    Multiplier for the diffusion coefficient in the k(-eps) model. Recommended range: 0.1 ... 1.0
    

.. index:: b2tqna_keps_shear

``b2tqna_keps_shear``    type: ``real``    default: ``0.0``
    Multiplier for the shear contribution to the diffusion coefficient in the k(-eps) model.
    Only affects results if ExB drifts are present.
    

.. index:: b2tqna_keps_heat

``b2tqna_keps_heat``    type: ``real``    default: ``2.0``
    Multiplier for the electron heat conductivity (w.r.t. diffusion coefficient).
    

.. index:: b2tqna_keps_heat_i

``b2tqna_keps_heat_i``    type: ``real``    default: ``2.0``
    Multiplier for the ion heat conductivity (w.r.t. diffusion coefficient).
    

.. index:: b2tqna_keps_visc

``b2tqna_keps_visc``    type: ``real``    default: ``0.2``
    Multiplier for the ion viscosity (w.r.t. diffusion coefficient).
    

.. index:: b2tqna_keps_sig

``b2tqna_keps_sig``    type: ``real``    default: ``1e-4``
    Multiplier for the anomalous electrical conductivity (w.r.t. diffusion coefficient x qe x ne(omp)).
    

.. index:: b2tqna_keps_alf

``b2tqna_keps_alf``    type: ``real``    default: ``1e-4``
    Multiplier for the anomalous thermo-electric coefficient (w.r.t. diffusion coefficient x sqrt(qe/te) x ne(omp)).
    

.. index:: b2tqna_keps_dkt

``b2tqna_keps_dkt``    type: ``real``    default: ``0.1``
    Multiplier for the k-conductivity (w.r.t. diffusion coefficient).
    

.. index:: b2tqna_keps_dzt

``b2tqna_keps_dzt``    type: ``real``    default: ``0.1``
    Multiplier for the diffusivity in z-equation (w.r.t. diffusion coefficient).
    

.. index:: b2tfhi_fflokt*

.. index:: b2tfhi_fflokt, b2tfhi_fconkt
.. c

``b2tfhi_fflokt*``

  - ``b2tfhi_fflokt``  -     type: ``real``    default: ``0.0``

  - ``b2tfhi_fconkt``  -     type: ``real``    default: ``0.0``


    fflokt and fconkt are fudge factors to approximate enhanced parallel transport of k due to term related to (fluctuations in parallel current) \* (fluctuations in potential)
    In principle this models the same effect as skt\_diss (thus: needs b2sikt\_fac\_sheath\_\* = 0.0).
    
.. index::
   single: b2tfhi_fflokt*; b2tfhi_fflokt
   single: b2tfhi_fflokt*; b2tfhi_fconkt


.. index:: b2tfhi_fflozt*

.. index:: b2tfhi_fflozt, b2tfhi_fconzt
.. c

``b2tfhi_fflozt*``

  - ``b2tfhi_fflozt``  -     type: ``real``    default: ``0.0``

  - ``b2tfhi_fconzt``  -     type: ``real``    default: ``0.0``


    fflozt and fconzt are fudge factors to the transport of zt. See code for details.
    
.. index::
   single: b2tfhi_fflozt*; b2tfhi_fflozt
   single: b2tfhi_fflozt*; b2tfhi_fconzt


.. index:: b2tfhe_vis_kt

``b2tfhe_vis_kt``    type: ``real``    default: ``0.0``
    Multiplier to the perpendicular current due to Reynolds-stress in k-model.
    

.. index:: b2tqna_keps_init*

.. index:: b2tqna_keps_init, b2tqna_keps_inc
.. c

``b2tqna_keps_init*``

  - ``b2tqna_keps_init``  -     type: ``real``    default: ``1.0``

  - ``b2tqna_keps_inc``  -     type: ``real``    default: ``1.0``


    Mechanism to enable a smooth transition between standard anomalous transport coefficients and k(-epsilon)-model coefficients.
    The final coefficients (dna0, vsa0, hcib, hce0, sig0, alf0) are linearly interpolated between the standard and the k(-epsilon) values based on keps\_fac.
    keps\_fac starts out as b2tqna\_keps\_init and the value is multiplied by b2tqna\_keps\_inc at each iteration.
    
.. index::
   single: b2tqna_keps_init*; b2tqna_keps_init
   single: b2tqna_keps_init*; b2tqna_keps_inc


.. index:: b2tfhi_fsigkt

``b2tfhi_fsigkt``    type: ``real``    default: ``0.1``
    Multiplier for the parallel transport term of kt.
    

.. index:: b2sikt_model

``b2sikt_model``    type: ``integer``    default: ``1``
    Model to compute the sources in the energy equations due to the k-eps model. Currently only a single model is available.
    

.. index:: b2sikt_style

``b2sikt_style``    type: ``integer``    default: ``0``
    Currently only a single computation style for the sources in the energy equations due to the k-eps model is available.
    

.. index:: b2sikt_sheath_local

``b2sikt_sheath_local``    type: ``integer``    default: ``1``
    If '0': use sound speed, connection length, and Larmor radius at OMP in k(-eps)-model.
    If '1': use local sound speed, connection length, and Larmor radius.
    

.. index:: b2sikt_kt_source_stab

``b2sikt_kt_source_stab``    type: ``integer``    default: ``1``
    Numerical stabilization of sources. See code for details.
    

.. index:: b2sikt_fac_diss

``b2sikt_fac_diss``    type: ``real``    default: ``10.0``
    Multiplier for the dissipation term of kt in the SOL region.
    

.. index:: b2sikt_fac_diss_core

``b2sikt_fac_diss_core``    type: ``real``    default: ``10.0``
    Multiplier for the dissipation term of kt in the core region.
    

.. index:: b2sikt_fac_sheath

``b2sikt_fac_sheath``    type: ``real``    default: ``0.0``
    Multiplier for the sheath loss term of kt in the SOL region.
    

.. index:: b2sikt_fac_sheath_core

``b2sikt_fac_sheath_core``    type: ``real``    default: ``0.0``
    Multiplier for the sheath loss term of kt in the core region.
    

.. index:: b2sikt_fac_diss_core_mode

``b2sikt_fac_diss_core_mode``    type: ``integer``    default: ``0``
    If '0': use connection length in expression for dissipation term of kt.
    If '1': use b2sikt\_fac\_diss\_lpar in expression for dissipation term of kt.
    

.. index:: b2sikt_min_source

``b2sikt_min_source``    type: ``integer``    default: ``0``
    If '1': sets minimum source for k to zero.
    

.. index:: b2sikt_fac_aniso

``b2sikt_fac_aniso``    type: ``integer``    default: ``1``
    If '1': add anisothermal contribution to transport coefficients from k-(epsilon)-model.
    

.. index:: b2sikt_fac_vis_RS

``b2sikt_fac_vis_RS``    type: ``real``    default: ``0.0``
    Multiplier for Reynolds-stress turbulent viscosity in k-model equations. Only active if ExB drifts are present.
    

.. index:: b2tfhi_fkt_hie

``b2tfhi_fkt_hie``    type: ``real``    default: ``0.0``
    Multiplier for transport of k associated with turbulent ExB heat fluxes.
    

.. index:: keps_anom_he_model

``keps_anom_he_model``    type: ``integer``    default: ``1``
    If set to 0, uses multiplier 5/2 for the anomalous convective and conductive heat fluxes associated with anomalous density transport, as per the SOLPS5.2 physics model.
    If set to 1 (default), uses multiplier 3/2 for the anomalous convective and conductive heat fluxes associated with electrostatic ExB drift turbulence, consistent with the keps-model derivation.
    If set to 2 (experimental), additionally assumes the corresponding physical fluxes across surfaces/boundaries to have multiplier 3/2.
    

.. index:: b2mn_afn

``b2mn_afn``    type: ``integer``    default: ``0``
    Main switch to turn on the AFN model for hydrogenic neutrals. If this switch is turned on, some default values are changed (see description of the corresponding switches).
    

.. index:: b2mn_spatial_hybrid

``b2mn_spatial_hybrid``    type: ``integer``    default: ``0``
    Switch to turn on the spatially hybrid fluid-kinetic neutral model. For multispecies simulations, the hybrid approach can only be used for the hydrogenic neutrals. For other species, you can use either a fully kinetic or purely fluid approach.
    

.. index:: b2stbr_recycle_afn

``b2stbr_recycle_afn``    type: ``integer``    default: ``0``
    When set to 1, the AFN recycling boundary conditions are used for hydrogenic neutrals. When b2mn\_afn.ne.0 and there is no specification of b2stbr\_recycle\_afn, the switch is automatically set to 1.
    

.. index:: b2stbr_afn_bcs_use_coarse

``b2stbr_afn_bcs_use_coarse``    type: ``integer``    default: ``1``
    When set to 1, the coarse representation of the integrated TRIM reflection coefficients is used for the AFN boundary conditions, which is expected to be sufficient. In case you want to use the original fine representation, use b2stbr\_afn\_bcs\_use\_coarse = 0. However, the fine representation is only present for D on Be, C and W.
    

.. index:: b2tqna_transport_afn

``b2tqna_transport_afn``    type: ``integer``    default: ``0``
    When set to 1, the AFN transport coefficients are used for hydrogenic neutrals. When b2mn\_afn.ne.0 and there is no specification of b2stbr\_transport\_afn, the switch is automatically set to 1.
    

.. index:: b2tqna_afn_vnn

``b2tqna_afn_vnn``    type: ``integer``    default: ``1``
    When set to 1, a collision frequency related to neutral-neutral collisions is added to the AFN transport coefficients. This is an ad-hoc model for fluid neutral transport in regions where plasma density is extremely low and CX effectively absent (e.g. below dome, far-SOL,...). When set to 0, the correction is not added.
    

.. index:: b2tqna_afn_vnn_ndiff

``b2tqna_afn_vnn_ndiff``    type: ``integer``    default: ``0``
    When set to 1, perpendicular transport in the AFN model due to neutral-neutral collisions is modelled as density diffusion rather than pressure diffusion. When set to 0, it is modelled as pressure diffusion.
    

.. index:: b2mn_tn_style

``b2mn_tn_style``    type: ``integer``    default: ``0``
    0: solving the total energy equation for all ion + (fluid) neutral species together; 1: solving the total energy equation without the contributions from hydrogenic neutrals. It is still assumed that the hydrogenic neutrals have the same temperature as the ions, i.e. tn=ti. (not recommended to turn on); 2: separate energy equation for the hydrogenic neutrals (tn.ne.ti). For simulations with hydrogenic mixtures and b2mn\_tn\_style = 2, a total energy equation for all hydrogenic neutrals together will be solved assuming tn for each hydrogenic neutral species.
    

.. index:: use_auto_spatial_hyb

``use_auto_spatial_hyb``    type: ``integer``    default: ``0``
    Advanced hybrid option. Forbidden to use for multispecies simulations (ns > 1) and only in use for the strata with HYB\_TYPE='A'.
    The local charge-exchange Knudsen number Kn is calculated at the boundary.
    If (Kn < auto\_spatial\_hyb\_Kn\_1) then the recycled atom is treated as a fluid.
    If (Kn > auto\_spatial\_hyb\_Kn\_2) then the recycled atom is treated kinetically.
    (otherwise) linear combination between fluid and kinetic.
    

.. index:: l_macro_afn

``l_macro_afn``    type: ``real``    default: ``0.1``
    Macroscopic length scale (in m) used to calculate the local Knudsen number.
    

.. index:: b2stbr_kn_b1

``b2stbr_kn_b1``    type: ``real``    default: ``0.01``
    Should be used in combination with MAXW in b2.neutrals.parameters (see description MAXW).
    

.. index:: b2stbr_kn_b2

``b2stbr_kn_b2``    type: ``real``    default: ``0.1``
    Should be used in combination with MAXW in b2.neutrals.parameters (see description MAXW).
    

.. index:: auto_spatial_hyb_Kn_1

``auto_spatial_hyb_Kn_1``    type: ``real``    default: ``0.0``
    Should be used in combination with use\_auto\_spatial\_hyb (see description use\_auto\_spatial\_hyb).
    

.. index:: auto_spatial_hyb_Kn_2

``auto_spatial_hyb_Kn_2``    type: ``real``    default: ``0.0``
    Should be used in combination with use\_auto\_spatial\_hyb (see description use\_auto\_spatial\_hyb).
    

.. index:: b2stbr_remove_fc_el

``b2stbr_remove_fc_el``    type: ``integer``    default: ``0``
    When set to 1, the energy required for the Franck-Condon dissociation of the thermally released particles at the surfaces in the AFN boundary conditions is subtracted from the electron energy equation. It is not recommended to turn this switch on, because it seems to lower the electron temperature to unrealistic values.
    

.. index:: b2trcl_min_collisions

``b2trcl_min_collisions``    type: ``real``    default: ``0.0``
    Defines the style of the ion heat flux limit. If the number of collisions in the flux tube (determined by its average collisionnality) is larger than the value in the key, the old style of ion flux limit will be applied. Otherwise the new style (flux limit is defined by the number of collisions) will be applied.
    

.. index:: b2stbc_delpo

``b2stbc_delpo``    type: ``real``    default: ``3.1``
    Potential drop used for BCENI/E = 15 when the potential equation is not solved (pot\_eq.ne.1), in units of the local electron temperature.
    

.. index:: b2tlc0_style_*

.. index:: b2tlv0_style, b2tlc0_style, b2tlh0_style
.. c

``b2tlc0_style_*``

  - ``b2tlv0_style``  -     type: ``integer``    default: ``1``

  - ``b2tlc0_style``  -     type: ``integer``    default: ``1``

  - ``b2tlh0_style``  -     type: ``integer``    default: ``1``


    Determines the method for applying flux limiters to fluid neutrals.
    style.eq.0: old treatment where the radial and poloidal conductive fluxes are limited separately.
    style.eq.1: improved treatment (isotropic flux limiters) where the total conductive flux is limited, preventing artificial rotation of the flow.
    
.. index::
   single: b2tlc0_style_*; b2tlv0_style
   single: b2tlc0_style_*; b2tlc0_style
   single: b2tlc0_style_*; b2tlh0_style


.. index:: b2tqna_keps_dna_min*

.. index:: b2tqna_keps_dna_min, b2tqna_keps_vsa_min, b2tqna_keps_hci_min, b2tqna_keps_hce_min
.. c

``b2tqna_keps_dna_min*``

  - ``b2tqna_keps_dna_min``  -     type: ``real``    default: ``1.0e-2``

  - ``b2tqna_keps_vsa_min``  -     type: ``real``    default: ``1.0e-2``

  - ``b2tqna_keps_hci_min``  -     type: ``real``    default: ``1.0e-2``

  - ``b2tqna_keps_hce_min``  -     type: ``real``    default: ``1.0e-2``


    Minimum transport coefficients for use in k-epsilon model. It is also possible to use these minima for other transport models by setting b2tqna\_limit\_coeff.eq.1.
    
.. index::
   single: b2tqna_keps_dna_min*; b2tqna_keps_dna_min
   single: b2tqna_keps_dna_min*; b2tqna_keps_vsa_min
   single: b2tqna_keps_dna_min*; b2tqna_keps_hci_min
   single: b2tqna_keps_dna_min*; b2tqna_keps_hce_min


.. index:: b2tqna_limit_coeff

``b2tqna_limit_coeff``    type: ``integer``    default: ``0``
    b2tqna\_limit\_coeff.ne.0: the minimum transport coefficients dna\_min, vsa\_min, hci\_min and hce\_min are for whatever transport model is selected.
    b2tqna\_limit\_coeff.eq.0: the minimum transport coefficients dna\_min, vsa\_min, hci\_min and hce\_min are only used for the k-epsilon model.
    

.. index:: b2siav_cqip1

``b2siav_cqip1``    type: ``real``    default: ``0.5``
    Constant c\_q1 in calculation of additional viscosity terms calculated in b2siav.
    

.. index:: b2sigp_phm0

``b2sigp_phm0``    type: ``real``    default: ``1.0``
    Multiplier for the pressure gradient term. Setting b2sigp\_phm0.ne.1.0 should only be done for specific testing purposes.
    

.. index:: b2nxfv_phm0

``b2nxfv_phm0``    type: ``real``    default: ``1.0``
    Multiplier for the convective term due to new form of ion viscosity term in the momentum correction equation. Applies to hydrogenic ions and fluid neutrals.
    

.. index:: b2nxfv_phm1

``b2nxfv_phm1``    type: ``real``    default: ``1.0``
    Multiplier for the convective term due to new form of ion viscosity term in the momentum correction equation. Applies only to hydrogenic fluid neutrals.
    

.. index:: b2stbc_phm0

``b2stbc_phm0``    type: ``real``    default: ``1.0``
    Multiplier for radial diamagnetic current in BCPOT=12.
    

.. index:: b2stbc_phm1

``b2stbc_phm1``    type: ``real``    default: ``1.0``
    Multiplier for radial inertial current in BCPOT=12.
    

.. index:: b2stbm_internal_energy_sources

``b2stbm_internal_energy_sources``    type: ``integer``    default: ``0``
    internal\_energy\_sources.eq.0: the externally provided energy sources are total energy sources and a conversion to internal energy sources is performed.
    internal\_energy\_sources.eq.1: the externally provided energy sources are already internal energy sources.
    

.. index:: b2tfhe_anomalous

``b2tfhe_anomalous``    type: ``real``    default: ``1.0``
    Multiplier to the anomalous current.
    

.. index:: b2tanml_anomalous

``b2tanml_anomalous``    type: ``real``    default: ``1.0``
    The correct switch is now b2tfhe\_anomalous. b2tanml\_anomalous is kept for backward compatibility. b2tanml\_anomalous will only be read if b2tfhe\_anomalous.eq.1.0.
    

.. index:: b2tqna_cfvma

``b2tqna_cfvma``    type: ``real``    default: ``0.0``
    Anomalous velocity in parallel momentum balance equation.
    

.. index:: b2tstbc_bc_ref*

.. index:: b2stbc_bc_ref, b2stbc_bc_ref_ti, b2stbc_bc_ref_te
.. c

``b2tstbc_bc_ref*``

  - ``b2stbc_bc_ref``  -     type: ``real``    default: ``0.01``

  - ``b2stbc_bc_ref_ti``  -     type: ``real``    default: ``0.01``

  - ``b2stbc_bc_ref_te``  -     type: ``real``    default: ``0.01``


    Under-relaxation factors related to feedback schemes for boundary conditions.
    
.. index::
   single: b2tstbc_bc_ref*; b2stbc_bc_ref
   single: b2tstbc_bc_ref*; b2stbc_bc_ref_ti
   single: b2tstbc_bc_ref*; b2stbc_bc_ref_te


.. index:: 
   single: Physics; b2siav_addvis
   single: Physics; b2siav_addvis1
   single: Physics; b2siav_style_qip
   single: Physics; b2npmo_b2sifr_
   single: Physics; b2sihs_istyle_Joule_heating
   single: Physics; b2sian_phm0
   single: Physics; b2sicf_phm0
   single: Physics; b2sicf_phm1
   single: Physics; b2t*_anomalous
   single: Physics; b2news_ExB
   single: Physics; b2news_vis
   single: Physics; b2tiner_inert
   single: Physics; b2tfhe_dia_cur
   single: Physics; b2tfhe_vdia_par
   single: Physics; b2tfhe_neutral
   single: Physics; b2tinnt_fchin_in_core
   single: Physics; b2tfhe_PSch
   single: Physics; b2tfhe_vis_par
   single: Physics; b2tfhe_vis_q
   single: Physics; b2tfhe_stochastic
   single: Physics; b2tstch_delta
   single: Physics; b2tstch_sig
   single: Physics; b2trno_con_e_stochastic
   single: Physics; b2trcl_lluciani
   single: Physics; b2trcl_lthf21
   single: Physics; b2trcl_lvis21
   single: Physics; b2tral_Zhdanov_closure
   single: Physics; b2tral_zh_imp_analyt
   single: Physics; b2tral_zh_analyt_mdf
   single: Physics; b2tral_Zhdanov_cond
   single: Physics; b2tral_Zhdanov_vish
   single: Physics; b2tral_Zhdanov_visu
   single: Physics; b2tral_zhflcorr
   single: Physics; b2tral_zhflcorrh
   single: Physics; b2tral_zhd_corr
   single: Physics; b2tral_zhd_corrT
   single: Physics; b2tral_zhcscorr
   single: Physics; b2tral_zhcscorr_vq
   single: Physics; b2sifr_Zhdanov_tf_fr
   single: Physics; b2sifr_Zhdanov_test
   single: Physics; b2tfhi_Zhdanov_vel_heat
   single: Physics; b2tral_zh_tf_toff
   single: Physics; b2tral_zh_vis_type
   single: Physics; b2npmo_smbvi_factor
   single: Physics; b2tral_amfact_on
   single: Physics; b2tral_amfact_***
   single: Physics; b2npmo_impr_form_fr
   single: Physics; b2npmo_impr_form_tf
   single: Physics; b2npmo mass multiplicator
   single: Physics; b2sqel_artificial_radiation
   single: Physics; b2stbc_*
   single: Physics; b2stbc_type13..21*
   single: Physics; b2stbc_bcene_15_style
   single: Physics; b2stbc_bceni_15_style
   single: Physics; b2stbc_bcene_16_style
   single: Physics; b2stbc_bceni_16_style
   single: Physics; b2stbc_secmodel
   single: Physics; b2mndr_boundary_sources
   single: Physics; b2mndr_equation_sources
   single: Physics; b2mndr_mms_...
   single: Physics; b2stbr_sputtering...
   single: Physics; b2stbr_refl*
   single: Physics; b2mndr_coronal_model
   single: Physics; b2mndr_hz
   single: Physics; b2tfhe_alfTeEh
   single: Physics; b2tfhe_fch_pTe
   single: Physics; b2tfnb_xcur
   single: Physics; b2tfnb_ycur
   single: Physics; b2tfnb_vis_per
   single: Physics; b2tfnb_vis_q
   single: Physics; b2tqce_fke_Zhdanov
   single: Physics; b2tqce_style_guard_cells
   single: Physics; b2tqna_user_transport...
   single: Physics; b2tqna_m*
   single: Physics; b2tqna_new_df0
   single: Physics; b2tqna_ballooning
   single: Physics; b2tqna_pfr_rescale
   single: Physics; b2tqna_divsol_rescale
   single: Physics; b2sifr_phm0
   single: Physics; b2sifr_phm1
   single: Physics; b2sifr_phm2
   single: Physics; b2sifr_phm3
   single: Physics; b2sifr_limth*
   single: Physics; b2trcl_cth*
   single: Physics; b2tlnl_*
   single: Physics; b2tfnb_PSch
   single: Physics; b2news_BoRiS
   single: Physics; b2tfhe_conduction_only
   single: Physics; b2tfnb_flux...
   single: Physics; b2tlc0_*
   single: Physics; b2tlh0_*
   single: Physics; b2tlv0_*
   single: Physics; b2tlmv_style
   single: Physics; b2tlhe_far_sol
   single: Physics; b2tlhi_far_sol
   single: Physics; b2tlmv_far_sol
   single: Physics; b2sihs_phm0
   single: Physics; b2sihs_phm1
   single: Physics; b2sihs_phm2
   single: Physics; b2sihs_phm3
   single: Physics; b2sihs_phm4
   single: Physics; b2sihs_phm5
   single: Physics; b2sihs_phm6
   single: Physics; b2sihs_phm7
   single: Physics; b2sihs_phm8
   single: Physics; b2sdia_facgt
   single: Physics; b2sral_style
   single: Physics; b2sqcx_phm.
   single: Physics; b2sqel_phm0
   single: Physics; b2sqel_phm1
   single: Physics; b2sqel_phm2
   single: Physics; b2stel_phm0
   single: Physics; b2tfhe_lim_flux
   single: Physics; b2tfhi_lim_flux
   single: Physics; b2treq_phm0
   single: Physics; b2tqca_phm0
   single: Physics; b2tqca_model
   single: Physics; b2tqce_model
   single: Physics; b2tqna_model_sig
   single: Physics; b2trno_csig_an_style
   single: Physics; b2tqin_csigin_style
   single: Physics; b2trno_pol_anom_scale
   single: Physics; eirene_l*
   single: Physics; eirene_repeat_first_call
   single: Physics; eirene_use_recyceir
   single: Physics; eirene_ionising_core
   single: Physics; eirene_background
   single: Physics; eirene_sheath_pot
   single: Physics; b2mndr_atomic_physics_rescale
   single: Physics; neoclassical_ic
   single: Physics; b2mndr_solve_keps
   single: Physics; b2tqna_transport_keps
   single: Physics; b2tqna_keps_local
   single: Physics; b2tqna_keps_iout
   single: Physics; b2tqna_keps_cd
   single: Physics; b2tqna_keps_shear
   single: Physics; b2tqna_keps_heat
   single: Physics; b2tqna_keps_heat_i
   single: Physics; b2tqna_keps_visc
   single: Physics; b2tqna_keps_sig
   single: Physics; b2tqna_keps_alf
   single: Physics; b2tqna_keps_dkt
   single: Physics; b2tqna_keps_dzt
   single: Physics; b2tfhi_fflokt*
   single: Physics; b2tfhi_fflozt*
   single: Physics; b2tfhe_vis_kt
   single: Physics; b2tqna_keps_init*
   single: Physics; b2tfhi_fsigkt
   single: Physics; b2sikt_model
   single: Physics; b2sikt_style
   single: Physics; b2sikt_sheath_local
   single: Physics; b2sikt_kt_source_stab
   single: Physics; b2sikt_fac_diss
   single: Physics; b2sikt_fac_diss_core
   single: Physics; b2sikt_fac_sheath
   single: Physics; b2sikt_fac_sheath_core
   single: Physics; b2sikt_fac_diss_core_mode
   single: Physics; b2sikt_min_source
   single: Physics; b2sikt_fac_aniso
   single: Physics; b2sikt_fac_vis_RS
   single: Physics; b2tfhi_fkt_hie
   single: Physics; keps_anom_he_model
   single: Physics; b2mn_afn
   single: Physics; b2mn_spatial_hybrid
   single: Physics; b2stbr_recycle_afn
   single: Physics; b2stbr_afn_bcs_use_coarse
   single: Physics; b2tqna_transport_afn
   single: Physics; b2tqna_afn_vnn
   single: Physics; b2tqna_afn_vnn_ndiff
   single: Physics; b2mn_tn_style
   single: Physics; use_auto_spatial_hyb
   single: Physics; l_macro_afn
   single: Physics; b2stbr_kn_b1
   single: Physics; b2stbr_kn_b2
   single: Physics; auto_spatial_hyb_Kn_1
   single: Physics; auto_spatial_hyb_Kn_2
   single: Physics; b2stbr_remove_fc_el
   single: Physics; b2trcl_min_collisions
   single: Physics; b2stbc_delpo
   single: Physics; b2tlc0_style_*
   single: Physics; b2tqna_keps_dna_min*
   single: Physics; b2tqna_limit_coeff
   single: Physics; b2siav_cqip1
   single: Physics; b2sigp_phm0
   single: Physics; b2nxfv_phm0
   single: Physics; b2nxfv_phm1
   single: Physics; b2stbc_phm0
   single: Physics; b2stbc_phm1
   single: Physics; b2stbm_internal_energy_sources
   single: Physics; b2tfhe_anomalous
   single: Physics; b2tanml_anomalous
   single: Physics; b2tqna_cfvma
   single: Physics; b2tstbc_bc_ref*

.. index:: Output

Output
======
.. index:: b2mndr_b2time

``b2mndr_b2time``    type: ``integer``    default: ``1``
    Specifies the number of timesteps between writes of the b2time.nc time-dependent file. If b2time.gt.0, always writes out on the last timestep. If b2mndr\_stim.lt.0, data from the current run is appended to the existing b2time.nc file, otherwise the file is overwritten.
    

.. index:: b2mndr_tally

``b2mndr_tally``    type: ``integer``    default: ``1``
    Specifies the number of timesteps between writes of tallies. If tally.gt.0, always writes out on the last timestep.
    

.. index:: b2mndt_moitlv

``b2mndt_moitlv``    type: ``integer``    default: ``-1``
    Controls detailed monitoring output. moitlv.eq.-1 means no output, moitlv.eq.0 means output once per timestep, moitlv.eq.1 means output once per nstg0 iteration, moitlv.eq.2 means output once per nstg1 iteration and moitlv.eq.3 means output once per nstg2 iteration. See 'b2mndr\_nstg?' description in Run section for more details.
    

.. index:: b2mndt_moqtlv

``b2mndt_moqtlv``    type: ``integer``    default: ``3``
    Controls quick trace output. moqtlv.eq.-1 means no output, moqtlv.eq.0 means output once per timestep, moqtlv.eq.1 means output once per nstg0 iteration, moqtlv.eq.2 means output once per nstg1 iteration and moqtlv.eq.3 means output once per nstg2 iteration. See 'b2mndr\_nstg?' description in Run section for more details.
    

.. index:: b2mndr_mvnum

``b2mndr_mvnum``    type: ``integer``    default: ``0``
    Specifies the maximum number of instances at which movie data will be output.
    

.. index:: b2mndr_mvinc

``b2mndr_mvinc``    type: ``integer``    default: ``1``
    Specifies the number of timesteps between movie output. If greater than 1 and the last timestep does not correspond to a planned frame, an extra endstate frame is added.
    

.. index:: b2mndr_plasnum

``b2mndr_plasnum``    type: ``integer``    default: ``0``
    Specifies the maximum number of instances at which extra writes of b2fplasmf.xxxx will occur.
    

.. index:: b2mndr_plasinc

``b2mndr_plasinc``    type: ``integer``    default: ``1``
    Specifies the number of timesteps between b2fplasmf.xxxx writes.
    

.. index:: b2mndr_cdfmovietim

``b2mndr_cdfmovietim``    type: ``real``    default: ``0.0``
    If non-zero, the movie file b2movies.nc is generated, containing several 2d quantities. Gives the real-time interval between writes of movie frames in b2movies.nc. If non-zero, must be at least as large as the simulation timestep.
    

.. index:: cdfmovie_fields

``cdfmovie_fields``    type: ``integer``    default: ``1``
    Controls the quantities outputted to b2movies.nc. If cdfmovie\_fields.ge.1 then only the main state variables (na, ne, Te, Ti, etc.) are written with each write to b2movies.nc. If cdfmovie\_fields.ge.2 then additional quantities (e.g. fluxes, particle and energy sources) are also included.
    

.. index:: b2mndr_ntim_save

``b2mndr_ntim_save``    type: ``integer``    default: ``0``
    Another option for plasma state file output. If greater than 0, gives the number of B2.5 full interations between successive write-ups of plasmastate files, in addition to the ones written at regular CPU intervals (see b2mndr\_savecpu and b2mndr\_plasmatim). Should be used, at the exclusion of other plasmastate write-up frequency settings, in conjunction with the Leuven Monte Carlo averaging scheme.
    

.. index:: b2mndt_av

``b2mndt_av``    type: ``integer``    default: ``0``
    If b2mndt\_av.gt.0, turns on computation of running averages.
    

.. index:: b2mndt_av_continue

``b2mndt_av_continue``    type: ``integer``    default: ``1``
    If b2mndt\_av\_continue.gt.0, continuously perform running averages.
    

.. index:: b2mndt_av_ntim_batch

``b2mndt_av_ntim_batch``    type: ``integer``    default: ``500``
    If ntim\_batch.gt.0, number of iterations used to compute batch averages, written out in 'b2batch.nc'.
    

.. index:: b2mndt_av_ntim_run

``b2mndt_av_ntim_run``    type: ``integer``    default: ``1000``
    If ntim\_run.gt.0, number of iterations used for writing running averages.
    

.. index:: b2mndt_av_batch_all

``b2mndt_av_batch_all``    type: ``integer``    default: ``0``
    If b2mndt\_av\_batch\_all.gt.0, produces standard output for batch averages.
    

.. index:: b2mndr_plasmatim

``b2mndr_plasmatim``    type: ``real``    default: ``0.0``
    Another option for plasma state file output. If greater than 0, gives the real-time interval between successive write-ups of plasmastate files, in addition to the ones written at regular CPU intervals (see b2mndr\_savecpu and b2mndr\_ntim\_save). Must then be at least as large as the simulation timestep.
    

.. index:: b2mndr_ids_save

``b2mndr_ids_save``    type: ``integer``    default: ``0``
    Frequency, in timesteps, at which an IDS is saved containing the plasma state. Can be used in conjunction with b2mndr\_ids\_time and b2mndr\_ids\_av.
    If used, an IDS time slice will be written at the end of run.
    If negative, a single IDS will be written at the end of the run.
    Will not work if running a "0 timesteps" simulation, in which case the use of b2\_ual\_write is recommended.
    

.. index:: b2mndr_ids_time

``b2mndr_ids_time``    type: ``real``    default: ``0.0``
    Frequency, in simulation seconds, at which an IDS is saved containing the plasma state. Can be used in conjunction with b2mndr\_ids\_save and b2mndr\_ids\_av.
    If non-zero, must be at least as large as the simulation timestep.
    If used, an IDS time slice will be written at the end of run.
    Will not work if running a "0 timesteps" simulation, in which case the use of b2\_ual\_write is recommended.
    

.. index:: b2mndr_ids_av

``b2mndr_ids_av``    type: ``integer``    default: ``0``
    Frequency, in number of batch averages, at which an IDS is saved containing the averaged plasma state. Can be used in conjunction with b2mndr\_ids\_save and b2mndr\_ids\_time.
    The averaged plasma state is saved as a separate occurrence of the edge\_profiles and edge\_sources IDSs.
    

.. index:: b2wdat_iout

``b2wdat_iout``    type: ``integer``    default: ``0``
    If iout.eq.1, a large set of \*.dat output files will be produced containing the values of a variety of code quantities, evaluated at the end of the B2.5 iteration.
    If iout.eq.4, an even larger set of output files will be produced, for the purposes of a full run analysis, evaluated in the individual routines where the quantities are used.
    For even more detailed debugging analysis, one should instead use "procedure\_name"\_iout.eq.1.
    The files and their content are fully described in the Output\_description.pdf file in the $SOLPSTOP/doc directory and Appendix G of the SOLPS-ITER manual.
    

.. index:: get_residuals

``get_residuals``    type: ``integer``    default: ``0``
    If get\_residuals.eq.1, then the residuals of unsolved equations will be outputted into b2ftrace. Equations are unsolved if 'b2news\_no\_solve' is nonzero or any elements of the solveco, solvemo, solveee, solveei, or solvepo are set to .false. .
    By default, get\_residuals.eq.0 and the residuals for unsolved equations are set to zero.
    The residual of the total momentum equation is nonzero when all momentum equations for parallel velocities are solved together.
    The residual of the total energy equation is nonzero when Te and Ti equations are solved together.
    

.. index:: b2wdat_append

``b2wdat_append``    type: ``integer``    default: ``0``
    If append.ne.0, the output files produced by the b2wdat\_iout.eq.4 switch are appended upon every write, instead of being rewritten every time.
    

.. index:: my_out_digits

``my_out_digits``    type: ``integer``    default: ``6 or 15``
    Specifies the number of significant digits with which the \*.dat files are written out. Defaults to 6 in normal mode and 15 in debug mode.
    Must be positive.
    

.. index:: b2mndr_old_style

``b2mndr_old_style``    type: ``integer``    default: ``0``
    If old\_style.gt.0, old-fashioned (SOLPS4 style) output is added at the end of the b2mn.prt file.
    

.. index:: b2mndr_av_read

``b2mndr_av_read``    type: ``integer``    default: ``0``
    If b2mndr\_av\_read.gt.0, the initial plasma is the averaged solution read from the b2faveri file. Check $SOLPSTOP/doc/SOLPS-ITER\_Eirene\_averaging.pdf for details.
    

.. index:: b2mndr_*

.. index:: b2mndr_na_eps, b2mndr_po_eps, b2mndr_te_eps, b2mndr_ti_eps, b2mndr_ua_eps
.. c

``b2mndr_*``

  - ``b2mndr_na_eps``  -     type: ``real``    default: ``1.0e19``

  - ``b2mndr_po_eps``  -     type: ``real``    default: ``1.0e+1``

  - ``b2mndr_te_eps``  -     type: ``real``    default: ``1.0e+1``

  - ``b2mndr_ti_eps``  -     type: ``real``    default: ``1.0e+1``

  - ``b2mndr_ua_eps``  -     type: ``real``    default: ``1.0e+4``


    The five switches above are safeguards numbers for when printing changes after a time step. The change is computed as: deltaX = abs((X(t)-X(t-1))/(X(t)+X\_eps))
    
.. index::
   single: b2mndr_*; b2mndr_na_eps
   single: b2mndr_*; b2mndr_po_eps
   single: b2mndr_*; b2mndr_te_eps
   single: b2mndr_*; b2mndr_ti_eps
   single: b2mndr_*; b2mndr_ua_eps


.. index:: b2mndr_trantim

``b2mndr_trantim``    type: ``real``    default: ``0.0``
    Produces a numbered 'tran' file every trantim real-time seconds. An endstate file is written if it falls between scheduled write-up times. Only available within the -DJET environment. If non-zero, must be at least as large as the simulation timestep.
    

.. index:: b2mwti_target_offset

``b2mwti_target_offset``    type: ``integer``    default: ``1``
    The diagnostic values from b2time.nc use guard cell values if target\_offset.eq.0, and values from the neighbouring real cell if target\_offset.eq.1. Fluxes are not affected.
    

.. index:: b2mwti_2dwrite

``b2mwti_2dwrite``    type: ``integer``    default: ``0``
    Controls additional output to b2time.nc.  If 2dwrite.ge.1 then a few 2d arrays (ne, Te, Ti) are written with each write to b2time.nc. If 2dwrite.ge.2 then fluxes, electric potential, kinetic energy, and fluid particle and energy source terms are also included (e.g., rsana, rsahi, rqrad).
    

.. index:: b2mwti_ismain0

``b2mwti_ismain0``    type: ``integer``    default: ``0``
    Index of the species used to create the 'dp3d?.last10' diagnostic files.
    Defaults to the neutral species associated with ismain. If no such species is declared, the default will be set to ismain. Is expected to either correspond to a neutral species or to ismain.
    Can also be used in b2ar.dat to specify the index of the main neutral CX species when resorting to the AMNS database (starting from version 1.3.2).
    If ismain is also defaulted, then will be 0.
    

.. index:: b2mwqt_style

``b2mwqt_style``    type: ``integer``    default: ``1``
    Specifies the amount of data that is written out to b2ftrace. See the manual (Section on b2yq) for full details.
    

.. index:: b2stbr_*_netcdf

.. index:: tallies_netcdf, b2stbr_b2wall_netcdf, balance_netcdf, balance_average
.. c

``b2stbr_*_netcdf``

  - ``tallies_netcdf``  -     type: ``integer``    default: ``0``

  - ``b2stbr_b2wall_netcdf``  -     type: ``integer``    default: ``0``

  - ``balance_netcdf``  -     type: ``integer``    default: ``0``

  - ``balance_average``  -     type: ``integer``    default: ``0``


    If tallies\_netcdf.ne.0, the file 'b2tallies.nc' is created, which contains the regional tallies in CDF format. If b2mndr\_stim.lt.0, data from the current run is appended to the existing b2tallies.nc file, otherwise the file is overwritten.
    If b2mndt\_av\_ntim\_batch.gt.0, the file 'b2batch.nc' is created, which contains the batch averages of the tallies.
    If b2wall\_netcdf.ne.0, the file 'b2wall.nc' is created, which contains the wall tallies in CDF format [written every b2wall\_netcdf main calls]. If b2mndr\_stim.lt.0, data from the current run is appended to the existing b2wall.nc file, otherwise the file is overwritten.
    If balance\_netcdf.ne.0, the file 'balance.nc' is created, which contains all of the arrays required by the balance post-processing routines, in CDF format.
    If balance\_average.ne.0, the balance arrays are averaged over the number of completed timesteps (itim).
    
.. index::
   single: b2stbr_*_netcdf; tallies_netcdf
   single: b2stbr_*_netcdf; b2stbr_b2wall_netcdf
   single: b2stbr_*_netcdf; balance_netcdf
   single: b2stbr_*_netcdf; balance_average


.. index:: ank_tracing

``ank_tracing``    type: ``integer``    default: ``0``
    If ank\_tracing.ge.1, additional tracing output from Andrei Kukushkin is produced, in files to be found in the tracing/ directory inside the run directory. The traces will be written every ank\_tracing iteration. If b2mndr\_stim.lt.0, data from the current run is appended to the existing files, otherwise the files are overwritten.
    

.. index:: b2stbc_diagno

``b2stbc_diagno``    type: ``integer``    default: ``0``
    Controls level of output in b2stbc and subservient routines.
    Level 1 (diagno.ge.1) output includes wrong\_flow warnings, transport coefficients at the (nx/2,ny) basis mesh position, the solution found for the given heat flux at constant temperature bc, and all feedback diagnostics.
    Level 2 output (diagno.ge.2) includes the integral current correction, the boundary sources on the first call, excessive sound speeds, and the iterative progress to the given heat flux at constant temperature bc.
    Level 3 output (diagno.ge.3) includes the boundary sources on each call, and the boundary.prt file listing all boundary cells.
    

.. index:: b2stbr_output

``b2stbr_output``    type: ``integer``    default: ``0``
    Output flag for the first\_flight model. If output.ge.1, the files start, end, and fort.88 are created, which contain information about the chords used in the model.
    

.. index:: b2npmo_vlct_diagno

``b2npmo_vlct_diagno``    type: ``integer``    default: ``1``
    Output flag to control diagnostics related to use of ion\_vlct\_restrict switch.
    If vlct\_diagno.eq.0, the velocity restrictions are applied silently.
    If vlct\_diagno.eq.1 (default), the user only gets a count of how many times the velocity restriction has been applied for each species, if any.
    If vlct\_diagno.eq.2, the user gets the full details of where and how large the applied velocity restriction was, if any.
    

.. index:: eirene_savef3*

.. index:: eirene_savef30, eirene_savef31
.. c

``eirene_savef3*``

  - ``eirene_savef30``  -     type: ``integer``    default: ``0``

  - ``eirene_savef31``  -     type: ``integer``    default: ``0``


    For coupled runs, the code will create two files named fort.30 and fort.31, containing the plasma geometry and plasma state, respectively, for use by Eirene. This happens irrespective of the setting of the two switches above. If however, the user wishes to obtain these files for a non-coupled run, then these two switches can be set to 1 and the files will then be produced at the end of the run. If savef31.lt.0, then a fort.31.###### file is produced after every B2.5 time step. Additionally, if savef31.ne.0, the fort.31 file will be updated before every Eirene call for coupled runs.
    
.. index::
   single: eirene_savef3*; eirene_savef30
   single: eirene_savef3*; eirene_savef31


.. index:: b2mndr_inverse_ua

``b2mndr_inverse_ua``    type: ``integer``    default: ``0``
    If inverse\_ua.eq.1, the code will produce a 'b2fstati\_with-ua' file that contains the same plasma information, but with the opposite sign convention for the parallel velocity. The run will then proceed with the new velocities with their sign inverted.
    

.. index:: b2yrdr_ns

``b2yrdr_ns``    type: ``integer``    default: ``ns``
    New number of species desired when reading a new atomic rates file using b2yr.exe. Must be specified within b2yr.dat.
    To be used for checking atomic rates after bundling and before any plasma state files have been created or converted, i.e. when the number of species in the atomic rates file b2frates does not match the number of species declared in the run parameters file b2fpardf.
    

.. index:: b2srsm_diagno

``b2srsm_diagno``    type: ``integer``    default: ``0``
    Controls level of output in b2srsm. If diagno.ge.2, output will be given on every call. If diagno.eq.1, output will be given on main calls only.
    

.. index:: b2ux5p_cpu

``b2ux5p_cpu``    type: ``integer``    default: ``0``
    If cpu.gt.0, prints out the time spent in the matrix solver.
    

.. index:: b2ux*

.. index:: b2ux5p_nltrsol, b2ux7p_nltrsol, b2ux9p_nltrsol, b2uxus_nltrsol
.. c

``b2ux*``

  - ``b2ux5p_nltrsol``  -     type: ``integer``    default: ``2``

  - ``b2ux7p_nltrsol``  -     type: ``integer``    default: ``2``

  - ``b2ux9p_nltrsol``  -     type: ``integer``    default: ``2``

  - ``b2uxus_nltrsol``  -     type: ``integer``    default: ``2``


    Output flag for the matrix solvers. Larger numbers mean increasing output level.
    
.. index::
   single: b2ux*; b2ux5p_nltrsol
   single: b2ux*; b2ux7p_nltrsol
   single: b2ux*; b2ux9p_nltrsol
   single: b2ux*; b2uxus_nltrsol


.. index:: eirene_mc_output_style

``eirene_mc_output_style``    type: ``integer``    default: ``1``
    If nonzero, prints sources computed by Eirene. If greater than 1, prints them on every use of the recycling sources, not just when they are computed.
    

.. index:: ma28_nwrite

``ma28_nwrite``    type: ``integer``    default: ``0``
    If nwrite.gt.0, prints the content of the sparse matrix in the b2\_matrix file, for the first nwrite calls.
    

.. index:: b2news_ncallout

``b2news_ncallout``    type: ``integer``    default: ``-1``
    If the iteration number is equal to ncallout, then several output files 'b2ne\_npmo', 'b2ne\_xppb', 'b2ne\_npco', 'b2ne+nppo' which detail the convergence behaviour and residuals.
    

.. index:: b2tqna_diagno

``b2tqna_diagno``    type: ``integer``    default: ``0``
    If diagno.gt.0, outputs details of the calculations of neutral transport coefficients when using the new\_df0 model. See switch b2tqna\_new\_df0 for more details.
    

.. index:: b2mndr_idout.

.. index:: b2mndr_idout0, b2mndr_idout1
.. c

``b2mndr_idout.``

  - ``b2mndr_idout0``  -     default: ``pgnl;pgmm;pzmm``

  - ``b2mndr_idout1``  -     default: ``pzmm``


    idout0 and idout1 specify the desired selection of output segments; idout0 for output before the calculation and idout1 for output at the conclusion of the calculation. The generic description of either of these 'idout' variables follows. idout specifies the desired selection of output segments for printed and graphical output. Associated with each segment is a four-character word, which is identified on the printed output. (The same word may be associated with several segments.) A particular segment will be produced only if its associated word has a match, as defined by the routine strmas, in idout.
    
.. index::
   single: b2mndr_idout.; b2mndr_idout0
   single: b2mndr_idout.; b2mndr_idout1


.. index:: eirene_format

``eirene_format``    type: ``string``    default: ``iter``
    This switch is to be provided within b2yt.dat to indicate to the b2yt converter the format of the original Eirene input.dat file to be modified. The accepted values are (case-insensitive):
    'old' for input files from SOLPS4.0 and SOLPS5.0 runs using 'old' Eirene\_96
    'new' for input files from SOLPS4.0 and SOLPS5.0 runs using 'new' Eirene\_99
    'facelift' for input files from SOLPS5.1 runs
    'juelich' for input files from Juelich Eirene versions (2008 and younger)
    'iter' for input files from SOLPS4.2/4.3 and SOLPS-ITER runs
    

.. index:: solps_version

``solps_version``    type: ``string``    default: ``iter``
    This switch is to be provided within b2yt.dat to indicate to the b2yt converter the format of the original fort.44 file to be modified. The accepted values are (case-insensitive):
    '4.3' for a fort.44 file produced from SOLPS4.3 runs
    '5.0' for a fort.44 file produced from SOLPS5.0 runs
    '5.1' for a fort.44 file produced from SOLPS5.1 runs
    '5.2' for a fort.44 file produced from SOLPS5.2 runs
    'iter' for input files from SOLPS-ITER runs (no conversion necessary)
    

.. index:: ids_from_43

``ids_from_43``    type: ``integer``    default: ``0``
    This switch is to be used when running the b2\_ual\_write utility program to obtain an IDS from the SOLPS run results.
    If set to 1, the IDS will indicate that the results come from a converted SOLPS4.3 run with no additional calculation. By default, the IDS will indicate a SOLPS-ITER run.
    

.. index:: AFN_out

``AFN_out``    type: ``integer``    default: ``0``
    If AFN\_out.ne.0, boundary flux components of the advanced fluid neutral models are written out. See code for details.
    

.. index:: 
   single: Output; b2mndr_b2time
   single: Output; b2mndr_tally
   single: Output; b2mndt_moitlv
   single: Output; b2mndt_moqtlv
   single: Output; b2mndr_mvnum
   single: Output; b2mndr_mvinc
   single: Output; b2mndr_plasnum
   single: Output; b2mndr_plasinc
   single: Output; b2mndr_cdfmovietim
   single: Output; cdfmovie_fields
   single: Output; b2mndr_ntim_save
   single: Output; b2mndt_av
   single: Output; b2mndt_av_continue
   single: Output; b2mndt_av_ntim_batch
   single: Output; b2mndt_av_ntim_run
   single: Output; b2mndt_av_batch_all
   single: Output; b2mndr_plasmatim
   single: Output; b2mndr_ids_save
   single: Output; b2mndr_ids_time
   single: Output; b2mndr_ids_av
   single: Output; b2wdat_iout
   single: Output; get_residuals
   single: Output; b2wdat_append
   single: Output; my_out_digits
   single: Output; b2mndr_old_style
   single: Output; b2mndr_av_read
   single: Output; b2mndr_*
   single: Output; b2mndr_trantim
   single: Output; b2mwti_target_offset
   single: Output; b2mwti_2dwrite
   single: Output; b2mwti_ismain0
   single: Output; b2mwqt_style
   single: Output; b2stbr_*_netcdf
   single: Output; ank_tracing
   single: Output; b2stbc_diagno
   single: Output; b2stbr_output
   single: Output; b2npmo_vlct_diagno
   single: Output; eirene_savef3*
   single: Output; b2mndr_inverse_ua
   single: Output; b2yrdr_ns
   single: Output; b2srsm_diagno
   single: Output; b2ux5p_cpu
   single: Output; b2ux*
   single: Output; eirene_mc_output_style
   single: Output; ma28_nwrite
   single: Output; b2news_ncallout
   single: Output; b2tqna_diagno
   single: Output; b2mndr_idout.
   single: Output; eirene_format
   single: Output; solps_version
   single: Output; ids_from_43
   single: Output; AFN_out

.. index:: Numerics

Numerics
========
.. index:: b2news_potit*

.. index:: b2news_potit, b2news_potitmin
.. c

``b2news_potit*``

  - ``b2news_potit``  -     type: ``integer``    default: ``50``

  - ``b2news_potitmin``  -     type: ``integer``    default: ``0``


    Obsolete. Removed from code.
    
.. index::
   single: b2news_potit*; b2news_potit
   single: b2news_potit*; b2news_potitmin


.. index:: b2news_potok

``b2news_potok``    type: ``real``    default: ``1.0e-2``
    Obsolete. Removed from code.
    

.. index:: b2news_ramp_slow

``b2news_ramp_slow``    type: ``integer``    default: ``0``
    If ramp\_slow.eq.0 (default), the ExB and diamagnetic drifts multipliers are ramped on each call of b2news, otherwise they are only changed on the first call of the nstg loop on the timestep.
    

.. index:: b2mndr_use_9pt_stencil

``b2mndr_use_9pt_stencil``    type: ``integer``    default: ``1``
    Master switch to turn on the 9-point stencil numerical treatment. If set to 0, reverts to the old 5-point stencil.
    Only usable with the SOLPS5.2 physics model.
    The perpendicular viscosity current terms are not yet available within this treatment.
    

.. index:: b2mndr_min_ares*

.. index:: b2mndr_min_areshe, b2mndr_min_areshi, b2mndr_min_aresco
.. c

``b2mndr_min_ares*``

  - ``b2mndr_min_areshe``  -     type: ``real``    default: ``0.0``

  - ``b2mndr_min_areshi``  -     type: ``real``    default: ``0.0``

  - ``b2mndr_min_aresco``  -     type: ``real``    default: ``0.0``


    Minimum residuals for stopping a run. All criteria must be met simultaneously for the run to stop. The continuity equation residual applies to the "ismain" species (See "Run" section).
    
.. index::
   single: b2mndr_min_ares*; b2mndr_min_areshe
   single: b2mndr_min_ares*; b2mndr_min_areshi
   single: b2mndr_min_ares*; b2mndr_min_aresco


.. index:: b2mndr_res_quit

``b2mndr_res_quit``    type: ``real``    default: ``1.0e-7``
    Threshold of the maximum residual among the equations solved below which the run is stopped. Only meaningful when compiled with FIXED\_POINT and with adjoint AD code.
    

.. index:: b2mndt_nstg_ares*

.. index:: b2mndt_nstg_areshe, b2mndt_nstg_areshi, b2mndt_nstg_aresco
.. c

``b2mndt_nstg_ares*``

  - ``b2mndt_nstg_areshe``  -     type: ``real``    default: ``0.0``

  - ``b2mndt_nstg_areshi``  -     type: ``real``    default: ``0.0``

  - ``b2mndt_nstg_aresco``  -     type: ``real``    default: ``0.0``


    Minimum residuals for an internal solution loop to stop.
    Used in conjunction with (not in replacement of) the nstg(0:2) numbers.
    All nonzero criteria must be met simultaneously. The continuity equation residual applies to the 'ismain' species (See 'Run' section).
    
.. index::
   single: b2mndt_nstg_ares*; b2mndt_nstg_areshe
   single: b2mndt_nstg_ares*; b2mndt_nstg_areshi
   single: b2mndt_nstg_ares*; b2mndt_nstg_aresco


.. index:: b2news_nsm*

.. index:: b2news_nsmin, b2news_nsmax
.. c

``b2news_nsm*``

  - ``b2news_nsmin``  -     type: ``integer``    default: ``0``

  - ``b2news_nsmax``  -     type: ``integer``    default: ``ns``


    Allows for solving only for the species range [nsmin:nsmax-1].
    
.. index::
   single: b2news_nsm*; b2news_nsmin
   single: b2news_nsm*; b2news_nsmax


.. index:: eirene_*

.. index:: eirene_na_max, eirene_na_min, eirene_ne_max, eirene_ne_min, eirene_te_max, eirene_te_min, eirene_ti_max, eirene_ti_min, eirene_ua_max, eirene_ua_min, eirene_M_max
.. c

``eirene_*``

  - ``eirene_na_max``  -     type: ``real``    default: ``1e30``

  - ``eirene_na_min``  -     type: ``real``    default: ``0.0``

  - ``eirene_ne_max``  -     type: ``real``    default: ``1e30``

  - ``eirene_ne_min``  -     type: ``real``    default: ``0.0``

  - ``eirene_te_max``  -     type: ``real``    default: ``1e30``

  - ``eirene_te_min``  -     type: ``real``    default: ``0.0``

  - ``eirene_ti_max``  -     type: ``real``    default: ``1e30``

  - ``eirene_ti_min``  -     type: ``real``    default: ``0.0``

  - ``eirene_ua_max``  -     type: ``real``    default: ``+c``

  - ``eirene_ua_min``  -     type: ``real``    default: ``-c``

  - ``eirene_M_max``  -     type: ``real``    default: ``1e30``
    If the Mach number based on the total fluid velocity of a background species exceeds eirene\_M\_max, all velocity components passed to Eirene are restricted to make the Mach number equal to eirene\_M\_max. It is an additional restriction on top of eirene\_ua\_min and eirene\_ua\_max.
    


    Upper and lower bounds used when writing out data for Eirene.
    
.. index::
   single: eirene_*; eirene_na_max
   single: eirene_*; eirene_na_min
   single: eirene_*; eirene_ne_max
   single: eirene_*; eirene_ne_min
   single: eirene_*; eirene_te_max
   single: eirene_*; eirene_te_min
   single: eirene_*; eirene_ti_max
   single: eirene_*; eirene_ti_min
   single: eirene_*; eirene_ua_max
   single: eirene_*; eirene_ua_min
   single: eirene_*; eirene_M_max


.. index:: eirene_print_minmax

``eirene_print_minmax``    type: ``integer``    default: ``0``
    Print min and max values of te, ti, na & ua
    

.. index:: eirene_extrap

``eirene_extrap``    type: ``integer``    default: ``1``
    If eirene\_extrap.eq.1, then guard cell plasma parameter values are calculated from the neighbouring real cell values. If eirene\_extrap.eq.0, the guard cell values are used unchanged.
    

.. index:: eirene_ank_mods

``eirene_ank_mods``    type: ``integer``    default: ``0``
    If ank\_mods.ne.0, then uses an additional scheme to ensure particle balance as the B2.5 solution evolves, due to the internal iteration scheme, away from the plasma background on which the Eirene sources were originally computed at the beginning of the time step. The user is referred to the text in $SOLPSTOP/doc/Source\_Scaling\_in\_B2.pdf for a full description of the method used.
    Cannot be used in conjunction with 'eirene\_ionising\_core'.
    

.. index:: eirene_dpc_fix

``eirene_dpc_fix``    type: ``integer``    default: ``1``
    If dpc\_fix.eq.1, then uses the true particle source from the stratum. If dpc\_fix.eq.2, sets this particle source to zero. The equivalent of the old behaviour is dpc\_fix.eq.0 and is wrong!
    

.. index:: b2stbr_eir_src_nhist

``b2stbr_eir_src_nhist``    type: ``integer``    default: ``1``
    If b2stbr\_eir\_src\_nhist.gt.1, then Eirene sources are accumulated and a moving average is computed. Note that only one of b2stbr\_eir\_src\_nhist, eirene\_neutr\_avg, or eirene\_underrelax may be nonzero.
    

.. index:: eirene_neutr_avg

``eirene_neutr_avg``    type: ``integer``    default: ``0``
    If eirene\_neutr\_avg.gt.0, then Eirene sources are accumulated and averaged until eirene\_neutr\_avg+1 steps, at which point the averaging process is reset. Note that only one of b2stbr\_eir\_src\_nhist, eirene\_neutr\_avg, or eirene\_underrelax may be nonzero.
    

.. index:: eirene_underrelax

``eirene_underrelax``    type: ``integer``    default: ``0``
    If eirene\_underrelax.gt.0, then an underrelaxation scheme is used for the Eirene sources, with an underrelaxation ratio of 1/eirene\_underrelax. Note that only one of b2stbr\_eir\_src\_nhist, eirene\_neutr\_avg, or eirene\_underrelax may be nonzero.
    

.. index:: eirene_uub_style

``eirene_uub_style``    type: ``integer``    default: ``0``
    If eirene\_uub\_style.eq.0, compute poloidal velocities passed to Eirene from ua, vadia, wadia, vaecrb arrays. If eirene\_uub\_style.eq.1, compute poloidal velocities passed to Eirene from fna and fna\_eir fluxes.
    

.. index:: b2news_area_fix

``b2news_area_fix``    type: ``integer``    default: ``3``
    Obsolete. Removed from code.
    New implementation supersedes treatment of area\_fix=3.
    

.. index:: b2npmo_ion_vlct_restrict

``b2npmo_ion_vlct_restrict``    type: ``integer``    default: ``0``
    If ion\_vlct\_restrict.ne.0, the parallel speed of ions and fluid neutrals is limited to be no more than M times the global plasma sound speed. In addition, if ion\_vlct\_restrict.eq.2, the ExB ion speeds are limited to be no more than M the local ion sound speed.
    M is given by b2npmo\_ion\_vlct\_restrict\_M.
    

.. index:: b2npmo_ion_vlct_restrict_M

``b2npmo_ion_vlct_restrict_M``    type: ``real``    default: ``3.0``
    Determines M for ion\_vlct\_restrict.ne.0.
    

.. index:: b2mndr_ua_max

``b2mndr_ua_max``    type: ``real``    default: ``1.0e6``
    Puts a hard limit on the absolute value of the parallel velocity, but applies only to fluid neutrals and in case the spatially hybrid fluid-kinetic model is active (spatial\_hybrid.ne.0).
    This switch was introduced when b2npmo\_ion\_vlct\_restrict only applied to ions. Now that b2npmo\_ion\_vlct\_restrict also applies to fluid neutrals, the removal of b2mndr\_ua\_max can be considered.
    For now it is kept for backward compatibility with published results.
    

.. index:: b2nppo_restr_po

``b2nppo_restr_po``    type: ``real``    default: ``0.0``
    If b2nppo\_restr\_po.ne.0.0, the electric potential is restricted such that its ratio (in absolute value) with the electron temperature (in eV) does not exceed b2nppo\_restr\_po.
    If b2nppo\_restr\_po is negative, the limit only applies to regions of negative electric potential.
    Only applies on open field lines.
    

.. index:: b2upht_rte_min

``b2upht_rte_min``    type: ``real``    default: ``0.0``
    If b2upht\_rte\_min.gt.0.0, the electron to ion temperature ratio is forced to not be lower than rte\_min (i.e. Te/Ti >= rte\_min).
    

.. index:: b2sihs_shivis

``b2sihs_shivis``    type: ``integer``    default: ``0``
    If b2sihs\_shivis.eq.1, then shivc and shiva (ion heat source due to viscosity) will be zeroed out in boundary-volume cells.
    If b2sihs\_shivis.eq.2, then shivc and shiva (ion heat source due to viscosity) will be zeroed out in boundary-volume cells except the ones that belong to the core and target boundaries.
    If b2sihs\_shivis.eq.3, then shivc and shiva (ion heat source due to viscosity) will be zeroed out in boundary-volume cells belonging to the main chamber wall bondary.
    

.. index:: b2sihs_shi

``b2sihs_shi``    type: ``integer``    default: ``0``
    If b2sihs\_shi.ne.0, then all b2sihs\_shi\* and b2sihs\_shivis keys will be assigned to b2sihs\_shi value as default (individual keys can still be overwritten by b2sihs\_shi\* and b2sihs\_shivis that take proprity over b2sihs\_shi).
    

.. index:: b2sihs_shidu

``b2sihs_shidu``    type: ``integer``    default: ``0``
    If b2sihs\_shidu.eq.1, then shidu (ion heat source due to divergence of velocity) will be zeroed out in boundary-volume cells.
    If b2sihs\_shidu.eq.2, then shidu (ion heat source due to divergence of velocity) will be zeroed out in boundary-volume cells except the ones that belong to the core and target boundaries.
    If b2sihs\_shidu.eq.3, then shidu (ion heat source due to divergence of velocity) will be zeroed out in boundary-volume cells belonging to the main chamber wall bondary.
    

.. index:: b2sihs_shidd

``b2sihs_shidd``    type: ``integer``    default: ``0``
    If b2sihs\_shidd.eq.1, then shidd (ion heat source due to divergence of drift velocity) will be zeroed out in boundary-volume cells.
    If b2sihs\_shidd.eq.2, then shidd (ion heat source due to divergence of drift velocity) will be zeroed out in boundary-volume cells except the  ones that belong to the core and target boundaries.
    If b2sihs\_shidd.eq.3, then shidd (ion heat source due to divergence of drift velocity) will be zeroed out in boundary-volume cells belonging to the main chamber wall bondary.
    

.. index:: b2sihs_shedu

``b2sihs_shedu``    type: ``integer``    default: ``0``
    If b2sihs\_shedu.eq.0, then shedu (electron heat source due to divergence of velocity) will be zeroed out in boundary-volume cells.
    If b2sihs\_shedu.eq.2, then shedu (electron heat source due to divergence of velocity) will be zeroed out in boundary-volume cells except the ones that belong to the core and target boundaries.
    If b2sihs\_shedu.eq.3, then shedu (electron heat source due to divergence of velocity) will be zeroed out in boundary-volume cells belonging to the main chamber wall bondary.
    

.. index:: b2sihs_shedd

``b2sihs_shedd``    type: ``integer``    default: ``0``
    If b2sihs\_shedd.eq.0, then shedd (electron heat source due to divergence of drift velocity) will be zeroed out in boundary-volume cells.
    If b2sihs\_shedd.eq.2, then shedd (electron heat source due to divergence of drift velocity) will be zeroed out in boundary-volume cells except the ones that belong to the core and target boundaries.
    If b2sihs\_shedd.eq.3, then shedd (electron heat source due to divergence of drift velocity) will be zeroed out in boundary-volume cells belonging to the main chamber wall bondary.
    

.. index:: b2tfhe_vis_per

``b2tfhe_vis_per``    type: ``real``    default: ``0.0``
    vis\_per is a multiplier to the perpendicular viscosity current.
    If vis\_per.ne.0.0, the electric potential equation is solved by the subroutine b2npp7 using a 7-point stencil.
    The value '1.0' is recommended for runs with drifts when perpendicular viscosity and corresponding perpendicular viscosity current is taken into account.
    Cannot be used in conjunction with the 9-point stencil numerical treatment. If used with the 5-point stencil treatment and with fluid neutrals, must be equal to b2tfnb\_vis\_per for numerical stability reasons.
    

.. index:: b2stbc_sheath_drift_fix

``b2stbc_sheath_drift_fix``    type: ``integer``    default: ``1``
    If sheath\_drift\_fix.eq.0, then the drift velocity used in the sheath boundary conditions is the sum of diamagnetic and ExB contributions (old, but likely wrong, treatment). If sheath\_drift\_fix.eq.1, then the drift velocity used in the sheath boundary conditions is the ExB velocity only (recommended).
    

.. index:: b2stbc_BC2_cor9

``b2stbc_BC2_cor9``    type: ``real``    default: ``0.0``
    This switch concerns a 9-point correction for the Neumann type boundary conditions (BCCON/BCMOM/BCENE/BCENI/BCPOT/BCENK/BCENZ = 2) for non-orthogonal cells.
    If b2stbc\_BC2\_cor9.eq.0.0, gradients tangential to the boundary are ignored. The actual normal gradient then deviates from the one requested by the user.
    If b2stbc\_BC2\_cor9.eq.1.0, an additional term based on the vertex values of the boundary face is added to correct for the tangential gradient, to get the correct (up to interpolation error) normal gradient.
    

.. index:: b2stbc_fix_fch_in_fhe_sheath

``b2stbc_fix_fch_in_fhe_sheath``    type: ``integer``    default: ``2``
    If fix\_fch\_in\_fhe\_sheath.eq.0, then the wrong (old) implementation of the FCH contribution to FHE used;
    If fix\_fch\_in\_fhe\_sheath.eq.1, then the wrong (second) implementation of the FCH contribution to FHE used;
    If fix\_fch\_in\_fhe\_sheath.eq.2, then the correct implementation of the FCH contribution to FHE used;
    

.. index:: b2stbr_potential_at_guard_cell

``b2stbr_potential_at_guard_cell``    type: ``integer``    default: ``1``
    If potential\_at\_guard\_cell.eq.1, the electric potential used for the computation of the incident energy for sputtering yields is taken as the value in the guard cell. If potential\_at\_guard\_cell.eq.0, the value from the neighbouring real cell is used instead.
    

.. index:: b2stbr_temperature_at_guard_cell

``b2stbr_temperature_at_guard_cell``    type: ``integer``    default: ``1``
    If temperature\_at\_guard\_cell.eq.1, the temperatures used for recycling and reflection are taken as the value in the guard cell.
    If temperature\_at\_guard\_cell.eq.0, the temperatures are interpolated between the guard cell and the neighbouring real cell.
    

.. index:: b2trcl_conductive_limit

``b2trcl_conductive_limit``    type: ``integer``    default: ``1``
    When set to '1', flux limit of the parallel electron and ion heat fluxes is applied to transport coefficients.
    It is recommended '1'. If 'b2trcl\_conductive\_limit' '0' then the keys 'b2tfhe\_lim\_flux' and 'b2tfhi\_lim\_flux' must be '0'.
    

.. index:: b2trcl_core_cond_limit

``b2trcl_core_cond_limit``    type: ``integer``    default: ``0``
    If core\_cond\_limit.eq.0, then the heat flux limits due to chvemx and chvimx are not applied in the core. Switch only active if 'b2trcl\_conductive\_limit' .ne. 0.
    

.. index:: b2tlh0_flux_limit_style

``b2tlh0_flux_limit_style``    type: ``integer``    default: ``2``
    If '0', use the SOLPS5.0 scheme for neutral heat conductivity flux limits.
    If '1', SPb form to calculate parallel and perpendicular neutral heat conductivity flux limit (does not preserve symmetry, kept for backward compatibility reasons).
    If '2', modifies the SPb treatment for the flux limits to be applied on the transport coefficients directly.
    It is recommended '2'.
    

.. index:: b2tral_mode

``b2tral_mode``    type: ``integer``    default: ``1``
    Switch to choose between various interpolation schemes for transport coefficients (Does not apply to pinch velocities vla or to the temperature-driven electric conductivity alf).
    mode.eq.-1: harmonic averaging
    mode.eq.0 : geometric averaging
    mode.eq.1 : arithmetic averaging (SOLPS5.0 formulation)
    mode.eq.2 : arithmetic averaging (SOLPS4.0 formulation)
    

.. index:: b2tfh._*hybr*

.. index:: b2tfhe_no_hybr, b2tfhi_no_hybr, b2tfnb_no_hybr, b2tfhe_hybr2, b2tfhi_hybr2
.. c

``b2tfh._*hybr*``

  - ``b2tfhe_no_hybr``  -     type: ``integer``    default: ``0``

  - ``b2tfhi_no_hybr``  -     type: ``integer``    default: ``0``

  - ``b2tfnb_no_hybr``  -     type: ``integer``    default: ``0``

  - ``b2tfhe_hybr2``  -     type: ``integer``    default: ``0``

  - ``b2tfhi_hybr2``  -     type: ``integer``    default: ``0``


    Switches to toggle between the standard 5.0 hybrid scheme (no\_hybr.eq.0) and the old 4.0 upwind scheme (no\_hybr.eq.1).
    These apply separately to the electron heat, ion heat and particle conservation equations.
    If hybr2.ne.0, then a mixed scheme is used where only the conductivity is computed according to the 4.0 scheme.
    Obsolete. Not available for WG. Replaced by the 'discr\_meth' switches.
    
.. index::
   single: b2tfh._*hybr*; b2tfhe_no_hybr
   single: b2tfh._*hybr*; b2tfhi_no_hybr
   single: b2tfh._*hybr*; b2tfnb_no_hybr
   single: b2tfh._*hybr*; b2tfhe_hybr2
   single: b2tfh._*hybr*; b2tfhi_hybr2


.. index:: ._upwind

.. index:: b2tfhe_upwind, b2tfhi_upwind
.. c

``._upwind``

  - ``b2tfhe_upwind``  -     type: ``integer``    default: ``0``

  - ``b2tfhi_upwind``  -     type: ``integer``    default: ``0``


    If upwind.ne.0, then the SOLPS4 upwind scheme in b2tfhe\_ and b2tfhi\_ to obtain the heat fluxes.
    Obsolete. Not available for WG. Replaced by the 'discr\_meth' switches.
    
.. index::
   single: ._upwind; b2tfhe_upwind
   single: ._upwind; b2tfhi_upwind


.. index:: b2tfnb_pflux_cor

``b2tfnb_pflux_cor``    type: ``integer``    default: ``1``
    If pflux\_cor.eq.1 and fna\_mdf is used, enforces that the integral particle flux across the domain boundaries computed from fna is equal to the same integral computed from the fna\_mdf fluxes.
    Not yet available for WG.
    

.. index:: b2trcl_cvsa_mltpl

``b2trcl_cvsa_mltpl``    type: ``real``    default: ``1.0``
    Artificial coefficient providing faster convergence to the neoclassical electric field but giving a distortion of the flows in the SOL as a side-effect.
    Can be applied <>1 during the convergence and turned off for the final stage of calculations. Use with caution.
    

.. index:: b2uxus_mult_nonzero

``b2uxus_mult_nonzero``    type: ``integer``    default: ``1``
    Number of expected nonzero matrix elements per matrix row.
    

.. index:: b2uxus_mult_solvdim*

.. index:: b2uxus_mult_solvdim, b2uxus_mult_solvdim1
.. c

``b2uxus_mult_solvdim*``

  - ``b2uxus_mult_solvdim``  -     type: ``integer``    default: ``15``

  - ``b2uxus_mult_solvdim1``  -     type: ``integer``    default: ``10``


    Multipliers to the number of nonzero elements in the solution matrix for workspace arrays in the matrix solver.
    
.. index::
   single: b2uxus_mult_solvdim*; b2uxus_mult_solvdim
   single: b2uxus_mult_solvdim*; b2uxus_mult_solvdim1


.. index:: b2ux5p_style

``b2ux5p_style``    type: ``integer``    default: ``2``
    Choose the type of 5-point stencil matrix solver. Style.eq.0 = iluter, Style.eq.1 = slv5pt, Style.eq.2 = MA28.
    NOTE: Only style.eq.2 will give good results. Other values are NOT recommended! style.eq.0 and style.eq.1 are only applicable to linear geometries with no cuts and no isolated regions.
    

.. index:: b2ux7p_style

``b2ux7p_style``    type: ``integer``    default: ``2``
    Choose the type of 7-point stencil matrix solver. Style.eq.0 = iluter, Style.eq.1 = slv5pt, Style.eq.2 = MA28copy3. Style.eq.3 = SDRV from YSMP.
    NOTE: Only style.eq.2 will give good results. Applying style.eq.3 should be corrected and is no longer recommended. It might give slow convergence or even divergence of the potential equation. Other values are NOT recommended! style.eq.0 .or. style.eq.1 will return an error.
    

.. index:: b2ux9p_style

``b2ux9p_style``    type: ``integer``    default: ``2``
    Choose the type of 9-point stencil matrix solver. Style.eq.0 = iluter, Style.eq.1 = slv5pt, Style.eq.2 = MA28copy.
    NOTE: Only style.eq.2 will give good results. Other values are NOT recommended! style.eq.0 and style.eq.1 will return an error.
    

.. index:: b2ux5p_acpar

``b2ux5p_acpar``    type: ``real``    default: ``8.0``
    Paremeter needed for iluter matrix solver.
    

.. index:: b2stbc_fchy_dia

``b2stbc_fchy_dia``    type: ``real``    default: ``0.0``
    Multiplier to the neoclassical current and diamagnetic heat flux convective boundary conditions, also multiplied by facdrift.
    Adds a poloidal variation consistent with neoclassics and diamagnetic contributions to the heat flux boundary conditions.
    Should only be used with the 5.0 model and heat flux boundaries.
    Allows use b2stbc\_integral\_current if fchy\_dia.eq.0, forbids it otherwise.
    Not yet available for WG.
    

.. index:: b2stbc_fchy_dia_coreonly

``b2stbc_fchy_dia_coreonly``    type: ``integer``    default: ``1``
    If fchy\_dia\_coreonly.eq.1, the neoclassical current and diamagnetic heat flux convective boundary conditions are only applied on the core boundary.
    If fchy\_dia\_coreonly.eq.0, those are applied to all boundaries, including PFR, North SOL edge and diverted island center boundary.
    Not yet available for WG.
    

.. index:: b2stbc_neoclassical

``b2stbc_neoclassical``    type: ``real``    default: ``0.0``
    Real parameter which establishes boundary conditions for radial component of the current for North and South boundaries when these lie on closed flux surfaces.
    If b2stbc\_neoclassical is 0 then the radial component of the current is zero.
    If b2stbc\_neoclassical is not 0 the radial component of the current is given by the neoclassical value. b2stbc\_neoclassical is superseded if facdrift.ne.0.
    This cannot be used in conjunction with b2stbc\_integral\_current below.
    

.. index:: b2stbc_cbc

``b2stbc_cbc``    type: ``real``    default: ``1.0``
    Multiplier to the ExB velocity for sheath boundary conditions BCMOM=13.
    Not yet available for WG.
    

.. index:: b2stbc_integral_current

``b2stbc_integral_current``    type: ``real``    default: ``0.0``
    If integral\_current.gt.0, corrects current sources so that there be no surface current at the North and South edges of the edge plasma.
    The value of integral\_current multiplies the correction term added to the current source.
    This setting is incompatible with the normal use of diamagnetic drift terms (facdrift.gt.0.0 .and. b2stbc\_fchy\_dia.ne.0.0) or neoclassical boundary conditions (b2stbc\_neoclassical.gt.0.0).
    Not yet available for WG.
    

.. index:: b2stbr_first_flight_dl

``b2stbr_first_flight_dl``    type: ``real``    default: ``0.001``
    Step length (in metres) for computing the first flight model chords.
    

.. index:: b2stbr_first_flight_no_of_flights

``b2stbr_first_flight_no_of_flights``    type: ``integer``    default: ``9``
    Number of chords started from each start point in the first flight model.
    

.. index:: b2stbr_first_flight_table_size

``b2stbr_first_flight_table_size``    type: ``integer``    default: ``200000``
    Workspace size given to the first flight table.
    

.. index:: b2stbc_s*

.. index:: b2stbc_she0ep, b2stbc_shi0ep, b2stbc_sna0ep
.. c

``b2stbc_s*``

  - ``b2stbc_she0ep``  -     type: ``real``    default: ``1.0e-36``

  - ``b2stbc_shi0ep``  -     type: ``real``    default: ``1.0e-36``

  - ``b2stbc_sna0ep``  -     type: ``real``    default: ``1.0e-36``


    Small level sources introduced in all cells.
    
.. index::
   single: b2stbc_s*; b2stbc_she0ep
   single: b2stbc_s*; b2stbc_shi0ep
   single: b2stbc_s*; b2stbc_sna0ep


.. index:: b2stbc_bcpot_16_step

``b2stbc_bcpot_16_step``    type: ``integer``    default: ``50``
    Frequency (in number of calls to b2stbc\_phys) at which the constant value of the potential at the boundaries where BCPOT=16 is applied will be recomputed.
    Not yet available for WG.
    

.. index:: b2stbc_stab_coeff_sheath_te

``b2stbc_stab_coeff_sheath_te``    type: ``real``    default: ``0.0``
    Stabilizing term to the source associated with boundary condition BCENE=15, when bcene\_15\_style.eq.1 (default).
    To help suppress electron temperature oscillations, this parameter can be set to a positive value. The range 1-100 is recommended.
    

.. index:: b2stbc_stab_coeff_sheath_ti

``b2stbc_stab_coeff_sheath_ti``    type: ``real``    default: ``0.0``
    Stabilizing term to the source associated with boundary condition BCENI=15.
    To help suppress ion temperature oscillations, this parameter can be set to a positive value. The range 1-100 is recommended.
    

.. index:: b2npht_stab_shei

``b2npht_stab_shei``    type: ``real``    default: ``0.0``
    Stabilizing term to the heat sources associated with ion-electron energy exchange.
    

.. index:: b2txcx_increase_transp_coefs

``b2txcx_increase_transp_coefs``    type: ``real``    default: ``0.0``
    Multiplication factor to the poloidal transport coefficients (electron and ion thermal conductivity, particle transport proportional to grad na and grad pa). Must be greater than 1.0 to have an effect.
    If b2txcx\_increase\_transp\_coefs.gt.1.0, b2trno\_set\_chcb\_0 will be assigned to 1.
    

.. index:: b2trno_set_chcb_0

``b2trno_set_chcb_0``    type: ``integer``    default: ``0``
    If set\_chcb\_0.eq.1, sets radial components of transport coefficients (electron and ion thermal conductivity, particle transport proportional to grad na and grad pa) equals to zero on not field-aligned boundary faces (as defined by b2us\_prep\_Qalfmin). Also decreases the same radial components by a b2txcx\_increase\_transp\_coefs factor on not field-aligned faces between two neighbouring boundary cells. Always on if b2txcx\_increase\_transp\_coefs.gt.1.0.
    

.. index:: b2mndr_na_min

``b2mndr_na_min``    type: ``real``    default: ``1.0e4``
    Minimal density maintained in all cells for all species (in m^{-3}).
    It must be true that na\_min is smaller than na\_new, as well as any of the initial densities provided in b2ai.dat.
    This switch replaces 'b2mndr\_na0eps' from SOLPS5.x.
    It is also used to avoid division by 0 when calculating kinetic neutral velocities from the kinetic flux densities in b2tinnt.F.
    

.. index:: b2mndr_na_new

``b2mndr_na_new``    type: ``real``    default: ``1.0e14``
    Initial density (in m^{-3}) put in all cells for all new species if not overwritten by initial state file. This switch replaces 'b2mndr\_na0eps' from SOLPS5.x.
    

.. index:: b2upht_te_min

``b2upht_te_min``    type: ``real``    default: ``0.1``
    Sets the minimum electron temperature value (in eV).
    

.. index:: b2upht_te_max

``b2upht_te_max``    type: ``real``    default: ``1.0e+30``
    Sets the maximum electron temperature value (in eV).
    

.. index:: b2upht_ti_min

``b2upht_ti_min``    type: ``real``    default: ``0.1``
    Sets the minimum ion temperature value (in eV).
    

.. index:: b2upht_ti_max

``b2upht_ti_max``    type: ``real``    default: ``1.0e+30``
    Sets the maximum ion temperature value (in eV).
    

.. index:: b2upht_tn_min

``b2upht_tn_min``    type: ``real``    default: ``0.1``
    Sets the minimum fluid neutral temperature value (in eV).
    

.. index:: b2upht_tn_max

``b2upht_tn_max``    type: ``real``    default: ``1.0e+30``
    Sets the maximum fluid neutral temperature value (in eV).
    

.. index:: b2upht_kt_min

``b2upht_kt_min``    type: ``real``    default: ``1.0e-5``
    Sets the minimum turbulent ExB kinetic energy value (in eV).
    

.. index:: b2upht_kt_max

``b2upht_kt_max``    type: ``real``    default: ``1.0e+30``
    Sets the maximum turbulent ExB kinetic energy value (in eV).
    

.. index:: b2upht_zt_min

``b2upht_zt_min``    type: ``real``    default: ``1.0e-8``
    Sets the minimum turbulent ExB enstrophy value (in s^{-2}).
    

.. index:: b2upht_zt_max

``b2upht_zt_max``    type: ``real``    default: ``1.0e+30``
    Sets the maximum turbulent ExB enstrophy value (in s^{-2}).
    

.. index:: b2news_guard_flows

``b2news_guard_flows``    type: ``integer``    default: ``2``
    Prohibited switch. As of v3.2.0, there are no faces between guard cells anymore.
    

.. index:: b2news_fac*

.. index:: b2news_facdrift_tanh_a, b2news_facdrift_tanh_b, b2news_fac_ExB_tanh_a, b2news_fac_ExB_tanh_b, b2news_fac_vis_tanh_a, b2news_fac_vis_tanh_b, b2news_iy_nocoreExB
.. c

``b2news_fac*``

  - ``b2news_facdrift_tanh_a``  -     type: ``real``    default: ``0.0``

  - ``b2news_facdrift_tanh_b``  -     type: ``real``    default: ``0.0``

  - ``b2news_fac_ExB_tanh_a``  -     type: ``real``    default: ``0.0``

  - ``b2news_fac_ExB_tanh_b``  -     type: ``real``    default: ``0.0``

  - ``b2news_fac_vis_tanh_a``  -     type: ``real``    default: ``0.0``

  - ``b2news_fac_vis_tanh_b``  -     type: ``real``    default: ``0.0``

  - ``b2news_iy_nocoreExB``  -     type: ``integer``    default: ``0``


    Parameters for spatial variation of the diamagnetic, ExB and viscosity drift term multipliers. These are allowed to have tanh profiles centered at tanh\_a and of width tanh\_b, where both quantities are in metres and measured along the outer midplane. The maximum value of facdrift and fac\_ExB is controlled by their respective \_start and \_target switches, see Run section for details. NOTE: none of them have been converted to WG!
    For consistency with the naming convention of related variables:
    b2news\_facExB\_tanh\_a is an alias for b2news\_fac\_ExB\_tanh\_a,
    b2news\_facExB\_tanh\_b is an alias for b2news\_fac\_ExB\_tanh\_b,
    b2news\_facvis\_tanh\_a is an alias for b2news\_fac\_vis\_tanh\_a, and b2news\_facvis\_tanh\_b is an alias for b2news\_fac\_vis\_tanh\_b. Additionally, for all deep core cell rings up to and including the iy\_nocoreExB-th, fac\_ExB(ix,iy) is set to zero. This means that ExB contributions and flows will be zeroed out in those cells.
    For consistency with the boundary condition treatment, the value iy\_nocoreExB.eq.1 is NOT recommended!
    
.. index::
   single: b2news_fac*; b2news_facdrift_tanh_a
   single: b2news_fac*; b2news_facdrift_tanh_b
   single: b2news_fac*; b2news_fac_ExB_tanh_a
   single: b2news_fac*; b2news_fac_ExB_tanh_b
   single: b2news_fac*; b2news_fac_vis_tanh_a
   single: b2news_fac*; b2news_fac_vis_tanh_b
   single: b2news_fac*; b2news_iy_nocoreExB


.. index:: b2stbc_istyle_cur_contr_on_S_and_N

``b2stbc_istyle_cur_contr_on_S_and_N``    type: ``integer``    default: ``2``
    When set to '2', SPb form of adding currents on the South core boundary is included by using BCPOT=12, and on the South PFR and North boundaries by using BCPOT=13. It is recommended '2', in conjunction with the BCPOT=12 and BCPOT=13 settings, respectively.
    When set to '1', SPb form of adding currents on South and North boundaries is done explicitly in addition to other existing boundary conditions for the potential equation.
    The old 5.0 calculation is recovered by using the value '0'.
    

.. index:: b2stbc_istyle_fchi

``b2stbc_istyle_fchi``    type: ``integer``    default: ``0``
    If '1', explicitly use the expression (bx\*cs\*na) of particle flux (fna) from boundary condition instead of fna, for boundary condition type BCPOT=11.
    Not yet available for WG.
    

.. index:: b2news_no_b2sral_call

``b2news_no_b2sral_call``    type: ``integer``    default: ``1``
    If no\_b2sral\_call.eq.0, add an additional call to recompute the sources in b2news\_ to reproduce the behaviour from SOLPS4.
    

.. index:: b2news_do_2nd_b2npco_call

``b2news_do_2nd_b2npco_call``    type: ``integer``    default: ``0``
    If do\_2nd\_b2npco\_call.eq.1, perform a second call to the density equation solve to improve particle balance, as done in SOLPS4.
    

.. index:: b2news_re_eval_prtls_fluxes

``b2news_re_eval_prtls_fluxes``    type: ``integer``    default: ``0``
    If re\_eval\_prtls\_fluxes.eq.1, the particle fluxes are recomputed at the end of b2news\_. This is necessary for rescaling of the Eirene sources during coupled runs, so this switch is superceded by use\_eirene, and also needed to reproduce SOLPS4 runs.
    

.. index:: b2mndt_style

``b2mndt_style``    type: ``integer``    default: ``1``
    If 0, refers to the obsolete SOLPS5.0 physics model, no longer supported.
    If 1, the SOLPS5.2 physics model is used, and b2news\_ is called to compute the new plasma state. (default)
    If 2, the SOLPS5.2 physics model is used, and b2news\_m is called instead to run the code in fully self-consistent time-dependent mode. B2news\_m uses a different order of solving equations: first the density equations, then the parallel velocity, electrical potential and Te and Ti equations (and optionally also the Tn and k-epsilon equations, if requested).
    

.. index:: b2mndt_ckn

``b2mndt_ckn``    type: ``integer``    default: ``1``
    If b2mndt\_ckn=2, the 2nd order Crank-Nicolson time-stepping scheme is used, instead of the default 1st order implicit Euler scheme.
    This scheme can be used both in time-dependent mode (b2mndt\_style=2) and in steady-state mode (b2mndt\_style=1).
    

.. index:: b2mndt_dummy

``b2mndt_dummy``    type: ``integer``    default: ``0``
    This switch is used internally in the code to initially run a dummy call to b2mndt, which is needed to use the Crank-Nicolson time-stepping scheme (b2mndt\_ckn=2). This switch is not meant to be changed by users, it should always stay at its default value of 0.
    

.. index:: b2mndt_ntim_step_out

``b2mndt_ntim_step_out``    type: ``integer``    default: ``1``
    When set to a value of 'K', residuals at each K-th step will be written in b2ftrace. It helps to avoid a huge b2ftrace files during long time run.
    

.. index:: b2mndt_calc_err_step_out

``b2mndt_calc_err_step_out``    type: ``integer``    default: ``1``
    When set to a value of 'K', the subroutine calc\_err will be run at each K-th step. It allows to output the error at desired times during a time-dependent MMS test.
    

.. index:: b2stb*

.. index:: b2stbc_cbsnafac, b2stbc_fchycore_alpha, b2stbc_fheycore_alpha, b2stbc_fhiycore_alpha, b2stbc_fnaycore_alpha, b2stbc_nesepm_alpha, b2stbc_nesepm_beta, b2stbc_nesepm_gamma, b2stbc_volrec_alpha, b2stbc_volrec_beta, b2stbr_sput_chem_alpha, b2stbr_sput_phys_alpha
.. c

``b2stb*``

  - ``b2stbc_cbsnafac``  -     type: ``real``    default: ``0.01``

  - ``b2stbc_fchycore_alpha``  -     type: ``real``    default: ``0.1``

  - ``b2stbc_fheycore_alpha``  -     type: ``real``    default: ``0.1``

  - ``b2stbc_fhiycore_alpha``  -     type: ``real``    default: ``0.1``

  - ``b2stbc_fnaycore_alpha``  -     type: ``real``    default: ``0.1``

  - ``b2stbc_nesepm_alpha``  -     type: ``real``    default: ``1.0e-3``

  - ``b2stbc_nesepm_beta``  -     type: ``real``    default: ``0.0``

  - ``b2stbc_nesepm_gamma``  -     type: ``real``    default: ``0.99``

  - ``b2stbc_volrec_alpha``  -     type: ``real``    default: ``1.0e-3``

  - ``b2stbc_volrec_beta``  -     type: ``real``    default: ``1.0``

  - ``b2stbr_sput_chem_alpha``  -     type: ``real``    default: ``1.0e-2``

  - ``b2stbr_sput_phys_alpha``  -     type: ``real``    default: ``1.0e-2``


    Feedback relaxation parameters. See Physics section for individual feedback quantities.
    
.. index::
   single: b2stb*; b2stbc_cbsnafac
   single: b2stb*; b2stbc_fchycore_alpha
   single: b2stb*; b2stbc_fheycore_alpha
   single: b2stb*; b2stbc_fhiycore_alpha
   single: b2stb*; b2stbc_fnaycore_alpha
   single: b2stb*; b2stbc_nesepm_alpha
   single: b2stb*; b2stbc_nesepm_beta
   single: b2stb*; b2stbc_nesepm_gamma
   single: b2stb*; b2stbc_volrec_alpha
   single: b2stb*; b2stbc_volrec_beta
   single: b2stb*; b2stbr_sput_chem_alpha
   single: b2stb*; b2stbr_sput_phys_alpha


.. index:: b2stbc_type13_*

.. index:: b2stbc_type13_fac, b2stbc_type13_norm
.. c

``b2stbc_type13_*``

  - ``b2stbc_type13_fac``  -     type: ``real``    default: ``1.0``

  - ``b2stbc_type13_norm``  -     type: ``real``    default: ``1.0e15``


    Additional feedback strength adjustment parameters for BCCON=13 boundary condition, density adjusted to match a specific flux.
    The density is adjusted by a factor of:
    (1.0\_R8+CONPAR(IS,IB,2)\*(DFS-FS)/ (abs(DFS)+abs(FS)+abs(type13\_norm)+abs(NAS\*type13\_fac)))
    where FS is the current particle flux, DFS is the desired particle flux, and NAS the current volume-averaged density. The desired flux DFS is computed as
    CONPAR(IS,IB,1)+CONPAR(IS,IB,3)
    where the first number is provided directly by the user in b2.boundary.parameters and the second is internally set to correspond to the re-entry of ionised neutrals that have crossed into the core for cases run with Eirene where eirene\_ionising\_core is activated.
    See also the description of 'eirene\_ionising\_core'.
    Not yet available for WG.
    
.. index::
   single: b2stbc_type13_*; b2stbc_type13_fac
   single: b2stbc_type13_*; b2stbc_type13_norm


.. index:: heatdiff1D_*

.. index:: heatdiff1D_linlog, heatdiff1D_ratio
.. c

``heatdiff1D_*``

  - ``heatdiff1D_linlog``  -     type: ``integer``    default: ``1``

  - ``heatdiff1D_ratio``  -     type: ``real``    default: ``100.0``


    Parameters related to solving the temperature equation for the target plate elements in depth. If linlog.eq.1, a linear subdividing of the plate element is used. If linlog.eq.2, a logarithmic subdividing is used, with the surface layer being ratio times thinner than the last layer in the bulk.
    ratio must be larger than 1.
    
.. index::
   single: heatdiff1D_*; heatdiff1D_linlog
   single: heatdiff1D_*; heatdiff1D_ratio


.. index:: b2trno_flux_limit_to_dpa

``b2trno_flux_limit_to_dpa``    type: ``integer``    default: ``1``
    If '1', flux limit to neutrals contribution to dpa0 - the diffusion coefficient is applied in b2tlc0.F. It is recommended '1'.
    b2tlc0.F has the flux limit parameters α and γ which are given by 'b2tlc0\_alpha' and 'b2tlc0\_gamma'. 'b2tfnb\_alpha' and 'b2tlc0\_alpha' cannot be different from zero simultaneously.
    'b2tfnb\_alpha' gives another form of flux limit which is applied to the whole particle flux.
    

.. index:: b2trno_flux_limit_to_vsa

``b2trno_flux_limit_to_vsa``    type: ``integer``    default: ``1``
    If '1', flux limit to neutrals contribution to vsa0 - the viscosity is applied in b2tlv0.F. It is recommended '1'.
    b2tlv0.F has the flux limit parameters α and γ which are given by 'b2tlv0\_alpha' and 'b2tlv0\_gamma'.
    

.. index:: b2mndr_*fb*

.. index:: b2mndr_isfb, b2mndr_ixfb, b2mndr_iyfb, b2mndr_ne_wanted, b2mndr_ne_wanted_time
.. c

``b2mndr_*fb*``

  - ``b2mndr_isfb``  -     type: ``real``    default: ``ismain``

  - ``b2mndr_ixfb``  -     type: ``real``    default: ``5*nx/8``

  - ``b2mndr_iyfb``  -     type: ``real``    default: ``ny/2``

  - ``b2mndr_ne_wanted``  -     type: ``real``    default: ``0.0``

  - ``b2mndr_ne_wanted_time``  -     type: ``real``    default: ``0.0``


    Experimental: allows for density feedback of the number of electrons accompanying species 'isfb' at location (ixfb,iyfb).
    Note that ixfb and iyfb are real numbers!
    
.. index::
   single: b2mndr_*fb*; b2mndr_isfb
   single: b2mndr_*fb*; b2mndr_ixfb
   single: b2mndr_*fb*; b2mndr_iyfb
   single: b2mndr_*fb*; b2mndr_ne_wanted
   single: b2mndr_*fb*; b2mndr_ne_wanted_time


.. index:: b2mndt_use_b2srst

``b2mndt_use_b2srst``    type: ``integer``    default: ``1``
    Switches off the stabilization of the source coefficients.
    

.. index:: b2mndt_rxf

``b2mndt_rxf``    type: ``real``    default: ``See description``
    Main under-relaxation parameter. The default value is 0.5 in steady-state mode (b2mndt\_style.eq.1).
    Setting this switch to zero prevents updating of the principal code quantities.
    In time-dependent mode (b2mndt\_style.eq.2), the default value is 1.0. It can be set lower than 1, provided that the following relationship is satisfied: DTxx=1/(1-(1-rxf)^nstgJ).
    DTxx are the time-step multipliers (xx=CO,MO,EE,EI,...) and nstgJ the inner iterations (J=0,1,2). For example, if rxf=0.5 and nstgJ=1, then it must be DTxx=2.
    Tip: If nstgJ is high enough, DTxx tends to 1 for any rxf, and no time-step multipliers need to be changed.
    

.. index:: b2news_xfm.

.. index:: b2news_xfm0, b2news_xfm1, b2news_xfm2, b2news_xfm3
.. c

``b2news_xfm.``

  - ``b2news_xfm0``  -     type: ``real``    default: ``1.0``

  - ``b2news_xfm1``  -     type: ``real``    default: ``1.0``

  - ``b2news_xfm2``  -     type: ``real``    default: ``1.0``

  - ``b2news_xfm3``  -     type: ``real``    default: ``1.0``


    Under-relaxation parameters for the parallel momentum, continuity, potential and energy equations respectively.
    Setting these switches to zero prevents updating of the associated code quantities.
    
.. index::
   single: b2news_xfm.; b2news_xfm0
   single: b2news_xfm.; b2news_xfm1
   single: b2news_xfm.; b2news_xfm2
   single: b2news_xfm.; b2news_xfm3


.. index:: b2npco_pcm.

.. index:: b2npco_pcm0, b2npco_pcm1
.. c

``b2npco_pcm.``

  - ``b2npco_pcm0``  -     type: ``real``    default: ``1.0``

  - ``b2npco_pcm1``  -     type: ``real``    default: ``1.0``


    Specifiy multipliers to Rhie-Chow corrections from particle equations
    Not used (and default set to zero) if running in time-dependent mode (b2mndt\_style.eq.2).
    b2npco\_pcm0 is a multiplier for the update on the parallel velocity following the pressure-correction equation.
    b2npco\_pcm1 is a multiplier for the Rhie-Chow terms in the particle fluxes.
    
.. index::
   single: b2npco_pcm.; b2npco_pcm0
   single: b2npco_pcm.; b2npco_pcm1


.. index:: b2npco_rxg

``b2npco_rxg``    type: ``real``    default: ``1.0``
    rxg specifies a special under-relaxation parameter. A term of the form "abs(residual)/rxg" is added to the diagonal of the matrix of the correction equation, with the effect of limiting the computed correction. rxg is dimensionless and of order unity; smaller values of rxg imply stronger damping.
    Not used if running in time-dependent mode (b2mndt\_style.eq.2).
    

.. index:: b2npht_pcm*

.. index:: b2npht_pcm0, b2npht_pcm1
.. c

``b2npht_pcm*``

  - ``b2npht_pcm0``  -     type: ``real``    default: ``1.0``

  - ``b2npht_pcm1``  -     type: ``real``    default: ``1.0``


    Specifies multipliers to Rhie-Chow corrections from heat equations.
    Not used (and default set to zero) if running in time-dependent mode (b2mndt\_style.eq.2).
    b2npht\_pcm0 is a multiplier for the update on the parallel velocity following the update of Ti and Te.
    b2npht\_pcm1 is a multiplier for the Rhie-Chow terms in the flow fields of ion, electron, and neutral heat.
    
.. index::
   single: b2npht_pcm*; b2npht_pcm0
   single: b2npht_pcm*; b2npht_pcm1


.. index:: b2npht_rxg

``b2npht_rxg``    type: ``real``    default: ``1.0``
    rxg specifies a special under-relaxation parameter. A term of the form "abs(residual)/rxg" is added to the diagonal of the matrix of the correction equation, with the effect of limiting the computed correction. rxg is dimensionless and of order unity; smaller values of rxg imply stronger damping.
    Not used if running in time-dependent mode (b2mndt\_style.eq.2).
    

.. index:: b2npht_style

``b2npht_style``    type: ``integer``    default: ``1``
    When set to '1', SPb form of the program b2sihs\_ is called. b2npht\_style.eq.0 no longer available for WG.
    

.. index:: b2npmo_rxg

``b2npmo_rxg``    type: ``real``    default: ``1.0e6``
    Normalisation factor for the parallel momentum equation.
    Not used when running in time\_dependent mode (b2mndt\_style.eq.2).
    

.. index:: b2news_poteq

``b2news_poteq``    type: ``integer``    default: ``1``
    If poteq.eq.0, the potential equation is jumped over and not solved.
    If poteq.eq.2, the potential is set to 3.1\*Te/qe as per SOLPS4.0.
    If poteq.eq.1, the potential equation is solved according to the no\_solve switch settings.
    If poteq.ne.1, then 'b2tfhe\_no\_current' must be set to '1'.
    

.. index:: b2nxdv_style

``b2nxdv_style``    type: ``integer``    default: ``1``
    When set to '1', the total friction force cancel is not calculated at the guard boundary cells.
    It is recommended '1'.
    

.. index:: b2nxfc_style

``b2nxfc_style``    type: ``integer``    default: ``1``
    style specifies the precise form of interpolation used in the computation of flcb and cvcb. When set to '1', SPb form of the transport terms in the momentum correction equation is used.
    It is recommended '1'.
    

.. index:: b2nxfx_style

``b2nxfx_style``    type: ``integer``    default: ``1``
    When set to '1', SPb form of an expression that occurs in the electron-atom thermal force is used. Only used if b2sigp\_style.ne.2.
    It is recommended '1'.
    

.. index:: b2sifr_styl0

``b2sifr_styl0``    type: ``integer``    default: ``0``
    Specify the type of linearisation used in the thermal force term.
    

.. index:: b2tfhe_mode_ehx

``b2tfhe_mode_ehx``    type: ``integer``    default: ``0``
    Switch to choose between various discretization schemes when computing the poloidal electric field.
    See code for details.
    

.. index:: b2tfhe_mode_ehy

``b2tfhe_mode_ehy``    type: ``integer``    default: ``0``
    Switch to choose between various discretization schemes when computing the radial electric field.
    See code for details.
    

.. index:: b2sigp_style

``b2sigp_style``    type: ``integer``    default: ``2``
    When set to '1', SPb form of the pressure gradient term on the right hand of the momentum balance equation is used.
    When set to '2', the parallel current term contains a correction due to impurities, when Z\_eff is not equal to the average plasma ion charge. Only usable if the potential equation is solved simultaneously (b2news\_poteq.eq.1).
    The default value of '2' is recommended for cases with one main hydrogenic species (or at least where the main species is the lightest one) and any amount of impurities. It is not guaranteed to yield correct results for hydrogen isotopic mixtures or non-hydrogenic plasmas.
    

.. index:: b2sigp_pressure_restriction

``b2sigp_pressure_restriction``    type: ``integer``    default: ``1``
    When set to '1', a CFL-like restriction is applied to the pressure gradient term for minority ions and for neutrals species.
    

.. index:: b2xzdd_zero_dead_and_core

``b2xzdd_zero_dead_and_core``    type: ``integer``    default: ``1``
    If 1 then zero passed sources in dead regions,
    If 2 zero passed sources in dead regions and core boundary cells
    If 0 then SKIP
    

.. index:: b2sihs_rf.

.. index:: b2sihs_rf0, b2sihs_rf1, b2sihs_rf2, b2sihs_rf3, b2sihs_rf4
.. c

``b2sihs_rf.``

  - ``b2sihs_rf0``  -     type: ``real``    default: ``1.0``

  - ``b2sihs_rf1``  -     type: ``real``    default: ``1.0``

  - ``b2sihs_rf2``  -     type: ``real``    default: ``1.0``

  - ``b2sihs_rf3``  -     type: ``real``    default: ``1.0``

  - ``b2sihs_rf4``  -     type: ``real``    default: ``1.0``


    rf0-4 are numerical parameters, see the code. All must be non-negative and of order unity; larger values are meant to provide more stabilisation. Some or all may be set to zero and removed eventually. I have had some experience to indicate that rf0, rf2, rf4 may have a useful function; however, later changes in the code may have made all these parameters superfluous.
    
.. index::
   single: b2sihs_rf.; b2sihs_rf0
   single: b2sihs_rf.; b2sihs_rf1
   single: b2sihs_rf.; b2sihs_rf2
   single: b2sihs_rf.; b2sihs_rf3
   single: b2sihs_rf.; b2sihs_rf4


.. index:: b2srdt_phm.

.. index:: b2srdt_phm0, b2srdt_phm1, b2srdt_phm3, b2srdt_phm4, b2srdt_phm5
.. c

``b2srdt_phm.``

  - ``b2srdt_phm0``  -     type: ``real``    default: ``1.0``

  - ``b2srdt_phm1``  -     type: ``real``    default: ``1.0``

  - ``b2srdt_phm3``  -     type: ``real``    default: ``1.0``

  - ``b2srdt_phm4``  -     type: ``real``    default: ``0.0``

  - ``b2srdt_phm5``  -     type: ``real``    default: ``1.0``


    Multipliers to the density, parallel momentum, heat, potential, and electron particle time-derivative source terms, respectively.
    'phm4' is normally zero since the potential equation contains no source terms.
    
.. index::
   single: b2srdt_phm.; b2srdt_phm0
   single: b2srdt_phm.; b2srdt_phm1
   single: b2srdt_phm.; b2srdt_phm3
   single: b2srdt_phm.; b2srdt_phm4
   single: b2srdt_phm.; b2srdt_phm5


.. index:: b2srst_rf*

.. index:: b2srst_rf0, b2srst_rf1, b2srst_rf2, b2srst_rf3
.. c

``b2srst_rf*``

  - ``b2srst_rf0``  -     type: ``real``    default: ``1.0``

  - ``b2srst_rf1``  -     type: ``real``    default: ``1.0``

  - ``b2srst_rf2``  -     type: ``real``    default: ``1.0``

  - ``b2srst_rf3``  -     type: ``real``    default: ``1.0``


    (rf0/1/2/3 for numerical stabilisation)
    
.. index::
   single: b2srst_rf*; b2srst_rf0
   single: b2srst_rf*; b2srst_rf1
   single: b2srst_rf*; b2srst_rf2
   single: b2srst_rf*; b2srst_rf3


.. index:: b2stcx_rg0

``b2stcx_rg0``    type: ``real``    default: ``1.0``
    (rg0 for numerical stabilisation; needs experiments.)
    

.. index:: b2stcx_styl0

``b2stcx_styl0``    type: ``integer``    default: ``0``
    Specifies the type of linearisation used in the charge exchange momentum source term.
    

.. index:: eirene_mc_linearisation

``eirene_mc_linearisation``    type: ``integer``    default: ``1``
    Specifies the type of linearisation used in the sources derived from the Monte Carlo neutrals. If linearisation.eq.0, all sources are fed to the constant term, if linearisation.eq.1, positive terms go in the constant term, and negative terms in the proportional term. 'eirene\_mc\_linearization' is an alias for this switch.
    

.. index:: b2stbm_linearisation

``b2stbm_linearisation``    type: ``real``    default: ``1.0``
    Same as above, but applied to the sources coming for an externally coupled code providing plasma sources, for instance a kinetic treatment of trace impurity ions. 'b2stbm\_linearization' is an alias for this switch.
    

.. index:: b2stbm_impgyro_mod

``b2stbm_impgyro_mod``    type: ``integer``    default: ``0``
    Specifies the frequency (in units of full B2.5 timesteps) at which an externally coupled code providing additional source (for instance a kinetic treatment of trace impurity ions such as IMPGYRO) should be called.
    

.. index:: b2stel_r*

.. index:: b2stel_rg0, b2stel_rg1, b2stel_rxm0, b2stel_rxm1, b2stel_rxm2, b2stel_rxm3, b2stel_rxm4
.. c

``b2stel_r*``

  - ``b2stel_rg0``  -     type: ``real``    default: ``1.0``

  - ``b2stel_rg1``  -     type: ``real``    default: ``1.0``

  - ``b2stel_rxm0``  -     type: ``real``    default: ``0.0``

  - ``b2stel_rxm1``  -     type: ``real``    default: ``0.0``

  - ``b2stel_rxm2``  -     type: ``real``    default: ``0.0``

  - ``b2stel_rxm3``  -     type: ``real``    default: ``0.0``

  - ``b2stel_rxm4``  -     type: ``real``    default: ``0.0``


    Damping coefficient applied to the atomic physics sources.
    
.. index::
   single: b2stel_r*; b2stel_rg0
   single: b2stel_r*; b2stel_rg1
   single: b2stel_r*; b2stel_rxm0
   single: b2stel_r*; b2stel_rxm1
   single: b2stel_r*; b2stel_rxm2
   single: b2stel_r*; b2stel_rxm3
   single: b2stel_r*; b2stel_rxm4


.. index:: b2stel_styl0

``b2stel_styl0``    type: ``integer``    default: ``0``
    Specifies the type of linearisation used in the charge exchange momentum source term.
    

.. index:: b2tfcc_xfac

``b2tfcc_xfac``    type: ``real``    default: ``1.0``
    Multiplier to the pressure force term.
    

.. index:: b2tfhe_mdf

``b2tfhe_mdf``    type: ``integer``    default: ``0``
    If '1', SPb new form of calculating electron heat flux is used. It is recommended '1' for runs with drifts.
    

.. index:: b2tfhe_no_current

``b2tfhe_no_current``    type: ``integer``    default: ``0``
    If no\_current.eq.1, all currents are set to zero. The setting no\_current.eq.1 must be used if the potential equation is not explicitly solved for, i.e. for b2news\_poteq.ne.1.
    

.. index:: b2tfhe_prl_cur

``b2tfhe_prl_cur``    type: ``real``    default: ``1.0``
    Multiplier to the parallel current.
    

.. index:: b2tfhi_mdf

``b2tfhi_mdf``    type: ``integer``    default: ``0``
    If '1', SPb new form of calculating ion heat flux is used.
    It is recommended '1' for runs with drifts.
    

.. index:: b2tfnb_drift_style

``b2tfnb_drift_style``    type: ``integer``    default: ``1``
    When set to '0', drift velocities are calculated in cell centers (NO LONGER SUPPORTED IN WG CODE).
    When set to '1', drift velocities are calculated in cell faces.
    It is recommended '1'.
    

.. index:: b2tfnb_poleldr

``b2tfnb_poleldr``    type: ``real``    default: ``1.0``
    Multiplier to the poloidal electrical drift velocity.
    

.. index:: b2tfnb_radeldr

``b2tfnb_radeldr``    type: ``real``    default: ``1.0``
    Multiplier to the radial electrical drift velocity.
    

.. index:: b2tfnb_poldidr

``b2tfnb_poldidr``    type: ``real``    default: ``1.0``
    Multiplier to the poloidal diamagnetic drift velocity.
    

.. index:: b2tfnb_raddidr

``b2tfnb_raddidr``    type: ``real``    default: ``1.0``
    Multiplier to the radial diamagnetic drift velocity.
    

.. index:: b2tfnb_mdf

``b2tfnb_mdf``    type: ``integer``    default: ``0``
    If '1', SPb new form of calculating particle flux is used.
    It is recommended '1' for runs with drifts.
    

.. index:: b2upht_stylec

``b2upht_stylec``    type: ``integer``    default: ``0``
    (stylec is a numerical switch, needs experiments)
    

.. index:: b2usmo_cfc0

``b2usmo_cfc0``    type: ``real``    default: ``1.0``
    Linearisation constant.
    

.. index:: b2srsm_enable

``b2srsm_enable``    type: ``integer``    default: ``0``
    If enable.ne.0, then the sources for particle, parallel momentum, electron and ion heat are rescaled, for non-boundary cells, if the local timestep exceeds the physics timescale implied by those sources.
    enable.ne.0 not yet available for WG.
    

.. index:: b2tinnt_style

``b2tinnt_style``    type: ``integer``    default: ``1``
    Integer switch to choose the numerical treatment of the ion pressure gradient calculation for the ion-neutral current.
    If b2tinnt\_style.eq.0, then the chain rule is first applied to the product of density and temperature, and (grad n)/n is rewritten as grad(log(n)).
    If b2tinnt\_style.eq.1 (default), then the gradient of the product of density and temperature is calculated directly.
    

.. index:: b2stbr_phys_lin_shi0

``b2stbr_phys_lin_shi0``    type: ``integer``    default: ``0``
    Determines the linearisation of the boundary condition heat source due to neutral recycling/reflection when erecyc in used. Not used for advanced fluid neutral (AFN) model.
    lin\_shi0.eq.0: put source in shi0(iCv,0).
    lin\_shi0.eq.1: put source/ti in shi0(iCv,1).
    

.. index:: b2npmo_discr_meth*

.. index:: b2npmo_discr_meth, b2tfhe_discr_meth, b2tfhi_discr_meth, b2tfnb_discr_meth
.. c

``b2npmo_discr_meth*``

  - ``b2npmo_discr_meth``  -     type: ``integer``    default: ``2``

  - ``b2tfhe_discr_meth``  -     type: ``integer``    default: ``2``

  - ``b2tfhi_discr_meth``  -     type: ``integer``    default: ``2``

  - ``b2tfnb_discr_meth``  -     type: ``integer``    default: ``2``


    Determines the discretization method for the calculation of the fluxes.
    discr\_meth.eq.0: central scheme
    discr\_meth.eq.1: upwind scheme
    discr\_meth.eq.2: SOLPS5 hybrid scheme
    discr\_meth.eq.3: SOLPS4 continuity scheme. Not yet available for WG.
    
.. index::
   single: b2npmo_discr_meth*; b2npmo_discr_meth
   single: b2npmo_discr_meth*; b2tfhe_discr_meth
   single: b2npmo_discr_meth*; b2tfhi_discr_meth
   single: b2npmo_discr_meth*; b2tfnb_discr_meth


.. index:: b2tfnb_style_int_vel

``b2tfnb_style_int_vel``    type: ``integer``    default: ``0``
    Determines the interpolation weights to get the parallel velocities at the cell faces.
    style\_int\_vel.eq.0: interpolation based on cell volumes.
    style\_int\_vel.eq.1: interpolation based on cell connector lengths.
    Only the combination b2tfnb\_style\_int\_vel=0 and b2sihs\_style\_int\_vel=0 works robustly for now. Other combinations gave rise to oscillations. More research needed.
    

.. index:: b2sihs_style_int_vel

``b2sihs_style_int_vel``    type: ``integer``    default: ``0``
    Determines the interpolation weights to get the parallel velocities at the cell faces for the calculation of divergence ua.
    style\_int\_vel.eq.0: interpolation based on cell connector lengths.
    style\_int\_vel.eq.1: interpolation based on cell volumes.
    Only the combination b2tfnb\_style\_int\_vel=0 and b2sihs\_style\_int\_vel=0 works robustly for now. Other combinations gave rise to oscillations. More research needed.
    

.. index:: 
   single: Numerics; b2news_potit*
   single: Numerics; b2news_potok
   single: Numerics; b2news_ramp_slow
   single: Numerics; b2mndr_use_9pt_stencil
   single: Numerics; b2mndr_min_ares*
   single: Numerics; b2mndr_res_quit
   single: Numerics; b2mndt_nstg_ares*
   single: Numerics; b2news_nsm*
   single: Numerics; eirene_*
   single: Numerics; eirene_print_minmax
   single: Numerics; eirene_extrap
   single: Numerics; eirene_ank_mods
   single: Numerics; eirene_dpc_fix
   single: Numerics; b2stbr_eir_src_nhist
   single: Numerics; eirene_neutr_avg
   single: Numerics; eirene_underrelax
   single: Numerics; eirene_uub_style
   single: Numerics; b2news_area_fix
   single: Numerics; b2npmo_ion_vlct_restrict
   single: Numerics; b2npmo_ion_vlct_restrict_M
   single: Numerics; b2mndr_ua_max
   single: Numerics; b2nppo_restr_po
   single: Numerics; b2upht_rte_min
   single: Numerics; b2sihs_shivis
   single: Numerics; b2sihs_shi
   single: Numerics; b2sihs_shidu
   single: Numerics; b2sihs_shidd
   single: Numerics; b2sihs_shedu
   single: Numerics; b2sihs_shedd
   single: Numerics; b2tfhe_vis_per
   single: Numerics; b2stbc_sheath_drift_fix
   single: Numerics; b2stbc_BC2_cor9
   single: Numerics; b2stbc_fix_fch_in_fhe_sheath
   single: Numerics; b2stbr_potential_at_guard_cell
   single: Numerics; b2stbr_temperature_at_guard_cell
   single: Numerics; b2trcl_conductive_limit
   single: Numerics; b2trcl_core_cond_limit
   single: Numerics; b2tlh0_flux_limit_style
   single: Numerics; b2tral_mode
   single: Numerics; b2tfh._*hybr*
   single: Numerics; ._upwind
   single: Numerics; b2tfnb_pflux_cor
   single: Numerics; b2trcl_cvsa_mltpl
   single: Numerics; b2uxus_mult_nonzero
   single: Numerics; b2uxus_mult_solvdim*
   single: Numerics; b2ux5p_style
   single: Numerics; b2ux7p_style
   single: Numerics; b2ux9p_style
   single: Numerics; b2ux5p_acpar
   single: Numerics; b2stbc_fchy_dia
   single: Numerics; b2stbc_fchy_dia_coreonly
   single: Numerics; b2stbc_neoclassical
   single: Numerics; b2stbc_cbc
   single: Numerics; b2stbc_integral_current
   single: Numerics; b2stbr_first_flight_dl
   single: Numerics; b2stbr_first_flight_no_of_flights
   single: Numerics; b2stbr_first_flight_table_size
   single: Numerics; b2stbc_s*
   single: Numerics; b2stbc_bcpot_16_step
   single: Numerics; b2stbc_stab_coeff_sheath_te
   single: Numerics; b2stbc_stab_coeff_sheath_ti
   single: Numerics; b2npht_stab_shei
   single: Numerics; b2txcx_increase_transp_coefs
   single: Numerics; b2trno_set_chcb_0
   single: Numerics; b2mndr_na_min
   single: Numerics; b2mndr_na_new
   single: Numerics; b2upht_te_min
   single: Numerics; b2upht_te_max
   single: Numerics; b2upht_ti_min
   single: Numerics; b2upht_ti_max
   single: Numerics; b2upht_tn_min
   single: Numerics; b2upht_tn_max
   single: Numerics; b2upht_kt_min
   single: Numerics; b2upht_kt_max
   single: Numerics; b2upht_zt_min
   single: Numerics; b2upht_zt_max
   single: Numerics; b2news_guard_flows
   single: Numerics; b2news_fac*
   single: Numerics; b2stbc_istyle_cur_contr_on_S_and_N
   single: Numerics; b2stbc_istyle_fchi
   single: Numerics; b2news_no_b2sral_call
   single: Numerics; b2news_do_2nd_b2npco_call
   single: Numerics; b2news_re_eval_prtls_fluxes
   single: Numerics; b2mndt_style
   single: Numerics; b2mndt_ckn
   single: Numerics; b2mndt_dummy
   single: Numerics; b2mndt_ntim_step_out
   single: Numerics; b2mndt_calc_err_step_out
   single: Numerics; b2stb*
   single: Numerics; b2stbc_type13_*
   single: Numerics; heatdiff1D_*
   single: Numerics; b2trno_flux_limit_to_dpa
   single: Numerics; b2trno_flux_limit_to_vsa
   single: Numerics; b2mndr_*fb*
   single: Numerics; b2mndt_use_b2srst
   single: Numerics; b2mndt_rxf
   single: Numerics; b2news_xfm.
   single: Numerics; b2npco_pcm.
   single: Numerics; b2npco_rxg
   single: Numerics; b2npht_pcm*
   single: Numerics; b2npht_rxg
   single: Numerics; b2npht_style
   single: Numerics; b2npmo_rxg
   single: Numerics; b2news_poteq
   single: Numerics; b2nxdv_style
   single: Numerics; b2nxfc_style
   single: Numerics; b2nxfx_style
   single: Numerics; b2sifr_styl0
   single: Numerics; b2tfhe_mode_ehx
   single: Numerics; b2tfhe_mode_ehy
   single: Numerics; b2sigp_style
   single: Numerics; b2sigp_pressure_restriction
   single: Numerics; b2xzdd_zero_dead_and_core
   single: Numerics; b2sihs_rf.
   single: Numerics; b2srdt_phm.
   single: Numerics; b2srst_rf*
   single: Numerics; b2stcx_rg0
   single: Numerics; b2stcx_styl0
   single: Numerics; eirene_mc_linearisation
   single: Numerics; b2stbm_linearisation
   single: Numerics; b2stbm_impgyro_mod
   single: Numerics; b2stel_r*
   single: Numerics; b2stel_styl0
   single: Numerics; b2tfcc_xfac
   single: Numerics; b2tfhe_mdf
   single: Numerics; b2tfhe_no_current
   single: Numerics; b2tfhe_prl_cur
   single: Numerics; b2tfhi_mdf
   single: Numerics; b2tfnb_drift_style
   single: Numerics; b2tfnb_poleldr
   single: Numerics; b2tfnb_radeldr
   single: Numerics; b2tfnb_poldidr
   single: Numerics; b2tfnb_raddidr
   single: Numerics; b2tfnb_mdf
   single: Numerics; b2upht_stylec
   single: Numerics; b2usmo_cfc0
   single: Numerics; b2srsm_enable
   single: Numerics; b2tinnt_style
   single: Numerics; b2stbr_phys_lin_shi0
   single: Numerics; b2npmo_discr_meth*
   single: Numerics; b2tfnb_style_int_vel
   single: Numerics; b2sihs_style_int_vel

.. index:: Atomic Physics

Atomic Physics
==============
.. index:: b2ardr_fix_cx

``b2ardr_fix_cx``    type: ``integer``    default: ``1``
    It is used to 'correct' the CX data
    0 => do not fix
    1 => only fix H if CX data is < 1e-40 [default]
    2 => fix if CX data is < 1e-40
    3 => fix H
    4 => fix all
    At the moment the only species with CX data in ADAS is C. Be careful with options that use the fit formula other than for H.
    See the comments in ratstr.F for the origin of the fit formula used to 'fix' the CX data.
    

.. index:: b2ardr_no_weisheit

``b2ardr_no_weisheit``    type: ``integer``    default: ``0``
    When set to 1, disables the correction of the hydrogen atomic rate data with the Weisheit data using ratwei.
    Must be set to 1 when using b2ardr\_amjhydhel.
    \*\*\* Use with caution! \*\*\*
    

.. index:: b2ardr_amjhydhel

``b2ardr_amjhydhel``    type: ``integer``    default: ``0``
    When not set to 0, reads reaction cards from the AMJUEL/HYDHEL database files to overwrite rates for neutral hydrogenic species.
    The list of reaction cards to be used should be given in the b2ar.dat file.
    Cannot be used in conjunction with no\_weisheit.eq.0.
    

.. index:: b2ardr_no_smoothing

``b2ardr_no_smoothing``    type: ``integer``    default: ``0``
    When set to 1, disables the tail smoothing for of rate coefficients to represent the effect of a power-law tail on the distribution function. It has been added for compatibility with SOLPS4.3
    

.. index:: adas_extrap

``adas_extrap``    type: ``integer``    default: ``1``
    Switch for choosing extrapolation method of ADAS data:
    If adas\_extrap.eq.0, a simple 2-D linear extrapolation in log-log space is used (may lead to spurious results).
    If adas\_extrap.eq.1, use the extrapolated result, but growing no faster than the parameter variation to the 3/2 power (default).
    If adas\_extrap.eq.2, use the nearest domain edge value.
    

.. index:: b2ardr_*_recomb

.. index:: b2ardr_fix_recomb, b2ardr_zmax_recomb
.. c

``b2ardr_*_recomb``

  - ``b2ardr_fix_recomb``  -     type: ``integer``    default: ``0``

  - ``b2ardr_zmax_recomb``  -     type: ``integer``    default: ``1``


    When fix\_recomb is changed from 0, and if the ADAS option is in use, then uses the PRB file to add the contribution arising from is-->is-1 processes.
    If the AMJUEL/HYDHEL rates are in use and fix\_recomb.eq.0, then the recombination energy is substracted to the electron recombination energy costs. May lead to negative rates!
    This term includes the bremsstrahlung.
    For ADAS, the '0' option only contains the bremsstrahlung for the is-->is-1 process.
    The correction is only applied for isonuclear sequences with nuclear charge up to zmax\_recomb, inclusive.
    Use of this option is still experimental!
    
.. index::
   single: b2ardr_*_recomb; b2ardr_fix_recomb
   single: b2ardr_*_recomb; b2ardr_zmax_recomb


.. index:: b2ardr_nreac

``b2ardr_nreac``    type: ``integer``    default: ``0``
    Number of AMJUEL/HYDHEL reactions you explicitly specify in b2ar.dat, when b2ardr\_amjhydhel = 1. A set of default reactions is taken but can be overwritten by the reactions you specify here.
    

.. index:: b2ardr_rtn.

.. index:: b2ardr_rtnt, b2ardr_rtnn
.. c

``b2ardr_rtn.``

  - ``b2ardr_rtnt``  -     type: ``integer``    default: ``40``

  - ``b2ardr_rtnn``  -     type: ``integer``    default: ``32``


    The number of intervals in the discretisation of the density (rtnn) and temperature (rtnt) ranges for the atomic physics tables.
    
.. index::
   single: b2ardr_rtn.; b2ardr_rtnt
   single: b2ardr_rtn.; b2ardr_rtnn


.. index:: b2mndr_dpc_mod_rates_*_hot*

.. index:: b2mndr_dpc_mod_rates_ne_hot_frac, b2mndr_dpc_mod_rates_te_hot
.. c

``b2mndr_dpc_mod_rates_*_hot*``

  - ``b2mndr_dpc_mod_rates_ne_hot_frac``  -     type: ``real``    default: ``0.0``

  - ``b2mndr_dpc_mod_rates_te_hot``  -     type: ``real``    default: ``0.0``


    Modify the atomic rates by including a hot electron population of temperature te\_hot (in eV) and a population faction ne\_hot\_frac.
    Still experimental.
    
.. index::
   single: b2mndr_dpc_mod_rates_*_hot*; b2mndr_dpc_mod_rates_ne_hot_frac
   single: b2mndr_dpc_mod_rates_*_hot*; b2mndr_dpc_mod_rates_te_hot


.. index:: b2ardr_t_min

``b2ardr_t_min``    type: ``real``    default: ``0.0``
    Lower temperature bound (in eV) used for rates imported from AMJUEL/HYDHEL database for neutral hydrogenic species. Rates below this bound are given the same value as they have at t\_min.
    Only operational if within the bounds provided by tlohi in the b2ar.dat file header.
    

.. index:: b2ardr_t_max

``b2ardr_t_max``    type: ``real``    default: ``1.0e30``
    Upper temperature bound (in eV) used for rates imported from AMJUEL/HYDHEL database for neutral hydrogenic species. Rates above this bound are given the same value as they have at t\_max.
    Only operational if within the bounds provided by tlohi in the b2ar.dat file header.
    

.. index:: b2ardr_nn_min

``b2ardr_nn_min``    type: ``real``    default: ``0.0``
    Lower density bound (in m^{-3}) used for rates imported from AMJUEL/HYDHEL database for neutral hydrogenic species. Rates below this bound are given the same value as they have at n\_min.
    Only operational if within the bounds provided by nlohi in the b2ar.dat file header.
    

.. index:: b2ardr_nn_max

``b2ardr_nn_max``    type: ``real``    default: ``1.0e30``
    Upper density bound (in m^{-3}) used for rates imported from AMJUEL/HYDHEL database for neutral hydrogenic species. Rates above this bound are given the same value as they have at n\_max.
    Only operational if within the bounds provided by nlohi in the b2ar.dat file header.
    

.. index:: 
   single: Atomic Physics; b2ardr_fix_cx
   single: Atomic Physics; b2ardr_no_weisheit
   single: Atomic Physics; b2ardr_amjhydhel
   single: Atomic Physics; b2ardr_no_smoothing
   single: Atomic Physics; adas_extrap
   single: Atomic Physics; b2ardr_*_recomb
   single: Atomic Physics; b2ardr_nreac
   single: Atomic Physics; b2ardr_rtn.
   single: Atomic Physics; b2mndr_dpc_mod_rates_*_hot*
   single: Atomic Physics; b2ardr_t_min
   single: Atomic Physics; b2ardr_t_max
   single: Atomic Physics; b2ardr_nn_min
   single: Atomic Physics; b2ardr_nn_max

.. index:: Optimization

Optimization
============
.. index:: b2optim_save_states

``b2optim_save_states``    default: ``0``
    If larger than zero, specifies the number of optimization iterations between writes of the intermediate state file b2fstate\_optim.XXXX.
    

.. index:: b2optim_reset_drift

``b2optim_reset_drift``    default: ``0.4``
    Percentage value at which drifts are reset at each function/gradient evaluation to avoid simualtion crash.
    

.. index:: b2optim_reset_iter

``b2optim_reset_iter``    default: ``2``
    When resetting drifts, the drift increase multiplier (e.g. fac\_exb\_inc) will be computed so that drifts are back at 100% in ntim/b2optim\_reset\_iter iterations.
    

.. index:: 
   single: Optimization; b2optim_save_states
   single: Optimization; b2optim_reset_drift
   single: Optimization; b2optim_reset_iter

*************
b2.parameters
*************
.. index:: b2.neutrals.parameters

b2.neutrals.parameters
======================
.. index:: NSTRAI

``NSTRAI``    type: ``integer``    default: ``0``
    Number of neutral sources, or 'strata'. Must not be larger than DEF\_NSTRA from the [$SOLPSTOP/modules/B2.5/]src/modules(.local)/b2mod\_dimensions.F file.
    Need not include the time-dependent stratum. If a time-dependent stratum is used, is incremented internally as needed. The incremented value is referred to as NSTRAT below.
    

.. index:: RCPOS

``RCPOS``    type: ``integer array of length (NSTRAT)``    default: ``-2``
    Position in the B2.5 grid of the strata. Similar use as BCPOS from /BOUNDARY/ namelist. Obsolete for WG.
    

.. index:: RCSTART

``RCSTART``    type: ``integer array of length (NSTRAT)``    default: ``-2``
    Starting label index on the B2.5 grid. Similar use as BCSTART from /BOUNDARY/ namelist.
    

.. index:: RCEND

``RCEND``    type: ``integer array of length (NSTRAT)``    default: ``-2``
    Ending label index on the B2.5 grid. Similar use as BCEND from /BOUNDARY/ namelist.
    

.. index:: RC_LIST_SIZE

``RC_LIST_SIZE``    type: ``integer array of length (NSTRAT)``    default: ``0``
    Contains the size of the recycling boundary lists. Similar use as BC\_LIST\_SIZE from /BOUNDARY/ namelist.
    

.. index:: RC_LIST_X

``RC_LIST_X``    type: ``integer array of length (2*(NXD+NYD),NSTRAT)``    default: ``-2``
    Contains the X-coordinate of the cells where recycling boundaries are applied. Similar use as BC\_LIST\_X from /BOUNDARY/ namelist. Obsolete for WG.
    

.. index:: RC_LIST_Y

``RC_LIST_Y``    type: ``integer array of length (2*(NXD+NYD),NSTRAT)``    default: ``-2``
    Contains the Y-coordinate of the cells where recycling boundaries are applied. Similar use as BC\_LIST\_Y from /BOUNDARY/ namelist. Obsolete for WG.
    

.. index:: TARGSP

``TARGSP``    type: ``integer array of size (NSTRAT,NTRACK)``    default: ``b2stbr_sput_dst``
    Identifies the base material(s) of this stratum wall. The number corresponds to the B2.5 species index produced by sputtering. Check b2cdci for details. If the bulk species is not sputtered, should contain -1.
    

.. index:: CHEMSP

``CHEMSP``    type: ``logical array of length NSTRAT``    default: ``.false.``
    Indicates whether chemical sputtering is allowed from this wall stratum.
    

.. index:: B2RECYC

``B2RECYC``    type: ``real array of size (0:NS-1,NSTRAT)``
    Stores the particle recycling coefficients of species (is) on stratum (istra). Defaults to 1.0 for non-carbon species and 0.0 for carbon species. Particles recycle into the neutral species associated to their isonuclear sequence.
    Applies to B2.5 neutral fluid species.
    If B2RECYC is not explicitly specified, the values from RECYC will be taken.
    

.. index:: RECYC

``RECYC``    type: ``real array of size (0:NS-1,NSTRAT)``
    Multiplies Eirene recycling fluxes if 'eirene\_use\_recyceir' is set to 0 (see b2cdci for details).
    If B2RECYC is not specified, RECYC will also be applied to B2.5 neutral fluid species.
    

.. index:: MRECYC

``MRECYC``    type: ``real array of size (0:NS-1,NSTRAT)``    default: ``0.0``
    Stores the parallel momentum recycling coefficients of species (is) on stratum (istra). The parallel momentum is carried back by the recycled neutrals. Applies only to B2.5 neutral fluid species.
    

.. index:: ERECYC

``ERECYC``    type: ``real array of size (0:NS-1,NSTRAT)``
    Stores the energy recycling coefficients of species (is) on stratum (istra). Defaults to 0.3 for non-carbon species and 0.0 for carbon species. The energy is carried back by the recycled neutrals.
    Applies only to B2.5 neutral fluid species.
    

.. index:: RCION

``RCION``    type: ``real array of size (0:NS-1,NSTRAT)``    default: ``0.0``
    Stores the particle-into-ion recycling coefficients of species (is) on stratum (istra). Particles recycle into the next ionised species associated to their isonuclear sequence. Applies only to B2.5 neutral fluid species.
    

.. index:: RECYCEIR

``RECYCEIR``    type: ``real array of size (NSTRAT)``    default: ``1.0``
    Multiplier to the Eirene recycling fluxes from stratum (istra). Only used if 'eirene\_use\_recyceir' is set to 1 (default).
    

.. index:: USERFLUXPARM

``USERFLUXPARM``    type: ``real array of size (NSTRAT,2)``    default: ``0``
    The element (istra,1) contains the strength of constant gas puff strata (type 'C') for Eirene in particles/second. Its values overwrite the values provided by the FLUX variables from the strata description in block 7 of the Eirene input file.
    

.. index:: CRCSTRA

``CRCSTRA``    type: ``character*1 array of length (NSTRAT)``    default: `` ``
    Contains the type of stratum for Eirene. Possible options include:
    'A' - (automatic) topological mesh boundaries (same use as BCCHAR in /BOUNDARY/ namelist). The boundary mesh faces that have fcLbl.ge.RCSTART and fcLbl.le.RCEND belong to this stratum.
    'V' - volume recombination source (related RCPOS, RCSTART, RCEND and RC\_LIST variables are ignored).
    'C' - constant or feedback gas puff source (related RCPOS, RCSTART, RCEND and RC\_LIST variables are ignored). Gas puffs for B2.5 fluid neutrals are handled via b2.boundary.parameters. Unless specified otherwise by use of 'eirene\_nesepm\_istra', it is the first 'C' stratum that is used for feedback puff schemes. See b2cdci for details.
    'T' - time-dependent source for Eirene (related RCPOS, RCSTART, RCEND and RC\_LIST variables are ignored). Long-lived Eirene neutrals are stored in this stratum. See EIRENE\_STEP\_DT below.
    

.. index:: STRASCLFL

``STRASCLFL``    type: ``real array of length (NSTRAT)``    default: ``1.0``
    Scaling factor for the fluid neutral B2.5 sources stemming from the stratum. This scaling is required for the spatially hybrid approach, where the hybrid model for hydrogenic strata is typically combined with a fully kinetic model for other species. In that case, STRASCLFL has to made 1.0 for hydrogenic strata and STRASCLFL has to become small for the other strata. STRASCLFL is a stratum-dependent multiplier in addition to b2mndr\_rescale\_neutrals\_sources. b2mndr\_rescale\_neutrals\_sources is used for all strata and has to be made 1.0 for the hybrid model.
    

.. index:: SURF_MAT

``SURF_MAT``    type: ``character*2 array of length (NSTRAT)``    default: ``'C'``
    Contains the surface material for surface strata, used for AFN neutrals. Examples:
    'Be' (beryllium), 'C' (carbon), 'Fe' (iron), 'Mo' (molybdenum) and 'W' (tungsten).
    

.. index:: ACCEL_ION

``ACCEL_ION``    type: ``integer array of length (NSTRAT)``    default: ``0``
    If 1, adding sheath acceleration for the ions hitting the boundary. Used for AFN boundary conditions.
    

.. index:: MAXW

``MAXW``    type: ``integer array of length (NSTRAT)``    default: ``1``
    Determines the approximation of the particle-velocity distribution of the incident atoms for the AFN boundary condition. MAXW=0: a diffusion approach is used; MAXW=1: a truncated drifting Maxwellian is used. For some cases, MAXW=0 slightly reduces the discrepancy between the fluid and kinetic solution due to an intrinsic correction for lower collisionality. The diffusion and Maxwellian approach are combined when using MAXW=2, for which the Maxwellian approach is used when the local Knudsen number (Kn) is smaller than b2stbr\_kn\_b1, the diffusion approach is used for Kn > b2stbr\_kn\_b2 and a linear interpolation between the two approaches for b2stbr\_kn\_b1 < Kn < b2stbr\_kn\_b2. The macroscopic length scale to determine the local Knudsen number is defined by the parameter l\_macro\_afn.
    

.. index:: MOL

``MOL``    type: ``integer array of length (NSTRAT)``    default: ``0``
    Option to define a purely molecular stratum. Useful if you want to treat only molecules kinetically, whereas the recycled atoms are treated on the B2.5 fluid side.
    

.. index:: HYB_TYPE

``HYB_TYPE``    type: ``character*1 array of length (NSTRAT)``    default: ``'M'``
    When HYB\_TYPE='A' (automatic), possibility to have automatic switching between fluid and kinetic recycling for the stratum for the advanced hybrid model. See description of use\_auto\_spatial\_hyb. HYB\_TYPE should be 'M' (manual) for all strata for multispecies simulations (ns > 1).
    

.. index:: E_FC

``E_FC``    type: ``real``    default: ``3.0``
    Franck-Condon energy assigned to the thermally released fraction of recycled hydrogen neutrals, used in the AFN boundary condition. It is assumed that thermally released molecules are dissociated immediately at the surface and get an energy E\_FC (eV) and are emitted isotropically. 3.0 eV is the value typically used in the EIRENE input file.
    

.. index:: RF_NEUT

``RF_NEUT``    type: ``real array of size (4)``    default: ``1.0``
    Relaxation parameters multiplying the Eirene particle, parallel momentum, electron energy and ion energy sources respectively before use in B2.
    

.. index:: PHYS_SPUT

``PHYS_SPUT``    type: ``real array of size (0:NS-1,NSTRAT)``    default: ``0.0``
    Stores the physical sputtering multiplier for B2.5 species (is) sputtering on the wall of stratum (istra). Must be non-zero for physical sputtering to occur. Only applies if using B2.5 fluid neutral model.
    

.. index:: CHEM_SPUT

``CHEM_SPUT``    type: ``real array of size (0:NS-1,NSTRAT)``    default: ``0.0``
    Stores the chemical sputtering multiplier for B2.5 species (is) sputtering on the wall of stratum (istra). Must be non-zero for chemical sputtering to occur. Only applies if using B2.5 fluid neutral model.
    

.. index:: EIRENE_STEP_CPU

``EIRENE_STEP_CPU``    type: ``real``    default: ``0.0``
    Length of CPU time devoted to Eirene calls after the first one (in s). If zero, the value given in the Eirene input file will be used.
    

.. index:: EIRENE_STEP_DT

``EIRENE_STEP_DT``    type: ``real``    default: ``0.0``
    Physical time (in s) the Eirene particles are to be followed before being passed to the time-dependent stratum. If zero, the value given by DTIMV in block 13 of the Eirene input file will be used.
    

.. index:: EIRENE_MOD

``EIRENE_MOD``    type: ``integer``    default: ``1``
    Frequency of Eirene calls. Eirene is called every EIRENE\_MOD full B2.5 iterations.
    

.. index:: VOLRECSTART

``VOLRECSTART``    type: ``real array of size (NSTRAT)``    default: ``1.e21``
    Initial volume recombination rate from stratum (istra) to be used for the volume recombination scaling regulation algorithm. Rendered obsolete by 'eirene\_dpc\_fix'.
    

.. index:: VOLRECINC

``VOLRECINC``    type: ``real``
    Maximum rate of increase of the volume recombination source strength. The volume recombination regulation scaling scheme is activated if VOLRECINC is neither 0 nor 1.
    Rendered obsolete by 'eirene\_dpc\_fix'.
    

.. index:: VOLRECWT

``VOLRECWT``    type: ``real``    default: ``0.1``
    Weight of new volume recombination strength relative to that of previous iteration in the volume recombination regulation scaling scheme.
    Rendered obsolete by 'eirene\_dpc\_fix'.
    

.. index:: B2SPECIES_START

``B2SPECIES_START``    type: ``integer array of size (NSTRAT)``    default: ``0``
    Specifies the index of the first B2.5 species involved in stratum (istra) for the B2.5 fluid neutral model.
    If not specified, B2SPECIES\_START = SPECIES\_START.
    

.. index:: B2SPECIES_END

``B2SPECIES_END``    type: ``integer array of size (NSTRAT)``    default: ``ns-1``
    Specifies the index of the last B2.5 species involved in stratum (istra) for the B2.5 fluid neutral model.
    If not specified, B2SPECIES\_END = SPECIES\_END.
    

.. index:: SPECIES_START

``SPECIES_START``    type: ``integer array of size (NSTRAT)``    default: ``0``
    Specifies the index of the first B2.5 species involved in stratum (istra) for EIRENE.
    SPECIES\_START is also used for the B2.5 fluid neutral model, if B2SPECIES\_START is not specified.
    

.. index:: SPECIES_END

``SPECIES_END``    type: ``integer array of size (NSTRAT)``    default: ``ns-1``
    Specifies the index of the last B2.5 species involved in stratum (istra) for EIRENE.
    SPECIES\_END is also used for the B2.5 fluid neutral model, if B2SPECIES\_END is not specified.
    

.. index:: NEUTRALS_FILENAME

``NEUTRALS_FILENAME``    type: ``character*256``    default: ``b2.neutrals.parameters``
    Name of the next file to use for reading a new /NEUTRALS/ namelist.
    

.. index:: NEUTRALS_TIME_MOD

``NEUTRALS_TIME_MOD``    type: ``real``    default: ``0.0``
    When the B2.5 run simulation time, in seconds, modulo(NEUTRALS\_TIME\_MOD), reaches or exceeds NEUTRALS\_TIME\_SWITCH, reads the new namelist from NEUTRALS\_FILENAME. Also switches to the new namelist if the ELM count (here time/NEUTRALS\_TIME\_MOD) changes. Only active if NEUTRALS\_TIME\_MOD is greater than 0.
    

.. index:: NEUTRALS_TIME_SWITCH

``NEUTRALS_TIME_SWITCH``    type: ``real``    default: ``0.0``
    If NEUTRALS\_TIME\_MOD is greater than 0, time (in seconds) within an ELM cycle at which a new NEUTRALS namelist is read.
    Otherwise, B2.5 simulation time, in seconds, when to read the next NEUTRALS namelist file from NEUTRALS\_FILENAME.
    Only active if NEUTRALS\_TIME\_SWITCH is greater than 0.
    

.. index:: L_NEUTRAD

``L_NEUTRAD``    type: ``integer``    default: ``0``
    If l\_neutrad >= 0, then the radiated power due to the neutrals atoms is taken directly from the Eirene calculation, instead of being recomputed by B2.
    

.. index:: L_NEUTFLUX

``L_NEUTFLUX``    type: ``integer``    default: ``0 for coupled cases, -1 otherwise``
    If l\_neutflux >=0, then correct treatment of the incident fluxes in B2.5 and b2plot; if <0, then old (approximate) treatment
    

.. index:: LSTRASCL

``LSTRASCL``    type: ``integer array of size (NSTRAT,0:natm)``
    Indicates with which Eirene atomic species to scale the Eirene stratum (istra) (0 means no scaling, default). Atomic species 0 stands for electrons.
    

.. index:: B2EATCR

``B2EATCR``    type: ``integer array of size (0:NS-1)``    default: ``ordering of the B2.5 isonuclear sequences``
    Contains the index of the Eirene atomic species corresponding to the B2.5 species (is).
    

.. index:: B2ESPCR

``B2ESPCR``    type: ``integer array of size (0:NS-1)``    default: ``ordering of the B2.5 isonuclear sequences``
    Contains the isonuclear sequence index of the B2.5 species (is).
    

.. index:: EB2ATCR

``EB2ATCR``    type: ``integer array of size (NATM)``    default: ``first B2.5 species of each isonuclear sequence``
    Contains the index of the B2.5 neutral fluid species corresponding to the Eirene atomic species (iatm).
    

.. index:: EB2SPCR

``EB2SPCR``    type: ``integer array of size (NSPECIES)``    default: ``first B2.5 species of each isonuclear sequence``
    Contains the index of the first B2.5 fluid for each species.
    

.. index:: LATMSCL

``LATMSCL``    type: ``integer array of size (NATM)``    default: ``assuming one-to-one match between Eirene and B2.5 atomic species``
    Contains the index of the B2.5 isonuclear sequence with which the Eirene atomic species (IATM) should be scaled.
    

.. index:: LMOLSCL

``LMOLSCL``    type: ``integer array of size (NMOL)``    default: ``0``
    Contains the index of the Eirene atomic species with which the Eirene molecular species (IMOL) should be scaled.
    

.. index:: MLCMP

``MLCMP``    type: ``integer array of size (NATM,NMOL)``    default: ``0``
    Contains the number of atoms from Eirene atomic species IATM within each molecule of Eirene molecular species IMOL.
    

.. index:: LIONSCL

``LIONSCL``    type: ``integer array of size (NION)``    default: ``0``
    Contains the index of the Eirene atomic species with which the Eirene test ion species (IION) should be scaled. If not provided, LIONSCL will map to LMOLSCL for molecular ions that match an existing declared molecule, or to the first species listed in the name of the molecular ion as declared in the Eirene input file if no matching molecule is found.
    

.. index:: LCNS

``LCNS``    type: ``integer array of size (NSTS)``    default: ``0``
    Contains the indices of Eirene non-standard surfaces (block 3A in input.dat) corresponding to core boundaries.
    

.. index:: LTNS

``LTNS``    type: ``integer array of size (NSTS)``    default: ``0``
    Contains the indices of Eirene non-standard surfaces (block 3A in input.dat) corresponding to target boundaries.
    

.. index:: LSNS

``LSNS``    type: ``integer array of size (NSTRAT*NSRFS)``    default: ``0``
    Contains the indices of Eirene surfaces related to the recycling sources.
    

.. index:: KSNS

``KSNS``    type: ``integer array of size (NSTRAT)``    default: ``0``
    Contains the number of Eirene surfaces for each Eirene recycling stratum.
    

.. index:: GPFC

``GPFC``    type: ``real array of size (NATM,NSTRAT)``    default: ``0.0``
    Specifies the fraction of Eirene atomic species (iatm) in one particle puffed from stratum (istra).
    

.. index:: DBG_EIR_MC

``DBG_EIR_MC``    type: ``integer``    default: ``0``
    Debug output control for eirene\_mc routine. See code for usage.
    

.. index:: DEBUG_FLAGS

``DEBUG_FLAGS``    type: ``integer array of size (100)``    default: ``0``
    Non-zero elements yield additional print-out data for debugging B2-Eirene coupling. See code for specific uses. Many slots still available for user-specific needs.
    If debug\_flags(81).gt.0, will print out target fluxes in files 'targb2.datv', 'targb2n.datv' and 'targb2pl.datv'.
    If debug\_flags(90).gt.0, will print output about Eirene non-standard surfaces [debug\_flags(90):debug\_flags(91)] and strata [debug\_flags(92):debug\_flags(93)] (0 means sum over all strata). Additional output can be obtained for strata [debug\_flags(94):debug\_flags(95)].
    If only debug\_flags(90) is specified, the output will include all individual Eirene strata, for all non-standard surfaces, starting from debug\_flags(90).
    

.. index:: NEUT_SCL_LIM

``NEUT_SCL_LIM``    type: ``real``    default: ``2.0``
    Maximum number by which Eirene neutral sources may be scaled in either direction within the ank-mods scheme. See explaining text in $SOLPSTOP/doc/Source\_Scaling\_in\_B2.pdf for details.
    

.. index:: TRACK_INDEX

``TRACK_INDEX``    type: ``integer array of size (0:NS-1)``    default: ``1 for species sput_dst, 0 for all others``
    Specifies the mixed material species index related to B2.5 species (is).
    

.. index:: TRACK_CHEM_SPUT

``TRACK_CHEM_SPUT``    type: ``logical array of size (NTRACK)``
    Indicates whether mixed material species (itrack) participates in chemical sputtering. Defaults to .true. for first tracked species if sput\_dst is carbon, and to .false. for all other cases.
    

.. index:: CHEMICAL_EROSION_REDEP_FAC

``CHEMICAL_EROSION_REDEP_FAC``    type: ``real``    default: ``1.0``
    Multiplier to the chemical sputtering coefficient of carbon for computing the rate used for redeposited carbon.
    

.. index:: CHEMICAL_EROSION_BE_FAC

``CHEMICAL_EROSION_BE_FAC``    type: ``logical``    default: ``.false.``
    Indicates whether the presence of beryllium is to impact on the chemical sputtering yield of carbon.
    

.. index:: CHEMICAL_EROSION_BE_FAC_A

``CHEMICAL_EROSION_BE_FAC_A``    type: ``real``    default: ``0.2``
    The chemical sputtering yield of carbon is multiplied by
    (1.0-C/2\*(tanh((frac-A)/B)-tanh((-A)/B)))
    where frac is the fractional content of Be in the surface layer material.
    

.. index:: CHEMICAL_EROSION_BE_FAC_B

``CHEMICAL_EROSION_BE_FAC_B``    type: ``real``    default: ``0.05``
    See above.
    

.. index:: CHEMICAL_EROSION_BE_FAC_C

``CHEMICAL_EROSION_BE_FAC_C``    type: ``real``    default: ``0.9``
    See above.
    

.. index:: N_SPCSRF

``N_SPCSRF``    type: ``integer``    default: ``0``
    Number of special surfaces groups for diagnostics.
    

.. index:: L_SPCSRF

``L_SPCSRF``    type: ``integer array of length (NLIM+NSTS)``    default: ``0``
    List of surface segments (non-default standard surfaces [NDSS] or additional surfaces in Eirene notation) included in the groups. Negative numbers correspond to NDSS.
    

.. index:: SPS_ID

``SPS_ID``    type: ``character*8 array of length (N_SPCSRF)``
    Labels of groups of special surfaces.
    

.. index:: I_SPCSRF

``I_SPCSRF``    type: ``integer array of length (N_SPCSRF)``    default: ``0``
    Index of the first Eirene surface belonging to a special surface group in the L\_SPCSRF list.
    

.. index:: J_SPCSRF

``J_SPCSRF``    type: ``integer array of length (N_SPCSRF)``    default: ``0``
    Index of the last Eirene surface belonging to a special surface group in the L\_SPCSRF list.
    

.. index:: SPS_ABSR

``SPS_ABSR``    type: ``real array of length (N_SPCSRF)``    default: ``-1.0``
    Particle absorption on the surface. If positive, will supercede the setting from the Eirene input file: RECYCT = 1-SPS\_ABSR. Ignored if negative.
    

.. index:: SPS_TRNO

``SPS_TRNO``    type: ``real array of length (N_SPCSRF)``    default: ``-1.0``
    Surface transparency in positive direction. If positive, will supercede the setting from the Eirene input file: TRANSP(1,) = SPS\_TRNO. Ignored if negative.
    

.. index:: SPS_TRNI

``SPS_TRNI``    type: ``real array of length (N_SPCSRF)``    default: ``-1.0``
    Surface transparency in negative direction. If positive, will supercede the setting from the Eirene input file: TRANSP(2,) = SPS\_TRNI. If negative, the setting from SPS\_TRNO is used.
    

.. index:: SPS_MTRI

``SPS_MTRI``    type: ``real array of length (N_SPCSRF)``    default: ``0``
    Surface material in Eirene notation (e.g., 1206 for C). If positive, will supercede the setting from the Eirene input file: ZNML = SPS\_MTRI. Ignored if negative.
    

.. index:: SPS_MTRL

``SPS_MTRL``    type: ``character*8 array of length (N_SPCSRF)``
    Surface material in human notation (e.g., 'C').
    

.. index:: SPS_TMPR

``SPS_TMPR``    type: ``real array of length (N_SPCSRF)``    default: ``1.e15``
    Surface temperature (in eV). If set larger to 1.e10, will be ignored. Otherwise, will supercede the setting from the Eirene input file: EWALL = SPS\_TMPR.
    

.. index:: SPS_SPPH

``SPS_SPPH``    type: ``real array of length (N_SPCSRF)``    default: ``-1.0``
    Fudge factor for physical sputtering. If positive, will supercede the setting from the Eirene input file: RECYCS = SPS\_SPPH. Ignored if negative.
    

.. index:: SPS_SPCH

``SPS_SPCH``    type: ``real array of length (N_SPCSRF)``    default: ``-1.0``
    Fudge factor for chemical sputtering. If positive, will supercede the setting from the Eirene input file: RECYCC = SPS\_SPCH. Ignored if negative.
    

.. index:: SPS_SGRP

``SPS_SGRP``    type: ``integer array of length (N_SPCSRF)``    default: ``-1``
    Sputtered particle species flag for chemical sputtering. If positive, will supercede the setting from the Eirene input file: ISRC = SPS\_SGRP. Ignored if negative.
    

.. index:: WRITE_NML_NEUT

``WRITE_NML_NEUT``    type: ``logical``    default: ``.true.``
    If .true. (default), writes the content of the namelist to stdout after it has been read.
    

.. index:: MAXPOIN

``MAXPOIN``    type: ``integer``    default: ``2000``
    Maximum number of points needed to describe a region contour in Eirene.
    

.. index:: TIME_DEP_PUFF

``TIME_DEP_PUFF``    type: ``logical array of length (NSTRAT)``    default: ``.false. for all strata``
    Indicates whether a stratum is a time-dependent gas puff. Should only be .true. for strata defined as gas puffs.
    

.. index:: TIME_DEP_PUFF_FUNC

``TIME_DEP_PUFF_FUNC``    type: ``logical array of length (NSTRAT)``    default: ``.false. for all strata``
    Indicates whether a stratum is using a time-dependent gas puff function. Should only be .true. for strata defined as gas puffs. For use with TIME\_DEP\_PUFF\_CASE and TIME\_DEP\_PUFF\_PARAM.
    

.. index:: TIME_DEP_PUFF_CASE

``TIME_DEP_PUFF_CASE``    type: ``integer array of length (NSTRAT)``    default: ``-1 for all strata``
    Used to select the functional form of the time-dependent gas puff function. For use with TIME\_DEP\_PUFF\_FUNC and TIME\_DEP\_PUFF\_PARAM.
    

.. index:: TIME_DEP_PUFF_PARAM

``TIME_DEP_PUFF_PARAM``    type: ``real array of length (NSTRAT)``    default: ``0 for all strata``
    Used to set the parameters for the functional form of the time-dependent gas puff function. For use with TIME\_DEP\_PUFF\_FUNC and TIME\_DEP\_PUFF\_CASE.
    

.. index:: NGPDATA

``NGPDATA``    type: ``integer data of size (NSTRAT)``    default: ``0``
    Number of points over which the time profile of the strength of gas puff (istra) is given. Defaults to 0. Current maximum value is 100.
    

.. index:: GPDATA

``GPDATA``    type: ``real data of size (NGPDATA,2,NSTRAT)``    default: ``0.0``
    For (i,ik,istra) in (1:NGPDATA(istra),1:2,1:NSTRAT),
    GPDATA(i,1,istra) contains the time point (i) for stratum (istra) (in s).
    GPDATA(i,2,istra) contains the gas puff strength of stratum (istra) at time point (i) (in particles/s).
    The gas puff strength before the first time point is given by USERFLUXPARM(istra,1).
    The gas puff strength after the last time point is given by the GPDATA value of the last time point.
    Otherwise, the gas puff strength is linearly interpolated from the given data.
    

.. index:: CHEMICAL_SPUTTER_YIELD

``CHEMICAL_SPUTTER_YIELD``    type: ``real array of size (0:NLIM+NSTS)``    default: ``0.0``
    Passed to Eirene. Chemical sputter yield of wall surface (ilim). Element 0 corresponds to the default setting for all surfaces.
    

.. index:: FCHAR_CHEMICAL

``FCHAR_CHEMICAL``    type: ``real``    default: ``0``
    Nuclear charge of atomic species causing the sputtering. If set to its default value of 0, then the chemical sputtering switches from this block are not used and the settings from the Eirene input file are used.
    

.. index:: IGASS_CHEMICAL

``IGASS_CHEMICAL``    type: ``integer``    default: ``0``
    Passed to Eirene. Eirene atomic species index of the sputtered particle. If igass\_chemical > natmi, the data from chemical\_sputter\_yield is not used and the yield from the Eirene surface blocks is used instead.
    

.. index:: ITSPUT_CHEMICAL

``ITSPUT_CHEMICAL``    type: ``integer``    default: ``0``
    Passed to Eirene. Eirene type index of the sputtered particle. Atoms = 1, Ions = 4. Defaults to 0, meaning 1 eV atom chemical sputtering.
    

.. index:: ISSPUT_CHEMICAL

``ISSPUT_CHEMICAL``    type: ``integer``    default: ``0``
    Passed to Eirene. Mass\*100 + nuclear charge of the sputtered particle. Defaults to 0, internally changed to 1206 = carbon.
    

.. index:: 
   single: b2.neutrals.parameters; NSTRAI
   single: b2.neutrals.parameters; RCPOS
   single: b2.neutrals.parameters; RCSTART
   single: b2.neutrals.parameters; RCEND
   single: b2.neutrals.parameters; RC_LIST_SIZE
   single: b2.neutrals.parameters; RC_LIST_X
   single: b2.neutrals.parameters; RC_LIST_Y
   single: b2.neutrals.parameters; TARGSP
   single: b2.neutrals.parameters; CHEMSP
   single: b2.neutrals.parameters; B2RECYC
   single: b2.neutrals.parameters; RECYC
   single: b2.neutrals.parameters; MRECYC
   single: b2.neutrals.parameters; ERECYC
   single: b2.neutrals.parameters; RCION
   single: b2.neutrals.parameters; RECYCEIR
   single: b2.neutrals.parameters; USERFLUXPARM
   single: b2.neutrals.parameters; CRCSTRA
   single: b2.neutrals.parameters; STRASCLFL
   single: b2.neutrals.parameters; SURF_MAT
   single: b2.neutrals.parameters; ACCEL_ION
   single: b2.neutrals.parameters; MAXW
   single: b2.neutrals.parameters; MOL
   single: b2.neutrals.parameters; HYB_TYPE
   single: b2.neutrals.parameters; E_FC
   single: b2.neutrals.parameters; RF_NEUT
   single: b2.neutrals.parameters; PHYS_SPUT
   single: b2.neutrals.parameters; CHEM_SPUT
   single: b2.neutrals.parameters; EIRENE_STEP_CPU
   single: b2.neutrals.parameters; EIRENE_STEP_DT
   single: b2.neutrals.parameters; EIRENE_MOD
   single: b2.neutrals.parameters; VOLRECSTART
   single: b2.neutrals.parameters; VOLRECINC
   single: b2.neutrals.parameters; VOLRECWT
   single: b2.neutrals.parameters; B2SPECIES_START
   single: b2.neutrals.parameters; B2SPECIES_END
   single: b2.neutrals.parameters; SPECIES_START
   single: b2.neutrals.parameters; SPECIES_END
   single: b2.neutrals.parameters; NEUTRALS_FILENAME
   single: b2.neutrals.parameters; NEUTRALS_TIME_MOD
   single: b2.neutrals.parameters; NEUTRALS_TIME_SWITCH
   single: b2.neutrals.parameters; L_NEUTRAD
   single: b2.neutrals.parameters; L_NEUTFLUX
   single: b2.neutrals.parameters; LSTRASCL
   single: b2.neutrals.parameters; B2EATCR
   single: b2.neutrals.parameters; B2ESPCR
   single: b2.neutrals.parameters; EB2ATCR
   single: b2.neutrals.parameters; EB2SPCR
   single: b2.neutrals.parameters; LATMSCL
   single: b2.neutrals.parameters; LMOLSCL
   single: b2.neutrals.parameters; MLCMP
   single: b2.neutrals.parameters; LIONSCL
   single: b2.neutrals.parameters; LCNS
   single: b2.neutrals.parameters; LTNS
   single: b2.neutrals.parameters; LSNS
   single: b2.neutrals.parameters; KSNS
   single: b2.neutrals.parameters; GPFC
   single: b2.neutrals.parameters; DBG_EIR_MC
   single: b2.neutrals.parameters; DEBUG_FLAGS
   single: b2.neutrals.parameters; NEUT_SCL_LIM
   single: b2.neutrals.parameters; TRACK_INDEX
   single: b2.neutrals.parameters; TRACK_CHEM_SPUT
   single: b2.neutrals.parameters; CHEMICAL_EROSION_REDEP_FAC
   single: b2.neutrals.parameters; CHEMICAL_EROSION_BE_FAC
   single: b2.neutrals.parameters; CHEMICAL_EROSION_BE_FAC_A
   single: b2.neutrals.parameters; CHEMICAL_EROSION_BE_FAC_B
   single: b2.neutrals.parameters; CHEMICAL_EROSION_BE_FAC_C
   single: b2.neutrals.parameters; N_SPCSRF
   single: b2.neutrals.parameters; L_SPCSRF
   single: b2.neutrals.parameters; SPS_ID
   single: b2.neutrals.parameters; I_SPCSRF
   single: b2.neutrals.parameters; J_SPCSRF
   single: b2.neutrals.parameters; SPS_ABSR
   single: b2.neutrals.parameters; SPS_TRNO
   single: b2.neutrals.parameters; SPS_TRNI
   single: b2.neutrals.parameters; SPS_MTRI
   single: b2.neutrals.parameters; SPS_MTRL
   single: b2.neutrals.parameters; SPS_TMPR
   single: b2.neutrals.parameters; SPS_SPPH
   single: b2.neutrals.parameters; SPS_SPCH
   single: b2.neutrals.parameters; SPS_SGRP
   single: b2.neutrals.parameters; WRITE_NML_NEUT
   single: b2.neutrals.parameters; MAXPOIN
   single: b2.neutrals.parameters; TIME_DEP_PUFF
   single: b2.neutrals.parameters; TIME_DEP_PUFF_FUNC
   single: b2.neutrals.parameters; TIME_DEP_PUFF_CASE
   single: b2.neutrals.parameters; TIME_DEP_PUFF_PARAM
   single: b2.neutrals.parameters; NGPDATA
   single: b2.neutrals.parameters; GPDATA
   single: b2.neutrals.parameters; CHEMICAL_SPUTTER_YIELD
   single: b2.neutrals.parameters; FCHAR_CHEMICAL
   single: b2.neutrals.parameters; IGASS_CHEMICAL
   single: b2.neutrals.parameters; ITSPUT_CHEMICAL
   single: b2.neutrals.parameters; ISSPUT_CHEMICAL

.. index:: b2.wall_save.parameters

b2.wall_save.parameters
=======================
.. index:: NDEPTH_NML

``NDEPTH_NML``    type: ``integer``    default: ``1``
    Dimension NDEPTH used for the arrays within this namelist. Represents the number of depth layer discretising the wall elements for the wall model. If using the 0-D model or the time-independent 1-D model, will contain 1 (default). Should not exceed the value of the parameter NDEPTH declared in b2mod\_wall.F.
    

.. index:: IMAPX

``IMAPX``    type: ``integer array of size (NWALL)``
    Indicates the (ix) position in the grid of wall element (iwall). Default ordering of the wall elements proceeds clockwise in physical space from the lower left corner.
    

.. index:: IMAPY

``IMAPY``    type: ``integer array of size (NWALL)``
    Indicates the (iy) position in the grid of wall element (iwall). Default ordering of the wall elements proceeds clockwise in physical space from the lower left corner.
    

.. index:: XYMAP

``XYMAP``    type: ``integer array of size (-1:NX,-1:NY)``
    XYMAP(ix,iy) contains the wall index (iwall) of the wall element located a grid locaion (ix,iy). If there is no wall element at this position, contains 0.
    Default ordering of the wall elements proceeds clockwise in physical space from the lower left corner.
    

.. index:: SURFACE_MATERIAL_NAME

``SURFACE_MATERIAL_NAME``    type: ``character*6 of size (NWALL)``    default: ``C``
    Contains the filename from which to extract the surface material properties for wall element (iwall). The files are to be found in $SOLPSTOP/data.local/Surface\_properties/ or $SOLPSTOP/modules/B2.5/Database/Surface\_properties/.
    

.. index:: COATING_MATERIAL_NAME

``COATING_MATERIAL_NAME``    type: ``character*6 of size (NWALL)``    default: `` ``
    Contains the filename from which to extract the bulk material properties of the eventual coating for wall element (iwall).
    

.. index:: BULK_MATERIAL_NAME

``BULK_MATERIAL_NAME``    type: ``character*6 of size (NWALL)``    default: ``C``
    Contains the filename from which to extract the bulk material properties for wall element (iwall). The files are to be found in $SOLPSTOP/data.local/Bulk\_properties/ or $SOLPSTOP/modules/B2.5/Database/Bulk\_properties/.
    

.. index:: LAYER_ALLOYS

``LAYER_ALLOYS``    type: ``character*6 of size (NALLOYS)``
    Contains the filename from which to extract the material properties for alloy (nalloy) which may be present in mixed materials deposited layers. Not yet operational. The files are to be found in $SOLPSTOP/data.local/Bulk\_properties/, $SOLPSTOP/data.local/Surface\_properties/, $SOLPSTOP/modules/B2.5/Database/Surface\_properties/, or $SOLPSTOP/modules/B2.5/Database/Bulk\_properties/.
    

.. index:: TARGET_TEMP

``TARGET_TEMP``    type: ``real array of size (NWALL,NDEPTH)``
    Contains the temperature (in Kelvin) of wall element (iwall) at depth layer (idepth).
    If plate\_option.eq.1, will be set to backplate\_temp(iwall).
    If plate\_option.eq.2 and empty, will be set to equilibrium 1-D profile deduced from plasma incoming fluxes.
    If plate-option.eq.3, must be set.
    

.. index:: INERTIAL_COOLING

``INERTIAL_COOLING``    type: ``logical array of size (NWALL)``    default: ``.false.``
    Indicates whether wall element (iwall) is inertially cooled instead of actively cooled.
    

.. index:: BACKPLATE_TEMP

``BACKPLATE_TEMP``    type: ``real array of size (NWALL)``    default: ``b2stbr_plate_temp``
    Contains the temperature (in Kelvin) maintained by cooling at the back end of wall element (iwall).
    

.. index:: PLATE_THICKNESS

``PLATE_THICKNESS``    type: ``real array of size (NWALL)``    default: ``b2stbr_plate_thick``
    Contains the thickness (in metres) of wall element (iwall).
    

.. index:: COATING_THICKNESS

``COATING_THICKNESS``    type: ``real array of size (NWALL)``    default: ``0``
    Contains the thickness (in metres) of the eventual coating on wall element (iwall).
    

.. index:: PLATE_TIME_FACTOR

``PLATE_TIME_FACTOR``    type: ``real array of size (NWALL)``    default: ``1.0``
    Multiplier to the time for the equations for temperature and composition evolution of wall element (iwall).
    

.. index:: DEPOSITION

``DEPOSITION``    type: ``real array of size (NWALL,NTRACK)``    default: ``0.0``
    Contains the amount of deposited material (in atoms) from species (itrack) onto wall element (iwall).
    

.. index:: EROSION

``EROSION``    type: ``real array of size(NWALL,NTRACK)``    default: ``0.0``
    Contains the amount of eroded material (in atoms) of species (itrack) from wall element(iwall).
    

.. index:: CHEMICAL_SPUTTERING

``CHEMICAL_SPUTTERING``    type: ``real array of size (NWALL,0:NS-1)``    default: ``0.0``
    Contains the chemical sputter yield of 'sput\_dst' or 'sput\_dst\_bulk' species on wall element (iwall) caused by B2.5 species (is).
    

.. index:: PHYSICAL_SPUTTERING

``PHYSICAL_SPUTTERING``    type: ``real array of size (NWALL,0:NS-1)``    default: ``0.0``
    Contains the physical sputter yield of 'sput\_dst' or 'sput\_dst\_bulk' species on wall element (iwall) caused by B2.5 species (is).
    

.. index:: PHYSICAL_SPUTTERING_ENERGY

``PHYSICAL_SPUTTERING_ENERGY``    type: ``real array of size (NWALL,0:NS-1)``    default: ``0.0``
    Contains the fraction of returned energy carried by sputtered particles of species 'sput\_dst' or 'sput\_dst\_bulk' species from wall element (iwall) caused by B2.5 species (is).
    

.. index:: RES_SPUTTERING

``RES_SPUTTERING``    type: ``real array of size (NWALL,0:NS-1)``    default: ``0.0``
    Contains the RES sputter yield of 'sput\_dst' or 'sput\_dst\_bulk' species on wall element (iwall) caused by B2.5 species (is).
    

.. index:: THERMAL_EVAPORATION

``THERMAL_EVAPORATION``    type: ``real array of size(NWALL,0:NS-1)``    default: ``0.0``
    Contains the rate of thermal evaporation of species (is) (in particles/second) from wall element (iwall).
    

.. index:: BACKSCATTERING

``BACKSCATTERING``    type: ``real array of size (NWALL,0:NS-1)``    default: ``0.0``
    Contains the backscattering fraction for incoming B2.5 species (is) onto wall element (iwall).
    

.. index:: BACKSCATTERING_ENERGY

``BACKSCATTERING_ENERGY``    type: ``real array of size (NWALL,0:NS-1)``    default: ``0.0``
    Contains the backscattered energy fraction for incoming B2.5 species (is) onto wall element (iwall).
    

.. index:: PLATE_TIME

``PLATE_TIME``    type: ``real array of size (NWALL)``    default: ``0.0``
    Indicates how much simulation time has elapsed for wall element (iwall) (in seconds).
    

.. index:: PLATE_AREA

``PLATE_AREA``    type: ``real array of size (NWALL)``
    Indicates the wall area (in square metres) for wall element (iwall). Defaults to the area computed from the B2.5 grid information.
    

.. index:: MONOLAYER_DEPOSITION

``MONOLAYER_DEPOSITION``    type: ``real array of size (NWALL,NTRACK)``    default: ``0.0``
    Contains the amount of deposited material (in monolayers) from species (itrack) onto wall element (iwall).
    

.. index:: MONOLAYER_EROSION

``MONOLAYER_EROSION``    type: ``real array of size (NWALL,NTRACK)``    default: ``0.0``
    Contains the amount of eroded material (in monolayers) of species (itrack) from wall element (iwall).
    

.. index:: LAYER_NCONSTITUENTS

``LAYER_NCONSTITUENTS``    type: ``integer array of size (NWALL)``    default: ``1``
    Indicates the number of elemental constituents within the surface layer of wall element (NWALL).
    

.. index:: LAYER_NZCONSTITUENTS

``LAYER_NZCONSTITUENTS``    type: ``integer array of size (NWALL,6+NTRACK)``
    Contains the atomic numbers Z of the various elements present within the surface layer of wall element (iwall). Defaults to 6 for the first value, 0 otherwise.
    

.. index:: LAYER_RELCONSTITUENTS

``LAYER_RELCONSTITUENTS``    type: ``real array of size (NWALL,6+NTRACK)``
    Contains the relative atomic abundances of the various elements present within the surface layer of wall element (iwall). Defaults to 1.0 for the first value, 0.0 otherwise.
    Replaces LAYER\_NRELCONSTITUENTS.
    

.. index:: 
   single: b2.wall_save.parameters; NDEPTH_NML
   single: b2.wall_save.parameters; IMAPX
   single: b2.wall_save.parameters; IMAPY
   single: b2.wall_save.parameters; XYMAP
   single: b2.wall_save.parameters; SURFACE_MATERIAL_NAME
   single: b2.wall_save.parameters; COATING_MATERIAL_NAME
   single: b2.wall_save.parameters; BULK_MATERIAL_NAME
   single: b2.wall_save.parameters; LAYER_ALLOYS
   single: b2.wall_save.parameters; TARGET_TEMP
   single: b2.wall_save.parameters; INERTIAL_COOLING
   single: b2.wall_save.parameters; BACKPLATE_TEMP
   single: b2.wall_save.parameters; PLATE_THICKNESS
   single: b2.wall_save.parameters; COATING_THICKNESS
   single: b2.wall_save.parameters; PLATE_TIME_FACTOR
   single: b2.wall_save.parameters; DEPOSITION
   single: b2.wall_save.parameters; EROSION
   single: b2.wall_save.parameters; CHEMICAL_SPUTTERING
   single: b2.wall_save.parameters; PHYSICAL_SPUTTERING
   single: b2.wall_save.parameters; PHYSICAL_SPUTTERING_ENERGY
   single: b2.wall_save.parameters; RES_SPUTTERING
   single: b2.wall_save.parameters; THERMAL_EVAPORATION
   single: b2.wall_save.parameters; BACKSCATTERING
   single: b2.wall_save.parameters; BACKSCATTERING_ENERGY
   single: b2.wall_save.parameters; PLATE_TIME
   single: b2.wall_save.parameters; PLATE_AREA
   single: b2.wall_save.parameters; MONOLAYER_DEPOSITION
   single: b2.wall_save.parameters; MONOLAYER_EROSION
   single: b2.wall_save.parameters; LAYER_NCONSTITUENTS
   single: b2.wall_save.parameters; LAYER_NZCONSTITUENTS
   single: b2.wall_save.parameters; LAYER_RELCONSTITUENTS

.. index:: b2md.dat

b2md.dat
========
.. index:: EXP

``EXP``    type: ``character*128``    default: ``NOT_SET``
    Name of the experiment being modelled.
    

.. index:: SHOT

``SHOT``    type: ``integer``
    Shot number identifying the run. Defaults to the last number found in shotnumber.history, or 0 if the file is not found.
    

.. index:: TIME

``TIME``    type: ``real``    default: ``0.0``
    Time point of the experimental shot being simulated.
    

.. index:: COMMENT

``COMMENT``    type: ``character*128``    default: ``NOT_SET``
    Label for the run.
    

.. index:: TIMEDEP

``TIMEDEP``    type: ``logical``
    If .true. (default), saves data from b2time.nc.
    

.. index:: SNAPSHOT

``SNAPSHOT``    type: ``logical``
    If .true. (default), saves data from b2fplasma.
    

.. index:: TALLIES

``TALLIES``    type: ``logical``
    If .true. (default), saves data from b2tallies.nc.
    

.. index:: MOVIES

``MOVIES``    type: ``logical``
    If .true. (default), saves data from b2movies.nc.
    

.. index:: OVERWRITE_SHOTNUMBER

``OVERWRITE_SHOTNUMBER``    type: ``integer``
    Indicate the shot number to overwrite (to be used only when updating an already saved run with 'resave\_mds' script).
    Defaults to the last number found in shotnumber.history, or 0 if the file is not found.
    

.. index:: 
   single: b2md.dat; EXP
   single: b2md.dat; SHOT
   single: b2md.dat; TIME
   single: b2md.dat; COMMENT
   single: b2md.dat; TIMEDEP
   single: b2md.dat; SNAPSHOT
   single: b2md.dat; TALLIES
   single: b2md.dat; MOVIES
   single: b2md.dat; OVERWRITE_SHOTNUMBER

.. index:: b2.boundary.parameters

b2.boundary.parameters
======================
.. index:: NBC

``NBC``    type: ``integer``    default: ``0``
    Number of boundary segments.

.. index:: BCCHAR

``BCCHAR``    type: ``character*1 array of length (NBC)``    default: `` ``
    In the WG code, BCHAR is always equal to 'A' (automatic) and a boundary list is defined by the mesh boundary faces that have fcLbl.ge.BCSTART and fcLbl.le.BCEND.
    

.. index:: CONPAR

``CONPAR``    type: ``real array of size (0:NS-1,NBC,3)``    default: ``0.0``
    Contains parameters helping to define the boundary conditions for the continuity equation of species (is). See description of BCCON below for details.
    

.. index:: MOMPAR

``MOMPAR``    type: ``real array of size (0:NS-1,NBC,2)``    default: ``0.0``
    Contains parameters helping to define the boundary conditions for the parallel momentum equation of species (is). See description of BCMOM below for details.
    

.. index:: ENEPAR

``ENEPAR``    type: ``real array of size (NBC,2)``    default: ``0.0``
    Contains parameters helping to define the boundary conditions for the electron energy equation. See description of BCENE below for details.
    

.. index:: ENIPAR

``ENIPAR``    type: ``real array of size (NBC,2)``    default: ``0.0``
    Contains parameters helping to define the boundary conditions for the ion energy equation. See description of BCENI below for details.
    

.. index:: POTPAR

``POTPAR``    type: ``real array of size (NBC,2)``    default: ``0.0``
    Contains parameters helping to define the boundary conditions for the potential equation. See description of BCPOT below for details.
    

.. index:: BCPOS

``BCPOS``    type: ``integer array, length (NBC)``    default: ``-2``
    For North, South or X boundary conditions, it specifies the row index; for West, East and Y boundary conditions, it specifies the column index. Obsolete for WG.
    

.. index:: BCSTART

``BCSTART``    type: ``integer array, length (NBC)``    default: ``-2``
    Starting label index (fcLbl) of the cells belonging to this boundary condition.
    

.. index:: BCEND

``BCEND``    type: ``integer array, length (NBC)``    default: ``-2``
    Ending label index (fcLbl) of the cells belonging to this boundary condition.
    

.. index:: BC_LIST_SIZE

``BC_LIST_SIZE``    type: ``integer array of length (NBC)``    default: ``0``
    Contains the size of the list of cells where a boundary condition is applied.
    

.. index:: BC_LIST_X

``BC_LIST_X``    type: ``integer array of length (2*(NXD+NYD),NBC)``    default: ``-2``
    Contains the X-coordinate of the cells where boundaries conditions are applied. Obsolete for WG.
    

.. index:: BC_LIST_Y

``BC_LIST_Y``    type: ``integer array of length (2*(NXD+NYD),NBC)``    default: ``-2``
    Contains the Y-coordinate of the cells where boundaries conditions are applied. Obsolete for WG.
    

.. index:: BCCON

``BCCON``    type: ``integer array, length (0:NS-1,NBC)``
    Specifying the type of density boundary condition for each segment and species (fastest varying index is species); makes use of CONPAR to specify additional information, as indicated:
    0 : default, no boundary condition is applied
    1 : prescribe the value of the density, CONPAR(,,1) specifies the required density in m^-3`
    2 : prescribe the gradient of the density, CONPAR(,,1) specifies the required density gradient in m^-4`
    3 : sheath conditions, CONPAR(,,1) not used (zero gradient is used)
    4 : prescribe the value of the density, weakly a mixed boundary condition, CONPAR(,,1) specifies the required density in m^-3` and CONPAR(,,2) specifies the 'strength' of the boundary condition.
    5 : prescribe the particle flux per unit area, CONPAR(,,1) specifies the required particle flux density in m^-2`.s.s^-1`
    6 : prescribe the total particle flux for a constant density, CONPAR(,,1) specifies the particle flux in s^-1`.. Not yet available for WG.
    7 : prescribe the given profile of density from the bv\_na.dat file (requires b2mndr\_boundary\_sources.eq.1)
    8 : prescribe the total particle flux with constant flux density, CONPAR(,,1) specifies the particle flux in s^-1`
    9 : prescribe the decay length for the density, CONPAR(,,1) specifies the gradient length in metres (should use type 15 instead when drifts are turned on)
    10 : leakage option for density, recommended for cases with drifts, CONPAR(,,1) specifies the leakage factor, α in Γ`_loss` = α C`_s` n`_a`,, CONPAR(,,2)>0 is the stabilizing factor which may be needed if drifts are activated.
    11 : should not be used for feedbacks anymore, not converted to WG code.
    12 : should not be used for feedbacks anymore, not converted to WG code.
    13 : particle density to achieve specified total flux, CONPAR(,,1) is the specified flux crossing the boundary flux surface, CONPAR(,,2) is the strength of the feedback (if left zero, b2stbc\_bc\_ref will be used), CONPAR(,,3), when running with Eirene and the 'ionising core' switch is used, is set internally to match the re-entering flux of ionised neutrals that crossed the core boundary (one must then have 'ionising\_core'.eq.-IB where IB is the boundary index).
    14 : sound speed velocity flux, CONPAR(,,1) is a multiplier to the outgoing sound speed C`_s`.. To be used in conjunction with BCENE/I=15, BCPOT=11, and BCMOM=13. Recommended for cases with drifts. If CONPAR(,,2).gt.0, an additional decay-length loss is added, where CONPAR(,,2) is the decay length.
    15 : prescribe a radial leakage velocity, CONPAR(,,1) specifies the leakage velocity in units of the local thermal velocity.
    16 : particle density to achieve specified total flux, used with ASTRA coupling. The total desired flux is summed over all BCCON=16 core boundaries. CONPAR(,,1) specifies the desired particle flux in s^-1`.. CONPAR(,,2) is the strength of the feedback (if left zero, b2stbc\_bc\_ref will be used).
    18 : prescribe total main ion particle flux, used with ASTRA coupling. Not yet available for WG.
    19 : particle flux feedback boundary condition, flux is summed over neutrals and ions, for coupling with ASTRA. The total desired flux is summed over all BCCON=19 core boundaries. This boundary condition type is applied to ions in their highest ionisation stage. CONPAR(,,1) specifies the desired particle flux in s^-1`.. CONPAR(,,2) is the strength of the feedback (if left zero, b2stbc\_bc\_ref will be used).
    20 : constant density feedback condition, CONPAR(,,1) specifies the desired density in m^-3`.. Not yet available for WG.
    21 : prescribe the value of the density and add a poloidal density variation to get a solution which is as close as possible to neoclassical theory. It is recommended to use this boundary condition together with corresponding condition on ion temperature (BCENI=24). The total desired density is summed over all BCCON=21 core boundaries. CONPAR(,,1) specifies the desired density in m^-3`..
    22 : feedback boundary condition: given total particle flux with constant average density. The poloidal density variation is added to make the solution as close as possible to the neoclassical value derived for pure H/D/T plasma. It is recommended to use this boundary condition with corresponding boundary condition on ion temperature (BCENI=23,24). The total desired flux is summed over all BCCON=22 core boundaries. CONPAR(,,1) specifies the desired particle flux in s^-1`.. CONPAR(,,2) is the strength of the feedback (if left zero, b2stbc\_bc\_ref will be used).
    23 : feedback boundary condition: given sum of integrated neutrals and main ion particle fluxes with constant average density. The poloidal density variation is added to make the solution as close as possible to the neoclassical value derived for pure H/D/T plasma. It is recommended to use this boundary condition with corresponding boundary condition on ion temperature (BCENI=23,24). The total desired flux is summed over all BCCON=23 core boundaries. CONPAR(,,1) specifies the desired particle flux in s^-1`.. CONPAR(,,2) is the strength of the feedback (if left zero, b2stbc\_bc\_ref will be used).
    24 : constant density feedback scaled by density on the ring 'bc\_type21\_ref' away. CONPAR(,,1) specifies the desired density in m^-3`.. CONPAR(,,2) is the strength of the feedback (if left zero, b2stbc\_bc\_ref will be used). Not yet available for WG.
    25 : feedback boundary condition: prescribe the average value of the density and add the poloidal density variation from the neighbouring radial ring. This boundary condition is suitable for any species of a multi-species plasma (i.e. in the case when the condition used in BCCON=21 fails). It is recommended to use this boundary condition together with the corresponding condition on ion temperature (BCENI=26,27). CONPAR(,,1) specifies the desired average density in m^-3`..
    26 : feedback boundary condition: prescribe the total ion flux and find the average density. The poloidal density variation from the neighbouring radial ring is applied on top of the average density. This boundary condition is suitable for any species of a multi-species plasma (i.e. in the case when the condition used in BCCON=22 fails). It is recommended to use this boundary condition together with a corresponding condition on the ion temperature (BCENI=26,27). The total desired flux is summed over all BCCON=26 core boundaries. CONPAR(,,1) specifies the desired particle flux in s^-1`.. CONPAR(,,2) is the strength of the feedback (if left zero, b2stbc\_bc\_ref will be used).
    27 : feedback boundary condition: prescribe the particle flux sum for all neutrals and ions belonging to a given isonuclear sequence and find the average density. The poloidal density variation from the neighbouring radial ring is applied on top of the average density. It is recommended to use this boundary condition together with corresponding condition on ion temperature (BCENI=25,26). The total desired flux is summed over all BCCON=27 core boundaries. CONPAR(,,1) specifies the desired particle flux in s^-1`.. CONPAR(,,2) is the strength of the feedback (if left zero, b2stbc\_bc\_ref will be used).
    28 : Prescribe the flux surface averaged density, with a poloidal perturbation taken from the flux tube just inside the domain. Only intended for core boundaries. CONPAR(,,1) specifies the desired average density in m^-3`..
    29 : Feedback on the total particle flux, by imposing a flux surface averaged density, with a poloidal perturbation taken from the flux tube just inside the domain. CONPAR(,,1) specifies the desired particle flux in s^-1`.. CONPAR(,,2) is the strength of the feedback (if left zero, b2stbc\_bc\_ref will be used). Intended for core boundaries only.
    

.. index:: BCMOM

``BCMOM``    type: ``integer array, length NS * NBC``
    Specifying the type of parallel momentum or velocity boundary condition for each segment and species (fastest varying index is species); makes use of MOMPAR to specify additional information, as indicated
    0 : default, no boundary condition is applied
    1 : prescribe the value of the parallel velocity, MOMPAR(,,1) specifies the parallel velocity in m.s^-1`
    2 : prescribe the gradient of the parallel velocity, MOMPAR(,,1) specifies the parallel velocity gradient in s^-1`
    3 : sheath conditions, Mach number as input, if MOMPAR(,,2) < 0.5, then the velocity is set to exactly MOMPAR(,,1) \* C`_s,collective`,, otherwise the velocity is set to be at least MOMPAR(,,1) \* C`_s,a`,, the thermal velocity of that species. BCMOM = 3 was not adapted for WG. Replace with drift-compatible BCMOM = 13.
    4 : prescribe the value of the velocity, weakly a mixed boundary condition, MOMPAR(,,1) specifies the parallel velocity in m.s^-1` and MOMPAR(,,2) specifies the 'strength' of the boundary condition.
    5 : prescribe the parallel momentum flux per unit area, MOMPAR(,,1) specifies the parallel momentum flux density in N.m^-2`
    6 : prescribe the total parallel momentum flux for a constant parallel velocity [not yet available]
    7 : prescribe the given profile of parallel velocity from the bv\_ua.dat file (requires b2mndr\_boundary\_sources.eq.1)
    8 : special : limited shear, imposes zero gradient for the Mach number. [[[Eventually intended to have MOMPAR(,,1) specify the gradient of the Mach number in m^-1`]]].]]].
    9 : prescribe the total parallel momentum flux with constant flux density, MOMPAR(,,1) specifies the parallel momentum flux in N.
    10 : prescribe the decay length for the parallel momentum, MOMPAR(,,1) specifies the decay length in m.
    11 : Rozhansky viscosity condition for the parallel momentum, MOMPAR(,,1) is not used. Not yet available for WG.
    12 : condition from b2stbc\_spb for the parallel momentum.
    13 : drift-compatible sheath boundary condition for the parallel momentum. To be used in conjunction with BCENE/I=15, BCPOT=11, and BCCON=14. Recommended for cases with drifts.
    14 : condition from b2stbc\_spb for the parallel momentum
    15 : prescribe the value of the parallel velocity, scaled with B\_average/B\_local. Not yet available for WG.
    16 : prescribe the average value of the parallel velocity MOMPAR(,,1) specifies the parallel velocity in m.s^-1`
    17 : leakage option for parallel momentum, MOMPAR(,,1) specifies the leakage factor, α in Γ`_loss` = α C`_s,a` m`_a` n`_a` u`_a`
    18 : explicitly enforce zero source terms, resulting in zero flux.
    

.. index:: BCENE

``BCENE``    type: ``integer array, length NBC``
    Specifying the type of electron energy or temperature boundary condition for each segment; makes use of ENEPAR to specify additional information, as indicated
    0 : default, no boundary condition is applied
    1 : prescribe the value of the electron temperature, ENEPAR(,1) specifies the temperature in eV
    2 : prescribe the gradient of the electron temperature, ENEPAR(,1) specifies the temperature gradient in eV.m^-1`
    3 : sheath conditions, electron energy transmission, ENEPAR(,1) specifies an additional contribution to the energy transmission coefficient in addition to that of the potential difference [the sound speed used depends on settings of MOMPAR(,ISMAIN,2)]. BCENE = 3 not adapted for WG. Replace with drift-compatible BCENE = 15.
    4 : prescribe the value of the electron temperature, weakly a mixed boundary condition, ENEPAR(,1) specifies the temperature in eV and ENEPAR(,2) specifies the 'strength' of the boundary condition.
    5 : prescribe the electron energy flux per unit area, ENEPAR(,1) specifies the energy flux density in W.m^-2`..
    6 : prescribe the total electron energy flux for a constant electron temperature, ENEPAR(,1) specifies the energy flux in W (no longer supported, use types [16] or [17] instead).
    7 : prescribe the electron temperature profile from the bv\_te.dat file (requires b2mndr\_boundary\_sources.eq.1).
    8 : prescribe the total electron heat flux with constant flux density, ENEPAR(,1) specifies the energy flux in W.
    9 : prescribe the decay length for the electron temperature, ENEPAR(,1) specifies the decay length in m (can also use type [19] instead).
    10 : should not be used for feedbacks anymore, not converted to WG code.
    11 : not used
    12 : sheath conditions, electron energy transmission coefficient, ENEPAR(,1) specifies an energy transmission factor, delta`_e` in Q`_e` = delta`_e` Γ`_e` T`_e`.. Obsolete. Replace with drift-compatible BCENE = 15.
    13 : prescribe the electron energy flux per unit area proportional to temperature, ENEPAR(,1) specifies the energy flux density per temperature in W.m^-2`.J.J^-1` (the temperature here in J).
    14 : leakage option for electron energy, ENEPAR(,1) specifies the leakage factor, α in Γ`_loss` = α C`_s`,, collective n`_e` T`_e`.. The energy loss also includes an electrostatic term as α ENEPAR(,2) C`_s`,collective,collective e Φ n`_e`..
    15 : sheath boundary condition, recommended when using drifts (see Section C.9.4 of manual for details). Linked to using BCCON=14 and BCMOM=13 for all ion species, BCENI=15, and BCPOT=11.
    16 : feedback boundary condition with constant temperature, ENEPAR(,1) specifies the power flux in W across the core boundary, ENEPAR(,2) should be something like 0.1 and specifies the strength of the feedback (if left zero, b2stbc\_bc\_ref\_te will be used). Also see type [17] below. Available if bcene\_16\_style=0 (default). If bcene\_16\_style=1, integrated electron heat flux with constant electron temperature, summed over all core boundaries with BCENE=16.
    17 : feedback boundary condition with constant shared temperature for both electrons and ions, with ENEPAR(,1) + ENIPAR(,1) giving the total power flux in W across the core boundary, ENEPAR(,2) should be something like 0.1 and specifies the strength of the feedback. Recommended to replace [16] for high densities.
    18 : fractional drop condition. Experimental. Attempts to set the guard cell temperature to be (1 - ENEPAR(,1)) times the boundary cell temperature.
    19 : same as [9] but to be used when simultaneously setting BCCON=1 on the same boundary. Not yet available for WG.
    20 : feedback boundary condition with constant temperature, as per type [16] but with a different feedback scheme. ENEPAR(,2) is the strength of the feedback (if left zero, b2stbc\_bc\_ref\_te is used).
    21 : constant temperature feedback scaled by temperature. ENEPAR(,1) specifies the desired electron temperature in eV. ENEPAR(,2) is the strength of the feedback (if left zero, b2stbc\_bc\_ref\_te is used).
    22 : radial leakage condition for the electron temperature. ENEPAR(,1) specifies the leakage velocity in units of the electron thermal velocity. A temperature gradient such that the diffusive flux is set to match this leakage is imposed.
    23 : prescribe the value of the electron temperature, with a poloidal perturbation taken from the flux tube just inside the domain. Intended only for core boundaries. ENEPAR(,1) specifies the desired average electron temperature in eV.
    24 : feedback on the total electron energy flux, by imposing a flux surface averaged temperature, with a poloidal perturbation taken from the flux tube just inside the domain. Intended only for core boundaries. ENEPAR(,1) specifies the energy flux in W. ENEPAR(,2) specifies the strength of the feedback (if left zero, b2stbc\_bc\_ref\_te will be used).
    

.. index:: BCENI

``BCENI``    type: ``integer array, length NBC``
    Specifying the type of ion energy or temperature boundary condition for each segment; makes use of ENIPAR to specify additional information, as indicated
    0 : default, no boundary condition is applied
    1 : prescribe the value of the ion temperature, ENIPAR(,1) specifies the temperature in eV
    2 : prescribe the gradient of the ion temperature, ENIPAR(,1) specifies the temperature gradient in eV.m^-1`
    3 : sheath conditions, ion energy transmission, ENIPAR(,1) specifies the contribution to the energy transmission coefficient [the sound speed used depends on settings of MOMPAR(,ISMAIN,2)]. BCENI = 3 not adapted for WG. Replace with drift-compatible BCENI = 15.
    4 : prescribe the value of the ion temperature, weakly a mixed boundary condition, ENIPAR(,1) specifies the temperature in eV and ENIPAR(,2) specifies the 'strength' of the boundary condition.
    5 : prescribe the ion energy flux per unit area, ENIPAR(,1) specifies the energy flux density in W.m^-2`..
    6 : prescribe the total ion energy flux for a constant ion temperature, ENIPAR(,1) specifies the energy flux in W (no longer supported, use types [16] or [17] instead)
    7 : prescribe the ion temperature profile from the bv\_ti.dat file (requires b2mndr\_boundary\_sources.eq.1)
    8 : prescribe the total ion heat flux with constant flux density, ENIPAR(,1) specifies the energy flux in W
    9 : prescribe the decay length for the ion temperature, ENIPAR(,1) specifies the decay length in m (can also use type [19] instead)
    10 : should not be used for feedbacks anymore, not converted to WG code.
    11 : sheath conditions, ion energy transmission coefficient, ENIPAR(,1) specifies an energy transmission factor, delta`_i` in Q`_i` = delta`_i` T`_i` sum`_a` n`_a` C`_s,a`.. Not yet available for WG.
    12 : sheath conditions, ion energy transmission coefficient, ENIPAR(,1) specifies an energy transmission factor, delta`_i` in Q`_i` = delta`_i` T`_i` sum`_a` Γ`_a`.. Obsolete. Replace with drift-compatible BCENI = 15.
    13 : prescribe the ion energy flux per unit area proportional to temperature, ENIPAR(,1) specifies the energy flux density per temperature in W.m^-2`.J.J^-1` (the temperature here in J).
    14 : leakage option for ion energy, ENIPAR(,1) specifies the leakage factor, α in Γ`_loss` = α C`_s`TT`_i`..
    15 : sheath boundary condition, recommended when using drifts (see Section C.9.5 of manual for details). Linked to using BCCON=14 and BCMOM=13 for all ion species, along with BCENE=15 and BCPOT=11.
    16 : feedback boundary condition with constant temperature, ENIPAR(,1) specifies the power flux in W across the flux surface with index 'b2stbc\_type16\_ref' (default=-1), ENIPAR(,2) should be something like 0.1 and specifies the strength of the feedback (if left zero, b2stbc\_bc\_ref\_ti will be used). Also see type [17] below. Available if bceni\_16\_style=0 (default). If bceni\_16\_style=1, integrated ion heat flux with constant ion temperature, summed over all core boundaries with BCENI=16. ENIPAR(,1) specifies the power flux in W.
    17 : feedback boundary condition with constant shared temperature for both electrons and ions, see BCENE=17 above for description.
    18 : fractional drop condition.  Experimental. Attempts to set the guard cell temperature to be (1 - ENIPAR(,1)) times the boundary cell temperature.
    19 : same as [9] but to be used when simultaneously setting BCCON=1 on the same boundary. Not yet available for WG.
    20 : feedback boundary condition with constant temperature, as per type [16] but with a different feedback scheme. ENEPAR(,2) is the strength of the feedback (if left zero, b2stbc\_bc\_ref\_ti is used).
    21 : from b2stbc\_spb. Not yet available for WG.
    22 : radial leakage condition for the ion temperature. ENIPAR(,1) specifies the leakage velocity in units of the collective ion thermal velocity. A temperature gradient such that the diffusive flux is set to match this leakage is imposed.
    23 : prescribe the poloidally averaged value of the ion temperature and introduce a poloidal variation as close as possible to neoclassical solution. It is recommended to use this boundary condition together with corresponding condition on ion density (BCCON=21,22,23). The average is taken over all core boundaries with BCENI=23. ENIPAR(,1) specifies the temperature in eV.
    24 : feedback boundary condition with prescribed total ion flux, constant poloidally averaged ion temperature and a poloidal variation as close as possible to neoclassical solution. It is recommended to use this boundary condition together with corresponding condition on ion density (BCCON=21,22,23). The flux is summed over all core boundaries with BCENI=24. ENIPAR(,1) specifies the energy flux in W. ENIPAR(,2) gives the strength of the feedback (if left zero, b2stbc\_bc\_ref\_ti will be used).
    25 : constant temperature feedback scaled by temperature on nearby ring. ENIPAR(,1) specifies the desired ion temperature in eV. ENIPAR(,2) is the strength of the feedback (if left zero, b2stbc\_bc\_ref\_ti will be used).
    26 : prescribe the poloidally averaged value of the ion temperature and introduce a poloidal variation in a simplified manner. This boundary condition is suitable for any plasma composition (i.e. when BCENI=23 fails). It is recommended to use this boundary condition together with corresponding condition on ion density (BCCON = 25,26,27). The average is taken over all core boundaries with BCENI=26. ENIPAR(,1) specifies the temperature in eV.
    27 : feedback boundary condition with prescribed total ion heat flux, constant poloidally averaged ion temperature and a poloidal variation in a simplified manner. This boundary condition is suitable for any plasma composition (i.e. when BCENI=24 fails). It is recommended to use this boundary condition together with corresponding condition on ion density (BCCON = 25,26,27). The flux is summed over all core boundaries with BCENI=27. ENIPAR(,1) specifies the energy flux in W. ENIPAR(,2) gives the strength of the feedback (if left zero, b2stbc\_bc\_ref\_ti will be used).
    28 : prescribe the value of the ion temperature, with a poloidal perturbation taken from the flux tube just inside the domain. ENIPAR(,1) specifies the average temperature in eV.
    29 : feedback on the total ion energy flux, by imposing a flux surface averaged temperature, with a poloidal perturbation taken from the flux tube just inside domain. ENIPAR(,1) specifies the energy flux in W. ENIPAR(,2) specifies the strength of the feedback (if left zero, b2stbc\_bc\_ref\_ti will be used).
    

.. index:: BCPOT

``BCPOT``    type: ``integer array, length NBC``
    Specifying the type of electric potential or current boundary condition for each segment; makes use of POTPAR to specify additional information, as indicated
    0 : default, no boundary condition is applied
    1 : prescribe the value of the potential, POTPAR(,1) specifies the potential in V
    2 : prescribe the gradient of the potential, POTPAR(,1) specifies the potential gradient in V.m^-1`
    3 : sheath conditions,

    |	POTPAR(,2) used for biasing [see code for details]. BCPOT = 3 not adapted for WG. Replace with drift-compatible BCPOT = 11.

    4 : prescribe the value of the potential weakly a mixed boundary condition, POTPAR(,1) specifies the potential in V and POTPAR(,2) specifies the 'strength' of the boundary condition.
    5 : prescribe the current flux density per unit area, POTPAR(,1) specifies the electric current flux density in A.m^-2`..
    6 : prescribe the total current flux density for a constant potential [not yet available]
    7 : prescribe the given profile of potential from the bv\_po.dat file (requires b2mndr\_boundary\_sources.eq.1)
    8 : prescribe the total electric current with constant flux density, POTPAR(,1) specifies the electric current in A
    9 : prescribe the decay length for the potential, POTPAR(,1) specifies the decay length in m.
    10 : should not be used for feedbacks anymore, not converted to WG code.
    11 : sheath conditions, electron energy transmission, POTPAR(,2) specifies the bias potential in V. Recommended for use in cases with drifts, along with BCENE/I=15, BCCON=14, and BCMOM=13.
    12 : imposes the currents due to drifts for the core boundary. Must be used in conjunction with istyle\_cur\_contr\_on\_S\_and\_N.eq.2
    13 : imposes the currents due to drifts for the private flux and main chamber boundaries. Must be used in conjunction with istyle\_cur\_contr\_on\_S\_and\_N.eq.2
    14 : prescribe the total current without imposing a specific profile. Follow the profile of the 1st flux tube inside. Intended use: core boundary, total PF boundary,.. For testing purposes, use with care!
    15 : feedback boundary condition on total current with constant potential. POTPAR(,1) specifies the electric current in A. POTPAR(,2) specifies the strength of the feedback (if left zero, b2stbc\_bc\_ref\_te will be used).
    16 : constant electric potential feedback on imposed total current. The current prescribed is given by the sum of the POTPAR(IB,1) (in A) over all the BCPOT=16 boundaries. Still experimental, will not work for drift cases.
    17 : feedback condition on total current, imposing a potential profile matching that of the neighbouring flux tube. POTPAR(,1) specifies the electric current in A. POTPAR(,2) specifies the strength of the feedback (if left zero, b2stbc\_bc\_ref\_te will be used).
    21 : constant potential feedback scaled by potential on the nearby ring. POTPAR(,,1) specifies the desired potential in V. POTPAR(,,2) is the strength of the feedback (if left zero, b2stbc\_bc\_ref\_te will be used).
    22 : prescribe the value of the potential, with a perturbation taken from the first flux tube in the domain. Intended for core boundaries only. POTPAR(,1) specifies the average potential.
    23 : potential feedback on the total current for the core boundary, imposing a flux surface averaged potential, with poloidal perturbation taken from flux tube just inside domain. The feedback is scaled with the ion temperature. POTPAR(,,1) specifies the desired integral current through flux surfaces (in Amperes). POTPAR(,,2) is the strength of the feedback (if left zero, b2stbc\_bc\_ref\_te will be used).
    

.. index:: BCENK

``BCENK``    type: ``integer array, length NBC``
    Specifying the type of boundary condition for the turbulent kinetic energy (kt) for each segment; makes use of ENKPAR to specify additional information, as indicated
    0 : default, no boundary condition is applied
    1 : prescribe the value of the turbulent kinetic energy, ENKPAR(,1) specifies the energy in eV.
    2 : prescribe the gradient of the turbulent kinetic energy, ENKPAR(,1) specifies the gradient of the turbulent kinetic energy in eV/m.
    6 : prescribe the total flux of turbulent kinetic energy, following the profile of the total heat flux. ENKPAR(,1) specifies the flux in W.
    7 : prescribe the total flux of turbulent kinetic energy, following the profile of the particle flux. ENKPAR(,1) specifies the flux in W.
    8 : prescribe the total flux of turbulent kinetic energy, with constant flux density. ENKPAR(,1) specifies the flux in W.
    14 : leakage option for turbulent kinetic energy, ENKPAR(,1) specifies the leakage factor, α in Γ`_loss`;; = α C`_s,collective` n`_i` κ.
    15 : sheath loss boundary condition. For now it assumes that BCCON = 14 is used. ENKPAR(,1) specifies the sheath transmission factor corresponding to the particle fluxes dictated by CONPAR(,,1) and ENKPAR(,2) specifies the sheath transmission factor corresponding to the particle fluxes dictated by CONPAR(,,2).
    16 : prescribe the value of the turbulent kinetic energy, with a poloidal perturbation taken from the flux tube just inside domain. kt = ENKPAR(,1) + kt2 - kt2av, where kt2 is the turbulent kinetic energy in the first cell inside the domain, and kt2av is the average turbulent kinetic energy in the flux tube just inside the domain. Intended for core boundaries only.
    17 : feedback on the turbulent kinetic energy flux, by imposing a flux surface averaged κ, with a poloidal perturbation taken from the flux tube just inside the domain. Intended for core boundaries only. ENKPAR(,1) specifies the flux in W. ENKPAR(,2) specifies the strength of the feedback (if left zero, b2stbc\_bc\_ref\_ti will be used).
    

.. index:: BCENZ

``BCENZ``    type: ``integer array, length NBC``
    Specifying the type of boundary condition for the turbulent enstrophy (zt) for each segment; makes use of ENZPAR to specify additional information, as indicated
    0 : default, no boundary condition is applied
    1 : prescribe the value of the turbulent enstrophy, ENZPAR(,1) specifies the enstrophy in s^-2`..
    2 : prescribe the gradient of the turbulent enstrophy, ENZPAR(,1) specifies the gradient of the turbulent enstrophy in s^-2`/m./m.
    14 : leakage option for turbulent enstrophy, ENZPAR(,1) specifies the leakage factor, α in Γ`_loss` = α C`_s,collective` n`_i` ζ
    15 : sheath loss boundary condition. For now it assumes that BCCON = 14 is used. ENZPAR(,1) specifies the sheath transmission factor corresponding to the particle fluxes dictated by CONPAR(,,1) and ENZPAR(,2) specifies the sheath transmission factor corresponding to the particle fluxes dictated by CONPAR(,,2).
    16 : prescribe the value of the turbulent enstrophy, with a poloidal perturbation taken from the flux tube just inside the domain. zt = ENZPAR(,1) + zt2 - zt2av, where zt2 is the enstrophy in the first cell inside the domain, and zt2av is the average enstrohpy in the flux tube just inside the domain. Intended for core boundaries only.
    

.. index:: GAMMAI

``GAMMAI``    type: ``real``    default: ``1.0``
    Adiabatic coefficient multiplying the ion temperature when computing the sound speeds.
    

.. index:: GAMMAE

``GAMMAE``    type: ``real``    default: ``0.5``
    Secondary electron emission coefficient.
    

.. index:: LBNDUSR

``LBNDUSR``    type: ``logical``    default: ``.false.``
    Obsolete.
    

.. index:: LFEEDBACK

``LFEEDBACK``    type: ``logical``    default: ``.false.``
    Indicates whether a feedback scheme is used. Obsolete. Superceded by 'b2stbc\_feedback'.
    

.. index:: NNISO

``NNISO``    type: ``integer``    default: ``0``
    Number of dead (or isolated) regions.
    

.. index:: NIISO

``NIISO``    type: ``real array of size (0:NS-1)``
    Density of species (is) in (m-3) to impose in isolated regions.
    

.. index:: TEISO

``TEISO``    type: ``real``    default: ``1.0``
    Electron temperature (in eV) to impose in isolated regions.
    

.. index:: TIISO

``TIISO``    type: ``real``    default: ``1.0``
    Ion temperature (in eV) to impose in isolated regions.
    

.. index:: PHIISO

``PHIISO``    type: ``real``    default: ``0.0``
    Electric potential (in V) to impose in isolated regions.
    

.. index:: NXISO1

``NXISO1``    type: ``integer array of size NNISO``    default: ``-2``
    Column number of bottom left corner of the dead region (iiso).
    

.. index:: NXISO2

``NXISO2``    type: ``integer array of size NNISO``    default: ``-2``
    Column number of top right corner of the dead region (iiso).
    

.. index:: NYISO1

``NYISO1``    type: ``integer array of size NNISO``    default: ``-2``
    Row number of bottom left corner of the dead region (iiso).
    

.. index:: NYISO2

``NYISO2``    type: ``integer array of size NNISO``    default: ``-2``
    Row number of top right corner of the dead region (iiso).
    

.. index:: BOUNDARY_FILENAME

``BOUNDARY_FILENAME``    type: ``character*256``    default: ``b2.boundary.parameters``
    Name of the next file to use for reading a new /BOUNDARY/ namelist.
    

.. index:: BOUNDARY_TIME_MOD

``BOUNDARY_TIME_MOD``    type: ``real``    default: ``0.0``
    When the B2.5 run simulation time, in seconds, modulo(BOUNDARY\_TIME\_MOD), reaches or exceeds BOUNDARY\_TIME\_SWITCH, reads the new namelist from BOUNDARY\_FILENAME. Also switches to the new namelist as the ELM count (here time/BOUNDARY\_TIME\_MOD) changes. Only active if BOUNDARY\_TIME\_MOD is greater than 0.
    

.. index:: BOUNDARY_TIME_SWITCH

``BOUNDARY_TIME_SWITCH``    type: ``real``    default: ``0.0``
    If BOUNDARY\_TIME\_MOD is greater than 0, time (in seconds) within an ELM cycle at which a new BOUNDARY namelist is read.
    Otherwise, B2.5 simulation time, in seconds, when to read the next BOUNDARY namelist file from BOUNDARY\_FILENAME.
    Only active if BOUNDARY\_TIME\_SWITCH is greater than 0.
    

.. index:: LCBS

``LCBS``    type: ``integer array of size (NBC)``    default: ``0``
    List of core boundary segments, according to their numbering in the current /BOUNDARY/ namelist.
    For cases with closed field lines, the code will attempt to build the array from the topology information available, i.e., it will contain the list of 'South' boundaries forming a closed contour.
    For linear cases, in case a "core" type boundary condition is desired, then LCBS must be specified explicitly.
    

.. index:: WRITE_NML_BND

``WRITE_NML_BND``    type: ``logical``    default: ``.true.``
    If .true. (default), writes the content of the namelist to stdout after it has been read.
    

.. index:: 
   single: b2.boundary.parameters; NBC
   single: b2.boundary.parameters; BCCHAR
   single: b2.boundary.parameters; CONPAR
   single: b2.boundary.parameters; MOMPAR
   single: b2.boundary.parameters; ENEPAR
   single: b2.boundary.parameters; ENIPAR
   single: b2.boundary.parameters; POTPAR
   single: b2.boundary.parameters; BCPOS
   single: b2.boundary.parameters; BCSTART
   single: b2.boundary.parameters; BCEND
   single: b2.boundary.parameters; BC_LIST_SIZE
   single: b2.boundary.parameters; BC_LIST_X
   single: b2.boundary.parameters; BC_LIST_Y
   single: b2.boundary.parameters; BCCON
   single: b2.boundary.parameters; BCMOM
   single: b2.boundary.parameters; BCENE
   single: b2.boundary.parameters; BCENI
   single: b2.boundary.parameters; BCPOT
   single: b2.boundary.parameters; BCENK
   single: b2.boundary.parameters; BCENZ
   single: b2.boundary.parameters; GAMMAI
   single: b2.boundary.parameters; GAMMAE
   single: b2.boundary.parameters; LBNDUSR
   single: b2.boundary.parameters; LFEEDBACK
   single: b2.boundary.parameters; NNISO
   single: b2.boundary.parameters; NIISO
   single: b2.boundary.parameters; TEISO
   single: b2.boundary.parameters; TIISO
   single: b2.boundary.parameters; PHIISO
   single: b2.boundary.parameters; NXISO1
   single: b2.boundary.parameters; NXISO2
   single: b2.boundary.parameters; NYISO1
   single: b2.boundary.parameters; NYISO2
   single: b2.boundary.parameters; BOUNDARY_FILENAME
   single: b2.boundary.parameters; BOUNDARY_TIME_MOD
   single: b2.boundary.parameters; BOUNDARY_TIME_SWITCH
   single: b2.boundary.parameters; LCBS
   single: b2.boundary.parameters; WRITE_NML_BND

.. index:: b2.feedback_save.parameters

b2.feedback_save.parameters
===========================
.. index:: SAVED_FB_ACTUATOR

``SAVED_FB_ACTUATOR``    type: ``real array of size (NFB)``    default: ``0.0``
    Last value used for the feedback actuator for each feedback.
    

.. index:: SAVED_FB_PREV

``SAVED_FB_PREV``    type: ``real array of size (NSPECIES)``    default: ``0.0``
    Last value of the density used for the feedback control for each isonuclear sequence.
    

.. index:: 
   single: b2.feedback_save.parameters; SAVED_FB_ACTUATOR
   single: b2.feedback_save.parameters; SAVED_FB_PREV

.. index:: b2.feedback_control.parameters

b2.feedback_control.parameters
==============================
.. index:: VACUUM_COMMUNICATION

``VACUUM_COMMUNICATION``    type: ``integer``    default: ``0``
    If > 0, allows for a	communication of particle fluxes across vacuum regions. This option only applies to neutrals. The density boundary condition is based on the difference between the average pressure and the local pressure.
    Not yet implemented in WG code.
    

.. index:: VACUUM_COMMUNICATION_NREG

``VACUUM_COMMUNICATION_NREG``    type: ``integer array of size (NVAC)``    default: ``0``
    Number of communicating vacuum regions.
    Not yet implemented in WG code.
    

.. index:: VACUUM_COMMUNICATION_METHOD

``VACUUM_COMMUNICATION_METHOD``    type: ``integer array of size (NVAC)``    default: ``0``
    Option for resorbing the pressure difference.

    |	1: Try to set a flux. Corr = (beta\*ave\_pressure - pressure)/temp \* alpha
    |	2: Try to set a density based on pressure equality.

    Corr = α \* beta \* pressure / Ti
    Not yet implemented in WG code.
    

.. index:: VACUUM_COMMUNICATION_IY

``VACUUM_COMMUNICATION_IY``    type: ``integer array of size (NVACREG,NVAC)``    default: ``-2``
    Radial index of the ring on which the neutral pressure is computed for region IREG.
    Not yet implemented in WG code.
    

.. index:: VACUUM_COMMUNICATION_IX1

``VACUUM_COMMUNICATION_IX1``    type: ``integer array of size (NVACREG,NVAC)``    default: ``-2``
    Poloidal lower bound of the range over which the neutral pressure is computed for region IREG.
    Not yet implemented in WG code.
    

.. index:: VACUUM_COMMUNICATION_IX2

``VACUUM_COMMUNICATION_IX2``    type: ``integer array of size (NVACREG,NVAC)``    default: ``-2``
    Poloidal upper bound of the range over which the neutral pressure is computed for region IREG.
    Not yet implemented in WG code.
    

.. index:: VACUUM_COMMUNICATION_ALPHA

``VACUUM_COMMUNICATION_ALPHA``    type: ``real array of size (0:NSPECIES-1,NVAC)``    default: ``0.0``
    Parameter for setting the pressure correction. See above.
    Not yet implemented in WG code.
    

.. index:: VACUUM_COMMUNICATION_BETA

``VACUUM_COMMUNICATION_BETA``    type: ``real array of size (0:NSPECIES-1,NVAC)``    default: ``1.0``
    Parameter for setting the pressure correction. See above.
    Not yet implemented in WG code.
    

.. index:: NFB

``NFB``    type: ``integer``    default: ``0``
    Number of feedback schemes applied.
    

.. index:: FB_TYPE

``FB_TYPE``    type: ``integer array of size (NFB)``    default: ``0``
    Choice of quantity on which the feedback is computed:

    |	0: no action
    |	1: local species density (averaged over cells/faces defined with fb\_reg or fb\_reg\_par). Summed over all charge states of that species.
    |	2: local electron density (averaged over cells/faces defined with fb\_reg or fb\_reg\_par).
    |	3: outer midplane separatrix electron density.
    |	4: total particle content for that species over cells/faces defined with fb\_reg or fb\_reg\_par.
    |	5: total ion content for that species (not including neutrals) over cells/faces defined with fb\_reg or fb\_reg\_par.
    |	6: neutral particle flux through the core boundary (for now only for kinetic neutral cases).
    |	7: relative average concentration of this species at the separatrix.
    |	8: relative average concentration of this species over cells/faces defined with fb\_reg or fb\_reg\_par.
    |	9: inner midplane separatrix electron density.
    |	10: boundary fna (similar to 'b2stbc\_fnaycore' but for any boundary)
    |	11: boundary fhe (similar to 'b2stbc\_fheycore' but for any boundary)
    |	12: boundary fhi (similar to 'b2stbc\_fhiycore' but for any boundary)
    |	13: boundary fch (similar to 'b2stbc\_fchycore' but for any boundary)
    |	14: total particle content of that species on the entire domain (similar to 'b2stbc\_ndes' and 'b2stbc\_ndes\_sol' but actuator applied to any boundary)
    |	15: Volumetric recombination (only for kinetic neutral cases) (similar to 'b2stbc\_volrec\_sol' but actuator applied to any boundary)
    |	16: Pedestal electron density (similar to 'b2stbc\_nepedm\_sol' but actuator applied to any boundary)
    |	17: Density of ions at the outer midplane separatrix
    |	18: Integrated electron cooling over the entire domain
    |	20: Neutral pressure of this sequence. It is necessary to set PFR\_CVS and NPFR\_CVS in b2.user.parameters to specify the control volumes used to compute the neutral pressure.
    |	21: Total radiation losses over the entire domain
    |	22: Average density of this species along the separatrix
    |	23: Peak heat flux density along a specific boundary. The boundary index should be defined by FB\_REG\_PAR. By default it equals 2, which usually maps to the outer target.
    |	24: Peak electron temperature along a specific boundary. The boundary index should be defined by FB\_REG\_PAR. By default it equals 2, which usually maps to the outer target.
    |	25: Peak electron density along a specific boundary. The boundary index should be defined by FB\_REG\_PAR. By default it equals 2, which usually maps to the outer target.
    |	26: Peak saturation current along a specific boundary. The boundary index should be defined by FB\_REG\_PAR. By default it equals 2, which usually maps to the outer target.
    |	27: Total particle content in the SOL and PFR for the isonuclear sequence (including Eirene neutrals).

    

.. index:: FB_RESCALE

``FB_RESCALE``    type: ``integer array of size (NFB)``    default: ``0``
    Option for computing the new fedback quantity.

    |	0: no action
    |	1: rescale slowed by fb\_alpha
    |	2: pure rescale
    |	3: rescaling slowed by tanh\_log
    |	4: rescale done according to SOLPS4 formula
    |		The target waveform for the particle content is
    |		N = C + V\*(time-T)
    |		and the current puffing rate S is adjusted
    |		S --> max(0, min(X,S + D)), where D = F\*((N - <N>)/dt + (<N>\_prev - <N>)/dt\_prev)
    |	5: rescale done according to SOLPS4 formula: N = C\*exp((time-T)\*V)
    |	6: rescale slowed by fb\_alpha (SOLPS4 style)
    |	7: If fb\_target/fb\_current < (1-fb\_const) or > (1+fb\_const), the rescaling coincides with FB\_RESCALE.eq.3. Otherwise no rescaling is applied.

    

.. index:: FB_ACTUATOR

``FB_ACTUATOR``    type: ``integer array of size (NFB)``    default: ``0``
    Choice for the actuator used for the feedback.
    0: no action
    1: gas puff via boundary condition
    2: rescale na [[Experimental!! Does not guarantee stable code runs]]
    3: charged species particle flux BC
    4: electron heat flux BC
    5: ion heat flux BC
    6: current BC
    7: density BC
    

.. index:: FB_TARGET

``FB_TARGET``    type: ``real array of size (NFB)``    default: ``0.0``
    Sets the target value of the quantity associated with feedback (IFB) for the feedback scheme defined by FB\_TYPE(IFB).
    

.. index:: FB_TYPE_INVERSE

``FB_TYPE_INVERSE``    type: ``logical array of size (NFB)``    default: ``.false.``
    If FB\_TYPE\_INVERSE(IFB) is .true., then the feedback is done on the inverse of the quantity provided as FB\_TARGET(IFB).
    Can be used in conjunction with FB\_TYPE=26.
    

.. index:: FB_SPECIES

``FB_SPECIES``    type: ``integer array of size (NFB)``    default: ``0``
    Specifies the species used to calculate the controlled variable and to which the actuator is applied. It follows the B2.5 plasma species enumeration. In general, controlled quantities are calculated on the whole isonuclear sequence to which fb\_species(ifb) belongs. Then if fb\_actuator.eq.1, it is applied to neutral species through gas puff; if fb\_actuator.eq.2, it is applied to the ionized species only; if fb\_actuator.eq.3 it is applied only to fb\_species. For fb\_type.eq.6 and fb\_actuator.eq.3 then it is also applied to all ionized species (as in the old feedback treatment). Overridden by switch 'b2stbc\_isfeedback'.
    

.. index:: FB_TIME

``FB_TIME``    type: ``real array of size (NFB)``    default: ``0.0``
    Sets the time of reference (in s) for the feedback (IFB).
    

.. index:: FB_ALPHA

``FB_ALPHA``    type: ``real array of size (NFB)``    default: ``0.001``
    Factor by which the rescaling is slowed. Rescaling factor is :
    Option 1: (1 + alpha\*target/current) / (1 + alpha)
    Option 3: 2\*\*(tanh(log(x)/beta)\*log(alpha)/log(2))
    Options 4 and 5: Corresponds to parameter F
    Can be overridden by switches 'b2stbc\_nesepm\_alpha', 'b2stbc\_fnaycore\_alpha', 'b2stbc\_fheycore\_alpha', 'b2stbc\_fhiycore\_alpha', 'b2stbc\_fchycore\_alpha', 'b2stbc\_volrec\_alpha'.
    

.. index:: FB_BETA

``FB_BETA``    type: ``real array of size (NFB)``    default: ``1.0``
    Factor by which the rescaling is slowed. See above. Options 4 and 5: Corresponds to parameter V (ffb\_rtvn). Cna be overridden by 'b2stbc\_volrec\_beta'.
    

.. index:: FB_CONST

``FB_CONST``    type: ``real array of size (NFB)``    default: ``0.0``
    Options 4 and 5: Corresponds to parameter C. If negative, C is computed as the initial total particle content of the sequence.
    

.. index:: FB_IB

``FB_IB``    type: ``integer array of size (NFB)``    default: ``-1``
    Index of boundary condition through which the feedback is being applied.
    

.. index:: FB_ISTRA

``FB_ISTRA``    type: ``integer array of size (NFB)``    default: ``0``
    Eirene strata where the gas puff feedback is applied. Overridden by switch 'eirene\_nesepm\_istra'.
    

.. index:: FB_PUFF_MIN

``FB_PUFF_MIN``    type: ``real array of size (NFB)``    default: ``0.0``
    Minimum gas puff being applied. Can be overrdidden by switch 'b2stbc\_nesepm\_minpuff'.
    

.. index:: FB_PUFF_MAX

``FB_PUFF_MAX``    type: ``real array of size (NFB)``    default: ``0.0``
    Maximum gas puff being applied. Can be overrdidden by switch 'b2stbc\_nesepm\_maxpuff'.
    

.. index:: FB_OVERSHOOT

``FB_OVERSHOOT``    type: ``real array of size (NFB)``    default: ``0.0``
    If the density is larger than target\*overshoot, the gas puff is turned off. Can be overridden by switch 'b2stbc\_nesepm\_overshoot', 'b2stbc\_volrec\_overshoot'.
    

.. index:: FB_REGP

``FB_REGP``    type: ``integer array of size (NFB,2)``    default: ``0``
    Pointing for each feedback to the first index in FB\_REG, and its number of CVs or faces.
    

.. index:: FB_REG

``FB_REG``    type: ``integer array of size (nMxFbReg)``    default: ``0``
    Listing for each feedback the cells or faces where controlled quantity is calculated. If different feedbacks use the same domain then this can be defined only ones and simply point to it twice with fb\_regP. nMxFbReg is a maximum length set in b2us\_feedback.
    

.. index:: FB_REG_PAR

``FB_REG_PAR``    type: ``integer array of size (NFB,2)``    default: ``0``
    If the two FB\_REG and FB\_REGP are not defined, then the code will look for this array.
    For fb\_type 6-10-11-12-13-23-24-25-26, fb\_reg\_par(ifb,:) indicates the starting (iFb,1) and ending (iFb,2) face region label over which the controlled quantity is calculated.
    For fb\_type 1-2-4-5-8, fb\_reg\_par(ifb,:) indicates the starting (iFb,1) and ending (iFb,2) volume region label over which the controlled quantity is calculated.
    

.. index:: 
   single: b2.feedback_control.parameters; VACUUM_COMMUNICATION
   single: b2.feedback_control.parameters; VACUUM_COMMUNICATION_NREG
   single: b2.feedback_control.parameters; VACUUM_COMMUNICATION_METHOD
   single: b2.feedback_control.parameters; VACUUM_COMMUNICATION_IY
   single: b2.feedback_control.parameters; VACUUM_COMMUNICATION_IX1
   single: b2.feedback_control.parameters; VACUUM_COMMUNICATION_IX2
   single: b2.feedback_control.parameters; VACUUM_COMMUNICATION_ALPHA
   single: b2.feedback_control.parameters; VACUUM_COMMUNICATION_BETA
   single: b2.feedback_control.parameters; NFB
   single: b2.feedback_control.parameters; FB_TYPE
   single: b2.feedback_control.parameters; FB_RESCALE
   single: b2.feedback_control.parameters; FB_ACTUATOR
   single: b2.feedback_control.parameters; FB_TARGET
   single: b2.feedback_control.parameters; FB_TYPE_INVERSE
   single: b2.feedback_control.parameters; FB_SPECIES
   single: b2.feedback_control.parameters; FB_TIME
   single: b2.feedback_control.parameters; FB_ALPHA
   single: b2.feedback_control.parameters; FB_BETA
   single: b2.feedback_control.parameters; FB_CONST
   single: b2.feedback_control.parameters; FB_IB
   single: b2.feedback_control.parameters; FB_ISTRA
   single: b2.feedback_control.parameters; FB_PUFF_MIN
   single: b2.feedback_control.parameters; FB_PUFF_MAX
   single: b2.feedback_control.parameters; FB_OVERSHOOT
   single: b2.feedback_control.parameters; FB_REGP
   single: b2.feedback_control.parameters; FB_REG
   single: b2.feedback_control.parameters; FB_REG_PAR

.. index:: b2.sources.profile

b2.sources.profile
==================
.. index:: NSDATA

``NSDATA``    type: ``integer array of size (NKIND_DATA,NKIND_SOURCE,0:NS)``    default: ``0``
    Number of points over which the source profile of (kind\_data,kind\_source,is) is defined. Should not exceed NY+2.

    |	If KIND\_DATA=1, the data is expressed as a profile in physical distance from the separatrix (in metres) along the outer midplane.
    |	The user can change this default reference location by use of the 'set\_transport\_i[xy]ref' switches.
    |	If KIND\_DATA=2, the data is expressed as a profile in flux distance from the separatrix (not yet available).

    

.. index:: SDATA

``SDATA``    type: ``real data of size (2,NY+2,NKIND_SOURCE,0:NS)``    default: ``0.0``
    For (i,ir,ik,is) in (1:2,1:NY+2,1:NKIND\_SOURCE,0:NS),
    SDATA(1,ir,:,:) contains the radial location of the profile point (ir).
    SDATA(2,ir,:,:) contains the source profile value at point (ir).
    KIND\_SOURCE=1 means particle source of species (is) (in particles/s/m3)
    KIND\_SOURCE=2 means parallel momentum source for species (is) (in N/m3)
    KIND\_SOURCE=3 means electron heat source (in Watts/m3)
    KIND\_SOURCE=4 means ion heat source (in Watts/m3)
    KIND\_SOURCE=5 means electric charge source (in Amperes/m3)
    KIND\_SOURCE=6 means non-ambipolar electron particle source (in e/s/m3)
    

.. index:: NXDATA

``NXDATA``    type: ``integer array of size (NKIND_DATA,NKIND_SOURCE,0:NS)``
    Number of points over which the axial profile of (kind\_data,kind\_source,is) is defined. Should not exceed NX+2. Defaults to 0.
    If KIND\_DATA=1, the data is expressed as a profile in physical distance, here connection length, rescaled from 0.0 to 1.0.
    For closed field lines, the reference location for the zero of distance is set by use of the 'set\_transport\_i[xy]ref' switches.
    If KIND\_DATA=2, the data is expressed as a profile in (ix) cell index, again normalized from 0.0 to 1.0 to match the [0:nx-1] interval.
    

.. index:: XDATA

``XDATA``    type: ``real data of size (2,NY+2,NKIND_SOURCE,0:NS)``    default: ``1.0``
    Multiplier to the poloidal source profile in the axial direction. Same convention for KIND\_SOURCE as above.
    

.. index:: DIVHEAT

``DIVHEAT``    type: ``real``    default: ``0.0``
    Additional divertor ion heat source (in Watts/m^3`))
    

.. index:: SOURCES_FILENAME

``SOURCES_FILENAME``    type: ``character*256``    default: ``b2.sources.profile``
    Name of the next file to use for reading a new /PROFILE/ namelist. Quantities not present in the new file will be inherited from the old one.
    

.. index:: SOURCES_TIME_MOD

``SOURCES_TIME_MOD``    type: ``real``    default: ``0.0``
    When the B2.5 run simulation time, in seconds, modulo(SOURCES\_TIME\_MOD), reaches or exceeds SOURCES\_TIME\_SWITCH, reads the new namelist from SOURCES\_FILENAME. Also switches to the new namelist if the ELM count (here time/SOURCES\_TIME\_MOD) changes. Only active if SOURCES\_TIME\_MOD is greater than 0.
    

.. index:: SOURCES_TIME_SWITCH

``SOURCES_TIME_SWITCH``    type: ``real``    default: ``0.0``
    If SOURCES\_TIME\_MOD is greater than 0, time (in seconds) within an ELM cycle at which a new PROFILE namelist is read.
    Otherwise, B2.5 simulation time, in seconds, when to read the next PROFILE namelist file from SOURCES\_FILENAME.
    Only active if SOURCES\_TIME\_SWITCH is greater than 0.
    

.. index:: 
   single: b2.sources.profile; NSDATA
   single: b2.sources.profile; SDATA
   single: b2.sources.profile; NXDATA
   single: b2.sources.profile; XDATA
   single: b2.sources.profile; DIVHEAT
   single: b2.sources.profile; SOURCES_FILENAME
   single: b2.sources.profile; SOURCES_TIME_MOD
   single: b2.sources.profile; SOURCES_TIME_SWITCH

.. index:: b2.transport.inputfile

b2.transport.inputfile
======================
.. index:: NDATA

``NDATA``    type: ``integer array of size (NKIND_DATA,NCOEF,0:NS)``    default: ``0``
    Number of points over which the source profile of (kind\_data,kind\_coef,is) is defined. Should not exceed NY+2.
    If KIND\_DATA=1, the data is expressed as a profiles in physical distance from the separatrix (in metres).
    If KIND\_DATA=2, the data is expressed as a profile in flux distance from the separatrix (not yet available).
    

.. index:: TDATA

``TDATA``    type: ``real data of size (3,NY+2,NKIND_COEFF,0:NS)``    default: ``0.0``
    For (i,ir,ik,is) in (1:3,1:NY+2,1:NKIND\_COEFF,0:NS), TDATA(1,ir,:,:) contains the radial location of the profile point (ir).
    By default, these are measured at the outer midplane, as distance to the separatrix in metres. The user can change this by setting the 'set\_transport\_i[xy]ref' switches to choose a different location for the distance reference.
    TDATA(2,ir,:,:) contains the transport profile value at point (ir).
    TDATA(3,ir,:,:) contains the ELM transport profile value at point (ir).
    KIND\_COEFF=1 means density-driven particle diffusivity for species (is)
    KIND\_COEFF=2 means pressure-driven particle diffusivity for species (is)
    KIND\_COEFF=3 means ion heat diffusivity for species (is)
    KIND\_COEFF=4 means electron heat diffusivity
    KIND\_COEFF=5 means poloidal pinch velocity for species (is)
    KIND\_COEFF=6 means radial pinch velocity for species (is)
    KIND\_COEFF=7 means viscosity for species (is)
    KIND\_COEFF=8 means field-driven radial current conductivity
    KIND\_COEFF=9 means temperature-driven radial current conductivity
    

.. index:: ADDSPEC

``ADDSPEC``    type: ``integer array of size (NS,NKIND_COEFF,0:NS)``    default: ``-5``
    If ADDSPEC(is,ikind,spec).ge.0, then the transport coefficient profile of type (ikind) from species (spec) is also used for species with index ADDSPEC(is,ikind,spec).
    

.. index:: TRANSPORT_IP_FILENAME

``TRANSPORT_IP_FILENAME``    type: ``character*256``    default: ``b2.transport.inputfile``
    Name of the next file to use for reading a new /TRANSPORT/ namelist.
    

.. index:: TRANSPORT_IP_TIME_MOD

``TRANSPORT_IP_TIME_MOD``    type: ``real``    default: ``0.0``
    When the B2.5 run simulation time, in seconds, modulo(TRANSPORT\_IP\_TIME\_MOD), reaches or exceeds TRANSPORT\_IP\_TIME\_SWITCH, reads the new namelist from TRANSPORT\_IP\_FILENAME. Also switches to the new namelist if the ELM count (here time/TRANSPORT\_IP\_TIME\_MOD) changes. Only active if TRANSPORT\_IP\_TIME\_MOD is greater than 0.
    

.. index:: TRANSPORT_IP_TIME_SWITCH

``TRANSPORT_IP_TIME_SWITCH``    type: ``real``    default: ``0.0``
    If TRANSPORT\_IP\_TIME\_MOD is greater than 0, time (in seconds) within an ELM cycle at which a new TRANSPORT namelist is read.
    Otherwise, B2.5 simulation time, in seconds, when to read the next TRANSPORT namelist file from TRANSPORT\_IP\_FILENAME.
    Only active if TRANSPORT\_IP\_TIME\_SWITCH is greater than 0.
    

.. index:: REGION_FLAGS

``REGION_FLAGS``    type: ``logical array of size (NREG,NKIND_COEFF)``    default: ``.true.``
    If region\_flags(ireg,ikind) is .true. (default), then the transport parameters profiles for region (ireg) and kind (ikind) are used.
    

.. index:: NO_PFLUX

``NO_PFLUX``    type: ``logical``    default: ``.false.``
    If .true., transport coefficients profiles are not implemented in the private flux regions.
    

.. index:: NO_DIV

``NO_DIV``    type: ``logical``    default: ``.false.``
    If .true., transport coefficients profiles are not implemented in the divertor regions.
    

.. index:: POLOIDAL_SCALING

``POLOIDAL_SCALING``    type: ``logical array of size (10)``    default: ``.false.``
    If .true., then the transport coefficients profiles from the current b2.transport.inputfile are increased by a factor of 1.0+Gaussian where Gaussian is a Gaussian profile in the poloidal direction of amplitude SCALING\_STRENGTH extending from SCALING\_IX\_BEGIN to SCALING\_IX\_END inclusively. The profile has a decay length of SCALING\_WIDTH (in units of the number of poloidal cells).
    

.. index:: SCALING_STRENGTH

``SCALING_STRENGTH``    type: ``real array of size 10``    default: ``0``
    See above.
    

.. index:: SCALING_WIDTH

``SCALING_WIDTH``    type: ``real array of size 10``    default: ``1/3 interval``
    See above. Defaults to about 1/3 of the interval over which the scaling is to be done.
    

.. index:: SCALING_IX_BEGIN

``SCALING_IX_BEGIN``    type: ``integer array of size 10``    default: ``-2``
    See above.
    

.. index:: SCALING_IX_END

``SCALING_IX_END``    type: ``integer array of size 10``    default: ``-2``
    See above.
    

.. index:: ELM_TIME_BEGIN

``ELM_TIME_BEGIN``    type: ``real``    default: ``0.0``
    Time (in seconds) modulo ELM\_TIME\_PERIOD at which the ELM phase begins and the ELM data must be used.
    

.. index:: ELM_TIME_END

``ELM_TIME_END``    type: ``real``    default: ``0.0``
    Time (in seconds) modulo ELM\_TIME\_PERIOD at which the ELM phase ends and the ELM data is no longer used.
    

.. index:: ELM_TIME_PERIOD

``ELM_TIME_PERIOD``    type: ``real``    default: ``0.0``
    Indicates the real frequency of simulated ELMs. See above for usage.
    If zero, no ELM profiles are used.
    

.. index:: ELM_IX_BEGIN

``ELM_IX_BEGIN``    type: ``integer``    default: ``-2``
    Poloidal position at which the ELM profile starts to be applied.
    

.. index:: ELM_IX_END

``ELM_IX_END``    type: ``integer``    default: ``-2``
    Poloidal position at which the ELM profile ends being applied.
    

.. index:: 
   single: b2.transport.inputfile; NDATA
   single: b2.transport.inputfile; TDATA
   single: b2.transport.inputfile; ADDSPEC
   single: b2.transport.inputfile; TRANSPORT_IP_FILENAME
   single: b2.transport.inputfile; TRANSPORT_IP_TIME_MOD
   single: b2.transport.inputfile; TRANSPORT_IP_TIME_SWITCH
   single: b2.transport.inputfile; REGION_FLAGS
   single: b2.transport.inputfile; NO_PFLUX
   single: b2.transport.inputfile; NO_DIV
   single: b2.transport.inputfile; POLOIDAL_SCALING
   single: b2.transport.inputfile; SCALING_STRENGTH
   single: b2.transport.inputfile; SCALING_WIDTH
   single: b2.transport.inputfile; SCALING_IX_BEGIN
   single: b2.transport.inputfile; SCALING_IX_END
   single: b2.transport.inputfile; ELM_TIME_BEGIN
   single: b2.transport.inputfile; ELM_TIME_END
   single: b2.transport.inputfile; ELM_TIME_PERIOD
   single: b2.transport.inputfile; ELM_IX_BEGIN
   single: b2.transport.inputfile; ELM_IX_END

.. index:: b2.neutrals_save.parameters

b2.neutrals_save.parameters
===========================
.. index:: SAVED_VOLREC

``SAVED_VOLREC``    type: ``real array of size (NSTRAT)``    default: ``0.0``
    Contains the last value of the strength of volume recombination sources from stratum (istra).
    

.. index:: 
   single: b2.neutrals_save.parameters; SAVED_VOLREC

.. index:: b2.numerics.parameters

b2.numerics.parameters
======================
.. index:: DTCO

``DTCO``    type: ``real array of size (0:NS-1,0:NREG)``    default: ``1.0``
    Multiplier to the time used in solving the continuity equation of species (is) in region (ireg).
    

.. index:: DTMO

``DTMO``    type: ``real array of size (0:NS-1,0:NREG)``    default: ``1.0``
    Multiplier to the time used in solving the parallel momentum equation of species (is) in region (ireg).
    

.. index:: DTEE

``DTEE``    type: ``real array of size (0:NREG)``    default: ``1.0``
    Multiplier to the time used in solving the electron heat equation in region (ireg).
    

.. index:: DTEI

``DTEI``    type: ``real array of size (0:NREG)``    default: ``1.0``
    Multiplier to the time used in solving the ion heat equation in region (ireg).
    

.. index:: DTEN

``DTEN``    type: ``real array of size (0:NREG)``    default: ``1.0``
    Multiplier to the time used in solving the fluid neutral heat equation in region (ireg).
    

.. index:: DTFTS

``DTFTS``    type: ``integer array of size (DEF_NYD)``    default: ``0``
    List of flux tube indices for which individual timestep multipliers can be applied.
    

.. index:: DTCO_FT

``DTCO_FT``    type: ``real array of size (DEF_NYD)``    default: ``1.0``
    Individual timestep multiplier to all continuity equations applied in the corresponding flux tube from the DTFTS list.
    Must be positive.
    

.. index:: DTMO_FT

``DTMO_FT``    type: ``real array of size (DEF_NYD)``    default: ``1.0``
    Individual timestep multiplier to all parallel momentum equations applied in the corresponding flux tube from the DTFTS list.
    Must be positive.
    

.. index:: DTEE_FT

``DTEE_FT``    type: ``real array of size (DEF_NYD)``    default: ``1.0``
    Individual timestep multiplier to the electron heat equation applied in the corresponding flux tube from the DTFTS list.
    Must be positive.
    

.. index:: DTEI_FT

``DTEI_FT``    type: ``real array of size (DEF_NYD)``    default: ``1.0``
    Individual timestep multiplier to the ion heat equation applied in the corresponding flux tube from the DTFTS list.
    Must be positive.
    

.. index:: SOLVECO

``SOLVECO``    type: ``logical array of size (0:NS-1,0:NREG)``    default: ``.true.``
    Indicates whether the continuity equation for species (is) is to be solved in region (ireg). Subservient to 'no\_solve' switch.
    

.. index:: SOLVEMO

``SOLVEMO``    type: ``logical array of size (0:NS-1,0:NREG)``    default: ``.true.``
    Indicates whether the parallel momentum equation for species (is) is to be solved in region (ireg). Subservient to 'no\_solve' switch.
    

.. index:: SOLVEMT

``SOLVEMT``    type: ``logical array of size (0:NREG)``
    Indicates whether the total parallel momentum equation is to be solved in region (ireg). For the total parallel momentum equation to be solved in a region, all momentum equations in the range defined by 'b2news\_nsmin' and 'b2news\_nsmax' must have SOLVEMO true in that region. Subservient to 'no\_solve' switch.
    It is important to note that the 'b2news\_no\_solve' switch allows for solving or not all momentum equations together as a whole, along with the total equation.
    Defaults to .true. unless using the time-dependent mode, in which case it is set to .false. and should not be used.
    

.. index:: SOLVEPO

``SOLVEPO``    type: ``logical array of size (0:NREG)``    default: ``.true.``
    Indicates whether the potential energy equation is to be solved in region (ireg). Subservient to 'no\_solve' switch.
    

.. index:: SOLVEEE

``SOLVEEE``    type: ``logical array of size (0:NREG)``    default: ``.true.``
    Indicates whether the electron energy equation is to be solved in region (ireg). Subservient to 'no\_solve' switch.
    

.. index:: SOLVEEI

``SOLVEEI``    type: ``logical array of size (0:NREG)``    default: ``.true.``
    Indicates whether the ion energy equation is to be solved in region (ireg). Subservient to 'no\_solve' switch.
    

.. index:: SOLVEEN

``SOLVEEN``    type: ``logical array of size (0:NREG)``    default: ``.true.``
    Indicates whether the fluid neutral energy equation is to be solved in region (ireg). Subservient to 'no\_solve' switch.
    

.. index:: SOLVEET

``SOLVEET``    type: ``logical array of size (0:NREG)``
    Indicates whether the total energy equation is to be solved in region (ireg). For the equation to be solved in region (ireg), both SOLVEEE and SOLVEEI must be true in that region. Subservient to 'no\_solve' switch.
    It is important to note that the 'b2news\_no\_solve' switch allows to solve or not to solve the electron and ion heat equations together with the total energy equation, as a group.
    Defaults to .true. unless using the time-dependent mode, in which case it is set to .false. and should not be used.
    

.. index:: SOLVEKT

``SOLVEKT``    type: ``logical array of size (0:NREG)``    default: ``.true.``
    Indicates whether the ExB turbulent kinetic energy equation is to be solved in region (ireg). Subservient to 'no\_solve' switch.
    

.. index:: SOLVEZT

``SOLVEZT``    type: ``logical array of size (0:NREG)``    default: ``.true.``
    Indicates whether the ExB turbulent enstrophy equation is to be solved in region (ireg). Subservient to 'no\_solve' switch.
    

.. index:: TIME_FACTOR_REQUIRED

``TIME_FACTOR_REQUIRED``    type: ``real``    default: ``0.1``
    Minimum time scale of evolution allowed for all equations. Only active is 'b2srsm\_enable' is set to 1.
    

.. index:: CORE_DT_SUPPRESSION

``CORE_DT_SUPPRESSION``    type: ``real``    default: ``1.0``
    De-multiplier to the timestep in the core. Only active if less than 1. Should be larger than 0. Applies fully to the innermost core ring of cells (IY .eq. -1). See CORE\_DT\_FACTOR for further use.
    

.. index:: CORE_DT_FACTOR

``CORE_DT_FACTOR``    type: ``real``    default: ``1.0``
    Multiplier to the timestep in the core. Only active is less than 1. Should be larger than 0. Multiplies each successive core ring of cells (increasing IY) by CORE\_DT\_FACTOR, until the local time step multiplier is equal to 1.
    

.. index:: CORR_CORE_DN

``CORR_CORE_DN``    type: ``real array of size (0:NS-1)``    default: ``1.0``
    Pressure correction speed-up parameter α\_a, acting on the density contribution from species a. Will apply in the core region, except for the nrings outer surfaces. See nrings\_for\_no\_speedup\_averaging for details.
    See Pressure\_correction\_speed-up.pdf in $SOLPSTOP/doc for a full description. Should be roughly equal to corr\_core\_dt below. Does not apply to neutral species.
    

.. index:: CORR_CORE_DT

``CORR_CORE_DT``    type: ``real``    default: ``1.0``
    Pressure correction speed-up parameter α\_T, acting on the temperature contributions. Will apply in the core region, except for the nrings outer surfaces. See nrings\_for\_no\_speedup\_averaging for details.
    See Pressure\_correction\_speed-up.pdf in $SOLPSTOP/doc for a full description. Should be roughly equal to corr\_core\_dn above.
    

.. index:: SNA_CORR

``SNA_CORR``    type: ``real array of size (1:NSPECIES)``    default: ``0.0``
    Multiplier to the neutral source differential between puffing (plus sputtering plus core boundary flux plus any external sources) and pumping, which is further added to the ionization source for code speed-up. One multiplier must be provided per isonuclear sequence. Such settings might be relevant for e.g. a mixture of main ion and trace impurity.
    See E. Kaveeva et al., Nucl. Fusion 58 (2018) 126018 for details and keep in mind that in that paper the scheme was described in its original species-unresolved form.
    

.. index:: TAUMAX

``TAUMAX``    type: ``real array of size (1:NSPECIES)``    default: ``0.05``
    Maximum allowed fraction of ionization source for a given isonuclear sequence from its neutral state (coming from Eirene) to be added or subtracted to the real Eirene source in the method of effective sources for code speed-up.
    

.. index:: DO_SNA_CORR_CORE

``DO_SNA_CORR_CORE``    type: ``logical array of size (1:NSPECIES)``    default: ``.true.``
    Parameter which controls exclusion/inclusion of confined region from/in the method of effective sources for code speed-up for each isonuclear sequence. If .true., then the flux through the core boundary of that species is taken into account during the source correction computation, and the source correction is applied on closed flux surfaces (default behavior). If .false., then the particle imbalance is computed as puffing plus sputtering plus any external sources minus pumping without account of the flux through the core boundary, and no source correction is applied on closed surfaces (such a setting might be helpful if the core flux is much bigger than the puffing rate and the core is isolated from the SOL by a strong transport barrier).
    

.. index:: NUMERICS_FILENAME

``NUMERICS_FILENAME``    type: ``character*256``    default: ``b2.numerics.namelist``
    Name of the next file to use for reading a new /NUMERICS/ namelist.
    

.. index:: NUMERICS_TIME_MOD

``NUMERICS_TIME_MOD``    type: ``real``    default: ``0.0``
    When the B2.5 run simulation time, in seconds, modulo(NUMERICS\_TIME\_MOD), reaches or exceeds NUMERICS\_TIME\_SWITCH, reads the new namelist from NUMERICS\_FILENAME. Also switches to the new namelist as the ELM count (here time/NUMERICS\_TIME\_MOD) changes. Only active if NUMERICS\_TIME\_MOD is greater than 0.
    

.. index:: NUMERICS_TIME_SWITCH

``NUMERICS_TIME_SWITCH``    type: ``real``    default: ``0.0``
    If NUMERICS\_TIME\_MOD is greater than 0, time (in seconds) within an ELM cycle at which a new NUMERICS namelist is read.
    Otherwise, B2.5 simulation time, in seconds, when to read the next NUMERICS namelist file from NUMERICS\_FILENAME.
    Only active if NUMERICS\_TIME\_SWITCH is greater than 0.
    

.. index:: WRITE_NML_NUM

``WRITE_NML_NUM``    type: ``logical``    default: ``.true.``
    If .true. (default), writes the content of the namelist to stdout after it has been read.
    

.. index:: ADD_TE_CORR_TO_PO

``ADD_TE_CORR_TO_PO``    type: ``logical array of size (0:NREG)``    default: ``.true.``
    If .true. (default), adds dte(ix,iy)/qe to the potential correction after the internal energy balance equations are solved, where dte(ix,iy) is the electron temperature correction on the time step. Individually set for each region index.
    

.. index:: 
   single: b2.numerics.parameters; DTCO
   single: b2.numerics.parameters; DTMO
   single: b2.numerics.parameters; DTEE
   single: b2.numerics.parameters; DTEI
   single: b2.numerics.parameters; DTEN
   single: b2.numerics.parameters; DTFTS
   single: b2.numerics.parameters; DTCO_FT
   single: b2.numerics.parameters; DTMO_FT
   single: b2.numerics.parameters; DTEE_FT
   single: b2.numerics.parameters; DTEI_FT
   single: b2.numerics.parameters; SOLVECO
   single: b2.numerics.parameters; SOLVEMO
   single: b2.numerics.parameters; SOLVEMT
   single: b2.numerics.parameters; SOLVEPO
   single: b2.numerics.parameters; SOLVEEE
   single: b2.numerics.parameters; SOLVEEI
   single: b2.numerics.parameters; SOLVEEN
   single: b2.numerics.parameters; SOLVEET
   single: b2.numerics.parameters; SOLVEKT
   single: b2.numerics.parameters; SOLVEZT
   single: b2.numerics.parameters; TIME_FACTOR_REQUIRED
   single: b2.numerics.parameters; CORE_DT_SUPPRESSION
   single: b2.numerics.parameters; CORE_DT_FACTOR
   single: b2.numerics.parameters; CORR_CORE_DN
   single: b2.numerics.parameters; CORR_CORE_DT
   single: b2.numerics.parameters; SNA_CORR
   single: b2.numerics.parameters; TAUMAX
   single: b2.numerics.parameters; DO_SNA_CORR_CORE
   single: b2.numerics.parameters; NUMERICS_FILENAME
   single: b2.numerics.parameters; NUMERICS_TIME_MOD
   single: b2.numerics.parameters; NUMERICS_TIME_SWITCH
   single: b2.numerics.parameters; WRITE_NML_NUM
   single: b2.numerics.parameters; ADD_TE_CORR_TO_PO

.. index:: b2.transport_models_save.parameters

b2.transport_models_save.parameters
===================================
.. index:: ETA_HCE_MULT

``ETA_HCE_MULT``    type: ``real array of size (-1:NY)``    default: ``1.0``
    Used by the user specified set\_transport\_eta transport model. See code for details.
    

.. index:: 
   single: b2.transport_models_save.parameters; ETA_HCE_MULT

.. index:: b2.transport.parameters

b2.transport.parameters
=======================
.. index:: FLAG*

.. index:: FLAG_DNA, FLAG_DPA, FLAG_VLA, FLAG_VSA, FLAG_HCI, FLAG_HCE, FLAG_SIG, FLAG_ALF
.. c

``FLAG*``

  - ``FLAG_DNA``  -     type: ``integer``
    Transport model flag for density-driven diffusion.
    

  - ``FLAG_DPA``  -     type: ``integer``
    Transport model flag for pressure-driven dffusion.
    

  - ``FLAG_VLA``  -     type: ``integer``
    Transport model flag for pinch velocity.
    

  - ``FLAG_VSA``  -     type: ``integer``
    Transport model flag for viscosity.
    

  - ``FLAG_HCI``  -     type: ``integer``
    Transport model flag for ion heat diffusivity.
    

  - ``FLAG_HCE``  -     type: ``integer``
    Transport model flag for electron heat diffusivity.
    

  - ``FLAG_SIG``  -     type: ``integer``
    Transport model flag for field-driven current radial conductivity.
    

  - ``FLAG_ALF``  -     type: ``integer``
    Transport model flag for temperature-driven current radial conductivity.
    


    All flags follow:
    FLAG=0: Use model from b2ah.dat and b2mn.dat. Default.
    FLAG=1: Constant, value set to PARM.
    FLAG=2: 1/N model, multiplied by PARM.
    FLAG=3: Bohm model, multiplied by PARM.
    FLAG=4: flux-scaled model, multiplied by PARM.
    
.. index::
   single: FLAG*; FLAG_DNA
   single: FLAG*; FLAG_DPA
   single: FLAG*; FLAG_VLA
   single: FLAG*; FLAG_VSA
   single: FLAG*; FLAG_HCI
   single: FLAG*; FLAG_HCE
   single: FLAG*; FLAG_SIG
   single: FLAG*; FLAG_ALF


.. index:: PARM_DNA

``PARM_DNA``    type: ``real array of size (0:NS-1)``
    Parameter for the density-driven particle diffusion coefficient for species (is).
    

.. index:: PARM_DPA

``PARM_DPA``    type: ``real array of size (0:NS-1)``
    Parameter for the pressure-driven particle diffusion coefficient for species (is).
    

.. index:: PARM_VLA

``PARM_VLA``    type: ``real array of size (0:NS-1)``
    Parameter for the anomalous radial pinch velocity for species (is).
    

.. index:: PARM_VSA

``PARM_VSA``    type: ``real array of size (0:NS-1)``
    Parameter for the viscosity for species (is).
    

.. index:: PARM_HCI

``PARM_HCI``    type: ``real array of size (0:NS-1)``
    Parameter for the heat diffusivity coefficient for species (is).
    

.. index:: PARM_HCE

``PARM_HCE``    type: ``real``
    Parameter for the electron heat diffusivity coefficient.
    

.. index:: PARM_SIG

``PARM_SIG``    type: ``real``
    Parameter for the anomalous radial field-driven current conductivity.
    

.. index:: PARM_ALF

``PARM_ALF``    type: ``real``
    Parameter for the anomalous radial temperature-driven current conductivity.
    

.. index:: TRANSPORT_FILENAME

``TRANSPORT_FILENAME``    type: ``character*256``    default: ``b2.transport.parameters``
    Name of the next file to use for reading a new /TRANSPORT/ namelist.
    

.. index:: TRANSPORT_TIME_MOD

``TRANSPORT_TIME_MOD``    type: ``real``    default: ``0.0``
    When the B2.5 run simulation time, in seconds, modulo(TRANSPORT\_TIME\_MOD), reaches or exceeds TRANSPORT\_TIME\_SWITCH, reads the new namelist from TRANSPORT\_FILENAME. Also switches to the new namelist if the ELM count (here time/TRANSPORT\_TIME\_MOD) changes. Only active if TRANSPORT\_TIME\_MOD is greater than 0.
    

.. index:: TRANSPORT_TIME_SWITCH

``TRANSPORT_TIME_SWITCH``    type: ``real``    default: ``0.0``
    If TRANSPORT\_TIME\_MOD is greater than 0, time (in seconds) within an ELM cycle at which a new TRANSPORT namelist is read.
    Otherwise, B2.5 simulation time, in seconds, when to read the next TRANSPORT namelist file from TRANSPORT\_FILENAME.
    Only active if TRANSPORT\_TIME\_SWITCH is greater than 0.
    

.. index:: CFL*

.. index:: CFLME, CFLMI, CFLMV, CFLAL, CFLAB
.. c

``CFL*``

  - ``CFLME``  -     type: ``real``    default: ``value inherited from b2ah.dat (or b2mn.dat if specified in b2cmpt block)``
    Multiplier to the electron heat flux limit.
    

  - ``CFLMI``  -     type: ``real``    default: ``value inherited from b2ah.dat (or b2mn.dat if specified in b2cmpt block)``
    Multiplier to the ion heat flux limit.
    

  - ``CFLMV``  -     type: ``real``    default: ``value inherited from b2ah.dat (or b2mn.dat if specified in b2cmpt block)``
    Multiplier to the viscous heat flux limit.
    

  - ``CFLAL``  -     type: ``real``    default: ``value inherited from b2ah.dat (or b2mn.dat if specified in b2cmpt block)``
    Multiplier to the thermo-electric coefficient flux limit.
    

  - ``CFLAB``  -     type: ``real``    default: ``value inherited from b2ah.dat (or b2mn.dat if specified in b2cmpt block)``
    Multiplier to the friction force flux limit.
    


    For all flux limit multipliers, setting them to zero turns off the corresponding flux limiter. Otherwise, the multipliers must be positive.
    
.. index::
   single: CFL*; CFLME
   single: CFL*; CFLMI
   single: CFL*; CFLMV
   single: CFL*; CFLAL
   single: CFL*; CFLAB


.. index:: WRITE_NML_TRANSP

``WRITE_NML_TRANSP``    type: ``logical``    default: ``.true.``
    If .true. (default), writes the content of the namelist to stdout after it has been read.
    

.. index:: *_CNV

.. index:: VOUT_CNV, PW0_CNV, PW1_CNV, PW2_CNV
.. c

``*_CNV``

  - ``VOUT_CNV``  -     type: ``real array of size (0:NS-1)``    default: ``0.0``
    Value of the "blob" convection velocity for species (is) at the outer grid edge (in m/s).
    

  - ``PW0_CNV``  -     type: ``real array of size (0:NS-1)``    default: ``1.0``
    Exponent in radial profile of the "blob" velocity for species (is).
    

  - ``PW1_CNV``  -     type: ``real array of size (0:NS-1)``    default: ``5.0``
    First exponent in poloidal profile of the "blob" velocity for species (is).
    

  - ``PW2_CNV``  -     type: ``real array of size (0:NS-1)``    default: ``2.0``
    Second exponent in a poloidal profile of the "blob" velocity for species (is).
    


    The four \*\_CNV parameters are only activated if 'b2tqna\_user\_transport' is set to '6'.
    
.. index::
   single: *_CNV; VOUT_CNV
   single: *_CNV; PW0_CNV
   single: *_CNV; PW1_CNV
   single: *_CNV; PW2_CNV


.. index:: 
   single: b2.transport.parameters; FLAG*
   single: b2.transport.parameters; PARM_DNA
   single: b2.transport.parameters; PARM_DPA
   single: b2.transport.parameters; PARM_VLA
   single: b2.transport.parameters; PARM_VSA
   single: b2.transport.parameters; PARM_HCI
   single: b2.transport.parameters; PARM_HCE
   single: b2.transport.parameters; PARM_SIG
   single: b2.transport.parameters; PARM_ALF
   single: b2.transport.parameters; TRANSPORT_FILENAME
   single: b2.transport.parameters; TRANSPORT_TIME_MOD
   single: b2.transport.parameters; TRANSPORT_TIME_SWITCH
   single: b2.transport.parameters; CFL*
   single: b2.transport.parameters; WRITE_NML_TRANSP
   single: b2.transport.parameters; *_CNV

.. index:: b2.user.parameters

b2.user.parameters
==================
.. index:: RZOMP

``RZOMP``    type: ``real array of size (2,2)``    default: ``0.0``
    Coordinates defining a segment. All control volumes intersected by this segment will be part of the outer midplane.
    rzomp(1,1:2) holds the R-coordinates of the first and second point of the segment.
    rzomp(2,1:2) holds the Z-coordinates of the first and second point of the segment.
    Warning! This variable needs always be defined for SOLPS-ITER version 3.2.0 or younger!
    

.. index:: RZIMP

``RZIMP``    type: ``real array of size (2,2)``    default: ``0.0``
    Coordinates defining a segment. All control volumes intersected by this segment will be part of the inner midplane.
    rzimp(1,1:2) holds the R-coordinates of the first and second point of the segment.
    rzimp(2,1:2) holds the Z-coordinates of the first and second point of the segment.
    

.. index:: LHETRGTS

``LHETRGTS``    type: ``integer array of size (NLIM)``    default: ``Eirene recycling target surfaces defined in the LTNS array``
    List of surface indices (EIRENE notation) which are used for calculation of helium enrichment.
    

.. index:: LPFRB_I

``LPFRB_I``    type: ``integer``    default: ``0``
    Obsolete. Use PFR\_CVS instead.
    B2.5 x-cell index corresponding to the first edge of the bypass between the inner and outer divertor (Western divertor, edge closest to target). If non-positive, counted backwards from the X-point location in the lower PFR, from the inner upper target in the upper PFR, from the lower outer target in the outer SOL, and from the inner upper target in the inner SOL.
    

.. index:: LPFRB_O

``LPFRB_O``    type: ``integer``    default: ``0``
    Obsolete. Use PFR\_CVS instead.
    B2.5 x-cell index corresponding to the first edge of the bypass between the inner and outer divertor (Eastern divertor, edge closest to target). If non-positive, counted backwards from the outer lower target in the lower PFR, from the lower outer target in the outer SOL, from the upper outer target in the upper PFR, and from the inner upper target in the inner SOL.
    

.. index:: LPFRT_I

``LPFRT_I``    type: ``integer``    default: ``0``
    Obsolete. Use PFR\_CVS instead.
    B2.5 x-cell index corresponding to the second edge of the bypass between the inner and outer divertor (Western divertor, edge furthest to target). If non-positive, counted backwards from the X-point location in the PFR, from the outer target in the outer SOL for a SN, from the top targets in the SOL for a DN.
    

.. index:: LPFRT_O

``LPFRT_O``    type: ``integer``    default: ``0``
    Obsolete. Use PFR\_CVS instead.
    B2.5 x-cell index corresponding to the second edge of the bypass between the inner and outer divertor (Eastern divertor, edge furthest to target). If non-positive, counted backwards from the X-point location in the PFR, from the outer target in the outer SOL for a SN, from the top targets in the SOL for a DN.
    

.. index:: J_HE_AT

``J_HE_AT``    type: ``integer``
    Species index of the helium atoms in Eirene. The code attempts to find a match by default.
    

.. index:: J_NE_AT

``J_NE_AT``    type: ``integer``
    Species index of the neon atoms in Eirene. The code attempts to find a match by default.
    

.. index:: J_H_AT

``J_H_AT``    type: ``integer array of size (3)``
    Species indices of the hydrogen isotopes in Eirene. If using only one hydrogen species, only the first element needs to be provided. Otherwise the 3 elements correspond to H/D/T. The code attempts to find a match by default.
    

.. index:: L_H_MOL

``L_H_MOL``    type: ``integer array of size (NMOL,3)``
    Number of hydrogen isotope nuclei for molecules in Eirene. If using only one hydrogen species, only the first element needs to be provided. Otherwise the 3 elements correspond to H/D/T. The code attempts to find a match by default.
    

.. index:: FUSION_POWER

``FUSION_POWER``    type: ``real``    default: ``0.0``
    Fusion power occuring in core (including neutrons, in Megawatts).
    

.. index:: SPMP_HE_TO_D

``SPMP_HE_TO_D``    type: ``real``    default: ``1.0``
    Ratio of He to DT pumping speeds (typically, 0.8).
    

.. index:: LPFRS_PMP

``LPFRS_PMP``    type: ``integer``    default: ``0``
    Location of the pump. 0 no pump at all (default), 1 - SN of lower DN PFR, 2 - (outer) SOL, 3 - upper DN PFR, 4 - inner SOL for DN
    

.. index:: NPFRGRP

``NPFRGRP``    type: ``integer``    default: ``0``
    Actual number of surface groups for PFR flows.
    

.. index:: LPFRGRP

``LPFRGRP``    type: ``integer array of size (NLIM)``
    List of surface segments for PFR flows.
    

.. index:: IPFRGRP

``IPFRGRP``    type: ``integer array of size (NPFRGRP)``    default: ``0``
    First positions in this list for each group.
    

.. index:: JPFRGRP

``JPFRGRP``    type: ``integer array of size (NPFRGRP)``    default: ``0``
    Last positions in this list for each group.
    

.. index:: GPFRGRP

``GPFRGRP``    type: ``character*8 array of size (NPFRGRP)``    default: `` ``
    Labels for surface groups for PFR flows.
    

.. index:: NNTRGRP

``NNTRGRP``    type: ``integer``
    Actual number of surface groups for neutral data.
    

.. index:: LNTRGRP

``LNTRGRP``    type: ``integer array of size (NLIM)``
    List of surface segments for neutral data.
    

.. index:: INTRGRP

``INTRGRP``    type: ``integer array of size (NNTRGRP)``
    First positions in this list for each group.
    

.. index:: JNTRGRP

``JNTRGRP``    type: ``integer array of size (NNTRGRP)``
    Last positions in this list for each group.
    

.. index:: GNTRGRP

``GNTRGRP``    type: ``character*8 array of size (NNTRGRP)``
    Labels for the neutral data surface groups.
    

.. index:: NPFR_CVS

``NPFR_CVS``    type: ``integer``    default: ``0``
    Number of control volumes which are written in PFR\_CVS.
    

.. index:: PFR_CVS

``PFR_CVS``    type: ``integer array of size (100)``    default: ``0``
    List of control volumes over which the average neutral pressure for fb\_type.eq.20 is calculated.
    

.. index:: SPMP_NOM

``SPMP_NOM``    type: ``real``    default: ``0.0``
    Nominal pumping speed.
    

.. index:: TE_DET_THRESHOLD

``TE_DET_THRESHOLD``    type: ``real``    default: ``2.0``
    Electron temperature at the target (in eV) which is used a threshold identifying the transition of the local magnetic flux tube to detachment. The width of the zone with Te less than TE\_DET\_THRESHOLD (counted from the strike point towards the SOL side) is outputted into user\_SPb.trc. This distance monotonically increases with increasing of radiated power fraction or with decreasing of peak target energy loads, therefore it may be used as a measure of the degree of detachment.
    

.. index:: Q95_ALBLL

``Q95_ALBLL``    type: ``real``    default: ``0.0``
    Safety factor used to estimate the ballooning "alpha" parameter, if not assigned will be estimated as L\_conn/(2\*pi\*R) at the core interface.
    

.. index:: R0_ALBLL

``R0_ALBLL``    type: ``real``    default: ``0.0``
    Major radius used to estimate the ballooning "alpha" parameter. If not assigned, will be estimated as 0.5\*(Rmin-Rmax) at the core interface.
    

.. index:: B0_ALBLL

``B0_ALBLL``    type: ``real``    default: ``0.0``
    Magnetic field used to estimate the ballooning "alpha" parameter. If not assigned, will be estimated as Bomp\*R0/Romp at the core interface.
    

.. index:: TRGSHP

``TRGSHP``    type: ``real array of size (NTRGTS)``    default: ``1.0``
    Target shaping factor applied to plasma heat loads in peak heat flux estimate calculated by b2mod\_usertrc.
    

.. index:: FILEDATA

``FILEDATA``    type: ``logical array of size 10``    default: ``.true.``
    Switches to turn on/off the tracing files controlled by the ank\_tracing switch. The files are defined in b2mod\_diag, in order, starting with element 2 of the filedata array: test.trc, residuals.trc, sources.trc, blnn.trc, blne.trc, integral.trc, user.trc, blnm.trc, sepdata.trc.
    If there is no b2.user.parameters file present, the flags for user.trc are set to .false..
    If the tracing files are to be appended but a reading error occurs when opening them, the corresponding filedata element is overwritten to .false..
    

.. index:: USER_FILENAME

``USER_FILENAME``    type: ``character*80``    default: ``b2.user.parameters``
    Filename where /USER/ namelist is stored.
    

.. index:: 
   single: b2.user.parameters; RZOMP
   single: b2.user.parameters; RZIMP
   single: b2.user.parameters; LHETRGTS
   single: b2.user.parameters; LPFRB_I
   single: b2.user.parameters; LPFRB_O
   single: b2.user.parameters; LPFRT_I
   single: b2.user.parameters; LPFRT_O
   single: b2.user.parameters; J_HE_AT
   single: b2.user.parameters; J_NE_AT
   single: b2.user.parameters; J_H_AT
   single: b2.user.parameters; L_H_MOL
   single: b2.user.parameters; FUSION_POWER
   single: b2.user.parameters; SPMP_HE_TO_D
   single: b2.user.parameters; LPFRS_PMP
   single: b2.user.parameters; NPFRGRP
   single: b2.user.parameters; LPFRGRP
   single: b2.user.parameters; IPFRGRP
   single: b2.user.parameters; JPFRGRP
   single: b2.user.parameters; GPFRGRP
   single: b2.user.parameters; NNTRGRP
   single: b2.user.parameters; LNTRGRP
   single: b2.user.parameters; INTRGRP
   single: b2.user.parameters; JNTRGRP
   single: b2.user.parameters; GNTRGRP
   single: b2.user.parameters; NPFR_CVS
   single: b2.user.parameters; PFR_CVS
   single: b2.user.parameters; SPMP_NOM
   single: b2.user.parameters; TE_DET_THRESHOLD
   single: b2.user.parameters; Q95_ALBLL
   single: b2.user.parameters; R0_ALBLL
   single: b2.user.parameters; B0_ALBLL
   single: b2.user.parameters; TRGSHP
   single: b2.user.parameters; FILEDATA
   single: b2.user.parameters; USER_FILENAME

.. index:: b2.optimization.parameters

b2.optimization.parameters
==========================
.. index:: NCF

``NCF``    type: ``integer``    default: ``0``
    Number of cost functions (icf = 1, NCF).
    

.. index:: CFTYPE

``CFTYPE``    type: ``integer array of size (NCF)``    default: ``-1``
    Specifies the type of cost function for index icf. Valid options are:
    0 - Sum of weighted least squares cost functions. CFSTART, CFEND indicate over which icf indexes the cost functions are to be summed (valid indexes are 1-3 and 7-9).
    1 - Difference, on the desired CVs, of calculated electron density and experimental values read from file, normalized with average experimental value  (units must be 10^{19}m^{-3}).
    2 - Difference, on the desired CVs, of calculated electron temperature and values read from file, normalized with average experimental value (units must be eV).
    3 - Difference, on the desired CVs, of calculated ion temperature and values read from file, normalized with average experimental value (units must be eV).
    4 - Maximum electron temperature on the desired CVs (output in eV).
    5 - Maximum heat flux on the desired FCs (output in W^{2}/m^{2}).
    6 - Bayesian MAP cost function. CFSTART, CFEND indicate over which icf indexes the cost functions are to be summed (valid indexes are 1-3 and 7-9).
    7 - Difference, on the desired CVs, of calculated electron density radial gradient and experimental values read from file, normalized with average experimental value  (units must be 10^{19}m^{-4}).
    8 - Difference, on the desired CVs, of calculated electron temperature radial gradient and values read from file, normalized with average experimental value (units must be eV/m).
    9 - Difference, on the desired CVs, of calculated ion temperature radial gradient and values read from file, normalized with average experimental value (units must be eV/m).
    10 - Difference, on the desired CVs, of calculated ion saturation current (as ne\*cs\*eV) and values read from file, normalized with average experimental value (units must be kA/m^{2}).
    11 - Heat flux peakedness on the desired FCs (output in W^{2}/m^{2}).
    12 - Difference, on the desired FCs, of calculated perpendicular or parallel heat flux and values read from file, normalized with average experimental value (units must be in MW^{2}/m^{2}). Use PARALLEL\_HF to specify whehter the parallel or perpendicular heat flux is used.
    

.. index:: PARALLEL_HF

``PARALLEL_HF``    type: ``logical``    default: ``TRUE``
    Indicates for cost function 12 if the heat flux considered is the one parallel to the magnetic field (TRUE) or perpendicular to the surface (FALSE).
    

.. index:: CFDEF

``CFDEF``    type: ``integer array of size (NCF)``    default: ``0``
    Indicates how the domain of cost function ifc is specified. Valid options are:
    1 - The cost function is defined on the OMP, using the rzomp array. In this case CFSTART,CFEND are not necessary and ignored.
    2 - The cost function is defined using the FC labels specified in CFSTART,CFEND. Cost functions requiring CVs or FCs can both be defined in this way.
    3 - The cost function is defined using the CV labels specified in CFSTART,CFEND. Only cost functions requiring CVs can be defined in this way.
    4 - The cost function is defined using the CF\_REG and CF\_REGP arrays. Cost functions requiring CVs or FCs can both be defined in this way.
    

.. index:: CFSTART, CFEND

``CFSTART, CFEND``    type: ``integer arrays of size (NCF)``    default: ``0``
    Specify the starting/ending, face (FC) label fcLbl or control volume (CV) label cvLbl where the cost function icf will be evaluated. For CFTYPE = 0 and CFTYPE = 6 they instead identify which cost functions will be summed together.
    

.. index:: CF_REG

``CF_REG``    type: ``integer array of size (mxnCf)``    default: ``0``
    Listing for each cost function the corresponding domain CVs or FCs. WARNING! No attempt is made to check if these CVs or FCs are connected, sorted or even available in the current geometry: it is up to the user to make sure the list is correct. mxnCf is a hard coded maximum length defined in b2mod\_par\_opt.
    

.. index:: CF_REGP

``CF_REGP``    type: ``integer array of size (NCF, 2)``    default: ``0``
    CF\_REGP(icf, 1) points, for cost function icf, to the first index in the CF\_REG list.
    CF\_REGP(icf, 2) number of items in CF\_REG list for cost function icf.
    

.. index:: CFWEIGHT

``CFWEIGHT``    type: ``real array of size (NCF)``    default: ``1.0``
    Multipliers to re-scale each cost function separately.
    

.. index:: MapToOMP

``MapToOMP``    type: ``logical array of size (NCF)``    default: ``FALSE``
    Indicates if cost function icf is to be re-mapped to the OMP, according to CFTYPE.
    Warning! The mapping is a rigid translation of the data to the OMP and is safe to work only for non-extended grids and for cost functions defined on the same number of elements as the OMP list.
    

.. index:: NSIGMA

``NSIGMA``    type: ``integer``    default: ``0``
    Number of standard deviation variables used for Bayesian MAP cost function (normally this should be equal to the number of cost functions summed for CFTYPE = 6, i.e. one for each variable on each domain) (isigma = 1, NSIGMA}).
    

.. index:: SIGMA

``SIGMA``    type: ``real array of size (NSIGMA)``    default: ``0.0``
    Value of the prediction error standard deviation. For absolute STD the units are the same as the experimental data used for the cost function it refers to.
    

.. index:: SCALE_SIGMA

``SCALE_SIGMA``    type: ``logical array of size (NSIGMA)``    default: ``TRUE``
    Indicates if SIGMA(isigma) is intended as relative standard deviation (SCALE\_SIGMA(isigma)=.TRUE.) or absolute (SCALE\_SIGMA(isigma)=.FALSE.).
    

.. index:: READ_SIGMA

``READ_SIGMA``    type: ``logical array of size (NSIGMA)``    default: ``FALSE``
    (Experimental! Do not use!) Specifies if sigma can be read from the experimental data files cfi.dat.
    

.. index:: NMEAN

``NMEAN``    type: ``integer``    default: ``0``
    Number of predictin error mean variables used for Bayesian MAP cost function.
    

.. index:: MEAN

``MEAN``    type: ``real*8 array of size (NMEAN)``    default: ``0.0``
    Value of the predictin error mean.
    

.. index:: PRIOR_TYPE

``PRIOR_TYPE``    type: ``integer array of size (NNVAR)``    default: ``-1``
    Defines the type of prior distribution for each parameter for the MAP cost function. Possible values are:
    0 - Uniform distribution (i.e. $\pi(\theta)=1.0$).
    1 - Uninformative Gaussian prior.
    2 - Gamma distribution, defined through mean and standard deviation.
    

.. index:: PRIOR_PAR

``PRIOR_PAR``    type: ``real array of size (NNVAR,2)``    default: ``-1.0``
    Indicates parameters for the prior distributions.
    For PRIOR\_TYPE=0, not used.
    For PRIOR\_TYPE=1 and 2, PRIOR\_TYPE(ii,1) indicates the mean and PRIOR\_TYPE(ii,2) indicates the standard deviation of the distribution.
    

.. index:: PRIOR_RANGE

``PRIOR_RANGE``    type: ``real array of size (NNVAR,2)``    default: ``10*p_infty``
    Indicates the valid range for the prior distributions, outside of which the program will return an infinite cost function value. PRIOR\_RANGE(:,1) sets the lower range and PRIOR\_RANGE(:,2) sets the upper range. (p\_infty is a parameter currently set to 1e30).
    

.. index:: SHIFT_CF_DATA

``SHIFT_CF_DATA``    type: ``integer array of size (NCF)``    default: ``0``
    For each cost function where experimental data is read, specifies whether or not to shift the separatrix position in the experimental data spatial coordinate as follows: (r - r\_{sep}) - SHIFT\_VALUE$. Unique integers larger than zero for each cost function means that each has its specific shift value. Using the same integer for two (or more) cost functions makes to code use the same shift value for those cost functions (the first SHIFT\_VALUE among the cost function with the same integer is adopted). Possible usage: Thomson scattering data of density and temperature which should be defined in two separate cost functions but come from the same source and thus have the same shift. NSHIFT is then the number of unique integers and is used to define other parameters below other parameters.
    

.. index:: SHIFT_VALUE

``SHIFT_VALUE``    type: ``real*8 array of size (NCF)``    default: ``0.0``
    Defines the value of the shift in millimeters for each cost function with SHIFT\_CF\_DATA .neq. 0. Tis is also used as initial guess in case of optimization.
    

.. index:: SHIFT_PRIOR_TYPE

``SHIFT_PRIOR_TYPE``    type: ``integer array of size (NSHIFT)``    default: ``-1``
    Same as PRIOR\_TYPE but defined for each unique cost function shift.
    

.. index:: SHIFT_PRIOR_PAR

``SHIFT_PRIOR_PAR``    type: ``real*8 array of size (NSHIFT,2)``    default: ``-1.0``
    Same as PRIOR\_PAR but defined for each unique cost function shift.
    

.. index:: SHIFT_PRIOR_RANGE

``SHIFT_PRIOR_RANGE``    type: ``real*8 array of size (NSHIFT,2)``    default: ``10*p_infty``
    Same as PRIOR\_RANGE but defined for each unique cost function shift.
    

.. index:: CORR_MODEL

``CORR_MODEL``    type: ``integer array of size (NCF)``    default: ``0``
    Specifies the type of correlation model for the covariance matrix in the MAP cost function.Possible values are:
    0 - No correlation, thus simple diagonal covariance matrix.
    1 - Correlation model based on exponential decay with a correlation length specified using CORR\_LENGTH.
    

.. index:: CORR_LENGTH

``CORR_LENGTH``    type: ``real*8 array of size (NCF)``    default: ``0.0``
    Defines the value of the correlation length in millimeters for each MAP-type cost function with CORR\_MODEL>0. This is also used as initial guess in case of optimization.
    

.. index:: CORR_CUTOFF

``CORR_CUTOFF``    type: ``real*8``    default: ``0.01``
    For the exponential decay correlation model, off-diagonal elements with value of the exponential below this threshold are set to zero.
    

.. index:: CORR_PRIOR_TYPE

``CORR_PRIOR_TYPE``    type: ``integer array of size (NCORR_OPT)``    default: ``-1``
    Same as PRIOR\_TYPE but defined for each MAP cost function where sensitivity for CORR\_LENGTH is calculated or this parameter optimized (see CORR\_OPT). NCORR\_OPT is the number of correlation lengths which are optimized, so for which a prior is required.
    

.. index:: CORR_PRIOR_PAR

``CORR_PRIOR_PAR``    type: ``real*8 array of size (NCORR_OPT,2)``    default: ``-1.0``
    Same as PRIOR\_PAR but defined for each MAP cost function where sensitivity for CORR\_LENGTH is calculated or this parameter optimized.
    

.. index:: CORR_PRIOR_RANGE

``CORR_PRIOR_RANGE``    type: ``real*8 array of size (NCORR_OPT,2)``    default: ``10*p_infty``
    Same as PRIOR\_RANGE but defined for each MAP cost function where sensitivity for CORR\_LENGTH is calculated or this parameter optimized.
    

.. index:: NNVAR

``NNVAR``    type: ``integer``    default: ``0``
    Number of sensitivity/optimization parameters (radially varying transport coefficients count as 1).
    

.. index:: PARTYPE

``PARTYPE``    type: ``integer array of size (NNVAR)``    default: ``-2``
    Indicates the type of sensitivity/optimization parameter. Valid options are:
    -1 - mean, error mean in likelihood function for Bayesian inference (one for each plasma quantity and location used). If present, these must ALWAYS be the last parameters in the vector!
    0 - sigma, standard deviation in likelihood function for Bayesian inference (one for each plasma quantity and location used). If present, these must ALWAYS be defined after each physical parameter (PARTYPE>0) and before the mean (PARTYPE=-1).
    1 - parm\_dna or tdata(:,:,1,:)
    2 - parm\_dpa or tdata(:,:,2,:)
    3 - parm\_hci or tdata(:,:,3,:)
    4 - parm\_hce or tdata(:,:,4,:)
    5 - tdata(:,:,5,:) (not yet tested!)
    6 - parm\_vla or tdata(:,:,6,:)
    7 - parm\_vsa or tdata(:,:,7,:)
    8 - parm\_sig or tdata(:,:,8,:)
    9 - parm\_alf or tdata(:,:,9,:)
    10 - enepar
    11 - enipar
    12 - conpar
    13 - mompar
    14 - potpar
    15 - enkpar
    16 - b2recyc
    17 - b2tqna\_ballooning
    18 - b2tqna\_ballooning\_rescale
    19 - keps\_cd
    20 - keps\_heat
    21 - keps\_heat\_i
    22 - keps\_sig
    23 - keps\_alf
    24 - keps\_visc
    25 - keps\_dkt
    26 - keps\_dzt
    27 - b2sikt\_fac\_diss
    28 - b2sikt\_fac\_diss\_core
    29 - b2sikt\_fac\_sheath
    30 - b2sikt\_fac\_sheath\_core
    31 - keps\_shear
    32 - b2tfhi\_fsigkt
    33 - b2sikt\_fac\_vis\_RS
    34 - b2tfhi\_fflokt
    35 - b2tfhi\_fconkt
    36 - b2tfhi\_fflozt
    37 - b2tfhi\_fconzt
    38 - b2tfhi\_fkt\_hie
    39 - b2tfhe\_vis\_kt
    

.. index:: SIGMA_OPT

``SIGMA_OPT``    type: ``logical array of size (NSIGMA)``    default: ``.true.``
    For each sigma, specifies whether its sensitivity is computed or not, and thus whether it is optimized or fixed.
    

.. index:: MEAN_OPT

``MEAN_OPT``    type: ``logical array of size (NMEAN)``    default: ``.false.``
    For each mean, specifies whether its sensitivity is computed or not, and thus whether it is optimized or fixed.
    

.. index:: SHIFT_OPT

``SHIFT_OPT``    type: ``logical array of size (NSHIFT)``    default: ``.false.``
    For each SHIFT\_CF\_VALUE, specifies whether its sensitivity is computed or not, and whether is optimized or fixed.
    

.. index:: CORR_OPT

``CORR_OPT``    type: ``logical array of size (NCF)``    default: ``.false.``
    For each MAP cost function where CORR\_MODEL>0, specifies whether CORR\_LENGTH sensitivity is computed or not, and whether is optimized or fixed.
    

.. index:: SPATIAL_DEP

``SPATIAL_DEP``    type: ``logical array of size (NNVAR)``    default: ``.false.``
    For each sensitivity/optimization variables, specifies if radially varying coefficients are optimized.
    Meaningful only for partype = 1 to 9.
    

.. index:: SPATIAL_POINTS

``SPATIAL_POINTS``    type: ``integer array of size (NNVAR)``    default: ``0``
    Number of spatial points for sensitivity/optimization parameter ipar (should be the same as ndata in b2.transport.inputfile). The actual number of optimized variables (NPAR\_OPT) is then equal to the total number of spatial points + any other additional parameter.
    

.. index:: PARIS

``PARIS``    type: ``integer array of size (NNVAR)``    default: ``0``
    Specifies the species of the sensitivity/optimization parameter. Only meaningful for partype = [1-3,5,7,12,13,16].
    

.. index:: PARIB

``PARIB``    type: ``integer array of size (NNVAR)``    default: ``0``
    Specifies the boundary/strata of the sensitivity/optimization parameter. Only meaningful for partype = [10-16].
    

.. index:: PAR_RESCALE

``PAR_RESCALE``    type: ``real array of size (NPAR_OPT)``    default: ``1.0``
    Coefficient to rescale optimization parameters (and their gradient). Note dimension is NPAR\_OPT, so need to specify it also for each point in case of spatially varying coefficients.
    

.. index:: X0

``X0``    type: ``real array of size (NPAR_OPT)``    default: ``10*p_infty``
    Initial guess for each optimization parameter. Must be defined (p\_infty is a parameter currently set to 1e30).
    

.. index:: XL

``XL``    type: ``real array of size (NPAR_OPT)``    default: ``-10*p_infty``
    Lower bound for each optimization parameter.
    

.. index:: XU

``XU``    type: ``real array of size (NPAR_OPT)``    default: ``10*p_infty``
    Upper bound for each optimization parameter.
    

.. index:: SHIFT_L

``SHIFT_L``    type: ``real*8 array of size (NCF)``    default: ``-1000.0``
    Lower bound for SHIFT\_CF\_DATA parameters.
    

.. index:: SHIFT_U

``SHIFT_U``    type: ``real*8 array of size (NCF)``    default: ``1000.0``
    Upper bound for SHIFT\_CF\_DATA parameters.
    

.. index:: CORR_L

``CORR_L``    type: ``real*8 array of size (NCF)``    default: ``-10*p_infty``
    Lower bound for CORR\_LENGTH parameters. Must be specified for each cost function!
    

.. index:: CORR_U

``CORR_U``    type: ``real*8 array of size (NCF)``    default: ``10*p_infty``
    Upper bound for CORR\_LENGTH parameters. Must be specified for each cost function!
    

.. index:: CORR_RESCALE

``CORR_RESCALE``    type: ``real*8 array of size (NCF)``    default: ``1.0``
    Same as PAR\_RESCALE but defined for CORR\_LENGTH} parameters. Must be specified for each cost function!
    

.. index:: MAXITER

``MAXITER``    type: ``integer``    default: ``100``
    Maximum number of optimization iterations. Can overridden with PETCs/Tao by using command line options for the optimization.
    

.. index:: CPU_OPT

``CPU_OPT``    type: ``real``    default: ``0.0``
    Maximum amount of CPU time in seconds after which the optimization is stopped.
    

.. index:: TOL_OPT

``TOL_OPT``    type: ``real``    default: ``1.0e-7``
    Tolerance below which optimization is stopped. For PETCs/Tao it is used for the absolute gradient norm, the relative gradient norm, and the gradient reduction stopping criteria. Can be overridden with PETCs/Tao by using command line options for the optimization.
    

.. index:: HESSIAN_APPROXIMATION

``HESSIAN_APPROXIMATION``    type: ``character*256``    default: ``'limited-memory'``
    Type of Hessian approximation employed. Depends on optimization library. Possible values are currently: 'limited-memory' and 'exact'. When using the 'exact' option the steepest descent algorithm is used.
    

.. index:: LIMITED_MEMORY_UPDATE_TYPE

``LIMITED_MEMORY_UPDATE_TYPE``    type: ``character*256``    default: ``'bfgs'``
    Specifies which kind of Hessian approximation is employed if HESSIAN\_APPROXIMATION is set to 'limited-memory'. Can overridden with PETCs/Tao by using command line options for the optimization.
    

.. index:: 
   single: b2.optimization.parameters; NCF
   single: b2.optimization.parameters; CFTYPE
   single: b2.optimization.parameters; PARALLEL_HF
   single: b2.optimization.parameters; CFDEF
   single: b2.optimization.parameters; CFSTART, CFEND
   single: b2.optimization.parameters; CF_REG
   single: b2.optimization.parameters; CF_REGP
   single: b2.optimization.parameters; CFWEIGHT
   single: b2.optimization.parameters; MapToOMP
   single: b2.optimization.parameters; NSIGMA
   single: b2.optimization.parameters; SIGMA
   single: b2.optimization.parameters; SCALE_SIGMA
   single: b2.optimization.parameters; READ_SIGMA
   single: b2.optimization.parameters; NMEAN
   single: b2.optimization.parameters; MEAN
   single: b2.optimization.parameters; PRIOR_TYPE
   single: b2.optimization.parameters; PRIOR_PAR
   single: b2.optimization.parameters; PRIOR_RANGE
   single: b2.optimization.parameters; SHIFT_CF_DATA
   single: b2.optimization.parameters; SHIFT_VALUE
   single: b2.optimization.parameters; SHIFT_PRIOR_TYPE
   single: b2.optimization.parameters; SHIFT_PRIOR_PAR
   single: b2.optimization.parameters; SHIFT_PRIOR_RANGE
   single: b2.optimization.parameters; CORR_MODEL
   single: b2.optimization.parameters; CORR_LENGTH
   single: b2.optimization.parameters; CORR_CUTOFF
   single: b2.optimization.parameters; CORR_PRIOR_TYPE
   single: b2.optimization.parameters; CORR_PRIOR_PAR
   single: b2.optimization.parameters; CORR_PRIOR_RANGE
   single: b2.optimization.parameters; NNVAR
   single: b2.optimization.parameters; PARTYPE
   single: b2.optimization.parameters; SIGMA_OPT
   single: b2.optimization.parameters; MEAN_OPT
   single: b2.optimization.parameters; SHIFT_OPT
   single: b2.optimization.parameters; CORR_OPT
   single: b2.optimization.parameters; SPATIAL_DEP
   single: b2.optimization.parameters; SPATIAL_POINTS
   single: b2.optimization.parameters; PARIS
   single: b2.optimization.parameters; PARIB
   single: b2.optimization.parameters; PAR_RESCALE
   single: b2.optimization.parameters; X0
   single: b2.optimization.parameters; XL
   single: b2.optimization.parameters; XU
   single: b2.optimization.parameters; SHIFT_L
   single: b2.optimization.parameters; SHIFT_U
   single: b2.optimization.parameters; CORR_L
   single: b2.optimization.parameters; CORR_U
   single: b2.optimization.parameters; CORR_RESCALE
   single: b2.optimization.parameters; MAXITER
   single: b2.optimization.parameters; CPU_OPT
   single: b2.optimization.parameters; TOL_OPT
   single: b2.optimization.parameters; HESSIAN_APPROXIMATION
   single: b2.optimization.parameters; LIMITED_MEMORY_UPDATE_TYPE

.. index:: b2.sputter_save.parameters

b2.sputter_save.parameters
==========================
.. index:: NX_SP

``NX_SP``    type: ``integer``    default: ``nx``
    Array dimension NX used in this namelist.
    

.. index:: NY_SP

``NY_SP``    type: ``integer``    default: ``ny``
    Array dimension NY used in this namelist.
    

.. index:: NS_SP

``NS_SP``    type: ``integer``    default: ``ns``
    Array dimension NS used in this namelist.
    

.. index:: SPUTTER_YIELD

``SPUTTER_YIELD``    type: ``real array of size (-1:NX,-1:NY,0:NS-1,1:2)``    default: ``0.0``
    Contains the chemical sputtering yield of species (is) at position (ix,iy) in element (:,:,:,1) and the physical sputtering yield in element (:,:,:,2).
    

.. index:: SPUTTER_YIELD2

``SPUTTER_YIELD2``    type: ``real array of size (-1:NX,-1:NY,0:NS-1,1:2)``    default: ``0.0``
    Contains the energy chemical sputtering yield of species (is) at position (ix,iy) in element (:,:,:,1) and the energy physical sputtering yield in element(:,:,:,2).
    

.. index:: 
   single: b2.sputter_save.parameters; NX_SP
   single: b2.sputter_save.parameters; NY_SP
   single: b2.sputter_save.parameters; NS_SP
   single: b2.sputter_save.parameters; SPUTTER_YIELD
   single: b2.sputter_save.parameters; SPUTTER_YIELD2

.. index:: b2.atomic_physics_rescale.parameters

b2.atomic_physics_rescale.parameters
====================================
.. index:: RESCALE_SA

``RESCALE_SA``    type: ``real array of size(0:NS-1)``    default: ``1.0``
    Scaling factors for rtsa: ionisation rates of species (is).
    

.. index:: RESCALE_RA

``RESCALE_RA``    type: ``real array of size(0:NS-1)``    default: ``1.0``
    Scaling factors for rtra: recombination rates of species (is).
    

.. index:: RESCALE_QA

``RESCALE_QA``    type: ``real array of size(0:NS-1)``    default: ``1.0``
    Scaling factors for rtqa: electron cooling rates of species (is).
    

.. index:: RESCALE_CX

``RESCALE_CX``    type: ``real array of size(0:NS-1)``    default: ``1.0``
    Scaling factors for rtcx: charge exchange rates of species (is).
    

.. index:: RESCALE_RD

``RESCALE_RD``    type: ``real array of size(0:NS-1)``    default: ``1.0``
    Scaling factors for rtrd: line radiation rates of species (is).
    

.. index:: RESCALE_BR

``RESCALE_BR``    type: ``real array of size(0:NS-1)``    default: ``1.0``
    Scaling factors for rtbr: bremsstrahlung radiation rates of species (is).
    

.. index:: 
   single: b2.atomic_physics_rescale.parameters; RESCALE_SA
   single: b2.atomic_physics_rescale.parameters; RESCALE_RA
   single: b2.atomic_physics_rescale.parameters; RESCALE_QA
   single: b2.atomic_physics_rescale.parameters; RESCALE_CX
   single: b2.atomic_physics_rescale.parameters; RESCALE_RD
   single: b2.atomic_physics_rescale.parameters; RESCALE_BR

