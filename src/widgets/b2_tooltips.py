
tooltips = {
   
   'b2ai.dat' : {
      
      'dimens' : ('b2ai params', 'None', """
					the number of charge states
				""", 'None'),
   
      'label' : ('b2ai params', 'None', """a label""", 'None'),
   
      'specs' : ('b2ai params', 'None', """
					atomic charge, nuclear charge, atomic mass and atomic charge squared for each charge stateminimum atomic charge of the stage, maximum atomic charge of the stage, nuclear charge, and atomic mass; this data should match that given in b2ah.dat
				""", 'None'),
   
      'naini' : ('b2ai params', 'None', """
					initial densities for each of the charge states, in m^-3
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
					specifies the number of regions where boundary conditions will be specified the 'south' boundary is broken into three pieces with one quarter of the cells in the first region, half ofthe cells in the second, and the remaining quarter in the third region (inner target private flux, core, outerprivate flux). This is geometry-dependent information the code will check against the mesh connectivity and return an error if the two do not match the 'north', 'west' and 'east' are not broken up, and correspond to the SOL boundary, inner target andouter target, respectively. For double-null cases, the north boundary should be split into two sections
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
					at least 100 additional numbers, of which only the first is relevant for us -1.0 read the mesh data using the "simplified" Carre format -2.0 read the mesh data using the Sonnet format
				""", 'None'),
   
      },
   
   'b2mn.dat' : {
      
      'b2stbc_coreregno' : ('', 'integer', """
					coreregno, coreregn2 - integers. coreregno is the boundary index of the core boundary in the input files b2ah.dat and b2mn.dat. For a standard single-null case, coreregno is 1. For a straight geometry or limiter case, it is likely that coreregno need be set to 0, depending on the actual geometry details. 
					coreregn2 is the boundary index of the second core boundary in case of a double-null geometry, and is not used otherwise.
				""", '1'),
   
      'b2stbc_coreregn2' : ('', 'integer', """
					coreregno, coreregn2 - integers. coreregno is the boundary index of the core boundary in the input files b2ah.dat and b2mn.dat. For a standard single-null case, coreregno is 1. For a straight geometry or limiter case, it is likely that coreregno need be set to 0, depending on the actual geometry details. 
					coreregn2 is the boundary index of the second core boundary in case of a double-null geometry, and is not used otherwise.
				""", '4'),
   
      'b2stbc_pfrregno1' : ('', 'integer', """
					pfrregno1, pfrregno2 - integers. 
					pfrregno1 is the boundary index of the first half of the private flux region boundary on which feedback is being applied (through b2stbc_ndes or b2stbc_private_flux_puff) in the input files b2ah.dat and b2mn.dat. pfrregno2 is the second half of the same private flux region. For a standard single null, the pair should be (0,2). For a standard double-null, the lower private flux region is labelled with the pair (0,5), and the upper private flux region with the pair (2,3). One can use only one private flux region by setting pfrregno1.eq.pfrregno2.
				""", '0'),
   
      'b2stbc_pfrregno2' : ('', 'integer', """
					pfrregno1, pfrregno2 - integers. 
					pfrregno1 is the boundary index of the first half of the private flux region boundary on which feedback is being applied (through b2stbc_ndes or b2stbc_private_flux_puff) in the input files b2ah.dat and b2mn.dat. pfrregno2 is the second half of the same private flux region. For a standard single null, the pair should be (0,2). For a standard double-null, the lower private flux region is labelled with the pair (0,5), and the upper private flux region with the pair (2,3). One can use only one private flux region by setting pfrregno1.eq.pfrregno2.
				""", '2'),
   
      'b2agfs_xoffset' : ('', 'real', """
					xoffset, yoffset - real*8. 
					xoffset and yoffset are offsets of the basis mesh in the x- and y-direction respectively. The mesh will be translated by (xoffset,yoffset) if any of the two is non-zero from its position given in the local_sonnet (See 'b2agfs_geometry' above) file. 
					To be used in b2ag.dat.
				""", '0.0'),
   
      'b2agfs_yoffset' : ('', 'real', """
					xoffset, yoffset - real*8. 
					xoffset and yoffset are offsets of the basis mesh in the x- and y-direction respectively. The mesh will be translated by (xoffset,yoffset) if any of the two is non-zero from its position given in the local_sonnet (See 'b2agfs_geometry' above) file. 
					To be used in b2ag.dat.
				""", '0.0'),
   
      'b2agfs_xrescale' : ('', 'real', """
					yrescale - real*8. 
					Rescaling factors of the x- and y- coordinates of the basis mesh. 
					To be used in b2ag.dat.
				""", '1.0'),
   
      'b2agfs_yrescale' : ('', 'real', """
					yrescale - real*8. 
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
   
      'b2agfs_geometry' : ('Geometry', '', """
					local_sonnet - character string.
					local_sonnet is the file name of the geometry file to be read. 
					The file will be looked for in the run directory, in the ../baserun directory and in $SOLPSTOP/data/meshes. To be used in b2ag.dat.
				""", 'upgrade.geometry'),
   
      'b2mwti_jxa' : ('Geometry', '', """
					jxa - integer. 
					Cell index, on the basis mesh, of the outer midplane. Default value depends on geometry: 
					Single-null : jxa=rightcut1(1)-(rightcut1(1)-leftcut1(1))/4, i.e. three quarters of the way between the two cuts. 
					Double-null : jxa=(rightcut1(1)+rightcut1(2))/2, i.e. halfway between the two outer cuts. Straight geometry : jxa=3*nx/4
				""", 'See description (integer)'),
   
      'b2mwti_jxi' : ('Geometry', 'integer', """
					Cell index, on the basis mesh, of the inner midplane. Default value depends on geometry:
					Single-null : jxi=leftcut1(1)+(rightcut1(1)-leftcut1(1))/4, i.e. one quarter of the way between the two cuts. Double-null : jxi=(leftcut1(1)+leftcut1(2))/2, i.e. halfway between the two inner cuts.
					Straight geometry : jxi=nx/4
				""", 'See description (integer)'),
   
      'b2agmx_pbs_from_basis_mesh' : ('Geometry', 'integer', """
					If pbs_from_basis_mesh.eq.0, the pbs array is computed from values on the actual working mesh (old treatment). 
					If pbs_from_basis_mesh.eq.1, the pbs array is computed from values on the (possibly) finer basis mesh from the geometry file and the contributions from each basis cell are added to obtain the value on the working mesh.
					In both cases, mind the value of 'b2news_area_fix', which should be also declared in b2ag.dat if the non-default behaviour is wanted.
				""", '1'),
   
      'b2agfs_periodic_bc' : ('Geometry', 'integer', """
					periodic_bc - integer. 
					periodic_bc specifies if this is either an island or limiter geometry. 
					If periodic_bc.eq.1 then island/limiter treatment is turned on. We differentiate between the two case through nncut: 
					nncut.eq.0 = limiter case 
					nncut.ge.1 = island divertor case (there should be nncut islands then)
					The case periodic_bc.eq.-1 is used to remove tranverse physics in 1-D cases. 
					If periodic_bc.eq.0 then we have the usual treatment. No other values are currently allowed. To be used in b2ag.dat.
				""", '0'),
   
      'b2agsi_isymm' : ('Geometry', 'integer', """
					isymm - integer. 
					isymm specifies the type of symmetry of the geometry: isymm.eq.0 implies a slab geometry, 
					isymm.eq.1.or.isymm.eq.2 imply rotational symmetry about the crx=0 axis, and isymm.eq.3.or.isymm.eq.4 indicate rotational symmetry about the cry=0 axis. 
					Other values are not allowed. 
					isymm.eq.1.or.isymm.eq.3 mean a toroidal geometry case, i.e. with a toroidal (out-of-plane) magnetic field component. 
					isymm.eq.2.or.isymm.eq.4 mean a cylindrical geometry case, i.e. no toroidal magnetic field component. To be used in b2ag.dat.
				""", '1'),
   
      'b2stbc_solregno' : ('Geometry', 'integer', """
					solregno - integer. 
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
					Bt_adjust - integer.
					If the mesh is offset (See b2agfs_xoffset, b2agfs_yoffset below) and Bt_adjust.eq.1, then the magnetic field is recomputed, keeping the pitch constant but changing the toroidal field magnitude according to Bt = Bt0/R. To be used in b2ag.dat.
				""", '0'),
   
      'b2agfs_Bt_rescale' : ('Geometry', 'real', """
					Bt_rescale - real*8. 
					The magnetic field will be multiplied by Bt_rescale. All components of the field are scaled together. To be used in b2ag.dat.
				""", '1.0'),
   
      'b2agfs_pit_rescale' : ('Geometry', 'real', """
					pit_rescale - real*8. 
					The magnetic field line pitch will be multiplied by pit_rescale. 
					This means that the poloidal field component is multiplied by pit_rescale, while the toroidal field component is left unchanged. To reverse the plasma current direction, set pit_rescale to -1.0. 
					The sign convention used is that a positive poloidal field points in the direction of increasing &lt;ix&gt;. Be mindful however that, when inverting the sign of the poloidal magnetic field, you are also inverting the direction of the parallel velocity. You will then need to use the 'b2mndr_inverse_ua' switch to correct for that. To be used in b2ag.dat.
				""", '1.0'),
   
      'b2agfs_Bt_reversal' : ('Geometry', 'integer', """
					Bt_reversal - integer. If Bt_reversal.eq.1, then the sign of the toroidal field component only is reversed. The sign convention used is that a positive toroidal field leads to a Bx(grad(B)) direction pointing down, so B is out of the page when looking at the usual view of the poloidal plane with the center line on the left. To be used in b2ag.dat.
				""", '0'),
   
      'b2agfs_min_pitch' : ('Geometry', 'real', """
					Minimum allowed value for the pitch angle (in degrees) at the plates.
				""", '1.0'),
   
      'b2agfs_nncut' : ('Geometry', 'integer', """
					Number of topological cuts in geometry. Needed only to force a different value from the one computed automatically by b2ag.
				""", 'See description (integer)'),
   
      'b2mndr_run_number' : ('', 'integer', """
					These switches server as identification for the simulation. They can be inherited from SOLPS-GUI:
					Run number : The number of the run.
					Shot number : Shot number identifying the run. Defaults to the last number found in shotnumber.history, or 0 if the file is not found.
					Device : The device where the simulation was run.
					User : The user who ran the simulation.
				""", '1000'),
   
      'b2mndr_shot_number' : ('', 'integer', """
					These switches server as identification for the simulation. They can be inherited from SOLPS-GUI:
					Run number : The number of the run.
					Shot number : Shot number identifying the run. Defaults to the last number found in shotnumber.history, or 0 if the file is not found.
					Device : The device where the simulation was run.
					User : The user who ran the simulation.
				""", '0'),
   
      'b2mndr_device' : ('', 'string', """
					These switches server as identification for the simulation. They can be inherited from SOLPS-GUI:
					Run number : The number of the run.
					Shot number : Shot number identifying the run. Defaults to the last number found in shotnumber.history, or 0 if the file is not found.
					Device : The device where the simulation was run.
					User : The user who ran the simulation.
				""", '$(DEVICE)'),
   
      'b2mndr_user' : ('', 'string', """
					These switches server as identification for the simulation. They can be inherited from SOLPS-GUI:
					Run number : The number of the run.
					Shot number : Shot number identifying the run. Defaults to the last number found in shotnumber.history, or 0 if the file is not found.
					Device : The device where the simulation was run.
					User : The user who ran the simulation.
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
					   ..compute source linearisation
					   ..do i2=1,nstg2
					    ..perform one inner iteration
					    ..re-compute auxiliary quantities
					    ..produce monitoring output
					   ..enddo
					  ..enddo
					 ..enddo
					This can be completed by the the 'b2mndt_nstg_ares??' switches.
					See 'Numerics' section for details.
				""", '1'),
   
      'b2mndt_nstg1' : ('', 'integer', """
					Time-dependent mode and iterative mode switches. The basic code timestep proceeds as follows:
					 ..test input arguments
					 ..compute auxiliary quantities
					 ..prepare source computation
					 ..do i0=1,nstg0
					  ..compute log-log linearised rate coefficients
					  ..do i1=1,nstg1
					   ..compute source linearisation
					   ..do i2=1,nstg2
					    ..perform one inner iteration
					    ..re-compute auxiliary quantities
					    ..produce monitoring output
					   ..enddo
					  ..enddo
					 ..enddo
					This can be completed by the the 'b2mndt_nstg_ares??' switches.
					See 'Numerics' section for details.
				""", '1'),
   
      'b2mndt_nstg2' : ('', 'integer', """
					Time-dependent mode and iterative mode switches. The basic code timestep proceeds as follows:
					 ..test input arguments
					 ..compute auxiliary quantities
					 ..prepare source computation
					 ..do i0=1,nstg0
					  ..compute log-log linearised rate coefficients
					  ..do i1=1,nstg1
					   ..compute source linearisation
					   ..do i2=1,nstg2
					    ..perform one inner iteration
					    ..re-compute auxiliary quantities
					    ..produce monitoring output
					   ..enddo
					  ..enddo
					 ..enddo
					This can be completed by the the 'b2mndt_nstg_ares??' switches.
					See 'Numerics' section for details.
				""", '1'),
   
      'b2news_facdrift_dec' : ('', 'real', """
					Ramping parameters for facdrift, which multiplies the diamagnetic terms. The code is started on the first time step with facdrift=facdrift_start. If facdrift_target.ne.facdrift_start, then, on each time step, facdrift is multiplied by facdrift_inc. If the code does not converge on the timestep, facdrift is decreased by facdrift_dec. A facdrift profile is also possible, see Numerics section for details.
				""", '0.0'),
   
      'b2news_facdrift_inc' : ('', 'real', """
					Ramping parameters for facdrift, which multiplies the diamagnetic terms. The code is started on the first time step with facdrift=facdrift_start. If facdrift_target.ne.facdrift_start, then, on each time step, facdrift is multiplied by facdrift_inc. If the code does not converge on the timestep, facdrift is decreased by facdrift_dec. A facdrift profile is also possible, see Numerics section for details.
				""", '1.0'),
   
      'b2news_facdrift_start' : ('', 'real', """
					Ramping parameters for facdrift, which multiplies the diamagnetic terms. The code is started on the first time step with facdrift=facdrift_start. If facdrift_target.ne.facdrift_start, then, on each time step, facdrift is multiplied by facdrift_inc. If the code does not converge on the timestep, facdrift is decreased by facdrift_dec. A facdrift profile is also possible, see Numerics section for details.
				""", '0.0'),
   
      'b2news_facdrift_target' : ('', 'real', """
					Ramping parameters for facdrift, which multiplies the diamagnetic terms. The code is started on the first time step with facdrift=facdrift_start. If facdrift_target.ne.facdrift_start, then, on each time step, facdrift is multiplied by facdrift_inc. If the code does not converge on the timestep, facdrift is decreased by facdrift_dec. A facdrift profile is also possible, see Numerics section for details.
				""", '0.0'),
   
      'b2news_facExB_dec' : ('', 'real', """
					Ramping parameters for facExB, which multiplies the ExB terms. Same treatment as above for facdrift.
				""", '0.0'),
   
      'b2news_facExB_inc' : ('', 'real', """
					Ramping parameters for facExB, which multiplies the ExB terms. Same treatment as above for facdrift.
				""", '1.0'),
   
      'b2news_facExB_start' : ('', 'real', """
					Ramping parameters for facExB, which multiplies the ExB terms. Same treatment as above for facdrift.
				""", '0.0'),
   
      'b2news_facExB_target' : ('', 'real', """
					Ramping parameters for facExB, which multiplies the ExB terms. Same treatment as above for facdrift.
				""", '0.0'),
   
      'b2news_facvis_dec' : ('', 'real', """
					Ramping parameters for facvis, which multiplies the drift viscosity terms. Same treatment as above for facdrift.
				""", '0.0'),
   
      'b2news_facvis_inc' : ('', 'real', """
					Ramping parameters for facvis, which multiplies the drift viscosity terms. Same treatment as above for facdrift.
				""", '1.0'),
   
      'b2news_facvis_start' : ('', 'real', """
					Ramping parameters for facvis, which multiplies the drift viscosity terms. Same treatment as above for facdrift.
				""", '0.0'),
   
      'b2news_facvis_target' : ('', 'real', """
					Ramping parameters for facvis, which multiplies the drift viscosity terms. Same treatment as above for facdrift.
				""", '0.0'),
   
      'b2stbc_boundary_namelist' : ('', 'integer', """
					Namelist file indicators. If xxx_namelist.eq.1, then the code looks for the file b2.xxx.parameters, in which it expects to find the xxx namelist.
				""", '0'),
   
      'b2stbr_neutrals_namelist' : ('', 'integer', """
					Namelist file indicators. If xxx_namelist.eq.1, then the code looks for the file b2.xxx.parameters, in which it expects to find the xxx namelist.
				""", '0'),
   
      'b2srdt_numerics_namelist' : ('', 'integer', """
					Namelist file indicators. If xxx_namelist.eq.1, then the code looks for the file b2.xxx.parameters, in which it expects to find the xxx namelist.
				""", '0'),
   
      'b2tqna_transport_namelist' : ('', 'integer', """
					Namelist file indicators. If xxx_namelist.eq.1, then the code looks for the file b2.xxx.parameters, in which it expects to find the xxx namelist.
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
					If set to a negative value, the run continues from the time read in b2fstati.
				""", '0.0'),
   
      'b2mndr_etim' : ('Run', 'real', """
					etim specifies the end time. Only active if etim &gt; stim.
				""", '0.0'),
   
      'b2news_no_solve' : ('Run', 'integer', """
					If no_solve.eq.1, then the code is run without actually solving any equations. All secondary and dependent data is computed. 
					The nstg(0:2) array is overwritten to '1's. The simulation time will not be updated. The code will compute fluxes, sources, transport coefficients, etc... 
					'ntim' times but not update the basic plasma quantities. Additionally, if no_solve is set to a negative value, then only some equations are solved (simulation time and nstg arrays will behave normally). 
					no_solve.eq.-1 will activate the parallel momentum equations only. 
					no_solve.eq.-2 will activate the density equations only. no_solve.eq.-4 will activate the potential equation only. (Active only if poteq.eq.1, otherwise, the behaviour dictated by the poteq setting applies). 
					no_solve.eq.-8 will activate the heat equations only. These can be combined. For example, no_solve.eq.-3 will activate the parallel momentum and particle conservation equations. 
					If the no_solve switch requires an equation not to be solved, the settings in the corresponding solvexx arrays from b2.numerics.parameters are moot. 
					The latter are reserved for fine-tuning numerical diagnostics.
				""", '0'),
   
      'b2mndr_cpu' : ('Run', 'real', """
					CPU limit. If cpu.eq.0.0, no CPU limit is enforced. Otherwise, the code stops smoothly after it has been running for at least 'cpu' CPU seconds.
				""", '0.0'),
   
      'b2mndr_elapsed' : ('Run', 'real', """
					Elapsed time limit. Is elapsed.eq.0.0, no time limit is enforced.
					Otherwise, the code stops smoothly after is has been running for at least 'elapsed' wall clock seconds.
				""", '0.0'),
   
      'b2mndr_savecpu' : ('Run', 'real', """
					CPU time interval after which save files plasmastate.xxxx are written. 
					These can be used, in conjunction with the b2co.exe instruction, to recover a crashed run.
				""", '3600.0'),
   
      'b2mndr_ismain' : ('Run', 'real', """
					ismain identifies the index of the main plasma species.
					It must hold that ismain is not a neutral species.
				""", '1'),
   
      'b2sral_inputfile' : ('Run', '', """
					Profiles file indicator. If b2sral_inputfile.eq.1, then the code looks for the file b2.sources.profile in which it expects to find the 'profile' namelist. 
					This namelist will contain profiles of sources measured from the location (ixref,iyref) (default is outer midplane separatrix), which is set with the 'set_transport_i[xy]ref' switches.
				""", '0'),
   
      'b2tqna_inputfile' : ('Run', 'integer', """
					Profiles file indicator. If b2tqna_inputfile.eq.1, then the code looks for the file b2.transport.inputfile, in which it expects to find the transport namelist. 
					This namelist will contain profiles of sources transport parameters measured from the location (ixref,iyref) (default is outer midplane separatrix), which is set with the 'set_transport_i[xy]ref' switches.
				""", '0'),
   
      'b2mndr_eirene' : ('Run', 'integer', """
					Turns on coupling with the Eirene Monte-Carlo neutral code if nonzero. 
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
					Timestep index after which the feedback in b2stbc is activated.
				""", '0'),
   
      'b2stbr_first_flight' : ('Run', 'integer', """
					If first_flight.ne.0, turns on the first flight model. See Physics section for additional details.
				""", '0'),
   
      'b2ytdr_ns' : ('Run', 'integer', """
					New number of species desired when creating a new initial state file using b2yt.exe. Must be specified within b2yt.dat.
				""", 'ns'),
   
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
					The 20 switches above are all feedback switches and require that b2stbc_feedback.ne.0 (See Run section for details) or that lfeedback=.true. in b2.boundary.parameters. The feedback is done as a boundary condition and is under-relaxed using the b2stbc_...._alpha switches (See Numerics section for details). 
					fheycore is the radial electron heat flow entering the core boundary. 
					fhiycore is the radial ion heat flow entering the core boundary. 
					fchycore is the radial current entering the core boundary. fnaycore is the radial flux of species "isfeedback" entering the core boundary. 
					If fhiycore_kinetic_energy.eq.1, the parallel kinetic energy flux is counted as part of the ion energy flux. 
					For double-null cases, the f..ycore variables contain the total flow through both core boundaries taken together. The core boundaries are identified by the coreregno and coreregn2 switches (see Geometry section). 
					The other seven switches are density feedback switches: nesepm is the outer midplane separatrix electron density. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is controlled through particle input of main plasma species isfeedback through the core boundary (See Geometry section for the core boundary indices coreregno and coreregn2). 
					nesepm_sol is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the SOL region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the SOL North boundary (See Geometry section for the SOL North boundary index solregno). If nesepm_overshoot.gt.1.0, the gas puff is turned off when the midplane separatrix density reaches nesepm*nesepm_overshoot. Minimum and maximum values of the feedback gas puff can be set using b2stbc_nesepm_minpuff and b2stbc_nesepm_maxpuff 
					nepedm_sol is similar to nesepm_sol but the feedback is exerted on the electron density at the top of the pedestal, along the outer midplane, at radial position b2stbc_iyped. ndes_sol is the total particle content from the homonuclear sequence of species 'isfeedback' over the entire simulation domain. 
					It is governed, like nesepm_sol, by nesepm_overshoot and nesepm_alpha and corresponds to a SOL boundary feedback. volrec_sol is the total particle source due to volume recombination coming from Eirene. Its feedback is governed by volrec_overshoot and volrec_alpha and volrec_beta parameters (See Numerics section for the latter two). nesepm_pfr is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the PFR region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the PFR South boundary indices pfrregno1 and pfrregno2). 
					ndes is the total particle (neutrals + ions) content of the species whose neutral species has index isfeedback. This is controlled through particle input of neutrals species isfeedback through the 
					private flux boundaries (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2). private_flux_puff is the particle flow of species isfeedback through the private flux region boundary. This is controlled through particle input of neutrals species isfeedback through the private flux boundaris (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2). 
					All but the first of these feedback schemes ("nesepm") can also be run though an Eirene neutral gas puff. In that case, one should set an appropriate gas puffing stratum in the Eirene input file input.dat, as well as in the b2.neutrals.parameters file. The code will assume, unless told otherwise through the use of "eirene_nesepm_istra", that the first stratum of type 'C' found in b2.neutrals.parameters is the stratum used for the feedback. If "eirene_nesepm_istra" is set to a positive number, the code will consider the feedback stratum to be the stratum in the "eirene_nesepm_istra"-th position in b2.neutrals.parameters.
				""", '0.0'),
   
      'b2stbc_fhiycore' : ('', 'real', """
					The 20 switches above are all feedback switches and require that b2stbc_feedback.ne.0 (See Run section for details) or that lfeedback=.true. in b2.boundary.parameters. The feedback is done as a boundary condition and is under-relaxed using the b2stbc_...._alpha switches (See Numerics section for details). 
					fheycore is the radial electron heat flow entering the core boundary. 
					fhiycore is the radial ion heat flow entering the core boundary. 
					fchycore is the radial current entering the core boundary. fnaycore is the radial flux of species "isfeedback" entering the core boundary. 
					If fhiycore_kinetic_energy.eq.1, the parallel kinetic energy flux is counted as part of the ion energy flux. 
					For double-null cases, the f..ycore variables contain the total flow through both core boundaries taken together. The core boundaries are identified by the coreregno and coreregn2 switches (see Geometry section). 
					The other seven switches are density feedback switches: nesepm is the outer midplane separatrix electron density. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is controlled through particle input of main plasma species isfeedback through the core boundary (See Geometry section for the core boundary indices coreregno and coreregn2). 
					nesepm_sol is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the SOL region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the SOL North boundary (See Geometry section for the SOL North boundary index solregno). If nesepm_overshoot.gt.1.0, the gas puff is turned off when the midplane separatrix density reaches nesepm*nesepm_overshoot. Minimum and maximum values of the feedback gas puff can be set using b2stbc_nesepm_minpuff and b2stbc_nesepm_maxpuff 
					nepedm_sol is similar to nesepm_sol but the feedback is exerted on the electron density at the top of the pedestal, along the outer midplane, at radial position b2stbc_iyped. ndes_sol is the total particle content from the homonuclear sequence of species 'isfeedback' over the entire simulation domain. 
					It is governed, like nesepm_sol, by nesepm_overshoot and nesepm_alpha and corresponds to a SOL boundary feedback. volrec_sol is the total particle source due to volume recombination coming from Eirene. Its feedback is governed by volrec_overshoot and volrec_alpha and volrec_beta parameters (See Numerics section for the latter two). nesepm_pfr is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the PFR region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the PFR South boundary indices pfrregno1 and pfrregno2). 
					ndes is the total particle (neutrals + ions) content of the species whose neutral species has index isfeedback. This is controlled through particle input of neutrals species isfeedback through the 
					private flux boundaries (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2). private_flux_puff is the particle flow of species isfeedback through the private flux region boundary. This is controlled through particle input of neutrals species isfeedback through the private flux boundaris (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2). 
					All but the first of these feedback schemes ("nesepm") can also be run though an Eirene neutral gas puff. In that case, one should set an appropriate gas puffing stratum in the Eirene input file input.dat, as well as in the b2.neutrals.parameters file. The code will assume, unless told otherwise through the use of "eirene_nesepm_istra", that the first stratum of type 'C' found in b2.neutrals.parameters is the stratum used for the feedback. If "eirene_nesepm_istra" is set to a positive number, the code will consider the feedback stratum to be the stratum in the "eirene_nesepm_istra"-th position in b2.neutrals.parameters.
				""", '0.0'),
   
      'b2stbc_fhiycore_kinetic_energy' : ('', 'integer', """
					The 20 switches above are all feedback switches and require that b2stbc_feedback.ne.0 (See Run section for details) or that lfeedback=.true. in b2.boundary.parameters. The feedback is done as a boundary condition and is under-relaxed using the b2stbc_...._alpha switches (See Numerics section for details). 
					fheycore is the radial electron heat flow entering the core boundary. 
					fhiycore is the radial ion heat flow entering the core boundary. 
					fchycore is the radial current entering the core boundary. fnaycore is the radial flux of species "isfeedback" entering the core boundary. 
					If fhiycore_kinetic_energy.eq.1, the parallel kinetic energy flux is counted as part of the ion energy flux. 
					For double-null cases, the f..ycore variables contain the total flow through both core boundaries taken together. The core boundaries are identified by the coreregno and coreregn2 switches (see Geometry section). 
					The other seven switches are density feedback switches: nesepm is the outer midplane separatrix electron density. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is controlled through particle input of main plasma species isfeedback through the core boundary (See Geometry section for the core boundary indices coreregno and coreregn2). 
					nesepm_sol is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the SOL region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the SOL North boundary (See Geometry section for the SOL North boundary index solregno). If nesepm_overshoot.gt.1.0, the gas puff is turned off when the midplane separatrix density reaches nesepm*nesepm_overshoot. Minimum and maximum values of the feedback gas puff can be set using b2stbc_nesepm_minpuff and b2stbc_nesepm_maxpuff 
					nepedm_sol is similar to nesepm_sol but the feedback is exerted on the electron density at the top of the pedestal, along the outer midplane, at radial position b2stbc_iyped. ndes_sol is the total particle content from the homonuclear sequence of species 'isfeedback' over the entire simulation domain. 
					It is governed, like nesepm_sol, by nesepm_overshoot and nesepm_alpha and corresponds to a SOL boundary feedback. volrec_sol is the total particle source due to volume recombination coming from Eirene. Its feedback is governed by volrec_overshoot and volrec_alpha and volrec_beta parameters (See Numerics section for the latter two). nesepm_pfr is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the PFR region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the PFR South boundary indices pfrregno1 and pfrregno2). 
					ndes is the total particle (neutrals + ions) content of the species whose neutral species has index isfeedback. This is controlled through particle input of neutrals species isfeedback through the 
					private flux boundaries (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2). private_flux_puff is the particle flow of species isfeedback through the private flux region boundary. This is controlled through particle input of neutrals species isfeedback through the private flux boundaris (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2). 
					All but the first of these feedback schemes ("nesepm") can also be run though an Eirene neutral gas puff. In that case, one should set an appropriate gas puffing stratum in the Eirene input file input.dat, as well as in the b2.neutrals.parameters file. The code will assume, unless told otherwise through the use of "eirene_nesepm_istra", that the first stratum of type 'C' found in b2.neutrals.parameters is the stratum used for the feedback. If "eirene_nesepm_istra" is set to a positive number, the code will consider the feedback stratum to be the stratum in the "eirene_nesepm_istra"-th position in b2.neutrals.parameters.
				""", '0'),
   
      'b2stbc_fchycore' : ('', 'real', """
					The 20 switches above are all feedback switches and require that b2stbc_feedback.ne.0 (See Run section for details) or that lfeedback=.true. in b2.boundary.parameters. The feedback is done as a boundary condition and is under-relaxed using the b2stbc_...._alpha switches (See Numerics section for details). 
					fheycore is the radial electron heat flow entering the core boundary. 
					fhiycore is the radial ion heat flow entering the core boundary. 
					fchycore is the radial current entering the core boundary. fnaycore is the radial flux of species "isfeedback" entering the core boundary. 
					If fhiycore_kinetic_energy.eq.1, the parallel kinetic energy flux is counted as part of the ion energy flux. 
					For double-null cases, the f..ycore variables contain the total flow through both core boundaries taken together. The core boundaries are identified by the coreregno and coreregn2 switches (see Geometry section). 
					The other seven switches are density feedback switches: nesepm is the outer midplane separatrix electron density. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is controlled through particle input of main plasma species isfeedback through the core boundary (See Geometry section for the core boundary indices coreregno and coreregn2). 
					nesepm_sol is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the SOL region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the SOL North boundary (See Geometry section for the SOL North boundary index solregno). If nesepm_overshoot.gt.1.0, the gas puff is turned off when the midplane separatrix density reaches nesepm*nesepm_overshoot. Minimum and maximum values of the feedback gas puff can be set using b2stbc_nesepm_minpuff and b2stbc_nesepm_maxpuff 
					nepedm_sol is similar to nesepm_sol but the feedback is exerted on the electron density at the top of the pedestal, along the outer midplane, at radial position b2stbc_iyped. ndes_sol is the total particle content from the homonuclear sequence of species 'isfeedback' over the entire simulation domain. 
					It is governed, like nesepm_sol, by nesepm_overshoot and nesepm_alpha and corresponds to a SOL boundary feedback. volrec_sol is the total particle source due to volume recombination coming from Eirene. Its feedback is governed by volrec_overshoot and volrec_alpha and volrec_beta parameters (See Numerics section for the latter two). nesepm_pfr is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the PFR region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the PFR South boundary indices pfrregno1 and pfrregno2). 
					ndes is the total particle (neutrals + ions) content of the species whose neutral species has index isfeedback. This is controlled through particle input of neutrals species isfeedback through the 
					private flux boundaries (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2). private_flux_puff is the particle flow of species isfeedback through the private flux region boundary. This is controlled through particle input of neutrals species isfeedback through the private flux boundaris (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2). 
					All but the first of these feedback schemes ("nesepm") can also be run though an Eirene neutral gas puff. In that case, one should set an appropriate gas puffing stratum in the Eirene input file input.dat, as well as in the b2.neutrals.parameters file. The code will assume, unless told otherwise through the use of "eirene_nesepm_istra", that the first stratum of type 'C' found in b2.neutrals.parameters is the stratum used for the feedback. If "eirene_nesepm_istra" is set to a positive number, the code will consider the feedback stratum to be the stratum in the "eirene_nesepm_istra"-th position in b2.neutrals.parameters.
				""", '-1.0e30'),
   
      'b2stbc_fnaycore' : ('', 'real', """
					The 20 switches above are all feedback switches and require that b2stbc_feedback.ne.0 (See Run section for details) or that lfeedback=.true. in b2.boundary.parameters. The feedback is done as a boundary condition and is under-relaxed using the b2stbc_...._alpha switches (See Numerics section for details). 
					fheycore is the radial electron heat flow entering the core boundary. 
					fhiycore is the radial ion heat flow entering the core boundary. 
					fchycore is the radial current entering the core boundary. fnaycore is the radial flux of species "isfeedback" entering the core boundary. 
					If fhiycore_kinetic_energy.eq.1, the parallel kinetic energy flux is counted as part of the ion energy flux. 
					For double-null cases, the f..ycore variables contain the total flow through both core boundaries taken together. The core boundaries are identified by the coreregno and coreregn2 switches (see Geometry section). 
					The other seven switches are density feedback switches: nesepm is the outer midplane separatrix electron density. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is controlled through particle input of main plasma species isfeedback through the core boundary (See Geometry section for the core boundary indices coreregno and coreregn2). 
					nesepm_sol is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the SOL region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the SOL North boundary (See Geometry section for the SOL North boundary index solregno). If nesepm_overshoot.gt.1.0, the gas puff is turned off when the midplane separatrix density reaches nesepm*nesepm_overshoot. Minimum and maximum values of the feedback gas puff can be set using b2stbc_nesepm_minpuff and b2stbc_nesepm_maxpuff 
					nepedm_sol is similar to nesepm_sol but the feedback is exerted on the electron density at the top of the pedestal, along the outer midplane, at radial position b2stbc_iyped. ndes_sol is the total particle content from the homonuclear sequence of species 'isfeedback' over the entire simulation domain. 
					It is governed, like nesepm_sol, by nesepm_overshoot and nesepm_alpha and corresponds to a SOL boundary feedback. volrec_sol is the total particle source due to volume recombination coming from Eirene. Its feedback is governed by volrec_overshoot and volrec_alpha and volrec_beta parameters (See Numerics section for the latter two). nesepm_pfr is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the PFR region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the PFR South boundary indices pfrregno1 and pfrregno2). 
					ndes is the total particle (neutrals + ions) content of the species whose neutral species has index isfeedback. This is controlled through particle input of neutrals species isfeedback through the 
					private flux boundaries (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2). private_flux_puff is the particle flow of species isfeedback through the private flux region boundary. This is controlled through particle input of neutrals species isfeedback through the private flux boundaris (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2). 
					All but the first of these feedback schemes ("nesepm") can also be run though an Eirene neutral gas puff. In that case, one should set an appropriate gas puffing stratum in the Eirene input file input.dat, as well as in the b2.neutrals.parameters file. The code will assume, unless told otherwise through the use of "eirene_nesepm_istra", that the first stratum of type 'C' found in b2.neutrals.parameters is the stratum used for the feedback. If "eirene_nesepm_istra" is set to a positive number, the code will consider the feedback stratum to be the stratum in the "eirene_nesepm_istra"-th position in b2.neutrals.parameters.
				""", '-1.0e30'),
   
      'b2stbc_isfeedback' : ('', 'integer', """
					The 20 switches above are all feedback switches and require that b2stbc_feedback.ne.0 (See Run section for details) or that lfeedback=.true. in b2.boundary.parameters. The feedback is done as a boundary condition and is under-relaxed using the b2stbc_...._alpha switches (See Numerics section for details). 
					fheycore is the radial electron heat flow entering the core boundary. 
					fhiycore is the radial ion heat flow entering the core boundary. 
					fchycore is the radial current entering the core boundary. fnaycore is the radial flux of species "isfeedback" entering the core boundary. 
					If fhiycore_kinetic_energy.eq.1, the parallel kinetic energy flux is counted as part of the ion energy flux. 
					For double-null cases, the f..ycore variables contain the total flow through both core boundaries taken together. The core boundaries are identified by the coreregno and coreregn2 switches (see Geometry section). 
					The other seven switches are density feedback switches: nesepm is the outer midplane separatrix electron density. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is controlled through particle input of main plasma species isfeedback through the core boundary (See Geometry section for the core boundary indices coreregno and coreregn2). 
					nesepm_sol is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the SOL region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the SOL North boundary (See Geometry section for the SOL North boundary index solregno). If nesepm_overshoot.gt.1.0, the gas puff is turned off when the midplane separatrix density reaches nesepm*nesepm_overshoot. Minimum and maximum values of the feedback gas puff can be set using b2stbc_nesepm_minpuff and b2stbc_nesepm_maxpuff 
					nepedm_sol is similar to nesepm_sol but the feedback is exerted on the electron density at the top of the pedestal, along the outer midplane, at radial position b2stbc_iyped. ndes_sol is the total particle content from the homonuclear sequence of species 'isfeedback' over the entire simulation domain. 
					It is governed, like nesepm_sol, by nesepm_overshoot and nesepm_alpha and corresponds to a SOL boundary feedback. volrec_sol is the total particle source due to volume recombination coming from Eirene. Its feedback is governed by volrec_overshoot and volrec_alpha and volrec_beta parameters (See Numerics section for the latter two). nesepm_pfr is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the PFR region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the PFR South boundary indices pfrregno1 and pfrregno2). 
					ndes is the total particle (neutrals + ions) content of the species whose neutral species has index isfeedback. This is controlled through particle input of neutrals species isfeedback through the 
					private flux boundaries (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2). private_flux_puff is the particle flow of species isfeedback through the private flux region boundary. This is controlled through particle input of neutrals species isfeedback through the private flux boundaris (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2). 
					All but the first of these feedback schemes ("nesepm") can also be run though an Eirene neutral gas puff. In that case, one should set an appropriate gas puffing stratum in the Eirene input file input.dat, as well as in the b2.neutrals.parameters file. The code will assume, unless told otherwise through the use of "eirene_nesepm_istra", that the first stratum of type 'C' found in b2.neutrals.parameters is the stratum used for the feedback. If "eirene_nesepm_istra" is set to a positive number, the code will consider the feedback stratum to be the stratum in the "eirene_nesepm_istra"-th position in b2.neutrals.parameters.
				""", '0'),
   
      'b2stbc_iyped' : ('', 'real', """
					The 20 switches above are all feedback switches and require that b2stbc_feedback.ne.0 (See Run section for details) or that lfeedback=.true. in b2.boundary.parameters. The feedback is done as a boundary condition and is under-relaxed using the b2stbc_...._alpha switches (See Numerics section for details). 
					fheycore is the radial electron heat flow entering the core boundary. 
					fhiycore is the radial ion heat flow entering the core boundary. 
					fchycore is the radial current entering the core boundary. fnaycore is the radial flux of species "isfeedback" entering the core boundary. 
					If fhiycore_kinetic_energy.eq.1, the parallel kinetic energy flux is counted as part of the ion energy flux. 
					For double-null cases, the f..ycore variables contain the total flow through both core boundaries taken together. The core boundaries are identified by the coreregno and coreregn2 switches (see Geometry section). 
					The other seven switches are density feedback switches: nesepm is the outer midplane separatrix electron density. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is controlled through particle input of main plasma species isfeedback through the core boundary (See Geometry section for the core boundary indices coreregno and coreregn2). 
					nesepm_sol is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the SOL region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the SOL North boundary (See Geometry section for the SOL North boundary index solregno). If nesepm_overshoot.gt.1.0, the gas puff is turned off when the midplane separatrix density reaches nesepm*nesepm_overshoot. Minimum and maximum values of the feedback gas puff can be set using b2stbc_nesepm_minpuff and b2stbc_nesepm_maxpuff 
					nepedm_sol is similar to nesepm_sol but the feedback is exerted on the electron density at the top of the pedestal, along the outer midplane, at radial position b2stbc_iyped. ndes_sol is the total particle content from the homonuclear sequence of species 'isfeedback' over the entire simulation domain. 
					It is governed, like nesepm_sol, by nesepm_overshoot and nesepm_alpha and corresponds to a SOL boundary feedback. volrec_sol is the total particle source due to volume recombination coming from Eirene. Its feedback is governed by volrec_overshoot and volrec_alpha and volrec_beta parameters (See Numerics section for the latter two). nesepm_pfr is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the PFR region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the PFR South boundary indices pfrregno1 and pfrregno2). 
					ndes is the total particle (neutrals + ions) content of the species whose neutral species has index isfeedback. This is controlled through particle input of neutrals species isfeedback through the 
					private flux boundaries (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2). private_flux_puff is the particle flow of species isfeedback through the private flux region boundary. This is controlled through particle input of neutrals species isfeedback through the private flux boundaris (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2). 
					All but the first of these feedback schemes ("nesepm") can also be run though an Eirene neutral gas puff. In that case, one should set an appropriate gas puffing stratum in the Eirene input file input.dat, as well as in the b2.neutrals.parameters file. The code will assume, unless told otherwise through the use of "eirene_nesepm_istra", that the first stratum of type 'C' found in b2.neutrals.parameters is the stratum used for the feedback. If "eirene_nesepm_istra" is set to a positive number, the code will consider the feedback stratum to be the stratum in the "eirene_nesepm_istra"-th position in b2.neutrals.parameters.
				""", 'jsep/2'),
   
      'b2stbc_ndes' : ('', 'real', """
					The 20 switches above are all feedback switches and require that b2stbc_feedback.ne.0 (See Run section for details) or that lfeedback=.true. in b2.boundary.parameters. The feedback is done as a boundary condition and is under-relaxed using the b2stbc_...._alpha switches (See Numerics section for details). 
					fheycore is the radial electron heat flow entering the core boundary. 
					fhiycore is the radial ion heat flow entering the core boundary. 
					fchycore is the radial current entering the core boundary. fnaycore is the radial flux of species "isfeedback" entering the core boundary. 
					If fhiycore_kinetic_energy.eq.1, the parallel kinetic energy flux is counted as part of the ion energy flux. 
					For double-null cases, the f..ycore variables contain the total flow through both core boundaries taken together. The core boundaries are identified by the coreregno and coreregn2 switches (see Geometry section). 
					The other seven switches are density feedback switches: nesepm is the outer midplane separatrix electron density. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is controlled through particle input of main plasma species isfeedback through the core boundary (See Geometry section for the core boundary indices coreregno and coreregn2). 
					nesepm_sol is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the SOL region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the SOL North boundary (See Geometry section for the SOL North boundary index solregno). If nesepm_overshoot.gt.1.0, the gas puff is turned off when the midplane separatrix density reaches nesepm*nesepm_overshoot. Minimum and maximum values of the feedback gas puff can be set using b2stbc_nesepm_minpuff and b2stbc_nesepm_maxpuff 
					nepedm_sol is similar to nesepm_sol but the feedback is exerted on the electron density at the top of the pedestal, along the outer midplane, at radial position b2stbc_iyped. ndes_sol is the total particle content from the homonuclear sequence of species 'isfeedback' over the entire simulation domain. 
					It is governed, like nesepm_sol, by nesepm_overshoot and nesepm_alpha and corresponds to a SOL boundary feedback. volrec_sol is the total particle source due to volume recombination coming from Eirene. Its feedback is governed by volrec_overshoot and volrec_alpha and volrec_beta parameters (See Numerics section for the latter two). nesepm_pfr is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the PFR region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the PFR South boundary indices pfrregno1 and pfrregno2). 
					ndes is the total particle (neutrals + ions) content of the species whose neutral species has index isfeedback. This is controlled through particle input of neutrals species isfeedback through the 
					private flux boundaries (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2). private_flux_puff is the particle flow of species isfeedback through the private flux region boundary. This is controlled through particle input of neutrals species isfeedback through the private flux boundaris (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2). 
					All but the first of these feedback schemes ("nesepm") can also be run though an Eirene neutral gas puff. In that case, one should set an appropriate gas puffing stratum in the Eirene input file input.dat, as well as in the b2.neutrals.parameters file. The code will assume, unless told otherwise through the use of "eirene_nesepm_istra", that the first stratum of type 'C' found in b2.neutrals.parameters is the stratum used for the feedback. If "eirene_nesepm_istra" is set to a positive number, the code will consider the feedback stratum to be the stratum in the "eirene_nesepm_istra"-th position in b2.neutrals.parameters.
				""", '0.0'),
   
      'b2stbc_ndes_sol' : ('', 'real', """
					The 20 switches above are all feedback switches and require that b2stbc_feedback.ne.0 (See Run section for details) or that lfeedback=.true. in b2.boundary.parameters. The feedback is done as a boundary condition and is under-relaxed using the b2stbc_...._alpha switches (See Numerics section for details). 
					fheycore is the radial electron heat flow entering the core boundary. 
					fhiycore is the radial ion heat flow entering the core boundary. 
					fchycore is the radial current entering the core boundary. fnaycore is the radial flux of species "isfeedback" entering the core boundary. 
					If fhiycore_kinetic_energy.eq.1, the parallel kinetic energy flux is counted as part of the ion energy flux. 
					For double-null cases, the f..ycore variables contain the total flow through both core boundaries taken together. The core boundaries are identified by the coreregno and coreregn2 switches (see Geometry section). 
					The other seven switches are density feedback switches: nesepm is the outer midplane separatrix electron density. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is controlled through particle input of main plasma species isfeedback through the core boundary (See Geometry section for the core boundary indices coreregno and coreregn2). 
					nesepm_sol is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the SOL region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the SOL North boundary (See Geometry section for the SOL North boundary index solregno). If nesepm_overshoot.gt.1.0, the gas puff is turned off when the midplane separatrix density reaches nesepm*nesepm_overshoot. Minimum and maximum values of the feedback gas puff can be set using b2stbc_nesepm_minpuff and b2stbc_nesepm_maxpuff 
					nepedm_sol is similar to nesepm_sol but the feedback is exerted on the electron density at the top of the pedestal, along the outer midplane, at radial position b2stbc_iyped. ndes_sol is the total particle content from the homonuclear sequence of species 'isfeedback' over the entire simulation domain. 
					It is governed, like nesepm_sol, by nesepm_overshoot and nesepm_alpha and corresponds to a SOL boundary feedback. volrec_sol is the total particle source due to volume recombination coming from Eirene. Its feedback is governed by volrec_overshoot and volrec_alpha and volrec_beta parameters (See Numerics section for the latter two). nesepm_pfr is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the PFR region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the PFR South boundary indices pfrregno1 and pfrregno2). 
					ndes is the total particle (neutrals + ions) content of the species whose neutral species has index isfeedback. This is controlled through particle input of neutrals species isfeedback through the 
					private flux boundaries (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2). private_flux_puff is the particle flow of species isfeedback through the private flux region boundary. This is controlled through particle input of neutrals species isfeedback through the private flux boundaris (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2). 
					All but the first of these feedback schemes ("nesepm") can also be run though an Eirene neutral gas puff. In that case, one should set an appropriate gas puffing stratum in the Eirene input file input.dat, as well as in the b2.neutrals.parameters file. The code will assume, unless told otherwise through the use of "eirene_nesepm_istra", that the first stratum of type 'C' found in b2.neutrals.parameters is the stratum used for the feedback. If "eirene_nesepm_istra" is set to a positive number, the code will consider the feedback stratum to be the stratum in the "eirene_nesepm_istra"-th position in b2.neutrals.parameters.
				""", '0.0'),
   
      'b2stbc_nepedm_sol' : ('', 'real', """
					The 20 switches above are all feedback switches and require that b2stbc_feedback.ne.0 (See Run section for details) or that lfeedback=.true. in b2.boundary.parameters. The feedback is done as a boundary condition and is under-relaxed using the b2stbc_...._alpha switches (See Numerics section for details). 
					fheycore is the radial electron heat flow entering the core boundary. 
					fhiycore is the radial ion heat flow entering the core boundary. 
					fchycore is the radial current entering the core boundary. fnaycore is the radial flux of species "isfeedback" entering the core boundary. 
					If fhiycore_kinetic_energy.eq.1, the parallel kinetic energy flux is counted as part of the ion energy flux. 
					For double-null cases, the f..ycore variables contain the total flow through both core boundaries taken together. The core boundaries are identified by the coreregno and coreregn2 switches (see Geometry section). 
					The other seven switches are density feedback switches: nesepm is the outer midplane separatrix electron density. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is controlled through particle input of main plasma species isfeedback through the core boundary (See Geometry section for the core boundary indices coreregno and coreregn2). 
					nesepm_sol is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the SOL region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the SOL North boundary (See Geometry section for the SOL North boundary index solregno). If nesepm_overshoot.gt.1.0, the gas puff is turned off when the midplane separatrix density reaches nesepm*nesepm_overshoot. Minimum and maximum values of the feedback gas puff can be set using b2stbc_nesepm_minpuff and b2stbc_nesepm_maxpuff 
					nepedm_sol is similar to nesepm_sol but the feedback is exerted on the electron density at the top of the pedestal, along the outer midplane, at radial position b2stbc_iyped. ndes_sol is the total particle content from the homonuclear sequence of species 'isfeedback' over the entire simulation domain. 
					It is governed, like nesepm_sol, by nesepm_overshoot and nesepm_alpha and corresponds to a SOL boundary feedback. volrec_sol is the total particle source due to volume recombination coming from Eirene. Its feedback is governed by volrec_overshoot and volrec_alpha and volrec_beta parameters (See Numerics section for the latter two). nesepm_pfr is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the PFR region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the PFR South boundary indices pfrregno1 and pfrregno2). 
					ndes is the total particle (neutrals + ions) content of the species whose neutral species has index isfeedback. This is controlled through particle input of neutrals species isfeedback through the 
					private flux boundaries (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2). private_flux_puff is the particle flow of species isfeedback through the private flux region boundary. This is controlled through particle input of neutrals species isfeedback through the private flux boundaris (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2). 
					All but the first of these feedback schemes ("nesepm") can also be run though an Eirene neutral gas puff. In that case, one should set an appropriate gas puffing stratum in the Eirene input file input.dat, as well as in the b2.neutrals.parameters file. The code will assume, unless told otherwise through the use of "eirene_nesepm_istra", that the first stratum of type 'C' found in b2.neutrals.parameters is the stratum used for the feedback. If "eirene_nesepm_istra" is set to a positive number, the code will consider the feedback stratum to be the stratum in the "eirene_nesepm_istra"-th position in b2.neutrals.parameters.
				""", '0.0'),
   
      'b2stbc_nesepm' : ('', 'real', """
					The 20 switches above are all feedback switches and require that b2stbc_feedback.ne.0 (See Run section for details) or that lfeedback=.true. in b2.boundary.parameters. The feedback is done as a boundary condition and is under-relaxed using the b2stbc_...._alpha switches (See Numerics section for details). 
					fheycore is the radial electron heat flow entering the core boundary. 
					fhiycore is the radial ion heat flow entering the core boundary. 
					fchycore is the radial current entering the core boundary. fnaycore is the radial flux of species "isfeedback" entering the core boundary. 
					If fhiycore_kinetic_energy.eq.1, the parallel kinetic energy flux is counted as part of the ion energy flux. 
					For double-null cases, the f..ycore variables contain the total flow through both core boundaries taken together. The core boundaries are identified by the coreregno and coreregn2 switches (see Geometry section). 
					The other seven switches are density feedback switches: nesepm is the outer midplane separatrix electron density. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is controlled through particle input of main plasma species isfeedback through the core boundary (See Geometry section for the core boundary indices coreregno and coreregn2). 
					nesepm_sol is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the SOL region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the SOL North boundary (See Geometry section for the SOL North boundary index solregno). If nesepm_overshoot.gt.1.0, the gas puff is turned off when the midplane separatrix density reaches nesepm*nesepm_overshoot. Minimum and maximum values of the feedback gas puff can be set using b2stbc_nesepm_minpuff and b2stbc_nesepm_maxpuff 
					nepedm_sol is similar to nesepm_sol but the feedback is exerted on the electron density at the top of the pedestal, along the outer midplane, at radial position b2stbc_iyped. ndes_sol is the total particle content from the homonuclear sequence of species 'isfeedback' over the entire simulation domain. 
					It is governed, like nesepm_sol, by nesepm_overshoot and nesepm_alpha and corresponds to a SOL boundary feedback. volrec_sol is the total particle source due to volume recombination coming from Eirene. Its feedback is governed by volrec_overshoot and volrec_alpha and volrec_beta parameters (See Numerics section for the latter two). nesepm_pfr is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the PFR region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the PFR South boundary indices pfrregno1 and pfrregno2). 
					ndes is the total particle (neutrals + ions) content of the species whose neutral species has index isfeedback. This is controlled through particle input of neutrals species isfeedback through the 
					private flux boundaries (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2). private_flux_puff is the particle flow of species isfeedback through the private flux region boundary. This is controlled through particle input of neutrals species isfeedback through the private flux boundaris (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2). 
					All but the first of these feedback schemes ("nesepm") can also be run though an Eirene neutral gas puff. In that case, one should set an appropriate gas puffing stratum in the Eirene input file input.dat, as well as in the b2.neutrals.parameters file. The code will assume, unless told otherwise through the use of "eirene_nesepm_istra", that the first stratum of type 'C' found in b2.neutrals.parameters is the stratum used for the feedback. If "eirene_nesepm_istra" is set to a positive number, the code will consider the feedback stratum to be the stratum in the "eirene_nesepm_istra"-th position in b2.neutrals.parameters.
				""", '0.0'),
   
      'b2stbc_nesepm_overshoot' : ('', 'real', """
					The 20 switches above are all feedback switches and require that b2stbc_feedback.ne.0 (See Run section for details) or that lfeedback=.true. in b2.boundary.parameters. The feedback is done as a boundary condition and is under-relaxed using the b2stbc_...._alpha switches (See Numerics section for details). 
					fheycore is the radial electron heat flow entering the core boundary. 
					fhiycore is the radial ion heat flow entering the core boundary. 
					fchycore is the radial current entering the core boundary. fnaycore is the radial flux of species "isfeedback" entering the core boundary. 
					If fhiycore_kinetic_energy.eq.1, the parallel kinetic energy flux is counted as part of the ion energy flux. 
					For double-null cases, the f..ycore variables contain the total flow through both core boundaries taken together. The core boundaries are identified by the coreregno and coreregn2 switches (see Geometry section). 
					The other seven switches are density feedback switches: nesepm is the outer midplane separatrix electron density. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is controlled through particle input of main plasma species isfeedback through the core boundary (See Geometry section for the core boundary indices coreregno and coreregn2). 
					nesepm_sol is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the SOL region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the SOL North boundary (See Geometry section for the SOL North boundary index solregno). If nesepm_overshoot.gt.1.0, the gas puff is turned off when the midplane separatrix density reaches nesepm*nesepm_overshoot. Minimum and maximum values of the feedback gas puff can be set using b2stbc_nesepm_minpuff and b2stbc_nesepm_maxpuff 
					nepedm_sol is similar to nesepm_sol but the feedback is exerted on the electron density at the top of the pedestal, along the outer midplane, at radial position b2stbc_iyped. ndes_sol is the total particle content from the homonuclear sequence of species 'isfeedback' over the entire simulation domain. 
					It is governed, like nesepm_sol, by nesepm_overshoot and nesepm_alpha and corresponds to a SOL boundary feedback. volrec_sol is the total particle source due to volume recombination coming from Eirene. Its feedback is governed by volrec_overshoot and volrec_alpha and volrec_beta parameters (See Numerics section for the latter two). nesepm_pfr is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the PFR region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the PFR South boundary indices pfrregno1 and pfrregno2). 
					ndes is the total particle (neutrals + ions) content of the species whose neutral species has index isfeedback. This is controlled through particle input of neutrals species isfeedback through the 
					private flux boundaries (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2). private_flux_puff is the particle flow of species isfeedback through the private flux region boundary. This is controlled through particle input of neutrals species isfeedback through the private flux boundaris (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2). 
					All but the first of these feedback schemes ("nesepm") can also be run though an Eirene neutral gas puff. In that case, one should set an appropriate gas puffing stratum in the Eirene input file input.dat, as well as in the b2.neutrals.parameters file. The code will assume, unless told otherwise through the use of "eirene_nesepm_istra", that the first stratum of type 'C' found in b2.neutrals.parameters is the stratum used for the feedback. If "eirene_nesepm_istra" is set to a positive number, the code will consider the feedback stratum to be the stratum in the "eirene_nesepm_istra"-th position in b2.neutrals.parameters.
				""", '0.0'),
   
      'b2stbc_nesepm_pfr' : ('', 'real', """
					The 20 switches above are all feedback switches and require that b2stbc_feedback.ne.0 (See Run section for details) or that lfeedback=.true. in b2.boundary.parameters. The feedback is done as a boundary condition and is under-relaxed using the b2stbc_...._alpha switches (See Numerics section for details). 
					fheycore is the radial electron heat flow entering the core boundary. 
					fhiycore is the radial ion heat flow entering the core boundary. 
					fchycore is the radial current entering the core boundary. fnaycore is the radial flux of species "isfeedback" entering the core boundary. 
					If fhiycore_kinetic_energy.eq.1, the parallel kinetic energy flux is counted as part of the ion energy flux. 
					For double-null cases, the f..ycore variables contain the total flow through both core boundaries taken together. The core boundaries are identified by the coreregno and coreregn2 switches (see Geometry section). 
					The other seven switches are density feedback switches: nesepm is the outer midplane separatrix electron density. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is controlled through particle input of main plasma species isfeedback through the core boundary (See Geometry section for the core boundary indices coreregno and coreregn2). 
					nesepm_sol is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the SOL region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the SOL North boundary (See Geometry section for the SOL North boundary index solregno). If nesepm_overshoot.gt.1.0, the gas puff is turned off when the midplane separatrix density reaches nesepm*nesepm_overshoot. Minimum and maximum values of the feedback gas puff can be set using b2stbc_nesepm_minpuff and b2stbc_nesepm_maxpuff 
					nepedm_sol is similar to nesepm_sol but the feedback is exerted on the electron density at the top of the pedestal, along the outer midplane, at radial position b2stbc_iyped. ndes_sol is the total particle content from the homonuclear sequence of species 'isfeedback' over the entire simulation domain. 
					It is governed, like nesepm_sol, by nesepm_overshoot and nesepm_alpha and corresponds to a SOL boundary feedback. volrec_sol is the total particle source due to volume recombination coming from Eirene. Its feedback is governed by volrec_overshoot and volrec_alpha and volrec_beta parameters (See Numerics section for the latter two). nesepm_pfr is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the PFR region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the PFR South boundary indices pfrregno1 and pfrregno2). 
					ndes is the total particle (neutrals + ions) content of the species whose neutral species has index isfeedback. This is controlled through particle input of neutrals species isfeedback through the 
					private flux boundaries (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2). private_flux_puff is the particle flow of species isfeedback through the private flux region boundary. This is controlled through particle input of neutrals species isfeedback through the private flux boundaris (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2). 
					All but the first of these feedback schemes ("nesepm") can also be run though an Eirene neutral gas puff. In that case, one should set an appropriate gas puffing stratum in the Eirene input file input.dat, as well as in the b2.neutrals.parameters file. The code will assume, unless told otherwise through the use of "eirene_nesepm_istra", that the first stratum of type 'C' found in b2.neutrals.parameters is the stratum used for the feedback. If "eirene_nesepm_istra" is set to a positive number, the code will consider the feedback stratum to be the stratum in the "eirene_nesepm_istra"-th position in b2.neutrals.parameters.
				""", '0.0'),
   
      'b2stbc_nesepm_sol' : ('', 'real', """
					The 20 switches above are all feedback switches and require that b2stbc_feedback.ne.0 (See Run section for details) or that lfeedback=.true. in b2.boundary.parameters. The feedback is done as a boundary condition and is under-relaxed using the b2stbc_...._alpha switches (See Numerics section for details). 
					fheycore is the radial electron heat flow entering the core boundary. 
					fhiycore is the radial ion heat flow entering the core boundary. 
					fchycore is the radial current entering the core boundary. fnaycore is the radial flux of species "isfeedback" entering the core boundary. 
					If fhiycore_kinetic_energy.eq.1, the parallel kinetic energy flux is counted as part of the ion energy flux. 
					For double-null cases, the f..ycore variables contain the total flow through both core boundaries taken together. The core boundaries are identified by the coreregno and coreregn2 switches (see Geometry section). 
					The other seven switches are density feedback switches: nesepm is the outer midplane separatrix electron density. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is controlled through particle input of main plasma species isfeedback through the core boundary (See Geometry section for the core boundary indices coreregno and coreregn2). 
					nesepm_sol is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the SOL region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the SOL North boundary (See Geometry section for the SOL North boundary index solregno). If nesepm_overshoot.gt.1.0, the gas puff is turned off when the midplane separatrix density reaches nesepm*nesepm_overshoot. Minimum and maximum values of the feedback gas puff can be set using b2stbc_nesepm_minpuff and b2stbc_nesepm_maxpuff 
					nepedm_sol is similar to nesepm_sol but the feedback is exerted on the electron density at the top of the pedestal, along the outer midplane, at radial position b2stbc_iyped. ndes_sol is the total particle content from the homonuclear sequence of species 'isfeedback' over the entire simulation domain. 
					It is governed, like nesepm_sol, by nesepm_overshoot and nesepm_alpha and corresponds to a SOL boundary feedback. volrec_sol is the total particle source due to volume recombination coming from Eirene. Its feedback is governed by volrec_overshoot and volrec_alpha and volrec_beta parameters (See Numerics section for the latter two). nesepm_pfr is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the PFR region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the PFR South boundary indices pfrregno1 and pfrregno2). 
					ndes is the total particle (neutrals + ions) content of the species whose neutral species has index isfeedback. This is controlled through particle input of neutrals species isfeedback through the 
					private flux boundaries (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2). private_flux_puff is the particle flow of species isfeedback through the private flux region boundary. This is controlled through particle input of neutrals species isfeedback through the private flux boundaris (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2). 
					All but the first of these feedback schemes ("nesepm") can also be run though an Eirene neutral gas puff. In that case, one should set an appropriate gas puffing stratum in the Eirene input file input.dat, as well as in the b2.neutrals.parameters file. The code will assume, unless told otherwise through the use of "eirene_nesepm_istra", that the first stratum of type 'C' found in b2.neutrals.parameters is the stratum used for the feedback. If "eirene_nesepm_istra" is set to a positive number, the code will consider the feedback stratum to be the stratum in the "eirene_nesepm_istra"-th position in b2.neutrals.parameters.
				""", '0.0'),
   
      'b2stbc_private_flux_puff' : ('', 'real', """
					The 20 switches above are all feedback switches and require that b2stbc_feedback.ne.0 (See Run section for details) or that lfeedback=.true. in b2.boundary.parameters. The feedback is done as a boundary condition and is under-relaxed using the b2stbc_...._alpha switches (See Numerics section for details). 
					fheycore is the radial electron heat flow entering the core boundary. 
					fhiycore is the radial ion heat flow entering the core boundary. 
					fchycore is the radial current entering the core boundary. fnaycore is the radial flux of species "isfeedback" entering the core boundary. 
					If fhiycore_kinetic_energy.eq.1, the parallel kinetic energy flux is counted as part of the ion energy flux. 
					For double-null cases, the f..ycore variables contain the total flow through both core boundaries taken together. The core boundaries are identified by the coreregno and coreregn2 switches (see Geometry section). 
					The other seven switches are density feedback switches: nesepm is the outer midplane separatrix electron density. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is controlled through particle input of main plasma species isfeedback through the core boundary (See Geometry section for the core boundary indices coreregno and coreregn2). 
					nesepm_sol is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the SOL region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the SOL North boundary (See Geometry section for the SOL North boundary index solregno). If nesepm_overshoot.gt.1.0, the gas puff is turned off when the midplane separatrix density reaches nesepm*nesepm_overshoot. Minimum and maximum values of the feedback gas puff can be set using b2stbc_nesepm_minpuff and b2stbc_nesepm_maxpuff 
					nepedm_sol is similar to nesepm_sol but the feedback is exerted on the electron density at the top of the pedestal, along the outer midplane, at radial position b2stbc_iyped. ndes_sol is the total particle content from the homonuclear sequence of species 'isfeedback' over the entire simulation domain. 
					It is governed, like nesepm_sol, by nesepm_overshoot and nesepm_alpha and corresponds to a SOL boundary feedback. volrec_sol is the total particle source due to volume recombination coming from Eirene. Its feedback is governed by volrec_overshoot and volrec_alpha and volrec_beta parameters (See Numerics section for the latter two). nesepm_pfr is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the PFR region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the PFR South boundary indices pfrregno1 and pfrregno2). 
					ndes is the total particle (neutrals + ions) content of the species whose neutral species has index isfeedback. This is controlled through particle input of neutrals species isfeedback through the 
					private flux boundaries (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2). private_flux_puff is the particle flow of species isfeedback through the private flux region boundary. This is controlled through particle input of neutrals species isfeedback through the private flux boundaris (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2). 
					All but the first of these feedback schemes ("nesepm") can also be run though an Eirene neutral gas puff. In that case, one should set an appropriate gas puffing stratum in the Eirene input file input.dat, as well as in the b2.neutrals.parameters file. The code will assume, unless told otherwise through the use of "eirene_nesepm_istra", that the first stratum of type 'C' found in b2.neutrals.parameters is the stratum used for the feedback. If "eirene_nesepm_istra" is set to a positive number, the code will consider the feedback stratum to be the stratum in the "eirene_nesepm_istra"-th position in b2.neutrals.parameters.
				""", '0.0'),
   
      'b2stbc_volrec' : ('', 'real', """
					The 20 switches above are all feedback switches and require that b2stbc_feedback.ne.0 (See Run section for details) or that lfeedback=.true. in b2.boundary.parameters. The feedback is done as a boundary condition and is under-relaxed using the b2stbc_...._alpha switches (See Numerics section for details). 
					fheycore is the radial electron heat flow entering the core boundary. 
					fhiycore is the radial ion heat flow entering the core boundary. 
					fchycore is the radial current entering the core boundary. fnaycore is the radial flux of species "isfeedback" entering the core boundary. 
					If fhiycore_kinetic_energy.eq.1, the parallel kinetic energy flux is counted as part of the ion energy flux. 
					For double-null cases, the f..ycore variables contain the total flow through both core boundaries taken together. The core boundaries are identified by the coreregno and coreregn2 switches (see Geometry section). 
					The other seven switches are density feedback switches: nesepm is the outer midplane separatrix electron density. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is controlled through particle input of main plasma species isfeedback through the core boundary (See Geometry section for the core boundary indices coreregno and coreregn2). 
					nesepm_sol is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the SOL region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the SOL North boundary (See Geometry section for the SOL North boundary index solregno). If nesepm_overshoot.gt.1.0, the gas puff is turned off when the midplane separatrix density reaches nesepm*nesepm_overshoot. Minimum and maximum values of the feedback gas puff can be set using b2stbc_nesepm_minpuff and b2stbc_nesepm_maxpuff 
					nepedm_sol is similar to nesepm_sol but the feedback is exerted on the electron density at the top of the pedestal, along the outer midplane, at radial position b2stbc_iyped. ndes_sol is the total particle content from the homonuclear sequence of species 'isfeedback' over the entire simulation domain. 
					It is governed, like nesepm_sol, by nesepm_overshoot and nesepm_alpha and corresponds to a SOL boundary feedback. volrec_sol is the total particle source due to volume recombination coming from Eirene. Its feedback is governed by volrec_overshoot and volrec_alpha and volrec_beta parameters (See Numerics section for the latter two). nesepm_pfr is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the PFR region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the PFR South boundary indices pfrregno1 and pfrregno2). 
					ndes is the total particle (neutrals + ions) content of the species whose neutral species has index isfeedback. This is controlled through particle input of neutrals species isfeedback through the 
					private flux boundaries (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2). private_flux_puff is the particle flow of species isfeedback through the private flux region boundary. This is controlled through particle input of neutrals species isfeedback through the private flux boundaris (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2). 
					All but the first of these feedback schemes ("nesepm") can also be run though an Eirene neutral gas puff. In that case, one should set an appropriate gas puffing stratum in the Eirene input file input.dat, as well as in the b2.neutrals.parameters file. The code will assume, unless told otherwise through the use of "eirene_nesepm_istra", that the first stratum of type 'C' found in b2.neutrals.parameters is the stratum used for the feedback. If "eirene_nesepm_istra" is set to a positive number, the code will consider the feedback stratum to be the stratum in the "eirene_nesepm_istra"-th position in b2.neutrals.parameters.
				""", '0.0'),
   
      'b2stbc_volrec_overshoot' : ('', 'real', """
					The 20 switches above are all feedback switches and require that b2stbc_feedback.ne.0 (See Run section for details) or that lfeedback=.true. in b2.boundary.parameters. The feedback is done as a boundary condition and is under-relaxed using the b2stbc_...._alpha switches (See Numerics section for details). 
					fheycore is the radial electron heat flow entering the core boundary. 
					fhiycore is the radial ion heat flow entering the core boundary. 
					fchycore is the radial current entering the core boundary. fnaycore is the radial flux of species "isfeedback" entering the core boundary. 
					If fhiycore_kinetic_energy.eq.1, the parallel kinetic energy flux is counted as part of the ion energy flux. 
					For double-null cases, the f..ycore variables contain the total flow through both core boundaries taken together. The core boundaries are identified by the coreregno and coreregn2 switches (see Geometry section). 
					The other seven switches are density feedback switches: nesepm is the outer midplane separatrix electron density. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is controlled through particle input of main plasma species isfeedback through the core boundary (See Geometry section for the core boundary indices coreregno and coreregn2). 
					nesepm_sol is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the SOL region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the SOL North boundary (See Geometry section for the SOL North boundary index solregno). If nesepm_overshoot.gt.1.0, the gas puff is turned off when the midplane separatrix density reaches nesepm*nesepm_overshoot. Minimum and maximum values of the feedback gas puff can be set using b2stbc_nesepm_minpuff and b2stbc_nesepm_maxpuff 
					nepedm_sol is similar to nesepm_sol but the feedback is exerted on the electron density at the top of the pedestal, along the outer midplane, at radial position b2stbc_iyped. ndes_sol is the total particle content from the homonuclear sequence of species 'isfeedback' over the entire simulation domain. 
					It is governed, like nesepm_sol, by nesepm_overshoot and nesepm_alpha and corresponds to a SOL boundary feedback. volrec_sol is the total particle source due to volume recombination coming from Eirene. Its feedback is governed by volrec_overshoot and volrec_alpha and volrec_beta parameters (See Numerics section for the latter two). nesepm_pfr is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the PFR region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the PFR South boundary indices pfrregno1 and pfrregno2). 
					ndes is the total particle (neutrals + ions) content of the species whose neutral species has index isfeedback. This is controlled through particle input of neutrals species isfeedback through the 
					private flux boundaries (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2). private_flux_puff is the particle flow of species isfeedback through the private flux region boundary. This is controlled through particle input of neutrals species isfeedback through the private flux boundaris (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2). 
					All but the first of these feedback schemes ("nesepm") can also be run though an Eirene neutral gas puff. In that case, one should set an appropriate gas puffing stratum in the Eirene input file input.dat, as well as in the b2.neutrals.parameters file. The code will assume, unless told otherwise through the use of "eirene_nesepm_istra", that the first stratum of type 'C' found in b2.neutrals.parameters is the stratum used for the feedback. If "eirene_nesepm_istra" is set to a positive number, the code will consider the feedback stratum to be the stratum in the "eirene_nesepm_istra"-th position in b2.neutrals.parameters.
				""", '0.0'),
   
      'b2stbc_nesepm_minpuff' : ('', 'real', """
					The 20 switches above are all feedback switches and require that b2stbc_feedback.ne.0 (See Run section for details) or that lfeedback=.true. in b2.boundary.parameters. The feedback is done as a boundary condition and is under-relaxed using the b2stbc_...._alpha switches (See Numerics section for details). 
					fheycore is the radial electron heat flow entering the core boundary. 
					fhiycore is the radial ion heat flow entering the core boundary. 
					fchycore is the radial current entering the core boundary. fnaycore is the radial flux of species "isfeedback" entering the core boundary. 
					If fhiycore_kinetic_energy.eq.1, the parallel kinetic energy flux is counted as part of the ion energy flux. 
					For double-null cases, the f..ycore variables contain the total flow through both core boundaries taken together. The core boundaries are identified by the coreregno and coreregn2 switches (see Geometry section). 
					The other seven switches are density feedback switches: nesepm is the outer midplane separatrix electron density. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is controlled through particle input of main plasma species isfeedback through the core boundary (See Geometry section for the core boundary indices coreregno and coreregn2). 
					nesepm_sol is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the SOL region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the SOL North boundary (See Geometry section for the SOL North boundary index solregno). If nesepm_overshoot.gt.1.0, the gas puff is turned off when the midplane separatrix density reaches nesepm*nesepm_overshoot. Minimum and maximum values of the feedback gas puff can be set using b2stbc_nesepm_minpuff and b2stbc_nesepm_maxpuff 
					nepedm_sol is similar to nesepm_sol but the feedback is exerted on the electron density at the top of the pedestal, along the outer midplane, at radial position b2stbc_iyped. ndes_sol is the total particle content from the homonuclear sequence of species 'isfeedback' over the entire simulation domain. 
					It is governed, like nesepm_sol, by nesepm_overshoot and nesepm_alpha and corresponds to a SOL boundary feedback. volrec_sol is the total particle source due to volume recombination coming from Eirene. Its feedback is governed by volrec_overshoot and volrec_alpha and volrec_beta parameters (See Numerics section for the latter two). nesepm_pfr is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the PFR region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the PFR South boundary indices pfrregno1 and pfrregno2). 
					ndes is the total particle (neutrals + ions) content of the species whose neutral species has index isfeedback. This is controlled through particle input of neutrals species isfeedback through the 
					private flux boundaries (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2). private_flux_puff is the particle flow of species isfeedback through the private flux region boundary. This is controlled through particle input of neutrals species isfeedback through the private flux boundaris (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2). 
					All but the first of these feedback schemes ("nesepm") can also be run though an Eirene neutral gas puff. In that case, one should set an appropriate gas puffing stratum in the Eirene input file input.dat, as well as in the b2.neutrals.parameters file. The code will assume, unless told otherwise through the use of "eirene_nesepm_istra", that the first stratum of type 'C' found in b2.neutrals.parameters is the stratum used for the feedback. If "eirene_nesepm_istra" is set to a positive number, the code will consider the feedback stratum to be the stratum in the "eirene_nesepm_istra"-th position in b2.neutrals.parameters.
				""", '0.0'),
   
      'b2stbc_nesepm_maxpuff' : ('', 'real', """
					The 20 switches above are all feedback switches and require that b2stbc_feedback.ne.0 (See Run section for details) or that lfeedback=.true. in b2.boundary.parameters. The feedback is done as a boundary condition and is under-relaxed using the b2stbc_...._alpha switches (See Numerics section for details). 
					fheycore is the radial electron heat flow entering the core boundary. 
					fhiycore is the radial ion heat flow entering the core boundary. 
					fchycore is the radial current entering the core boundary. fnaycore is the radial flux of species "isfeedback" entering the core boundary. 
					If fhiycore_kinetic_energy.eq.1, the parallel kinetic energy flux is counted as part of the ion energy flux. 
					For double-null cases, the f..ycore variables contain the total flow through both core boundaries taken together. The core boundaries are identified by the coreregno and coreregn2 switches (see Geometry section). 
					The other seven switches are density feedback switches: nesepm is the outer midplane separatrix electron density. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is controlled through particle input of main plasma species isfeedback through the core boundary (See Geometry section for the core boundary indices coreregno and coreregn2). 
					nesepm_sol is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the SOL region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the SOL North boundary (See Geometry section for the SOL North boundary index solregno). If nesepm_overshoot.gt.1.0, the gas puff is turned off when the midplane separatrix density reaches nesepm*nesepm_overshoot. Minimum and maximum values of the feedback gas puff can be set using b2stbc_nesepm_minpuff and b2stbc_nesepm_maxpuff 
					nepedm_sol is similar to nesepm_sol but the feedback is exerted on the electron density at the top of the pedestal, along the outer midplane, at radial position b2stbc_iyped. ndes_sol is the total particle content from the homonuclear sequence of species 'isfeedback' over the entire simulation domain. 
					It is governed, like nesepm_sol, by nesepm_overshoot and nesepm_alpha and corresponds to a SOL boundary feedback. volrec_sol is the total particle source due to volume recombination coming from Eirene. Its feedback is governed by volrec_overshoot and volrec_alpha and volrec_beta parameters (See Numerics section for the latter two). nesepm_pfr is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the PFR region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the PFR South boundary indices pfrregno1 and pfrregno2). 
					ndes is the total particle (neutrals + ions) content of the species whose neutral species has index isfeedback. This is controlled through particle input of neutrals species isfeedback through the 
					private flux boundaries (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2). private_flux_puff is the particle flow of species isfeedback through the private flux region boundary. This is controlled through particle input of neutrals species isfeedback through the private flux boundaris (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2). 
					All but the first of these feedback schemes ("nesepm") can also be run though an Eirene neutral gas puff. In that case, one should set an appropriate gas puffing stratum in the Eirene input file input.dat, as well as in the b2.neutrals.parameters file. The code will assume, unless told otherwise through the use of "eirene_nesepm_istra", that the first stratum of type 'C' found in b2.neutrals.parameters is the stratum used for the feedback. If "eirene_nesepm_istra" is set to a positive number, the code will consider the feedback stratum to be the stratum in the "eirene_nesepm_istra"-th position in b2.neutrals.parameters.
				""", '0.0'),
   
      'eirene_nesepm_istra' : ('', 'integer', """
					The 20 switches above are all feedback switches and require that b2stbc_feedback.ne.0 (See Run section for details) or that lfeedback=.true. in b2.boundary.parameters. The feedback is done as a boundary condition and is under-relaxed using the b2stbc_...._alpha switches (See Numerics section for details). 
					fheycore is the radial electron heat flow entering the core boundary. 
					fhiycore is the radial ion heat flow entering the core boundary. 
					fchycore is the radial current entering the core boundary. fnaycore is the radial flux of species "isfeedback" entering the core boundary. 
					If fhiycore_kinetic_energy.eq.1, the parallel kinetic energy flux is counted as part of the ion energy flux. 
					For double-null cases, the f..ycore variables contain the total flow through both core boundaries taken together. The core boundaries are identified by the coreregno and coreregn2 switches (see Geometry section). 
					The other seven switches are density feedback switches: nesepm is the outer midplane separatrix electron density. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is controlled through particle input of main plasma species isfeedback through the core boundary (See Geometry section for the core boundary indices coreregno and coreregn2). 
					nesepm_sol is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the SOL region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the SOL North boundary (See Geometry section for the SOL North boundary index solregno). If nesepm_overshoot.gt.1.0, the gas puff is turned off when the midplane separatrix density reaches nesepm*nesepm_overshoot. Minimum and maximum values of the feedback gas puff can be set using b2stbc_nesepm_minpuff and b2stbc_nesepm_maxpuff 
					nepedm_sol is similar to nesepm_sol but the feedback is exerted on the electron density at the top of the pedestal, along the outer midplane, at radial position b2stbc_iyped. ndes_sol is the total particle content from the homonuclear sequence of species 'isfeedback' over the entire simulation domain. 
					It is governed, like nesepm_sol, by nesepm_overshoot and nesepm_alpha and corresponds to a SOL boundary feedback. volrec_sol is the total particle source due to volume recombination coming from Eirene. Its feedback is governed by volrec_overshoot and volrec_alpha and volrec_beta parameters (See Numerics section for the latter two). nesepm_pfr is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the PFR region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the PFR South boundary indices pfrregno1 and pfrregno2). 
					ndes is the total particle (neutrals + ions) content of the species whose neutral species has index isfeedback. This is controlled through particle input of neutrals species isfeedback through the 
					private flux boundaries (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2). private_flux_puff is the particle flow of species isfeedback through the private flux region boundary. This is controlled through particle input of neutrals species isfeedback through the private flux boundaris (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2). 
					All but the first of these feedback schemes ("nesepm") can also be run though an Eirene neutral gas puff. In that case, one should set an appropriate gas puffing stratum in the Eirene input file input.dat, as well as in the b2.neutrals.parameters file. The code will assume, unless told otherwise through the use of "eirene_nesepm_istra", that the first stratum of type 'C' found in b2.neutrals.parameters is the stratum used for the feedback. If "eirene_nesepm_istra" is set to a positive number, the code will consider the feedback stratum to be the stratum in the "eirene_nesepm_istra"-th position in b2.neutrals.parameters.
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
   
      'b2stbr_plate_model' : ('', 'integer', """
					Sputtering model switches. See the code in b2stbr and the b2mod_sputter module for specific implementation details and references. 
					The default values represent the case of Graphite plates. Sput_src is the atomic number of the plasma species which causes chemical sputtering. 
					Sput_dst (when .ge.0) is the species index of the destination species produced by physical sputtering, chemical sputtering and/or RES. If either of the latter two processes are included, the production chemical sputtering and RES rate calculations provided in the code assume that sput_dst points to a Carbon species. 
					Sput_dst2 and sput_dst3 (when .ge.0) represent other species produced by wall interactions for mixed materials scenarios. 
					Sput_frac_flag is the switch to turn on mixed materials scenarios (when sput_frac_flag.eq.1). 
					Plate_model.eq.0 means the 0-D time-independent plate heating model while plate_model.eq.1 indicates the 1-D time-dependent plate heating treatment. Plate_model.eq.2 gives acces to a 2-D time-dependent model. Plate_option chooses the initialisation of the plate temperature profile. If plate_option.eq.1, the profile is set to the constant given in plate_temp. If plate_option.eq.2, the profile is computed to be the 0-D equilibrium profile. If plate_option.eq.3, the profile is read from results of the previous run.
					Sput_phys_model is a switch for choosing between the TRIM tables (model 1, default) or an empirical formula (model 0). When TRIM data is not available, the empirical formula is automatically used. Extrapolations of low and high energy ranges beyond the TRIM table data is done using the same physical dependencies as the empirical formula. Sput_chem_model is a switch for the chemical sputtering model used. 
					If sput_chem_model.eq.0 (default), the empirical formula is used. 
					If sput_chem_model.eq.1, a constant with a low energy cut-off is used. 
					The cutoff occurs at approximately sput_chem_cutoff_alpha and the width is determined by sput_chem_cutoff_beta (the larger the value, the narrower the width over which the transition from 0 to 1 occurs). 
					For model 0, sput_frc is a multiplier to the empirical formula, while for model 1, sput_frc is the constant chemical sputtering yield. 
					Sput_frc is superseded by the chem_sput array from b2.neutrals.namelist if the latter is used. 
					For neutrals species, we add a factor of alpha*na*vbar to the particle flux to the plate (used to compute chemical and RES sputtering), where vbar is the average neutral particle speed. 
					Sput_phys turns on physical sputtering when sput_phys.gt.0.0 and contains a (real) multiplier for the physical sputtering rate looked up in the TRIM tables. It is superseded by the phys_sput array in b2.neutrals.parameters if the latter is used. 
					sput_phys_col indicates which column to use in the TRIM table; the default (3) corresponds to 30 degrees incidence. The columns are for
                      0 15 30 45 55 65 75 80 85
                    degrees. This angle is also used in the empirical formula. Plate_temp is the temperature (in Kelvin) of the COOLED end of the divertor plates. The surface temperature is computed self-consistently (using a 1-D description) according to the incident heat fluxes from the plasma. The plate is assumed to have a thickness of plate_thick, measured in meters. When plate_thick.eq.0 (default), the plate surface temperature is assumed to be the same as plate_temp. Sput_res turns on radiation enhanced sublimation (RES) when .gt.0.0 and is a multiplier to the RES rate. 
					The switch sputter_energy_on turns on the energy contribution from the sputtered particles (physical and chemical). If sputter_energy_on.eq.0, the particles are sputtered cold, with no energy contribution to the ion heat equation. 
					If sputter_energy_on.ne.0 (default), the chemically sputtered particles are re-introduced into the plasma with the thermal energy corresponding to the surface temperature of the material, while physically sputtered particles are re-introduced with the TRIM-calculated energy sputtering yield (if the TRIM model is used). 
					Therm_evap turns on thermal evaporation when .gt.0.0 and is a multiplier to the thermal evaporation rate. 
					Redep_alpha is the multiplier to the reduction of the sputtering yield due to prompt redeposition. The promptly redeposited species is counted as eroded-then-deposited species.
				""", '0'),
   
      'b2stbr_plate_option' : ('', 'integer', """
					Sputtering model switches. See the code in b2stbr and the b2mod_sputter module for specific implementation details and references. 
					The default values represent the case of Graphite plates. Sput_src is the atomic number of the plasma species which causes chemical sputtering. 
					Sput_dst (when .ge.0) is the species index of the destination species produced by physical sputtering, chemical sputtering and/or RES. If either of the latter two processes are included, the production chemical sputtering and RES rate calculations provided in the code assume that sput_dst points to a Carbon species. 
					Sput_dst2 and sput_dst3 (when .ge.0) represent other species produced by wall interactions for mixed materials scenarios. 
					Sput_frac_flag is the switch to turn on mixed materials scenarios (when sput_frac_flag.eq.1). 
					Plate_model.eq.0 means the 0-D time-independent plate heating model while plate_model.eq.1 indicates the 1-D time-dependent plate heating treatment. Plate_model.eq.2 gives acces to a 2-D time-dependent model. Plate_option chooses the initialisation of the plate temperature profile. If plate_option.eq.1, the profile is set to the constant given in plate_temp. If plate_option.eq.2, the profile is computed to be the 0-D equilibrium profile. If plate_option.eq.3, the profile is read from results of the previous run.
					Sput_phys_model is a switch for choosing between the TRIM tables (model 1, default) or an empirical formula (model 0). When TRIM data is not available, the empirical formula is automatically used. Extrapolations of low and high energy ranges beyond the TRIM table data is done using the same physical dependencies as the empirical formula. Sput_chem_model is a switch for the chemical sputtering model used. 
					If sput_chem_model.eq.0 (default), the empirical formula is used. 
					If sput_chem_model.eq.1, a constant with a low energy cut-off is used. 
					The cutoff occurs at approximately sput_chem_cutoff_alpha and the width is determined by sput_chem_cutoff_beta (the larger the value, the narrower the width over which the transition from 0 to 1 occurs). 
					For model 0, sput_frc is a multiplier to the empirical formula, while for model 1, sput_frc is the constant chemical sputtering yield. 
					Sput_frc is superseded by the chem_sput array from b2.neutrals.namelist if the latter is used. 
					For neutrals species, we add a factor of alpha*na*vbar to the particle flux to the plate (used to compute chemical and RES sputtering), where vbar is the average neutral particle speed. 
					Sput_phys turns on physical sputtering when sput_phys.gt.0.0 and contains a (real) multiplier for the physical sputtering rate looked up in the TRIM tables. It is superseded by the phys_sput array in b2.neutrals.parameters if the latter is used. 
					sput_phys_col indicates which column to use in the TRIM table; the default (3) corresponds to 30 degrees incidence. The columns are for
                      0 15 30 45 55 65 75 80 85
                    degrees. This angle is also used in the empirical formula. Plate_temp is the temperature (in Kelvin) of the COOLED end of the divertor plates. The surface temperature is computed self-consistently (using a 1-D description) according to the incident heat fluxes from the plasma. The plate is assumed to have a thickness of plate_thick, measured in meters. When plate_thick.eq.0 (default), the plate surface temperature is assumed to be the same as plate_temp. Sput_res turns on radiation enhanced sublimation (RES) when .gt.0.0 and is a multiplier to the RES rate. 
					The switch sputter_energy_on turns on the energy contribution from the sputtered particles (physical and chemical). If sputter_energy_on.eq.0, the particles are sputtered cold, with no energy contribution to the ion heat equation. 
					If sputter_energy_on.ne.0 (default), the chemically sputtered particles are re-introduced into the plasma with the thermal energy corresponding to the surface temperature of the material, while physically sputtered particles are re-introduced with the TRIM-calculated energy sputtering yield (if the TRIM model is used). 
					Therm_evap turns on thermal evaporation when .gt.0.0 and is a multiplier to the thermal evaporation rate. 
					Redep_alpha is the multiplier to the reduction of the sputtering yield due to prompt redeposition. The promptly redeposited species is counted as eroded-then-deposited species.
				""", '3'),
   
      'b2stbr_sput_chem_model' : ('', 'integer', """
					Sputtering model switches. See the code in b2stbr and the b2mod_sputter module for specific implementation details and references. 
					The default values represent the case of Graphite plates. Sput_src is the atomic number of the plasma species which causes chemical sputtering. 
					Sput_dst (when .ge.0) is the species index of the destination species produced by physical sputtering, chemical sputtering and/or RES. If either of the latter two processes are included, the production chemical sputtering and RES rate calculations provided in the code assume that sput_dst points to a Carbon species. 
					Sput_dst2 and sput_dst3 (when .ge.0) represent other species produced by wall interactions for mixed materials scenarios. 
					Sput_frac_flag is the switch to turn on mixed materials scenarios (when sput_frac_flag.eq.1). 
					Plate_model.eq.0 means the 0-D time-independent plate heating model while plate_model.eq.1 indicates the 1-D time-dependent plate heating treatment. Plate_model.eq.2 gives acces to a 2-D time-dependent model. Plate_option chooses the initialisation of the plate temperature profile. If plate_option.eq.1, the profile is set to the constant given in plate_temp. If plate_option.eq.2, the profile is computed to be the 0-D equilibrium profile. If plate_option.eq.3, the profile is read from results of the previous run.
					Sput_phys_model is a switch for choosing between the TRIM tables (model 1, default) or an empirical formula (model 0). When TRIM data is not available, the empirical formula is automatically used. Extrapolations of low and high energy ranges beyond the TRIM table data is done using the same physical dependencies as the empirical formula. Sput_chem_model is a switch for the chemical sputtering model used. 
					If sput_chem_model.eq.0 (default), the empirical formula is used. 
					If sput_chem_model.eq.1, a constant with a low energy cut-off is used. 
					The cutoff occurs at approximately sput_chem_cutoff_alpha and the width is determined by sput_chem_cutoff_beta (the larger the value, the narrower the width over which the transition from 0 to 1 occurs). 
					For model 0, sput_frc is a multiplier to the empirical formula, while for model 1, sput_frc is the constant chemical sputtering yield. 
					Sput_frc is superseded by the chem_sput array from b2.neutrals.namelist if the latter is used. 
					For neutrals species, we add a factor of alpha*na*vbar to the particle flux to the plate (used to compute chemical and RES sputtering), where vbar is the average neutral particle speed. 
					Sput_phys turns on physical sputtering when sput_phys.gt.0.0 and contains a (real) multiplier for the physical sputtering rate looked up in the TRIM tables. It is superseded by the phys_sput array in b2.neutrals.parameters if the latter is used. 
					sput_phys_col indicates which column to use in the TRIM table; the default (3) corresponds to 30 degrees incidence. The columns are for
                      0 15 30 45 55 65 75 80 85
                    degrees. This angle is also used in the empirical formula. Plate_temp is the temperature (in Kelvin) of the COOLED end of the divertor plates. The surface temperature is computed self-consistently (using a 1-D description) according to the incident heat fluxes from the plasma. The plate is assumed to have a thickness of plate_thick, measured in meters. When plate_thick.eq.0 (default), the plate surface temperature is assumed to be the same as plate_temp. Sput_res turns on radiation enhanced sublimation (RES) when .gt.0.0 and is a multiplier to the RES rate. 
					The switch sputter_energy_on turns on the energy contribution from the sputtered particles (physical and chemical). If sputter_energy_on.eq.0, the particles are sputtered cold, with no energy contribution to the ion heat equation. 
					If sputter_energy_on.ne.0 (default), the chemically sputtered particles are re-introduced into the plasma with the thermal energy corresponding to the surface temperature of the material, while physically sputtered particles are re-introduced with the TRIM-calculated energy sputtering yield (if the TRIM model is used). 
					Therm_evap turns on thermal evaporation when .gt.0.0 and is a multiplier to the thermal evaporation rate. 
					Redep_alpha is the multiplier to the reduction of the sputtering yield due to prompt redeposition. The promptly redeposited species is counted as eroded-then-deposited species.
				""", '0'),
   
      'b2stbr_sput_chem_cutoff_alpha' : ('', 'real', """
					Sputtering model switches. See the code in b2stbr and the b2mod_sputter module for specific implementation details and references. 
					The default values represent the case of Graphite plates. Sput_src is the atomic number of the plasma species which causes chemical sputtering. 
					Sput_dst (when .ge.0) is the species index of the destination species produced by physical sputtering, chemical sputtering and/or RES. If either of the latter two processes are included, the production chemical sputtering and RES rate calculations provided in the code assume that sput_dst points to a Carbon species. 
					Sput_dst2 and sput_dst3 (when .ge.0) represent other species produced by wall interactions for mixed materials scenarios. 
					Sput_frac_flag is the switch to turn on mixed materials scenarios (when sput_frac_flag.eq.1). 
					Plate_model.eq.0 means the 0-D time-independent plate heating model while plate_model.eq.1 indicates the 1-D time-dependent plate heating treatment. Plate_model.eq.2 gives acces to a 2-D time-dependent model. Plate_option chooses the initialisation of the plate temperature profile. If plate_option.eq.1, the profile is set to the constant given in plate_temp. If plate_option.eq.2, the profile is computed to be the 0-D equilibrium profile. If plate_option.eq.3, the profile is read from results of the previous run.
					Sput_phys_model is a switch for choosing between the TRIM tables (model 1, default) or an empirical formula (model 0). When TRIM data is not available, the empirical formula is automatically used. Extrapolations of low and high energy ranges beyond the TRIM table data is done using the same physical dependencies as the empirical formula. Sput_chem_model is a switch for the chemical sputtering model used. 
					If sput_chem_model.eq.0 (default), the empirical formula is used. 
					If sput_chem_model.eq.1, a constant with a low energy cut-off is used. 
					The cutoff occurs at approximately sput_chem_cutoff_alpha and the width is determined by sput_chem_cutoff_beta (the larger the value, the narrower the width over which the transition from 0 to 1 occurs). 
					For model 0, sput_frc is a multiplier to the empirical formula, while for model 1, sput_frc is the constant chemical sputtering yield. 
					Sput_frc is superseded by the chem_sput array from b2.neutrals.namelist if the latter is used. 
					For neutrals species, we add a factor of alpha*na*vbar to the particle flux to the plate (used to compute chemical and RES sputtering), where vbar is the average neutral particle speed. 
					Sput_phys turns on physical sputtering when sput_phys.gt.0.0 and contains a (real) multiplier for the physical sputtering rate looked up in the TRIM tables. It is superseded by the phys_sput array in b2.neutrals.parameters if the latter is used. 
					sput_phys_col indicates which column to use in the TRIM table; the default (3) corresponds to 30 degrees incidence. The columns are for
                      0 15 30 45 55 65 75 80 85
                    degrees. This angle is also used in the empirical formula. Plate_temp is the temperature (in Kelvin) of the COOLED end of the divertor plates. The surface temperature is computed self-consistently (using a 1-D description) according to the incident heat fluxes from the plasma. The plate is assumed to have a thickness of plate_thick, measured in meters. When plate_thick.eq.0 (default), the plate surface temperature is assumed to be the same as plate_temp. Sput_res turns on radiation enhanced sublimation (RES) when .gt.0.0 and is a multiplier to the RES rate. 
					The switch sputter_energy_on turns on the energy contribution from the sputtered particles (physical and chemical). If sputter_energy_on.eq.0, the particles are sputtered cold, with no energy contribution to the ion heat equation. 
					If sputter_energy_on.ne.0 (default), the chemically sputtered particles are re-introduced into the plasma with the thermal energy corresponding to the surface temperature of the material, while physically sputtered particles are re-introduced with the TRIM-calculated energy sputtering yield (if the TRIM model is used). 
					Therm_evap turns on thermal evaporation when .gt.0.0 and is a multiplier to the thermal evaporation rate. 
					Redep_alpha is the multiplier to the reduction of the sputtering yield due to prompt redeposition. The promptly redeposited species is counted as eroded-then-deposited species.
				""", '1.0'),
   
      'b2stbr_sput_chem_cutoff_beta' : ('', 'real', """
					Sputtering model switches. See the code in b2stbr and the b2mod_sputter module for specific implementation details and references. 
					The default values represent the case of Graphite plates. Sput_src is the atomic number of the plasma species which causes chemical sputtering. 
					Sput_dst (when .ge.0) is the species index of the destination species produced by physical sputtering, chemical sputtering and/or RES. If either of the latter two processes are included, the production chemical sputtering and RES rate calculations provided in the code assume that sput_dst points to a Carbon species. 
					Sput_dst2 and sput_dst3 (when .ge.0) represent other species produced by wall interactions for mixed materials scenarios. 
					Sput_frac_flag is the switch to turn on mixed materials scenarios (when sput_frac_flag.eq.1). 
					Plate_model.eq.0 means the 0-D time-independent plate heating model while plate_model.eq.1 indicates the 1-D time-dependent plate heating treatment. Plate_model.eq.2 gives acces to a 2-D time-dependent model. Plate_option chooses the initialisation of the plate temperature profile. If plate_option.eq.1, the profile is set to the constant given in plate_temp. If plate_option.eq.2, the profile is computed to be the 0-D equilibrium profile. If plate_option.eq.3, the profile is read from results of the previous run.
					Sput_phys_model is a switch for choosing between the TRIM tables (model 1, default) or an empirical formula (model 0). When TRIM data is not available, the empirical formula is automatically used. Extrapolations of low and high energy ranges beyond the TRIM table data is done using the same physical dependencies as the empirical formula. Sput_chem_model is a switch for the chemical sputtering model used. 
					If sput_chem_model.eq.0 (default), the empirical formula is used. 
					If sput_chem_model.eq.1, a constant with a low energy cut-off is used. 
					The cutoff occurs at approximately sput_chem_cutoff_alpha and the width is determined by sput_chem_cutoff_beta (the larger the value, the narrower the width over which the transition from 0 to 1 occurs). 
					For model 0, sput_frc is a multiplier to the empirical formula, while for model 1, sput_frc is the constant chemical sputtering yield. 
					Sput_frc is superseded by the chem_sput array from b2.neutrals.namelist if the latter is used. 
					For neutrals species, we add a factor of alpha*na*vbar to the particle flux to the plate (used to compute chemical and RES sputtering), where vbar is the average neutral particle speed. 
					Sput_phys turns on physical sputtering when sput_phys.gt.0.0 and contains a (real) multiplier for the physical sputtering rate looked up in the TRIM tables. It is superseded by the phys_sput array in b2.neutrals.parameters if the latter is used. 
					sput_phys_col indicates which column to use in the TRIM table; the default (3) corresponds to 30 degrees incidence. The columns are for
                      0 15 30 45 55 65 75 80 85
                    degrees. This angle is also used in the empirical formula. Plate_temp is the temperature (in Kelvin) of the COOLED end of the divertor plates. The surface temperature is computed self-consistently (using a 1-D description) according to the incident heat fluxes from the plasma. The plate is assumed to have a thickness of plate_thick, measured in meters. When plate_thick.eq.0 (default), the plate surface temperature is assumed to be the same as plate_temp. Sput_res turns on radiation enhanced sublimation (RES) when .gt.0.0 and is a multiplier to the RES rate. 
					The switch sputter_energy_on turns on the energy contribution from the sputtered particles (physical and chemical). If sputter_energy_on.eq.0, the particles are sputtered cold, with no energy contribution to the ion heat equation. 
					If sputter_energy_on.ne.0 (default), the chemically sputtered particles are re-introduced into the plasma with the thermal energy corresponding to the surface temperature of the material, while physically sputtered particles are re-introduced with the TRIM-calculated energy sputtering yield (if the TRIM model is used). 
					Therm_evap turns on thermal evaporation when .gt.0.0 and is a multiplier to the thermal evaporation rate. 
					Redep_alpha is the multiplier to the reduction of the sputtering yield due to prompt redeposition. The promptly redeposited species is counted as eroded-then-deposited species.
				""", '3.0'),
   
      'b2stbr_sput_mixed_alpha' : ('', 'real', """
					Sputtering model switches. See the code in b2stbr and the b2mod_sputter module for specific implementation details and references. 
					The default values represent the case of Graphite plates. Sput_src is the atomic number of the plasma species which causes chemical sputtering. 
					Sput_dst (when .ge.0) is the species index of the destination species produced by physical sputtering, chemical sputtering and/or RES. If either of the latter two processes are included, the production chemical sputtering and RES rate calculations provided in the code assume that sput_dst points to a Carbon species. 
					Sput_dst2 and sput_dst3 (when .ge.0) represent other species produced by wall interactions for mixed materials scenarios. 
					Sput_frac_flag is the switch to turn on mixed materials scenarios (when sput_frac_flag.eq.1). 
					Plate_model.eq.0 means the 0-D time-independent plate heating model while plate_model.eq.1 indicates the 1-D time-dependent plate heating treatment. Plate_model.eq.2 gives acces to a 2-D time-dependent model. Plate_option chooses the initialisation of the plate temperature profile. If plate_option.eq.1, the profile is set to the constant given in plate_temp. If plate_option.eq.2, the profile is computed to be the 0-D equilibrium profile. If plate_option.eq.3, the profile is read from results of the previous run.
					Sput_phys_model is a switch for choosing between the TRIM tables (model 1, default) or an empirical formula (model 0). When TRIM data is not available, the empirical formula is automatically used. Extrapolations of low and high energy ranges beyond the TRIM table data is done using the same physical dependencies as the empirical formula. Sput_chem_model is a switch for the chemical sputtering model used. 
					If sput_chem_model.eq.0 (default), the empirical formula is used. 
					If sput_chem_model.eq.1, a constant with a low energy cut-off is used. 
					The cutoff occurs at approximately sput_chem_cutoff_alpha and the width is determined by sput_chem_cutoff_beta (the larger the value, the narrower the width over which the transition from 0 to 1 occurs). 
					For model 0, sput_frc is a multiplier to the empirical formula, while for model 1, sput_frc is the constant chemical sputtering yield. 
					Sput_frc is superseded by the chem_sput array from b2.neutrals.namelist if the latter is used. 
					For neutrals species, we add a factor of alpha*na*vbar to the particle flux to the plate (used to compute chemical and RES sputtering), where vbar is the average neutral particle speed. 
					Sput_phys turns on physical sputtering when sput_phys.gt.0.0 and contains a (real) multiplier for the physical sputtering rate looked up in the TRIM tables. It is superseded by the phys_sput array in b2.neutrals.parameters if the latter is used. 
					sput_phys_col indicates which column to use in the TRIM table; the default (3) corresponds to 30 degrees incidence. The columns are for
                      0 15 30 45 55 65 75 80 85
                    degrees. This angle is also used in the empirical formula. Plate_temp is the temperature (in Kelvin) of the COOLED end of the divertor plates. The surface temperature is computed self-consistently (using a 1-D description) according to the incident heat fluxes from the plasma. The plate is assumed to have a thickness of plate_thick, measured in meters. When plate_thick.eq.0 (default), the plate surface temperature is assumed to be the same as plate_temp. Sput_res turns on radiation enhanced sublimation (RES) when .gt.0.0 and is a multiplier to the RES rate. 
					The switch sputter_energy_on turns on the energy contribution from the sputtered particles (physical and chemical). If sputter_energy_on.eq.0, the particles are sputtered cold, with no energy contribution to the ion heat equation. 
					If sputter_energy_on.ne.0 (default), the chemically sputtered particles are re-introduced into the plasma with the thermal energy corresponding to the surface temperature of the material, while physically sputtered particles are re-introduced with the TRIM-calculated energy sputtering yield (if the TRIM model is used). 
					Therm_evap turns on thermal evaporation when .gt.0.0 and is a multiplier to the thermal evaporation rate. 
					Redep_alpha is the multiplier to the reduction of the sputtering yield due to prompt redeposition. The promptly redeposited species is counted as eroded-then-deposited species.
				""", '1.0'),
   
      'b2stbr_sput_mixed_beta' : ('', 'real', """
					Sputtering model switches. See the code in b2stbr and the b2mod_sputter module for specific implementation details and references. 
					The default values represent the case of Graphite plates. Sput_src is the atomic number of the plasma species which causes chemical sputtering. 
					Sput_dst (when .ge.0) is the species index of the destination species produced by physical sputtering, chemical sputtering and/or RES. If either of the latter two processes are included, the production chemical sputtering and RES rate calculations provided in the code assume that sput_dst points to a Carbon species. 
					Sput_dst2 and sput_dst3 (when .ge.0) represent other species produced by wall interactions for mixed materials scenarios. 
					Sput_frac_flag is the switch to turn on mixed materials scenarios (when sput_frac_flag.eq.1). 
					Plate_model.eq.0 means the 0-D time-independent plate heating model while plate_model.eq.1 indicates the 1-D time-dependent plate heating treatment. Plate_model.eq.2 gives acces to a 2-D time-dependent model. Plate_option chooses the initialisation of the plate temperature profile. If plate_option.eq.1, the profile is set to the constant given in plate_temp. If plate_option.eq.2, the profile is computed to be the 0-D equilibrium profile. If plate_option.eq.3, the profile is read from results of the previous run.
					Sput_phys_model is a switch for choosing between the TRIM tables (model 1, default) or an empirical formula (model 0). When TRIM data is not available, the empirical formula is automatically used. Extrapolations of low and high energy ranges beyond the TRIM table data is done using the same physical dependencies as the empirical formula. Sput_chem_model is a switch for the chemical sputtering model used. 
					If sput_chem_model.eq.0 (default), the empirical formula is used. 
					If sput_chem_model.eq.1, a constant with a low energy cut-off is used. 
					The cutoff occurs at approximately sput_chem_cutoff_alpha and the width is determined by sput_chem_cutoff_beta (the larger the value, the narrower the width over which the transition from 0 to 1 occurs). 
					For model 0, sput_frc is a multiplier to the empirical formula, while for model 1, sput_frc is the constant chemical sputtering yield. 
					Sput_frc is superseded by the chem_sput array from b2.neutrals.namelist if the latter is used. 
					For neutrals species, we add a factor of alpha*na*vbar to the particle flux to the plate (used to compute chemical and RES sputtering), where vbar is the average neutral particle speed. 
					Sput_phys turns on physical sputtering when sput_phys.gt.0.0 and contains a (real) multiplier for the physical sputtering rate looked up in the TRIM tables. It is superseded by the phys_sput array in b2.neutrals.parameters if the latter is used. 
					sput_phys_col indicates which column to use in the TRIM table; the default (3) corresponds to 30 degrees incidence. The columns are for
                      0 15 30 45 55 65 75 80 85
                    degrees. This angle is also used in the empirical formula. Plate_temp is the temperature (in Kelvin) of the COOLED end of the divertor plates. The surface temperature is computed self-consistently (using a 1-D description) according to the incident heat fluxes from the plasma. The plate is assumed to have a thickness of plate_thick, measured in meters. When plate_thick.eq.0 (default), the plate surface temperature is assumed to be the same as plate_temp. Sput_res turns on radiation enhanced sublimation (RES) when .gt.0.0 and is a multiplier to the RES rate. 
					The switch sputter_energy_on turns on the energy contribution from the sputtered particles (physical and chemical). If sputter_energy_on.eq.0, the particles are sputtered cold, with no energy contribution to the ion heat equation. 
					If sputter_energy_on.ne.0 (default), the chemically sputtered particles are re-introduced into the plasma with the thermal energy corresponding to the surface temperature of the material, while physically sputtered particles are re-introduced with the TRIM-calculated energy sputtering yield (if the TRIM model is used). 
					Therm_evap turns on thermal evaporation when .gt.0.0 and is a multiplier to the thermal evaporation rate. 
					Redep_alpha is the multiplier to the reduction of the sputtering yield due to prompt redeposition. The promptly redeposited species is counted as eroded-then-deposited species.
				""", '1.0'),
   
      'b2stbr_sput_phys_model' : ('', 'integer', """
					Sputtering model switches. See the code in b2stbr and the b2mod_sputter module for specific implementation details and references. 
					The default values represent the case of Graphite plates. Sput_src is the atomic number of the plasma species which causes chemical sputtering. 
					Sput_dst (when .ge.0) is the species index of the destination species produced by physical sputtering, chemical sputtering and/or RES. If either of the latter two processes are included, the production chemical sputtering and RES rate calculations provided in the code assume that sput_dst points to a Carbon species. 
					Sput_dst2 and sput_dst3 (when .ge.0) represent other species produced by wall interactions for mixed materials scenarios. 
					Sput_frac_flag is the switch to turn on mixed materials scenarios (when sput_frac_flag.eq.1). 
					Plate_model.eq.0 means the 0-D time-independent plate heating model while plate_model.eq.1 indicates the 1-D time-dependent plate heating treatment. Plate_model.eq.2 gives acces to a 2-D time-dependent model. Plate_option chooses the initialisation of the plate temperature profile. If plate_option.eq.1, the profile is set to the constant given in plate_temp. If plate_option.eq.2, the profile is computed to be the 0-D equilibrium profile. If plate_option.eq.3, the profile is read from results of the previous run.
					Sput_phys_model is a switch for choosing between the TRIM tables (model 1, default) or an empirical formula (model 0). When TRIM data is not available, the empirical formula is automatically used. Extrapolations of low and high energy ranges beyond the TRIM table data is done using the same physical dependencies as the empirical formula. Sput_chem_model is a switch for the chemical sputtering model used. 
					If sput_chem_model.eq.0 (default), the empirical formula is used. 
					If sput_chem_model.eq.1, a constant with a low energy cut-off is used. 
					The cutoff occurs at approximately sput_chem_cutoff_alpha and the width is determined by sput_chem_cutoff_beta (the larger the value, the narrower the width over which the transition from 0 to 1 occurs). 
					For model 0, sput_frc is a multiplier to the empirical formula, while for model 1, sput_frc is the constant chemical sputtering yield. 
					Sput_frc is superseded by the chem_sput array from b2.neutrals.namelist if the latter is used. 
					For neutrals species, we add a factor of alpha*na*vbar to the particle flux to the plate (used to compute chemical and RES sputtering), where vbar is the average neutral particle speed. 
					Sput_phys turns on physical sputtering when sput_phys.gt.0.0 and contains a (real) multiplier for the physical sputtering rate looked up in the TRIM tables. It is superseded by the phys_sput array in b2.neutrals.parameters if the latter is used. 
					sput_phys_col indicates which column to use in the TRIM table; the default (3) corresponds to 30 degrees incidence. The columns are for
                      0 15 30 45 55 65 75 80 85
                    degrees. This angle is also used in the empirical formula. Plate_temp is the temperature (in Kelvin) of the COOLED end of the divertor plates. The surface temperature is computed self-consistently (using a 1-D description) according to the incident heat fluxes from the plasma. The plate is assumed to have a thickness of plate_thick, measured in meters. When plate_thick.eq.0 (default), the plate surface temperature is assumed to be the same as plate_temp. Sput_res turns on radiation enhanced sublimation (RES) when .gt.0.0 and is a multiplier to the RES rate. 
					The switch sputter_energy_on turns on the energy contribution from the sputtered particles (physical and chemical). If sputter_energy_on.eq.0, the particles are sputtered cold, with no energy contribution to the ion heat equation. 
					If sputter_energy_on.ne.0 (default), the chemically sputtered particles are re-introduced into the plasma with the thermal energy corresponding to the surface temperature of the material, while physically sputtered particles are re-introduced with the TRIM-calculated energy sputtering yield (if the TRIM model is used). 
					Therm_evap turns on thermal evaporation when .gt.0.0 and is a multiplier to the thermal evaporation rate. 
					Redep_alpha is the multiplier to the reduction of the sputtering yield due to prompt redeposition. The promptly redeposited species is counted as eroded-then-deposited species.
				""", '1'),
   
      'b2stbr_sputter_energy_on' : ('', 'integer', """
					Sputtering model switches. See the code in b2stbr and the b2mod_sputter module for specific implementation details and references. 
					The default values represent the case of Graphite plates. Sput_src is the atomic number of the plasma species which causes chemical sputtering. 
					Sput_dst (when .ge.0) is the species index of the destination species produced by physical sputtering, chemical sputtering and/or RES. If either of the latter two processes are included, the production chemical sputtering and RES rate calculations provided in the code assume that sput_dst points to a Carbon species. 
					Sput_dst2 and sput_dst3 (when .ge.0) represent other species produced by wall interactions for mixed materials scenarios. 
					Sput_frac_flag is the switch to turn on mixed materials scenarios (when sput_frac_flag.eq.1). 
					Plate_model.eq.0 means the 0-D time-independent plate heating model while plate_model.eq.1 indicates the 1-D time-dependent plate heating treatment. Plate_model.eq.2 gives acces to a 2-D time-dependent model. Plate_option chooses the initialisation of the plate temperature profile. If plate_option.eq.1, the profile is set to the constant given in plate_temp. If plate_option.eq.2, the profile is computed to be the 0-D equilibrium profile. If plate_option.eq.3, the profile is read from results of the previous run.
					Sput_phys_model is a switch for choosing between the TRIM tables (model 1, default) or an empirical formula (model 0). When TRIM data is not available, the empirical formula is automatically used. Extrapolations of low and high energy ranges beyond the TRIM table data is done using the same physical dependencies as the empirical formula. Sput_chem_model is a switch for the chemical sputtering model used. 
					If sput_chem_model.eq.0 (default), the empirical formula is used. 
					If sput_chem_model.eq.1, a constant with a low energy cut-off is used. 
					The cutoff occurs at approximately sput_chem_cutoff_alpha and the width is determined by sput_chem_cutoff_beta (the larger the value, the narrower the width over which the transition from 0 to 1 occurs). 
					For model 0, sput_frc is a multiplier to the empirical formula, while for model 1, sput_frc is the constant chemical sputtering yield. 
					Sput_frc is superseded by the chem_sput array from b2.neutrals.namelist if the latter is used. 
					For neutrals species, we add a factor of alpha*na*vbar to the particle flux to the plate (used to compute chemical and RES sputtering), where vbar is the average neutral particle speed. 
					Sput_phys turns on physical sputtering when sput_phys.gt.0.0 and contains a (real) multiplier for the physical sputtering rate looked up in the TRIM tables. It is superseded by the phys_sput array in b2.neutrals.parameters if the latter is used. 
					sput_phys_col indicates which column to use in the TRIM table; the default (3) corresponds to 30 degrees incidence. The columns are for
                      0 15 30 45 55 65 75 80 85
                    degrees. This angle is also used in the empirical formula. Plate_temp is the temperature (in Kelvin) of the COOLED end of the divertor plates. The surface temperature is computed self-consistently (using a 1-D description) according to the incident heat fluxes from the plasma. The plate is assumed to have a thickness of plate_thick, measured in meters. When plate_thick.eq.0 (default), the plate surface temperature is assumed to be the same as plate_temp. Sput_res turns on radiation enhanced sublimation (RES) when .gt.0.0 and is a multiplier to the RES rate. 
					The switch sputter_energy_on turns on the energy contribution from the sputtered particles (physical and chemical). If sputter_energy_on.eq.0, the particles are sputtered cold, with no energy contribution to the ion heat equation. 
					If sputter_energy_on.ne.0 (default), the chemically sputtered particles are re-introduced into the plasma with the thermal energy corresponding to the surface temperature of the material, while physically sputtered particles are re-introduced with the TRIM-calculated energy sputtering yield (if the TRIM model is used). 
					Therm_evap turns on thermal evaporation when .gt.0.0 and is a multiplier to the thermal evaporation rate. 
					Redep_alpha is the multiplier to the reduction of the sputtering yield due to prompt redeposition. The promptly redeposited species is counted as eroded-then-deposited species.
				""", '1'),
   
      'b2stbr_sput_res' : ('', 'real', """
					Sputtering model switches. See the code in b2stbr and the b2mod_sputter module for specific implementation details and references. 
					The default values represent the case of Graphite plates. Sput_src is the atomic number of the plasma species which causes chemical sputtering. 
					Sput_dst (when .ge.0) is the species index of the destination species produced by physical sputtering, chemical sputtering and/or RES. If either of the latter two processes are included, the production chemical sputtering and RES rate calculations provided in the code assume that sput_dst points to a Carbon species. 
					Sput_dst2 and sput_dst3 (when .ge.0) represent other species produced by wall interactions for mixed materials scenarios. 
					Sput_frac_flag is the switch to turn on mixed materials scenarios (when sput_frac_flag.eq.1). 
					Plate_model.eq.0 means the 0-D time-independent plate heating model while plate_model.eq.1 indicates the 1-D time-dependent plate heating treatment. Plate_model.eq.2 gives acces to a 2-D time-dependent model. Plate_option chooses the initialisation of the plate temperature profile. If plate_option.eq.1, the profile is set to the constant given in plate_temp. If plate_option.eq.2, the profile is computed to be the 0-D equilibrium profile. If plate_option.eq.3, the profile is read from results of the previous run.
					Sput_phys_model is a switch for choosing between the TRIM tables (model 1, default) or an empirical formula (model 0). When TRIM data is not available, the empirical formula is automatically used. Extrapolations of low and high energy ranges beyond the TRIM table data is done using the same physical dependencies as the empirical formula. Sput_chem_model is a switch for the chemical sputtering model used. 
					If sput_chem_model.eq.0 (default), the empirical formula is used. 
					If sput_chem_model.eq.1, a constant with a low energy cut-off is used. 
					The cutoff occurs at approximately sput_chem_cutoff_alpha and the width is determined by sput_chem_cutoff_beta (the larger the value, the narrower the width over which the transition from 0 to 1 occurs). 
					For model 0, sput_frc is a multiplier to the empirical formula, while for model 1, sput_frc is the constant chemical sputtering yield. 
					Sput_frc is superseded by the chem_sput array from b2.neutrals.namelist if the latter is used. 
					For neutrals species, we add a factor of alpha*na*vbar to the particle flux to the plate (used to compute chemical and RES sputtering), where vbar is the average neutral particle speed. 
					Sput_phys turns on physical sputtering when sput_phys.gt.0.0 and contains a (real) multiplier for the physical sputtering rate looked up in the TRIM tables. It is superseded by the phys_sput array in b2.neutrals.parameters if the latter is used. 
					sput_phys_col indicates which column to use in the TRIM table; the default (3) corresponds to 30 degrees incidence. The columns are for
                      0 15 30 45 55 65 75 80 85
                    degrees. This angle is also used in the empirical formula. Plate_temp is the temperature (in Kelvin) of the COOLED end of the divertor plates. The surface temperature is computed self-consistently (using a 1-D description) according to the incident heat fluxes from the plasma. The plate is assumed to have a thickness of plate_thick, measured in meters. When plate_thick.eq.0 (default), the plate surface temperature is assumed to be the same as plate_temp. Sput_res turns on radiation enhanced sublimation (RES) when .gt.0.0 and is a multiplier to the RES rate. 
					The switch sputter_energy_on turns on the energy contribution from the sputtered particles (physical and chemical). If sputter_energy_on.eq.0, the particles are sputtered cold, with no energy contribution to the ion heat equation. 
					If sputter_energy_on.ne.0 (default), the chemically sputtered particles are re-introduced into the plasma with the thermal energy corresponding to the surface temperature of the material, while physically sputtered particles are re-introduced with the TRIM-calculated energy sputtering yield (if the TRIM model is used). 
					Therm_evap turns on thermal evaporation when .gt.0.0 and is a multiplier to the thermal evaporation rate. 
					Redep_alpha is the multiplier to the reduction of the sputtering yield due to prompt redeposition. The promptly redeposited species is counted as eroded-then-deposited species.
				""", '0.0'),
   
      'b2stbr_therm_evap' : ('', 'real', """
					Sputtering model switches. See the code in b2stbr and the b2mod_sputter module for specific implementation details and references. 
					The default values represent the case of Graphite plates. Sput_src is the atomic number of the plasma species which causes chemical sputtering. 
					Sput_dst (when .ge.0) is the species index of the destination species produced by physical sputtering, chemical sputtering and/or RES. If either of the latter two processes are included, the production chemical sputtering and RES rate calculations provided in the code assume that sput_dst points to a Carbon species. 
					Sput_dst2 and sput_dst3 (when .ge.0) represent other species produced by wall interactions for mixed materials scenarios. 
					Sput_frac_flag is the switch to turn on mixed materials scenarios (when sput_frac_flag.eq.1). 
					Plate_model.eq.0 means the 0-D time-independent plate heating model while plate_model.eq.1 indicates the 1-D time-dependent plate heating treatment. Plate_model.eq.2 gives acces to a 2-D time-dependent model. Plate_option chooses the initialisation of the plate temperature profile. If plate_option.eq.1, the profile is set to the constant given in plate_temp. If plate_option.eq.2, the profile is computed to be the 0-D equilibrium profile. If plate_option.eq.3, the profile is read from results of the previous run.
					Sput_phys_model is a switch for choosing between the TRIM tables (model 1, default) or an empirical formula (model 0). When TRIM data is not available, the empirical formula is automatically used. Extrapolations of low and high energy ranges beyond the TRIM table data is done using the same physical dependencies as the empirical formula. Sput_chem_model is a switch for the chemical sputtering model used. 
					If sput_chem_model.eq.0 (default), the empirical formula is used. 
					If sput_chem_model.eq.1, a constant with a low energy cut-off is used. 
					The cutoff occurs at approximately sput_chem_cutoff_alpha and the width is determined by sput_chem_cutoff_beta (the larger the value, the narrower the width over which the transition from 0 to 1 occurs). 
					For model 0, sput_frc is a multiplier to the empirical formula, while for model 1, sput_frc is the constant chemical sputtering yield. 
					Sput_frc is superseded by the chem_sput array from b2.neutrals.namelist if the latter is used. 
					For neutrals species, we add a factor of alpha*na*vbar to the particle flux to the plate (used to compute chemical and RES sputtering), where vbar is the average neutral particle speed. 
					Sput_phys turns on physical sputtering when sput_phys.gt.0.0 and contains a (real) multiplier for the physical sputtering rate looked up in the TRIM tables. It is superseded by the phys_sput array in b2.neutrals.parameters if the latter is used. 
					sput_phys_col indicates which column to use in the TRIM table; the default (3) corresponds to 30 degrees incidence. The columns are for
                      0 15 30 45 55 65 75 80 85
                    degrees. This angle is also used in the empirical formula. Plate_temp is the temperature (in Kelvin) of the COOLED end of the divertor plates. The surface temperature is computed self-consistently (using a 1-D description) according to the incident heat fluxes from the plasma. The plate is assumed to have a thickness of plate_thick, measured in meters. When plate_thick.eq.0 (default), the plate surface temperature is assumed to be the same as plate_temp. Sput_res turns on radiation enhanced sublimation (RES) when .gt.0.0 and is a multiplier to the RES rate. 
					The switch sputter_energy_on turns on the energy contribution from the sputtered particles (physical and chemical). If sputter_energy_on.eq.0, the particles are sputtered cold, with no energy contribution to the ion heat equation. 
					If sputter_energy_on.ne.0 (default), the chemically sputtered particles are re-introduced into the plasma with the thermal energy corresponding to the surface temperature of the material, while physically sputtered particles are re-introduced with the TRIM-calculated energy sputtering yield (if the TRIM model is used). 
					Therm_evap turns on thermal evaporation when .gt.0.0 and is a multiplier to the thermal evaporation rate. 
					Redep_alpha is the multiplier to the reduction of the sputtering yield due to prompt redeposition. The promptly redeposited species is counted as eroded-then-deposited species.
				""", '0.0'),
   
      'b2stbr_sput_dst' : ('', 'integer', """
					Sputtering model switches. See the code in b2stbr and the b2mod_sputter module for specific implementation details and references. 
					The default values represent the case of Graphite plates. Sput_src is the atomic number of the plasma species which causes chemical sputtering. 
					Sput_dst (when .ge.0) is the species index of the destination species produced by physical sputtering, chemical sputtering and/or RES. If either of the latter two processes are included, the production chemical sputtering and RES rate calculations provided in the code assume that sput_dst points to a Carbon species. 
					Sput_dst2 and sput_dst3 (when .ge.0) represent other species produced by wall interactions for mixed materials scenarios. 
					Sput_frac_flag is the switch to turn on mixed materials scenarios (when sput_frac_flag.eq.1). 
					Plate_model.eq.0 means the 0-D time-independent plate heating model while plate_model.eq.1 indicates the 1-D time-dependent plate heating treatment. Plate_model.eq.2 gives acces to a 2-D time-dependent model. Plate_option chooses the initialisation of the plate temperature profile. If plate_option.eq.1, the profile is set to the constant given in plate_temp. If plate_option.eq.2, the profile is computed to be the 0-D equilibrium profile. If plate_option.eq.3, the profile is read from results of the previous run.
					Sput_phys_model is a switch for choosing between the TRIM tables (model 1, default) or an empirical formula (model 0). When TRIM data is not available, the empirical formula is automatically used. Extrapolations of low and high energy ranges beyond the TRIM table data is done using the same physical dependencies as the empirical formula. Sput_chem_model is a switch for the chemical sputtering model used. 
					If sput_chem_model.eq.0 (default), the empirical formula is used. 
					If sput_chem_model.eq.1, a constant with a low energy cut-off is used. 
					The cutoff occurs at approximately sput_chem_cutoff_alpha and the width is determined by sput_chem_cutoff_beta (the larger the value, the narrower the width over which the transition from 0 to 1 occurs). 
					For model 0, sput_frc is a multiplier to the empirical formula, while for model 1, sput_frc is the constant chemical sputtering yield. 
					Sput_frc is superseded by the chem_sput array from b2.neutrals.namelist if the latter is used. 
					For neutrals species, we add a factor of alpha*na*vbar to the particle flux to the plate (used to compute chemical and RES sputtering), where vbar is the average neutral particle speed. 
					Sput_phys turns on physical sputtering when sput_phys.gt.0.0 and contains a (real) multiplier for the physical sputtering rate looked up in the TRIM tables. It is superseded by the phys_sput array in b2.neutrals.parameters if the latter is used. 
					sput_phys_col indicates which column to use in the TRIM table; the default (3) corresponds to 30 degrees incidence. The columns are for
                      0 15 30 45 55 65 75 80 85
                    degrees. This angle is also used in the empirical formula. Plate_temp is the temperature (in Kelvin) of the COOLED end of the divertor plates. The surface temperature is computed self-consistently (using a 1-D description) according to the incident heat fluxes from the plasma. The plate is assumed to have a thickness of plate_thick, measured in meters. When plate_thick.eq.0 (default), the plate surface temperature is assumed to be the same as plate_temp. Sput_res turns on radiation enhanced sublimation (RES) when .gt.0.0 and is a multiplier to the RES rate. 
					The switch sputter_energy_on turns on the energy contribution from the sputtered particles (physical and chemical). If sputter_energy_on.eq.0, the particles are sputtered cold, with no energy contribution to the ion heat equation. 
					If sputter_energy_on.ne.0 (default), the chemically sputtered particles are re-introduced into the plasma with the thermal energy corresponding to the surface temperature of the material, while physically sputtered particles are re-introduced with the TRIM-calculated energy sputtering yield (if the TRIM model is used). 
					Therm_evap turns on thermal evaporation when .gt.0.0 and is a multiplier to the thermal evaporation rate. 
					Redep_alpha is the multiplier to the reduction of the sputtering yield due to prompt redeposition. The promptly redeposited species is counted as eroded-then-deposited species.
				""", '-1'),
   
      'b2stbr_sput_dst2' : ('', 'integer', """
					Sputtering model switches. See the code in b2stbr and the b2mod_sputter module for specific implementation details and references. 
					The default values represent the case of Graphite plates. Sput_src is the atomic number of the plasma species which causes chemical sputtering. 
					Sput_dst (when .ge.0) is the species index of the destination species produced by physical sputtering, chemical sputtering and/or RES. If either of the latter two processes are included, the production chemical sputtering and RES rate calculations provided in the code assume that sput_dst points to a Carbon species. 
					Sput_dst2 and sput_dst3 (when .ge.0) represent other species produced by wall interactions for mixed materials scenarios. 
					Sput_frac_flag is the switch to turn on mixed materials scenarios (when sput_frac_flag.eq.1). 
					Plate_model.eq.0 means the 0-D time-independent plate heating model while plate_model.eq.1 indicates the 1-D time-dependent plate heating treatment. Plate_model.eq.2 gives acces to a 2-D time-dependent model. Plate_option chooses the initialisation of the plate temperature profile. If plate_option.eq.1, the profile is set to the constant given in plate_temp. If plate_option.eq.2, the profile is computed to be the 0-D equilibrium profile. If plate_option.eq.3, the profile is read from results of the previous run.
					Sput_phys_model is a switch for choosing between the TRIM tables (model 1, default) or an empirical formula (model 0). When TRIM data is not available, the empirical formula is automatically used. Extrapolations of low and high energy ranges beyond the TRIM table data is done using the same physical dependencies as the empirical formula. Sput_chem_model is a switch for the chemical sputtering model used. 
					If sput_chem_model.eq.0 (default), the empirical formula is used. 
					If sput_chem_model.eq.1, a constant with a low energy cut-off is used. 
					The cutoff occurs at approximately sput_chem_cutoff_alpha and the width is determined by sput_chem_cutoff_beta (the larger the value, the narrower the width over which the transition from 0 to 1 occurs). 
					For model 0, sput_frc is a multiplier to the empirical formula, while for model 1, sput_frc is the constant chemical sputtering yield. 
					Sput_frc is superseded by the chem_sput array from b2.neutrals.namelist if the latter is used. 
					For neutrals species, we add a factor of alpha*na*vbar to the particle flux to the plate (used to compute chemical and RES sputtering), where vbar is the average neutral particle speed. 
					Sput_phys turns on physical sputtering when sput_phys.gt.0.0 and contains a (real) multiplier for the physical sputtering rate looked up in the TRIM tables. It is superseded by the phys_sput array in b2.neutrals.parameters if the latter is used. 
					sput_phys_col indicates which column to use in the TRIM table; the default (3) corresponds to 30 degrees incidence. The columns are for
                      0 15 30 45 55 65 75 80 85
                    degrees. This angle is also used in the empirical formula. Plate_temp is the temperature (in Kelvin) of the COOLED end of the divertor plates. The surface temperature is computed self-consistently (using a 1-D description) according to the incident heat fluxes from the plasma. The plate is assumed to have a thickness of plate_thick, measured in meters. When plate_thick.eq.0 (default), the plate surface temperature is assumed to be the same as plate_temp. Sput_res turns on radiation enhanced sublimation (RES) when .gt.0.0 and is a multiplier to the RES rate. 
					The switch sputter_energy_on turns on the energy contribution from the sputtered particles (physical and chemical). If sputter_energy_on.eq.0, the particles are sputtered cold, with no energy contribution to the ion heat equation. 
					If sputter_energy_on.ne.0 (default), the chemically sputtered particles are re-introduced into the plasma with the thermal energy corresponding to the surface temperature of the material, while physically sputtered particles are re-introduced with the TRIM-calculated energy sputtering yield (if the TRIM model is used). 
					Therm_evap turns on thermal evaporation when .gt.0.0 and is a multiplier to the thermal evaporation rate. 
					Redep_alpha is the multiplier to the reduction of the sputtering yield due to prompt redeposition. The promptly redeposited species is counted as eroded-then-deposited species.
				""", '-1'),
   
      'b2stbr_sput_dst3' : ('', 'integer', """
					Sputtering model switches. See the code in b2stbr and the b2mod_sputter module for specific implementation details and references. 
					The default values represent the case of Graphite plates. Sput_src is the atomic number of the plasma species which causes chemical sputtering. 
					Sput_dst (when .ge.0) is the species index of the destination species produced by physical sputtering, chemical sputtering and/or RES. If either of the latter two processes are included, the production chemical sputtering and RES rate calculations provided in the code assume that sput_dst points to a Carbon species. 
					Sput_dst2 and sput_dst3 (when .ge.0) represent other species produced by wall interactions for mixed materials scenarios. 
					Sput_frac_flag is the switch to turn on mixed materials scenarios (when sput_frac_flag.eq.1). 
					Plate_model.eq.0 means the 0-D time-independent plate heating model while plate_model.eq.1 indicates the 1-D time-dependent plate heating treatment. Plate_model.eq.2 gives acces to a 2-D time-dependent model. Plate_option chooses the initialisation of the plate temperature profile. If plate_option.eq.1, the profile is set to the constant given in plate_temp. If plate_option.eq.2, the profile is computed to be the 0-D equilibrium profile. If plate_option.eq.3, the profile is read from results of the previous run.
					Sput_phys_model is a switch for choosing between the TRIM tables (model 1, default) or an empirical formula (model 0). When TRIM data is not available, the empirical formula is automatically used. Extrapolations of low and high energy ranges beyond the TRIM table data is done using the same physical dependencies as the empirical formula. Sput_chem_model is a switch for the chemical sputtering model used. 
					If sput_chem_model.eq.0 (default), the empirical formula is used. 
					If sput_chem_model.eq.1, a constant with a low energy cut-off is used. 
					The cutoff occurs at approximately sput_chem_cutoff_alpha and the width is determined by sput_chem_cutoff_beta (the larger the value, the narrower the width over which the transition from 0 to 1 occurs). 
					For model 0, sput_frc is a multiplier to the empirical formula, while for model 1, sput_frc is the constant chemical sputtering yield. 
					Sput_frc is superseded by the chem_sput array from b2.neutrals.namelist if the latter is used. 
					For neutrals species, we add a factor of alpha*na*vbar to the particle flux to the plate (used to compute chemical and RES sputtering), where vbar is the average neutral particle speed. 
					Sput_phys turns on physical sputtering when sput_phys.gt.0.0 and contains a (real) multiplier for the physical sputtering rate looked up in the TRIM tables. It is superseded by the phys_sput array in b2.neutrals.parameters if the latter is used. 
					sput_phys_col indicates which column to use in the TRIM table; the default (3) corresponds to 30 degrees incidence. The columns are for
                      0 15 30 45 55 65 75 80 85
                    degrees. This angle is also used in the empirical formula. Plate_temp is the temperature (in Kelvin) of the COOLED end of the divertor plates. The surface temperature is computed self-consistently (using a 1-D description) according to the incident heat fluxes from the plasma. The plate is assumed to have a thickness of plate_thick, measured in meters. When plate_thick.eq.0 (default), the plate surface temperature is assumed to be the same as plate_temp. Sput_res turns on radiation enhanced sublimation (RES) when .gt.0.0 and is a multiplier to the RES rate. 
					The switch sputter_energy_on turns on the energy contribution from the sputtered particles (physical and chemical). If sputter_energy_on.eq.0, the particles are sputtered cold, with no energy contribution to the ion heat equation. 
					If sputter_energy_on.ne.0 (default), the chemically sputtered particles are re-introduced into the plasma with the thermal energy corresponding to the surface temperature of the material, while physically sputtered particles are re-introduced with the TRIM-calculated energy sputtering yield (if the TRIM model is used). 
					Therm_evap turns on thermal evaporation when .gt.0.0 and is a multiplier to the thermal evaporation rate. 
					Redep_alpha is the multiplier to the reduction of the sputtering yield due to prompt redeposition. The promptly redeposited species is counted as eroded-then-deposited species.
				""", '-1'),
   
      'b2stbr_sput_frac_flag' : ('', 'integer', """
					Sputtering model switches. See the code in b2stbr and the b2mod_sputter module for specific implementation details and references. 
					The default values represent the case of Graphite plates. Sput_src is the atomic number of the plasma species which causes chemical sputtering. 
					Sput_dst (when .ge.0) is the species index of the destination species produced by physical sputtering, chemical sputtering and/or RES. If either of the latter two processes are included, the production chemical sputtering and RES rate calculations provided in the code assume that sput_dst points to a Carbon species. 
					Sput_dst2 and sput_dst3 (when .ge.0) represent other species produced by wall interactions for mixed materials scenarios. 
					Sput_frac_flag is the switch to turn on mixed materials scenarios (when sput_frac_flag.eq.1). 
					Plate_model.eq.0 means the 0-D time-independent plate heating model while plate_model.eq.1 indicates the 1-D time-dependent plate heating treatment. Plate_model.eq.2 gives acces to a 2-D time-dependent model. Plate_option chooses the initialisation of the plate temperature profile. If plate_option.eq.1, the profile is set to the constant given in plate_temp. If plate_option.eq.2, the profile is computed to be the 0-D equilibrium profile. If plate_option.eq.3, the profile is read from results of the previous run.
					Sput_phys_model is a switch for choosing between the TRIM tables (model 1, default) or an empirical formula (model 0). When TRIM data is not available, the empirical formula is automatically used. Extrapolations of low and high energy ranges beyond the TRIM table data is done using the same physical dependencies as the empirical formula. Sput_chem_model is a switch for the chemical sputtering model used. 
					If sput_chem_model.eq.0 (default), the empirical formula is used. 
					If sput_chem_model.eq.1, a constant with a low energy cut-off is used. 
					The cutoff occurs at approximately sput_chem_cutoff_alpha and the width is determined by sput_chem_cutoff_beta (the larger the value, the narrower the width over which the transition from 0 to 1 occurs). 
					For model 0, sput_frc is a multiplier to the empirical formula, while for model 1, sput_frc is the constant chemical sputtering yield. 
					Sput_frc is superseded by the chem_sput array from b2.neutrals.namelist if the latter is used. 
					For neutrals species, we add a factor of alpha*na*vbar to the particle flux to the plate (used to compute chemical and RES sputtering), where vbar is the average neutral particle speed. 
					Sput_phys turns on physical sputtering when sput_phys.gt.0.0 and contains a (real) multiplier for the physical sputtering rate looked up in the TRIM tables. It is superseded by the phys_sput array in b2.neutrals.parameters if the latter is used. 
					sput_phys_col indicates which column to use in the TRIM table; the default (3) corresponds to 30 degrees incidence. The columns are for
                      0 15 30 45 55 65 75 80 85
                    degrees. This angle is also used in the empirical formula. Plate_temp is the temperature (in Kelvin) of the COOLED end of the divertor plates. The surface temperature is computed self-consistently (using a 1-D description) according to the incident heat fluxes from the plasma. The plate is assumed to have a thickness of plate_thick, measured in meters. When plate_thick.eq.0 (default), the plate surface temperature is assumed to be the same as plate_temp. Sput_res turns on radiation enhanced sublimation (RES) when .gt.0.0 and is a multiplier to the RES rate. 
					The switch sputter_energy_on turns on the energy contribution from the sputtered particles (physical and chemical). If sputter_energy_on.eq.0, the particles are sputtered cold, with no energy contribution to the ion heat equation. 
					If sputter_energy_on.ne.0 (default), the chemically sputtered particles are re-introduced into the plasma with the thermal energy corresponding to the surface temperature of the material, while physically sputtered particles are re-introduced with the TRIM-calculated energy sputtering yield (if the TRIM model is used). 
					Therm_evap turns on thermal evaporation when .gt.0.0 and is a multiplier to the thermal evaporation rate. 
					Redep_alpha is the multiplier to the reduction of the sputtering yield due to prompt redeposition. The promptly redeposited species is counted as eroded-then-deposited species.
				""", '0'),
   
      'b2stbr_sput_frc' : ('', 'real', """
					Sputtering model switches. See the code in b2stbr and the b2mod_sputter module for specific implementation details and references. 
					The default values represent the case of Graphite plates. Sput_src is the atomic number of the plasma species which causes chemical sputtering. 
					Sput_dst (when .ge.0) is the species index of the destination species produced by physical sputtering, chemical sputtering and/or RES. If either of the latter two processes are included, the production chemical sputtering and RES rate calculations provided in the code assume that sput_dst points to a Carbon species. 
					Sput_dst2 and sput_dst3 (when .ge.0) represent other species produced by wall interactions for mixed materials scenarios. 
					Sput_frac_flag is the switch to turn on mixed materials scenarios (when sput_frac_flag.eq.1). 
					Plate_model.eq.0 means the 0-D time-independent plate heating model while plate_model.eq.1 indicates the 1-D time-dependent plate heating treatment. Plate_model.eq.2 gives acces to a 2-D time-dependent model. Plate_option chooses the initialisation of the plate temperature profile. If plate_option.eq.1, the profile is set to the constant given in plate_temp. If plate_option.eq.2, the profile is computed to be the 0-D equilibrium profile. If plate_option.eq.3, the profile is read from results of the previous run.
					Sput_phys_model is a switch for choosing between the TRIM tables (model 1, default) or an empirical formula (model 0). When TRIM data is not available, the empirical formula is automatically used. Extrapolations of low and high energy ranges beyond the TRIM table data is done using the same physical dependencies as the empirical formula. Sput_chem_model is a switch for the chemical sputtering model used. 
					If sput_chem_model.eq.0 (default), the empirical formula is used. 
					If sput_chem_model.eq.1, a constant with a low energy cut-off is used. 
					The cutoff occurs at approximately sput_chem_cutoff_alpha and the width is determined by sput_chem_cutoff_beta (the larger the value, the narrower the width over which the transition from 0 to 1 occurs). 
					For model 0, sput_frc is a multiplier to the empirical formula, while for model 1, sput_frc is the constant chemical sputtering yield. 
					Sput_frc is superseded by the chem_sput array from b2.neutrals.namelist if the latter is used. 
					For neutrals species, we add a factor of alpha*na*vbar to the particle flux to the plate (used to compute chemical and RES sputtering), where vbar is the average neutral particle speed. 
					Sput_phys turns on physical sputtering when sput_phys.gt.0.0 and contains a (real) multiplier for the physical sputtering rate looked up in the TRIM tables. It is superseded by the phys_sput array in b2.neutrals.parameters if the latter is used. 
					sput_phys_col indicates which column to use in the TRIM table; the default (3) corresponds to 30 degrees incidence. The columns are for
                      0 15 30 45 55 65 75 80 85
                    degrees. This angle is also used in the empirical formula. Plate_temp is the temperature (in Kelvin) of the COOLED end of the divertor plates. The surface temperature is computed self-consistently (using a 1-D description) according to the incident heat fluxes from the plasma. The plate is assumed to have a thickness of plate_thick, measured in meters. When plate_thick.eq.0 (default), the plate surface temperature is assumed to be the same as plate_temp. Sput_res turns on radiation enhanced sublimation (RES) when .gt.0.0 and is a multiplier to the RES rate. 
					The switch sputter_energy_on turns on the energy contribution from the sputtered particles (physical and chemical). If sputter_energy_on.eq.0, the particles are sputtered cold, with no energy contribution to the ion heat equation. 
					If sputter_energy_on.ne.0 (default), the chemically sputtered particles are re-introduced into the plasma with the thermal energy corresponding to the surface temperature of the material, while physically sputtered particles are re-introduced with the TRIM-calculated energy sputtering yield (if the TRIM model is used). 
					Therm_evap turns on thermal evaporation when .gt.0.0 and is a multiplier to the thermal evaporation rate. 
					Redep_alpha is the multiplier to the reduction of the sputtering yield due to prompt redeposition. The promptly redeposited species is counted as eroded-then-deposited species.
				""", '0.0'),
   
      'b2stbr_sput_phys' : ('', 'real', """
					Sputtering model switches. See the code in b2stbr and the b2mod_sputter module for specific implementation details and references. 
					The default values represent the case of Graphite plates. Sput_src is the atomic number of the plasma species which causes chemical sputtering. 
					Sput_dst (when .ge.0) is the species index of the destination species produced by physical sputtering, chemical sputtering and/or RES. If either of the latter two processes are included, the production chemical sputtering and RES rate calculations provided in the code assume that sput_dst points to a Carbon species. 
					Sput_dst2 and sput_dst3 (when .ge.0) represent other species produced by wall interactions for mixed materials scenarios. 
					Sput_frac_flag is the switch to turn on mixed materials scenarios (when sput_frac_flag.eq.1). 
					Plate_model.eq.0 means the 0-D time-independent plate heating model while plate_model.eq.1 indicates the 1-D time-dependent plate heating treatment. Plate_model.eq.2 gives acces to a 2-D time-dependent model. Plate_option chooses the initialisation of the plate temperature profile. If plate_option.eq.1, the profile is set to the constant given in plate_temp. If plate_option.eq.2, the profile is computed to be the 0-D equilibrium profile. If plate_option.eq.3, the profile is read from results of the previous run.
					Sput_phys_model is a switch for choosing between the TRIM tables (model 1, default) or an empirical formula (model 0). When TRIM data is not available, the empirical formula is automatically used. Extrapolations of low and high energy ranges beyond the TRIM table data is done using the same physical dependencies as the empirical formula. Sput_chem_model is a switch for the chemical sputtering model used. 
					If sput_chem_model.eq.0 (default), the empirical formula is used. 
					If sput_chem_model.eq.1, a constant with a low energy cut-off is used. 
					The cutoff occurs at approximately sput_chem_cutoff_alpha and the width is determined by sput_chem_cutoff_beta (the larger the value, the narrower the width over which the transition from 0 to 1 occurs). 
					For model 0, sput_frc is a multiplier to the empirical formula, while for model 1, sput_frc is the constant chemical sputtering yield. 
					Sput_frc is superseded by the chem_sput array from b2.neutrals.namelist if the latter is used. 
					For neutrals species, we add a factor of alpha*na*vbar to the particle flux to the plate (used to compute chemical and RES sputtering), where vbar is the average neutral particle speed. 
					Sput_phys turns on physical sputtering when sput_phys.gt.0.0 and contains a (real) multiplier for the physical sputtering rate looked up in the TRIM tables. It is superseded by the phys_sput array in b2.neutrals.parameters if the latter is used. 
					sput_phys_col indicates which column to use in the TRIM table; the default (3) corresponds to 30 degrees incidence. The columns are for
                      0 15 30 45 55 65 75 80 85
                    degrees. This angle is also used in the empirical formula. Plate_temp is the temperature (in Kelvin) of the COOLED end of the divertor plates. The surface temperature is computed self-consistently (using a 1-D description) according to the incident heat fluxes from the plasma. The plate is assumed to have a thickness of plate_thick, measured in meters. When plate_thick.eq.0 (default), the plate surface temperature is assumed to be the same as plate_temp. Sput_res turns on radiation enhanced sublimation (RES) when .gt.0.0 and is a multiplier to the RES rate. 
					The switch sputter_energy_on turns on the energy contribution from the sputtered particles (physical and chemical). If sputter_energy_on.eq.0, the particles are sputtered cold, with no energy contribution to the ion heat equation. 
					If sputter_energy_on.ne.0 (default), the chemically sputtered particles are re-introduced into the plasma with the thermal energy corresponding to the surface temperature of the material, while physically sputtered particles are re-introduced with the TRIM-calculated energy sputtering yield (if the TRIM model is used). 
					Therm_evap turns on thermal evaporation when .gt.0.0 and is a multiplier to the thermal evaporation rate. 
					Redep_alpha is the multiplier to the reduction of the sputtering yield due to prompt redeposition. The promptly redeposited species is counted as eroded-then-deposited species.
				""", '0.0'),
   
      'b2stbr_sput_src' : ('', 'integer', """
					Sputtering model switches. See the code in b2stbr and the b2mod_sputter module for specific implementation details and references. 
					The default values represent the case of Graphite plates. Sput_src is the atomic number of the plasma species which causes chemical sputtering. 
					Sput_dst (when .ge.0) is the species index of the destination species produced by physical sputtering, chemical sputtering and/or RES. If either of the latter two processes are included, the production chemical sputtering and RES rate calculations provided in the code assume that sput_dst points to a Carbon species. 
					Sput_dst2 and sput_dst3 (when .ge.0) represent other species produced by wall interactions for mixed materials scenarios. 
					Sput_frac_flag is the switch to turn on mixed materials scenarios (when sput_frac_flag.eq.1). 
					Plate_model.eq.0 means the 0-D time-independent plate heating model while plate_model.eq.1 indicates the 1-D time-dependent plate heating treatment. Plate_model.eq.2 gives acces to a 2-D time-dependent model. Plate_option chooses the initialisation of the plate temperature profile. If plate_option.eq.1, the profile is set to the constant given in plate_temp. If plate_option.eq.2, the profile is computed to be the 0-D equilibrium profile. If plate_option.eq.3, the profile is read from results of the previous run.
					Sput_phys_model is a switch for choosing between the TRIM tables (model 1, default) or an empirical formula (model 0). When TRIM data is not available, the empirical formula is automatically used. Extrapolations of low and high energy ranges beyond the TRIM table data is done using the same physical dependencies as the empirical formula. Sput_chem_model is a switch for the chemical sputtering model used. 
					If sput_chem_model.eq.0 (default), the empirical formula is used. 
					If sput_chem_model.eq.1, a constant with a low energy cut-off is used. 
					The cutoff occurs at approximately sput_chem_cutoff_alpha and the width is determined by sput_chem_cutoff_beta (the larger the value, the narrower the width over which the transition from 0 to 1 occurs). 
					For model 0, sput_frc is a multiplier to the empirical formula, while for model 1, sput_frc is the constant chemical sputtering yield. 
					Sput_frc is superseded by the chem_sput array from b2.neutrals.namelist if the latter is used. 
					For neutrals species, we add a factor of alpha*na*vbar to the particle flux to the plate (used to compute chemical and RES sputtering), where vbar is the average neutral particle speed. 
					Sput_phys turns on physical sputtering when sput_phys.gt.0.0 and contains a (real) multiplier for the physical sputtering rate looked up in the TRIM tables. It is superseded by the phys_sput array in b2.neutrals.parameters if the latter is used. 
					sput_phys_col indicates which column to use in the TRIM table; the default (3) corresponds to 30 degrees incidence. The columns are for
                      0 15 30 45 55 65 75 80 85
                    degrees. This angle is also used in the empirical formula. Plate_temp is the temperature (in Kelvin) of the COOLED end of the divertor plates. The surface temperature is computed self-consistently (using a 1-D description) according to the incident heat fluxes from the plasma. The plate is assumed to have a thickness of plate_thick, measured in meters. When plate_thick.eq.0 (default), the plate surface temperature is assumed to be the same as plate_temp. Sput_res turns on radiation enhanced sublimation (RES) when .gt.0.0 and is a multiplier to the RES rate. 
					The switch sputter_energy_on turns on the energy contribution from the sputtered particles (physical and chemical). If sputter_energy_on.eq.0, the particles are sputtered cold, with no energy contribution to the ion heat equation. 
					If sputter_energy_on.ne.0 (default), the chemically sputtered particles are re-introduced into the plasma with the thermal energy corresponding to the surface temperature of the material, while physically sputtered particles are re-introduced with the TRIM-calculated energy sputtering yield (if the TRIM model is used). 
					Therm_evap turns on thermal evaporation when .gt.0.0 and is a multiplier to the thermal evaporation rate. 
					Redep_alpha is the multiplier to the reduction of the sputtering yield due to prompt redeposition. The promptly redeposited species is counted as eroded-then-deposited species.
				""", '1'),
   
      'b2stbr_sput_phys_col' : ('', 'integer', """
					Sputtering model switches. See the code in b2stbr and the b2mod_sputter module for specific implementation details and references. 
					The default values represent the case of Graphite plates. Sput_src is the atomic number of the plasma species which causes chemical sputtering. 
					Sput_dst (when .ge.0) is the species index of the destination species produced by physical sputtering, chemical sputtering and/or RES. If either of the latter two processes are included, the production chemical sputtering and RES rate calculations provided in the code assume that sput_dst points to a Carbon species. 
					Sput_dst2 and sput_dst3 (when .ge.0) represent other species produced by wall interactions for mixed materials scenarios. 
					Sput_frac_flag is the switch to turn on mixed materials scenarios (when sput_frac_flag.eq.1). 
					Plate_model.eq.0 means the 0-D time-independent plate heating model while plate_model.eq.1 indicates the 1-D time-dependent plate heating treatment. Plate_model.eq.2 gives acces to a 2-D time-dependent model. Plate_option chooses the initialisation of the plate temperature profile. If plate_option.eq.1, the profile is set to the constant given in plate_temp. If plate_option.eq.2, the profile is computed to be the 0-D equilibrium profile. If plate_option.eq.3, the profile is read from results of the previous run.
					Sput_phys_model is a switch for choosing between the TRIM tables (model 1, default) or an empirical formula (model 0). When TRIM data is not available, the empirical formula is automatically used. Extrapolations of low and high energy ranges beyond the TRIM table data is done using the same physical dependencies as the empirical formula. Sput_chem_model is a switch for the chemical sputtering model used. 
					If sput_chem_model.eq.0 (default), the empirical formula is used. 
					If sput_chem_model.eq.1, a constant with a low energy cut-off is used. 
					The cutoff occurs at approximately sput_chem_cutoff_alpha and the width is determined by sput_chem_cutoff_beta (the larger the value, the narrower the width over which the transition from 0 to 1 occurs). 
					For model 0, sput_frc is a multiplier to the empirical formula, while for model 1, sput_frc is the constant chemical sputtering yield. 
					Sput_frc is superseded by the chem_sput array from b2.neutrals.namelist if the latter is used. 
					For neutrals species, we add a factor of alpha*na*vbar to the particle flux to the plate (used to compute chemical and RES sputtering), where vbar is the average neutral particle speed. 
					Sput_phys turns on physical sputtering when sput_phys.gt.0.0 and contains a (real) multiplier for the physical sputtering rate looked up in the TRIM tables. It is superseded by the phys_sput array in b2.neutrals.parameters if the latter is used. 
					sput_phys_col indicates which column to use in the TRIM table; the default (3) corresponds to 30 degrees incidence. The columns are for
                      0 15 30 45 55 65 75 80 85
                    degrees. This angle is also used in the empirical formula. Plate_temp is the temperature (in Kelvin) of the COOLED end of the divertor plates. The surface temperature is computed self-consistently (using a 1-D description) according to the incident heat fluxes from the plasma. The plate is assumed to have a thickness of plate_thick, measured in meters. When plate_thick.eq.0 (default), the plate surface temperature is assumed to be the same as plate_temp. Sput_res turns on radiation enhanced sublimation (RES) when .gt.0.0 and is a multiplier to the RES rate. 
					The switch sputter_energy_on turns on the energy contribution from the sputtered particles (physical and chemical). If sputter_energy_on.eq.0, the particles are sputtered cold, with no energy contribution to the ion heat equation. 
					If sputter_energy_on.ne.0 (default), the chemically sputtered particles are re-introduced into the plasma with the thermal energy corresponding to the surface temperature of the material, while physically sputtered particles are re-introduced with the TRIM-calculated energy sputtering yield (if the TRIM model is used). 
					Therm_evap turns on thermal evaporation when .gt.0.0 and is a multiplier to the thermal evaporation rate. 
					Redep_alpha is the multiplier to the reduction of the sputtering yield due to prompt redeposition. The promptly redeposited species is counted as eroded-then-deposited species.
				""", '3'),
   
      'b2stbr_alpha' : ('', 'real', """
					Sputtering model switches. See the code in b2stbr and the b2mod_sputter module for specific implementation details and references. 
					The default values represent the case of Graphite plates. Sput_src is the atomic number of the plasma species which causes chemical sputtering. 
					Sput_dst (when .ge.0) is the species index of the destination species produced by physical sputtering, chemical sputtering and/or RES. If either of the latter two processes are included, the production chemical sputtering and RES rate calculations provided in the code assume that sput_dst points to a Carbon species. 
					Sput_dst2 and sput_dst3 (when .ge.0) represent other species produced by wall interactions for mixed materials scenarios. 
					Sput_frac_flag is the switch to turn on mixed materials scenarios (when sput_frac_flag.eq.1). 
					Plate_model.eq.0 means the 0-D time-independent plate heating model while plate_model.eq.1 indicates the 1-D time-dependent plate heating treatment. Plate_model.eq.2 gives acces to a 2-D time-dependent model. Plate_option chooses the initialisation of the plate temperature profile. If plate_option.eq.1, the profile is set to the constant given in plate_temp. If plate_option.eq.2, the profile is computed to be the 0-D equilibrium profile. If plate_option.eq.3, the profile is read from results of the previous run.
					Sput_phys_model is a switch for choosing between the TRIM tables (model 1, default) or an empirical formula (model 0). When TRIM data is not available, the empirical formula is automatically used. Extrapolations of low and high energy ranges beyond the TRIM table data is done using the same physical dependencies as the empirical formula. Sput_chem_model is a switch for the chemical sputtering model used. 
					If sput_chem_model.eq.0 (default), the empirical formula is used. 
					If sput_chem_model.eq.1, a constant with a low energy cut-off is used. 
					The cutoff occurs at approximately sput_chem_cutoff_alpha and the width is determined by sput_chem_cutoff_beta (the larger the value, the narrower the width over which the transition from 0 to 1 occurs). 
					For model 0, sput_frc is a multiplier to the empirical formula, while for model 1, sput_frc is the constant chemical sputtering yield. 
					Sput_frc is superseded by the chem_sput array from b2.neutrals.namelist if the latter is used. 
					For neutrals species, we add a factor of alpha*na*vbar to the particle flux to the plate (used to compute chemical and RES sputtering), where vbar is the average neutral particle speed. 
					Sput_phys turns on physical sputtering when sput_phys.gt.0.0 and contains a (real) multiplier for the physical sputtering rate looked up in the TRIM tables. It is superseded by the phys_sput array in b2.neutrals.parameters if the latter is used. 
					sput_phys_col indicates which column to use in the TRIM table; the default (3) corresponds to 30 degrees incidence. The columns are for
                      0 15 30 45 55 65 75 80 85
                    degrees. This angle is also used in the empirical formula. Plate_temp is the temperature (in Kelvin) of the COOLED end of the divertor plates. The surface temperature is computed self-consistently (using a 1-D description) according to the incident heat fluxes from the plasma. The plate is assumed to have a thickness of plate_thick, measured in meters. When plate_thick.eq.0 (default), the plate surface temperature is assumed to be the same as plate_temp. Sput_res turns on radiation enhanced sublimation (RES) when .gt.0.0 and is a multiplier to the RES rate. 
					The switch sputter_energy_on turns on the energy contribution from the sputtered particles (physical and chemical). If sputter_energy_on.eq.0, the particles are sputtered cold, with no energy contribution to the ion heat equation. 
					If sputter_energy_on.ne.0 (default), the chemically sputtered particles are re-introduced into the plasma with the thermal energy corresponding to the surface temperature of the material, while physically sputtered particles are re-introduced with the TRIM-calculated energy sputtering yield (if the TRIM model is used). 
					Therm_evap turns on thermal evaporation when .gt.0.0 and is a multiplier to the thermal evaporation rate. 
					Redep_alpha is the multiplier to the reduction of the sputtering yield due to prompt redeposition. The promptly redeposited species is counted as eroded-then-deposited species.
				""", '0.25'),
   
      'b2stbr_plate_temp' : ('', 'real', """
					Sputtering model switches. See the code in b2stbr and the b2mod_sputter module for specific implementation details and references. 
					The default values represent the case of Graphite plates. Sput_src is the atomic number of the plasma species which causes chemical sputtering. 
					Sput_dst (when .ge.0) is the species index of the destination species produced by physical sputtering, chemical sputtering and/or RES. If either of the latter two processes are included, the production chemical sputtering and RES rate calculations provided in the code assume that sput_dst points to a Carbon species. 
					Sput_dst2 and sput_dst3 (when .ge.0) represent other species produced by wall interactions for mixed materials scenarios. 
					Sput_frac_flag is the switch to turn on mixed materials scenarios (when sput_frac_flag.eq.1). 
					Plate_model.eq.0 means the 0-D time-independent plate heating model while plate_model.eq.1 indicates the 1-D time-dependent plate heating treatment. Plate_model.eq.2 gives acces to a 2-D time-dependent model. Plate_option chooses the initialisation of the plate temperature profile. If plate_option.eq.1, the profile is set to the constant given in plate_temp. If plate_option.eq.2, the profile is computed to be the 0-D equilibrium profile. If plate_option.eq.3, the profile is read from results of the previous run.
					Sput_phys_model is a switch for choosing between the TRIM tables (model 1, default) or an empirical formula (model 0). When TRIM data is not available, the empirical formula is automatically used. Extrapolations of low and high energy ranges beyond the TRIM table data is done using the same physical dependencies as the empirical formula. Sput_chem_model is a switch for the chemical sputtering model used. 
					If sput_chem_model.eq.0 (default), the empirical formula is used. 
					If sput_chem_model.eq.1, a constant with a low energy cut-off is used. 
					The cutoff occurs at approximately sput_chem_cutoff_alpha and the width is determined by sput_chem_cutoff_beta (the larger the value, the narrower the width over which the transition from 0 to 1 occurs). 
					For model 0, sput_frc is a multiplier to the empirical formula, while for model 1, sput_frc is the constant chemical sputtering yield. 
					Sput_frc is superseded by the chem_sput array from b2.neutrals.namelist if the latter is used. 
					For neutrals species, we add a factor of alpha*na*vbar to the particle flux to the plate (used to compute chemical and RES sputtering), where vbar is the average neutral particle speed. 
					Sput_phys turns on physical sputtering when sput_phys.gt.0.0 and contains a (real) multiplier for the physical sputtering rate looked up in the TRIM tables. It is superseded by the phys_sput array in b2.neutrals.parameters if the latter is used. 
					sput_phys_col indicates which column to use in the TRIM table; the default (3) corresponds to 30 degrees incidence. The columns are for
                      0 15 30 45 55 65 75 80 85
                    degrees. This angle is also used in the empirical formula. Plate_temp is the temperature (in Kelvin) of the COOLED end of the divertor plates. The surface temperature is computed self-consistently (using a 1-D description) according to the incident heat fluxes from the plasma. The plate is assumed to have a thickness of plate_thick, measured in meters. When plate_thick.eq.0 (default), the plate surface temperature is assumed to be the same as plate_temp. Sput_res turns on radiation enhanced sublimation (RES) when .gt.0.0 and is a multiplier to the RES rate. 
					The switch sputter_energy_on turns on the energy contribution from the sputtered particles (physical and chemical). If sputter_energy_on.eq.0, the particles are sputtered cold, with no energy contribution to the ion heat equation. 
					If sputter_energy_on.ne.0 (default), the chemically sputtered particles are re-introduced into the plasma with the thermal energy corresponding to the surface temperature of the material, while physically sputtered particles are re-introduced with the TRIM-calculated energy sputtering yield (if the TRIM model is used). 
					Therm_evap turns on thermal evaporation when .gt.0.0 and is a multiplier to the thermal evaporation rate. 
					Redep_alpha is the multiplier to the reduction of the sputtering yield due to prompt redeposition. The promptly redeposited species is counted as eroded-then-deposited species.
				""", '300.0'),
   
      'b2stbr_plate_thick' : ('', 'real', """
					Sputtering model switches. See the code in b2stbr and the b2mod_sputter module for specific implementation details and references. 
					The default values represent the case of Graphite plates. Sput_src is the atomic number of the plasma species which causes chemical sputtering. 
					Sput_dst (when .ge.0) is the species index of the destination species produced by physical sputtering, chemical sputtering and/or RES. If either of the latter two processes are included, the production chemical sputtering and RES rate calculations provided in the code assume that sput_dst points to a Carbon species. 
					Sput_dst2 and sput_dst3 (when .ge.0) represent other species produced by wall interactions for mixed materials scenarios. 
					Sput_frac_flag is the switch to turn on mixed materials scenarios (when sput_frac_flag.eq.1). 
					Plate_model.eq.0 means the 0-D time-independent plate heating model while plate_model.eq.1 indicates the 1-D time-dependent plate heating treatment. Plate_model.eq.2 gives acces to a 2-D time-dependent model. Plate_option chooses the initialisation of the plate temperature profile. If plate_option.eq.1, the profile is set to the constant given in plate_temp. If plate_option.eq.2, the profile is computed to be the 0-D equilibrium profile. If plate_option.eq.3, the profile is read from results of the previous run.
					Sput_phys_model is a switch for choosing between the TRIM tables (model 1, default) or an empirical formula (model 0). When TRIM data is not available, the empirical formula is automatically used. Extrapolations of low and high energy ranges beyond the TRIM table data is done using the same physical dependencies as the empirical formula. Sput_chem_model is a switch for the chemical sputtering model used. 
					If sput_chem_model.eq.0 (default), the empirical formula is used. 
					If sput_chem_model.eq.1, a constant with a low energy cut-off is used. 
					The cutoff occurs at approximately sput_chem_cutoff_alpha and the width is determined by sput_chem_cutoff_beta (the larger the value, the narrower the width over which the transition from 0 to 1 occurs). 
					For model 0, sput_frc is a multiplier to the empirical formula, while for model 1, sput_frc is the constant chemical sputtering yield. 
					Sput_frc is superseded by the chem_sput array from b2.neutrals.namelist if the latter is used. 
					For neutrals species, we add a factor of alpha*na*vbar to the particle flux to the plate (used to compute chemical and RES sputtering), where vbar is the average neutral particle speed. 
					Sput_phys turns on physical sputtering when sput_phys.gt.0.0 and contains a (real) multiplier for the physical sputtering rate looked up in the TRIM tables. It is superseded by the phys_sput array in b2.neutrals.parameters if the latter is used. 
					sput_phys_col indicates which column to use in the TRIM table; the default (3) corresponds to 30 degrees incidence. The columns are for
                      0 15 30 45 55 65 75 80 85
                    degrees. This angle is also used in the empirical formula. Plate_temp is the temperature (in Kelvin) of the COOLED end of the divertor plates. The surface temperature is computed self-consistently (using a 1-D description) according to the incident heat fluxes from the plasma. The plate is assumed to have a thickness of plate_thick, measured in meters. When plate_thick.eq.0 (default), the plate surface temperature is assumed to be the same as plate_temp. Sput_res turns on radiation enhanced sublimation (RES) when .gt.0.0 and is a multiplier to the RES rate. 
					The switch sputter_energy_on turns on the energy contribution from the sputtered particles (physical and chemical). If sputter_energy_on.eq.0, the particles are sputtered cold, with no energy contribution to the ion heat equation. 
					If sputter_energy_on.ne.0 (default), the chemically sputtered particles are re-introduced into the plasma with the thermal energy corresponding to the surface temperature of the material, while physically sputtered particles are re-introduced with the TRIM-calculated energy sputtering yield (if the TRIM model is used). 
					Therm_evap turns on thermal evaporation when .gt.0.0 and is a multiplier to the thermal evaporation rate. 
					Redep_alpha is the multiplier to the reduction of the sputtering yield due to prompt redeposition. The promptly redeposited species is counted as eroded-then-deposited species.
				""", '0.00'),
   
      'b2stbr_redep_alpha' : ('', 'real', """
					Sputtering model switches. See the code in b2stbr and the b2mod_sputter module for specific implementation details and references. 
					The default values represent the case of Graphite plates. Sput_src is the atomic number of the plasma species which causes chemical sputtering. 
					Sput_dst (when .ge.0) is the species index of the destination species produced by physical sputtering, chemical sputtering and/or RES. If either of the latter two processes are included, the production chemical sputtering and RES rate calculations provided in the code assume that sput_dst points to a Carbon species. 
					Sput_dst2 and sput_dst3 (when .ge.0) represent other species produced by wall interactions for mixed materials scenarios. 
					Sput_frac_flag is the switch to turn on mixed materials scenarios (when sput_frac_flag.eq.1). 
					Plate_model.eq.0 means the 0-D time-independent plate heating model while plate_model.eq.1 indicates the 1-D time-dependent plate heating treatment. Plate_model.eq.2 gives acces to a 2-D time-dependent model. Plate_option chooses the initialisation of the plate temperature profile. If plate_option.eq.1, the profile is set to the constant given in plate_temp. If plate_option.eq.2, the profile is computed to be the 0-D equilibrium profile. If plate_option.eq.3, the profile is read from results of the previous run.
					Sput_phys_model is a switch for choosing between the TRIM tables (model 1, default) or an empirical formula (model 0). When TRIM data is not available, the empirical formula is automatically used. Extrapolations of low and high energy ranges beyond the TRIM table data is done using the same physical dependencies as the empirical formula. Sput_chem_model is a switch for the chemical sputtering model used. 
					If sput_chem_model.eq.0 (default), the empirical formula is used. 
					If sput_chem_model.eq.1, a constant with a low energy cut-off is used. 
					The cutoff occurs at approximately sput_chem_cutoff_alpha and the width is determined by sput_chem_cutoff_beta (the larger the value, the narrower the width over which the transition from 0 to 1 occurs). 
					For model 0, sput_frc is a multiplier to the empirical formula, while for model 1, sput_frc is the constant chemical sputtering yield. 
					Sput_frc is superseded by the chem_sput array from b2.neutrals.namelist if the latter is used. 
					For neutrals species, we add a factor of alpha*na*vbar to the particle flux to the plate (used to compute chemical and RES sputtering), where vbar is the average neutral particle speed. 
					Sput_phys turns on physical sputtering when sput_phys.gt.0.0 and contains a (real) multiplier for the physical sputtering rate looked up in the TRIM tables. It is superseded by the phys_sput array in b2.neutrals.parameters if the latter is used. 
					sput_phys_col indicates which column to use in the TRIM table; the default (3) corresponds to 30 degrees incidence. The columns are for
                      0 15 30 45 55 65 75 80 85
                    degrees. This angle is also used in the empirical formula. Plate_temp is the temperature (in Kelvin) of the COOLED end of the divertor plates. The surface temperature is computed self-consistently (using a 1-D description) according to the incident heat fluxes from the plasma. The plate is assumed to have a thickness of plate_thick, measured in meters. When plate_thick.eq.0 (default), the plate surface temperature is assumed to be the same as plate_temp. Sput_res turns on radiation enhanced sublimation (RES) when .gt.0.0 and is a multiplier to the RES rate. 
					The switch sputter_energy_on turns on the energy contribution from the sputtered particles (physical and chemical). If sputter_energy_on.eq.0, the particles are sputtered cold, with no energy contribution to the ion heat equation. 
					If sputter_energy_on.ne.0 (default), the chemically sputtered particles are re-introduced into the plasma with the thermal energy corresponding to the surface temperature of the material, while physically sputtered particles are re-introduced with the TRIM-calculated energy sputtering yield (if the TRIM model is used). 
					Therm_evap turns on thermal evaporation when .gt.0.0 and is a multiplier to the thermal evaporation rate. 
					Redep_alpha is the multiplier to the reduction of the sputtering yield due to prompt redeposition. The promptly redeposited species is counted as eroded-then-deposited species.
				""", '0.00'),
   
      'b2stbr_refl_model' : ('', 'integer', """
					Reflection model switches. If the recycling coefficients (particle and energy) are set to zero, then the code attempts to use, for surfaces in contact with walls, the TRIM reflection data for particle and energy reflection coefficients, when refl_model.eq.1. If refl_model.eq.0, an empirical formula is used instead. The model switch is subservient to reflection_on.ne.0. If reflection_on.eq.0, then no reflection is used. 
					If reflection_on.eq.1 (default), then the incident species is reflected unchanged. Otherwise, the reflected flux is of the associated neutral species to the incident particles.
				""", '1'),
   
      'b2stbr_reflection_on' : ('', 'integer', """
					Reflection model switches. If the recycling coefficients (particle and energy) are set to zero, then the code attempts to use, for surfaces in contact with walls, the TRIM reflection data for particle and energy reflection coefficients, when refl_model.eq.1. If refl_model.eq.0, an empirical formula is used instead. The model switch is subservient to reflection_on.ne.0. If reflection_on.eq.0, then no reflection is used. 
					If reflection_on.eq.1 (default), then the incident species is reflected unchanged. Otherwise, the reflected flux is of the associated neutral species to the incident particles.
				""", '1'),
   
      'b2tqna_user_transport' : ('', 'integer', """
					The last switch is subservient to b2tqna_user_transport, and only used if user_transport.ne.0. When this is the case, the electron perpendicular heat diffusivity and anomalous perpendicular particle transport coefficient are scaled so as to maintain the required_te_gradient (in units of eV/m), at the location (ixref,iyref) on the basis mesh. The default position of the reference cell is on the outer midplane, sligthly inside the separatrix, as follows:
					Configuration |     ixref                    |     iyref
					---------------+------------------------------+----------------------
					Single-null   | rightcut1(1)-                | 2*topcut1(1)/3
					| (rightcut1(1)-leftcut1(1))/4 |
					|                              |
					Double-null   | (rightcut1(1)+rightcut1(2))/2| 2*min(topcut1(1),
					|                              | topcut1(2))/3
					|                              |
					Straight      | 3*nx/4                       | ny/2
					|                              |
					The transport_eta switches are activated when user_transport.eq.3 and allow modifications of the electron heat conductivity according to a constant eta (Grad Te / Grad Ne) model. See routine set_transport_eta code for details.
					A model for disruption transport coefficients is available with user_transport.eq.7. See routine set_transport_disruption code for details.
					The value user_transport.eq.8 activates the neoclassical model for computation of the transport coefficients in the core. See routine set_transport_neo and subroutines called for details. Implemented from the NEOART package.
					The location given by ixref and iyref can also serve as the anchor point for the transport and/or sources profiles provided by the user in the b2.transport.inputfile and b2.sources.profile files.
				""", '0'),
   
      'set_transport_eta' : ('', 'real', """
					The last switch is subservient to b2tqna_user_transport, and only used if user_transport.ne.0. When this is the case, the electron perpendicular heat diffusivity and anomalous perpendicular particle transport coefficient are scaled so as to maintain the required_te_gradient (in units of eV/m), at the location (ixref,iyref) on the basis mesh. The default position of the reference cell is on the outer midplane, sligthly inside the separatrix, as follows:
					Configuration |     ixref                    |     iyref
					---------------+------------------------------+----------------------
					Single-null   | rightcut1(1)-                | 2*topcut1(1)/3
					| (rightcut1(1)-leftcut1(1))/4 |
					|                              |
					Double-null   | (rightcut1(1)+rightcut1(2))/2| 2*min(topcut1(1),
					|                              | topcut1(2))/3
					|                              |
					Straight      | 3*nx/4                       | ny/2
					|                              |
					The transport_eta switches are activated when user_transport.eq.3 and allow modifications of the electron heat conductivity according to a constant eta (Grad Te / Grad Ne) model. See routine set_transport_eta code for details.
					A model for disruption transport coefficients is available with user_transport.eq.7. See routine set_transport_disruption code for details.
					The value user_transport.eq.8 activates the neoclassical model for computation of the transport coefficients in the core. See routine set_transport_neo and subroutines called for details. Implemented from the NEOART package.
					The location given by ixref and iyref can also serve as the anchor point for the transport and/or sources profiles provided by the user in the b2.transport.inputfile and b2.sources.profile files.
				""", '2.0'),
   
      'set_transport_eta_alpha' : ('', 'real', """
					The last switch is subservient to b2tqna_user_transport, and only used if user_transport.ne.0. When this is the case, the electron perpendicular heat diffusivity and anomalous perpendicular particle transport coefficient are scaled so as to maintain the required_te_gradient (in units of eV/m), at the location (ixref,iyref) on the basis mesh. The default position of the reference cell is on the outer midplane, sligthly inside the separatrix, as follows:
					Configuration |     ixref                    |     iyref
					---------------+------------------------------+----------------------
					Single-null   | rightcut1(1)-                | 2*topcut1(1)/3
					| (rightcut1(1)-leftcut1(1))/4 |
					|                              |
					Double-null   | (rightcut1(1)+rightcut1(2))/2| 2*min(topcut1(1),
					|                              | topcut1(2))/3
					|                              |
					Straight      | 3*nx/4                       | ny/2
					|                              |
					The transport_eta switches are activated when user_transport.eq.3 and allow modifications of the electron heat conductivity according to a constant eta (Grad Te / Grad Ne) model. See routine set_transport_eta code for details.
					A model for disruption transport coefficients is available with user_transport.eq.7. See routine set_transport_disruption code for details.
					The value user_transport.eq.8 activates the neoclassical model for computation of the transport coefficients in the core. See routine set_transport_neo and subroutines called for details. Implemented from the NEOART package.
					The location given by ixref and iyref can also serve as the anchor point for the transport and/or sources profiles provided by the user in the b2.transport.inputfile and b2.sources.profile files.
				""", '0.5'),
   
      'set_transport_eta_floor' : ('', 'real', """
					The last switch is subservient to b2tqna_user_transport, and only used if user_transport.ne.0. When this is the case, the electron perpendicular heat diffusivity and anomalous perpendicular particle transport coefficient are scaled so as to maintain the required_te_gradient (in units of eV/m), at the location (ixref,iyref) on the basis mesh. The default position of the reference cell is on the outer midplane, sligthly inside the separatrix, as follows:
					Configuration |     ixref                    |     iyref
					---------------+------------------------------+----------------------
					Single-null   | rightcut1(1)-                | 2*topcut1(1)/3
					| (rightcut1(1)-leftcut1(1))/4 |
					|                              |
					Double-null   | (rightcut1(1)+rightcut1(2))/2| 2*min(topcut1(1),
					|                              | topcut1(2))/3
					|                              |
					Straight      | 3*nx/4                       | ny/2
					|                              |
					The transport_eta switches are activated when user_transport.eq.3 and allow modifications of the electron heat conductivity according to a constant eta (Grad Te / Grad Ne) model. See routine set_transport_eta code for details.
					A model for disruption transport coefficients is available with user_transport.eq.7. See routine set_transport_disruption code for details.
					The value user_transport.eq.8 activates the neoclassical model for computation of the transport coefficients in the core. See routine set_transport_neo and subroutines called for details. Implemented from the NEOART package.
					The location given by ixref and iyref can also serve as the anchor point for the transport and/or sources profiles provided by the user in the b2.transport.inputfile and b2.sources.profile files.
				""", '0.1'),
   
      'set_transport_eta_ceiling' : ('', 'real', """
					The last switch is subservient to b2tqna_user_transport, and only used if user_transport.ne.0. When this is the case, the electron perpendicular heat diffusivity and anomalous perpendicular particle transport coefficient are scaled so as to maintain the required_te_gradient (in units of eV/m), at the location (ixref,iyref) on the basis mesh. The default position of the reference cell is on the outer midplane, sligthly inside the separatrix, as follows:
					Configuration |     ixref                    |     iyref
					---------------+------------------------------+----------------------
					Single-null   | rightcut1(1)-                | 2*topcut1(1)/3
					| (rightcut1(1)-leftcut1(1))/4 |
					|                              |
					Double-null   | (rightcut1(1)+rightcut1(2))/2| 2*min(topcut1(1),
					|                              | topcut1(2))/3
					|                              |
					Straight      | 3*nx/4                       | ny/2
					|                              |
					The transport_eta switches are activated when user_transport.eq.3 and allow modifications of the electron heat conductivity according to a constant eta (Grad Te / Grad Ne) model. See routine set_transport_eta code for details.
					A model for disruption transport coefficients is available with user_transport.eq.7. See routine set_transport_disruption code for details.
					The value user_transport.eq.8 activates the neoclassical model for computation of the transport coefficients in the core. See routine set_transport_neo and subroutines called for details. Implemented from the NEOART package.
					The location given by ixref and iyref can also serve as the anchor point for the transport and/or sources profiles provided by the user in the b2.transport.inputfile and b2.sources.profile files.
				""", '10.0'),
   
      'set_transport_ixref' : ('', 'integer', """
					The last switch is subservient to b2tqna_user_transport, and only used if user_transport.ne.0. When this is the case, the electron perpendicular heat diffusivity and anomalous perpendicular particle transport coefficient are scaled so as to maintain the required_te_gradient (in units of eV/m), at the location (ixref,iyref) on the basis mesh. The default position of the reference cell is on the outer midplane, sligthly inside the separatrix, as follows:
					Configuration |     ixref                    |     iyref
					---------------+------------------------------+----------------------
					Single-null   | rightcut1(1)-                | 2*topcut1(1)/3
					| (rightcut1(1)-leftcut1(1))/4 |
					|                              |
					Double-null   | (rightcut1(1)+rightcut1(2))/2| 2*min(topcut1(1),
					|                              | topcut1(2))/3
					|                              |
					Straight      | 3*nx/4                       | ny/2
					|                              |
					The transport_eta switches are activated when user_transport.eq.3 and allow modifications of the electron heat conductivity according to a constant eta (Grad Te / Grad Ne) model. See routine set_transport_eta code for details.
					A model for disruption transport coefficients is available with user_transport.eq.7. See routine set_transport_disruption code for details.
					The value user_transport.eq.8 activates the neoclassical model for computation of the transport coefficients in the core. See routine set_transport_neo and subroutines called for details. Implemented from the NEOART package.
					The location given by ixref and iyref can also serve as the anchor point for the transport and/or sources profiles provided by the user in the b2.transport.inputfile and b2.sources.profile files.
				""", 'See description (integer)'),
   
      'set_transport_iyref' : ('', 'integer', """
					The last switch is subservient to b2tqna_user_transport, and only used if user_transport.ne.0. When this is the case, the electron perpendicular heat diffusivity and anomalous perpendicular particle transport coefficient are scaled so as to maintain the required_te_gradient (in units of eV/m), at the location (ixref,iyref) on the basis mesh. The default position of the reference cell is on the outer midplane, sligthly inside the separatrix, as follows:
					Configuration |     ixref                    |     iyref
					---------------+------------------------------+----------------------
					Single-null   | rightcut1(1)-                | 2*topcut1(1)/3
					| (rightcut1(1)-leftcut1(1))/4 |
					|                              |
					Double-null   | (rightcut1(1)+rightcut1(2))/2| 2*min(topcut1(1),
					|                              | topcut1(2))/3
					|                              |
					Straight      | 3*nx/4                       | ny/2
					|                              |
					The transport_eta switches are activated when user_transport.eq.3 and allow modifications of the electron heat conductivity according to a constant eta (Grad Te / Grad Ne) model. See routine set_transport_eta code for details.
					A model for disruption transport coefficients is available with user_transport.eq.7. See routine set_transport_disruption code for details.
					The value user_transport.eq.8 activates the neoclassical model for computation of the transport coefficients in the core. See routine set_transport_neo and subroutines called for details. Implemented from the NEOART package.
					The location given by ixref and iyref can also serve as the anchor point for the transport and/or sources profiles provided by the user in the b2.transport.inputfile and b2.sources.profile files.
				""", 'See description (integer)'),
   
      'set_transport_required_te_gradient' : ('', 'real', """
					The last switch is subservient to b2tqna_user_transport, and only used if user_transport.ne.0. When this is the case, the electron perpendicular heat diffusivity and anomalous perpendicular particle transport coefficient are scaled so as to maintain the required_te_gradient (in units of eV/m), at the location (ixref,iyref) on the basis mesh. The default position of the reference cell is on the outer midplane, sligthly inside the separatrix, as follows:
					Configuration |     ixref                    |     iyref
					---------------+------------------------------+----------------------
					Single-null   | rightcut1(1)-                | 2*topcut1(1)/3
					| (rightcut1(1)-leftcut1(1))/4 |
					|                              |
					Double-null   | (rightcut1(1)+rightcut1(2))/2| 2*min(topcut1(1),
					|                              | topcut1(2))/3
					|                              |
					Straight      | 3*nx/4                       | ny/2
					|                              |
					The transport_eta switches are activated when user_transport.eq.3 and allow modifications of the electron heat conductivity according to a constant eta (Grad Te / Grad Ne) model. See routine set_transport_eta code for details.
					A model for disruption transport coefficients is available with user_transport.eq.7. See routine set_transport_disruption code for details.
					The value user_transport.eq.8 activates the neoclassical model for computation of the transport coefficients in the core. See routine set_transport_neo and subroutines called for details. Implemented from the NEOART package.
					The location given by ixref and iyref can also serve as the anchor point for the transport and/or sources profiles provided by the user in the b2.transport.inputfile and b2.sources.profile files.
				""", '5.0e4'),
   
      'b2tqna_max_df0' : ('', 'real', """
					Upper and lower limits of the diffusivity coefficients df0 computed in b2tqna for each species.
				""", '1e30'),
   
      'b2tqna_min_df0' : ('', 'real', """
					Upper and lower limits of the diffusivity coefficients df0 computed in b2tqna for each species.
				""", '0.0'),
   
      'b2tqna_ballooning' : ('', 'real', """
					Ballooning model switches. If ballooning.ne.0, then all transport coefficients in cell (i) are rescaled by a factor of ballooning_rescale*abs(bb_ref/bb(i))**ballooning . 
					The default value for bb_ref is the arithmetic average of the total magnetic field strength over the entire computational domain.
				""", '0.0'),
   
      'b2tqna_ballooning_rescale' : ('', 'real', """
					Ballooning model switches. If ballooning.ne.0, then all transport coefficients in cell (i) are rescaled by a factor of ballooning_rescale*abs(bb_ref/bb(i))**ballooning . 
					The default value for bb_ref is the arithmetic average of the total magnetic field strength over the entire computational domain.
				""", '1.0'),
   
      'b2tqna_bb_ref' : ('', 'real', """
					Ballooning model switches. If ballooning.ne.0, then all transport coefficients in cell (i) are rescaled by a factor of ballooning_rescale*abs(bb_ref/bb(i))**ballooning . 
					The default value for bb_ref is the arithmetic average of the total magnetic field strength over the entire computational domain.
				""", 'See description (real)'),
   
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
					The default formula is to use the Braginskii formulation, which will give the same answer for electron-electron (ee), electron-ion (ei), and ion-ion (ii) collisions. Respectively, non-default values of '1', '2' and '3' for b2tlnl_ee, _ei, and _ii, respectively, make use of the calculation according to Wesson.
				""", '-5.0'),
   
      'b2tlnl_ee' : ('', 'integer', """
					If lambda is positive, the Coulomb logarithm is set to lambda. 
					If lambda is negative, then abs(lambda) is the lower bound to be used when computing the Coulomb logarithm according to the NRL formulae. 
					The computation of the Coulomb logarithm takes place in b2tlnl. 
					The default formula is to use the Braginskii formulation, which will give the same answer for electron-electron (ee), electron-ion (ei), and ion-ion (ii) collisions. Respectively, non-default values of '1', '2' and '3' for b2tlnl_ee, _ei, and _ii, respectively, make use of the calculation according to Wesson.
				""", '0'),
   
      'b2tlnl_ei' : ('', 'integer', """
					If lambda is positive, the Coulomb logarithm is set to lambda. 
					If lambda is negative, then abs(lambda) is the lower bound to be used when computing the Coulomb logarithm according to the NRL formulae. 
					The computation of the Coulomb logarithm takes place in b2tlnl. 
					The default formula is to use the Braginskii formulation, which will give the same answer for electron-electron (ee), electron-ion (ei), and ion-ion (ii) collisions. Respectively, non-default values of '1', '2' and '3' for b2tlnl_ee, _ei, and _ii, respectively, make use of the calculation according to Wesson.
				""", '0'),
   
      'b2tlnl_ii' : ('', 'integer', """
					If lambda is positive, the Coulomb logarithm is set to lambda. 
					If lambda is negative, then abs(lambda) is the lower bound to be used when computing the Coulomb logarithm according to the NRL formulae. 
					The computation of the Coulomb logarithm takes place in b2tlnl. 
					The default formula is to use the Braginskii formulation, which will give the same answer for electron-electron (ee), electron-ion (ei), and ion-ion (ii) collisions. Respectively, non-default values of '1', '2' and '3' for b2tlnl_ee, _ei, and _ii, respectively, make use of the calculation according to Wesson.
				""", '0'),
   
      'b2tfnb_alpha' : ('', 'real', """
					Parameters for the flux limit to the convective neutral flow. 
					Alpha is a multiplier to the classical flux limit value. 
					The larger alpha is, the weaker the flux limit is. 
					Gamma is the exponent used in the flux-limiting formula. 
					The smaller gamma is, the stronger the flux limit is. 
					If alpha.eq.0, no flux limit is applied. 
					flux_limit_min_ti specifies the minimum ti to be used (in eV).
				""", '0.0'),
   
      'b2tfnb_gamma' : ('', 'real', """
					Parameters for the flux limit to the convective neutral flow. 
					Alpha is a multiplier to the classical flux limit value. 
					The larger alpha is, the weaker the flux limit is. 
					Gamma is the exponent used in the flux-limiting formula. 
					The smaller gamma is, the stronger the flux limit is. 
					If alpha.eq.0, no flux limit is applied. 
					flux_limit_min_ti specifies the minimum ti to be used (in eV).
				""", '2.0'),
   
      'b2tfnb_flux_limit_min_ti' : ('', 'real', """
					Parameters for the flux limit to the convective neutral flow. 
					Alpha is a multiplier to the classical flux limit value. 
					The larger alpha is, the weaker the flux limit is. 
					Gamma is the exponent used in the flux-limiting formula. 
					The smaller gamma is, the stronger the flux limit is. 
					If alpha.eq.0, no flux limit is applied. 
					flux_limit_min_ti specifies the minimum ti to be used (in eV).
				""", '0.0'),
   
      'b2tlc0_alpha' : ('', 'real', """
					Parameters for the flux limit to dpa0 - pressure driven neutral diffusion. 
					Alpha is a multiplier to the classical flux limit value. 
					Gamma is the exponent used in the flux-limiting formula. If alpha.eq.0, no flux limit is applied.
				""", '0.0'),
   
      'b2tlc0_gamma' : ('', 'real', """
					Parameters for the flux limit to dpa0 - pressure driven neutral diffusion. 
					Alpha is a multiplier to the classical flux limit value. 
					Gamma is the exponent used in the flux-limiting formula. If alpha.eq.0, no flux limit is applied.
				""", '2.0'),
   
      'b2tlh0_alpha' : ('', 'real', """
					Parameters for the flux limit to the heat conductivity of the neutrals. Alpha is a multiplier to the classical flux limit value. 
					The larger alpha is, the weaker the flux limit is. 
					Gamma is the exponent used in the flux-limiting formula. 
					The smaller gamma is, the stronger the flux limit is. 
					If alpha.eq.0, no flux limit is applied. 
					flux_limit_min_ti specifies the minimum ti to be used (in eV).
				""", '0.0'),
   
      'b2tlh0_gamma' : ('', 'real', """
					Parameters for the flux limit to the heat conductivity of the neutrals. Alpha is a multiplier to the classical flux limit value. 
					The larger alpha is, the weaker the flux limit is. 
					Gamma is the exponent used in the flux-limiting formula. 
					The smaller gamma is, the stronger the flux limit is. 
					If alpha.eq.0, no flux limit is applied. 
					flux_limit_min_ti specifies the minimum ti to be used (in eV).
				""", '2.0'),
   
      'b2tlh0_flux_limit_min_ti' : ('', 'real', """
					Parameters for the flux limit to the heat conductivity of the neutrals. Alpha is a multiplier to the classical flux limit value. 
					The larger alpha is, the weaker the flux limit is. 
					Gamma is the exponent used in the flux-limiting formula. 
					The smaller gamma is, the stronger the flux limit is. 
					If alpha.eq.0, no flux limit is applied. 
					flux_limit_min_ti specifies the minimum ti to be used (in eV).
				""", '0.0'),
   
      'b2sqcx_styl0' : ('', 'integer', """
					phm0 : Multiplier to the charge exchange rate coefficient. Subservient to styl0: only used if styl0.eq.0 or is.lt.2. If styl0.ne.0, the charge exchange rate coefficients for species of index 2 and above are set to zero.
				""", '0'),
   
      'b2sqcx_phm0' : ('', 'real', """
					phm0 : Multiplier to the charge exchange rate coefficient. Subservient to styl0: only used if styl0.eq.0 or is.lt.2. If styl0.ne.0, the charge exchange rate coefficients for species of index 2 and above are set to zero.
				""", '1.0'),
   
      'b2siav_addvis' : ('Physics', 'real', """
					Multiplier to heat flux contribution to divergence of viscosity tensor in the momentum equation.
				""", '0.0'),
   
      'b2siav_addvis1' : ('Physics', 'real', """
					When not equal to '0.0', adds contribution to divergence of viscosity tensor coming from x-variations in B.
				""", '1.0'),
   
      'b2npmo_b2sifr_' : ('Physics', 'integer', """
					When set to '1', the new correct form of the friction force is used. 
					The value '0' corresponds to the old SOLPS5.0 treatment.
				""", '1'),
   
      'b2sihs_istyle_Joule_heating' : ('Physics', 'integer', """
					When set to '1', there is no radial contribution in Joule heating because there are no physical reasons to take it into account. 
					The value '0' corresponds to the old SOLPS5.0 treatment.
				""", '1'),
   
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
   
      'b2tfhe_neutral' : ('Physics', 'real', """
					Real parameter which multiplies ion-neutral current. 
					If b2tfhe_neutral is 0 then ion-neutral current is switched off otherwise ion-neutral current is switched on.
				""", '0.0'),
   
      'b2tfhe_vis_par' : ('Physics', 'real', """
					Real parameter which multiplies current driven by parallel viscosity. 
					If b2tfhe_vis_par is 0 then viscosity-driven current is switched off otherwise viscosity-driven current is switched on.
				""", '0.0'),
   
      'b2tfhe_vis_q' : ('Physics', 'real', """
					Real parameter which multiplies current driven by heat viscosity effects.
				""", '1.0'),
   
      'b2trcl_lluciani' : ('Physics', 'integer', """
					If lluciani.ne.0, then transport coefficients on cells belonging to closed field lines are modified according to the Luciani model. 
					If lluciani.eq.1, the standard connection length formulation is used. 
					If lluciani.eq.2, the old SOLPS4.0 formulation is used for backward compatibility. 
					If lluciani.eq.3, Spb's new form Luciani's coefficient.
				""", '3'),
   
      'b2trcl_lthf21' : ('Physics', 'integer', """
					If lthf21.ne.0, then the heat transfer model is modified according to the 21-moment approach. This should only be used for multi-fluid runs.
				""", '0'),
   
      'b2trcl_lvis21' : ('Physics', 'integer', """
					If lvis21.ne.0, then the viscosities are modified according to the 21-moment approach. This should only be used for multi-fluid runs. This switch should not be used along with 'b2tfhe_vis_par' to avoid double-counting of classical viscosity effects.
				""", '0'),
   
      'b2sqel_artificial_radiation' : ('Physics', 'real', """
					If art_rad.ne.0, then an artificial radiation loss term is added to the electron cooling rate. Art_rad represents the percent fraction of impurities in the plasma.
				""", '0.0'),
   
      'b2stbc_secmodel' : ('Physics', 'integer', """
					If secmodel.eq.1, then the secondary electron emission coefficient at the plates is computed locally according to a kinetic model, otherwise the default values of cbsch(7,ireg) and/or gammae are used.
				""", '0'),
   
      'b2mndr_coronal_model' : ('Physics', 'integer', """
					Turns on the coronal model if coronal.ne.0. I.e., the reaction rates of all reactions are made density-independent, and the value computed at the lowest density (given in b2ar.dat) is used.
				""", '0'),
   
      'b2mndr_hz' : ('Physics', 'real', """
					hz has been introduced into the new form of the parallel momentum balance equation. If fac_hz = 0.0 then hz = 1 and old form of equations is used. If fac_hz = 1.0 then new form of equations is used.
				""", '0.0'),
   
      'b2stbr_bas_recycled_neutrals_contr' : ('Physics', 'real', """
					Introduced for nulling recycling energy when it is zero.
				""", '1.0'),
   
      'b2tfhe_alfTeEh' : ('Physics', 'real', """
					When set to '0.0', the old form of the electron heat flux calculation is used. It is recommended to use 1.0.
				""", '0.0'),
   
      'b2tfhe_fch_pTe' : ('Physics', 'real', """
					When set to '1.0', the new form of the electron heat flux calculation is used. It is recommended to use 1.0.
				""", '1.0'),
   
      'b2tfnb_ycur' : ('Physics', 'real', """
					Ycur is a multiplier to the parallel viscosity, ion inertial and anomalous currents to the ion radial flows (particle and energy).
				""", '1.0'),
   
      'b2tqce_fke_Zhdanov' : ('Physics', 'integer', """
					When set to '1', Zhdanov's expression is used in the electron thermal conductivity. It is recommended to use 'b2tqce_fke_Zhdanov' '1'. 
					This switch is only active if, simultaneously, one has b2tqce_model.eq.1 and b2tfhe_fch_pTe.eq.1.0.
				""", '1'),
   
      'b2tqna_ixref' : ('Physics', 'integer', """
					Poloidal index (on the basis mesh) of the reference surface for the flux-scaled transport model. The default value is the outer midplane, computed as such (see b2mwti_jxa in Geometry section or set_transport_ixref below): 
					Single-null : ixref=rightcut1(1)-(rightcut1(1)-leftcut1(1))/4. 
					Double-null : ixref=(rightcut1(1)+rightcut1(2))/2. Straight geometry : ixref=3*nx/4. 
					The flux-scaled transport model is used in conjunction with scaling factors listed in column (7) of the transport coefficients description in input files b2ah.dat and b2mn.dat.
				""", 'See description (integer)'),
   
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
					Multiplier of the friction term between charged species.
				""", '1.0'),
   
      'b2sifr_phm1' : ('Physics', 'real', """
					Multiplier of the ehxp term in the thermal force term.
				""", '1.0'),
   
      'b2sifr_phm2' : ('Physics', 'real', """
					Multiplier of the electron thermal gradient term in the thermal force term
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
					if style = 0 then it is applied the origin flux limit to the viscosity else it is applied the SPb flux limit to the viscosity
				""", '1'),
   
      'b2sihs_phm0' : ('Physics', 'real', """
					Multiplier of the contribution to electron heat sources from divergence(ue,ve).
				""", '1.0'),
   
      'b2sihs_phm1' : ('Physics', 'real', """
					Multiplier of the contribution to ion heat sources from divergence(ua,va). This term is superseded by the BoRiS switch if invoked.
				""", '1.0'),
   
      'b2sihs_phm2' : ('Physics', 'real', """
					Multiplier of the contribution to ion heat sources from viscous heating. This term is superseded by the BoRiS switch if invoked.
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
   
      'b2sdia_facgt' : ('Physics', 'real', """
					Multiplier of the contribution to electron and ion heat sources from divergence of the gradTxB heat flux. That contribution is also multiplied by facdrift. This term is no longer needed as it has been transferred from being a source to being included in the flows.
				""", '0.0'),
   
      'b2sral_style' : ('Physics', 'integer', """
					When set to '0', in the expression of the electron particle flux (fne) the particle flux with drift terms is used and temporary drift velocities on the first call are calculated. When set to '1' or '2', the particle flux without drift terms is used in fne. It is recommended '2'.
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
					Multiplier of the recombination contribution to the electron cooling rate (if ADPAK rates are not used because those are already included). Assumes all recombination is three-body.
				""", '0.0'),
   
      'b2tfhe_lim_flux' : ('Physics', 'integer', """
					If '0', flux limit is not applied directly to the electron heat flux but is applied through transport coefficients if 'b2trcl_conductive_limit' is '1'. It is recommended '0'.
				""", '0'),
   
      'b2tfhi_lim_flux' : ('Physics', 'integer', """
					If '0', flux limit is not applied directly to the ion heat flux but is applied through transport coefficients if 'b2trcl_conductive_limit' is '1'. It is recommended '0'.
				""", '1'),
   
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
   
      'b2trno_pol_anom_scale' : ('Physics', 'real', """
					If pol_anom_scale.ne.1, the poloidal anomalous transport coefficients are scaled by the number. To get the same treatment as setting the old switch (radial_only) to 1, set the new switch to 0.0. 
					This multiplication is to only take place for charged species.
				""", '1.0'),
   
      'eirene_lhalpha' : ('Physics', 'integer', """
					If 0 then no calculation of halpha in wneutral, otherwise halpha is calculated
				""", '1'),
   
      'eirene_lvib' : ('Physics', 'integer', """
					If 0 then the sigadd4 (molecular ions) and sigadd5 (negative ions) contributions to the halpha in wneutral are not included, otherwise they are
				""", '0'),
   
      'eirene_repeat_first_call' : ('Physics', 'integer', """
					If &gt; 0 then repeats the first call to eirene in eirene_mc so many times. 
					Useful if a density feedback gas puff is being used because the flux passed to Eirene on its first call is ignored (instead the value in the Eirene input file is used).
				""", '1'),
   
      'eirene_use_recyceir' : ('Physics', 'integer', """
					If &gt; 0 use recyceir (non species dependent) to specify the recycling* coefficients, else if 0 use recyc (species dependent).
				""", '1'),
   
      'eirene_ionising_core' : ('Physics', 'integer', """
					If &lt;&gt; 0 then recycles the neutral flux having crossed the core boundary within Eirene as ions. The recycling is surface-averaged, and neutrals come back as fully-stripped ions. 
					'eirene_ionizing_core' is an alias for this switch. 
					If the value = 1, then the flux is added by direct modification of the sources in the guard cells --- this will only work if a standard flux boundary condition is applied at that boundary. 
					If the value is &lt; 0, then the absolute value specifies which boundary in b2.boundary.parameters is to be used. This will only work for the new type 13 boundary condition.
				""", '0'),
   
      'eirene_background' : ('Physics', 'integer', """
					If eirene_background.eq.0, the ion velocities passed to Eirene to be used for the collisions are based on grad-B and ExB drifts (vadia + vaecrb).
					If eirene_background.eq.1, these velocities contain the full diamagnetic and ExB drifts (wadia + vaecrb).
					Note: recycling fluxes are always computed based on grad-B and ExB drifts only (and are not affected by this switch), because diamagnetic drift flows largely close within the sheath.
				""", '1'),
   
      'eirene_sheath_pot' : ('Physics', 'integer', """
					If eirene_sheath_pot.eq.1, the sheath potential drop as computed by B2.5 (i.e. including effects of parallel currents, secondary electron emission, etc.) is passed to EIRENE to compute ion acceleration in the sheath. 
					If eirene_sheath_pot.eq.0, the sheath potential drop is 
					recomputed by EIRENE, usually assuming zero current and secondary
					electron emission.
				""", '1'),
   
      'b2stel_fix_recomb_energy' : ('Physics', 'integer', """
					If changed to 1, then the recombination energy (rpi) is added to the electron energy for each recombination. This should only be used if the is--&gt;is-1 energy terms have been included in the electron cooling rates (as done by setting the switch 'b2ardr_fix_recomb' in b2ar.dat to a non-zero value and recalculating b2frates).
					See 'Atomic Physics' section.
					*** Use with caution! ***
				""", '0'),
   
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
					mind that B2 already calculates the classical transport !
					avoid double transport, 0+4 for cross checks only !
				""", '3'),
   
      'b2mndr_na_eps' : ('', 'real', """
					The five switches above are safeguards numbers for when printing changes after a time-step. The change is computed as: deltaX = abs((X(t)-X(t-1))/(X(t)+X_eps))
				""", '1.0e19'),
   
      'b2mndr_po_eps' : ('', 'real', """
					The five switches above are safeguards numbers for when printing changes after a time-step. The change is computed as: deltaX = abs((X(t)-X(t-1))/(X(t)+X_eps))
				""", '1.0e+1'),
   
      'b2mndr_te_eps' : ('', 'real', """
					The five switches above are safeguards numbers for when printing changes after a time-step. The change is computed as: deltaX = abs((X(t)-X(t-1))/(X(t)+X_eps))
				""", '1.0e+1'),
   
      'b2mndr_ti_eps' : ('', 'real', """
					The five switches above are safeguards numbers for when printing changes after a time-step. The change is computed as: deltaX = abs((X(t)-X(t-1))/(X(t)+X_eps))
				""", '1.0e+1'),
   
      'b2mndr_ua_eps' : ('', 'real', """
					The five switches above are safeguards numbers for when printing changes after a time-step. The change is computed as: deltaX = abs((X(t)-X(t-1))/(X(t)+X_eps))
				""", '1.0e+4'),
   
      'tallies_netcdf' : ('', 'integer', """
					If tallies_netcdf.ne.0, the file 'b2tallies.nc' is created, which contains the regional tallies in CDF format.
					If b2wall_netcdf.ne.0, the file 'b2wall.nc' is created, which contains the wall tallies in CDF format [written every b2wall_netcdf 'main calls'].
				""", '0'),
   
      'b2stbr_b2wall_netcdf' : ('', 'integer', """
					If tallies_netcdf.ne.0, the file 'b2tallies.nc' is created, which contains the regional tallies in CDF format.
					If b2wall_netcdf.ne.0, the file 'b2wall.nc' is created, which contains the wall tallies in CDF format [written every b2wall_netcdf 'main calls'].
				""", '0'),
   
      'balance_netcdf' : ('', '', """
					If tallies_netcdf.ne.0, the file 'b2tallies.nc' is created, which contains the regional tallies in CDF format.
					If b2wall_netcdf.ne.0, the file 'b2wall.nc' is created, which contains the wall tallies in CDF format [written every b2wall_netcdf 'main calls'].
				""", '0'),
   
      'eirene_savef30' : ('', 'integer', """
					For coupled runs, the code will create two files named fort.30 and fort.31, containing the plasma geometry and plasma state, respectively, for use by Eirene. This happens irrespective of the setting of the two switches above. If however, the user wishes to obtain these files for a non-coupled run, then these two switches can be set to 1 and the files will then be produced at the end of the run. If savef31.lt.0, then a fort.31.###### file is produced after every B2.5 time step. Additionally, if savef31.ne.0, the fort.31 file will be updated before every Eirene call for coupled runs.
				""", '0'),
   
      'eirene_savef31' : ('', 'integer', """
					For coupled runs, the code will create two files named fort.30 and fort.31, containing the plasma geometry and plasma state, respectively, for use by Eirene. This happens irrespective of the setting of the two switches above. If however, the user wishes to obtain these files for a non-coupled run, then these two switches can be set to 1 and the files will then be produced at the end of the run. If savef31.lt.0, then a fort.31.###### file is produced after every B2.5 time step. Additionally, if savef31.ne.0, the fort.31 file will be updated before every Eirene call for coupled runs.
				""", '0'),
   
      'b2ux5p_nltrsol' : ('', 'integer', """
					Output flag for the iluter matrix solver. Larger numbers mean increasing output level.
				""", '2'),
   
      'b2ux7p_nltrsol' : ('', 'integer', """
					Output flag for the iluter matrix solver. Larger numbers mean increasing output level.
				""", '0'),
   
      'b2ux9p_nltrsol' : ('', 'integer', """
					Output flag for the iluter matrix solver. Larger numbers mean increasing output level.
				""", '0'),
   
      'b2mndr_idout0' : ('', '', """
					idout0 and idout1 specify the desired selection of output segments; idout0 for output before the calculation and idout1 for output at the conclusion of the calculation. The generic description of either of these 'idout' variables follows. idout specifies the desired selection of output segments for printed and graphical output. Associated with each segment is a four-character word, which is identified on the printed output. (The same word may be associated with several segments.) A particular segment will be produced only if its associated word has a match, as defined by the routine strmas, in idout.
				""", 'pgnl;pgmm;pzmm'),
   
      'b2mndr_idout1' : ('', '', """
					idout0 and idout1 specify the desired selection of output segments; idout0 for output before the calculation and idout1 for output at the conclusion of the calculation. The generic description of either of these 'idout' variables follows. idout specifies the desired selection of output segments for printed and graphical output. Associated with each segment is a four-character word, which is identified on the printed output. (The same word may be associated with several segments.) A particular segment will be produced only if its associated word has a match, as defined by the routine strmas, in idout.
				""", 'pzmm'),
   
      'b2mndr_b2time' : ('Output', 'integer', """
					Specifies the number of timesteps between writes of the time-dependent file. If b2time.gt.0, always writes out on the last timestep.
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
					Another option for movie output. Give the real-time interval between movie frames.
				""", '0.0'),
   
      'b2mndr_ntim_save' : ('Output', 'integer', """
					Another option for plasma state file output. Give the number of B2.5 full interations between succesive write-ups of plasmastate files, in addition to the ones written at regular CPU intervals. Should be used, at the exclusion of other plasmastate write-up frequency settings, in conjunction with the Leuven Monte-Carlo averaging scheme.
				""", '0'),
   
      'b2mndr_plasmatim' : ('Output', 'real', """
					Another option for plasma state file output. Give the real-time interval between succesive write-ups of plasmastate files, in addition to the ones written at regular CPU intervals.
				""", '0.0'),
   
      'b2wdat_iout' : ('Output', 'integer', """
					If iout.eq.1, a large set of *.dat output files will be produced containing the values of a variety of code quantities. See the "Output description" file for details.
				""", '0'),
   
      'b2mndr_trantim' : ('Output', 'real', """
					Produces a numbered 'tran' file every trantim real-time seconds. An endstate file is written if it falls between scheduled write-up times. Only available within the -DJET environment.
				""", '0.0'),
   
      'b2mwti_target_offset' : ('Output', 'integer', """
					The diagnostic values from b2time.nc use guard cell values if target_offset.eq.0, and values from the neighbouring real cell if target_offset.eq.1. Fluxes are not affected.
				""", '1'),
   
      'b2mwti_ismain0' : ('Output', 'integer', """
					Index of the species used to create the 'dp3d?.last10' diagnostic files.
					Defaults to the neutral species associated with ismain. If no such species is declared, the default will be set to ismain. Is expected to either correspond to a neutral species or to ismain.
					If ismain is also defaulted, then will be 0.
				""", '0'),
   
      'b2mwqt_style' : ('Output', 'integer', """
					Specifies the amount of data that is written out to b2ftrace. See the manual (Section on b2yq) for full details.
				""", '1'),
   
      'ank_tracing' : ('Output', 'integer', """
					If ank_tracing.ge.1, additional tracing output from Andrei Kukushkin is produced, in files to be found in the tracing/ directory inside the run directory. The traces will be written every ank_tracing iteration.
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
   
      'b2news_potit' : ('', 'integer', """
					Maximum and minimum number of iterations in the potential equation. It must hold that potitmin &lt; potit.
				""", '50'),
   
      'b2news_potitmin' : ('', 'integer', """
					Maximum and minimum number of iterations in the potential equation. It must hold that potitmin &lt; potit.
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
					All non-zero criteria must be met simultaneously. The continuity equation residual applies to the 'ismain' species (See 'Run' section).
				""", '0.0'),
   
      'b2mndt_nstg_areshi' : ('', 'real', """
					Minimum residuals for an internal solution loop to stop.
					Used in conjunction with (not in replacement of) the nstg(0:2) numbers.
					All non-zero criteria must be met simultaneously. The continuity equation residual applies to the 'ismain' species (See 'Run' section).
				""", '0.0'),
   
      'b2mndt_nstg_aresco' : ('', 'real', """
					Minimum residuals for an internal solution loop to stop.
					Used in conjunction with (not in replacement of) the nstg(0:2) numbers.
					All non-zero criteria must be met simultaneously. The continuity equation residual applies to the 'ismain' species (See 'Run' section).
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
   
      'b2tfhe_no_hybr' : ('', 'integer', """
					Switches to toggle between the standard 5.0 hybrid scheme (no_hybr.eq.0) and the old 4.0 upwind scheme (no_hybr.eq.1).
					These apply separately to the electron heat, ion heat and particle conservation equations.
					If hybr2.ne.0, then a mixed scheme is used where only the conductivity is computed according to the 4.0 scheme.
				""", '0'),
   
      'b2tfhi_no_hybr' : ('', 'integer', """
					Switches to toggle between the standard 5.0 hybrid scheme (no_hybr.eq.0) and the old 4.0 upwind scheme (no_hybr.eq.1).
					These apply separately to the electron heat, ion heat and particle conservation equations.
					If hybr2.ne.0, then a mixed scheme is used where only the conductivity is computed according to the 4.0 scheme.
				""", '0'),
   
      'b2tfnb_no_hybr' : ('', 'integer', """
					Switches to toggle between the standard 5.0 hybrid scheme (no_hybr.eq.0) and the old 4.0 upwind scheme (no_hybr.eq.1).
					These apply separately to the electron heat, ion heat and particle conservation equations.
					If hybr2.ne.0, then a mixed scheme is used where only the conductivity is computed according to the 4.0 scheme.
				""", '0'),
   
      'b2tfhe_hybr2' : ('', 'integer', """
					Switches to toggle between the standard 5.0 hybrid scheme (no_hybr.eq.0) and the old 4.0 upwind scheme (no_hybr.eq.1).
					These apply separately to the electron heat, ion heat and particle conservation equations.
					If hybr2.ne.0, then a mixed scheme is used where only the conductivity is computed according to the 4.0 scheme.
				""", '0'),
   
      'b2tfhi_hybr2' : ('', 'integer', """
					Switches to toggle between the standard 5.0 hybrid scheme (no_hybr.eq.0) and the old 4.0 upwind scheme (no_hybr.eq.1).
					These apply separately to the electron heat, ion heat and particle conservation equations.
					If hybr2.ne.0, then a mixed scheme is used where only the conductivity is computed according to the 4.0 scheme.
				""", '0'),
   
      'b2tfhe_upwind' : ('', 'integer', """
					If upwind.ne.0, then the SOLPS4 upwind scheme in b2tfhe_ and b2tfhi_ to obtain the heat fluxes.
				""", '0'),
   
      'b2tfhi_upwind' : ('', 'integer', """
					If upwind.ne.0, then the SOLPS4 upwind scheme in b2tfhe_ and b2tfhi_ to obtain the heat fluxes.
				""", '0'),
   
      'b2ux5p_mult_solvdim' : ('', 'integer', """
					Multipliers to the number of nonzero elements in the solution matrix for workspace arrays in the matrix solver.
				""", '15'),
   
      'b2ux5p_mult_solvdim1' : ('', 'integer', """
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
   
      'b2news_fac_ref' : ('', '', """
					Parameters for spatial variation of the diamagnetic, ExB and viscosity drift term multipliers. These are allowed to have tanh profiles centered at tanh_a and of width tanh_b, where both quantities are in metres and measured along the radial coordinate for the cell column ix.eq.fac_ref (default value is jxa, see Geometry section for its computation). The maximum value of facdrift and fac_ExB is controlled by their respective _start and _target switches, see Run section for details.
					For consistency with the naming convention of related variables:
					b2news_facExB_tanh_a is an alias for b2news_fac_ExB_tanh_a,
					b2news_facExB_tanh_b is an alias for b2news_fac_ExB_tanh_b,
					b2news_facvis_tanh_a is an alias for b2news_fac_vis_tanh_a, and b2news_facvis_tanh_b is an alias for b2news_fac_vis_tanh_b. Additionally, for all core cell rows where iy.le.iy_nocoreExB, fac_ExB(ix,iy) is set to zero. This means that ExB contributions and flows will be zeroed out in those cells.
					For consistency with the boundary condition treatment, the value iy_nocoreExB.eq.-1 is NOT recommended!
				""", 'See description (integer)'),
   
      'b2news_facdrift_tanh_a' : ('', 'real', """
					Parameters for spatial variation of the diamagnetic, ExB and viscosity drift term multipliers. These are allowed to have tanh profiles centered at tanh_a and of width tanh_b, where both quantities are in metres and measured along the radial coordinate for the cell column ix.eq.fac_ref (default value is jxa, see Geometry section for its computation). The maximum value of facdrift and fac_ExB is controlled by their respective _start and _target switches, see Run section for details.
					For consistency with the naming convention of related variables:
					b2news_facExB_tanh_a is an alias for b2news_fac_ExB_tanh_a,
					b2news_facExB_tanh_b is an alias for b2news_fac_ExB_tanh_b,
					b2news_facvis_tanh_a is an alias for b2news_fac_vis_tanh_a, and b2news_facvis_tanh_b is an alias for b2news_fac_vis_tanh_b. Additionally, for all core cell rows where iy.le.iy_nocoreExB, fac_ExB(ix,iy) is set to zero. This means that ExB contributions and flows will be zeroed out in those cells.
					For consistency with the boundary condition treatment, the value iy_nocoreExB.eq.-1 is NOT recommended!
				""", '0.0'),
   
      'b2news_facdrift_tanh_b' : ('', 'real', """
					Parameters for spatial variation of the diamagnetic, ExB and viscosity drift term multipliers. These are allowed to have tanh profiles centered at tanh_a and of width tanh_b, where both quantities are in metres and measured along the radial coordinate for the cell column ix.eq.fac_ref (default value is jxa, see Geometry section for its computation). The maximum value of facdrift and fac_ExB is controlled by their respective _start and _target switches, see Run section for details.
					For consistency with the naming convention of related variables:
					b2news_facExB_tanh_a is an alias for b2news_fac_ExB_tanh_a,
					b2news_facExB_tanh_b is an alias for b2news_fac_ExB_tanh_b,
					b2news_facvis_tanh_a is an alias for b2news_fac_vis_tanh_a, and b2news_facvis_tanh_b is an alias for b2news_fac_vis_tanh_b. Additionally, for all core cell rows where iy.le.iy_nocoreExB, fac_ExB(ix,iy) is set to zero. This means that ExB contributions and flows will be zeroed out in those cells.
					For consistency with the boundary condition treatment, the value iy_nocoreExB.eq.-1 is NOT recommended!
				""", '0.0'),
   
      'b2news_fac_ExB_tanh_a' : ('', 'real', """
					Parameters for spatial variation of the diamagnetic, ExB and viscosity drift term multipliers. These are allowed to have tanh profiles centered at tanh_a and of width tanh_b, where both quantities are in metres and measured along the radial coordinate for the cell column ix.eq.fac_ref (default value is jxa, see Geometry section for its computation). The maximum value of facdrift and fac_ExB is controlled by their respective _start and _target switches, see Run section for details.
					For consistency with the naming convention of related variables:
					b2news_facExB_tanh_a is an alias for b2news_fac_ExB_tanh_a,
					b2news_facExB_tanh_b is an alias for b2news_fac_ExB_tanh_b,
					b2news_facvis_tanh_a is an alias for b2news_fac_vis_tanh_a, and b2news_facvis_tanh_b is an alias for b2news_fac_vis_tanh_b. Additionally, for all core cell rows where iy.le.iy_nocoreExB, fac_ExB(ix,iy) is set to zero. This means that ExB contributions and flows will be zeroed out in those cells.
					For consistency with the boundary condition treatment, the value iy_nocoreExB.eq.-1 is NOT recommended!
				""", '0.0'),
   
      'b2news_fac_ExB_tanh_b' : ('', 'real', """
					Parameters for spatial variation of the diamagnetic, ExB and viscosity drift term multipliers. These are allowed to have tanh profiles centered at tanh_a and of width tanh_b, where both quantities are in metres and measured along the radial coordinate for the cell column ix.eq.fac_ref (default value is jxa, see Geometry section for its computation). The maximum value of facdrift and fac_ExB is controlled by their respective _start and _target switches, see Run section for details.
					For consistency with the naming convention of related variables:
					b2news_facExB_tanh_a is an alias for b2news_fac_ExB_tanh_a,
					b2news_facExB_tanh_b is an alias for b2news_fac_ExB_tanh_b,
					b2news_facvis_tanh_a is an alias for b2news_fac_vis_tanh_a, and b2news_facvis_tanh_b is an alias for b2news_fac_vis_tanh_b. Additionally, for all core cell rows where iy.le.iy_nocoreExB, fac_ExB(ix,iy) is set to zero. This means that ExB contributions and flows will be zeroed out in those cells.
					For consistency with the boundary condition treatment, the value iy_nocoreExB.eq.-1 is NOT recommended!
				""", '0.0'),
   
      'b2news_fac_vis_tanh_a' : ('', 'real', """
					Parameters for spatial variation of the diamagnetic, ExB and viscosity drift term multipliers. These are allowed to have tanh profiles centered at tanh_a and of width tanh_b, where both quantities are in metres and measured along the radial coordinate for the cell column ix.eq.fac_ref (default value is jxa, see Geometry section for its computation). The maximum value of facdrift and fac_ExB is controlled by their respective _start and _target switches, see Run section for details.
					For consistency with the naming convention of related variables:
					b2news_facExB_tanh_a is an alias for b2news_fac_ExB_tanh_a,
					b2news_facExB_tanh_b is an alias for b2news_fac_ExB_tanh_b,
					b2news_facvis_tanh_a is an alias for b2news_fac_vis_tanh_a, and b2news_facvis_tanh_b is an alias for b2news_fac_vis_tanh_b. Additionally, for all core cell rows where iy.le.iy_nocoreExB, fac_ExB(ix,iy) is set to zero. This means that ExB contributions and flows will be zeroed out in those cells.
					For consistency with the boundary condition treatment, the value iy_nocoreExB.eq.-1 is NOT recommended!
				""", '0.0'),
   
      'b2news_fac_vis_tanh_b' : ('', 'real', """
					Parameters for spatial variation of the diamagnetic, ExB and viscosity drift term multipliers. These are allowed to have tanh profiles centered at tanh_a and of width tanh_b, where both quantities are in metres and measured along the radial coordinate for the cell column ix.eq.fac_ref (default value is jxa, see Geometry section for its computation). The maximum value of facdrift and fac_ExB is controlled by their respective _start and _target switches, see Run section for details.
					For consistency with the naming convention of related variables:
					b2news_facExB_tanh_a is an alias for b2news_fac_ExB_tanh_a,
					b2news_facExB_tanh_b is an alias for b2news_fac_ExB_tanh_b,
					b2news_facvis_tanh_a is an alias for b2news_fac_vis_tanh_a, and b2news_facvis_tanh_b is an alias for b2news_fac_vis_tanh_b. Additionally, for all core cell rows where iy.le.iy_nocoreExB, fac_ExB(ix,iy) is set to zero. This means that ExB contributions and flows will be zeroed out in those cells.
					For consistency with the boundary condition treatment, the value iy_nocoreExB.eq.-1 is NOT recommended!
				""", '0.0'),
   
      'b2news_iy_nocoreExB' : ('', 'integer', """
					Parameters for spatial variation of the diamagnetic, ExB and viscosity drift term multipliers. These are allowed to have tanh profiles centered at tanh_a and of width tanh_b, where both quantities are in metres and measured along the radial coordinate for the cell column ix.eq.fac_ref (default value is jxa, see Geometry section for its computation). The maximum value of facdrift and fac_ExB is controlled by their respective _start and _target switches, see Run section for details.
					For consistency with the naming convention of related variables:
					b2news_facExB_tanh_a is an alias for b2news_fac_ExB_tanh_a,
					b2news_facExB_tanh_b is an alias for b2news_fac_ExB_tanh_b,
					b2news_facvis_tanh_a is an alias for b2news_fac_vis_tanh_a, and b2news_facvis_tanh_b is an alias for b2news_fac_vis_tanh_b. Additionally, for all core cell rows where iy.le.iy_nocoreExB, fac_ExB(ix,iy) is set to zero. This means that ExB contributions and flows will be zeroed out in those cells.
					For consistency with the boundary condition treatment, the value iy_nocoreExB.eq.-1 is NOT recommended!
				""", '-2'),
   
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
				""", '1.0'),
   
      'b2stbc_type13_norm' : ('', 'real', """
					Additional feedback strength adjustment parameters for BCCON=13 boundary condition, density adjusted to match a specific flux.
					The density is adjusted by a factor of:
					(1.0_R8+CONPAR(IS,IB,2)*(DFS-FS)/ (abs(DFS)+abs(FS)+abs(type13_norm)+abs(NAS*type13_fac)))
					where FS is the current particle flux, DFS is the desired particle flux, and NAS the current volume-averaged density. The desired flux DFS is computed as
					CONPAR(IS,IB,1)+CONPAR(IS,IB,3)
					where the first number is provided directly by the user in b2.boundary.parameters and the second is internally set to correspond to the re-entry of ionised neutrals that have crossed into the core for cases run with Eirene where eirene_ionising_core is activated.
					See also the description of 'eirene_ionising_core'.
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
				""", '1.0'),
   
      'b2news_xfm1' : ('', 'real', """
					Under-relaxation parameters for the parallel momentum, continuity, potential and energy equations respectively.
				""", '1.0'),
   
      'b2news_xfm2' : ('', 'real', """
					Under-relaxation parameters for the parallel momentum, continuity, potential and energy equations respectively.
				""", '1.0'),
   
      'b2news_xfm3' : ('', 'real', """
					Under-relaxation parameters for the parallel momentum, continuity, potential and energy equations respectively.
				""", '1.0'),
   
      'b2npco_pcm0' : ('', 'real', """
					pcm0 specifies an additional under-relaxation factor that is applied to the velocity correction. It is required that 0.le.pcm0.and.0.le.pcm1.
				""", '1.0'),
   
      'b2npco_pcm1' : ('', 'real', """
					pcm0 specifies an additional under-relaxation factor that is applied to the velocity correction. It is required that 0.le.pcm0.and.0.le.pcm1.
				""", '1.0'),
   
      'b2npht_pcm0' : ('', 'real', """
					pcm0 specifies an additional under-relaxation factor that is applied to the temperature correction. 
					It is required that 0.le.pcm0.and.0.le.pcm1.
				""", '1.0'),
   
      'b2npht_pcm1' : ('', 'real', """
					pcm0 specifies an additional under-relaxation factor that is applied to the temperature correction. 
					It is required that 0.le.pcm0.and.0.le.pcm1.
				""", '1.0'),
   
      'b2npht_style' : ('', 'integer', """
					When set to '1', SPb's form of the program b2sihs_ is called. It is recommended '1'.
				""", '1'),
   
      'b2nph9_style' : ('', 'integer', """
					When set to '1', SPb's form of the program b2sihs_ is called. It is recommended '1'.
				""", '1'),
   
      'b2sifr_styl0' : ('', 'integer', """
					Specify the type of linearisation used in the thermal force term.
				""", '0'),
   
      'b2sifr_styl1' : ('', 'integer', """
					Specify the type of linearisation used in the thermal force term.
				""", '0'),
   
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
					Multipliers to the density, parallel momentum, heat, potential, and electron prticle time-derivative source terms, respectively. 
					'phm4' is normally zero since the potential equation contains no source terms.
				""", '1.0'),
   
      'b2srdt_phm1' : ('', 'real', """
					Multipliers to the density, parallel momentum, heat, potential, and electron prticle time-derivative source terms, respectively. 
					'phm4' is normally zero since the potential equation contains no source terms.
				""", '1.0'),
   
      'b2srdt_phm3' : ('', 'real', """
					Multipliers to the density, parallel momentum, heat, potential, and electron prticle time-derivative source terms, respectively. 
					'phm4' is normally zero since the potential equation contains no source terms.
				""", '1.0'),
   
      'b2srdt_phm4' : ('', 'real', """
					Multipliers to the density, parallel momentum, heat, potential, and electron prticle time-derivative source terms, respectively. 
					'phm4' is normally zero since the potential equation contains no source terms.
				""", '0.0'),
   
      'b2srdt_phm5' : ('', 'real', """
					Multipliers to the density, parallel momentum, heat, potential, and electron prticle time-derivative source terms, respectively. 
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
   
      'b2news_potok' : ('Numerics', 'real', """
					Target residual for the potential equation.
				""", '1.0e-2'),
   
      'b2news_ramp_slow' : ('Numerics', 'integer', """
					If ramp_slow.eq.0 (default), the ExB and diamagnetic drifts multipliers are ramped on each call of b2news, otherwise they are only changed on the first call of the nstg loop on the timestep.
				""", '0'),
   
      'eirene_print_minmax' : ('Numerics', 'integer', """
					Print min and max values of te, ti, na &amp; ua
				""", '0'),
   
      'eirene_extrap' : ('Numerics', 'integer', """
					If eirene_extrap.eq.1, then guard cell plasma parameter values are calculated from the neighbouring real cell values. If eirene_extrap.eq.0, the guard cell values are used unchanged.
				""", '1'),
   
      'eirene_ank_mods' : ('Numerics', 'integer', """
					If ank_mods.ne.0, then uses an additional scheme to ensure particle balance as the B2 solution evolves, due to the internal iteration scheme, away from the plasma background on which the Eirene sources were originally computed at the beginning of the time-step. The user is referred to the text in $SOLPSTOP/doc/Source_Scaling_in_B2.pdf for a full description of the method used.
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
					When area_fix.eq.0, recovers old SOLPS5.0 behaviour.
					If area_fix.ge.1, then certain computations of poloidal velocities are done by dividing flows by the area normal to the flux tube as opposed to the area of contact.
					If area_fix.ge.2, then additionally this treatment is used for the parallel contact area used in determining plasma flux limiters.
					If area_fix.ge.3, then additionally this treatment is used for all parallel contact areas.
				""", '3'),
   
      'b2tfhe_vis_per' : ('Numerics', 'integer', """
					If '1.0', the electric potential equation is solved by the subroutine b2npp7 using a 7-point stencil.
					The value '1.0' is recommended for runs with drifts when perpendicular viscosity and corresponding perpendicular viscosity current is taken into account.
				""", '0.0'),
   
      'b2stbc_sheath_drift_fix' : ('Numerics', 'integer', """
					If sheath_drift_fix.eq.0, then the drift velocity used in the sheath boundary conditions is the sum of diamagnetic and ExB contributions (old, but likely wrong, treatment). If sheath_drift_fix.eq.1, then the drift velocity used in the sheath boundary conditions is the ExB velocity only (recommended).
				""", '1'),
   
      'b2stbc_fix_fch_in_fhe_sheath' : ('Numerics', 'integer', """
					If fix_fch_in_fhe_sheath.eq.0, then the wrong (old) implementation of the FCH contribution to FHE used;
					If fix_fch_in_fhe_sheath.eq.1, then the wrong (second) implementation of the FCH contribution to FHE used;
					If fix_fch_in_fhe_sheath.eq.2, then the correct implementation of the FCH contribution to FHE used;
				""", '2'),
   
      'b2stbr_potential_at_guard_cell' : ('Numerics', 'integer', """
					If potential_at_guard_cell.eq.1, the electric potential used for the computation of the incident energy for sputtering yields is taken as the value in the guard cell. If potential_at_guard_cell.eq.0, the value from the neighbouring real cell is used instead.
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
					If '1', Spb's form to calculate parallel and perpendicular neutral heat conductivity flux limit (does not preserve symmetry, kept for backward compatibility reasons).
					If '2', modifies the Spb treatment for the flux limits to be applied on the transport coefficients directly.
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
				""", '1'),
   
      'b2trcl_cvsa_mltpl' : ('Numerics', 'integer', """
					Artificial coefficient providing faster convergence to the neoclassical electric field but giving a distortion of the flows in the SOL as a side-effect. 
					Can be applied &lt;&gt;1 during the convergence and turned off for the final stage of calculations. Use with caution.
				""", '1.0'),
   
      'b2ux5p_mult_nonzero' : ('Numerics', 'integer', """
					Number of expected nonzero matrix elements per matrix row.
				""", '10'),
   
      'b2ux5p_style' : ('Numerics', 'integer', """
					Choose the type of matrix solver. Style.eq.0 = iluter, Style.eq.1 = 5-pt stencil, Style.eq.2 = MA28. 
					NOTE: Only style.eq.2 will give good results. Other values are NOT recommended!
				""", '2'),
   
      'b2ux7p_style' : ('Numerics', 'integer', """
					Choose the type of matrix solver. Style.eq.0 = iluter, Style.eq.1 = 5-pt stencil, Style.eq.2 = MA28copy. Style.eq.3 = SDRV from YSMP 
					NOTE: Only style.eq.3 will give good results. Other values are NOT recommended!
				""", '3'),
   
      'b2ux9p_style' : ('Numerics', 'integer', """
					Choose the type of matrix solver. Style.eq.0 = iluter, Style.eq.1 = 5-pt stencil, Style.eq.2 = MA28copy. 
					NOTE: Only style.eq.2 will give good results. Other values are NOT recommended!
				""", '2'),
   
      'b2ux5p_acpar' : ('Numerics', 'real', """
					Paremeter needed for iluter matrix solver.
				""", '8.0'),
   
      'b2stbc_fchy_dia' : ('Numerics', 'real', """
					Multiplier to the neoclassical current and diamagnetic heat flux convective boundary conditions, also multiplied by facdrift.
					Adds a poloidal variation consistent with neoclassics and diamagnetic contributions to the heat flux boundary conditions.
					Should only be used with the 5.0 model and heat flux boundaries.
					Allows use b2stbc_integral_current if fchy_dia.eq.0, forbids it otherwise.
				""", '0.0'),
   
      'b2stbc_fchy_dia_coreonly' : ('Numerics', 'integer', """
					If fchy_dia_coreonly.eq.1, the neoclassical current and diamagnetic heat flux convective boundary conditions are only applied on the core boundary.
					If fchy_dia_coreonly.eq.0, those are applied to all boundaries, including PFR, North SOL edge and diverted island center boundary.
				""", '1'),
   
      'b2stbc_neoclassical' : ('Numerics', 'real', """
					Real parameter which establishes boundary conditions for radial component of the current for North and South boundaries when these lie on closed flux surfaces.
					If b2stbc_neoclassical is 0 then the radial component of the current is zero.
					If b2stbc_neoclassical is not 0 the radial component of the current is given by the neoclassical value. b2stbc_neoclassical is superseded if facdrift.ne.0.
					This cannot be used in conjunction with b2stbc_integral_current below.
				""", '0.0'),
   
      'b2stbc_cbc' : ('Numerics', 'real', """
					Multiplier to the ExB velocity for sheath boundary conditions in b2stbc_spb and BCMOM=13 case of b2stbc_phys.
				""", '1.0'),
   
      'b2stbc_integral_current' : ('Numerics', 'real', """
					If integral_current.gt.0, corrects current sources so that there be no surface current at the North and South edges of the edge plasma.
					The value of integral_current multiplies the correction term added to the current source.
					This setting is incompatible with the normal use of diamagnetic drift terms (facdrift.gt.0.0 .and. b2stbc_fchy_dia.ne.0.0) or neoclassical boundary conditions (b2stbc_neoclassical.gt.0.0).
				""", '0.0'),
   
      'b2stbr_first_flight_dl' : ('Numerics', 'real', """
					Step length (in meters) for computing the first flight model chords.
				""", '0.001'),
   
      'b2stbr_first_flight_no_of_flights' : ('Numerics', 'integer', """
					Number of chords started from each start point in the first flight model.
				""", '9'),
   
      'b2stbr_first_flight_table_size' : ('Numerics', 'integer', """
					Workspace size given to the first flight table.
				""", '200000'),
   
      'b2stbc_bcpot_16_step' : ('Numerics', 'integer', """
					Frequency (in number of calls to b2stbc_phys) at which the constant value of the potential at the boundaries where BCPOT=16 is applied will be recomputed.
				""", '50'),
   
      'b2mndr_na_min' : ('Numerics', 'real', """
					Minimal density maintained in all cells for all species. 
					It must be true that na_min is smaller than na_new, as well as any of the initial densities provided in b2ai.dat. 
					This switch replaces 'b2mndr_na0eps' from SOLPS5.x.
				""", '1.0e4'),
   
      'b2mndr_na_new' : ('Numerics', 'real', """
					Initial density put in all cells for all new species if not overwritten by initial state file. This switch replaces 'b2mndr_na0eps' from SOLPS5.x.
				""", '1.0e14'),
   
      'b2news_guard_flows' : ('Numerics', 'integer', """
					If guard_flows.eq.0, flows between neighbouring guard cells are blocked.
					If guard_flows.eq.1, flows between neighbouring guard cells are kept.
					If guard_flows.eq.2, particle flows between neighbouring guard cells are blocked for the density equations and the incorrect corner values are replaced by interpolated values. It is recommended 2.
				""", '2'),
   
      'b2stbc_istyle_cur_contr_on_S_and_N' : ('Numerics', 'integer', """
					When set to '2', SPB's form of adding currents on the South core boundary is included by using BCPOT=12, and on the SOuth PFR and North boundaries by using BCPOT=13. It is recommended '2', in conjunction with the BCPOT=12 and BCPOT=13 settings, respectively.
					When set to '1', SPb's form of adding currents on South and North boundaries is done explicitly in addition to other existing boundary conditions for the potential equation.
					The old 5.0 calculation is recovered by using the value '0'.
				""", '2'),
   
      'b2stbc_istyle_fchi' : ('Numerics', 'integer', """
					If '1', explicitly use the expression (bx*cs*na) of particle flux (fna) from boundary condition instead of fna.
				""", '0'),
   
      'b2news_recalculate_contributions' : ('Numerics', 'integer', """
					If recalculate_contributions.eq.0, turns off recomputation of sources when wrong_flow flag is active.
				""", '1'),
   
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
					If 0, b2news is called (SOLPS5.0/1) If 1, b2news_ is called (SOLPS5.2)
				""", '1'),
   
      'b2mndt_ntim_step_out' : ('Numerics', 'integer', """
					When set to a value of 'K', residuals at each K-th step will be written in b2ftrace. It helps to avoid a huge b2ftrace files during long time run.
				""", '1'),
   
      'b2tlh0_hcimx_flag' : ('Numerics', 'integer', """
					When set to -1, only the gradient to the left/bottom is used to compute the conductive neutral flux limits.
					When set to 0, only the gradient to the left/bottom is used to compute the conductive neutral flux limits, except when these do not exist (the other face value is used).
				""", '1'),
   
      'b2trno_flux_limit_to_dpa' : ('Numerics', 'integer', """
					If '1', flux limit to neutrals contribution to dpa0 - the diffusion coefficient is applied in b2tlc0.F. It is recommended '1'.
					b2tlc0.F has the flux limit parameters alpha and gamma which are given by 'b2tlc0_alpha' and 'b2tlc0_gamma'. 'b2tfnb_alpha' and 'b2tlc0_alpha' cannot be different from zero simultaneously.
					'b2tfnb_alpha' gives another form of flux limit which is applied to the whole particle flux.
				""", '1'),
   
      'b2mndt_use_b2srst' : ('Numerics', 'integer', """
					Switches off the stabilization of the source coefficients.
				""", '1'),
   
      'b2mndt_rxf' : ('Numerics', 'real', """
					Main under-relaxation parameter.
				""", '0.5'),
   
      'b2npco_rxg' : ('Numerics', 'real', """
					rxg specifies a special under-relaxation parameter. A term of the form "abs(residual)/rxg" is added to the diagonal of the matrix of the correction equation, with the effect of limiting the computed correction. rxg is dimensionless and of order unity; smaller values of rxg imply stronger damping.
				""", '1.0'),
   
      'b2npht_rxg' : ('Numerics', 'real', """
					rxg specifies a special under-relaxation parameter. A term of the form "abs(residual)/rxg" is added to the diagonal of the matrix of the correction equation, with the effect of limiting the computed correction. rxg is dimensionless and of order unity; smaller values of rxg imply stronger damping.
				""", '1.0'),
   
      'b2npp7_style' : ('Numerics', 'integer', """
					When set to '1', SPb's form of the program b2usp7_ is called. It is recommended '1'.
				""", '1'),
   
      'b2npmo_rxg' : ('Numerics', 'real', """
					Normalisation factor for the parallel momentum equation.
				""", '1.0e6'),
   
      'b2news_poteq' : ('Numerics', 'integer', """
					If poteq.eq.0, the potential equation is jumped over and not solved.
					If poteq.eq.2, the potential is set to 3.1*Te/qe as per SOLPS4.0.
					If poteq.eq.1, the potential equation is solved according to the no_solve switch settings.
					If poteq.ne.1, then 'b2tfhe_no_current'must be set to '1'.
				""", '1'),
   
      'b2nxdv_style' : ('Numerics', 'integer', """
					When set to '1', the total friction force cancel is not calculated at the guard boundary cells. 
					It is recommended '1'.
				""", '1'),
   
      'b2nxfc_style' : ('Numerics', 'integer', """
					style specifies the precise form of interpolation used in the computation of flcb and cvcb. When set to '1', SPb's form of the transport terms in the momentum correction equation is used. 
					It is recommended '1'.
				""", '1'),
   
      'b2nxfx_style' : ('Numerics', 'integer', """
					When set to '1', SPb's form of an expression that occurs in the electron-atom thermal force is used. 
					It is recommended '1'.
				""", '1'),
   
      'b2sigp_style' : ('Numerics', 'integer', """
					When set to '1', SPb's form of the pressure gradient term on the right hand of the momentum balance equation is used. 
					It is recommended '1'.
				""", '1'),
   
      'b2xzdd_zero_dead_and_core' : ('Numerics', 'integer', """
					If 1 then zero passed sources in dead regions, 
					If 2 zero passed sources in dead regions and core boundary cells 
					If 0 then SKIP
				""", '1'),
   
      'b2sihs_style' : ('Numerics', 'integer', """
					style determines the form of the strange electron-atom energy transfer term.
				""", '0'),
   
      'b2stcx_rg0' : ('Numerics', 'real', """
					(rg0 for numerical stabilisation; needs experiments.)
				""", '1.0'),
   
      'b2stcx_styl0' : ('Numerics', 'integer', """
					Specifies the type of linearisation used in the charge exchange momentum source term.
				""", '0'),
   
      'eirene_mc_linearisation' : ('Numerics', 'integer', """
					Specifies the type of linearisation used in the sources derived from the Monte-Carlo neutrals. If linearisation.eq.0, all sources are fed to the constant term, if linearisation.eq.1, positive terms go in the constant term, and negative terms in the proportional term. 'eirene_mc_linearization' is an alias for this switch.
				""", '1'),
   
      'b2stbm_linearisation' : ('Numerics', 'real', """
					Same as above, but applied to the sources coming for an externally coupled code providing plasma sources, for instance a kinetic treatment of trace impurity ions. 'b2stbm_linearization' is an alias for this switch.
				""", '1.0'),
   
      'b2stbm_impgyro_mod' : ('Numerics', 'integer', """
					Specifies the frequency (in units of full b2 timesteps) at which an externally coupled code providing additional source (for instance a kinetic treatment of trace impurity ions such as IMPGYRO) should be called.
				""", '0'),
   
      'b2stel_styl0' : ('Numerics', 'integer', """
					Specifies the type of linearisation used in the charge exchange momentum source term.
				""", '0'),
   
      'b2tfcc_xfac' : ('Numerics', 'real', """
					Multiplier to the pressure force term.
				""", '1.0'),
   
      'b2tfhe_mdf' : ('Numerics', 'integer', """
					If '1', Spb's new form of calculating electron heat flux is used. It is recommended '1' for runs with drifts.
				""", '0'),
   
      'b2tfhe_no_current' : ('Numerics', 'integer', """
					If no_current.eq.1, all currents are set to zero. The setting no_current.eq.1 must be used if the potential equation is not explicitly solved for, i.e. for b2news_poteq.ne.1.
				""", '0'),
   
      'b2tfhi_mdf' : ('Numerics', 'integer', """
					If '1', Spb's new form of calculating ion heat flux is used. 
					It is recommended '1' for runs with drifts.
				""", '0'),
   
      'b2tfnb_drift_style' : ('Numerics', 'integer', """
					When set to '0', drift velocities are calculated in cell centers. When set to '1', drift velocities are calculated in cell faces.
					 It is recommended '1'.
				""", '1'),
   
      'b2tfnb_fnb_nodrift_style' : ('Numerics', 'integer', """
					When set to '1', SPb's form of calculating no drift part of the particle fluxes is used. 
					It is recommended '1'.
				""", '1'),
   
      'b2tfnb_mdf' : ('Numerics', 'integer', """
					If '1', Spb's new form of calculating particle flux is used. 
					It is recommended '1' for runs with drifts.
				""", '0'),
   
      'b2tfnb_xfrhie' : ('Numerics', 'real', """
					Multiplier to the Rhie and Chow upwind correction.
				""", '1.0'),
   
      'b2upht_stylec' : ('Numerics', 'integer', """
					(stylec is a numerical switch, needs experiments)
				""", '0'),
   
      'b2usmo_cfc0' : ('Numerics', 'real', """
					Linearisation constant.
				""", '1.0'),
   
      'b2srsm_enable' : ('Numerics', 'integer', """
					If enable.ne.0, then the sources for particle, parallel momentum, electron and ion heat are rescaled, for non-boundary cells, if the local timestep exceeds the physics timescale implied by those sources.
				""", '0'),
   
      'b2ardr_rtnt' : ('', 'integer', """
					The number of intervals in the discretisation of the density (rtnn) and temperature (rtnt) ranges for the atomic physics tables.
				""", '40'),
   
      'b2ardr_rtnn' : ('', 'integer', """
					The number of intervals in the discretisation of the density (rtnn) and temperature (rtnt) ranges for the atomic physics tables.
				""", '16'),
   
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
					*** Use with caution! ***
				""", '0'),
   
      'b2ardr_no_smoothing' : ('Atomic Physics', 'integer', """
					When set to 1, disables the tail smoothing for of rate coefficients to represent the effect of a power-law tail on the distribution function. It has been added for compatibility with SOLPS4.3
				""", '0'),
   
      'b2ardr_fix_recomb' : ('Atomic Physics', 'integer', """
					When changed from 0, and if the ADAS option is in use, then uses the PRB file to add the contribution arising from is--&gt;is-1 processes.
					This term includes the Bremsstrahlung.
					The default option ('0') only contains the Bremsstrahlung for the is--&gt;is-1 process.
					This option should be used with the 'b2stel_fix_recomb_energy' option b2mn.dat set to '1'. See 'Physics' section.
					*** Use with caution! ***
				""", '0'),
   
      'label' : ('', 'string', """
					Specifies, on the next line, a label for the run.
				""", ''),
   
      'b2cmpa' : ('', '', """
					Specifies a block of basic parameters, overriding those specified in the block of the same name in b2ah.dat
				""", ''),
   
      'b2cmpb' : ('', '', """
					Specifies a block of boundary conditions, overriding those specified in the block of the same name in b2ah.dat
				""", ''),
   
      'b2cmpt' : ('', '', """
					specifies a block of transport coefficients, overriding those specified in the block of the same name in b2ah.dat
				""", ''),
   
      },
   
   'b2.parameters' : {
      
      'NSTRAI' : ('b2.neutrals.parameters', 'integer', """
					Number of neutral sources, or 'strata'. Must not be larger than DEF_NSTRA from $(SOLPSTOP)/include(.local)/DIMENSIONS.F file. 
					Need not include the time-dependent stratum. If a time-dependent stratum is used, is incremented internally as needed. The incremented value is referred to as NSTRAT below.
				""", '0'),
   
      'RCPOS' : ('b2.neutrals.parameters', 'integer array of length (NSTRAT)', """
					Position in the B2 grid of the of strata. Similar use as BCPOS from /BOUNDARY/ namelist.
				""", '-2'),
   
      'RCSTART' : ('b2.neutrals.parameters', 'integer array of length (NSTRAT)', """
					Start coordinate on the B2 grid the strata. Similar use as BCSTART from /BOUNDARY/ namelist.
				""", '-2'),
   
      'RCEND' : ('b2.neutrals.parameters', 'integer array of length (NSTRAT)', """
					End coordinate on the B2 grid of the strata. Similar use as BCEND from /BOUNDARY/ namelist.
				""", '-2'),
   
      'RC_LIST_SIZE' : ('b2.neutrals.parameters', 'integer array of length (NSTRAT)', """
					Contains the size of the recycling boundary lists. Similar use as BC_LIST_SIZE from /BOUNDARY/ namelist.
				""", '0'),
   
      'RC_LIST_X' : ('b2.neutrals.parameters', 'integer array of length (2*(NXD+NYD),NSTRAT)', """
					Contains the X-coordinate of the cells where recycling boundaries are applied. Similar use as BC_LIST_X from /BOUNDARY/ namelist.
				""", '-2'),
   
      'RC_LIST_Y' : ('b2.neutrals.parameters', 'integer array of length (2*(NXD+NYD),NSTRAT)', """
					Contains the Y-coordinate of the cells where recycling boundaries are applied. Similar use as BC_LIST_Y from /BOUNDARY/ namelist.
				""", '-2'),
   
      'TARGSP' : ('b2.neutrals.parameters', 'integer array of size (NSTRAT,NTRACK)', """
					Identifies the base material(s) of this stratum wall. The number corresponds to the B2 species index produced by sputtering. Check b2cdci for details. If the bulk species is not sputtered, should contain -1.
				""", 'b2stbr_sput_dst'),
   
      'CHEMSP' : ('b2.neutrals.parameters', 'logical array of length NSTRAT', """
					Indicates whether chemical sputtering is allowed from this wall stratum.
				""", '.false.'),
   
      'RECYC' : ('b2.neutrals.parameters', 'real*8 array of size (0:NS-1,NSTRAT)', """
					Stores the particle recycling coefficients of species (is) on stratum (istra). Defaults to 1.0 for non-carbon species and 0.0 for carbon species. Particles recycle into the neutral species associated to their homonuclear sequence. 
					Applies to B2 neutral fluid species.
					Also multiplies Eirene recycling fluxes if 'eirene_use_recyceir' is set to 0 (see b2cdci for details).
				""", ''),
   
      'MRECYC' : ('b2.neutrals.parameters', 'real*8 array of size (0:NS-1,NSTRAT)', """
					Stores the parallel momentum recycling coefficients of species (is) on stratum (istra). The parallel momentum is carried back by the recycled neutrals. Applies only to B2 neutral fluid species.
				""", '0.0'),
   
      'ERECYC' : ('b2.neutrals.parameters', 'real*8 array of size (0:NS-1,NSTRAT)', """
					Stores the energy recycling coefficients of species (is) on stratum (istra). Defaults to 0.3 for non-carbon species and 0.0 for carbon species. The energy is carried back by the recycled neutrals.
					Applies only to B2 neutral fluid species.
				""", ''),
   
      'RCION' : ('b2.neutrals.parameters', 'real*8 array of size (0:NS-1,NSTRAT)', """
					Stores the particle-into-ion recycling coefficients of species (is) on stratum (istra). Particles recycle into the next ionised species associated to their homonuclear sequence. Applies only to B2 neutral fluid species.
				""", '0.0'),
   
      'RECYCEIR' : ('b2.neutrals.parameters', 'real*8 array of size (NSTRAT)', """
					Multiplier to the Eirene recycling fluxes from stratum (istra). Only used if 'eirene_use_recyceir' is set to 1 (default).
				""", '1.0'),
   
      'USERFLUXPARM' : ('b2.neutrals.parameters', 'real*8 array of size (NSTRAT,2)', """
					The element (istra,1) contains the strength of constant gas puff strata (type 'C') for Eirene in particles/second.
				""", '0'),
   
      'CRCSTRA' : ('b2.neutrals.parameters', 'character*1 array of length (NSTRAT)', """
					Contains the type of stratum for Eirene. Possible options include:
					'N','S','W','E' - topological mesh boundaries (same use as BCCHAR in /BOUNDARY/ namelist)
					'V' - volume recombination source (related RCPOS, RCSTART, RCEND and RC_LIST variables are ignored).
					'C' - constant or feedback gas puff source (related RCPOS, RCSTART, RCEND and RC_LIST variables are ignored). Gas puffs for B2 fluid neutrals are handled via b2.boundary.parameters. Unless specified otherwise by use of 'eirene_nesepm_istra', it is the first 'C' stratum that is used for feedback puff schemes. See b2cdci for details.
					'T' - time-dependent source for Eirene (related RCPOS, RCSTART, RCEND and RC_LIST variables are ignored). Long-lived Eirene neutrals are stored in this stratum. See EIRENE_STEP_DT below.
				""", ' '),
   
      'RF_NEUT' : ('b2.neutrals.parameters', 'real*8 array of size (4)', """
					Relaxation parameters multiplying the Eirene particle, parallel momentum, electron energy and ion energy sources respectively before use in B2.
				""", '1.0'),
   
      'PHYS_SPUT' : ('b2.neutrals.parameters', 'real*8 array of size (0:NS-1,NSTRAT)', """
					Stores the physical sputtering multiplier for B2 species (is) sputtering on the wall of stratum (istra). Must be non-zero for physical sputtering to occur. Only applies if using B2 fluid neutral model.
				""", '0.0'),
   
      'CHEM_SPUT' : ('b2.neutrals.parameters', 'real*8 array of size (0:NS-1,NSTRAT)', """
					Stores the chemical sputtering multiplier for B2 species (is) sputtering on the wall of stratum (istra). Must be non-zero for chemical sputtering to occur. Only applies if using B2 fluid neutral model.
				""", '0.0'),
   
      'EIRENE_STEP_CPU' : ('b2.neutrals.parameters', 'real*8', """
					Length of CPU time devoted to Eirene calls after the first one (in s). Defaults to the value given in input.dat.
				""", ''),
   
      'EIRENE_STEP_DT' : ('b2.neutrals.parameters', 'real*8', """
					Physical time (in s) the Eirene particles are to be followed before being passed to the time-dependent stratum.
				""", '1.0e-3'),
   
      'EIRENE_MOD' : ('b2.neutrals.parameters', 'integer', """
					Frequency of Eirene calls. Eirene is called every EIRENE_MOD full B2 iterations.
				""", '1'),
   
      'VOLRECSTART' : ('b2.neutrals.parameters', 'real*8 array of size (NSTRAT)', """
					Initial volume recombination rate from stratum (istra) to be used for the volume recombination scaling regulation algorithm. Rendered obsolete by 'eirene_dpc_fix'.
				""", '1.e21'),
   
      'VOLRECINC' : ('b2.neutrals.parameters', 'real*8', """
					Maximum rate of increase of the volume recombination source strength. The volume recombination regulation scaling scheme is activated if VOLRECINC is neither 0 nor 1.
					Rendered obsolete by 'eirene_dpc_fix'.
				""", ''),
   
      'VOLRECWT' : ('b2.neutrals.parameters', 'real*8', """
					Weight of new volume recombination strength relative to that of previous iteration in the volume recombination regulation scaling scheme.
					Rendered obsolete by 'eirene_dpc_fix'.
				""", '0.1'),
   
      'SPECIES_START' : ('b2.neutrals.parameters', 'integer array of size (NSTRAT)', """
					Specifies the index of the first B2 species involved in stratum (istra).
				""", '0'),
   
      'SPECIES_END' : ('b2.neutrals.parameters', 'integer array of size (NSTRAT)', """
					Specifies the index of the last B2 species involved in stratum (istra).
				""", 'ns-1'),
   
      'NEUTRALS_FILENAME' : ('b2.neutrals.parameters', 'character*256', """
					Name of the next file to use for reading a new /NEUTRALS/ namelist.
				""", 'b2.neutrals.parameters'),
   
      'NEUTRALS_TIME_MOD' : ('b2.neutrals.parameters', 'real*8', """
					When the B2 run simulation time, in seconds,*     				modulo(NEUTRALS_TIME_MOD), exceeds NEUTRALS_TIME_SWITCH, reads the new namelist from NEUTRALS_FILENAME. Also switches to the new namelist if the ELM count (here time/NEUTRALS_TIME_MOD) changes. Only active if NEUTRALS_TIME_MOD is greater than 0.
				""", '0.0'),
   
      'NEUTRALS_TIME_SWITCH' : ('b2.neutrals.parameters', 'real*8', """
					Time (in seconds) within an ELM cycle after which a new NEUTRALS namelist is read.
				""", '0.0'),
   
      'L_NEUTRAD' : ('b2.neutrals.parameters', 'integer', """
					If l_neutrad &gt;= 0, then the radiated power due to the neutrals atoms is taken directly from the Eirene calculation, instead of being recomputed by B2.
				""", '0'),
   
      'L_NEUTFLUX' : ('b2.neutrals.parameters', 'integer', """
					If l_neutflux &gt;=0, then correct treatment of the incident fluxes in B2 and b2plot; if &lt;0, then old (approximate) treatment
				""", ''),
   
      'LSTRASCL' : ('b2.neutrals.parameters', 'integer array of size (NSTRAT,0:natm)', """
					Indicates with which Eirene atomic species to scale the Eirene stratum (istra) (0 means no scaling, default). Atomic species 0 stands for electrons.
				""", ''),
   
      'B2ESPCR' : ('b2.neutrals.parameters', 'integer array of size (0:NS-1)', """
					Contains the index of the Eirene atomic species corresponding to the B2 species (is).
				""", 'ordering of the B2 isonuclear sequences'),
   
      'EB2SPCR' : ('b2.neutrals.parameters', 'integer array of size (NATM)', """
					Contains the index of the B2 neutral fluid species corresponding to the Eirene atomic species (iatm).
				""", 'first B2 species of each isonuclear sequence'),
   
      'LMOLSCL' : ('b2.neutrals.parameters', 'integer array of size (NMOL)', """
					Contains the index of the Eirene atomic species with which the Eirene molecular species (IMOL) should be scaled.
				""", '0'),
   
      'MLCMP' : ('b2.neutrals.parameters', 'integer array of size (NATM,NMOL)', """
					Contains the number of atoms from Eirene atomic species IATM within each molecule of Eirene molecular species IMOL.
				""", '0'),
   
      'LIONSCL' : ('b2.neutrals.parameters', 'integer array of size (NION)', """
					Contains the index of the Eirene atomic species with which the Eirene test ion species (IION) should be scaled.
				""", '0'),
   
      'LCNS' : ('b2.neutrals.parameters', 'integer array of size (NSTS)', """
					Contains the indices of Eirene non-standard surfaces (block 3A in input.dat) corresponding to core boundaries.
				""", '0'),
   
      'LTNS' : ('b2.neutrals.parameters', 'integer array of size (NSTS)', """
					Contains the indices of Eirene non-standard surfaces (block 3A in input.dat) corresponding to target boundaries.
				""", '0'),
   
      'LSNS' : ('b2.neutrals.parameters', 'integer array of size (NSTRAT)', """
					Contains the indices of Eirene surfaces related to the recycling sources.
				""", '0'),
   
      'KSNS' : ('b2.neutrals.parameters', 'integer array of size (NSTRAT)', """
					Contains the number of parts for each Eirene recycling stratum.
				""", '0'),
   
      'GPFC' : ('b2.neutrals.parameters', 'real*8 array of size (NATM,NSTRAT)', """
					Specifies the fraction of Eirene atomic species (iatm) in one particle puffed from stratum (istra).
				""", '0.0'),
   
      'DBG_EIR_MC' : ('b2.neutrals.parameters', 'integer', """
					Debug output control for eirene_mc routine. See code for usage.
				""", '0'),
   
      'DEBUG_FLAGS' : ('b2.neutrals.parameters', 'integer array of size (100)', """
					Non-zero elements yield additional print-out data for debugging B2-Eirene coupling. See code for specific uses. Many slots still available for user-specific needs.
				""", '0'),
   
      'NEUT_SCL_LIM' : ('b2.neutrals.parameters', 'real*8', """
					Maximum number by which Eirene neutral sources may be scaled in either direction within the ank-mods scheme. See explaining text in $SOLPSTOP/doc/Source_Scaling_in_B2.pdf for details.
				""", '2.0'),
   
      'TRACK_INDEX' : ('b2.neutrals.parameters', 'integer array of size (0:NS-1)', """
					Specifies the mixed material species index related to B2 species (is).
				""", '1 for species spud_dst, 0 for other'),
   
      'TRACK_CHEM_SPUT' : ('b2.neutrals.parameters', 'logical array of size (NTRACK)', """
					Indicates whether mixed material species (itrack) participates in chemical sputtering. Defaults to .true. for first tracked species if sput_dst is carbon, and to .false. for all other cases.
				""", ''),
   
      'CHEMICAL_EROSION_REDEP_FAC' : ('b2.neutrals.parameters', 'real*8', """
					Multiplier to the chemical sputtering coefficient of carbon for computing the rate used for redeposited carbon.
				""", '1.0'),
   
      'CHEMICAL_EROSION_BE_FAC' : ('b2.neutrals.parameters', 'logical', """
					Indicates whether the presence of beryllium is to impact on the chemical sputtering yield of carbon.
				""", '.false.'),
   
      'CHEMICAL_EROSION_BE_FAC_A' : ('b2.neutrals.parameters', 'real*8', """
					The chemical sputtering yield of carbon is multiplied by
					(1.0-C/2*(tanh((frac-A)/B)-tanh((-A)/B)))
					where frac is the fractional content of Be in the surface layer material.
				""", '0.2'),
   
      'CHEMICAL_EROSION_BE_FAC_B' : ('b2.neutrals.parameters', 'real*8', """
					See above.
				""", '0.05'),
   
      'CHEMICAL_EROSION_BE_FAC_C' : ('b2.neutrals.parameters', 'real*8', """
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
   
      'SPS_ABSR' : ('b2.neutrals.parameters', 'real*8 array of length (N_SPCSRF)', """
					Particle absorption on the surface. If positive, will supercede the setting from the Eirene input file: RECYCT = 1-SPS_ABSR. Ignored if negative.
				""", '-1.0'),
   
      'SPS_TRNO' : ('b2.neutrals.parameters', 'real*8 array of length (N_SPCSRF)', """
					Surface transparency in positive direction. If positive, will supercede the setting from the Eirene input file: TRANSP(1,) = SPS_TRNO. Ignored if negative.
				""", '-1.0'),
   
      'SPS_TRNI' : ('b2.neutrals.parameters', 'real*8 array of length (N_SPCSRF)', """
					Surface transparency in negative direction. If positive, will supercede the setting from the Eirene input file: TRANSP(2,) = SPS_TRNI. If negative, the setting from SPS_TRNO is used.
				""", '-1.0'),
   
      'SPS_MTRI' : ('b2.neutrals.parameters', 'real*8 array of length (N_SPCSRF)', """
					Surface material in Eirene notation (e.g., 1206 for C). If positive, will supercede the setting from the Eirene input file: ZNML = SPS_MTRI. Ignored if negative.
				""", '0'),
   
      'SPS_MTRL' : ('b2.neutrals.parameters', 'character*8 array of length (N_SPCSRF)', """
					Surface material in human notation (e.g., 'C').
				""", ''),
   
      'SPS_TMPR' : ('b2.neutrals.parameters', 'real*8 array of length (N_SPCSRF)', """
					Surface temperature (in eV). If set larger to 1.e10, will be ignored. Otherwise, will supercede the setting from the Eirene input file: EWALL = SPS_TMPR.
				""", '1.e15'),
   
      'SPS_SPPH' : ('b2.neutrals.parameters', 'real*8 array of length (N_SPCSRF)', """
					Fudge factor for physical sputtering. If positive, will supercede the setting from the Eirene input file: RECYCS = SPS_SPPH. Ignored if negative.
				""", '-1.0'),
   
      'SPS_SPCH' : ('b2.neutrals.parameters', 'real*8 array of length (N_SPCSRF)', """
					Fudge factor for chemical sputtering. If positive, will supercede the setting from the Eirene input file: RECYCC = SPS_SPCH. Ignored if negative.
				""", '-1.0'),
   
      'SPS_SGRP' : ('b2.neutrals.parameters', 'integer array of length (N_SPCSRF)', """
					Sputtered particle species flag for chemical sputtering. If positive, will supercede the setting from the Eirene input file: ISRC = SPS_SGRP. Ignored if negative.
				""", '-1'),
   
      'WRITE_NML_NEUT' : ('b2.neutrals.parameters', 'logical', """
					If .true. (default), writes the content of the namelist to stdout after it has been read.
				""", '.true.'),
   
      'TIME_DEP_PUFF' : ('b2.neutrals.parameters', 'logical array of length (NSTRAT)', """
					Indicates whether a stratum is a time-dependent gas puff. Should only be .true. for strata defined as gas puffs.
				""", '.false. for all strata'),
   
      'NGPDATA' : ('b2.neutrals.parameters', 'integer data of size (NSTRAT)', """
					Number of points over which the time profile of the strength of gas puff (istra) is given. Defaults to 0. Current maximum value is 100.
				""", '0'),
   
      'GPDATA' : ('b2.neutrals.parameters', 'real*8 data of size (NGPDATA,2,NSTRAT)', """
					For (i,ik,istra) in (1:NGPDATA(istra),1:2,1:NSTRAT),
					GPDATA(i,1,istra) contains the time point (i) for stratum (istra) (in s).
					GPDATA(i,2,istra) contains the gas puff strength of stratum (istra) at time point (i) (in particles/s).
					The gas puff strength before the first time point is given by USERFLUXPARM(1,istra).
					The gas puff strength after the last time point is given by the GPDATA value of the last time point.
					Otherwise, the gas puff strength is linearly interpolated from the given data.
				""", '0.0'),
   
      'CHEMICAL_SPUTTER_YIELD' : ('b2.neutrals.parameters', 'real*8 array of size (0:NLIM+NSTS)', """
					Passed to Eirene. Chemical sputter yield of wall surface (ilim).
				""", '0.0'),
   
      'FCHAR_CHEMICAL' : ('b2.neutrals.parameters', 'real*8', """
					Nuclear charge of atomic species causing the sputtering. Default means no chemical sputtering.
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
					Contains the filename from which to extract the surface material properties for wall element (iwall). The files are to be found in $(SOLPSTOP)/data(.local)/Surface_properties/.
				""", 'C'),
   
      'COATING_MATERIAL_NAME' : ('b2.wall_save.parameters', 'character*6 of size (NWALL)', """
					Contains the filename from which to extract the bulk material properties of the eventual coating for wall element (iwall).
				""", ' '),
   
      'BULK_MATERIAL_NAME' : ('b2.wall_save.parameters', 'character*6 of size (NWALL)', """
					Contains the filename from which to extract the bulk material properties for wall element (iwall). The files are to be found in $(SOLPSTOP)/data(.local)/Bulk_properties/.
				""", 'C'),
   
      'LAYER_ALLOYS' : ('b2.wall_save.parameters', 'character*6 of size (NALLOYS)', """
					Contains the filename from which to extract the material properties for alloy (nalloy) which may be present in mixed materials deposited layers. Not yet operational. The files are to be found in $(SOLPSTOP)/data(.local)/Bulk_properties/ and $(SOLPSTOP)/data(.local)/Surface_properties/.
				""", ''),
   
      'TARGET_TEMP' : ('b2.wall_save.parameters', 'real*8 array of size (NWALL,NDEPTH)', """
					Contains the temperature (in Kelvin) of wall element (iwall) at depth layer (idepth).
					If plate_option.eq.1, will be set to backplate_temp(iwall).
					If plate_option.eq.2 and empty, will be set to equilibrium 1-D profile deduced from plasma incoming fluxes.
					If plate-option.eq.3, must be set.
				""", ''),
   
      'INERTIAL_COOLING' : ('b2.wall_save.parameters', 'logical array of size (NWALL)', """
					Indicates whether wall element (iwall) is inertially cooled instead of actively cooled.
				""", '.false.'),
   
      'BACKPLATE_TEMP' : ('b2.wall_save.parameters', 'real*8 array of size (NWALL)', """
					Contains the temperature (in Kelvin) maintained by cooling at the back end of wall element (iwall).
				""", 'b2stbr_plate_temp'),
   
      'PLATE_THICKNESS' : ('b2.wall_save.parameters', 'real*8 array of size (NWALL)', """
					Contains the thickness (in meters) of wall element (iwall).
				""", 'b2stbr_plate_thick'),
   
      'COATING_THICKNESS' : ('b2.wall_save.parameters', 'real*8 array of size (NWALL)', """
					Contains the thickness (in meters) of the eventual coating on wall element (iwall).
				""", '0'),
   
      'PLATE_TIME_FACTOR' : ('b2.wall_save.parameters', 'real*8 array of size (NWALL)', """
					Multiplier to the time for the equations for temperature and composition evolution of wall element (iwall).
				""", '1.0'),
   
      'DEPOSITION' : ('b2.wall_save.parameters', 'real*8 array of size (NWALL, NTRACK)', """
					Contains the amount of deposited material (in atoms) from species (itrack) onto wall element (iwall).
				""", '0.0'),
   
      'EROSION' : ('b2.wall_save.parameters', 'real*8 array of size(NWALL, NTRACK)', """
					Contains the amount of eroded material (in atoms) of species (itrack) from wall element(iwall).
				""", '0.0'),
   
      'CHEMICAL_SPUTTERING' : ('b2.wall_save.parameters', 'real*8 array of size (NWALL,0:NS-1)', """
					Contains the chemical sputter yield of 'sput_dst' or 'sput_dst_bulk' species on wall element (iwall) caused by B2 species (is).
				""", '0.0'),
   
      'PHYSICAL_SPUTTERING' : ('b2.wall_save.parameters', 'real*8 array of size (NWALL,0:NS-1)', """
					Contains the physical sputter yield of 'sput_dst' or 'sput_dst_bulk' species on wall element (iwall) caused by B2 species (is).
				""", '0.0'),
   
      'PHYSICAL_SPUTTERING_ENERGY' : ('b2.wall_save.parameters', 'real*8 array of size (NWALL,0:NS-1)', """
					Contains the fraction of returned energy carried by sputtered particles of species 'sput_dst' or 'sput_dst_bulk' species from wall element (iwall) caused by B2 species (is).
				""", '0.0'),
   
      'RES_SPUTTERING' : ('b2.wall_save.parameters', 'real*8 array of size (NWALL,0:NS-1)', """
					Contains the RES sputter yield of 'sput_dst' or 'sput_dst_bulk' species on wall element (iwall) caused by B2 species (is).
				""", '0.0'),
   
      'THERMAL_EVAPORATION' : ('b2.wall_save.parameters', 'real*8 array of size(NWALL,0:NS-1)', """
					Contains the rate of thermal evaporation of species (is) (in particles/second) from wall element (iwall).
				""", '0.0'),
   
      'BACKSCATTERING' : ('b2.wall_save.parameters', 'real*8 array of size (NWALL,0:NS-1)', """
					Contains the backscattering fraction for incoming B2 species (is) onto wall element (iwall).
				""", '0.0'),
   
      'BACKSCATTERING_ENERGY' : ('b2.wall_save.parameters', 'real*8 array of size (NWALL,0:NS-1)', """
					Contains the backscattered energy fraction for incoming B2 species (is) onto wall element (iwall).
				""", '0.0'),
   
      'PLATE_TIME' : ('b2.wall_save.parameters', 'real*8 array of size (NWALL)', """
					Indicates how much simulation time has elapsed for wall element (iwall) (in seconds).
				""", '0.0'),
   
      'PLATE_AREA' : ('b2.wall_save.parameters', 'real*8 array of size (NWALL)', """
					Indicates the wall area (in square meters) for wall element (iwall). Defaults to the area computed from the B2 grid information.
				""", ''),
   
      'MONOLAYER_DEPOSITION' : ('b2.wall_save.parameters', 'real*8 array of size (NWALL,NTRACK)', """
					Contains the amount of deposited material (in monolayers) from species (itrack) onto wall element (iwall).
				""", '0.0'),
   
      'MONOLAYER_EROSION' : ('b2.wall_save.parameters', 'real*8 array of size (NWALL,NTRACK)', """
					Contains the amount of eroded material (in monolayers) of species (itrack) from wall element (iwall).
				""", '0.0'),
   
      'LAYER_NCONSTITUENTS' : ('b2.wall_save.parameters', 'integer array of size (NWALL)', """
					Indicates the number of elemental constituents within the surface layer of wall element (NWALL).
				""", '1'),
   
      'LAYER_NZCONSTITUENTS' : ('b2.wall_save.parameters', 'integer array of size (NWALL,6+NTRACK)', """
					Contains the atomic numbers Z of the various elements present within the surface layer of wall element (iwall). Defaults to 6 for the first value, 0 otherwise.
				""", ''),
   
      'LAYER_NRELCONSTITUENTS' : ('b2.wall_save.parameters', 'real*8 array of size (NWALL,6+NTRACK)', """
					Contains the relative atomic abundances of the various elements present within the surface layer of wall element (iwall). Defaults to 1.0 for the first value, 0.0 otherwise.
				""", ''),
   
      'EXP' : ('b2md.dat', 'character*128', """
					Name of the experiment being modelled.
				""", 'NOT_SET'),
   
      'SHOT' : ('b2md.dat', 'integer', """
					Shot number identifying the run. Defaults to the last number found in shotnumber.history, or 0 if the file is not found.
				""", ''),
   
      'TIME' : ('b2md.dat', 'real*8', """
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
   
      'NBC' : ('b2.boundary.parameters', 'integer', """Number of boundary segments.""", '0'),
   
      'BCCHAR' : ('b2.boundary.parameters', 'character*1 array of length (NBC)', """
					Specifies the nature of the boundary segment
					N = 'North' boundary
					S = 'South' boundary
					W = 'West' boundary
					E = 'East' boundary
					X = 'X' boundary used for specifying a fixed value on a row of cells
					Y = 'Y' boundary used for specifying a fixed value on a column of cells
				""", ' '),
   
      'CONPAR' : ('b2.boundary.parameters', 'real*8 array of size (0:NS-1,NBC,3)', """
					Contains parameters helping to define the boundary conditions for the continuity equation of species (is). See description of BCCON below for details.
				""", '0.0'),
   
      'MOMPAR' : ('b2.boundary.parameters', 'real*8 array of size (0:NS-1,NBC,2)', """
					Contains parameters helping to define the boundary conditions for the parallel momentum equation of species (is). See description of BCMOM below for details.
				""", '0.0'),
   
      'ENEPAR' : ('b2.boundary.parameters', 'real*8 array of size (NBC,2)', """
					Contains parameters helping to define the boundary conditions for the electron energy equation. See description of BCENE below for details.
				""", '0.0'),
   
      'ENIPAR' : ('b2.boundary.parameters', 'real*8 array of size (NBC,2)', """
					Contains parameters helping to define the boundary conditions for the ion energy equation. See description of BCENI below for details.
				""", '0.0'),
   
      'POTPAR' : ('b2.boundary.parameters', 'real*8 array of size (NBC,2)', """
					Contains parameters helping to define the boundary conditions for the potential equation. See description of BCPOT below for details.
				""", '0.0'),
   
      'BCPOS' : ('b2.boundary.parameters', 'integer array, length (NBC)', """
					For North, South or X boundary conditions, it specifies the row index; for West, East and Y boundary conditions, it specifies the column index.
				""", '-2'),
   
      'BCSTART' : ('b2.boundary.parameters', 'integer array, length (NBC)', """
					For North, South or X boundary conditions, it specifies the start column index; for West, East and Y boundary conditions, it specifies the start row index.
				""", '-2'),
   
      'BCEND' : ('b2.boundary.parameters', 'integer array, length (NBC)', """
					For North, South X boundary conditions, it specifies the end column index; for West, East and Y boundary conditions, it specifies the end row index.
				""", '-2'),
   
      'BC_LIST_SIZE' : ('b2.boundary.parameters', 'integer array of length (NBC)', """
					Contains the size of the list of cells where a boundary condition is applied.
				""", '0'),
   
      'BC_LIST_X' : ('b2.boundary.parameters', 'integer array of length (2*(NXD+NYD),NBC)', """
					Contains the X-coordinate of the cells where boundaries conditions are applied.
				""", '-2'),
   
      'BC_LIST_Y' : ('b2.boundary.parameters', 'integer array of length (2*(NXD+NYD),NBC)', """
					Contains the Y-coordinate of the cells where boundaries conditions are applied.
				""", '-2'),
   
      'BCCON' : ('b2.boundary.parameters', 'integer array, length (0:NS-1,NBC)', """
					Specifying the type of density boundary condition for each segment and species (fastest varying index is species); makes use of CONPAR to specify additional information, as indicated:
					0 : default, no boundary condition is applied
					1 : prescribe the value of the density, CONPAR(,,1) specifies the required density in m<sup>-3</sup>
					2 : prescribe the gradient of the density, CONPAR(,,1) specifies the required density gradient in m<sup>-4</sup>
					3 : sheath conditions, CONPAR(,,1) not used (zero gradient is used)
					4 : prescribe the value of the density, weakly a mixed boundary condition, CONPAR(,,1) specifies the required density in m<sup>-3</sup> and CONPAR(,,2) specifies the 'strength' of the boundary condition
					5 : prescribe the particle flux per unit area, CONPAR(,,1) specifies the required particle flux density in m<sup>-2</sup> s<sup>-1</sup>
					6 : prescribe the total particle flux for a constant density, CONPAR(,,1) specifies the particle flux in s<sup>-1</sup>
					7 : prescribe the density as a function of other plasma parameters [not yet available]
					8 : prescribe the total particle flux with constant flux density, CONPAR(,,1) specifies the particle flux in s<sup>-1</sup>
					9 : prescribe the decay length for the density, CONPAR(,,1) specifies the gradient length in $m$ (should use type 15 instead when drifts are turned on)	
					10 : leakage option for density, recommended for cases with drifts, CONPAR(,,1) specifies the leakage factor, alpha in Gamma_loss = alpha C<sub>s</sub> n<sub>a</sub>
					11 : particle flux feedback boundary condition, CONPAR(,,1) not used, derived from CBSNA(0,IS,IREG). The species used must be declared using the 'b2stbc_isfeedback' switch.
					12 : particle density feedback boundary condition, as above, CONPAR(,,1) not used, derived from CBSNA(0,IS,IREG). The species used must be declared using the 'b2stbc_isfeedback' switch.
					13 : particle density to achieve specified total flux, 
					CONPAR(,,1) is the specified flux crossing the flux surface 'b2stbc_type13_ref' steps away from the boundary,
					CONPAR(,,2) is the strength of the feedback,
					CONPAR(,,3)) when running with Eirene and the 'ionising core' switch is used, 
					CONPAR(,,2) is set internally to match the re-entering flux of ionised neutrals that crossed the core boundary (when running with Eirene and the 'ionising_core' option).
					The feedback scheme can be further tweaked with the switches 'b2stbc_type13_norm' and 'b2stbc_type13_fac'. See code for details.
					14 : sound speed velocity flux, CONPAR(,,1) is a multiplier to the outgoing sound speed C<sub>s</sub>.
					15 : prescribe a radial leakage velocity, CONPAR(,,1) specifies the leakage velocity in units of the local thermal velocity.
					16 : particle density to achieve specified total flux, used with ASTRA coupling. The total desired flux is summed over all BCCON=16 core boundaries. CONPAR(,,1) specifies the desired particle flux in s<sup>-1</sup> .
					18 : prescribe total main ion particle flux, used with ASTRA coupling.
					19 : particle flux feedback boundary condition, flux is summed over neutrals and ions, for coupling with ASTRA. The total desired flux is summed over all BCCON=19 core boundaries. This boundary condition type is applied to ions in their highest ionisation stage. CONPAR(,,1) specifies the desired particle flux in s<sup>-1</sup> .
					20 : constant density feedback condition, CONPAR(,,1) specifies the desired density in m<sup>-3</sup> .
					21 : prescribe the value of the density and add a density perturbation to get a solution which is as close as possible to neoclassical theory. It is recommended to use this boundary condition together with corresponding condition on ion temperature (BCENI=24). The total desired density is summed over all BCCON=21 core boundaries. CONPAR(,,1) specifies the desired density in m<sup>-3</sup>.
					22 : Feedback boundary condition: given total particle flux with constant average density. The poloidal density variation is added to make the solution as close as possible to the neoclassical value derived for pure H/D/T plasma. It is recommended to use this boundary condition with corresponding boundary condition on ion temperature (BCENI=23,24). The total desired flux is summed over all BCCON=22 core boundaries. CONPAR(,,1) specifies the desired particle flux in s<sup>-1</sup> .
					23 : Feedback boundary condition: given sum of integrated neutrals and main ion particle fluxes with constant average density. The poloidal density variation is added to make the solution as close as possible to the neoclassical value derived for pure H/D/T plasma. It is recommended to use this boundary condition with corresponding boundary condition on ion temperature (BCENI=23,24). The total desired flux is summed over all BCCON=23 core boundaries. CONPAR(,,1) specifies the desired particle flux in s<sup>-1</sup> .
					24 : constant density feedback scaled by density on the ring 'bc_type21_ref' away. CONPAR(,,1) specifies the desired density in m<sup>-3</sup> . CONPAR(,,2) is the strength of the feedback
					25 : Feedback boundary condition: prescribe the average value of the density and add a density perturbation from neighbouring radial cell. This boundary condition is suitable for any species of a multi-species plasma (i.e. in the case when the condition used in BCCON=21 fails). It is recommended to use this boundary condition together with the corresponding condition on ion temperature (BCENI=26,27). CONPAR(,,1) specifies the desired average density in m<sup>-3</sup> .
					26 : Feedback boundary condition: prescribe the total ion flux and find the average density. A density perturbation is taken from the neighbouring radial cell. This boundary condition is suitable for any species of a multi-species plasma (i.e. in the case when the condition used in BCCON=22 fails). It is recommended to use this boundary condition together with a corresponding condition on the ion temperature (BCENI=26,27). The total desired flux is summed over all BCCON=26 core boundaries. CONPAR(,,1) specifies the desired particle flux in s<sup>-1</sup> .
					27 : Feedback boundary condition: prescribe the particle flux sum for all neutrals and ions belonging to a given isonuclear sequence and find the average density of the highest ionization stage. A density perturbation is taken from the neighbouring radial cell. It is recommended to use this boundary condition together with corresponding condition on ion temperature (BCENI=25,26). The total desired flux is summed over all BCCON=27 core boundaries. CONPAR(,,1) specifies the desired particle flux in s<sup>-1</sup> .
				""", ''),
   
      'BCMOM' : ('b2.boundary.parameters', 'integer array, length NS * NBC', """
					Specifying the type of parallel momentum or velocity boundary condition for each segment and species (fastest varying index is species); makes use of MOMPAR to specify additional information, as indicated
					0 : default, no boundary condition is applied
					1 : prescribe the value of the parallel velocity, MOMPAR(,,1) specifies the parallel velocity in m.s<sup>-1</sup>
					2 : prescribe the gradient of the parallel velocity, MOMPAR(,,1) specifies the parallel velocity gradient in s<sup>-1</sup>
					3 : sheath conditions, mach number as input, 
					if MOMPAR(,,2) &lt; 0.5 , then the velocity is set to exactly 
					MOMPAR(,,1) * C<sub>s,collective</sub>, otherwise the velocity is set to be at least MOMPAR(,,1) * C<sub>s,collective</sub>, species
					4 : prescribe the value of the velocity, weakly a mixed boundary condition, MOMPAR(,,1) specifies the parallel velocity in m.s<sup>-1</sup> and MOMPAR(,,2) specifies the 'strength' of the boundary condition
					5 : prescribe the parallel momentum flux per unit area, MOMPAR(,,1) specifies the parallel momentum flux density in N.m<sup>-2</sup>
					6 : prescribe the total parallel momentum flux for a constant parallel velocity [not yet available]
					7 : prescribe the parallel momentum as a function of other plasma parameters [not yet available]
					8 : special : limited shear, imposes zero gradient for the Mach number. [[[Eventually intended to have MOMPAR(,,1) specify the gradient of the Mach number in m<sup>-1</sup> ]]]
					9 : prescribe the total parallel momentum flux with constant flux density, MOMPAR(,,1) specifies the parallel momentum flux in N
					10 : prescribe the decay length for the parallel momentum, MOMPAR(,,1) specifies the decay length in m
					11 : Rozhansky viscosity condition for the parallel momentum, MOMPAR(,,1) is not used
					12 : Condition from b2stbc_spb for the parallel momentum
					13 : sheath boundary condition from b2stbc_spb for the parallel momentum
					14 : Condition from b2stbc_spb for the parallel momentum
					15 : Prescribe the value of the parallel velocity, scaled with B_average/B_local
					16 : Prescribe the average value of the parallel velocity MOMPAR(,,1) specifies the parallel velocity in m.s -1
				""", ''),
   
      'BCENE' : ('b2.boundary.parameters', 'integer array, length NBC', """
					Specifying the type of electron energy or temperature boundary condition for each segment; makes use of ENEPAR to specify additional information, as indicated
					0 : default, no boundary condition is applied
					1 : prescribe the value of the electron temperature, ENEPAR(,1) specifies the temperature in eV
					2 : prescribe the gradient of the electron temperature, ENEPAR(,1) specifies the temperature gradient in eV.m -1
					3 : sheath conditions, electron energy transmission, ENEPAR(,1) specifies an additional contribution to the energy transmission coefficient in addition to that of the potential difference [the sound speed used depends on settings of MOMPAR(,ISMAIN,2)]
					4 : prescribe the value of the electron temperature, weakly a mixed boundary condition, ENEPAR(,1) specifies the temperature in eV and ENEPAR(,2) specifies the 'strength' of the boundary condition
					5 : prescribe the electron energy flux per unit area, ENEPAR(,1) specifies the energy flux density in W.m-2
					6 : prescribe the total electron energy flux for a constant electron temperature, ENEPAR(,1) specifies the energy flux in W (no longer supported, use types [16] or [17] instead)
					7 : prescribe the electron temperature as a function of other plasma parameters [not yet available]
					8 : prescribe the total electron heat flux with constant flux density, ENEPAR(,1) specifies the energy flux in W
					9 : prescribe the decay length for the electron temperature, ENEPAR(,1) specifies the decay length in m (can also use type [19] instead)
					10 : feedback option for core, ENEPAR(,1) not used, derived from CBSHE(0,coreregno)
					11 : not used
					12 : sheath conditions, electron energy transmission coefficient, ENEPAR(,1) specifies an energy transmission factor, delta_e in Q_e = delta_e Gamma_e T_e
					13 : prescribe the electron energy flux per unit area proportional to temperature, ENEPAR(,1) specifies the energy flux density per temperature in W m<sup>-2</sup> J<sup>-1</sup> (the temperature here in J)
					14 : leakage option for electron energy, ENEPAR(,1) specifies the leakage factor, alpha in Gamma_loss = alpha C<sub>s</sub> n<sub>e</sub>
					15 : not used
					16 : Feedback boundary condition with constant temperature, ENEPAR(,1) specifies the power flux in W across the flux surface with index 'b2stbc_type16_ref' (default=-1), ENEPAR(,2) should be something like 0.1 and specifies the strength of the feedback. Also see type [17] below. Available if bcene_16_style=0 (default). If bcene_16_style=1, integrated electron heat flux with constant electron temperature, summed over all core boundaries with BCENE=16.
					17 : Feedback boundary condition with constant shared temperature for both electrons and ions, with ENEPAR(,1) + ENIPAR(,1) giving the total power flux in W across the flux surface with index 'b2stbc_type16_ref' (default=-1), ENEPAR(,2) should be something like 0.1 and specifies the strength of the feedback. Replaces [16] for high densities and large values of 'b2stbc_type16_ref'.
					18 : Fractional drop condition. Not yet working.
					19 : same as [9] but to be used when simultaneously setting BCCON=1 on the same boundary.
					20 : Feedback boundary condition with constant temperature, as per type [16] but with 'type20_' switches and a different feedback scheme.
					21 : constant temperature feedback scaled by temperature on the ring bc_type21_ref away 
					ENEPAR(,1) specifies the desired electron temperature in eV. 
					ENEPAR(,2) is the strength of the feedback
					22 : radial leakage condition for the electron temperature. ENEPAR(,1) specifies the leakage velocity in units of the electron thermal velocity. A temperature gradient such that the diffusive flux is set to match this leakage is imposed.
				""", ''),
   
      'BCENI' : ('b2.boundary.parameters', 'integer array, length NBC', """
					Specifying the type of ion energy or temperature boundary condition for each segment; makes use of ENIPAR to specify additional information, as indicated
					0 : default, no boundary condition is applied
					1 : prescribe the value of the ion temperature, ENIPAR(,1) specifies the temperature in eV
					2 : prescribe the gradient of the ion temperature, ENIPAR(,1) specifies the temperature gradient in eV.m<sup>-1</sup>
					3 : sheath conditions, ion energy transmission, ENIPAR(,1) specifies the contribution to the energy transmission coefficient [the sound speed used depends on settings of MOMPAR(,ISMAIN,2)]
					4 : prescribe the value of the ion temperature, weakly a mixed boundary condition, ENIPAR(,1) specifies the temperature in eV and ENIPAR(,2) specifies the 'strength' of the boundary condition
					5 : prescribe the ion energy flux per unit area, ENIPAR(,1) specifies the energy flux density in W.m<sup>-2</sup>
					6 : prescribe the total ion energy flux for a constant ion temperature, ENIPAR(,1) specifies the energy flux in W (no longer supported, use types [16] or [17] instead)
					7 : prescribe the ion temperature as a function of other plasma parameters [not yet available]
					8 : prescribe the total ion heat flux with constant flux density, ENIPAR(,1) specifies the energy flux in W
					9 : prescribe the decay length for the ion temperature, ENIPAR(,1) specifies the decay length in m (can also use type [19] instead)
					10 : feedback option for core, ENIPAR(,1) not used, derived from cbshi(0,ISMAIN,coreregno)
					11 : sheath conditions, ion energy transmission coefficient, ENIPAR(,1) specifies an energy transmission factor, delta<sub>i</sub> in Q<sub>i</sub> = delta<sub>i</sub> T<sub>i</sub> sum<sub>a</sub> n<sub>a</sub> C<sub>s,a</sub>
					12 : sheath conditions, ion energy transmission coefficient, ENIPAR(,1) specifies an energy transmission factor, delta<sub>i</sub> in Q<sub>i</sub> = delta<sub>i</sub> T<sub>i</sub> sum<sub>a</sub> Gamma<sub>a</sub>
					13 : prescribe the ion energy flux per unit area proportional to temperature, ENIPAR(,1) specifies the energy flux density per temperature in W.m -2 .J -1 (the temperature here in J)
					14 : leakage option for ion energy, ENIPAR(,1) specifies the leakage factor, alpha in Gamma<sub>loss</sub> = alpha C<sub>s</sub>T<sub>i</sub>
					15 : from b2stbc_spb
					16 : Feedback boundary condition with constant temperature, ENIPAR(,1) specifies the power flux in W across the flux surface with index 'b2stbc_type16_ref' (default=-1), ENIPAR(,2) should be something like 0.1 and specifies the strength of the feedback. Also see type [17] below. Available if bceni_16_style=0 (default). If bceni_16_style=1, integrated ion heat flux with constant ion temperature, summed over all core boundaries with BCENI=16.
					ENIPAR(,1) specifies the power flux in W
					17 : Feedback boundary condition with constant shared temperature for both electrons and ions, see BCENE=17 above for description.
					18 : Fractional drop condition. Not yet working.
					19 : same as [9] but to be used when simultaneously setting BCCON=1 on the same boundary.
					20 : Feedback boundary condition with constant temperature, as per type [16] but with 'type20_' switches and a different feedback scheme.
					21 : from b2stbc_spb
					22 : Radial leakage condition for the ion temperature. ENIPAR(,1) specifies the leakage velocity in units of the collective ion thermal velocity. A temperature gradient such that the diffusive flux is set to match this leakage is imposed.
					23 : Prescribe the poloidally averaged value of the ion temperature and introduce a poloidal variation as close as possible to neoclassical solution. It is recommended to use this boundary condition together with corresponding condition on ion density (BCCON=21,22,23). The average is taken over all core boundaries with BCENI=23. ENIPAR(,1) specifies the temperature in eV
					24 : Feedback boundary condition with prescribed total ion flux, constant poloidally averaged ion temperature	and a poloidal variation as close as possible to neoclassical solution. It is recommended to use this boundary condition together with corresponding condition on ion density (BCCON=21,22,23). The flux is	summed over all core boundaries with BCENI=24. ENIPAR(,1) specifies the energy flux in W
					25 : Constant temperature feedback scaled by temperature on the ring bc_type21_ref away. ENIPAR(,1) specifies the desired ion temperature in eV . ENIPAR(,2) is the strength of the feedback
					26 : Prescribe the poloidally averaged value of the ion temperature and introduce a poloidal variation in a simplified manner. This boundary condition is suitable for any plasma composition (i.e. when BCENI=23 fails). It is recommended to use this boundary condition together with corresponding condition on ion density (BCCON = 25,26,27). The average is taken over all core boundaries with BCENI=26. ENIPAR(,1) specifies the temperature in eV
					27 : Feedback boundary condition with prescribed total ion heat flux, constant poloidally averaged ion temperature and a poloidal variation in a simplified manner. This boundary condition is suitable for any plasma composition (i.e. when BCENI=24 fails). It is recommended to use this boundary condition together with corresponding condition on ion density (BCCON = 25,26,27). The flux is summed over all core boundaries with BCENI=27. ENIPAR(,1) specifies the energy flux in W
				""", ''),
   
      'BCPOT' : ('b2.boundary.parameters', 'integer array, length NBC', """
					Specifying the type of electric potential or current boundary condition for each segment; makes use of POTPAR to specify additional information, as indicated
					0 : default, no boundary condition is applied
					1 : prescribe the value of the potential, POTPAR(,1) specifies the potential in V
					2 : prescribe the gradient of the potential, POTPAR(,1) specifies the potential gradient in V.m<sup>-1</sup>
					3 : sheath conditions, 
					POTPAR(,2) used for biasing [see code for details]
					4 : prescribe the value of the potential weakly a mixed boundary condition, POTPAR(,1) specifies the potential in V and POTPAR(,2) specifies the 'strength' of the boundary condition
					5 : prescribe the current flux density per unit area, POTPAR(,1) specifies the electric current flux density in A.m<sup>-2</sup>
					6 : prescribe the total current flux density for a constant potential [not yet available]
					7 : prescribe the potential as a function of other plasma parameters [not yet available]
					8 : prescribe the total electric current with constant flux density, POTPAR(,1) specifies the electric current in A
					9 : prescribe the decay length for the potential, POTPAR(,1) specifies the decay length in m
					10 : feedback option for core [not yet tested!!!!!!!!!] (based on using cbsch(0,coreregno))
					11 : sheath conditions, electron energy transmission from b2stbc_spb, POTPAR(,2) specifies the bias potential in V
					12 : Imposes the currents due to drifts for the South core boundary. Must be used in conjunction with istyle_cur_contr_on_S_and_N.eq.2
					13 : Imposes the currents due to drifts for the South private flux and North boundaries. Must be used in conjunction with istyle_cur_contr_on_S_and_N.eq.2
					16 : Constant electric potential feedback on imposed total current. The current prescribed is given by the sum of the POTPAR(IB,1) (in A) over all the BCPOT=16 boundaries. 
					Still experimental, will not work for drift cases.
					21 : constant potential feedback scaled by potential on the ring 'bc_type21_ref' away.
					POTPAR(,,1) specifies the desired potential in V.
					POTPAR(,,2) is the strength of the feedback
				""", ''),
   
      'GAMMAI' : ('b2.boundary.parameters', 'real*8', """
					Ratio of specific heats (adiabatic coefficient).
				""", '5/3'),
   
      'GAMMAE' : ('b2.boundary.parameters', 'real*8', """
					Secondary electron emission coefficient.
				""", '0.5'),
   
      'LBNDUSR' : ('b2.boundary.parameters', 'logical', """
					If .true. will also call Bas' boundary condition routine after the end of the physics boundary condition routine (governed by the data from b2ah.dat and b2mn.dat).
				""", '.false.'),
   
      'LFEEDBACK' : ('b2.boundary.parameters', 'logical', """
					Indicates whether a feedback scheme is used. Obsolete. Superceded by 'b2stbc_feedback'.
				""", '.false.'),
   
      'NNISO' : ('b2.boundary.parameters', 'integer', """
					Number of dead (or isolated) regions.
				""", '0'),
   
      'NIISO' : ('b2.boundary.parameters', 'real*8 array of size (0:NS-1)', """
					Density of species (is) in (m-3) to impose in isolated regions.
				""", ''),
   
      'TEISO' : ('b2.boundary.parameters', 'real*8', """
					Electron temperature (in eV) to impose in isolated regions.
				""", '1.0'),
   
      'TIISO' : ('b2.boundary.parameters', 'real*8', """
					Ion temperature (in eV) to impose in isolated regions.
				""", '1.0'),
   
      'PHIISO' : ('b2.boundary.parameters', 'real*8', """
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
   
      'BOUNDARY_TIME_MOD' : ('b2.boundary.parameters', 'real*8', """
					When the B2 run simulation time, in seconds, modulo(BOUNDARY_TIME_MOD), exceeds BOUNDARY_TIME_SWITCH, reads the new namelist from BOUNDARY_FILENAME. Also switches to the new namelist as the ELM count (here time/BOUNDARY_TIME_MOD) changes.
					Only active if BOUNDARY_TIME_MOD is greater than 0.
				""", '0.0'),
   
      'BOUNDARY_TIME_SWITCH' : ('b2.boundary.parameters', 'real*8', """
					Time (in seconds) within an ELM cycle after which a new /BOUNDARY/ namelist is read.
				""", '0.0'),
   
      'LCBS' : ('b2.boundary.parameters', 'integer array of size (NBC)', """
					Indices of the core boundary segments in B2 for passing to EIRENE. Defaults to the list of 'S' boundaries in regions 1 and 5.
				""", ''),
   
      'WRITE_NML_BND' : ('b2.boundary.parameters', 'logical', """
					If .true. (default), writes the content of the namelist to stdout after it has been read.
				""", '.true.'),
   
      'SAVED_CBSHE_CORE' : ('b2.feedback_save.parameters', 'real*8', """
					Last value used for the core electron energy radial flux feedback.
				""", '0.0'),
   
      'SAVED_CBSHI_CORE' : ('b2.feedback_save.parameters', 'real*8', """
					Last value used for the core ion energy radial flux feedback.
				""", '0.0'),
   
      'SAVED_CBSNA_CORE' : ('b2.feedback_save.parameters', 'real*8', """
					Last value used for the core particle radial flux feedback. Corresponds to 'isfeedback' B2 species.
				""", '0.0'),
   
      'SAVED_CBSCH_CORE' : ('b2.feedback_save.parameters', 'real*8', """
					Last value used for the core radial electric current feedback.
				""", '0.0'),
   
      'SAVED_CBSNA_PFR1' : ('b2.feedback_save.parameters', 'real*8', """
					Last value used for the radial inner PFR boundary flux feedback. Corresponds to 'isfeedback' B2 species.
				""", '0.0'),
   
      'SAVED_CBSNA_PFR2' : ('b2.feedback_save.parameters', 'real*8', """
					Last value used for the radial outer PFR boundary flux feedback. Corresponds to 'isfeedback' B2 species.
				""", '0.0'),
   
      'SAVED_CBSNA_SOL' : ('b2.feedback_save.parameters', 'real*8', """
					Last value used for the radial particle flux feedback in the SOL. Corresponds to 'isfeedback' B2 species.
				""", '0.0'),
   
      'VACUUM_COMMUNICATION' : ('b2.feedback_control.parameters', 'Integer', """
					If &gt; 0, allows for a
					communication of particle fluxes across vacuum regions. This option only applies to neutrals. The density boundary condition is based on the difference between the average pressure and the local pressure.
				""", '0'),
   
      'VACUUM_COMMUNICATION_NREG' : ('b2.feedback_control.parameters', 'Integer array of size (NVAC)', """
					Number of communicating vacuum regions.
				""", '0'),
   
      'VACUUM_COMMUNICATION_METHOD' : ('b2.feedback_control.parameters', 'Integer array of size (NVAC)', """
					Option for resorbing the pressure difference.
						1: Try to set a flux. Corr = (beta*ave_pressure - pressure)/temp * alpha
						2: Try to set a density based on pressure equality.
					Corr = alpha * beta * pressure / Ti
				""", '0'),
   
      'VACUUM_COMMUNICATION_IY' : ('b2.feedback_control.parameters', 'Integer array of size (NVACREG,NVAC)', """
					Radial index of the ring on which the neutral pressure is computed for region IREG.
				""", '-2'),
   
      'VACUUM_COMMUNICATION_IX1' : ('b2.feedback_control.parameters', 'Integer array of size (NVACREG,NVAC)', """
					Poloidal lower bound of the range over which the neutral pressure is computed for region IREG.
				""", '-2'),
   
      'VACUUM_COMMUNICATION_IX2' : ('b2.feedback_control.parameters', 'Integer array of size (NVACREG,NVAC)', """
					Poloidal upper bound of the range over which the neutral pressure is computed for region IREG.
				""", '-2'),
   
      'VACUUM_COMMUNICATION_ALPHA' : ('b2.feedback_control.parameters', 'Real*8 array of size (0:NSPECIES-1,NVAC)', """
					Parameter for setting the pressure correction. See above.
				""", '0.0'),
   
      'VACUUM_COMMINICATION_BETA' : ('b2.feedback_control.parameters', 'Real*8 array of size (0:NSPECIES-1,NVAC)', """
					Parameter for setting the pressure correction. See above.
				""", '1.0'),
   
      'NA_FEEDBACK_TARGET' : ('b2.feedback_control.parameters', 'Real*8 array of size (0:NSPECIES-1)', """
					Sets the target density of species (ISPECIES) for the feedback scheme.
				""", '0.0'),
   
      'NA_FEEDBACK_TIME' : ('b2.feedback_control.parameters', 'Real*8 array of size (0:NSPECIES-1)', """
					Sets the time of reference (in s) for the feedback of species (ISPECIES).
				""", '0.0'),
   
      'NA_FEEDBACK_CHOICE' : ('b2.feedback_control.parameters', 'Integer array of size (0:NSPECIES-1)', """
					Choice of quantity on which the feedback is computed:
						0: no action
						1: local species density (averaged over the rectangle of cells[IX1:IX2,IY1:IY2]). Summed over all charge states of that species.
						2: local electron density (averaged over the rectangle of cells[IX1:IX2,IY1:IY2]).
						3: outer midplane separatrix electron density.
						4: total particle content for that species.
						5: total ion content for that species (not including neutrals).
						6: neutral particle flux through the core boundary.
						7: relative average concentration of this species at the separatrix.
				""", '0'),
   
      'NA_FEEDBACK_OPTION' : ('b2.feedback_control.parameters', 'Integer array of size (0:NSPECIES-1)', """
					Option for computing the new fedback quantity.
						0: no action
						1: rescale slowed by na_feedback_alpha
						2: pure rescale
						3: rescaling slowed by tanh_log
						4: rescale done according to SOLPS4 formula 
							The target waveform for the particle content is 
							 N = C + V*(time-T) 
						   and the current puffing rate S is adjusted 
						   S --&gt; max(0, min(X,S + D)), where D = F*((N - &lt;N&gt;)/dt + (&lt;N&gt;_prev - &lt;N&gt;)/dt_prev)
						5: rescale done according to SOLPS4 formula: N = C*exp((time-T)*V)
						6: rescale slowed by na_feedback_alpha (SOLPS4 style)
				""", '0'),
   
      'NA_FEEDBACK_ACTUATOR' : ('b2.feedback_control.parameters', 'Integer array of size (0:NSPECIES-1)', """
					Choice for the actuator used for the feedback.
					0: no action
					1: gas puff via boundary condition
					2: rescale na
					3: core boundary flux condition
				""", '0'),
   
      'NA_FEEDBACK_ALPHA' : ('b2.feedback_control.parameters', 'Real*8 array of size (0:NSPECIES-1)', """
					Factor by which the rescaling is slowed. Rescaling factor is :
					Option 1: (1 + alpha*target/current) / (1 + alpha)
					Option 3: 2**(tanh(log(x)/beta)*log(alpha)/log(2))
					Options 4 and 5: Corresponds to parameter F
				""", '0.001'),
   
      'NA_FEEDBACK_BETA' : ('b2.feedback_control.parameters', 'Real*8 array of size (0:NSPECIES-1)', """
					Factor by which the rescaling is slowed. See above. Options 4 and 5: Corresponds to parameter V (ffb_rtvn)
				""", '1.0'),
   
      'NA_FEEDBACK_CONST' : ('b2.feedback_control.parameters', 'Real*8 array of size (0:NSPECIES-1)', """
					Options 4 and 5: Corresponds to parameter C. If negative, C is
						computed as the initial total particle content of the sequence.
				""", '0.0'),
   
      'NA_FEEDBACK_IX1' : ('b2.feedback_control.parameters', 'Integer array of size (0:NSPECIES-1)', """
					Lower poloidal bound for the region of which the density is being averaged.
				""", '-2'),
   
      'NA_FEEDBACK_IX2' : ('b2.feedback_control.parameters', 'Integer array of size (0:NSPECIES-1)', """
					Upper poloidal bound for the region of which the density is being averaged.
				""", '-2'),
   
      'NA_FEEDBACK_IY1' : ('b2.feedback_control.parameters', 'Integer array of size (0:NSPECIES-1)', """
					Lower radial bound for the region of which the density is being averaged.
				""", '-2'),
   
      'NA_FEEDBACK_IY2' : ('b2.feedback_control.parameters', 'Integer array of size (0:NSPECIES-1)', """
					Upper poloidal bound for the region of which the density is being averaged.
				""", '-2'),
   
      'NA_FEEDBACK_IB' : ('b2.feedback_control.parameters', 'Integer array of size (0:NSPECIES-1)', """
					Index of boundary condition through which the feedback is being applied.
				""", '-1'),
   
      'NA_FEEDBACK_PUFF_MIN' : ('b2.feedback_control.parameters', 'Real*8 array of size (0:NSPECIES-1)', """
					Minimum gas puff being applied.
				""", '0.0'),
   
      'NA_FEEDBACK_PUFF_MAX' : ('b2.feedback_control.parameters', 'Real*8 array of size (0:NSPECIES-1)', """
					Maximum gas puff being applied.
				""", '0.0'),
   
      'NA_FEEDBACK_OVERSHOOT' : ('b2.feedback_control.parameters', 'Real*8 array of size (0:NSPECIES-1)', """
					If the density is larger than target*overshoot, the gas puff is turned off.
				""", '0.0'),
   
      'NSDATA' : ('b2.sources.profile', 'integer array of size (NKIND_DATA,NKIND_SOURCE,0:NS)', """
					Number of points over which the source profile of (kind_data,kind_source,is) is defined. Should not exceed NY+2.
						If KIND_DATA=1, the data is expressed as a profile in physical distance from the separatrix (in metres) along the outer midplane.
						The user can change this default reference location by use of the 'set_transport_i[xy]ref' switches.
						If KIND_DATA=2, the data is expressed as a profile in flux distance from the separatrix (not yet available).
				""", '0'),
   
      'SDATA' : ('b2.sources.profile', 'real*8 data of size (2,NY+2,NKIND_SOURCE,0:NS)', """
					For (i,ir,ik,is) in (1:2,1:NY+2,1:NKIND_SOURCE,0:NS),
					SDATA(1,ir,:,:) contains the radial location of the profile point (ir).
					SDATA(2,ir,:,:) contains the source profile value at point (ir).
					KIND_SOURCE=1 means particle source of species (is) (in particles/m3)
					KIND_SOURCE=2 means parallel momentum source for species (is) (in kg.m/s/m3)
					KIND_SOURCE=3 means electron heat source (in Watts/m3)
					KIND_SOURCE=4 means ion heat source (in Watts/m3)
					KIND_SOURCE=5 means electric charge source (in Coulombs/m3)
					KIND_SOURCE=6 means non-ambipolar electron particle source (in e/m3)
				""", '0.0'),
   
      'NXDATA' : ('b2.sources.profile', 'integer array of size (NKIND_DATA,NKIND_SOURCE,0:NS)', """
					Number of points over which the axial profile of (kind_data,kind_source,is) is defined. Should not exceed NX+2. Defaults to 0.
					If KIND_DATA=1, the data is expressed as a profile in physical distance, here connection length, rescaled from 0.0 to 1.0.
					For closed field lines, the reference location for the zero of distance is set by use of the 'set_transport_i[xy]ref' switches.
					If KIND_DATA=2, the data is expressed as a profile in (ix) cell index, again normalized from 0.0 to 1.0 to match the [0:nx-1] interval.
				""", ''),
   
      'XDATA' : ('b2.sources.profile', 'real*8 data of size (2,NY+2,NKIND_SOURCE,0:NS)', """
					Multiplier to the poloidal source profile in the axial direction. Same convention for KIND_SOURCE as above.
				""", '1.0'),
   
      'DIVHEAT' : ('b2.sources.profile', 'real*8', """
					Additional divertor ion heat source (in Watts/m3)
				""", '0.0'),
   
      'SOURCES_FILENAME' : ('b2.sources.profile', 'character*256', """
					Name of the next file to use for reading a new /PROFILE/ namelist. Quantities not present in the new file will be inherited from the old one.
				""", 'b2.sources.profile'),
   
      'SOURCES_TIME_MOD' : ('b2.sources.profile', 'real*8', """
					When the B2 run simulation time, in seconds, modulo(SOURCES_TIME_MOD),exceeds SOURCES_TIME_SWITCH, reads the new namelist from SOURCES_FILENAME. Also switches to the new namelist if the ELM count (here time/SOURCES_TIME_MOD) changes. Only active if SOURCES_TIME_MOD is greater than 0.
				""", '0.0'),
   
      'SOURCES_TIME_SWITCH' : ('b2.sources.profile', 'real*8', """
					Time (in seconds) within an ELM cycle after which a new /PROFILE/ namelist is read.
				""", '0.0'),
   
      'NDATA' : ('b2.transport.inputfile', 'integer array of size (NKIND_DATA,NCOEF,0:NS)', """
					Number of points over which the source profile of (kind_data,kind_coef,is) is defined. Should not exceed NY+2.
					If KIND_DATA=1, the data is expressed as a profiles in physical distance from the separatrix (in metres).
					If KIND_DATA=2, the data is expressed as a profile in flux distance from the separatrix (not yet available).
				""", '0'),
   
      'TDATA' : ('b2.transport.inputfile', 'real*8 data of size (3,NY+2,NKIND_COEFF,0:NS)', """
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
   
      'TRANSPORT_FILENAME' : ('b2.transport.inputfile', 'character*256', """
					Name of the next file to use for reading a new /TRANSPORT/ namelist.
				""", 'b2.transport.inputfile'),
   
      'TRANSPORT_TIME_MOD' : ('b2.transport.inputfile', 'real*8', """
					When the B2 run simulation time, in seconds, modulo(TRANSPORT_TIME_MOD),exceeds TRANSPORT_TIME_SWITCH, reads the new namelist from TRANSPORT_FILENAME. Also switches to the new namelist if the ELM count (here time/TRANSPORT_TIME_MOD) changes. Only active if TRANSPORT_TIME_MOD is greater than 0.
				""", '0.0'),
   
      'TRANSPORT_TIME_SWITCH' : ('b2.transport.inputfile', 'real*8', """
					Time (in seconds) within an ELM cycle after which a new /TRANSPORT/ namelist is read.
				""", '0.0'),
   
      'REGION_FLAGS' : ('b2.transport.inputfile', 'logical array of size (NREG,NKIND_COEFF)', """
					If region_flags(ireg,ikind) is .true. (default), then the transport parameters profiles for region (ireg) and kind (ikind) are used.
				""", '.true.'),
   
      'NO_PFLUX' : ('b2.transport.inputfile', 'logical', """
					If .true., transport coefficients profiles are not implemented in the private flux regions.
				""", '.false.'),
   
      'POLOIDAL_SCALING' : ('b2.transport.inputfile', 'logical array of size (10)', """
					If .true., then the transport coefficients profiles from the current b2.transport.inputfile are increased by a factor of 1.0+Gaussian where Gaussian is a Gaussian profile in the poloidal direction of amplitude SCALING_STRENGTH extending from SCALING_IX_BEGIN to SCALING_IX_END inclusively. The profile has a decay length of SCALING_WIDTH (in units of the number of poloidal cells).
				""", '.false.'),
   
      'SCALING_STRENGTH' : ('b2.transport.inputfile', 'real*8 array of size 10', """
					See above.
				""", '0'),
   
      'SCALING_WIDTH' : ('b2.transport.inputfile', 'real*8 array of size 10', """
					See above. Defaults to about 1/3 of the interval over which the scaling is to be done.
				""", '1/3 interval'),
   
      'SCALING_IX_BEGIN' : ('b2.transport.inputfile', 'integer array of size 10', """
					See above.
				""", '-2'),
   
      'SCALING_IX_END' : ('b2.transport.inputfile', 'integer array of size 10', """
					See above.
				""", '-2'),
   
      'ELM_TIME_BEGIN' : ('b2.transport.inputfile', 'real*8', """
					Time (in seconds) modulo ELM_TIME_PERIOD at which the ELM phase begins and the ELM data must be used.
				""", '0.0'),
   
      'ELM_TIME_END' : ('b2.transport.inputfile', 'real*8', """
					Time (in seconds) modulo ELM_TIME_PERIOD at which the ELM phase ends and the ELM data is no longer used.
				""", '0.0'),
   
      'ELM_TIME_PERIOD' : ('b2.transport.inputfile', 'real*8', """
					Indicates the real frequency of simulated ELMs. See above for usage.
					If zero, no ELM profiles are used.
				""", '0.0'),
   
      'ELM_IX_BEGIN' : ('b2.transport.inputfile', 'integer', """
					Poloidal position at which the ELM profile starts to be applied.
				""", '-2'),
   
      'ELM_IX_END' : ('b2.transport.inputfile', 'integer', """
					Poloidal position at which the ELM profile ends being applied.
				""", '-2'),
   
      'SAVED_VOLREC' : ('b2.neutrals_save.parameters', 'real*8 array of size (NSTRAT)', """
					Contains the last value of the strength of volume recombination sources from stratum (istra).
				""", '0.0'),
   
      'DTCO' : ('b2.numerics.parameters', 'real*8 array of size (0:NS-1,0:NREG)', """
					Multiplier to the time used in solving the continuity equation of species (is) in region (ireg).
				""", '1.0'),
   
      'DTMO' : ('b2.numerics.parameters', 'real*8 array of size (0:NS-1,0:NREG)', """
					Multiplier to the time used in solving the parallel momentum equation of species (is) in region (ireg).
				""", '1.0'),
   
      'DTEE' : ('b2.numerics.parameters', 'real*8 array of size (0:NREG)', """
					Multiplier to the time used in solving the electron heat equation in region (ireg).
				""", '1.0'),
   
      'DTEI' : ('b2.numerics.parameters', 'real*8 array of size (0:NREG)', """
					Multiplier to the time used in solving the ion heat equation in region (ireg).
				""", '1.0'),
   
      'SOLVECO' : ('b2.numerics.parameters', 'logical array of size (0:NS-1,0:NREG)', """
					Indicates whether the continuity equation for species (is) is to be solved in region (ireg). Subservient to 'no_solve' switch.
				""", '.true.'),
   
      'SOLVEMO' : ('b2.numerics.parameters', 'logical array of size (0:NS-1,0:NREG)', """
					Indicates whether the parallel momentum equation for species (is) is to be solved in region (ireg). Subservient to 'no_solve' switch.
				""", '.true.'),
   
      'SOLVEPO' : ('b2.numerics.parameters', 'logical array of size (0:NREG)', """
					Indicates whether the potential energy equation is to be solved in region (ireg). Subservient to 'no_solve' switch.
				""", '.true.'),
   
      'SOLVEEE' : ('b2.numerics.parameters', 'logical array of size (0:NREG)', """
					Indicates whether the electron energy equation is to be solved in region (ireg). Subservient to 'no_solve' switch.
				""", '.true.'),
   
      'SOLVEEI' : ('b2.numerics.parameters', 'logical array of size (0:NREG)', """
					Indicates whether the ion energy equation is to be solved in region (ireg). Subservient to 'no_solve' switch.
				""", '.true.'),
   
      'TIME_FACTOR_REQUIRED' : ('b2.numerics.parameters', 'real*8', """
					Minimum time scale of evolution allowed for all equations. Only active is 'b2srsm_enable' is set to 1.
				""", '0.1'),
   
      'CORE_DT_SUPPRESSION' : ('b2.numerics.parameters', 'real*8', """
					De-multiplier to the timestep in the core. Only active if less than 1. Should be larger than 0. Applies fully to the innermost core ring of cells (IY .eq. -1). See CORE_DT_FACTOR for further use.
				""", '1.0'),
   
      'CORE_DT_FACTOR' : ('b2.numerics.parameters', 'real*8', """
					Multiplier to the timestep in the core. Only active is less than 1. Should be larger than 0. Multiplies each successive core ring of cells (increasing IY) by CORE_DT_FACTOR, until the local time step multiplier is equal to 1.
				""", '1.0'),
   
      'NUMERICS_FILENAME' : ('b2.numerics.parameters', 'character*256', """
					Name of the next file to use for reading a new /NUMERICS/ namelist.
				""", 'b2.numerics.namelist'),
   
      'NUMERICS_TIME_MOD' : ('b2.numerics.parameters', 'real*8', """
					When the B2 run simulation time, in seconds, modulo(NUMERICS_TIME_MOD), exceeds NUMERICS_TIME_SWITCH, reads the new namelist from NUMERICS_FILENAME. Also switches to the new namelist as the ELM count (here time/NUMERICS_TIME_MOD) changes. Only active if NUMERICS_TIME_MOD is greater than 0.
				""", '0.0'),
   
      'NUMERICS_TIME_SWITCH' : ('b2.numerics.parameters', 'real*8', """
					Time (in seconds) within an ELM cycle after which a new /NUMERICS/ namelist is read.
				""", '0.0'),
   
      'WRITE_NML_NUM' : ('b2.numerics.parameters', 'logical', """
					If .true. (default), writes the content of the namelist to stdout after it has been read.
				""", '.true.'),
   
      'ETA_HCE_MULT' : ('b2.transport_models_save.parameters', 'real*8 array of size (-1:NY)', """
					Used by the user specified set_transport_eta transport model. See code for details.
				""", '1.0'),
   
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
   
      'CFLME' : ('', 'real*8', """
					For all flux limit multipliers, setting them to zero turns off the corresponding flux limiter.
				""", 'Default inherited from b2mn.dat'),
   
      'CFLMI' : ('', 'real*8', """
					For all flux limit multipliers, setting them to zero turns off the corresponding flux limiter.
				""", 'Default inherited from b2mn.dat'),
   
      'CFLMV' : ('', 'real*8', """
					For all flux limit multipliers, setting them to zero turns off the corresponding flux limiter.
				""", 'Default inherited from b2mn.dat'),
   
      'VOUT_CNV' : ('', 'real*8 array of size (0:NS-1)', """
					The four *_CNV parameters are only activated if 'b2tqna_user_transport' is set to '6'.
				""", '0.0'),
   
      'PW0_CNV' : ('', 'real*8 array of size (0:NS-1)', """
					The four *_CNV parameters are only activated if 'b2tqna_user_transport' is set to '6'.
				""", '1.0'),
   
      'PW1_CNV' : ('', 'real*8 array of size (0:NS-1)', """
					The four *_CNV parameters are only activated if 'b2tqna_user_transport' is set to '6'.
				""", '5.0'),
   
      'PW2_CNV' : ('', 'real*8 array of size (0:NS-1)', """
					The four *_CNV parameters are only activated if 'b2tqna_user_transport' is set to '6'.
				""", '2.0'),
   
      'PARM_DNA' : ('b2.transport.parameters', 'real*8 array of size (0:NS-1)', """
					Parameter for the density-driven particle diffusion coefficient for species (is).
				""", ''),
   
      'PARM_DPA' : ('b2.transport.parameters', 'real*8 array of size (0:NS-1)', """
					Parameter for the pressure-driven particle diffusion coefficient for species (is).
				""", ''),
   
      'PARM_VLA' : ('b2.transport.parameters', 'real*8 array of size (0:NS-1)', """
					Parameter for the anomalous radial pinch velocity for species (is).
				""", ''),
   
      'PARM_VSA' : ('b2.transport.parameters', 'real*8 array of size (0:NS-1)', """
					Parameter for the viscosity for species (is).
				""", ''),
   
      'PARM_HCI' : ('b2.transport.parameters', 'real*8 array of size (0:NS-1)', """
					Parameter for the heat diffusivity coefficient for species (is).
				""", ''),
   
      'PARM_HCE' : ('b2.transport.parameters', 'real*8', """
					Parameter for the electron heat diffusivity coefficient.
				""", ''),
   
      'PARM_SIG' : ('b2.transport.parameters', 'real*8', """
					Parameter for the anomalous radial field-driven current conductivity.
				""", ''),
   
      'PARM_ALF' : ('b2.transport.parameters', 'real*8', """
					Parameter for the anomalous radial temperature-driven current conductivity.
				""", ''),
   
      'TRANSPORT_FILENAME' : ('b2.transport.parameters', 'character*256', """
					Name of the next file to use for reading a new /TRANSPORT/ namelist.
				""", 'b2.transport.parameters'),
   
      'TRANSPORT_TIME_MOD' : ('b2.transport.parameters', 'real*8', """
					When the B2 run simulation time, in seconds, modulo(TRANSPORT_TIME_MOD), exceeds TRANSPORT_TIME_SWITCH, reads the new namelist from TRANSPORT_FILENAME. Also switches to the new namelist if the ELM count (here time/TRANSPORT_TIME_MOD) changes.
					Only active if TRANSPORT_TIME_MOD is greater than 0.
				""", '0.0'),
   
      'TRANSPORT_TIME_SWITCH' : ('b2.transport.parameters', 'real*8', """
					Time (in seconds) within an ELM cycle after which a new /TRANSPORT/ namelist is read.
				""", '0.0'),
   
      'WRITE_NML_TRANSP' : ('b2.transport.parameters', 'logical', """
					If .true. (default), writes the content of the namelist to stdout after it has been read.
				""", '.true.'),
   
      'LHETRGTS' : ('b2.user.parameters', 'integer array of size (NLIM)', """
					List of surface indices (EIRENE notation) which are used for calculation of helium enrichment.
				""", '-2 for the firt element, -3 for the second element and 0 otherwise'),
   
      'LPFRB_I' : ('b2.user.parameters', 'integer', """
					B2 x-cell indices corresponding to the bottom of the bypass between the inner and outer divertor (counted from the bottom, if non-positive) (inner side).
				""", '-2'),
   
      'LPFRB_O' : ('b2.user.parameters', 'integer', """
					B2 x-cell indices corresponding to the bottom of the bypass between the inner and outer divertor (counted from the bottom, if non-positive) (outer side).
				""", '-2'),
   
      'LPFRT_I' : ('b2.user.parameters', 'integer', """
					B2 x-cell indices corresponding to the top of the bypass between the inner and outer divertor (counted from the x-point, if non-positive) (inner side).
				""", '-2'),
   
      'LPFRT_O' : ('b2.user.parameters', 'integer', """
					B2 x-cell indices corresponding to the top of the bypass between the inner and outer divertor (counted from the x-point, if non-positive) (outer side).
				""", '-2'),
   
      'J_HE_AT' : ('b2.user.parameters', 'integer', """
					Species index of the helium atoms in Eirene. The code attempts to find a match by default.
				""", ''),
   
      'J_NE_AT' : ('b2.user.parameters', 'integer', """
					Species index of the neon atoms in Eirene. The code attempts to find a match by default.
				""", ''),
   
      'J_H_AT' : ('b2.user.parameters', 'integer', """
					Species index of the hydrogen atoms in Eirene. The code attempts to find a match by default.
				""", ''),
   
      'L_H_MOL' : ('b2.user.parameters', 'integer', """
					Species index of the hydrogen molecules in Eirene. The code attempts to find a match by default.
				""", ''),
   
      'FUSION_POWER' : ('b2.user.parameters', 'real*8', """
					Fusion power occuring in core (including neutrons, in Megawatts).
				""", '0.0'),
   
      'SPMP_HE_TO_D' : ('b2.user.parameters', 'real*8', """
					Ratio of He to DT pumping speeds (typically, 0.8).
				""", '1.0'),
   
      'LPFRS_PMP' : ('b2.user.parameters', 'integer', """
					Location of the pump. 0 no pump at all (default), 1 - lower PFR, 2 - lower outer
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
   
      'SPMP_NOM' : ('b2.user.parameters', 'real*8', """
					Nominal pumping speed.
				""", '0.0'),
   
      'USER_FILENAME' : ('b2.user.parameters', 'character*80', """
					Filename where /USER/ namelist is stored.
				""", 'b2.user.parameters'),
   
      'NX_SP' : ('b2.sputter_save.parameters', 'integer', """
					Array dimension NX used in this namelist.
				""", 'nx'),
   
      'NY_SP' : ('b2.sputter_save.parameters', 'integer', """
					Array dimension NY used in this namelist.
				""", 'ny'),
   
      'NS_SP' : ('b2.sputter_save.parameters', 'integer', """
					Array dimension NS used in this namelist.
				""", 'ns'),
   
      'SPUTTER_YIELD' : ('b2.sputter_save.parameters', 'real*8 array of size (-1:NX,-1:NY,0:NS-1,1:2)', """
					Contains the physical sputtering yield of species (is) at position (ix,iy) in element (:,:,:,1) and the chemical sputtering yield in element (:,:,:,2).
				""", '0.0'),
   
      'SPUTTER_YIELD2' : ('b2.sputter_save.parameters', 'real*8 array of size (-1:NX,-1:NY,0:NS-1,1:2)', """
					Contains the energy physical sputtering yield of species (is) at position (ix,iy) in element (:,:,:,1) and the energy chemical sputtering yield in element(:,:,:,2).
				""", '0.0'),
   
      'RESCALE_SA' : ('b2.atomic_physics_rescale.parameters', 'real*8 array of size(0:NS-1)', """
					Scaling factors for rtsa: ionisation rates of species (is).
				""", '1.0'),
   
      'RESCALE_RA' : ('b2.atomic_physics_rescale.parameters', 'real*8 array of size(0:NS-1)', """
					Scaling factors for rtra: recombination rates of species (is).
				""", '1.0'),
   
      'RESCALE_QA' : ('b2.atomic_physics_rescale.parameters', 'real*8 array of size(0:NS-1)', """
					Scaling factors for rtqa: electron cooling rates of species (is).
				""", '1.0'),
   
      'RESCALE_CX' : ('b2.atomic_physics_rescale.parameters', 'real*8 array of size(0:NS-1)', """
					Scaling factors for rtcx: charge exchange rates of species (is).
				""", '1.0'),
   
      'RESCALE_RD' : ('b2.atomic_physics_rescale.parameters', 'real*8 array of size(0:NS-1)', """
					Scaling factors for rtrd: line radiation rates of species (is).
				""", '1.0'),
   
      'RESCALE_BR' : ('b2.atomic_physics_rescale.parameters', 'real*8 array of size(0:NS-1)', """
					Scaling factors for rtbr: bremsstrahlung radiation rates of species (is).
				""", '1.0'),
   
      },
   
}

