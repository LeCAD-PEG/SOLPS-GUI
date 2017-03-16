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
    atomic charge, nuclear charge, atomic mass and atomic charge squared for each charge stateminimum atomic charge of the stage, maximum atomic charge of the stage, nuclear charge, and atomic mass; this data should match that given in b2ah.dat
    

.. index:: naini

``naini``    type: ``None``    default: ``None``
    initial densities for each of the charge states, in m^-3
    

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
    specifies the number of regions where boundary conditions will be specified the 'south' boundary is broken into three pieces with one quarter of the cells in the first region, half ofthe cells in the second, and the remaining quarter in the third region (inner target private flux, core, outerprivate flux). This is geometry-dependent information the code will check against the mesh connectivity and return an error if the two do not match the 'north', 'west' and 'east' are not broken up, and correspond to the SOL boundary, inner target andouter target, respectively. For double-null cases, the north boundary should be split into two sections
    

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
    at least 100 additional numbers, of which only the first is relevant for us -1.0 read the mesh data using the "simplified" Carre format -2.0 read the mesh data using the Sonnet format
    

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

``b2agfs_geometry``    default: ``upgrade.geometry``
    local\_sonnet - character string.
    local\_sonnet is the file name of the geometry file to be read. 
    The file will be looked for in the run directory, in the ../baserun directory and in $SOLPSTOP/data/meshes. To be used in b2ag.dat.
    

.. index:: b2mwti_jxa

``b2mwti_jxa``    default: ``See description (integer)``
    jxa - integer. 
    Cell index, on the basis mesh, of the outer midplane. Default value depends on geometry: 
    Single-null : jxa=rightcut1(1)-(rightcut1(1)-leftcut1(1))/4, i.e. three quarters of the way between the two cuts. 
    Double-null : jxa=(rightcut1(1)+rightcut1(2))/2, i.e. halfway between the two outer cuts. Straight geometry : jxa=3\*nx/4
    

.. index:: b2mwti_jxi

``b2mwti_jxi``    type: ``integer``    default: ``See description (integer)``
    Cell index, on the basis mesh, of the inner midplane. Default value depends on geometry:
    Single-null : jxi=leftcut1(1)+(rightcut1(1)-leftcut1(1))/4, i.e. one quarter of the way between the two cuts. Double-null : jxi=(leftcut1(1)+leftcut1(2))/2, i.e. halfway between the two inner cuts.
    Straight geometry : jxi=nx/4
    

.. index:: b2agmx_pbs_from_basis_mesh

``b2agmx_pbs_from_basis_mesh``    type: ``integer``    default: ``1``
    If pbs\_from\_basis\_mesh.eq.0, the pbs array is computed from values on the actual working mesh (old treatment). 
    If pbs\_from\_basis\_mesh.eq.1, the pbs array is computed from values on the (possibly) finer basis mesh from the geometry file and the contributions from each basis cell are added to obtain the value on the working mesh.
    In both cases, mind the value of 'b2news\_area\_fix', which should be also declared in b2ag.dat if the non-default behaviour is wanted.
    

.. index:: b2agfs_periodic_bc

``b2agfs_periodic_bc``    type: ``integer``    default: ``0``
    periodic\_bc - integer. 
    periodic\_bc specifies if this is either an island or limiter geometry. 
    If periodic\_bc.eq.1 then island/limiter treatment is turned on. We differentiate between the two case through nncut: 
    nncut.eq.0 = limiter case 
    nncut.ge.1 = island divertor case (there should be nncut islands then)
    The case periodic\_bc.eq.-1 is used to remove tranverse physics in 1-D cases. 
    If periodic\_bc.eq.0 then we have the usual treatment. No other values are currently allowed. To be used in b2ag.dat.
    

.. index:: b2agsi_isymm

``b2agsi_isymm``    type: ``integer``    default: ``1``
    isymm - integer. 
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


    coreregno, coreregn2 - integers. coreregno is the boundary index of the core boundary in the input files b2ah.dat and b2mn.dat. For a standard single-null case, coreregno is 1. For a straight geometry or limiter case, it is likely that coreregno need be set to 0, depending on the actual geometry details. 
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


    pfrregno1, pfrregno2 - integers. 
    pfrregno1 is the boundary index of the first half of the private flux region boundary on which feedback is being applied (through b2stbc\_ndes or b2stbc\_private\_flux\_puff) in the input files b2ah.dat and b2mn.dat. pfrregno2 is the second half of the same private flux region. For a standard single null, the pair should be (0,2). For a standard double-null, the lower private flux region is labelled with the pair (0,5), and the upper private flux region with the pair (2,3). One can use only one private flux region by setting pfrregno1.eq.pfrregno2.
    
.. index::
   single: b2stbc_pfrregno*; b2stbc_pfrregno1
   single: b2stbc_pfrregno*; b2stbc_pfrregno2


.. index:: b2stbc_solregno

``b2stbc_solregno``    type: ``integer``    default: ``3``
    solregno - integer. 
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
    Bt\_adjust - integer.
    If the mesh is offset (See b2agfs\_xoffset, b2agfs\_yoffset below) and Bt\_adjust.eq.1, then the magnetic field is recomputed, keeping the pitch constant but changing the toroidal field magnitude according to Bt = Bt0/R. To be used in b2ag.dat.
    

.. index:: b2agfs_Bt_rescale

``b2agfs_Bt_rescale``    type: ``real``    default: ``1.0``
    Bt\_rescale - real\*8. 
    The magnetic field will be multiplied by Bt\_rescale. All components of the field are scaled together. To be used in b2ag.dat.
    

.. index:: b2agfs_pit_rescale

``b2agfs_pit_rescale``    type: ``real*8``    default: ``1.0``
    The magnetic field line pitch will be multiplied by pit\_rescale. 
    This means that the poloidal field component is multiplied by pit\_rescale, while the toroidal field component is left unchanged. To reverse the plasma current direction, set pit\_rescale to -1.0. 
    The sign convention used is that a positive poloidal field points in the direction of increasing <ix>. Be mindful however that, when inverting the sign of the poloidal magnetic field, you are also inverting the direction of the parallel velocity. You will then need to use the 'b2mndr\_inverse\_ua' switch to correct for that. To be used in b2ag.dat.
    

.. index:: b2agfs_Bt_reversal

``b2agfs_Bt_reversal``    type: ``integer``    default: ``0``
    Bt\_reversal - integer. If Bt\_reversal.eq.1, then the sign of the toroidal field component only is reversed. The sign convention used is that a positive toroidal field leads to a Bx(grad(B)) direction pointing down, so B is out of the page when looking at the usual view of the poloidal plane with the center line on the left. To be used in b2ag.dat.
    

.. index:: b2agfs_min_pitch

``b2agfs_min_pitch``    type: ``real``    default: ``1.0``
    Minimum allowed value for the pitch angle (in degrees) at the plates.
    

.. index:: b2agfs_.offset

.. index:: b2agfs_xoffset, b2agfs_yoffset
.. c

``b2agfs_.offset``

  - ``b2agfs_xoffset``  -     type: ``real``    default: ``0.0``

  - ``b2agfs_yoffset``  -     type: ``real``    default: ``0.0``


    xoffset, yoffset - real\*8. 
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


    yrescale - real\*8. 
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


.. index:: 
   single: Geometry; b2agfs_geometry
   single: Geometry; b2mwti_jxa
   single: Geometry; b2mwti_jxi
   single: Geometry; b2agmx_pbs_from_basis_mesh
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

.. index:: Run

Run
===
.. index:: b2mndr_id

.. index:: b2mndr_run_number, b2mndr_shot_number, b2mndr_device, b2mndr_user
.. c

``b2mndr_id``

  - ``b2mndr_run_number``  -     type: ``integer``    default: ``1000``

  - ``b2mndr_shot_number``  -     type: ``integer``    default: ``0``

  - ``b2mndr_device``  -     type: ``string``    default: ``$(DEVICE)``

  - ``b2mndr_user``  -     type: ``string``    default: ``$(USER)``


    These switches server as identification for the simulation. They can be inherited from SOLPS-GUI:
    Run number : The number of the run.
    Shot number : Shot number identifying the run. Defaults to the last number found in shotnumber.history, or 0 if the file is not found.
    Device : The device where the simulation was run.
    User : The user who ran the simulation.
    
.. index::
   single: b2mndr_id; b2mndr_run_number
   single: b2mndr_id; b2mndr_shot_number
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
    If set to a negative value, the run continues from the time read in b2fstati.
    

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
    |   ..compute source linearisation
    |   ..do i2=1,nstg2
    |    ..perform one inner iteration
    |    ..re-compute auxiliary quantities
    |    ..produce monitoring output
    |   ..enddo
    |  ..enddo
    | ..enddo

    This can be completed by the the 'b2mndt\_nstg\_ares??' switches.
    See 'Numerics' section for details.
    
.. index::
   single: b2mndt_nstg.; b2mndt_nstg0
   single: b2mndt_nstg.; b2mndt_nstg1
   single: b2mndt_nstg.; b2mndt_nstg2


.. index:: b2news_no_solve

``b2news_no_solve``    type: ``integer``    default: ``0``
    If no\_solve.eq.1, then the code is run without actually solving any equations. All secondary and dependent data is computed. 
    The nstg(0:2) array is overwritten to '1's. The simulation time will not be updated. The code will compute fluxes, sources, transport coefficients, etc... 
    'ntim' times but not update the basic plasma quantities. Additionally, if no\_solve is set to a negative value, then only some equations are solved (simulation time and nstg arrays will behave normally). 
    no\_solve.eq.-1 will activate the parallel momentum equations only. 
    no\_solve.eq.-2 will activate the density equations only. no\_solve.eq.-4 will activate the potential equation only. (Active only if poteq.eq.1, otherwise, the behaviour dictated by the poteq setting applies). 
    no\_solve.eq.-8 will activate the heat equations only. These can be combined. For example, no\_solve.eq.-3 will activate the parallel momentum and particle conservation equations. 
    If the no\_solve switch requires an equation not to be solved, the settings in the corresponding solvexx arrays from b2.numerics.parameters are moot. 
    The latter are reserved for fine-tuning numerical diagnostics.
    

.. index:: b2mndr_cpu

``b2mndr_cpu``    type: ``real``    default: ``0.0``
    CPU limit. If cpu.eq.0.0, no CPU limit is enforced. Otherwise, the code stops smoothly after it has been running for at least 'cpu' CPU seconds.
    

.. index:: b2mndr_elapsed

``b2mndr_elapsed``    type: ``real``    default: ``0.0``
    Elapsed time limit. Is elapsed.eq.0.0, no time limit is enforced.
    Otherwise, the code stops smoothly after is has been running for at least 'elapsed' wall clock seconds.
    

.. index:: b2mndr_savecpu

``b2mndr_savecpu``    type: ``real``    default: ``3600.0``
    CPU time interval after which save files plasmastate.xxxx are written. 
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


    Ramping parameters for facdrift, which multiplies the diamagnetic terms. The code is started on the first time step with facdrift=facdrift\_start. If facdrift\_target.ne.facdrift\_start, then, on each time step, facdrift is multiplied by facdrift\_inc. If the code does not converge on the timestep, facdrift is decreased by facdrift\_dec. A facdrift profile is also possible, see Numerics section for details.
    
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


    Ramping parameters for facExB, which multiplies the ExB terms. Same treatment as above for facdrift.
    
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


    Ramping parameters for facvis, which multiplies the drift viscosity terms. Same treatment as above for facdrift.
    
.. index::
   single: b2news_facvis_*; b2news_facvis_dec
   single: b2news_facvis_*; b2news_facvis_inc
   single: b2news_facvis_*; b2news_facvis_start
   single: b2news_facvis_*; b2news_facvis_target


.. index:: b2srdt_*_namelist

.. index:: b2stbc_boundary_namelist, b2stbr_neutrals_namelist, b2srdt_numerics_namelist, b2tqna_transport_namelist
.. c

``b2srdt_*_namelist``

  - ``b2stbc_boundary_namelist``  -     type: ``integer``    default: ``0``

  - ``b2stbr_neutrals_namelist``  -     type: ``integer``    default: ``0``

  - ``b2srdt_numerics_namelist``  -     type: ``integer``    default: ``0``

  - ``b2tqna_transport_namelist``  -     type: ``integer``    default: ``0``


    Namelist file indicators. If xxx\_namelist.eq.1, then the code looks for the file b2.xxx.parameters, in which it expects to find the xxx namelist.
    
.. index::
   single: b2srdt_*_namelist; b2stbc_boundary_namelist
   single: b2srdt_*_namelist; b2stbr_neutrals_namelist
   single: b2srdt_*_namelist; b2srdt_numerics_namelist
   single: b2srdt_*_namelist; b2tqna_transport_namelist


.. index:: b2sral_inputfile

``b2sral_inputfile``    default: ``0``
    Profiles file indicator. If b2sral\_inputfile.eq.1, then the code looks for the file b2.sources.profile in which it expects to find the 'profile' namelist. 
    This namelist will contain profiles of sources measured from the location (ixref,iyref) (default is outer midplane separatrix), which is set with the 'set\_transport\_i[xy]ref' switches.
    

.. index:: b2tqna_inputfile

``b2tqna_inputfile``    type: ``integer``    default: ``0``
    Profiles file indicator. If b2tqna\_inputfile.eq.1, then the code looks for the file b2.transport.inputfile, in which it expects to find the transport namelist. 
    This namelist will contain profiles of sources transport parameters measured from the location (ixref,iyref) (default is outer midplane separatrix), which is set with the 'set\_transport\_i[xy]ref' switches.
    

.. index:: b2mndr_eirene

``b2mndr_eirene``    type: ``integer``    default: ``0``
    Turns on coupling with the Eirene Monte-Carlo neutral code if nonzero. 
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
    Timestep index after which the feedback in b2stbc is activated.
    

.. index:: b2stbr_first_flight

``b2stbr_first_flight``    type: ``integer``    default: ``0``
    If first\_flight.ne.0, turns on the first flight model. See Physics section for additional details.
    

.. index:: b2ytdr_ns

``b2ytdr_ns``    type: ``integer``    default: ``ns``
    New number of species desired when creating a new initial state file using b2yt.exe. Must be specified within b2yt.dat.
    

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
   single: Run; b2ytdr_ndepth1
   single: Run; b2ytdr_rescale_neutrals
   single: Run; b2ytdr_non_commensurate

.. index:: Physics

Physics
=======
.. index:: b2siav_addvis

``b2siav_addvis``    type: ``real``    default: ``0.0``
    Multiplier to heat flux contribution to divergence of viscosity tensor in the momentum equation.
    

.. index:: b2siav_addvis1

``b2siav_addvis1``    type: ``real``    default: ``1.0``
    When not equal to '0.0', adds contribution to divergence of viscosity tensor coming from x-variations in B.
    

.. index:: b2npmo_b2sifr_

``b2npmo_b2sifr_``    type: ``integer``    default: ``1``
    When set to '1', the new correct form of the friction force is used. 
    The value '0' corresponds to the old SOLPS5.0 treatment.
    

.. index:: b2sihs_istyle_Joule_heating

``b2sihs_istyle_Joule_heating``    type: ``integer``    default: ``1``
    When set to '1', there is no radial contribution in Joule heating because there are no physical reasons to take it into account. 
    The value '0' corresponds to the old SOLPS5.0 treatment.
    

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
    

.. index:: b2tfhe_neutral

``b2tfhe_neutral``    type: ``real``    default: ``0.0``
    Real parameter which multiplies ion-neutral current. 
    If b2tfhe\_neutral is 0 then ion-neutral current is switched off otherwise ion-neutral current is switched on.
    

.. index:: b2tfhe_vis_par

``b2tfhe_vis_par``    type: ``real``    default: ``0.0``
    Real parameter which multiplies current driven by parallel viscosity. 
    If b2tfhe\_vis\_par is 0 then viscosity-driven current is switched off otherwise viscosity-driven current is switched on.
    

.. index:: b2tfhe_vis_q

``b2tfhe_vis_q``    type: ``real``    default: ``1.0``
    Real parameter which multiplies current driven by heat viscosity effects.
    

.. index:: b2trcl_lluciani

``b2trcl_lluciani``    type: ``integer``    default: ``3``
    If lluciani.ne.0, then transport coefficients on cells belonging to closed field lines are modified according to the Luciani model. 
    If lluciani.eq.1, the standard connection length formulation is used. 
    If lluciani.eq.2, the old SOLPS4.0 formulation is used for backward compatibility. 
    If lluciani.eq.3, Spb's new form Luciani's coefficient.
    

.. index:: b2trcl_lthf21

``b2trcl_lthf21``    type: ``integer``    default: ``0``
    If lthf21.ne.0, then the heat transfer model is modified according to the 21-moment approach. This should only be used for multi-fluid runs.
    

.. index:: b2trcl_lvis21

