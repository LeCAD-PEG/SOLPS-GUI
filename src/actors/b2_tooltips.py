
# -*- coding: utf-8 -*-

tooltips = {

'b2ai.dat' : {

      'dimens' : ('b2ai params', 'None', """
					the number of charge states
				""", 'None'),
   
      'label' : ('b2ai params', 'None', """a label""", 'None'),
   
      'specs' : ('b2ai params', 'None', """
					atomic charge, nuclear charge, atomic mass and atomic charge squared for each charge state, minimum atomic charge of the stage, maximum atomic charge of the stage, nuclear charge, and atomic mass; this data should match that given in b2ah.dat
				""", 'None'),
   
      'naini' : ('b2ai params', 'None', """
					initial densities for each of the charge states, in m<sup>-3</sup>
				""", 'None'),
   
      'ttini' : ('b2ai params', 'None', """
					initial ion and electron temperatures, in eV
				""", 'None'),
   
},

'b2ah.dat' : {

      'dimens' : ('b2ah params', '', """
					the number of charge states
				""", 'None'),
   
      'label' : ('b2ah params', '', """
					specifies, on the next line, a label for the run
				""", 'None'),
   
      'b2cmpa' : ('b2ah params', '', """
					specifies a block of basic parameters.
				""", 'None'),
   
      'b2cmpb' : ('b2ah params', '', """
					specifies a block of boundary conditions
				""", 'None'),
   
      'b2cmpt' : ('b2ah params', '', """
					specifies a block of transport coefficients
				""", 'None'),
   
      'specs' : ('b2ah params', '', """
					atomic charge, nuclear charge, atomic mass and atomic charge squared; this data should match that given in b2ai.dat. Starting with code version 01.001.024, an alternative means of describing the plasma species and filling out the b2cmpa block is provided, in order to allow for bundling of charge states, when running cases with high-Z species. The relevant description is then minimum atomic charge of the stage, maximum atomic charge of the stage, nuclear charge, and atomic mass; this data should match that given in b2ai.dat The code can accept indifferently both types of input and makes the appropriate self-consistency checks. It is not permitted to bundle neutral and ionized species together.
				""", ''),
   
      'cbregs' : ('b2ah params', '', """
					specifies the number of regions where boundary conditions will be specified the 'south' boundary is broken into three pieces with one quarter of the cells in the first region, half of the cells in the second, and the remaining quarter in the third region (Western target private flux, core, Eastern target private flux). This is geometry-dependent information the code will check against the mesh connectivity and return an error if the two do not match the 'north', 'west' and 'east' are not broken up, and correspond to the SOL boundary, inner (outer) target and outer (inner) target, respectively for lower (upper) single-null topologies. For double-null cases, the north boundary should be split into two sections.
				""", 'None'),
   
      'region' : ('b2ah params', '', """
					one block for each of the regions containing; the immediately following line being the region dentifier
				""", 'None'),
   
      'cbsna' : ('b2ah params', '', """
					boundary conditions for density (1 line per species)
				""", 'None'),
   
      'cbsmo' : ('b2ah params', '', """
					boundary conditions for parallel momentum (1 line per species)
				""", 'None'),
   
      'cbshi' : ('b2ah params', '', """
					ion/neutral (or "atomic") temperature/energy boundary condition (1 line per species)
				""", 'None'),
   
      'cbshe' : ('b2ah params', '', """
					electron temperature/heat flux boundary condition
				""", 'None'),
   
      'cbsch' : ('b2ah params', '', """
					boundary condition for the electric potential equation
				""", 'None'),
   
      'cbrec' : ('b2ah params', '', """
					recycling coefficients (1 line per species)
				""", 'None'),
   
      'cbmsa' : ('b2ah params', '', """
					[unused]
				""", 'None'),
   
      'cbmsb' : ('b2ah params', '', """
					[unused] (1 line per species)
				""", 'None'),
   
},

'b2ag.dat' : {

      'dimens' : ('b2ag params', 'None', """
					specifies the size of the grid first pair is NX &amp; NY of the grid you want to produce second pair is the size of the grid that was originally created each needs to be an integer multiple of the corresponding entry of the first pair. Note that for double-null cases, the interior guard cells corresponding to the top divertor boundaries should not be multiplied.
				""", 'None'),
   
      'param' : ('b2ag params', 'None', """
					at least 100 additional numbers, of which only the first is relevant, unless using an analytic formulation for the grid.
					A value of -1.0 asks to read the mesh data using the "simplified" Carre format.
					A value of -2.0 asks to read the mesh data using the Sonnet format.
				""", 'None'),
   
},

'b2mn.dat' : {

      'b2stbc_coreregno' : ('', 'integer', """
					coreregno is the boundary index of the core boundary in the input files b2ah.dat and b2mn.dat. For standard single-null and double-null cases, the default value of coreregno is 1. For a straight geometry or limiter case, the default value of coreregno is 0.
					coreregn2 is the boundary index of the second core boundary in case of a double-null geometry, and is not used otherwise.
				""", '1'),
   
      'b2stbc_coreregn2' : ('', 'integer', """
					coreregno is the boundary index of the core boundary in the input files b2ah.dat and b2mn.dat. For standard single-null and double-null cases, the default value of coreregno is 1. For a straight geometry or limiter case, the default value of coreregno is 0.
					coreregn2 is the boundary index of the second core boundary in case of a double-null geometry, and is not used otherwise.
				""", '4'),
   
      'b2stbc_pfrregno1' : ('', 'integer', """
					pfrregno1 is the boundary index of the first half of the private flux region boundary on which feedback is being applied (through b2stbc_ndes or b2stbc_private_flux_puff) in the input files b2ah.dat and b2mn.dat. pfrregno2 is the second half of the same private flux region. For a standard single null, the pair should be (0,2). For a standard double-null, the lower private flux region is labelled with the pair (0,5), and the upper private flux region with the pair (2,3). One can use only one private flux region by setting pfrregno1.eq.pfrregno2.
				""", '0'),
   
      'b2stbc_pfrregno2' : ('', 'integer', """
					pfrregno1 is the boundary index of the first half of the private flux region boundary on which feedback is being applied (through b2stbc_ndes or b2stbc_private_flux_puff) in the input files b2ah.dat and b2mn.dat. pfrregno2 is the second half of the same private flux region. For a standard single null, the pair should be (0,2). For a standard double-null, the lower private flux region is labelled with the pair (0,5), and the upper private flux region with the pair (2,3). One can use only one private flux region by setting pfrregno1.eq.pfrregno2.
				""", '2'),
   
      'b2agfs_xoffset' : ('', 'real', """
					xoffset and yoffset are offsets of the basis mesh in the x- and y-direction respectively. The mesh will be translated by (xoffset,yoffset) if any of the two is non-zero from its position given in the local_sonnet (See 'b2agfs_geometry' above) file.
					To be used in b2ag.dat.
				""", '0.0'),
   
      'b2agfs_yoffset' : ('', 'real', """
					xoffset and yoffset are offsets of the basis mesh in the x- and y-direction respectively. The mesh will be translated by (xoffset,yoffset) if any of the two is non-zero from its position given in the local_sonnet (See 'b2agfs_geometry' above) file.
					To be used in b2ag.dat.
				""", '0.0'),
   
      'b2agfs_xrescale' : ('', 'real', """
					Rescaling factors of the x- and y- coordinates of the basis mesh.
					To be used in b2ag.dat.
				""", '1.0'),
   
      'b2agfs_yrescale' : ('', 'real', """
					Rescaling factors of the x- and y- coordinates of the basis mesh.
					To be used in b2ag.dat.
				""", '1.0'),
   
      'b2agfs_leftcut' : ('', 'integer', """
					Parameters describing the position and extent of the first topological cut, i.e. corresponding to the first X-point. Needed only to force different values from the ones computed automatically by b2ag.
					leftcut is the poloidal index of cells directly to the RIGHT of the left branch of the cut.
					rightcut is the poloidal index of cells directly to the RIGHT of the right branch of the cut.
					bottomcut is the radial index of cells directly below the cut.
					topcut is the radial index of cells directly above the cut.
				""", 'See description (integer)'),
   
      'b2agfs_rightcut' : ('', 'integer', """
					Parameters describing the position and extent of the first topological cut, i.e. corresponding to the first X-point. Needed only to force different values from the ones computed automatically by b2ag.
					leftcut is the poloidal index of cells directly to the RIGHT of the left branch of the cut.
					rightcut is the poloidal index of cells directly to the RIGHT of the right branch of the cut.
					bottomcut is the radial index of cells directly below the cut.
					topcut is the radial index of cells directly above the cut.
				""", 'See description (integer)'),
   
      'b2agfs_bottomcut' : ('', 'integer', """
					Parameters describing the position and extent of the first topological cut, i.e. corresponding to the first X-point. Needed only to force different values from the ones computed automatically by b2ag.
					leftcut is the poloidal index of cells directly to the RIGHT of the left branch of the cut.
					rightcut is the poloidal index of cells directly to the RIGHT of the right branch of the cut.
					bottomcut is the radial index of cells directly below the cut.
					topcut is the radial index of cells directly above the cut.
				""", 'See description (integer)'),
   
      'b2agfs_topcut' : ('', 'integer', """
					Parameters describing the position and extent of the first topological cut, i.e. corresponding to the first X-point. Needed only to force different values from the ones computed automatically by b2ag.
					leftcut is the poloidal index of cells directly to the RIGHT of the left branch of the cut.
					rightcut is the poloidal index of cells directly to the RIGHT of the right branch of the cut.
					bottomcut is the radial index of cells directly below the cut.
					topcut is the radial index of cells directly above the cut.
				""", 'See description (integer)'),
   
      'b2agfs_leftcut2' : ('', 'integer', """
					Parameters describing the position and extent of the second topological cut, i.e. corresponding to the second X-point. Needed only to force different values from the ones computed automatically by b2ag.
					leftcut2 is the poloidal index of cells directly to the RIGHT of the left branch of the second cut.
					rightcut2 is the poloidal index of cells directly to the RIGHT of the right branch of the second cut.
					bottomcut is the radial index of cells directly below the second cut.
					topcut is the radial index of cells directly above the second cut.
				""", 'See description (integer)'),
   
      'b2agfs_rightcut2' : ('', 'integer', """
					Parameters describing the position and extent of the second topological cut, i.e. corresponding to the second X-point. Needed only to force different values from the ones computed automatically by b2ag.
					leftcut2 is the poloidal index of cells directly to the RIGHT of the left branch of the second cut.
					rightcut2 is the poloidal index of cells directly to the RIGHT of the right branch of the second cut.
					bottomcut is the radial index of cells directly below the second cut.
					topcut is the radial index of cells directly above the second cut.
				""", 'See description (integer)'),
   
      'b2agfs_bottomcut2' : ('', 'integer', """
					Parameters describing the position and extent of the second topological cut, i.e. corresponding to the second X-point. Needed only to force different values from the ones computed automatically by b2ag.
					leftcut2 is the poloidal index of cells directly to the RIGHT of the left branch of the second cut.
					rightcut2 is the poloidal index of cells directly to the RIGHT of the right branch of the second cut.
					bottomcut is the radial index of cells directly below the second cut.
					topcut is the radial index of cells directly above the second cut.
				""", 'See description (integer)'),
   
      'b2agfs_topcut2' : ('', 'integer', """
					Parameters describing the position and extent of the second topological cut, i.e. corresponding to the second X-point. Needed only to force different values from the ones computed automatically by b2ag.
					leftcut2 is the poloidal index of cells directly to the RIGHT of the left branch of the second cut.
					rightcut2 is the poloidal index of cells directly to the RIGHT of the right branch of the second cut.
					bottomcut is the radial index of cells directly below the second cut.
					topcut is the radial index of cells directly above the second cut.
				""", 'See description (integer)'),
   
      'b2agdr_nxiso1' : ('', 'integer', """
					Range of an optional isolated region to be included in the geometry.
					The isolated region will extend over the cell range spanned by (nxiso1:nxiso2,nyiso1:nyiso2).
					If only some of the four coordinates are given, the region is made to extent from the given coordinates to the end of the grid.
					Neighbourhood arrays and region indices are automatically adjusted.
				""", '-2'),
   
      'b2agdr_nxiso2' : ('', 'integer', """
					Range of an optional isolated region to be included in the geometry.
					The isolated region will extend over the cell range spanned by (nxiso1:nxiso2,nyiso1:nyiso2).
					If only some of the four coordinates are given, the region is made to extent from the given coordinates to the end of the grid.
					Neighbourhood arrays and region indices are automatically adjusted.
				""", '-2'),
   
      'b2agdr_nyiso1' : ('', 'integer', """
					Range of an optional isolated region to be included in the geometry.
					The isolated region will extend over the cell range spanned by (nxiso1:nxiso2,nyiso1:nyiso2).
					If only some of the four coordinates are given, the region is made to extent from the given coordinates to the end of the grid.
					Neighbourhood arrays and region indices are automatically adjusted.
				""", '-2'),
   
      'b2agdr_nyiso2' : ('', 'integer', """
					Range of an optional isolated region to be included in the geometry.
					The isolated region will extend over the cell range spanned by (nxiso1:nxiso2,nyiso1:nyiso2).
					If only some of the four coordinates are given, the region is made to extent from the given coordinates to the end of the grid.
					Neighbourhood arrays and region indices are automatically adjusted.
				""", '-2'),
   
      'b2agfs_geometry' : ('Geometry', 'string', """
					contains the file name of the geometry file to be read.
					The file will be looked for in the run directory, in the ../baserun directory, in $SOLPSTOP/data.local/meshes, and in $SOLPSTOP/modules/Carre/meshes/$DEVICE. To be used in b2ag.dat.
				""", 'upgrade.geometry'),
   
      'b2mwti_jxa' : ('Geometry', 'integer', """
					Cell index, on the basis mesh, of the outer midplane. Default value depends on geometry:
					Lower Single-null  : jxa=rightcut(1)-(rightcut(1)-leftcut(1))/4, i.e. three quarters of the way between the two cuts.
					Upper Single-null  : jxa=leftcut(1)+(rightcut(1)-leftcut(1))/4, i.e. one quarter of the way between the two cuts.
					Stellarator island : jxa=leftcut(1)+(rightcut(1)-leftcut(1))/2, i.e. midway between the two cuts.
					Double-null        : jxa=(rightcut(1)+rightcut(2))/2, i.e. halfway between the two outer cuts.
					Limiter geometry   : jxa=nx/2
					Straight geometry  : jxa=nx/2
					Superseded by the RZOMP definition from b2.user.parameters.
				""", 'See description (integer)'),
   
      'b2mwti_jxi' : ('Geometry', 'integer', """
					Cell index, on the basis mesh, of the inner midplane. Default value depends on geometry:
					Lower Single-null  : jxi=leftcut(1)+(rightcut(1)-leftcut(1))/4, i.e. one quarter of the way between the two cuts.
					Upper Single-null  : jxi=rightcut(1)-(rightcut(1)-leftcut(1))/4, i.e. three quarters of the way between the two cuts.
					Stellarator island : jxi=leftcut(1)+(rightcut(1)-leftcut(1))/4, i.e. one quarter of the way between the two cuts.
					Double-null        : jxi=(leftcut(1)+leftcut(2))/2, i.e. halfway between the two inner cuts.
					Limiter geometry   : jxi=nx/4
					Straight geometry  : jxi=nx/4
					Superseded by the RZIMP definition from b2.user.parameters.
				""", 'See description (integer)'),
   
      'b2mwti_jsep' : ('Geometry', 'integer', """
					Flux surface index, on the basis mesh, of the active separatrix. Can only be provided for slab geometries, otherwise deduced from geometry.
				""", 'See description (integer)'),
   
      'b2agmx_pbs_from_basis_mesh' : ('Geometry', 'integer', """
					If pbs_from_basis_mesh.eq.0, the pbs array is computed from values on the actual working mesh (old treatment).
					If pbs_from_basis_mesh.eq.1, the pbs array is computed from values on the (possibly) finer basis mesh from the geometry file and the contributions from each basis cell are added to obtain the value on the working mesh.
					In both cases, mind the value of 'b2news_area_fix', which should be also declared in b2ag.dat if the non-default behaviour is wanted.
				""", '1'),
   
      'b2agdr_redef_pbs' : ('Geometry', 'integer', """
					When b2agdr_redef_pbs.eq.1, geometrical quantities are adjusted so as to ensure that the poloidal flux between two flux surfaces remains constant.
				""", '1'),
   
      'b2mndr_redef_pbs' : ('Geometry', 'integer', """
					Obsolete. Should use b2agdr_redef_pbs instead.
				""", '0'),
   
      'b2agfs_periodic_bc' : ('Geometry', 'integer', """
					periodic_bc specifies if this is either an island or limiter geometry.
					If periodic_bc.eq.1 then island/limiter treatment is turned on. We differentiate between the two case through nncut:
					nncut.eq.0 = limiter case
					nncut.ge.1 = island divertor case (there should be nncut islands then)
					The case periodic_bc.eq.-1 is used to remove tranverse physics in 1-D cases.
					If periodic_bc.eq.0 then we have the usual treatment. No other values are currently allowed. To be used in b2ag.dat.
				""", '0'),
   
      'b2agsi_isymm' : ('Geometry', 'integer', """
					isymm specifies the type of symmetry of the geometry: isymm.eq.0 implies a slab geometry,
					isymm.eq.1.or.isymm.eq.2 imply rotational symmetry about the crx=0 axis, and isymm.eq.3.or.isymm.eq.4 indicate rotational symmetry about the cry=0 axis.
					Other values are not allowed.
					isymm.eq.1.or.isymm.eq.3 mean a toroidal geometry case, i.e. with a toroidal (out-of-plane) magnetic field component.
					isymm.eq.2.or.isymm.eq.4 mean a cylindrical geometry case, i.e. no toroidal magnetic field component. To be used in b2ag.dat.
				""", '1'),
   
      'b2stbc_solregno' : ('Geometry', 'integer', """
					solregno is the boundary index of the SOL North boundary in the input files b2ah.dat and b2mn.dat. For a standard single-null case, solregno is 3. For a standard double-null case, solregno for the outer SOL North boundary would be 7.
				""", '3'),
   
      'b2agmt_1d_width' : ('Geometry', 'real', """
					For 1-D cases, gives the width of the domain (in m) in the third (toroidal) dimension.
				""", '1.0'),
   
      'b2stbr_first_flight_no_of_start_points' : ('Geometry', 'integer', """
					When the first flight model is turned on, this number must be greater than or equal to the num
					ber of boundary cells on the mesh. Only in cases with special geometries (i.e. limiters, islands, ...) need it be increased beyond the default value above. This variable is only used within the first flight module.
				""", '2*(nx+2)+2*max(nncut,1)*(ny+2)'),
   
      'b2agfs_geom_match_dist' : ('Geometry', 'real', """
					Distance used as the matching criterion when reading the geometry file.
				""", '1.0e-6'),
   
      'b2agfs_Bt_adjust' : ('Geometry', 'integer', """
					If the mesh is offset (See b2agfs_xoffset, b2agfs_yoffset below) and Bt_adjust.eq.1, then the magnetic field is recomputed for toroidal geometries, keeping the pitch constant but changing the toroidal field magnitude according to Bt = Bt0/R. To be used in b2ag.dat.
				""", '0'),
   
      'b2agfs_Bt_rescale' : ('Geometry', 'real', """
					The magnetic field will be multiplied by Bt_rescale. All components of the field are scaled together. To be used in b2ag.dat.
				""", '1.0'),
   
      'b2agfs_pit_rescale' : ('Geometry', 'real', """
					The magnetic field line pitch will be multiplied by pit_rescale.
					This means that the poloidal field component is multiplied by pit_rescale, while the toroidal field component is left unchanged. To reverse the plasma current direction, set pit_rescale to -1.0.
					The sign convention used is that a positive poloidal field points in the direction of increasing &lt;ix&gt;. Be mindful however that, when inverting the sign of the poloidal magnetic field, you are also inverting the direction of the parallel velocity. You will then need to use the 'b2mndr_inverse_ua' switch to correct for that. To be used in b2ag.dat.
				""", '1.0'),
   
      'b2agfs_Bt_reversal' : ('Geometry', 'integer', """
					If Bt_reversal.eq.1, then the sign of the toroidal field component only is reversed. The sign convention used is that a positive toroidal field leads to a Bx(grad(B)) direction pointing down, so B is out of the page when looking at the usual view of the poloidal plane with the center line on the left. To be used in b2ag.dat.
				""", '0'),
   
      'b2agfs_min_pitch' : ('Geometry', 'real', """
					Minimum allowed value for the pitch angle (in degrees) at the plates.
				""", '1.0'),
   
      'b2agfs_nncut' : ('Geometry', 'integer', """
					Number of topological cuts in geometry. Needed only to force a different value from the one computed automatically by b2ag.
				""", 'See description (integer)'),
   
      'b2us_write_b2fgmtry_us' : ('Geometry', 'integer', """
					Switch for conversion with b2us; can be specified in the b2mn.dat file read by b2us during case conversion to unstructured format. When set to 1, unstructured b2fgmtry_us file is written by b2us. When set to 0, it is not.
				""", '1'),
   
      'b2us_write_b2fstati_us' : ('Geometry', 'integer', """
					Switch for conversion with b2us; can be specified in the b2mn.dat file read by b2us during case conversion to unstructured format. When set to 1, unstructured b2fstati_us file is written by b2us. When set to 0, it is not.
				""", '1'),
   
      'conv_triangles_old_co' : ('Geometry', 'integer', """
					Switch for conversion with b2us; can be specified in the b2mn.dat file read by b2us during case conversion to unstructured format. When converting a structured case with b2us and conv_triangles_old_co = 1, the coordinates of the nodes of the triangles from the original fort.33 file will be used in the unstructured format. Otherwise, the triangular mesh will be exactly matched to the B2.5 grid.  Setting the switch to 1 may be required when converting triangle grids that include extreme slender/skewed triangles (typically manifested through FOLNEUT errors at runtime after case conversion).
				""", '0'),
   
      'b2us_auto_midplane_det' : ('Geometry', 'integer', """
					Switch for conversion with b2us; can be specified in the b2mn.dat file read by b2us during case conversion to unstructured format. When set to 1, b2us will automatically try to reconstruct outer and inner midplane from the geometry (magnetic field and cell coordinates), and write the corresponding coordinates in b2.user.parameters. When set to 0, the IMP and OMP definition will be based on the values of b2mwti_jxi, b2mwti_jxa, b2mwti_jsep.
				""", '1'),
   
      'b2us_prep_Qalfmin' : ('Geometry', 'real', """
					If abs(cos(alpha)*bx).ge.b2us_prep_Qalfmin, the beta angle is assigned to zero during writing of b2fgmtry.
					If abs(cos(alpha)*bx).lt.b2us_prep_Qalfmin, boundary faces are treated like field-aligned faces in BCMOM=13, BCCON=14, BCENE=15 (style=1), BCENI=15 (style=0) and BCPOT=11. Leakage coefficients (if they are needed) are set equal to b2us_prep_Qalfmax.
				""", '1e-3'),
   
      'b2us_prep_Qalfmax' : ('Geometry', 'real', """
					If abs(cos(alpha)*bx).ge.b2us_prep_Qalfmin .and. abs(cos(alpha)*bx).lt.b2us_prep_Qalfmax, fcPbs is set equal to b2us_prep_Qalfmax*fcS for boundary faces during writing of b2fgmtry.
				""", '1e-3'),
   
      'b2us_prep_mod_hc' : ('Geometry', 'integer', """
					If b2us_prep_mod_hc.eq.1 then the length between cell face center and neighboring cell centers (fcHc) will be modified.	It will be the same for neighboring boundary faces belonging to the same flux tube. For all boundary faces it will be recalculated to decrease the distance between boundary face and guard cell centers.
				""", '0'),
   
      'b2us_prep_set_beta_0' : ('Geometry', 'integer', """
					If b2us_prep_set_beta_0.eq.1, the beta angle will be assigned to zero for faces between boundary cells belonging to same shaved flux tube.
				""", '0'),
   
      'b2mndr_ids_path' : ('', 'character*256', """
					These switches serve as identification for the simulation. They can be inherited from the SOLPS-GUI:
					IDS path : Only available if using IMAS Access Layer 5. The directory path where the IMAS data entry will be saved. Supersedes the pulse (previously shot) and run numbers. May begin with "$HOME", "$IMASDIR", or "$SOLPSTOP", that will be parsed by the code. If it begins with a '/', is understood as an absolute path, otherwise will be prefixed with the $IMASDIR environment variable. Defaults to the last line in the 'shotnumber.history' file if present, and to $IMASDIR/${pulse_number}/${run_number} otherwise or if $IMASDIR is modified from its default value by the switches below.
					Pulse number : Pulse number identifying the run (supersedes b2mndr_shot_number). Defaults to the last number found in shotnumber.history, or 0 if the file is not found. Must be positive and non-zero if an IMAS data entry is requested. If using IMAS Access Layer 4, cannot exceed 214748.
					Run number : The number of the run. Must be positive or zero. If using IMAS Access Layer 4, limited to 5 digits (i.e. span from 0 to 99999).
					Database : IMAS IDS database name (supersedes b2mndr_device). Defaults to 'solps-iter' if $DEVICE if undefined. If $DEVICE is 'iter', the code internally changes it to 'ITER' to follow the IMAS convention. Can be used to rebuild the IMASDIR path.
					User : The user who ran the simulation. Can be used to rebuild the IMASDIR path.
				""", 'See description'),
   
      'b2mndr_pulse_number' : ('', 'integer', """
					These switches serve as identification for the simulation. They can be inherited from the SOLPS-GUI:
					IDS path : Only available if using IMAS Access Layer 5. The directory path where the IMAS data entry will be saved. Supersedes the pulse (previously shot) and run numbers. May begin with "$HOME", "$IMASDIR", or "$SOLPSTOP", that will be parsed by the code. If it begins with a '/', is understood as an absolute path, otherwise will be prefixed with the $IMASDIR environment variable. Defaults to the last line in the 'shotnumber.history' file if present, and to $IMASDIR/${pulse_number}/${run_number} otherwise or if $IMASDIR is modified from its default value by the switches below.
					Pulse number : Pulse number identifying the run (supersedes b2mndr_shot_number). Defaults to the last number found in shotnumber.history, or 0 if the file is not found. Must be positive and non-zero if an IMAS data entry is requested. If using IMAS Access Layer 4, cannot exceed 214748.
					Run number : The number of the run. Must be positive or zero. If using IMAS Access Layer 4, limited to 5 digits (i.e. span from 0 to 99999).
					Database : IMAS IDS database name (supersedes b2mndr_device). Defaults to 'solps-iter' if $DEVICE if undefined. If $DEVICE is 'iter', the code internally changes it to 'ITER' to follow the IMAS convention. Can be used to rebuild the IMASDIR path.
					User : The user who ran the simulation. Can be used to rebuild the IMASDIR path.
				""", '0'),
   
      'b2mndr_shot_number' : ('', 'integer', """
					These switches serve as identification for the simulation. They can be inherited from the SOLPS-GUI:
					IDS path : Only available if using IMAS Access Layer 5. The directory path where the IMAS data entry will be saved. Supersedes the pulse (previously shot) and run numbers. May begin with "$HOME", "$IMASDIR", or "$SOLPSTOP", that will be parsed by the code. If it begins with a '/', is understood as an absolute path, otherwise will be prefixed with the $IMASDIR environment variable. Defaults to the last line in the 'shotnumber.history' file if present, and to $IMASDIR/${pulse_number}/${run_number} otherwise or if $IMASDIR is modified from its default value by the switches below.
					Pulse number : Pulse number identifying the run (supersedes b2mndr_shot_number). Defaults to the last number found in shotnumber.history, or 0 if the file is not found. Must be positive and non-zero if an IMAS data entry is requested. If using IMAS Access Layer 4, cannot exceed 214748.
					Run number : The number of the run. Must be positive or zero. If using IMAS Access Layer 4, limited to 5 digits (i.e. span from 0 to 99999).
					Database : IMAS IDS database name (supersedes b2mndr_device). Defaults to 'solps-iter' if $DEVICE if undefined. If $DEVICE is 'iter', the code internally changes it to 'ITER' to follow the IMAS convention. Can be used to rebuild the IMASDIR path.
					User : The user who ran the simulation. Can be used to rebuild the IMASDIR path.
				""", '0'),
   
      'b2mndr_run_number' : ('', 'integer', """
					These switches serve as identification for the simulation. They can be inherited from the SOLPS-GUI:
					IDS path : Only available if using IMAS Access Layer 5. The directory path where the IMAS data entry will be saved. Supersedes the pulse (previously shot) and run numbers. May begin with "$HOME", "$IMASDIR", or "$SOLPSTOP", that will be parsed by the code. If it begins with a '/', is understood as an absolute path, otherwise will be prefixed with the $IMASDIR environment variable. Defaults to the last line in the 'shotnumber.history' file if present, and to $IMASDIR/${pulse_number}/${run_number} otherwise or if $IMASDIR is modified from its default value by the switches below.
					Pulse number : Pulse number identifying the run (supersedes b2mndr_shot_number). Defaults to the last number found in shotnumber.history, or 0 if the file is not found. Must be positive and non-zero if an IMAS data entry is requested. If using IMAS Access Layer 4, cannot exceed 214748.
					Run number : The number of the run. Must be positive or zero. If using IMAS Access Layer 4, limited to 5 digits (i.e. span from 0 to 99999).
					Database : IMAS IDS database name (supersedes b2mndr_device). Defaults to 'solps-iter' if $DEVICE if undefined. If $DEVICE is 'iter', the code internally changes it to 'ITER' to follow the IMAS convention. Can be used to rebuild the IMASDIR path.
					User : The user who ran the simulation. Can be used to rebuild the IMASDIR path.
				""", '0'),
   
      'b2mndr_database' : ('', 'string', """
					These switches serve as identification for the simulation. They can be inherited from the SOLPS-GUI:
					IDS path : Only available if using IMAS Access Layer 5. The directory path where the IMAS data entry will be saved. Supersedes the pulse (previously shot) and run numbers. May begin with "$HOME", "$IMASDIR", or "$SOLPSTOP", that will be parsed by the code. If it begins with a '/', is understood as an absolute path, otherwise will be prefixed with the $IMASDIR environment variable. Defaults to the last line in the 'shotnumber.history' file if present, and to $IMASDIR/${pulse_number}/${run_number} otherwise or if $IMASDIR is modified from its default value by the switches below.
					Pulse number : Pulse number identifying the run (supersedes b2mndr_shot_number). Defaults to the last number found in shotnumber.history, or 0 if the file is not found. Must be positive and non-zero if an IMAS data entry is requested. If using IMAS Access Layer 4, cannot exceed 214748.
					Run number : The number of the run. Must be positive or zero. If using IMAS Access Layer 4, limited to 5 digits (i.e. span from 0 to 99999).
					Database : IMAS IDS database name (supersedes b2mndr_device). Defaults to 'solps-iter' if $DEVICE if undefined. If $DEVICE is 'iter', the code internally changes it to 'ITER' to follow the IMAS convention. Can be used to rebuild the IMASDIR path.
					User : The user who ran the simulation. Can be used to rebuild the IMASDIR path.
				""", '$(DEVICE)'),
   
      'b2mndr_device' : ('', 'string', """
					These switches serve as identification for the simulation. They can be inherited from the SOLPS-GUI:
					IDS path : Only available if using IMAS Access Layer 5. The directory path where the IMAS data entry will be saved. Supersedes the pulse (previously shot) and run numbers. May begin with "$HOME", "$IMASDIR", or "$SOLPSTOP", that will be parsed by the code. If it begins with a '/', is understood as an absolute path, otherwise will be prefixed with the $IMASDIR environment variable. Defaults to the last line in the 'shotnumber.history' file if present, and to $IMASDIR/${pulse_number}/${run_number} otherwise or if $IMASDIR is modified from its default value by the switches below.
					Pulse number : Pulse number identifying the run (supersedes b2mndr_shot_number). Defaults to the last number found in shotnumber.history, or 0 if the file is not found. Must be positive and non-zero if an IMAS data entry is requested. If using IMAS Access Layer 4, cannot exceed 214748.
					Run number : The number of the run. Must be positive or zero. If using IMAS Access Layer 4, limited to 5 digits (i.e. span from 0 to 99999).
					Database : IMAS IDS database name (supersedes b2mndr_device). Defaults to 'solps-iter' if $DEVICE if undefined. If $DEVICE is 'iter', the code internally changes it to 'ITER' to follow the IMAS convention. Can be used to rebuild the IMASDIR path.
					User : The user who ran the simulation. Can be used to rebuild the IMASDIR path.
				""", '$(DEVICE)'),
   
      'b2mndr_user' : ('', 'string', """
					These switches serve as identification for the simulation. They can be inherited from the SOLPS-GUI:
					IDS path : Only available if using IMAS Access Layer 5. The directory path where the IMAS data entry will be saved. Supersedes the pulse (previously shot) and run numbers. May begin with "$HOME", "$IMASDIR", or "$SOLPSTOP", that will be parsed by the code. If it begins with a '/', is understood as an absolute path, otherwise will be prefixed with the $IMASDIR environment variable. Defaults to the last line in the 'shotnumber.history' file if present, and to $IMASDIR/${pulse_number}/${run_number} otherwise or if $IMASDIR is modified from its default value by the switches below.
					Pulse number : Pulse number identifying the run (supersedes b2mndr_shot_number). Defaults to the last number found in shotnumber.history, or 0 if the file is not found. Must be positive and non-zero if an IMAS data entry is requested. If using IMAS Access Layer 4, cannot exceed 214748.
					Run number : The number of the run. Must be positive or zero. If using IMAS Access Layer 4, limited to 5 digits (i.e. span from 0 to 99999).
					Database : IMAS IDS database name (supersedes b2mndr_device). Defaults to 'solps-iter' if $DEVICE if undefined. If $DEVICE is 'iter', the code internally changes it to 'ITER' to follow the IMAS convention. Can be used to rebuild the IMASDIR path.
					User : The user who ran the simulation. Can be used to rebuild the IMASDIR path.
				""", '$(USER)'),
   
      'b2mndr_delta_max' : ('', 'real', """
					One of the dynamic timestep control parameters. Only active if both delta_max and delta_min are nonzero. The timestep is increased by a factor dt_change_inc or decreased by a factor dt_change_dec, within the bounds [dt_min, dt_max], according to whether the largest instantaneous change in all equations is smaller than delta_min or larger than delta_max, respectively.
				""", '0.0'),
   
      'b2mndr_delta_min' : ('', 'real', """
					One of the dynamic timestep control parameters. Only active if both delta_max and delta_min are nonzero. The timestep is increased by a factor dt_change_inc or decreased by a factor dt_change_dec, within the bounds [dt_min, dt_max], according to whether the largest instantaneous change in all equations is smaller than delta_min or larger than delta_max, respectively.
				""", '0.0'),
   
      'b2mndr_dt_change_dec' : ('', 'real', """
					One of the dynamic timestep control parameters. Only active if both delta_max and delta_min are nonzero. The timestep is increased by a factor dt_change_inc or decreased by a factor dt_change_dec, within the bounds [dt_min, dt_max], according to whether the largest instantaneous change in all equations is smaller than delta_min or larger than delta_max, respectively.
				""", '1.0'),
   
      'b2mndr_dt_change_inc' : ('', 'real', """
					One of the dynamic timestep control parameters. Only active if both delta_max and delta_min are nonzero. The timestep is increased by a factor dt_change_inc or decreased by a factor dt_change_dec, within the bounds [dt_min, dt_max], according to whether the largest instantaneous change in all equations is smaller than delta_min or larger than delta_max, respectively.
				""", '1.0'),
   
      'b2mndr_dt_max' : ('', 'real', """
					One of the dynamic timestep control parameters. Only active if both delta_max and delta_min are nonzero. The timestep is increased by a factor dt_change_inc or decreased by a factor dt_change_dec, within the bounds [dt_min, dt_max], according to whether the largest instantaneous change in all equations is smaller than delta_min or larger than delta_max, respectively.
				""", '1.0e+01'),
   
      'b2mndr_dt_min' : ('', 'real', """
					One of the dynamic timestep control parameters. Only active if both delta_max and delta_min are nonzero. The timestep is increased by a factor dt_change_inc or decreased by a factor dt_change_dec, within the bounds [dt_min, dt_max], according to whether the largest instantaneous change in all equations is smaller than delta_min or larger than delta_max, respectively.
				""", '1.0e-30'),
   
      'b2mndt_nstg0' : ('', 'integer', """
					Time-dependent mode and iterative mode switches. The basic code timestep proceeds as follows:
					 ..test input arguments
					 ..compute auxiliary quantities
					 ..prepare source computation
					 ..do i0=1,nstg0
					  ..compute log-log linearised rate coefficients
					  ..do i1=1,nstg1
					   ..compute source linearisation (Eirene call)
					   ..do i2=1,nstg2
					    ..perform one inner iteration (on fluid equations)
					    ..re-compute auxiliary quantities
					    ..produce monitoring output
					   ..enddo
					  ..enddo
					 ..enddo
					This can be completed by the the 'b2mndt_nstg_ares??' switches. See 'Numerics' section for details.
					It is recommended to use these inner iterations when running in time-dependent mode (b2mndt_style=2) to make residuals converge within each time-step.
				""", '1'),
   
      'b2mndt_nstg1' : ('', 'integer', """
					Time-dependent mode and iterative mode switches. The basic code timestep proceeds as follows:
					 ..test input arguments
					 ..compute auxiliary quantities
					 ..prepare source computation
					 ..do i0=1,nstg0
					  ..compute log-log linearised rate coefficients
					  ..do i1=1,nstg1
					   ..compute source linearisation (Eirene call)
					   ..do i2=1,nstg2
					    ..perform one inner iteration (on fluid equations)
					    ..re-compute auxiliary quantities
					    ..produce monitoring output
					   ..enddo
					  ..enddo
					 ..enddo
					This can be completed by the the 'b2mndt_nstg_ares??' switches. See 'Numerics' section for details.
					It is recommended to use these inner iterations when running in time-dependent mode (b2mndt_style=2) to make residuals converge within each time-step.
				""", '1'),
   
      'b2mndt_nstg2' : ('', 'integer', """
					Time-dependent mode and iterative mode switches. The basic code timestep proceeds as follows:
					 ..test input arguments
					 ..compute auxiliary quantities
					 ..prepare source computation
					 ..do i0=1,nstg0
					  ..compute log-log linearised rate coefficients
					  ..do i1=1,nstg1
					   ..compute source linearisation (Eirene call)
					   ..do i2=1,nstg2
					    ..perform one inner iteration (on fluid equations)
					    ..re-compute auxiliary quantities
					    ..produce monitoring output
					   ..enddo
					  ..enddo
					 ..enddo
					This can be completed by the the 'b2mndt_nstg_ares??' switches. See 'Numerics' section for details.
					It is recommended to use these inner iterations when running in time-dependent mode (b2mndt_style=2) to make residuals converge within each time-step.
				""", '1'),
   
      'b2news_facdrift_dec' : ('', 'real', """
					Ramping parameters for facdrift, which multiplies the diamagnetic terms as well as the ion inertia current. The code is started on the first time step with facdrift=facdrift_start. If facdrift_target.ne.facdrift_start, then, on each time step, facdrift is multiplied by facdrift_inc. If the code does not converge on the timestep, facdrift is decreased by facdrift_dec. A facdrift profile is also possible, see Numerics section for details.
					The ion-neutral friction current requires either facdrift or fac_ExB to be turned on as well.
				""", '0.0'),
   
      'b2news_facdrift_inc' : ('', 'real', """
					Ramping parameters for facdrift, which multiplies the diamagnetic terms as well as the ion inertia current. The code is started on the first time step with facdrift=facdrift_start. If facdrift_target.ne.facdrift_start, then, on each time step, facdrift is multiplied by facdrift_inc. If the code does not converge on the timestep, facdrift is decreased by facdrift_dec. A facdrift profile is also possible, see Numerics section for details.
					The ion-neutral friction current requires either facdrift or fac_ExB to be turned on as well.
				""", '1.0'),
   
      'b2news_facdrift_start' : ('', 'real', """
					Ramping parameters for facdrift, which multiplies the diamagnetic terms as well as the ion inertia current. The code is started on the first time step with facdrift=facdrift_start. If facdrift_target.ne.facdrift_start, then, on each time step, facdrift is multiplied by facdrift_inc. If the code does not converge on the timestep, facdrift is decreased by facdrift_dec. A facdrift profile is also possible, see Numerics section for details.
					The ion-neutral friction current requires either facdrift or fac_ExB to be turned on as well.
				""", '0.0'),
   
      'b2news_facdrift_target' : ('', 'real', """
					Ramping parameters for facdrift, which multiplies the diamagnetic terms as well as the ion inertia current. The code is started on the first time step with facdrift=facdrift_start. If facdrift_target.ne.facdrift_start, then, on each time step, facdrift is multiplied by facdrift_inc. If the code does not converge on the timestep, facdrift is decreased by facdrift_dec. A facdrift profile is also possible, see Numerics section for details.
					The ion-neutral friction current requires either facdrift or fac_ExB to be turned on as well.
				""", '0.0'),
   
      'b2news_facExB_dec' : ('', 'real', """
					Ramping parameters for facExB, which multiplies the ExB terms. Same treatment as above for facdrift. Can be superseded by b2news_ExB to set a constant value throughout the run.
				""", '0.0'),
   
      'b2news_facExB_inc' : ('', 'real', """
					Ramping parameters for facExB, which multiplies the ExB terms. Same treatment as above for facdrift. Can be superseded by b2news_ExB to set a constant value throughout the run.
				""", '1.0'),
   
      'b2news_facExB_start' : ('', 'real', """
					Ramping parameters for facExB, which multiplies the ExB terms. Same treatment as above for facdrift. Can be superseded by b2news_ExB to set a constant value throughout the run.
				""", '0.0'),
   
      'b2news_facExB_target' : ('', 'real', """
					Ramping parameters for facExB, which multiplies the ExB terms. Same treatment as above for facdrift. Can be superseded by b2news_ExB to set a constant value throughout the run.
				""", '0.0'),
   
      'b2news_facvis_dec' : ('', 'real', """
					Ramping parameters for facvis, which multiplies the drift viscosity terms. Same treatment as above for facdrift. Can be superseded by b2news_vis to set a constant value throughout the run.
				""", '0.0'),
   
      'b2news_facvis_inc' : ('', 'real', """
					Ramping parameters for facvis, which multiplies the drift viscosity terms. Same treatment as above for facdrift. Can be superseded by b2news_vis to set a constant value throughout the run.
				""", '1.0'),
   
      'b2news_facvis_start' : ('', 'real', """
					Ramping parameters for facvis, which multiplies the drift viscosity terms. Same treatment as above for facdrift. Can be superseded by b2news_vis to set a constant value throughout the run.
				""", '0.0'),
   
      'b2news_facvis_target' : ('', 'real', """
					Ramping parameters for facvis, which multiplies the drift viscosity terms. Same treatment as above for facdrift. Can be superseded by b2news_vis to set a constant value throughout the run.
				""", '0.0'),
   
      'b2stbc_boundary_namelist' : ('', 'integer', """
					Namelist file indicators. If xxx_namelist.eq.1, then the code looks for the file b2.xxx.parameters, in which it expects to find the xxx namelist.
					In the case of boundary_namelist, defaults to 1 for double-null and snowflake geometries, 0 otherwise.
				""", 'See description'),
   
      'b2stbr_neutrals_namelist' : ('', 'integer', """
					Namelist file indicators. If xxx_namelist.eq.1, then the code looks for the file b2.xxx.parameters, in which it expects to find the xxx namelist.
					In the case of boundary_namelist, defaults to 1 for double-null and snowflake geometries, 0 otherwise.
				""", '0'),
   
      'b2srdt_numerics_namelist' : ('', 'integer', """
					Namelist file indicators. If xxx_namelist.eq.1, then the code looks for the file b2.xxx.parameters, in which it expects to find the xxx namelist.
					In the case of boundary_namelist, defaults to 1 for double-null and snowflake geometries, 0 otherwise.
				""", '0'),
   
      'b2tqna_transport_namelist' : ('', 'integer', """
					Namelist file indicators. If xxx_namelist.eq.1, then the code looks for the file b2.xxx.parameters, in which it expects to find the xxx namelist.
					In the case of boundary_namelist, defaults to 1 for double-null and snowflake geometries, 0 otherwise.
				""", '0'),
   
      'b2optim_namelist' : ('', 'integer', """
					Namelist file indicators. If xxx_namelist.eq.1, then the code looks for the file b2.xxx.parameters, in which it expects to find the xxx namelist.
					In the case of boundary_namelist, defaults to 1 for double-null and snowflake geometries, 0 otherwise.
				""", '0'),
   
      'b2aidr_read_b2fstate' : ('Run', 'integer', """
					If read_b2fstate.ne.0, b2aidr will read an existing b2fstate file and append to it a flat state description for additional new species being introduced in the run.
				""", '0'),
   
      'b2mndr_ntim' : ('Run', 'integer', """
					Number of timesteps desired in this run. If ntim.eq.0, the code simply reads the input file and creates the b2fplasma and b2fstate files corresponding to the present plasma state.
				""", '1'),
   
      'b2mndr_dtim' : ('Run', 'real', """
					Timestep (in seconds).
				""", '1.0'),
   
      'b2mndr_stim' : ('Run', 'real', """
					stim specifies the initial time --- default 0.
					If set to a positive or zero value, this overwrites the time value read from b2fstati.
					If set to a negative value, the run continues from the time read in b2fstati. In that case, the tracing data is appended to the existing files, otherwise the tracing files are overwritten.
				""", '0.0'),
   
      'b2mndr_etim' : ('Run', 'real', """
					etim specifies the end time. Only active if etim &gt; stim.
				""", '0.0'),
   
      'b2news_no_solve' : ('Run', 'integer', """
					If no_solve.eq.1, then the code is run without actually solving any equations. All secondary and dependent data is computed.
					The nstg(0:2) array is overwritten to '1's. The simulation time will not be updated. The code will compute fluxes, sources, transport coefficients, etc... 'ntim' times but not update the basic plasma quantities. Additionally, if no_solve is set to a negative value, then only some equations are solved (simulation time and nstg arrays will behave normally).
					no_solve.eq.-1 will activate the parallel momentum equations only.
					no_solve.eq.-2 will activate the density equations only.
					no_solve.eq.-4 will activate the potential equation only. (Active only if poteq.eq.1, otherwise, the behaviour dictated by the poteq setting applies).
					no_solve.eq.-8 will activate the heat equations only. These can be combined. For example, no_solve.eq.-3 will activate the parallel momentum and particle conservation equations.
					If the no_solve switch requires an equation not to be solved, the settings in the corresponding solvexx arrays from b2.numerics.parameters are moot.
					The latter are reserved for fine-tuning numerical diagnostics.
					If wishing to toggle whether to solve or not to solve each equation separately, one should set, in the b2.numerics.parameters input file, the SOLVEMO, SOLVEMT, SOLVECO, SOLVEE, SOLVEEI, SOLVEET and SOLVEPO arrays, respectively, for each of the parallel momentum equations, the total momentum equation, each density equation, the electron and ion heat equations, and the total energy equation.
					When running in time-dependent mode, the total energy and total momentum equations are not solved.
					The table below shows which combination of equations will be solved	depending on the value of switch 'b2news_no_solve'
					*----------------------------------------------------
					*        | value |  co  |  mo  |  he  |  hi  |  po  |
					*----------------------------------------------------
					*        |   0   |  +   |  +   |  +   |  +   |  +   |
					*----------------------------------------------------
					*        |   1   |  -   |  -   |  -   |  -   |  -   |
					*----------------------------------------------------
					*        |  -1   |  -   |  +   |  -   |  -   |  -   |
					*----------------------------------------------------
					*        |  -2   |  +   |  -   |  -   |  -   |  -   |
					*----------------------------------------------------
					*        |  -3   |  +   |  +   |  -   |  -   |  -   |
					*----------------------------------------------------
					*        |  -4   |  -   |  -   |  -   |  -   |  +   |
					*----------------------------------------------------
					*        |  -5   |  -   |  +   |  -   |  -   |  +   |
					*----------------------------------------------------
					*        |  -6   |  +   |  -   |  -   |  -   |  +   |
					*----------------------------------------------------
					*        |  -7   |  +   |  +   |  -   |  -   |  +   |
					*----------------------------------------------------
					*        |  -8   |  -   |  -   |  +   |  +   |  -   |
					*----------------------------------------------------
					*        |  -9   |  -   |  +   |  +   |  +   |  -   |
					*----------------------------------------------------
					*        | -10   |  +   |  -   |  +   |  +   |  -   |
					*----------------------------------------------------
					*        | -11   |  +   |  +   |  +   |  +   |  -   |
					*----------------------------------------------------
					*        | -12   |  -   |  -   |  +   |  +   |  +   |
					*----------------------------------------------------
					*        | -13   |  -   |  +   |  +   |  +   |  +   |
					*----------------------------------------------------
					*        | -14   |  +   |  -   |  +   |  +   |  +   |
					*----------------------------------------------------
				""", '0'),
   
      'b2mndr_cpu' : ('Run', 'real', """
					CPU limit. If cpu.eq.0.0, no CPU limit is enforced. Otherwise, the code stops smoothly after it has been running for at least 'cpu' CPU seconds.
				""", '0.0'),
   
      'b2mndr_elapsed' : ('Run', 'real', """
					Elapsed time limit. Is elapsed.eq.0.0, no time limit is enforced.
					Otherwise, the code stops smoothly after is has been running for at least 'elapsed' wall clock seconds.
				""", '0.0'),
   
      'b2mndr_savecpu' : ('Run', 'real', """
					If savecpu.gt.0.0, CPU time interval after which save files plasmastate.xxxx are written. Other additional options for writing of the checkpointing files are available by means of the b2mndt_ntim_save and/or b2mndr_plasmatim switches.
					These can be used, in conjunction with the b2co.exe instruction, to recover a crashed run.
				""", '3600.0'),
   
      'b2mndr_ismain' : ('Run', 'real', """
					ismain identifies the index of the main plasma species.
					It must hold that ismain is not a neutral species.
				""", '1'),
   
      'b2sral_inputfile' : ('Run', '', """
					Profiles file indicator. If b2sral_inputfile.eq.1, then the code looks for the file b2.sources.profile in which it expects to find the 'profile' namelist.
					This namelist will contain profiles of sources measured from the outer midplane separatrix location, which is set with the [RZ]OMP variables in b2.user.parameters.
				""", '0'),
   
      'b2tqna_inputfile' : ('Run', 'integer', """
					Profiles file indicator. If b2tqna_inputfile.eq.1, then the code looks for the file b2.transport.inputfile, in which it expects to find the transport namelist.
					This namelist will contain profiles of transport parameters measured from the outer midplane separatrix location, which is set with the [RZ]OMP variables in b2.user.parameters.
				""", '0'),
   
      'b2mndr_eirene' : ('Run', 'integer', """
					Turns on coupling with the Eirene Monte Carlo neutral code if nonzero.
					To be used, the code must be compiled with the -DB25_EIRENE option.
				""", '0'),
   
      'b2mndr_astra' : ('Run', 'integer', """
					Turns on coupling with the ASTRA core transport code if nonzero.
					To be used, the code must be compiled with the -DASTRA option.
				""", '0'),
   
      'b2mndr_rescale_neutrals_sources' : ('Run', 'real', """
					Multiplier to the neutral sources (either computed by Eirene or the corresponding rate coefficients).
				""", '1.0'),
   
      'b2mndr_rescale_neutrals' : ('Run', 'real', """
					Multiplier to the neutral density on the first timestep.
				""", '1.0'),
   
      'b2mndr_density_rescale' : ('Run', 'real', """
					Multiplier of all densities on the first timestep.
				""", '1.0'),
   
      'b2stbr_core_sources_rescale' : ('Run', 'real', """
					Multiplier to the totally ionised species sources at the core boundary.
				""", '1.0'),
   
      'b2mndt_density_control' : ('Run', 'integer', """
					Feedback on the total heavy particle density. If density_control.ne.0, the sum of all densities is kept constant.
				""", '0'),
   
      'b2stbc_feedback' : ('Run', 'integer', """
					If feedback.eq.1, turns on feedback mode for the boundary conditions.
					See Physics section for more details. Equivalent to LFEEDBACK=.true. in the b2.boundary.parameters namelist.
				""", '0'),
   
      'b2stbc_ncallfeedback' : ('Run', 'integer', """
					Timestep index after which the feedback in b2stbc is activated. NOT YET CONVERTED IN WG CODE
				""", '0'),
   
      'b2stbr_first_flight' : ('Run', 'integer', """
					If first_flight.ne.0, turns on the first flight model. See Physics section for additional details.
				""", '0'),
   
      'b2ytdr_ns' : ('Run', 'integer', """
					New number of species desired when creating a new initial state file using b2yt.exe. Must be specified within b2yt.dat.
				""", 'ns'),
   
      'b2ytdr_jsep1' : ('Run', 'integer', """
					Radial index of separatrix in the converted grid. Must be specified within b2yt.dat. Only applies when converting linear geometries.
				""", 'nx1/2'),
   
      'b2ytdr_ndepth1' : ('Run', 'integer', """
					New resolution of target depth desired when creating a new initial state file using b2yt.exe. Must be specified within b2yt.dat.
				""", 'ndepth_nml'),
   
      'b2ytdr_rescale_neutrals' : ('Run', 'real', """
					Rescaling of neutral densities by rescale_neutrals when creating a new initial state file using b2yt.exe. Must be specified within b2yt.dat.
				""", '1.0'),
   
      'b2ytdr_non_commensurate' : ('Run', 'integer', """
					When set to 1, b2yt will attempt to interpolate a plasma solution and create new input files for a new grid which is not commensurate to the original grid, but still has the same topology.
					Must be specified within b2yt.dat.
				""", '0'),
   
      'b2tfhe_anomalous' : ('', 'real', """
					Real parameter which determines anomalous current.
					Both b2tfhe_anomalous and b2tanml_anomalous point to the same switch (backward compatibility with SOLPS5.2): b2tfhe_anomalous is checked first and only if it is not found is b2tanml_anomalous looked for.
					If b2tfhe_anomalous is 0 then anomalous current is switched off otherwise anomalous current is switched on, and the numerical value of b2tfhe_anomalous acts as a multiplier to the anomalous electrical conductivity and thermo-electric coefficients provided.
				""", '1.0'),
   
      'b2tanml_anomalous' : ('', 'real', """
					Real parameter which determines anomalous current.
					Both b2tfhe_anomalous and b2tanml_anomalous point to the same switch (backward compatibility with SOLPS5.2): b2tfhe_anomalous is checked first and only if it is not found is b2tanml_anomalous looked for.
					If b2tfhe_anomalous is 0 then anomalous current is switched off otherwise anomalous current is switched on, and the numerical value of b2tfhe_anomalous acts as a multiplier to the anomalous electrical conductivity and thermo-electric coefficients provided.
				""", '1.0'),
   
      'b2stbc_fheycore' : ('', 'real', """
					The 20 switches above are all feedback switches and require that b2stbc_feedback.ne.0 (See Run section for details) or that lfeedback=.true. in b2.boundary.parameters. Feedback schemes are now all applied in the same way in a dedicated module b2us_feedback (see FEEDBACK_CONTROL namelist). Switches in b2mn.dat are still available and will override whatever is specified in b2.feedback_control.parameters, but it is recommended to not use switches anymore. This will allow more flexibility in applying such schemes.
					The feedback is done as a boundary condition and is under-relaxed using the b2stbc_...._alpha switches (See Numerics section for details).
					fheycore is the radial electron heat flow entering the core boundary.  Will apply fb_type=11, fb_rescale=1, fb_actuator=4 on region defined by coreregno.
					fhiycore is the radial ion heat flow entering the core boundary. Will apply fb_type=12, fb_rescale=1, fb_actuator=5 on region defined by coreregno.
					fchycore is the radial current entering the core boundary. Will apply fb_type=13, fb_rescale=1, fb_actuator=4 on region defined by coreregno.
					fnaycore is the radial flux of species "isfeedback" entering the core boundary. Will apply fb_type=10, fb_rescale=1, fb_actuator=3 on region defined by coreregno.
					If fhiycore_kinetic_energy.eq.1, the parallel kinetic energy flux is counted as part of the ion energy flux.
					For double-null cases, the f..ycore variables contain the total flow through both core boundaries taken together (to be checked for WG code!).
					The core boundaries are identified by the coreregno and coreregn2 switches (see Geometry section). These switches need to be manually adjusted for WG cases as now they indicate the boundary where the feedback is applied. For switches like b2stbc_xxxycore or private_gas\_puff the user has to specify in b2.feedback_control.parameters} where the feedback is calculated (see b2us.regions.parameters produced at conversion), while coreregno still indicates where it is applied. pfrregno and solregno lose meaning in kinetic cases if the actuator is the gas puff. Coreregn2 and pfrregno2 are not yet converted/used.
					The other seven switches are density feedback switches: nesepm is the outer midplane separatrix electron density. (See rzomp switch in b2.user.parameters for setting of midplane position). This is controlled through particle input of main plasma species isfeedback through the core boundary (See Geometry section for the core boundary indices coreregno and coreregn2).
					nesepm_sol is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the SOL region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the SOL North boundary (See Geometry section for the SOL North boundary index solregno). If nesepm_overshoot.gt.1.0, the gas puff is turned off when the midplane separatrix density reaches nesepm*nesepm_overshoot. Minimum and maximum values of the feedback gas puff can be set using b2stbc_nesepm_minpuff and b2stbc_nesepm_maxpuff. It will apply fb_type=3, fb_rescale=1, fb_actuator=1 on region defined by solregno.
					nepedm_sol is similar to nesepm_sol but the feedback is exerted on the electron density at the top of the pedestal, along the outer midplane, at the icped-th ring (where icped=iyped+2) counting from the inner core boundary. It will apply fb_type=16, fb_rescale=1, fb_actuator=1 on region defined by solregno.
					ndes_sol is the total particle content from the isonuclear sequence of species 'isfeedback' over the entire simulation domain. It is governed, like nesepm_sol, by nesepm_overshoot and nesepm_alpha and corresponds to a SOL boundary feedback. Will apply fb_type=14, fb_rescale=1, fb_actuator=1 on region defined by solregno. WARNING: in the structured code this switch was asking for BCCON=12, so density BC for fluid neutrals feedback but then it switches to gas  puff for kinetic neutrals. Now it is ONLY gaspuff.
					volrec_sol is the total particle source due to volume recombination coming from Eirene. Its feedback is governed by volrec_overshoot and volrec_alpha and volrec_beta parameters (See Numerics section for the latter two). Will apply fb_type=15, fb_rescale=1, fb_actuator=1 on region defined by pfrregno1. WARNING: not available yet for fluid neutrals.
					nesepm_pfr is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the PFR region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the PFR South boundary indices pfrregno1 and pfrregno2). will apply fb_type=3, fb_rescale=1, fb_actuator=1 on region defined pfrregno1
					ndes is the total particle (neutrals + ions) content of the species whose neutral species has index isfeedback. This is controlled through particle input of neutrals species isfeedback through the	private flux boundaries (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2). will apply fb_type=14, fb_rescale=1, fb_actuator=1 on region defined by pfrregno1. WARNING: in the structured code this switch was asking for BCCON=12, so density BC for fluid neutrals feedback but then it switches to gas puff for kinetic neutrals. Now it is ONLY gas puff.
					private_flux_puff NOT YET CONVERTED TO WG CODE! is the particle flow of species isfeedback through the private flux region boundary. This is controlled through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2).
					All but the first of these feedback schemes ("nesepm") can also be run though an Eirene neutral gas puff. In that case, one should set an appropriate gas puffing stratum in the Eirene input file input.dat, as well as in the b2.neutrals.parameters file. The code will assume, unless told otherwise through the use of "eirene_nesepm_istra", that the first stratum of type 'C' found in b2.neutrals.parameters is the stratum used for the feedback. If "eirene_nesepm_istra" is set to a positive number, the code will consider the feedback stratum to be the stratum in the "eirene_nesepm_istra"-th position in b2.neutrals.parameters.
					b2stbc_iyped is the index in the OMP CV list (defined with RZOMP in b2.user.parameters) of the pedestal cell (defaults to icsepomp/2).
				""", '0.0'),
   
      'b2stbc_fhiycore' : ('', 'real', """
					The 20 switches above are all feedback switches and require that b2stbc_feedback.ne.0 (See Run section for details) or that lfeedback=.true. in b2.boundary.parameters. Feedback schemes are now all applied in the same way in a dedicated module b2us_feedback (see FEEDBACK_CONTROL namelist). Switches in b2mn.dat are still available and will override whatever is specified in b2.feedback_control.parameters, but it is recommended to not use switches anymore. This will allow more flexibility in applying such schemes.
					The feedback is done as a boundary condition and is under-relaxed using the b2stbc_...._alpha switches (See Numerics section for details).
					fheycore is the radial electron heat flow entering the core boundary.  Will apply fb_type=11, fb_rescale=1, fb_actuator=4 on region defined by coreregno.
					fhiycore is the radial ion heat flow entering the core boundary. Will apply fb_type=12, fb_rescale=1, fb_actuator=5 on region defined by coreregno.
					fchycore is the radial current entering the core boundary. Will apply fb_type=13, fb_rescale=1, fb_actuator=4 on region defined by coreregno.
					fnaycore is the radial flux of species "isfeedback" entering the core boundary. Will apply fb_type=10, fb_rescale=1, fb_actuator=3 on region defined by coreregno.
					If fhiycore_kinetic_energy.eq.1, the parallel kinetic energy flux is counted as part of the ion energy flux.
					For double-null cases, the f..ycore variables contain the total flow through both core boundaries taken together (to be checked for WG code!).
					The core boundaries are identified by the coreregno and coreregn2 switches (see Geometry section). These switches need to be manually adjusted for WG cases as now they indicate the boundary where the feedback is applied. For switches like b2stbc_xxxycore or private_gas\_puff the user has to specify in b2.feedback_control.parameters} where the feedback is calculated (see b2us.regions.parameters produced at conversion), while coreregno still indicates where it is applied. pfrregno and solregno lose meaning in kinetic cases if the actuator is the gas puff. Coreregn2 and pfrregno2 are not yet converted/used.
					The other seven switches are density feedback switches: nesepm is the outer midplane separatrix electron density. (See rzomp switch in b2.user.parameters for setting of midplane position). This is controlled through particle input of main plasma species isfeedback through the core boundary (See Geometry section for the core boundary indices coreregno and coreregn2).
					nesepm_sol is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the SOL region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the SOL North boundary (See Geometry section for the SOL North boundary index solregno). If nesepm_overshoot.gt.1.0, the gas puff is turned off when the midplane separatrix density reaches nesepm*nesepm_overshoot. Minimum and maximum values of the feedback gas puff can be set using b2stbc_nesepm_minpuff and b2stbc_nesepm_maxpuff. It will apply fb_type=3, fb_rescale=1, fb_actuator=1 on region defined by solregno.
					nepedm_sol is similar to nesepm_sol but the feedback is exerted on the electron density at the top of the pedestal, along the outer midplane, at the icped-th ring (where icped=iyped+2) counting from the inner core boundary. It will apply fb_type=16, fb_rescale=1, fb_actuator=1 on region defined by solregno.
					ndes_sol is the total particle content from the isonuclear sequence of species 'isfeedback' over the entire simulation domain. It is governed, like nesepm_sol, by nesepm_overshoot and nesepm_alpha and corresponds to a SOL boundary feedback. Will apply fb_type=14, fb_rescale=1, fb_actuator=1 on region defined by solregno. WARNING: in the structured code this switch was asking for BCCON=12, so density BC for fluid neutrals feedback but then it switches to gas  puff for kinetic neutrals. Now it is ONLY gaspuff.
					volrec_sol is the total particle source due to volume recombination coming from Eirene. Its feedback is governed by volrec_overshoot and volrec_alpha and volrec_beta parameters (See Numerics section for the latter two). Will apply fb_type=15, fb_rescale=1, fb_actuator=1 on region defined by pfrregno1. WARNING: not available yet for fluid neutrals.
					nesepm_pfr is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the PFR region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the PFR South boundary indices pfrregno1 and pfrregno2). will apply fb_type=3, fb_rescale=1, fb_actuator=1 on region defined pfrregno1
					ndes is the total particle (neutrals + ions) content of the species whose neutral species has index isfeedback. This is controlled through particle input of neutrals species isfeedback through the	private flux boundaries (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2). will apply fb_type=14, fb_rescale=1, fb_actuator=1 on region defined by pfrregno1. WARNING: in the structured code this switch was asking for BCCON=12, so density BC for fluid neutrals feedback but then it switches to gas puff for kinetic neutrals. Now it is ONLY gas puff.
					private_flux_puff NOT YET CONVERTED TO WG CODE! is the particle flow of species isfeedback through the private flux region boundary. This is controlled through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2).
					All but the first of these feedback schemes ("nesepm") can also be run though an Eirene neutral gas puff. In that case, one should set an appropriate gas puffing stratum in the Eirene input file input.dat, as well as in the b2.neutrals.parameters file. The code will assume, unless told otherwise through the use of "eirene_nesepm_istra", that the first stratum of type 'C' found in b2.neutrals.parameters is the stratum used for the feedback. If "eirene_nesepm_istra" is set to a positive number, the code will consider the feedback stratum to be the stratum in the "eirene_nesepm_istra"-th position in b2.neutrals.parameters.
					b2stbc_iyped is the index in the OMP CV list (defined with RZOMP in b2.user.parameters) of the pedestal cell (defaults to icsepomp/2).
				""", '0.0'),
   
      'b2stbc_fhiycore_kinetic_energy' : ('', 'integer', """
					The 20 switches above are all feedback switches and require that b2stbc_feedback.ne.0 (See Run section for details) or that lfeedback=.true. in b2.boundary.parameters. Feedback schemes are now all applied in the same way in a dedicated module b2us_feedback (see FEEDBACK_CONTROL namelist). Switches in b2mn.dat are still available and will override whatever is specified in b2.feedback_control.parameters, but it is recommended to not use switches anymore. This will allow more flexibility in applying such schemes.
					The feedback is done as a boundary condition and is under-relaxed using the b2stbc_...._alpha switches (See Numerics section for details).
					fheycore is the radial electron heat flow entering the core boundary.  Will apply fb_type=11, fb_rescale=1, fb_actuator=4 on region defined by coreregno.
					fhiycore is the radial ion heat flow entering the core boundary. Will apply fb_type=12, fb_rescale=1, fb_actuator=5 on region defined by coreregno.
					fchycore is the radial current entering the core boundary. Will apply fb_type=13, fb_rescale=1, fb_actuator=4 on region defined by coreregno.
					fnaycore is the radial flux of species "isfeedback" entering the core boundary. Will apply fb_type=10, fb_rescale=1, fb_actuator=3 on region defined by coreregno.
					If fhiycore_kinetic_energy.eq.1, the parallel kinetic energy flux is counted as part of the ion energy flux.
					For double-null cases, the f..ycore variables contain the total flow through both core boundaries taken together (to be checked for WG code!).
					The core boundaries are identified by the coreregno and coreregn2 switches (see Geometry section). These switches need to be manually adjusted for WG cases as now they indicate the boundary where the feedback is applied. For switches like b2stbc_xxxycore or private_gas\_puff the user has to specify in b2.feedback_control.parameters} where the feedback is calculated (see b2us.regions.parameters produced at conversion), while coreregno still indicates where it is applied. pfrregno and solregno lose meaning in kinetic cases if the actuator is the gas puff. Coreregn2 and pfrregno2 are not yet converted/used.
					The other seven switches are density feedback switches: nesepm is the outer midplane separatrix electron density. (See rzomp switch in b2.user.parameters for setting of midplane position). This is controlled through particle input of main plasma species isfeedback through the core boundary (See Geometry section for the core boundary indices coreregno and coreregn2).
					nesepm_sol is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the SOL region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the SOL North boundary (See Geometry section for the SOL North boundary index solregno). If nesepm_overshoot.gt.1.0, the gas puff is turned off when the midplane separatrix density reaches nesepm*nesepm_overshoot. Minimum and maximum values of the feedback gas puff can be set using b2stbc_nesepm_minpuff and b2stbc_nesepm_maxpuff. It will apply fb_type=3, fb_rescale=1, fb_actuator=1 on region defined by solregno.
					nepedm_sol is similar to nesepm_sol but the feedback is exerted on the electron density at the top of the pedestal, along the outer midplane, at the icped-th ring (where icped=iyped+2) counting from the inner core boundary. It will apply fb_type=16, fb_rescale=1, fb_actuator=1 on region defined by solregno.
					ndes_sol is the total particle content from the isonuclear sequence of species 'isfeedback' over the entire simulation domain. It is governed, like nesepm_sol, by nesepm_overshoot and nesepm_alpha and corresponds to a SOL boundary feedback. Will apply fb_type=14, fb_rescale=1, fb_actuator=1 on region defined by solregno. WARNING: in the structured code this switch was asking for BCCON=12, so density BC for fluid neutrals feedback but then it switches to gas  puff for kinetic neutrals. Now it is ONLY gaspuff.
					volrec_sol is the total particle source due to volume recombination coming from Eirene. Its feedback is governed by volrec_overshoot and volrec_alpha and volrec_beta parameters (See Numerics section for the latter two). Will apply fb_type=15, fb_rescale=1, fb_actuator=1 on region defined by pfrregno1. WARNING: not available yet for fluid neutrals.
					nesepm_pfr is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the PFR region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the PFR South boundary indices pfrregno1 and pfrregno2). will apply fb_type=3, fb_rescale=1, fb_actuator=1 on region defined pfrregno1
					ndes is the total particle (neutrals + ions) content of the species whose neutral species has index isfeedback. This is controlled through particle input of neutrals species isfeedback through the	private flux boundaries (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2). will apply fb_type=14, fb_rescale=1, fb_actuator=1 on region defined by pfrregno1. WARNING: in the structured code this switch was asking for BCCON=12, so density BC for fluid neutrals feedback but then it switches to gas puff for kinetic neutrals. Now it is ONLY gas puff.
					private_flux_puff NOT YET CONVERTED TO WG CODE! is the particle flow of species isfeedback through the private flux region boundary. This is controlled through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2).
					All but the first of these feedback schemes ("nesepm") can also be run though an Eirene neutral gas puff. In that case, one should set an appropriate gas puffing stratum in the Eirene input file input.dat, as well as in the b2.neutrals.parameters file. The code will assume, unless told otherwise through the use of "eirene_nesepm_istra", that the first stratum of type 'C' found in b2.neutrals.parameters is the stratum used for the feedback. If "eirene_nesepm_istra" is set to a positive number, the code will consider the feedback stratum to be the stratum in the "eirene_nesepm_istra"-th position in b2.neutrals.parameters.
					b2stbc_iyped is the index in the OMP CV list (defined with RZOMP in b2.user.parameters) of the pedestal cell (defaults to icsepomp/2).
				""", '0'),
   
      'b2stbc_fchycore' : ('', 'real', """
					The 20 switches above are all feedback switches and require that b2stbc_feedback.ne.0 (See Run section for details) or that lfeedback=.true. in b2.boundary.parameters. Feedback schemes are now all applied in the same way in a dedicated module b2us_feedback (see FEEDBACK_CONTROL namelist). Switches in b2mn.dat are still available and will override whatever is specified in b2.feedback_control.parameters, but it is recommended to not use switches anymore. This will allow more flexibility in applying such schemes.
					The feedback is done as a boundary condition and is under-relaxed using the b2stbc_...._alpha switches (See Numerics section for details).
					fheycore is the radial electron heat flow entering the core boundary.  Will apply fb_type=11, fb_rescale=1, fb_actuator=4 on region defined by coreregno.
					fhiycore is the radial ion heat flow entering the core boundary. Will apply fb_type=12, fb_rescale=1, fb_actuator=5 on region defined by coreregno.
					fchycore is the radial current entering the core boundary. Will apply fb_type=13, fb_rescale=1, fb_actuator=4 on region defined by coreregno.
					fnaycore is the radial flux of species "isfeedback" entering the core boundary. Will apply fb_type=10, fb_rescale=1, fb_actuator=3 on region defined by coreregno.
					If fhiycore_kinetic_energy.eq.1, the parallel kinetic energy flux is counted as part of the ion energy flux.
					For double-null cases, the f..ycore variables contain the total flow through both core boundaries taken together (to be checked for WG code!).
					The core boundaries are identified by the coreregno and coreregn2 switches (see Geometry section). These switches need to be manually adjusted for WG cases as now they indicate the boundary where the feedback is applied. For switches like b2stbc_xxxycore or private_gas\_puff the user has to specify in b2.feedback_control.parameters} where the feedback is calculated (see b2us.regions.parameters produced at conversion), while coreregno still indicates where it is applied. pfrregno and solregno lose meaning in kinetic cases if the actuator is the gas puff. Coreregn2 and pfrregno2 are not yet converted/used.
					The other seven switches are density feedback switches: nesepm is the outer midplane separatrix electron density. (See rzomp switch in b2.user.parameters for setting of midplane position). This is controlled through particle input of main plasma species isfeedback through the core boundary (See Geometry section for the core boundary indices coreregno and coreregn2).
					nesepm_sol is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the SOL region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the SOL North boundary (See Geometry section for the SOL North boundary index solregno). If nesepm_overshoot.gt.1.0, the gas puff is turned off when the midplane separatrix density reaches nesepm*nesepm_overshoot. Minimum and maximum values of the feedback gas puff can be set using b2stbc_nesepm_minpuff and b2stbc_nesepm_maxpuff. It will apply fb_type=3, fb_rescale=1, fb_actuator=1 on region defined by solregno.
					nepedm_sol is similar to nesepm_sol but the feedback is exerted on the electron density at the top of the pedestal, along the outer midplane, at the icped-th ring (where icped=iyped+2) counting from the inner core boundary. It will apply fb_type=16, fb_rescale=1, fb_actuator=1 on region defined by solregno.
					ndes_sol is the total particle content from the isonuclear sequence of species 'isfeedback' over the entire simulation domain. It is governed, like nesepm_sol, by nesepm_overshoot and nesepm_alpha and corresponds to a SOL boundary feedback. Will apply fb_type=14, fb_rescale=1, fb_actuator=1 on region defined by solregno. WARNING: in the structured code this switch was asking for BCCON=12, so density BC for fluid neutrals feedback but then it switches to gas  puff for kinetic neutrals. Now it is ONLY gaspuff.
					volrec_sol is the total particle source due to volume recombination coming from Eirene. Its feedback is governed by volrec_overshoot and volrec_alpha and volrec_beta parameters (See Numerics section for the latter two). Will apply fb_type=15, fb_rescale=1, fb_actuator=1 on region defined by pfrregno1. WARNING: not available yet for fluid neutrals.
					nesepm_pfr is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the PFR region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the PFR South boundary indices pfrregno1 and pfrregno2). will apply fb_type=3, fb_rescale=1, fb_actuator=1 on region defined pfrregno1
					ndes is the total particle (neutrals + ions) content of the species whose neutral species has index isfeedback. This is controlled through particle input of neutrals species isfeedback through the	private flux boundaries (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2). will apply fb_type=14, fb_rescale=1, fb_actuator=1 on region defined by pfrregno1. WARNING: in the structured code this switch was asking for BCCON=12, so density BC for fluid neutrals feedback but then it switches to gas puff for kinetic neutrals. Now it is ONLY gas puff.
					private_flux_puff NOT YET CONVERTED TO WG CODE! is the particle flow of species isfeedback through the private flux region boundary. This is controlled through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2).
					All but the first of these feedback schemes ("nesepm") can also be run though an Eirene neutral gas puff. In that case, one should set an appropriate gas puffing stratum in the Eirene input file input.dat, as well as in the b2.neutrals.parameters file. The code will assume, unless told otherwise through the use of "eirene_nesepm_istra", that the first stratum of type 'C' found in b2.neutrals.parameters is the stratum used for the feedback. If "eirene_nesepm_istra" is set to a positive number, the code will consider the feedback stratum to be the stratum in the "eirene_nesepm_istra"-th position in b2.neutrals.parameters.
					b2stbc_iyped is the index in the OMP CV list (defined with RZOMP in b2.user.parameters) of the pedestal cell (defaults to icsepomp/2).
				""", '-1.0e30'),
   
      'b2stbc_fnaycore' : ('', 'real', """
					The 20 switches above are all feedback switches and require that b2stbc_feedback.ne.0 (See Run section for details) or that lfeedback=.true. in b2.boundary.parameters. Feedback schemes are now all applied in the same way in a dedicated module b2us_feedback (see FEEDBACK_CONTROL namelist). Switches in b2mn.dat are still available and will override whatever is specified in b2.feedback_control.parameters, but it is recommended to not use switches anymore. This will allow more flexibility in applying such schemes.
					The feedback is done as a boundary condition and is under-relaxed using the b2stbc_...._alpha switches (See Numerics section for details).
					fheycore is the radial electron heat flow entering the core boundary.  Will apply fb_type=11, fb_rescale=1, fb_actuator=4 on region defined by coreregno.
					fhiycore is the radial ion heat flow entering the core boundary. Will apply fb_type=12, fb_rescale=1, fb_actuator=5 on region defined by coreregno.
					fchycore is the radial current entering the core boundary. Will apply fb_type=13, fb_rescale=1, fb_actuator=4 on region defined by coreregno.
					fnaycore is the radial flux of species "isfeedback" entering the core boundary. Will apply fb_type=10, fb_rescale=1, fb_actuator=3 on region defined by coreregno.
					If fhiycore_kinetic_energy.eq.1, the parallel kinetic energy flux is counted as part of the ion energy flux.
					For double-null cases, the f..ycore variables contain the total flow through both core boundaries taken together (to be checked for WG code!).
					The core boundaries are identified by the coreregno and coreregn2 switches (see Geometry section). These switches need to be manually adjusted for WG cases as now they indicate the boundary where the feedback is applied. For switches like b2stbc_xxxycore or private_gas\_puff the user has to specify in b2.feedback_control.parameters} where the feedback is calculated (see b2us.regions.parameters produced at conversion), while coreregno still indicates where it is applied. pfrregno and solregno lose meaning in kinetic cases if the actuator is the gas puff. Coreregn2 and pfrregno2 are not yet converted/used.
					The other seven switches are density feedback switches: nesepm is the outer midplane separatrix electron density. (See rzomp switch in b2.user.parameters for setting of midplane position). This is controlled through particle input of main plasma species isfeedback through the core boundary (See Geometry section for the core boundary indices coreregno and coreregn2).
					nesepm_sol is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the SOL region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the SOL North boundary (See Geometry section for the SOL North boundary index solregno). If nesepm_overshoot.gt.1.0, the gas puff is turned off when the midplane separatrix density reaches nesepm*nesepm_overshoot. Minimum and maximum values of the feedback gas puff can be set using b2stbc_nesepm_minpuff and b2stbc_nesepm_maxpuff. It will apply fb_type=3, fb_rescale=1, fb_actuator=1 on region defined by solregno.
					nepedm_sol is similar to nesepm_sol but the feedback is exerted on the electron density at the top of the pedestal, along the outer midplane, at the icped-th ring (where icped=iyped+2) counting from the inner core boundary. It will apply fb_type=16, fb_rescale=1, fb_actuator=1 on region defined by solregno.
					ndes_sol is the total particle content from the isonuclear sequence of species 'isfeedback' over the entire simulation domain. It is governed, like nesepm_sol, by nesepm_overshoot and nesepm_alpha and corresponds to a SOL boundary feedback. Will apply fb_type=14, fb_rescale=1, fb_actuator=1 on region defined by solregno. WARNING: in the structured code this switch was asking for BCCON=12, so density BC for fluid neutrals feedback but then it switches to gas  puff for kinetic neutrals. Now it is ONLY gaspuff.
					volrec_sol is the total particle source due to volume recombination coming from Eirene. Its feedback is governed by volrec_overshoot and volrec_alpha and volrec_beta parameters (See Numerics section for the latter two). Will apply fb_type=15, fb_rescale=1, fb_actuator=1 on region defined by pfrregno1. WARNING: not available yet for fluid neutrals.
					nesepm_pfr is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the PFR region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the PFR South boundary indices pfrregno1 and pfrregno2). will apply fb_type=3, fb_rescale=1, fb_actuator=1 on region defined pfrregno1
					ndes is the total particle (neutrals + ions) content of the species whose neutral species has index isfeedback. This is controlled through particle input of neutrals species isfeedback through the	private flux boundaries (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2). will apply fb_type=14, fb_rescale=1, fb_actuator=1 on region defined by pfrregno1. WARNING: in the structured code this switch was asking for BCCON=12, so density BC for fluid neutrals feedback but then it switches to gas puff for kinetic neutrals. Now it is ONLY gas puff.
					private_flux_puff NOT YET CONVERTED TO WG CODE! is the particle flow of species isfeedback through the private flux region boundary. This is controlled through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2).
					All but the first of these feedback schemes ("nesepm") can also be run though an Eirene neutral gas puff. In that case, one should set an appropriate gas puffing stratum in the Eirene input file input.dat, as well as in the b2.neutrals.parameters file. The code will assume, unless told otherwise through the use of "eirene_nesepm_istra", that the first stratum of type 'C' found in b2.neutrals.parameters is the stratum used for the feedback. If "eirene_nesepm_istra" is set to a positive number, the code will consider the feedback stratum to be the stratum in the "eirene_nesepm_istra"-th position in b2.neutrals.parameters.
					b2stbc_iyped is the index in the OMP CV list (defined with RZOMP in b2.user.parameters) of the pedestal cell (defaults to icsepomp/2).
				""", '-1.0e30'),
   
      'b2stbc_isfeedback' : ('', 'integer', """
					The 20 switches above are all feedback switches and require that b2stbc_feedback.ne.0 (See Run section for details) or that lfeedback=.true. in b2.boundary.parameters. Feedback schemes are now all applied in the same way in a dedicated module b2us_feedback (see FEEDBACK_CONTROL namelist). Switches in b2mn.dat are still available and will override whatever is specified in b2.feedback_control.parameters, but it is recommended to not use switches anymore. This will allow more flexibility in applying such schemes.
					The feedback is done as a boundary condition and is under-relaxed using the b2stbc_...._alpha switches (See Numerics section for details).
					fheycore is the radial electron heat flow entering the core boundary.  Will apply fb_type=11, fb_rescale=1, fb_actuator=4 on region defined by coreregno.
					fhiycore is the radial ion heat flow entering the core boundary. Will apply fb_type=12, fb_rescale=1, fb_actuator=5 on region defined by coreregno.
					fchycore is the radial current entering the core boundary. Will apply fb_type=13, fb_rescale=1, fb_actuator=4 on region defined by coreregno.
					fnaycore is the radial flux of species "isfeedback" entering the core boundary. Will apply fb_type=10, fb_rescale=1, fb_actuator=3 on region defined by coreregno.
					If fhiycore_kinetic_energy.eq.1, the parallel kinetic energy flux is counted as part of the ion energy flux.
					For double-null cases, the f..ycore variables contain the total flow through both core boundaries taken together (to be checked for WG code!).
					The core boundaries are identified by the coreregno and coreregn2 switches (see Geometry section). These switches need to be manually adjusted for WG cases as now they indicate the boundary where the feedback is applied. For switches like b2stbc_xxxycore or private_gas\_puff the user has to specify in b2.feedback_control.parameters} where the feedback is calculated (see b2us.regions.parameters produced at conversion), while coreregno still indicates where it is applied. pfrregno and solregno lose meaning in kinetic cases if the actuator is the gas puff. Coreregn2 and pfrregno2 are not yet converted/used.
					The other seven switches are density feedback switches: nesepm is the outer midplane separatrix electron density. (See rzomp switch in b2.user.parameters for setting of midplane position). This is controlled through particle input of main plasma species isfeedback through the core boundary (See Geometry section for the core boundary indices coreregno and coreregn2).
					nesepm_sol is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the SOL region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the SOL North boundary (See Geometry section for the SOL North boundary index solregno). If nesepm_overshoot.gt.1.0, the gas puff is turned off when the midplane separatrix density reaches nesepm*nesepm_overshoot. Minimum and maximum values of the feedback gas puff can be set using b2stbc_nesepm_minpuff and b2stbc_nesepm_maxpuff. It will apply fb_type=3, fb_rescale=1, fb_actuator=1 on region defined by solregno.
					nepedm_sol is similar to nesepm_sol but the feedback is exerted on the electron density at the top of the pedestal, along the outer midplane, at the icped-th ring (where icped=iyped+2) counting from the inner core boundary. It will apply fb_type=16, fb_rescale=1, fb_actuator=1 on region defined by solregno.
					ndes_sol is the total particle content from the isonuclear sequence of species 'isfeedback' over the entire simulation domain. It is governed, like nesepm_sol, by nesepm_overshoot and nesepm_alpha and corresponds to a SOL boundary feedback. Will apply fb_type=14, fb_rescale=1, fb_actuator=1 on region defined by solregno. WARNING: in the structured code this switch was asking for BCCON=12, so density BC for fluid neutrals feedback but then it switches to gas  puff for kinetic neutrals. Now it is ONLY gaspuff.
					volrec_sol is the total particle source due to volume recombination coming from Eirene. Its feedback is governed by volrec_overshoot and volrec_alpha and volrec_beta parameters (See Numerics section for the latter two). Will apply fb_type=15, fb_rescale=1, fb_actuator=1 on region defined by pfrregno1. WARNING: not available yet for fluid neutrals.
					nesepm_pfr is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the PFR region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the PFR South boundary indices pfrregno1 and pfrregno2). will apply fb_type=3, fb_rescale=1, fb_actuator=1 on region defined pfrregno1
					ndes is the total particle (neutrals + ions) content of the species whose neutral species has index isfeedback. This is controlled through particle input of neutrals species isfeedback through the	private flux boundaries (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2). will apply fb_type=14, fb_rescale=1, fb_actuator=1 on region defined by pfrregno1. WARNING: in the structured code this switch was asking for BCCON=12, so density BC for fluid neutrals feedback but then it switches to gas puff for kinetic neutrals. Now it is ONLY gas puff.
					private_flux_puff NOT YET CONVERTED TO WG CODE! is the particle flow of species isfeedback through the private flux region boundary. This is controlled through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2).
					All but the first of these feedback schemes ("nesepm") can also be run though an Eirene neutral gas puff. In that case, one should set an appropriate gas puffing stratum in the Eirene input file input.dat, as well as in the b2.neutrals.parameters file. The code will assume, unless told otherwise through the use of "eirene_nesepm_istra", that the first stratum of type 'C' found in b2.neutrals.parameters is the stratum used for the feedback. If "eirene_nesepm_istra" is set to a positive number, the code will consider the feedback stratum to be the stratum in the "eirene_nesepm_istra"-th position in b2.neutrals.parameters.
					b2stbc_iyped is the index in the OMP CV list (defined with RZOMP in b2.user.parameters) of the pedestal cell (defaults to icsepomp/2).
				""", '0'),
   
      'b2stbc_iyped' : ('', 'real', """
					The 20 switches above are all feedback switches and require that b2stbc_feedback.ne.0 (See Run section for details) or that lfeedback=.true. in b2.boundary.parameters. Feedback schemes are now all applied in the same way in a dedicated module b2us_feedback (see FEEDBACK_CONTROL namelist). Switches in b2mn.dat are still available and will override whatever is specified in b2.feedback_control.parameters, but it is recommended to not use switches anymore. This will allow more flexibility in applying such schemes.
					The feedback is done as a boundary condition and is under-relaxed using the b2stbc_...._alpha switches (See Numerics section for details).
					fheycore is the radial electron heat flow entering the core boundary.  Will apply fb_type=11, fb_rescale=1, fb_actuator=4 on region defined by coreregno.
					fhiycore is the radial ion heat flow entering the core boundary. Will apply fb_type=12, fb_rescale=1, fb_actuator=5 on region defined by coreregno.
					fchycore is the radial current entering the core boundary. Will apply fb_type=13, fb_rescale=1, fb_actuator=4 on region defined by coreregno.
					fnaycore is the radial flux of species "isfeedback" entering the core boundary. Will apply fb_type=10, fb_rescale=1, fb_actuator=3 on region defined by coreregno.
					If fhiycore_kinetic_energy.eq.1, the parallel kinetic energy flux is counted as part of the ion energy flux.
					For double-null cases, the f..ycore variables contain the total flow through both core boundaries taken together (to be checked for WG code!).
					The core boundaries are identified by the coreregno and coreregn2 switches (see Geometry section). These switches need to be manually adjusted for WG cases as now they indicate the boundary where the feedback is applied. For switches like b2stbc_xxxycore or private_gas\_puff the user has to specify in b2.feedback_control.parameters} where the feedback is calculated (see b2us.regions.parameters produced at conversion), while coreregno still indicates where it is applied. pfrregno and solregno lose meaning in kinetic cases if the actuator is the gas puff. Coreregn2 and pfrregno2 are not yet converted/used.
					The other seven switches are density feedback switches: nesepm is the outer midplane separatrix electron density. (See rzomp switch in b2.user.parameters for setting of midplane position). This is controlled through particle input of main plasma species isfeedback through the core boundary (See Geometry section for the core boundary indices coreregno and coreregn2).
					nesepm_sol is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the SOL region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the SOL North boundary (See Geometry section for the SOL North boundary index solregno). If nesepm_overshoot.gt.1.0, the gas puff is turned off when the midplane separatrix density reaches nesepm*nesepm_overshoot. Minimum and maximum values of the feedback gas puff can be set using b2stbc_nesepm_minpuff and b2stbc_nesepm_maxpuff. It will apply fb_type=3, fb_rescale=1, fb_actuator=1 on region defined by solregno.
					nepedm_sol is similar to nesepm_sol but the feedback is exerted on the electron density at the top of the pedestal, along the outer midplane, at the icped-th ring (where icped=iyped+2) counting from the inner core boundary. It will apply fb_type=16, fb_rescale=1, fb_actuator=1 on region defined by solregno.
					ndes_sol is the total particle content from the isonuclear sequence of species 'isfeedback' over the entire simulation domain. It is governed, like nesepm_sol, by nesepm_overshoot and nesepm_alpha and corresponds to a SOL boundary feedback. Will apply fb_type=14, fb_rescale=1, fb_actuator=1 on region defined by solregno. WARNING: in the structured code this switch was asking for BCCON=12, so density BC for fluid neutrals feedback but then it switches to gas  puff for kinetic neutrals. Now it is ONLY gaspuff.
					volrec_sol is the total particle source due to volume recombination coming from Eirene. Its feedback is governed by volrec_overshoot and volrec_alpha and volrec_beta parameters (See Numerics section for the latter two). Will apply fb_type=15, fb_rescale=1, fb_actuator=1 on region defined by pfrregno1. WARNING: not available yet for fluid neutrals.
					nesepm_pfr is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the PFR region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the PFR South boundary indices pfrregno1 and pfrregno2). will apply fb_type=3, fb_rescale=1, fb_actuator=1 on region defined pfrregno1
					ndes is the total particle (neutrals + ions) content of the species whose neutral species has index isfeedback. This is controlled through particle input of neutrals species isfeedback through the	private flux boundaries (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2). will apply fb_type=14, fb_rescale=1, fb_actuator=1 on region defined by pfrregno1. WARNING: in the structured code this switch was asking for BCCON=12, so density BC for fluid neutrals feedback but then it switches to gas puff for kinetic neutrals. Now it is ONLY gas puff.
					private_flux_puff NOT YET CONVERTED TO WG CODE! is the particle flow of species isfeedback through the private flux region boundary. This is controlled through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2).
					All but the first of these feedback schemes ("nesepm") can also be run though an Eirene neutral gas puff. In that case, one should set an appropriate gas puffing stratum in the Eirene input file input.dat, as well as in the b2.neutrals.parameters file. The code will assume, unless told otherwise through the use of "eirene_nesepm_istra", that the first stratum of type 'C' found in b2.neutrals.parameters is the stratum used for the feedback. If "eirene_nesepm_istra" is set to a positive number, the code will consider the feedback stratum to be the stratum in the "eirene_nesepm_istra"-th position in b2.neutrals.parameters.
					b2stbc_iyped is the index in the OMP CV list (defined with RZOMP in b2.user.parameters) of the pedestal cell (defaults to icsepomp/2).
				""", 'jsep/2'),
   
      'b2stbc_ndes' : ('', 'real', """
					The 20 switches above are all feedback switches and require that b2stbc_feedback.ne.0 (See Run section for details) or that lfeedback=.true. in b2.boundary.parameters. Feedback schemes are now all applied in the same way in a dedicated module b2us_feedback (see FEEDBACK_CONTROL namelist). Switches in b2mn.dat are still available and will override whatever is specified in b2.feedback_control.parameters, but it is recommended to not use switches anymore. This will allow more flexibility in applying such schemes.
					The feedback is done as a boundary condition and is under-relaxed using the b2stbc_...._alpha switches (See Numerics section for details).
					fheycore is the radial electron heat flow entering the core boundary.  Will apply fb_type=11, fb_rescale=1, fb_actuator=4 on region defined by coreregno.
					fhiycore is the radial ion heat flow entering the core boundary. Will apply fb_type=12, fb_rescale=1, fb_actuator=5 on region defined by coreregno.
					fchycore is the radial current entering the core boundary. Will apply fb_type=13, fb_rescale=1, fb_actuator=4 on region defined by coreregno.
					fnaycore is the radial flux of species "isfeedback" entering the core boundary. Will apply fb_type=10, fb_rescale=1, fb_actuator=3 on region defined by coreregno.
					If fhiycore_kinetic_energy.eq.1, the parallel kinetic energy flux is counted as part of the ion energy flux.
					For double-null cases, the f..ycore variables contain the total flow through both core boundaries taken together (to be checked for WG code!).
					The core boundaries are identified by the coreregno and coreregn2 switches (see Geometry section). These switches need to be manually adjusted for WG cases as now they indicate the boundary where the feedback is applied. For switches like b2stbc_xxxycore or private_gas\_puff the user has to specify in b2.feedback_control.parameters} where the feedback is calculated (see b2us.regions.parameters produced at conversion), while coreregno still indicates where it is applied. pfrregno and solregno lose meaning in kinetic cases if the actuator is the gas puff. Coreregn2 and pfrregno2 are not yet converted/used.
					The other seven switches are density feedback switches: nesepm is the outer midplane separatrix electron density. (See rzomp switch in b2.user.parameters for setting of midplane position). This is controlled through particle input of main plasma species isfeedback through the core boundary (See Geometry section for the core boundary indices coreregno and coreregn2).
					nesepm_sol is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the SOL region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the SOL North boundary (See Geometry section for the SOL North boundary index solregno). If nesepm_overshoot.gt.1.0, the gas puff is turned off when the midplane separatrix density reaches nesepm*nesepm_overshoot. Minimum and maximum values of the feedback gas puff can be set using b2stbc_nesepm_minpuff and b2stbc_nesepm_maxpuff. It will apply fb_type=3, fb_rescale=1, fb_actuator=1 on region defined by solregno.
					nepedm_sol is similar to nesepm_sol but the feedback is exerted on the electron density at the top of the pedestal, along the outer midplane, at the icped-th ring (where icped=iyped+2) counting from the inner core boundary. It will apply fb_type=16, fb_rescale=1, fb_actuator=1 on region defined by solregno.
					ndes_sol is the total particle content from the isonuclear sequence of species 'isfeedback' over the entire simulation domain. It is governed, like nesepm_sol, by nesepm_overshoot and nesepm_alpha and corresponds to a SOL boundary feedback. Will apply fb_type=14, fb_rescale=1, fb_actuator=1 on region defined by solregno. WARNING: in the structured code this switch was asking for BCCON=12, so density BC for fluid neutrals feedback but then it switches to gas  puff for kinetic neutrals. Now it is ONLY gaspuff.
					volrec_sol is the total particle source due to volume recombination coming from Eirene. Its feedback is governed by volrec_overshoot and volrec_alpha and volrec_beta parameters (See Numerics section for the latter two). Will apply fb_type=15, fb_rescale=1, fb_actuator=1 on region defined by pfrregno1. WARNING: not available yet for fluid neutrals.
					nesepm_pfr is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the PFR region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the PFR South boundary indices pfrregno1 and pfrregno2). will apply fb_type=3, fb_rescale=1, fb_actuator=1 on region defined pfrregno1
					ndes is the total particle (neutrals + ions) content of the species whose neutral species has index isfeedback. This is controlled through particle input of neutrals species isfeedback through the	private flux boundaries (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2). will apply fb_type=14, fb_rescale=1, fb_actuator=1 on region defined by pfrregno1. WARNING: in the structured code this switch was asking for BCCON=12, so density BC for fluid neutrals feedback but then it switches to gas puff for kinetic neutrals. Now it is ONLY gas puff.
					private_flux_puff NOT YET CONVERTED TO WG CODE! is the particle flow of species isfeedback through the private flux region boundary. This is controlled through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2).
					All but the first of these feedback schemes ("nesepm") can also be run though an Eirene neutral gas puff. In that case, one should set an appropriate gas puffing stratum in the Eirene input file input.dat, as well as in the b2.neutrals.parameters file. The code will assume, unless told otherwise through the use of "eirene_nesepm_istra", that the first stratum of type 'C' found in b2.neutrals.parameters is the stratum used for the feedback. If "eirene_nesepm_istra" is set to a positive number, the code will consider the feedback stratum to be the stratum in the "eirene_nesepm_istra"-th position in b2.neutrals.parameters.
					b2stbc_iyped is the index in the OMP CV list (defined with RZOMP in b2.user.parameters) of the pedestal cell (defaults to icsepomp/2).
				""", '0.0'),
   
      'b2stbc_ndes_sol' : ('', 'real', """
					The 20 switches above are all feedback switches and require that b2stbc_feedback.ne.0 (See Run section for details) or that lfeedback=.true. in b2.boundary.parameters. Feedback schemes are now all applied in the same way in a dedicated module b2us_feedback (see FEEDBACK_CONTROL namelist). Switches in b2mn.dat are still available and will override whatever is specified in b2.feedback_control.parameters, but it is recommended to not use switches anymore. This will allow more flexibility in applying such schemes.
					The feedback is done as a boundary condition and is under-relaxed using the b2stbc_...._alpha switches (See Numerics section for details).
					fheycore is the radial electron heat flow entering the core boundary.  Will apply fb_type=11, fb_rescale=1, fb_actuator=4 on region defined by coreregno.
					fhiycore is the radial ion heat flow entering the core boundary. Will apply fb_type=12, fb_rescale=1, fb_actuator=5 on region defined by coreregno.
					fchycore is the radial current entering the core boundary. Will apply fb_type=13, fb_rescale=1, fb_actuator=4 on region defined by coreregno.
					fnaycore is the radial flux of species "isfeedback" entering the core boundary. Will apply fb_type=10, fb_rescale=1, fb_actuator=3 on region defined by coreregno.
					If fhiycore_kinetic_energy.eq.1, the parallel kinetic energy flux is counted as part of the ion energy flux.
					For double-null cases, the f..ycore variables contain the total flow through both core boundaries taken together (to be checked for WG code!).
					The core boundaries are identified by the coreregno and coreregn2 switches (see Geometry section). These switches need to be manually adjusted for WG cases as now they indicate the boundary where the feedback is applied. For switches like b2stbc_xxxycore or private_gas\_puff the user has to specify in b2.feedback_control.parameters} where the feedback is calculated (see b2us.regions.parameters produced at conversion), while coreregno still indicates where it is applied. pfrregno and solregno lose meaning in kinetic cases if the actuator is the gas puff. Coreregn2 and pfrregno2 are not yet converted/used.
					The other seven switches are density feedback switches: nesepm is the outer midplane separatrix electron density. (See rzomp switch in b2.user.parameters for setting of midplane position). This is controlled through particle input of main plasma species isfeedback through the core boundary (See Geometry section for the core boundary indices coreregno and coreregn2).
					nesepm_sol is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the SOL region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the SOL North boundary (See Geometry section for the SOL North boundary index solregno). If nesepm_overshoot.gt.1.0, the gas puff is turned off when the midplane separatrix density reaches nesepm*nesepm_overshoot. Minimum and maximum values of the feedback gas puff can be set using b2stbc_nesepm_minpuff and b2stbc_nesepm_maxpuff. It will apply fb_type=3, fb_rescale=1, fb_actuator=1 on region defined by solregno.
					nepedm_sol is similar to nesepm_sol but the feedback is exerted on the electron density at the top of the pedestal, along the outer midplane, at the icped-th ring (where icped=iyped+2) counting from the inner core boundary. It will apply fb_type=16, fb_rescale=1, fb_actuator=1 on region defined by solregno.
					ndes_sol is the total particle content from the isonuclear sequence of species 'isfeedback' over the entire simulation domain. It is governed, like nesepm_sol, by nesepm_overshoot and nesepm_alpha and corresponds to a SOL boundary feedback. Will apply fb_type=14, fb_rescale=1, fb_actuator=1 on region defined by solregno. WARNING: in the structured code this switch was asking for BCCON=12, so density BC for fluid neutrals feedback but then it switches to gas  puff for kinetic neutrals. Now it is ONLY gaspuff.
					volrec_sol is the total particle source due to volume recombination coming from Eirene. Its feedback is governed by volrec_overshoot and volrec_alpha and volrec_beta parameters (See Numerics section for the latter two). Will apply fb_type=15, fb_rescale=1, fb_actuator=1 on region defined by pfrregno1. WARNING: not available yet for fluid neutrals.
					nesepm_pfr is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the PFR region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the PFR South boundary indices pfrregno1 and pfrregno2). will apply fb_type=3, fb_rescale=1, fb_actuator=1 on region defined pfrregno1
					ndes is the total particle (neutrals + ions) content of the species whose neutral species has index isfeedback. This is controlled through particle input of neutrals species isfeedback through the	private flux boundaries (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2). will apply fb_type=14, fb_rescale=1, fb_actuator=1 on region defined by pfrregno1. WARNING: in the structured code this switch was asking for BCCON=12, so density BC for fluid neutrals feedback but then it switches to gas puff for kinetic neutrals. Now it is ONLY gas puff.
					private_flux_puff NOT YET CONVERTED TO WG CODE! is the particle flow of species isfeedback through the private flux region boundary. This is controlled through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2).
					All but the first of these feedback schemes ("nesepm") can also be run though an Eirene neutral gas puff. In that case, one should set an appropriate gas puffing stratum in the Eirene input file input.dat, as well as in the b2.neutrals.parameters file. The code will assume, unless told otherwise through the use of "eirene_nesepm_istra", that the first stratum of type 'C' found in b2.neutrals.parameters is the stratum used for the feedback. If "eirene_nesepm_istra" is set to a positive number, the code will consider the feedback stratum to be the stratum in the "eirene_nesepm_istra"-th position in b2.neutrals.parameters.
					b2stbc_iyped is the index in the OMP CV list (defined with RZOMP in b2.user.parameters) of the pedestal cell (defaults to icsepomp/2).
				""", '0.0'),
   
      'b2stbc_nepedm_sol' : ('', 'real', """
					The 20 switches above are all feedback switches and require that b2stbc_feedback.ne.0 (See Run section for details) or that lfeedback=.true. in b2.boundary.parameters. Feedback schemes are now all applied in the same way in a dedicated module b2us_feedback (see FEEDBACK_CONTROL namelist). Switches in b2mn.dat are still available and will override whatever is specified in b2.feedback_control.parameters, but it is recommended to not use switches anymore. This will allow more flexibility in applying such schemes.
					The feedback is done as a boundary condition and is under-relaxed using the b2stbc_...._alpha switches (See Numerics section for details).
					fheycore is the radial electron heat flow entering the core boundary.  Will apply fb_type=11, fb_rescale=1, fb_actuator=4 on region defined by coreregno.
					fhiycore is the radial ion heat flow entering the core boundary. Will apply fb_type=12, fb_rescale=1, fb_actuator=5 on region defined by coreregno.
					fchycore is the radial current entering the core boundary. Will apply fb_type=13, fb_rescale=1, fb_actuator=4 on region defined by coreregno.
					fnaycore is the radial flux of species "isfeedback" entering the core boundary. Will apply fb_type=10, fb_rescale=1, fb_actuator=3 on region defined by coreregno.
					If fhiycore_kinetic_energy.eq.1, the parallel kinetic energy flux is counted as part of the ion energy flux.
					For double-null cases, the f..ycore variables contain the total flow through both core boundaries taken together (to be checked for WG code!).
					The core boundaries are identified by the coreregno and coreregn2 switches (see Geometry section). These switches need to be manually adjusted for WG cases as now they indicate the boundary where the feedback is applied. For switches like b2stbc_xxxycore or private_gas\_puff the user has to specify in b2.feedback_control.parameters} where the feedback is calculated (see b2us.regions.parameters produced at conversion), while coreregno still indicates where it is applied. pfrregno and solregno lose meaning in kinetic cases if the actuator is the gas puff. Coreregn2 and pfrregno2 are not yet converted/used.
					The other seven switches are density feedback switches: nesepm is the outer midplane separatrix electron density. (See rzomp switch in b2.user.parameters for setting of midplane position). This is controlled through particle input of main plasma species isfeedback through the core boundary (See Geometry section for the core boundary indices coreregno and coreregn2).
					nesepm_sol is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the SOL region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the SOL North boundary (See Geometry section for the SOL North boundary index solregno). If nesepm_overshoot.gt.1.0, the gas puff is turned off when the midplane separatrix density reaches nesepm*nesepm_overshoot. Minimum and maximum values of the feedback gas puff can be set using b2stbc_nesepm_minpuff and b2stbc_nesepm_maxpuff. It will apply fb_type=3, fb_rescale=1, fb_actuator=1 on region defined by solregno.
					nepedm_sol is similar to nesepm_sol but the feedback is exerted on the electron density at the top of the pedestal, along the outer midplane, at the icped-th ring (where icped=iyped+2) counting from the inner core boundary. It will apply fb_type=16, fb_rescale=1, fb_actuator=1 on region defined by solregno.
					ndes_sol is the total particle content from the isonuclear sequence of species 'isfeedback' over the entire simulation domain. It is governed, like nesepm_sol, by nesepm_overshoot and nesepm_alpha and corresponds to a SOL boundary feedback. Will apply fb_type=14, fb_rescale=1, fb_actuator=1 on region defined by solregno. WARNING: in the structured code this switch was asking for BCCON=12, so density BC for fluid neutrals feedback but then it switches to gas  puff for kinetic neutrals. Now it is ONLY gaspuff.
					volrec_sol is the total particle source due to volume recombination coming from Eirene. Its feedback is governed by volrec_overshoot and volrec_alpha and volrec_beta parameters (See Numerics section for the latter two). Will apply fb_type=15, fb_rescale=1, fb_actuator=1 on region defined by pfrregno1. WARNING: not available yet for fluid neutrals.
					nesepm_pfr is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the PFR region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the PFR South boundary indices pfrregno1 and pfrregno2). will apply fb_type=3, fb_rescale=1, fb_actuator=1 on region defined pfrregno1
					ndes is the total particle (neutrals + ions) content of the species whose neutral species has index isfeedback. This is controlled through particle input of neutrals species isfeedback through the	private flux boundaries (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2). will apply fb_type=14, fb_rescale=1, fb_actuator=1 on region defined by pfrregno1. WARNING: in the structured code this switch was asking for BCCON=12, so density BC for fluid neutrals feedback but then it switches to gas puff for kinetic neutrals. Now it is ONLY gas puff.
					private_flux_puff NOT YET CONVERTED TO WG CODE! is the particle flow of species isfeedback through the private flux region boundary. This is controlled through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2).
					All but the first of these feedback schemes ("nesepm") can also be run though an Eirene neutral gas puff. In that case, one should set an appropriate gas puffing stratum in the Eirene input file input.dat, as well as in the b2.neutrals.parameters file. The code will assume, unless told otherwise through the use of "eirene_nesepm_istra", that the first stratum of type 'C' found in b2.neutrals.parameters is the stratum used for the feedback. If "eirene_nesepm_istra" is set to a positive number, the code will consider the feedback stratum to be the stratum in the "eirene_nesepm_istra"-th position in b2.neutrals.parameters.
					b2stbc_iyped is the index in the OMP CV list (defined with RZOMP in b2.user.parameters) of the pedestal cell (defaults to icsepomp/2).
				""", '0.0'),
   
      'b2stbc_nesepm' : ('', 'real', """
					The 20 switches above are all feedback switches and require that b2stbc_feedback.ne.0 (See Run section for details) or that lfeedback=.true. in b2.boundary.parameters. Feedback schemes are now all applied in the same way in a dedicated module b2us_feedback (see FEEDBACK_CONTROL namelist). Switches in b2mn.dat are still available and will override whatever is specified in b2.feedback_control.parameters, but it is recommended to not use switches anymore. This will allow more flexibility in applying such schemes.
					The feedback is done as a boundary condition and is under-relaxed using the b2stbc_...._alpha switches (See Numerics section for details).
					fheycore is the radial electron heat flow entering the core boundary.  Will apply fb_type=11, fb_rescale=1, fb_actuator=4 on region defined by coreregno.
					fhiycore is the radial ion heat flow entering the core boundary. Will apply fb_type=12, fb_rescale=1, fb_actuator=5 on region defined by coreregno.
					fchycore is the radial current entering the core boundary. Will apply fb_type=13, fb_rescale=1, fb_actuator=4 on region defined by coreregno.
					fnaycore is the radial flux of species "isfeedback" entering the core boundary. Will apply fb_type=10, fb_rescale=1, fb_actuator=3 on region defined by coreregno.
					If fhiycore_kinetic_energy.eq.1, the parallel kinetic energy flux is counted as part of the ion energy flux.
					For double-null cases, the f..ycore variables contain the total flow through both core boundaries taken together (to be checked for WG code!).
					The core boundaries are identified by the coreregno and coreregn2 switches (see Geometry section). These switches need to be manually adjusted for WG cases as now they indicate the boundary where the feedback is applied. For switches like b2stbc_xxxycore or private_gas\_puff the user has to specify in b2.feedback_control.parameters} where the feedback is calculated (see b2us.regions.parameters produced at conversion), while coreregno still indicates where it is applied. pfrregno and solregno lose meaning in kinetic cases if the actuator is the gas puff. Coreregn2 and pfrregno2 are not yet converted/used.
					The other seven switches are density feedback switches: nesepm is the outer midplane separatrix electron density. (See rzomp switch in b2.user.parameters for setting of midplane position). This is controlled through particle input of main plasma species isfeedback through the core boundary (See Geometry section for the core boundary indices coreregno and coreregn2).
					nesepm_sol is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the SOL region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the SOL North boundary (See Geometry section for the SOL North boundary index solregno). If nesepm_overshoot.gt.1.0, the gas puff is turned off when the midplane separatrix density reaches nesepm*nesepm_overshoot. Minimum and maximum values of the feedback gas puff can be set using b2stbc_nesepm_minpuff and b2stbc_nesepm_maxpuff. It will apply fb_type=3, fb_rescale=1, fb_actuator=1 on region defined by solregno.
					nepedm_sol is similar to nesepm_sol but the feedback is exerted on the electron density at the top of the pedestal, along the outer midplane, at the icped-th ring (where icped=iyped+2) counting from the inner core boundary. It will apply fb_type=16, fb_rescale=1, fb_actuator=1 on region defined by solregno.
					ndes_sol is the total particle content from the isonuclear sequence of species 'isfeedback' over the entire simulation domain. It is governed, like nesepm_sol, by nesepm_overshoot and nesepm_alpha and corresponds to a SOL boundary feedback. Will apply fb_type=14, fb_rescale=1, fb_actuator=1 on region defined by solregno. WARNING: in the structured code this switch was asking for BCCON=12, so density BC for fluid neutrals feedback but then it switches to gas  puff for kinetic neutrals. Now it is ONLY gaspuff.
					volrec_sol is the total particle source due to volume recombination coming from Eirene. Its feedback is governed by volrec_overshoot and volrec_alpha and volrec_beta parameters (See Numerics section for the latter two). Will apply fb_type=15, fb_rescale=1, fb_actuator=1 on region defined by pfrregno1. WARNING: not available yet for fluid neutrals.
					nesepm_pfr is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the PFR region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the PFR South boundary indices pfrregno1 and pfrregno2). will apply fb_type=3, fb_rescale=1, fb_actuator=1 on region defined pfrregno1
					ndes is the total particle (neutrals + ions) content of the species whose neutral species has index isfeedback. This is controlled through particle input of neutrals species isfeedback through the	private flux boundaries (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2). will apply fb_type=14, fb_rescale=1, fb_actuator=1 on region defined by pfrregno1. WARNING: in the structured code this switch was asking for BCCON=12, so density BC for fluid neutrals feedback but then it switches to gas puff for kinetic neutrals. Now it is ONLY gas puff.
					private_flux_puff NOT YET CONVERTED TO WG CODE! is the particle flow of species isfeedback through the private flux region boundary. This is controlled through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2).
					All but the first of these feedback schemes ("nesepm") can also be run though an Eirene neutral gas puff. In that case, one should set an appropriate gas puffing stratum in the Eirene input file input.dat, as well as in the b2.neutrals.parameters file. The code will assume, unless told otherwise through the use of "eirene_nesepm_istra", that the first stratum of type 'C' found in b2.neutrals.parameters is the stratum used for the feedback. If "eirene_nesepm_istra" is set to a positive number, the code will consider the feedback stratum to be the stratum in the "eirene_nesepm_istra"-th position in b2.neutrals.parameters.
					b2stbc_iyped is the index in the OMP CV list (defined with RZOMP in b2.user.parameters) of the pedestal cell (defaults to icsepomp/2).
				""", '0.0'),
   
      'b2stbc_nesepm_overshoot' : ('', 'real', """
					The 20 switches above are all feedback switches and require that b2stbc_feedback.ne.0 (See Run section for details) or that lfeedback=.true. in b2.boundary.parameters. Feedback schemes are now all applied in the same way in a dedicated module b2us_feedback (see FEEDBACK_CONTROL namelist). Switches in b2mn.dat are still available and will override whatever is specified in b2.feedback_control.parameters, but it is recommended to not use switches anymore. This will allow more flexibility in applying such schemes.
					The feedback is done as a boundary condition and is under-relaxed using the b2stbc_...._alpha switches (See Numerics section for details).
					fheycore is the radial electron heat flow entering the core boundary.  Will apply fb_type=11, fb_rescale=1, fb_actuator=4 on region defined by coreregno.
					fhiycore is the radial ion heat flow entering the core boundary. Will apply fb_type=12, fb_rescale=1, fb_actuator=5 on region defined by coreregno.
					fchycore is the radial current entering the core boundary. Will apply fb_type=13, fb_rescale=1, fb_actuator=4 on region defined by coreregno.
					fnaycore is the radial flux of species "isfeedback" entering the core boundary. Will apply fb_type=10, fb_rescale=1, fb_actuator=3 on region defined by coreregno.
					If fhiycore_kinetic_energy.eq.1, the parallel kinetic energy flux is counted as part of the ion energy flux.
					For double-null cases, the f..ycore variables contain the total flow through both core boundaries taken together (to be checked for WG code!).
					The core boundaries are identified by the coreregno and coreregn2 switches (see Geometry section). These switches need to be manually adjusted for WG cases as now they indicate the boundary where the feedback is applied. For switches like b2stbc_xxxycore or private_gas\_puff the user has to specify in b2.feedback_control.parameters} where the feedback is calculated (see b2us.regions.parameters produced at conversion), while coreregno still indicates where it is applied. pfrregno and solregno lose meaning in kinetic cases if the actuator is the gas puff. Coreregn2 and pfrregno2 are not yet converted/used.
					The other seven switches are density feedback switches: nesepm is the outer midplane separatrix electron density. (See rzomp switch in b2.user.parameters for setting of midplane position). This is controlled through particle input of main plasma species isfeedback through the core boundary (See Geometry section for the core boundary indices coreregno and coreregn2).
					nesepm_sol is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the SOL region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the SOL North boundary (See Geometry section for the SOL North boundary index solregno). If nesepm_overshoot.gt.1.0, the gas puff is turned off when the midplane separatrix density reaches nesepm*nesepm_overshoot. Minimum and maximum values of the feedback gas puff can be set using b2stbc_nesepm_minpuff and b2stbc_nesepm_maxpuff. It will apply fb_type=3, fb_rescale=1, fb_actuator=1 on region defined by solregno.
					nepedm_sol is similar to nesepm_sol but the feedback is exerted on the electron density at the top of the pedestal, along the outer midplane, at the icped-th ring (where icped=iyped+2) counting from the inner core boundary. It will apply fb_type=16, fb_rescale=1, fb_actuator=1 on region defined by solregno.
					ndes_sol is the total particle content from the isonuclear sequence of species 'isfeedback' over the entire simulation domain. It is governed, like nesepm_sol, by nesepm_overshoot and nesepm_alpha and corresponds to a SOL boundary feedback. Will apply fb_type=14, fb_rescale=1, fb_actuator=1 on region defined by solregno. WARNING: in the structured code this switch was asking for BCCON=12, so density BC for fluid neutrals feedback but then it switches to gas  puff for kinetic neutrals. Now it is ONLY gaspuff.
					volrec_sol is the total particle source due to volume recombination coming from Eirene. Its feedback is governed by volrec_overshoot and volrec_alpha and volrec_beta parameters (See Numerics section for the latter two). Will apply fb_type=15, fb_rescale=1, fb_actuator=1 on region defined by pfrregno1. WARNING: not available yet for fluid neutrals.
					nesepm_pfr is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the PFR region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the PFR South boundary indices pfrregno1 and pfrregno2). will apply fb_type=3, fb_rescale=1, fb_actuator=1 on region defined pfrregno1
					ndes is the total particle (neutrals + ions) content of the species whose neutral species has index isfeedback. This is controlled through particle input of neutrals species isfeedback through the	private flux boundaries (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2). will apply fb_type=14, fb_rescale=1, fb_actuator=1 on region defined by pfrregno1. WARNING: in the structured code this switch was asking for BCCON=12, so density BC for fluid neutrals feedback but then it switches to gas puff for kinetic neutrals. Now it is ONLY gas puff.
					private_flux_puff NOT YET CONVERTED TO WG CODE! is the particle flow of species isfeedback through the private flux region boundary. This is controlled through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2).
					All but the first of these feedback schemes ("nesepm") can also be run though an Eirene neutral gas puff. In that case, one should set an appropriate gas puffing stratum in the Eirene input file input.dat, as well as in the b2.neutrals.parameters file. The code will assume, unless told otherwise through the use of "eirene_nesepm_istra", that the first stratum of type 'C' found in b2.neutrals.parameters is the stratum used for the feedback. If "eirene_nesepm_istra" is set to a positive number, the code will consider the feedback stratum to be the stratum in the "eirene_nesepm_istra"-th position in b2.neutrals.parameters.
					b2stbc_iyped is the index in the OMP CV list (defined with RZOMP in b2.user.parameters) of the pedestal cell (defaults to icsepomp/2).
				""", '0.0'),
   
      'b2stbc_nesepm_pfr' : ('', 'real', """
					The 20 switches above are all feedback switches and require that b2stbc_feedback.ne.0 (See Run section for details) or that lfeedback=.true. in b2.boundary.parameters. Feedback schemes are now all applied in the same way in a dedicated module b2us_feedback (see FEEDBACK_CONTROL namelist). Switches in b2mn.dat are still available and will override whatever is specified in b2.feedback_control.parameters, but it is recommended to not use switches anymore. This will allow more flexibility in applying such schemes.
					The feedback is done as a boundary condition and is under-relaxed using the b2stbc_...._alpha switches (See Numerics section for details).
					fheycore is the radial electron heat flow entering the core boundary.  Will apply fb_type=11, fb_rescale=1, fb_actuator=4 on region defined by coreregno.
					fhiycore is the radial ion heat flow entering the core boundary. Will apply fb_type=12, fb_rescale=1, fb_actuator=5 on region defined by coreregno.
					fchycore is the radial current entering the core boundary. Will apply fb_type=13, fb_rescale=1, fb_actuator=4 on region defined by coreregno.
					fnaycore is the radial flux of species "isfeedback" entering the core boundary. Will apply fb_type=10, fb_rescale=1, fb_actuator=3 on region defined by coreregno.
					If fhiycore_kinetic_energy.eq.1, the parallel kinetic energy flux is counted as part of the ion energy flux.
					For double-null cases, the f..ycore variables contain the total flow through both core boundaries taken together (to be checked for WG code!).
					The core boundaries are identified by the coreregno and coreregn2 switches (see Geometry section). These switches need to be manually adjusted for WG cases as now they indicate the boundary where the feedback is applied. For switches like b2stbc_xxxycore or private_gas\_puff the user has to specify in b2.feedback_control.parameters} where the feedback is calculated (see b2us.regions.parameters produced at conversion), while coreregno still indicates where it is applied. pfrregno and solregno lose meaning in kinetic cases if the actuator is the gas puff. Coreregn2 and pfrregno2 are not yet converted/used.
					The other seven switches are density feedback switches: nesepm is the outer midplane separatrix electron density. (See rzomp switch in b2.user.parameters for setting of midplane position). This is controlled through particle input of main plasma species isfeedback through the core boundary (See Geometry section for the core boundary indices coreregno and coreregn2).
					nesepm_sol is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the SOL region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the SOL North boundary (See Geometry section for the SOL North boundary index solregno). If nesepm_overshoot.gt.1.0, the gas puff is turned off when the midplane separatrix density reaches nesepm*nesepm_overshoot. Minimum and maximum values of the feedback gas puff can be set using b2stbc_nesepm_minpuff and b2stbc_nesepm_maxpuff. It will apply fb_type=3, fb_rescale=1, fb_actuator=1 on region defined by solregno.
					nepedm_sol is similar to nesepm_sol but the feedback is exerted on the electron density at the top of the pedestal, along the outer midplane, at the icped-th ring (where icped=iyped+2) counting from the inner core boundary. It will apply fb_type=16, fb_rescale=1, fb_actuator=1 on region defined by solregno.
					ndes_sol is the total particle content from the isonuclear sequence of species 'isfeedback' over the entire simulation domain. It is governed, like nesepm_sol, by nesepm_overshoot and nesepm_alpha and corresponds to a SOL boundary feedback. Will apply fb_type=14, fb_rescale=1, fb_actuator=1 on region defined by solregno. WARNING: in the structured code this switch was asking for BCCON=12, so density BC for fluid neutrals feedback but then it switches to gas  puff for kinetic neutrals. Now it is ONLY gaspuff.
					volrec_sol is the total particle source due to volume recombination coming from Eirene. Its feedback is governed by volrec_overshoot and volrec_alpha and volrec_beta parameters (See Numerics section for the latter two). Will apply fb_type=15, fb_rescale=1, fb_actuator=1 on region defined by pfrregno1. WARNING: not available yet for fluid neutrals.
					nesepm_pfr is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the PFR region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the PFR South boundary indices pfrregno1 and pfrregno2). will apply fb_type=3, fb_rescale=1, fb_actuator=1 on region defined pfrregno1
					ndes is the total particle (neutrals + ions) content of the species whose neutral species has index isfeedback. This is controlled through particle input of neutrals species isfeedback through the	private flux boundaries (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2). will apply fb_type=14, fb_rescale=1, fb_actuator=1 on region defined by pfrregno1. WARNING: in the structured code this switch was asking for BCCON=12, so density BC for fluid neutrals feedback but then it switches to gas puff for kinetic neutrals. Now it is ONLY gas puff.
					private_flux_puff NOT YET CONVERTED TO WG CODE! is the particle flow of species isfeedback through the private flux region boundary. This is controlled through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2).
					All but the first of these feedback schemes ("nesepm") can also be run though an Eirene neutral gas puff. In that case, one should set an appropriate gas puffing stratum in the Eirene input file input.dat, as well as in the b2.neutrals.parameters file. The code will assume, unless told otherwise through the use of "eirene_nesepm_istra", that the first stratum of type 'C' found in b2.neutrals.parameters is the stratum used for the feedback. If "eirene_nesepm_istra" is set to a positive number, the code will consider the feedback stratum to be the stratum in the "eirene_nesepm_istra"-th position in b2.neutrals.parameters.
					b2stbc_iyped is the index in the OMP CV list (defined with RZOMP in b2.user.parameters) of the pedestal cell (defaults to icsepomp/2).
				""", '0.0'),
   
      'b2stbc_nesepm_sol' : ('', 'real', """
					The 20 switches above are all feedback switches and require that b2stbc_feedback.ne.0 (See Run section for details) or that lfeedback=.true. in b2.boundary.parameters. Feedback schemes are now all applied in the same way in a dedicated module b2us_feedback (see FEEDBACK_CONTROL namelist). Switches in b2mn.dat are still available and will override whatever is specified in b2.feedback_control.parameters, but it is recommended to not use switches anymore. This will allow more flexibility in applying such schemes.
					The feedback is done as a boundary condition and is under-relaxed using the b2stbc_...._alpha switches (See Numerics section for details).
					fheycore is the radial electron heat flow entering the core boundary.  Will apply fb_type=11, fb_rescale=1, fb_actuator=4 on region defined by coreregno.
					fhiycore is the radial ion heat flow entering the core boundary. Will apply fb_type=12, fb_rescale=1, fb_actuator=5 on region defined by coreregno.
					fchycore is the radial current entering the core boundary. Will apply fb_type=13, fb_rescale=1, fb_actuator=4 on region defined by coreregno.
					fnaycore is the radial flux of species "isfeedback" entering the core boundary. Will apply fb_type=10, fb_rescale=1, fb_actuator=3 on region defined by coreregno.
					If fhiycore_kinetic_energy.eq.1, the parallel kinetic energy flux is counted as part of the ion energy flux.
					For double-null cases, the f..ycore variables contain the total flow through both core boundaries taken together (to be checked for WG code!).
					The core boundaries are identified by the coreregno and coreregn2 switches (see Geometry section). These switches need to be manually adjusted for WG cases as now they indicate the boundary where the feedback is applied. For switches like b2stbc_xxxycore or private_gas\_puff the user has to specify in b2.feedback_control.parameters} where the feedback is calculated (see b2us.regions.parameters produced at conversion), while coreregno still indicates where it is applied. pfrregno and solregno lose meaning in kinetic cases if the actuator is the gas puff. Coreregn2 and pfrregno2 are not yet converted/used.
					The other seven switches are density feedback switches: nesepm is the outer midplane separatrix electron density. (See rzomp switch in b2.user.parameters for setting of midplane position). This is controlled through particle input of main plasma species isfeedback through the core boundary (See Geometry section for the core boundary indices coreregno and coreregn2).
					nesepm_sol is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the SOL region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the SOL North boundary (See Geometry section for the SOL North boundary index solregno). If nesepm_overshoot.gt.1.0, the gas puff is turned off when the midplane separatrix density reaches nesepm*nesepm_overshoot. Minimum and maximum values of the feedback gas puff can be set using b2stbc_nesepm_minpuff and b2stbc_nesepm_maxpuff. It will apply fb_type=3, fb_rescale=1, fb_actuator=1 on region defined by solregno.
					nepedm_sol is similar to nesepm_sol but the feedback is exerted on the electron density at the top of the pedestal, along the outer midplane, at the icped-th ring (where icped=iyped+2) counting from the inner core boundary. It will apply fb_type=16, fb_rescale=1, fb_actuator=1 on region defined by solregno.
					ndes_sol is the total particle content from the isonuclear sequence of species 'isfeedback' over the entire simulation domain. It is governed, like nesepm_sol, by nesepm_overshoot and nesepm_alpha and corresponds to a SOL boundary feedback. Will apply fb_type=14, fb_rescale=1, fb_actuator=1 on region defined by solregno. WARNING: in the structured code this switch was asking for BCCON=12, so density BC for fluid neutrals feedback but then it switches to gas  puff for kinetic neutrals. Now it is ONLY gaspuff.
					volrec_sol is the total particle source due to volume recombination coming from Eirene. Its feedback is governed by volrec_overshoot and volrec_alpha and volrec_beta parameters (See Numerics section for the latter two). Will apply fb_type=15, fb_rescale=1, fb_actuator=1 on region defined by pfrregno1. WARNING: not available yet for fluid neutrals.
					nesepm_pfr is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the PFR region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the PFR South boundary indices pfrregno1 and pfrregno2). will apply fb_type=3, fb_rescale=1, fb_actuator=1 on region defined pfrregno1
					ndes is the total particle (neutrals + ions) content of the species whose neutral species has index isfeedback. This is controlled through particle input of neutrals species isfeedback through the	private flux boundaries (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2). will apply fb_type=14, fb_rescale=1, fb_actuator=1 on region defined by pfrregno1. WARNING: in the structured code this switch was asking for BCCON=12, so density BC for fluid neutrals feedback but then it switches to gas puff for kinetic neutrals. Now it is ONLY gas puff.
					private_flux_puff NOT YET CONVERTED TO WG CODE! is the particle flow of species isfeedback through the private flux region boundary. This is controlled through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2).
					All but the first of these feedback schemes ("nesepm") can also be run though an Eirene neutral gas puff. In that case, one should set an appropriate gas puffing stratum in the Eirene input file input.dat, as well as in the b2.neutrals.parameters file. The code will assume, unless told otherwise through the use of "eirene_nesepm_istra", that the first stratum of type 'C' found in b2.neutrals.parameters is the stratum used for the feedback. If "eirene_nesepm_istra" is set to a positive number, the code will consider the feedback stratum to be the stratum in the "eirene_nesepm_istra"-th position in b2.neutrals.parameters.
					b2stbc_iyped is the index in the OMP CV list (defined with RZOMP in b2.user.parameters) of the pedestal cell (defaults to icsepomp/2).
				""", '0.0'),
   
      'b2stbc_private_flux_puff' : ('', 'real', """
					The 20 switches above are all feedback switches and require that b2stbc_feedback.ne.0 (See Run section for details) or that lfeedback=.true. in b2.boundary.parameters. Feedback schemes are now all applied in the same way in a dedicated module b2us_feedback (see FEEDBACK_CONTROL namelist). Switches in b2mn.dat are still available and will override whatever is specified in b2.feedback_control.parameters, but it is recommended to not use switches anymore. This will allow more flexibility in applying such schemes.
					The feedback is done as a boundary condition and is under-relaxed using the b2stbc_...._alpha switches (See Numerics section for details).
					fheycore is the radial electron heat flow entering the core boundary.  Will apply fb_type=11, fb_rescale=1, fb_actuator=4 on region defined by coreregno.
					fhiycore is the radial ion heat flow entering the core boundary. Will apply fb_type=12, fb_rescale=1, fb_actuator=5 on region defined by coreregno.
					fchycore is the radial current entering the core boundary. Will apply fb_type=13, fb_rescale=1, fb_actuator=4 on region defined by coreregno.
					fnaycore is the radial flux of species "isfeedback" entering the core boundary. Will apply fb_type=10, fb_rescale=1, fb_actuator=3 on region defined by coreregno.
					If fhiycore_kinetic_energy.eq.1, the parallel kinetic energy flux is counted as part of the ion energy flux.
					For double-null cases, the f..ycore variables contain the total flow through both core boundaries taken together (to be checked for WG code!).
					The core boundaries are identified by the coreregno and coreregn2 switches (see Geometry section). These switches need to be manually adjusted for WG cases as now they indicate the boundary where the feedback is applied. For switches like b2stbc_xxxycore or private_gas\_puff the user has to specify in b2.feedback_control.parameters} where the feedback is calculated (see b2us.regions.parameters produced at conversion), while coreregno still indicates where it is applied. pfrregno and solregno lose meaning in kinetic cases if the actuator is the gas puff. Coreregn2 and pfrregno2 are not yet converted/used.
					The other seven switches are density feedback switches: nesepm is the outer midplane separatrix electron density. (See rzomp switch in b2.user.parameters for setting of midplane position). This is controlled through particle input of main plasma species isfeedback through the core boundary (See Geometry section for the core boundary indices coreregno and coreregn2).
					nesepm_sol is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the SOL region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the SOL North boundary (See Geometry section for the SOL North boundary index solregno). If nesepm_overshoot.gt.1.0, the gas puff is turned off when the midplane separatrix density reaches nesepm*nesepm_overshoot. Minimum and maximum values of the feedback gas puff can be set using b2stbc_nesepm_minpuff and b2stbc_nesepm_maxpuff. It will apply fb_type=3, fb_rescale=1, fb_actuator=1 on region defined by solregno.
					nepedm_sol is similar to nesepm_sol but the feedback is exerted on the electron density at the top of the pedestal, along the outer midplane, at the icped-th ring (where icped=iyped+2) counting from the inner core boundary. It will apply fb_type=16, fb_rescale=1, fb_actuator=1 on region defined by solregno.
					ndes_sol is the total particle content from the isonuclear sequence of species 'isfeedback' over the entire simulation domain. It is governed, like nesepm_sol, by nesepm_overshoot and nesepm_alpha and corresponds to a SOL boundary feedback. Will apply fb_type=14, fb_rescale=1, fb_actuator=1 on region defined by solregno. WARNING: in the structured code this switch was asking for BCCON=12, so density BC for fluid neutrals feedback but then it switches to gas  puff for kinetic neutrals. Now it is ONLY gaspuff.
					volrec_sol is the total particle source due to volume recombination coming from Eirene. Its feedback is governed by volrec_overshoot and volrec_alpha and volrec_beta parameters (See Numerics section for the latter two). Will apply fb_type=15, fb_rescale=1, fb_actuator=1 on region defined by pfrregno1. WARNING: not available yet for fluid neutrals.
					nesepm_pfr is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the PFR region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the PFR South boundary indices pfrregno1 and pfrregno2). will apply fb_type=3, fb_rescale=1, fb_actuator=1 on region defined pfrregno1
					ndes is the total particle (neutrals + ions) content of the species whose neutral species has index isfeedback. This is controlled through particle input of neutrals species isfeedback through the	private flux boundaries (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2). will apply fb_type=14, fb_rescale=1, fb_actuator=1 on region defined by pfrregno1. WARNING: in the structured code this switch was asking for BCCON=12, so density BC for fluid neutrals feedback but then it switches to gas puff for kinetic neutrals. Now it is ONLY gas puff.
					private_flux_puff NOT YET CONVERTED TO WG CODE! is the particle flow of species isfeedback through the private flux region boundary. This is controlled through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2).
					All but the first of these feedback schemes ("nesepm") can also be run though an Eirene neutral gas puff. In that case, one should set an appropriate gas puffing stratum in the Eirene input file input.dat, as well as in the b2.neutrals.parameters file. The code will assume, unless told otherwise through the use of "eirene_nesepm_istra", that the first stratum of type 'C' found in b2.neutrals.parameters is the stratum used for the feedback. If "eirene_nesepm_istra" is set to a positive number, the code will consider the feedback stratum to be the stratum in the "eirene_nesepm_istra"-th position in b2.neutrals.parameters.
					b2stbc_iyped is the index in the OMP CV list (defined with RZOMP in b2.user.parameters) of the pedestal cell (defaults to icsepomp/2).
				""", '0.0'),
   
      'b2stbc_volrec' : ('', 'real', """
					The 20 switches above are all feedback switches and require that b2stbc_feedback.ne.0 (See Run section for details) or that lfeedback=.true. in b2.boundary.parameters. Feedback schemes are now all applied in the same way in a dedicated module b2us_feedback (see FEEDBACK_CONTROL namelist). Switches in b2mn.dat are still available and will override whatever is specified in b2.feedback_control.parameters, but it is recommended to not use switches anymore. This will allow more flexibility in applying such schemes.
					The feedback is done as a boundary condition and is under-relaxed using the b2stbc_...._alpha switches (See Numerics section for details).
					fheycore is the radial electron heat flow entering the core boundary.  Will apply fb_type=11, fb_rescale=1, fb_actuator=4 on region defined by coreregno.
					fhiycore is the radial ion heat flow entering the core boundary. Will apply fb_type=12, fb_rescale=1, fb_actuator=5 on region defined by coreregno.
					fchycore is the radial current entering the core boundary. Will apply fb_type=13, fb_rescale=1, fb_actuator=4 on region defined by coreregno.
					fnaycore is the radial flux of species "isfeedback" entering the core boundary. Will apply fb_type=10, fb_rescale=1, fb_actuator=3 on region defined by coreregno.
					If fhiycore_kinetic_energy.eq.1, the parallel kinetic energy flux is counted as part of the ion energy flux.
					For double-null cases, the f..ycore variables contain the total flow through both core boundaries taken together (to be checked for WG code!).
					The core boundaries are identified by the coreregno and coreregn2 switches (see Geometry section). These switches need to be manually adjusted for WG cases as now they indicate the boundary where the feedback is applied. For switches like b2stbc_xxxycore or private_gas\_puff the user has to specify in b2.feedback_control.parameters} where the feedback is calculated (see b2us.regions.parameters produced at conversion), while coreregno still indicates where it is applied. pfrregno and solregno lose meaning in kinetic cases if the actuator is the gas puff. Coreregn2 and pfrregno2 are not yet converted/used.
					The other seven switches are density feedback switches: nesepm is the outer midplane separatrix electron density. (See rzomp switch in b2.user.parameters for setting of midplane position). This is controlled through particle input of main plasma species isfeedback through the core boundary (See Geometry section for the core boundary indices coreregno and coreregn2).
					nesepm_sol is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the SOL region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the SOL North boundary (See Geometry section for the SOL North boundary index solregno). If nesepm_overshoot.gt.1.0, the gas puff is turned off when the midplane separatrix density reaches nesepm*nesepm_overshoot. Minimum and maximum values of the feedback gas puff can be set using b2stbc_nesepm_minpuff and b2stbc_nesepm_maxpuff. It will apply fb_type=3, fb_rescale=1, fb_actuator=1 on region defined by solregno.
					nepedm_sol is similar to nesepm_sol but the feedback is exerted on the electron density at the top of the pedestal, along the outer midplane, at the icped-th ring (where icped=iyped+2) counting from the inner core boundary. It will apply fb_type=16, fb_rescale=1, fb_actuator=1 on region defined by solregno.
					ndes_sol is the total particle content from the isonuclear sequence of species 'isfeedback' over the entire simulation domain. It is governed, like nesepm_sol, by nesepm_overshoot and nesepm_alpha and corresponds to a SOL boundary feedback. Will apply fb_type=14, fb_rescale=1, fb_actuator=1 on region defined by solregno. WARNING: in the structured code this switch was asking for BCCON=12, so density BC for fluid neutrals feedback but then it switches to gas  puff for kinetic neutrals. Now it is ONLY gaspuff.
					volrec_sol is the total particle source due to volume recombination coming from Eirene. Its feedback is governed by volrec_overshoot and volrec_alpha and volrec_beta parameters (See Numerics section for the latter two). Will apply fb_type=15, fb_rescale=1, fb_actuator=1 on region defined by pfrregno1. WARNING: not available yet for fluid neutrals.
					nesepm_pfr is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the PFR region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the PFR South boundary indices pfrregno1 and pfrregno2). will apply fb_type=3, fb_rescale=1, fb_actuator=1 on region defined pfrregno1
					ndes is the total particle (neutrals + ions) content of the species whose neutral species has index isfeedback. This is controlled through particle input of neutrals species isfeedback through the	private flux boundaries (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2). will apply fb_type=14, fb_rescale=1, fb_actuator=1 on region defined by pfrregno1. WARNING: in the structured code this switch was asking for BCCON=12, so density BC for fluid neutrals feedback but then it switches to gas puff for kinetic neutrals. Now it is ONLY gas puff.
					private_flux_puff NOT YET CONVERTED TO WG CODE! is the particle flow of species isfeedback through the private flux region boundary. This is controlled through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2).
					All but the first of these feedback schemes ("nesepm") can also be run though an Eirene neutral gas puff. In that case, one should set an appropriate gas puffing stratum in the Eirene input file input.dat, as well as in the b2.neutrals.parameters file. The code will assume, unless told otherwise through the use of "eirene_nesepm_istra", that the first stratum of type 'C' found in b2.neutrals.parameters is the stratum used for the feedback. If "eirene_nesepm_istra" is set to a positive number, the code will consider the feedback stratum to be the stratum in the "eirene_nesepm_istra"-th position in b2.neutrals.parameters.
					b2stbc_iyped is the index in the OMP CV list (defined with RZOMP in b2.user.parameters) of the pedestal cell (defaults to icsepomp/2).
				""", '0.0'),
   
      'b2stbc_volrec_overshoot' : ('', 'real', """
					The 20 switches above are all feedback switches and require that b2stbc_feedback.ne.0 (See Run section for details) or that lfeedback=.true. in b2.boundary.parameters. Feedback schemes are now all applied in the same way in a dedicated module b2us_feedback (see FEEDBACK_CONTROL namelist). Switches in b2mn.dat are still available and will override whatever is specified in b2.feedback_control.parameters, but it is recommended to not use switches anymore. This will allow more flexibility in applying such schemes.
					The feedback is done as a boundary condition and is under-relaxed using the b2stbc_...._alpha switches (See Numerics section for details).
					fheycore is the radial electron heat flow entering the core boundary.  Will apply fb_type=11, fb_rescale=1, fb_actuator=4 on region defined by coreregno.
					fhiycore is the radial ion heat flow entering the core boundary. Will apply fb_type=12, fb_rescale=1, fb_actuator=5 on region defined by coreregno.
					fchycore is the radial current entering the core boundary. Will apply fb_type=13, fb_rescale=1, fb_actuator=4 on region defined by coreregno.
					fnaycore is the radial flux of species "isfeedback" entering the core boundary. Will apply fb_type=10, fb_rescale=1, fb_actuator=3 on region defined by coreregno.
					If fhiycore_kinetic_energy.eq.1, the parallel kinetic energy flux is counted as part of the ion energy flux.
					For double-null cases, the f..ycore variables contain the total flow through both core boundaries taken together (to be checked for WG code!).
					The core boundaries are identified by the coreregno and coreregn2 switches (see Geometry section). These switches need to be manually adjusted for WG cases as now they indicate the boundary where the feedback is applied. For switches like b2stbc_xxxycore or private_gas\_puff the user has to specify in b2.feedback_control.parameters} where the feedback is calculated (see b2us.regions.parameters produced at conversion), while coreregno still indicates where it is applied. pfrregno and solregno lose meaning in kinetic cases if the actuator is the gas puff. Coreregn2 and pfrregno2 are not yet converted/used.
					The other seven switches are density feedback switches: nesepm is the outer midplane separatrix electron density. (See rzomp switch in b2.user.parameters for setting of midplane position). This is controlled through particle input of main plasma species isfeedback through the core boundary (See Geometry section for the core boundary indices coreregno and coreregn2).
					nesepm_sol is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the SOL region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the SOL North boundary (See Geometry section for the SOL North boundary index solregno). If nesepm_overshoot.gt.1.0, the gas puff is turned off when the midplane separatrix density reaches nesepm*nesepm_overshoot. Minimum and maximum values of the feedback gas puff can be set using b2stbc_nesepm_minpuff and b2stbc_nesepm_maxpuff. It will apply fb_type=3, fb_rescale=1, fb_actuator=1 on region defined by solregno.
					nepedm_sol is similar to nesepm_sol but the feedback is exerted on the electron density at the top of the pedestal, along the outer midplane, at the icped-th ring (where icped=iyped+2) counting from the inner core boundary. It will apply fb_type=16, fb_rescale=1, fb_actuator=1 on region defined by solregno.
					ndes_sol is the total particle content from the isonuclear sequence of species 'isfeedback' over the entire simulation domain. It is governed, like nesepm_sol, by nesepm_overshoot and nesepm_alpha and corresponds to a SOL boundary feedback. Will apply fb_type=14, fb_rescale=1, fb_actuator=1 on region defined by solregno. WARNING: in the structured code this switch was asking for BCCON=12, so density BC for fluid neutrals feedback but then it switches to gas  puff for kinetic neutrals. Now it is ONLY gaspuff.
					volrec_sol is the total particle source due to volume recombination coming from Eirene. Its feedback is governed by volrec_overshoot and volrec_alpha and volrec_beta parameters (See Numerics section for the latter two). Will apply fb_type=15, fb_rescale=1, fb_actuator=1 on region defined by pfrregno1. WARNING: not available yet for fluid neutrals.
					nesepm_pfr is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the PFR region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the PFR South boundary indices pfrregno1 and pfrregno2). will apply fb_type=3, fb_rescale=1, fb_actuator=1 on region defined pfrregno1
					ndes is the total particle (neutrals + ions) content of the species whose neutral species has index isfeedback. This is controlled through particle input of neutrals species isfeedback through the	private flux boundaries (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2). will apply fb_type=14, fb_rescale=1, fb_actuator=1 on region defined by pfrregno1. WARNING: in the structured code this switch was asking for BCCON=12, so density BC for fluid neutrals feedback but then it switches to gas puff for kinetic neutrals. Now it is ONLY gas puff.
					private_flux_puff NOT YET CONVERTED TO WG CODE! is the particle flow of species isfeedback through the private flux region boundary. This is controlled through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2).
					All but the first of these feedback schemes ("nesepm") can also be run though an Eirene neutral gas puff. In that case, one should set an appropriate gas puffing stratum in the Eirene input file input.dat, as well as in the b2.neutrals.parameters file. The code will assume, unless told otherwise through the use of "eirene_nesepm_istra", that the first stratum of type 'C' found in b2.neutrals.parameters is the stratum used for the feedback. If "eirene_nesepm_istra" is set to a positive number, the code will consider the feedback stratum to be the stratum in the "eirene_nesepm_istra"-th position in b2.neutrals.parameters.
					b2stbc_iyped is the index in the OMP CV list (defined with RZOMP in b2.user.parameters) of the pedestal cell (defaults to icsepomp/2).
				""", '0.0'),
   
      'b2stbc_nesepm_minpuff' : ('', 'real', """
					The 20 switches above are all feedback switches and require that b2stbc_feedback.ne.0 (See Run section for details) or that lfeedback=.true. in b2.boundary.parameters. Feedback schemes are now all applied in the same way in a dedicated module b2us_feedback (see FEEDBACK_CONTROL namelist). Switches in b2mn.dat are still available and will override whatever is specified in b2.feedback_control.parameters, but it is recommended to not use switches anymore. This will allow more flexibility in applying such schemes.
					The feedback is done as a boundary condition and is under-relaxed using the b2stbc_...._alpha switches (See Numerics section for details).
					fheycore is the radial electron heat flow entering the core boundary.  Will apply fb_type=11, fb_rescale=1, fb_actuator=4 on region defined by coreregno.
					fhiycore is the radial ion heat flow entering the core boundary. Will apply fb_type=12, fb_rescale=1, fb_actuator=5 on region defined by coreregno.
					fchycore is the radial current entering the core boundary. Will apply fb_type=13, fb_rescale=1, fb_actuator=4 on region defined by coreregno.
					fnaycore is the radial flux of species "isfeedback" entering the core boundary. Will apply fb_type=10, fb_rescale=1, fb_actuator=3 on region defined by coreregno.
					If fhiycore_kinetic_energy.eq.1, the parallel kinetic energy flux is counted as part of the ion energy flux.
					For double-null cases, the f..ycore variables contain the total flow through both core boundaries taken together (to be checked for WG code!).
					The core boundaries are identified by the coreregno and coreregn2 switches (see Geometry section). These switches need to be manually adjusted for WG cases as now they indicate the boundary where the feedback is applied. For switches like b2stbc_xxxycore or private_gas\_puff the user has to specify in b2.feedback_control.parameters} where the feedback is calculated (see b2us.regions.parameters produced at conversion), while coreregno still indicates where it is applied. pfrregno and solregno lose meaning in kinetic cases if the actuator is the gas puff. Coreregn2 and pfrregno2 are not yet converted/used.
					The other seven switches are density feedback switches: nesepm is the outer midplane separatrix electron density. (See rzomp switch in b2.user.parameters for setting of midplane position). This is controlled through particle input of main plasma species isfeedback through the core boundary (See Geometry section for the core boundary indices coreregno and coreregn2).
					nesepm_sol is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the SOL region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the SOL North boundary (See Geometry section for the SOL North boundary index solregno). If nesepm_overshoot.gt.1.0, the gas puff is turned off when the midplane separatrix density reaches nesepm*nesepm_overshoot. Minimum and maximum values of the feedback gas puff can be set using b2stbc_nesepm_minpuff and b2stbc_nesepm_maxpuff. It will apply fb_type=3, fb_rescale=1, fb_actuator=1 on region defined by solregno.
					nepedm_sol is similar to nesepm_sol but the feedback is exerted on the electron density at the top of the pedestal, along the outer midplane, at the icped-th ring (where icped=iyped+2) counting from the inner core boundary. It will apply fb_type=16, fb_rescale=1, fb_actuator=1 on region defined by solregno.
					ndes_sol is the total particle content from the isonuclear sequence of species 'isfeedback' over the entire simulation domain. It is governed, like nesepm_sol, by nesepm_overshoot and nesepm_alpha and corresponds to a SOL boundary feedback. Will apply fb_type=14, fb_rescale=1, fb_actuator=1 on region defined by solregno. WARNING: in the structured code this switch was asking for BCCON=12, so density BC for fluid neutrals feedback but then it switches to gas  puff for kinetic neutrals. Now it is ONLY gaspuff.
					volrec_sol is the total particle source due to volume recombination coming from Eirene. Its feedback is governed by volrec_overshoot and volrec_alpha and volrec_beta parameters (See Numerics section for the latter two). Will apply fb_type=15, fb_rescale=1, fb_actuator=1 on region defined by pfrregno1. WARNING: not available yet for fluid neutrals.
					nesepm_pfr is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the PFR region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the PFR South boundary indices pfrregno1 and pfrregno2). will apply fb_type=3, fb_rescale=1, fb_actuator=1 on region defined pfrregno1
					ndes is the total particle (neutrals + ions) content of the species whose neutral species has index isfeedback. This is controlled through particle input of neutrals species isfeedback through the	private flux boundaries (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2). will apply fb_type=14, fb_rescale=1, fb_actuator=1 on region defined by pfrregno1. WARNING: in the structured code this switch was asking for BCCON=12, so density BC for fluid neutrals feedback but then it switches to gas puff for kinetic neutrals. Now it is ONLY gas puff.
					private_flux_puff NOT YET CONVERTED TO WG CODE! is the particle flow of species isfeedback through the private flux region boundary. This is controlled through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2).
					All but the first of these feedback schemes ("nesepm") can also be run though an Eirene neutral gas puff. In that case, one should set an appropriate gas puffing stratum in the Eirene input file input.dat, as well as in the b2.neutrals.parameters file. The code will assume, unless told otherwise through the use of "eirene_nesepm_istra", that the first stratum of type 'C' found in b2.neutrals.parameters is the stratum used for the feedback. If "eirene_nesepm_istra" is set to a positive number, the code will consider the feedback stratum to be the stratum in the "eirene_nesepm_istra"-th position in b2.neutrals.parameters.
					b2stbc_iyped is the index in the OMP CV list (defined with RZOMP in b2.user.parameters) of the pedestal cell (defaults to icsepomp/2).
				""", '0.0'),
   
      'b2stbc_nesepm_maxpuff' : ('', 'real', """
					The 20 switches above are all feedback switches and require that b2stbc_feedback.ne.0 (See Run section for details) or that lfeedback=.true. in b2.boundary.parameters. Feedback schemes are now all applied in the same way in a dedicated module b2us_feedback (see FEEDBACK_CONTROL namelist). Switches in b2mn.dat are still available and will override whatever is specified in b2.feedback_control.parameters, but it is recommended to not use switches anymore. This will allow more flexibility in applying such schemes.
					The feedback is done as a boundary condition and is under-relaxed using the b2stbc_...._alpha switches (See Numerics section for details).
					fheycore is the radial electron heat flow entering the core boundary.  Will apply fb_type=11, fb_rescale=1, fb_actuator=4 on region defined by coreregno.
					fhiycore is the radial ion heat flow entering the core boundary. Will apply fb_type=12, fb_rescale=1, fb_actuator=5 on region defined by coreregno.
					fchycore is the radial current entering the core boundary. Will apply fb_type=13, fb_rescale=1, fb_actuator=4 on region defined by coreregno.
					fnaycore is the radial flux of species "isfeedback" entering the core boundary. Will apply fb_type=10, fb_rescale=1, fb_actuator=3 on region defined by coreregno.
					If fhiycore_kinetic_energy.eq.1, the parallel kinetic energy flux is counted as part of the ion energy flux.
					For double-null cases, the f..ycore variables contain the total flow through both core boundaries taken together (to be checked for WG code!).
					The core boundaries are identified by the coreregno and coreregn2 switches (see Geometry section). These switches need to be manually adjusted for WG cases as now they indicate the boundary where the feedback is applied. For switches like b2stbc_xxxycore or private_gas\_puff the user has to specify in b2.feedback_control.parameters} where the feedback is calculated (see b2us.regions.parameters produced at conversion), while coreregno still indicates where it is applied. pfrregno and solregno lose meaning in kinetic cases if the actuator is the gas puff. Coreregn2 and pfrregno2 are not yet converted/used.
					The other seven switches are density feedback switches: nesepm is the outer midplane separatrix electron density. (See rzomp switch in b2.user.parameters for setting of midplane position). This is controlled through particle input of main plasma species isfeedback through the core boundary (See Geometry section for the core boundary indices coreregno and coreregn2).
					nesepm_sol is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the SOL region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the SOL North boundary (See Geometry section for the SOL North boundary index solregno). If nesepm_overshoot.gt.1.0, the gas puff is turned off when the midplane separatrix density reaches nesepm*nesepm_overshoot. Minimum and maximum values of the feedback gas puff can be set using b2stbc_nesepm_minpuff and b2stbc_nesepm_maxpuff. It will apply fb_type=3, fb_rescale=1, fb_actuator=1 on region defined by solregno.
					nepedm_sol is similar to nesepm_sol but the feedback is exerted on the electron density at the top of the pedestal, along the outer midplane, at the icped-th ring (where icped=iyped+2) counting from the inner core boundary. It will apply fb_type=16, fb_rescale=1, fb_actuator=1 on region defined by solregno.
					ndes_sol is the total particle content from the isonuclear sequence of species 'isfeedback' over the entire simulation domain. It is governed, like nesepm_sol, by nesepm_overshoot and nesepm_alpha and corresponds to a SOL boundary feedback. Will apply fb_type=14, fb_rescale=1, fb_actuator=1 on region defined by solregno. WARNING: in the structured code this switch was asking for BCCON=12, so density BC for fluid neutrals feedback but then it switches to gas  puff for kinetic neutrals. Now it is ONLY gaspuff.
					volrec_sol is the total particle source due to volume recombination coming from Eirene. Its feedback is governed by volrec_overshoot and volrec_alpha and volrec_beta parameters (See Numerics section for the latter two). Will apply fb_type=15, fb_rescale=1, fb_actuator=1 on region defined by pfrregno1. WARNING: not available yet for fluid neutrals.
					nesepm_pfr is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the PFR region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the PFR South boundary indices pfrregno1 and pfrregno2). will apply fb_type=3, fb_rescale=1, fb_actuator=1 on region defined pfrregno1
					ndes is the total particle (neutrals + ions) content of the species whose neutral species has index isfeedback. This is controlled through particle input of neutrals species isfeedback through the	private flux boundaries (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2). will apply fb_type=14, fb_rescale=1, fb_actuator=1 on region defined by pfrregno1. WARNING: in the structured code this switch was asking for BCCON=12, so density BC for fluid neutrals feedback but then it switches to gas puff for kinetic neutrals. Now it is ONLY gas puff.
					private_flux_puff NOT YET CONVERTED TO WG CODE! is the particle flow of species isfeedback through the private flux region boundary. This is controlled through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2).
					All but the first of these feedback schemes ("nesepm") can also be run though an Eirene neutral gas puff. In that case, one should set an appropriate gas puffing stratum in the Eirene input file input.dat, as well as in the b2.neutrals.parameters file. The code will assume, unless told otherwise through the use of "eirene_nesepm_istra", that the first stratum of type 'C' found in b2.neutrals.parameters is the stratum used for the feedback. If "eirene_nesepm_istra" is set to a positive number, the code will consider the feedback stratum to be the stratum in the "eirene_nesepm_istra"-th position in b2.neutrals.parameters.
					b2stbc_iyped is the index in the OMP CV list (defined with RZOMP in b2.user.parameters) of the pedestal cell (defaults to icsepomp/2).
				""", '0.0'),
   
      'eirene_nesepm_istra' : ('', 'integer', """
					The 20 switches above are all feedback switches and require that b2stbc_feedback.ne.0 (See Run section for details) or that lfeedback=.true. in b2.boundary.parameters. Feedback schemes are now all applied in the same way in a dedicated module b2us_feedback (see FEEDBACK_CONTROL namelist). Switches in b2mn.dat are still available and will override whatever is specified in b2.feedback_control.parameters, but it is recommended to not use switches anymore. This will allow more flexibility in applying such schemes.
					The feedback is done as a boundary condition and is under-relaxed using the b2stbc_...._alpha switches (See Numerics section for details).
					fheycore is the radial electron heat flow entering the core boundary.  Will apply fb_type=11, fb_rescale=1, fb_actuator=4 on region defined by coreregno.
					fhiycore is the radial ion heat flow entering the core boundary. Will apply fb_type=12, fb_rescale=1, fb_actuator=5 on region defined by coreregno.
					fchycore is the radial current entering the core boundary. Will apply fb_type=13, fb_rescale=1, fb_actuator=4 on region defined by coreregno.
					fnaycore is the radial flux of species "isfeedback" entering the core boundary. Will apply fb_type=10, fb_rescale=1, fb_actuator=3 on region defined by coreregno.
					If fhiycore_kinetic_energy.eq.1, the parallel kinetic energy flux is counted as part of the ion energy flux.
					For double-null cases, the f..ycore variables contain the total flow through both core boundaries taken together (to be checked for WG code!).
					The core boundaries are identified by the coreregno and coreregn2 switches (see Geometry section). These switches need to be manually adjusted for WG cases as now they indicate the boundary where the feedback is applied. For switches like b2stbc_xxxycore or private_gas\_puff the user has to specify in b2.feedback_control.parameters} where the feedback is calculated (see b2us.regions.parameters produced at conversion), while coreregno still indicates where it is applied. pfrregno and solregno lose meaning in kinetic cases if the actuator is the gas puff. Coreregn2 and pfrregno2 are not yet converted/used.
					The other seven switches are density feedback switches: nesepm is the outer midplane separatrix electron density. (See rzomp switch in b2.user.parameters for setting of midplane position). This is controlled through particle input of main plasma species isfeedback through the core boundary (See Geometry section for the core boundary indices coreregno and coreregn2).
					nesepm_sol is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the SOL region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the SOL North boundary (See Geometry section for the SOL North boundary index solregno). If nesepm_overshoot.gt.1.0, the gas puff is turned off when the midplane separatrix density reaches nesepm*nesepm_overshoot. Minimum and maximum values of the feedback gas puff can be set using b2stbc_nesepm_minpuff and b2stbc_nesepm_maxpuff. It will apply fb_type=3, fb_rescale=1, fb_actuator=1 on region defined by solregno.
					nepedm_sol is similar to nesepm_sol but the feedback is exerted on the electron density at the top of the pedestal, along the outer midplane, at the icped-th ring (where icped=iyped+2) counting from the inner core boundary. It will apply fb_type=16, fb_rescale=1, fb_actuator=1 on region defined by solregno.
					ndes_sol is the total particle content from the isonuclear sequence of species 'isfeedback' over the entire simulation domain. It is governed, like nesepm_sol, by nesepm_overshoot and nesepm_alpha and corresponds to a SOL boundary feedback. Will apply fb_type=14, fb_rescale=1, fb_actuator=1 on region defined by solregno. WARNING: in the structured code this switch was asking for BCCON=12, so density BC for fluid neutrals feedback but then it switches to gas  puff for kinetic neutrals. Now it is ONLY gaspuff.
					volrec_sol is the total particle source due to volume recombination coming from Eirene. Its feedback is governed by volrec_overshoot and volrec_alpha and volrec_beta parameters (See Numerics section for the latter two). Will apply fb_type=15, fb_rescale=1, fb_actuator=1 on region defined by pfrregno1. WARNING: not available yet for fluid neutrals.
					nesepm_pfr is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the PFR region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the PFR South boundary indices pfrregno1 and pfrregno2). will apply fb_type=3, fb_rescale=1, fb_actuator=1 on region defined pfrregno1
					ndes is the total particle (neutrals + ions) content of the species whose neutral species has index isfeedback. This is controlled through particle input of neutrals species isfeedback through the	private flux boundaries (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2). will apply fb_type=14, fb_rescale=1, fb_actuator=1 on region defined by pfrregno1. WARNING: in the structured code this switch was asking for BCCON=12, so density BC for fluid neutrals feedback but then it switches to gas puff for kinetic neutrals. Now it is ONLY gas puff.
					private_flux_puff NOT YET CONVERTED TO WG CODE! is the particle flow of species isfeedback through the private flux region boundary. This is controlled through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2).
					All but the first of these feedback schemes ("nesepm") can also be run though an Eirene neutral gas puff. In that case, one should set an appropriate gas puffing stratum in the Eirene input file input.dat, as well as in the b2.neutrals.parameters file. The code will assume, unless told otherwise through the use of "eirene_nesepm_istra", that the first stratum of type 'C' found in b2.neutrals.parameters is the stratum used for the feedback. If "eirene_nesepm_istra" is set to a positive number, the code will consider the feedback stratum to be the stratum in the "eirene_nesepm_istra"-th position in b2.neutrals.parameters.
					b2stbc_iyped is the index in the OMP CV list (defined with RZOMP in b2.user.parameters) of the pedestal cell (defaults to icsepomp/2).
				""", '-1'),
   
      'b2stbc_type13_ref' : ('', 'integer', """
					These switches are associated with the boundary condition of type 13, 16, 17, 20 or 21 for particle flux, or electron and ion energy fluxes, i.e. constant density or temperature giving a prescribed flux through a radial surface, located type13_ref or type16_ref radial steps away from the boundary of the computational domain, respectively, and applied type20_ref steps away. See code and description in b2cdcn for details.
					Type 21 also applies to the electric potential boundary condition.
					It scales the feedback strength according to the value of the variable on the ring type21_ref steps inside.
					When type16_ref.gt.1, then the position where the core flux tallies are computed moves along with the boundary condition.
					If type16_kinetic_energy.eq.1, then the parallel kinetic energy flux is included in the ion heat flux component of type 16 and 17 boundary conditions.
				""", '1'),
   
      'b2stbc_type16_ref' : ('', 'integer', """
					These switches are associated with the boundary condition of type 13, 16, 17, 20 or 21 for particle flux, or electron and ion energy fluxes, i.e. constant density or temperature giving a prescribed flux through a radial surface, located type13_ref or type16_ref radial steps away from the boundary of the computational domain, respectively, and applied type20_ref steps away. See code and description in b2cdcn for details.
					Type 21 also applies to the electric potential boundary condition.
					It scales the feedback strength according to the value of the variable on the ring type21_ref steps inside.
					When type16_ref.gt.1, then the position where the core flux tallies are computed moves along with the boundary condition.
					If type16_kinetic_energy.eq.1, then the parallel kinetic energy flux is included in the ion heat flux component of type 16 and 17 boundary conditions.
				""", '1'),
   
      'b2stbc_type20_ref' : ('', 'integer', """
					These switches are associated with the boundary condition of type 13, 16, 17, 20 or 21 for particle flux, or electron and ion energy fluxes, i.e. constant density or temperature giving a prescribed flux through a radial surface, located type13_ref or type16_ref radial steps away from the boundary of the computational domain, respectively, and applied type20_ref steps away. See code and description in b2cdcn for details.
					Type 21 also applies to the electric potential boundary condition.
					It scales the feedback strength according to the value of the variable on the ring type21_ref steps inside.
					When type16_ref.gt.1, then the position where the core flux tallies are computed moves along with the boundary condition.
					If type16_kinetic_energy.eq.1, then the parallel kinetic energy flux is included in the ion heat flux component of type 16 and 17 boundary conditions.
				""", '1'),
   
      'b2stbc_type21_ref' : ('', 'integer', """
					These switches are associated with the boundary condition of type 13, 16, 17, 20 or 21 for particle flux, or electron and ion energy fluxes, i.e. constant density or temperature giving a prescribed flux through a radial surface, located type13_ref or type16_ref radial steps away from the boundary of the computational domain, respectively, and applied type20_ref steps away. See code and description in b2cdcn for details.
					Type 21 also applies to the electric potential boundary condition.
					It scales the feedback strength according to the value of the variable on the ring type21_ref steps inside.
					When type16_ref.gt.1, then the position where the core flux tallies are computed moves along with the boundary condition.
					If type16_kinetic_energy.eq.1, then the parallel kinetic energy flux is included in the ion heat flux component of type 16 and 17 boundary conditions.
				""", '1'),
   
      'b2stbc_type16_kinetic_energy' : ('', 'integer', """
					These switches are associated with the boundary condition of type 13, 16, 17, 20 or 21 for particle flux, or electron and ion energy fluxes, i.e. constant density or temperature giving a prescribed flux through a radial surface, located type13_ref or type16_ref radial steps away from the boundary of the computational domain, respectively, and applied type20_ref steps away. See code and description in b2cdcn for details.
					Type 21 also applies to the electric potential boundary condition.
					It scales the feedback strength according to the value of the variable on the ring type21_ref steps inside.
					When type16_ref.gt.1, then the position where the core flux tallies are computed moves along with the boundary condition.
					If type16_kinetic_energy.eq.1, then the parallel kinetic energy flux is included in the ion heat flux component of type 16 and 17 boundary conditions.
				""", '0'),
   
      'b2mndr_use_mms' : ('', 'integer', """
					If use_mms.eq.1, specifies a run using the Method of Manufactured Solutions in steady-state mode (b2mndt_style.eq.1). If use_mms.eq.2, specifies a run using the Method of Manufactured Solutions in time-dependent mode (b2mndt_style.eq.2). The exact solutions to match are provided by the b2mndr_set_XX_numerical switches.
					An exact solution is available for comparison if the corresponding b2mndr_set_XX_numerical switch is nonzero. The exact solutions for steady-state are provided, respectively, in the exact_na.dat and exact_ne.dat, exact_ua.dat, exact_te.dat, exact_ti.dat, and exact_po.dat files. The exact solutions for time-dependent must be provided for each time-step: exact_XX0001.dat, exact_XX0002.dat, exact_XX0003.dat, and so on.
					The exact_na.dat and exact_ne.dat files must be provided simultaneously.
				""", '0'),
   
      'b2mndr_set_na_numerical' : ('', 'integer', """
					If use_mms.eq.1, specifies a run using the Method of Manufactured Solutions in steady-state mode (b2mndt_style.eq.1). If use_mms.eq.2, specifies a run using the Method of Manufactured Solutions in time-dependent mode (b2mndt_style.eq.2). The exact solutions to match are provided by the b2mndr_set_XX_numerical switches.
					An exact solution is available for comparison if the corresponding b2mndr_set_XX_numerical switch is nonzero. The exact solutions for steady-state are provided, respectively, in the exact_na.dat and exact_ne.dat, exact_ua.dat, exact_te.dat, exact_ti.dat, and exact_po.dat files. The exact solutions for time-dependent must be provided for each time-step: exact_XX0001.dat, exact_XX0002.dat, exact_XX0003.dat, and so on.
					The exact_na.dat and exact_ne.dat files must be provided simultaneously.
				""", '0'),
   
      'b2mndr_set_ua_numerical' : ('', 'integer', """
					If use_mms.eq.1, specifies a run using the Method of Manufactured Solutions in steady-state mode (b2mndt_style.eq.1). If use_mms.eq.2, specifies a run using the Method of Manufactured Solutions in time-dependent mode (b2mndt_style.eq.2). The exact solutions to match are provided by the b2mndr_set_XX_numerical switches.
					An exact solution is available for comparison if the corresponding b2mndr_set_XX_numerical switch is nonzero. The exact solutions for steady-state are provided, respectively, in the exact_na.dat and exact_ne.dat, exact_ua.dat, exact_te.dat, exact_ti.dat, and exact_po.dat files. The exact solutions for time-dependent must be provided for each time-step: exact_XX0001.dat, exact_XX0002.dat, exact_XX0003.dat, and so on.
					The exact_na.dat and exact_ne.dat files must be provided simultaneously.
				""", '0'),
   
      'b2mndr_set_te_numerical' : ('', 'integer', """
					If use_mms.eq.1, specifies a run using the Method of Manufactured Solutions in steady-state mode (b2mndt_style.eq.1). If use_mms.eq.2, specifies a run using the Method of Manufactured Solutions in time-dependent mode (b2mndt_style.eq.2). The exact solutions to match are provided by the b2mndr_set_XX_numerical switches.
					An exact solution is available for comparison if the corresponding b2mndr_set_XX_numerical switch is nonzero. The exact solutions for steady-state are provided, respectively, in the exact_na.dat and exact_ne.dat, exact_ua.dat, exact_te.dat, exact_ti.dat, and exact_po.dat files. The exact solutions for time-dependent must be provided for each time-step: exact_XX0001.dat, exact_XX0002.dat, exact_XX0003.dat, and so on.
					The exact_na.dat and exact_ne.dat files must be provided simultaneously.
				""", '0'),
   
      'b2mndr_set_ti_numerical' : ('', 'integer', """
					If use_mms.eq.1, specifies a run using the Method of Manufactured Solutions in steady-state mode (b2mndt_style.eq.1). If use_mms.eq.2, specifies a run using the Method of Manufactured Solutions in time-dependent mode (b2mndt_style.eq.2). The exact solutions to match are provided by the b2mndr_set_XX_numerical switches.
					An exact solution is available for comparison if the corresponding b2mndr_set_XX_numerical switch is nonzero. The exact solutions for steady-state are provided, respectively, in the exact_na.dat and exact_ne.dat, exact_ua.dat, exact_te.dat, exact_ti.dat, and exact_po.dat files. The exact solutions for time-dependent must be provided for each time-step: exact_XX0001.dat, exact_XX0002.dat, exact_XX0003.dat, and so on.
					The exact_na.dat and exact_ne.dat files must be provided simultaneously.
				""", '0'),
   
      'b2mndr_set_tn_numerical' : ('', 'integer', """
					If use_mms.eq.1, specifies a run using the Method of Manufactured Solutions in steady-state mode (b2mndt_style.eq.1). If use_mms.eq.2, specifies a run using the Method of Manufactured Solutions in time-dependent mode (b2mndt_style.eq.2). The exact solutions to match are provided by the b2mndr_set_XX_numerical switches.
					An exact solution is available for comparison if the corresponding b2mndr_set_XX_numerical switch is nonzero. The exact solutions for steady-state are provided, respectively, in the exact_na.dat and exact_ne.dat, exact_ua.dat, exact_te.dat, exact_ti.dat, and exact_po.dat files. The exact solutions for time-dependent must be provided for each time-step: exact_XX0001.dat, exact_XX0002.dat, exact_XX0003.dat, and so on.
					The exact_na.dat and exact_ne.dat files must be provided simultaneously.
				""", '0'),
   
      'b2mndr_set_po_numerical' : ('', 'integer', """
					If use_mms.eq.1, specifies a run using the Method of Manufactured Solutions in steady-state mode (b2mndt_style.eq.1). If use_mms.eq.2, specifies a run using the Method of Manufactured Solutions in time-dependent mode (b2mndt_style.eq.2). The exact solutions to match are provided by the b2mndr_set_XX_numerical switches.
					An exact solution is available for comparison if the corresponding b2mndr_set_XX_numerical switch is nonzero. The exact solutions for steady-state are provided, respectively, in the exact_na.dat and exact_ne.dat, exact_ua.dat, exact_te.dat, exact_ti.dat, and exact_po.dat files. The exact solutions for time-dependent must be provided for each time-step: exact_XX0001.dat, exact_XX0002.dat, exact_XX0003.dat, and so on.
					The exact_na.dat and exact_ne.dat files must be provided simultaneously.
				""", '0'),
   
      'b2stbr_plate_model' : ('', 'integer', """
					Sputtering model switches. Not yet available for WG. See the code in b2stbr and the b2mod_sputter module for specific implementation details and references.
					The default values represent the case of Graphite plates. Sput_src is the atomic number of the plasma species which causes chemical sputtering.
					Sput_dst (when .ge.0) is the species index of the destination species produced by physical sputtering, chemical sputtering and/or RES. If either of the latter two processes are included, the chemical sputtering and RES production rate calculations provided in the code assume that sput_dst points to a Carbon species.
					Sput_dst2 and sput_dst3 (when .ge.0) represent other species produced by wall interactions for mixed materials scenarios.
					Sput_frac_flag is the switch to turn on mixed materials scenarios (when sput_frac_flag.eq.1).
					Plate_model.eq.0 means the 0-D time-independent plate heating model while plate_model.eq.1 indicates the 1-D time-dependent plate heating treatment. Plate_model.eq.2 gives acces to a 2-D time-dependent model. Plate_option chooses the initialisation of the plate temperature profile. If plate_option.eq.1, the profile is set to the constant given in plate_temp. If plate_option.eq.2, the profile is computed to be the 0-D equilibrium profile. If plate_option.eq.3, the profile is read from results of the previous run.
					Sput_phys_model is a switch for choosing between the TRIM tables (model 1, default) or an empirical formula (model 0). When TRIM data is not available, the empirical formula is automatically used. Extrapolations of low and high energy ranges beyond the TRIM table data is done using the same physical dependencies as the empirical formula. Sput_chem_model is a switch for the chemical sputtering model used.
					If sput_chem_model.eq.0 (default), the empirical formula is used.
					If sput_chem_model.eq.1, a constant with a low energy cut-off is used.
					The cutoff occurs at approximately sput_chem_cutoff_alpha and the width is determined by sput_chem_cutoff_beta (the larger the value, the narrower the width over which the transition from 0 to 1 occurs).
					For model 0, sput_frc is a multiplier to the empirical formula, while for model 1, sput_frc is the constant chemical sputtering yield.
					Sput_frc is superseded by the chem_sput array from b2.neutrals.namelist if the latter is used.
					For neutrals species, we add a factor of α*na*vbar to the particle flux to the plate (used to compute chemical and RES sputtering), where vbar is the average neutral particle speed.
					Sput_phys turns on physical sputtering when sput_phys.gt.0.0 and contains a (real) multiplier for the physical sputtering rate looked up in the TRIM tables. It is superseded by the phys_sput array in b2.neutrals.parameters if the latter is used.
					sput_phys_col indicates which column to use in the TRIM table; the default (3) corresponds to 30 degrees incidence. The columns are for
					  0 15 30 45 55 65 75 80 85
					degrees. This angle is also used in the empirical formula. Plate_temp is the temperature (in Kelvin) of the COOLED end of the divertor plates. The surface temperature is computed self-consistently (using a 1-D description) according to the incident heat fluxes from the plasma. The plate is assumed to have a thickness of plate_thick, measured in metres. When plate_thick.eq.0 (default), the plate surface temperature is assumed to be the same as plate_temp. Sput_res turns on radiation enhanced sublimation (RES) when .gt.0.0 and is a multiplier to the RES rate.
					The switch sputter_energy_on turns on the energy contribution from the sputtered particles (physical and chemical). If sputter_energy_on.eq.0, the particles are sputtered cold, with no energy contribution to the ion heat equation.
					If sputter_energy_on.ne.0 (default), the chemically sputtered particles are re-introduced into the plasma with the thermal energy corresponding to the surface temperature of the material, while physically sputtered particles are re-introduced with the TRIM-calculated energy sputtering yield (if the TRIM model is used).
					Therm_evap turns on thermal evaporation when .gt.0.0 and is a multiplier to the thermal evaporation rate.
					Redep_alpha is the multiplier to the reduction of the sputtering yield due to prompt redeposition. The promptly redeposited species is counted as eroded-then-deposited species.
				""", '0'),
   
      'b2stbr_plate_option' : ('', 'integer', """
					Sputtering model switches. Not yet available for WG. See the code in b2stbr and the b2mod_sputter module for specific implementation details and references.
					The default values represent the case of Graphite plates. Sput_src is the atomic number of the plasma species which causes chemical sputtering.
					Sput_dst (when .ge.0) is the species index of the destination species produced by physical sputtering, chemical sputtering and/or RES. If either of the latter two processes are included, the chemical sputtering and RES production rate calculations provided in the code assume that sput_dst points to a Carbon species.
					Sput_dst2 and sput_dst3 (when .ge.0) represent other species produced by wall interactions for mixed materials scenarios.
					Sput_frac_flag is the switch to turn on mixed materials scenarios (when sput_frac_flag.eq.1).
					Plate_model.eq.0 means the 0-D time-independent plate heating model while plate_model.eq.1 indicates the 1-D time-dependent plate heating treatment. Plate_model.eq.2 gives acces to a 2-D time-dependent model. Plate_option chooses the initialisation of the plate temperature profile. If plate_option.eq.1, the profile is set to the constant given in plate_temp. If plate_option.eq.2, the profile is computed to be the 0-D equilibrium profile. If plate_option.eq.3, the profile is read from results of the previous run.
					Sput_phys_model is a switch for choosing between the TRIM tables (model 1, default) or an empirical formula (model 0). When TRIM data is not available, the empirical formula is automatically used. Extrapolations of low and high energy ranges beyond the TRIM table data is done using the same physical dependencies as the empirical formula. Sput_chem_model is a switch for the chemical sputtering model used.
					If sput_chem_model.eq.0 (default), the empirical formula is used.
					If sput_chem_model.eq.1, a constant with a low energy cut-off is used.
					The cutoff occurs at approximately sput_chem_cutoff_alpha and the width is determined by sput_chem_cutoff_beta (the larger the value, the narrower the width over which the transition from 0 to 1 occurs).
					For model 0, sput_frc is a multiplier to the empirical formula, while for model 1, sput_frc is the constant chemical sputtering yield.
					Sput_frc is superseded by the chem_sput array from b2.neutrals.namelist if the latter is used.
					For neutrals species, we add a factor of α*na*vbar to the particle flux to the plate (used to compute chemical and RES sputtering), where vbar is the average neutral particle speed.
					Sput_phys turns on physical sputtering when sput_phys.gt.0.0 and contains a (real) multiplier for the physical sputtering rate looked up in the TRIM tables. It is superseded by the phys_sput array in b2.neutrals.parameters if the latter is used.
					sput_phys_col indicates which column to use in the TRIM table; the default (3) corresponds to 30 degrees incidence. The columns are for
					  0 15 30 45 55 65 75 80 85
					degrees. This angle is also used in the empirical formula. Plate_temp is the temperature (in Kelvin) of the COOLED end of the divertor plates. The surface temperature is computed self-consistently (using a 1-D description) according to the incident heat fluxes from the plasma. The plate is assumed to have a thickness of plate_thick, measured in metres. When plate_thick.eq.0 (default), the plate surface temperature is assumed to be the same as plate_temp. Sput_res turns on radiation enhanced sublimation (RES) when .gt.0.0 and is a multiplier to the RES rate.
					The switch sputter_energy_on turns on the energy contribution from the sputtered particles (physical and chemical). If sputter_energy_on.eq.0, the particles are sputtered cold, with no energy contribution to the ion heat equation.
					If sputter_energy_on.ne.0 (default), the chemically sputtered particles are re-introduced into the plasma with the thermal energy corresponding to the surface temperature of the material, while physically sputtered particles are re-introduced with the TRIM-calculated energy sputtering yield (if the TRIM model is used).
					Therm_evap turns on thermal evaporation when .gt.0.0 and is a multiplier to the thermal evaporation rate.
					Redep_alpha is the multiplier to the reduction of the sputtering yield due to prompt redeposition. The promptly redeposited species is counted as eroded-then-deposited species.
				""", '3'),
   
      'b2stbr_sput_chem_model' : ('', 'integer', """
					Sputtering model switches. Not yet available for WG. See the code in b2stbr and the b2mod_sputter module for specific implementation details and references.
					The default values represent the case of Graphite plates. Sput_src is the atomic number of the plasma species which causes chemical sputtering.
					Sput_dst (when .ge.0) is the species index of the destination species produced by physical sputtering, chemical sputtering and/or RES. If either of the latter two processes are included, the chemical sputtering and RES production rate calculations provided in the code assume that sput_dst points to a Carbon species.
					Sput_dst2 and sput_dst3 (when .ge.0) represent other species produced by wall interactions for mixed materials scenarios.
					Sput_frac_flag is the switch to turn on mixed materials scenarios (when sput_frac_flag.eq.1).
					Plate_model.eq.0 means the 0-D time-independent plate heating model while plate_model.eq.1 indicates the 1-D time-dependent plate heating treatment. Plate_model.eq.2 gives acces to a 2-D time-dependent model. Plate_option chooses the initialisation of the plate temperature profile. If plate_option.eq.1, the profile is set to the constant given in plate_temp. If plate_option.eq.2, the profile is computed to be the 0-D equilibrium profile. If plate_option.eq.3, the profile is read from results of the previous run.
					Sput_phys_model is a switch for choosing between the TRIM tables (model 1, default) or an empirical formula (model 0). When TRIM data is not available, the empirical formula is automatically used. Extrapolations of low and high energy ranges beyond the TRIM table data is done using the same physical dependencies as the empirical formula. Sput_chem_model is a switch for the chemical sputtering model used.
					If sput_chem_model.eq.0 (default), the empirical formula is used.
					If sput_chem_model.eq.1, a constant with a low energy cut-off is used.
					The cutoff occurs at approximately sput_chem_cutoff_alpha and the width is determined by sput_chem_cutoff_beta (the larger the value, the narrower the width over which the transition from 0 to 1 occurs).
					For model 0, sput_frc is a multiplier to the empirical formula, while for model 1, sput_frc is the constant chemical sputtering yield.
					Sput_frc is superseded by the chem_sput array from b2.neutrals.namelist if the latter is used.
					For neutrals species, we add a factor of α*na*vbar to the particle flux to the plate (used to compute chemical and RES sputtering), where vbar is the average neutral particle speed.
					Sput_phys turns on physical sputtering when sput_phys.gt.0.0 and contains a (real) multiplier for the physical sputtering rate looked up in the TRIM tables. It is superseded by the phys_sput array in b2.neutrals.parameters if the latter is used.
					sput_phys_col indicates which column to use in the TRIM table; the default (3) corresponds to 30 degrees incidence. The columns are for
					  0 15 30 45 55 65 75 80 85
					degrees. This angle is also used in the empirical formula. Plate_temp is the temperature (in Kelvin) of the COOLED end of the divertor plates. The surface temperature is computed self-consistently (using a 1-D description) according to the incident heat fluxes from the plasma. The plate is assumed to have a thickness of plate_thick, measured in metres. When plate_thick.eq.0 (default), the plate surface temperature is assumed to be the same as plate_temp. Sput_res turns on radiation enhanced sublimation (RES) when .gt.0.0 and is a multiplier to the RES rate.
					The switch sputter_energy_on turns on the energy contribution from the sputtered particles (physical and chemical). If sputter_energy_on.eq.0, the particles are sputtered cold, with no energy contribution to the ion heat equation.
					If sputter_energy_on.ne.0 (default), the chemically sputtered particles are re-introduced into the plasma with the thermal energy corresponding to the surface temperature of the material, while physically sputtered particles are re-introduced with the TRIM-calculated energy sputtering yield (if the TRIM model is used).
					Therm_evap turns on thermal evaporation when .gt.0.0 and is a multiplier to the thermal evaporation rate.
					Redep_alpha is the multiplier to the reduction of the sputtering yield due to prompt redeposition. The promptly redeposited species is counted as eroded-then-deposited species.
				""", '0'),
   
      'b2stbr_sput_chem_cutoff_alpha' : ('', 'real', """
					Sputtering model switches. Not yet available for WG. See the code in b2stbr and the b2mod_sputter module for specific implementation details and references.
					The default values represent the case of Graphite plates. Sput_src is the atomic number of the plasma species which causes chemical sputtering.
					Sput_dst (when .ge.0) is the species index of the destination species produced by physical sputtering, chemical sputtering and/or RES. If either of the latter two processes are included, the chemical sputtering and RES production rate calculations provided in the code assume that sput_dst points to a Carbon species.
					Sput_dst2 and sput_dst3 (when .ge.0) represent other species produced by wall interactions for mixed materials scenarios.
					Sput_frac_flag is the switch to turn on mixed materials scenarios (when sput_frac_flag.eq.1).
					Plate_model.eq.0 means the 0-D time-independent plate heating model while plate_model.eq.1 indicates the 1-D time-dependent plate heating treatment. Plate_model.eq.2 gives acces to a 2-D time-dependent model. Plate_option chooses the initialisation of the plate temperature profile. If plate_option.eq.1, the profile is set to the constant given in plate_temp. If plate_option.eq.2, the profile is computed to be the 0-D equilibrium profile. If plate_option.eq.3, the profile is read from results of the previous run.
					Sput_phys_model is a switch for choosing between the TRIM tables (model 1, default) or an empirical formula (model 0). When TRIM data is not available, the empirical formula is automatically used. Extrapolations of low and high energy ranges beyond the TRIM table data is done using the same physical dependencies as the empirical formula. Sput_chem_model is a switch for the chemical sputtering model used.
					If sput_chem_model.eq.0 (default), the empirical formula is used.
					If sput_chem_model.eq.1, a constant with a low energy cut-off is used.
					The cutoff occurs at approximately sput_chem_cutoff_alpha and the width is determined by sput_chem_cutoff_beta (the larger the value, the narrower the width over which the transition from 0 to 1 occurs).
					For model 0, sput_frc is a multiplier to the empirical formula, while for model 1, sput_frc is the constant chemical sputtering yield.
					Sput_frc is superseded by the chem_sput array from b2.neutrals.namelist if the latter is used.
					For neutrals species, we add a factor of α*na*vbar to the particle flux to the plate (used to compute chemical and RES sputtering), where vbar is the average neutral particle speed.
					Sput_phys turns on physical sputtering when sput_phys.gt.0.0 and contains a (real) multiplier for the physical sputtering rate looked up in the TRIM tables. It is superseded by the phys_sput array in b2.neutrals.parameters if the latter is used.
					sput_phys_col indicates which column to use in the TRIM table; the default (3) corresponds to 30 degrees incidence. The columns are for
					  0 15 30 45 55 65 75 80 85
					degrees. This angle is also used in the empirical formula. Plate_temp is the temperature (in Kelvin) of the COOLED end of the divertor plates. The surface temperature is computed self-consistently (using a 1-D description) according to the incident heat fluxes from the plasma. The plate is assumed to have a thickness of plate_thick, measured in metres. When plate_thick.eq.0 (default), the plate surface temperature is assumed to be the same as plate_temp. Sput_res turns on radiation enhanced sublimation (RES) when .gt.0.0 and is a multiplier to the RES rate.
					The switch sputter_energy_on turns on the energy contribution from the sputtered particles (physical and chemical). If sputter_energy_on.eq.0, the particles are sputtered cold, with no energy contribution to the ion heat equation.
					If sputter_energy_on.ne.0 (default), the chemically sputtered particles are re-introduced into the plasma with the thermal energy corresponding to the surface temperature of the material, while physically sputtered particles are re-introduced with the TRIM-calculated energy sputtering yield (if the TRIM model is used).
					Therm_evap turns on thermal evaporation when .gt.0.0 and is a multiplier to the thermal evaporation rate.
					Redep_alpha is the multiplier to the reduction of the sputtering yield due to prompt redeposition. The promptly redeposited species is counted as eroded-then-deposited species.
				""", '1.0'),
   
      'b2stbr_sput_chem_cutoff_beta' : ('', 'real', """
					Sputtering model switches. Not yet available for WG. See the code in b2stbr and the b2mod_sputter module for specific implementation details and references.
					The default values represent the case of Graphite plates. Sput_src is the atomic number of the plasma species which causes chemical sputtering.
					Sput_dst (when .ge.0) is the species index of the destination species produced by physical sputtering, chemical sputtering and/or RES. If either of the latter two processes are included, the chemical sputtering and RES production rate calculations provided in the code assume that sput_dst points to a Carbon species.
					Sput_dst2 and sput_dst3 (when .ge.0) represent other species produced by wall interactions for mixed materials scenarios.
					Sput_frac_flag is the switch to turn on mixed materials scenarios (when sput_frac_flag.eq.1).
					Plate_model.eq.0 means the 0-D time-independent plate heating model while plate_model.eq.1 indicates the 1-D time-dependent plate heating treatment. Plate_model.eq.2 gives acces to a 2-D time-dependent model. Plate_option chooses the initialisation of the plate temperature profile. If plate_option.eq.1, the profile is set to the constant given in plate_temp. If plate_option.eq.2, the profile is computed to be the 0-D equilibrium profile. If plate_option.eq.3, the profile is read from results of the previous run.
					Sput_phys_model is a switch for choosing between the TRIM tables (model 1, default) or an empirical formula (model 0). When TRIM data is not available, the empirical formula is automatically used. Extrapolations of low and high energy ranges beyond the TRIM table data is done using the same physical dependencies as the empirical formula. Sput_chem_model is a switch for the chemical sputtering model used.
					If sput_chem_model.eq.0 (default), the empirical formula is used.
					If sput_chem_model.eq.1, a constant with a low energy cut-off is used.
					The cutoff occurs at approximately sput_chem_cutoff_alpha and the width is determined by sput_chem_cutoff_beta (the larger the value, the narrower the width over which the transition from 0 to 1 occurs).
					For model 0, sput_frc is a multiplier to the empirical formula, while for model 1, sput_frc is the constant chemical sputtering yield.
					Sput_frc is superseded by the chem_sput array from b2.neutrals.namelist if the latter is used.
					For neutrals species, we add a factor of α*na*vbar to the particle flux to the plate (used to compute chemical and RES sputtering), where vbar is the average neutral particle speed.
					Sput_phys turns on physical sputtering when sput_phys.gt.0.0 and contains a (real) multiplier for the physical sputtering rate looked up in the TRIM tables. It is superseded by the phys_sput array in b2.neutrals.parameters if the latter is used.
					sput_phys_col indicates which column to use in the TRIM table; the default (3) corresponds to 30 degrees incidence. The columns are for
					  0 15 30 45 55 65 75 80 85
					degrees. This angle is also used in the empirical formula. Plate_temp is the temperature (in Kelvin) of the COOLED end of the divertor plates. The surface temperature is computed self-consistently (using a 1-D description) according to the incident heat fluxes from the plasma. The plate is assumed to have a thickness of plate_thick, measured in metres. When plate_thick.eq.0 (default), the plate surface temperature is assumed to be the same as plate_temp. Sput_res turns on radiation enhanced sublimation (RES) when .gt.0.0 and is a multiplier to the RES rate.
					The switch sputter_energy_on turns on the energy contribution from the sputtered particles (physical and chemical). If sputter_energy_on.eq.0, the particles are sputtered cold, with no energy contribution to the ion heat equation.
					If sputter_energy_on.ne.0 (default), the chemically sputtered particles are re-introduced into the plasma with the thermal energy corresponding to the surface temperature of the material, while physically sputtered particles are re-introduced with the TRIM-calculated energy sputtering yield (if the TRIM model is used).
					Therm_evap turns on thermal evaporation when .gt.0.0 and is a multiplier to the thermal evaporation rate.
					Redep_alpha is the multiplier to the reduction of the sputtering yield due to prompt redeposition. The promptly redeposited species is counted as eroded-then-deposited species.
				""", '3.0'),
   
      'b2stbr_sput_mixed_alpha' : ('', 'real', """
					Sputtering model switches. Not yet available for WG. See the code in b2stbr and the b2mod_sputter module for specific implementation details and references.
					The default values represent the case of Graphite plates. Sput_src is the atomic number of the plasma species which causes chemical sputtering.
					Sput_dst (when .ge.0) is the species index of the destination species produced by physical sputtering, chemical sputtering and/or RES. If either of the latter two processes are included, the chemical sputtering and RES production rate calculations provided in the code assume that sput_dst points to a Carbon species.
					Sput_dst2 and sput_dst3 (when .ge.0) represent other species produced by wall interactions for mixed materials scenarios.
					Sput_frac_flag is the switch to turn on mixed materials scenarios (when sput_frac_flag.eq.1).
					Plate_model.eq.0 means the 0-D time-independent plate heating model while plate_model.eq.1 indicates the 1-D time-dependent plate heating treatment. Plate_model.eq.2 gives acces to a 2-D time-dependent model. Plate_option chooses the initialisation of the plate temperature profile. If plate_option.eq.1, the profile is set to the constant given in plate_temp. If plate_option.eq.2, the profile is computed to be the 0-D equilibrium profile. If plate_option.eq.3, the profile is read from results of the previous run.
					Sput_phys_model is a switch for choosing between the TRIM tables (model 1, default) or an empirical formula (model 0). When TRIM data is not available, the empirical formula is automatically used. Extrapolations of low and high energy ranges beyond the TRIM table data is done using the same physical dependencies as the empirical formula. Sput_chem_model is a switch for the chemical sputtering model used.
					If sput_chem_model.eq.0 (default), the empirical formula is used.
					If sput_chem_model.eq.1, a constant with a low energy cut-off is used.
					The cutoff occurs at approximately sput_chem_cutoff_alpha and the width is determined by sput_chem_cutoff_beta (the larger the value, the narrower the width over which the transition from 0 to 1 occurs).
					For model 0, sput_frc is a multiplier to the empirical formula, while for model 1, sput_frc is the constant chemical sputtering yield.
					Sput_frc is superseded by the chem_sput array from b2.neutrals.namelist if the latter is used.
					For neutrals species, we add a factor of α*na*vbar to the particle flux to the plate (used to compute chemical and RES sputtering), where vbar is the average neutral particle speed.
					Sput_phys turns on physical sputtering when sput_phys.gt.0.0 and contains a (real) multiplier for the physical sputtering rate looked up in the TRIM tables. It is superseded by the phys_sput array in b2.neutrals.parameters if the latter is used.
					sput_phys_col indicates which column to use in the TRIM table; the default (3) corresponds to 30 degrees incidence. The columns are for
					  0 15 30 45 55 65 75 80 85
					degrees. This angle is also used in the empirical formula. Plate_temp is the temperature (in Kelvin) of the COOLED end of the divertor plates. The surface temperature is computed self-consistently (using a 1-D description) according to the incident heat fluxes from the plasma. The plate is assumed to have a thickness of plate_thick, measured in metres. When plate_thick.eq.0 (default), the plate surface temperature is assumed to be the same as plate_temp. Sput_res turns on radiation enhanced sublimation (RES) when .gt.0.0 and is a multiplier to the RES rate.
					The switch sputter_energy_on turns on the energy contribution from the sputtered particles (physical and chemical). If sputter_energy_on.eq.0, the particles are sputtered cold, with no energy contribution to the ion heat equation.
					If sputter_energy_on.ne.0 (default), the chemically sputtered particles are re-introduced into the plasma with the thermal energy corresponding to the surface temperature of the material, while physically sputtered particles are re-introduced with the TRIM-calculated energy sputtering yield (if the TRIM model is used).
					Therm_evap turns on thermal evaporation when .gt.0.0 and is a multiplier to the thermal evaporation rate.
					Redep_alpha is the multiplier to the reduction of the sputtering yield due to prompt redeposition. The promptly redeposited species is counted as eroded-then-deposited species.
				""", '1.0'),
   
      'b2stbr_sput_mixed_beta' : ('', 'real', """
					Sputtering model switches. Not yet available for WG. See the code in b2stbr and the b2mod_sputter module for specific implementation details and references.
					The default values represent the case of Graphite plates. Sput_src is the atomic number of the plasma species which causes chemical sputtering.
					Sput_dst (when .ge.0) is the species index of the destination species produced by physical sputtering, chemical sputtering and/or RES. If either of the latter two processes are included, the chemical sputtering and RES production rate calculations provided in the code assume that sput_dst points to a Carbon species.
					Sput_dst2 and sput_dst3 (when .ge.0) represent other species produced by wall interactions for mixed materials scenarios.
					Sput_frac_flag is the switch to turn on mixed materials scenarios (when sput_frac_flag.eq.1).
					Plate_model.eq.0 means the 0-D time-independent plate heating model while plate_model.eq.1 indicates the 1-D time-dependent plate heating treatment. Plate_model.eq.2 gives acces to a 2-D time-dependent model. Plate_option chooses the initialisation of the plate temperature profile. If plate_option.eq.1, the profile is set to the constant given in plate_temp. If plate_option.eq.2, the profile is computed to be the 0-D equilibrium profile. If plate_option.eq.3, the profile is read from results of the previous run.
					Sput_phys_model is a switch for choosing between the TRIM tables (model 1, default) or an empirical formula (model 0). When TRIM data is not available, the empirical formula is automatically used. Extrapolations of low and high energy ranges beyond the TRIM table data is done using the same physical dependencies as the empirical formula. Sput_chem_model is a switch for the chemical sputtering model used.
					If sput_chem_model.eq.0 (default), the empirical formula is used.
					If sput_chem_model.eq.1, a constant with a low energy cut-off is used.
					The cutoff occurs at approximately sput_chem_cutoff_alpha and the width is determined by sput_chem_cutoff_beta (the larger the value, the narrower the width over which the transition from 0 to 1 occurs).
					For model 0, sput_frc is a multiplier to the empirical formula, while for model 1, sput_frc is the constant chemical sputtering yield.
					Sput_frc is superseded by the chem_sput array from b2.neutrals.namelist if the latter is used.
					For neutrals species, we add a factor of α*na*vbar to the particle flux to the plate (used to compute chemical and RES sputtering), where vbar is the average neutral particle speed.
					Sput_phys turns on physical sputtering when sput_phys.gt.0.0 and contains a (real) multiplier for the physical sputtering rate looked up in the TRIM tables. It is superseded by the phys_sput array in b2.neutrals.parameters if the latter is used.
					sput_phys_col indicates which column to use in the TRIM table; the default (3) corresponds to 30 degrees incidence. The columns are for
					  0 15 30 45 55 65 75 80 85
					degrees. This angle is also used in the empirical formula. Plate_temp is the temperature (in Kelvin) of the COOLED end of the divertor plates. The surface temperature is computed self-consistently (using a 1-D description) according to the incident heat fluxes from the plasma. The plate is assumed to have a thickness of plate_thick, measured in metres. When plate_thick.eq.0 (default), the plate surface temperature is assumed to be the same as plate_temp. Sput_res turns on radiation enhanced sublimation (RES) when .gt.0.0 and is a multiplier to the RES rate.
					The switch sputter_energy_on turns on the energy contribution from the sputtered particles (physical and chemical). If sputter_energy_on.eq.0, the particles are sputtered cold, with no energy contribution to the ion heat equation.
					If sputter_energy_on.ne.0 (default), the chemically sputtered particles are re-introduced into the plasma with the thermal energy corresponding to the surface temperature of the material, while physically sputtered particles are re-introduced with the TRIM-calculated energy sputtering yield (if the TRIM model is used).
					Therm_evap turns on thermal evaporation when .gt.0.0 and is a multiplier to the thermal evaporation rate.
					Redep_alpha is the multiplier to the reduction of the sputtering yield due to prompt redeposition. The promptly redeposited species is counted as eroded-then-deposited species.
				""", '1.0'),
   
      'b2stbr_sput_phys_model' : ('', 'integer', """
					Sputtering model switches. Not yet available for WG. See the code in b2stbr and the b2mod_sputter module for specific implementation details and references.
					The default values represent the case of Graphite plates. Sput_src is the atomic number of the plasma species which causes chemical sputtering.
					Sput_dst (when .ge.0) is the species index of the destination species produced by physical sputtering, chemical sputtering and/or RES. If either of the latter two processes are included, the chemical sputtering and RES production rate calculations provided in the code assume that sput_dst points to a Carbon species.
					Sput_dst2 and sput_dst3 (when .ge.0) represent other species produced by wall interactions for mixed materials scenarios.
					Sput_frac_flag is the switch to turn on mixed materials scenarios (when sput_frac_flag.eq.1).
					Plate_model.eq.0 means the 0-D time-independent plate heating model while plate_model.eq.1 indicates the 1-D time-dependent plate heating treatment. Plate_model.eq.2 gives acces to a 2-D time-dependent model. Plate_option chooses the initialisation of the plate temperature profile. If plate_option.eq.1, the profile is set to the constant given in plate_temp. If plate_option.eq.2, the profile is computed to be the 0-D equilibrium profile. If plate_option.eq.3, the profile is read from results of the previous run.
					Sput_phys_model is a switch for choosing between the TRIM tables (model 1, default) or an empirical formula (model 0). When TRIM data is not available, the empirical formula is automatically used. Extrapolations of low and high energy ranges beyond the TRIM table data is done using the same physical dependencies as the empirical formula. Sput_chem_model is a switch for the chemical sputtering model used.
					If sput_chem_model.eq.0 (default), the empirical formula is used.
					If sput_chem_model.eq.1, a constant with a low energy cut-off is used.
					The cutoff occurs at approximately sput_chem_cutoff_alpha and the width is determined by sput_chem_cutoff_beta (the larger the value, the narrower the width over which the transition from 0 to 1 occurs).
					For model 0, sput_frc is a multiplier to the empirical formula, while for model 1, sput_frc is the constant chemical sputtering yield.
					Sput_frc is superseded by the chem_sput array from b2.neutrals.namelist if the latter is used.
					For neutrals species, we add a factor of α*na*vbar to the particle flux to the plate (used to compute chemical and RES sputtering), where vbar is the average neutral particle speed.
					Sput_phys turns on physical sputtering when sput_phys.gt.0.0 and contains a (real) multiplier for the physical sputtering rate looked up in the TRIM tables. It is superseded by the phys_sput array in b2.neutrals.parameters if the latter is used.
					sput_phys_col indicates which column to use in the TRIM table; the default (3) corresponds to 30 degrees incidence. The columns are for
					  0 15 30 45 55 65 75 80 85
					degrees. This angle is also used in the empirical formula. Plate_temp is the temperature (in Kelvin) of the COOLED end of the divertor plates. The surface temperature is computed self-consistently (using a 1-D description) according to the incident heat fluxes from the plasma. The plate is assumed to have a thickness of plate_thick, measured in metres. When plate_thick.eq.0 (default), the plate surface temperature is assumed to be the same as plate_temp. Sput_res turns on radiation enhanced sublimation (RES) when .gt.0.0 and is a multiplier to the RES rate.
					The switch sputter_energy_on turns on the energy contribution from the sputtered particles (physical and chemical). If sputter_energy_on.eq.0, the particles are sputtered cold, with no energy contribution to the ion heat equation.
					If sputter_energy_on.ne.0 (default), the chemically sputtered particles are re-introduced into the plasma with the thermal energy corresponding to the surface temperature of the material, while physically sputtered particles are re-introduced with the TRIM-calculated energy sputtering yield (if the TRIM model is used).
					Therm_evap turns on thermal evaporation when .gt.0.0 and is a multiplier to the thermal evaporation rate.
					Redep_alpha is the multiplier to the reduction of the sputtering yield due to prompt redeposition. The promptly redeposited species is counted as eroded-then-deposited species.
				""", '1'),
   
      'b2stbr_sputter_energy_on' : ('', 'integer', """
					Sputtering model switches. Not yet available for WG. See the code in b2stbr and the b2mod_sputter module for specific implementation details and references.
					The default values represent the case of Graphite plates. Sput_src is the atomic number of the plasma species which causes chemical sputtering.
					Sput_dst (when .ge.0) is the species index of the destination species produced by physical sputtering, chemical sputtering and/or RES. If either of the latter two processes are included, the chemical sputtering and RES production rate calculations provided in the code assume that sput_dst points to a Carbon species.
					Sput_dst2 and sput_dst3 (when .ge.0) represent other species produced by wall interactions for mixed materials scenarios.
					Sput_frac_flag is the switch to turn on mixed materials scenarios (when sput_frac_flag.eq.1).
					Plate_model.eq.0 means the 0-D time-independent plate heating model while plate_model.eq.1 indicates the 1-D time-dependent plate heating treatment. Plate_model.eq.2 gives acces to a 2-D time-dependent model. Plate_option chooses the initialisation of the plate temperature profile. If plate_option.eq.1, the profile is set to the constant given in plate_temp. If plate_option.eq.2, the profile is computed to be the 0-D equilibrium profile. If plate_option.eq.3, the profile is read from results of the previous run.
					Sput_phys_model is a switch for choosing between the TRIM tables (model 1, default) or an empirical formula (model 0). When TRIM data is not available, the empirical formula is automatically used. Extrapolations of low and high energy ranges beyond the TRIM table data is done using the same physical dependencies as the empirical formula. Sput_chem_model is a switch for the chemical sputtering model used.
					If sput_chem_model.eq.0 (default), the empirical formula is used.
					If sput_chem_model.eq.1, a constant with a low energy cut-off is used.
					The cutoff occurs at approximately sput_chem_cutoff_alpha and the width is determined by sput_chem_cutoff_beta (the larger the value, the narrower the width over which the transition from 0 to 1 occurs).
					For model 0, sput_frc is a multiplier to the empirical formula, while for model 1, sput_frc is the constant chemical sputtering yield.
					Sput_frc is superseded by the chem_sput array from b2.neutrals.namelist if the latter is used.
					For neutrals species, we add a factor of α*na*vbar to the particle flux to the plate (used to compute chemical and RES sputtering), where vbar is the average neutral particle speed.
					Sput_phys turns on physical sputtering when sput_phys.gt.0.0 and contains a (real) multiplier for the physical sputtering rate looked up in the TRIM tables. It is superseded by the phys_sput array in b2.neutrals.parameters if the latter is used.
					sput_phys_col indicates which column to use in the TRIM table; the default (3) corresponds to 30 degrees incidence. The columns are for
					  0 15 30 45 55 65 75 80 85
					degrees. This angle is also used in the empirical formula. Plate_temp is the temperature (in Kelvin) of the COOLED end of the divertor plates. The surface temperature is computed self-consistently (using a 1-D description) according to the incident heat fluxes from the plasma. The plate is assumed to have a thickness of plate_thick, measured in metres. When plate_thick.eq.0 (default), the plate surface temperature is assumed to be the same as plate_temp. Sput_res turns on radiation enhanced sublimation (RES) when .gt.0.0 and is a multiplier to the RES rate.
					The switch sputter_energy_on turns on the energy contribution from the sputtered particles (physical and chemical). If sputter_energy_on.eq.0, the particles are sputtered cold, with no energy contribution to the ion heat equation.
					If sputter_energy_on.ne.0 (default), the chemically sputtered particles are re-introduced into the plasma with the thermal energy corresponding to the surface temperature of the material, while physically sputtered particles are re-introduced with the TRIM-calculated energy sputtering yield (if the TRIM model is used).
					Therm_evap turns on thermal evaporation when .gt.0.0 and is a multiplier to the thermal evaporation rate.
					Redep_alpha is the multiplier to the reduction of the sputtering yield due to prompt redeposition. The promptly redeposited species is counted as eroded-then-deposited species.
				""", '1'),
   
      'b2stbr_sput_res' : ('', 'real', """
					Sputtering model switches. Not yet available for WG. See the code in b2stbr and the b2mod_sputter module for specific implementation details and references.
					The default values represent the case of Graphite plates. Sput_src is the atomic number of the plasma species which causes chemical sputtering.
					Sput_dst (when .ge.0) is the species index of the destination species produced by physical sputtering, chemical sputtering and/or RES. If either of the latter two processes are included, the chemical sputtering and RES production rate calculations provided in the code assume that sput_dst points to a Carbon species.
					Sput_dst2 and sput_dst3 (when .ge.0) represent other species produced by wall interactions for mixed materials scenarios.
					Sput_frac_flag is the switch to turn on mixed materials scenarios (when sput_frac_flag.eq.1).
					Plate_model.eq.0 means the 0-D time-independent plate heating model while plate_model.eq.1 indicates the 1-D time-dependent plate heating treatment. Plate_model.eq.2 gives acces to a 2-D time-dependent model. Plate_option chooses the initialisation of the plate temperature profile. If plate_option.eq.1, the profile is set to the constant given in plate_temp. If plate_option.eq.2, the profile is computed to be the 0-D equilibrium profile. If plate_option.eq.3, the profile is read from results of the previous run.
					Sput_phys_model is a switch for choosing between the TRIM tables (model 1, default) or an empirical formula (model 0). When TRIM data is not available, the empirical formula is automatically used. Extrapolations of low and high energy ranges beyond the TRIM table data is done using the same physical dependencies as the empirical formula. Sput_chem_model is a switch for the chemical sputtering model used.
					If sput_chem_model.eq.0 (default), the empirical formula is used.
					If sput_chem_model.eq.1, a constant with a low energy cut-off is used.
					The cutoff occurs at approximately sput_chem_cutoff_alpha and the width is determined by sput_chem_cutoff_beta (the larger the value, the narrower the width over which the transition from 0 to 1 occurs).
					For model 0, sput_frc is a multiplier to the empirical formula, while for model 1, sput_frc is the constant chemical sputtering yield.
					Sput_frc is superseded by the chem_sput array from b2.neutrals.namelist if the latter is used.
					For neutrals species, we add a factor of α*na*vbar to the particle flux to the plate (used to compute chemical and RES sputtering), where vbar is the average neutral particle speed.
					Sput_phys turns on physical sputtering when sput_phys.gt.0.0 and contains a (real) multiplier for the physical sputtering rate looked up in the TRIM tables. It is superseded by the phys_sput array in b2.neutrals.parameters if the latter is used.
					sput_phys_col indicates which column to use in the TRIM table; the default (3) corresponds to 30 degrees incidence. The columns are for
					  0 15 30 45 55 65 75 80 85
					degrees. This angle is also used in the empirical formula. Plate_temp is the temperature (in Kelvin) of the COOLED end of the divertor plates. The surface temperature is computed self-consistently (using a 1-D description) according to the incident heat fluxes from the plasma. The plate is assumed to have a thickness of plate_thick, measured in metres. When plate_thick.eq.0 (default), the plate surface temperature is assumed to be the same as plate_temp. Sput_res turns on radiation enhanced sublimation (RES) when .gt.0.0 and is a multiplier to the RES rate.
					The switch sputter_energy_on turns on the energy contribution from the sputtered particles (physical and chemical). If sputter_energy_on.eq.0, the particles are sputtered cold, with no energy contribution to the ion heat equation.
					If sputter_energy_on.ne.0 (default), the chemically sputtered particles are re-introduced into the plasma with the thermal energy corresponding to the surface temperature of the material, while physically sputtered particles are re-introduced with the TRIM-calculated energy sputtering yield (if the TRIM model is used).
					Therm_evap turns on thermal evaporation when .gt.0.0 and is a multiplier to the thermal evaporation rate.
					Redep_alpha is the multiplier to the reduction of the sputtering yield due to prompt redeposition. The promptly redeposited species is counted as eroded-then-deposited species.
				""", '0.0'),
   
      'b2stbr_therm_evap' : ('', 'real', """
					Sputtering model switches. Not yet available for WG. See the code in b2stbr and the b2mod_sputter module for specific implementation details and references.
					The default values represent the case of Graphite plates. Sput_src is the atomic number of the plasma species which causes chemical sputtering.
					Sput_dst (when .ge.0) is the species index of the destination species produced by physical sputtering, chemical sputtering and/or RES. If either of the latter two processes are included, the chemical sputtering and RES production rate calculations provided in the code assume that sput_dst points to a Carbon species.
					Sput_dst2 and sput_dst3 (when .ge.0) represent other species produced by wall interactions for mixed materials scenarios.
					Sput_frac_flag is the switch to turn on mixed materials scenarios (when sput_frac_flag.eq.1).
					Plate_model.eq.0 means the 0-D time-independent plate heating model while plate_model.eq.1 indicates the 1-D time-dependent plate heating treatment. Plate_model.eq.2 gives acces to a 2-D time-dependent model. Plate_option chooses the initialisation of the plate temperature profile. If plate_option.eq.1, the profile is set to the constant given in plate_temp. If plate_option.eq.2, the profile is computed to be the 0-D equilibrium profile. If plate_option.eq.3, the profile is read from results of the previous run.
					Sput_phys_model is a switch for choosing between the TRIM tables (model 1, default) or an empirical formula (model 0). When TRIM data is not available, the empirical formula is automatically used. Extrapolations of low and high energy ranges beyond the TRIM table data is done using the same physical dependencies as the empirical formula. Sput_chem_model is a switch for the chemical sputtering model used.
					If sput_chem_model.eq.0 (default), the empirical formula is used.
					If sput_chem_model.eq.1, a constant with a low energy cut-off is used.
					The cutoff occurs at approximately sput_chem_cutoff_alpha and the width is determined by sput_chem_cutoff_beta (the larger the value, the narrower the width over which the transition from 0 to 1 occurs).
					For model 0, sput_frc is a multiplier to the empirical formula, while for model 1, sput_frc is the constant chemical sputtering yield.
					Sput_frc is superseded by the chem_sput array from b2.neutrals.namelist if the latter is used.
					For neutrals species, we add a factor of α*na*vbar to the particle flux to the plate (used to compute chemical and RES sputtering), where vbar is the average neutral particle speed.
					Sput_phys turns on physical sputtering when sput_phys.gt.0.0 and contains a (real) multiplier for the physical sputtering rate looked up in the TRIM tables. It is superseded by the phys_sput array in b2.neutrals.parameters if the latter is used.
					sput_phys_col indicates which column to use in the TRIM table; the default (3) corresponds to 30 degrees incidence. The columns are for
					  0 15 30 45 55 65 75 80 85
					degrees. This angle is also used in the empirical formula. Plate_temp is the temperature (in Kelvin) of the COOLED end of the divertor plates. The surface temperature is computed self-consistently (using a 1-D description) according to the incident heat fluxes from the plasma. The plate is assumed to have a thickness of plate_thick, measured in metres. When plate_thick.eq.0 (default), the plate surface temperature is assumed to be the same as plate_temp. Sput_res turns on radiation enhanced sublimation (RES) when .gt.0.0 and is a multiplier to the RES rate.
					The switch sputter_energy_on turns on the energy contribution from the sputtered particles (physical and chemical). If sputter_energy_on.eq.0, the particles are sputtered cold, with no energy contribution to the ion heat equation.
					If sputter_energy_on.ne.0 (default), the chemically sputtered particles are re-introduced into the plasma with the thermal energy corresponding to the surface temperature of the material, while physically sputtered particles are re-introduced with the TRIM-calculated energy sputtering yield (if the TRIM model is used).
					Therm_evap turns on thermal evaporation when .gt.0.0 and is a multiplier to the thermal evaporation rate.
					Redep_alpha is the multiplier to the reduction of the sputtering yield due to prompt redeposition. The promptly redeposited species is counted as eroded-then-deposited species.
				""", '0.0'),
   
      'b2stbr_sput_dst' : ('', 'integer', """
					Sputtering model switches. Not yet available for WG. See the code in b2stbr and the b2mod_sputter module for specific implementation details and references.
					The default values represent the case of Graphite plates. Sput_src is the atomic number of the plasma species which causes chemical sputtering.
					Sput_dst (when .ge.0) is the species index of the destination species produced by physical sputtering, chemical sputtering and/or RES. If either of the latter two processes are included, the chemical sputtering and RES production rate calculations provided in the code assume that sput_dst points to a Carbon species.
					Sput_dst2 and sput_dst3 (when .ge.0) represent other species produced by wall interactions for mixed materials scenarios.
					Sput_frac_flag is the switch to turn on mixed materials scenarios (when sput_frac_flag.eq.1).
					Plate_model.eq.0 means the 0-D time-independent plate heating model while plate_model.eq.1 indicates the 1-D time-dependent plate heating treatment. Plate_model.eq.2 gives acces to a 2-D time-dependent model. Plate_option chooses the initialisation of the plate temperature profile. If plate_option.eq.1, the profile is set to the constant given in plate_temp. If plate_option.eq.2, the profile is computed to be the 0-D equilibrium profile. If plate_option.eq.3, the profile is read from results of the previous run.
					Sput_phys_model is a switch for choosing between the TRIM tables (model 1, default) or an empirical formula (model 0). When TRIM data is not available, the empirical formula is automatically used. Extrapolations of low and high energy ranges beyond the TRIM table data is done using the same physical dependencies as the empirical formula. Sput_chem_model is a switch for the chemical sputtering model used.
					If sput_chem_model.eq.0 (default), the empirical formula is used.
					If sput_chem_model.eq.1, a constant with a low energy cut-off is used.
					The cutoff occurs at approximately sput_chem_cutoff_alpha and the width is determined by sput_chem_cutoff_beta (the larger the value, the narrower the width over which the transition from 0 to 1 occurs).
					For model 0, sput_frc is a multiplier to the empirical formula, while for model 1, sput_frc is the constant chemical sputtering yield.
					Sput_frc is superseded by the chem_sput array from b2.neutrals.namelist if the latter is used.
					For neutrals species, we add a factor of α*na*vbar to the particle flux to the plate (used to compute chemical and RES sputtering), where vbar is the average neutral particle speed.
					Sput_phys turns on physical sputtering when sput_phys.gt.0.0 and contains a (real) multiplier for the physical sputtering rate looked up in the TRIM tables. It is superseded by the phys_sput array in b2.neutrals.parameters if the latter is used.
					sput_phys_col indicates which column to use in the TRIM table; the default (3) corresponds to 30 degrees incidence. The columns are for
					  0 15 30 45 55 65 75 80 85
					degrees. This angle is also used in the empirical formula. Plate_temp is the temperature (in Kelvin) of the COOLED end of the divertor plates. The surface temperature is computed self-consistently (using a 1-D description) according to the incident heat fluxes from the plasma. The plate is assumed to have a thickness of plate_thick, measured in metres. When plate_thick.eq.0 (default), the plate surface temperature is assumed to be the same as plate_temp. Sput_res turns on radiation enhanced sublimation (RES) when .gt.0.0 and is a multiplier to the RES rate.
					The switch sputter_energy_on turns on the energy contribution from the sputtered particles (physical and chemical). If sputter_energy_on.eq.0, the particles are sputtered cold, with no energy contribution to the ion heat equation.
					If sputter_energy_on.ne.0 (default), the chemically sputtered particles are re-introduced into the plasma with the thermal energy corresponding to the surface temperature of the material, while physically sputtered particles are re-introduced with the TRIM-calculated energy sputtering yield (if the TRIM model is used).
					Therm_evap turns on thermal evaporation when .gt.0.0 and is a multiplier to the thermal evaporation rate.
					Redep_alpha is the multiplier to the reduction of the sputtering yield due to prompt redeposition. The promptly redeposited species is counted as eroded-then-deposited species.
				""", '-1'),
   
      'b2stbr_sput_dst2' : ('', 'integer', """
					Sputtering model switches. Not yet available for WG. See the code in b2stbr and the b2mod_sputter module for specific implementation details and references.
					The default values represent the case of Graphite plates. Sput_src is the atomic number of the plasma species which causes chemical sputtering.
					Sput_dst (when .ge.0) is the species index of the destination species produced by physical sputtering, chemical sputtering and/or RES. If either of the latter two processes are included, the chemical sputtering and RES production rate calculations provided in the code assume that sput_dst points to a Carbon species.
					Sput_dst2 and sput_dst3 (when .ge.0) represent other species produced by wall interactions for mixed materials scenarios.
					Sput_frac_flag is the switch to turn on mixed materials scenarios (when sput_frac_flag.eq.1).
					Plate_model.eq.0 means the 0-D time-independent plate heating model while plate_model.eq.1 indicates the 1-D time-dependent plate heating treatment. Plate_model.eq.2 gives acces to a 2-D time-dependent model. Plate_option chooses the initialisation of the plate temperature profile. If plate_option.eq.1, the profile is set to the constant given in plate_temp. If plate_option.eq.2, the profile is computed to be the 0-D equilibrium profile. If plate_option.eq.3, the profile is read from results of the previous run.
					Sput_phys_model is a switch for choosing between the TRIM tables (model 1, default) or an empirical formula (model 0). When TRIM data is not available, the empirical formula is automatically used. Extrapolations of low and high energy ranges beyond the TRIM table data is done using the same physical dependencies as the empirical formula. Sput_chem_model is a switch for the chemical sputtering model used.
					If sput_chem_model.eq.0 (default), the empirical formula is used.
					If sput_chem_model.eq.1, a constant with a low energy cut-off is used.
					The cutoff occurs at approximately sput_chem_cutoff_alpha and the width is determined by sput_chem_cutoff_beta (the larger the value, the narrower the width over which the transition from 0 to 1 occurs).
					For model 0, sput_frc is a multiplier to the empirical formula, while for model 1, sput_frc is the constant chemical sputtering yield.
					Sput_frc is superseded by the chem_sput array from b2.neutrals.namelist if the latter is used.
					For neutrals species, we add a factor of α*na*vbar to the particle flux to the plate (used to compute chemical and RES sputtering), where vbar is the average neutral particle speed.
					Sput_phys turns on physical sputtering when sput_phys.gt.0.0 and contains a (real) multiplier for the physical sputtering rate looked up in the TRIM tables. It is superseded by the phys_sput array in b2.neutrals.parameters if the latter is used.
					sput_phys_col indicates which column to use in the TRIM table; the default (3) corresponds to 30 degrees incidence. The columns are for
					  0 15 30 45 55 65 75 80 85
					degrees. This angle is also used in the empirical formula. Plate_temp is the temperature (in Kelvin) of the COOLED end of the divertor plates. The surface temperature is computed self-consistently (using a 1-D description) according to the incident heat fluxes from the plasma. The plate is assumed to have a thickness of plate_thick, measured in metres. When plate_thick.eq.0 (default), the plate surface temperature is assumed to be the same as plate_temp. Sput_res turns on radiation enhanced sublimation (RES) when .gt.0.0 and is a multiplier to the RES rate.
					The switch sputter_energy_on turns on the energy contribution from the sputtered particles (physical and chemical). If sputter_energy_on.eq.0, the particles are sputtered cold, with no energy contribution to the ion heat equation.
					If sputter_energy_on.ne.0 (default), the chemically sputtered particles are re-introduced into the plasma with the thermal energy corresponding to the surface temperature of the material, while physically sputtered particles are re-introduced with the TRIM-calculated energy sputtering yield (if the TRIM model is used).
					Therm_evap turns on thermal evaporation when .gt.0.0 and is a multiplier to the thermal evaporation rate.
					Redep_alpha is the multiplier to the reduction of the sputtering yield due to prompt redeposition. The promptly redeposited species is counted as eroded-then-deposited species.
				""", '-1'),
   
      'b2stbr_sput_dst3' : ('', 'integer', """
					Sputtering model switches. Not yet available for WG. See the code in b2stbr and the b2mod_sputter module for specific implementation details and references.
					The default values represent the case of Graphite plates. Sput_src is the atomic number of the plasma species which causes chemical sputtering.
					Sput_dst (when .ge.0) is the species index of the destination species produced by physical sputtering, chemical sputtering and/or RES. If either of the latter two processes are included, the chemical sputtering and RES production rate calculations provided in the code assume that sput_dst points to a Carbon species.
					Sput_dst2 and sput_dst3 (when .ge.0) represent other species produced by wall interactions for mixed materials scenarios.
					Sput_frac_flag is the switch to turn on mixed materials scenarios (when sput_frac_flag.eq.1).
					Plate_model.eq.0 means the 0-D time-independent plate heating model while plate_model.eq.1 indicates the 1-D time-dependent plate heating treatment. Plate_model.eq.2 gives acces to a 2-D time-dependent model. Plate_option chooses the initialisation of the plate temperature profile. If plate_option.eq.1, the profile is set to the constant given in plate_temp. If plate_option.eq.2, the profile is computed to be the 0-D equilibrium profile. If plate_option.eq.3, the profile is read from results of the previous run.
					Sput_phys_model is a switch for choosing between the TRIM tables (model 1, default) or an empirical formula (model 0). When TRIM data is not available, the empirical formula is automatically used. Extrapolations of low and high energy ranges beyond the TRIM table data is done using the same physical dependencies as the empirical formula. Sput_chem_model is a switch for the chemical sputtering model used.
					If sput_chem_model.eq.0 (default), the empirical formula is used.
					If sput_chem_model.eq.1, a constant with a low energy cut-off is used.
					The cutoff occurs at approximately sput_chem_cutoff_alpha and the width is determined by sput_chem_cutoff_beta (the larger the value, the narrower the width over which the transition from 0 to 1 occurs).
					For model 0, sput_frc is a multiplier to the empirical formula, while for model 1, sput_frc is the constant chemical sputtering yield.
					Sput_frc is superseded by the chem_sput array from b2.neutrals.namelist if the latter is used.
					For neutrals species, we add a factor of α*na*vbar to the particle flux to the plate (used to compute chemical and RES sputtering), where vbar is the average neutral particle speed.
					Sput_phys turns on physical sputtering when sput_phys.gt.0.0 and contains a (real) multiplier for the physical sputtering rate looked up in the TRIM tables. It is superseded by the phys_sput array in b2.neutrals.parameters if the latter is used.
					sput_phys_col indicates which column to use in the TRIM table; the default (3) corresponds to 30 degrees incidence. The columns are for
					  0 15 30 45 55 65 75 80 85
					degrees. This angle is also used in the empirical formula. Plate_temp is the temperature (in Kelvin) of the COOLED end of the divertor plates. The surface temperature is computed self-consistently (using a 1-D description) according to the incident heat fluxes from the plasma. The plate is assumed to have a thickness of plate_thick, measured in metres. When plate_thick.eq.0 (default), the plate surface temperature is assumed to be the same as plate_temp. Sput_res turns on radiation enhanced sublimation (RES) when .gt.0.0 and is a multiplier to the RES rate.
					The switch sputter_energy_on turns on the energy contribution from the sputtered particles (physical and chemical). If sputter_energy_on.eq.0, the particles are sputtered cold, with no energy contribution to the ion heat equation.
					If sputter_energy_on.ne.0 (default), the chemically sputtered particles are re-introduced into the plasma with the thermal energy corresponding to the surface temperature of the material, while physically sputtered particles are re-introduced with the TRIM-calculated energy sputtering yield (if the TRIM model is used).
					Therm_evap turns on thermal evaporation when .gt.0.0 and is a multiplier to the thermal evaporation rate.
					Redep_alpha is the multiplier to the reduction of the sputtering yield due to prompt redeposition. The promptly redeposited species is counted as eroded-then-deposited species.
				""", '-1'),
   
      'b2stbr_sput_frac_flag' : ('', 'integer', """
					Sputtering model switches. Not yet available for WG. See the code in b2stbr and the b2mod_sputter module for specific implementation details and references.
					The default values represent the case of Graphite plates. Sput_src is the atomic number of the plasma species which causes chemical sputtering.
					Sput_dst (when .ge.0) is the species index of the destination species produced by physical sputtering, chemical sputtering and/or RES. If either of the latter two processes are included, the chemical sputtering and RES production rate calculations provided in the code assume that sput_dst points to a Carbon species.
					Sput_dst2 and sput_dst3 (when .ge.0) represent other species produced by wall interactions for mixed materials scenarios.
					Sput_frac_flag is the switch to turn on mixed materials scenarios (when sput_frac_flag.eq.1).
					Plate_model.eq.0 means the 0-D time-independent plate heating model while plate_model.eq.1 indicates the 1-D time-dependent plate heating treatment. Plate_model.eq.2 gives acces to a 2-D time-dependent model. Plate_option chooses the initialisation of the plate temperature profile. If plate_option.eq.1, the profile is set to the constant given in plate_temp. If plate_option.eq.2, the profile is computed to be the 0-D equilibrium profile. If plate_option.eq.3, the profile is read from results of the previous run.
					Sput_phys_model is a switch for choosing between the TRIM tables (model 1, default) or an empirical formula (model 0). When TRIM data is not available, the empirical formula is automatically used. Extrapolations of low and high energy ranges beyond the TRIM table data is done using the same physical dependencies as the empirical formula. Sput_chem_model is a switch for the chemical sputtering model used.
					If sput_chem_model.eq.0 (default), the empirical formula is used.
					If sput_chem_model.eq.1, a constant with a low energy cut-off is used.
					The cutoff occurs at approximately sput_chem_cutoff_alpha and the width is determined by sput_chem_cutoff_beta (the larger the value, the narrower the width over which the transition from 0 to 1 occurs).
					For model 0, sput_frc is a multiplier to the empirical formula, while for model 1, sput_frc is the constant chemical sputtering yield.
					Sput_frc is superseded by the chem_sput array from b2.neutrals.namelist if the latter is used.
					For neutrals species, we add a factor of α*na*vbar to the particle flux to the plate (used to compute chemical and RES sputtering), where vbar is the average neutral particle speed.
					Sput_phys turns on physical sputtering when sput_phys.gt.0.0 and contains a (real) multiplier for the physical sputtering rate looked up in the TRIM tables. It is superseded by the phys_sput array in b2.neutrals.parameters if the latter is used.
					sput_phys_col indicates which column to use in the TRIM table; the default (3) corresponds to 30 degrees incidence. The columns are for
					  0 15 30 45 55 65 75 80 85
					degrees. This angle is also used in the empirical formula. Plate_temp is the temperature (in Kelvin) of the COOLED end of the divertor plates. The surface temperature is computed self-consistently (using a 1-D description) according to the incident heat fluxes from the plasma. The plate is assumed to have a thickness of plate_thick, measured in metres. When plate_thick.eq.0 (default), the plate surface temperature is assumed to be the same as plate_temp. Sput_res turns on radiation enhanced sublimation (RES) when .gt.0.0 and is a multiplier to the RES rate.
					The switch sputter_energy_on turns on the energy contribution from the sputtered particles (physical and chemical). If sputter_energy_on.eq.0, the particles are sputtered cold, with no energy contribution to the ion heat equation.
					If sputter_energy_on.ne.0 (default), the chemically sputtered particles are re-introduced into the plasma with the thermal energy corresponding to the surface temperature of the material, while physically sputtered particles are re-introduced with the TRIM-calculated energy sputtering yield (if the TRIM model is used).
					Therm_evap turns on thermal evaporation when .gt.0.0 and is a multiplier to the thermal evaporation rate.
					Redep_alpha is the multiplier to the reduction of the sputtering yield due to prompt redeposition. The promptly redeposited species is counted as eroded-then-deposited species.
				""", '0'),
   
      'b2stbr_sput_frc' : ('', 'real', """
					Sputtering model switches. Not yet available for WG. See the code in b2stbr and the b2mod_sputter module for specific implementation details and references.
					The default values represent the case of Graphite plates. Sput_src is the atomic number of the plasma species which causes chemical sputtering.
					Sput_dst (when .ge.0) is the species index of the destination species produced by physical sputtering, chemical sputtering and/or RES. If either of the latter two processes are included, the chemical sputtering and RES production rate calculations provided in the code assume that sput_dst points to a Carbon species.
					Sput_dst2 and sput_dst3 (when .ge.0) represent other species produced by wall interactions for mixed materials scenarios.
					Sput_frac_flag is the switch to turn on mixed materials scenarios (when sput_frac_flag.eq.1).
					Plate_model.eq.0 means the 0-D time-independent plate heating model while plate_model.eq.1 indicates the 1-D time-dependent plate heating treatment. Plate_model.eq.2 gives acces to a 2-D time-dependent model. Plate_option chooses the initialisation of the plate temperature profile. If plate_option.eq.1, the profile is set to the constant given in plate_temp. If plate_option.eq.2, the profile is computed to be the 0-D equilibrium profile. If plate_option.eq.3, the profile is read from results of the previous run.
					Sput_phys_model is a switch for choosing between the TRIM tables (model 1, default) or an empirical formula (model 0). When TRIM data is not available, the empirical formula is automatically used. Extrapolations of low and high energy ranges beyond the TRIM table data is done using the same physical dependencies as the empirical formula. Sput_chem_model is a switch for the chemical sputtering model used.
					If sput_chem_model.eq.0 (default), the empirical formula is used.
					If sput_chem_model.eq.1, a constant with a low energy cut-off is used.
					The cutoff occurs at approximately sput_chem_cutoff_alpha and the width is determined by sput_chem_cutoff_beta (the larger the value, the narrower the width over which the transition from 0 to 1 occurs).
					For model 0, sput_frc is a multiplier to the empirical formula, while for model 1, sput_frc is the constant chemical sputtering yield.
					Sput_frc is superseded by the chem_sput array from b2.neutrals.namelist if the latter is used.
					For neutrals species, we add a factor of α*na*vbar to the particle flux to the plate (used to compute chemical and RES sputtering), where vbar is the average neutral particle speed.
					Sput_phys turns on physical sputtering when sput_phys.gt.0.0 and contains a (real) multiplier for the physical sputtering rate looked up in the TRIM tables. It is superseded by the phys_sput array in b2.neutrals.parameters if the latter is used.
					sput_phys_col indicates which column to use in the TRIM table; the default (3) corresponds to 30 degrees incidence. The columns are for
					  0 15 30 45 55 65 75 80 85
					degrees. This angle is also used in the empirical formula. Plate_temp is the temperature (in Kelvin) of the COOLED end of the divertor plates. The surface temperature is computed self-consistently (using a 1-D description) according to the incident heat fluxes from the plasma. The plate is assumed to have a thickness of plate_thick, measured in metres. When plate_thick.eq.0 (default), the plate surface temperature is assumed to be the same as plate_temp. Sput_res turns on radiation enhanced sublimation (RES) when .gt.0.0 and is a multiplier to the RES rate.
					The switch sputter_energy_on turns on the energy contribution from the sputtered particles (physical and chemical). If sputter_energy_on.eq.0, the particles are sputtered cold, with no energy contribution to the ion heat equation.
					If sputter_energy_on.ne.0 (default), the chemically sputtered particles are re-introduced into the plasma with the thermal energy corresponding to the surface temperature of the material, while physically sputtered particles are re-introduced with the TRIM-calculated energy sputtering yield (if the TRIM model is used).
					Therm_evap turns on thermal evaporation when .gt.0.0 and is a multiplier to the thermal evaporation rate.
					Redep_alpha is the multiplier to the reduction of the sputtering yield due to prompt redeposition. The promptly redeposited species is counted as eroded-then-deposited species.
				""", '0.0'),
   
      'b2stbr_sput_phys' : ('', 'real', """
					Sputtering model switches. Not yet available for WG. See the code in b2stbr and the b2mod_sputter module for specific implementation details and references.
					The default values represent the case of Graphite plates. Sput_src is the atomic number of the plasma species which causes chemical sputtering.
					Sput_dst (when .ge.0) is the species index of the destination species produced by physical sputtering, chemical sputtering and/or RES. If either of the latter two processes are included, the chemical sputtering and RES production rate calculations provided in the code assume that sput_dst points to a Carbon species.
					Sput_dst2 and sput_dst3 (when .ge.0) represent other species produced by wall interactions for mixed materials scenarios.
					Sput_frac_flag is the switch to turn on mixed materials scenarios (when sput_frac_flag.eq.1).
					Plate_model.eq.0 means the 0-D time-independent plate heating model while plate_model.eq.1 indicates the 1-D time-dependent plate heating treatment. Plate_model.eq.2 gives acces to a 2-D time-dependent model. Plate_option chooses the initialisation of the plate temperature profile. If plate_option.eq.1, the profile is set to the constant given in plate_temp. If plate_option.eq.2, the profile is computed to be the 0-D equilibrium profile. If plate_option.eq.3, the profile is read from results of the previous run.
					Sput_phys_model is a switch for choosing between the TRIM tables (model 1, default) or an empirical formula (model 0). When TRIM data is not available, the empirical formula is automatically used. Extrapolations of low and high energy ranges beyond the TRIM table data is done using the same physical dependencies as the empirical formula. Sput_chem_model is a switch for the chemical sputtering model used.
					If sput_chem_model.eq.0 (default), the empirical formula is used.
					If sput_chem_model.eq.1, a constant with a low energy cut-off is used.
					The cutoff occurs at approximately sput_chem_cutoff_alpha and the width is determined by sput_chem_cutoff_beta (the larger the value, the narrower the width over which the transition from 0 to 1 occurs).
					For model 0, sput_frc is a multiplier to the empirical formula, while for model 1, sput_frc is the constant chemical sputtering yield.
					Sput_frc is superseded by the chem_sput array from b2.neutrals.namelist if the latter is used.
					For neutrals species, we add a factor of α*na*vbar to the particle flux to the plate (used to compute chemical and RES sputtering), where vbar is the average neutral particle speed.
					Sput_phys turns on physical sputtering when sput_phys.gt.0.0 and contains a (real) multiplier for the physical sputtering rate looked up in the TRIM tables. It is superseded by the phys_sput array in b2.neutrals.parameters if the latter is used.
					sput_phys_col indicates which column to use in the TRIM table; the default (3) corresponds to 30 degrees incidence. The columns are for
					  0 15 30 45 55 65 75 80 85
					degrees. This angle is also used in the empirical formula. Plate_temp is the temperature (in Kelvin) of the COOLED end of the divertor plates. The surface temperature is computed self-consistently (using a 1-D description) according to the incident heat fluxes from the plasma. The plate is assumed to have a thickness of plate_thick, measured in metres. When plate_thick.eq.0 (default), the plate surface temperature is assumed to be the same as plate_temp. Sput_res turns on radiation enhanced sublimation (RES) when .gt.0.0 and is a multiplier to the RES rate.
					The switch sputter_energy_on turns on the energy contribution from the sputtered particles (physical and chemical). If sputter_energy_on.eq.0, the particles are sputtered cold, with no energy contribution to the ion heat equation.
					If sputter_energy_on.ne.0 (default), the chemically sputtered particles are re-introduced into the plasma with the thermal energy corresponding to the surface temperature of the material, while physically sputtered particles are re-introduced with the TRIM-calculated energy sputtering yield (if the TRIM model is used).
					Therm_evap turns on thermal evaporation when .gt.0.0 and is a multiplier to the thermal evaporation rate.
					Redep_alpha is the multiplier to the reduction of the sputtering yield due to prompt redeposition. The promptly redeposited species is counted as eroded-then-deposited species.
				""", '0.0'),
   
      'b2stbr_sput_src' : ('', 'integer', """
					Sputtering model switches. Not yet available for WG. See the code in b2stbr and the b2mod_sputter module for specific implementation details and references.
					The default values represent the case of Graphite plates. Sput_src is the atomic number of the plasma species which causes chemical sputtering.
					Sput_dst (when .ge.0) is the species index of the destination species produced by physical sputtering, chemical sputtering and/or RES. If either of the latter two processes are included, the chemical sputtering and RES production rate calculations provided in the code assume that sput_dst points to a Carbon species.
					Sput_dst2 and sput_dst3 (when .ge.0) represent other species produced by wall interactions for mixed materials scenarios.
					Sput_frac_flag is the switch to turn on mixed materials scenarios (when sput_frac_flag.eq.1).
					Plate_model.eq.0 means the 0-D time-independent plate heating model while plate_model.eq.1 indicates the 1-D time-dependent plate heating treatment. Plate_model.eq.2 gives acces to a 2-D time-dependent model. Plate_option chooses the initialisation of the plate temperature profile. If plate_option.eq.1, the profile is set to the constant given in plate_temp. If plate_option.eq.2, the profile is computed to be the 0-D equilibrium profile. If plate_option.eq.3, the profile is read from results of the previous run.
					Sput_phys_model is a switch for choosing between the TRIM tables (model 1, default) or an empirical formula (model 0). When TRIM data is not available, the empirical formula is automatically used. Extrapolations of low and high energy ranges beyond the TRIM table data is done using the same physical dependencies as the empirical formula. Sput_chem_model is a switch for the chemical sputtering model used.
					If sput_chem_model.eq.0 (default), the empirical formula is used.
					If sput_chem_model.eq.1, a constant with a low energy cut-off is used.
					The cutoff occurs at approximately sput_chem_cutoff_alpha and the width is determined by sput_chem_cutoff_beta (the larger the value, the narrower the width over which the transition from 0 to 1 occurs).
					For model 0, sput_frc is a multiplier to the empirical formula, while for model 1, sput_frc is the constant chemical sputtering yield.
					Sput_frc is superseded by the chem_sput array from b2.neutrals.namelist if the latter is used.
					For neutrals species, we add a factor of α*na*vbar to the particle flux to the plate (used to compute chemical and RES sputtering), where vbar is the average neutral particle speed.
					Sput_phys turns on physical sputtering when sput_phys.gt.0.0 and contains a (real) multiplier for the physical sputtering rate looked up in the TRIM tables. It is superseded by the phys_sput array in b2.neutrals.parameters if the latter is used.
					sput_phys_col indicates which column to use in the TRIM table; the default (3) corresponds to 30 degrees incidence. The columns are for
					  0 15 30 45 55 65 75 80 85
					degrees. This angle is also used in the empirical formula. Plate_temp is the temperature (in Kelvin) of the COOLED end of the divertor plates. The surface temperature is computed self-consistently (using a 1-D description) according to the incident heat fluxes from the plasma. The plate is assumed to have a thickness of plate_thick, measured in metres. When plate_thick.eq.0 (default), the plate surface temperature is assumed to be the same as plate_temp. Sput_res turns on radiation enhanced sublimation (RES) when .gt.0.0 and is a multiplier to the RES rate.
					The switch sputter_energy_on turns on the energy contribution from the sputtered particles (physical and chemical). If sputter_energy_on.eq.0, the particles are sputtered cold, with no energy contribution to the ion heat equation.
					If sputter_energy_on.ne.0 (default), the chemically sputtered particles are re-introduced into the plasma with the thermal energy corresponding to the surface temperature of the material, while physically sputtered particles are re-introduced with the TRIM-calculated energy sputtering yield (if the TRIM model is used).
					Therm_evap turns on thermal evaporation when .gt.0.0 and is a multiplier to the thermal evaporation rate.
					Redep_alpha is the multiplier to the reduction of the sputtering yield due to prompt redeposition. The promptly redeposited species is counted as eroded-then-deposited species.
				""", '1'),
   
      'b2stbr_sput_phys_col' : ('', 'integer', """
					Sputtering model switches. Not yet available for WG. See the code in b2stbr and the b2mod_sputter module for specific implementation details and references.
					The default values represent the case of Graphite plates. Sput_src is the atomic number of the plasma species which causes chemical sputtering.
					Sput_dst (when .ge.0) is the species index of the destination species produced by physical sputtering, chemical sputtering and/or RES. If either of the latter two processes are included, the chemical sputtering and RES production rate calculations provided in the code assume that sput_dst points to a Carbon species.
					Sput_dst2 and sput_dst3 (when .ge.0) represent other species produced by wall interactions for mixed materials scenarios.
					Sput_frac_flag is the switch to turn on mixed materials scenarios (when sput_frac_flag.eq.1).
					Plate_model.eq.0 means the 0-D time-independent plate heating model while plate_model.eq.1 indicates the 1-D time-dependent plate heating treatment. Plate_model.eq.2 gives acces to a 2-D time-dependent model. Plate_option chooses the initialisation of the plate temperature profile. If plate_option.eq.1, the profile is set to the constant given in plate_temp. If plate_option.eq.2, the profile is computed to be the 0-D equilibrium profile. If plate_option.eq.3, the profile is read from results of the previous run.
					Sput_phys_model is a switch for choosing between the TRIM tables (model 1, default) or an empirical formula (model 0). When TRIM data is not available, the empirical formula is automatically used. Extrapolations of low and high energy ranges beyond the TRIM table data is done using the same physical dependencies as the empirical formula. Sput_chem_model is a switch for the chemical sputtering model used.
					If sput_chem_model.eq.0 (default), the empirical formula is used.
					If sput_chem_model.eq.1, a constant with a low energy cut-off is used.
					The cutoff occurs at approximately sput_chem_cutoff_alpha and the width is determined by sput_chem_cutoff_beta (the larger the value, the narrower the width over which the transition from 0 to 1 occurs).
					For model 0, sput_frc is a multiplier to the empirical formula, while for model 1, sput_frc is the constant chemical sputtering yield.
					Sput_frc is superseded by the chem_sput array from b2.neutrals.namelist if the latter is used.
					For neutrals species, we add a factor of α*na*vbar to the particle flux to the plate (used to compute chemical and RES sputtering), where vbar is the average neutral particle speed.
					Sput_phys turns on physical sputtering when sput_phys.gt.0.0 and contains a (real) multiplier for the physical sputtering rate looked up in the TRIM tables. It is superseded by the phys_sput array in b2.neutrals.parameters if the latter is used.
					sput_phys_col indicates which column to use in the TRIM table; the default (3) corresponds to 30 degrees incidence. The columns are for
					  0 15 30 45 55 65 75 80 85
					degrees. This angle is also used in the empirical formula. Plate_temp is the temperature (in Kelvin) of the COOLED end of the divertor plates. The surface temperature is computed self-consistently (using a 1-D description) according to the incident heat fluxes from the plasma. The plate is assumed to have a thickness of plate_thick, measured in metres. When plate_thick.eq.0 (default), the plate surface temperature is assumed to be the same as plate_temp. Sput_res turns on radiation enhanced sublimation (RES) when .gt.0.0 and is a multiplier to the RES rate.
					The switch sputter_energy_on turns on the energy contribution from the sputtered particles (physical and chemical). If sputter_energy_on.eq.0, the particles are sputtered cold, with no energy contribution to the ion heat equation.
					If sputter_energy_on.ne.0 (default), the chemically sputtered particles are re-introduced into the plasma with the thermal energy corresponding to the surface temperature of the material, while physically sputtered particles are re-introduced with the TRIM-calculated energy sputtering yield (if the TRIM model is used).
					Therm_evap turns on thermal evaporation when .gt.0.0 and is a multiplier to the thermal evaporation rate.
					Redep_alpha is the multiplier to the reduction of the sputtering yield due to prompt redeposition. The promptly redeposited species is counted as eroded-then-deposited species.
				""", '3'),
   
      'b2stbr_alpha' : ('', 'real', """
					Sputtering model switches. Not yet available for WG. See the code in b2stbr and the b2mod_sputter module for specific implementation details and references.
					The default values represent the case of Graphite plates. Sput_src is the atomic number of the plasma species which causes chemical sputtering.
					Sput_dst (when .ge.0) is the species index of the destination species produced by physical sputtering, chemical sputtering and/or RES. If either of the latter two processes are included, the chemical sputtering and RES production rate calculations provided in the code assume that sput_dst points to a Carbon species.
					Sput_dst2 and sput_dst3 (when .ge.0) represent other species produced by wall interactions for mixed materials scenarios.
					Sput_frac_flag is the switch to turn on mixed materials scenarios (when sput_frac_flag.eq.1).
					Plate_model.eq.0 means the 0-D time-independent plate heating model while plate_model.eq.1 indicates the 1-D time-dependent plate heating treatment. Plate_model.eq.2 gives acces to a 2-D time-dependent model. Plate_option chooses the initialisation of the plate temperature profile. If plate_option.eq.1, the profile is set to the constant given in plate_temp. If plate_option.eq.2, the profile is computed to be the 0-D equilibrium profile. If plate_option.eq.3, the profile is read from results of the previous run.
					Sput_phys_model is a switch for choosing between the TRIM tables (model 1, default) or an empirical formula (model 0). When TRIM data is not available, the empirical formula is automatically used. Extrapolations of low and high energy ranges beyond the TRIM table data is done using the same physical dependencies as the empirical formula. Sput_chem_model is a switch for the chemical sputtering model used.
					If sput_chem_model.eq.0 (default), the empirical formula is used.
					If sput_chem_model.eq.1, a constant with a low energy cut-off is used.
					The cutoff occurs at approximately sput_chem_cutoff_alpha and the width is determined by sput_chem_cutoff_beta (the larger the value, the narrower the width over which the transition from 0 to 1 occurs).
					For model 0, sput_frc is a multiplier to the empirical formula, while for model 1, sput_frc is the constant chemical sputtering yield.
					Sput_frc is superseded by the chem_sput array from b2.neutrals.namelist if the latter is used.
					For neutrals species, we add a factor of α*na*vbar to the particle flux to the plate (used to compute chemical and RES sputtering), where vbar is the average neutral particle speed.
					Sput_phys turns on physical sputtering when sput_phys.gt.0.0 and contains a (real) multiplier for the physical sputtering rate looked up in the TRIM tables. It is superseded by the phys_sput array in b2.neutrals.parameters if the latter is used.
					sput_phys_col indicates which column to use in the TRIM table; the default (3) corresponds to 30 degrees incidence. The columns are for
					  0 15 30 45 55 65 75 80 85
					degrees. This angle is also used in the empirical formula. Plate_temp is the temperature (in Kelvin) of the COOLED end of the divertor plates. The surface temperature is computed self-consistently (using a 1-D description) according to the incident heat fluxes from the plasma. The plate is assumed to have a thickness of plate_thick, measured in metres. When plate_thick.eq.0 (default), the plate surface temperature is assumed to be the same as plate_temp. Sput_res turns on radiation enhanced sublimation (RES) when .gt.0.0 and is a multiplier to the RES rate.
					The switch sputter_energy_on turns on the energy contribution from the sputtered particles (physical and chemical). If sputter_energy_on.eq.0, the particles are sputtered cold, with no energy contribution to the ion heat equation.
					If sputter_energy_on.ne.0 (default), the chemically sputtered particles are re-introduced into the plasma with the thermal energy corresponding to the surface temperature of the material, while physically sputtered particles are re-introduced with the TRIM-calculated energy sputtering yield (if the TRIM model is used).
					Therm_evap turns on thermal evaporation when .gt.0.0 and is a multiplier to the thermal evaporation rate.
					Redep_alpha is the multiplier to the reduction of the sputtering yield due to prompt redeposition. The promptly redeposited species is counted as eroded-then-deposited species.
				""", '0.25'),
   
      'b2stbr_plate_temp' : ('', 'real', """
					Sputtering model switches. Not yet available for WG. See the code in b2stbr and the b2mod_sputter module for specific implementation details and references.
					The default values represent the case of Graphite plates. Sput_src is the atomic number of the plasma species which causes chemical sputtering.
					Sput_dst (when .ge.0) is the species index of the destination species produced by physical sputtering, chemical sputtering and/or RES. If either of the latter two processes are included, the chemical sputtering and RES production rate calculations provided in the code assume that sput_dst points to a Carbon species.
					Sput_dst2 and sput_dst3 (when .ge.0) represent other species produced by wall interactions for mixed materials scenarios.
					Sput_frac_flag is the switch to turn on mixed materials scenarios (when sput_frac_flag.eq.1).
					Plate_model.eq.0 means the 0-D time-independent plate heating model while plate_model.eq.1 indicates the 1-D time-dependent plate heating treatment. Plate_model.eq.2 gives acces to a 2-D time-dependent model. Plate_option chooses the initialisation of the plate temperature profile. If plate_option.eq.1, the profile is set to the constant given in plate_temp. If plate_option.eq.2, the profile is computed to be the 0-D equilibrium profile. If plate_option.eq.3, the profile is read from results of the previous run.
					Sput_phys_model is a switch for choosing between the TRIM tables (model 1, default) or an empirical formula (model 0). When TRIM data is not available, the empirical formula is automatically used. Extrapolations of low and high energy ranges beyond the TRIM table data is done using the same physical dependencies as the empirical formula. Sput_chem_model is a switch for the chemical sputtering model used.
					If sput_chem_model.eq.0 (default), the empirical formula is used.
					If sput_chem_model.eq.1, a constant with a low energy cut-off is used.
					The cutoff occurs at approximately sput_chem_cutoff_alpha and the width is determined by sput_chem_cutoff_beta (the larger the value, the narrower the width over which the transition from 0 to 1 occurs).
					For model 0, sput_frc is a multiplier to the empirical formula, while for model 1, sput_frc is the constant chemical sputtering yield.
					Sput_frc is superseded by the chem_sput array from b2.neutrals.namelist if the latter is used.
					For neutrals species, we add a factor of α*na*vbar to the particle flux to the plate (used to compute chemical and RES sputtering), where vbar is the average neutral particle speed.
					Sput_phys turns on physical sputtering when sput_phys.gt.0.0 and contains a (real) multiplier for the physical sputtering rate looked up in the TRIM tables. It is superseded by the phys_sput array in b2.neutrals.parameters if the latter is used.
					sput_phys_col indicates which column to use in the TRIM table; the default (3) corresponds to 30 degrees incidence. The columns are for
					  0 15 30 45 55 65 75 80 85
					degrees. This angle is also used in the empirical formula. Plate_temp is the temperature (in Kelvin) of the COOLED end of the divertor plates. The surface temperature is computed self-consistently (using a 1-D description) according to the incident heat fluxes from the plasma. The plate is assumed to have a thickness of plate_thick, measured in metres. When plate_thick.eq.0 (default), the plate surface temperature is assumed to be the same as plate_temp. Sput_res turns on radiation enhanced sublimation (RES) when .gt.0.0 and is a multiplier to the RES rate.
					The switch sputter_energy_on turns on the energy contribution from the sputtered particles (physical and chemical). If sputter_energy_on.eq.0, the particles are sputtered cold, with no energy contribution to the ion heat equation.
					If sputter_energy_on.ne.0 (default), the chemically sputtered particles are re-introduced into the plasma with the thermal energy corresponding to the surface temperature of the material, while physically sputtered particles are re-introduced with the TRIM-calculated energy sputtering yield (if the TRIM model is used).
					Therm_evap turns on thermal evaporation when .gt.0.0 and is a multiplier to the thermal evaporation rate.
					Redep_alpha is the multiplier to the reduction of the sputtering yield due to prompt redeposition. The promptly redeposited species is counted as eroded-then-deposited species.
				""", '300.0'),
   
      'b2stbr_plate_thick' : ('', 'real', """
					Sputtering model switches. Not yet available for WG. See the code in b2stbr and the b2mod_sputter module for specific implementation details and references.
					The default values represent the case of Graphite plates. Sput_src is the atomic number of the plasma species which causes chemical sputtering.
					Sput_dst (when .ge.0) is the species index of the destination species produced by physical sputtering, chemical sputtering and/or RES. If either of the latter two processes are included, the chemical sputtering and RES production rate calculations provided in the code assume that sput_dst points to a Carbon species.
					Sput_dst2 and sput_dst3 (when .ge.0) represent other species produced by wall interactions for mixed materials scenarios.
					Sput_frac_flag is the switch to turn on mixed materials scenarios (when sput_frac_flag.eq.1).
					Plate_model.eq.0 means the 0-D time-independent plate heating model while plate_model.eq.1 indicates the 1-D time-dependent plate heating treatment. Plate_model.eq.2 gives acces to a 2-D time-dependent model. Plate_option chooses the initialisation of the plate temperature profile. If plate_option.eq.1, the profile is set to the constant given in plate_temp. If plate_option.eq.2, the profile is computed to be the 0-D equilibrium profile. If plate_option.eq.3, the profile is read from results of the previous run.
					Sput_phys_model is a switch for choosing between the TRIM tables (model 1, default) or an empirical formula (model 0). When TRIM data is not available, the empirical formula is automatically used. Extrapolations of low and high energy ranges beyond the TRIM table data is done using the same physical dependencies as the empirical formula. Sput_chem_model is a switch for the chemical sputtering model used.
					If sput_chem_model.eq.0 (default), the empirical formula is used.
					If sput_chem_model.eq.1, a constant with a low energy cut-off is used.
					The cutoff occurs at approximately sput_chem_cutoff_alpha and the width is determined by sput_chem_cutoff_beta (the larger the value, the narrower the width over which the transition from 0 to 1 occurs).
					For model 0, sput_frc is a multiplier to the empirical formula, while for model 1, sput_frc is the constant chemical sputtering yield.
					Sput_frc is superseded by the chem_sput array from b2.neutrals.namelist if the latter is used.
					For neutrals species, we add a factor of α*na*vbar to the particle flux to the plate (used to compute chemical and RES sputtering), where vbar is the average neutral particle speed.
					Sput_phys turns on physical sputtering when sput_phys.gt.0.0 and contains a (real) multiplier for the physical sputtering rate looked up in the TRIM tables. It is superseded by the phys_sput array in b2.neutrals.parameters if the latter is used.
					sput_phys_col indicates which column to use in the TRIM table; the default (3) corresponds to 30 degrees incidence. The columns are for
					  0 15 30 45 55 65 75 80 85
					degrees. This angle is also used in the empirical formula. Plate_temp is the temperature (in Kelvin) of the COOLED end of the divertor plates. The surface temperature is computed self-consistently (using a 1-D description) according to the incident heat fluxes from the plasma. The plate is assumed to have a thickness of plate_thick, measured in metres. When plate_thick.eq.0 (default), the plate surface temperature is assumed to be the same as plate_temp. Sput_res turns on radiation enhanced sublimation (RES) when .gt.0.0 and is a multiplier to the RES rate.
					The switch sputter_energy_on turns on the energy contribution from the sputtered particles (physical and chemical). If sputter_energy_on.eq.0, the particles are sputtered cold, with no energy contribution to the ion heat equation.
					If sputter_energy_on.ne.0 (default), the chemically sputtered particles are re-introduced into the plasma with the thermal energy corresponding to the surface temperature of the material, while physically sputtered particles are re-introduced with the TRIM-calculated energy sputtering yield (if the TRIM model is used).
					Therm_evap turns on thermal evaporation when .gt.0.0 and is a multiplier to the thermal evaporation rate.
					Redep_alpha is the multiplier to the reduction of the sputtering yield due to prompt redeposition. The promptly redeposited species is counted as eroded-then-deposited species.
				""", '0.00'),
   
      'b2stbr_redep_alpha' : ('', 'real', """
					Sputtering model switches. Not yet available for WG. See the code in b2stbr and the b2mod_sputter module for specific implementation details and references.
					The default values represent the case of Graphite plates. Sput_src is the atomic number of the plasma species which causes chemical sputtering.
					Sput_dst (when .ge.0) is the species index of the destination species produced by physical sputtering, chemical sputtering and/or RES. If either of the latter two processes are included, the chemical sputtering and RES production rate calculations provided in the code assume that sput_dst points to a Carbon species.
					Sput_dst2 and sput_dst3 (when .ge.0) represent other species produced by wall interactions for mixed materials scenarios.
					Sput_frac_flag is the switch to turn on mixed materials scenarios (when sput_frac_flag.eq.1).
					Plate_model.eq.0 means the 0-D time-independent plate heating model while plate_model.eq.1 indicates the 1-D time-dependent plate heating treatment. Plate_model.eq.2 gives acces to a 2-D time-dependent model. Plate_option chooses the initialisation of the plate temperature profile. If plate_option.eq.1, the profile is set to the constant given in plate_temp. If plate_option.eq.2, the profile is computed to be the 0-D equilibrium profile. If plate_option.eq.3, the profile is read from results of the previous run.
					Sput_phys_model is a switch for choosing between the TRIM tables (model 1, default) or an empirical formula (model 0). When TRIM data is not available, the empirical formula is automatically used. Extrapolations of low and high energy ranges beyond the TRIM table data is done using the same physical dependencies as the empirical formula. Sput_chem_model is a switch for the chemical sputtering model used.
					If sput_chem_model.eq.0 (default), the empirical formula is used.
					If sput_chem_model.eq.1, a constant with a low energy cut-off is used.
					The cutoff occurs at approximately sput_chem_cutoff_alpha and the width is determined by sput_chem_cutoff_beta (the larger the value, the narrower the width over which the transition from 0 to 1 occurs).
					For model 0, sput_frc is a multiplier to the empirical formula, while for model 1, sput_frc is the constant chemical sputtering yield.
					Sput_frc is superseded by the chem_sput array from b2.neutrals.namelist if the latter is used.
					For neutrals species, we add a factor of α*na*vbar to the particle flux to the plate (used to compute chemical and RES sputtering), where vbar is the average neutral particle speed.
					Sput_phys turns on physical sputtering when sput_phys.gt.0.0 and contains a (real) multiplier for the physical sputtering rate looked up in the TRIM tables. It is superseded by the phys_sput array in b2.neutrals.parameters if the latter is used.
					sput_phys_col indicates which column to use in the TRIM table; the default (3) corresponds to 30 degrees incidence. The columns are for
					  0 15 30 45 55 65 75 80 85
					degrees. This angle is also used in the empirical formula. Plate_temp is the temperature (in Kelvin) of the COOLED end of the divertor plates. The surface temperature is computed self-consistently (using a 1-D description) according to the incident heat fluxes from the plasma. The plate is assumed to have a thickness of plate_thick, measured in metres. When plate_thick.eq.0 (default), the plate surface temperature is assumed to be the same as plate_temp. Sput_res turns on radiation enhanced sublimation (RES) when .gt.0.0 and is a multiplier to the RES rate.
					The switch sputter_energy_on turns on the energy contribution from the sputtered particles (physical and chemical). If sputter_energy_on.eq.0, the particles are sputtered cold, with no energy contribution to the ion heat equation.
					If sputter_energy_on.ne.0 (default), the chemically sputtered particles are re-introduced into the plasma with the thermal energy corresponding to the surface temperature of the material, while physically sputtered particles are re-introduced with the TRIM-calculated energy sputtering yield (if the TRIM model is used).
					Therm_evap turns on thermal evaporation when .gt.0.0 and is a multiplier to the thermal evaporation rate.
					Redep_alpha is the multiplier to the reduction of the sputtering yield due to prompt redeposition. The promptly redeposited species is counted as eroded-then-deposited species.
				""", '0.00'),
   
      'b2stbr_refl_model' : ('', 'integer', """
					Reflection model switches. If the recycling coefficients (particle and energy) are set to zero, then the code attempts to use, for surfaces in contact with walls, the TRIM reflection data for particle and energy reflection coefficients, when refl_model.eq.1. If refl_model.eq.0, an empirical formula is used instead. The model switch is subservient to reflection_on.ne.0. If reflection_on.eq.0, then no reflection is used.
					If reflection_on.eq.1 (default), then the incident species is reflected unchanged. Otherwise, the reflected flux is of the associated neutral species to the incident particles.
					Not converted for WG. It is recommended to use the advanced fluid neutral (AFN) models instead.
				""", '1'),
   
      'b2stbr_reflection_on' : ('', 'integer', """
					Reflection model switches. If the recycling coefficients (particle and energy) are set to zero, then the code attempts to use, for surfaces in contact with walls, the TRIM reflection data for particle and energy reflection coefficients, when refl_model.eq.1. If refl_model.eq.0, an empirical formula is used instead. The model switch is subservient to reflection_on.ne.0. If reflection_on.eq.0, then no reflection is used.
					If reflection_on.eq.1 (default), then the incident species is reflected unchanged. Otherwise, the reflected flux is of the associated neutral species to the incident particles.
					Not converted for WG. It is recommended to use the advanced fluid neutral (AFN) models instead.
				""", '1'),
   
      'b2tqna_user_transport' : ('', 'integer', """
					The last switch is subservient to b2tqna_user_transport, and only used if user_transport.ne.0. When this is the case, the electron perpendicular heat diffusivity and anomalous perpendicular particle transport coefficient are scaled so as to maintain the required_te_gradient (in units of eV/m), at the iyref-th radial ring along the outer midplane. By default, this is the ring immediately inside the separatrix.
					The transport_eta switches are activated when user_transport.eq.3 and allow modifications of the electron heat conductivity according to a constant eta (Grad Te / Grad Ne) model. See routine set_transport_eta code for details.
					A model for disruption transport coefficients is available with user_transport.eq.7. See routine set_transport_disruption code for details. Not yet available for WG.
					The value user_transport.eq.8 activates the neoclassical model for computation of the transport coefficients in the core. See routine set_transport_neo and subroutines called for details. Implemented from the NEOART package.
				""", '0'),
   
      'set_transport_eta' : ('', 'real', """
					The last switch is subservient to b2tqna_user_transport, and only used if user_transport.ne.0. When this is the case, the electron perpendicular heat diffusivity and anomalous perpendicular particle transport coefficient are scaled so as to maintain the required_te_gradient (in units of eV/m), at the iyref-th radial ring along the outer midplane. By default, this is the ring immediately inside the separatrix.
					The transport_eta switches are activated when user_transport.eq.3 and allow modifications of the electron heat conductivity according to a constant eta (Grad Te / Grad Ne) model. See routine set_transport_eta code for details.
					A model for disruption transport coefficients is available with user_transport.eq.7. See routine set_transport_disruption code for details. Not yet available for WG.
					The value user_transport.eq.8 activates the neoclassical model for computation of the transport coefficients in the core. See routine set_transport_neo and subroutines called for details. Implemented from the NEOART package.
				""", '2.0'),
   
      'set_transport_eta_alpha' : ('', 'real', """
					The last switch is subservient to b2tqna_user_transport, and only used if user_transport.ne.0. When this is the case, the electron perpendicular heat diffusivity and anomalous perpendicular particle transport coefficient are scaled so as to maintain the required_te_gradient (in units of eV/m), at the iyref-th radial ring along the outer midplane. By default, this is the ring immediately inside the separatrix.
					The transport_eta switches are activated when user_transport.eq.3 and allow modifications of the electron heat conductivity according to a constant eta (Grad Te / Grad Ne) model. See routine set_transport_eta code for details.
					A model for disruption transport coefficients is available with user_transport.eq.7. See routine set_transport_disruption code for details. Not yet available for WG.
					The value user_transport.eq.8 activates the neoclassical model for computation of the transport coefficients in the core. See routine set_transport_neo and subroutines called for details. Implemented from the NEOART package.
				""", '0.5'),
   
      'set_transport_eta_floor' : ('', 'real', """
					The last switch is subservient to b2tqna_user_transport, and only used if user_transport.ne.0. When this is the case, the electron perpendicular heat diffusivity and anomalous perpendicular particle transport coefficient are scaled so as to maintain the required_te_gradient (in units of eV/m), at the iyref-th radial ring along the outer midplane. By default, this is the ring immediately inside the separatrix.
					The transport_eta switches are activated when user_transport.eq.3 and allow modifications of the electron heat conductivity according to a constant eta (Grad Te / Grad Ne) model. See routine set_transport_eta code for details.
					A model for disruption transport coefficients is available with user_transport.eq.7. See routine set_transport_disruption code for details. Not yet available for WG.
					The value user_transport.eq.8 activates the neoclassical model for computation of the transport coefficients in the core. See routine set_transport_neo and subroutines called for details. Implemented from the NEOART package.
				""", '0.1'),
   
      'set_transport_eta_ceiling' : ('', 'real', """
					The last switch is subservient to b2tqna_user_transport, and only used if user_transport.ne.0. When this is the case, the electron perpendicular heat diffusivity and anomalous perpendicular particle transport coefficient are scaled so as to maintain the required_te_gradient (in units of eV/m), at the iyref-th radial ring along the outer midplane. By default, this is the ring immediately inside the separatrix.
					The transport_eta switches are activated when user_transport.eq.3 and allow modifications of the electron heat conductivity according to a constant eta (Grad Te / Grad Ne) model. See routine set_transport_eta code for details.
					A model for disruption transport coefficients is available with user_transport.eq.7. See routine set_transport_disruption code for details. Not yet available for WG.
					The value user_transport.eq.8 activates the neoclassical model for computation of the transport coefficients in the core. See routine set_transport_neo and subroutines called for details. Implemented from the NEOART package.
				""", '10.0'),
   
      'set_transport_iyref' : ('', 'integer', """
					The last switch is subservient to b2tqna_user_transport, and only used if user_transport.ne.0. When this is the case, the electron perpendicular heat diffusivity and anomalous perpendicular particle transport coefficient are scaled so as to maintain the required_te_gradient (in units of eV/m), at the iyref-th radial ring along the outer midplane. By default, this is the ring immediately inside the separatrix.
					The transport_eta switches are activated when user_transport.eq.3 and allow modifications of the electron heat conductivity according to a constant eta (Grad Te / Grad Ne) model. See routine set_transport_eta code for details.
					A model for disruption transport coefficients is available with user_transport.eq.7. See routine set_transport_disruption code for details. Not yet available for WG.
					The value user_transport.eq.8 activates the neoclassical model for computation of the transport coefficients in the core. See routine set_transport_neo and subroutines called for details. Implemented from the NEOART package.
				""", 'See description (integer)'),
   
      'set_transport_required_te_gradient' : ('', 'real', """
					The last switch is subservient to b2tqna_user_transport, and only used if user_transport.ne.0. When this is the case, the electron perpendicular heat diffusivity and anomalous perpendicular particle transport coefficient are scaled so as to maintain the required_te_gradient (in units of eV/m), at the iyref-th radial ring along the outer midplane. By default, this is the ring immediately inside the separatrix.
					The transport_eta switches are activated when user_transport.eq.3 and allow modifications of the electron heat conductivity according to a constant eta (Grad Te / Grad Ne) model. See routine set_transport_eta code for details.
					A model for disruption transport coefficients is available with user_transport.eq.7. See routine set_transport_disruption code for details. Not yet available for WG.
					The value user_transport.eq.8 activates the neoclassical model for computation of the transport coefficients in the core. See routine set_transport_neo and subroutines called for details. Implemented from the NEOART package.
				""", '5.0e4'),
   
      'b2tqna_max_df0' : ('', 'real', """
					Upper and lower limits of the diffusivity coefficients df0 computed in b2tqna for each neutral species.
				""", '1e30'),
   
      'b2tqna_min_df0' : ('', 'real', """
					Upper and lower limits of the diffusivity coefficients df0 computed in b2tqna for each neutral species.
				""", '0.0'),
   
      'b2tqna_ballooning' : ('', 'real', """
					Ballooning model switches. If ballooning.ne.0, then all transport coefficients in cell (i) are rescaled by a factor of ballooning_rescale*abs(bb_ref/bb(i))**ballooning .
					The default value for bb_ref is the arithmetic average of the total magnetic field strength over the entire computational domain. If b2tqna_ballooning_sig.ne.0 (default), the ballooning factor is also applied to the anomalous radial electrical conductivity and the anomalous radial thermo-electric coefficient.
				""", '0.0'),
   
      'b2tqna_ballooning_rescale' : ('', 'real', """
					Ballooning model switches. If ballooning.ne.0, then all transport coefficients in cell (i) are rescaled by a factor of ballooning_rescale*abs(bb_ref/bb(i))**ballooning .
					The default value for bb_ref is the arithmetic average of the total magnetic field strength over the entire computational domain. If b2tqna_ballooning_sig.ne.0 (default), the ballooning factor is also applied to the anomalous radial electrical conductivity and the anomalous radial thermo-electric coefficient.
				""", '1.0'),
   
      'b2tqna_bb_ref' : ('', 'real', """
					Ballooning model switches. If ballooning.ne.0, then all transport coefficients in cell (i) are rescaled by a factor of ballooning_rescale*abs(bb_ref/bb(i))**ballooning .
					The default value for bb_ref is the arithmetic average of the total magnetic field strength over the entire computational domain. If b2tqna_ballooning_sig.ne.0 (default), the ballooning factor is also applied to the anomalous radial electrical conductivity and the anomalous radial thermo-electric coefficient.
				""", 'See description (real)'),
   
      'b2tqna_ballooning_sig' : ('', 'integer', """
					Ballooning model switches. If ballooning.ne.0, then all transport coefficients in cell (i) are rescaled by a factor of ballooning_rescale*abs(bb_ref/bb(i))**ballooning .
					The default value for bb_ref is the arithmetic average of the total magnetic field strength over the entire computational domain. If b2tqna_ballooning_sig.ne.0 (default), the ballooning factor is also applied to the anomalous radial electrical conductivity and the anomalous radial thermo-electric coefficient.
				""", '1'),
   
      'b2sifr_limthee' : ('', 'real', """
					Parameters for the computation of the thermal force term.
				""", '0.3'),
   
      'b2sifr_limthii' : ('', 'real', """
					Parameters for the computation of the thermal force term.
				""", '0.3'),
   
      'b2trcl_cthe' : ('', 'real', """
					Parameters for the computation of the thermal force term.
				""", '0.0'),
   
      'b2trcl_cthi' : ('', 'real', """
					Parameters for the computation of the thermal force term.
				""", '2.65'),
   
      'b2trcl_lambda' : ('', 'real', """
					If lambda is positive, the Coulomb logarithm is set to lambda.
					If lambda is negative, then abs(lambda) is the lower bound to be used when computing the Coulomb logarithm according to the NRL formulae.
					The computation of the Coulomb logarithm takes place in b2tlnl.
					The default formula is to use the Braginskii formulation, which will give the same answer for electron-electron (ee), electron-ion (ei), and ion-ion (ii) collisions. Respectively, non-default values of '1', '2' and '3' for b2tlnl_ii, _ee, and _ei, respectively, make use of the calculation according to Wesson.
				""", '-5.0'),
   
      'b2tlnl_ee' : ('', 'integer', """
					If lambda is positive, the Coulomb logarithm is set to lambda.
					If lambda is negative, then abs(lambda) is the lower bound to be used when computing the Coulomb logarithm according to the NRL formulae.
					The computation of the Coulomb logarithm takes place in b2tlnl.
					The default formula is to use the Braginskii formulation, which will give the same answer for electron-electron (ee), electron-ion (ei), and ion-ion (ii) collisions. Respectively, non-default values of '1', '2' and '3' for b2tlnl_ii, _ee, and _ei, respectively, make use of the calculation according to Wesson.
				""", '0'),
   
      'b2tlnl_ei' : ('', 'integer', """
					If lambda is positive, the Coulomb logarithm is set to lambda.
					If lambda is negative, then abs(lambda) is the lower bound to be used when computing the Coulomb logarithm according to the NRL formulae.
					The computation of the Coulomb logarithm takes place in b2tlnl.
					The default formula is to use the Braginskii formulation, which will give the same answer for electron-electron (ee), electron-ion (ei), and ion-ion (ii) collisions. Respectively, non-default values of '1', '2' and '3' for b2tlnl_ii, _ee, and _ei, respectively, make use of the calculation according to Wesson.
				""", '0'),
   
      'b2tlnl_ii' : ('', 'integer', """
					If lambda is positive, the Coulomb logarithm is set to lambda.
					If lambda is negative, then abs(lambda) is the lower bound to be used when computing the Coulomb logarithm according to the NRL formulae.
					The computation of the Coulomb logarithm takes place in b2tlnl.
					The default formula is to use the Braginskii formulation, which will give the same answer for electron-electron (ee), electron-ion (ei), and ion-ion (ii) collisions. Respectively, non-default values of '1', '2' and '3' for b2tlnl_ii, _ee, and _ei, respectively, make use of the calculation according to Wesson.
				""", '0'),
   
      'b2tfnb_alpha' : ('', 'real', """
					Parameters for the flux limit to the convective neutral flow.
					Alpha is a multiplier to the classical flux limit value.
					The larger α is, the weaker the flux limit is.
					γ is the exponent used in the flux-limiting formula.
					The smaller γ is, the stronger the flux limit is.
					If alpha.eq.0, no flux limit is applied.
					flux_limit_min_ti specifies the minimum ti to be used (in eV).
				""", '0.0'),
   
      'b2tfnb_gamma' : ('', 'real', """
					Parameters for the flux limit to the convective neutral flow.
					Alpha is a multiplier to the classical flux limit value.
					The larger α is, the weaker the flux limit is.
					γ is the exponent used in the flux-limiting formula.
					The smaller γ is, the stronger the flux limit is.
					If alpha.eq.0, no flux limit is applied.
					flux_limit_min_ti specifies the minimum ti to be used (in eV).
				""", '2.0'),
   
      'b2tfnb_flux_limit_min_ti' : ('', 'real', """
					Parameters for the flux limit to the convective neutral flow.
					Alpha is a multiplier to the classical flux limit value.
					The larger α is, the weaker the flux limit is.
					γ is the exponent used in the flux-limiting formula.
					The smaller γ is, the stronger the flux limit is.
					If alpha.eq.0, no flux limit is applied.
					flux_limit_min_ti specifies the minimum ti to be used (in eV).
				""", '0.0'),
   
      'b2tlc0_alpha' : ('', 'real', """
					Parameters for the flux limit to dpa0 - pressure driven neutral diffusion.
					Alpha is a multiplier to the classical flux limit value.
					γ is the exponent used in the flux-limiting formula. If alpha.eq.0, no flux limit is applied.
				""", '0.0 (if b2mn_afn = 0); 1.0 (otherwise)'),
   
      'b2tlc0_gamma' : ('', 'real', """
					Parameters for the flux limit to dpa0 - pressure driven neutral diffusion.
					Alpha is a multiplier to the classical flux limit value.
					γ is the exponent used in the flux-limiting formula. If alpha.eq.0, no flux limit is applied.
				""", '2.0'),
   
      'b2tlh0_alpha' : ('', 'real', """
					Parameters for the flux limit to the heat conductivity of the neutrals. Alpha is a multiplier to the classical flux limit value.
					The larger α is, the weaker the flux limit is.
					γ is the exponent used in the flux-limiting formula.
					The smaller γ is, the stronger the flux limit is.
					If alpha.eq.0, no flux limit is applied.
					flux_limit_min_ti specifies the minimum ti to be used (in eV).
				""", '0.0 (if b2mn_afn = 0); 1.0 (otherwise)'),
   
      'b2tlh0_gamma' : ('', 'real', """
					Parameters for the flux limit to the heat conductivity of the neutrals. Alpha is a multiplier to the classical flux limit value.
					The larger α is, the weaker the flux limit is.
					γ is the exponent used in the flux-limiting formula.
					The smaller γ is, the stronger the flux limit is.
					If alpha.eq.0, no flux limit is applied.
					flux_limit_min_ti specifies the minimum ti to be used (in eV).
				""", '2.0'),
   
      'b2tlh0_flux_limit_min_ti' : ('', 'real', """
					Parameters for the flux limit to the heat conductivity of the neutrals. Alpha is a multiplier to the classical flux limit value.
					The larger α is, the weaker the flux limit is.
					γ is the exponent used in the flux-limiting formula.
					The smaller γ is, the stronger the flux limit is.
					If alpha.eq.0, no flux limit is applied.
					flux_limit_min_ti specifies the minimum ti to be used (in eV).
				""", '0.0'),
   
      'b2tlv0_alpha' : ('', 'real', """
					Parameters for the flux limit to the viscosity of the neutrals. Alpha is a multiplier to the classical flux limit value.
					The larger α is, the weaker the flux limit is.
					γ is the exponent used in the flux-limiting formula.
					The smaller γ is, the stronger the flux limit is.
					If alpha.eq.0, no flux limit is applied.
				""", '0.0 (if b2mn_afn = 0); 1.0 (otherwise)'),
   
      'b2tlv0_gamma' : ('', 'real', """
					Parameters for the flux limit to the viscosity of the neutrals. Alpha is a multiplier to the classical flux limit value.
					The larger α is, the weaker the flux limit is.
					γ is the exponent used in the flux-limiting formula.
					The smaller γ is, the stronger the flux limit is.
					If alpha.eq.0, no flux limit is applied.
				""", '2.0'),
   
      'b2sqcx_styl0' : ('', 'integer', """
					phm0 : Multiplier to the charge exchange rate coefficient. Subservient to styl0: only used if styl0.eq.0 or is.lt.2. If styl0.ne.0, the charge exchange rate coefficients for species of index 2 and above are set to zero.
				""", '0'),
   
      'b2sqcx_phm0' : ('', 'real', """
					phm0 : Multiplier to the charge exchange rate coefficient. Subservient to styl0: only used if styl0.eq.0 or is.lt.2. If styl0.ne.0, the charge exchange rate coefficients for species of index 2 and above are set to zero.
				""", '1.0'),
   
      'eirene_lhalpha' : ('', 'integer', """
					Deprecated. Use "DEFINE_LINES" in block 12 of Eirene input file instead.
				""", '1'),
   
      'eirene_lvib' : ('', 'integer', """
					Deprecated. Use "DEFINE_LINES" in block 12 of Eirene input file instead.
				""", '1'),
   
      'b2tfhi_fflokt' : ('', 'real', """
					fflokt and fconkt are fudge factors to approximate enhanced parallel transport of k due to term related to (fluctuations in parallel current) * (fluctuations in potential)
					In principle this models the same effect as skt_diss (thus: needs b2sikt_fac_sheath_* = 0.0).
				""", '0.0'),
   
      'b2tfhi_fconkt' : ('', 'real', """
					fflokt and fconkt are fudge factors to approximate enhanced parallel transport of k due to term related to (fluctuations in parallel current) * (fluctuations in potential)
					In principle this models the same effect as skt_diss (thus: needs b2sikt_fac_sheath_* = 0.0).
				""", '0.0'),
   
      'b2tfhi_fflozt' : ('', 'real', """
					fflozt and fconzt are fudge factors to the transport of zt. See code for details.
				""", '0.0'),
   
      'b2tfhi_fconzt' : ('', 'real', """
					fflozt and fconzt are fudge factors to the transport of zt. See code for details.
				""", '0.0'),
   
      'b2tqna_keps_init' : ('', 'real', """
					Mechanism to enable a smooth transition between standard anomalous transport coefficients and k(-epsilon)-model coefficients.
					The final coefficients (dna0, vsa0, hcib, hce0, sig0, alf0) are linearly interpolated between the standard and the k(-epsilon) values based on keps_fac.
					keps_fac starts out as b2tqna_keps_init and the value is multiplied by b2tqna_keps_inc at each iteration.
				""", '1.0'),
   
      'b2tqna_keps_inc' : ('', 'real', """
					Mechanism to enable a smooth transition between standard anomalous transport coefficients and k(-epsilon)-model coefficients.
					The final coefficients (dna0, vsa0, hcib, hce0, sig0, alf0) are linearly interpolated between the standard and the k(-epsilon) values based on keps_fac.
					keps_fac starts out as b2tqna_keps_init and the value is multiplied by b2tqna_keps_inc at each iteration.
				""", '1.0'),
   
      'b2tlv0_style' : ('', 'integer', """
					Determines the method for applying flux limiters to fluid neutrals.
					style.eq.0: old treatment where the radial and poloidal conductive fluxes are limited separately.
					style.eq.1: improved treatment (isotropic flux limiters) where the total conductive flux is limited, preventing artificial rotation of the flow.
				""", '1'),
   
      'b2tlc0_style' : ('', 'integer', """
					Determines the method for applying flux limiters to fluid neutrals.
					style.eq.0: old treatment where the radial and poloidal conductive fluxes are limited separately.
					style.eq.1: improved treatment (isotropic flux limiters) where the total conductive flux is limited, preventing artificial rotation of the flow.
				""", '1'),
   
      'b2tlh0_style' : ('', 'integer', """
					Determines the method for applying flux limiters to fluid neutrals.
					style.eq.0: old treatment where the radial and poloidal conductive fluxes are limited separately.
					style.eq.1: improved treatment (isotropic flux limiters) where the total conductive flux is limited, preventing artificial rotation of the flow.
				""", '1'),
   
      'b2tqna_keps_dna_min' : ('', 'real', """
					Minimum transport coefficients for use in k-epsilon model. It is also possible to use these minima for other transport models by setting b2tqna_limit_coeff.eq.1.
				""", '1.0e-2'),
   
      'b2tqna_keps_vsa_min' : ('', 'real', """
					Minimum transport coefficients for use in k-epsilon model. It is also possible to use these minima for other transport models by setting b2tqna_limit_coeff.eq.1.
				""", '1.0e-2'),
   
      'b2tqna_keps_hci_min' : ('', 'real', """
					Minimum transport coefficients for use in k-epsilon model. It is also possible to use these minima for other transport models by setting b2tqna_limit_coeff.eq.1.
				""", '1.0e-2'),
   
      'b2tqna_keps_hce_min' : ('', 'real', """
					Minimum transport coefficients for use in k-epsilon model. It is also possible to use these minima for other transport models by setting b2tqna_limit_coeff.eq.1.
				""", '1.0e-2'),
   
      'b2stbc_bc_ref' : ('', 'real', """
					Under-relaxation factors related to feedback schemes for boundary conditions.
				""", '0.01'),
   
      'b2stbc_bc_ref_ti' : ('', 'real', """
					Under-relaxation factors related to feedback schemes for boundary conditions.
				""", '0.01'),
   
      'b2stbc_bc_ref_te' : ('', 'real', """
					Under-relaxation factors related to feedback schemes for boundary conditions.
				""", '0.01'),
   
      'b2siav_addvis' : ('Physics', 'real', """
					Multiplier to heat flux contribution to divergence of viscosity tensor in the momentum equation.
				""", '1.0'),
   
      'b2siav_addvis1' : ('Physics', 'real', """
					When not equal to '0.0', adds contribution to divergence of viscosity tensor coming from x-variations in B.
				""", '1.0'),
   
      'b2siav_style_qip' : ('Physics', 'integer', """
					If style_qip.eq.1, adds a classical ion heat conductivity term to the heat flux used to compute the heat viscosity current (see manual for full details).
				""", '0'),
   
      'b2npmo_b2sifr_' : ('Physics', 'integer', """
					If b2sigp_style is set to '2', this switch has no effect.
					When set to '1', the new correct form of the friction force is used, applicable for non-hydrogenic plasmas or hydrogenic mixtures.
					The value '0' corresponds to the old SOLPS5.0 treatment. Not recommended unless wanting to recover older 5.0 results.
				""", '1'),
   
      'b2sihs_istyle_Joule_heating' : ('Physics', 'integer', """
					When set to '1', there is no radial contribution in Joule heating because there are no physical reasons to take it into account.
					The value '0' corresponds to the old SOLPS5.0 treatment.
				""", '1'),
   
      'b2sian_phm0' : ('Physics', 'real', """
					Multiplier to the parallel momentum source term associated with the anomalous current. It is recommended '1.0'. Only active if both the ExB and diamagnetic drifts are turned on.
					The value '0.0' corresponds to the old SOLPS5.0 treatment.
				""", '1.0'),
   
      'b2sicf_phm0' : ('Physics', 'real', """
					Multiplier of the centrifugal force term. It is recommended '1.0'.
					The value '0.0' corresponds to the old SOLPS5.0 treatment.
				""", '1.0'),
   
      'b2sicf_phm1' : ('Physics', 'real', """
					Multiplier of the centrifugal force correction term due to linearization.
					It is recommended '1.0'.
					The value '0.0' corresponds to the old SOLPS5.0 treatment.
				""", '1.0'),
   
      'b2news_ExB' : ('Physics', 'real', """
					Real parameter which multiplies ExB flows. If b2news_ExB.eq.0 and b2news_facExB_start.eq.0 then ExB flows are switched off. If b2news_ExB is nonzero, then ExB flows are multiplied by that constant throughout the run.
					See also Run section on switches b2news_facExB_... for more details. A spatial fac_ExB profile is also possible, see Numerics section for details.
				""", '0.0'),
   
      'b2news_vis' : ('Physics', 'real', """
					Real parameter which multiplies the viscous drift flows. If b2news_vis.eq.0 and b2news_facvis_start.eq.0 then the viscous drift flows are switched off. If b2news_vis is nonzero, then the viscous drift flows are multiplied by that constant throughout the run.
					See also Run section on switches b2news_facvis_... for more details. A spatial fac_vis profile is also possible, see Numerics section for details.
				""", '0.0'),
   
      'b2tiner_inert' : ('Physics', 'real', """
					Real parameter which multiplies the ion inertial current.
				""", '1.0'),
   
      'b2tfhe_dia_cur' : ('Physics', 'real', """
					Real parameter which multiplies the diamagnetic current.
				""", '1.0'),
   
      'b2tfhe_vdia_par' : ('Physics', 'real', """
					Real parameter which multiplies the convective heat flux due to grad B-drift of guiding centers in non-modified heat fluxes of electrons and ions.
				""", '1.0'),
   
      'b2tfhe_neutral' : ('Physics', 'real', """
					Real parameter which multiplies the ion-neutral current.
					If b2tfhe_neutral is 0 then the ion-neutral current is switched off otherwise the ion-neutral current is switched on.
					The ion-neutral current also requires either the diamagnetic or ExB drifts to be turned on as well.
				""", '0.0'),
   
      'b2tinnt_fchin_in_core' : ('Physics', 'integer', """
					Integer switch to turn off or on the ion-neutral current in the core region (applies to coupled runs only). This is recommended in cases where the neutral densities are very low in the core region and the ion-neutral current is likely to vary widely from one iteration to the next as a result of Monte Carlo noise.
					If fchin_in_core.eq.0 (default), then fchin is set to zero in the core.
					If fchin_in_core.eq.1, then fchin is unchanged.
					fchin_in_core.eq.1 not yet available for WG.
				""", '0'),
   
      'b2tfhe_PSch' : ('Physics', 'real', """
					Real parameter which multiplies the Pfirsch-Schlueter electron heat flux and conductivity.
				""", '1.0'),
   
      'b2tfhe_vis_par' : ('Physics', 'real', """
					Real parameter which multiplies the current driven by parallel viscosity.
					If b2tfhe_vis_par is 0 then the viscosity-driven current is switched off otherwise the viscosity-driven current is switched on.
				""", '0.0'),
   
      'b2tfhe_vis_q' : ('Physics', 'real', """
					Real parameter which multiplies the current driven by heat viscosity effects.
				""", '1.0'),
   
      'b2tfhe_stochastic' : ('Physics', 'real', """
					Real parameter which turns on stochastic current.
					If b2tfhe_stochastic is 0 then stochastic current is switched off otherwise stochastic current is switched on.
					Not yet available for WG.
				""", '0.0'),
   
      'b2tstch_delta' : ('Physics', 'real', """
					Width of the stochastic current layer (in metres), measured from the separatrix inward, along the poloidal index ixref (given by b2tqna_ixref).
					If b2tfhe_stochastic.ne.0, then b2tstch_delta must be greater than zero.
					Not yet available for WG.
				""", '0.0'),
   
      'b2tstch_sig' : ('Physics', 'real', """
					Multiplier to the magnetic field line stochastic diffusion coefficient, describing the stochastic conductivity.
					Not yet available for WG.
				""", '1.0'),
   
      'b2trno_con_e_stochastic' : ('Physics', 'real', """
					Multiplier to the stochastic conductivity.
					Not yet available for WG.
				""", '1.0'),
   
      'b2trcl_lluciani' : ('Physics', 'integer', """
					If lluciani.ne.0, then transport coefficients on cells belonging to closed field lines are modified according to the Luciani model.
					If lluciani.eq.1, the standard connection length formulation is used.
					If lluciani.eq.2, the old SOLPS4.0 formulation is used for backward compatibility.
					If lluciani.eq.3, Spb's new form Luciani's coefficient.
				""", '3'),
   
      'b2trcl_lthf21' : ('Physics', 'integer', """
					If lthf21.ne.0, then the heat transfer model is modified according to the 21-moment approach. This should only be used for multi-fluid runs.
					Not yet available for WG.
				""", '0'),
   
      'b2trcl_lvis21' : ('Physics', 'integer', """
					If lvis21.ne.0, then the viscosities are modified according to the 21-moment approach. This should only be used for multi-fluid runs. This switch should not be used along with 'b2tfhe_vis_par' to avoid double-counting of classical viscosity effects.
					Not yet available for WG.
				""", '0'),
   
      'b2tral_Zhdanov_closure' : ('Physics', 'integer', """
					If b2tral_Zhdanov_closure.eq.1, the Zhdanov-Grad module is enabled, and fully multi-ion collisional closure for the components along the magnetic field of the vector and tensor moments of the distribution function is applied for all the ions (without specifying main ions and impurities) based on the works of Zhdanov [V. M. Zhdanov, 2002] and Makarov et al. [S. O. Makarov et al., PoP 2021]. Otherwise the standard SOLPS-ITER model is applied.
				""", '0'),
   
      'b2tral_zh_imp_analyt' : ('Physics', 'integer', """
					If b2tral_zh_imp_analyt.eq.0, the Zhdanov-Grad closure method is applied by means of the explicit matrix inversion methed (EMIM).
					If b2tral_zh_imp_analyt.eq.1, the improved analytical method (IAM) is applied. See [S. O. Makarov et al., PoP 2021] for details.
					This switch is subservient to b2tral_Zhdanov_closure.
				""", '0'),
   
      'b2tral_zh_analyt_mdf' : ('Physics', 'integer', """
					If b2tral_zh_analyt_mdf.eq.1, the MDF friction force calculation is applied. See [S. O. Makarov et al., PoP 2021] for details.
					This switch is subservient to b2tral_Zhdanov_closure.
				""", '0'),
   
      'b2tral_Zhdanov_cond' : ('Physics', 'integer', """
					If b2tral_Zhdanov_cond.eq.0, the Braginskii expression for the ion conductivity is used.
					This switch is subservient to b2tral_Zhdanov_closure.
				""", '1'),
   
      'b2tral_Zhdanov_vish' : ('Physics', 'integer', """
					If b2tral_Zhdanov_vish.eq.0, the Braginskii expression for the heat flux dependent viscous stress is used.
					This switch is subservient to b2tral_Zhdanov_closure.
				""", '1'),
   
      'b2tral_Zhdanov_visu' : ('Physics', 'integer', """
					If b2tral_Zhdanov_visu.eq.0, the Braginskii expression for the velocity-dependent viscous stress is used.
					This switch is subservient to b2tral_Zhdanov_closure.
				""", '1'),
   
      'b2tral_zhflcorr' : ('Physics', 'real', """
					Flux-limiting coefficient multiplier.
				""", '3.0'),
   
      'b2tral_zhflcorrh' : ('Physics', 'real', """
					Additional flux-limiting coefficient multiplier for the heat flux.
				""", '0.4'),
   
      'b2tral_zhd_corr' : ('Physics', 'integer', """
					Multiplier to the corrections due to the difference in definition for temperature and Joule heating between Zhdanov and Braginskii.
					This switch is subservient to b2tral_Zhdanov_closure.
				""", '1'),
   
      'b2tral_zhd_corrT' : ('Physics', 'integer', """
					Multiplier to the corrections due to the difference in definition for temperature between Zhdanov and Braginskii in the thermal force calculation.
					This switch is subservient to b2tral_Zhdanov_closure.
				""", '1'),
   
      'b2tral_zhcscorr' : ('Physics', 'integer', """
					If b2tral_zhcscorr.eq.0, the corrections for each individual ion charge state from the isonuclear sequence value are disabled.
					This switch is subservient to b2tral_Zhdanov_closure.
				""", '1'),
   
      'b2tral_zhcscorr_vq' : ('Physics', 'integer', """
					If b2tral_zhcscorr_vq.eq.0, the corrections for each individual ion charge state from the isonuclear sequence value are disabled for the heat stress-viscosity.
					This switch is subservient to b2tral_Zhdanov_closure.
				""", '1'),
   
      'b2sifr_Zhdanov_tf_fr' : ('Physics', 'integer', """
					If b2sifr_Zhdanov_tf_fr.eq.1, the Zhdanov expressions for the thermal and friction forces are used.
					This switch is subservient to b2tral_Zhdanov_closure.
				""", '1'),
   
      'b2sifr_Zhdanov_test' : ('Physics', 'integer', """
					If b2sifr_Zhdanov_test.eq.1, the Zhdanov-Grad calculation takes place, but is not used. To be used for testing purposes.
				""", '0'),
   
      'b2tfhi_Zhdanov_vel_heat' : ('Physics', 'integer', """
					If b2tfhi_Zhdanov_vel_heat.eq.1, the Zhdanov velocity-dependent ion heat flux is used.
					This switch is subservient to b2tral_Zhdanov_closure.
				""", '1'),
   
      'b2tral_zh_tf_toff' : ('Physics', 'string', """
					String of integers with (nspecies*(nspecies+1))/2-nspecies digits. If a digit is {\tt 1}, turn off the thermal force between corresponding species starting from 1 and 2; 1 and 3;....; up to nspecies-1 and nspecies.
					This switch is subservient to b2tral_Zhdanov_closure.
				""", '0'),
   
      'b2tral_zh_vis_type' : ('Physics', 'integer', """
					If b2tral_zh_vis_type.eq.0, the Braginskii-like velocity-dependent stress-viscosity is used.
					If b2tral_zh_vis_type.eq.1, the Zhdanov-like velocity-dependent stress-viscosity is used.
					If b2tral_zh_vis_type.eq.2, the Makarov-like velocity-dependent stress-viscosity is used.
				""", '0'),
   
      'b2npmo_smbvi_factor' : ('Physics', 'real', """
					This switch defines the fraction of the cross-ion part of the stress-viscosity term which is applied. The cross-ion part of the stress-viscosity term can lead to numerical problems. If so, it is recommended to start from '0.0' and increase it step by step.
					This switch is subservient to b2tral_Zhdanov_closure.
				""", '1.0'),
   
      'b2tral_amfact_on' : ('Physics', 'integer', """
					If b2tral_amfact_on.eq.1, the mass correction for the thermal and friction force calculation is applied.
				""", '0'),
   
      'b2tral_amfact_...' : ('Physics', 'real', """
					If b2tral_amfact_on.eq.1, this multiplier is applied for the mass of the species corresponding to isonuclear sequence number '***'. Recall the sequence numbering starts at zero (e.g. b2tral_amfact_000, b2tral_amfact_001, ...).
				""", '1.0'),
   
      'b2npmo_impr_form_fr' : ('Physics', 'integer', """
					If b2npmo_impr_form_fr.eq.1, an improved analytical form for the friction force is computed instead of the form corrresponding to b2sigp_style.eq.2.
					Used only if b2tral_Zhdanov_closure is equal to 0.
				""", '0'),
   
      'b2npmo_impr_form_tf' : ('Physics', 'integer', """
					If b2npmo_impr_form_tf.eq.1, an improved analytical form for the thermal force is computed instead of the form corresponding to b2sigp_style.eq.2.
					Used only if b2tral_Zhdanov_closure is equal to 0.
				""", '0'),
   
      'b2npmo mass multiplicator' : ('Physics', 'real', """
					Using this number the impurity mass can be artificialy increased.
					Used only if b2tral_Zhdanov_closure is equal to 0.
				""", '1.0'),
   
      'b2sqel_artificial_radiation' : ('Physics', 'real', """
					If art_rad.ne.0, then an artificial radiation loss term is added to the electron cooling rate. Art_rad represents the percent fraction of impurities in the plasma.
				""", '0.0'),
   
      'b2stbc_bcene_15_style' : ('Physics', 'integer', """
					If bcene_15_style.eq.0, the electron sheath boundary condition computes the electron current as the difference between the ion flow and the poloidal current.
					If bcene_15_style.eq.1 (recommended, default), the electron current at the sheath is computed directly from the sheath potential drop. This method has proven numerically more stable, especially in cases with drifts.
				""", '1'),
   
      'b2stbc_bceni_15_style' : ('Physics', 'integer', """
					If bceni_15_style.eq.0 (default), use the ion sheath transmission factor specified by ENIPAR(IB,1).
					If bceni_15_style.eq.1, use the self-consistent ion sheath transmission factor implied by the truncated drifting Maxwellian ion distribution determined by the Eirene sheath model (ENIPAR(IB,1) is not used). See Eirene manual Section 1.5.1 for the detailed expression.
				""", '0'),
   
      'b2stbc_bcene_16_style' : ('Physics', 'integer', """
					If bcene_16_style.eq.1, the boundary condition is enforced using the modified fluxes fhe_mdf. Recommended when running cases with drifts.
					bcene_16_style.eq.1 not yet available for WG.
				""", '0'),
   
      'b2stbc_bceni_16_style' : ('Physics', 'integer', """
					If bceni_16_style.eq.1, the boundary condition is enforced using the modified fluxes fhi_mdf. Recommended when running cases with drifts.
					bceni_16_style.eq.1 not yet available for WG.
				""", '0'),
   
      'b2stbc_secmodel' : ('Physics', 'integer', """
					If secmodel.eq.1, then the secondary electron emission coefficient at the plates is computed locally according to a kinetic model, otherwise the default values of cbsch(7,ireg) and/or gammae are used.
					Not yet available for WG.
				""", '0'),
   
      'b2mndr_boundary_sources' : ('Physics', 'integer', """
					If boundary_sources.ne.0, allow for the specification of boundary values for all equations, using BC type 7, provided in the bv_na.dat, bv_ua.dat, bv_te.dat, bv_ti.dat, and bv_po.dat files. Only the files corresponding to the solved equations must be provided. For time-dependent MMS (use_mms.eq.2), boundary values must be provided for each time-step: bv_XX0001.dat, bv_XX0002.dat, bv_XX0003.dat, and so on.
				""", '0'),
   
      'b2mndr_equation_sources' : ('Physics', 'integer', """
					If equation_sources.ne.0, allow for the specification of source term values for all equations, per unit volume, provided in the art_sna.dat, art_smo.dat, art_she.dat, art_shi.dat, and art_sch.dat files. Only the files corresponding to the solved equations must be provided. For time-dependent MMS (use_mms.eq.2), artifical sources must be provided for each time-step: art_sXX0001.dat, art_sXX0002.dat, art_sXX0003.dat, and so on.
				""", '0'),
   
      'b2mndr_coronal_model' : ('Physics', 'integer', """
					Turns on the coronal model if coronal.ne.0. I.e., the reaction rates of all reactions are made density-independent, and the value computed at the lowest density (given in b2ar.dat) is used.
				""", '0'),
   
      'b2mndr_hz' : ('Physics', 'real', """
					hz has been introduced into the new form of the parallel momentum balance equation. If fac_hz = 0.0 then hz = 1 and old form of equations is used. If fac_hz = 1.0 then new form of equations is used.
				""", '1.0'),
   
      'b2tfhe_alfTeEh' : ('Physics', 'real', """
					When set to '1.0', the old form of the electron heat flux calculation is used and b2tfhe_fch_pTe should be set to '0.0'. It is recommended to use 0.0.
					Cannot be set to 1.0 when using the SOLPS5.2 physics model.
				""", '0.0'),
   
      'b2tfhe_fch_pTe' : ('Physics', 'real', """
					When set to '1.0', the new form of the electron heat flux calculation is used and b2tfhe_alfTeEh should be set to '0.0'. It is recommended to use 1.0.
					Cannot be set to 0.0 when using the SOLPS5.2 physics model.
				""", '1.0'),
   
      'b2tfnb_xcur' : ('Physics', 'real', """
					Xcur is a multiplier to the parallel viscosity, perpendicular viscosity, heat viscosity, ion inertial and anomalous current contributions to the ion poloidal flows (particle and energy).
					If set to 0 (default), these currents are carried by electrons. If set to 1, these poloidal currents are carried by the main hydrogenic ions. The latter option can only be used if the plasma has a single majority hydrogenic species. Otherwise, an error will be returned.
				""", '0.0'),
   
      'b2tfnb_ycur' : ('Physics', 'real', """
					Ycur is a multiplier to the parallel viscosity, perpendicular viscosity, heat viscosity, ion inertial and anomalous current contributions to the ion radial flows (particle and energy).
					If set to 0, these currents are carried by electrons. If set to 1 (default), these radial currents are carried by the main hydrogenic ions. The latter option can only be used if the plasma has a single majority hydrogenic species. Otherwise, an error will be returned.
				""", '1.0'),
   
      'b2tfnb_vis_per' : ('Physics', 'real', """
					vis_per is a multiplier to the perpendicular viscosity current contributions to the ion poloidal flows (particle and energy). Subservient to b2tfnb_xcur and b2tfnb_ycur.
					Cannot be used in conjunction with the 9-point stencil numerical treatment. If used with the 5-point stencil treatment and with fluid neutrals, must be equal to b2tfhe_vis_per for numerical stability reasons.
				""", '0.0'),
   
      'b2tfnb_vis_q' : ('Physics', 'real', """
					vis_q is a multiplier to the heat viscosity current contributions to the ion poloidal flows (particle and energy). Subservient to b2tfnb_xcur and b2tfnb_ycur.
				""", '1.0'),
   
      'b2tqce_fke_Zhdanov' : ('Physics', 'integer', """
					When set to '1', the Zhdanov expression is used in the electron thermal conductivity. It is recommended to use 'b2tqce_fke_Zhdanov' '1'.
					This switch is only active if, simultaneously, one has b2tqce_model.eq.1 and b2tfhe_fch_pTe.eq.1.0.
				""", '1'),
   
      'b2tqce_style_guard_cells' : ('Physics', 'integer', """
					When set to '0', b2tqce calculates all classical contributions to the electron transport coefficients on all cells.
					When set to '1', the electrical conductivity (sig) and the thermo-electric coefficient (alf) are not calculated in the guard cells that lie on open flux surfaces.
				""", '0'),
   
      'b2tqna_new_df0' : ('Physics', 'integer', """
					When new_df0.eq.1, the neutral diffusivity is computed according to the local charge exchange, ionisation and elastic collision rates, instead of the standard form with constant cross-sections.
				""", '0'),
   
      'b2tqna_pfr_rescale' : ('Physics', 'real', """
					Scaling factor for all ion and electron transport coefficients inside private flux regions.
				""", '1.0'),
   
      'b2tqna_divsol_rescale' : ('Physics', 'real', """
					Scaling factor for all ion and electron transport coefficients inside divertor SOL regions.
				""", '1.0'),
   
      'b2sifr_phm0' : ('Physics', 'real', """
					Multiplier of the friction term between charged species (only ions in case b2sigp_style.eq.2).
				""", '1.0'),
   
      'b2sifr_phm1' : ('Physics', 'real', """
					If b2sigp_style.eq.2, multiplier to the friction force term between electrons and ions.
					Otherwise, multiplier of the ehxp term in the older expression for the thermal force.
				""", '1.0'),
   
      'b2sifr_phm2' : ('Physics', 'real', """
					Multiplier of the electron thermal gradient term in the thermal force term and parallel current
				""", '1.0'),
   
      'b2sifr_phm3' : ('Physics', 'real', """
					Multiplier of the ion thermal gradient term in the thermal force term.
				""", '1.0'),
   
      'b2tfnb_PSch' : ('Physics', 'real', """
					Multiplier to the Pfirsch-Schlueter flows.
				""", '1.0'),
   
      'b2news_BoRiS' : ('Physics', 'real', """
					The poloidal convective heat flux contains a prefactor of (3/2+BoRiS). The default gives us the internal energy equation. The value BoRiS = 1.0 gives us the total energy equation.
					Only for use to benchmark with codes using the total energy equation. When used, the meaning of fhe and fhi changes from internal energy fluxes to total energy fluxes.
				""", '0.0'),
   
      'b2tfhe_conduction_only' : ('Physics', 'integer', """
					When conduction_only.eq.1, convective heat transfer terms are turned off. Only to be used when benchmarking against pure conduction cases.
				""", '0'),
   
      'b2tlmv_style' : ('Physics', 'integer', """
					If style = 0 then the original form of the viscosity flux limit is used, otherwise the SPb flux limit is used.
				""", '1'),
   
      'b2tlhe_far_sol' : ('Physics', 'integer', """
					EXPERIMENTAL SWITCH GROUP, USE WITH CARE.
					If set to 1, enables gradual modification of the electron heat flux limiter towards low density regions. Above b2tlhe_ne_max (default 1.0e18 m^{-3}), the standard value cflme is used. Below b2tlhe_ne_min (default 1.0e17 m^{-3}), the value b2tlhe_cflme_min is used (default 0.2). For densities in between b2tlhe_ne_min and b2tlhe_ne_max, the heat flux limiter is computed based on linear interpolation between the limiting values.
				""", '0'),
   
      'b2tlhi_far_sol' : ('Physics', 'integer', """
					EXPERIMENTAL SWITCH GROUP, USE WITH CARE.
					If set to 1, enables gradual modification of the ion heat flux limiter towards low density regions. Above b2tlhi_ni_max (default 1.0e18 m^{-3}), the standard value cflmi is used. Below b2tlhi_ni_min (default 1.0e17 m^{-3}), the value b2tlhi_cflmi_min is used (default 1.0e1). For densities in between b2tlhi_ni_min and b2tlhi_ni_max, the heat flux limiter is computed based on linear interpolation between the limiting values.
				""", '0'),
   
      'b2tlmv_far_sol' : ('Physics', 'integer', """
					EXPERIMENTAL SWITCH GROUP, USE WITH CARE.
					If set to 1, enables gradual modification of the parallel viscosity flux limiter towards low density regions. Above b2tlmv_ni_max  (default 1.0e18 m^{-3}), the standard value cflmv is used. Below b2tlmv_ni_min (default 1.0e17 m^{-3}), the value b2tlmv_cflmv_min is used (default 0.5). For densities in between b2tlmv_ni_min and b2tlmv_ni_max, the flux limiter is computed based on linear interpolation between the limiting values.
				""", '0'),
   
      'b2sihs_phm0' : ('Physics', 'real', """
					Multiplier of the contribution to electron heat sources from divergence(ue,ve). This term is superseded by the BoRiS switch if invoked.
				""", '1.0'),
   
      'b2sihs_phm1' : ('Physics', 'real', """
					Multiplier of the contribution to ion heat sources from divergence(ua,va). This term is superseded by the BoRiS switch if invoked.
				""", '1.0'),
   
      'b2sihs_phm2' : ('Physics', 'real', """
					Multiplier of the contribution to ion heat sources from viscous heating due to poloidal velocity differences. This term is superseded by the BoRiS switch if invoked.
				""", '1.0'),
   
      'b2sihs_phm3' : ('Physics', 'real', """
					Multiplier of the contribution to electron heat sources from Joule heating (electron-ion friction).
				""", '1.0'),
   
      'b2sihs_phm4' : ('Physics', 'real', """
					Multiplier of the contribution to ion heat sources from atom-atom friction. This term is superseded by the BoRiS switch if invoked.
				""", '1.0'),
   
      'b2sihs_phm5' : ('Physics', 'real', """
					Multiplier of the contribution to electron heat sources from divergence of the electrical drift. That contribution is also multiplied by facExB.
				""", '1.0'),
   
      'b2sihs_phm6' : ('Physics', 'real', """
					Multiplier of the contribution to ion heat sources from divergence of the electrical drift. That contribution is also multiplied by facExB.
				""", '1.0'),
   
      'b2sihs_phm7' : ('Physics', 'real', """
					Multiplier of the contribution to heat sources from friction due to diamagnetic velocities. Normally already included in 'phm3' term above.
				""", '0.0'),
   
      'b2sihs_phm8' : ('Physics', 'real', """
					Multiplier of the contribution to heat sources from viscous heating due to radial velocity differences. This term is only included when using b2nph9_style.eq.1 or b2npht_style.eq.1 (defaults). This term is superseded by the BoRiS switch if invoked.
				""", '1.0'),
   
      'b2sdia_facgt' : ('Physics', 'real', """
					Multiplier of the contribution to electron and ion heat sources from divergence of the gradTxB heat flux. That contribution is also multiplied by facdrift. This term is no longer needed as it has been transferred from being a source to being included in the flows.
				""", '0.0'),
   
      'b2sral_style' : ('Physics', 'integer', """
					When set to '0' or '2', the code calls the standard b2stbc routine, which uses the particle flux with drift terms included in the expression of the electron particle flux (fne). Option '1' is obsolete. It is recommended '2'.
				""", '2'),
   
      'b2sqel_phm0' : ('Physics', 'real', """
					Multiplier to the ionisation rate coefficient.
				""", '1.0'),
   
      'b2sqel_phm1' : ('Physics', 'real', """
					Multiplier to the recombination rate coefficient.
				""", '1.0'),
   
      'b2sqel_phm2' : ('Physics', 'real', """
					Multiplier to the heat loss rate coefficient.
				""", '1.0'),
   
      'b2stel_phm0' : ('Physics', 'real', """
					Multiplier of the sources due to atomic physics.
				""", '1.0'),
   
      'b2tfhe_lim_flux' : ('Physics', 'integer', """
					If '0', flux limit is not applied directly to the electron heat flux but is applied through transport coefficients if 'b2trcl_conductive_limit' is '1'. It is recommended '0'.
					b2tfhe_lim_flux.eq.1 not yet available for WG.
				""", '0'),
   
      'b2tfhi_lim_flux' : ('Physics', 'integer', """
					If '0', flux limit is not applied directly to the ion heat flux but is applied through transport coefficients if 'b2trcl_conductive_limit' is '1'. It is recommended '0'.
					b2tfhi_lim_flux.eq.1 not yet available for WG.
				""", '0'),
   
      'b2treq_phm0' : ('Physics', 'real', """
					Multiplier to the temperature equipartition term.
				""", '1.0'),
   
      'b2tqca_phm0' : ('Physics', 'real', """
					Multiplier for the classical parallel viscosity.
				""", '1.0'),
   
      'b2tqca_model' : ('Physics', 'integer', """
					If model.eq.1, use the Balescu formulation from SOLPS5.2 classical parallel ion heat diffusivity.
					If model.eq.2, use the older Braginskii SOLPS4.0 model.
					Note: old option model.eq.3 removed, replaced with model.eq.1., but numerical treatment w.r.t. factor 4/3 according to old model.eq.3.
				""", '1'),
   
      'b2tqce_model' : ('Physics', 'integer', """
					If model.eq.1, use the fitted Balescu formulation from SOLPS5.0 classical parallel electron heat diffusivity.
					If model.eq.2, use the older Braginskii SOLPS4.0 model.
					If model.eq.3, use the 21-moment Balescu results.
				""", '1'),
   
      'b2tqna_model_sig' : ('Physics', 'integer', """
					If '1', use constant density in core region to calculate anomalous conductivity sig0=dfsig*qe*ne(nmdpl,-1), nmdpl - number of midplane cell. If '0', use sig0=dfsig*qe*ne(x,y)
				""", '0'),
   
      'b2trno_csig_an_style' : ('Physics', 'integer', """
					If '1', the anomalous contributions in the parallel direction to the electrical conductivity csig and the thermo-electric coefficient calf are zeroed out.
				""", '1'),
   
      'b2tqin_csigin_style' : ('Physics', 'integer', """
					Integer switch to choose the expression for the ion-neutral conductivity.
					If '1', the ion-neutral conductivity is computed from hydrogen gas diffusivity (SOLPS5.2 treatment).
					If '0' (default), it is computed from the local CX rate (SOLPS5.0/5.1 and AFN treatments).
				""", '0'),
   
      'b2trno_pol_anom_scale' : ('Physics', 'real', """
					If pol_anom_scale.ne.1, the poloidal anomalous transport coefficients are scaled by the number. To get the same treatment as setting the old switch (radial_only) to 1, set the new switch to 0.0.
					This multiplication is to only take place for charged species.
				""", '1.0'),
   
      'eirene_repeat_first_call' : ('Physics', 'integer', """
					If &gt; 0 then repeats the first call to Eirene in eirene_mc so many times.
					Useful if a density feedback gas puff is being used because the flux passed to Eirene on its first call is ignored (instead the value in the Eirene input file is used).
				""", '1'),
   
      'eirene_use_recyceir' : ('Physics', 'integer', """
					If &gt; 0 use recyceir (non species dependent) to specify the recycling coefficients, else if 0 use recyc (species dependent).
				""", '1'),
   
      'eirene_ionising_core' : ('Physics', 'integer', """
					If &lt;&gt; 0 then recycles the neutral flux having crossed the core boundary within Eirene as ions. The recycling is modulated as per the poloidal density distribution of the ions, and neutrals come back as fully-stripped ions.
					'eirene_ionizing_core' is an alias for this switch.
					If the value = 1, then the flux is added by direct modification of the sources in the guard cells --- this will only work if a standard flux boundary condition is applied at that boundary.
					If the value is &lt; 0, then the absolute value specifies which boundary in b2.boundary.parameters is to be used. This will only work for the BCCON = 13 type boundary condition, for which a negative value for ionizing_core is required.
					Cannot be used in conjunction with 'eirene_ank_mods'.
					Use of this switch is not allowed if the core boundary condition is not of a flux type. Moreover, certain boundary conditions expressly include the flux of neutrals already (BCCON = 6, 19, 21, 23, 26, or 27), in which case use of this switch is redundant and should be avoided.
				""", '0'),
   
      'eirene_background' : ('Physics', 'integer', """
					If eirene_background.eq.0, the ion velocities passed to Eirene to be used for the collisions are based on grad-B and ExB drifts (vadia + vaecrb).
					If eirene_background.eq.1, these velocities contain the full diamagnetic and ExB drifts (wadia + vaecrb).
					Note: recycling fluxes are always computed based on grad-B and ExB drifts only (and are not affected by this switch), because diamagnetic drift flows largely close within the sheath.
				""", '1'),
   
      'eirene_sheath_pot' : ('Physics', 'integer', """
					If eirene_sheath_pot.eq.1, the sheath potential drop as computed by B2.5 (i.e. including effects of parallel currents, secondary electron emission, etc.) is passed to EIRENE to compute ion acceleration in the sheath.
					If eirene_sheath_pot.eq.0, the sheath potential drop is	recomputed by EIRENE, usually assuming zero current and secondary electron emission.
				""", '1'),
   
      'b2mndr_atomic_physics_rescale' : ('Physics', 'integer', """
					If atomic_physics_rescale is not 0, then the code will rescale the rates stored in b2frates according to the multipliers given in the b2.atomic_physics_rescale.parameters inputfile before making use of them.
				""", '0'),
   
      'neoclassical_ic' : ('Physics', 'integer', """
					..set the contribution ic in NEOART
					0 --- classical particle flux
					1 --- banana plateau contribution
					2 --- Pfirsch-Schlueter contribution
					3 --- both banana and PS
					4 --- all contributions
					mind that B2.5 already calculates the classical transport !
					avoid double transport, 0+4 for cross-checks only !
				""", '3'),
   
      'b2mndr_solve_keps' : ('Physics', 'integer', """
					Main switch controlling the use of the k(-eps)-model. In this model, anomalous transport coefficients are determined self-consistently through the solution of an additional transport equation for the turbulent kinetic energy k (variable "kt" in the code) and possibly the turbulent enstrophy zeta (variable "zt" in the code). Note that both the k and k-eps models are currently under active development/testing, and should be used with care. In particular, the k-eps model (option '2') is not suitable for routine testing yet.
					If '0': k(-eps)-model not used.
					If '1': one additional transport equation solved for k.
					If '2': two additional transport equations solved for k and zeta. Warning: under development - expert use only!
					Note: solutions to these equations are only used to compute the transport coefficients if the switch b2tqna_transport_keps is set.
				""", '0'),
   
      'b2tqna_transport_keps' : ('Physics', 'integer', """
					Compute transport coefficients based on k(-eps)-model.
					If '0': transport coefficients not computed based on k(-eps)-model.
					If '1': transport coefficients computed using k-model (i.e. based on kt).
					If '2': transport coefficients computed using k-eps model (i.e. based on kt and zt). Warning: under development - expert use only!
				""", '0'),
   
      'b2tqna_keps_local' : ('Physics', 'integer', """
					If '0': use Larmor radius at OMP separatrix in k(-eps)-model.
					If '1': use local Larmor radius for each cell in k(-eps)-model.
				""", '1'),
   
      'b2tqna_keps_iout' : ('Physics', 'integer', """
					If '1': print output for k(-eps)-model.
				""", '0'),
   
      'b2tqna_keps_cd' : ('Physics', 'real', """
					Multiplier for the diffusion coefficient in the k(-eps) model. Recommended range: 0.1 ... 1.0
				""", '0.1'),
   
      'b2tqna_keps_shear' : ('Physics', 'real', """
					Multiplier for the shear contribution to the diffusion coefficient in the k(-eps) model.
					Only affects results if ExB drifts are present.
				""", '0.0'),
   
      'b2tqna_keps_heat' : ('Physics', 'real', """
					Multiplier for the electron heat conductivity (w.r.t. diffusion coefficient).
				""", '2.0'),
   
      'b2tqna_keps_heat_i' : ('Physics', 'real', """
					Multiplier for the ion heat conductivity (w.r.t. diffusion coefficient).
				""", '2.0'),
   
      'b2tqna_keps_visc' : ('Physics', 'real', """
					Multiplier for the ion viscosity (w.r.t. diffusion coefficient).
				""", '0.2'),
   
      'b2tqna_keps_sig' : ('Physics', 'real', """
					Multiplier for the anomalous electrical conductivity (w.r.t. diffusion coefficient x qe x ne(omp)).
				""", '1e-4'),
   
      'b2tqna_keps_alf' : ('Physics', 'real', """
					Multiplier for the anomalous thermo-electric coefficient (w.r.t. diffusion coefficient x sqrt(qe/te) x ne(omp)).
				""", '1e-4'),
   
      'b2tqna_keps_dkt' : ('Physics', 'real', """
					Multiplier for the k-conductivity (w.r.t. diffusion coefficient).
				""", '0.1'),
   
      'b2tqna_keps_dzt' : ('Physics', 'real', """
					Multiplier for the diffusivity in z-equation (w.r.t. diffusion coefficient).
				""", '0.1'),
   
      'b2tfhe_vis_kt' : ('Physics', 'real', """
					Multiplier to the perpendicular current due to Reynolds-stress in k-model.
				""", '0.0'),
   
      'b2tfhi_fsigkt' : ('Physics', 'real', """
					Multiplier for the parallel transport term of kt.
				""", '0.1'),
   
      'b2sikt_model' : ('Physics', 'integer', """
					Model to compute the sources in the energy equations due to the k-eps model. Currently only a single model is available.
				""", '1'),
   
      'b2sikt_style' : ('Physics', 'integer', """
					Currently only a single computation style for the sources in the energy equations due to the k-eps model is available.
				""", '0'),
   
      'b2sikt_sheath_local' : ('Physics', 'integer', """
					If '0': use sound speed, connection length, and Larmor radius at OMP in k(-eps)-model.
					If '1': use local sound speed, connection length, and Larmor radius.
				""", '1'),
   
      'b2sikt_kt_source_stab' : ('Physics', 'integer', """
					Numerical stabilization of sources. See code for details.
				""", '1'),
   
      'b2sikt_fac_diss' : ('Physics', 'real', """
					Multiplier for the dissipation term of kt in the SOL region.
				""", '10.0'),
   
      'b2sikt_fac_diss_core' : ('Physics', 'real', """
					Multiplier for the dissipation term of kt in the core region.
				""", '10.0'),
   
      'b2sikt_fac_sheath' : ('Physics', 'real', """
					Multiplier for the sheath loss term of kt in the SOL region.
				""", '0.0'),
   
      'b2sikt_fac_sheath_core' : ('Physics', 'real', """
					Multiplier for the sheath loss term of kt in the core region.
				""", '0.0'),
   
      'b2sikt_fac_diss_core_mode' : ('Physics', 'integer', """
					If '0': use connection length in expression for dissipation term of kt.
					If '1': use b2sikt_fac_diss_lpar in expression for dissipation term of kt.
				""", '0'),
   
      'b2sikt_min_source' : ('Physics', 'integer', """
					If '1': sets minimum source for k to zero.
				""", '0'),
   
      'b2sikt_fac_aniso' : ('Physics', 'integer', """
					If '1': add anisothermal contribution to transport coefficients from k-(epsilon)-model.
				""", '1'),
   
      'b2sikt_fac_vis_RS' : ('Physics', 'real', """
					Multiplier for Reynolds-stress turbulent viscosity in k-model equations. Only active if ExB drifts are present.
				""", '0.0'),
   
      'b2tfhi_fkt_hie' : ('Physics', 'real', """
					Multiplier for transport of k associated with turbulent ExB heat fluxes.
				""", '0.0'),
   
      'keps_anom_he_model' : ('Physics', 'integer', """
					If set to 0, uses multiplier 5/2 for the anomalous convective and conductive heat fluxes associated with anomalous density transport, as per the SOLPS5.2 physics model.
					If set to 1 (default), uses multiplier 3/2 for the anomalous convective and conductive heat fluxes associated with electrostatic ExB drift turbulence, consistent with the keps-model derivation.
					If set to 2 (experimental), additionally assumes the corresponding physical fluxes across surfaces/boundaries to have multiplier 3/2.
				""", '1'),
   
      'b2mn_afn' : ('Physics', 'integer', """
					Main switch to turn on the AFN model for hydrogenic neutrals. If this switch is turned on, some default values are changed (see description of the corresponding switches).
				""", '0'),
   
      'b2mn_spatial_hybrid' : ('Physics', 'integer', """
					Switch to turn on the spatially hybrid fluid-kinetic neutral model. For multispecies simulations, the hybrid approach can only be used for the hydrogenic neutrals. For other species, you can use either a fully kinetic or purely fluid approach.
				""", '0'),
   
      'b2stbr_recycle_afn' : ('Physics', 'integer', """
					When set to 1, the AFN recycling boundary conditions are used for hydrogenic neutrals. When b2mn_afn.ne.0 and there is no specification of b2stbr_recycle_afn, the switch is automatically set to 1.
				""", '0'),
   
      'b2stbr_afn_bcs_use_coarse' : ('Physics', 'integer', """
					When set to 1, the coarse representation of the integrated TRIM reflection coefficients is used for the AFN boundary conditions, which is expected to be sufficient. In case you want to use the original fine representation, use b2stbr_afn_bcs_use_coarse = 0. However, the fine representation is only present for D on Be, C and W.
				""", '1'),
   
      'b2tqna_transport_afn' : ('Physics', 'integer', """
					When set to 1, the AFN transport coefficients are used for hydrogenic neutrals. When b2mn_afn.ne.0 and there is no specification of b2stbr_transport_afn, the switch is automatically set to 1.
				""", '0'),
   
      'b2tqna_afn_vnn' : ('Physics', 'integer', """
					When set to 1, a collision frequency related to neutral-neutral collisions is added to the AFN transport coefficients. This is an ad-hoc model for fluid neutral transport in regions where plasma density is extremely low and CX effectively absent (e.g. below dome, far-SOL,...). When set to 0, the correction is not added.
				""", '1'),
   
      'b2tqna_afn_vnn_ndiff' : ('Physics', 'integer', """
					When set to 1, perpendicular transport in the AFN model due to neutral-neutral collisions is modelled as density diffusion rather than pressure diffusion. When set to 0, it is modelled as pressure diffusion.
				""", '0'),
   
      'b2mn_tn_style' : ('Physics', 'integer', """
					0: solving the total energy equation for all ion + (fluid) neutral species together; 1: solving the total energy equation without the contributions from hydrogenic neutrals. It is still assumed that the hydrogenic neutrals have the same temperature as the ions, i.e. tn=ti. (not recommended to turn on); 2: separate energy equation for the hydrogenic neutrals (tn.ne.ti). For simulations with hydrogenic mixtures and b2mn_tn_style = 2, a total energy equation for all hydrogenic neutrals together will be solved assuming tn for each hydrogenic neutral species.
				""", '0'),
   
      'use_auto_spatial_hyb' : ('Physics', 'integer', """
					Advanced hybrid option. Forbidden to use for multispecies simulations (ns &gt; 1) and only in use for the strata with HYB_TYPE='A'.
					The local charge-exchange Knudsen number Kn is calculated at the boundary.
					If (Kn &lt; auto_spatial_hyb_Kn_1) then the recycled atom is treated as a fluid.
					If (Kn &gt; auto_spatial_hyb_Kn_2) then the recycled atom is treated kinetically.
					(otherwise) linear combination between fluid and kinetic.
				""", '0'),
   
      'l_macro_afn' : ('Physics', 'real', """
					Macroscopic length scale (in m) used to calculate the local Knudsen number.
				""", '0.1'),
   
      'b2stbr_kn_b1' : ('Physics', 'real', """
					Should be used in combination with MAXW in b2.neutrals.parameters (see description MAXW).
				""", '0.01'),
   
      'b2stbr_kn_b2' : ('Physics', 'real', """
					Should be used in combination with MAXW in b2.neutrals.parameters (see description MAXW).
				""", '0.1'),
   
      'auto_spatial_hyb_Kn_1' : ('Physics', 'real', """
					Should be used in combination with use_auto_spatial_hyb (see description use_auto_spatial_hyb).
				""", '0.0'),
   
      'auto_spatial_hyb_Kn_2' : ('Physics', 'real', """
					Should be used in combination with use_auto_spatial_hyb (see description use_auto_spatial_hyb).
				""", '0.0'),
   
      'b2stbr_remove_fc_el' : ('Physics', 'integer', """
					When set to 1, the energy required for the Franck-Condon dissociation of the thermally released particles at the surfaces in the AFN boundary conditions is subtracted from the electron energy equation. It is not recommended to turn this switch on, because it seems to lower the electron temperature to unrealistic values.
				""", '0'),
   
      'b2trcl_min_collisions' : ('Physics', 'real', """
					Defines the style of the ion heat flux limit. If the number of collisions in the flux tube (determined by its average collisionnality) is larger than the value in the key, the old style of ion flux limit will be applied. Otherwise the new style (flux limit is defined by the number of collisions) will be applied.
				""", '0.0'),
   
      'b2stbc_delpo' : ('Physics', 'real', """
					Potential drop used for BCENI/E = 15 when the potential equation is not solved (pot_eq.ne.1), in units of the local electron temperature.
				""", '3.1'),
   
      'b2tqna_limit_coeff' : ('Physics', 'integer', """
					b2tqna_limit_coeff.ne.0: the minimum transport coefficients dna_min, vsa_min, hci_min and hce_min are for whatever transport model is selected.
					b2tqna_limit_coeff.eq.0: the minimum transport coefficients dna_min, vsa_min, hci_min and hce_min are only used for the k-epsilon model.
				""", '0'),
   
      'b2siav_cqip1' : ('Physics', 'real', """
					Constant c_q1 in calculation of additional viscosity terms calculated in b2siav.
				""", '0.5'),
   
      'b2sigp_phm0' : ('Physics', 'real', """
					Multiplier for the pressure gradient term. Setting b2sigp_phm0.ne.1.0 should only be done for specific testing purposes.
				""", '1.0'),
   
      'b2nxfv_phm0' : ('Physics', 'real', """
					Multiplier for the convective term due to new form of ion viscosity term in the momentum correction equation. Applies to hydrogenic ions and fluid neutrals.
				""", '1.0'),
   
      'b2nxfv_phm1' : ('Physics', 'real', """
					Multiplier for the convective term due to new form of ion viscosity term in the momentum correction equation. Applies only to hydrogenic fluid neutrals.
				""", '1.0'),
   
      'b2stbc_phm0' : ('Physics', 'real', """
					Multiplier for radial diamagnetic current in BCPOT=12.
				""", '1.0'),
   
      'b2stbc_phm1' : ('Physics', 'real', """
					Multiplier for radial inertial current in BCPOT=12.
				""", '1.0'),
   
      'b2stbm_internal_energy_sources' : ('Physics', 'integer', """
					internal_energy_sources.eq.0: the externally provided energy sources are total energy sources and a conversion to internal energy sources is performed.
					internal_energy_sources.eq.1: the externally provided energy sources are already internal energy sources.
				""", '0'),
   
      'b2tfhe_anomalous' : ('Physics', 'real', """
					Multiplier to the anomalous current.
				""", '1.0'),
   
      'b2tanml_anomalous' : ('Physics', 'real', """
					The correct switch is now b2tfhe_anomalous. b2tanml_anomalous is kept for backward compatibility. b2tanml_anomalous will only be read if b2tfhe_anomalous.eq.1.0.
				""", '1.0'),
   
      'b2tqna_cfvma' : ('Physics', 'real', """
					Anomalous velocity in parallel momentum balance equation.
				""", '0.0'),
   
      'b2mndr_na_eps' : ('', 'real', """
					The five switches above are safeguards numbers for when printing changes after a time step. The change is computed as: deltaX = abs((X(t)-X(t-1))/(X(t)+X_eps))
				""", '1.0e19'),
   
      'b2mndr_po_eps' : ('', 'real', """
					The five switches above are safeguards numbers for when printing changes after a time step. The change is computed as: deltaX = abs((X(t)-X(t-1))/(X(t)+X_eps))
				""", '1.0e+1'),
   
      'b2mndr_te_eps' : ('', 'real', """
					The five switches above are safeguards numbers for when printing changes after a time step. The change is computed as: deltaX = abs((X(t)-X(t-1))/(X(t)+X_eps))
				""", '1.0e+1'),
   
      'b2mndr_ti_eps' : ('', 'real', """
					The five switches above are safeguards numbers for when printing changes after a time step. The change is computed as: deltaX = abs((X(t)-X(t-1))/(X(t)+X_eps))
				""", '1.0e+1'),
   
      'b2mndr_ua_eps' : ('', 'real', """
					The five switches above are safeguards numbers for when printing changes after a time step. The change is computed as: deltaX = abs((X(t)-X(t-1))/(X(t)+X_eps))
				""", '1.0e+4'),
   
      'tallies_netcdf' : ('', 'integer', """
					If tallies_netcdf.ne.0, the file 'b2tallies.nc' is created, which contains the regional tallies in CDF format. If b2mndr_stim.lt.0, data from the current run is appended to the existing b2tallies.nc file, otherwise the file is overwritten.
					If b2mndt_av_ntim_batch.gt.0, the file 'b2batch.nc' is created, which contains the batch averages of the tallies.
					If b2wall_netcdf.ne.0, the file 'b2wall.nc' is created, which contains the wall tallies in CDF format [written every b2wall_netcdf main calls]. If b2mndr_stim.lt.0, data from the current run is appended to the existing b2wall.nc file, otherwise the file is overwritten.
					If balance_netcdf.ne.0, the file 'balance.nc' is created, which contains all of the arrays required by the balance post-processing routines, in CDF format.
					If balance_average.ne.0, the balance arrays are averaged over the number of completed timesteps (itim).
				""", '0'),
   
      'b2stbr_b2wall_netcdf' : ('', 'integer', """
					If tallies_netcdf.ne.0, the file 'b2tallies.nc' is created, which contains the regional tallies in CDF format. If b2mndr_stim.lt.0, data from the current run is appended to the existing b2tallies.nc file, otherwise the file is overwritten.
					If b2mndt_av_ntim_batch.gt.0, the file 'b2batch.nc' is created, which contains the batch averages of the tallies.
					If b2wall_netcdf.ne.0, the file 'b2wall.nc' is created, which contains the wall tallies in CDF format [written every b2wall_netcdf main calls]. If b2mndr_stim.lt.0, data from the current run is appended to the existing b2wall.nc file, otherwise the file is overwritten.
					If balance_netcdf.ne.0, the file 'balance.nc' is created, which contains all of the arrays required by the balance post-processing routines, in CDF format.
					If balance_average.ne.0, the balance arrays are averaged over the number of completed timesteps (itim).
				""", '0'),
   
      'balance_netcdf' : ('', 'integer', """
					If tallies_netcdf.ne.0, the file 'b2tallies.nc' is created, which contains the regional tallies in CDF format. If b2mndr_stim.lt.0, data from the current run is appended to the existing b2tallies.nc file, otherwise the file is overwritten.
					If b2mndt_av_ntim_batch.gt.0, the file 'b2batch.nc' is created, which contains the batch averages of the tallies.
					If b2wall_netcdf.ne.0, the file 'b2wall.nc' is created, which contains the wall tallies in CDF format [written every b2wall_netcdf main calls]. If b2mndr_stim.lt.0, data from the current run is appended to the existing b2wall.nc file, otherwise the file is overwritten.
					If balance_netcdf.ne.0, the file 'balance.nc' is created, which contains all of the arrays required by the balance post-processing routines, in CDF format.
					If balance_average.ne.0, the balance arrays are averaged over the number of completed timesteps (itim).
				""", '0'),
   
      'balance_average' : ('', 'integer', """
					If tallies_netcdf.ne.0, the file 'b2tallies.nc' is created, which contains the regional tallies in CDF format. If b2mndr_stim.lt.0, data from the current run is appended to the existing b2tallies.nc file, otherwise the file is overwritten.
					If b2mndt_av_ntim_batch.gt.0, the file 'b2batch.nc' is created, which contains the batch averages of the tallies.
					If b2wall_netcdf.ne.0, the file 'b2wall.nc' is created, which contains the wall tallies in CDF format [written every b2wall_netcdf main calls]. If b2mndr_stim.lt.0, data from the current run is appended to the existing b2wall.nc file, otherwise the file is overwritten.
					If balance_netcdf.ne.0, the file 'balance.nc' is created, which contains all of the arrays required by the balance post-processing routines, in CDF format.
					If balance_average.ne.0, the balance arrays are averaged over the number of completed timesteps (itim).
				""", '0'),
   
      'eirene_savef30' : ('', 'integer', """
					For coupled runs, the code will create two files named fort.30 and fort.31, containing the plasma geometry and plasma state, respectively, for use by Eirene. This happens irrespective of the setting of the two switches above. If however, the user wishes to obtain these files for a non-coupled run, then these two switches can be set to 1 and the files will then be produced at the end of the run. If savef31.lt.0, then a fort.31.###### file is produced after every B2.5 time step. Additionally, if savef31.ne.0, the fort.31 file will be updated before every Eirene call for coupled runs.
				""", '0'),
   
      'eirene_savef31' : ('', 'integer', """
					For coupled runs, the code will create two files named fort.30 and fort.31, containing the plasma geometry and plasma state, respectively, for use by Eirene. This happens irrespective of the setting of the two switches above. If however, the user wishes to obtain these files for a non-coupled run, then these two switches can be set to 1 and the files will then be produced at the end of the run. If savef31.lt.0, then a fort.31.###### file is produced after every B2.5 time step. Additionally, if savef31.ne.0, the fort.31 file will be updated before every Eirene call for coupled runs.
				""", '0'),
   
      'b2ux5p_nltrsol' : ('', 'integer', """
					Output flag for the matrix solvers. Larger numbers mean increasing output level.
				""", '2'),
   
      'b2ux7p_nltrsol' : ('', 'integer', """
					Output flag for the matrix solvers. Larger numbers mean increasing output level.
				""", '2'),
   
      'b2ux9p_nltrsol' : ('', 'integer', """
					Output flag for the matrix solvers. Larger numbers mean increasing output level.
				""", '2'),
   
      'b2uxus_nltrsol' : ('', 'integer', """
					Output flag for the matrix solvers. Larger numbers mean increasing output level.
				""", '2'),
   
      'b2mndr_idout0' : ('', '', """
					idout0 and idout1 specify the desired selection of output segments; idout0 for output before the calculation and idout1 for output at the conclusion of the calculation. The generic description of either of these 'idout' variables follows. idout specifies the desired selection of output segments for printed and graphical output. Associated with each segment is a four-character word, which is identified on the printed output. (The same word may be associated with several segments.) A particular segment will be produced only if its associated word has a match, as defined by the routine strmas, in idout.
				""", 'pgnl;pgmm;pzmm'),
   
      'b2mndr_idout1' : ('', '', """
					idout0 and idout1 specify the desired selection of output segments; idout0 for output before the calculation and idout1 for output at the conclusion of the calculation. The generic description of either of these 'idout' variables follows. idout specifies the desired selection of output segments for printed and graphical output. Associated with each segment is a four-character word, which is identified on the printed output. (The same word may be associated with several segments.) A particular segment will be produced only if its associated word has a match, as defined by the routine strmas, in idout.
				""", 'pzmm'),
   
      'b2mndr_b2time' : ('Output', 'integer', """
					Specifies the number of timesteps between writes of the b2time.nc time-dependent file. If b2time.gt.0, always writes out on the last timestep. If b2mndr_stim.lt.0, data from the current run is appended to the existing b2time.nc file, otherwise the file is overwritten.
				""", '1'),
   
      'b2mndr_tally' : ('Output', 'integer', """
					Specifies the number of timesteps between writes of tallies. If tally.gt.0, always writes out on the last timestep.
				""", '1'),
   
      'b2mndt_moitlv' : ('Output', 'integer', """
					Controls detailed monitoring output. moitlv.eq.-1 means no output, moitlv.eq.0 means output once per timestep, moitlv.eq.1 means output once per nstg0 iteration, moitlv.eq.2 means output once per nstg1 iteration and moitlv.eq.3 means output once per nstg2 iteration. See 'b2mndr_nstg?' description in Run section for more details.
				""", '-1'),
   
      'b2mndt_moqtlv' : ('Output', 'integer', """
					Controls quick trace output. moqtlv.eq.-1 means no output, moqtlv.eq.0 means output once per timestep, moqtlv.eq.1 means output once per nstg0 iteration, moqtlv.eq.2 means output once per nstg1 iteration and moqtlv.eq.3 means output once per nstg2 iteration. See 'b2mndr_nstg?' description in Run section for more details.
				""", '3'),
   
      'b2mndr_mvnum' : ('Output', 'integer', """
					Specifies the maximum number of instances at which movie data will be output.
				""", '0'),
   
      'b2mndr_mvinc' : ('Output', 'integer', """
					Specifies the number of timesteps between movie output. If greater than 1 and the last timestep does not correspond to a planned frame, an extra endstate frame is added.
				""", '1'),
   
      'b2mndr_plasnum' : ('Output', 'integer', """
					Specifies the maximum number of instances at which extra writes of b2fplasmf.xxxx will occur.
				""", '0'),
   
      'b2mndr_plasinc' : ('Output', 'integer', """
					Specifies the number of timesteps between b2fplasmf.xxxx writes.
				""", '1'),
   
      'b2mndr_cdfmovietim' : ('Output', 'real', """
					If non-zero, the movie file b2movies.nc is generated, containing several 2d quantities. Gives the real-time interval between writes of movie frames in b2movies.nc. If non-zero, must be at least as large as the simulation timestep.
				""", '0.0'),
   
      'cdfmovie_fields' : ('Output', 'integer', """
					Controls the quantities outputted to b2movies.nc. If cdfmovie_fields.ge.1 then only the main state variables (na, ne, Te, Ti, etc.) are written with each write to b2movies.nc. If cdfmovie_fields.ge.2 then additional quantities (e.g. fluxes, particle and energy sources) are also included.
				""", '1'),
   
      'b2mndr_ntim_save' : ('Output', 'integer', """
					Another option for plasma state file output. If greater than 0, gives the number of B2.5 full interations between successive write-ups of plasmastate files, in addition to the ones written at regular CPU intervals (see b2mndr_savecpu and b2mndr_plasmatim). Should be used, at the exclusion of other plasmastate write-up frequency settings, in conjunction with the Leuven Monte Carlo averaging scheme.
				""", '0'),
   
      'b2mndt_av' : ('Output', 'integer', """
					If b2mndt_av.gt.0, turns on computation of running averages.
				""", '0'),
   
      'b2mndt_av_continue' : ('Output', 'integer', """
					If b2mndt_av_continue.gt.0, continuously perform running averages.
				""", '1'),
   
      'b2mndt_av_ntim_batch' : ('Output', 'integer', """
					If ntim_batch.gt.0, number of iterations used to compute batch averages, written out in 'b2batch.nc'.
				""", '500'),
   
      'b2mndt_av_ntim_run' : ('Output', 'integer', """
					If ntim_run.gt.0, number of iterations used for writing running averages.
				""", '1000'),
   
      'b2mndt_av_batch_all' : ('Output', 'integer', """
					If b2mndt_av_batch_all.gt.0, produces standard output for batch averages.
				""", '0'),
   
      'b2mndr_plasmatim' : ('Output', 'real', """
					Another option for plasma state file output. If greater than 0, gives the real-time interval between successive write-ups of plasmastate files, in addition to the ones written at regular CPU intervals (see b2mndr_savecpu and b2mndr_ntim_save). Must then be at least as large as the simulation timestep.
				""", '0.0'),
   
      'b2mndr_ids_save' : ('Output', 'integer', """
					Frequency, in timesteps, at which an IDS is saved containing the plasma state. Can be used in conjunction with b2mndr_ids_time and b2mndr_ids_av.
					If used, an IDS time slice will be written at the end of run.
					If negative, a single IDS will be written at the end of the run.
					Will not work if running a "0 timesteps" simulation, in which case the use of b2_ual_write is recommended.
				""", '0'),
   
      'b2mndr_ids_time' : ('Output', 'real', """
					Frequency, in simulation seconds, at which an IDS is saved containing the plasma state. Can be used in conjunction with b2mndr_ids_save and b2mndr_ids_av.
					If non-zero, must be at least as large as the simulation timestep.
					If used, an IDS time slice will be written at the end of run.
					Will not work if running a "0 timesteps" simulation, in which case the use of b2_ual_write is recommended.
				""", '0.0'),
   
      'b2mndr_ids_av' : ('Output', 'integer', """
					Frequency, in number of batch averages, at which an IDS is saved containing the averaged plasma state. Can be used in conjunction with b2mndr_ids_save and b2mndr_ids_time.
					The averaged plasma state is saved as a separate occurrence of the edge_profiles and edge_sources IDSs.
				""", '0'),
   
      'b2wdat_iout' : ('Output', 'integer', """
					If iout.eq.1, a large set of *.dat output files will be produced containing the values of a variety of code quantities, evaluated at the end of the B2.5 iteration.
					If iout.eq.4, an even larger set of output files will be produced, for the purposes of a full run analysis, evaluated in the individual routines where the quantities are used.
					For even more detailed debugging analysis, one should instead use "procedure_name"_iout.eq.1.
					The files and their content are fully described in the Output_description.pdf file in the $SOLPSTOP/doc directory and Appendix G of the SOLPS-ITER manual.
				""", '0'),
   
      'get_residuals' : ('Output', 'integer', """
					If get_residuals.eq.1, then the residuals of unsolved equations will be outputted into b2ftrace. Equations are unsolved if 'b2news_no_solve' is nonzero or any elements of the solveco, solvemo, solveee, solveei, or solvepo are set to .false. .
					By default, get_residuals.eq.0 and the residuals for unsolved equations are set to zero.
					The residual of the total momentum equation is nonzero when all momentum equations for parallel velocities are solved together.
					The residual of the total energy equation is nonzero when Te and Ti equations are solved together.
				""", '0'),
   
      'b2wdat_append' : ('Output', 'integer', """
					If append.ne.0, the output files produced by the b2wdat_iout.eq.4 switch are appended upon every write, instead of being rewritten every time.
				""", '0'),
   
      'my_out_digits' : ('Output', 'integer', """
					Specifies the number of significant digits with which the *.dat files are written out. Defaults to 6 in normal mode and 15 in debug mode.
					Must be positive.
				""", '6 or 15'),
   
      'b2mndr_old_style' : ('Output', 'integer', """
					If old_style.gt.0, old-fashioned (SOLPS4 style) output is added at the end of the b2mn.prt file.
				""", '0'),
   
      'b2mndr_av_read' : ('Output', 'integer', """
					If b2mndr_av_read.gt.0, the initial plasma is the averaged solution read from the b2faveri file. Check $SOLPSTOP/doc/SOLPS-ITER_Eirene_averaging.pdf for details.
				""", '0'),
   
      'b2mndr_trantim' : ('Output', 'real', """
					Produces a numbered 'tran' file every trantim real-time seconds. An endstate file is written if it falls between scheduled write-up times. Only available within the -DJET environment. If non-zero, must be at least as large as the simulation timestep.
				""", '0.0'),
   
      'b2mwti_target_offset' : ('Output', 'integer', """
					The diagnostic values from b2time.nc use guard cell values if target_offset.eq.0, and values from the neighbouring real cell if target_offset.eq.1. Fluxes are not affected.
				""", '1'),
   
      'b2mwti_2dwrite' : ('Output', 'integer', """
					Controls additional output to b2time.nc.  If 2dwrite.ge.1 then a few 2d arrays (ne, Te, Ti) are written with each write to b2time.nc. If 2dwrite.ge.2 then fluxes, electric potential, kinetic energy, and fluid particle and energy source terms are also included (e.g., rsana, rsahi, rqrad).
				""", '0'),
   
      'b2mwti_ismain0' : ('Output', 'integer', """
					Index of the species used to create the 'dp3d?.last10' diagnostic files.
					Defaults to the neutral species associated with ismain. If no such species is declared, the default will be set to ismain. Is expected to either correspond to a neutral species or to ismain.
					Can also be used in b2ar.dat to specify the index of the main neutral CX species when resorting to the AMNS database (starting from version 1.3.2).
					If ismain is also defaulted, then will be 0.
				""", '0'),
   
      'b2mwqt_style' : ('Output', 'integer', """
					Specifies the amount of data that is written out to b2ftrace. See the manual (Section on b2yq) for full details.
				""", '1'),
   
      'ank_tracing' : ('Output', 'integer', """
					If ank_tracing.ge.1, additional tracing output from Andrei Kukushkin is produced, in files to be found in the tracing/ directory inside the run directory. The traces will be written every ank_tracing iteration. If b2mndr_stim.lt.0, data from the current run is appended to the existing files, otherwise the files are overwritten.
				""", '0'),
   
      'b2stbc_diagno' : ('Output', 'integer', """
					Controls level of output in b2stbc and subservient routines.
					Level 1 (diagno.ge.1) output includes wrong_flow warnings, transport coefficients at the (nx/2,ny) basis mesh position, the solution found for the given heat flux at constant temperature bc, and all feedback diagnostics.
					Level 2 output (diagno.ge.2) includes the integral current correction, the boundary sources on the first call, excessive sound speeds, and the iterative progress to the given heat flux at constant temperature bc.
					Level 3 output (diagno.ge.3) includes the boundary sources on each call, and the boundary.prt file listing all boundary cells.
				""", '0'),
   
      'b2stbr_output' : ('Output', 'integer', """
					Output flag for the first_flight model. If output.ge.1, the files start, end, and fort.88 are created, which contain information about the chords used in the model.
				""", '0'),
   
      'b2npmo_vlct_diagno' : ('Output', 'integer', """
					Output flag to control diagnostics related to use of ion_vlct_restrict switch.
					If vlct_diagno.eq.0, the velocity restrictions are applied silently.
					If vlct_diagno.eq.1 (default), the user only gets a count of how many times the velocity restriction has been applied for each species, if any.
					If vlct_diagno.eq.2, the user gets the full details of where and how large the applied velocity restriction was, if any.
				""", '1'),
   
      'b2mndr_inverse_ua' : ('Output', 'integer', """
					If inverse_ua.eq.1, the code will produce a 'b2fstati_with-ua' file that contains the same plasma information, but with the opposite sign convention for the parallel velocity. The run will then proceed with the new velocities with their sign inverted.
				""", '0'),
   
      'b2yrdr_ns' : ('Output', 'integer', """
					New number of species desired when reading a new atomic rates file using b2yr.exe. Must be specified within b2yr.dat.
					To be used for checking atomic rates after bundling and before any plasma state files have been created or converted, i.e. when the number of species in the atomic rates file b2frates does not match the number of species declared in the run parameters file b2fpardf.
				""", 'ns'),
   
      'b2srsm_diagno' : ('Output', 'integer', """
					Controls level of output in b2srsm. If diagno.ge.2, output will be given on every call. If diagno.eq.1, output will be given on main calls only.
				""", '0'),
   
      'b2ux5p_cpu' : ('Output', 'integer', """
					If cpu.gt.0, prints out the time spent in the matrix solver.
				""", '0'),
   
      'eirene_mc_output_style' : ('Output', 'integer', """
					If nonzero, prints sources computed by Eirene. If greater than 1, prints them on every use of the recycling sources, not just when they are computed.
				""", '1'),
   
      'ma28_nwrite' : ('Output', 'integer', """
					If nwrite.gt.0, prints the content of the sparse matrix in the b2_matrix file, for the first nwrite calls.
				""", '0'),
   
      'b2news_ncallout' : ('Output', 'integer', """
					If the iteration number is equal to ncallout, then several output files 'b2ne_npmo', 'b2ne_xppb', 'b2ne_npco', 'b2ne+nppo' which detail the convergence behaviour and residuals.
				""", '-1'),
   
      'b2tqna_diagno' : ('Output', 'integer', """
					If diagno.gt.0, outputs details of the calculations of neutral transport coefficients when using the new_df0 model. See switch b2tqna_new_df0 for more details.
				""", '0'),
   
      'eirene_format' : ('Output', 'string', """
					This switch is to be provided within b2yt.dat to indicate to the b2yt converter the format of the original Eirene input.dat file to be modified. The accepted values are (case-insensitive):
					'old' for input files from SOLPS4.0 and SOLPS5.0 runs using 'old' Eirene_96
					'new' for input files from SOLPS4.0 and SOLPS5.0 runs using 'new' Eirene_99
					'facelift' for input files from SOLPS5.1 runs
					'juelich' for input files from Juelich Eirene versions (2008 and younger)
					'iter' for input files from SOLPS4.2/4.3 and SOLPS-ITER runs
				""", 'iter'),
   
      'solps_version' : ('Output', 'string', """
					This switch is to be provided within b2yt.dat to indicate to the b2yt converter the format of the original fort.44 file to be modified. The accepted values are (case-insensitive):
					'4.3' for a fort.44 file produced from SOLPS4.3 runs
					'5.0' for a fort.44 file produced from SOLPS5.0 runs
					'5.1' for a fort.44 file produced from SOLPS5.1 runs
					'5.2' for a fort.44 file produced from SOLPS5.2 runs
					'iter' for input files from SOLPS-ITER runs (no conversion necessary)
				""", 'iter'),
   
      'ids_from_43' : ('Output', 'integer', """
					This switch is to be used when running the b2_ual_write utility program to obtain an IDS from the SOLPS run results.
					If set to 1, the IDS will indicate that the results come from a converted SOLPS4.3 run with no additional calculation. By default, the IDS will indicate a SOLPS-ITER run.
				""", '0'),
   
      'AFN_out' : ('Output', 'integer', """
					If AFN_out.ne.0, boundary flux components of the advanced fluid neutral models are written out. See code for details.
				""", '0'),
   
      'b2news_potit' : ('', 'integer', """
					Obsolete. Removed from code.
				""", '50'),
   
      'b2news_potitmin' : ('', 'integer', """
					Obsolete. Removed from code.
				""", '0'),
   
      'b2mndr_min_areshe' : ('', 'real', """
					Minimum residuals for stopping a run. All criteria must be met simultaneously for the run to stop. The continuity equation residual applies to the "ismain" species (See "Run" section).
				""", '0.0'),
   
      'b2mndr_min_areshi' : ('', 'real', """
					Minimum residuals for stopping a run. All criteria must be met simultaneously for the run to stop. The continuity equation residual applies to the "ismain" species (See "Run" section).
				""", '0.0'),
   
      'b2mndr_min_aresco' : ('', 'real', """
					Minimum residuals for stopping a run. All criteria must be met simultaneously for the run to stop. The continuity equation residual applies to the "ismain" species (See "Run" section).
				""", '0.0'),
   
      'b2mndt_nstg_areshe' : ('', 'real', """
					Minimum residuals for an internal solution loop to stop.
					Used in conjunction with (not in replacement of) the nstg(0:2) numbers.
					All nonzero criteria must be met simultaneously. The continuity equation residual applies to the 'ismain' species (See 'Run' section).
				""", '0.0'),
   
      'b2mndt_nstg_areshi' : ('', 'real', """
					Minimum residuals for an internal solution loop to stop.
					Used in conjunction with (not in replacement of) the nstg(0:2) numbers.
					All nonzero criteria must be met simultaneously. The continuity equation residual applies to the 'ismain' species (See 'Run' section).
				""", '0.0'),
   
      'b2mndt_nstg_aresco' : ('', 'real', """
					Minimum residuals for an internal solution loop to stop.
					Used in conjunction with (not in replacement of) the nstg(0:2) numbers.
					All nonzero criteria must be met simultaneously. The continuity equation residual applies to the 'ismain' species (See 'Run' section).
				""", '0.0'),
   
      'b2news_nsmin' : ('', 'integer', """
					Allows for solving only for the species range [nsmin:nsmax-1].
				""", '0'),
   
      'b2news_nsmax' : ('', 'integer', """
					Allows for solving only for the species range [nsmin:nsmax-1].
				""", 'ns'),
   
      'eirene_na_max' : ('', 'real', """
					Upper and lower bounds used when writing out data for Eirene.
				""", '1e30'),
   
      'eirene_na_min' : ('', 'real', """
					Upper and lower bounds used when writing out data for Eirene.
				""", '0.0'),
   
      'eirene_ne_max' : ('', 'real', """
					Upper and lower bounds used when writing out data for Eirene.
				""", '1e30'),
   
      'eirene_ne_min' : ('', 'real', """
					Upper and lower bounds used when writing out data for Eirene.
				""", '0.0'),
   
      'eirene_te_max' : ('', 'real', """
					Upper and lower bounds used when writing out data for Eirene.
				""", '1e30'),
   
      'eirene_te_min' : ('', 'real', """
					Upper and lower bounds used when writing out data for Eirene.
				""", '0.0'),
   
      'eirene_ti_max' : ('', 'real', """
					Upper and lower bounds used when writing out data for Eirene.
				""", '1e30'),
   
      'eirene_ti_min' : ('', 'real', """
					Upper and lower bounds used when writing out data for Eirene.
				""", '0.0'),
   
      'eirene_ua_max' : ('', 'real', """
					Upper and lower bounds used when writing out data for Eirene.
				""", '+c'),
   
      'eirene_ua_min' : ('', 'real', """
					Upper and lower bounds used when writing out data for Eirene.
				""", '-c'),
   
      'eirene_M_max' : ('', 'real', """
					Upper and lower bounds used when writing out data for Eirene.
				""", '1e30'),
   
      'b2tfhe_no_hybr' : ('', 'integer', """
					Switches to toggle between the standard 5.0 hybrid scheme (no_hybr.eq.0) and the old 4.0 upwind scheme (no_hybr.eq.1).
					These apply separately to the electron heat, ion heat and particle conservation equations.
					If hybr2.ne.0, then a mixed scheme is used where only the conductivity is computed according to the 4.0 scheme.
					Obsolete. Not available for WG. Replaced by the 'discr_meth' switches.
				""", '0'),
   
      'b2tfhi_no_hybr' : ('', 'integer', """
					Switches to toggle between the standard 5.0 hybrid scheme (no_hybr.eq.0) and the old 4.0 upwind scheme (no_hybr.eq.1).
					These apply separately to the electron heat, ion heat and particle conservation equations.
					If hybr2.ne.0, then a mixed scheme is used where only the conductivity is computed according to the 4.0 scheme.
					Obsolete. Not available for WG. Replaced by the 'discr_meth' switches.
				""", '0'),
   
      'b2tfnb_no_hybr' : ('', 'integer', """
					Switches to toggle between the standard 5.0 hybrid scheme (no_hybr.eq.0) and the old 4.0 upwind scheme (no_hybr.eq.1).
					These apply separately to the electron heat, ion heat and particle conservation equations.
					If hybr2.ne.0, then a mixed scheme is used where only the conductivity is computed according to the 4.0 scheme.
					Obsolete. Not available for WG. Replaced by the 'discr_meth' switches.
				""", '0'),
   
      'b2tfhe_hybr2' : ('', 'integer', """
					Switches to toggle between the standard 5.0 hybrid scheme (no_hybr.eq.0) and the old 4.0 upwind scheme (no_hybr.eq.1).
					These apply separately to the electron heat, ion heat and particle conservation equations.
					If hybr2.ne.0, then a mixed scheme is used where only the conductivity is computed according to the 4.0 scheme.
					Obsolete. Not available for WG. Replaced by the 'discr_meth' switches.
				""", '0'),
   
      'b2tfhi_hybr2' : ('', 'integer', """
					Switches to toggle between the standard 5.0 hybrid scheme (no_hybr.eq.0) and the old 4.0 upwind scheme (no_hybr.eq.1).
					These apply separately to the electron heat, ion heat and particle conservation equations.
					If hybr2.ne.0, then a mixed scheme is used where only the conductivity is computed according to the 4.0 scheme.
					Obsolete. Not available for WG. Replaced by the 'discr_meth' switches.
				""", '0'),
   
      'b2tfhe_upwind' : ('', 'integer', """
					If upwind.ne.0, then the SOLPS4 upwind scheme in b2tfhe_ and b2tfhi_ to obtain the heat fluxes.
					Obsolete. Not available for WG. Replaced by the 'discr_meth' switches.
				""", '0'),
   
      'b2tfhi_upwind' : ('', 'integer', """
					If upwind.ne.0, then the SOLPS4 upwind scheme in b2tfhe_ and b2tfhi_ to obtain the heat fluxes.
					Obsolete. Not available for WG. Replaced by the 'discr_meth' switches.
				""", '0'),
   
      'b2uxus_mult_solvdim' : ('', 'integer', """
					Multipliers to the number of nonzero elements in the solution matrix for workspace arrays in the matrix solver.
				""", '15'),
   
      'b2uxus_mult_solvdim1' : ('', 'integer', """
					Multipliers to the number of nonzero elements in the solution matrix for workspace arrays in the matrix solver.
				""", '10'),
   
      'b2stbc_she0ep' : ('', 'real', """
					Small level sources introduced in all cells.
				""", '1.0e-36'),
   
      'b2stbc_shi0ep' : ('', 'real', """
					Small level sources introduced in all cells.
				""", '1.0e-36'),
   
      'b2stbc_sna0ep' : ('', 'real', """
					Small level sources introduced in all cells.
				""", '1.0e-36'),
   
      'b2news_facdrift_tanh_a' : ('', 'real', """
					Parameters for spatial variation of the diamagnetic, ExB and viscosity drift term multipliers. These are allowed to have tanh profiles centered at tanh_a and of width tanh_b, where both quantities are in metres and measured along the outer midplane. The maximum value of facdrift and fac_ExB is controlled by their respective _start and _target switches, see Run section for details. NOTE: none of them have been converted to WG!
					For consistency with the naming convention of related variables:
					b2news_facExB_tanh_a is an alias for b2news_fac_ExB_tanh_a,
					b2news_facExB_tanh_b is an alias for b2news_fac_ExB_tanh_b,
					b2news_facvis_tanh_a is an alias for b2news_fac_vis_tanh_a, and b2news_facvis_tanh_b is an alias for b2news_fac_vis_tanh_b. Additionally, for all deep core cell rings up to and including the iy_nocoreExB-th, fac_ExB(ix,iy) is set to zero. This means that ExB contributions and flows will be zeroed out in those cells.
					For consistency with the boundary condition treatment, the value iy_nocoreExB.eq.1 is NOT recommended!
				""", '0.0'),
   
      'b2news_facdrift_tanh_b' : ('', 'real', """
					Parameters for spatial variation of the diamagnetic, ExB and viscosity drift term multipliers. These are allowed to have tanh profiles centered at tanh_a and of width tanh_b, where both quantities are in metres and measured along the outer midplane. The maximum value of facdrift and fac_ExB is controlled by their respective _start and _target switches, see Run section for details. NOTE: none of them have been converted to WG!
					For consistency with the naming convention of related variables:
					b2news_facExB_tanh_a is an alias for b2news_fac_ExB_tanh_a,
					b2news_facExB_tanh_b is an alias for b2news_fac_ExB_tanh_b,
					b2news_facvis_tanh_a is an alias for b2news_fac_vis_tanh_a, and b2news_facvis_tanh_b is an alias for b2news_fac_vis_tanh_b. Additionally, for all deep core cell rings up to and including the iy_nocoreExB-th, fac_ExB(ix,iy) is set to zero. This means that ExB contributions and flows will be zeroed out in those cells.
					For consistency with the boundary condition treatment, the value iy_nocoreExB.eq.1 is NOT recommended!
				""", '0.0'),
   
      'b2news_fac_ExB_tanh_a' : ('', 'real', """
					Parameters for spatial variation of the diamagnetic, ExB and viscosity drift term multipliers. These are allowed to have tanh profiles centered at tanh_a and of width tanh_b, where both quantities are in metres and measured along the outer midplane. The maximum value of facdrift and fac_ExB is controlled by their respective _start and _target switches, see Run section for details. NOTE: none of them have been converted to WG!
					For consistency with the naming convention of related variables:
					b2news_facExB_tanh_a is an alias for b2news_fac_ExB_tanh_a,
					b2news_facExB_tanh_b is an alias for b2news_fac_ExB_tanh_b,
					b2news_facvis_tanh_a is an alias for b2news_fac_vis_tanh_a, and b2news_facvis_tanh_b is an alias for b2news_fac_vis_tanh_b. Additionally, for all deep core cell rings up to and including the iy_nocoreExB-th, fac_ExB(ix,iy) is set to zero. This means that ExB contributions and flows will be zeroed out in those cells.
					For consistency with the boundary condition treatment, the value iy_nocoreExB.eq.1 is NOT recommended!
				""", '0.0'),
   
      'b2news_fac_ExB_tanh_b' : ('', 'real', """
					Parameters for spatial variation of the diamagnetic, ExB and viscosity drift term multipliers. These are allowed to have tanh profiles centered at tanh_a and of width tanh_b, where both quantities are in metres and measured along the outer midplane. The maximum value of facdrift and fac_ExB is controlled by their respective _start and _target switches, see Run section for details. NOTE: none of them have been converted to WG!
					For consistency with the naming convention of related variables:
					b2news_facExB_tanh_a is an alias for b2news_fac_ExB_tanh_a,
					b2news_facExB_tanh_b is an alias for b2news_fac_ExB_tanh_b,
					b2news_facvis_tanh_a is an alias for b2news_fac_vis_tanh_a, and b2news_facvis_tanh_b is an alias for b2news_fac_vis_tanh_b. Additionally, for all deep core cell rings up to and including the iy_nocoreExB-th, fac_ExB(ix,iy) is set to zero. This means that ExB contributions and flows will be zeroed out in those cells.
					For consistency with the boundary condition treatment, the value iy_nocoreExB.eq.1 is NOT recommended!
				""", '0.0'),
   
      'b2news_fac_vis_tanh_a' : ('', 'real', """
					Parameters for spatial variation of the diamagnetic, ExB and viscosity drift term multipliers. These are allowed to have tanh profiles centered at tanh_a and of width tanh_b, where both quantities are in metres and measured along the outer midplane. The maximum value of facdrift and fac_ExB is controlled by their respective _start and _target switches, see Run section for details. NOTE: none of them have been converted to WG!
					For consistency with the naming convention of related variables:
					b2news_facExB_tanh_a is an alias for b2news_fac_ExB_tanh_a,
					b2news_facExB_tanh_b is an alias for b2news_fac_ExB_tanh_b,
					b2news_facvis_tanh_a is an alias for b2news_fac_vis_tanh_a, and b2news_facvis_tanh_b is an alias for b2news_fac_vis_tanh_b. Additionally, for all deep core cell rings up to and including the iy_nocoreExB-th, fac_ExB(ix,iy) is set to zero. This means that ExB contributions and flows will be zeroed out in those cells.
					For consistency with the boundary condition treatment, the value iy_nocoreExB.eq.1 is NOT recommended!
				""", '0.0'),
   
      'b2news_fac_vis_tanh_b' : ('', 'real', """
					Parameters for spatial variation of the diamagnetic, ExB and viscosity drift term multipliers. These are allowed to have tanh profiles centered at tanh_a and of width tanh_b, where both quantities are in metres and measured along the outer midplane. The maximum value of facdrift and fac_ExB is controlled by their respective _start and _target switches, see Run section for details. NOTE: none of them have been converted to WG!
					For consistency with the naming convention of related variables:
					b2news_facExB_tanh_a is an alias for b2news_fac_ExB_tanh_a,
					b2news_facExB_tanh_b is an alias for b2news_fac_ExB_tanh_b,
					b2news_facvis_tanh_a is an alias for b2news_fac_vis_tanh_a, and b2news_facvis_tanh_b is an alias for b2news_fac_vis_tanh_b. Additionally, for all deep core cell rings up to and including the iy_nocoreExB-th, fac_ExB(ix,iy) is set to zero. This means that ExB contributions and flows will be zeroed out in those cells.
					For consistency with the boundary condition treatment, the value iy_nocoreExB.eq.1 is NOT recommended!
				""", '0.0'),
   
      'b2news_iy_nocoreExB' : ('', 'integer', """
					Parameters for spatial variation of the diamagnetic, ExB and viscosity drift term multipliers. These are allowed to have tanh profiles centered at tanh_a and of width tanh_b, where both quantities are in metres and measured along the outer midplane. The maximum value of facdrift and fac_ExB is controlled by their respective _start and _target switches, see Run section for details. NOTE: none of them have been converted to WG!
					For consistency with the naming convention of related variables:
					b2news_facExB_tanh_a is an alias for b2news_fac_ExB_tanh_a,
					b2news_facExB_tanh_b is an alias for b2news_fac_ExB_tanh_b,
					b2news_facvis_tanh_a is an alias for b2news_fac_vis_tanh_a, and b2news_facvis_tanh_b is an alias for b2news_fac_vis_tanh_b. Additionally, for all deep core cell rings up to and including the iy_nocoreExB-th, fac_ExB(ix,iy) is set to zero. This means that ExB contributions and flows will be zeroed out in those cells.
					For consistency with the boundary condition treatment, the value iy_nocoreExB.eq.1 is NOT recommended!
				""", '0'),
   
      'b2stbc_cbsnafac' : ('', 'real', """
					Feedback relaxation parameters. See Physics section for individual feedback quantities.
				""", '0.01'),
   
      'b2stbc_fchycore_alpha' : ('', 'real', """
					Feedback relaxation parameters. See Physics section for individual feedback quantities.
				""", '0.1'),
   
      'b2stbc_fheycore_alpha' : ('', 'real', """
					Feedback relaxation parameters. See Physics section for individual feedback quantities.
				""", '0.1'),
   
      'b2stbc_fhiycore_alpha' : ('', 'real', """
					Feedback relaxation parameters. See Physics section for individual feedback quantities.
				""", '0.1'),
   
      'b2stbc_fnaycore_alpha' : ('', 'real', """
					Feedback relaxation parameters. See Physics section for individual feedback quantities.
				""", '0.1'),
   
      'b2stbc_nesepm_alpha' : ('', 'real', """
					Feedback relaxation parameters. See Physics section for individual feedback quantities.
				""", '1.0e-3'),
   
      'b2stbc_nesepm_beta' : ('', 'real', """
					Feedback relaxation parameters. See Physics section for individual feedback quantities.
				""", '0.0'),
   
      'b2stbc_nesepm_gamma' : ('', 'real', """
					Feedback relaxation parameters. See Physics section for individual feedback quantities.
				""", '0.99'),
   
      'b2stbc_volrec_alpha' : ('', 'real', """
					Feedback relaxation parameters. See Physics section for individual feedback quantities.
				""", '1.0e-3'),
   
      'b2stbc_volrec_beta' : ('', 'real', """
					Feedback relaxation parameters. See Physics section for individual feedback quantities.
				""", '1.0'),
   
      'b2stbr_sput_chem_alpha' : ('', 'real', """
					Feedback relaxation parameters. See Physics section for individual feedback quantities.
				""", '1.0e-2'),
   
      'b2stbr_sput_phys_alpha' : ('', 'real', """
					Feedback relaxation parameters. See Physics section for individual feedback quantities.
				""", '1.0e-2'),
   
      'b2stbc_type13_fac' : ('', 'real', """
					Additional feedback strength adjustment parameters for BCCON=13 boundary condition, density adjusted to match a specific flux.
					The density is adjusted by a factor of:
					(1.0_R8+CONPAR(IS,IB,2)*(DFS-FS)/ (abs(DFS)+abs(FS)+abs(type13_norm)+abs(NAS*type13_fac)))
					where FS is the current particle flux, DFS is the desired particle flux, and NAS the current volume-averaged density. The desired flux DFS is computed as
					CONPAR(IS,IB,1)+CONPAR(IS,IB,3)
					where the first number is provided directly by the user in b2.boundary.parameters and the second is internally set to correspond to the re-entry of ionised neutrals that have crossed into the core for cases run with Eirene where eirene_ionising_core is activated.
					See also the description of 'eirene_ionising_core'.
					Not yet available for WG.
				""", '1.0'),
   
      'b2stbc_type13_norm' : ('', 'real', """
					Additional feedback strength adjustment parameters for BCCON=13 boundary condition, density adjusted to match a specific flux.
					The density is adjusted by a factor of:
					(1.0_R8+CONPAR(IS,IB,2)*(DFS-FS)/ (abs(DFS)+abs(FS)+abs(type13_norm)+abs(NAS*type13_fac)))
					where FS is the current particle flux, DFS is the desired particle flux, and NAS the current volume-averaged density. The desired flux DFS is computed as
					CONPAR(IS,IB,1)+CONPAR(IS,IB,3)
					where the first number is provided directly by the user in b2.boundary.parameters and the second is internally set to correspond to the re-entry of ionised neutrals that have crossed into the core for cases run with Eirene where eirene_ionising_core is activated.
					See also the description of 'eirene_ionising_core'.
					Not yet available for WG.
				""", '1.0e15'),
   
      'heatdiff1D_linlog' : ('', 'integer', """
					Parameters related to solving the temperature equation for the target plate elements in depth. If linlog.eq.1, a linear subdividing of the plate element is used. If linlog.eq.2, a logarithmic subdividing is used, with the surface layer being ratio times thinner than the last layer in the bulk.
					ratio must be larger than 1.
				""", '1'),
   
      'heatdiff1D_ratio' : ('', 'real', """
					Parameters related to solving the temperature equation for the target plate elements in depth. If linlog.eq.1, a linear subdividing of the plate element is used. If linlog.eq.2, a logarithmic subdividing is used, with the surface layer being ratio times thinner than the last layer in the bulk.
					ratio must be larger than 1.
				""", '100.0'),
   
      'b2mndr_isfb' : ('', 'real', """
					Experimental: allows for density feedback of the number of electrons accompanying species 'isfb' at location (ixfb,iyfb).
					Note that ixfb and iyfb are real numbers!
				""", 'ismain'),
   
      'b2mndr_ixfb' : ('', 'real', """
					Experimental: allows for density feedback of the number of electrons accompanying species 'isfb' at location (ixfb,iyfb).
					Note that ixfb and iyfb are real numbers!
				""", '5*nx/8'),
   
      'b2mndr_iyfb' : ('', 'real', """
					Experimental: allows for density feedback of the number of electrons accompanying species 'isfb' at location (ixfb,iyfb).
					Note that ixfb and iyfb are real numbers!
				""", 'ny/2'),
   
      'b2mndr_ne_wanted' : ('', 'real', """
					Experimental: allows for density feedback of the number of electrons accompanying species 'isfb' at location (ixfb,iyfb).
					Note that ixfb and iyfb are real numbers!
				""", '0.0'),
   
      'b2mndr_ne_wanted_time' : ('', 'real', """
					Experimental: allows for density feedback of the number of electrons accompanying species 'isfb' at location (ixfb,iyfb).
					Note that ixfb and iyfb are real numbers!
				""", '0.0'),
   
      'b2news_xfm0' : ('', 'real', """
					Under-relaxation parameters for the parallel momentum, continuity, potential and energy equations respectively.
					Setting these switches to zero prevents updating of the associated code quantities.
				""", '1.0'),
   
      'b2news_xfm1' : ('', 'real', """
					Under-relaxation parameters for the parallel momentum, continuity, potential and energy equations respectively.
					Setting these switches to zero prevents updating of the associated code quantities.
				""", '1.0'),
   
      'b2news_xfm2' : ('', 'real', """
					Under-relaxation parameters for the parallel momentum, continuity, potential and energy equations respectively.
					Setting these switches to zero prevents updating of the associated code quantities.
				""", '1.0'),
   
      'b2news_xfm3' : ('', 'real', """
					Under-relaxation parameters for the parallel momentum, continuity, potential and energy equations respectively.
					Setting these switches to zero prevents updating of the associated code quantities.
				""", '1.0'),
   
      'b2npco_pcm0' : ('', 'real', """
					Specifiy multipliers to Rhie-Chow corrections from particle equations
					Not used (and default set to zero) if running in time-dependent mode (b2mndt_style.eq.2).
					b2npco_pcm0 is a multiplier for the update on the parallel velocity following the pressure-correction equation.
					b2npco_pcm1 is a multiplier for the Rhie-Chow terms in the particle fluxes.
				""", '1.0'),
   
      'b2npco_pcm1' : ('', 'real', """
					Specifiy multipliers to Rhie-Chow corrections from particle equations
					Not used (and default set to zero) if running in time-dependent mode (b2mndt_style.eq.2).
					b2npco_pcm0 is a multiplier for the update on the parallel velocity following the pressure-correction equation.
					b2npco_pcm1 is a multiplier for the Rhie-Chow terms in the particle fluxes.
				""", '1.0'),
   
      'b2npht_pcm0' : ('', 'real', """
					Specifies multipliers to Rhie-Chow corrections from heat equations.
					Not used (and default set to zero) if running in time-dependent mode (b2mndt_style.eq.2).
					b2npht_pcm0 is a multiplier for the update on the parallel velocity following the update of Ti and Te.
					b2npht_pcm1 is a multiplier for the Rhie-Chow terms in the flow fields of ion, electron, and neutral heat.
				""", '1.0'),
   
      'b2npht_pcm1' : ('', 'real', """
					Specifies multipliers to Rhie-Chow corrections from heat equations.
					Not used (and default set to zero) if running in time-dependent mode (b2mndt_style.eq.2).
					b2npht_pcm0 is a multiplier for the update on the parallel velocity following the update of Ti and Te.
					b2npht_pcm1 is a multiplier for the Rhie-Chow terms in the flow fields of ion, electron, and neutral heat.
				""", '1.0'),
   
      'b2sihs_rf0' : ('', 'real', """
					rf0-4 are numerical parameters, see the code. All must be non-negative and of order unity; larger values are meant to provide more stabilisation. Some or all may be set to zero and removed eventually. I have had some experience to indicate that rf0, rf2, rf4 may have a useful function; however, later changes in the code may have made all these parameters superfluous.
				""", '1.0'),
   
      'b2sihs_rf1' : ('', 'real', """
					rf0-4 are numerical parameters, see the code. All must be non-negative and of order unity; larger values are meant to provide more stabilisation. Some or all may be set to zero and removed eventually. I have had some experience to indicate that rf0, rf2, rf4 may have a useful function; however, later changes in the code may have made all these parameters superfluous.
				""", '1.0'),
   
      'b2sihs_rf2' : ('', 'real', """
					rf0-4 are numerical parameters, see the code. All must be non-negative and of order unity; larger values are meant to provide more stabilisation. Some or all may be set to zero and removed eventually. I have had some experience to indicate that rf0, rf2, rf4 may have a useful function; however, later changes in the code may have made all these parameters superfluous.
				""", '1.0'),
   
      'b2sihs_rf3' : ('', 'real', """
					rf0-4 are numerical parameters, see the code. All must be non-negative and of order unity; larger values are meant to provide more stabilisation. Some or all may be set to zero and removed eventually. I have had some experience to indicate that rf0, rf2, rf4 may have a useful function; however, later changes in the code may have made all these parameters superfluous.
				""", '1.0'),
   
      'b2sihs_rf4' : ('', 'real', """
					rf0-4 are numerical parameters, see the code. All must be non-negative and of order unity; larger values are meant to provide more stabilisation. Some or all may be set to zero and removed eventually. I have had some experience to indicate that rf0, rf2, rf4 may have a useful function; however, later changes in the code may have made all these parameters superfluous.
				""", '1.0'),
   
      'b2srdt_phm0' : ('', 'real', """
					Multipliers to the density, parallel momentum, heat, potential, and electron particle time-derivative source terms, respectively.
					'phm4' is normally zero since the potential equation contains no source terms.
				""", '1.0'),
   
      'b2srdt_phm1' : ('', 'real', """
					Multipliers to the density, parallel momentum, heat, potential, and electron particle time-derivative source terms, respectively.
					'phm4' is normally zero since the potential equation contains no source terms.
				""", '1.0'),
   
      'b2srdt_phm3' : ('', 'real', """
					Multipliers to the density, parallel momentum, heat, potential, and electron particle time-derivative source terms, respectively.
					'phm4' is normally zero since the potential equation contains no source terms.
				""", '1.0'),
   
      'b2srdt_phm4' : ('', 'real', """
					Multipliers to the density, parallel momentum, heat, potential, and electron particle time-derivative source terms, respectively.
					'phm4' is normally zero since the potential equation contains no source terms.
				""", '0.0'),
   
      'b2srdt_phm5' : ('', 'real', """
					Multipliers to the density, parallel momentum, heat, potential, and electron particle time-derivative source terms, respectively.
					'phm4' is normally zero since the potential equation contains no source terms.
				""", '1.0'),
   
      'b2srst_rf0' : ('', 'real', """
					(rf0/1/2/3 for numerical stabilisation)
				""", '1.0'),
   
      'b2srst_rf1' : ('', 'real', """
					(rf0/1/2/3 for numerical stabilisation)
				""", '1.0'),
   
      'b2srst_rf2' : ('', 'real', """
					(rf0/1/2/3 for numerical stabilisation)
				""", '1.0'),
   
      'b2srst_rf3' : ('', 'real', """
					(rf0/1/2/3 for numerical stabilisation)
				""", '1.0'),
   
      'b2stel_rg0' : ('', 'real', """
					Damping coefficient applied to the atomic physics sources.
				""", '1.0'),
   
      'b2stel_rg1' : ('', 'real', """
					Damping coefficient applied to the atomic physics sources.
				""", '1.0'),
   
      'b2stel_rxm0' : ('', 'real', """
					Damping coefficient applied to the atomic physics sources.
				""", '0.0'),
   
      'b2stel_rxm1' : ('', 'real', """
					Damping coefficient applied to the atomic physics sources.
				""", '0.0'),
   
      'b2stel_rxm2' : ('', 'real', """
					Damping coefficient applied to the atomic physics sources.
				""", '0.0'),
   
      'b2stel_rxm3' : ('', 'real', """
					Damping coefficient applied to the atomic physics sources.
				""", '0.0'),
   
      'b2stel_rxm4' : ('', 'real', """
					Damping coefficient applied to the atomic physics sources.
				""", '0.0'),
   
      'b2npmo_discr_meth' : ('', 'integer', """
					Determines the discretization method for the calculation of the fluxes.
					discr_meth.eq.0: central scheme
					discr_meth.eq.1: upwind scheme
					discr_meth.eq.2: SOLPS5 hybrid scheme
					discr_meth.eq.3: SOLPS4 continuity scheme. Not yet available for WG.
				""", '2'),
   
      'b2tfhe_discr_meth' : ('', 'integer', """
					Determines the discretization method for the calculation of the fluxes.
					discr_meth.eq.0: central scheme
					discr_meth.eq.1: upwind scheme
					discr_meth.eq.2: SOLPS5 hybrid scheme
					discr_meth.eq.3: SOLPS4 continuity scheme. Not yet available for WG.
				""", '2'),
   
      'b2tfhi_discr_meth' : ('', 'integer', """
					Determines the discretization method for the calculation of the fluxes.
					discr_meth.eq.0: central scheme
					discr_meth.eq.1: upwind scheme
					discr_meth.eq.2: SOLPS5 hybrid scheme
					discr_meth.eq.3: SOLPS4 continuity scheme. Not yet available for WG.
				""", '2'),
   
      'b2tfnb_discr_meth' : ('', 'integer', """
					Determines the discretization method for the calculation of the fluxes.
					discr_meth.eq.0: central scheme
					discr_meth.eq.1: upwind scheme
					discr_meth.eq.2: SOLPS5 hybrid scheme
					discr_meth.eq.3: SOLPS4 continuity scheme. Not yet available for WG.
				""", '2'),
   
      'b2news_potok' : ('Numerics', 'real', """
					Obsolete. Removed from code.
				""", '1.0e-2'),
   
      'b2news_ramp_slow' : ('Numerics', 'integer', """
					If ramp_slow.eq.0 (default), the ExB and diamagnetic drifts multipliers are ramped on each call of b2news, otherwise they are only changed on the first call of the nstg loop on the timestep.
				""", '0'),
   
      'b2mndr_use_9pt_stencil' : ('Numerics', 'integer', """
					Master switch to turn on the 9-point stencil numerical treatment. If set to 0, reverts to the old 5-point stencil.
					Only usable with the SOLPS5.2 physics model.
					The perpendicular viscosity current terms are not yet available within this treatment.
				""", '1'),
   
      'b2mndr_res_quit' : ('Numerics', 'real', """
					Threshold of the maximum residual among the equations solved below which the run is stopped. Only meaningful when compiled with FIXED_POINT and with adjoint AD code.
				""", '1.0e-7'),
   
      'eirene_print_minmax' : ('Numerics', 'integer', """
					Print min and max values of te, ti, na &amp; ua
				""", '0'),
   
      'eirene_extrap' : ('Numerics', 'integer', """
					If eirene_extrap.eq.1, then guard cell plasma parameter values are calculated from the neighbouring real cell values. If eirene_extrap.eq.0, the guard cell values are used unchanged.
				""", '1'),
   
      'eirene_ank_mods' : ('Numerics', 'integer', """
					If ank_mods.ne.0, then uses an additional scheme to ensure particle balance as the B2.5 solution evolves, due to the internal iteration scheme, away from the plasma background on which the Eirene sources were originally computed at the beginning of the time step. The user is referred to the text in $SOLPSTOP/doc/Source_Scaling_in_B2.pdf for a full description of the method used.
					Cannot be used in conjunction with 'eirene_ionising_core'.
				""", '0'),
   
      'eirene_dpc_fix' : ('Numerics', 'integer', """
					If dpc_fix.eq.1, then uses the true particle source from the stratum. If dpc_fix.eq.2, sets this particle source to zero. The equivalent of the old behaviour is dpc_fix.eq.0 and is wrong!
				""", '1'),
   
      'b2stbr_eir_src_nhist' : ('Numerics', 'integer', """
					If b2stbr_eir_src_nhist.gt.1, then Eirene sources are accumulated and a moving average is computed. Note that only one of b2stbr_eir_src_nhist, eirene_neutr_avg, or eirene_underrelax may be nonzero.
				""", '1'),
   
      'eirene_neutr_avg' : ('Numerics', 'integer', """
					If eirene_neutr_avg.gt.0, then Eirene sources are accumulated and averaged until eirene_neutr_avg+1 steps, at which point the averaging process is reset. Note that only one of b2stbr_eir_src_nhist, eirene_neutr_avg, or eirene_underrelax may be nonzero.
				""", '0'),
   
      'eirene_underrelax' : ('Numerics', 'integer', """
					If eirene_underrelax.gt.0, then an underrelaxation scheme is used for the Eirene sources, with an underrelaxation ratio of 1/eirene_underrelax. Note that only one of b2stbr_eir_src_nhist, eirene_neutr_avg, or eirene_underrelax may be nonzero.
				""", '0'),
   
      'eirene_uub_style' : ('Numerics', 'integer', """
					If eirene_uub_style.eq.0, compute poloidal velocities passed to Eirene from ua, vadia, wadia, vaecrb arrays. If eirene_uub_style.eq.1, compute poloidal velocities passed to Eirene from fna and fna_eir fluxes.
				""", '0'),
   
      'b2news_area_fix' : ('Numerics', 'integer', """
					Obsolete. Removed from code.
					New implementation supersedes treatment of area_fix=3.
				""", '3'),
   
      'b2npmo_ion_vlct_restrict' : ('Numerics', 'integer', """
					If ion_vlct_restrict.ne.0, the parallel speed of ions and fluid neutrals is limited to be no more than M times the global plasma sound speed. In addition, if ion_vlct_restrict.eq.2, the ExB ion speeds are limited to be no more than M the local ion sound speed.
					M is given by b2npmo_ion_vlct_restrict_M.
				""", '0'),
   
      'b2npmo_ion_vlct_restrict_M' : ('Numerics', 'real', """
					Determines M for ion_vlct_restrict.ne.0.
				""", '3.0'),
   
      'b2mndr_ua_max' : ('Numerics', 'real', """
					Puts a hard limit on the absolute value of the parallel velocity, but applies only to fluid neutrals and in case the spatially hybrid fluid-kinetic model is active (spatial_hybrid.ne.0).
					This switch was introduced when b2npmo_ion_vlct_restrict only applied to ions. Now that b2npmo_ion_vlct_restrict also applies to fluid neutrals, the removal of b2mndr_ua_max can be considered.
					For now it is kept for backward compatibility with published results.
				""", '1.0e6'),
   
      'b2nppo_restr_po' : ('Numerics', 'real', """
					If b2nppo_restr_po.ne.0.0, the electric potential is restricted such that its ratio (in absolute value) with the electron temperature (in eV) does not exceed b2nppo_restr_po.
					If b2nppo_restr_po is negative, the limit only applies to regions of negative electric potential.
					Only applies on open field lines.
				""", '0.0'),
   
      'b2upht_rte_min' : ('Numerics', 'real', """
					If b2upht_rte_min.gt.0.0, the electron to ion temperature ratio is forced to not be lower than rte_min (i.e. Te/Ti &gt;= rte_min).
				""", '0.0'),
   
      'b2sihs_shivis' : ('Numerics', 'integer', """
					If b2sihs_shivis.eq.1, then shivc and shiva (ion heat source due to viscosity) will be zeroed out in boundary-volume cells.
					If b2sihs_shivis.eq.2, then shivc and shiva (ion heat source due to viscosity) will be zeroed out in boundary-volume cells except the ones that belong to the core and target boundaries.
					If b2sihs_shivis.eq.3, then shivc and shiva (ion heat source due to viscosity) will be zeroed out in boundary-volume cells belonging to the main chamber wall bondary.
				""", '0'),
   
      'b2sihs_shi' : ('Numerics', 'integer', """
					If b2sihs_shi.ne.0, then all b2sihs_shi* and b2sihs_shivis keys will be assigned to b2sihs_shi value as default (individual keys can still be overwritten by b2sihs_shi* and b2sihs_shivis that take proprity over b2sihs_shi).
				""", '0'),
   
      'b2sihs_shidu' : ('Numerics', 'integer', """
					If b2sihs_shidu.eq.1, then shidu (ion heat source due to divergence of velocity) will be zeroed out in boundary-volume cells.
					If b2sihs_shidu.eq.2, then shidu (ion heat source due to divergence of velocity) will be zeroed out in boundary-volume cells except the ones that belong to the core and target boundaries.
					If b2sihs_shidu.eq.3, then shidu (ion heat source due to divergence of velocity) will be zeroed out in boundary-volume cells belonging to the main chamber wall bondary.
				""", '0'),
   
      'b2sihs_shidd' : ('Numerics', 'integer', """
					If b2sihs_shidd.eq.1, then shidd (ion heat source due to divergence of drift velocity) will be zeroed out in boundary-volume cells.
					If b2sihs_shidd.eq.2, then shidd (ion heat source due to divergence of drift velocity) will be zeroed out in boundary-volume cells except the  ones that belong to the core and target boundaries.
					If b2sihs_shidd.eq.3, then shidd (ion heat source due to divergence of drift velocity) will be zeroed out in boundary-volume cells belonging to the main chamber wall bondary.
				""", '0'),
   
      'b2sihs_shedu' : ('Numerics', 'integer', """
					If b2sihs_shedu.eq.0, then shedu (electron heat source due to divergence of velocity) will be zeroed out in boundary-volume cells.
					If b2sihs_shedu.eq.2, then shedu (electron heat source due to divergence of velocity) will be zeroed out in boundary-volume cells except the ones that belong to the core and target boundaries.
					If b2sihs_shedu.eq.3, then shedu (electron heat source due to divergence of velocity) will be zeroed out in boundary-volume cells belonging to the main chamber wall bondary.
				""", '0'),
   
      'b2sihs_shedd' : ('Numerics', 'integer', """
					If b2sihs_shedd.eq.0, then shedd (electron heat source due to divergence of drift velocity) will be zeroed out in boundary-volume cells.
					If b2sihs_shedd.eq.2, then shedd (electron heat source due to divergence of drift velocity) will be zeroed out in boundary-volume cells except the ones that belong to the core and target boundaries.
					If b2sihs_shedd.eq.3, then shedd (electron heat source due to divergence of drift velocity) will be zeroed out in boundary-volume cells belonging to the main chamber wall bondary.
				""", '0'),
   
      'b2tfhe_vis_per' : ('Numerics', 'real', """
					vis_per is a multiplier to the perpendicular viscosity current.
					If vis_per.ne.0.0, the electric potential equation is solved by the subroutine b2npp7 using a 7-point stencil.
					The value '1.0' is recommended for runs with drifts when perpendicular viscosity and corresponding perpendicular viscosity current is taken into account.
					Cannot be used in conjunction with the 9-point stencil numerical treatment. If used with the 5-point stencil treatment and with fluid neutrals, must be equal to b2tfnb_vis_per for numerical stability reasons.
				""", '0.0'),
   
      'b2stbc_sheath_drift_fix' : ('Numerics', 'integer', """
					If sheath_drift_fix.eq.0, then the drift velocity used in the sheath boundary conditions is the sum of diamagnetic and ExB contributions (old, but likely wrong, treatment). If sheath_drift_fix.eq.1, then the drift velocity used in the sheath boundary conditions is the ExB velocity only (recommended).
				""", '1'),
   
      'b2stbc_BC2_cor9' : ('Numerics', 'real', """
					This switch concerns a 9-point correction for the Neumann type boundary conditions (BCCON/BCMOM/BCENE/BCENI/BCPOT/BCENK/BCENZ = 2) for non-orthogonal cells.
					If b2stbc_BC2_cor9.eq.0.0, gradients tangential to the boundary are ignored. The actual normal gradient then deviates from the one requested by the user.
					If b2stbc_BC2_cor9.eq.1.0, an additional term based on the vertex values of the boundary face is added to correct for the tangential gradient, to get the correct (up to interpolation error) normal gradient.
				""", '0.0'),
   
      'b2stbc_fix_fch_in_fhe_sheath' : ('Numerics', 'integer', """
					If fix_fch_in_fhe_sheath.eq.0, then the wrong (old) implementation of the FCH contribution to FHE used;
					If fix_fch_in_fhe_sheath.eq.1, then the wrong (second) implementation of the FCH contribution to FHE used;
					If fix_fch_in_fhe_sheath.eq.2, then the correct implementation of the FCH contribution to FHE used;
				""", '2'),
   
      'b2stbr_potential_at_guard_cell' : ('Numerics', 'integer', """
					If potential_at_guard_cell.eq.1, the electric potential used for the computation of the incident energy for sputtering yields is taken as the value in the guard cell. If potential_at_guard_cell.eq.0, the value from the neighbouring real cell is used instead.
				""", '1'),
   
      'b2stbr_temperature_at_guard_cell' : ('Numerics', 'integer', """
					If temperature_at_guard_cell.eq.1, the temperatures used for recycling and reflection are taken as the value in the guard cell.
					If temperature_at_guard_cell.eq.0, the temperatures are interpolated between the guard cell and the neighbouring real cell.
				""", '1'),
   
      'b2trcl_conductive_limit' : ('Numerics', 'integer', """
					When set to '1', flux limit of the parallel electron and ion heat fluxes is applied to transport coefficients.
					It is recommended '1'. If 'b2trcl_conductive_limit' '0' then the keys 'b2tfhe_lim_flux' and 'b2tfhi_lim_flux' must be '0'.
				""", '1'),
   
      'b2trcl_core_cond_limit' : ('Numerics', 'integer', """
					If core_cond_limit.eq.0, then the heat flux limits due to chvemx and chvimx are not applied in the core. Switch only active if 'b2trcl_conductive_limit' .ne. 0.
				""", '0'),
   
      'b2tlh0_flux_limit_style' : ('Numerics', 'integer', """
					If '0', use the SOLPS5.0 scheme for neutral heat conductivity flux limits.
					If '1', SPb form to calculate parallel and perpendicular neutral heat conductivity flux limit (does not preserve symmetry, kept for backward compatibility reasons).
					If '2', modifies the SPb treatment for the flux limits to be applied on the transport coefficients directly.
					It is recommended '2'.
				""", '2'),
   
      'b2tral_mode' : ('Numerics', 'integer', """
					Switch to choose between various interpolation schemes for transport coefficients (Does not apply to pinch velocities vla or to the temperature-driven electric conductivity alf).
					mode.eq.-1: harmonic averaging
					mode.eq.0 : geometric averaging
					mode.eq.1 : arithmetic averaging (SOLPS5.0 formulation)
					mode.eq.2 : arithmetic averaging (SOLPS4.0 formulation)
				""", '1'),
   
      'b2tfnb_pflux_cor' : ('Numerics', 'integer', """
					If pflux_cor.eq.1 and fna_mdf is used, enforces that the integral particle flux across the domain boundaries computed from fna is equal to the same integral computed from the fna_mdf fluxes.
					Not yet available for WG.
				""", '1'),
   
      'b2trcl_cvsa_mltpl' : ('Numerics', 'real', """
					Artificial coefficient providing faster convergence to the neoclassical electric field but giving a distortion of the flows in the SOL as a side-effect.
					Can be applied &lt;&gt;1 during the convergence and turned off for the final stage of calculations. Use with caution.
				""", '1.0'),
   
      'b2uxus_mult_nonzero' : ('Numerics', 'integer', """
					Number of expected nonzero matrix elements per matrix row.
				""", '1'),
   
      'b2ux5p_style' : ('Numerics', 'integer', """
					Choose the type of 5-point stencil matrix solver. Style.eq.0 = iluter, Style.eq.1 = slv5pt, Style.eq.2 = MA28.
					NOTE: Only style.eq.2 will give good results. Other values are NOT recommended! style.eq.0 and style.eq.1 are only applicable to linear geometries with no cuts and no isolated regions.
				""", '2'),
   
      'b2ux7p_style' : ('Numerics', 'integer', """
				Choose the type of 7-point stencil matrix solver. Style.eq.0 = iluter, Style.eq.1 = slv5pt, Style.eq.2 = MA28copy3. Style.eq.3 = SDRV from YSMP.
				NOTE: Only style.eq.2 will give good results. Applying style.eq.3 should be corrected and is no longer recommended. It might give slow convergence or even divergence of the potential equation. Other values are NOT recommended! style.eq.0 .or. style.eq.1 will return an error.
				""", '2'),
   
      'b2ux9p_style' : ('Numerics', 'integer', """
					Choose the type of 9-point stencil matrix solver. Style.eq.0 = iluter, Style.eq.1 = slv5pt, Style.eq.2 = MA28copy.
					NOTE: Only style.eq.2 will give good results. Other values are NOT recommended! style.eq.0 and style.eq.1 will return an error.
				""", '2'),
   
      'b2ux5p_acpar' : ('Numerics', 'real', """
					Paremeter needed for iluter matrix solver.
				""", '8.0'),
   
      'b2stbc_fchy_dia' : ('Numerics', 'real', """
					Multiplier to the neoclassical current and diamagnetic heat flux convective boundary conditions, also multiplied by facdrift.
					Adds a poloidal variation consistent with neoclassics and diamagnetic contributions to the heat flux boundary conditions.
					Should only be used with the 5.0 model and heat flux boundaries.
					Allows use b2stbc_integral_current if fchy_dia.eq.0, forbids it otherwise.
					Not yet available for WG.
				""", '0.0'),
   
      'b2stbc_fchy_dia_coreonly' : ('Numerics', 'integer', """
					If fchy_dia_coreonly.eq.1, the neoclassical current and diamagnetic heat flux convective boundary conditions are only applied on the core boundary.
					If fchy_dia_coreonly.eq.0, those are applied to all boundaries, including PFR, North SOL edge and diverted island center boundary.
					Not yet available for WG.
				""", '1'),
   
      'b2stbc_neoclassical' : ('Numerics', 'real', """
					Real parameter which establishes boundary conditions for radial component of the current for North and South boundaries when these lie on closed flux surfaces.
					If b2stbc_neoclassical is 0 then the radial component of the current is zero.
					If b2stbc_neoclassical is not 0 the radial component of the current is given by the neoclassical value. b2stbc_neoclassical is superseded if facdrift.ne.0.
					This cannot be used in conjunction with b2stbc_integral_current below.
				""", '0.0'),
   
      'b2stbc_cbc' : ('Numerics', 'real', """
					Multiplier to the ExB velocity for sheath boundary conditions BCMOM=13.
					Not yet available for WG.
				""", '1.0'),
   
      'b2stbc_integral_current' : ('Numerics', 'real', """
					If integral_current.gt.0, corrects current sources so that there be no surface current at the North and South edges of the edge plasma.
					The value of integral_current multiplies the correction term added to the current source.
					This setting is incompatible with the normal use of diamagnetic drift terms (facdrift.gt.0.0 .and. b2stbc_fchy_dia.ne.0.0) or neoclassical boundary conditions (b2stbc_neoclassical.gt.0.0).
					Not yet available for WG.
				""", '0.0'),
   
      'b2stbr_first_flight_dl' : ('Numerics', 'real', """
					Step length (in metres) for computing the first flight model chords.
				""", '0.001'),
   
      'b2stbr_first_flight_no_of_flights' : ('Numerics', 'integer', """
					Number of chords started from each start point in the first flight model.
				""", '9'),
   
      'b2stbr_first_flight_table_size' : ('Numerics', 'integer', """
					Workspace size given to the first flight table.
				""", '200000'),
   
      'b2stbc_bcpot_16_step' : ('Numerics', 'integer', """
					Frequency (in number of calls to b2stbc_phys) at which the constant value of the potential at the boundaries where BCPOT=16 is applied will be recomputed.
					Not yet available for WG.
				""", '50'),
   
      'b2stbc_stab_coeff_sheath_te' : ('Numerics', 'real', """
					Stabilizing term to the source associated with boundary condition BCENE=15, when bcene_15_style.eq.1 (default).
					To help suppress electron temperature oscillations, this parameter can be set to a positive value. The range 1-100 is recommended.
				""", '0.0'),
   
      'b2stbc_stab_coeff_sheath_ti' : ('Numerics', 'real', """
					Stabilizing term to the source associated with boundary condition BCENI=15.
					To help suppress ion temperature oscillations, this parameter can be set to a positive value. The range 1-100 is recommended.
				""", '0.0'),
   
      'b2npht_stab_shei' : ('Numerics', 'real', """
					Stabilizing term to the heat sources associated with ion-electron energy exchange.
				""", '0.0'),
   
      'b2txcx_increase_transp_coefs' : ('Numerics', 'real', """
					Multiplication factor to the poloidal transport coefficients (electron and ion thermal conductivity, particle transport proportional to grad na and grad pa). Must be greater than 1.0 to have an effect.
					If b2txcx_increase_transp_coefs.gt.1.0, b2trno_set_chcb_0 will be assigned to 1.
				""", '0.0'),
   
      'b2trno_set_chcb_0' : ('Numerics', 'integer', """
					If set_chcb_0.eq.1, sets radial components of transport coefficients (electron and ion thermal conductivity, particle transport proportional to grad na and grad pa) equals to zero on not field-aligned boundary faces (as defined by b2us_prep_Qalfmin). Also decreases the same radial components by a b2txcx_increase_transp_coefs factor on not field-aligned faces between two neighbouring boundary cells. Always on if b2txcx_increase_transp_coefs.gt.1.0.
				""", '0'),
   
      'b2mndr_na_min' : ('Numerics', 'real', """
					Minimal density maintained in all cells for all species (in m^{-3}).
					It must be true that na_min is smaller than na_new, as well as any of the initial densities provided in b2ai.dat.
					This switch replaces 'b2mndr_na0eps' from SOLPS5.x.
					It is also used to avoid division by 0 when calculating kinetic neutral velocities from the kinetic flux densities in b2tinnt.F.
				""", '1.0e4'),
   
      'b2mndr_na_new' : ('Numerics', 'real', """
					Initial density (in m^{-3}) put in all cells for all new species if not overwritten by initial state file. This switch replaces 'b2mndr_na0eps' from SOLPS5.x.
				""", '1.0e14'),
   
      'b2upht_te_min' : ('Numerics', 'real', """
					Sets the minimum electron temperature value (in eV).
				""", '0.1'),
   
      'b2upht_te_max' : ('Numerics', 'real', """
					Sets the maximum electron temperature value (in eV).
				""", '1.0e+30'),
   
      'b2upht_ti_min' : ('Numerics', 'real', """
					Sets the minimum ion temperature value (in eV).
				""", '0.1'),
   
      'b2upht_ti_max' : ('Numerics', 'real', """
					Sets the maximum ion temperature value (in eV).
				""", '1.0e+30'),
   
      'b2upht_tn_min' : ('Numerics', 'real', """
					Sets the minimum fluid neutral temperature value (in eV).
				""", '0.1'),
   
      'b2upht_tn_max' : ('Numerics', 'real', """
					Sets the maximum fluid neutral temperature value (in eV).
				""", '1.0e+30'),
   
      'b2upht_kt_min' : ('Numerics', 'real', """
					Sets the minimum turbulent ExB kinetic energy value (in eV).
				""", '1.0e-5'),
   
      'b2upht_kt_max' : ('Numerics', 'real', """
					Sets the maximum turbulent ExB kinetic energy value (in eV).
				""", '1.0e+30'),
   
      'b2upht_zt_min' : ('Numerics', 'real', """
					Sets the minimum turbulent ExB enstrophy value (in s^{-2}).
				""", '1.0e-8'),
   
      'b2upht_zt_max' : ('Numerics', 'real', """
					Sets the maximum turbulent ExB enstrophy value (in s^{-2}).
				""", '1.0e+30'),
   
      'b2news_guard_flows' : ('Numerics', 'integer', """
					Prohibited switch. As of v3.2.0, there are no faces between guard cells anymore.
				""", '2'),
   
      'b2stbc_istyle_cur_contr_on_S_and_N' : ('Numerics', 'integer', """
					When set to '2', SPb form of adding currents on the South core boundary is included by using BCPOT=12, and on the South PFR and North boundaries by using BCPOT=13. It is recommended '2', in conjunction with the BCPOT=12 and BCPOT=13 settings, respectively.
					When set to '1', SPb form of adding currents on South and North boundaries is done explicitly in addition to other existing boundary conditions for the potential equation.
					The old 5.0 calculation is recovered by using the value '0'.
				""", '2'),
   
      'b2stbc_istyle_fchi' : ('Numerics', 'integer', """
					If '1', explicitly use the expression (bx*cs*na) of particle flux (fna) from boundary condition instead of fna, for boundary condition type BCPOT=11.
					Not yet available for WG.
				""", '0'),
   
      'b2news_no_b2sral_call' : ('Numerics', 'integer', """
					If no_b2sral_call.eq.0, add an additional call to recompute the sources in b2news_ to reproduce the behaviour from SOLPS4.
				""", '1'),
   
      'b2news_do_2nd_b2npco_call' : ('Numerics', 'integer', """
					If do_2nd_b2npco_call.eq.1, perform a second call to the density equation solve to improve particle balance, as done in SOLPS4.
				""", '0'),
   
      'b2news_re_eval_prtls_fluxes' : ('Numerics', 'integer', """
					If re_eval_prtls_fluxes.eq.1, the particle fluxes are recomputed at the end of b2news_. This is necessary for rescaling of the Eirene sources during coupled runs, so this switch is superceded by use_eirene, and also needed to reproduce SOLPS4 runs.
				""", '0'),
   
      'b2mndt_style' : ('Numerics', 'integer', """
					If 0, refers to the obsolete SOLPS5.0 physics model, no longer supported.
					If 1, the SOLPS5.2 physics model is used, and b2news_ is called to compute the new plasma state. (default)
					If 2, the SOLPS5.2 physics model is used, and b2news_m is called instead to run the code in fully self-consistent time-dependent mode. B2news_m uses a different order of solving equations: first the density equations, then the parallel velocity, electrical potential and Te and Ti equations (and optionally also the Tn and k-epsilon equations, if requested).
				""", '1'),
   
      'b2mndt_ckn' : ('Numerics', 'integer', """
					If b2mndt_ckn=2, the 2nd order Crank-Nicolson time-stepping scheme is used, instead of the default 1st order implicit Euler scheme.
					This scheme can be used both in time-dependent mode (b2mndt_style=2) and in steady-state mode (b2mndt_style=1).
				""", '1'),
   
      'b2mndt_dummy' : ('Numerics', 'integer', """
					This switch is used internally in the code to initially run a dummy call to b2mndt, which is needed to use the Crank-Nicolson time-stepping scheme (b2mndt_ckn=2). This switch is not meant to be changed by users, it should always stay at its default value of 0.
				""", '0'),
   
      'b2mndt_ntim_step_out' : ('Numerics', 'integer', """
					When set to a value of 'K', residuals at each K-th step will be written in b2ftrace. It helps to avoid a huge b2ftrace files during long time run.
				""", '1'),
   
      'b2mndt_calc_err_step_out' : ('Numerics', 'integer', """
					When set to a value of 'K', the subroutine calc_err will be run at each K-th step. It allows to output the error at desired times during a time-dependent MMS test.
				""", '1'),
   
      'b2trno_flux_limit_to_dpa' : ('Numerics', 'integer', """
					If '1', flux limit to neutrals contribution to dpa0 - the diffusion coefficient is applied in b2tlc0.F. It is recommended '1'.
					b2tlc0.F has the flux limit parameters α and γ which are given by 'b2tlc0_alpha' and 'b2tlc0_gamma'. 'b2tfnb_alpha' and 'b2tlc0_alpha' cannot be different from zero simultaneously.
					'b2tfnb_alpha' gives another form of flux limit which is applied to the whole particle flux.
				""", '1'),
   
      'b2trno_flux_limit_to_vsa' : ('Numerics', 'integer', """
					If '1', flux limit to neutrals contribution to vsa0 - the viscosity is applied in b2tlv0.F. It is recommended '1'.
					b2tlv0.F has the flux limit parameters α and γ which are given by 'b2tlv0_alpha' and 'b2tlv0_gamma'.
				""", '1'),
   
      'b2mndt_use_b2srst' : ('Numerics', 'integer', """
					Switches off the stabilization of the source coefficients.
				""", '1'),
   
      'b2mndt_rxf' : ('Numerics', 'real', """
					Main under-relaxation parameter. The default value is 0.5 in steady-state mode (b2mndt_style.eq.1).
					Setting this switch to zero prevents updating of the principal code quantities.
					In time-dependent mode (b2mndt_style.eq.2), the default value is 1.0. It can be set lower than 1, provided that the following relationship is satisfied: DTxx=1/(1-(1-rxf)^nstgJ).
					DTxx are the time-step multipliers (xx=CO,MO,EE,EI,...) and nstgJ the inner iterations (J=0,1,2). For example, if rxf=0.5 and nstgJ=1, then it must be DTxx=2.
					Tip: If nstgJ is high enough, DTxx tends to 1 for any rxf, and no time-step multipliers need to be changed.
				""", 'See description'),
   
      'b2npco_rxg' : ('Numerics', 'real', """
					rxg specifies a special under-relaxation parameter. A term of the form "abs(residual)/rxg" is added to the diagonal of the matrix of the correction equation, with the effect of limiting the computed correction. rxg is dimensionless and of order unity; smaller values of rxg imply stronger damping.
					Not used if running in time-dependent mode (b2mndt_style.eq.2).
				""", '1.0'),
   
      'b2npht_rxg' : ('Numerics', 'real', """
					rxg specifies a special under-relaxation parameter. A term of the form "abs(residual)/rxg" is added to the diagonal of the matrix of the correction equation, with the effect of limiting the computed correction. rxg is dimensionless and of order unity; smaller values of rxg imply stronger damping.
					Not used if running in time-dependent mode (b2mndt_style.eq.2).
				""", '1.0'),
   
      'b2npht_style' : ('Numerics', 'integer', """
					When set to '1', SPb form of the program b2sihs_ is called. b2npht_style.eq.0 no longer available for WG.
				""", '1'),
   
      'b2npmo_rxg' : ('Numerics', 'real', """
					Normalisation factor for the parallel momentum equation.
					Not used when running in time_dependent mode (b2mndt_style.eq.2).
				""", '1.0e6'),
   
      'b2news_poteq' : ('Numerics', 'integer', """
					If poteq.eq.0, the potential equation is jumped over and not solved.
					If poteq.eq.2, the potential is set to 3.1*Te/qe as per SOLPS4.0.
					If poteq.eq.1, the potential equation is solved according to the no_solve switch settings.
					If poteq.ne.1, then 'b2tfhe_no_current' must be set to '1'.
				""", '1'),
   
      'b2nxdv_style' : ('Numerics', 'integer', """
					When set to '1', the total friction force cancel is not calculated at the guard boundary cells.
					It is recommended '1'.
				""", '1'),
   
      'b2nxfc_style' : ('Numerics', 'integer', """
					style specifies the precise form of interpolation used in the computation of flcb and cvcb. When set to '1', SPb form of the transport terms in the momentum correction equation is used.
					It is recommended '1'.
				""", '1'),
   
      'b2nxfx_style' : ('Numerics', 'integer', """
					When set to '1', SPb form of an expression that occurs in the electron-atom thermal force is used. Only used if b2sigp_style.ne.2.
					It is recommended '1'.
				""", '1'),
   
      'b2sifr_styl0' : ('Numerics', 'integer', """
					Specify the type of linearisation used in the thermal force term.
				""", '0'),
   
      'b2tfhe_mode_ehx' : ('Numerics', 'integer', """
					Switch to choose between various discretization schemes when computing the poloidal electric field.
					See code for details.
				""", '0'),
   
      'b2tfhe_mode_ehy' : ('Numerics', 'integer', """
					Switch to choose between various discretization schemes when computing the radial electric field.
					See code for details.
				""", '0'),
   
      'b2sigp_style' : ('Numerics', 'integer', """
					When set to '1', SPb form of the pressure gradient term on the right hand of the momentum balance equation is used.
					When set to '2', the parallel current term contains a correction due to impurities, when Z_eff is not equal to the average plasma ion charge. Only usable if the potential equation is solved simultaneously (b2news_poteq.eq.1).
					The default value of '2' is recommended for cases with one main hydrogenic species (or at least where the main species is the lightest one) and any amount of impurities. It is not guaranteed to yield correct results for hydrogen isotopic mixtures or non-hydrogenic plasmas.
				""", '2'),
   
      'b2sigp_pressure_restriction' : ('Numerics', 'integer', """
					When set to '1', a CFL-like restriction is applied to the pressure gradient term for minority ions and for neutrals species.
				""", '1'),
   
      'b2xzdd_zero_dead_and_core' : ('Numerics', 'integer', """
					If 1 then zero passed sources in dead regions,
					If 2 zero passed sources in dead regions and core boundary cells
					If 0 then SKIP
				""", '1'),
   
      'b2stcx_rg0' : ('Numerics', 'real', """
					(rg0 for numerical stabilisation; needs experiments.)
				""", '1.0'),
   
      'b2stcx_styl0' : ('Numerics', 'integer', """
					Specifies the type of linearisation used in the charge exchange momentum source term.
				""", '0'),
   
      'eirene_mc_linearisation' : ('Numerics', 'integer', """
					Specifies the type of linearisation used in the sources derived from the Monte Carlo neutrals. If linearisation.eq.0, all sources are fed to the constant term, if linearisation.eq.1, positive terms go in the constant term, and negative terms in the proportional term. 'eirene_mc_linearization' is an alias for this switch.
				""", '1'),
   
      'b2stbm_linearisation' : ('Numerics', 'real', """
					Same as above, but applied to the sources coming for an externally coupled code providing plasma sources, for instance a kinetic treatment of trace impurity ions. 'b2stbm_linearization' is an alias for this switch.
				""", '1.0'),
   
      'b2stbm_impgyro_mod' : ('Numerics', 'integer', """
					Specifies the frequency (in units of full B2.5 timesteps) at which an externally coupled code providing additional source (for instance a kinetic treatment of trace impurity ions such as IMPGYRO) should be called.
				""", '0'),
   
      'b2stel_styl0' : ('Numerics', 'integer', """
					Specifies the type of linearisation used in the charge exchange momentum source term.
				""", '0'),
   
      'b2tfcc_xfac' : ('Numerics', 'real', """
					Multiplier to the pressure force term.
				""", '1.0'),
   
      'b2tfhe_mdf' : ('Numerics', 'integer', """
					If '1', SPb new form of calculating electron heat flux is used. It is recommended '1' for runs with drifts.
				""", '0'),
   
      'b2tfhe_no_current' : ('Numerics', 'integer', """
					If no_current.eq.1, all currents are set to zero. The setting no_current.eq.1 must be used if the potential equation is not explicitly solved for, i.e. for b2news_poteq.ne.1.
				""", '0'),
   
      'b2tfhe_prl_cur' : ('Numerics', 'real', """
					Multiplier to the parallel current.
				""", '1.0'),
   
      'b2tfhi_mdf' : ('Numerics', 'integer', """
					If '1', SPb new form of calculating ion heat flux is used.
					It is recommended '1' for runs with drifts.
				""", '0'),
   
      'b2tfnb_drift_style' : ('Numerics', 'integer', """
					When set to '0', drift velocities are calculated in cell centers (NO LONGER SUPPORTED IN WG CODE).
					When set to '1', drift velocities are calculated in cell faces.
					It is recommended '1'.
				""", '1'),
   
      'b2tfnb_poleldr' : ('Numerics', 'real', """
					Multiplier to the poloidal electrical drift velocity.
				""", '1.0'),
   
      'b2tfnb_radeldr' : ('Numerics', 'real', """
					Multiplier to the radial electrical drift velocity.
				""", '1.0'),
   
      'b2tfnb_poldidr' : ('Numerics', 'real', """
					Multiplier to the poloidal diamagnetic drift velocity.
				""", '1.0'),
   
      'b2tfnb_raddidr' : ('Numerics', 'real', """
					Multiplier to the radial diamagnetic drift velocity.
				""", '1.0'),
   
      'b2tfnb_mdf' : ('Numerics', 'integer', """
					If '1', SPb new form of calculating particle flux is used.
					It is recommended '1' for runs with drifts.
				""", '0'),
   
      'b2upht_stylec' : ('Numerics', 'integer', """
					(stylec is a numerical switch, needs experiments)
				""", '0'),
   
      'b2usmo_cfc0' : ('Numerics', 'real', """
					Linearisation constant.
				""", '1.0'),
   
      'b2srsm_enable' : ('Numerics', 'integer', """
					If enable.ne.0, then the sources for particle, parallel momentum, electron and ion heat are rescaled, for non-boundary cells, if the local timestep exceeds the physics timescale implied by those sources.
					enable.ne.0 not yet available for WG.
				""", '0'),
   
      'b2tinnt_style' : ('Numerics', 'integer', """
					Integer switch to choose the numerical treatment of the ion pressure gradient calculation for the ion-neutral current.
					If b2tinnt_style.eq.0, then the chain rule is first applied to the product of density and temperature, and (grad n)/n is rewritten as grad(log(n)).
					If b2tinnt_style.eq.1 (default), then the gradient of the product of density and temperature is calculated directly.
				""", '1'),
   
      'b2stbr_phys_lin_shi0' : ('Numerics', 'integer', """
					Determines the linearisation of the boundary condition heat source due to neutral recycling/reflection when erecyc in used. Not used for advanced fluid neutral (AFN) model.
					lin_shi0.eq.0: put source in shi0(iCv,0).
					lin_shi0.eq.1: put source/ti in shi0(iCv,1).
				""", '0'),
   
      'b2tfnb_style_int_vel' : ('Numerics', 'integer', """
					Determines the interpolation weights to get the parallel velocities at the cell faces.
					style_int_vel.eq.0: interpolation based on cell volumes.
					style_int_vel.eq.1: interpolation based on cell connector lengths.
					Only the combination b2tfnb_style_int_vel=0 and b2sihs_style_int_vel=0 works robustly for now. Other combinations gave rise to oscillations. More research needed.
				""", '0'),
   
      'b2sihs_style_int_vel' : ('Numerics', 'integer', """
					Determines the interpolation weights to get the parallel velocities at the cell faces for the calculation of divergence ua.
					style_int_vel.eq.0: interpolation based on cell connector lengths.
					style_int_vel.eq.1: interpolation based on cell volumes.
					Only the combination b2tfnb_style_int_vel=0 and b2sihs_style_int_vel=0 works robustly for now. Other combinations gave rise to oscillations. More research needed.
				""", '0'),
   
      'b2ardr_fix_recomb' : ('', 'integer', """
					When fix_recomb is changed from 0, and if the ADAS option is in use, then uses the PRB file to add the contribution arising from is--&gt;is-1 processes.
					If the AMJUEL/HYDHEL rates are in use and fix_recomb.eq.0, then the recombination energy is substracted to the electron recombination energy costs. May lead to negative rates!
					This term includes the bremsstrahlung.
					For ADAS, the '0' option only contains the bremsstrahlung for the is--&gt;is-1 process.
					The correction is only applied for isonuclear sequences with nuclear charge up to zmax_recomb, inclusive.
					Use of this option is still experimental!
				""", '0'),
   
      'b2ardr_zmax_recomb' : ('', 'integer', """
					When fix_recomb is changed from 0, and if the ADAS option is in use, then uses the PRB file to add the contribution arising from is--&gt;is-1 processes.
					If the AMJUEL/HYDHEL rates are in use and fix_recomb.eq.0, then the recombination energy is substracted to the electron recombination energy costs. May lead to negative rates!
					This term includes the bremsstrahlung.
					For ADAS, the '0' option only contains the bremsstrahlung for the is--&gt;is-1 process.
					The correction is only applied for isonuclear sequences with nuclear charge up to zmax_recomb, inclusive.
					Use of this option is still experimental!
				""", '1'),
   
      'b2ardr_rtnt' : ('', 'integer', """
					The number of intervals in the discretisation of the density (rtnn) and temperature (rtnt) ranges for the atomic physics tables.
				""", '40'),
   
      'b2ardr_rtnn' : ('', 'integer', """
					The number of intervals in the discretisation of the density (rtnn) and temperature (rtnt) ranges for the atomic physics tables.
				""", '32'),
   
      'b2mndr_dpc_mod_rates_ne_hot_frac' : ('', 'real', """
					Modify the atomic rates by including a hot electron population of temperature te_hot (in eV) and a population faction ne_hot_frac.
					Still experimental.
				""", '0.0'),
   
      'b2mndr_dpc_mod_rates_te_hot' : ('', 'real', """
					Modify the atomic rates by including a hot electron population of temperature te_hot (in eV) and a population faction ne_hot_frac.
					Still experimental.
				""", '0.0'),
   
      'b2ardr_fix_cx' : ('Atomic Physics', 'integer', """
					It is used to 'correct' the CX data
					0 =&gt; do not fix
					1 =&gt; only fix H if CX data is &lt; 1e-40 [default]
					2 =&gt; fix if CX data is &lt; 1e-40
					3 =&gt; fix H
					4 =&gt; fix all
					At the moment the only species with CX data in ADAS is C. Be careful with options that use the fit formula other than for H.
					See the comments in ratstr.F for the origin of the fit formula used to 'fix' the CX data.
				""", '1'),
   
      'b2ardr_no_weisheit' : ('Atomic Physics', 'integer', """
					When set to 1, disables the correction of the hydrogen atomic rate data with the Weisheit data using ratwei.
					Must be set to 1 when using b2ardr_amjhydhel.
					*** Use with caution! ***
				""", '0'),
   
      'b2ardr_amjhydhel' : ('Atomic Physics', 'integer', """
					When not set to 0, reads reaction cards from the AMJUEL/HYDHEL database files to overwrite rates for neutral hydrogenic species.
					The list of reaction cards to be used should be given in the b2ar.dat file.
					Cannot be used in conjunction with no_weisheit.eq.0.
				""", '0'),
   
      'b2ardr_no_smoothing' : ('Atomic Physics', 'integer', """
					When set to 1, disables the tail smoothing for of rate coefficients to represent the effect of a power-law tail on the distribution function. It has been added for compatibility with SOLPS4.3
				""", '0'),
   
      'adas_extrap' : ('Atomic Physics', 'integer', """
					Switch for choosing extrapolation method of ADAS data:
					If adas_extrap.eq.0, a simple 2-D linear extrapolation in log-log space is used (may lead to spurious results).
					If adas_extrap.eq.1, use the extrapolated result, but growing no faster than the parameter variation to the 3/2 power (default).
					If adas_extrap.eq.2, use the nearest domain edge value.
				""", '1'),
   
      'b2ardr_nreac' : ('Atomic Physics', 'integer', """
					Number of AMJUEL/HYDHEL reactions you explicitly specify in b2ar.dat, when b2ardr_amjhydhel = 1. A set of default reactions is taken but can be overwritten by the reactions you specify here.
				""", '0'),
   
      'b2ardr_t_min' : ('Atomic Physics', 'real', """
					Lower temperature bound (in eV) used for rates imported from AMJUEL/HYDHEL database for neutral hydrogenic species. Rates below this bound are given the same value as they have at t_min.
					Only operational if within the bounds provided by tlohi in the b2ar.dat file header.
				""", '0.0'),
   
      'b2ardr_t_max' : ('Atomic Physics', 'real', """
					Upper temperature bound (in eV) used for rates imported from AMJUEL/HYDHEL database for neutral hydrogenic species. Rates above this bound are given the same value as they have at t_max.
					Only operational if within the bounds provided by tlohi in the b2ar.dat file header.
				""", '1.0e30'),
   
      'b2ardr_nn_min' : ('Atomic Physics', 'real', """
					Lower density bound (in m^{-3}) used for rates imported from AMJUEL/HYDHEL database for neutral hydrogenic species. Rates below this bound are given the same value as they have at n_min.
					Only operational if within the bounds provided by nlohi in the b2ar.dat file header.
				""", '0.0'),
   
      'b2ardr_nn_max' : ('Atomic Physics', 'real', """
					Upper density bound (in m^{-3}) used for rates imported from AMJUEL/HYDHEL database for neutral hydrogenic species. Rates above this bound are given the same value as they have at n_max.
					Only operational if within the bounds provided by nlohi in the b2ar.dat file header.
				""", '1.0e30'),
   
      'b2optim_save_states' : ('Optimization', '', """
					If larger than zero, specifies the number of optimization iterations between writes of the intermediate state file b2fstate_optim.XXXX.
				""", '0'),
   
      'b2optim_reset_drift' : ('Optimization', '', """
					Percentage value at which drifts are reset at each function/gradient evaluation to avoid simualtion crash.
				""", '0.4'),
   
      'b2optim_reset_iter' : ('Optimization', '', """
					When resetting drifts, the drift increase multiplier (e.g. fac_exb_inc) will be computed so that drifts are back at 100% in ntim/b2optim_reset_iter iterations.
				""", '2'),
   
},

'b2.neutrals.parameters' : {

      'NSTRAI' : ('b2.neutrals.parameters', 'integer', """
					Number of neutral sources, or 'strata'. Must not be larger than DEF_NSTRA from the [$SOLPSTOP/modules/B2.5/]src/modules(.local)/b2mod_dimensions.F file.
					Need not include the time-dependent stratum. If a time-dependent stratum is used, is incremented internally as needed. The incremented value is referred to as NSTRAT below.
				""", '0'),
   
      'RCPOS' : ('b2.neutrals.parameters', 'integer array of length (NSTRAT)', """
					Position in the B2.5 grid of the strata. Similar use as BCPOS from /BOUNDARY/ namelist. Obsolete for WG.
				""", '-2'),
   
      'RCSTART' : ('b2.neutrals.parameters', 'integer array of length (NSTRAT)', """
					Starting label index on the B2.5 grid. Similar use as BCSTART from /BOUNDARY/ namelist.
				""", '-2'),
   
      'RCEND' : ('b2.neutrals.parameters', 'integer array of length (NSTRAT)', """
					Ending label index on the B2.5 grid. Similar use as BCEND from /BOUNDARY/ namelist.
				""", '-2'),
   
      'RC_LIST_SIZE' : ('b2.neutrals.parameters', 'integer array of length (NSTRAT)', """
					Contains the size of the recycling boundary lists. Similar use as BC_LIST_SIZE from /BOUNDARY/ namelist.
				""", '0'),
   
      'RC_LIST_X' : ('b2.neutrals.parameters', 'integer array of length (2*(NXD+NYD),NSTRAT)', """
					Contains the X-coordinate of the cells where recycling boundaries are applied. Similar use as BC_LIST_X from /BOUNDARY/ namelist. Obsolete for WG.
				""", '-2'),
   
      'RC_LIST_Y' : ('b2.neutrals.parameters', 'integer array of length (2*(NXD+NYD),NSTRAT)', """
					Contains the Y-coordinate of the cells where recycling boundaries are applied. Similar use as BC_LIST_Y from /BOUNDARY/ namelist. Obsolete for WG.
				""", '-2'),
   
      'TARGSP' : ('b2.neutrals.parameters', 'integer array of size (NSTRAT,NTRACK)', """
					Identifies the base material(s) of this stratum wall. The number corresponds to the B2.5 species index produced by sputtering. Check b2cdci for details. If the bulk species is not sputtered, should contain -1.
				""", 'b2stbr_sput_dst'),
   
      'CHEMSP' : ('b2.neutrals.parameters', 'logical array of length NSTRAT', """
					Indicates whether chemical sputtering is allowed from this wall stratum.
				""", '.false.'),
   
      'B2RECYC' : ('b2.neutrals.parameters', 'real array of size (0:NS-1,NSTRAT)', """
					Stores the particle recycling coefficients of species (is) on stratum (istra). Defaults to 1.0 for non-carbon species and 0.0 for carbon species. Particles recycle into the neutral species associated to their isonuclear sequence.
					Applies to B2.5 neutral fluid species.
					If B2RECYC is not explicitly specified, the values from RECYC will be taken.
				""", ''),
   
      'RECYC' : ('b2.neutrals.parameters', 'real array of size (0:NS-1,NSTRAT)', """
					Multiplies Eirene recycling fluxes if 'eirene_use_recyceir' is set to 0 (see b2cdci for details).
					If B2RECYC is not specified, RECYC will also be applied to B2.5 neutral fluid species.
				""", ''),
   
      'MRECYC' : ('b2.neutrals.parameters', 'real array of size (0:NS-1,NSTRAT)', """
					Stores the parallel momentum recycling coefficients of species (is) on stratum (istra). The parallel momentum is carried back by the recycled neutrals. Applies only to B2.5 neutral fluid species.
				""", '0.0'),
   
      'ERECYC' : ('b2.neutrals.parameters', 'real array of size (0:NS-1,NSTRAT)', """
					Stores the energy recycling coefficients of species (is) on stratum (istra). Defaults to 0.3 for non-carbon species and 0.0 for carbon species. The energy is carried back by the recycled neutrals.
					Applies only to B2.5 neutral fluid species.
				""", ''),
   
      'RCION' : ('b2.neutrals.parameters', 'real array of size (0:NS-1,NSTRAT)', """
					Stores the particle-into-ion recycling coefficients of species (is) on stratum (istra). Particles recycle into the next ionised species associated to their isonuclear sequence. Applies only to B2.5 neutral fluid species.
				""", '0.0'),
   
      'RECYCEIR' : ('b2.neutrals.parameters', 'real array of size (NSTRAT)', """
					Multiplier to the Eirene recycling fluxes from stratum (istra). Only used if 'eirene_use_recyceir' is set to 1 (default).
				""", '1.0'),
   
      'USERFLUXPARM' : ('b2.neutrals.parameters', 'real array of size (NSTRAT,2)', """
					The element (istra,1) contains the strength of constant gas puff strata (type 'C') for Eirene in particles/second. Its values overwrite the values provided by the FLUX variables from the strata description in block 7 of the Eirene input file.
				""", '0'),
   
      'CRCSTRA' : ('b2.neutrals.parameters', 'character*1 array of length (NSTRAT)', """
					Contains the type of stratum for Eirene. Possible options include:
					'A' - (automatic) topological mesh boundaries (same use as BCCHAR in /BOUNDARY/ namelist). The boundary mesh faces that have fcLbl.ge.RCSTART and fcLbl.le.RCEND belong to this stratum.
					'V' - volume recombination source (related RCPOS, RCSTART, RCEND and RC_LIST variables are ignored).
					'C' - constant or feedback gas puff source (related RCPOS, RCSTART, RCEND and RC_LIST variables are ignored). Gas puffs for B2.5 fluid neutrals are handled via b2.boundary.parameters. Unless specified otherwise by use of 'eirene_nesepm_istra', it is the first 'C' stratum that is used for feedback puff schemes. See b2cdci for details.
					'T' - time-dependent source for Eirene (related RCPOS, RCSTART, RCEND and RC_LIST variables are ignored). Long-lived Eirene neutrals are stored in this stratum. See EIRENE_STEP_DT below.
				""", ' '),
   
      'STRASCLFL' : ('b2.neutrals.parameters', 'real array of length (NSTRAT)', """
					Scaling factor for the fluid neutral B2.5 sources stemming from the stratum. This scaling is required for the spatially hybrid approach, where the hybrid model for hydrogenic strata is typically combined with a fully kinetic model for other species. In that case, STRASCLFL has to made 1.0 for hydrogenic strata and STRASCLFL has to become small for the other strata. STRASCLFL is a stratum-dependent multiplier in addition to b2mndr_rescale_neutrals_sources. b2mndr_rescale_neutrals_sources is used for all strata and has to be made 1.0 for the hybrid model.
				""", '1.0'),
   
      'SURF_MAT' : ('b2.neutrals.parameters', 'character*2 array of length (NSTRAT)', """
					Contains the surface material for surface strata, used for AFN neutrals. Examples:
					'Be' (beryllium), 'C' (carbon), 'Fe' (iron), 'Mo' (molybdenum) and 'W' (tungsten).
				""", 'C'),
   
      'ACCEL_ION' : ('b2.neutrals.parameters', 'integer array of length (NSTRAT)', """
					If 1, adding sheath acceleration for the ions hitting the boundary. Used for AFN boundary conditions.
				""", '0'),
   
      'MAXW' : ('b2.neutrals.parameters', 'integer array of length (NSTRAT)', """
					Determines the approximation of the particle-velocity distribution of the incident atoms for the AFN boundary condition. MAXW=0: a diffusion approach is used; MAXW=1: a truncated drifting Maxwellian is used. For some cases, MAXW=0 slightly reduces the discrepancy between the fluid and kinetic solution due to an intrinsic correction for lower collisionality. The diffusion and Maxwellian approach are combined when using MAXW=2, for which the Maxwellian approach is used when the local Knudsen number (Kn) is smaller than b2stbr_kn_b1, the diffusion approach is used for Kn &gt; b2stbr_kn_b2 and a linear interpolation between the two approaches for b2stbr_kn_b1 &lt; Kn &lt; b2stbr_kn_b2. The macroscopic length scale to determine the local Knudsen number is defined by the parameter l_macro_afn.
				""", '1'),
   
      'MOL' : ('b2.neutrals.parameters', 'integer array of length (NSTRAT)', """
					Option to define a purely molecular stratum. Useful if you want to treat only molecules kinetically, whereas the recycled atoms are treated on the B2.5 fluid side.
				""", '0'),
   
      'HYB_TYPE' : ('b2.neutrals.parameters', 'character*1 array of length (NSTRAT)', """
					When HYB_TYPE='A' (automatic), possibility to have automatic switching between fluid and kinetic recycling for the stratum for the advanced hybrid model. See description of use_auto_spatial_hyb. HYB_TYPE should be 'M' (manual) for all strata for multispecies simulations (ns &gt; 1).
				""", 'M'),
   
      'E_FC' : ('b2.neutrals.parameters', 'real', """
					Franck-Condon energy assigned to the thermally released fraction of recycled hydrogen neutrals, used in the AFN boundary condition. It is assumed that thermally released molecules are dissociated immediately at the surface and get an energy E_FC (eV) and are emitted isotropically. 3.0 eV is the value typically used in the EIRENE input file.
				""", '3.0'),
   
      'RF_NEUT' : ('b2.neutrals.parameters', 'real array of size (4)', """
					Relaxation parameters multiplying the Eirene particle, parallel momentum, electron energy and ion energy sources respectively before use in B2.
				""", '1.0'),
   
      'PHYS_SPUT' : ('b2.neutrals.parameters', 'real array of size (0:NS-1,NSTRAT)', """
					Stores the physical sputtering multiplier for B2.5 species (is) sputtering on the wall of stratum (istra). Must be non-zero for physical sputtering to occur. Only applies if using B2.5 fluid neutral model.
				""", '0.0'),
   
      'CHEM_SPUT' : ('b2.neutrals.parameters', 'real array of size (0:NS-1,NSTRAT)', """
					Stores the chemical sputtering multiplier for B2.5 species (is) sputtering on the wall of stratum (istra). Must be non-zero for chemical sputtering to occur. Only applies if using B2.5 fluid neutral model.
				""", '0.0'),
   
      'EIRENE_STEP_CPU' : ('b2.neutrals.parameters', 'real', """
					Length of CPU time devoted to Eirene calls after the first one (in s). If zero, the value given in the Eirene input file will be used.
				""", '0.0'),
   
      'EIRENE_STEP_DT' : ('b2.neutrals.parameters', 'real', """
					Physical time (in s) the Eirene particles are to be followed before being passed to the time-dependent stratum. If zero, the value given by DTIMV in block 13 of the Eirene input file will be used.
				""", '0.0'),
   
      'EIRENE_MOD' : ('b2.neutrals.parameters', 'integer', """
					Frequency of Eirene calls. Eirene is called every EIRENE_MOD full B2.5 iterations.
				""", '1'),
   
      'VOLRECSTART' : ('b2.neutrals.parameters', 'real array of size (NSTRAT)', """
					Initial volume recombination rate from stratum (istra) to be used for the volume recombination scaling regulation algorithm. Rendered obsolete by 'eirene_dpc_fix'.
				""", '1.e21'),
   
      'VOLRECINC' : ('b2.neutrals.parameters', 'real', """
					Maximum rate of increase of the volume recombination source strength. The volume recombination regulation scaling scheme is activated if VOLRECINC is neither 0 nor 1.
					Rendered obsolete by 'eirene_dpc_fix'.
				""", ''),
   
      'VOLRECWT' : ('b2.neutrals.parameters', 'real', """
					Weight of new volume recombination strength relative to that of previous iteration in the volume recombination regulation scaling scheme.
					Rendered obsolete by 'eirene_dpc_fix'.
				""", '0.1'),
   
      'B2SPECIES_START' : ('b2.neutrals.parameters', 'integer array of size (NSTRAT)', """
					Specifies the index of the first B2.5 species involved in stratum (istra) for the B2.5 fluid neutral model.
					If not specified, B2SPECIES_START = SPECIES_START.
				""", '0'),
   
      'B2SPECIES_END' : ('b2.neutrals.parameters', 'integer array of size (NSTRAT)', """
					Specifies the index of the last B2.5 species involved in stratum (istra) for the B2.5 fluid neutral model.
					If not specified, B2SPECIES_END = SPECIES_END.
				""", 'ns-1'),
   
      'SPECIES_START' : ('b2.neutrals.parameters', 'integer array of size (NSTRAT)', """
					Specifies the index of the first B2.5 species involved in stratum (istra) for EIRENE.
					SPECIES_START is also used for the B2.5 fluid neutral model, if B2SPECIES_START is not specified.
				""", '0'),
   
      'SPECIES_END' : ('b2.neutrals.parameters', 'integer array of size (NSTRAT)', """
					Specifies the index of the last B2.5 species involved in stratum (istra) for EIRENE.
					SPECIES_END is also used for the B2.5 fluid neutral model, if B2SPECIES_END is not specified.
				""", 'ns-1'),
   
      'NEUTRALS_FILENAME' : ('b2.neutrals.parameters', 'character*256', """
					Name of the next file to use for reading a new /NEUTRALS/ namelist.
				""", 'b2.neutrals.parameters'),
   
      'NEUTRALS_TIME_MOD' : ('b2.neutrals.parameters', 'real', """
					When the B2.5 run simulation time, in seconds, modulo(NEUTRALS_TIME_MOD), reaches or exceeds NEUTRALS_TIME_SWITCH, reads the new namelist from NEUTRALS_FILENAME. Also switches to the new namelist if the ELM count (here time/NEUTRALS_TIME_MOD) changes. Only active if NEUTRALS_TIME_MOD is greater than 0.
				""", '0.0'),
   
      'NEUTRALS_TIME_SWITCH' : ('b2.neutrals.parameters', 'real', """
					If NEUTRALS_TIME_MOD is greater than 0, time (in seconds) within an ELM cycle at which a new NEUTRALS namelist is read.
					Otherwise, B2.5 simulation time, in seconds, when to read the next NEUTRALS namelist file from NEUTRALS_FILENAME.
					Only active if NEUTRALS_TIME_SWITCH is greater than 0.
				""", '0.0'),
   
      'L_NEUTRAD' : ('b2.neutrals.parameters', 'integer', """
					If l_neutrad &gt;= 0, then the radiated power due to the neutrals atoms is taken directly from the Eirene calculation, instead of being recomputed by B2.
				""", '0'),
   
      'L_NEUTFLUX' : ('b2.neutrals.parameters', 'integer', """
					If l_neutflux &gt;=0, then correct treatment of the incident fluxes in B2.5 and b2plot; if &lt;0, then old (approximate) treatment
				""", '0 for coupled cases, -1 otherwise'),
   
      'LSTRASCL' : ('b2.neutrals.parameters', 'integer array of size (NSTRAT,0:natm)', """
					Indicates with which Eirene atomic species to scale the Eirene stratum (istra) (0 means no scaling, default). Atomic species 0 stands for electrons.
				""", ''),
   
      'B2EATCR' : ('b2.neutrals.parameters', 'integer array of size (0:NS-1)', """
					Contains the index of the Eirene atomic species corresponding to the B2.5 species (is).
				""", 'ordering of the B2.5 isonuclear sequences'),
   
      'B2ESPCR' : ('b2.neutrals.parameters', 'integer array of size (0:NS-1)', """
					Contains the isonuclear sequence index of the B2.5 species (is).
				""", 'ordering of the B2.5 isonuclear sequences'),
   
      'EB2ATCR' : ('b2.neutrals.parameters', 'integer array of size (NATM)', """
					Contains the index of the B2.5 neutral fluid species corresponding to the Eirene atomic species (iatm).
				""", 'first B2.5 species of each isonuclear sequence'),
   
      'EB2SPCR' : ('b2.neutrals.parameters', 'integer array of size (NSPECIES)', """
					Contains the index of the first B2.5 fluid for each species.
				""", 'first B2.5 species of each isonuclear sequence'),
   
      'LATMSCL' : ('b2.neutrals.parameters', 'integer array of size (NATM)', """
					Contains the index of the B2.5 isonuclear sequence with which the Eirene atomic species (IATM) should be scaled.
				""", 'assuming one-to-one match between Eirene and B2.5 atomic species'),
   
      'LMOLSCL' : ('b2.neutrals.parameters', 'integer array of size (NMOL)', """
					Contains the index of the Eirene atomic species with which the Eirene molecular species (IMOL) should be scaled.
				""", '0'),
   
      'MLCMP' : ('b2.neutrals.parameters', 'integer array of size (NATM,NMOL)', """
					Contains the number of atoms from Eirene atomic species IATM within each molecule of Eirene molecular species IMOL.
				""", '0'),
   
      'LIONSCL' : ('b2.neutrals.parameters', 'integer array of size (NION)', """
					Contains the index of the Eirene atomic species with which the Eirene test ion species (IION) should be scaled. If not provided, LIONSCL will map to LMOLSCL for molecular ions that match an existing declared molecule, or to the first species listed in the name of the molecular ion as declared in the Eirene input file if no matching molecule is found.
				""", '0'),
   
      'LCNS' : ('b2.neutrals.parameters', 'integer array of size (NSTS)', """
					Contains the indices of Eirene non-standard surfaces (block 3A in input.dat) corresponding to core boundaries.
				""", '0'),
   
      'LTNS' : ('b2.neutrals.parameters', 'integer array of size (NSTS)', """
					Contains the indices of Eirene non-standard surfaces (block 3A in input.dat) corresponding to target boundaries.
				""", '0'),
   
      'LSNS' : ('b2.neutrals.parameters', 'integer array of size (NSTRAT*NSRFS)', """
					Contains the indices of Eirene surfaces related to the recycling sources.
				""", '0'),
   
      'KSNS' : ('b2.neutrals.parameters', 'integer array of size (NSTRAT)', """
					Contains the number of Eirene surfaces for each Eirene recycling stratum.
				""", '0'),
   
      'GPFC' : ('b2.neutrals.parameters', 'real array of size (NATM,NSTRAT)', """
					Specifies the fraction of Eirene atomic species (iatm) in one particle puffed from stratum (istra).
				""", '0.0'),
   
      'DBG_EIR_MC' : ('b2.neutrals.parameters', 'integer', """
					Debug output control for eirene_mc routine. See code for usage.
				""", '0'),
   
      'DEBUG_FLAGS' : ('b2.neutrals.parameters', 'integer array of size (100)', """
					Non-zero elements yield additional print-out data for debugging B2-Eirene coupling. See code for specific uses. Many slots still available for user-specific needs.
					If debug_flags(81).gt.0, will print out target fluxes in files 'targb2.datv', 'targb2n.datv' and 'targb2pl.datv'.
					If debug_flags(90).gt.0, will print output about Eirene non-standard surfaces [debug_flags(90):debug_flags(91)] and strata [debug_flags(92):debug_flags(93)] (0 means sum over all strata). Additional output can be obtained for strata [debug_flags(94):debug_flags(95)].
					If only debug_flags(90) is specified, the output will include all individual Eirene strata, for all non-standard surfaces, starting from debug_flags(90).
				""", '0'),
   
      'NEUT_SCL_LIM' : ('b2.neutrals.parameters', 'real', """
					Maximum number by which Eirene neutral sources may be scaled in either direction within the ank-mods scheme. See explaining text in $SOLPSTOP/doc/Source_Scaling_in_B2.pdf for details.
				""", '2.0'),
   
      'TRACK_INDEX' : ('b2.neutrals.parameters', 'integer array of size (0:NS-1)', """
					Specifies the mixed material species index related to B2.5 species (is).
				""", '1 for species sput_dst, 0 for all others'),
   
      'TRACK_CHEM_SPUT' : ('b2.neutrals.parameters', 'logical array of size (NTRACK)', """
					Indicates whether mixed material species (itrack) participates in chemical sputtering. Defaults to .true. for first tracked species if sput_dst is carbon, and to .false. for all other cases.
				""", ''),
   
      'CHEMICAL_EROSION_REDEP_FAC' : ('b2.neutrals.parameters', 'real', """
					Multiplier to the chemical sputtering coefficient of carbon for computing the rate used for redeposited carbon.
				""", '1.0'),
   
      'CHEMICAL_EROSION_BE_FAC' : ('b2.neutrals.parameters', 'logical', """
					Indicates whether the presence of beryllium is to impact on the chemical sputtering yield of carbon.
				""", '.false.'),
   
      'CHEMICAL_EROSION_BE_FAC_A' : ('b2.neutrals.parameters', 'real', """
					The chemical sputtering yield of carbon is multiplied by
					(1.0-C/2*(tanh((frac-A)/B)-tanh((-A)/B)))
					where frac is the fractional content of Be in the surface layer material.
				""", '0.2'),
   
      'CHEMICAL_EROSION_BE_FAC_B' : ('b2.neutrals.parameters', 'real', """
					See above.
				""", '0.05'),
   
      'CHEMICAL_EROSION_BE_FAC_C' : ('b2.neutrals.parameters', 'real', """
					See above.
				""", '0.9'),
   
      'N_SPCSRF' : ('b2.neutrals.parameters', 'integer', """
					Number of special surfaces groups for diagnostics.
				""", '0'),
   
      'L_SPCSRF' : ('b2.neutrals.parameters', 'integer array of length (NLIM+NSTS)', """
					List of surface segments (non-default standard surfaces [NDSS] or additional surfaces in Eirene notation) included in the groups. Negative numbers correspond to NDSS.
				""", '0'),
   
      'SPS_ID' : ('b2.neutrals.parameters', 'character*8 array of length (N_SPCSRF)', """
					Labels of groups of special surfaces.
				""", ''),
   
      'I_SPCSRF' : ('b2.neutrals.parameters', 'integer array of length (N_SPCSRF)', """
					Index of the first Eirene surface belonging to a special surface group in the L_SPCSRF list.
				""", '0'),
   
      'J_SPCSRF' : ('b2.neutrals.parameters', 'integer array of length (N_SPCSRF)', """
					Index of the last Eirene surface belonging to a special surface group in the L_SPCSRF list.
				""", '0'),
   
      'SPS_ABSR' : ('b2.neutrals.parameters', 'real array of length (N_SPCSRF)', """
					Particle absorption on the surface. If positive, will supercede the setting from the Eirene input file: RECYCT = 1-SPS_ABSR. Ignored if negative.
				""", '-1.0'),
   
      'SPS_TRNO' : ('b2.neutrals.parameters', 'real array of length (N_SPCSRF)', """
					Surface transparency in positive direction. If positive, will supercede the setting from the Eirene input file: TRANSP(1,) = SPS_TRNO. Ignored if negative.
				""", '-1.0'),
   
      'SPS_TRNI' : ('b2.neutrals.parameters', 'real array of length (N_SPCSRF)', """
					Surface transparency in negative direction. If positive, will supercede the setting from the Eirene input file: TRANSP(2,) = SPS_TRNI. If negative, the setting from SPS_TRNO is used.
				""", '-1.0'),
   
      'SPS_MTRI' : ('b2.neutrals.parameters', 'real array of length (N_SPCSRF)', """
					Surface material in Eirene notation (e.g., 1206 for C). If positive, will supercede the setting from the Eirene input file: ZNML = SPS_MTRI. Ignored if negative.
				""", '0'),
   
      'SPS_MTRL' : ('b2.neutrals.parameters', 'character*8 array of length (N_SPCSRF)', """
					Surface material in human notation (e.g., 'C').
				""", ''),
   
      'SPS_TMPR' : ('b2.neutrals.parameters', 'real array of length (N_SPCSRF)', """
					Surface temperature (in eV). If set larger to 1.e10, will be ignored. Otherwise, will supercede the setting from the Eirene input file: EWALL = SPS_TMPR.
				""", '1.e15'),
   
      'SPS_SPPH' : ('b2.neutrals.parameters', 'real array of length (N_SPCSRF)', """
					Fudge factor for physical sputtering. If positive, will supercede the setting from the Eirene input file: RECYCS = SPS_SPPH. Ignored if negative.
				""", '-1.0'),
   
      'SPS_SPCH' : ('b2.neutrals.parameters', 'real array of length (N_SPCSRF)', """
					Fudge factor for chemical sputtering. If positive, will supercede the setting from the Eirene input file: RECYCC = SPS_SPCH. Ignored if negative.
				""", '-1.0'),
   
      'SPS_SGRP' : ('b2.neutrals.parameters', 'integer array of length (N_SPCSRF)', """
					Sputtered particle species flag for chemical sputtering. If positive, will supercede the setting from the Eirene input file: ISRC = SPS_SGRP. Ignored if negative.
				""", '-1'),
   
      'WRITE_NML_NEUT' : ('b2.neutrals.parameters', 'logical', """
					If .true. (default), writes the content of the namelist to stdout after it has been read.
				""", '.true.'),
   
      'MAXPOIN' : ('b2.neutrals.parameters', 'integer', """
					Maximum number of points needed to describe a region contour in Eirene.
				""", '2000'),
   
      'TIME_DEP_PUFF' : ('b2.neutrals.parameters', 'logical array of length (NSTRAT)', """
					Indicates whether a stratum is a time-dependent gas puff. Should only be .true. for strata defined as gas puffs.
				""", '.false. for all strata'),
   
      'TIME_DEP_PUFF_FUNC' : ('b2.neutrals.parameters', 'logical array of length (NSTRAT)', """
					Indicates whether a stratum is using a time-dependent gas puff function. Should only be .true. for strata defined as gas puffs. For use with TIME_DEP_PUFF_CASE and TIME_DEP_PUFF_PARAM.
				""", '.false. for all strata'),
   
      'TIME_DEP_PUFF_CASE' : ('b2.neutrals.parameters', 'integer array of length (NSTRAT)', """
					Used to select the functional form of the time-dependent gas puff function. For use with TIME_DEP_PUFF_FUNC and TIME_DEP_PUFF_PARAM.
				""", '-1 for all strata'),
   
      'TIME_DEP_PUFF_PARAM' : ('b2.neutrals.parameters', 'real array of length (NSTRAT)', """
					Used to set the parameters for the functional form of the time-dependent gas puff function. For use with TIME_DEP_PUFF_FUNC and TIME_DEP_PUFF_CASE.
				""", '0 for all strata'),
   
      'NGPDATA' : ('b2.neutrals.parameters', 'integer data of size (NSTRAT)', """
					Number of points over which the time profile of the strength of gas puff (istra) is given. Defaults to 0. Current maximum value is 100.
				""", '0'),
   
      'GPDATA' : ('b2.neutrals.parameters', 'real data of size (NGPDATA,2,NSTRAT)', """
					For (i,ik,istra) in (1:NGPDATA(istra),1:2,1:NSTRAT),
					GPDATA(i,1,istra) contains the time point (i) for stratum (istra) (in s).
					GPDATA(i,2,istra) contains the gas puff strength of stratum (istra) at time point (i) (in particles/s).
					The gas puff strength before the first time point is given by USERFLUXPARM(istra,1).
					The gas puff strength after the last time point is given by the GPDATA value of the last time point.
					Otherwise, the gas puff strength is linearly interpolated from the given data.
				""", '0.0'),
   
      'CHEMICAL_SPUTTER_YIELD' : ('b2.neutrals.parameters', 'real array of size (0:NLIM+NSTS)', """
					Passed to Eirene. Chemical sputter yield of wall surface (ilim). Element 0 corresponds to the default setting for all surfaces.
				""", '0.0'),
   
      'FCHAR_CHEMICAL' : ('b2.neutrals.parameters', 'real', """
					Nuclear charge of atomic species causing the sputtering. If set to its default value of 0, then the chemical sputtering switches from this block are not used and the settings from the Eirene input file are used.
				""", '0'),
   
      'IGASS_CHEMICAL' : ('b2.neutrals.parameters', 'integer', """
					Passed to Eirene. Eirene atomic species index of the sputtered particle. If igass_chemical &gt; natmi, the data from chemical_sputter_yield is not used and the yield from the Eirene surface blocks is used instead.
				""", '0'),
   
      'ITSPUT_CHEMICAL' : ('b2.neutrals.parameters', 'integer', """
					Passed to Eirene. Eirene type index of the sputtered particle. Atoms = 1, Ions = 4. Defaults to 0, meaning 1 eV atom chemical sputtering.
				""", '0'),
   
      'ISSPUT_CHEMICAL' : ('b2.neutrals.parameters', 'integer', """
					Passed to Eirene. Mass*100 + nuclear charge of the sputtered particle. Defaults to 0, internally changed to 1206 = carbon.
				""", '0'),
    
},

'b2.wall_save.parameters' : {

      'NDEPTH_NML' : ('b2.wall_save.parameters', 'integer', """
					Dimension NDEPTH used for the arrays within this namelist. Represents the number of depth layer discretising the wall elements for the wall model. If using the 0-D model or the time-independent 1-D model, will contain 1 (default). Should not exceed the value of the parameter NDEPTH declared in b2mod_wall.F.
				""", '1'),
   
      'IMAPX' : ('b2.wall_save.parameters', 'integer array of size (NWALL)', """
					Indicates the (ix) position in the grid of wall element (iwall). Default ordering of the wall elements proceeds clockwise in physical space from the lower left corner.
				""", ''),
   
      'IMAPY' : ('b2.wall_save.parameters', 'integer array of size (NWALL)', """
					Indicates the (iy) position in the grid of wall element (iwall). Default ordering of the wall elements proceeds clockwise in physical space from the lower left corner.
				""", ''),
   
      'XYMAP' : ('b2.wall_save.parameters', 'integer array of size (-1:NX,-1:NY)', """
					XYMAP(ix,iy) contains the wall index (iwall) of the wall element located a grid locaion (ix,iy). If there is no wall element at this position, contains 0.
					Default ordering of the wall elements proceeds clockwise in physical space from the lower left corner.
				""", ''),
   
      'SURFACE_MATERIAL_NAME' : ('b2.wall_save.parameters', 'character*6 of size (NWALL)', """
					Contains the filename from which to extract the surface material properties for wall element (iwall). The files are to be found in $SOLPSTOP/data.local/Surface_properties/ or $SOLPSTOP/modules/B2.5/Database/Surface_properties/.
				""", 'C'),
   
      'COATING_MATERIAL_NAME' : ('b2.wall_save.parameters', 'character*6 of size (NWALL)', """
					Contains the filename from which to extract the bulk material properties of the eventual coating for wall element (iwall).
				""", ' '),
   
      'BULK_MATERIAL_NAME' : ('b2.wall_save.parameters', 'character*6 of size (NWALL)', """
					Contains the filename from which to extract the bulk material properties for wall element (iwall). The files are to be found in $SOLPSTOP/data.local/Bulk_properties/ or $SOLPSTOP/modules/B2.5/Database/Bulk_properties/.
				""", 'C'),
   
      'LAYER_ALLOYS' : ('b2.wall_save.parameters', 'character*6 of size (NALLOYS)', """
					Contains the filename from which to extract the material properties for alloy (nalloy) which may be present in mixed materials deposited layers. Not yet operational. The files are to be found in $SOLPSTOP/data.local/Bulk_properties/, $SOLPSTOP/data.local/Surface_properties/, $SOLPSTOP/modules/B2.5/Database/Surface_properties/, or $SOLPSTOP/modules/B2.5/Database/Bulk_properties/.
				""", ''),
   
      'TARGET_TEMP' : ('b2.wall_save.parameters', 'real array of size (NWALL,NDEPTH)', """
					Contains the temperature (in Kelvin) of wall element (iwall) at depth layer (idepth).
					If plate_option.eq.1, will be set to backplate_temp(iwall).
					If plate_option.eq.2 and empty, will be set to equilibrium 1-D profile deduced from plasma incoming fluxes.
					If plate-option.eq.3, must be set.
				""", ''),
   
      'INERTIAL_COOLING' : ('b2.wall_save.parameters', 'logical array of size (NWALL)', """
					Indicates whether wall element (iwall) is inertially cooled instead of actively cooled.
				""", '.false.'),
   
      'BACKPLATE_TEMP' : ('b2.wall_save.parameters', 'real array of size (NWALL)', """
					Contains the temperature (in Kelvin) maintained by cooling at the back end of wall element (iwall).
				""", 'b2stbr_plate_temp'),
   
      'PLATE_THICKNESS' : ('b2.wall_save.parameters', 'real array of size (NWALL)', """
					Contains the thickness (in metres) of wall element (iwall).
				""", 'b2stbr_plate_thick'),
   
      'COATING_THICKNESS' : ('b2.wall_save.parameters', 'real array of size (NWALL)', """
					Contains the thickness (in metres) of the eventual coating on wall element (iwall).
				""", '0'),
   
      'PLATE_TIME_FACTOR' : ('b2.wall_save.parameters', 'real array of size (NWALL)', """
					Multiplier to the time for the equations for temperature and composition evolution of wall element (iwall).
				""", '1.0'),
   
      'DEPOSITION' : ('b2.wall_save.parameters', 'real array of size (NWALL,NTRACK)', """
					Contains the amount of deposited material (in atoms) from species (itrack) onto wall element (iwall).
				""", '0.0'),
   
      'EROSION' : ('b2.wall_save.parameters', 'real array of size(NWALL,NTRACK)', """
					Contains the amount of eroded material (in atoms) of species (itrack) from wall element(iwall).
				""", '0.0'),
   
      'CHEMICAL_SPUTTERING' : ('b2.wall_save.parameters', 'real array of size (NWALL,0:NS-1)', """
					Contains the chemical sputter yield of 'sput_dst' or 'sput_dst_bulk' species on wall element (iwall) caused by B2.5 species (is).
				""", '0.0'),
   
      'PHYSICAL_SPUTTERING' : ('b2.wall_save.parameters', 'real array of size (NWALL,0:NS-1)', """
					Contains the physical sputter yield of 'sput_dst' or 'sput_dst_bulk' species on wall element (iwall) caused by B2.5 species (is).
				""", '0.0'),
   
      'PHYSICAL_SPUTTERING_ENERGY' : ('b2.wall_save.parameters', 'real array of size (NWALL,0:NS-1)', """
					Contains the fraction of returned energy carried by sputtered particles of species 'sput_dst' or 'sput_dst_bulk' species from wall element (iwall) caused by B2.5 species (is).
				""", '0.0'),
   
      'RES_SPUTTERING' : ('b2.wall_save.parameters', 'real array of size (NWALL,0:NS-1)', """
					Contains the RES sputter yield of 'sput_dst' or 'sput_dst_bulk' species on wall element (iwall) caused by B2.5 species (is).
				""", '0.0'),
   
      'THERMAL_EVAPORATION' : ('b2.wall_save.parameters', 'real array of size(NWALL,0:NS-1)', """
					Contains the rate of thermal evaporation of species (is) (in particles/second) from wall element (iwall).
				""", '0.0'),
   
      'BACKSCATTERING' : ('b2.wall_save.parameters', 'real array of size (NWALL,0:NS-1)', """
					Contains the backscattering fraction for incoming B2.5 species (is) onto wall element (iwall).
				""", '0.0'),
   
      'BACKSCATTERING_ENERGY' : ('b2.wall_save.parameters', 'real array of size (NWALL,0:NS-1)', """
					Contains the backscattered energy fraction for incoming B2.5 species (is) onto wall element (iwall).
				""", '0.0'),
   
      'PLATE_TIME' : ('b2.wall_save.parameters', 'real array of size (NWALL)', """
					Indicates how much simulation time has elapsed for wall element (iwall) (in seconds).
				""", '0.0'),
   
      'PLATE_AREA' : ('b2.wall_save.parameters', 'real array of size (NWALL)', """
					Indicates the wall area (in square metres) for wall element (iwall). Defaults to the area computed from the B2.5 grid information.
				""", ''),
   
      'MONOLAYER_DEPOSITION' : ('b2.wall_save.parameters', 'real array of size (NWALL,NTRACK)', """
					Contains the amount of deposited material (in monolayers) from species (itrack) onto wall element (iwall).
				""", '0.0'),
   
      'MONOLAYER_EROSION' : ('b2.wall_save.parameters', 'real array of size (NWALL,NTRACK)', """
					Contains the amount of eroded material (in monolayers) of species (itrack) from wall element (iwall).
				""", '0.0'),
   
      'LAYER_NCONSTITUENTS' : ('b2.wall_save.parameters', 'integer array of size (NWALL)', """
					Indicates the number of elemental constituents within the surface layer of wall element (NWALL).
				""", '1'),
   
      'LAYER_NZCONSTITUENTS' : ('b2.wall_save.parameters', 'integer array of size (NWALL,6+NTRACK)', """
					Contains the atomic numbers Z of the various elements present within the surface layer of wall element (iwall). Defaults to 6 for the first value, 0 otherwise.
				""", ''),
   
      'LAYER_RELCONSTITUENTS' : ('b2.wall_save.parameters', 'real array of size (NWALL,6+NTRACK)', """
					Contains the relative atomic abundances of the various elements present within the surface layer of wall element (iwall). Defaults to 1.0 for the first value, 0.0 otherwise.
					Replaces LAYER_NRELCONSTITUENTS.
				""", ''),
    
},

'b2md.dat' : {

      'EXP' : ('b2md.dat', 'character*128', """
					Name of the experiment being modelled.
				""", 'NOT_SET'),
   
      'SHOT' : ('b2md.dat', 'integer', """
					Shot number identifying the run. Defaults to the last number found in shotnumber.history, or 0 if the file is not found.
				""", ''),
   
      'TIME' : ('b2md.dat', 'real', """
					Time point of the experimental shot being simulated.
				""", '0.0'),
   
      'COMMENT' : ('b2md.dat', 'character*128', """
					Label for the run.
				""", 'NOT_SET'),
   
      'TIMEDEP' : ('b2md.dat', 'logical', """
					If .true. (default), saves data from b2time.nc.
				""", ''),
   
      'SNAPSHOT' : ('b2md.dat', 'logical', """
					If .true. (default), saves data from b2fplasma.
				""", ''),
   
      'TALLIES' : ('b2md.dat', 'logical', """
					If .true. (default), saves data from b2tallies.nc.
				""", ''),
   
      'MOVIES' : ('b2md.dat', 'logical', """
					If .true. (default), saves data from b2movies.nc.
				""", ''),
   
      'OVERWRITE_SHOTNUMBER' : ('b2md.dat', 'integer', """
					Indicate the shot number to overwrite (to be used only when updating an already saved run with 'resave_mds' script).
					Defaults to the last number found in shotnumber.history, or 0 if the file is not found.
				""", ''),
    
},

'b2.boundary.parameters' : {

      'NBC' : ('b2.boundary.parameters', 'integer', """Number of boundary segments.""", '0'),
   
      'BCCHAR' : ('b2.boundary.parameters', 'character*1 array of length (NBC)', """
					In the WG code, BCHAR is always equal to 'A' (automatic) and a boundary list is defined by the mesh boundary faces that have fcLbl.ge.BCSTART and fcLbl.le.BCEND.
				""", ' '),
   
      'CONPAR' : ('b2.boundary.parameters', 'real array of size (0:NS-1,NBC,3)', """
					Contains parameters helping to define the boundary conditions for the continuity equation of species (is). See description of BCCON below for details.
				""", '0.0'),
   
      'MOMPAR' : ('b2.boundary.parameters', 'real array of size (0:NS-1,NBC,2)', """
					Contains parameters helping to define the boundary conditions for the parallel momentum equation of species (is). See description of BCMOM below for details.
				""", '0.0'),
   
      'ENEPAR' : ('b2.boundary.parameters', 'real array of size (NBC,2)', """
					Contains parameters helping to define the boundary conditions for the electron energy equation. See description of BCENE below for details.
				""", '0.0'),
   
      'ENIPAR' : ('b2.boundary.parameters', 'real array of size (NBC,2)', """
					Contains parameters helping to define the boundary conditions for the ion energy equation. See description of BCENI below for details.
				""", '0.0'),
   
      'POTPAR' : ('b2.boundary.parameters', 'real array of size (NBC,2)', """
					Contains parameters helping to define the boundary conditions for the potential equation. See description of BCPOT below for details.
				""", '0.0'),
   
      'BCPOS' : ('b2.boundary.parameters', 'integer array, length (NBC)', """
					For North, South or X boundary conditions, it specifies the row index; for West, East and Y boundary conditions, it specifies the column index. Obsolete for WG.
				""", '-2'),
   
      'BCSTART' : ('b2.boundary.parameters', 'integer array, length (NBC)', """
					Starting label index (fcLbl) of the cells belonging to this boundary condition.
				""", '-2'),
   
      'BCEND' : ('b2.boundary.parameters', 'integer array, length (NBC)', """
					Ending label index (fcLbl) of the cells belonging to this boundary condition.
				""", '-2'),
   
      'BC_LIST_SIZE' : ('b2.boundary.parameters', 'integer array of length (NBC)', """
					Contains the size of the list of cells where a boundary condition is applied.
				""", '0'),
   
      'BC_LIST_X' : ('b2.boundary.parameters', 'integer array of length (2*(NXD+NYD),NBC)', """
					Contains the X-coordinate of the cells where boundaries conditions are applied. Obsolete for WG.
				""", '-2'),
   
      'BC_LIST_Y' : ('b2.boundary.parameters', 'integer array of length (2*(NXD+NYD),NBC)', """
					Contains the Y-coordinate of the cells where boundaries conditions are applied. Obsolete for WG.
				""", '-2'),
   
      'BCCON' : ('b2.boundary.parameters', 'integer array, length (0:NS-1,NBC)', """
					Specifying the type of density boundary condition for each segment and species (fastest varying index is species); makes use of CONPAR to specify additional information, as indicated:
					0 : default, no boundary condition is applied
					1 : prescribe the value of the density, CONPAR(,,1) specifies the required density in m<sup>-3</sup>
					2 : prescribe the gradient of the density, CONPAR(,,1) specifies the required density gradient in m<sup>-4</sup>
					3 : sheath conditions, CONPAR(,,1) not used (zero gradient is used)
					4 : prescribe the value of the density, weakly a mixed boundary condition, CONPAR(,,1) specifies the required density in m<sup>-3</sup> and CONPAR(,,2) specifies the 'strength' of the boundary condition.
					5 : prescribe the particle flux per unit area, CONPAR(,,1) specifies the required particle flux density in m<sup>-2</sup>.s<sup>-1</sup>
					6 : prescribe the total particle flux for a constant density, CONPAR(,,1) specifies the particle flux in s<sup>-1</sup>. Not yet available for WG.
					7 : prescribe the given profile of density from the bv_na.dat file (requires b2mndr_boundary_sources.eq.1)
					8 : prescribe the total particle flux with constant flux density, CONPAR(,,1) specifies the particle flux in s<sup>-1</sup>
					9 : prescribe the decay length for the density, CONPAR(,,1) specifies the gradient length in metres (should use type 15 instead when drifts are turned on)
					10 : leakage option for density, recommended for cases with drifts, CONPAR(,,1) specifies the leakage factor, α in Γ<sub>loss</sub> = α C<sub>s</sub> n<sub>a</sub>, CONPAR(,,2)&gt;0 is the stabilizing factor which may be needed if drifts are activated.
					11 : should not be used for feedbacks anymore, not converted to WG code.
					12 : should not be used for feedbacks anymore, not converted to WG code.
					13 : particle density to achieve specified total flux, CONPAR(,,1) is the specified flux crossing the boundary flux surface, CONPAR(,,2) is the strength of the feedback (if left zero, b2stbc_bc_ref will be used), CONPAR(,,3), when running with Eirene and the 'ionising core' switch is used, is set internally to match the re-entering flux of ionised neutrals that crossed the core boundary (one must then have 'ionising_core'.eq.-IB where IB is the boundary index).
					14 : sound speed velocity flux, CONPAR(,,1) is a multiplier to the outgoing sound speed C<sub>s</sub>. To be used in conjunction with BCENE/I=15, BCPOT=11, and BCMOM=13. Recommended for cases with drifts. If CONPAR(,,2).gt.0, an additional decay-length loss is added, where CONPAR(,,2) is the decay length.
					15 : prescribe a radial leakage velocity, CONPAR(,,1) specifies the leakage velocity in units of the local thermal velocity.
					16 : particle density to achieve specified total flux, used with ASTRA coupling. The total desired flux is summed over all BCCON=16 core boundaries. CONPAR(,,1) specifies the desired particle flux in s<sup>-1</sup>. CONPAR(,,2) is the strength of the feedback (if left zero, b2stbc_bc_ref will be used).
					18 : prescribe total main ion particle flux, used with ASTRA coupling. Not yet available for WG.
					19 : particle flux feedback boundary condition, flux is summed over neutrals and ions, for coupling with ASTRA. The total desired flux is summed over all BCCON=19 core boundaries. This boundary condition type is applied to ions in their highest ionisation stage. CONPAR(,,1) specifies the desired particle flux in s<sup>-1</sup>. CONPAR(,,2) is the strength of the feedback (if left zero, b2stbc_bc_ref will be used).
					20 : constant density feedback condition, CONPAR(,,1) specifies the desired density in m<sup>-3</sup>. Not yet available for WG.
					21 : prescribe the value of the density and add a poloidal density variation to get a solution which is as close as possible to neoclassical theory. It is recommended to use this boundary condition together with corresponding condition on ion temperature (BCENI=24). The total desired density is summed over all BCCON=21 core boundaries. CONPAR(,,1) specifies the desired density in m<sup>-3</sup>.
					22 : feedback boundary condition: given total particle flux with constant average density. The poloidal density variation is added to make the solution as close as possible to the neoclassical value derived for pure H/D/T plasma. It is recommended to use this boundary condition with corresponding boundary condition on ion temperature (BCENI=23,24). The total desired flux is summed over all BCCON=22 core boundaries. CONPAR(,,1) specifies the desired particle flux in s<sup>-1</sup>. CONPAR(,,2) is the strength of the feedback (if left zero, b2stbc_bc_ref will be used).
					23 : feedback boundary condition: given sum of integrated neutrals and main ion particle fluxes with constant average density. The poloidal density variation is added to make the solution as close as possible to the neoclassical value derived for pure H/D/T plasma. It is recommended to use this boundary condition with corresponding boundary condition on ion temperature (BCENI=23,24). The total desired flux is summed over all BCCON=23 core boundaries. CONPAR(,,1) specifies the desired particle flux in s<sup>-1</sup>. CONPAR(,,2) is the strength of the feedback (if left zero, b2stbc_bc_ref will be used).
					24 : constant density feedback scaled by density on the ring 'bc_type21_ref' away. CONPAR(,,1) specifies the desired density in m<sup>-3</sup>. CONPAR(,,2) is the strength of the feedback (if left zero, b2stbc_bc_ref will be used). Not yet available for WG.
					25 : feedback boundary condition: prescribe the average value of the density and add the poloidal density variation from the neighbouring radial ring. This boundary condition is suitable for any species of a multi-species plasma (i.e. in the case when the condition used in BCCON=21 fails). It is recommended to use this boundary condition together with the corresponding condition on ion temperature (BCENI=26,27). CONPAR(,,1) specifies the desired average density in m<sup>-3</sup>.
					26 : feedback boundary condition: prescribe the total ion flux and find the average density. The poloidal density variation from the neighbouring radial ring is applied on top of the average density. This boundary condition is suitable for any species of a multi-species plasma (i.e. in the case when the condition used in BCCON=22 fails). It is recommended to use this boundary condition together with a corresponding condition on the ion temperature (BCENI=26,27). The total desired flux is summed over all BCCON=26 core boundaries. CONPAR(,,1) specifies the desired particle flux in s<sup>-1</sup>. CONPAR(,,2) is the strength of the feedback (if left zero, b2stbc_bc_ref will be used).
					27 : feedback boundary condition: prescribe the particle flux sum for all neutrals and ions belonging to a given isonuclear sequence and find the average density. The poloidal density variation from the neighbouring radial ring is applied on top of the average density. It is recommended to use this boundary condition together with corresponding condition on ion temperature (BCENI=25,26). The total desired flux is summed over all BCCON=27 core boundaries. CONPAR(,,1) specifies the desired particle flux in s<sup>-1</sup>. CONPAR(,,2) is the strength of the feedback (if left zero, b2stbc_bc_ref will be used).
					28 : Prescribe the flux surface averaged density, with a poloidal perturbation taken from the flux tube just inside the domain. Only intended for core boundaries. CONPAR(,,1) specifies the desired average density in m<sup>-3</sup>.
					29 : Feedback on the total particle flux, by imposing a flux surface averaged density, with a poloidal perturbation taken from the flux tube just inside the domain. CONPAR(,,1) specifies the desired particle flux in s<sup>-1</sup>. CONPAR(,,2) is the strength of the feedback (if left zero, b2stbc_bc_ref will be used). Intended for core boundaries only.
				""", ''),
   
      'BCMOM' : ('b2.boundary.parameters', 'integer array, length NS * NBC', """
					Specifying the type of parallel momentum or velocity boundary condition for each segment and species (fastest varying index is species); makes use of MOMPAR to specify additional information, as indicated
					0 : default, no boundary condition is applied
					1 : prescribe the value of the parallel velocity, MOMPAR(,,1) specifies the parallel velocity in m.s<sup>-1</sup>
					2 : prescribe the gradient of the parallel velocity, MOMPAR(,,1) specifies the parallel velocity gradient in s<sup>-1</sup>
					3 : sheath conditions, Mach number as input, if MOMPAR(,,2) &lt; 0.5, then the velocity is set to exactly MOMPAR(,,1) * C<sub>s,collective</sub>, otherwise the velocity is set to be at least MOMPAR(,,1) * C<sub>s,a</sub>, the thermal velocity of that species. BCMOM = 3 was not adapted for WG. Replace with drift-compatible BCMOM = 13.
					4 : prescribe the value of the velocity, weakly a mixed boundary condition, MOMPAR(,,1) specifies the parallel velocity in m.s<sup>-1</sup> and MOMPAR(,,2) specifies the 'strength' of the boundary condition.
					5 : prescribe the parallel momentum flux per unit area, MOMPAR(,,1) specifies the parallel momentum flux density in N.m<sup>-2</sup>
					6 : prescribe the total parallel momentum flux for a constant parallel velocity [not yet available]
					7 : prescribe the given profile of parallel velocity from the bv_ua.dat file (requires b2mndr_boundary_sources.eq.1)
					8 : special : limited shear, imposes zero gradient for the Mach number. [[[Eventually intended to have MOMPAR(,,1) specify the gradient of the Mach number in m<sup>-1</sup>]]].
					9 : prescribe the total parallel momentum flux with constant flux density, MOMPAR(,,1) specifies the parallel momentum flux in N.
					10 : prescribe the decay length for the parallel momentum, MOMPAR(,,1) specifies the decay length in m.
					11 : Rozhansky viscosity condition for the parallel momentum, MOMPAR(,,1) is not used. Not yet available for WG.
					12 : condition from b2stbc_spb for the parallel momentum.
					13 : drift-compatible sheath boundary condition for the parallel momentum. To be used in conjunction with BCENE/I=15, BCPOT=11, and BCCON=14. Recommended for cases with drifts.
					14 : condition from b2stbc_spb for the parallel momentum
					15 : prescribe the value of the parallel velocity, scaled with B_average/B_local. Not yet available for WG.
					16 : prescribe the average value of the parallel velocity MOMPAR(,,1) specifies the parallel velocity in m.s<sup>-1</sup>
					17 : leakage option for parallel momentum, MOMPAR(,,1) specifies the leakage factor, α in Γ<sub>loss</sub> = α C<sub>s,a</sub> m<sub>a</sub> n<sub>a</sub> u<sub>a</sub>
					18 : explicitly enforce zero source terms, resulting in zero flux.
				""", ''),
   
      'BCENE' : ('b2.boundary.parameters', 'integer array, length NBC', """
					Specifying the type of electron energy or temperature boundary condition for each segment; makes use of ENEPAR to specify additional information, as indicated
					0 : default, no boundary condition is applied
					1 : prescribe the value of the electron temperature, ENEPAR(,1) specifies the temperature in eV
					2 : prescribe the gradient of the electron temperature, ENEPAR(,1) specifies the temperature gradient in eV.m<sup>-1</sup>
					3 : sheath conditions, electron energy transmission, ENEPAR(,1) specifies an additional contribution to the energy transmission coefficient in addition to that of the potential difference [the sound speed used depends on settings of MOMPAR(,ISMAIN,2)]. BCENE = 3 not adapted for WG. Replace with drift-compatible BCENE = 15.
					4 : prescribe the value of the electron temperature, weakly a mixed boundary condition, ENEPAR(,1) specifies the temperature in eV and ENEPAR(,2) specifies the 'strength' of the boundary condition.
					5 : prescribe the electron energy flux per unit area, ENEPAR(,1) specifies the energy flux density in W.m<sup>-2</sup>.
					6 : prescribe the total electron energy flux for a constant electron temperature, ENEPAR(,1) specifies the energy flux in W (no longer supported, use types [16] or [17] instead).
					7 : prescribe the electron temperature profile from the bv_te.dat file (requires b2mndr_boundary_sources.eq.1).
					8 : prescribe the total electron heat flux with constant flux density, ENEPAR(,1) specifies the energy flux in W.
					9 : prescribe the decay length for the electron temperature, ENEPAR(,1) specifies the decay length in m (can also use type [19] instead).
					10 : should not be used for feedbacks anymore, not converted to WG code.
					11 : not used
					12 : sheath conditions, electron energy transmission coefficient, ENEPAR(,1) specifies an energy transmission factor, delta<sub>e</sub> in Q<sub>e</sub> = delta<sub>e</sub> Γ<sub>e</sub> T<sub>e</sub>. Obsolete. Replace with drift-compatible BCENE = 15.
					13 : prescribe the electron energy flux per unit area proportional to temperature, ENEPAR(,1) specifies the energy flux density per temperature in W.m<sup>-2</sup>.J<sup>-1</sup> (the temperature here in J).
					14 : leakage option for electron energy, ENEPAR(,1) specifies the leakage factor, α in Γ<sub>loss</sub> = α C<sub>s</sub>, collective n<sub>e</sub> T<sub>e</sub>. The energy loss also includes an electrostatic term as α ENEPAR(,2) C<sub>s</sub>,collective e Φ n<sub>e</sub>.
					15 : sheath boundary condition, recommended when using drifts (see Section C.9.4 of manual for details). Linked to using BCCON=14 and BCMOM=13 for all ion species, BCENI=15, and BCPOT=11.
					16 : feedback boundary condition with constant temperature, ENEPAR(,1) specifies the power flux in W across the core boundary, ENEPAR(,2) should be something like 0.1 and specifies the strength of the feedback (if left zero, b2stbc_bc_ref_te will be used). Also see type [17] below. Available if bcene_16_style=0 (default). If bcene_16_style=1, integrated electron heat flux with constant electron temperature, summed over all core boundaries with BCENE=16.
					17 : feedback boundary condition with constant shared temperature for both electrons and ions, with ENEPAR(,1) + ENIPAR(,1) giving the total power flux in W across the core boundary, ENEPAR(,2) should be something like 0.1 and specifies the strength of the feedback. Recommended to replace [16] for high densities.
					18 : fractional drop condition. Experimental. Attempts to set the guard cell temperature to be (1 - ENEPAR(,1)) times the boundary cell temperature.
					19 : same as [9] but to be used when simultaneously setting BCCON=1 on the same boundary. Not yet available for WG.
					20 : feedback boundary condition with constant temperature, as per type [16] but with a different feedback scheme. ENEPAR(,2) is the strength of the feedback (if left zero, b2stbc_bc_ref_te is used).
					21 : constant temperature feedback scaled by temperature. ENEPAR(,1) specifies the desired electron temperature in eV. ENEPAR(,2) is the strength of the feedback (if left zero, b2stbc_bc_ref_te is used).
					22 : radial leakage condition for the electron temperature. ENEPAR(,1) specifies the leakage velocity in units of the electron thermal velocity. A temperature gradient such that the diffusive flux is set to match this leakage is imposed.
					23 : prescribe the value of the electron temperature, with a poloidal perturbation taken from the flux tube just inside the domain. Intended only for core boundaries. ENEPAR(,1) specifies the desired average electron temperature in eV.
					24 : feedback on the total electron energy flux, by imposing a flux surface averaged temperature, with a poloidal perturbation taken from the flux tube just inside the domain. Intended only for core boundaries. ENEPAR(,1) specifies the energy flux in W. ENEPAR(,2) specifies the strength of the feedback (if left zero, b2stbc_bc_ref_te will be used).
				""", ''),
   
      'BCENI' : ('b2.boundary.parameters', 'integer array, length NBC', """
					Specifying the type of ion energy or temperature boundary condition for each segment; makes use of ENIPAR to specify additional information, as indicated
					0 : default, no boundary condition is applied
					1 : prescribe the value of the ion temperature, ENIPAR(,1) specifies the temperature in eV
					2 : prescribe the gradient of the ion temperature, ENIPAR(,1) specifies the temperature gradient in eV.m<sup>-1</sup>
					3 : sheath conditions, ion energy transmission, ENIPAR(,1) specifies the contribution to the energy transmission coefficient [the sound speed used depends on settings of MOMPAR(,ISMAIN,2)]. BCENI = 3 not adapted for WG. Replace with drift-compatible BCENI = 15.
					4 : prescribe the value of the ion temperature, weakly a mixed boundary condition, ENIPAR(,1) specifies the temperature in eV and ENIPAR(,2) specifies the 'strength' of the boundary condition.
					5 : prescribe the ion energy flux per unit area, ENIPAR(,1) specifies the energy flux density in W.m<sup>-2</sup>.
					6 : prescribe the total ion energy flux for a constant ion temperature, ENIPAR(,1) specifies the energy flux in W (no longer supported, use types [16] or [17] instead)
					7 : prescribe the ion temperature profile from the bv_ti.dat file (requires b2mndr_boundary_sources.eq.1)
					8 : prescribe the total ion heat flux with constant flux density, ENIPAR(,1) specifies the energy flux in W
					9 : prescribe the decay length for the ion temperature, ENIPAR(,1) specifies the decay length in m (can also use type [19] instead)
					10 : should not be used for feedbacks anymore, not converted to WG code.
					11 : sheath conditions, ion energy transmission coefficient, ENIPAR(,1) specifies an energy transmission factor, delta<sub>i</sub> in Q<sub>i</sub> = delta<sub>i</sub> T<sub>i</sub> sum<sub>a</sub> n<sub>a</sub> C<sub>s,a</sub>. Not yet available for WG.
					12 : sheath conditions, ion energy transmission coefficient, ENIPAR(,1) specifies an energy transmission factor, delta<sub>i</sub> in Q<sub>i</sub> = delta<sub>i</sub> T<sub>i</sub> sum<sub>a</sub> Γ<sub>a</sub>. Obsolete. Replace with drift-compatible BCENI = 15.
					13 : prescribe the ion energy flux per unit area proportional to temperature, ENIPAR(,1) specifies the energy flux density per temperature in W.m<sup>-2</sup>.J<sup>-1</sup> (the temperature here in J).
					14 : leakage option for ion energy, ENIPAR(,1) specifies the leakage factor, α in Γ<sub>loss</sub> = α C<sub>s</sub>T<sub>i</sub>.
					15 : sheath boundary condition, recommended when using drifts (see Section C.9.5 of manual for details). Linked to using BCCON=14 and BCMOM=13 for all ion species, along with BCENE=15 and BCPOT=11.
					16 : feedback boundary condition with constant temperature, ENIPAR(,1) specifies the power flux in W across the flux surface with index 'b2stbc_type16_ref' (default=-1), ENIPAR(,2) should be something like 0.1 and specifies the strength of the feedback (if left zero, b2stbc_bc_ref_ti will be used). Also see type [17] below. Available if bceni_16_style=0 (default). If bceni_16_style=1, integrated ion heat flux with constant ion temperature, summed over all core boundaries with BCENI=16. ENIPAR(,1) specifies the power flux in W.
					17 : feedback boundary condition with constant shared temperature for both electrons and ions, see BCENE=17 above for description.
					18 : fractional drop condition.  Experimental. Attempts to set the guard cell temperature to be (1 - ENIPAR(,1)) times the boundary cell temperature.
					19 : same as [9] but to be used when simultaneously setting BCCON=1 on the same boundary. Not yet available for WG.
					20 : feedback boundary condition with constant temperature, as per type [16] but with a different feedback scheme. ENEPAR(,2) is the strength of the feedback (if left zero, b2stbc_bc_ref_ti is used).
					21 : from b2stbc_spb. Not yet available for WG.
					22 : radial leakage condition for the ion temperature. ENIPAR(,1) specifies the leakage velocity in units of the collective ion thermal velocity. A temperature gradient such that the diffusive flux is set to match this leakage is imposed.
					23 : prescribe the poloidally averaged value of the ion temperature and introduce a poloidal variation as close as possible to neoclassical solution. It is recommended to use this boundary condition together with corresponding condition on ion density (BCCON=21,22,23). The average is taken over all core boundaries with BCENI=23. ENIPAR(,1) specifies the temperature in eV.
					24 : feedback boundary condition with prescribed total ion flux, constant poloidally averaged ion temperature and a poloidal variation as close as possible to neoclassical solution. It is recommended to use this boundary condition together with corresponding condition on ion density (BCCON=21,22,23). The flux is summed over all core boundaries with BCENI=24. ENIPAR(,1) specifies the energy flux in W. ENIPAR(,2) gives the strength of the feedback (if left zero, b2stbc_bc_ref_ti will be used).
					25 : constant temperature feedback scaled by temperature on nearby ring. ENIPAR(,1) specifies the desired ion temperature in eV. ENIPAR(,2) is the strength of the feedback (if left zero, b2stbc_bc_ref_ti will be used).
					26 : prescribe the poloidally averaged value of the ion temperature and introduce a poloidal variation in a simplified manner. This boundary condition is suitable for any plasma composition (i.e. when BCENI=23 fails). It is recommended to use this boundary condition together with corresponding condition on ion density (BCCON = 25,26,27). The average is taken over all core boundaries with BCENI=26. ENIPAR(,1) specifies the temperature in eV.
					27 : feedback boundary condition with prescribed total ion heat flux, constant poloidally averaged ion temperature and a poloidal variation in a simplified manner. This boundary condition is suitable for any plasma composition (i.e. when BCENI=24 fails). It is recommended to use this boundary condition together with corresponding condition on ion density (BCCON = 25,26,27). The flux is summed over all core boundaries with BCENI=27. ENIPAR(,1) specifies the energy flux in W. ENIPAR(,2) gives the strength of the feedback (if left zero, b2stbc_bc_ref_ti will be used).
					28 : prescribe the value of the ion temperature, with a poloidal perturbation taken from the flux tube just inside the domain. ENIPAR(,1) specifies the average temperature in eV.
					29 : feedback on the total ion energy flux, by imposing a flux surface averaged temperature, with a poloidal perturbation taken from the flux tube just inside domain. ENIPAR(,1) specifies the energy flux in W. ENIPAR(,2) specifies the strength of the feedback (if left zero, b2stbc_bc_ref_ti will be used).
				""", ''),
   
      'BCPOT' : ('b2.boundary.parameters', 'integer array, length NBC', """
					Specifying the type of electric potential or current boundary condition for each segment; makes use of POTPAR to specify additional information, as indicated
					0 : default, no boundary condition is applied
					1 : prescribe the value of the potential, POTPAR(,1) specifies the potential in V
					2 : prescribe the gradient of the potential, POTPAR(,1) specifies the potential gradient in V.m<sup>-1</sup>
					3 : sheath conditions,
						POTPAR(,2) used for biasing [see code for details]. BCPOT = 3 not adapted for WG. Replace with drift-compatible BCPOT = 11.
					4 : prescribe the value of the potential weakly a mixed boundary condition, POTPAR(,1) specifies the potential in V and POTPAR(,2) specifies the 'strength' of the boundary condition.
					5 : prescribe the current flux density per unit area, POTPAR(,1) specifies the electric current flux density in A.m<sup>-2</sup>.
					6 : prescribe the total current flux density for a constant potential [not yet available]
					7 : prescribe the given profile of potential from the bv_po.dat file (requires b2mndr_boundary_sources.eq.1)
					8 : prescribe the total electric current with constant flux density, POTPAR(,1) specifies the electric current in A
					9 : prescribe the decay length for the potential, POTPAR(,1) specifies the decay length in m.
					10 : should not be used for feedbacks anymore, not converted to WG code.
					11 : sheath conditions, electron energy transmission, POTPAR(,2) specifies the bias potential in V. Recommended for use in cases with drifts, along with BCENE/I=15, BCCON=14, and BCMOM=13.
					12 : imposes the currents due to drifts for the core boundary. Must be used in conjunction with istyle_cur_contr_on_S_and_N.eq.2
					13 : imposes the currents due to drifts for the private flux and main chamber boundaries. Must be used in conjunction with istyle_cur_contr_on_S_and_N.eq.2
					14 : prescribe the total current without imposing a specific profile. Follow the profile of the 1st flux tube inside. Intended use: core boundary, total PF boundary,.. For testing purposes, use with care!
					15 : feedback boundary condition on total current with constant potential. POTPAR(,1) specifies the electric current in A. POTPAR(,2) specifies the strength of the feedback (if left zero, b2stbc_bc_ref_te will be used).
					16 : constant electric potential feedback on imposed total current. The current prescribed is given by the sum of the POTPAR(IB,1) (in A) over all the BCPOT=16 boundaries. Still experimental, will not work for drift cases.
					17 : feedback condition on total current, imposing a potential profile matching that of the neighbouring flux tube. POTPAR(,1) specifies the electric current in A. POTPAR(,2) specifies the strength of the feedback (if left zero, b2stbc_bc_ref_te will be used).
					21 : constant potential feedback scaled by potential on the nearby ring. POTPAR(,,1) specifies the desired potential in V. POTPAR(,,2) is the strength of the feedback (if left zero, b2stbc_bc_ref_te will be used).
					22 : prescribe the value of the potential, with a perturbation taken from the first flux tube in the domain. Intended for core boundaries only. POTPAR(,1) specifies the average potential.
					23 : potential feedback on the total current for the core boundary, imposing a flux surface averaged potential, with poloidal perturbation taken from flux tube just inside domain. The feedback is scaled with the ion temperature. POTPAR(,,1) specifies the desired integral current through flux surfaces (in Amperes). POTPAR(,,2) is the strength of the feedback (if left zero, b2stbc_bc_ref_te will be used).
				""", ''),
   
      'BCENK' : ('b2.boundary.parameters', 'integer array, length NBC', """
					Specifying the type of boundary condition for the turbulent kinetic energy (kt) for each segment; makes use of ENKPAR to specify additional information, as indicated
					0 : default, no boundary condition is applied
					1 : prescribe the value of the turbulent kinetic energy, ENKPAR(,1) specifies the energy in eV.
					2 : prescribe the gradient of the turbulent kinetic energy, ENKPAR(,1) specifies the gradient of the turbulent kinetic energy in eV/m.
					6 : prescribe the total flux of turbulent kinetic energy, following the profile of the total heat flux. ENKPAR(,1) specifies the flux in W.
					7 : prescribe the total flux of turbulent kinetic energy, following the profile of the particle flux. ENKPAR(,1) specifies the flux in W.
					8 : prescribe the total flux of turbulent kinetic energy, with constant flux density. ENKPAR(,1) specifies the flux in W.
					14 : leakage option for turbulent kinetic energy, ENKPAR(,1) specifies the leakage factor, α in Γ<sub>loss</sub>; = α C<sub>s,collective</sub> n<sub>i</sub> κ.
					15 : sheath loss boundary condition. For now it assumes that BCCON = 14 is used. ENKPAR(,1) specifies the sheath transmission factor corresponding to the particle fluxes dictated by CONPAR(,,1) and ENKPAR(,2) specifies the sheath transmission factor corresponding to the particle fluxes dictated by CONPAR(,,2).
					16 : prescribe the value of the turbulent kinetic energy, with a poloidal perturbation taken from the flux tube just inside domain. kt = ENKPAR(,1) + kt2 - kt2av, where kt2 is the turbulent kinetic energy in the first cell inside the domain, and kt2av is the average turbulent kinetic energy in the flux tube just inside the domain. Intended for core boundaries only.
					17 : feedback on the turbulent kinetic energy flux, by imposing a flux surface averaged κ, with a poloidal perturbation taken from the flux tube just inside the domain. Intended for core boundaries only. ENKPAR(,1) specifies the flux in W. ENKPAR(,2) specifies the strength of the feedback (if left zero, b2stbc_bc_ref_ti will be used).
				""", ''),
   
      'BCENZ' : ('b2.boundary.parameters', 'integer array, length NBC', """
					Specifying the type of boundary condition for the turbulent enstrophy (zt) for each segment; makes use of ENZPAR to specify additional information, as indicated
					0 : default, no boundary condition is applied
					1 : prescribe the value of the turbulent enstrophy, ENZPAR(,1) specifies the enstrophy in s<sup>-2</sup>.
					2 : prescribe the gradient of the turbulent enstrophy, ENZPAR(,1) specifies the gradient of the turbulent enstrophy in s<sup>-2</sup>/m.
					14 : leakage option for turbulent enstrophy, ENZPAR(,1) specifies the leakage factor, α in Γ<sub>loss</sub> = α C<sub>s,collective</sub> n<sub>i</sub> ζ
					15 : sheath loss boundary condition. For now it assumes that BCCON = 14 is used. ENZPAR(,1) specifies the sheath transmission factor corresponding to the particle fluxes dictated by CONPAR(,,1) and ENZPAR(,2) specifies the sheath transmission factor corresponding to the particle fluxes dictated by CONPAR(,,2).
					16 : prescribe the value of the turbulent enstrophy, with a poloidal perturbation taken from the flux tube just inside the domain. zt = ENZPAR(,1) + zt2 - zt2av, where zt2 is the enstrophy in the first cell inside the domain, and zt2av is the average enstrohpy in the flux tube just inside the domain. Intended for core boundaries only.
				""", ''),
   
      'GAMMAI' : ('b2.boundary.parameters', 'real', """
					Adiabatic coefficient multiplying the ion temperature when computing the sound speeds.
				""", '1.0'),
   
      'GAMMAE' : ('b2.boundary.parameters', 'real', """
					Secondary electron emission coefficient.
				""", '0.5'),
   
      'LBNDUSR' : ('b2.boundary.parameters', 'logical', """
					Obsolete.
				""", '.false.'),
   
      'LFEEDBACK' : ('b2.boundary.parameters', 'logical', """
					Indicates whether a feedback scheme is used. Obsolete. Superceded by 'b2stbc_feedback'.
				""", '.false.'),
   
      'NNISO' : ('b2.boundary.parameters', 'integer', """
					Number of dead (or isolated) regions.
				""", '0'),
   
      'NIISO' : ('b2.boundary.parameters', 'real array of size (0:NS-1)', """
					Density of species (is) in (m-3) to impose in isolated regions.
				""", ''),
   
      'TEISO' : ('b2.boundary.parameters', 'real', """
					Electron temperature (in eV) to impose in isolated regions.
				""", '1.0'),
   
      'TIISO' : ('b2.boundary.parameters', 'real', """
					Ion temperature (in eV) to impose in isolated regions.
				""", '1.0'),
   
      'PHIISO' : ('b2.boundary.parameters', 'real', """
					Electric potential (in V) to impose in isolated regions.
				""", '0.0'),
   
      'NXISO1' : ('b2.boundary.parameters', 'integer array of size NNISO', """
					Column number of bottom left corner of the dead region (iiso).
				""", '-2'),
   
      'NXISO2' : ('b2.boundary.parameters', 'integer array of size NNISO', """
					Column number of top right corner of the dead region (iiso).
				""", '-2'),
   
      'NYISO1' : ('b2.boundary.parameters', 'integer array of size NNISO', """
					Row number of bottom left corner of the dead region (iiso).
				""", '-2'),
   
      'NYISO2' : ('b2.boundary.parameters', 'integer array of size NNISO', """
					Row number of top right corner of the dead region (iiso).
				""", '-2'),
   
      'BOUNDARY_FILENAME' : ('b2.boundary.parameters', 'character*256', """
					Name of the next file to use for reading a new /BOUNDARY/ namelist.
				""", 'b2.boundary.parameters'),
   
      'BOUNDARY_TIME_MOD' : ('b2.boundary.parameters', 'real', """
					When the B2.5 run simulation time, in seconds, modulo(BOUNDARY_TIME_MOD), reaches or exceeds BOUNDARY_TIME_SWITCH, reads the new namelist from BOUNDARY_FILENAME. Also switches to the new namelist as the ELM count (here time/BOUNDARY_TIME_MOD) changes. Only active if BOUNDARY_TIME_MOD is greater than 0.
				""", '0.0'),
   
      'BOUNDARY_TIME_SWITCH' : ('b2.boundary.parameters', 'real', """
					If BOUNDARY_TIME_MOD is greater than 0, time (in seconds) within an ELM cycle at which a new BOUNDARY namelist is read.
					Otherwise, B2.5 simulation time, in seconds, when to read the next BOUNDARY namelist file from BOUNDARY_FILENAME.
					Only active if BOUNDARY_TIME_SWITCH is greater than 0.
				""", '0.0'),
   
      'LCBS' : ('b2.boundary.parameters', 'integer array of size (NBC)', """
					List of core boundary segments, according to their numbering in the current /BOUNDARY/ namelist.
					For cases with closed field lines, the code will attempt to build the array from the topology information available, i.e., it will contain the list of 'South' boundaries forming a closed contour.
					For linear cases, in case a "core" type boundary condition is desired, then LCBS must be specified explicitly.
				""", '0'),
   
      'WRITE_NML_BND' : ('b2.boundary.parameters', 'logical', """
					If .true. (default), writes the content of the namelist to stdout after it has been read.
				""", '.true.'),
    
},

'b2.feedback_save.parameters' : {

      'SAVED_FB_ACTUATOR' : ('b2.feedback_save.parameters', 'real array of size (NFB)', """
					Last value used for the feedback actuator for each feedback.
				""", '0.0'),
   
      'SAVED_FB_PREV' : ('b2.feedback_save.parameters', 'real array of size (NSPECIES)', """
					Last value of the density used for the feedback control for each isonuclear sequence.
				""", '0.0'),
    
},

'b2.feedback_control.parameters' : {

      'VACUUM_COMMUNICATION' : ('b2.feedback_control.parameters', 'integer', """
					If &gt; 0, allows for a	communication of particle fluxes across vacuum regions. This option only applies to neutrals. The density boundary condition is based on the difference between the average pressure and the local pressure.
					Not yet implemented in WG code.
				""", '0'),
   
      'VACUUM_COMMUNICATION_NREG' : ('b2.feedback_control.parameters', 'integer array of size (NVAC)', """
					Number of communicating vacuum regions.
					Not yet implemented in WG code.
				""", '0'),
   
      'VACUUM_COMMUNICATION_METHOD' : ('b2.feedback_control.parameters', 'integer array of size (NVAC)', """
					Option for resorbing the pressure difference.
						1: Try to set a flux. Corr = (beta*ave_pressure - pressure)/temp * alpha
						2: Try to set a density based on pressure equality.
					Corr = α * beta * pressure / Ti
					Not yet implemented in WG code.
				""", '0'),
   
      'VACUUM_COMMUNICATION_IY' : ('b2.feedback_control.parameters', 'integer array of size (NVACREG,NVAC)', """
					Radial index of the ring on which the neutral pressure is computed for region IREG.
					Not yet implemented in WG code.
				""", '-2'),
   
      'VACUUM_COMMUNICATION_IX1' : ('b2.feedback_control.parameters', 'integer array of size (NVACREG,NVAC)', """
					Poloidal lower bound of the range over which the neutral pressure is computed for region IREG.
					Not yet implemented in WG code.
				""", '-2'),
   
      'VACUUM_COMMUNICATION_IX2' : ('b2.feedback_control.parameters', 'integer array of size (NVACREG,NVAC)', """
					Poloidal upper bound of the range over which the neutral pressure is computed for region IREG.
					Not yet implemented in WG code.
				""", '-2'),
   
      'VACUUM_COMMUNICATION_ALPHA' : ('b2.feedback_control.parameters', 'real array of size (0:NSPECIES-1,NVAC)', """
					Parameter for setting the pressure correction. See above.
					Not yet implemented in WG code.
				""", '0.0'),
   
      'VACUUM_COMMUNICATION_BETA' : ('b2.feedback_control.parameters', 'real array of size (0:NSPECIES-1,NVAC)', """
					Parameter for setting the pressure correction. See above.
					Not yet implemented in WG code.
				""", '1.0'),
   
      'NFB' : ('b2.feedback_control.parameters', 'integer', """
					Number of feedback schemes applied.
				""", '0'),
   
      'FB_TYPE' : ('b2.feedback_control.parameters', 'integer array of size (NFB)', """
					Choice of quantity on which the feedback is computed:
						0: no action
						1: local species density (averaged over cells/faces defined with fb_reg or fb_reg_par). Summed over all charge states of that species.
						2: local electron density (averaged over cells/faces defined with fb_reg or fb_reg_par).
						3: outer midplane separatrix electron density.
						4: total particle content for that species over cells/faces defined with fb_reg or fb_reg_par.
						5: total ion content for that species (not including neutrals) over cells/faces defined with fb_reg or fb_reg_par.
						6: neutral particle flux through the core boundary (for now only for kinetic neutral cases).
						7: relative average concentration of this species at the separatrix.
						8: relative average concentration of this species over cells/faces defined with fb_reg or fb_reg_par.
						9: inner midplane separatrix electron density.
						10: boundary fna (similar to 'b2stbc_fnaycore' but for any boundary)
						11: boundary fhe (similar to 'b2stbc_fheycore' but for any boundary)
						12: boundary fhi (similar to 'b2stbc_fhiycore' but for any boundary)
						13: boundary fch (similar to 'b2stbc_fchycore' but for any boundary)
						14: total particle content of that species on the entire domain (similar to 'b2stbc_ndes' and 'b2stbc_ndes_sol' but actuator applied to any boundary)
						15: Volumetric recombination (only for kinetic neutral cases) (similar to 'b2stbc_volrec_sol' but actuator applied to any boundary)
						16: Pedestal electron density (similar to 'b2stbc_nepedm_sol' but actuator applied to any boundary)
						17: Density of ions at the outer midplane separatrix
						18: Integrated electron cooling over the entire domain
						20: Neutral pressure of this sequence. It is necessary to set PFR_CVS and NPFR_CVS in b2.user.parameters to specify the control volumes used to compute the neutral pressure.
						21: Total radiation losses over the entire domain
						22: Average density of this species along the separatrix
						23: Peak heat flux density along a specific boundary. The boundary index should be defined by FB_REG_PAR. By default it equals 2, which usually maps to the outer target.
						24: Peak electron temperature along a specific boundary. The boundary index should be defined by FB_REG_PAR. By default it equals 2, which usually maps to the outer target.
						25: Peak electron density along a specific boundary. The boundary index should be defined by FB_REG_PAR. By default it equals 2, which usually maps to the outer target.
						26: Peak saturation current along a specific boundary. The boundary index should be defined by FB_REG_PAR. By default it equals 2, which usually maps to the outer target.
						27: Total particle content in the SOL and PFR for the isonuclear sequence (including Eirene neutrals).
				""", '0'),
   
      'FB_RESCALE' : ('b2.feedback_control.parameters', 'integer array of size (NFB)', """
					Option for computing the new fedback quantity.
						0: no action
						1: rescale slowed by fb_alpha
						2: pure rescale
						3: rescaling slowed by tanh_log
						4: rescale done according to SOLPS4 formula
							The target waveform for the particle content is
							N = C + V*(time-T)
							and the current puffing rate S is adjusted
							S --&gt; max(0, min(X,S + D)), where D = F*((N - &lt;N&gt;)/dt + (&lt;N&gt;_prev - &lt;N&gt;)/dt_prev)
						5: rescale done according to SOLPS4 formula: N = C*exp((time-T)*V)
						6: rescale slowed by fb_alpha (SOLPS4 style)
						7: If fb_target/fb_current &lt; (1-fb_const) or &gt; (1+fb_const), the rescaling coincides with FB_RESCALE.eq.3. Otherwise no rescaling is applied.
				""", '0'),
   
      'FB_ACTUATOR' : ('b2.feedback_control.parameters', 'integer array of size (NFB)', """
					Choice for the actuator used for the feedback.
					0: no action
					1: gas puff via boundary condition
					2: rescale na [[Experimental!! Does not guarantee stable code runs]]
					3: charged species particle flux BC
					4: electron heat flux BC
					5: ion heat flux BC
					6: current BC
					7: density BC
				""", '0'),
   
      'FB_TARGET' : ('b2.feedback_control.parameters', 'real array of size (NFB)', """
					Sets the target value of the quantity associated with feedback (IFB) for the feedback scheme defined by FB_TYPE(IFB).
				""", '0.0'),
   
      'FB_TYPE_INVERSE' : ('b2.feedback_control.parameters', 'logical array of size (NFB)', """
					If FB_TYPE_INVERSE(IFB) is .true., then the feedback is done on the inverse of the quantity provided as FB_TARGET(IFB).
					Can be used in conjunction with FB_TYPE=26.
				""", '.false.'),
   
      'FB_SPECIES' : ('b2.feedback_control.parameters', 'integer array of size (NFB)', """
					Specifies the species used to calculate the controlled variable and to which the actuator is applied. It follows the B2.5 plasma species enumeration. In general, controlled quantities are calculated on the whole isonuclear sequence to which fb_species(ifb) belongs. Then if fb_actuator.eq.1, it is applied to neutral species through gas puff; if fb_actuator.eq.2, it is applied to the ionized species only; if fb_actuator.eq.3 it is applied only to fb_species. For fb_type.eq.6 and fb_actuator.eq.3 then it is also applied to all ionized species (as in the old feedback treatment). Overridden by switch 'b2stbc_isfeedback'.
				""", '0'),
   
      'FB_TIME' : ('b2.feedback_control.parameters', 'real array of size (NFB)', """
					Sets the time of reference (in s) for the feedback (IFB).
				""", '0.0'),
   
      'FB_ALPHA' : ('b2.feedback_control.parameters', 'real array of size (NFB)', """
					Factor by which the rescaling is slowed. Rescaling factor is :
					Option 1: (1 + alpha*target/current) / (1 + alpha)
					Option 3: 2**(tanh(log(x)/beta)*log(alpha)/log(2))
					Options 4 and 5: Corresponds to parameter F
					Can be overridden by switches 'b2stbc_nesepm_alpha', 'b2stbc_fnaycore_alpha', 'b2stbc_fheycore_alpha', 'b2stbc_fhiycore_alpha', 'b2stbc_fchycore_alpha', 'b2stbc_volrec_alpha'.
				""", '0.001'),
   
      'FB_BETA' : ('b2.feedback_control.parameters', 'real array of size (NFB)', """
					Factor by which the rescaling is slowed. See above. Options 4 and 5: Corresponds to parameter V (ffb_rtvn). Cna be overridden by 'b2stbc_volrec_beta'.
				""", '1.0'),
   
      'FB_CONST' : ('b2.feedback_control.parameters', 'real array of size (NFB)', """
					Options 4 and 5: Corresponds to parameter C. If negative, C is computed as the initial total particle content of the sequence.
				""", '0.0'),
   
      'FB_IB' : ('b2.feedback_control.parameters', 'integer array of size (NFB)', """
					Index of boundary condition through which the feedback is being applied.
				""", '-1'),
   
      'FB_ISTRA' : ('b2.feedback_control.parameters', 'integer array of size (NFB)', """
					Eirene strata where the gas puff feedback is applied. Overridden by switch 'eirene_nesepm_istra'.
				""", '0'),
   
      'FB_PUFF_MIN' : ('b2.feedback_control.parameters', 'real array of size (NFB)', """
					Minimum gas puff being applied. Can be overrdidden by switch 'b2stbc_nesepm_minpuff'.
				""", '0.0'),
   
      'FB_PUFF_MAX' : ('b2.feedback_control.parameters', 'real array of size (NFB)', """
					Maximum gas puff being applied. Can be overrdidden by switch 'b2stbc_nesepm_maxpuff'.
				""", '0.0'),
   
      'FB_OVERSHOOT' : ('b2.feedback_control.parameters', 'real array of size (NFB)', """
					If the density is larger than target*overshoot, the gas puff is turned off. Can be overridden by switch 'b2stbc_nesepm_overshoot', 'b2stbc_volrec_overshoot'.
				""", '0.0'),
   
      'FB_REGP' : ('b2.feedback_control.parameters', 'integer array of size (NFB,2)', """
					Pointing for each feedback to the first index in FB_REG, and its number of CVs or faces.
				""", '0'),
   
      'FB_REG' : ('b2.feedback_control.parameters', 'integer array of size (nMxFbReg)', """
					Listing for each feedback the cells or faces where controlled quantity is calculated. If different feedbacks use the same domain then this can be defined only ones and simply point to it twice with fb_regP. nMxFbReg is a maximum length set in b2us_feedback.
				""", '0'),
   
      'FB_REG_PAR' : ('b2.feedback_control.parameters', 'integer array of size (NFB,2)', """
					If the two FB_REG and FB_REGP are not defined, then the code will look for this array.
					For fb_type 6-10-11-12-13-23-24-25-26, fb_reg_par(ifb,:) indicates the starting (iFb,1) and ending (iFb,2) face region label over which the controlled quantity is calculated.
					For fb_type 1-2-4-5-8, fb_reg_par(ifb,:) indicates the starting (iFb,1) and ending (iFb,2) volume region label over which the controlled quantity is calculated.
				""", '0'),
    
},

'b2.sources.profile' : {

      'NSDATA' : ('b2.sources.profile', 'integer array of size (NKIND_DATA,NKIND_SOURCE,0:NS)', """
					Number of points over which the source profile of (kind_data,kind_source,is) is defined. Should not exceed NY+2.
						If KIND_DATA=1, the data is expressed as a profile in physical distance from the separatrix (in metres) along the outer midplane.
						The user can change this default reference location by use of the 'set_transport_i[xy]ref' switches.
						If KIND_DATA=2, the data is expressed as a profile in flux distance from the separatrix (not yet available).
				""", '0'),
   
      'SDATA' : ('b2.sources.profile', 'real data of size (2,NY+2,NKIND_SOURCE,0:NS)', """
					For (i,ir,ik,is) in (1:2,1:NY+2,1:NKIND_SOURCE,0:NS),
					SDATA(1,ir,:,:) contains the radial location of the profile point (ir).
					SDATA(2,ir,:,:) contains the source profile value at point (ir).
					KIND_SOURCE=1 means particle source of species (is) (in particles/s/m3)
					KIND_SOURCE=2 means parallel momentum source for species (is) (in N/m3)
					KIND_SOURCE=3 means electron heat source (in Watts/m3)
					KIND_SOURCE=4 means ion heat source (in Watts/m3)
					KIND_SOURCE=5 means electric charge source (in Amperes/m3)
					KIND_SOURCE=6 means non-ambipolar electron particle source (in e/s/m3)
				""", '0.0'),
   
      'NXDATA' : ('b2.sources.profile', 'integer array of size (NKIND_DATA,NKIND_SOURCE,0:NS)', """
					Number of points over which the axial profile of (kind_data,kind_source,is) is defined. Should not exceed NX+2. Defaults to 0.
					If KIND_DATA=1, the data is expressed as a profile in physical distance, here connection length, rescaled from 0.0 to 1.0.
					For closed field lines, the reference location for the zero of distance is set by use of the 'set_transport_i[xy]ref' switches.
					If KIND_DATA=2, the data is expressed as a profile in (ix) cell index, again normalized from 0.0 to 1.0 to match the [0:nx-1] interval.
				""", ''),
   
      'XDATA' : ('b2.sources.profile', 'real data of size (2,NY+2,NKIND_SOURCE,0:NS)', """
					Multiplier to the poloidal source profile in the axial direction. Same convention for KIND_SOURCE as above.
				""", '1.0'),
   
      'DIVHEAT' : ('b2.sources.profile', 'real', """
					Additional divertor ion heat source (in Watts/m<sup>3</sup>)
				""", '0.0'),
   
      'SOURCES_FILENAME' : ('b2.sources.profile', 'character*256', """
					Name of the next file to use for reading a new /PROFILE/ namelist. Quantities not present in the new file will be inherited from the old one.
				""", 'b2.sources.profile'),
   
      'SOURCES_TIME_MOD' : ('b2.sources.profile', 'real', """
					When the B2.5 run simulation time, in seconds, modulo(SOURCES_TIME_MOD), reaches or exceeds SOURCES_TIME_SWITCH, reads the new namelist from SOURCES_FILENAME. Also switches to the new namelist if the ELM count (here time/SOURCES_TIME_MOD) changes. Only active if SOURCES_TIME_MOD is greater than 0.
				""", '0.0'),
   
      'SOURCES_TIME_SWITCH' : ('b2.sources.profile', 'real', """
					If SOURCES_TIME_MOD is greater than 0, time (in seconds) within an ELM cycle at which a new PROFILE namelist is read.
					Otherwise, B2.5 simulation time, in seconds, when to read the next PROFILE namelist file from SOURCES_FILENAME.
					Only active if SOURCES_TIME_SWITCH is greater than 0.
				""", '0.0'),
    
},

'b2.transport.inputfile' : {

      'NDATA' : ('b2.transport.inputfile', 'integer array of size (NKIND_DATA,NCOEF,0:NS)', """
					Number of points over which the source profile of (kind_data,kind_coef,is) is defined. Should not exceed NY+2.
					If KIND_DATA=1, the data is expressed as a profiles in physical distance from the separatrix (in metres).
					If KIND_DATA=2, the data is expressed as a profile in flux distance from the separatrix (not yet available).
				""", '0'),
   
      'TDATA' : ('b2.transport.inputfile', 'real data of size (3,NY+2,NKIND_COEFF,0:NS)', """
					For (i,ir,ik,is) in (1:3,1:NY+2,1:NKIND_COEFF,0:NS), TDATA(1,ir,:,:) contains the radial location of the profile point (ir).
					By default, these are measured at the outer midplane, as distance to the separatrix in metres. The user can change this by setting the 'set_transport_i[xy]ref' switches to choose a different location for the distance reference.
					TDATA(2,ir,:,:) contains the transport profile value at point (ir).
					TDATA(3,ir,:,:) contains the ELM transport profile value at point (ir).
					KIND_COEFF=1 means density-driven particle diffusivity for species (is)
					KIND_COEFF=2 means pressure-driven particle diffusivity for species (is)
					KIND_COEFF=3 means ion heat diffusivity for species (is)
					KIND_COEFF=4 means electron heat diffusivity
					KIND_COEFF=5 means poloidal pinch velocity for species (is)
					KIND_COEFF=6 means radial pinch velocity for species (is)
					KIND_COEFF=7 means viscosity for species (is)
					KIND_COEFF=8 means field-driven radial current conductivity
					KIND_COEFF=9 means temperature-driven radial current conductivity
				""", '0.0'),
   
      'ADDSPEC' : ('b2.transport.inputfile', 'integer array of size (NS,NKIND_COEFF,0:NS)', """
					If ADDSPEC(is,ikind,spec).ge.0, then the transport coefficient profile of type (ikind) from species (spec) is also used for species with index ADDSPEC(is,ikind,spec).
				""", '-5'),
   
      'TRANSPORT_IP_FILENAME' : ('b2.transport.inputfile', 'character*256', """
					Name of the next file to use for reading a new /TRANSPORT/ namelist.
				""", 'b2.transport.inputfile'),
   
      'TRANSPORT_IP_TIME_MOD' : ('b2.transport.inputfile', 'real', """
					When the B2.5 run simulation time, in seconds, modulo(TRANSPORT_IP_TIME_MOD), reaches or exceeds TRANSPORT_IP_TIME_SWITCH, reads the new namelist from TRANSPORT_IP_FILENAME. Also switches to the new namelist if the ELM count (here time/TRANSPORT_IP_TIME_MOD) changes. Only active if TRANSPORT_IP_TIME_MOD is greater than 0.
				""", '0.0'),
   
      'TRANSPORT_IP_TIME_SWITCH' : ('b2.transport.inputfile', 'real', """
					If TRANSPORT_IP_TIME_MOD is greater than 0, time (in seconds) within an ELM cycle at which a new TRANSPORT namelist is read.
					Otherwise, B2.5 simulation time, in seconds, when to read the next TRANSPORT namelist file from TRANSPORT_IP_FILENAME.
					Only active if TRANSPORT_IP_TIME_SWITCH is greater than 0.
				""", '0.0'),
   
      'REGION_FLAGS' : ('b2.transport.inputfile', 'logical array of size (NREG,NKIND_COEFF)', """
					If region_flags(ireg,ikind) is .true. (default), then the transport parameters profiles for region (ireg) and kind (ikind) are used.
				""", '.true.'),
   
      'NO_PFLUX' : ('b2.transport.inputfile', 'logical', """
					If .true., transport coefficients profiles are not implemented in the private flux regions.
				""", '.false.'),
   
      'NO_DIV' : ('b2.transport.inputfile', 'logical', """
					If .true., transport coefficients profiles are not implemented in the divertor regions.
				""", '.false.'),
   
      'POLOIDAL_SCALING' : ('b2.transport.inputfile', 'logical array of size (10)', """
					If .true., then the transport coefficients profiles from the current b2.transport.inputfile are increased by a factor of 1.0+Gaussian where Gaussian is a Gaussian profile in the poloidal direction of amplitude SCALING_STRENGTH extending from SCALING_IX_BEGIN to SCALING_IX_END inclusively. The profile has a decay length of SCALING_WIDTH (in units of the number of poloidal cells).
				""", '.false.'),
   
      'SCALING_STRENGTH' : ('b2.transport.inputfile', 'real array of size 10', """
					See above.
				""", '0'),
   
      'SCALING_WIDTH' : ('b2.transport.inputfile', 'real array of size 10', """
					See above. Defaults to about 1/3 of the interval over which the scaling is to be done.
				""", '1/3 interval'),
   
      'SCALING_IX_BEGIN' : ('b2.transport.inputfile', 'integer array of size 10', """
					See above.
				""", '-2'),
   
      'SCALING_IX_END' : ('b2.transport.inputfile', 'integer array of size 10', """
					See above.
				""", '-2'),
   
      'ELM_TIME_BEGIN' : ('b2.transport.inputfile', 'real', """
					Time (in seconds) modulo ELM_TIME_PERIOD at which the ELM phase begins and the ELM data must be used.
				""", '0.0'),
   
      'ELM_TIME_END' : ('b2.transport.inputfile', 'real', """
					Time (in seconds) modulo ELM_TIME_PERIOD at which the ELM phase ends and the ELM data is no longer used.
				""", '0.0'),
   
      'ELM_TIME_PERIOD' : ('b2.transport.inputfile', 'real', """
					Indicates the real frequency of simulated ELMs. See above for usage.
					If zero, no ELM profiles are used.
				""", '0.0'),
   
      'ELM_IX_BEGIN' : ('b2.transport.inputfile', 'integer', """
					Poloidal position at which the ELM profile starts to be applied.
				""", '-2'),
   
      'ELM_IX_END' : ('b2.transport.inputfile', 'integer', """
					Poloidal position at which the ELM profile ends being applied.
				""", '-2'),
    
},

'b2.neutrals_save.parameters' : {

      'SAVED_VOLREC' : ('b2.neutrals_save.parameters', 'real array of size (NSTRAT)', """
					Contains the last value of the strength of volume recombination sources from stratum (istra).
				""", '0.0'),
    
},

'b2.numerics.parameters' : {

      'DTCO' : ('b2.numerics.parameters', 'real array of size (0:NS-1,0:NREG)', """
					Multiplier to the time used in solving the continuity equation of species (is) in region (ireg).
				""", '1.0'),
   
      'DTMO' : ('b2.numerics.parameters', 'real array of size (0:NS-1,0:NREG)', """
					Multiplier to the time used in solving the parallel momentum equation of species (is) in region (ireg).
				""", '1.0'),
   
      'DTEE' : ('b2.numerics.parameters', 'real array of size (0:NREG)', """
					Multiplier to the time used in solving the electron heat equation in region (ireg).
				""", '1.0'),
   
      'DTEI' : ('b2.numerics.parameters', 'real array of size (0:NREG)', """
					Multiplier to the time used in solving the ion heat equation in region (ireg).
				""", '1.0'),
   
      'DTEN' : ('b2.numerics.parameters', 'real array of size (0:NREG)', """
					Multiplier to the time used in solving the fluid neutral heat equation in region (ireg).
				""", '1.0'),
   
      'DTFTS' : ('b2.numerics.parameters', 'integer array of size (DEF_NYD)', """
					List of flux tube indices for which individual timestep multipliers can be applied.
				""", '0'),
   
      'DTCO_FT' : ('b2.numerics.parameters', 'real array of size (DEF_NYD)', """
					Individual timestep multiplier to all continuity equations applied in the corresponding flux tube from the DTFTS list.
					Must be positive.
				""", '1.0'),
   
      'DTMO_FT' : ('b2.numerics.parameters', 'real array of size (DEF_NYD)', """
					Individual timestep multiplier to all parallel momentum equations applied in the corresponding flux tube from the DTFTS list.
					Must be positive.
				""", '1.0'),
   
      'DTEE_FT' : ('b2.numerics.parameters', 'real array of size (DEF_NYD)', """
					Individual timestep multiplier to the electron heat equation applied in the corresponding flux tube from the DTFTS list.
					Must be positive.
				""", '1.0'),
   
      'DTEI_FT' : ('b2.numerics.parameters', 'real array of size (DEF_NYD)', """
					Individual timestep multiplier to the ion heat equation applied in the corresponding flux tube from the DTFTS list.
					Must be positive.
				""", '1.0'),
   
      'SOLVECO' : ('b2.numerics.parameters', 'logical array of size (0:NS-1,0:NREG)', """
					Indicates whether the continuity equation for species (is) is to be solved in region (ireg). Subservient to 'no_solve' switch.
				""", '.true.'),
   
      'SOLVEMO' : ('b2.numerics.parameters', 'logical array of size (0:NS-1,0:NREG)', """
					Indicates whether the parallel momentum equation for species (is) is to be solved in region (ireg). Subservient to 'no_solve' switch.
				""", '.true.'),
   
      'SOLVEMT' : ('b2.numerics.parameters', 'logical array of size (0:NREG)', """
					Indicates whether the total parallel momentum equation is to be solved in region (ireg). For the total parallel momentum equation to be solved in a region, all momentum equations in the range defined by 'b2news_nsmin' and 'b2news_nsmax' must have SOLVEMO true in that region. Subservient to 'no_solve' switch.
					It is important to note that the 'b2news_no_solve' switch allows for solving or not all momentum equations together as a whole, along with the total equation.
					Defaults to .true. unless using the time-dependent mode, in which case it is set to .false. and should not be used.
				""", ''),
   
      'SOLVEPO' : ('b2.numerics.parameters', 'logical array of size (0:NREG)', """
					Indicates whether the potential energy equation is to be solved in region (ireg). Subservient to 'no_solve' switch.
				""", '.true.'),
   
      'SOLVEEE' : ('b2.numerics.parameters', 'logical array of size (0:NREG)', """
					Indicates whether the electron energy equation is to be solved in region (ireg). Subservient to 'no_solve' switch.
				""", '.true.'),
   
      'SOLVEEI' : ('b2.numerics.parameters', 'logical array of size (0:NREG)', """
					Indicates whether the ion energy equation is to be solved in region (ireg). Subservient to 'no_solve' switch.
				""", '.true.'),
   
      'SOLVEEN' : ('b2.numerics.parameters', 'logical array of size (0:NREG)', """
					Indicates whether the fluid neutral energy equation is to be solved in region (ireg). Subservient to 'no_solve' switch.
				""", '.true.'),
   
      'SOLVEET' : ('b2.numerics.parameters', 'logical array of size (0:NREG)', """
					Indicates whether the total energy equation is to be solved in region (ireg). For the equation to be solved in region (ireg), both SOLVEEE and SOLVEEI must be true in that region. Subservient to 'no_solve' switch.
					It is important to note that the 'b2news_no_solve' switch allows to solve or not to solve the electron and ion heat equations together with the total energy equation, as a group.
					Defaults to .true. unless using the time-dependent mode, in which case it is set to .false. and should not be used.
				""", ''),
   
      'SOLVEKT' : ('b2.numerics.parameters', 'logical array of size (0:NREG)', """
					Indicates whether the ExB turbulent kinetic energy equation is to be solved in region (ireg). Subservient to 'no_solve' switch.
				""", '.true.'),
   
      'SOLVEZT' : ('b2.numerics.parameters', 'logical array of size (0:NREG)', """
					Indicates whether the ExB turbulent enstrophy equation is to be solved in region (ireg). Subservient to 'no_solve' switch.
				""", '.true.'),
   
      'TIME_FACTOR_REQUIRED' : ('b2.numerics.parameters', 'real', """
					Minimum time scale of evolution allowed for all equations. Only active is 'b2srsm_enable' is set to 1.
				""", '0.1'),
   
      'CORE_DT_SUPPRESSION' : ('b2.numerics.parameters', 'real', """
					De-multiplier to the timestep in the core. Only active if less than 1. Should be larger than 0. Applies fully to the innermost core ring of cells (IY .eq. -1). See CORE_DT_FACTOR for further use.
				""", '1.0'),
   
      'CORE_DT_FACTOR' : ('b2.numerics.parameters', 'real', """
					Multiplier to the timestep in the core. Only active is less than 1. Should be larger than 0. Multiplies each successive core ring of cells (increasing IY) by CORE_DT_FACTOR, until the local time step multiplier is equal to 1.
				""", '1.0'),
   
      'CORR_CORE_DN' : ('b2.numerics.parameters', 'real array of size (0:NS-1)', """
					Pressure correction speed-up parameter α_a, acting on the density contribution from species a. Will apply in the core region, except for the nrings outer surfaces. See nrings_for_no_speedup_averaging for details.
					See Pressure_correction_speed-up.pdf in $SOLPSTOP/doc for a full description. Should be roughly equal to corr_core_dt below. Does not apply to neutral species.
				""", '1.0'),
   
      'CORR_CORE_DT' : ('b2.numerics.parameters', 'real', """
					Pressure correction speed-up parameter α_T, acting on the temperature contributions. Will apply in the core region, except for the nrings outer surfaces. See nrings_for_no_speedup_averaging for details.
					See Pressure_correction_speed-up.pdf in $SOLPSTOP/doc for a full description. Should be roughly equal to corr_core_dn above.
				""", '1.0'),
   
      'SNA_CORR' : ('b2.numerics.parameters', 'real array of size (1:NSPECIES)', """
					Multiplier to the neutral source differential between puffing (plus sputtering plus core boundary flux plus any external sources) and pumping, which is further added to the ionization source for code speed-up. One multiplier must be provided per isonuclear sequence. Such settings might be relevant for e.g. a mixture of main ion and trace impurity.
					See E. Kaveeva et al., Nucl. Fusion 58 (2018) 126018 for details and keep in mind that in that paper the scheme was described in its original species-unresolved form.
				""", '0.0'),
   
      'TAUMAX' : ('b2.numerics.parameters', 'real array of size (1:NSPECIES)', """
					Maximum allowed fraction of ionization source for a given isonuclear sequence from its neutral state (coming from Eirene) to be added or subtracted to the real Eirene source in the method of effective sources for code speed-up.
				""", '0.05'),
   
      'DO_SNA_CORR_CORE' : ('b2.numerics.parameters', 'logical array of size (1:NSPECIES)', """
					Parameter which controls exclusion/inclusion of confined region from/in the method of effective sources for code speed-up for each isonuclear sequence. If .true., then the flux through the core boundary of that species is taken into account during the source correction computation, and the source correction is applied on closed flux surfaces (default behavior). If .false., then the particle imbalance is computed as puffing plus sputtering plus any external sources minus pumping without account of the flux through the core boundary, and no source correction is applied on closed surfaces (such a setting might be helpful if the core flux is much bigger than the puffing rate and the core is isolated from the SOL by a strong transport barrier).
				""", '.true.'),
   
      'NUMERICS_FILENAME' : ('b2.numerics.parameters', 'character*256', """
					Name of the next file to use for reading a new /NUMERICS/ namelist.
				""", 'b2.numerics.namelist'),
   
      'NUMERICS_TIME_MOD' : ('b2.numerics.parameters', 'real', """
					When the B2.5 run simulation time, in seconds, modulo(NUMERICS_TIME_MOD), reaches or exceeds NUMERICS_TIME_SWITCH, reads the new namelist from NUMERICS_FILENAME. Also switches to the new namelist as the ELM count (here time/NUMERICS_TIME_MOD) changes. Only active if NUMERICS_TIME_MOD is greater than 0.
				""", '0.0'),
   
      'NUMERICS_TIME_SWITCH' : ('b2.numerics.parameters', 'real', """
					If NUMERICS_TIME_MOD is greater than 0, time (in seconds) within an ELM cycle at which a new NUMERICS namelist is read.
					Otherwise, B2.5 simulation time, in seconds, when to read the next NUMERICS namelist file from NUMERICS_FILENAME.
					Only active if NUMERICS_TIME_SWITCH is greater than 0.
				""", '0.0'),
   
      'WRITE_NML_NUM' : ('b2.numerics.parameters', 'logical', """
					If .true. (default), writes the content of the namelist to stdout after it has been read.
				""", '.true.'),
   
      'ADD_TE_CORR_TO_PO' : ('b2.numerics.parameters', 'logical array of size (0:NREG)', """
					If .true. (default), adds dte(ix,iy)/qe to the potential correction after the internal energy balance equations are solved, where dte(ix,iy) is the electron temperature correction on the time step. Individually set for each region index.
				""", '.true.'),
    
},

'b2.transport_models_save.parameters' : {

      'ETA_HCE_MULT' : ('b2.transport_models_save.parameters', 'real array of size (-1:NY)', """
					Used by the user specified set_transport_eta transport model. See code for details.
				""", '1.0'),
    
},

'b2.transport.parameters' : {

      'FLAG_DNA' : ('', 'integer', """
					All flags follow:
					FLAG=0: Use model from b2ah.dat and b2mn.dat. Default.
					FLAG=1: Constant, value set to PARM.
					FLAG=2: 1/N model, multiplied by PARM.
					FLAG=3: Bohm model, multiplied by PARM.
					FLAG=4: flux-scaled model, multiplied by PARM.
				""", ''),
   
      'FLAG_DPA' : ('', 'integer', """
					All flags follow:
					FLAG=0: Use model from b2ah.dat and b2mn.dat. Default.
					FLAG=1: Constant, value set to PARM.
					FLAG=2: 1/N model, multiplied by PARM.
					FLAG=3: Bohm model, multiplied by PARM.
					FLAG=4: flux-scaled model, multiplied by PARM.
				""", ''),
   
      'FLAG_VLA' : ('', 'integer', """
					All flags follow:
					FLAG=0: Use model from b2ah.dat and b2mn.dat. Default.
					FLAG=1: Constant, value set to PARM.
					FLAG=2: 1/N model, multiplied by PARM.
					FLAG=3: Bohm model, multiplied by PARM.
					FLAG=4: flux-scaled model, multiplied by PARM.
				""", ''),
   
      'FLAG_VSA' : ('', 'integer', """
					All flags follow:
					FLAG=0: Use model from b2ah.dat and b2mn.dat. Default.
					FLAG=1: Constant, value set to PARM.
					FLAG=2: 1/N model, multiplied by PARM.
					FLAG=3: Bohm model, multiplied by PARM.
					FLAG=4: flux-scaled model, multiplied by PARM.
				""", ''),
   
      'FLAG_HCI' : ('', 'integer', """
					All flags follow:
					FLAG=0: Use model from b2ah.dat and b2mn.dat. Default.
					FLAG=1: Constant, value set to PARM.
					FLAG=2: 1/N model, multiplied by PARM.
					FLAG=3: Bohm model, multiplied by PARM.
					FLAG=4: flux-scaled model, multiplied by PARM.
				""", ''),
   
      'FLAG_HCE' : ('', 'integer', """
					All flags follow:
					FLAG=0: Use model from b2ah.dat and b2mn.dat. Default.
					FLAG=1: Constant, value set to PARM.
					FLAG=2: 1/N model, multiplied by PARM.
					FLAG=3: Bohm model, multiplied by PARM.
					FLAG=4: flux-scaled model, multiplied by PARM.
				""", ''),
   
      'FLAG_SIG' : ('', 'integer', """
					All flags follow:
					FLAG=0: Use model from b2ah.dat and b2mn.dat. Default.
					FLAG=1: Constant, value set to PARM.
					FLAG=2: 1/N model, multiplied by PARM.
					FLAG=3: Bohm model, multiplied by PARM.
					FLAG=4: flux-scaled model, multiplied by PARM.
				""", ''),
   
      'FLAG_ALF' : ('', 'integer', """
					All flags follow:
					FLAG=0: Use model from b2ah.dat and b2mn.dat. Default.
					FLAG=1: Constant, value set to PARM.
					FLAG=2: 1/N model, multiplied by PARM.
					FLAG=3: Bohm model, multiplied by PARM.
					FLAG=4: flux-scaled model, multiplied by PARM.
				""", ''),
   
      'CFLME' : ('', 'real', """
					For all flux limit multipliers, setting them to zero turns off the corresponding flux limiter. Otherwise, the multipliers must be positive.
				""", 'value inherited from b2ah.dat (or b2mn.dat if specified in b2cmpt block)'),
   
      'CFLMI' : ('', 'real', """
					For all flux limit multipliers, setting them to zero turns off the corresponding flux limiter. Otherwise, the multipliers must be positive.
				""", 'value inherited from b2ah.dat (or b2mn.dat if specified in b2cmpt block)'),
   
      'CFLMV' : ('', 'real', """
					For all flux limit multipliers, setting them to zero turns off the corresponding flux limiter. Otherwise, the multipliers must be positive.
				""", 'value inherited from b2ah.dat (or b2mn.dat if specified in b2cmpt block)'),
   
      'CFLAL' : ('', 'real', """
					For all flux limit multipliers, setting them to zero turns off the corresponding flux limiter. Otherwise, the multipliers must be positive.
				""", 'value inherited from b2ah.dat (or b2mn.dat if specified in b2cmpt block)'),
   
      'CFLAB' : ('', 'real', """
					For all flux limit multipliers, setting them to zero turns off the corresponding flux limiter. Otherwise, the multipliers must be positive.
				""", 'value inherited from b2ah.dat (or b2mn.dat if specified in b2cmpt block)'),
   
      'VOUT_CNV' : ('', 'real array of size (0:NS-1)', """
					The four *_CNV parameters are only activated if 'b2tqna_user_transport' is set to '6'.
				""", '0.0'),
   
      'PW0_CNV' : ('', 'real array of size (0:NS-1)', """
					The four *_CNV parameters are only activated if 'b2tqna_user_transport' is set to '6'.
				""", '1.0'),
   
      'PW1_CNV' : ('', 'real array of size (0:NS-1)', """
					The four *_CNV parameters are only activated if 'b2tqna_user_transport' is set to '6'.
				""", '5.0'),
   
      'PW2_CNV' : ('', 'real array of size (0:NS-1)', """
					The four *_CNV parameters are only activated if 'b2tqna_user_transport' is set to '6'.
				""", '2.0'),
   
      'PARM_DNA' : ('b2.transport.parameters', 'real array of size (0:NS-1)', """
					Parameter for the density-driven particle diffusion coefficient for species (is).
				""", ''),
   
      'PARM_DPA' : ('b2.transport.parameters', 'real array of size (0:NS-1)', """
					Parameter for the pressure-driven particle diffusion coefficient for species (is).
				""", ''),
   
      'PARM_VLA' : ('b2.transport.parameters', 'real array of size (0:NS-1)', """
					Parameter for the anomalous radial pinch velocity for species (is).
				""", ''),
   
      'PARM_VSA' : ('b2.transport.parameters', 'real array of size (0:NS-1)', """
					Parameter for the viscosity for species (is).
				""", ''),
   
      'PARM_HCI' : ('b2.transport.parameters', 'real array of size (0:NS-1)', """
					Parameter for the heat diffusivity coefficient for species (is).
				""", ''),
   
      'PARM_HCE' : ('b2.transport.parameters', 'real', """
					Parameter for the electron heat diffusivity coefficient.
				""", ''),
   
      'PARM_SIG' : ('b2.transport.parameters', 'real', """
					Parameter for the anomalous radial field-driven current conductivity.
				""", ''),
   
      'PARM_ALF' : ('b2.transport.parameters', 'real', """
					Parameter for the anomalous radial temperature-driven current conductivity.
				""", ''),
   
      'TRANSPORT_FILENAME' : ('b2.transport.parameters', 'character*256', """
					Name of the next file to use for reading a new /TRANSPORT/ namelist.
				""", 'b2.transport.parameters'),
   
      'TRANSPORT_TIME_MOD' : ('b2.transport.parameters', 'real', """
					When the B2.5 run simulation time, in seconds, modulo(TRANSPORT_TIME_MOD), reaches or exceeds TRANSPORT_TIME_SWITCH, reads the new namelist from TRANSPORT_FILENAME. Also switches to the new namelist if the ELM count (here time/TRANSPORT_TIME_MOD) changes. Only active if TRANSPORT_TIME_MOD is greater than 0.
				""", '0.0'),
   
      'TRANSPORT_TIME_SWITCH' : ('b2.transport.parameters', 'real', """
					If TRANSPORT_TIME_MOD is greater than 0, time (in seconds) within an ELM cycle at which a new TRANSPORT namelist is read.
					Otherwise, B2.5 simulation time, in seconds, when to read the next TRANSPORT namelist file from TRANSPORT_FILENAME.
					Only active if TRANSPORT_TIME_SWITCH is greater than 0.
				""", '0.0'),
   
      'WRITE_NML_TRANSP' : ('b2.transport.parameters', 'logical', """
					If .true. (default), writes the content of the namelist to stdout after it has been read.
				""", '.true.'),
    
},

'b2.user.parameters' : {

      'RZOMP' : ('b2.user.parameters', 'real array of size (2,2)', """
					Coordinates defining a segment. All control volumes intersected by this segment will be part of the outer midplane.
					rzomp(1,1:2) holds the R-coordinates of the first and second point of the segment.
					rzomp(2,1:2) holds the Z-coordinates of the first and second point of the segment.
					Warning! This variable needs always be defined for SOLPS-ITER version 3.2.0 or younger!
				""", '0.0'),
   
      'RZIMP' : ('b2.user.parameters', 'real array of size (2,2)', """
					Coordinates defining a segment. All control volumes intersected by this segment will be part of the inner midplane.
					rzimp(1,1:2) holds the R-coordinates of the first and second point of the segment.
					rzimp(2,1:2) holds the Z-coordinates of the first and second point of the segment.
				""", '0.0'),
   
      'LHETRGTS' : ('b2.user.parameters', 'integer array of size (NLIM)', """
					List of surface indices (EIRENE notation) which are used for calculation of helium enrichment.
				""", 'Eirene recycling target surfaces defined in the LTNS array'),
   
      'LPFRB_I' : ('b2.user.parameters', 'integer', """
					Obsolete. Use PFR_CVS instead.
					B2.5 x-cell index corresponding to the first edge of the bypass between the inner and outer divertor (Western divertor, edge closest to target). If non-positive, counted backwards from the X-point location in the lower PFR, from the inner upper target in the upper PFR, from the lower outer target in the outer SOL, and from the inner upper target in the inner SOL.
				""", '0'),
   
      'LPFRB_O' : ('b2.user.parameters', 'integer', """
					Obsolete. Use PFR_CVS instead.
					B2.5 x-cell index corresponding to the first edge of the bypass between the inner and outer divertor (Eastern divertor, edge closest to target). If non-positive, counted backwards from the outer lower target in the lower PFR, from the lower outer target in the outer SOL, from the upper outer target in the upper PFR, and from the inner upper target in the inner SOL.
				""", '0'),
   
      'LPFRT_I' : ('b2.user.parameters', 'integer', """
					Obsolete. Use PFR_CVS instead.
					B2.5 x-cell index corresponding to the second edge of the bypass between the inner and outer divertor (Western divertor, edge furthest to target). If non-positive, counted backwards from the X-point location in the PFR, from the outer target in the outer SOL for a SN, from the top targets in the SOL for a DN.
				""", '0'),
   
      'LPFRT_O' : ('b2.user.parameters', 'integer', """
					Obsolete. Use PFR_CVS instead.
					B2.5 x-cell index corresponding to the second edge of the bypass between the inner and outer divertor (Eastern divertor, edge furthest to target). If non-positive, counted backwards from the X-point location in the PFR, from the outer target in the outer SOL for a SN, from the top targets in the SOL for a DN.
				""", '0'),
   
      'J_HE_AT' : ('b2.user.parameters', 'integer', """
					Species index of the helium atoms in Eirene. The code attempts to find a match by default.
				""", ''),
   
      'J_NE_AT' : ('b2.user.parameters', 'integer', """
					Species index of the neon atoms in Eirene. The code attempts to find a match by default.
				""", ''),
   
      'J_H_AT' : ('b2.user.parameters', 'integer array of size (3)', """
					Species indices of the hydrogen isotopes in Eirene. If using only one hydrogen species, only the first element needs to be provided. Otherwise the 3 elements correspond to H/D/T. The code attempts to find a match by default.
				""", ''),
   
      'L_H_MOL' : ('b2.user.parameters', 'integer array of size (NMOL,3)', """
					Number of hydrogen isotope nuclei for molecules in Eirene. If using only one hydrogen species, only the first element needs to be provided. Otherwise the 3 elements correspond to H/D/T. The code attempts to find a match by default.
				""", ''),
   
      'FUSION_POWER' : ('b2.user.parameters', 'real', """
					Fusion power occuring in core (including neutrons, in Megawatts).
				""", '0.0'),
   
      'SPMP_HE_TO_D' : ('b2.user.parameters', 'real', """
					Ratio of He to DT pumping speeds (typically, 0.8).
				""", '1.0'),
   
      'LPFRS_PMP' : ('b2.user.parameters', 'integer', """
					Location of the pump. 0 no pump at all (default), 1 - SN of lower DN PFR, 2 - (outer) SOL, 3 - upper DN PFR, 4 - inner SOL for DN
				""", '0'),
   
      'NPFRGRP' : ('b2.user.parameters', 'integer', """
					Actual number of surface groups for PFR flows.
				""", '0'),
   
      'LPFRGRP' : ('b2.user.parameters', 'integer array of size (NLIM)', """
					List of surface segments for PFR flows.
				""", ''),
   
      'IPFRGRP' : ('b2.user.parameters', 'integer array of size (NPFRGRP)', """
					First positions in this list for each group.
				""", '0'),
   
      'JPFRGRP' : ('b2.user.parameters', 'integer array of size (NPFRGRP)', """
					Last positions in this list for each group.
				""", '0'),
   
      'GPFRGRP' : ('b2.user.parameters', 'character*8 array of size (NPFRGRP)', """
					Labels for surface groups for PFR flows.
				""", ' '),
   
      'NNTRGRP' : ('b2.user.parameters', 'integer', """
					Actual number of surface groups for neutral data.
				""", ''),
   
      'LNTRGRP' : ('b2.user.parameters', 'integer array of size (NLIM)', """
					List of surface segments for neutral data.
				""", ''),
   
      'INTRGRP' : ('b2.user.parameters', 'integer array of size (NNTRGRP)', """
					First positions in this list for each group.
				""", ''),
   
      'JNTRGRP' : ('b2.user.parameters', 'integer array of size (NNTRGRP)', """
					Last positions in this list for each group.
				""", ''),
   
      'GNTRGRP' : ('b2.user.parameters', 'character*8 array of size (NNTRGRP)', """
					Labels for the neutral data surface groups.
				""", ''),
   
      'NPFR_CVS' : ('b2.user.parameters', 'integer', """
					Number of control volumes which are written in PFR_CVS.
				""", '0'),
   
      'PFR_CVS' : ('b2.user.parameters', 'integer array of size (100)', """
					List of control volumes over which the average neutral pressure for fb_type.eq.20 is calculated.
				""", '0'),
   
      'SPMP_NOM' : ('b2.user.parameters', 'real', """
					Nominal pumping speed.
				""", '0.0'),
   
      'TE_DET_THRESHOLD' : ('b2.user.parameters', 'real', """
					Electron temperature at the target (in eV) which is used a threshold identifying the transition of the local magnetic flux tube to detachment. The width of the zone with Te less than TE_DET_THRESHOLD (counted from the strike point towards the SOL side) is outputted into user_SPb.trc. This distance monotonically increases with increasing of radiated power fraction or with decreasing of peak target energy loads, therefore it may be used as a measure of the degree of detachment.
				""", '2.0'),
   
      'Q95_ALBLL' : ('b2.user.parameters', 'real', """
					Safety factor used to estimate the ballooning "alpha" parameter, if not assigned will be estimated as L_conn/(2*pi*R) at the core interface.
				""", '0.0'),
   
      'R0_ALBLL' : ('b2.user.parameters', 'real', """
					Major radius used to estimate the ballooning "alpha" parameter. If not assigned, will be estimated as 0.5*(Rmin-Rmax) at the core interface.
				""", '0.0'),
   
      'B0_ALBLL' : ('b2.user.parameters', 'real', """
					Magnetic field used to estimate the ballooning "alpha" parameter. If not assigned, will be estimated as Bomp*R0/Romp at the core interface.
				""", '0.0'),
   
      'TRGSHP' : ('b2.user.parameters', 'real array of size (NTRGTS)', """
					Target shaping factor applied to plasma heat loads in peak heat flux estimate calculated by b2mod_usertrc.
				""", '1.0'),
   
      'FILEDATA' : ('b2.user.parameters', 'logical array of size 10', """
					Switches to turn on/off the tracing files controlled by the ank_tracing switch. The files are defined in b2mod_diag, in order, starting with element 2 of the filedata array: test.trc, residuals.trc, sources.trc, blnn.trc, blne.trc, integral.trc, user.trc, blnm.trc, sepdata.trc.
					If there is no b2.user.parameters file present, the flags for user.trc are set to .false..
					If the tracing files are to be appended but a reading error occurs when opening them, the corresponding filedata element is overwritten to .false..
				""", '.true.'),
   
      'USER_FILENAME' : ('b2.user.parameters', 'character*80', """
					Filename where /USER/ namelist is stored.
				""", 'b2.user.parameters'),
    
},

'b2.optimization.parameters' : {

      'NCF' : ('b2.optimization.parameters', 'integer', """
					Number of cost functions (icf = 1, NCF).
				""", '0'),
   
      'CFTYPE' : ('b2.optimization.parameters', 'integer array of size (NCF)', """
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
					10 - Difference, on the desired CVs, of calculated ion saturation current (as ne*cs*eV) and values read from file, normalized with average experimental value (units must be kA/m^{2}).
					11 - Heat flux peakedness on the desired FCs (output in W^{2}/m^{2}).
					12 - Difference, on the desired FCs, of calculated perpendicular or parallel heat flux and values read from file, normalized with average experimental value (units must be in MW^{2}/m^{2}). Use PARALLEL_HF to specify whehter the parallel or perpendicular heat flux is used.
				""", '-1'),
   
      'PARALLEL_HF' : ('b2.optimization.parameters', 'logical', """
					Indicates for cost function 12 if the heat flux considered is the one parallel to the magnetic field (TRUE) or perpendicular to the surface (FALSE).
				""", 'TRUE'),
   
      'CFDEF' : ('b2.optimization.parameters', 'integer array of size (NCF)', """
					Indicates how the domain of cost function ifc is specified. Valid options are:
					1 - The cost function is defined on the OMP, using the rzomp array. In this case CFSTART,CFEND are not necessary and ignored.
					2 - The cost function is defined using the FC labels specified in CFSTART,CFEND. Cost functions requiring CVs or FCs can both be defined in this way.
					3 - The cost function is defined using the CV labels specified in CFSTART,CFEND. Only cost functions requiring CVs can be defined in this way.
					4 - The cost function is defined using the CF_REG and CF_REGP arrays. Cost functions requiring CVs or FCs can both be defined in this way.
				""", '0'),
   
      'CFSTART, CFEND' : ('b2.optimization.parameters', 'integer arrays of size (NCF)', """
					Specify the starting/ending, face (FC) label fcLbl or control volume (CV) label cvLbl where the cost function icf will be evaluated. For CFTYPE = 0 and CFTYPE = 6 they instead identify which cost functions will be summed together.
				""", '0'),
   
      'CF_REG' : ('b2.optimization.parameters', 'integer array of size (mxnCf)', """
					Listing for each cost function the corresponding domain CVs or FCs. WARNING! No attempt is made to check if these CVs or FCs are connected, sorted or even available in the current geometry: it is up to the user to make sure the list is correct. mxnCf is a hard coded maximum length defined in b2mod_par_opt.
				""", '0'),
   
      'CF_REGP' : ('b2.optimization.parameters', 'integer array of size (NCF, 2)', """
					CF_REGP(icf, 1) points, for cost function icf, to the first index in the CF_REG list.
					CF_REGP(icf, 2) number of items in CF_REG list for cost function icf.
				""", '0'),
   
      'CFWEIGHT' : ('b2.optimization.parameters', 'real array of size (NCF)', """
					Multipliers to re-scale each cost function separately.
				""", '1.0'),
   
      'MapToOMP' : ('b2.optimization.parameters', 'logical array of size (NCF)', """
					Indicates if cost function icf is to be re-mapped to the OMP, according to CFTYPE.
					Warning! The mapping is a rigid translation of the data to the OMP and is safe to work only for non-extended grids and for cost functions defined on the same number of elements as the OMP list.
				""", 'FALSE'),
   
      'NSIGMA' : ('b2.optimization.parameters', 'integer', """
					Number of standard deviation variables used for Bayesian MAP cost function (normally this should be equal to the number of cost functions summed for CFTYPE = 6, i.e. one for each variable on each domain) (isigma = 1, NSIGMA}).
				""", '0'),
   
      'SIGMA' : ('b2.optimization.parameters', 'real array of size (NSIGMA)', """
					Value of the prediction error standard deviation. For absolute STD the units are the same as the experimental data used for the cost function it refers to.
				""", '0.0'),
   
      'SCALE_SIGMA' : ('b2.optimization.parameters', 'logical array of size (NSIGMA)', """
					Indicates if SIGMA(isigma) is intended as relative standard deviation (SCALE_SIGMA(isigma)=.TRUE.) or absolute (SCALE_SIGMA(isigma)=.FALSE.).
				""", 'TRUE'),
   
      'READ_SIGMA' : ('b2.optimization.parameters', 'logical array of size (NSIGMA)', """
					(Experimental! Do not use!) Specifies if sigma can be read from the experimental data files cfi.dat.
				""", 'FALSE'),
   
      'NMEAN' : ('b2.optimization.parameters', 'integer', """
					Number of predictin error mean variables used for Bayesian MAP cost function.
				""", '0'),
   
      'MEAN' : ('b2.optimization.parameters', 'real*8 array of size (NMEAN)', """
					Value of the predictin error mean.
				""", '0.0'),
   
      'PRIOR_TYPE' : ('b2.optimization.parameters', 'integer array of size (NNVAR)', """
					Defines the type of prior distribution for each parameter for the MAP cost function. Possible values are:
					0 - Uniform distribution (i.e. $\pi(\theta)=1.0$).
					1 - Uninformative Gaussian prior.
					2 - Gamma distribution, defined through mean and standard deviation.
				""", '-1'),
   
      'PRIOR_PAR' : ('b2.optimization.parameters', 'real array of size (NNVAR,2)', """
					Indicates parameters for the prior distributions.
					For PRIOR_TYPE=0, not used.
					For PRIOR_TYPE=1 and 2, PRIOR_TYPE(ii,1) indicates the mean and PRIOR_TYPE(ii,2) indicates the standard deviation of the distribution.
				""", '-1.0'),
   
      'PRIOR_RANGE' : ('b2.optimization.parameters', 'real array of size (NNVAR,2)', """
					Indicates the valid range for the prior distributions, outside of which the program will return an infinite cost function value. PRIOR_RANGE(:,1) sets the lower range and PRIOR_RANGE(:,2) sets the upper range. (p_infty is a parameter currently set to 1e30).
				""", '10*p_infty'),
   
      'SHIFT_CF_DATA' : ('b2.optimization.parameters', 'integer array of size (NCF)', """
					For each cost function where experimental data is read, specifies whether or not to shift the separatrix position in the experimental data spatial coordinate as follows: (r - r_{sep}) - SHIFT_VALUE$. Unique integers larger than zero for each cost function means that each has its specific shift value. Using the same integer for two (or more) cost functions makes to code use the same shift value for those cost functions (the first SHIFT_VALUE among the cost function with the same integer is adopted). Possible usage: Thomson scattering data of density and temperature which should be defined in two separate cost functions but come from the same source and thus have the same shift. NSHIFT is then the number of unique integers and is used to define other parameters below other parameters.
				""", '0'),
   
      'SHIFT_VALUE' : ('b2.optimization.parameters', 'real*8 array of size (NCF)', """
					Defines the value of the shift in millimeters for each cost function with SHIFT_CF_DATA .neq. 0. Tis is also used as initial guess in case of optimization.
				""", '0.0'),
   
      'SHIFT_PRIOR_TYPE' : ('b2.optimization.parameters', 'integer array of size (NSHIFT)', """
					Same as PRIOR_TYPE but defined for each unique cost function shift.
				""", '-1'),
   
      'SHIFT_PRIOR_PAR' : ('b2.optimization.parameters', 'real*8 array of size (NSHIFT,2)', """
					Same as PRIOR_PAR but defined for each unique cost function shift.
				""", '-1.0'),
   
      'SHIFT_PRIOR_RANGE' : ('b2.optimization.parameters', 'real*8 array of size (NSHIFT,2)', """
					Same as PRIOR_RANGE but defined for each unique cost function shift.
				""", '10*p_infty'),
   
      'CORR_MODEL' : ('b2.optimization.parameters', 'integer array of size (NCF)', """
					Specifies the type of correlation model for the covariance matrix in the MAP cost function.Possible values are:
					0 - No correlation, thus simple diagonal covariance matrix.
					1 - Correlation model based on exponential decay with a correlation length specified using CORR_LENGTH.
				""", '0'),
   
      'CORR_LENGTH' : ('b2.optimization.parameters', 'real*8 array of size (NCF)', """
					Defines the value of the correlation length in millimeters for each MAP-type cost function with CORR_MODEL&gt;0. This is also used as initial guess in case of optimization.
				""", '0.0'),
   
      'CORR_CUTOFF' : ('b2.optimization.parameters', 'real*8', """
					For the exponential decay correlation model, off-diagonal elements with value of the exponential below this threshold are set to zero.
				""", '0.01'),
   
      'CORR_PRIOR_TYPE' : ('b2.optimization.parameters', 'integer array of size (NCORR_OPT)', """
					Same as PRIOR_TYPE but defined for each MAP cost function where sensitivity for CORR_LENGTH is calculated or this parameter optimized (see CORR_OPT). NCORR_OPT is the number of correlation lengths which are optimized, so for which a prior is required.
				""", '-1'),
   
      'CORR_PRIOR_PAR' : ('b2.optimization.parameters', 'real*8 array of size (NCORR_OPT,2)', """
					Same as PRIOR_PAR but defined for each MAP cost function where sensitivity for CORR_LENGTH is calculated or this parameter optimized.
				""", '-1.0'),
   
      'CORR_PRIOR_RANGE' : ('b2.optimization.parameters', 'real*8 array of size (NCORR_OPT,2)', """
					Same as PRIOR_RANGE but defined for each MAP cost function where sensitivity for CORR_LENGTH is calculated or this parameter optimized.
				""", '10*p_infty'),
   
      'NNVAR' : ('b2.optimization.parameters', 'integer', """
					Number of sensitivity/optimization parameters (radially varying transport coefficients count as 1).
				""", '0'),
   
      'PARTYPE' : ('b2.optimization.parameters', 'integer array of size (NNVAR)', """
					Indicates the type of sensitivity/optimization parameter. Valid options are:
					-1 - mean, error mean in likelihood function for Bayesian inference (one for each plasma quantity and location used). If present, these must ALWAYS be the last parameters in the vector!
					0 - sigma, standard deviation in likelihood function for Bayesian inference (one for each plasma quantity and location used). If present, these must ALWAYS be defined after each physical parameter (PARTYPE&gt;0) and before the mean (PARTYPE=-1).
					1 - parm_dna or tdata(:,:,1,:)
					2 - parm_dpa or tdata(:,:,2,:)
					3 - parm_hci or tdata(:,:,3,:)
					4 - parm_hce or tdata(:,:,4,:)
					5 - tdata(:,:,5,:) (not yet tested!)
					6 - parm_vla or tdata(:,:,6,:)
					7 - parm_vsa or tdata(:,:,7,:)
					8 - parm_sig or tdata(:,:,8,:)
					9 - parm_alf or tdata(:,:,9,:)
					10 - enepar
					11 - enipar
					12 - conpar
					13 - mompar
					14 - potpar
					15 - enkpar
					16 - b2recyc
					17 - b2tqna_ballooning
					18 - b2tqna_ballooning_rescale
					19 - keps_cd
					20 - keps_heat
					21 - keps_heat_i
					22 - keps_sig
					23 - keps_alf
					24 - keps_visc
					25 - keps_dkt
					26 - keps_dzt
					27 - b2sikt_fac_diss
					28 - b2sikt_fac_diss_core
					29 - b2sikt_fac_sheath
					30 - b2sikt_fac_sheath_core
					31 - keps_shear
					32 - b2tfhi_fsigkt
					33 - b2sikt_fac_vis_RS
					34 - b2tfhi_fflokt
					35 - b2tfhi_fconkt
					36 - b2tfhi_fflozt
					37 - b2tfhi_fconzt
					38 - b2tfhi_fkt_hie
					39 - b2tfhe_vis_kt
				""", '-2'),
   
      'SIGMA_OPT' : ('b2.optimization.parameters', 'logical array of size (NSIGMA)', """
					For each sigma, specifies whether its sensitivity is computed or not, and thus whether it is optimized or fixed.
				""", '.true.'),
   
      'MEAN_OPT' : ('b2.optimization.parameters', 'logical array of size (NMEAN)', """
					For each mean, specifies whether its sensitivity is computed or not, and thus whether it is optimized or fixed.
				""", '.false.'),
   
      'SHIFT_OPT' : ('b2.optimization.parameters', 'logical array of size (NSHIFT)', """
					For each SHIFT_CF_VALUE, specifies whether its sensitivity is computed or not, and whether is optimized or fixed.
				""", '.false.'),
   
      'CORR_OPT' : ('b2.optimization.parameters', 'logical array of size (NCF)', """
					For each MAP cost function where CORR_MODEL&gt;0, specifies whether CORR_LENGTH sensitivity is computed or not, and whether is optimized or fixed.
				""", '.false.'),
   
      'SPATIAL_DEP' : ('b2.optimization.parameters', 'logical array of size (NNVAR)', """
					For each sensitivity/optimization variables, specifies if radially varying coefficients are optimized.
					Meaningful only for partype = 1 to 9.
				""", '.false.'),
   
      'SPATIAL_POINTS' : ('b2.optimization.parameters', 'integer array of size (NNVAR)', """
					Number of spatial points for sensitivity/optimization parameter ipar (should be the same as ndata in b2.transport.inputfile). The actual number of optimized variables (NPAR_OPT) is then equal to the total number of spatial points + any other additional parameter.
				""", '0'),
   
      'PARIS' : ('b2.optimization.parameters', 'integer array of size (NNVAR)', """
					Specifies the species of the sensitivity/optimization parameter. Only meaningful for partype = [1-3,5,7,12,13,16].
				""", '0'),
   
      'PARIB' : ('b2.optimization.parameters', 'integer array of size (NNVAR)', """
					Specifies the boundary/strata of the sensitivity/optimization parameter. Only meaningful for partype = [10-16].
				""", '0'),
   
      'PAR_RESCALE' : ('b2.optimization.parameters', 'real array of size (NPAR_OPT)', """
					Coefficient to rescale optimization parameters (and their gradient). Note dimension is NPAR_OPT, so need to specify it also for each point in case of spatially varying coefficients.
				""", '1.0'),
   
      'X0' : ('b2.optimization.parameters', 'real array of size (NPAR_OPT)', """
					Initial guess for each optimization parameter. Must be defined (p_infty is a parameter currently set to 1e30).
				""", '10*p_infty'),
   
      'XL' : ('b2.optimization.parameters', 'real array of size (NPAR_OPT)', """
					Lower bound for each optimization parameter.
				""", '-10*p_infty'),
   
      'XU' : ('b2.optimization.parameters', 'real array of size (NPAR_OPT)', """
					Upper bound for each optimization parameter.
				""", '10*p_infty'),
   
      'SHIFT_L' : ('b2.optimization.parameters', 'real*8 array of size (NCF)', """
					Lower bound for SHIFT_CF_DATA parameters.
				""", '-1000.0'),
   
      'SHIFT_U' : ('b2.optimization.parameters', 'real*8 array of size (NCF)', """
					Upper bound for SHIFT_CF_DATA parameters.
				""", '1000.0'),
   
      'CORR_L' : ('b2.optimization.parameters', 'real*8 array of size (NCF)', """
					Lower bound for CORR_LENGTH parameters. Must be specified for each cost function!
				""", '-10*p_infty'),
   
      'CORR_U' : ('b2.optimization.parameters', 'real*8 array of size (NCF)', """
					Upper bound for CORR_LENGTH parameters. Must be specified for each cost function!
				""", '10*p_infty'),
   
      'CORR_RESCALE' : ('b2.optimization.parameters', 'real*8 array of size (NCF)', """
					Same as PAR_RESCALE but defined for CORR_LENGTH} parameters. Must be specified for each cost function!
				""", '1.0'),
   
      'MAXITER' : ('b2.optimization.parameters', 'integer', """
					Maximum number of optimization iterations. Can overridden with PETCs/Tao by using command line options for the optimization.
				""", '100'),
   
      'CPU_OPT' : ('b2.optimization.parameters', 'real', """
					Maximum amount of CPU time in seconds after which the optimization is stopped.
				""", '0.0'),
   
      'TOL_OPT' : ('b2.optimization.parameters', 'real', """
					Tolerance below which optimization is stopped. For PETCs/Tao it is used for the absolute gradient norm, the relative gradient norm, and the gradient reduction stopping criteria. Can be overridden with PETCs/Tao by using command line options for the optimization.
				""", '1.0e-7'),
   
      'HESSIAN_APPROXIMATION' : ('b2.optimization.parameters', 'character*256', """
					Type of Hessian approximation employed. Depends on optimization library. Possible values are currently: 'limited-memory' and 'exact'. When using the 'exact' option the steepest descent algorithm is used.
				""", 'limited-memory'),
   
      'LIMITED_MEMORY_UPDATE_TYPE' : ('b2.optimization.parameters', 'character*256', """
					Specifies which kind of Hessian approximation is employed if HESSIAN_APPROXIMATION is set to 'limited-memory'. Can overridden with PETCs/Tao by using command line options for the optimization.
				""", 'bfgs'),
    
},

'b2.sputter_save.parameters' : {

      'NX_SP' : ('b2.sputter_save.parameters', 'integer', """
					Array dimension NX used in this namelist.
				""", 'nx'),
   
      'NY_SP' : ('b2.sputter_save.parameters', 'integer', """
					Array dimension NY used in this namelist.
				""", 'ny'),
   
      'NS_SP' : ('b2.sputter_save.parameters', 'integer', """
					Array dimension NS used in this namelist.
				""", 'ns'),
   
      'SPUTTER_YIELD' : ('b2.sputter_save.parameters', 'real array of size (-1:NX,-1:NY,0:NS-1,1:2)', """
					Contains the chemical sputtering yield of species (is) at position (ix,iy) in element (:,:,:,1) and the physical sputtering yield in element (:,:,:,2).
				""", '0.0'),
   
      'SPUTTER_YIELD2' : ('b2.sputter_save.parameters', 'real array of size (-1:NX,-1:NY,0:NS-1,1:2)', """
					Contains the energy chemical sputtering yield of species (is) at position (ix,iy) in element (:,:,:,1) and the energy physical sputtering yield in element(:,:,:,2).
				""", '0.0'),
    
},

'b2.atomic_physics_rescale.parameters' : {

      'RESCALE_SA' : ('b2.atomic_physics_rescale.parameters', 'real array of size(0:NS-1)', """
					Scaling factors for rtsa: ionisation rates of species (is).
				""", '1.0'),
   
      'RESCALE_RA' : ('b2.atomic_physics_rescale.parameters', 'real array of size(0:NS-1)', """
					Scaling factors for rtra: recombination rates of species (is).
				""", '1.0'),
   
      'RESCALE_QA' : ('b2.atomic_physics_rescale.parameters', 'real array of size(0:NS-1)', """
					Scaling factors for rtqa: electron cooling rates of species (is).
				""", '1.0'),
   
      'RESCALE_CX' : ('b2.atomic_physics_rescale.parameters', 'real array of size(0:NS-1)', """
					Scaling factors for rtcx: charge exchange rates of species (is).
				""", '1.0'),
   
      'RESCALE_RD' : ('b2.atomic_physics_rescale.parameters', 'real array of size(0:NS-1)', """
					Scaling factors for rtrd: line radiation rates of species (is).
				""", '1.0'),
   
      'RESCALE_BR' : ('b2.atomic_physics_rescale.parameters', 'real array of size(0:NS-1)', """
					Scaling factors for rtbr: bremsstrahlung radiation rates of species (is).
				""", '1.0'),
    
},

}