``b2trcl_lvis21``    type: ``integer``    default: ``0``
    If lvis21.ne.0, then the viscosities are modified according to the 21-moment approach. This should only be used for multi-fluid runs. This switch should not be used along with 'b2tfhe\_vis\_par' to avoid double-counting of classical viscosity effects.
    

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


    The 20 switches above are all feedback switches and require that b2stbc\_feedback.ne.0 (See Run section for details) or that lfeedback=.true. in b2.boundary.parameters. The feedback is done as a boundary condition and is under-relaxed using the b2stbc\_....\_alpha switches (See Numerics section for details). 
    fheycore is the radial electron heat flow entering the core boundary. 
    fhiycore is the radial ion heat flow entering the core boundary. 
    fchycore is the radial current entering the core boundary. fnaycore is the radial flux of species "isfeedback" entering the core boundary. 
    If fhiycore\_kinetic\_energy.eq.1, the parallel kinetic energy flux is counted as part of the ion energy flux. 
    For double-null cases, the f..ycore variables contain the total flow through both core boundaries taken together. The core boundaries are identified by the coreregno and coreregn2 switches (see Geometry section). 
    The other seven switches are density feedback switches: nesepm is the outer midplane separatrix electron density. (See b2mwti\_jxa switch in Geometry section for setting of midplane position). This is controlled through particle input of main plasma species isfeedback through the core boundary (See Geometry section for the core boundary indices coreregno and coreregn2). 
    nesepm\_sol is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the SOL region. (See b2mwti\_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the SOL North boundary (See Geometry section for the SOL North boundary index solregno). If nesepm\_overshoot.gt.1.0, the gas puff is turned off when the midplane separatrix density reaches nesepm\*nesepm\_overshoot. Minimum and maximum values of the feedback gas puff can be set using b2stbc\_nesepm\_minpuff and b2stbc\_nesepm\_maxpuff 
    nepedm\_sol is similar to nesepm\_sol but the feedback is exerted on the electron density at the top of the pedestal, along the outer midplane, at radial position b2stbc\_iyped. ndes\_sol is the total particle content from the homonuclear sequence of species 'isfeedback' over the entire simulation domain. 
    It is governed, like nesepm\_sol, by nesepm\_overshoot and nesepm\_alpha and corresponds to a SOL boundary feedback. volrec\_sol is the total particle source due to volume recombination coming from Eirene. Its feedback is governed by volrec\_overshoot and volrec\_alpha and volrec\_beta parameters (See Numerics section for the latter two). nesepm\_pfr is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the PFR region. (See b2mwti\_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the PFR South boundary indices pfrregno1 and pfrregno2). 
    ndes is the total particle (neutrals + ions) content of the species whose neutral species has index isfeedback. This is controlled through particle input of neutrals species isfeedback through the 
    private flux boundaries (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2). private\_flux\_puff is the particle flow of species isfeedback through the private flux region boundary. This is controlled through particle input of neutrals species isfeedback through the private flux boundaris (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2). 
    All but the first of these feedback schemes ("nesepm") can also be run though an Eirene neutral gas puff. In that case, one should set an appropriate gas puffing stratum in the Eirene input file input.dat, as well as in the b2.neutrals.parameters file. The code will assume, unless told otherwise through the use of "eirene\_nesepm\_istra", that the first stratum of type 'C' found in b2.neutrals.parameters is the stratum used for the feedback. If "eirene\_nesepm\_istra" is set to a positive number, the code will consider the feedback stratum to be the stratum in the "eirene\_nesepm\_istra"-th position in b2.neutrals.parameters.
    
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


.. index:: b2stbc_secmodel

``b2stbc_secmodel``    type: ``integer``    default: ``0``
    If secmodel.eq.1, then the secondary electron emission coefficient at the plates is computed locally according to a kinetic model, otherwise the default values of cbsch(7,ireg) and/or gammae are used.
    

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


    Sputtering model switches. See the code in b2stbr and the b2mod\_sputter module for specific implementation details and references. 
    The default values represent the case of Graphite plates. Sput\_src is the atomic number of the plasma species which causes chemical sputtering. 
    Sput\_dst (when .ge.0) is the species index of the destination species produced by physical sputtering, chemical sputtering and/or RES. If either of the latter two processes are included, the production chemical sputtering and RES rate calculations provided in the code assume that sput\_dst points to a Carbon species. 
    Sput\_dst2 and sput\_dst3 (when .ge.0) represent other species produced by wall interactions for mixed materials scenarios. 
    Sput\_frac\_flag is the switch to turn on mixed materials scenarios (when sput\_frac\_flag.eq.1). 
    Plate\_model.eq.0 means the 0-D time-independent plate heating model while plate\_model.eq.1 indicates the 1-D time-dependent plate heating treatment. Plate\_model.eq.2 gives acces to a 2-D time-dependent model. Plate\_option chooses the initialisation of the plate temperature profile. If plate\_option.eq.1, the profile is set to the constant given in plate\_temp. If plate\_option.eq.2, the profile is computed to be the 0-D equilibrium profile. If plate\_option.eq.3, the profile is read from results of the previous run.
    Sput\_phys\_model is a switch for choosing between the TRIM tables (model 1, default) or an empirical formula (model 0). When TRIM data is not available, the empirical formula is automatically used. Extrapolations of low and high energy ranges beyond the TRIM table data is done using the same physical dependencies as the empirical formula. Sput\_chem\_model is a switch for the chemical sputtering model used. 
    If sput\_chem\_model.eq.0 (default), the empirical formula is used. 
    If sput\_chem\_model.eq.1, a constant with a low energy cut-off is used. 
    The cutoff occurs at approximately sput\_chem\_cutoff\_alpha and the width is determined by sput\_chem\_cutoff\_beta (the larger the value, the narrower the width over which the transition from 0 to 1 occurs). 
    For model 0, sput\_frc is a multiplier to the empirical formula, while for model 1, sput\_frc is the constant chemical sputtering yield. 
    Sput\_frc is superseded by the chem\_sput array from b2.neutrals.namelist if the latter is used. 
    For neutrals species, we add a factor of alpha\*na\*vbar to the particle flux to the plate (used to compute chemical and RES sputtering), where vbar is the average neutral particle speed. 
    Sput\_phys turns on physical sputtering when sput\_phys.gt.0.0 and contains a (real) multiplier for the physical sputtering rate looked up in the TRIM tables. It is superseded by the phys\_sput array in b2.neutrals.parameters if the latter is used. 
    sput\_phys\_col indicates which column to use in the TRIM table; the default (3) corresponds to 30 degrees incidence. The columns are for
    0 15 30 45 55 65 75 80 85 degrees. This angle is also used in the empirical formula. Plate\_temp is the temperature (in Kelvin) of the COOLED end of the divertor plates. The surface temperature is computed self-consistently (using a 1-D description) according to the incident heat fluxes from the plasma. The plate is assumed to have a thickness of plate\_thick, measured in meters. When plate\_thick.eq.0 (default), the plate surface temperature is assumed to be the same as plate\_temp. Sput\_res turns on radiation enhanced sublimation (RES) when .gt.0.0 and is a multiplier to the RES rate. 
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
    
.. index::
   single: b2stbr_refl*; b2stbr_refl_model
   single: b2stbr_refl*; b2stbr_reflection_on


.. index:: b2mndr_coronal_model

``b2mndr_coronal_model``    type: ``integer``    default: ``0``
    Turns on the coronal model if coronal.ne.0. I.e., the reaction rates of all reactions are made density-independent, and the value computed at the lowest density (given in b2ar.dat) is used.
    

.. index:: b2mndr_hz

``b2mndr_hz``    type: ``real``    default: ``0.0``
    hz has been introduced into the new form of the parallel momentum balance equation. If fac\_hz = 0.0 then hz = 1 and old form of equations is used. If fac\_hz = 1.0 then new form of equations is used.
    

.. index:: b2stbr_bas_recycled_neutrals_contr

``b2stbr_bas_recycled_neutrals_contr``    type: ``real``    default: ``1.0``
    Introduced for nulling recycling energy when it is zero.
    

.. index:: b2tfhe_alfTeEh

``b2tfhe_alfTeEh``    type: ``real``    default: ``0.0``
    When set to '0.0', the old form of the electron heat flux calculation is used. It is recommended to use 1.0.
    

.. index:: b2tfhe_fch_pTe

``b2tfhe_fch_pTe``    type: ``real``    default: ``1.0``
    When set to '1.0', the new form of the electron heat flux calculation is used. It is recommended to use 1.0.
    

.. index:: b2tfnb_ycur

``b2tfnb_ycur``    type: ``real``    default: ``1.0``
    Ycur is a multiplier to the parallel viscosity, ion inertial and anomalous currents to the ion radial flows (particle and energy).
    

.. index:: b2tqce_fke_Zhdanov

``b2tqce_fke_Zhdanov``    type: ``integer``    default: ``1``
    When set to '1', Zhdanov's expression is used in the electron thermal conductivity. It is recommended to use 'b2tqce\_fke\_Zhdanov' '1'. 
    This switch is only active if, simultaneously, one has b2tqce\_model.eq.1 and b2tfhe\_fch\_pTe.eq.1.0.
    

.. index:: b2tqna_ixref

``b2tqna_ixref``    type: ``integer``    default: ``See description (integer)``
    Poloidal index (on the basis mesh) of the reference surface for the flux-scaled transport model. The default value is the outer midplane, computed as such (see b2mwti\_jxa in Geometry section or set\_transport\_ixref below): 
    Single-null : ixref=rightcut1(1)-(rightcut1(1)-leftcut1(1))/4. 
    Double-null : ixref=(rightcut1(1)+rightcut1(2))/2. Straight geometry : ixref=3\*nx/4. 
    The flux-scaled transport model is used in conjunction with scaling factors listed in column (7) of the transport coefficients description in input files b2ah.dat and b2mn.dat.
    

.. index:: b2tqna_user_transport...

.. index:: b2tqna_user_transport, set_transport_eta, set_transport_eta_alpha, set_transport_eta_floor, set_transport_eta_ceiling, set_transport_ixref, set_transport_iyref, set_transport_required_te_gradient
.. c

``b2tqna_user_transport...``

  - ``b2tqna_user_transport``  -     type: ``integer``    default: ``0``

  - ``set_transport_eta``  -     type: ``real``    default: ``2.0``

  - ``set_transport_eta_alpha``  -     type: ``real``    default: ``0.5``

  - ``set_transport_eta_floor``  -     type: ``real``    default: ``0.1``

  - ``set_transport_eta_ceiling``  -     type: ``real``    default: ``10.0``

  - ``set_transport_ixref``  -     type: ``integer``    default: ``See description (integer)``

  - ``set_transport_iyref``  -     type: ``integer``    default: ``See description (integer)``

  - ``set_transport_required_te_gradient``  -     type: ``real``    default: ``5.0e4``


    The last switch is subservient to b2tqna\_user\_transport, and only used if user\_transport.ne.0. When this is the case, the electron perpendicular heat diffusivity and anomalous perpendicular particle transport coefficient are scaled so as to maintain the required\_te\_gradient (in units of eV/m), at the location (ixref,iyref) on the basis mesh. The default position of the reference cell is on the outer midplane, sligthly inside the separatrix, as follows:
    Configuration |     ixref                    |     iyref
    ---------------+------------------------------+----------------------
    Single-null   | rightcut1(1)-                | 2\*topcut1(1)/3
    | (rightcut1(1)-leftcut1(1))/4 |
    |                              |
    Double-null   | (rightcut1(1)+rightcut1(2))/2| 2\*min(topcut1(1),
    |                              | topcut1(2))/3
    |                              |
    Straight      | 3\*nx/4                       | ny/2
    |                              |
    The transport\_eta switches are activated when user\_transport.eq.3 and allow modifications of the electron heat conductivity according to a constant eta (Grad Te / Grad Ne) model. See routine set\_transport\_eta code for details.
    A model for disruption transport coefficients is available with user\_transport.eq.7. See routine set\_transport\_disruption code for details.
    The value user\_transport.eq.8 activates the neoclassical model for computation of the transport coefficients in the core. See routine set\_transport\_neo and subroutines called for details. Implemented from the NEOART package.
    The location given by ixref and iyref can also serve as the anchor point for the transport and/or sources profiles provided by the user in the b2.transport.inputfile and b2.sources.profile files.
    
.. index::
   single: b2tqna_user_transport...; b2tqna_user_transport
   single: b2tqna_user_transport...; set_transport_eta
   single: b2tqna_user_transport...; set_transport_eta_alpha
   single: b2tqna_user_transport...; set_transport_eta_floor
   single: b2tqna_user_transport...; set_transport_eta_ceiling
   single: b2tqna_user_transport...; set_transport_ixref
   single: b2tqna_user_transport...; set_transport_iyref
   single: b2tqna_user_transport...; set_transport_required_te_gradient


.. index:: b2tqna_m*

.. index:: b2tqna_max_df0, b2tqna_min_df0
.. c

``b2tqna_m*``

  - ``b2tqna_max_df0``  -     type: ``real``    default: ``1e30``

  - ``b2tqna_min_df0``  -     type: ``real``    default: ``0.0``


    Upper and lower limits of the diffusivity coefficients df0 computed in b2tqna for each species.
    
.. index::
   single: b2tqna_m*; b2tqna_max_df0
   single: b2tqna_m*; b2tqna_min_df0


.. index:: b2tqna_new_df0

``b2tqna_new_df0``    type: ``integer``    default: ``0``
    When new\_df0.eq.1, the neutral diffusivity is computed according to the local charge exchange, ionisation and elastic collision rates, instead of the standard form with constant cross-sections.
    

.. index:: b2tqna_ballooning

.. index:: b2tqna_ballooning, b2tqna_ballooning_rescale, b2tqna_bb_ref
.. c

``b2tqna_ballooning``

  - ``b2tqna_ballooning``  -     type: ``real``    default: ``0.0``

  - ``b2tqna_ballooning_rescale``  -     type: ``real``    default: ``1.0``

  - ``b2tqna_bb_ref``  -     type: ``real``    default: ``See description (real)``


    Ballooning model switches. If ballooning.ne.0, then all transport coefficients in cell (i) are rescaled by a factor of ballooning\_rescale\*abs(bb\_ref/bb(i))\*\*ballooning . 
    The default value for bb\_ref is the arithmetic average of the total magnetic field strength over the entire computational domain.
    
.. index::
   single: b2tqna_ballooning; b2tqna_ballooning
   single: b2tqna_ballooning; b2tqna_ballooning_rescale
   single: b2tqna_ballooning; b2tqna_bb_ref


.. index:: b2tqna_pfr_rescale

``b2tqna_pfr_rescale``    type: ``real``    default: ``1.0``
    Scaling factor for all ion and electron transport coefficients inside private flux regions.
    

.. index:: b2tqna_divsol_rescale

``b2tqna_divsol_rescale``    type: ``real``    default: ``1.0``
    Scaling factor for all ion and electron transport coefficients inside divertor SOL regions.
    

.. index:: b2sifr_phm0

``b2sifr_phm0``    type: ``real``    default: ``1.0``
    Multiplier of the friction term between charged species.
    

.. index:: b2sifr_phm1

``b2sifr_phm1``    type: ``real``    default: ``1.0``
    Multiplier of the ehxp term in the thermal force term.
    

.. index:: b2sifr_phm2

``b2sifr_phm2``    type: ``real``    default: ``1.0``
    Multiplier of the electron thermal gradient term in the thermal force term
    

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
    The default formula is to use the Braginskii formulation, which will give the same answer for electron-electron (ee), electron-ion (ei), and ion-ion (ii) collisions. Respectively, non-default values of '1', '2' and '3' for b2tlnl\_ee, \_ei, and \_ii, respectively, make use of the calculation according to Wesson.
    
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
    The larger alpha is, the weaker the flux limit is. 
    Gamma is the exponent used in the flux-limiting formula. 
    The smaller gamma is, the stronger the flux limit is. 
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

  - ``b2tlc0_alpha``  -     type: ``real``    default: ``0.0``

  - ``b2tlc0_gamma``  -     type: ``real``    default: ``2.0``


    Parameters for the flux limit to dpa0 - pressure driven neutral diffusion. 
    Alpha is a multiplier to the classical flux limit value. 
    Gamma is the exponent used in the flux-limiting formula. If alpha.eq.0, no flux limit is applied.
    
.. index::
   single: b2tlc0_*; b2tlc0_alpha
   single: b2tlc0_*; b2tlc0_gamma


.. index:: b2tlh0_*

.. index:: b2tlh0_alpha, b2tlh0_gamma, b2tlh0_flux_limit_min_ti
.. c

``b2tlh0_*``

  - ``b2tlh0_alpha``  -     type: ``real``    default: ``0.0``

  - ``b2tlh0_gamma``  -     type: ``real``    default: ``2.0``

  - ``b2tlh0_flux_limit_min_ti``  -     type: ``real``    default: ``0.0``


    Parameters for the flux limit to the heat conductivity of the neutrals. Alpha is a multiplier to the classical flux limit value. 
    The larger alpha is, the weaker the flux limit is. 
    Gamma is the exponent used in the flux-limiting formula. 
    The smaller gamma is, the stronger the flux limit is. 
    If alpha.eq.0, no flux limit is applied. 
    flux\_limit\_min\_ti specifies the minimum ti to be used (in eV).
    
.. index::
   single: b2tlh0_*; b2tlh0_alpha
   single: b2tlh0_*; b2tlh0_gamma
   single: b2tlh0_*; b2tlh0_flux_limit_min_ti


.. index:: b2tlmv_style

``b2tlmv_style``    type: ``integer``    default: ``1``
    if style = 0 then it is applied the origin flux limit to the viscosity else it is applied the SPb flux limit to the viscosity
    

.. index:: b2sihs_phm0

``b2sihs_phm0``    type: ``real``    default: ``1.0``
    Multiplier of the contribution to electron heat sources from divergence(ue,ve).
    

.. index:: b2sihs_phm1

``b2sihs_phm1``    type: ``real``    default: ``1.0``
    Multiplier of the contribution to ion heat sources from divergence(ua,va). This term is superseded by the BoRiS switch if invoked.
    

.. index:: b2sihs_phm2

``b2sihs_phm2``    type: ``real``    default: ``1.0``
    Multiplier of the contribution to ion heat sources from viscous heating. This term is superseded by the BoRiS switch if invoked.
    

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
    

.. index:: b2sdia_facgt

``b2sdia_facgt``    type: ``real``    default: ``0.0``
    Multiplier of the contribution to electron and ion heat sources from divergence of the gradTxB heat flux. That contribution is also multiplied by facdrift. This term is no longer needed as it has been transferred from being a source to being included in the flows.
    

.. index:: b2sral_style

``b2sral_style``    type: ``integer``    default: ``2``
    When set to '0', in the expression of the electron particle flux (fne) the particle flux with drift terms is used and temporary drift velocities on the first call are calculated. When set to '1' or '2', the particle flux without drift terms is used in fne. It is recommended '2'.
    

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

``b2stel_phm0``    type: ``real``    default: ``0.0``
    Multiplier of the recombination contribution to the electron cooling rate (if ADPAK rates are not used because those are already included). Assumes all recombination is three-body.
    

.. index:: b2tfhe_lim_flux

``b2tfhe_lim_flux``    type: ``integer``    default: ``0``
    If '0', flux limit is not applied directly to the electron heat flux but is applied through transport coefficients if 'b2trcl\_conductive\_limit' is '1'. It is recommended '0'.
    

.. index:: b2tfhi_lim_flux

``b2tfhi_lim_flux``    type: ``integer``    default: ``1``
    If '0', flux limit is not applied directly to the ion heat flux but is applied through transport coefficients if 'b2trcl\_conductive\_limit' is '1'. It is recommended '0'.
    

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
    

.. index:: b2trno_pol_anom_scale

``b2trno_pol_anom_scale``    type: ``real``    default: ``1.0``
    If pol\_anom\_scale.ne.1, the poloidal anomalous transport coefficients are scaled by the number. To get the same treatment as setting the old switch (radial\_only) to 1, set the new switch to 0.0. 
    This multiplication is to only take place for charged species.
    

.. index:: eirene_lhalpha

``eirene_lhalpha``    type: ``integer``    default: ``1``
    If 0 then no calculation of halpha in wneutral, otherwise halpha is calculated
    

.. index:: eirene_lvib

``eirene_lvib``    type: ``integer``    default: ``0``
    If 0 then the sigadd4 (molecular ions) and sigadd5 (negative ions) contributions to the halpha in wneutral are not included, otherwise they are
    

.. index:: eirene_repeat_first_call

``eirene_repeat_first_call``    type: ``integer``    default: ``1``
    If > 0 then repeats the first call to eirene in eirene\_mc so many times. 
    Useful if a density feedback gas puff is being used because the flux passed to Eirene on its first call is ignored (instead the value in the Eirene input file is used).
    

.. index:: eirene_use_recyceir

``eirene_use_recyceir``    type: ``integer``    default: ``1``
    If > 0 use recyceir (non species dependent) to specify the recycling\* coefficients, else if 0 use recyc (species dependent).
    

.. index:: eirene_ionising_core

``eirene_ionising_core``    type: ``integer``    default: ``0``
    If <> 0 then recycles the neutral flux having crossed the core boundary within Eirene as ions. The recycling is surface-averaged, and neutrals come back as fully-stripped ions. 
    'eirene\_ionizing\_core' is an alias for this switch. 
    If the value = 1, then the flux is added by direct modification of the sources in the guard cells --- this will only work if a standard flux boundary condition is applied at that boundary. 
    If the value is < 0, then the absolute value specifies which boundary in b2.boundary.parameters is to be used. This will only work for the new type 13 boundary condition.
    

.. index:: eirene_background

``eirene_background``    type: ``integer``    default: ``1``
    If eirene\_background.eq.0, the ion velocities passed to Eirene to be used for the collisions are based on grad-B and ExB drifts (vadia + vaecrb).
    If eirene\_background.eq.1, these velocities contain the full diamagnetic and ExB drifts (wadia + vaecrb).
    Note: recycling fluxes are always computed based on grad-B and ExB drifts only (and are not affected by this switch), because diamagnetic drift flows largely close within the sheath.
    

.. index:: eirene_sheath_pot

``eirene_sheath_pot``    type: ``integer``    default: ``1``
    If eirene\_sheath\_pot.eq.1, the sheath potential drop as computed by B2.5 (i.e. including effects of parallel currents, secondary electron emission, etc.) is passed to EIRENE to compute ion acceleration in the sheath. 
    If eirene\_sheath\_pot.eq.0, the sheath potential drop is 
    recomputed by EIRENE, usually assuming zero current and secondary
    electron emission.
    

.. index:: b2stel_fix_recomb_energy

``b2stel_fix_recomb_energy``    type: ``integer``    default: ``0``
    If changed to 1, then the recombination energy (rpi) is added to the electron energy for each recombination. This should only be used if the is-->is-1 energy terms have been included in the electron cooling rates (as done by setting the switch 'b2ardr\_fix\_recomb' in b2ar.dat to a non-zero value and recalculating b2frates).
    See 'Atomic Physics' section.
    \*\*\* Use with caution! \*\*\*
    

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
    mind that B2 already calculates the classical transport !
    avoid double transport, 0+4 for cross checks only !
    

.. index:: 
   single: Physics; b2siav_addvis
   single: Physics; b2siav_addvis1
   single: Physics; b2npmo_b2sifr_
   single: Physics; b2sihs_istyle_Joule_heating
   single: Physics; b2sicf_phm0
   single: Physics; b2sicf_phm1
   single: Physics; b2t*_anomalous
   single: Physics; b2news_ExB
   single: Physics; b2tfhe_neutral
   single: Physics; b2tfhe_vis_par
   single: Physics; b2tfhe_vis_q
   single: Physics; b2trcl_lluciani
   single: Physics; b2trcl_lthf21
   single: Physics; b2trcl_lvis21
   single: Physics; b2sqel_artificial_radiation
   single: Physics; b2stbc_*
   single: Physics; b2stbc_type13..21*
   single: Physics; b2stbc_secmodel
   single: Physics; b2stbr_sputtering...
   single: Physics; b2stbr_refl*
   single: Physics; b2mndr_coronal_model
   single: Physics; b2mndr_hz
   single: Physics; b2stbr_bas_recycled_neutrals_contr
   single: Physics; b2tfhe_alfTeEh
   single: Physics; b2tfhe_fch_pTe
   single: Physics; b2tfnb_ycur
   single: Physics; b2tqce_fke_Zhdanov
   single: Physics; b2tqna_ixref
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
   single: Physics; b2tlmv_style
   single: Physics; b2sihs_phm0
   single: Physics; b2sihs_phm1
   single: Physics; b2sihs_phm2
   single: Physics; b2sihs_phm3
   single: Physics; b2sihs_phm4
   single: Physics; b2sihs_phm5
   single: Physics; b2sihs_phm6
   single: Physics; b2sihs_phm7
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
   single: Physics; b2trno_pol_anom_scale
   single: Physics; eirene_lhalpha
   single: Physics; eirene_lvib
   single: Physics; eirene_repeat_first_call
   single: Physics; eirene_use_recyceir
   single: Physics; eirene_ionising_core
   single: Physics; eirene_background
   single: Physics; eirene_sheath_pot
   single: Physics; b2stel_fix_recomb_energy
   single: Physics; b2mndr_atomic_physics_rescale
   single: Physics; neoclassical_ic

.. index:: Output

Output
======
.. index:: b2mndr_b2time

``b2mndr_b2time``    type: ``integer``    default: ``1``
    Specifies the number of timesteps between writes of the time-dependent file. If b2time.gt.0, always writes out on the last timestep.
    

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
    Another option for movie output. Give the real-time interval between movie frames.
    

.. index:: b2mndr_ntim_save

``b2mndr_ntim_save``    type: ``integer``    default: ``0``
    Another option for plasma state file output. Give the number of B2.5 full interations between succesive write-ups of plasmastate files, in addition to the ones written at regular CPU intervals. Should be used, at the exclusion of other plasmastate write-up frequency settings, in conjunction with the Leuven Monte-Carlo averaging scheme.
    

.. index:: b2mndr_plasmatim

``b2mndr_plasmatim``    type: ``real``    default: ``0.0``
    Another option for plasma state file output. Give the real-time interval between succesive write-ups of plasmastate files, in addition to the ones written at regular CPU intervals.
    

.. index:: b2wdat_iout

``b2wdat_iout``    type: ``integer``    default: ``0``
    If iout.eq.1, a large set of \*.dat output files will be produced containing the values of a variety of code quantities. See the "Output description" file for details.
    

.. index:: b2mndr_*

.. index:: b2mndr_na_eps, b2mndr_po_eps, b2mndr_te_eps, b2mndr_ti_eps, b2mndr_ua_eps
.. c

``b2mndr_*``

  - ``b2mndr_na_eps``  -     type: ``real``    default: ``1.0e19``

  - ``b2mndr_po_eps``  -     type: ``real``    default: ``1.0e+1``

  - ``b2mndr_te_eps``  -     type: ``real``    default: ``1.0e+1``

  - ``b2mndr_ti_eps``  -     type: ``real``    default: ``1.0e+1``

  - ``b2mndr_ua_eps``  -     type: ``real``    default: ``1.0e+4``


    The five switches above are safeguards numbers for when printing changes after a time-step. The change is computed as: deltaX = abs((X(t)-X(t-1))/(X(t)+X\_eps))
    
.. index::
   single: b2mndr_*; b2mndr_na_eps
   single: b2mndr_*; b2mndr_po_eps
   single: b2mndr_*; b2mndr_te_eps
   single: b2mndr_*; b2mndr_ti_eps
   single: b2mndr_*; b2mndr_ua_eps


.. index:: b2mndr_trantim

``b2mndr_trantim``    type: ``real``    default: ``0.0``
    Produces a numbered 'tran' file every trantim real-time seconds. An endstate file is written if it falls between scheduled write-up times. Only available within the -DJET environment.
    

.. index:: b2mwti_target_offset

``b2mwti_target_offset``    type: ``integer``    default: ``1``
    The diagnostic values from b2time.nc use guard cell values if target\_offset.eq.0, and values from the neighbouring real cell if target\_offset.eq.1. Fluxes are not affected.
    

.. index:: b2mwti_ismain0

``b2mwti_ismain0``    type: ``integer``    default: ``0``
    Index of the species used to create the 'dp3d?.last10' diagnostic files.
    Defaults to the neutral species associated with ismain. If no such species is declared, the default will be set to ismain. Is expected to either correspond to a neutral species or to ismain.
    If ismain is also defaulted, then will be 0.
    

.. index:: b2mwqt_style

``b2mwqt_style``    type: ``integer``    default: ``1``
    Specifies the amount of data that is written out to b2ftrace. See the manual (Section on b2yq) for full details.
    

.. index:: b2stbr_*_netcdf

.. index:: tallies_netcdf, b2stbr_b2wall_netcdf, balance_netcdf
.. c

``b2stbr_*_netcdf``

  - ``tallies_netcdf``  -     type: ``integer``    default: ``0``

  - ``b2stbr_b2wall_netcdf``  -     type: ``integer``    default: ``0``

  - ``balance_netcdf``  -     default: ``0``


    If tallies\_netcdf.ne.0, the file 'b2tallies.nc' is created, which contains the regional tallies in CDF format.
    If b2wall\_netcdf.ne.0, the file 'b2wall.nc' is created, which contains the wall tallies in CDF format [written every b2wall\_netcdf 'main calls'].
    
.. index::
   single: b2stbr_*_netcdf; tallies_netcdf
   single: b2stbr_*_netcdf; b2stbr_b2wall_netcdf
   single: b2stbr_*_netcdf; balance_netcdf


.. index:: ank_tracing

``ank_tracing``    type: ``integer``    default: ``0``
    If ank\_tracing.ge.1, additional tracing output from Andrei Kukushkin is produced, in files to be found in the tracing/ directory inside the run directory. The traces will be written every ank\_tracing iteration.
    

.. index:: b2stbc_diagno

``b2stbc_diagno``    type: ``integer``    default: ``0``
    Controls level of output in b2stbc and subservient routines.
    Level 1 (diagno.ge.1) output includes wrong\_flow warnings, transport coefficients at the (nx/2,ny) basis mesh position, the solution found for the given heat flux at constant temperature bc, and all feedback diagnostics.
    Level 2 output (diagno.ge.2) includes the integral current correction, the boundary sources on the first call, excessive sound speeds, and the iterative progress to the given heat flux at constant temperature bc. 
    Level 3 output (diagno.ge.3) includes the boundary sources on each call, and the boundary.prt file listing all boundary cells.
    

.. index:: b2stbr_output

``b2stbr_output``    type: ``integer``    default: ``0``
    Output flag for the first\_flight model. If output.ge.1, the files start, end, and fort.88 are created, which contain information about the chords used in the model.
    

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

.. index:: b2ux5p_nltrsol, b2ux7p_nltrsol, b2ux9p_nltrsol
.. c

``b2ux*``

  - ``b2ux5p_nltrsol``  -     type: ``integer``    default: ``2``

  - ``b2ux7p_nltrsol``  -     type: ``integer``    default: ``0``

  - ``b2ux9p_nltrsol``  -     type: ``integer``    default: ``0``


    Output flag for the iluter matrix solver. Larger numbers mean increasing output level.
    
.. index::
   single: b2ux*; b2ux5p_nltrsol
   single: b2ux*; b2ux7p_nltrsol
   single: b2ux*; b2ux9p_nltrsol


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
   single: Output; b2mndr_ntim_save
   single: Output; b2mndr_plasmatim
   single: Output; b2wdat_iout
   single: Output; b2mndr_*
   single: Output; b2mndr_trantim
   single: Output; b2mwti_target_offset
   single: Output; b2mwti_ismain0
   single: Output; b2mwqt_style
   single: Output; b2stbr_*_netcdf
   single: Output; ank_tracing
   single: Output; b2stbc_diagno
   single: Output; b2stbr_output
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

.. index:: Numerics

Numerics
========
.. index:: b2news_potit*

.. index:: b2news_potit, b2news_potitmin
.. c

``b2news_potit*``

  - ``b2news_potit``  -     type: ``integer``    default: ``50``

  - ``b2news_potitmin``  -     type: ``integer``    default: ``0``


    Maximum and minimum number of iterations in the potential equation. It must hold that potitmin < potit.
    
.. index::
   single: b2news_potit*; b2news_potit
   single: b2news_potit*; b2news_potitmin


.. index:: b2news_potok

``b2news_potok``    type: ``real``    default: ``1.0e-2``
    Target residual for the potential equation.
    

.. index:: b2news_ramp_slow

``b2news_ramp_slow``    type: ``integer``    default: ``0``
    If ramp\_slow.eq.0 (default), the ExB and diamagnetic drifts multipliers are ramped on each call of b2news, otherwise they are only changed on the first call of the nstg loop on the timestep.
    

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


.. index:: b2mndt_nstg_ares*

.. index:: b2mndt_nstg_areshe, b2mndt_nstg_areshi, b2mndt_nstg_aresco
.. c

``b2mndt_nstg_ares*``

  - ``b2mndt_nstg_areshe``  -     type: ``real``    default: ``0.0``

  - ``b2mndt_nstg_areshi``  -     type: ``real``    default: ``0.0``

  - ``b2mndt_nstg_aresco``  -     type: ``real``    default: ``0.0``


    Minimum residuals for an internal solution loop to stop.
    Used in conjunction with (not in replacement of) the nstg(0:2) numbers.
    All non-zero criteria must be met simultaneously. The continuity equation residual applies to the 'ismain' species (See 'Run' section).
    
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

.. index:: eirene_na_max, eirene_na_min, eirene_te_max, eirene_te_min, eirene_ti_max, eirene_ti_min, eirene_ua_max, eirene_ua_min
.. c

``eirene_*``

  - ``eirene_na_max``  -     type: ``real``    default: ``1e30``

  - ``eirene_na_min``  -     type: ``real``    default: ``0.0``

  - ``eirene_te_max``  -     type: ``real``    default: ``1e30``

  - ``eirene_te_min``  -     type: ``real``    default: ``0.0``

  - ``eirene_ti_max``  -     type: ``real``    default: ``1e30``

  - ``eirene_ti_min``  -     type: ``real``    default: ``0.0``

  - ``eirene_ua_max``  -     type: ``real``    default: ``+c``

  - ``eirene_ua_min``  -     type: ``real``    default: ``-c``


    Upper and lower bounds used when writing out data for Eirene.
    
.. index::
   single: eirene_*; eirene_na_max
   single: eirene_*; eirene_na_min
   single: eirene_*; eirene_te_max
   single: eirene_*; eirene_te_min
   single: eirene_*; eirene_ti_max
   single: eirene_*; eirene_ti_min
   single: eirene_*; eirene_ua_max
   single: eirene_*; eirene_ua_min


.. index:: eirene_print_minmax

``eirene_print_minmax``    type: ``integer``    default: ``0``
    Print min and max values of te, ti, na & ua
    

.. index:: eirene_extrap

``eirene_extrap``    type: ``integer``    default: ``1``
    If eirene\_extrap.eq.1, then guard cell plasma parameter values are calculated from the neighbouring real cell values. If eirene\_extrap.eq.0, the guard cell values are used unchanged.
    

.. index:: eirene_ank_mods

``eirene_ank_mods``    type: ``integer``    default: ``0``
    If ank\_mods.ne.0, then uses an additional scheme to ensure particle balance as the B2 solution evolves, due to the internal iteration scheme, away from the plasma background on which the Eirene sources were originally computed at the beginning of the time-step. The user is referred to the text in $SOLPSTOP/doc/Source\_Scaling\_in\_B2.pdf for a full description of the method used.
    

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
    When area\_fix.eq.0, recovers old SOLPS5.0 behaviour.
    If area\_fix.ge.1, then certain computations of poloidal velocities are done by dividing flows by the area normal to the flux tube as opposed to the area of contact.
    If area\_fix.ge.2, then additionally this treatment is used for the parallel contact area used in determining plasma flux limiters.
    If area\_fix.ge.3, then additionally this treatment is used for all parallel contact areas.
    

.. index:: b2tfhe_vis_per

``b2tfhe_vis_per``    type: ``integer``    default: ``0.0``
    If '1.0', the electric potential equation is solved by the subroutine b2npp7 using a 7-point stencil.
    The value '1.0' is recommended for runs with drifts when perpendicular viscosity and corresponding perpendicular viscosity current is taken into account.
    

.. index:: b2stbc_sheath_drift_fix

``b2stbc_sheath_drift_fix``    type: ``integer``    default: ``1``
    If sheath\_drift\_fix.eq.0, then the drift velocity used in the sheath boundary conditions is the sum of diamagnetic and ExB contributions (old, but likely wrong, treatment). If sheath\_drift\_fix.eq.1, then the drift velocity used in the sheath boundary conditions is the ExB velocity only (recommended).
    

.. index:: b2stbc_fix_fch_in_fhe_sheath

``b2stbc_fix_fch_in_fhe_sheath``    type: ``integer``    default: ``2``
    If fix\_fch\_in\_fhe\_sheath.eq.0, then the wrong (old) implementation of the FCH contribution to FHE used;
    If fix\_fch\_in\_fhe\_sheath.eq.1, then the wrong (second) implementation of the FCH contribution to FHE used;
    If fix\_fch\_in\_fhe\_sheath.eq.2, then the correct implementation of the FCH contribution to FHE used;
    

.. index:: b2stbr_potential_at_guard_cell

``b2stbr_potential_at_guard_cell``    type: ``integer``    default: ``1``
    If potential\_at\_guard\_cell.eq.1, the electric potential used for the computation of the incident energy for sputtering yields is taken as the value in the guard cell. If potential\_at\_guard\_cell.eq.0, the value from the neighbouring real cell is used instead.
    

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
    If '1', Spb's form to calculate parallel and perpendicular neutral heat conductivity flux limit (does not preserve symmetry, kept for backward compatibility reasons).
    If '2', modifies the Spb treatment for the flux limits to be applied on the transport coefficients directly.
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
    
.. index::
   single: ._upwind; b2tfhe_upwind
   single: ._upwind; b2tfhi_upwind


.. index:: b2tfnb_pflux_cor

``b2tfnb_pflux_cor``    type: ``integer``    default: ``1``
    If pflux\_cor.eq.1 and fna\_mdf is used, enforces that the integral particle flux across the domain boundaries computed from fna is equal to the same integral computed from the fna\_mdf fluxes.
    

.. index:: b2trcl_cvsa_mltpl

``b2trcl_cvsa_mltpl``    type: ``integer``    default: ``1.0``
    Artificial coefficient providing faster convergence to the neoclassical electric field but giving a distortion of the flows in the SOL as a side-effect. 
    Can be applied <>1 during the convergence and turned off for the final stage of calculations. Use with caution.
    

.. index:: b2ux5p_mult_nonzero

``b2ux5p_mult_nonzero``    type: ``integer``    default: ``10``
    Number of expected nonzero matrix elements per matrix row.
    

.. index:: b2ux5p_mult_solvdim*

.. index:: b2ux5p_mult_solvdim, b2ux5p_mult_solvdim1
.. c

``b2ux5p_mult_solvdim*``

  - ``b2ux5p_mult_solvdim``  -     type: ``integer``    default: ``15``

  - ``b2ux5p_mult_solvdim1``  -     type: ``integer``    default: ``10``


    Multipliers to the number of nonzero elements in the solution matrix for workspace arrays in the matrix solver.
    
.. index::
   single: b2ux5p_mult_solvdim*; b2ux5p_mult_solvdim
   single: b2ux5p_mult_solvdim*; b2ux5p_mult_solvdim1


.. index:: b2ux5p_style

``b2ux5p_style``    type: ``integer``    default: ``2``
    Choose the type of matrix solver. Style.eq.0 = iluter, Style.eq.1 = 5-pt stencil, Style.eq.2 = MA28. 
    NOTE: Only style.eq.2 will give good results. Other values are NOT recommended!
    

.. index:: b2ux7p_style

``b2ux7p_style``    type: ``integer``    default: ``3``
    Choose the type of matrix solver. Style.eq.0 = iluter, Style.eq.1 = 5-pt stencil, Style.eq.2 = MA28copy. Style.eq.3 = SDRV from YSMP 
    NOTE: Only style.eq.3 will give good results. Other values are NOT recommended!
    

.. index:: b2ux9p_style

``b2ux9p_style``    type: ``integer``    default: ``2``
    Choose the type of matrix solver. Style.eq.0 = iluter, Style.eq.1 = 5-pt stencil, Style.eq.2 = MA28copy. 
    NOTE: Only style.eq.2 will give good results. Other values are NOT recommended!
    

.. index:: b2ux5p_acpar

``b2ux5p_acpar``    type: ``real``    default: ``8.0``
    Paremeter needed for iluter matrix solver.
    

.. index:: b2stbc_fchy_dia

``b2stbc_fchy_dia``    type: ``real``    default: ``0.0``
    Multiplier to the neoclassical current and diamagnetic heat flux convective boundary conditions, also multiplied by facdrift.
    Adds a poloidal variation consistent with neoclassics and diamagnetic contributions to the heat flux boundary conditions.
    Should only be used with the 5.0 model and heat flux boundaries.
    Allows use b2stbc\_integral\_current if fchy\_dia.eq.0, forbids it otherwise.
    

.. index:: b2stbc_fchy_dia_coreonly

``b2stbc_fchy_dia_coreonly``    type: ``integer``    default: ``1``
    If fchy\_dia\_coreonly.eq.1, the neoclassical current and diamagnetic heat flux convective boundary conditions are only applied on the core boundary.
    If fchy\_dia\_coreonly.eq.0, those are applied to all boundaries, including PFR, North SOL edge and diverted island center boundary.
    

.. index:: b2stbc_neoclassical

``b2stbc_neoclassical``    type: ``real``    default: ``0.0``
    Real parameter which establishes boundary conditions for radial component of the current for North and South boundaries when these lie on closed flux surfaces.
    If b2stbc\_neoclassical is 0 then the radial component of the current is zero.
    If b2stbc\_neoclassical is not 0 the radial component of the current is given by the neoclassical value. b2stbc\_neoclassical is superseded if facdrift.ne.0.
    This cannot be used in conjunction with b2stbc\_integral\_current below.
    

.. index:: b2stbc_cbc

``b2stbc_cbc``    type: ``real``    default: ``1.0``
    Multiplier to the ExB velocity for sheath boundary conditions in b2stbc\_spb and BCMOM=13 case of b2stbc\_phys.
    

.. index:: b2stbc_integral_current

``b2stbc_integral_current``    type: ``real``    default: ``0.0``
    If integral\_current.gt.0, corrects current sources so that there be no surface current at the North and South edges of the edge plasma.
    The value of integral\_current multiplies the correction term added to the current source.
    This setting is incompatible with the normal use of diamagnetic drift terms (facdrift.gt.0.0 .and. b2stbc\_fchy\_dia.ne.0.0) or neoclassical boundary conditions (b2stbc\_neoclassical.gt.0.0).
    

.. index:: b2stbr_first_flight_dl

``b2stbr_first_flight_dl``    type: ``real``    default: ``0.001``
    Step length (in meters) for computing the first flight model chords.
    

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
    

.. index:: b2mndr_na_min

``b2mndr_na_min``    type: ``real``    default: ``1.0e4``
    Minimal density maintained in all cells for all species. 
    It must be true that na\_min is smaller than na\_new, as well as any of the initial densities provided in b2ai.dat. 
    This switch replaces 'b2mndr\_na0eps' from SOLPS5.x.
    

.. index:: b2mndr_na_new

``b2mndr_na_new``    type: ``real``    default: ``1.0e14``
    Initial density put in all cells for all new species if not overwritten by initial state file. This switch replaces 'b2mndr\_na0eps' from SOLPS5.x.
    

.. index:: b2news_guard_flows

``b2news_guard_flows``    type: ``integer``    default: ``2``
    If guard\_flows.eq.0, flows between neighbouring guard cells are blocked.
    If guard\_flows.eq.1, flows between neighbouring guard cells are kept.
    If guard\_flows.eq.2, particle flows between neighbouring guard cells are blocked for the density equations and the incorrect corner values are replaced by interpolated values. It is recommended 2.
    

.. index:: b2news_fac*

.. index:: b2news_fac_ref, b2news_facdrift_tanh_a, b2news_facdrift_tanh_b, b2news_fac_ExB_tanh_a, b2news_fac_ExB_tanh_b, b2news_fac_vis_tanh_a, b2news_fac_vis_tanh_b, b2news_iy_nocoreExB
.. c

``b2news_fac*``

  - ``b2news_fac_ref``  -     default: ``See description (integer)``

  - ``b2news_facdrift_tanh_a``  -     type: ``real``    default: ``0.0``

  - ``b2news_facdrift_tanh_b``  -     type: ``real``    default: ``0.0``

  - ``b2news_fac_ExB_tanh_a``  -     type: ``real``    default: ``0.0``

  - ``b2news_fac_ExB_tanh_b``  -     type: ``real``    default: ``0.0``

  - ``b2news_fac_vis_tanh_a``  -     type: ``real``    default: ``0.0``

  - ``b2news_fac_vis_tanh_b``  -     type: ``real``    default: ``0.0``

  - ``b2news_iy_nocoreExB``  -     type: ``integer``    default: ``-2``


    Parameters for spatial variation of the diamagnetic, ExB and viscosity drift term multipliers. These are allowed to have tanh profiles centered at tanh\_a and of width tanh\_b, where both quantities are in metres and measured along the radial coordinate for the cell column ix.eq.fac\_ref (default value is jxa, see Geometry section for its computation). The maximum value of facdrift and fac\_ExB is controlled by their respective \_start and \_target switches, see Run section for details.
    For consistency with the naming convention of related variables:
    b2news\_facExB\_tanh\_a is an alias for b2news\_fac\_ExB\_tanh\_a,
    b2news\_facExB\_tanh\_b is an alias for b2news\_fac\_ExB\_tanh\_b,
    b2news\_facvis\_tanh\_a is an alias for b2news\_fac\_vis\_tanh\_a, and b2news\_facvis\_tanh\_b is an alias for b2news\_fac\_vis\_tanh\_b. Additionally, for all core cell rows where iy.le.iy\_nocoreExB, fac\_ExB(ix,iy) is set to zero. This means that ExB contributions and flows will be zeroed out in those cells.
    For consistency with the boundary condition treatment, the value iy\_nocoreExB.eq.-1 is NOT recommended!
    
.. index::
   single: b2news_fac*; b2news_fac_ref
   single: b2news_fac*; b2news_facdrift_tanh_a
   single: b2news_fac*; b2news_facdrift_tanh_b
   single: b2news_fac*; b2news_fac_ExB_tanh_a
   single: b2news_fac*; b2news_fac_ExB_tanh_b
   single: b2news_fac*; b2news_fac_vis_tanh_a
   single: b2news_fac*; b2news_fac_vis_tanh_b
   single: b2news_fac*; b2news_iy_nocoreExB


.. index:: b2stbc_istyle_cur_contr_on_S_and_N

``b2stbc_istyle_cur_contr_on_S_and_N``    type: ``integer``    default: ``2``
    When set to '2', SPB's form of adding currents on the South core boundary is included by using BCPOT=12, and on the SOuth PFR and North boundaries by using BCPOT=13. It is recommended '2', in conjunction with the BCPOT=12 and BCPOT=13 settings, respectively.
    When set to '1', SPb's form of adding currents on South and North boundaries is done explicitly in addition to other existing boundary conditions for the potential equation.
    The old 5.0 calculation is recovered by using the value '0'.
    

.. index:: b2stbc_istyle_fchi

``b2stbc_istyle_fchi``    type: ``integer``    default: ``0``
    If '1', explicitly use the expression (bx\*cs\*na) of particle flux (fna) from boundary condition instead of fna.
    

.. index:: b2news_recalculate_contributions

``b2news_recalculate_contributions``    type: ``integer``    default: ``1``
    If recalculate\_contributions.eq.0, turns off recomputation of sources when wrong\_flow flag is active.
    

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
    If 0, b2news is called (SOLPS5.0/1) If 1, b2news\_ is called (SOLPS5.2)
    

.. index:: b2mndt_ntim_step_out

``b2mndt_ntim_step_out``    type: ``integer``    default: ``1``
    When set to a value of 'K', residuals at each K-th step will be written in b2ftrace. It helps to avoid a huge b2ftrace files during long time run.
    

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


.. index:: b2tlh0_hcimx_flag

``b2tlh0_hcimx_flag``    type: ``integer``    default: ``1``
    When set to -1, only the gradient to the left/bottom is used to compute the conductive neutral flux limits.
    When set to 0, only the gradient to the left/bottom is used to compute the conductive neutral flux limits, except when these do not exist (the other face value is used).
    

.. index:: b2trno_flux_limit_to_dpa

``b2trno_flux_limit_to_dpa``    type: ``integer``    default: ``1``
    If '1', flux limit to neutrals contribution to dpa0 - the diffusion coefficient is applied in b2tlc0.F. It is recommended '1'.
    b2tlc0.F has the flux limit parameters alpha and gamma which are given by 'b2tlc0\_alpha' and 'b2tlc0\_gamma'. 'b2tfnb\_alpha' and 'b2tlc0\_alpha' cannot be different from zero simultaneously.
    'b2tfnb\_alpha' gives another form of flux limit which is applied to the whole particle flux.
    

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

``b2mndt_rxf``    type: ``real``    default: ``0.5``
    Main under-relaxation parameter.
    

.. index:: b2news_xfm.

.. index:: b2news_xfm0, b2news_xfm1, b2news_xfm2, b2news_xfm3
.. c

``b2news_xfm.``

  - ``b2news_xfm0``  -     type: ``real``    default: ``1.0``

  - ``b2news_xfm1``  -     type: ``real``    default: ``1.0``

  - ``b2news_xfm2``  -     type: ``real``    default: ``1.0``

  - ``b2news_xfm3``  -     type: ``real``    default: ``1.0``


    Under-relaxation parameters for the parallel momentum, continuity, potential and energy equations respectively.
    
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


    pcm0 specifies an additional under-relaxation factor that is applied to the velocity correction. It is required that 0.le.pcm0.and.0.le.pcm1.
    
.. index::
   single: b2npco_pcm.; b2npco_pcm0
   single: b2npco_pcm.; b2npco_pcm1


.. index:: b2npco_rxg

``b2npco_rxg``    type: ``real``    default: ``1.0``
    rxg specifies a special under-relaxation parameter. A term of the form "abs(residual)/rxg" is added to the diagonal of the matrix of the correction equation, with the effect of limiting the computed correction. rxg is dimensionless and of order unity; smaller values of rxg imply stronger damping.
    

.. index:: b2npht_pcm*

.. index:: b2npht_pcm0, b2npht_pcm1
.. c

``b2npht_pcm*``

  - ``b2npht_pcm0``  -     type: ``real``    default: ``1.0``

  - ``b2npht_pcm1``  -     type: ``real``    default: ``1.0``


    pcm0 specifies an additional under-relaxation factor that is applied to the temperature correction. 
    It is required that 0.le.pcm0.and.0.le.pcm1.
    
.. index::
   single: b2npht_pcm*; b2npht_pcm0
   single: b2npht_pcm*; b2npht_pcm1


.. index:: b2npht_rxg

``b2npht_rxg``    type: ``real``    default: ``1.0``
    rxg specifies a special under-relaxation parameter. A term of the form "abs(residual)/rxg" is added to the diagonal of the matrix of the correction equation, with the effect of limiting the computed correction. rxg is dimensionless and of order unity; smaller values of rxg imply stronger damping.
    

.. index:: b2nph*

.. index:: b2npht_style, b2nph9_style
.. c

``b2nph*``

  - ``b2npht_style``  -     type: ``integer``    default: ``1``

  - ``b2nph9_style``  -     type: ``integer``    default: ``1``


    When set to '1', SPb's form of the program b2sihs\_ is called. It is recommended '1'.
    
.. index::
   single: b2nph*; b2npht_style
   single: b2nph*; b2nph9_style


.. index:: b2npp7_style

``b2npp7_style``    type: ``integer``    default: ``1``
    When set to '1', SPb's form of the program b2usp7\_ is called. It is recommended '1'.
    

.. index:: b2npmo_rxg

``b2npmo_rxg``    type: ``real``    default: ``1.0e6``
    Normalisation factor for the parallel momentum equation.
    

.. index:: b2news_poteq

``b2news_poteq``    type: ``integer``    default: ``1``
    If poteq.eq.0, the potential equation is jumped over and not solved.
    If poteq.eq.2, the potential is set to 3.1\*Te/qe as per SOLPS4.0.
    If poteq.eq.1, the potential equation is solved according to the no\_solve switch settings.
    If poteq.ne.1, then 'b2tfhe\_no\_current'must be set to '1'.
    

.. index:: b2nxdv_style

``b2nxdv_style``    type: ``integer``    default: ``1``
    When set to '1', the total friction force cancel is not calculated at the guard boundary cells. 
    It is recommended '1'.
    

.. index:: b2nxfc_style

``b2nxfc_style``    type: ``integer``    default: ``1``
    style specifies the precise form of interpolation used in the computation of flcb and cvcb. When set to '1', SPb's form of the transport terms in the momentum correction equation is used. 
    It is recommended '1'.
    

.. index:: b2nxfx_style

``b2nxfx_style``    type: ``integer``    default: ``1``
    When set to '1', SPb's form of an expression that occurs in the electron-atom thermal force is used. 
    It is recommended '1'.
    

.. index:: b2sifr_styl*

.. index:: b2sifr_styl0, b2sifr_styl1
.. c

``b2sifr_styl*``

  - ``b2sifr_styl0``  -     type: ``integer``    default: ``0``

  - ``b2sifr_styl1``  -     type: ``integer``    default: ``0``


    Specify the type of linearisation used in the thermal force term.
    
.. index::
   single: b2sifr_styl*; b2sifr_styl0
   single: b2sifr_styl*; b2sifr_styl1


.. index:: b2sigp_style

``b2sigp_style``    type: ``integer``    default: ``1``
    When set to '1', SPb's form of the pressure gradient term on the right hand of the momentum balance equation is used. 
    It is recommended '1'.
    

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


.. index:: b2sihs_style

``b2sihs_style``    type: ``integer``    default: ``0``
    style determines the form of the strange electron-atom energy transfer term.
    

.. index:: b2srdt_phm.

.. index:: b2srdt_phm0, b2srdt_phm1, b2srdt_phm3, b2srdt_phm4, b2srdt_phm5
.. c

``b2srdt_phm.``

  - ``b2srdt_phm0``  -     type: ``real``    default: ``1.0``

  - ``b2srdt_phm1``  -     type: ``real``    default: ``1.0``

  - ``b2srdt_phm3``  -     type: ``real``    default: ``1.0``

  - ``b2srdt_phm4``  -     type: ``real``    default: ``0.0``

  - ``b2srdt_phm5``  -     type: ``real``    default: ``1.0``


    Multipliers to the density, parallel momentum, heat, potential, and electron prticle time-derivative source terms, respectively. 
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
    Specifies the type of linearisation used in the sources derived from the Monte-Carlo neutrals. If linearisation.eq.0, all sources are fed to the constant term, if linearisation.eq.1, positive terms go in the constant term, and negative terms in the proportional term. 'eirene\_mc\_linearization' is an alias for this switch.
    

.. index:: b2stbm_linearisation

``b2stbm_linearisation``    type: ``real``    default: ``1.0``
    Same as above, but applied to the sources coming for an externally coupled code providing plasma sources, for instance a kinetic treatment of trace impurity ions. 'b2stbm\_linearization' is an alias for this switch.
    

.. index:: b2stbm_impgyro_mod

``b2stbm_impgyro_mod``    type: ``integer``    default: ``0``
    Specifies the frequency (in units of full b2 timesteps) at which an externally coupled code providing additional source (for instance a kinetic treatment of trace impurity ions such as IMPGYRO) should be called.
    

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
    If '1', Spb's new form of calculating electron heat flux is used. It is recommended '1' for runs with drifts.
    

.. index:: b2tfhe_no_current

``b2tfhe_no_current``    type: ``integer``    default: ``0``
    If no\_current.eq.1, all currents are set to zero. The setting no\_current.eq.1 must be used if the potential equation is not explicitly solved for, i.e. for b2news\_poteq.ne.1.
    

.. index:: b2tfhi_mdf

``b2tfhi_mdf``    type: ``integer``    default: ``0``
    If '1', Spb's new form of calculating ion heat flux is used. 
    It is recommended '1' for runs with drifts.
    

.. index:: b2tfnb_drift_style

``b2tfnb_drift_style``    type: ``integer``    default: ``1``
    When set to '0', drift velocities are calculated in cell centers. When set to '1', drift velocities are calculated in cell faces.

    | It is recommended '1'.

    

.. index:: b2tfnb_fnb_nodrift_style

``b2tfnb_fnb_nodrift_style``    type: ``integer``    default: ``1``
    When set to '1', SPb's form of calculating no drift part of the particle fluxes is used. 
    It is recommended '1'.
    

.. index:: b2tfnb_mdf

``b2tfnb_mdf``    type: ``integer``    default: ``0``
    If '1', Spb's new form of calculating particle flux is used. 
    It is recommended '1' for runs with drifts.
    

.. index:: b2tfnb_xfrhie

``b2tfnb_xfrhie``    type: ``real``    default: ``1.0``
    Multiplier to the Rhie and Chow upwind correction.
    

.. index:: b2upht_stylec

``b2upht_stylec``    type: ``integer``    default: ``0``
    (stylec is a numerical switch, needs experiments)
    

.. index:: b2usmo_cfc0

``b2usmo_cfc0``    type: ``real``    default: ``1.0``
    Linearisation constant.
    

.. index:: b2srsm_enable

``b2srsm_enable``    type: ``integer``    default: ``0``
    If enable.ne.0, then the sources for particle, parallel momentum, electron and ion heat are rescaled, for non-boundary cells, if the local timestep exceeds the physics timescale implied by those sources.
    

.. index:: 
   single: Numerics; b2news_potit*
   single: Numerics; b2news_potok
   single: Numerics; b2news_ramp_slow
   single: Numerics; b2mndr_min_ares*
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
   single: Numerics; b2tfhe_vis_per
   single: Numerics; b2stbc_sheath_drift_fix
   single: Numerics; b2stbc_fix_fch_in_fhe_sheath
   single: Numerics; b2stbr_potential_at_guard_cell
   single: Numerics; b2trcl_conductive_limit
   single: Numerics; b2trcl_core_cond_limit
   single: Numerics; b2tlh0_flux_limit_style
   single: Numerics; b2tral_mode
   single: Numerics; b2tfh._*hybr*
   single: Numerics; ._upwind
   single: Numerics; b2tfnb_pflux_cor
   single: Numerics; b2trcl_cvsa_mltpl
   single: Numerics; b2ux5p_mult_nonzero
   single: Numerics; b2ux5p_mult_solvdim*
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
   single: Numerics; b2mndr_na_min
   single: Numerics; b2mndr_na_new
   single: Numerics; b2news_guard_flows
   single: Numerics; b2news_fac*
   single: Numerics; b2stbc_istyle_cur_contr_on_S_and_N
   single: Numerics; b2stbc_istyle_fchi
   single: Numerics; b2news_recalculate_contributions
   single: Numerics; b2news_no_b2sral_call
   single: Numerics; b2news_do_2nd_b2npco_call
   single: Numerics; b2news_re_eval_prtls_fluxes
   single: Numerics; b2mndt_style
   single: Numerics; b2mndt_ntim_step_out
   single: Numerics; b2stb*
   single: Numerics; b2stbc_type13_*
   single: Numerics; heatdiff1D_*
   single: Numerics; b2tlh0_hcimx_flag
   single: Numerics; b2trno_flux_limit_to_dpa
   single: Numerics; b2mndr_*fb*
   single: Numerics; b2mndt_use_b2srst
   single: Numerics; b2mndt_rxf
   single: Numerics; b2news_xfm.
   single: Numerics; b2npco_pcm.
   single: Numerics; b2npco_rxg
   single: Numerics; b2npht_pcm*
   single: Numerics; b2npht_rxg
   single: Numerics; b2nph*
   single: Numerics; b2npp7_style
   single: Numerics; b2npmo_rxg
   single: Numerics; b2news_poteq
   single: Numerics; b2nxdv_style
   single: Numerics; b2nxfc_style
   single: Numerics; b2nxfx_style
   single: Numerics; b2sifr_styl*
   single: Numerics; b2sigp_style
   single: Numerics; b2xzdd_zero_dead_and_core
   single: Numerics; b2sihs_rf.
   single: Numerics; b2sihs_style
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
   single: Numerics; b2tfhi_mdf
   single: Numerics; b2tfnb_drift_style
   single: Numerics; b2tfnb_fnb_nodrift_style
   single: Numerics; b2tfnb_mdf
   single: Numerics; b2tfnb_xfrhie
   single: Numerics; b2upht_stylec
   single: Numerics; b2usmo_cfc0
   single: Numerics; b2srsm_enable

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
    \*\*\* Use with caution! \*\*\*
    

.. index:: b2ardr_no_smoothing

``b2ardr_no_smoothing``    type: ``integer``    default: ``0``
    When set to 1, disables the tail smoothing for of rate coefficients to represent the effect of a power-law tail on the distribution function. It has been added for compatibility with SOLPS4.3
    

.. index:: b2ardr_fix_recomb

``b2ardr_fix_recomb``    type: ``integer``    default: ``0``
    When changed from 0, and if the ADAS option is in use, then uses the PRB file to add the contribution arising from is-->is-1 processes.
    This term includes the Bremsstrahlung.
    The default option ('0') only contains the Bremsstrahlung for the is-->is-1 process.
    This option should be used with the 'b2stel\_fix\_recomb\_energy' option b2mn.dat set to '1'. See 'Physics' section.
    \*\*\* Use with caution! \*\*\*
    

.. index:: b2ardr_rtn.

.. index:: b2ardr_rtnt, b2ardr_rtnn
.. c

``b2ardr_rtn.``

  - ``b2ardr_rtnt``  -     type: ``integer``    default: ``40``

  - ``b2ardr_rtnn``  -     type: ``integer``    default: ``16``


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


.. index:: 
   single: Atomic Physics; b2ardr_fix_cx
   single: Atomic Physics; b2ardr_no_weisheit
   single: Atomic Physics; b2ardr_no_smoothing
   single: Atomic Physics; b2ardr_fix_recomb
   single: Atomic Physics; b2ardr_rtn.
   single: Atomic Physics; b2mndr_dpc_mod_rates_*_hot*

*************
b2.parameters
*************
.. index:: b2.neutrals.parameters

b2.neutrals.parameters
======================
.. index:: NSTRAI

``NSTRAI``    type: ``integer``    default: ``0``
    Number of neutral sources, or 'strata'. Must not be larger than DEF\_NSTRA from $(SOLPSTOP)/include(.local)/DIMENSIONS.F file. 
    Need not include the time-dependent stratum. If a time-dependent stratum is used, is incremented internally as needed. The incremented value is referred to as NSTRAT below.
    

.. index:: RCPOS

``RCPOS``    type: ``integer array of length (NSTRAT)``    default: ``-2``
    Position in the B2 grid of the of strata. Similar use as BCPOS from /BOUNDARY/ namelist.
    

.. index:: RCSTART

``RCSTART``    type: ``integer array of length (NSTRAT)``    default: ``-2``
    Start coordinate on the B2 grid the strata. Similar use as BCSTART from /BOUNDARY/ namelist.
    

.. index:: RCEND

``RCEND``    type: ``integer array of length (NSTRAT)``    default: ``-2``
    End coordinate on the B2 grid of the strata. Similar use as BCEND from /BOUNDARY/ namelist.
    

.. index:: RC_LIST_SIZE

``RC_LIST_SIZE``    type: ``integer array of length (NSTRAT)``    default: ``0``
    Contains the size of the recycling boundary lists. Similar use as BC\_LIST\_SIZE from /BOUNDARY/ namelist.
    

.. index:: RC_LIST_X

``RC_LIST_X``    type: ``integer array of length (2*(NXD+NYD),NSTRAT)``    default: ``-2``
    Contains the X-coordinate of the cells where recycling boundaries are applied. Similar use as BC\_LIST\_X from /BOUNDARY/ namelist.
    

.. index:: RC_LIST_Y

``RC_LIST_Y``    type: ``integer array of length (2*(NXD+NYD),NSTRAT)``    default: ``-2``
    Contains the Y-coordinate of the cells where recycling boundaries are applied. Similar use as BC\_LIST\_Y from /BOUNDARY/ namelist.
    

.. index:: TARGSP

``TARGSP``    type: ``integer array of size (NSTRAT,NTRACK)``    default: ``b2stbr_sput_dst``
    Identifies the base material(s) of this stratum wall. The number corresponds to the B2 species index produced by sputtering. Check b2cdci for details. If the bulk species is not sputtered, should contain -1.
    

.. index:: CHEMSP

``CHEMSP``    type: ``logical array of length NSTRAT``    default: ``.false.``
    Indicates whether chemical sputtering is allowed from this wall stratum.
    

.. index:: RECYC

``RECYC``    type: ``real*8 array of size (0:NS-1,NSTRAT)``
    Stores the particle recycling coefficients of species (is) on stratum (istra). Defaults to 1.0 for non-carbon species and 0.0 for carbon species. Particles recycle into the neutral species associated to their homonuclear sequence. 
    Applies to B2 neutral fluid species.
    Also multiplies Eirene recycling fluxes if 'eirene\_use\_recyceir' is set to 0 (see b2cdci for details).
    

.. index:: MRECYC

``MRECYC``    type: ``real*8 array of size (0:NS-1,NSTRAT)``    default: ``0.0``
    Stores the parallel momentum recycling coefficients of species (is) on stratum (istra). The parallel momentum is carried back by the recycled neutrals. Applies only to B2 neutral fluid species.
    

.. index:: ERECYC

``ERECYC``    type: ``real*8 array of size (0:NS-1,NSTRAT)``
    Stores the energy recycling coefficients of species (is) on stratum (istra). Defaults to 0.3 for non-carbon species and 0.0 for carbon species. The energy is carried back by the recycled neutrals.
    Applies only to B2 neutral fluid species.
    

.. index:: RCION

``RCION``    type: ``real*8 array of size (0:NS-1,NSTRAT)``    default: ``0.0``
    Stores the particle-into-ion recycling coefficients of species (is) on stratum (istra). Particles recycle into the next ionised species associated to their homonuclear sequence. Applies only to B2 neutral fluid species.
    

.. index:: RECYCEIR

``RECYCEIR``    type: ``real*8 array of size (NSTRAT)``    default: ``1.0``
    Multiplier to the Eirene recycling fluxes from stratum (istra). Only used if 'eirene\_use\_recyceir' is set to 1 (default).
    

.. index:: USERFLUXPARM

``USERFLUXPARM``    type: ``real*8 array of size (NSTRAT,2)``    default: ``0``
    The element (istra,1) contains the strength of constant gas puff strata (type 'C') for Eirene in particles/second.
    

.. index:: CRCSTRA

``CRCSTRA``    type: ``character*1 array of length (NSTRAT)``    default: `` ``
    Contains the type of stratum for Eirene. Possible options include:
    'N','S','W','E' - topological mesh boundaries (same use as BCCHAR in /BOUNDARY/ namelist)
    'V' - volume recombination source (related RCPOS, RCSTART, RCEND and RC\_LIST variables are ignored).
    'C' - constant or feedback gas puff source (related RCPOS, RCSTART, RCEND and RC\_LIST variables are ignored). Gas puffs for B2 fluid neutrals are handled via b2.boundary.parameters. Unless specified otherwise by use of 'eirene\_nesepm\_istra', it is the first 'C' stratum that is used for feedback puff schemes. See b2cdci for details.
    'T' - time-dependent source for Eirene (related RCPOS, RCSTART, RCEND and RC\_LIST variables are ignored). Long-lived Eirene neutrals are stored in this stratum. See EIRENE\_STEP\_DT below.
    

.. index:: RF_NEUT

``RF_NEUT``    type: ``real*8 array of size (4)``    default: ``1.0``
    Relaxation parameters multiplying the Eirene particle, parallel momentum, electron energy and ion energy sources respectively before use in B2.
    

.. index:: PHYS_SPUT

``PHYS_SPUT``    type: ``real*8 array of size (0:NS-1,NSTRAT)``    default: ``0.0``
    Stores the physical sputtering multiplier for B2 species (is) sputtering on the wall of stratum (istra). Must be non-zero for physical sputtering to occur. Only applies if using B2 fluid neutral model.
    

.. index:: CHEM_SPUT

``CHEM_SPUT``    type: ``real*8 array of size (0:NS-1,NSTRAT)``    default: ``0.0``
    Stores the chemical sputtering multiplier for B2 species (is) sputtering on the wall of stratum (istra). Must be non-zero for chemical sputtering to occur. Only applies if using B2 fluid neutral model.
    

.. index:: EIRENE_STEP_CPU

``EIRENE_STEP_CPU``    type: ``real*8``
    Length of CPU time devoted to Eirene calls after the first one (in s). Defaults to the value given in input.dat.
    

.. index:: EIRENE_STEP_DT

``EIRENE_STEP_DT``    type: ``real*8``    default: ``1.0e-3``
    Physical time (in s) the Eirene particles are to be followed before being passed to the time-dependent stratum.
    

.. index:: EIRENE_MOD

``EIRENE_MOD``    type: ``integer``    default: ``1``
    Frequency of Eirene calls. Eirene is called every EIRENE\_MOD full B2 iterations.
    

.. index:: VOLRECSTART

``VOLRECSTART``    type: ``real*8 array of size (NSTRAT)``    default: ``1.e21``
    Initial volume recombination rate from stratum (istra) to be used for the volume recombination scaling regulation algorithm. Rendered obsolete by 'eirene\_dpc\_fix'.
    

.. index:: VOLRECINC

``VOLRECINC``    type: ``real*8``
    Maximum rate of increase of the volume recombination source strength. The volume recombination regulation scaling scheme is activated if VOLRECINC is neither 0 nor 1.
    Rendered obsolete by 'eirene\_dpc\_fix'.
    

.. index:: VOLRECWT

``VOLRECWT``    type: ``real*8``    default: ``0.1``
    Weight of new volume recombination strength relative to that of previous iteration in the volume recombination regulation scaling scheme.
    Rendered obsolete by 'eirene\_dpc\_fix'.
    

.. index:: SPECIES_START

``SPECIES_START``    type: ``integer array of size (NSTRAT)``    default: ``0``
    Specifies the index of the first B2 species involved in stratum (istra).
    

.. index:: SPECIES_END

``SPECIES_END``    type: ``integer array of size (NSTRAT)``    default: ``ns-1``
    Specifies the index of the last B2 species involved in stratum (istra).
    

.. index:: NEUTRALS_FILENAME

``NEUTRALS_FILENAME``    type: ``character*256``    default: ``b2.neutrals.parameters``
    Name of the next file to use for reading a new /NEUTRALS/ namelist.
    

.. index:: NEUTRALS_TIME_MOD

``NEUTRALS_TIME_MOD``    type: ``real*8``    default: ``0.0``
    When the B2 run simulation time, in seconds,\*     				modulo(NEUTRALS\_TIME\_MOD), exceeds NEUTRALS\_TIME\_SWITCH, reads the new namelist from NEUTRALS\_FILENAME. Also switches to the new namelist if the ELM count (here time/NEUTRALS\_TIME\_MOD) changes. Only active if NEUTRALS\_TIME\_MOD is greater than 0.
    

.. index:: NEUTRALS_TIME_SWITCH

``NEUTRALS_TIME_SWITCH``    type: ``real*8``    default: ``0.0``
    Time (in seconds) within an ELM cycle after which a new NEUTRALS namelist is read.
    

.. index:: L_NEUTRAD

``L_NEUTRAD``    type: ``integer``    default: ``0``
    If l\_neutrad >= 0, then the radiated power due to the neutrals atoms is taken directly from the Eirene calculation, instead of being recomputed by B2.
    

.. index:: L_NEUTFLUX

``L_NEUTFLUX``    type: ``integer``
    If l\_neutflux >=0, then correct treatment of the incident fluxes in B2 and b2plot; if <0, then old (approximate) treatment
    

.. index:: LSTRASCL

``LSTRASCL``    type: ``integer array of size (NSTRAT,0:natm)``
    Indicates with which Eirene atomic species to scale the Eirene stratum (istra) (0 means no scaling, default). Atomic species 0 stands for electrons.
    

.. index:: B2ESPCR

``B2ESPCR``    type: ``integer array of size (0:NS-1)``    default: ``ordering of the B2 isonuclear sequences``
    Contains the index of the Eirene atomic species corresponding to the B2 species (is).
    

.. index:: EB2SPCR

``EB2SPCR``    type: ``integer array of size (NATM)``    default: ``first B2 species of each isonuclear sequence``
    Contains the index of the B2 neutral fluid species corresponding to the Eirene atomic species (iatm).
    

.. index:: LMOLSCL

``LMOLSCL``    type: ``integer array of size (NMOL)``    default: ``0``
    Contains the index of the Eirene atomic species with which the Eirene molecular species (IMOL) should be scaled.
    

.. index:: MLCMP

``MLCMP``    type: ``integer array of size (NATM,NMOL)``    default: ``0``
    Contains the number of atoms from Eirene atomic species IATM within each molecule of Eirene molecular species IMOL.
    

.. index:: LIONSCL

``LIONSCL``    type: ``integer array of size (NION)``    default: ``0``
    Contains the index of the Eirene atomic species with which the Eirene test ion species (IION) should be scaled.
    

.. index:: LCNS

``LCNS``    type: ``integer array of size (NSTS)``    default: ``0``
    Contains the indices of Eirene non-standard surfaces (block 3A in input.dat) corresponding to core boundaries.
    

.. index:: LTNS

``LTNS``    type: ``integer array of size (NSTS)``    default: ``0``
    Contains the indices of Eirene non-standard surfaces (block 3A in input.dat) corresponding to target boundaries.
    

.. index:: LSNS

``LSNS``    type: ``integer array of size (NSTRAT)``    default: ``0``
    Contains the indices of Eirene surfaces related to the recycling sources.
    

.. index:: KSNS

``KSNS``    type: ``integer array of size (NSTRAT)``    default: ``0``
    Contains the number of parts for each Eirene recycling stratum.
    

.. index:: GPFC

``GPFC``    type: ``real*8 array of size (NATM,NSTRAT)``    default: ``0.0``
    Specifies the fraction of Eirene atomic species (iatm) in one particle puffed from stratum (istra).
    

.. index:: DBG_EIR_MC

``DBG_EIR_MC``    type: ``integer``    default: ``0``
    Debug output control for eirene\_mc routine. See code for usage.
    

.. index:: DEBUG_FLAGS

``DEBUG_FLAGS``    type: ``integer array of size (100)``    default: ``0``
    Non-zero elements yield additional print-out data for debugging B2-Eirene coupling. See code for specific uses. Many slots still available for user-specific needs.
    

.. index:: NEUT_SCL_LIM

``NEUT_SCL_LIM``    type: ``real*8``    default: ``2.0``
    Maximum number by which Eirene neutral sources may be scaled in either direction within the ank-mods scheme. See explaining text in $SOLPSTOP/doc/Source\_Scaling\_in\_B2.pdf for details.
    

.. index:: TRACK_INDEX

``TRACK_INDEX``    type: ``integer array of size (0:NS-1)``    default: ``1 for species spud_dst, 0 for other``
    Specifies the mixed material species index related to B2 species (is).
    

.. index:: TRACK_CHEM_SPUT

``TRACK_CHEM_SPUT``    type: ``logical array of size (NTRACK)``
    Indicates whether mixed material species (itrack) participates in chemical sputtering. Defaults to .true. for first tracked species if sput\_dst is carbon, and to .false. for all other cases.
    

.. index:: CHEMICAL_EROSION_REDEP_FAC

``CHEMICAL_EROSION_REDEP_FAC``    type: ``real*8``    default: ``1.0``
    Multiplier to the chemical sputtering coefficient of carbon for computing the rate used for redeposited carbon.
    

.. index:: CHEMICAL_EROSION_BE_FAC

``CHEMICAL_EROSION_BE_FAC``    type: ``logical``    default: ``.false.``
    Indicates whether the presence of beryllium is to impact on the chemical sputtering yield of carbon.
    

.. index:: CHEMICAL_EROSION_BE_FAC_A

``CHEMICAL_EROSION_BE_FAC_A``    type: ``real*8``    default: ``0.2``
    The chemical sputtering yield of carbon is multiplied by
    (1.0-C/2\*(tanh((frac-A)/B)-tanh((-A)/B)))
    where frac is the fractional content of Be in the surface layer material.
    

.. index:: CHEMICAL_EROSION_BE_FAC_B

``CHEMICAL_EROSION_BE_FAC_B``    type: ``real*8``    default: ``0.05``
    See above.
    

.. index:: CHEMICAL_EROSION_BE_FAC_C

``CHEMICAL_EROSION_BE_FAC_C``    type: ``real*8``    default: ``0.9``
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

``SPS_ABSR``    type: ``real*8 array of length (N_SPCSRF)``    default: ``-1.0``
    Particle absorption on the surface. If positive, will supercede the setting from the Eirene input file: RECYCT = 1-SPS\_ABSR. Ignored if negative.
    

.. index:: SPS_TRNO

``SPS_TRNO``    type: ``real*8 array of length (N_SPCSRF)``    default: ``-1.0``
    Surface transparency in positive direction. If positive, will supercede the setting from the Eirene input file: TRANSP(1,) = SPS\_TRNO. Ignored if negative.
    

.. index:: SPS_TRNI

``SPS_TRNI``    type: ``real*8 array of length (N_SPCSRF)``    default: ``-1.0``
    Surface transparency in negative direction. If positive, will supercede the setting from the Eirene input file: TRANSP(2,) = SPS\_TRNI. If negative, the setting from SPS\_TRNO is used.
    

.. index:: SPS_MTRI

``SPS_MTRI``    type: ``real*8 array of length (N_SPCSRF)``    default: ``0``
    Surface material in Eirene notation (e.g., 1206 for C). If positive, will supercede the setting from the Eirene input file: ZNML = SPS\_MTRI. Ignored if negative.
    

.. index:: SPS_MTRL

``SPS_MTRL``    type: ``character*8 array of length (N_SPCSRF)``
    Surface material in human notation (e.g., 'C').
    

.. index:: SPS_TMPR

``SPS_TMPR``    type: ``real*8 array of length (N_SPCSRF)``    default: ``1.e15``
    Surface temperature (in eV). If set larger to 1.e10, will be ignored. Otherwise, will supercede the setting from the Eirene input file: EWALL = SPS\_TMPR.
    

.. index:: SPS_SPPH

``SPS_SPPH``    type: ``real*8 array of length (N_SPCSRF)``    default: ``-1.0``
    Fudge factor for physical sputtering. If positive, will supercede the setting from the Eirene input file: RECYCS = SPS\_SPPH. Ignored if negative.
    

.. index:: SPS_SPCH

``SPS_SPCH``    type: ``real*8 array of length (N_SPCSRF)``    default: ``-1.0``
    Fudge factor for chemical sputtering. If positive, will supercede the setting from the Eirene input file: RECYCC = SPS\_SPCH. Ignored if negative.
    

.. index:: SPS_SGRP

``SPS_SGRP``    type: ``integer array of length (N_SPCSRF)``    default: ``-1``
    Sputtered particle species flag for chemical sputtering. If positive, will supercede the setting from the Eirene input file: ISRC = SPS\_SGRP. Ignored if negative.
    

.. index:: WRITE_NML_NEUT

``WRITE_NML_NEUT``    type: ``logical``    default: ``.true.``
    If .true. (default), writes the content of the namelist to stdout after it has been read.
    

.. index:: TIME_DEP_PUFF

``TIME_DEP_PUFF``    type: ``logical array of length (NSTRAT)``    default: ``.false. for all strata``
    Indicates whether a stratum is a time-dependent gas puff. Should only be .true. for strata defined as gas puffs.
    

.. index:: NGPDATA

``NGPDATA``    type: ``integer data of size (NSTRAT)``    default: ``0``
    Number of points over which the time profile of the strength of gas puff (istra) is given. Defaults to 0. Current maximum value is 100.
    

.. index:: GPDATA

``GPDATA``    type: ``real*8 data of size (NGPDATA,2,NSTRAT)``    default: ``0.0``
    For (i,ik,istra) in (1:NGPDATA(istra),1:2,1:NSTRAT),
    GPDATA(i,1,istra) contains the time point (i) for stratum (istra) (in s).
    GPDATA(i,2,istra) contains the gas puff strength of stratum (istra) at time point (i) (in particles/s).
    The gas puff strength before the first time point is given by USERFLUXPARM(1,istra).
    The gas puff strength after the last time point is given by the GPDATA value of the last time point.
    Otherwise, the gas puff strength is linearly interpolated from the given data.
    

.. index:: CHEMICAL_SPUTTER_YIELD

``CHEMICAL_SPUTTER_YIELD``    type: ``real*8 array of size (0:NLIM+NSTS)``    default: ``0.0``
    Passed to Eirene. Chemical sputter yield of wall surface (ilim).
    

.. index:: FCHAR_CHEMICAL

``FCHAR_CHEMICAL``    type: ``real*8``    default: ``0``
    Nuclear charge of atomic species causing the sputtering. Default means no chemical sputtering.
    

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
   single: b2.neutrals.parameters; RECYC
   single: b2.neutrals.parameters; MRECYC
   single: b2.neutrals.parameters; ERECYC
   single: b2.neutrals.parameters; RCION
   single: b2.neutrals.parameters; RECYCEIR
   single: b2.neutrals.parameters; USERFLUXPARM
   single: b2.neutrals.parameters; CRCSTRA
   single: b2.neutrals.parameters; RF_NEUT
   single: b2.neutrals.parameters; PHYS_SPUT
   single: b2.neutrals.parameters; CHEM_SPUT
   single: b2.neutrals.parameters; EIRENE_STEP_CPU
   single: b2.neutrals.parameters; EIRENE_STEP_DT
   single: b2.neutrals.parameters; EIRENE_MOD
   single: b2.neutrals.parameters; VOLRECSTART
   single: b2.neutrals.parameters; VOLRECINC
   single: b2.neutrals.parameters; VOLRECWT
   single: b2.neutrals.parameters; SPECIES_START
   single: b2.neutrals.parameters; SPECIES_END
   single: b2.neutrals.parameters; NEUTRALS_FILENAME
   single: b2.neutrals.parameters; NEUTRALS_TIME_MOD
   single: b2.neutrals.parameters; NEUTRALS_TIME_SWITCH
   single: b2.neutrals.parameters; L_NEUTRAD
   single: b2.neutrals.parameters; L_NEUTFLUX
   single: b2.neutrals.parameters; LSTRASCL
   single: b2.neutrals.parameters; B2ESPCR
   single: b2.neutrals.parameters; EB2SPCR
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
   single: b2.neutrals.parameters; TIME_DEP_PUFF
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
    Contains the filename from which to extract the surface material properties for wall element (iwall). The files are to be found in $(SOLPSTOP)/data(.local)/Surface\_properties/.
    

.. index:: COATING_MATERIAL_NAME

``COATING_MATERIAL_NAME``    type: ``character*6 of size (NWALL)``    default: `` ``
    Contains the filename from which to extract the bulk material properties of the eventual coating for wall element (iwall).
    

.. index:: BULK_MATERIAL_NAME

``BULK_MATERIAL_NAME``    type: ``character*6 of size (NWALL)``    default: ``C``
    Contains the filename from which to extract the bulk material properties for wall element (iwall). The files are to be found in $(SOLPSTOP)/data(.local)/Bulk\_properties/.
    

.. index:: LAYER_ALLOYS

``LAYER_ALLOYS``    type: ``character*6 of size (NALLOYS)``
    Contains the filename from which to extract the material properties for alloy (nalloy) which may be present in mixed materials deposited layers. Not yet operational. The files are to be found in $(SOLPSTOP)/data(.local)/Bulk\_properties/ and $(SOLPSTOP)/data(.local)/Surface\_properties/.
    

.. index:: TARGET_TEMP

``TARGET_TEMP``    type: ``real*8 array of size (NWALL,NDEPTH)``
    Contains the temperature (in Kelvin) of wall element (iwall) at depth layer (idepth).
    If plate\_option.eq.1, will be set to backplate\_temp(iwall).
    If plate\_option.eq.2 and empty, will be set to equilibrium 1-D profile deduced from plasma incoming fluxes.
    If plate-option.eq.3, must be set.
    

.. index:: INERTIAL_COOLING

``INERTIAL_COOLING``    type: ``logical array of size (NWALL)``    default: ``.false.``
    Indicates whether wall element (iwall) is inertially cooled instead of actively cooled.
    

.. index:: BACKPLATE_TEMP

``BACKPLATE_TEMP``    type: ``real*8 array of size (NWALL)``    default: ``b2stbr_plate_temp``
    Contains the temperature (in Kelvin) maintained by cooling at the back end of wall element (iwall).
    

.. index:: PLATE_THICKNESS

``PLATE_THICKNESS``    type: ``real*8 array of size (NWALL)``    default: ``b2stbr_plate_thick``
    Contains the thickness (in meters) of wall element (iwall).
    

.. index:: COATING_THICKNESS

``COATING_THICKNESS``    type: ``real*8 array of size (NWALL)``    default: ``0``
    Contains the thickness (in meters) of the eventual coating on wall element (iwall).
    

.. index:: PLATE_TIME_FACTOR

``PLATE_TIME_FACTOR``    type: ``real*8 array of size (NWALL)``    default: ``1.0``
    Multiplier to the time for the equations for temperature and composition evolution of wall element (iwall).
    

.. index:: DEPOSITION

``DEPOSITION``    type: ``real*8 array of size (NWALL, NTRACK)``    default: ``0.0``
    Contains the amount of deposited material (in atoms) from species (itrack) onto wall element (iwall).
    

.. index:: EROSION

``EROSION``    type: ``real*8 array of size(NWALL, NTRACK)``    default: ``0.0``
    Contains the amount of eroded material (in atoms) of species (itrack) from wall element(iwall).
    

.. index:: CHEMICAL_SPUTTERING

``CHEMICAL_SPUTTERING``    type: ``real*8 array of size (NWALL,0:NS-1)``    default: ``0.0``
    Contains the chemical sputter yield of 'sput\_dst' or 'sput\_dst\_bulk' species on wall element (iwall) caused by B2 species (is).
    

.. index:: PHYSICAL_SPUTTERING

``PHYSICAL_SPUTTERING``    type: ``real*8 array of size (NWALL,0:NS-1)``    default: ``0.0``
    Contains the physical sputter yield of 'sput\_dst' or 'sput\_dst\_bulk' species on wall element (iwall) caused by B2 species (is).
    

.. index:: PHYSICAL_SPUTTERING_ENERGY

``PHYSICAL_SPUTTERING_ENERGY``    type: ``real*8 array of size (NWALL,0:NS-1)``    default: ``0.0``
    Contains the fraction of returned energy carried by sputtered particles of species 'sput\_dst' or 'sput\_dst\_bulk' species from wall element (iwall) caused by B2 species (is).
    

.. index:: RES_SPUTTERING

``RES_SPUTTERING``    type: ``real*8 array of size (NWALL,0:NS-1)``    default: ``0.0``
    Contains the RES sputter yield of 'sput\_dst' or 'sput\_dst\_bulk' species on wall element (iwall) caused by B2 species (is).
    

.. index:: THERMAL_EVAPORATION

``THERMAL_EVAPORATION``    type: ``real*8 array of size(NWALL,0:NS-1)``    default: ``0.0``
    Contains the rate of thermal evaporation of species (is) (in particles/second) from wall element (iwall).
    

.. index:: BACKSCATTERING

``BACKSCATTERING``    type: ``real*8 array of size (NWALL,0:NS-1)``    default: ``0.0``
    Contains the backscattering fraction for incoming B2 species (is) onto wall element (iwall).
    

.. index:: BACKSCATTERING_ENERGY

``BACKSCATTERING_ENERGY``    type: ``real*8 array of size (NWALL,0:NS-1)``    default: ``0.0``
    Contains the backscattered energy fraction for incoming B2 species (is) onto wall element (iwall).
    

.. index:: PLATE_TIME

``PLATE_TIME``    type: ``real*8 array of size (NWALL)``    default: ``0.0``
    Indicates how much simulation time has elapsed for wall element (iwall) (in seconds).
    

.. index:: PLATE_AREA

``PLATE_AREA``    type: ``real*8 array of size (NWALL)``
    Indicates the wall area (in square meters) for wall element (iwall). Defaults to the area computed from the B2 grid information.
    

.. index:: MONOLAYER_DEPOSITION

``MONOLAYER_DEPOSITION``    type: ``real*8 array of size (NWALL,NTRACK)``    default: ``0.0``
    Contains the amount of deposited material (in monolayers) from species (itrack) onto wall element (iwall).
    

.. index:: MONOLAYER_EROSION

``MONOLAYER_EROSION``    type: ``real*8 array of size (NWALL,NTRACK)``    default: ``0.0``
    Contains the amount of eroded material (in monolayers) of species (itrack) from wall element (iwall).
    

.. index:: LAYER_NCONSTITUENTS

``LAYER_NCONSTITUENTS``    type: ``integer array of size (NWALL)``    default: ``1``
    Indicates the number of elemental constituents within the surface layer of wall element (NWALL).
    

.. index:: LAYER_NZCONSTITUENTS

``LAYER_NZCONSTITUENTS``    type: ``integer array of size (NWALL,6+NTRACK)``
    Contains the atomic numbers Z of the various elements present within the surface layer of wall element (iwall). Defaults to 6 for the first value, 0 otherwise.
    

.. index:: LAYER_NRELCONSTITUENTS

``LAYER_NRELCONSTITUENTS``    type: ``real*8 array of size (NWALL,6+NTRACK)``
    Contains the relative atomic abundances of the various elements present within the surface layer of wall element (iwall). Defaults to 1.0 for the first value, 0.0 otherwise.
    

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
   single: b2.wall_save.parameters; LAYER_NRELCONSTITUENTS

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

``TIME``    type: ``real*8``    default: ``0.0``
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
    Specifies the nature of the boundary segment
    N = 'North' boundary
    S = 'South' boundary
    W = 'West' boundary
    E = 'East' boundary
    X = 'X' boundary used for specifying a fixed value on a row of cells
    Y = 'Y' boundary used for specifying a fixed value on a column of cells
    

.. index:: CONPAR

``CONPAR``    type: ``real*8 array of size (0:NS-1,NBC,3)``    default: ``0.0``
    Contains parameters helping to define the boundary conditions for the continuity equation of species (is). See description of BCCON below for details.
    

.. index:: MOMPAR

``MOMPAR``    type: ``real*8 array of size (0:NS-1,NBC,2)``    default: ``0.0``
    Contains parameters helping to define the boundary conditions for the parallel momentum equation of species (is). See description of BCMOM below for details.
    

.. index:: ENEPAR

``ENEPAR``    type: ``real*8 array of size (NBC,2)``    default: ``0.0``
    Contains parameters helping to define the boundary conditions for the electron energy equation. See description of BCENE below for details.
    

.. index:: ENIPAR

``ENIPAR``    type: ``real*8 array of size (NBC,2)``    default: ``0.0``
    Contains parameters helping to define the boundary conditions for the ion energy equation. See description of BCENI below for details.
    

.. index:: POTPAR

``POTPAR``    type: ``real*8 array of size (NBC,2)``    default: ``0.0``
    Contains parameters helping to define the boundary conditions for the potential equation. See description of BCPOT below for details.
    

.. index:: BCPOS

``BCPOS``    type: ``integer array, length (NBC)``    default: ``-2``
    For North, South or X boundary conditions, it specifies the row index; for West, East and Y boundary conditions, it specifies the column index.
    

.. index:: BCSTART

``BCSTART``    type: ``integer array, length (NBC)``    default: ``-2``
    For North, South or X boundary conditions, it specifies the start column index; for West, East and Y boundary conditions, it specifies the start row index.
    

.. index:: BCEND

``BCEND``    type: ``integer array, length (NBC)``    default: ``-2``
    For North, South X boundary conditions, it specifies the end column index; for West, East and Y boundary conditions, it specifies the end row index.
    

.. index:: BC_LIST_SIZE

``BC_LIST_SIZE``    type: ``integer array of length (NBC)``    default: ``0``
    Contains the size of the list of cells where a boundary condition is applied.
    

.. index:: BC_LIST_X

``BC_LIST_X``    type: ``integer array of length (2*(NXD+NYD),NBC)``    default: ``-2``
    Contains the X-coordinate of the cells where boundaries conditions are applied.
    

.. index:: BC_LIST_Y

``BC_LIST_Y``    type: ``integer array of length (2*(NXD+NYD),NBC)``    default: ``-2``
    Contains the Y-coordinate of the cells where boundaries conditions are applied.
    

.. index:: BCCON

``BCCON``    type: ``integer array, length (0:NS-1,NBC)``
    Specifying the type of density boundary condition for each segment and species (fastest varying index is species); makes use of CONPAR to specify additional information, as indicated:

    |	 0 : default, no boundary condition is applied
    |	 1 : prescribe the value of the density, CONPAR(,,1) specifies the required density in m^-3`
    |	 2 : prescribe the gradient of the density, CONPAR(,,1) specifies the required density gradient in m^-4`
    |	 3 : sheath conditions, CONPAR(,,1) not used (zero gradient is used)
    |	 4 : prescribe the value of the density, weakly a mixed boundary condition, CONPAR(,,1) specifies the required density in m^-3` and CONPAR(,,2) specifies the 'strength' of the boundary condition
    |	 5 : prescribe the particle flux per unit area, CONPAR(,,1) specifies the required particle flux density in m^-2` s^-1`
    |	 6 : prescribe the total particle flux for a constant density, CONPAR(,,1) specifies the particle flux in s^-1`
    |	 7 : prescribe the density as a function of other plasma parameters [not yet available]
    |	 8 : prescribe the total particle flux with constant flux density, CONPAR(,,1) specifies the particle flux in s^-1`
    |	 9 : prescribe the decay length for the density, CONPAR(,,1) specifies the gradient length in $m$ (should use type 15 instead when drifts are turned on)	
    |	10 : leakage option for density, recommended for cases with drifts, CONPAR(,,1) specifies the leakage factor, alpha in Gamma\_loss = alpha C`_s` n`_a`
    |	11 : particle flux feedback boundary condition, CONPAR(,,1) not used, derived from CBSNA(0,IS,IREG). The species used must be declared using the 'b2stbc\_isfeedback' switch.
    |	12 : particle density feedback boundary condition, as above, CONPAR(,,1) not used, derived from CBSNA(0,IS,IREG). The species used must be declared using the 'b2stbc\_isfeedback' switch.
    |	13 : particle density to achieve specified total flux, 
    |		CONPAR(,,1) is the specified flux crossing the flux surface 'b2stbc\_type13\_ref' steps away from the boundary,
    |		CONPAR(,,2) is the strength of the feedback,
    |		CONPAR(,,3)) when running with Eirene and the 'ionising core' switch is used, 
    |		CONPAR(,,2) is set internally to match the re-entering flux of ionised neutrals that crossed the core boundary (when running with Eirene and the 'ionising\_core' option).
    |		The feedback scheme can be further tweaked with the switches 'b2stbc\_type13\_norm' and 'b2stbc\_type13\_fac'. See code for details.
    |	14 : sound speed velocity flux, CONPAR(,,1) is a multiplier to the outgoing sound speed C`_s`..
    |	15 : prescribe a radial leakage velocity, CONPAR(,,1) specifies the leakage velocity in units of the local thermal velocity.
    |	16 : particle density to achieve specified total flux, used with ASTRA coupling. The total desired flux is summed over all BCCON=16 core boundaries. CONPAR(,,1) specifies the desired particle flux in s^-1` .
    |	18 : prescribe total main ion particle flux, used with ASTRA coupling.
    |	19 : particle flux feedback boundary condition, flux is summed over neutrals and ions, for coupling with ASTRA. The total desired flux is summed over all BCCON=19 core boundaries. This boundary condition type is applied to ions in their highest ionisation stage. CONPAR(,,1) specifies the desired particle flux in s^-1` .
    |	20 : constant density feedback condition, CONPAR(,,1) specifies the desired density in m^-3` .
    |	21 : prescribe the value of the density and add a density perturbation to get a solution which is as close as possible to neoclassical theory. It is recommended to use this boundary condition together with corresponding condition on ion temperature (BCENI=24). The total desired density is summed over all BCCON=21 core boundaries. CONPAR(,,1) specifies the desired density in m^-3`..
    |	22 : Feedback boundary condition: given total particle flux with constant average density. The poloidal density variation is added to make the solution as close as possible to the neoclassical value derived for pure H/D/T plasma. It is recommended to use this boundary condition with corresponding boundary condition on ion temperature (BCENI=23,24). The total desired flux is summed over all BCCON=22 core boundaries. CONPAR(,,1) specifies the desired particle flux in s^-1` .
    |	23 : Feedback boundary condition: given sum of integrated neutrals and main ion particle fluxes with constant average density. The poloidal density variation is added to make the solution as close as possible to the neoclassical value derived for pure H/D/T plasma. It is recommended to use this boundary condition with corresponding boundary condition on ion temperature (BCENI=23,24). The total desired flux is summed over all BCCON=23 core boundaries. CONPAR(,,1) specifies the desired particle flux in s^-1` .
    |	24 : constant density feedback scaled by density on the ring 'bc\_type21\_ref' away. CONPAR(,,1) specifies the desired density in m^-3` . CONPAR(,,2) is the strength of the feedback
    |	25 : Feedback boundary condition: prescribe the average value of the density and add a density perturbation from neighbouring radial cell. This boundary condition is suitable for any species of a multi-species plasma (i.e. in the case when the condition used in BCCON=21 fails). It is recommended to use this boundary condition together with the corresponding condition on ion temperature (BCENI=26,27). CONPAR(,,1) specifies the desired average density in m^-3` .
    |	26 : Feedback boundary condition: prescribe the total ion flux and find the average density. A density perturbation is taken from the neighbouring radial cell. This boundary condition is suitable for any species of a multi-species plasma (i.e. in the case when the condition used in BCCON=22 fails). It is recommended to use this boundary condition together with a corresponding condition on the ion temperature (BCENI=26,27). The total desired flux is summed over all BCCON=26 core boundaries. CONPAR(,,1) specifies the desired particle flux in s^-1` .
    |	27 : Feedback boundary condition: prescribe the particle flux sum for all neutrals and ions belonging to a given isonuclear sequence and find the average density of the highest ionization stage. A density perturbation is taken from the neighbouring radial cell. It is recommended to use this boundary condition together with corresponding condition on ion temperature (BCENI=25,26). The total desired flux is summed over all BCCON=27 core boundaries. CONPAR(,,1) specifies the desired particle flux in s^-1` .

    

.. index:: BCMOM

``BCMOM``    type: ``integer array, length NS * NBC``
    Specifying the type of parallel momentum or velocity boundary condition for each segment and species (fastest varying index is species); makes use of MOMPAR to specify additional information, as indicated

    |	 0 : default, no boundary condition is applied
    |	 1 : prescribe the value of the parallel velocity, MOMPAR(,,1) specifies the parallel velocity in m.s^-1`
    |	 2 : prescribe the gradient of the parallel velocity, MOMPAR(,,1) specifies the parallel velocity gradient in s^-1`
    |	 3 : sheath conditions, mach number as input, 
    |		if MOMPAR(,,2) < 0.5 , then the velocity is set to exactly 
    |		MOMPAR(,,1) \* C`_s,collective`,, otherwise the velocity is set to be at least MOMPAR(,,1) \* C`_s,collective`,, species
    |	 4 : prescribe the value of the velocity, weakly a mixed boundary condition, MOMPAR(,,1) specifies the parallel velocity in m.s^-1` and MOMPAR(,,2) specifies the 'strength' of the boundary condition
    |	 5 : prescribe the parallel momentum flux per unit area, MOMPAR(,,1) specifies the parallel momentum flux density in N.m^-2`
    |	 6 : prescribe the total parallel momentum flux for a constant parallel velocity [not yet available]
    |	 7 : prescribe the parallel momentum as a function of other plasma parameters [not yet available]
    |	 8 : special : limited shear, imposes zero gradient for the Mach number. [[[Eventually intended to have MOMPAR(,,1) specify the gradient of the Mach number in m^-1` ]]]
    |	 9 : prescribe the total parallel momentum flux with constant flux density, MOMPAR(,,1) specifies the parallel momentum flux in N
    |	10 : prescribe the decay length for the parallel momentum, MOMPAR(,,1) specifies the decay length in m
    |	11 : Rozhansky viscosity condition for the parallel momentum, MOMPAR(,,1) is not used
    |	12 : Condition from b2stbc\_spb for the parallel momentum
    |	13 : sheath boundary condition from b2stbc\_spb for the parallel momentum
    |	14 : Condition from b2stbc\_spb for the parallel momentum
    |	15 : Prescribe the value of the parallel velocity, scaled with B\_average/B\_local
    |	16 : Prescribe the average value of the parallel velocity MOMPAR(,,1) specifies the parallel velocity in m.s -1

    

.. index:: BCENE

``BCENE``    type: ``integer array, length NBC``
    Specifying the type of electron energy or temperature boundary condition for each segment; makes use of ENEPAR to specify additional information, as indicated

    |	 0 : default, no boundary condition is applied
    |	 1 : prescribe the value of the electron temperature, ENEPAR(,1) specifies the temperature in eV
    |	 2 : prescribe the gradient of the electron temperature, ENEPAR(,1) specifies the temperature gradient in eV.m -1
    |	 3 : sheath conditions, electron energy transmission, ENEPAR(,1) specifies an additional contribution to the energy transmission coefficient in addition to that of the potential difference [the sound speed used depends on settings of MOMPAR(,ISMAIN,2)]
    |	 4 : prescribe the value of the electron temperature, weakly a mixed boundary condition, ENEPAR(,1) specifies the temperature in eV and ENEPAR(,2) specifies the 'strength' of the boundary condition
    |	 5 : prescribe the electron energy flux per unit area, ENEPAR(,1) specifies the energy flux density in W.m-2
    |	 6 : prescribe the total electron energy flux for a constant electron temperature, ENEPAR(,1) specifies the energy flux in W (no longer supported, use types [16] or [17] instead)
    |	 7 : prescribe the electron temperature as a function of other plasma parameters [not yet available]
    |	 8 : prescribe the total electron heat flux with constant flux density, ENEPAR(,1) specifies the energy flux in W
    |	 9 : prescribe the decay length for the electron temperature, ENEPAR(,1) specifies the decay length in m (can also use type [19] instead)
    |	10 : feedback option for core, ENEPAR(,1) not used, derived from CBSHE(0,coreregno)
    |	11 : not used
    |	12 : sheath conditions, electron energy transmission coefficient, ENEPAR(,1) specifies an energy transmission factor, delta\_e in Q\_e = delta\_e Gamma\_e T\_e
    |	13 : prescribe the electron energy flux per unit area proportional to temperature, ENEPAR(,1) specifies the energy flux density per temperature in W m^-2` J^-1` (the temperature here in J)
    |	14 : leakage option for electron energy, ENEPAR(,1) specifies the leakage factor, alpha in Gamma\_loss = alpha C`_s` n`_e`
    |	15 : not used
    |	16 : Feedback boundary condition with constant temperature, ENEPAR(,1) specifies the power flux in W across the flux surface with index 'b2stbc\_type16\_ref' (default=-1), ENEPAR(,2) should be something like 0.1 and specifies the strength of the feedback. Also see type [17] below. Available if bcene\_16\_style=0 (default). If bcene\_16\_style=1, integrated electron heat flux with constant electron temperature, summed over all core boundaries with BCENE=16.
    |	17 : Feedback boundary condition with constant shared temperature for both electrons and ions, with ENEPAR(,1) + ENIPAR(,1) giving the total power flux in W across the flux surface with index 'b2stbc\_type16\_ref' (default=-1), ENEPAR(,2) should be something like 0.1 and specifies the strength of the feedback. Replaces [16] for high densities and large values of 'b2stbc\_type16\_ref'.
    |	18 : Fractional drop condition. Not yet working.
    |	19 : same as [9] but to be used when simultaneously setting BCCON=1 on the same boundary.
    |	20 : Feedback boundary condition with constant temperature, as per type [16] but with 'type20\_' switches and a different feedback scheme.
    |	21 : constant temperature feedback scaled by temperature on the ring bc\_type21\_ref away 
    |		ENEPAR(,1) specifies the desired electron temperature in eV. 
    |		ENEPAR(,2) is the strength of the feedback
    |	22 : radial leakage condition for the electron temperature. ENEPAR(,1) specifies the leakage velocity in units of the electron thermal velocity. A temperature gradient such that the diffusive flux is set to match this leakage is imposed.

    

.. index:: BCENI

``BCENI``    type: ``integer array, length NBC``
    Specifying the type of ion energy or temperature boundary condition for each segment; makes use of ENIPAR to specify additional information, as indicated

    |	 0 : default, no boundary condition is applied
    |	 1 : prescribe the value of the ion temperature, ENIPAR(,1) specifies the temperature in eV
    |	 2 : prescribe the gradient of the ion temperature, ENIPAR(,1) specifies the temperature gradient in eV.m^-1`
    |	 3 : sheath conditions, ion energy transmission, ENIPAR(,1) specifies the contribution to the energy transmission coefficient [the sound speed used depends on settings of MOMPAR(,ISMAIN,2)]
    |	 4 : prescribe the value of the ion temperature, weakly a mixed boundary condition, ENIPAR(,1) specifies the temperature in eV and ENIPAR(,2) specifies the 'strength' of the boundary condition
    |	 5 : prescribe the ion energy flux per unit area, ENIPAR(,1) specifies the energy flux density in W.m^-2`
    |	 6 : prescribe the total ion energy flux for a constant ion temperature, ENIPAR(,1) specifies the energy flux in W (no longer supported, use types [16] or [17] instead)
    |	 7 : prescribe the ion temperature as a function of other plasma parameters [not yet available]
    |	 8 : prescribe the total ion heat flux with constant flux density, ENIPAR(,1) specifies the energy flux in W
    |	 9 : prescribe the decay length for the ion temperature, ENIPAR(,1) specifies the decay length in m (can also use type [19] instead)
    |	10 : feedback option for core, ENIPAR(,1) not used, derived from cbshi(0,ISMAIN,coreregno)
    |	11 : sheath conditions, ion energy transmission coefficient, ENIPAR(,1) specifies an energy transmission factor, delta`_i` in Q`_i` = delta`_i` T`_i` sum`_a` n`_a` C`_s,a`
    |	12 : sheath conditions, ion energy transmission coefficient, ENIPAR(,1) specifies an energy transmission factor, delta`_i` in Q`_i` = delta`_i` T`_i` sum`_a` Gamma`_a`
    |	13 : prescribe the ion energy flux per unit area proportional to temperature, ENIPAR(,1) specifies the energy flux density per temperature in W.m -2 .J -1 (the temperature here in J)
    |	14 : leakage option for ion energy, ENIPAR(,1) specifies the leakage factor, alpha in Gamma`_loss` = alpha C`_s`TT`_i`
    |	15 : from b2stbc\_spb
    |	16 : Feedback boundary condition with constant temperature, ENIPAR(,1) specifies the power flux in W across the flux surface with index 'b2stbc\_type16\_ref' (default=-1), ENIPAR(,2) should be something like 0.1 and specifies the strength of the feedback. Also see type [17] below. Available if bceni\_16\_style=0 (default). If bceni\_16\_style=1, integrated ion heat flux with constant ion temperature, summed over all core boundaries with BCENI=16.
    |		ENIPAR(,1) specifies the power flux in W
    |	17 : Feedback boundary condition with constant shared temperature for both electrons and ions, see BCENE=17 above for description.
    |	18 : Fractional drop condition. Not yet working.
    |	19 : same as [9] but to be used when simultaneously setting BCCON=1 on the same boundary.
    |	20 : Feedback boundary condition with constant temperature, as per type [16] but with 'type20\_' switches and a different feedback scheme.
    |	21 : from b2stbc\_spb
    |	22 : Radial leakage condition for the ion temperature. ENIPAR(,1) specifies the leakage velocity in units of the collective ion thermal velocity. A temperature gradient such that the diffusive flux is set to match this leakage is imposed.
    |	23 : Prescribe the poloidally averaged value of the ion temperature and introduce a poloidal variation as close as possible to neoclassical solution. It is recommended to use this boundary condition together with corresponding condition on ion density (BCCON=21,22,23). The average is taken over all core boundaries with BCENI=23. ENIPAR(,1) specifies the temperature in eV
    |	24 : Feedback boundary condition with prescribed total ion flux, constant poloidally averaged ion temperature	and a poloidal variation as close as possible to neoclassical solution. It is recommended to use this boundary condition together with corresponding condition on ion density (BCCON=21,22,23). The flux is	summed over all core boundaries with BCENI=24. ENIPAR(,1) specifies the energy flux in W
    |	25 : Constant temperature feedback scaled by temperature on the ring bc\_type21\_ref away. ENIPAR(,1) specifies the desired ion temperature in eV . ENIPAR(,2) is the strength of the feedback
    |	26 : Prescribe the poloidally averaged value of the ion temperature and introduce a poloidal variation in a simplified manner. This boundary condition is suitable for any plasma composition (i.e. when BCENI=23 fails). It is recommended to use this boundary condition together with corresponding condition on ion density (BCCON = 25,26,27). The average is taken over all core boundaries with BCENI=26. ENIPAR(,1) specifies the temperature in eV
    |	27 : Feedback boundary condition with prescribed total ion heat flux, constant poloidally averaged ion temperature and a poloidal variation in a simplified manner. This boundary condition is suitable for any plasma composition (i.e. when BCENI=24 fails). It is recommended to use this boundary condition together with corresponding condition on ion density (BCCON = 25,26,27). The flux is summed over all core boundaries with BCENI=27. ENIPAR(,1) specifies the energy flux in W

    

.. index:: BCPOT

``BCPOT``    type: ``integer array, length NBC``
    Specifying the type of electric potential or current boundary condition for each segment; makes use of POTPAR to specify additional information, as indicated

    |	 0 : default, no boundary condition is applied
    |	 1 : prescribe the value of the potential, POTPAR(,1) specifies the potential in V
    |	 2 : prescribe the gradient of the potential, POTPAR(,1) specifies the potential gradient in V.m^-1`
    |	 3 : sheath conditions, 
    |		POTPAR(,2) used for biasing [see code for details]
    |	 4 : prescribe the value of the potential weakly a mixed boundary condition, POTPAR(,1) specifies the potential in V and POTPAR(,2) specifies the 'strength' of the boundary condition
    |	 5 : prescribe the current flux density per unit area, POTPAR(,1) specifies the electric current flux density in A.m^-2`
    |	 6 : prescribe the total current flux density for a constant potential [not yet available]
    |	 7 : prescribe the potential as a function of other plasma parameters [not yet available]
    |	 8 : prescribe the total electric current with constant flux density, POTPAR(,1) specifies the electric current in A
    |	 9 : prescribe the decay length for the potential, POTPAR(,1) specifies the decay length in m
    |	10 : feedback option for core [not yet tested!!!!!!!!!] (based on using cbsch(0,coreregno))
    |	11 : sheath conditions, electron energy transmission from b2stbc\_spb, POTPAR(,2) specifies the bias potential in V
    |	12 : Imposes the currents due to drifts for the South core boundary. Must be used in conjunction with istyle\_cur\_contr\_on\_S\_and\_N.eq.2
    |	13 : Imposes the currents due to drifts for the South private flux and North boundaries. Must be used in conjunction with istyle\_cur\_contr\_on\_S\_and\_N.eq.2
    |	16 : Constant electric potential feedback on imposed total current. The current prescribed is given by the sum of the POTPAR(IB,1) (in A) over all the BCPOT=16 boundaries. 
    |		Still experimental, will not work for drift cases.
    |	21 : constant potential feedback scaled by potential on the ring 'bc\_type21\_ref' away.
    |		POTPAR(,,1) specifies the desired potential in V.
    |		POTPAR(,,2) is the strength of the feedback

    

.. index:: GAMMAI

``GAMMAI``    type: ``real*8``    default: ``5/3``
    Ratio of specific heats (adiabatic coefficient).
    

.. index:: GAMMAE

``GAMMAE``    type: ``real*8``    default: ``0.5``
    Secondary electron emission coefficient.
    

.. index:: LBNDUSR

``LBNDUSR``    type: ``logical``    default: ``.false.``
    If .true. will also call Bas' boundary condition routine after the end of the physics boundary condition routine (governed by the data from b2ah.dat and b2mn.dat).
    

.. index:: LFEEDBACK

``LFEEDBACK``    type: ``logical``    default: ``.false.``
    Indicates whether a feedback scheme is used. Obsolete. Superceded by 'b2stbc\_feedback'.
    

.. index:: NNISO

``NNISO``    type: ``integer``    default: ``0``
    Number of dead (or isolated) regions.
    

.. index:: NIISO

``NIISO``    type: ``real*8 array of size (0:NS-1)``
    Density of species (is) in (m-3) to impose in isolated regions.
    

.. index:: TEISO

``TEISO``    type: ``real*8``    default: ``1.0``
    Electron temperature (in eV) to impose in isolated regions.
    

.. index:: TIISO

``TIISO``    type: ``real*8``    default: ``1.0``
    Ion temperature (in eV) to impose in isolated regions.
    

.. index:: PHIISO

``PHIISO``    type: ``real*8``    default: ``0.0``
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

``BOUNDARY_TIME_MOD``    type: ``real*8``    default: ``0.0``
    When the B2 run simulation time, in seconds, modulo(BOUNDARY\_TIME\_MOD), exceeds BOUNDARY\_TIME\_SWITCH, reads the new namelist from BOUNDARY\_FILENAME. Also switches to the new namelist as the ELM count (here time/BOUNDARY\_TIME\_MOD) changes.
    Only active if BOUNDARY\_TIME\_MOD is greater than 0.
    

.. index:: BOUNDARY_TIME_SWITCH

``BOUNDARY_TIME_SWITCH``    type: ``real*8``    default: ``0.0``
    Time (in seconds) within an ELM cycle after which a new /BOUNDARY/ namelist is read.
    

.. index:: LCBS

``LCBS``    type: ``integer array of size (NBC)``
    Indices of the core boundary segments in B2 for passing to EIRENE. Defaults to the list of 'S' boundaries in regions 1 and 5.
    

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
.. index:: SAVED_CBSHE_CORE

``SAVED_CBSHE_CORE``    type: ``real*8``    default: ``0.0``
    Last value used for the core electron energy radial flux feedback.
    

.. index:: SAVED_CBSHI_CORE

``SAVED_CBSHI_CORE``    type: ``real*8``    default: ``0.0``
    Last value used for the core ion energy radial flux feedback.
    

.. index:: SAVED_CBSNA_CORE

``SAVED_CBSNA_CORE``    type: ``real*8``    default: ``0.0``
    Last value used for the core particle radial flux feedback. Corresponds to 'isfeedback' B2 species.
    

.. index:: SAVED_CBSCH_CORE

``SAVED_CBSCH_CORE``    type: ``real*8``    default: ``0.0``
    Last value used for the core radial electric current feedback.
    

.. index:: SAVED_CBSNA_PFR1

``SAVED_CBSNA_PFR1``    type: ``real*8``    default: ``0.0``
    Last value used for the radial inner PFR boundary flux feedback. Corresponds to 'isfeedback' B2 species.
    

.. index:: SAVED_CBSNA_PFR2

``SAVED_CBSNA_PFR2``    type: ``real*8``    default: ``0.0``
    Last value used for the radial outer PFR boundary flux feedback. Corresponds to 'isfeedback' B2 species.
    

.. index:: SAVED_CBSNA_SOL

``SAVED_CBSNA_SOL``    type: ``real*8``    default: ``0.0``
    Last value used for the radial particle flux feedback in the SOL. Corresponds to 'isfeedback' B2 species.
    

.. index:: 
   single: b2.feedback_save.parameters; SAVED_CBSHE_CORE
   single: b2.feedback_save.parameters; SAVED_CBSHI_CORE
   single: b2.feedback_save.parameters; SAVED_CBSNA_CORE
   single: b2.feedback_save.parameters; SAVED_CBSCH_CORE
   single: b2.feedback_save.parameters; SAVED_CBSNA_PFR1
   single: b2.feedback_save.parameters; SAVED_CBSNA_PFR2
   single: b2.feedback_save.parameters; SAVED_CBSNA_SOL

.. index:: b2.feedback_control.parameters

b2.feedback_control.parameters
==============================
.. index:: VACUUM_COMMUNICATION

``VACUUM_COMMUNICATION``    type: ``Integer``    default: ``0``
    If > 0, allows for a
    communication of particle fluxes across vacuum regions. This option only applies to neutrals. The density boundary condition is based on the difference between the average pressure and the local pressure.
    

.. index:: VACUUM_COMMUNICATION_NREG

``VACUUM_COMMUNICATION_NREG``    type: ``Integer array of size (NVAC)``    default: ``0``
    Number of communicating vacuum regions.
    

.. index:: VACUUM_COMMUNICATION_METHOD

``VACUUM_COMMUNICATION_METHOD``    type: ``Integer array of size (NVAC)``    default: ``0``
    Option for resorbing the pressure difference.

    |	1: Try to set a flux. Corr = (beta\*ave\_pressure - pressure)/temp \* alpha
    |	2: Try to set a density based on pressure equality.

    Corr = alpha \* beta \* pressure / Ti
    

.. index:: VACUUM_COMMUNICATION_IY

``VACUUM_COMMUNICATION_IY``    type: ``Integer array of size (NVACREG,NVAC)``    default: ``-2``
    Radial index of the ring on which the neutral pressure is computed for region IREG.
    

.. index:: VACUUM_COMMUNICATION_IX1

``VACUUM_COMMUNICATION_IX1``    type: ``Integer array of size (NVACREG,NVAC)``    default: ``-2``
    Poloidal lower bound of the range over which the neutral pressure is computed for region IREG.
    

.. index:: VACUUM_COMMUNICATION_IX2

``VACUUM_COMMUNICATION_IX2``    type: ``Integer array of size (NVACREG,NVAC)``    default: ``-2``
    Poloidal upper bound of the range over which the neutral pressure is computed for region IREG.
    

.. index:: VACUUM_COMMUNICATION_ALPHA

``VACUUM_COMMUNICATION_ALPHA``    type: ``Real*8 array of size (0:NSPECIES-1,NVAC)``    default: ``0.0``
    Parameter for setting the pressure correction. See above.
    

.. index:: VACUUM_COMMINICATION_BETA

``VACUUM_COMMINICATION_BETA``    type: ``Real*8 array of size (0:NSPECIES-1,NVAC)``    default: ``1.0``
    Parameter for setting the pressure correction. See above.
    

.. index:: NA_FEEDBACK_TARGET

``NA_FEEDBACK_TARGET``    type: ``Real*8 array of size (0:NSPECIES-1)``    default: ``0.0``
    Sets the target density of species (ISPECIES) for the feedback scheme.
    

.. index:: NA_FEEDBACK_TIME

``NA_FEEDBACK_TIME``    type: ``Real*8 array of size (0:NSPECIES-1)``    default: ``0.0``
    Sets the time of reference (in s) for the feedback of species (ISPECIES).
    

.. index:: NA_FEEDBACK_CHOICE

``NA_FEEDBACK_CHOICE``    type: ``Integer array of size (0:NSPECIES-1)``    default: ``0``
    Choice of quantity on which the feedback is computed:

    |	0: no action
    |	1: local species density (averaged over the rectangle of cells[IX1:IX2,IY1:IY2]). Summed over all charge states of that species.
    |	2: local electron density (averaged over the rectangle of cells[IX1:IX2,IY1:IY2]).
    |	3: outer midplane separatrix electron density.
    |	4: total particle content for that species.
    |	5: total ion content for that species (not including neutrals).
    |	6: neutral particle flux through the core boundary.
    |	7: relative average concentration of this species at the separatrix.

    

.. index:: NA_FEEDBACK_OPTION

``NA_FEEDBACK_OPTION``    type: ``Integer array of size (0:NSPECIES-1)``    default: ``0``
    Option for computing the new fedback quantity.

    |	0: no action
    |	1: rescale slowed by na\_feedback\_alpha
    |	2: pure rescale
    |	3: rescaling slowed by tanh\_log
    |	4: rescale done according to SOLPS4 formula 
    |		The target waveform for the particle content is 
    |		 N = C + V\*(time-T) 
    |	   and the current puffing rate S is adjusted 
    |	   S --> max(0, min(X,S + D)), where D = F\*((N - <N>)/dt + (<N>\_prev - <N>)/dt\_prev)
    |	5: rescale done according to SOLPS4 formula: N = C\*exp((time-T)\*V)
    |	6: rescale slowed by na\_feedback\_alpha (SOLPS4 style)

    

.. index:: NA_FEEDBACK_ACTUATOR

``NA_FEEDBACK_ACTUATOR``    type: ``Integer array of size (0:NSPECIES-1)``    default: ``0``
    Choice for the actuator used for the feedback.
    0: no action
    1: gas puff via boundary condition
    2: rescale na
    3: core boundary flux condition
    

.. index:: NA_FEEDBACK_ALPHA

``NA_FEEDBACK_ALPHA``    type: ``Real*8 array of size (0:NSPECIES-1)``    default: ``0.001``
    Factor by which the rescaling is slowed. Rescaling factor is :
    Option 1: (1 + alpha\*target/current) / (1 + alpha)
    Option 3: 2\*\*(tanh(log(x)/beta)\*log(alpha)/log(2))
    Options 4 and 5: Corresponds to parameter F
    

.. index:: NA_FEEDBACK_BETA

``NA_FEEDBACK_BETA``    type: ``Real*8 array of size (0:NSPECIES-1)``    default: ``1.0``
    Factor by which the rescaling is slowed. See above. Options 4 and 5: Corresponds to parameter V (ffb\_rtvn)
    

.. index:: NA_FEEDBACK_CONST

``NA_FEEDBACK_CONST``    type: ``Real*8 array of size (0:NSPECIES-1)``    default: ``0.0``
    Options 4 and 5: Corresponds to parameter C. If negative, C is

    |	computed as the initial total particle content of the sequence.

    

.. index:: NA_FEEDBACK_IX1

``NA_FEEDBACK_IX1``    type: ``Integer array of size (0:NSPECIES-1)``    default: ``-2``
    Lower poloidal bound for the region of which the density is being averaged.
    

.. index:: NA_FEEDBACK_IX2

``NA_FEEDBACK_IX2``    type: ``Integer array of size (0:NSPECIES-1)``    default: ``-2``
    Upper poloidal bound for the region of which the density is being averaged.
    

.. index:: NA_FEEDBACK_IY1

``NA_FEEDBACK_IY1``    type: ``Integer array of size (0:NSPECIES-1)``    default: ``-2``
    Lower radial bound for the region of which the density is being averaged.
    

.. index:: NA_FEEDBACK_IY2

``NA_FEEDBACK_IY2``    type: ``Integer array of size (0:NSPECIES-1)``    default: ``-2``
    Upper poloidal bound for the region of which the density is being averaged.
    

.. index:: NA_FEEDBACK_IB

``NA_FEEDBACK_IB``    type: ``Integer array of size (0:NSPECIES-1)``    default: ``-1``
    Index of boundary condition through which the feedback is being applied.
    

.. index:: NA_FEEDBACK_PUFF_MIN

``NA_FEEDBACK_PUFF_MIN``    type: ``Real*8 array of size (0:NSPECIES-1)``    default: ``0.0``
    Minimum gas puff being applied.
    

.. index:: NA_FEEDBACK_PUFF_MAX

``NA_FEEDBACK_PUFF_MAX``    type: ``Real*8 array of size (0:NSPECIES-1)``    default: ``0.0``
    Maximum gas puff being applied.
    

.. index:: NA_FEEDBACK_OVERSHOOT

``NA_FEEDBACK_OVERSHOOT``    type: ``Real*8 array of size (0:NSPECIES-1)``    default: ``0.0``
    If the density is larger than target\*overshoot, the gas puff is turned off.
    

.. index:: 
   single: b2.feedback_control.parameters; VACUUM_COMMUNICATION
   single: b2.feedback_control.parameters; VACUUM_COMMUNICATION_NREG
   single: b2.feedback_control.parameters; VACUUM_COMMUNICATION_METHOD
   single: b2.feedback_control.parameters; VACUUM_COMMUNICATION_IY
   single: b2.feedback_control.parameters; VACUUM_COMMUNICATION_IX1
   single: b2.feedback_control.parameters; VACUUM_COMMUNICATION_IX2
   single: b2.feedback_control.parameters; VACUUM_COMMUNICATION_ALPHA
   single: b2.feedback_control.parameters; VACUUM_COMMINICATION_BETA
   single: b2.feedback_control.parameters; NA_FEEDBACK_TARGET
   single: b2.feedback_control.parameters; NA_FEEDBACK_TIME
   single: b2.feedback_control.parameters; NA_FEEDBACK_CHOICE
   single: b2.feedback_control.parameters; NA_FEEDBACK_OPTION
   single: b2.feedback_control.parameters; NA_FEEDBACK_ACTUATOR
   single: b2.feedback_control.parameters; NA_FEEDBACK_ALPHA
   single: b2.feedback_control.parameters; NA_FEEDBACK_BETA
   single: b2.feedback_control.parameters; NA_FEEDBACK_CONST
   single: b2.feedback_control.parameters; NA_FEEDBACK_IX1
   single: b2.feedback_control.parameters; NA_FEEDBACK_IX2
   single: b2.feedback_control.parameters; NA_FEEDBACK_IY1
   single: b2.feedback_control.parameters; NA_FEEDBACK_IY2
   single: b2.feedback_control.parameters; NA_FEEDBACK_IB
   single: b2.feedback_control.parameters; NA_FEEDBACK_PUFF_MIN
   single: b2.feedback_control.parameters; NA_FEEDBACK_PUFF_MAX
   single: b2.feedback_control.parameters; NA_FEEDBACK_OVERSHOOT

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

``SDATA``    type: ``real*8 data of size (2,NY+2,NKIND_SOURCE,0:NS)``    default: ``0.0``
    For (i,ir,ik,is) in (1:2,1:NY+2,1:NKIND\_SOURCE,0:NS),
    SDATA(1,ir,:,:) contains the radial location of the profile point (ir).
    SDATA(2,ir,:,:) contains the source profile value at point (ir).
    KIND\_SOURCE=1 means particle source of species (is) (in particles/m3)
    KIND\_SOURCE=2 means parallel momentum source for species (is) (in kg.m/s/m3)
    KIND\_SOURCE=3 means electron heat source (in Watts/m3)
    KIND\_SOURCE=4 means ion heat source (in Watts/m3)
    KIND\_SOURCE=5 means electric charge source (in Coulombs/m3)
    KIND\_SOURCE=6 means non-ambipolar electron particle source (in e/m3)
    

.. index:: NXDATA

``NXDATA``    type: ``integer array of size (NKIND_DATA,NKIND_SOURCE,0:NS)``
    Number of points over which the axial profile of (kind\_data,kind\_source,is) is defined. Should not exceed NX+2. Defaults to 0.
    If KIND\_DATA=1, the data is expressed as a profile in physical distance, here connection length, rescaled from 0.0 to 1.0.
    For closed field lines, the reference location for the zero of distance is set by use of the 'set\_transport\_i[xy]ref' switches.
    If KIND\_DATA=2, the data is expressed as a profile in (ix) cell index, again normalized from 0.0 to 1.0 to match the [0:nx-1] interval.
    

.. index:: XDATA

``XDATA``    type: ``real*8 data of size (2,NY+2,NKIND_SOURCE,0:NS)``    default: ``1.0``
    Multiplier to the poloidal source profile in the axial direction. Same convention for KIND\_SOURCE as above.
    

.. index:: DIVHEAT

``DIVHEAT``    type: ``real*8``    default: ``0.0``
    Additional divertor ion heat source (in Watts/m3)
    

.. index:: SOURCES_FILENAME

``SOURCES_FILENAME``    type: ``character*256``    default: ``b2.sources.profile``
    Name of the next file to use for reading a new /PROFILE/ namelist. Quantities not present in the new file will be inherited from the old one.
    

.. index:: SOURCES_TIME_MOD

``SOURCES_TIME_MOD``    type: ``real*8``    default: ``0.0``
    When the B2 run simulation time, in seconds, modulo(SOURCES\_TIME\_MOD),exceeds SOURCES\_TIME\_SWITCH, reads the new namelist from SOURCES\_FILENAME. Also switches to the new namelist if the ELM count (here time/SOURCES\_TIME\_MOD) changes. Only active if SOURCES\_TIME\_MOD is greater than 0.
    

.. index:: SOURCES_TIME_SWITCH

``SOURCES_TIME_SWITCH``    type: ``real*8``    default: ``0.0``
    Time (in seconds) within an ELM cycle after which a new /PROFILE/ namelist is read.
    

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

``TDATA``    type: ``real*8 data of size (3,NY+2,NKIND_COEFF,0:NS)``    default: ``0.0``
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
    

.. index:: TRANSPORT_FILENAME

``TRANSPORT_FILENAME``    type: ``character*256``    default: ``b2.transport.inputfile``
    Name of the next file to use for reading a new /TRANSPORT/ namelist.
    

.. index:: TRANSPORT_TIME_MOD

``TRANSPORT_TIME_MOD``    type: ``real*8``    default: ``0.0``
    When the B2 run simulation time, in seconds, modulo(TRANSPORT\_TIME\_MOD),exceeds TRANSPORT\_TIME\_SWITCH, reads the new namelist from TRANSPORT\_FILENAME. Also switches to the new namelist if the ELM count (here time/TRANSPORT\_TIME\_MOD) changes. Only active if TRANSPORT\_TIME\_MOD is greater than 0.
    

.. index:: TRANSPORT_TIME_SWITCH

``TRANSPORT_TIME_SWITCH``    type: ``real*8``    default: ``0.0``
    Time (in seconds) within an ELM cycle after which a new /TRANSPORT/ namelist is read.
    

.. index:: REGION_FLAGS

``REGION_FLAGS``    type: ``logical array of size (NREG,NKIND_COEFF)``    default: ``.true.``
    If region\_flags(ireg,ikind) is .true. (default), then the transport parameters profiles for region (ireg) and kind (ikind) are used.
    

.. index:: NO_PFLUX

``NO_PFLUX``    type: ``logical``    default: ``.false.``
    If .true., transport coefficients profiles are not implemented in the private flux regions.
    

.. index:: POLOIDAL_SCALING

``POLOIDAL_SCALING``    type: ``logical array of size (10)``    default: ``.false.``
    If .true., then the transport coefficients profiles from the current b2.transport.inputfile are increased by a factor of 1.0+Gaussian where Gaussian is a Gaussian profile in the poloidal direction of amplitude SCALING\_STRENGTH extending from SCALING\_IX\_BEGIN to SCALING\_IX\_END inclusively. The profile has a decay length of SCALING\_WIDTH (in units of the number of poloidal cells).
    

.. index:: SCALING_STRENGTH

``SCALING_STRENGTH``    type: ``real*8 array of size 10``    default: ``0``
    See above.
    

.. index:: SCALING_WIDTH

``SCALING_WIDTH``    type: ``real*8 array of size 10``    default: ``1/3 interval``
    See above. Defaults to about 1/3 of the interval over which the scaling is to be done.
    

.. index:: SCALING_IX_BEGIN

``SCALING_IX_BEGIN``    type: ``integer array of size 10``    default: ``-2``
    See above.
    

.. index:: SCALING_IX_END

``SCALING_IX_END``    type: ``integer array of size 10``    default: ``-2``
    See above.
    

.. index:: ELM_TIME_BEGIN

``ELM_TIME_BEGIN``    type: ``real*8``    default: ``0.0``
    Time (in seconds) modulo ELM\_TIME\_PERIOD at which the ELM phase begins and the ELM data must be used.
    

.. index:: ELM_TIME_END

``ELM_TIME_END``    type: ``real*8``    default: ``0.0``
    Time (in seconds) modulo ELM\_TIME\_PERIOD at which the ELM phase ends and the ELM data is no longer used.
    

.. index:: ELM_TIME_PERIOD

``ELM_TIME_PERIOD``    type: ``real*8``    default: ``0.0``
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
   single: b2.transport.inputfile; TRANSPORT_FILENAME
   single: b2.transport.inputfile; TRANSPORT_TIME_MOD
   single: b2.transport.inputfile; TRANSPORT_TIME_SWITCH
   single: b2.transport.inputfile; REGION_FLAGS
   single: b2.transport.inputfile; NO_PFLUX
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

``SAVED_VOLREC``    type: ``real*8 array of size (NSTRAT)``    default: ``0.0``
    Contains the last value of the strength of volume recombination sources from stratum (istra).
    

.. index:: 
   single: b2.neutrals_save.parameters; SAVED_VOLREC

.. index:: b2.numerics.parameters

b2.numerics.parameters
======================
.. index:: DTCO

``DTCO``    type: ``real*8 array of size (0:NS-1,0:NREG)``    default: ``1.0``
    Multiplier to the time used in solving the continuity equation of species (is) in region (ireg).
    

.. index:: DTMO

``DTMO``    type: ``real*8 array of size (0:NS-1,0:NREG)``    default: ``1.0``
    Multiplier to the time used in solving the parallel momentum equation of species (is) in region (ireg).
    

.. index:: DTEE

``DTEE``    type: ``real*8 array of size (0:NREG)``    default: ``1.0``
    Multiplier to the time used in solving the electron heat equation in region (ireg).
    

.. index:: DTEI

``DTEI``    type: ``real*8 array of size (0:NREG)``    default: ``1.0``
    Multiplier to the time used in solving the ion heat equation in region (ireg).
    

.. index:: SOLVECO

``SOLVECO``    type: ``logical array of size (0:NS-1,0:NREG)``    default: ``.true.``
    Indicates whether the continuity equation for species (is) is to be solved in region (ireg). Subservient to 'no\_solve' switch.
    

.. index:: SOLVEMO

``SOLVEMO``    type: ``logical array of size (0:NS-1,0:NREG)``    default: ``.true.``
    Indicates whether the parallel momentum equation for species (is) is to be solved in region (ireg). Subservient to 'no\_solve' switch.
    

.. index:: SOLVEPO

``SOLVEPO``    type: ``logical array of size (0:NREG)``    default: ``.true.``
    Indicates whether the potential energy equation is to be solved in region (ireg). Subservient to 'no\_solve' switch.
    

.. index:: SOLVEEE

``SOLVEEE``    type: ``logical array of size (0:NREG)``    default: ``.true.``
    Indicates whether the electron energy equation is to be solved in region (ireg). Subservient to 'no\_solve' switch.
    

.. index:: SOLVEEI

``SOLVEEI``    type: ``logical array of size (0:NREG)``    default: ``.true.``
    Indicates whether the ion energy equation is to be solved in region (ireg). Subservient to 'no\_solve' switch.
    

.. index:: TIME_FACTOR_REQUIRED

``TIME_FACTOR_REQUIRED``    type: ``real*8``    default: ``0.1``
    Minimum time scale of evolution allowed for all equations. Only active is 'b2srsm\_enable' is set to 1.
    

.. index:: CORE_DT_SUPPRESSION

``CORE_DT_SUPPRESSION``    type: ``real*8``    default: ``1.0``
    De-multiplier to the timestep in the core. Only active if less than 1. Should be larger than 0. Applies fully to the innermost core ring of cells (IY .eq. -1). See CORE\_DT\_FACTOR for further use.
    

.. index:: CORE_DT_FACTOR

``CORE_DT_FACTOR``    type: ``real*8``    default: ``1.0``
    Multiplier to the timestep in the core. Only active is less than 1. Should be larger than 0. Multiplies each successive core ring of cells (increasing IY) by CORE\_DT\_FACTOR, until the local time step multiplier is equal to 1.
    

.. index:: NUMERICS_FILENAME

``NUMERICS_FILENAME``    type: ``character*256``    default: ``b2.numerics.namelist``
    Name of the next file to use for reading a new /NUMERICS/ namelist.
    

.. index:: NUMERICS_TIME_MOD

``NUMERICS_TIME_MOD``    type: ``real*8``    default: ``0.0``
    When the B2 run simulation time, in seconds, modulo(NUMERICS\_TIME\_MOD), exceeds NUMERICS\_TIME\_SWITCH, reads the new namelist from NUMERICS\_FILENAME. Also switches to the new namelist as the ELM count (here time/NUMERICS\_TIME\_MOD) changes. Only active if NUMERICS\_TIME\_MOD is greater than 0.
    

.. index:: NUMERICS_TIME_SWITCH

``NUMERICS_TIME_SWITCH``    type: ``real*8``    default: ``0.0``
    Time (in seconds) within an ELM cycle after which a new /NUMERICS/ namelist is read.
    

.. index:: WRITE_NML_NUM

``WRITE_NML_NUM``    type: ``logical``    default: ``.true.``
    If .true. (default), writes the content of the namelist to stdout after it has been read.
    

.. index:: 
   single: b2.numerics.parameters; DTCO
   single: b2.numerics.parameters; DTMO
   single: b2.numerics.parameters; DTEE
   single: b2.numerics.parameters; DTEI
   single: b2.numerics.parameters; SOLVECO
   single: b2.numerics.parameters; SOLVEMO
   single: b2.numerics.parameters; SOLVEPO
   single: b2.numerics.parameters; SOLVEEE
   single: b2.numerics.parameters; SOLVEEI
   single: b2.numerics.parameters; TIME_FACTOR_REQUIRED
   single: b2.numerics.parameters; CORE_DT_SUPPRESSION
   single: b2.numerics.parameters; CORE_DT_FACTOR
   single: b2.numerics.parameters; NUMERICS_FILENAME
   single: b2.numerics.parameters; NUMERICS_TIME_MOD
   single: b2.numerics.parameters; NUMERICS_TIME_SWITCH
   single: b2.numerics.parameters; WRITE_NML_NUM

.. index:: b2.transport_models_save.parameters

b2.transport_models_save.parameters
===================================
.. index:: ETA_HCE_MULT

``ETA_HCE_MULT``    type: ``real*8 array of size (-1:NY)``    default: ``1.0``
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

``PARM_DNA``    type: ``real*8 array of size (0:NS-1)``
    Parameter for the density-driven particle diffusion coefficient for species (is).
    

.. index:: PARM_DPA

``PARM_DPA``    type: ``real*8 array of size (0:NS-1)``
    Parameter for the pressure-driven particle diffusion coefficient for species (is).
    

.. index:: PARM_VLA

``PARM_VLA``    type: ``real*8 array of size (0:NS-1)``
    Parameter for the anomalous radial pinch velocity for species (is).
    

.. index:: PARM_VSA

``PARM_VSA``    type: ``real*8 array of size (0:NS-1)``
    Parameter for the viscosity for species (is).
    

.. index:: PARM_HCI

``PARM_HCI``    type: ``real*8 array of size (0:NS-1)``
    Parameter for the heat diffusivity coefficient for species (is).
    

.. index:: PARM_HCE

``PARM_HCE``    type: ``real*8``
    Parameter for the electron heat diffusivity coefficient.
    

.. index:: PARM_SIG

``PARM_SIG``    type: ``real*8``
    Parameter for the anomalous radial field-driven current conductivity.
    

.. index:: PARM_ALF

``PARM_ALF``    type: ``real*8``
    Parameter for the anomalous radial temperature-driven current conductivity.
    

.. index:: TRANSPORT_FILENAME

``TRANSPORT_FILENAME``    type: ``character*256``    default: ``b2.transport.parameters``
    Name of the next file to use for reading a new /TRANSPORT/ namelist.
    

.. index:: TRANSPORT_TIME_MOD

``TRANSPORT_TIME_MOD``    type: ``real*8``    default: ``0.0``
    When the B2 run simulation time, in seconds, modulo(TRANSPORT\_TIME\_MOD), exceeds TRANSPORT\_TIME\_SWITCH, reads the new namelist from TRANSPORT\_FILENAME. Also switches to the new namelist if the ELM count (here time/TRANSPORT\_TIME\_MOD) changes.
    Only active if TRANSPORT\_TIME\_MOD is greater than 0.
    

.. index:: TRANSPORT_TIME_SWITCH

``TRANSPORT_TIME_SWITCH``    type: ``real*8``    default: ``0.0``
    Time (in seconds) within an ELM cycle after which a new /TRANSPORT/ namelist is read.
    

.. index:: CFLM*

.. index:: CFLME, CFLMI, CFLMV
.. c

``CFLM*``

  - ``CFLME``  -     type: ``real*8``    default: ``Default inherited from b2mn.dat``
    Multiplier to the electron heat flux limit.
    

  - ``CFLMI``  -     type: ``real*8``    default: ``Default inherited from b2mn.dat``
    Multiplier to the ion heat flux limit.
    

  - ``CFLMV``  -     type: ``real*8``    default: ``Default inherited from b2mn.dat``
    Multiplier to the viscous heat flux limit.
    


    For all flux limit multipliers, setting them to zero turns off the corresponding flux limiter.
    
.. index::
   single: CFLM*; CFLME
   single: CFLM*; CFLMI
   single: CFLM*; CFLMV


.. index:: WRITE_NML_TRANSP

``WRITE_NML_TRANSP``    type: ``logical``    default: ``.true.``
    If .true. (default), writes the content of the namelist to stdout after it has been read.
    

.. index:: *_CNV

.. index:: VOUT_CNV, PW0_CNV, PW1_CNV, PW2_CNV
.. c

``*_CNV``

  - ``VOUT_CNV``  -     type: ``real*8 array of size (0:NS-1)``    default: ``0.0``
    Value of the "blob" convection velocity for species (is) at the outer grid edge (in m/s).
    

  - ``PW0_CNV``  -     type: ``real*8 array of size (0:NS-1)``    default: ``1.0``
    Exponent in radial profile of the "blob" velocity for species (is).
    

  - ``PW1_CNV``  -     type: ``real*8 array of size (0:NS-1)``    default: ``5.0``
    First exponent in poloidal profile of the "blob" velocity for species (is).
    

  - ``PW2_CNV``  -     type: ``real*8 array of size (0:NS-1)``    default: ``2.0``
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
   single: b2.transport.parameters; CFLM*
   single: b2.transport.parameters; WRITE_NML_TRANSP
   single: b2.transport.parameters; *_CNV

.. index:: b2.user.parameters

b2.user.parameters
==================
.. index:: LHETRGTS

``LHETRGTS``    type: ``integer array of size (NLIM)``    default: ``-2 for the firt element, -3 for the second element and 0 otherwise``
    List of surface indices (EIRENE notation) which are used for calculation of helium enrichment.
    

.. index:: LPFRB_I

``LPFRB_I``    type: ``integer``    default: ``-2``
    B2 x-cell indices corresponding to the bottom of the bypass between the inner and outer divertor (counted from the bottom, if non-positive) (inner side).
    

.. index:: LPFRB_O

``LPFRB_O``    type: ``integer``    default: ``-2``
    B2 x-cell indices corresponding to the bottom of the bypass between the inner and outer divertor (counted from the bottom, if non-positive) (outer side).
    

.. index:: LPFRT_I

``LPFRT_I``    type: ``integer``    default: ``-2``
    B2 x-cell indices corresponding to the top of the bypass between the inner and outer divertor (counted from the x-point, if non-positive) (inner side).
    

.. index:: LPFRT_O

``LPFRT_O``    type: ``integer``    default: ``-2``
    B2 x-cell indices corresponding to the top of the bypass between the inner and outer divertor (counted from the x-point, if non-positive) (outer side).
    

.. index:: J_HE_AT

``J_HE_AT``    type: ``integer``
    Species index of the helium atoms in Eirene. The code attempts to find a match by default.
    

.. index:: J_NE_AT

``J_NE_AT``    type: ``integer``
    Species index of the neon atoms in Eirene. The code attempts to find a match by default.
    

.. index:: J_H_AT

``J_H_AT``    type: ``integer``
    Species index of the hydrogen atoms in Eirene. The code attempts to find a match by default.
    

.. index:: L_H_MOL

``L_H_MOL``    type: ``integer``
    Species index of the hydrogen molecules in Eirene. The code attempts to find a match by default.
    

.. index:: FUSION_POWER

``FUSION_POWER``    type: ``real*8``    default: ``0.0``
    Fusion power occuring in core (including neutrons, in Megawatts).
    

.. index:: SPMP_HE_TO_D

``SPMP_HE_TO_D``    type: ``real*8``    default: ``1.0``
    Ratio of He to DT pumping speeds (typically, 0.8).
    

.. index:: LPFRS_PMP

``LPFRS_PMP``    type: ``integer``    default: ``0``
    Location of the pump. 0 no pump at all (default), 1 - lower PFR, 2 - lower outer
    

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
    

.. index:: SPMP_NOM

``SPMP_NOM``    type: ``real*8``    default: ``0.0``
    Nominal pumping speed.
    

.. index:: USER_FILENAME

``USER_FILENAME``    type: ``character*80``    default: ``b2.user.parameters``
    Filename where /USER/ namelist is stored.
    

.. index:: 
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
   single: b2.user.parameters; SPMP_NOM
   single: b2.user.parameters; USER_FILENAME

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

``SPUTTER_YIELD``    type: ``real*8 array of size (-1:NX,-1:NY,0:NS-1,1:2)``    default: ``0.0``
    Contains the physical sputtering yield of species (is) at position (ix,iy) in element (:,:,:,1) and the chemical sputtering yield in element (:,:,:,2).
    

.. index:: SPUTTER_YIELD2

``SPUTTER_YIELD2``    type: ``real*8 array of size (-1:NX,-1:NY,0:NS-1,1:2)``    default: ``0.0``
    Contains the energy physical sputtering yield of species (is) at position (ix,iy) in element (:,:,:,1) and the energy chemical sputtering yield in element(:,:,:,2).
    

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

``RESCALE_SA``    type: ``real*8 array of size(0:NS-1)``    default: ``1.0``
    Scaling factors for rtsa: ionisation rates of species (is).
    

.. index:: RESCALE_RA

``RESCALE_RA``    type: ``real*8 array of size(0:NS-1)``    default: ``1.0``
    Scaling factors for rtra: recombination rates of species (is).
    

.. index:: RESCALE_QA

``RESCALE_QA``    type: ``real*8 array of size(0:NS-1)``    default: ``1.0``
    Scaling factors for rtqa: electron cooling rates of species (is).
    

.. index:: RESCALE_CX

``RESCALE_CX``    type: ``real*8 array of size(0:NS-1)``    default: ``1.0``
    Scaling factors for rtcx: charge exchange rates of species (is).
    

.. index:: RESCALE_RD

``RESCALE_RD``    type: ``real*8 array of size(0:NS-1)``    default: ``1.0``
    Scaling factors for rtrd: line radiation rates of species (is).
    

.. index:: RESCALE_BR

``RESCALE_BR``    type: ``real*8 array of size(0:NS-1)``    default: ``1.0``
    Scaling factors for rtbr: bremsstrahlung radiation rates of species (is).
    

.. index:: 
   single: b2.atomic_physics_rescale.parameters; RESCALE_SA
   single: b2.atomic_physics_rescale.parameters; RESCALE_RA
   single: b2.atomic_physics_rescale.parameters; RESCALE_QA
   single: b2.atomic_physics_rescale.parameters; RESCALE_CX
   single: b2.atomic_physics_rescale.parameters; RESCALE_RD
   single: b2.atomic_physics_rescale.parameters; RESCALE_BR


