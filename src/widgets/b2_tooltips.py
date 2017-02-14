b2ag_tooltips = {
         
      'dimens' : ('', 'string', 'specifies the size of the gridfirst pair is NX & NY of the grid you want to producesecond pair is the size of the grid that was originally createdeach needs to be an integer multiple of the corresponding entry of the first pair. Note that for double-
				null cases, the interior guard cells corresponding to the top divertor boundaries should not be multi-
				plied.', """None"""),
   
      'param' : ('', 'Integers', 'at least 100 additional numbers, of which only the first is relevant for us-1.0read the mesh data using the ”simplified” Carre format-2.0read the mesh data using the Sonnet format', """None"""),
   
}
b2ah_tooltips = {
         
      'dimens' : ('', 'Integer', 'the number of charge states', """None"""),
   
      'label' : ('', 'String', 'specifies, on the next line, a label for the run', """None"""),
   
      'b2cmpa' : ('', 'String', 'specifies a block of basic parameters.', """None"""),
   
      'b2cmpb' : ('', 'String', 'specifies a block of boundary conditions', """None"""),
   
      'b2cmpt' : ('', 'String', 'specifies a block of transport coefficients', """None"""),
   
      'specs' : ('', 'Strings', 'atomic charge, nuclear charge, atomic mass and atomic charge squared; this data should match that given in b2ai.dat
				Starting with code version 01.001.024, an alternative means of describing the plasma species and filling out the
				b2cmpa block is provided, in order to allow for bundling of charge states, when running cases with high-Z species.
				The relevant description is then
				minimum atomic charge of the stage, maximum atomic charge of the stage, nuclear charge, and atomic mass;
				this data should match that given in b2ai.dat
				The code can accept indifferently both types of input and makes the appropriate self-consistency checks. It is not
				permitted to bundle neutral and ionized species together.', """"""),
   
      'cbregs' : ('', 'Custom', 'specifies the number of regions where boundary conditions will be specifiedthe 'south' boundary is broken into three pieces with one quarter of the cells in the first region, half of
				the cells in the second, and the remaining quarter in the third region (inner target private flux, core, outer
				private flux). This is geometry-dependent information the code will check against the mesh connectivity
				and return an error if the two do not matchthe 'north', 'west' and 'east' are not broken up, and correspond to the SOL boundary, inner target and
				outer target, respectively. For double-null cases, the north boundary should be split into two sections', """None"""),
   
      'region' : ('', 'Custom', 'one block for each of the regions containing; the immediately following line being the region identifier', """None"""),
   
      'cbsna' : ('', 'Custom', 'boundary conditions for density (1 line per species)', """None"""),
   
      'cbsmo' : ('', 'String', 'boundary conditions for parallel momentum (1 line per species)', """None"""),
   
      'cbshi' : ('', 'String', 'ion/neutral (or "atomic") temperature/energy boundary condition (1 line per species)', """None"""),
   
      'cbshe' : ('', 'String', 'electron temperature/heat flux boundary condition', """None"""),
   
      'cbsch' : ('', 'String', 'boundary condition for the electric potential equation', """None"""),
   
      'cbrec' : ('', 'String', 'recycling coefficients (1 line per species)', """None"""),
   
      'cbmsa' : ('', 'String', '[unused]', """None"""),
   
      'cbmsb' : ('', 'String', '[unused] (1 line per species)', """None"""),
   
}
b2ar_tooltips = {
         
      'tlohi' : ('', 'Real*2', 'range of temperatures for atomic physics table in eV', """None"""),
   
      'nlohi' : ('', 'Real*2', 'range of densities for atomic physics table in m^-3', """None"""),
   
      'numnuc' : ('', 'Integer', 'number of distinct species', """None"""),
   
      'nucspec' : ('', 'Integer*3', 'nuclear charge, lowest charge state, highest charge state', """None"""),
   
      'flag' : ('', 'String', 'which atomic physics database to use', """adpak or strahl"""),
   
      'tailep' : ('', 'Real*2', 'range of temperatures for atomic physics table in eV', """None"""),
   
      'adpak' : ('', 'Real*2', 'A complete atomic physics package with scaling law rates applicable to all charge states, but not always of high accuracy [1]', """None"""),
   
      'strahl' : ('', 'Real*2', 'A collisional-radiative package developed at IPP–Garching [2], stored in the stra.dat file', """None"""),
   
      'adas' : ('', 'Real*2', '(Atomic Data and Analysis Structure) A complete collisional-radiative atomic physics database, actively being maintained and upgraded [3, 4]. Recommended. Available at http://adas.phys.strath.ac.uk/', """None"""),
   
      'amns' : ('', 'Real*2', '(Atomic, Molecular, Nuclear, and Surface data) For ITM-environment runs only, uses access to the ITM AMNS tools and database', """None"""),
   
}
b2ai_tooltips = {
         
      'dimens' : ('', 'Integer', 'the number of charge states', """None"""),
   
      'label' : ('', 'String', 'a label', """None"""),
   
      'specs' : ('', 'String Integer*4', 'atomic charge, nuclear charge, atomic mass and atomic charge squared for each charge stateminimum atomic charge of the stage, maximum atomic charge of the stage, nuclear charge, and atomic mass; this data should match that given in b2ah.dat', """None"""),
   
      'naini' : ('', 'Real*ns', 'initial densities for each of the charge states, in m^-3', """None"""),
   
      'ttini' : ('', 'Real', 'initial ion and electron temperature, in eV', """None"""),
   
}
b2mn_tooltips = {
         
      'b2cmpa' : ('', 'string', 'specifies a block of basic parameters, overriding those specified in the block of the same name in b2ah.dat', """None"""),
   
      'b2cmpb' : ('', 'string', 'specifies a block of boundary conditions, overriding those specified in the block of the same name in
        		b2ah.dat', """None"""),
   
      'b2cmpt' : ('', 'string', 'specifies a block of transport coefficients, overriding those specified in the block of the same name in
        		b2ah.dat', """None"""),
   
      'cflim' : ('', 'string', 'TODO', """None"""),
   
      'b2agdr_nxiso1' : ('Geometry', 'integer', '
				Range of an optional isolated region to be included in the geometry. 
				The isolated region will extend over the cell range spanned by (nxiso1:nxiso2,nyiso1:nyiso2).
				If only some of the four coordinates are given, the region is made to extent from the given coordinates to the end of the grid. Neighbourhood arrays and region indices are automatically adjusted.
			', """-2"""),
   
      'b2agdr_nxiso2' : ('Geometry', 'integer', '
				Range of an optional isolated region to be included in the geometry. 
				The isolated region will extend over the cell range spanned by (nxiso1:nxiso2,nyiso1:nyiso2).
				If only some of the four coordinates are given, the region is made to extent from the given coordinates to the end of the grid. Neighbourhood arrays and region indices are automatically adjusted.
			', """-2"""),
   
      'b2agdr_nyiso1' : ('Geometry', 'integer', '
				Range of an optional isolated region to be included in the geometry. 
				The isolated region will extend over the cell range spanned by (nxiso1:nxiso2,nyiso1:nyiso2).
				If only some of the four coordinates are given, the region is made to extent from the given coordinates to the end of the grid. Neighbourhood arrays and region indices are automatically adjusted.
			', """-2"""),
   
      'b2agdr_nyiso2' : ('Geometry', 'integer', '
				Range of an optional isolated region to be included in the geometry. 
				The isolated region will extend over the cell range spanned by (nxiso1:nxiso2,nyiso1:nyiso2).
				If only some of the four coordinates are given, the region is made to extent from the given coordinates to the end of the grid. Neighbourhood arrays and region indices are automatically adjusted.
			', """-2"""),
   
      'b2agfs_leftcut' : ('Geometry', 'integer', '
				Parameters describing the position and extent of the first topological cut, i.e. corresponding to the first X-point. Needed only to force different values from the ones computed automatically by b2ag.
			', """See description (integer)"""),
   
      'b2agfs_rightcut' : ('Geometry', 'integer', '
				Parameters describing the position and extent of the first topological cut, i.e. corresponding to the first X-point. Needed only to force different values from the ones computed automatically by b2ag.
			', """See description (integer)"""),
   
      'b2agfs_bottomcut' : ('Geometry', 'integer', '
				Parameters describing the position and extent of the first topological cut, i.e. corresponding to the first X-point. Needed only to force different values from the ones computed automatically by b2ag.
			', """See description (integer)"""),
   
      'b2agfs_topcut' : ('Geometry', 'integer', '
				Parameters describing the position and extent of the first topological cut, i.e. corresponding to the first X-point. Needed only to force different values from the ones computed automatically by b2ag.
			', """See description (integer)"""),
   
      'b2agfs_leftcut2' : ('Geometry', 'integer', '
				Parameters describing the position and extent of the second topological cut, i.e. corresponding to the second X-point. Needed only to force different values from the ones computed automatically by b2ag.		
			', """See description (integer)"""),
   
      'b2agfs_rightcut2' : ('Geometry', 'integer', '
				Parameters describing the position and extent of the second topological cut, i.e. corresponding to the second X-point. Needed only to force different values from the ones computed automatically by b2ag.		
			', """See description (integer)"""),
   
      'b2agfs_bottomcut2' : ('Geometry', 'integer', '
				Parameters describing the position and extent of the second topological cut, i.e. corresponding to the second X-point. Needed only to force different values from the ones computed automatically by b2ag.		
			', """See description (integer)"""),
   
      'b2agfs_topcut2' : ('Geometry', 'integer', '
				Parameters describing the position and extent of the second topological cut, i.e. corresponding to the second X-point. Needed only to force different values from the ones computed automatically by b2ag.		
			', """See description (integer)"""),
   
      'b2agfs_xoffset' : ('Geometry', 'real*8', '
				xoffset and yoffset are offsets of the basis mesh in the x- and y-direction respectively. The mesh will be translated by (xoffset,yoffset) if any of the two is non-zero from its position given in the local_sonnet (See 'b2agfs_geometry' above) file.
				To be used in b2ag.dat.
			', """0.0"""),
   
      'b2agfs_yoffset' : ('Geometry', 'real*8', '
				xoffset and yoffset are offsets of the basis mesh in the x- and y-direction respectively. The mesh will be translated by (xoffset,yoffset) if any of the two is non-zero from its position given in the local_sonnet (See 'b2agfs_geometry' above) file.
				To be used in b2ag.dat.
			', """0.0"""),
   
      'b2agfs_xrescale' : ('Geometry', 'real*8', '
				yrescale - real*8.
				Rescaling factors of the x- and y- coordinates of the basis mesh.
				To be used in b2ag.dat.
			', """1.0"""),
   
      'b2agfs_yrescale' : ('Geometry', 'real*8', '
				yrescale - real*8.
				Rescaling factors of the x- and y- coordinates of the basis mesh.
				To be used in b2ag.dat.
			', """1.0"""),
   
      'b2ardr_rtnt' : ('Atomic Physics', 'integer', '
				The number of intervals in the discretisation of the density (rtnn) and temperature (rtnt) ranges for the atomic physics tables.
			', """40"""),
   
      'b2ardr_rtnn' : ('Atomic Physics', 'integer', '
				The number of intervals in the discretisation of the density (rtnn) and temperature (rtnt) ranges for the atomic physics tables.
			', """16"""),
   
      'b2mndr_delta_max' : ('Run', 'real', '
				One of the dynamic timestep control parameters. Only active if both delta_max and delta_min are non-zero. The timestep is increased by a factor dt_change_inc or decreased by a factor dt_change_dec, within the bounds [dt_min, dt_max], according to whether the largest instantaneous change in all equations is smaller than delta_min or larger than delta_max, respectively.
			', """0.0"""),
   
      'b2mndr_delta_min' : ('Run', 'real', '
				One of the dynamic timestep control parameters. Only active if both delta_max and delta_min are non-zero. The timestep is increased by a factor dt_change_inc or decreased by a factor dt_change_dec, within the bounds [dt_min, dt_max], according to whether the largest instantaneous change in all equations is smaller than delta_min or larger than delta_max, respectively.
			', """0.0"""),
   
      'b2mndr_dt_change_dec' : ('Run', 'real', '
				One of the dynamic timestep control parameters. Only active if both delta_max and delta_min are non-zero. The timestep is increased by a factor dt_change_inc or decreased by a factor dt_change_dec, within the bounds [dt_min, dt_max], according to whether the largest instantaneous change in all equations is smaller than delta_min or larger than delta_max, respectively.
			', """1.0"""),
   
      'b2mndr_dt_change_inc' : ('Run', 'real', '
				One of the dynamic timestep control parameters. Only active if both delta_max and delta_min are non-zero. The timestep is increased by a factor dt_change_inc or decreased by a factor dt_change_dec, within the bounds [dt_min, dt_max], according to whether the largest instantaneous change in all equations is smaller than delta_min or larger than delta_max, respectively.
			', """1.0"""),
   
      'b2mndr_dt_max' : ('Run', 'real', '
				One of the dynamic timestep control parameters. Only active if both delta_max and delta_min are non-zero. The timestep is increased by a factor dt_change_inc or decreased by a factor dt_change_dec, within the bounds [dt_min, dt_max], according to whether the largest instantaneous change in all equations is smaller than delta_min or larger than delta_max, respectively.
			', """1.0e+01"""),
   
      'b2mndr_dt_min' : ('Run', 'real', '
				One of the dynamic timestep control parameters. Only active if both delta_max and delta_min are non-zero. The timestep is increased by a factor dt_change_inc or decreased by a factor dt_change_dec, within the bounds [dt_min, dt_max], according to whether the largest instantaneous change in all equations is smaller than delta_min or larger than delta_max, respectively.
			', """1.0e-30"""),
   
      'b2mndr_dpc_mod_rates_ne_hot_frac' : ('', 'real', '', """0.0"""),
   
      'b2mndr_dpc_mod_rates_te_hot' : ('', 'real', '', """0.0"""),
   
      'b2mndr_idout0' : ('Output', 'string', '
				idout0 and idout1 specify the desired selection of output segments; idout0 for output before the calculation and idout1 for output at the conclusion of the calculation. The generic description of either of these 'idout' variables follows. idout specifies the desired selection of output segments for printed and graphical output. Associated with each segment is a four-character word, which is identified on the printed output. (The same word may be associated with several segments.) A particular segment will be produced only if its associated word has a match, as defined by the routine strmas, in idout.
			', """pgnl;pgmm;pzmm"""),
   
      'b2mndr_idout1' : ('Output', 'string', '
				idout0 and idout1 specify the desired selection of output segments; idout0 for output before the calculation and idout1 for output at the conclusion of the calculation. The generic description of either of these 'idout' variables follows. idout specifies the desired selection of output segments for printed and graphical output. Associated with each segment is a four-character word, which is identified on the printed output. (The same word may be associated with several segments.) A particular segment will be produced only if its associated word has a match, as defined by the routine strmas, in idout.
			', """pzmm"""),
   
      'b2mndr_isfb' : ('Numerics', 'string', '
				Experimental: allows for density feedback of the number of electrons accompanying species 'isfb' at location (ixfb,iyfb).
				Note that ixfb and iyfb are real numbers!
			', """ismain"""),
   
      'b2mndr_ixfb' : ('Numerics', 'integer', '
				Experimental: allows for density feedback of the number of electrons accompanying species 'isfb' at location (ixfb,iyfb).
				Note that ixfb and iyfb are real numbers!
			', """5*nx/8"""),
   
      'b2mndr_iyfb' : ('Numerics', 'integer', '
				Experimental: allows for density feedback of the number of electrons accompanying species 'isfb' at location (ixfb,iyfb).
				Note that ixfb and iyfb are real numbers!
			', """ny/2"""),
   
      'b2mndr_ne_wanted' : ('Numerics', 'real', '
				Experimental: allows for density feedback of the number of electrons accompanying species 'isfb' at location (ixfb,iyfb).
				Note that ixfb and iyfb are real numbers!
			', """0.0"""),
   
      'b2mndr_ne_wanted_time' : ('Numerics', 'real', '
				Experimental: allows for density feedback of the number of electrons accompanying species 'isfb' at location (ixfb,iyfb).
				Note that ixfb and iyfb are real numbers!
			', """0.0"""),
   
      'b2mndr_min_areshe' : ('Numerics', 'real', '
				Minimum residuals for stopping a run. All criteria must be met simultaneously for the run to stop. The continuity equation residual applies to the "ismain" species (See "Run" section).
			', """0.0"""),
   
      'b2mndr_min_areshi' : ('Numerics', 'real', '
				Minimum residuals for stopping a run. All criteria must be met simultaneously for the run to stop. The continuity equation residual applies to the "ismain" species (See "Run" section).
			', """0.0"""),
   
      'b2mndr_min_aresco' : ('Numerics', 'real', '
				Minimum residuals for stopping a run. All criteria must be met simultaneously for the run to stop. The continuity equation residual applies to the "ismain" species (See "Run" section).
			', """0.0"""),
   
      'b2mndr_na_eps' : ('Output', 'real', '
					The five switches above are safeguards numbers for when printing changes after a time-step. The change is computed as:
					deltaX = abs((X(t)-X(t-1))/(X(t)+X_eps))
			', """1.0e19"""),
   
      'b2mndr_po_eps' : ('Output', 'real', '
					The five switches above are safeguards numbers for when printing changes after a time-step. The change is computed as:
					deltaX = abs((X(t)-X(t-1))/(X(t)+X_eps))
			', """1.0e+1"""),
   
      'b2mndr_te_eps' : ('Output', 'real', '
					The five switches above are safeguards numbers for when printing changes after a time-step. The change is computed as:
					deltaX = abs((X(t)-X(t-1))/(X(t)+X_eps))
			', """1.0e+1"""),
   
      'b2mndr_ti_eps' : ('Output', 'real', '
					The five switches above are safeguards numbers for when printing changes after a time-step. The change is computed as:
					deltaX = abs((X(t)-X(t-1))/(X(t)+X_eps))
			', """1.0e+1"""),
   
      'b2mndr_ua_eps' : ('Output', 'real', '
					The five switches above are safeguards numbers for when printing changes after a time-step. The change is computed as:
					deltaX = abs((X(t)-X(t-1))/(X(t)+X_eps))
			', """1.0e+4"""),
   
      'b2mndt_nstg_areshe' : ('Numerics', 'real', '
				Minimum residuals for an internal solution loop to stop.
				Used in conjunction with (not in replacement of) the nstg(0:2) numbers.
				All non-zero criteria must be met simultaneously. The continuity equation residual applies to the "ismain" species (See "Run" section).
			', """0.0"""),
   
      'b2mndt_nstg_areshi' : ('Numerics', 'real', '
				Minimum residuals for an internal solution loop to stop.
				Used in conjunction with (not in replacement of) the nstg(0:2) numbers.
				All non-zero criteria must be met simultaneously. The continuity equation residual applies to the "ismain" species (See "Run" section).
			', """0.0"""),
   
      'b2mndt_nstg_aresco' : ('Numerics', 'real', '
				Minimum residuals for an internal solution loop to stop.
				Used in conjunction with (not in replacement of) the nstg(0:2) numbers.
				All non-zero criteria must be met simultaneously. The continuity equation residual applies to the "ismain" species (See "Run" section).
			', """0.0"""),
   
      'b2mndt_nstg0' : ('Run', 'integer', '
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
				See "Numerics" section for details.
			', """1"""),
   
      'b2mndt_nstg1' : ('Run', 'integer', '
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
				See "Numerics" section for details.
			', """1"""),
   
      'b2mndt_nstg2' : ('Run', 'integer', '
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
				See "Numerics" section for details.
			', """1"""),
   
      'b2news_fac_ref' : ('Numerics', 'integer', '
				Parameters for spatial variation of the diamagnetic, ExB and viscosity drift term multipliers. These are allowed to have tanh profiles centered at tanh_a and of width tanh_b, where both quantities are in metres and measured along the radial coordinate for the cell column ix.eq.fac_ref (default value is jxa, see Geometry section for its computation). The maximum value of facdrift and fac_ExB is controlled by their respective _start and _target switches, see Run section for details.
				For consistency with the naming convention of related variables:
				b2news_facExB_tanh_a is an alias for b2news_fac_ExB_tanh_a,
				b2news_facExB_tanh_b is an alias for b2news_fac_ExB_tanh_b,
				b2news_facvis_tanh_a is an alias for 2news_fac_vis_tanh_a, and b2news_facvis_tanh_b is an alias for b2news_fac_vis_tanh_b. Additionally, for all core cell rows where iy.le.iy_nocoreExB, fac_ExB(ix,iy) is set to zero. This means that ExB contributions and flows will be zeroed out in those cells.
				For consistency with the boundary condition treatment, the value iy_nocoreExB.eq.-1 is NOT recommended!
			', """See description"""),
   
      'b2news_facdrift_tanh_a' : ('Numerics', 'real', '
				Parameters for spatial variation of the diamagnetic, ExB and viscosity drift term multipliers. These are allowed to have tanh profiles centered at tanh_a and of width tanh_b, where both quantities are in metres and measured along the radial coordinate for the cell column ix.eq.fac_ref (default value is jxa, see Geometry section for its computation). The maximum value of facdrift and fac_ExB is controlled by their respective _start and _target switches, see Run section for details.
				For consistency with the naming convention of related variables:
				b2news_facExB_tanh_a is an alias for b2news_fac_ExB_tanh_a,
				b2news_facExB_tanh_b is an alias for b2news_fac_ExB_tanh_b,
				b2news_facvis_tanh_a is an alias for 2news_fac_vis_tanh_a, and b2news_facvis_tanh_b is an alias for b2news_fac_vis_tanh_b. Additionally, for all core cell rows where iy.le.iy_nocoreExB, fac_ExB(ix,iy) is set to zero. This means that ExB contributions and flows will be zeroed out in those cells.
				For consistency with the boundary condition treatment, the value iy_nocoreExB.eq.-1 is NOT recommended!
			', """0.0"""),
   
      'b2news_facdrift_tanh_b' : ('Numerics', 'real', '
				Parameters for spatial variation of the diamagnetic, ExB and viscosity drift term multipliers. These are allowed to have tanh profiles centered at tanh_a and of width tanh_b, where both quantities are in metres and measured along the radial coordinate for the cell column ix.eq.fac_ref (default value is jxa, see Geometry section for its computation). The maximum value of facdrift and fac_ExB is controlled by their respective _start and _target switches, see Run section for details.
				For consistency with the naming convention of related variables:
				b2news_facExB_tanh_a is an alias for b2news_fac_ExB_tanh_a,
				b2news_facExB_tanh_b is an alias for b2news_fac_ExB_tanh_b,
				b2news_facvis_tanh_a is an alias for 2news_fac_vis_tanh_a, and b2news_facvis_tanh_b is an alias for b2news_fac_vis_tanh_b. Additionally, for all core cell rows where iy.le.iy_nocoreExB, fac_ExB(ix,iy) is set to zero. This means that ExB contributions and flows will be zeroed out in those cells.
				For consistency with the boundary condition treatment, the value iy_nocoreExB.eq.-1 is NOT recommended!
			', """0.0"""),
   
      'b2news_fac_ExB_tanh_a' : ('Numerics', 'real', '
				Parameters for spatial variation of the diamagnetic, ExB and viscosity drift term multipliers. These are allowed to have tanh profiles centered at tanh_a and of width tanh_b, where both quantities are in metres and measured along the radial coordinate for the cell column ix.eq.fac_ref (default value is jxa, see Geometry section for its computation). The maximum value of facdrift and fac_ExB is controlled by their respective _start and _target switches, see Run section for details.
				For consistency with the naming convention of related variables:
				b2news_facExB_tanh_a is an alias for b2news_fac_ExB_tanh_a,
				b2news_facExB_tanh_b is an alias for b2news_fac_ExB_tanh_b,
				b2news_facvis_tanh_a is an alias for 2news_fac_vis_tanh_a, and b2news_facvis_tanh_b is an alias for b2news_fac_vis_tanh_b. Additionally, for all core cell rows where iy.le.iy_nocoreExB, fac_ExB(ix,iy) is set to zero. This means that ExB contributions and flows will be zeroed out in those cells.
				For consistency with the boundary condition treatment, the value iy_nocoreExB.eq.-1 is NOT recommended!
			', """0.0"""),
   
      'b2news_fac_ExB_tanh_b' : ('Numerics', 'real', '
				Parameters for spatial variation of the diamagnetic, ExB and viscosity drift term multipliers. These are allowed to have tanh profiles centered at tanh_a and of width tanh_b, where both quantities are in metres and measured along the radial coordinate for the cell column ix.eq.fac_ref (default value is jxa, see Geometry section for its computation). The maximum value of facdrift and fac_ExB is controlled by their respective _start and _target switches, see Run section for details.
				For consistency with the naming convention of related variables:
				b2news_facExB_tanh_a is an alias for b2news_fac_ExB_tanh_a,
				b2news_facExB_tanh_b is an alias for b2news_fac_ExB_tanh_b,
				b2news_facvis_tanh_a is an alias for 2news_fac_vis_tanh_a, and b2news_facvis_tanh_b is an alias for b2news_fac_vis_tanh_b. Additionally, for all core cell rows where iy.le.iy_nocoreExB, fac_ExB(ix,iy) is set to zero. This means that ExB contributions and flows will be zeroed out in those cells.
				For consistency with the boundary condition treatment, the value iy_nocoreExB.eq.-1 is NOT recommended!
			', """0.0"""),
   
      'b2news_fac_vis_tanh_a' : ('Numerics', 'real', '
				Parameters for spatial variation of the diamagnetic, ExB and viscosity drift term multipliers. These are allowed to have tanh profiles centered at tanh_a and of width tanh_b, where both quantities are in metres and measured along the radial coordinate for the cell column ix.eq.fac_ref (default value is jxa, see Geometry section for its computation). The maximum value of facdrift and fac_ExB is controlled by their respective _start and _target switches, see Run section for details.
				For consistency with the naming convention of related variables:
				b2news_facExB_tanh_a is an alias for b2news_fac_ExB_tanh_a,
				b2news_facExB_tanh_b is an alias for b2news_fac_ExB_tanh_b,
				b2news_facvis_tanh_a is an alias for 2news_fac_vis_tanh_a, and b2news_facvis_tanh_b is an alias for b2news_fac_vis_tanh_b. Additionally, for all core cell rows where iy.le.iy_nocoreExB, fac_ExB(ix,iy) is set to zero. This means that ExB contributions and flows will be zeroed out in those cells.
				For consistency with the boundary condition treatment, the value iy_nocoreExB.eq.-1 is NOT recommended!
			', """0.0"""),
   
      'b2news_fac_vis_tanh_b' : ('Numerics', 'real', '
				Parameters for spatial variation of the diamagnetic, ExB and viscosity drift term multipliers. These are allowed to have tanh profiles centered at tanh_a and of width tanh_b, where both quantities are in metres and measured along the radial coordinate for the cell column ix.eq.fac_ref (default value is jxa, see Geometry section for its computation). The maximum value of facdrift and fac_ExB is controlled by their respective _start and _target switches, see Run section for details.
				For consistency with the naming convention of related variables:
				b2news_facExB_tanh_a is an alias for b2news_fac_ExB_tanh_a,
				b2news_facExB_tanh_b is an alias for b2news_fac_ExB_tanh_b,
				b2news_facvis_tanh_a is an alias for 2news_fac_vis_tanh_a, and b2news_facvis_tanh_b is an alias for b2news_fac_vis_tanh_b. Additionally, for all core cell rows where iy.le.iy_nocoreExB, fac_ExB(ix,iy) is set to zero. This means that ExB contributions and flows will be zeroed out in those cells.
				For consistency with the boundary condition treatment, the value iy_nocoreExB.eq.-1 is NOT recommended!
			', """0.0"""),
   
      'b2news_iy_nocoreExB' : ('Numerics', 'integer', '
				Parameters for spatial variation of the diamagnetic, ExB and viscosity drift term multipliers. These are allowed to have tanh profiles centered at tanh_a and of width tanh_b, where both quantities are in metres and measured along the radial coordinate for the cell column ix.eq.fac_ref (default value is jxa, see Geometry section for its computation). The maximum value of facdrift and fac_ExB is controlled by their respective _start and _target switches, see Run section for details.
				For consistency with the naming convention of related variables:
				b2news_facExB_tanh_a is an alias for b2news_fac_ExB_tanh_a,
				b2news_facExB_tanh_b is an alias for b2news_fac_ExB_tanh_b,
				b2news_facvis_tanh_a is an alias for 2news_fac_vis_tanh_a, and b2news_facvis_tanh_b is an alias for b2news_fac_vis_tanh_b. Additionally, for all core cell rows where iy.le.iy_nocoreExB, fac_ExB(ix,iy) is set to zero. This means that ExB contributions and flows will be zeroed out in those cells.
				For consistency with the boundary condition treatment, the value iy_nocoreExB.eq.-1 is NOT recommended!
			', """-2"""),
   
      'b2news_facdrift_dec' : ('Run', 'real', '
				Ramping parameters for facdrift, which multiplies the diamagnetic terms. The code is started on the first time step with facdrift=facdrift_start. If facdrift_target.ne.facdrift_start, then, on each time step, facdrift is multiplied by facdrift_inc. If the code does not converge on the timestep, facdrift is decreased by facdrift_dec. A facdrift profile is also possible, see Numerics section for details.
			', """0.0"""),
   
      'b2news_facdrift_inc' : ('Run', 'real', '
				Ramping parameters for facdrift, which multiplies the diamagnetic terms. The code is started on the first time step with facdrift=facdrift_start. If facdrift_target.ne.facdrift_start, then, on each time step, facdrift is multiplied by facdrift_inc. If the code does not converge on the timestep, facdrift is decreased by facdrift_dec. A facdrift profile is also possible, see Numerics section for details.
			', """1.0"""),
   
      'b2news_facdrift_start' : ('Run', 'real', '
				Ramping parameters for facdrift, which multiplies the diamagnetic terms. The code is started on the first time step with facdrift=facdrift_start. If facdrift_target.ne.facdrift_start, then, on each time step, facdrift is multiplied by facdrift_inc. If the code does not converge on the timestep, facdrift is decreased by facdrift_dec. A facdrift profile is also possible, see Numerics section for details.
			', """0.0"""),
   
      'b2news_facdrift_target' : ('Run', 'real', '
				Ramping parameters for facdrift, which multiplies the diamagnetic terms. The code is started on the first time step with facdrift=facdrift_start. If facdrift_target.ne.facdrift_start, then, on each time step, facdrift is multiplied by facdrift_inc. If the code does not converge on the timestep, facdrift is decreased by facdrift_dec. A facdrift profile is also possible, see Numerics section for details.
			', """0.0"""),
   
      'b2news_facExB_dec' : ('Run', 'real', '
				Ramping parameters for facExB, which multiplies the ExB terms. Same treatment as above for facdrift.
			', """0.0"""),
   
      'b2news_facExB_inc' : ('Run', 'real', '
				Ramping parameters for facExB, which multiplies the ExB terms. Same treatment as above for facdrift.
			', """1.0"""),
   
      'b2news_facExB_start' : ('Run', 'real', '
				Ramping parameters for facExB, which multiplies the ExB terms. Same treatment as above for facdrift.
			', """0.0"""),
   
      'b2news_facExB_target' : ('Run', 'real', '
				Ramping parameters for facExB, which multiplies the ExB terms. Same treatment as above for facdrift.
			', """0.0"""),
   
      'b2news_facvis_dec' : ('Run', 'real', '
				Ramping parameters for facvis, which multiplies the drift viscosity terms. Same treatment as above for facdrift.
			', """0.0"""),
   
      'b2news_facvis_inc' : ('Run', 'real', '
				Ramping parameters for facvis, which multiplies the drift viscosity terms. Same treatment as above for facdrift.
			', """1.0"""),
   
      'b2news_facvis_start' : ('Run', 'real', '
				Ramping parameters for facvis, which multiplies the drift viscosity terms. Same treatment as above for facdrift.
			', """0.0"""),
   
      'b2news_facvis_target' : ('Run', 'real', '
				Ramping parameters for facvis, which multiplies the drift viscosity terms. Same treatment as above for facdrift.
			', """0.0"""),
   
      'b2news_nsmin' : ('Numerics', 'integer', '
				Allows for solving only for the species range [nsmin:nsmax-1].
				ns - Number of species
			', """0"""),
   
      'b2news_nsmax' : ('Numerics', 'integer', '
				Allows for solving only for the species range [nsmin:nsmax-1].
				ns - Number of species
			', """ns"""),
   
      'b2news_potit' : ('Numerics', 'integer', '
				Maximum and minimum number of iterations in the potential equation. It must hold that potitmin < potit.
			', """50"""),
   
      'b2news_potitmin' : ('Numerics', 'integer', '
				Maximum and minimum number of iterations in the potential equation. It must hold that potitmin < potit.
			', """0"""),
   
      'b2news_xfm0' : ('Numerics', 'real', '
				Under-relaxation parameters for the parallel momentum, continuity, potential and energy equations respectively.
			', """1.0"""),
   
      'b2news_xfm1' : ('Numerics', 'real', '
				Under-relaxation parameters for the parallel momentum, continuity, potential and energy equations respectively.
			', """1.0"""),
   
      'b2news_xfm2' : ('Numerics', 'real', '
				Under-relaxation parameters for the parallel momentum, continuity, potential and energy equations respectively.
			', """1.0"""),
   
      'b2news_xfm3' : ('Numerics', 'real', '
				Under-relaxation parameters for the parallel momentum, continuity, potential and energy equations respectively.
			', """1.0"""),
   
      'b2npco_pcm0' : ('Numerics', 'real', '
				pcm0 specifies an additional under-relaxation factor that is applied to the velocity correction. It is required that 0.le.pcm0.and.0.le.pcm1.
			', """1.0"""),
   
      'b2npco_pcm1' : ('Numerics', 'real', '
				pcm0 specifies an additional under-relaxation factor that is applied to the velocity correction. It is required that 0.le.pcm0.and.0.le.pcm1.
			', """1.0"""),
   
      'b2npht_pcm0' : ('Numerics', 'real', '
				pcm0 specifies an additional under-relaxation factor that is applied to the temperature correction.
			', """1.0"""),
   
      'b2npht_pcm1' : ('Numerics', 'real', '
				pcm0 specifies an additional under-relaxation factor that is applied to the temperature correction.
			', """1.0"""),
   
      'b2sifr_limthee' : ('Physics', 'real', '
				Parameters for the computation of the thermal force term.
			', """0.3"""),
   
      'b2sifr_limthii' : ('Physics', 'real', '
				Parameters for the computation of the thermal force term.
			', """0.3"""),
   
      'b2sifr_phm1' : ('Physics', 'real', '
				Parameters for the computation of the thermal force term.
			', """1.0"""),
   
      'b2trcl_cthe' : ('Physics', 'real', '
				Parameters for the computation of the thermal force term.
			', """0.0"""),
   
      'b2trcl_cthi' : ('Physics', 'real', '
				Parameters for the computation of the thermal force term.
			', """2.65"""),
   
      'b2sifr_styl0' : ('Numerics', 'integer', '
				Specify the type of linearisation used in the thermal force term.
			', """0"""),
   
      'b2sifr_styl1' : ('Numerics', 'integer', '
				Specify the type of linearisation used in the thermal force term.
			', """0"""),
   
      'b2sihs_rf0' : ('Numerics', 'real', '
				rf0-4 are numerical parameters, see the code. All must be non-negative and of order unity; larger values are meant to provide more stabilisation. Some or all may be set to zero and
				removed eventually. I have had some experience to indicate that rf0, rf2, rf4 may have a useful function; however, later changes in the code may have made all these parameters superfluous.
			', """1.0"""),
   
      'b2sihs_rf1' : ('Numerics', 'real', '
				rf0-4 are numerical parameters, see the code. All must be non-negative and of order unity; larger values are meant to provide more stabilisation. Some or all may be set to zero and
				removed eventually. I have had some experience to indicate that rf0, rf2, rf4 may have a useful function; however, later changes in the code may have made all these parameters superfluous.
			', """1.0"""),
   
      'b2sihs_rf2' : ('Numerics', 'real', '
				rf0-4 are numerical parameters, see the code. All must be non-negative and of order unity; larger values are meant to provide more stabilisation. Some or all may be set to zero and
				removed eventually. I have had some experience to indicate that rf0, rf2, rf4 may have a useful function; however, later changes in the code may have made all these parameters superfluous.
			', """1.0"""),
   
      'b2sihs_rf3' : ('Numerics', 'real', '
				rf0-4 are numerical parameters, see the code. All must be non-negative and of order unity; larger values are meant to provide more stabilisation. Some or all may be set to zero and
				removed eventually. I have had some experience to indicate that rf0, rf2, rf4 may have a useful function; however, later changes in the code may have made all these parameters superfluous.
			', """1.0"""),
   
      'b2sihs_rf4' : ('Numerics', 'real', '
				rf0-4 are numerical parameters, see the code. All must be non-negative and of order unity; larger values are meant to provide more stabilisation. Some or all may be set to zero and
				removed eventually. I have had some experience to indicate that rf0, rf2, rf4 may have a useful function; however, later changes in the code may have made all these parameters superfluous.
			', """1.0"""),
   
      'b2sqcx_phm0' : ('Physics', 'real', '
				phm0 : Multiplier to the charge-exchange rate coefficient. Subservient to styl0: only used if styl0.eq.0 or is.lt.2. If styl0.ne.0, the charge-exchange rate coefficients for species of index 2 and above are set to zero.
			', """1.0"""),
   
      'b2sqcx_styl0' : ('Physics', 'integer', '
				phm0 : Multiplier to the charge-exchange rate coefficient. Subservient to styl0: only used if styl0.eq.0 or is.lt.2. If styl0.ne.0, the charge-exchange rate coefficients for species of index 2 and above are set to zero.
			', """0"""),
   
      'b2srdt_numerics_namelist' : ('Run', 'integer', '
				Namelist file indicators. If xxx_namelist.eq.1, then the code looks for the file b2.xxx.parameters, in which it expects to find the xxx namelist.
			', """0"""),
   
      'b2stbc_boundary_namelist' : ('Run', 'integer', '
				Namelist file indicators. If xxx_namelist.eq.1, then the code looks for the file b2.xxx.parameters, in which it expects to find the xxx namelist.
			', """0"""),
   
      'b2stbr_neutrals_namelist' : ('Run', 'integer', '
				Namelist file indicators. If xxx_namelist.eq.1, then the code looks for the file b2.xxx.parameters, in which it expects to find the xxx namelist.
			', """0"""),
   
      'b2tqna_transport_namelist' : ('Run', 'integer', '
				Namelist file indicators. If xxx_namelist.eq.1, then the code looks for the file b2.xxx.parameters, in which it expects to find the xxx namelist.
			', """0"""),
   
      'b2srdt_phm0' : ('Numerics', 'real', '
				Multipliers to the density, parallel momentum, heat, potential, and electron prticle time-derivative source terms, respectively.
				'phm4' is normally zero since the potential equation contains no source terms.
			', """1.0"""),
   
      'b2srdt_phm1' : ('Numerics', 'real', '
				Multipliers to the density, parallel momentum, heat, potential, and electron prticle time-derivative source terms, respectively.
				'phm4' is normally zero since the potential equation contains no source terms.
			', """1.0"""),
   
      'b2srdt_phm3' : ('Numerics', 'real', '
				Multipliers to the density, parallel momentum, heat, potential, and electron prticle time-derivative source terms, respectively.
				'phm4' is normally zero since the potential equation contains no source terms.
			', """1.0"""),
   
      'b2srdt_phm4' : ('Numerics', 'real', '
				Multipliers to the density, parallel momentum, heat, potential, and electron prticle time-derivative source terms, respectively.
				'phm4' is normally zero since the potential equation contains no source terms.
			', """0.0"""),
   
      'b2srdt_phm5' : ('Numerics', 'real', '
				Multipliers to the density, parallel momentum, heat, potential, and electron prticle time-derivative source terms, respectively.
				'phm4' is normally zero since the potential equation contains no source terms.
			', """1.0"""),
   
      'b2srst_rf0' : ('Numerics', 'real', '
				(rf0/1/2/3 for numerical stabilisation)
			', """1.0"""),
   
      'b2srst_rf1' : ('Numerics', 'real', '
				(rf0/1/2/3 for numerical stabilisation)
			', """1.0"""),
   
      'b2srst_rf2' : ('Numerics', 'real', '
				(rf0/1/2/3 for numerical stabilisation)
			', """1.0"""),
   
      'b2srst_rf3' : ('Numerics', 'real', '
				(rf0/1/2/3 for numerical stabilisation)
			', """1.0"""),
   
      'b2stbc_cbsnafac' : ('Numerics', 'real', '
				Feedback relaxation parameters. See Physics section for individual feedback quantities.
			', """0.01"""),
   
      'b2stbc_fchycore_alpha' : ('Numerics', 'real', '
				Feedback relaxation parameters. See Physics section for individual feedback quantities.
			', """0.1"""),
   
      'b2stbc_fheycore_alpha' : ('Numerics', 'real', '
				Feedback relaxation parameters. See Physics section for individual feedback quantities.
			', """0.1"""),
   
      'b2stbc_fhiycore_alpha' : ('Numerics', 'real', '
				Feedback relaxation parameters. See Physics section for individual feedback quantities.
			', """0.1"""),
   
      'b2stbc_fnaycore_alpha' : ('Numerics', 'real', '
				Feedback relaxation parameters. See Physics section for individual feedback quantities.
			', """0.1"""),
   
      'b2stbc_nesepm_alpha' : ('Numerics', 'real', '
				Feedback relaxation parameters. See Physics section for individual feedback quantities.
			', """1.0e-3"""),
   
      'b2stbc_nesepm_beta' : ('Numerics', 'real', '
				Feedback relaxation parameters. See Physics section for individual feedback quantities.
			', """0.0"""),
   
      'b2stbc_nesepm_gamma' : ('Numerics', 'real', '
				Feedback relaxation parameters. See Physics section for individual feedback quantities.
			', """0.99"""),
   
      'b2stbc_volrec_alpha' : ('Numerics', 'real', '
				Feedback relaxation parameters. See Physics section for individual feedback quantities.
			', """1.0e-3"""),
   
      'b2stbc_volrec_beta' : ('Numerics', 'real', '
				Feedback relaxation parameters. See Physics section for individual feedback quantities.
			', """1.0"""),
   
      'b2stbr_sput_chem_alpha' : ('Numerics', 'real', '
				Feedback relaxation parameters. See Physics section for individual feedback quantities.
			', """1.0e-2"""),
   
      'b2stbr_sput_phys_alpha' : ('Numerics', 'real', '
				Feedback relaxation parameters. See Physics section for individual feedback quantities.
			', """1.0e-2"""),
   
      'b2stbc_coreregno' : ('Geometry', '', '
				coreregno is the boundary index of the core boundary in the input files b2ah.dat and b2mn.dat. For a standard single-null case, coreregno is 1. For a straight geometry or limiter case, it is likely that coreregno need be set to 0, depending on the actual geometry details.
				coreregn2 is the boundary index of the second core boundary in case of a double-null geometry, and is not used otherwise.
			', """integer"""),
   
      'b2stbc_coreregn2' : ('Geometry', '', '
				coreregno is the boundary index of the core boundary in the input files b2ah.dat and b2mn.dat. For a standard single-null case, coreregno is 1. For a straight geometry or limiter case, it is likely that coreregno need be set to 0, depending on the actual geometry details.
				coreregn2 is the boundary index of the second core boundary in case of a double-null geometry, and is not used otherwise.
			', """integer"""),
   
      'b2stbc_fchycore' : ('Physics', 'real', '
				The 20 switches above are all feedback switches and require that b2stbc_feedback.ne.0 (See Run section for details) or that lfeedback=.true. in b2.boundary.parameters. The feedback is done as a boundary condition and is under-relaxed using the b2stbc_...._alpha switches (See Numerics section for details).
				fheycore is the radial electron heat flow entering the core boundary.
				fhiycore is the radial ion heat flow entering the core boundary.
				fchycore is the radial current entering the core boundary. fnaycore is the radial flux of species "isfeedback" entering the core boundary.
				If fhiycore_kinetic_energy.eq.1, the parallel kinetic energy flux is counted as part of the ion energy flux.
				For double-null cases, the f..ycore variables contain the total flow through both core boundaries taken together. The core boundaries are identified by the coreregno and coreregn2 switches (see Geometry section).
				The other seven switches are density feedback switches: nesepm is the outer midplane separatrix electron density. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is controlled through particle input of main plasma species isfeedback through the core boundary (See Geometry section for the core boundary indices coreregno and coreregn2).
				nesepm_sol is the outer midplane separatrix electron density, but
				this time controlled through a gas puff outside the SOL region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the SOL North boundary (See Geometry section for the SOL North boundary index solregno). If nesepm_overshoot.gt.1.0, the gas puff is turned off when the midplane separatrix density reaches nesepm*nesepm_overshoot. Minimum and maximum values of the feedback gas puff can be set using b2stbc_nesepm_minpuff and b2stbc_nesepm_maxpuff
				nepedm_sol is similar to nesepm_sol but the feedback is exerted on the electron density at the top of the pedestal, along the outer midplane, at radial position b2stbc_iyped. ndes_sol is the total particle content from the homonuclear sequence of species 'isfeedback' over the entire simulation domain.
				It is governed, like nesepm_sol, by nesepm_overshoot and nesepm_alpha and corresponds to a SOL boundary feedback. volrec_sol is the total particle source due to volume recombination coming from Eirene. Its feedback is governed by volrec_overshoot and volrec_alpha and volrec_beta parameters (See Numerics section for the latter two). nesepm_pfr is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the PFR region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the PFR South boundary indices pfrregno1 and pfrregno2).
				ndes is the total particle (neutrals + ions) content of the species whose neutral species has index isfeedback. This is controlled through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2).
				private_flux_puff is the particle flow of species isfeedback through the private flux region boundary. This is controlled through particle input of neutrals species isfeedback through the private flux boundaris (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2). 
				All but the first of these feedback schemes ("nesepm") can also be run though an Eirene neutral gas puff. In that case, one should set an appropriate gas puffing stratum in the Eirene input file input.dat, as well as in the b2.neutrals.parameters file. The code will assume, unless told otherwise through the use of "eirene_nesepm_istra", that the first stratum of type 'C' found in b2.neutrals.parameters is the stratum used for the feedback. If "eirene_nesepm_istra" is set to a positive number, the code will consider the feedback stratum to be the stratum in the "eirene_nesepm_istra"-th position in b2.neutrals.parameters.
			', """-1.0e30"""),
   
      'b2stbc_fheycore' : ('Physics', 'real', '
				The 20 switches above are all feedback switches and require that b2stbc_feedback.ne.0 (See Run section for details) or that lfeedback=.true. in b2.boundary.parameters. The feedback is done as a boundary condition and is under-relaxed using the b2stbc_...._alpha switches (See Numerics section for details).
				fheycore is the radial electron heat flow entering the core boundary.
				fhiycore is the radial ion heat flow entering the core boundary.
				fchycore is the radial current entering the core boundary. fnaycore is the radial flux of species "isfeedback" entering the core boundary.
				If fhiycore_kinetic_energy.eq.1, the parallel kinetic energy flux is counted as part of the ion energy flux.
				For double-null cases, the f..ycore variables contain the total flow through both core boundaries taken together. The core boundaries are identified by the coreregno and coreregn2 switches (see Geometry section).
				The other seven switches are density feedback switches: nesepm is the outer midplane separatrix electron density. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is controlled through particle input of main plasma species isfeedback through the core boundary (See Geometry section for the core boundary indices coreregno and coreregn2).
				nesepm_sol is the outer midplane separatrix electron density, but
				this time controlled through a gas puff outside the SOL region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the SOL North boundary (See Geometry section for the SOL North boundary index solregno). If nesepm_overshoot.gt.1.0, the gas puff is turned off when the midplane separatrix density reaches nesepm*nesepm_overshoot. Minimum and maximum values of the feedback gas puff can be set using b2stbc_nesepm_minpuff and b2stbc_nesepm_maxpuff
				nepedm_sol is similar to nesepm_sol but the feedback is exerted on the electron density at the top of the pedestal, along the outer midplane, at radial position b2stbc_iyped. ndes_sol is the total particle content from the homonuclear sequence of species 'isfeedback' over the entire simulation domain.
				It is governed, like nesepm_sol, by nesepm_overshoot and nesepm_alpha and corresponds to a SOL boundary feedback. volrec_sol is the total particle source due to volume recombination coming from Eirene. Its feedback is governed by volrec_overshoot and volrec_alpha and volrec_beta parameters (See Numerics section for the latter two). nesepm_pfr is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the PFR region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the PFR South boundary indices pfrregno1 and pfrregno2).
				ndes is the total particle (neutrals + ions) content of the species whose neutral species has index isfeedback. This is controlled through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2).
				private_flux_puff is the particle flow of species isfeedback through the private flux region boundary. This is controlled through particle input of neutrals species isfeedback through the private flux boundaris (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2). 
				All but the first of these feedback schemes ("nesepm") can also be run though an Eirene neutral gas puff. In that case, one should set an appropriate gas puffing stratum in the Eirene input file input.dat, as well as in the b2.neutrals.parameters file. The code will assume, unless told otherwise through the use of "eirene_nesepm_istra", that the first stratum of type 'C' found in b2.neutrals.parameters is the stratum used for the feedback. If "eirene_nesepm_istra" is set to a positive number, the code will consider the feedback stratum to be the stratum in the "eirene_nesepm_istra"-th position in b2.neutrals.parameters.
			', """0.0"""),
   
      'b2stbc_fhiycore' : ('Physics', 'real', '
				The 20 switches above are all feedback switches and require that b2stbc_feedback.ne.0 (See Run section for details) or that lfeedback=.true. in b2.boundary.parameters. The feedback is done as a boundary condition and is under-relaxed using the b2stbc_...._alpha switches (See Numerics section for details).
				fheycore is the radial electron heat flow entering the core boundary.
				fhiycore is the radial ion heat flow entering the core boundary.
				fchycore is the radial current entering the core boundary. fnaycore is the radial flux of species "isfeedback" entering the core boundary.
				If fhiycore_kinetic_energy.eq.1, the parallel kinetic energy flux is counted as part of the ion energy flux.
				For double-null cases, the f..ycore variables contain the total flow through both core boundaries taken together. The core boundaries are identified by the coreregno and coreregn2 switches (see Geometry section).
				The other seven switches are density feedback switches: nesepm is the outer midplane separatrix electron density. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is controlled through particle input of main plasma species isfeedback through the core boundary (See Geometry section for the core boundary indices coreregno and coreregn2).
				nesepm_sol is the outer midplane separatrix electron density, but
				this time controlled through a gas puff outside the SOL region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the SOL North boundary (See Geometry section for the SOL North boundary index solregno). If nesepm_overshoot.gt.1.0, the gas puff is turned off when the midplane separatrix density reaches nesepm*nesepm_overshoot. Minimum and maximum values of the feedback gas puff can be set using b2stbc_nesepm_minpuff and b2stbc_nesepm_maxpuff
				nepedm_sol is similar to nesepm_sol but the feedback is exerted on the electron density at the top of the pedestal, along the outer midplane, at radial position b2stbc_iyped. ndes_sol is the total particle content from the homonuclear sequence of species 'isfeedback' over the entire simulation domain.
				It is governed, like nesepm_sol, by nesepm_overshoot and nesepm_alpha and corresponds to a SOL boundary feedback. volrec_sol is the total particle source due to volume recombination coming from Eirene. Its feedback is governed by volrec_overshoot and volrec_alpha and volrec_beta parameters (See Numerics section for the latter two). nesepm_pfr is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the PFR region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the PFR South boundary indices pfrregno1 and pfrregno2).
				ndes is the total particle (neutrals + ions) content of the species whose neutral species has index isfeedback. This is controlled through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2).
				private_flux_puff is the particle flow of species isfeedback through the private flux region boundary. This is controlled through particle input of neutrals species isfeedback through the private flux boundaris (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2). 
				All but the first of these feedback schemes ("nesepm") can also be run though an Eirene neutral gas puff. In that case, one should set an appropriate gas puffing stratum in the Eirene input file input.dat, as well as in the b2.neutrals.parameters file. The code will assume, unless told otherwise through the use of "eirene_nesepm_istra", that the first stratum of type 'C' found in b2.neutrals.parameters is the stratum used for the feedback. If "eirene_nesepm_istra" is set to a positive number, the code will consider the feedback stratum to be the stratum in the "eirene_nesepm_istra"-th position in b2.neutrals.parameters.
			', """0.0"""),
   
      'b2stbc_fhiycore_kinetic_energy' : ('Physics', 'integer', '
				The 20 switches above are all feedback switches and require that b2stbc_feedback.ne.0 (See Run section for details) or that lfeedback=.true. in b2.boundary.parameters. The feedback is done as a boundary condition and is under-relaxed using the b2stbc_...._alpha switches (See Numerics section for details).
				fheycore is the radial electron heat flow entering the core boundary.
				fhiycore is the radial ion heat flow entering the core boundary.
				fchycore is the radial current entering the core boundary. fnaycore is the radial flux of species "isfeedback" entering the core boundary.
				If fhiycore_kinetic_energy.eq.1, the parallel kinetic energy flux is counted as part of the ion energy flux.
				For double-null cases, the f..ycore variables contain the total flow through both core boundaries taken together. The core boundaries are identified by the coreregno and coreregn2 switches (see Geometry section).
				The other seven switches are density feedback switches: nesepm is the outer midplane separatrix electron density. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is controlled through particle input of main plasma species isfeedback through the core boundary (See Geometry section for the core boundary indices coreregno and coreregn2).
				nesepm_sol is the outer midplane separatrix electron density, but
				this time controlled through a gas puff outside the SOL region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the SOL North boundary (See Geometry section for the SOL North boundary index solregno). If nesepm_overshoot.gt.1.0, the gas puff is turned off when the midplane separatrix density reaches nesepm*nesepm_overshoot. Minimum and maximum values of the feedback gas puff can be set using b2stbc_nesepm_minpuff and b2stbc_nesepm_maxpuff
				nepedm_sol is similar to nesepm_sol but the feedback is exerted on the electron density at the top of the pedestal, along the outer midplane, at radial position b2stbc_iyped. ndes_sol is the total particle content from the homonuclear sequence of species 'isfeedback' over the entire simulation domain.
				It is governed, like nesepm_sol, by nesepm_overshoot and nesepm_alpha and corresponds to a SOL boundary feedback. volrec_sol is the total particle source due to volume recombination coming from Eirene. Its feedback is governed by volrec_overshoot and volrec_alpha and volrec_beta parameters (See Numerics section for the latter two). nesepm_pfr is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the PFR region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the PFR South boundary indices pfrregno1 and pfrregno2).
				ndes is the total particle (neutrals + ions) content of the species whose neutral species has index isfeedback. This is controlled through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2).
				private_flux_puff is the particle flow of species isfeedback through the private flux region boundary. This is controlled through particle input of neutrals species isfeedback through the private flux boundaris (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2). 
				All but the first of these feedback schemes ("nesepm") can also be run though an Eirene neutral gas puff. In that case, one should set an appropriate gas puffing stratum in the Eirene input file input.dat, as well as in the b2.neutrals.parameters file. The code will assume, unless told otherwise through the use of "eirene_nesepm_istra", that the first stratum of type 'C' found in b2.neutrals.parameters is the stratum used for the feedback. If "eirene_nesepm_istra" is set to a positive number, the code will consider the feedback stratum to be the stratum in the "eirene_nesepm_istra"-th position in b2.neutrals.parameters.
			', """0"""),
   
      'b2stbc_fnaycore' : ('Physics', 'real', '
				The 20 switches above are all feedback switches and require that b2stbc_feedback.ne.0 (See Run section for details) or that lfeedback=.true. in b2.boundary.parameters. The feedback is done as a boundary condition and is under-relaxed using the b2stbc_...._alpha switches (See Numerics section for details).
				fheycore is the radial electron heat flow entering the core boundary.
				fhiycore is the radial ion heat flow entering the core boundary.
				fchycore is the radial current entering the core boundary. fnaycore is the radial flux of species "isfeedback" entering the core boundary.
				If fhiycore_kinetic_energy.eq.1, the parallel kinetic energy flux is counted as part of the ion energy flux.
				For double-null cases, the f..ycore variables contain the total flow through both core boundaries taken together. The core boundaries are identified by the coreregno and coreregn2 switches (see Geometry section).
				The other seven switches are density feedback switches: nesepm is the outer midplane separatrix electron density. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is controlled through particle input of main plasma species isfeedback through the core boundary (See Geometry section for the core boundary indices coreregno and coreregn2).
				nesepm_sol is the outer midplane separatrix electron density, but
				this time controlled through a gas puff outside the SOL region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the SOL North boundary (See Geometry section for the SOL North boundary index solregno). If nesepm_overshoot.gt.1.0, the gas puff is turned off when the midplane separatrix density reaches nesepm*nesepm_overshoot. Minimum and maximum values of the feedback gas puff can be set using b2stbc_nesepm_minpuff and b2stbc_nesepm_maxpuff
				nepedm_sol is similar to nesepm_sol but the feedback is exerted on the electron density at the top of the pedestal, along the outer midplane, at radial position b2stbc_iyped. ndes_sol is the total particle content from the homonuclear sequence of species 'isfeedback' over the entire simulation domain.
				It is governed, like nesepm_sol, by nesepm_overshoot and nesepm_alpha and corresponds to a SOL boundary feedback. volrec_sol is the total particle source due to volume recombination coming from Eirene. Its feedback is governed by volrec_overshoot and volrec_alpha and volrec_beta parameters (See Numerics section for the latter two). nesepm_pfr is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the PFR region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the PFR South boundary indices pfrregno1 and pfrregno2).
				ndes is the total particle (neutrals + ions) content of the species whose neutral species has index isfeedback. This is controlled through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2).
				private_flux_puff is the particle flow of species isfeedback through the private flux region boundary. This is controlled through particle input of neutrals species isfeedback through the private flux boundaris (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2). 
				All but the first of these feedback schemes ("nesepm") can also be run though an Eirene neutral gas puff. In that case, one should set an appropriate gas puffing stratum in the Eirene input file input.dat, as well as in the b2.neutrals.parameters file. The code will assume, unless told otherwise through the use of "eirene_nesepm_istra", that the first stratum of type 'C' found in b2.neutrals.parameters is the stratum used for the feedback. If "eirene_nesepm_istra" is set to a positive number, the code will consider the feedback stratum to be the stratum in the "eirene_nesepm_istra"-th position in b2.neutrals.parameters.
			', """-1.0e30"""),
   
      'b2stbc_isfeedback' : ('Physics', 'integer', '
				The 20 switches above are all feedback switches and require that b2stbc_feedback.ne.0 (See Run section for details) or that lfeedback=.true. in b2.boundary.parameters. The feedback is done as a boundary condition and is under-relaxed using the b2stbc_...._alpha switches (See Numerics section for details).
				fheycore is the radial electron heat flow entering the core boundary.
				fhiycore is the radial ion heat flow entering the core boundary.
				fchycore is the radial current entering the core boundary. fnaycore is the radial flux of species "isfeedback" entering the core boundary.
				If fhiycore_kinetic_energy.eq.1, the parallel kinetic energy flux is counted as part of the ion energy flux.
				For double-null cases, the f..ycore variables contain the total flow through both core boundaries taken together. The core boundaries are identified by the coreregno and coreregn2 switches (see Geometry section).
				The other seven switches are density feedback switches: nesepm is the outer midplane separatrix electron density. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is controlled through particle input of main plasma species isfeedback through the core boundary (See Geometry section for the core boundary indices coreregno and coreregn2).
				nesepm_sol is the outer midplane separatrix electron density, but
				this time controlled through a gas puff outside the SOL region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the SOL North boundary (See Geometry section for the SOL North boundary index solregno). If nesepm_overshoot.gt.1.0, the gas puff is turned off when the midplane separatrix density reaches nesepm*nesepm_overshoot. Minimum and maximum values of the feedback gas puff can be set using b2stbc_nesepm_minpuff and b2stbc_nesepm_maxpuff
				nepedm_sol is similar to nesepm_sol but the feedback is exerted on the electron density at the top of the pedestal, along the outer midplane, at radial position b2stbc_iyped. ndes_sol is the total particle content from the homonuclear sequence of species 'isfeedback' over the entire simulation domain.
				It is governed, like nesepm_sol, by nesepm_overshoot and nesepm_alpha and corresponds to a SOL boundary feedback. volrec_sol is the total particle source due to volume recombination coming from Eirene. Its feedback is governed by volrec_overshoot and volrec_alpha and volrec_beta parameters (See Numerics section for the latter two). nesepm_pfr is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the PFR region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the PFR South boundary indices pfrregno1 and pfrregno2).
				ndes is the total particle (neutrals + ions) content of the species whose neutral species has index isfeedback. This is controlled through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2).
				private_flux_puff is the particle flow of species isfeedback through the private flux region boundary. This is controlled through particle input of neutrals species isfeedback through the private flux boundaris (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2). 
				All but the first of these feedback schemes ("nesepm") can also be run though an Eirene neutral gas puff. In that case, one should set an appropriate gas puffing stratum in the Eirene input file input.dat, as well as in the b2.neutrals.parameters file. The code will assume, unless told otherwise through the use of "eirene_nesepm_istra", that the first stratum of type 'C' found in b2.neutrals.parameters is the stratum used for the feedback. If "eirene_nesepm_istra" is set to a positive number, the code will consider the feedback stratum to be the stratum in the "eirene_nesepm_istra"-th position in b2.neutrals.parameters.
			', """0"""),
   
      'b2stbc_iyped' : ('Physics', 'integer', '
				The 20 switches above are all feedback switches and require that b2stbc_feedback.ne.0 (See Run section for details) or that lfeedback=.true. in b2.boundary.parameters. The feedback is done as a boundary condition and is under-relaxed using the b2stbc_...._alpha switches (See Numerics section for details).
				fheycore is the radial electron heat flow entering the core boundary.
				fhiycore is the radial ion heat flow entering the core boundary.
				fchycore is the radial current entering the core boundary. fnaycore is the radial flux of species "isfeedback" entering the core boundary.
				If fhiycore_kinetic_energy.eq.1, the parallel kinetic energy flux is counted as part of the ion energy flux.
				For double-null cases, the f..ycore variables contain the total flow through both core boundaries taken together. The core boundaries are identified by the coreregno and coreregn2 switches (see Geometry section).
				The other seven switches are density feedback switches: nesepm is the outer midplane separatrix electron density. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is controlled through particle input of main plasma species isfeedback through the core boundary (See Geometry section for the core boundary indices coreregno and coreregn2).
				nesepm_sol is the outer midplane separatrix electron density, but
				this time controlled through a gas puff outside the SOL region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the SOL North boundary (See Geometry section for the SOL North boundary index solregno). If nesepm_overshoot.gt.1.0, the gas puff is turned off when the midplane separatrix density reaches nesepm*nesepm_overshoot. Minimum and maximum values of the feedback gas puff can be set using b2stbc_nesepm_minpuff and b2stbc_nesepm_maxpuff
				nepedm_sol is similar to nesepm_sol but the feedback is exerted on the electron density at the top of the pedestal, along the outer midplane, at radial position b2stbc_iyped. ndes_sol is the total particle content from the homonuclear sequence of species 'isfeedback' over the entire simulation domain.
				It is governed, like nesepm_sol, by nesepm_overshoot and nesepm_alpha and corresponds to a SOL boundary feedback. volrec_sol is the total particle source due to volume recombination coming from Eirene. Its feedback is governed by volrec_overshoot and volrec_alpha and volrec_beta parameters (See Numerics section for the latter two). nesepm_pfr is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the PFR region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the PFR South boundary indices pfrregno1 and pfrregno2).
				ndes is the total particle (neutrals + ions) content of the species whose neutral species has index isfeedback. This is controlled through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2).
				private_flux_puff is the particle flow of species isfeedback through the private flux region boundary. This is controlled through particle input of neutrals species isfeedback through the private flux boundaris (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2). 
				All but the first of these feedback schemes ("nesepm") can also be run though an Eirene neutral gas puff. In that case, one should set an appropriate gas puffing stratum in the Eirene input file input.dat, as well as in the b2.neutrals.parameters file. The code will assume, unless told otherwise through the use of "eirene_nesepm_istra", that the first stratum of type 'C' found in b2.neutrals.parameters is the stratum used for the feedback. If "eirene_nesepm_istra" is set to a positive number, the code will consider the feedback stratum to be the stratum in the "eirene_nesepm_istra"-th position in b2.neutrals.parameters.
			', """jsep/2"""),
   
      'b2stbc_ndes' : ('Physics', 'real', '
				The 20 switches above are all feedback switches and require that b2stbc_feedback.ne.0 (See Run section for details) or that lfeedback=.true. in b2.boundary.parameters. The feedback is done as a boundary condition and is under-relaxed using the b2stbc_...._alpha switches (See Numerics section for details).
				fheycore is the radial electron heat flow entering the core boundary.
				fhiycore is the radial ion heat flow entering the core boundary.
				fchycore is the radial current entering the core boundary. fnaycore is the radial flux of species "isfeedback" entering the core boundary.
				If fhiycore_kinetic_energy.eq.1, the parallel kinetic energy flux is counted as part of the ion energy flux.
				For double-null cases, the f..ycore variables contain the total flow through both core boundaries taken together. The core boundaries are identified by the coreregno and coreregn2 switches (see Geometry section).
				The other seven switches are density feedback switches: nesepm is the outer midplane separatrix electron density. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is controlled through particle input of main plasma species isfeedback through the core boundary (See Geometry section for the core boundary indices coreregno and coreregn2).
				nesepm_sol is the outer midplane separatrix electron density, but
				this time controlled through a gas puff outside the SOL region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the SOL North boundary (See Geometry section for the SOL North boundary index solregno). If nesepm_overshoot.gt.1.0, the gas puff is turned off when the midplane separatrix density reaches nesepm*nesepm_overshoot. Minimum and maximum values of the feedback gas puff can be set using b2stbc_nesepm_minpuff and b2stbc_nesepm_maxpuff
				nepedm_sol is similar to nesepm_sol but the feedback is exerted on the electron density at the top of the pedestal, along the outer midplane, at radial position b2stbc_iyped. ndes_sol is the total particle content from the homonuclear sequence of species 'isfeedback' over the entire simulation domain.
				It is governed, like nesepm_sol, by nesepm_overshoot and nesepm_alpha and corresponds to a SOL boundary feedback. volrec_sol is the total particle source due to volume recombination coming from Eirene. Its feedback is governed by volrec_overshoot and volrec_alpha and volrec_beta parameters (See Numerics section for the latter two). nesepm_pfr is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the PFR region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the PFR South boundary indices pfrregno1 and pfrregno2).
				ndes is the total particle (neutrals + ions) content of the species whose neutral species has index isfeedback. This is controlled through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2).
				private_flux_puff is the particle flow of species isfeedback through the private flux region boundary. This is controlled through particle input of neutrals species isfeedback through the private flux boundaris (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2). 
				All but the first of these feedback schemes ("nesepm") can also be run though an Eirene neutral gas puff. In that case, one should set an appropriate gas puffing stratum in the Eirene input file input.dat, as well as in the b2.neutrals.parameters file. The code will assume, unless told otherwise through the use of "eirene_nesepm_istra", that the first stratum of type 'C' found in b2.neutrals.parameters is the stratum used for the feedback. If "eirene_nesepm_istra" is set to a positive number, the code will consider the feedback stratum to be the stratum in the "eirene_nesepm_istra"-th position in b2.neutrals.parameters.
			', """0.0"""),
   
      'b2stbc_ndes_sol' : ('Physics', 'real', '
				The 20 switches above are all feedback switches and require that b2stbc_feedback.ne.0 (See Run section for details) or that lfeedback=.true. in b2.boundary.parameters. The feedback is done as a boundary condition and is under-relaxed using the b2stbc_...._alpha switches (See Numerics section for details).
				fheycore is the radial electron heat flow entering the core boundary.
				fhiycore is the radial ion heat flow entering the core boundary.
				fchycore is the radial current entering the core boundary. fnaycore is the radial flux of species "isfeedback" entering the core boundary.
				If fhiycore_kinetic_energy.eq.1, the parallel kinetic energy flux is counted as part of the ion energy flux.
				For double-null cases, the f..ycore variables contain the total flow through both core boundaries taken together. The core boundaries are identified by the coreregno and coreregn2 switches (see Geometry section).
				The other seven switches are density feedback switches: nesepm is the outer midplane separatrix electron density. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is controlled through particle input of main plasma species isfeedback through the core boundary (See Geometry section for the core boundary indices coreregno and coreregn2).
				nesepm_sol is the outer midplane separatrix electron density, but
				this time controlled through a gas puff outside the SOL region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the SOL North boundary (See Geometry section for the SOL North boundary index solregno). If nesepm_overshoot.gt.1.0, the gas puff is turned off when the midplane separatrix density reaches nesepm*nesepm_overshoot. Minimum and maximum values of the feedback gas puff can be set using b2stbc_nesepm_minpuff and b2stbc_nesepm_maxpuff
				nepedm_sol is similar to nesepm_sol but the feedback is exerted on the electron density at the top of the pedestal, along the outer midplane, at radial position b2stbc_iyped. ndes_sol is the total particle content from the homonuclear sequence of species 'isfeedback' over the entire simulation domain.
				It is governed, like nesepm_sol, by nesepm_overshoot and nesepm_alpha and corresponds to a SOL boundary feedback. volrec_sol is the total particle source due to volume recombination coming from Eirene. Its feedback is governed by volrec_overshoot and volrec_alpha and volrec_beta parameters (See Numerics section for the latter two). nesepm_pfr is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the PFR region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the PFR South boundary indices pfrregno1 and pfrregno2).
				ndes is the total particle (neutrals + ions) content of the species whose neutral species has index isfeedback. This is controlled through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2).
				private_flux_puff is the particle flow of species isfeedback through the private flux region boundary. This is controlled through particle input of neutrals species isfeedback through the private flux boundaris (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2). 
				All but the first of these feedback schemes ("nesepm") can also be run though an Eirene neutral gas puff. In that case, one should set an appropriate gas puffing stratum in the Eirene input file input.dat, as well as in the b2.neutrals.parameters file. The code will assume, unless told otherwise through the use of "eirene_nesepm_istra", that the first stratum of type 'C' found in b2.neutrals.parameters is the stratum used for the feedback. If "eirene_nesepm_istra" is set to a positive number, the code will consider the feedback stratum to be the stratum in the "eirene_nesepm_istra"-th position in b2.neutrals.parameters.
			', """0.0"""),
   
      'b2stbc_nepedm_sol' : ('Physics', 'real', '
				The 20 switches above are all feedback switches and require that b2stbc_feedback.ne.0 (See Run section for details) or that lfeedback=.true. in b2.boundary.parameters. The feedback is done as a boundary condition and is under-relaxed using the b2stbc_...._alpha switches (See Numerics section for details).
				fheycore is the radial electron heat flow entering the core boundary.
				fhiycore is the radial ion heat flow entering the core boundary.
				fchycore is the radial current entering the core boundary. fnaycore is the radial flux of species "isfeedback" entering the core boundary.
				If fhiycore_kinetic_energy.eq.1, the parallel kinetic energy flux is counted as part of the ion energy flux.
				For double-null cases, the f..ycore variables contain the total flow through both core boundaries taken together. The core boundaries are identified by the coreregno and coreregn2 switches (see Geometry section).
				The other seven switches are density feedback switches: nesepm is the outer midplane separatrix electron density. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is controlled through particle input of main plasma species isfeedback through the core boundary (See Geometry section for the core boundary indices coreregno and coreregn2).
				nesepm_sol is the outer midplane separatrix electron density, but
				this time controlled through a gas puff outside the SOL region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the SOL North boundary (See Geometry section for the SOL North boundary index solregno). If nesepm_overshoot.gt.1.0, the gas puff is turned off when the midplane separatrix density reaches nesepm*nesepm_overshoot. Minimum and maximum values of the feedback gas puff can be set using b2stbc_nesepm_minpuff and b2stbc_nesepm_maxpuff
				nepedm_sol is similar to nesepm_sol but the feedback is exerted on the electron density at the top of the pedestal, along the outer midplane, at radial position b2stbc_iyped. ndes_sol is the total particle content from the homonuclear sequence of species 'isfeedback' over the entire simulation domain.
				It is governed, like nesepm_sol, by nesepm_overshoot and nesepm_alpha and corresponds to a SOL boundary feedback. volrec_sol is the total particle source due to volume recombination coming from Eirene. Its feedback is governed by volrec_overshoot and volrec_alpha and volrec_beta parameters (See Numerics section for the latter two). nesepm_pfr is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the PFR region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the PFR South boundary indices pfrregno1 and pfrregno2).
				ndes is the total particle (neutrals + ions) content of the species whose neutral species has index isfeedback. This is controlled through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2).
				private_flux_puff is the particle flow of species isfeedback through the private flux region boundary. This is controlled through particle input of neutrals species isfeedback through the private flux boundaris (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2). 
				All but the first of these feedback schemes ("nesepm") can also be run though an Eirene neutral gas puff. In that case, one should set an appropriate gas puffing stratum in the Eirene input file input.dat, as well as in the b2.neutrals.parameters file. The code will assume, unless told otherwise through the use of "eirene_nesepm_istra", that the first stratum of type 'C' found in b2.neutrals.parameters is the stratum used for the feedback. If "eirene_nesepm_istra" is set to a positive number, the code will consider the feedback stratum to be the stratum in the "eirene_nesepm_istra"-th position in b2.neutrals.parameters.
			', """0.0"""),
   
      'b2stbc_nesepm' : ('Physics', 'real', '
				The 20 switches above are all feedback switches and require that b2stbc_feedback.ne.0 (See Run section for details) or that lfeedback=.true. in b2.boundary.parameters. The feedback is done as a boundary condition and is under-relaxed using the b2stbc_...._alpha switches (See Numerics section for details).
				fheycore is the radial electron heat flow entering the core boundary.
				fhiycore is the radial ion heat flow entering the core boundary.
				fchycore is the radial current entering the core boundary. fnaycore is the radial flux of species "isfeedback" entering the core boundary.
				If fhiycore_kinetic_energy.eq.1, the parallel kinetic energy flux is counted as part of the ion energy flux.
				For double-null cases, the f..ycore variables contain the total flow through both core boundaries taken together. The core boundaries are identified by the coreregno and coreregn2 switches (see Geometry section).
				The other seven switches are density feedback switches: nesepm is the outer midplane separatrix electron density. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is controlled through particle input of main plasma species isfeedback through the core boundary (See Geometry section for the core boundary indices coreregno and coreregn2).
				nesepm_sol is the outer midplane separatrix electron density, but
				this time controlled through a gas puff outside the SOL region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the SOL North boundary (See Geometry section for the SOL North boundary index solregno). If nesepm_overshoot.gt.1.0, the gas puff is turned off when the midplane separatrix density reaches nesepm*nesepm_overshoot. Minimum and maximum values of the feedback gas puff can be set using b2stbc_nesepm_minpuff and b2stbc_nesepm_maxpuff
				nepedm_sol is similar to nesepm_sol but the feedback is exerted on the electron density at the top of the pedestal, along the outer midplane, at radial position b2stbc_iyped. ndes_sol is the total particle content from the homonuclear sequence of species 'isfeedback' over the entire simulation domain.
				It is governed, like nesepm_sol, by nesepm_overshoot and nesepm_alpha and corresponds to a SOL boundary feedback. volrec_sol is the total particle source due to volume recombination coming from Eirene. Its feedback is governed by volrec_overshoot and volrec_alpha and volrec_beta parameters (See Numerics section for the latter two). nesepm_pfr is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the PFR region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the PFR South boundary indices pfrregno1 and pfrregno2).
				ndes is the total particle (neutrals + ions) content of the species whose neutral species has index isfeedback. This is controlled through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2).
				private_flux_puff is the particle flow of species isfeedback through the private flux region boundary. This is controlled through particle input of neutrals species isfeedback through the private flux boundaris (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2). 
				All but the first of these feedback schemes ("nesepm") can also be run though an Eirene neutral gas puff. In that case, one should set an appropriate gas puffing stratum in the Eirene input file input.dat, as well as in the b2.neutrals.parameters file. The code will assume, unless told otherwise through the use of "eirene_nesepm_istra", that the first stratum of type 'C' found in b2.neutrals.parameters is the stratum used for the feedback. If "eirene_nesepm_istra" is set to a positive number, the code will consider the feedback stratum to be the stratum in the "eirene_nesepm_istra"-th position in b2.neutrals.parameters.
			', """0.0"""),
   
      'b2stbc_nesepm_overshoot' : ('Physics', 'real', '
				The 20 switches above are all feedback switches and require that b2stbc_feedback.ne.0 (See Run section for details) or that lfeedback=.true. in b2.boundary.parameters. The feedback is done as a boundary condition and is under-relaxed using the b2stbc_...._alpha switches (See Numerics section for details).
				fheycore is the radial electron heat flow entering the core boundary.
				fhiycore is the radial ion heat flow entering the core boundary.
				fchycore is the radial current entering the core boundary. fnaycore is the radial flux of species "isfeedback" entering the core boundary.
				If fhiycore_kinetic_energy.eq.1, the parallel kinetic energy flux is counted as part of the ion energy flux.
				For double-null cases, the f..ycore variables contain the total flow through both core boundaries taken together. The core boundaries are identified by the coreregno and coreregn2 switches (see Geometry section).
				The other seven switches are density feedback switches: nesepm is the outer midplane separatrix electron density. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is controlled through particle input of main plasma species isfeedback through the core boundary (See Geometry section for the core boundary indices coreregno and coreregn2).
				nesepm_sol is the outer midplane separatrix electron density, but
				this time controlled through a gas puff outside the SOL region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the SOL North boundary (See Geometry section for the SOL North boundary index solregno). If nesepm_overshoot.gt.1.0, the gas puff is turned off when the midplane separatrix density reaches nesepm*nesepm_overshoot. Minimum and maximum values of the feedback gas puff can be set using b2stbc_nesepm_minpuff and b2stbc_nesepm_maxpuff
				nepedm_sol is similar to nesepm_sol but the feedback is exerted on the electron density at the top of the pedestal, along the outer midplane, at radial position b2stbc_iyped. ndes_sol is the total particle content from the homonuclear sequence of species 'isfeedback' over the entire simulation domain.
				It is governed, like nesepm_sol, by nesepm_overshoot and nesepm_alpha and corresponds to a SOL boundary feedback. volrec_sol is the total particle source due to volume recombination coming from Eirene. Its feedback is governed by volrec_overshoot and volrec_alpha and volrec_beta parameters (See Numerics section for the latter two). nesepm_pfr is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the PFR region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the PFR South boundary indices pfrregno1 and pfrregno2).
				ndes is the total particle (neutrals + ions) content of the species whose neutral species has index isfeedback. This is controlled through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2).
				private_flux_puff is the particle flow of species isfeedback through the private flux region boundary. This is controlled through particle input of neutrals species isfeedback through the private flux boundaris (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2). 
				All but the first of these feedback schemes ("nesepm") can also be run though an Eirene neutral gas puff. In that case, one should set an appropriate gas puffing stratum in the Eirene input file input.dat, as well as in the b2.neutrals.parameters file. The code will assume, unless told otherwise through the use of "eirene_nesepm_istra", that the first stratum of type 'C' found in b2.neutrals.parameters is the stratum used for the feedback. If "eirene_nesepm_istra" is set to a positive number, the code will consider the feedback stratum to be the stratum in the "eirene_nesepm_istra"-th position in b2.neutrals.parameters.
			', """0.0"""),
   
      'b2stbc_nesepm_minpuff' : ('Physics', 'real', '
				The 20 switches above are all feedback switches and require that b2stbc_feedback.ne.0 (See Run section for details) or that lfeedback=.true. in b2.boundary.parameters. The feedback is done as a boundary condition and is under-relaxed using the b2stbc_...._alpha switches (See Numerics section for details).
				fheycore is the radial electron heat flow entering the core boundary.
				fhiycore is the radial ion heat flow entering the core boundary.
				fchycore is the radial current entering the core boundary. fnaycore is the radial flux of species "isfeedback" entering the core boundary.
				If fhiycore_kinetic_energy.eq.1, the parallel kinetic energy flux is counted as part of the ion energy flux.
				For double-null cases, the f..ycore variables contain the total flow through both core boundaries taken together. The core boundaries are identified by the coreregno and coreregn2 switches (see Geometry section).
				The other seven switches are density feedback switches: nesepm is the outer midplane separatrix electron density. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is controlled through particle input of main plasma species isfeedback through the core boundary (See Geometry section for the core boundary indices coreregno and coreregn2).
				nesepm_sol is the outer midplane separatrix electron density, but
				this time controlled through a gas puff outside the SOL region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the SOL North boundary (See Geometry section for the SOL North boundary index solregno). If nesepm_overshoot.gt.1.0, the gas puff is turned off when the midplane separatrix density reaches nesepm*nesepm_overshoot. Minimum and maximum values of the feedback gas puff can be set using b2stbc_nesepm_minpuff and b2stbc_nesepm_maxpuff
				nepedm_sol is similar to nesepm_sol but the feedback is exerted on the electron density at the top of the pedestal, along the outer midplane, at radial position b2stbc_iyped. ndes_sol is the total particle content from the homonuclear sequence of species 'isfeedback' over the entire simulation domain.
				It is governed, like nesepm_sol, by nesepm_overshoot and nesepm_alpha and corresponds to a SOL boundary feedback. volrec_sol is the total particle source due to volume recombination coming from Eirene. Its feedback is governed by volrec_overshoot and volrec_alpha and volrec_beta parameters (See Numerics section for the latter two). nesepm_pfr is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the PFR region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the PFR South boundary indices pfrregno1 and pfrregno2).
				ndes is the total particle (neutrals + ions) content of the species whose neutral species has index isfeedback. This is controlled through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2).
				private_flux_puff is the particle flow of species isfeedback through the private flux region boundary. This is controlled through particle input of neutrals species isfeedback through the private flux boundaris (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2). 
				All but the first of these feedback schemes ("nesepm") can also be run though an Eirene neutral gas puff. In that case, one should set an appropriate gas puffing stratum in the Eirene input file input.dat, as well as in the b2.neutrals.parameters file. The code will assume, unless told otherwise through the use of "eirene_nesepm_istra", that the first stratum of type 'C' found in b2.neutrals.parameters is the stratum used for the feedback. If "eirene_nesepm_istra" is set to a positive number, the code will consider the feedback stratum to be the stratum in the "eirene_nesepm_istra"-th position in b2.neutrals.parameters.
			', """0.0"""),
   
      'b2stbc_nesepm_maxpuff' : ('Physics', 'real', '
				The 20 switches above are all feedback switches and require that b2stbc_feedback.ne.0 (See Run section for details) or that lfeedback=.true. in b2.boundary.parameters. The feedback is done as a boundary condition and is under-relaxed using the b2stbc_...._alpha switches (See Numerics section for details).
				fheycore is the radial electron heat flow entering the core boundary.
				fhiycore is the radial ion heat flow entering the core boundary.
				fchycore is the radial current entering the core boundary. fnaycore is the radial flux of species "isfeedback" entering the core boundary.
				If fhiycore_kinetic_energy.eq.1, the parallel kinetic energy flux is counted as part of the ion energy flux.
				For double-null cases, the f..ycore variables contain the total flow through both core boundaries taken together. The core boundaries are identified by the coreregno and coreregn2 switches (see Geometry section).
				The other seven switches are density feedback switches: nesepm is the outer midplane separatrix electron density. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is controlled through particle input of main plasma species isfeedback through the core boundary (See Geometry section for the core boundary indices coreregno and coreregn2).
				nesepm_sol is the outer midplane separatrix electron density, but
				this time controlled through a gas puff outside the SOL region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the SOL North boundary (See Geometry section for the SOL North boundary index solregno). If nesepm_overshoot.gt.1.0, the gas puff is turned off when the midplane separatrix density reaches nesepm*nesepm_overshoot. Minimum and maximum values of the feedback gas puff can be set using b2stbc_nesepm_minpuff and b2stbc_nesepm_maxpuff
				nepedm_sol is similar to nesepm_sol but the feedback is exerted on the electron density at the top of the pedestal, along the outer midplane, at radial position b2stbc_iyped. ndes_sol is the total particle content from the homonuclear sequence of species 'isfeedback' over the entire simulation domain.
				It is governed, like nesepm_sol, by nesepm_overshoot and nesepm_alpha and corresponds to a SOL boundary feedback. volrec_sol is the total particle source due to volume recombination coming from Eirene. Its feedback is governed by volrec_overshoot and volrec_alpha and volrec_beta parameters (See Numerics section for the latter two). nesepm_pfr is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the PFR region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the PFR South boundary indices pfrregno1 and pfrregno2).
				ndes is the total particle (neutrals + ions) content of the species whose neutral species has index isfeedback. This is controlled through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2).
				private_flux_puff is the particle flow of species isfeedback through the private flux region boundary. This is controlled through particle input of neutrals species isfeedback through the private flux boundaris (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2). 
				All but the first of these feedback schemes ("nesepm") can also be run though an Eirene neutral gas puff. In that case, one should set an appropriate gas puffing stratum in the Eirene input file input.dat, as well as in the b2.neutrals.parameters file. The code will assume, unless told otherwise through the use of "eirene_nesepm_istra", that the first stratum of type 'C' found in b2.neutrals.parameters is the stratum used for the feedback. If "eirene_nesepm_istra" is set to a positive number, the code will consider the feedback stratum to be the stratum in the "eirene_nesepm_istra"-th position in b2.neutrals.parameters.
			', """0.0"""),
   
      'b2stbc_nesepm_pfr' : ('Physics', 'real', '
				The 20 switches above are all feedback switches and require that b2stbc_feedback.ne.0 (See Run section for details) or that lfeedback=.true. in b2.boundary.parameters. The feedback is done as a boundary condition and is under-relaxed using the b2stbc_...._alpha switches (See Numerics section for details).
				fheycore is the radial electron heat flow entering the core boundary.
				fhiycore is the radial ion heat flow entering the core boundary.
				fchycore is the radial current entering the core boundary. fnaycore is the radial flux of species "isfeedback" entering the core boundary.
				If fhiycore_kinetic_energy.eq.1, the parallel kinetic energy flux is counted as part of the ion energy flux.
				For double-null cases, the f..ycore variables contain the total flow through both core boundaries taken together. The core boundaries are identified by the coreregno and coreregn2 switches (see Geometry section).
				The other seven switches are density feedback switches: nesepm is the outer midplane separatrix electron density. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is controlled through particle input of main plasma species isfeedback through the core boundary (See Geometry section for the core boundary indices coreregno and coreregn2).
				nesepm_sol is the outer midplane separatrix electron density, but
				this time controlled through a gas puff outside the SOL region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the SOL North boundary (See Geometry section for the SOL North boundary index solregno). If nesepm_overshoot.gt.1.0, the gas puff is turned off when the midplane separatrix density reaches nesepm*nesepm_overshoot. Minimum and maximum values of the feedback gas puff can be set using b2stbc_nesepm_minpuff and b2stbc_nesepm_maxpuff
				nepedm_sol is similar to nesepm_sol but the feedback is exerted on the electron density at the top of the pedestal, along the outer midplane, at radial position b2stbc_iyped. ndes_sol is the total particle content from the homonuclear sequence of species 'isfeedback' over the entire simulation domain.
				It is governed, like nesepm_sol, by nesepm_overshoot and nesepm_alpha and corresponds to a SOL boundary feedback. volrec_sol is the total particle source due to volume recombination coming from Eirene. Its feedback is governed by volrec_overshoot and volrec_alpha and volrec_beta parameters (See Numerics section for the latter two). nesepm_pfr is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the PFR region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the PFR South boundary indices pfrregno1 and pfrregno2).
				ndes is the total particle (neutrals + ions) content of the species whose neutral species has index isfeedback. This is controlled through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2).
				private_flux_puff is the particle flow of species isfeedback through the private flux region boundary. This is controlled through particle input of neutrals species isfeedback through the private flux boundaris (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2). 
				All but the first of these feedback schemes ("nesepm") can also be run though an Eirene neutral gas puff. In that case, one should set an appropriate gas puffing stratum in the Eirene input file input.dat, as well as in the b2.neutrals.parameters file. The code will assume, unless told otherwise through the use of "eirene_nesepm_istra", that the first stratum of type 'C' found in b2.neutrals.parameters is the stratum used for the feedback. If "eirene_nesepm_istra" is set to a positive number, the code will consider the feedback stratum to be the stratum in the "eirene_nesepm_istra"-th position in b2.neutrals.parameters.
			', """0.0"""),
   
      'b2stbc_nesepm_sol' : ('Physics', 'real', '
				The 20 switches above are all feedback switches and require that b2stbc_feedback.ne.0 (See Run section for details) or that lfeedback=.true. in b2.boundary.parameters. The feedback is done as a boundary condition and is under-relaxed using the b2stbc_...._alpha switches (See Numerics section for details).
				fheycore is the radial electron heat flow entering the core boundary.
				fhiycore is the radial ion heat flow entering the core boundary.
				fchycore is the radial current entering the core boundary. fnaycore is the radial flux of species "isfeedback" entering the core boundary.
				If fhiycore_kinetic_energy.eq.1, the parallel kinetic energy flux is counted as part of the ion energy flux.
				For double-null cases, the f..ycore variables contain the total flow through both core boundaries taken together. The core boundaries are identified by the coreregno and coreregn2 switches (see Geometry section).
				The other seven switches are density feedback switches: nesepm is the outer midplane separatrix electron density. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is controlled through particle input of main plasma species isfeedback through the core boundary (See Geometry section for the core boundary indices coreregno and coreregn2).
				nesepm_sol is the outer midplane separatrix electron density, but
				this time controlled through a gas puff outside the SOL region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the SOL North boundary (See Geometry section for the SOL North boundary index solregno). If nesepm_overshoot.gt.1.0, the gas puff is turned off when the midplane separatrix density reaches nesepm*nesepm_overshoot. Minimum and maximum values of the feedback gas puff can be set using b2stbc_nesepm_minpuff and b2stbc_nesepm_maxpuff
				nepedm_sol is similar to nesepm_sol but the feedback is exerted on the electron density at the top of the pedestal, along the outer midplane, at radial position b2stbc_iyped. ndes_sol is the total particle content from the homonuclear sequence of species 'isfeedback' over the entire simulation domain.
				It is governed, like nesepm_sol, by nesepm_overshoot and nesepm_alpha and corresponds to a SOL boundary feedback. volrec_sol is the total particle source due to volume recombination coming from Eirene. Its feedback is governed by volrec_overshoot and volrec_alpha and volrec_beta parameters (See Numerics section for the latter two). nesepm_pfr is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the PFR region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the PFR South boundary indices pfrregno1 and pfrregno2).
				ndes is the total particle (neutrals + ions) content of the species whose neutral species has index isfeedback. This is controlled through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2).
				private_flux_puff is the particle flow of species isfeedback through the private flux region boundary. This is controlled through particle input of neutrals species isfeedback through the private flux boundaris (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2). 
				All but the first of these feedback schemes ("nesepm") can also be run though an Eirene neutral gas puff. In that case, one should set an appropriate gas puffing stratum in the Eirene input file input.dat, as well as in the b2.neutrals.parameters file. The code will assume, unless told otherwise through the use of "eirene_nesepm_istra", that the first stratum of type 'C' found in b2.neutrals.parameters is the stratum used for the feedback. If "eirene_nesepm_istra" is set to a positive number, the code will consider the feedback stratum to be the stratum in the "eirene_nesepm_istra"-th position in b2.neutrals.parameters.
			', """0.0"""),
   
      'b2stbc_private_flux_puff' : ('Physics', 'real', '
				The 20 switches above are all feedback switches and require that b2stbc_feedback.ne.0 (See Run section for details) or that lfeedback=.true. in b2.boundary.parameters. The feedback is done as a boundary condition and is under-relaxed using the b2stbc_...._alpha switches (See Numerics section for details).
				fheycore is the radial electron heat flow entering the core boundary.
				fhiycore is the radial ion heat flow entering the core boundary.
				fchycore is the radial current entering the core boundary. fnaycore is the radial flux of species "isfeedback" entering the core boundary.
				If fhiycore_kinetic_energy.eq.1, the parallel kinetic energy flux is counted as part of the ion energy flux.
				For double-null cases, the f..ycore variables contain the total flow through both core boundaries taken together. The core boundaries are identified by the coreregno and coreregn2 switches (see Geometry section).
				The other seven switches are density feedback switches: nesepm is the outer midplane separatrix electron density. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is controlled through particle input of main plasma species isfeedback through the core boundary (See Geometry section for the core boundary indices coreregno and coreregn2).
				nesepm_sol is the outer midplane separatrix electron density, but
				this time controlled through a gas puff outside the SOL region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the SOL North boundary (See Geometry section for the SOL North boundary index solregno). If nesepm_overshoot.gt.1.0, the gas puff is turned off when the midplane separatrix density reaches nesepm*nesepm_overshoot. Minimum and maximum values of the feedback gas puff can be set using b2stbc_nesepm_minpuff and b2stbc_nesepm_maxpuff
				nepedm_sol is similar to nesepm_sol but the feedback is exerted on the electron density at the top of the pedestal, along the outer midplane, at radial position b2stbc_iyped. ndes_sol is the total particle content from the homonuclear sequence of species 'isfeedback' over the entire simulation domain.
				It is governed, like nesepm_sol, by nesepm_overshoot and nesepm_alpha and corresponds to a SOL boundary feedback. volrec_sol is the total particle source due to volume recombination coming from Eirene. Its feedback is governed by volrec_overshoot and volrec_alpha and volrec_beta parameters (See Numerics section for the latter two). nesepm_pfr is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the PFR region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the PFR South boundary indices pfrregno1 and pfrregno2).
				ndes is the total particle (neutrals + ions) content of the species whose neutral species has index isfeedback. This is controlled through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2).
				private_flux_puff is the particle flow of species isfeedback through the private flux region boundary. This is controlled through particle input of neutrals species isfeedback through the private flux boundaris (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2). 
				All but the first of these feedback schemes ("nesepm") can also be run though an Eirene neutral gas puff. In that case, one should set an appropriate gas puffing stratum in the Eirene input file input.dat, as well as in the b2.neutrals.parameters file. The code will assume, unless told otherwise through the use of "eirene_nesepm_istra", that the first stratum of type 'C' found in b2.neutrals.parameters is the stratum used for the feedback. If "eirene_nesepm_istra" is set to a positive number, the code will consider the feedback stratum to be the stratum in the "eirene_nesepm_istra"-th position in b2.neutrals.parameters.
			', """0.0"""),
   
      'b2stbc_volrec' : ('Physics', 'real', '
				The 20 switches above are all feedback switches and require that b2stbc_feedback.ne.0 (See Run section for details) or that lfeedback=.true. in b2.boundary.parameters. The feedback is done as a boundary condition and is under-relaxed using the b2stbc_...._alpha switches (See Numerics section for details).
				fheycore is the radial electron heat flow entering the core boundary.
				fhiycore is the radial ion heat flow entering the core boundary.
				fchycore is the radial current entering the core boundary. fnaycore is the radial flux of species "isfeedback" entering the core boundary.
				If fhiycore_kinetic_energy.eq.1, the parallel kinetic energy flux is counted as part of the ion energy flux.
				For double-null cases, the f..ycore variables contain the total flow through both core boundaries taken together. The core boundaries are identified by the coreregno and coreregn2 switches (see Geometry section).
				The other seven switches are density feedback switches: nesepm is the outer midplane separatrix electron density. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is controlled through particle input of main plasma species isfeedback through the core boundary (See Geometry section for the core boundary indices coreregno and coreregn2).
				nesepm_sol is the outer midplane separatrix electron density, but
				this time controlled through a gas puff outside the SOL region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the SOL North boundary (See Geometry section for the SOL North boundary index solregno). If nesepm_overshoot.gt.1.0, the gas puff is turned off when the midplane separatrix density reaches nesepm*nesepm_overshoot. Minimum and maximum values of the feedback gas puff can be set using b2stbc_nesepm_minpuff and b2stbc_nesepm_maxpuff
				nepedm_sol is similar to nesepm_sol but the feedback is exerted on the electron density at the top of the pedestal, along the outer midplane, at radial position b2stbc_iyped. ndes_sol is the total particle content from the homonuclear sequence of species 'isfeedback' over the entire simulation domain.
				It is governed, like nesepm_sol, by nesepm_overshoot and nesepm_alpha and corresponds to a SOL boundary feedback. volrec_sol is the total particle source due to volume recombination coming from Eirene. Its feedback is governed by volrec_overshoot and volrec_alpha and volrec_beta parameters (See Numerics section for the latter two). nesepm_pfr is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the PFR region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the PFR South boundary indices pfrregno1 and pfrregno2).
				ndes is the total particle (neutrals + ions) content of the species whose neutral species has index isfeedback. This is controlled through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2).
				private_flux_puff is the particle flow of species isfeedback through the private flux region boundary. This is controlled through particle input of neutrals species isfeedback through the private flux boundaris (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2). 
				All but the first of these feedback schemes ("nesepm") can also be run though an Eirene neutral gas puff. In that case, one should set an appropriate gas puffing stratum in the Eirene input file input.dat, as well as in the b2.neutrals.parameters file. The code will assume, unless told otherwise through the use of "eirene_nesepm_istra", that the first stratum of type 'C' found in b2.neutrals.parameters is the stratum used for the feedback. If "eirene_nesepm_istra" is set to a positive number, the code will consider the feedback stratum to be the stratum in the "eirene_nesepm_istra"-th position in b2.neutrals.parameters.
			', """0.0"""),
   
      'b2stbc_volrec_overshoot' : ('Physics', 'real', '
				The 20 switches above are all feedback switches and require that b2stbc_feedback.ne.0 (See Run section for details) or that lfeedback=.true. in b2.boundary.parameters. The feedback is done as a boundary condition and is under-relaxed using the b2stbc_...._alpha switches (See Numerics section for details).
				fheycore is the radial electron heat flow entering the core boundary.
				fhiycore is the radial ion heat flow entering the core boundary.
				fchycore is the radial current entering the core boundary. fnaycore is the radial flux of species "isfeedback" entering the core boundary.
				If fhiycore_kinetic_energy.eq.1, the parallel kinetic energy flux is counted as part of the ion energy flux.
				For double-null cases, the f..ycore variables contain the total flow through both core boundaries taken together. The core boundaries are identified by the coreregno and coreregn2 switches (see Geometry section).
				The other seven switches are density feedback switches: nesepm is the outer midplane separatrix electron density. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is controlled through particle input of main plasma species isfeedback through the core boundary (See Geometry section for the core boundary indices coreregno and coreregn2).
				nesepm_sol is the outer midplane separatrix electron density, but
				this time controlled through a gas puff outside the SOL region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the SOL North boundary (See Geometry section for the SOL North boundary index solregno). If nesepm_overshoot.gt.1.0, the gas puff is turned off when the midplane separatrix density reaches nesepm*nesepm_overshoot. Minimum and maximum values of the feedback gas puff can be set using b2stbc_nesepm_minpuff and b2stbc_nesepm_maxpuff
				nepedm_sol is similar to nesepm_sol but the feedback is exerted on the electron density at the top of the pedestal, along the outer midplane, at radial position b2stbc_iyped. ndes_sol is the total particle content from the homonuclear sequence of species 'isfeedback' over the entire simulation domain.
				It is governed, like nesepm_sol, by nesepm_overshoot and nesepm_alpha and corresponds to a SOL boundary feedback. volrec_sol is the total particle source due to volume recombination coming from Eirene. Its feedback is governed by volrec_overshoot and volrec_alpha and volrec_beta parameters (See Numerics section for the latter two). nesepm_pfr is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the PFR region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the PFR South boundary indices pfrregno1 and pfrregno2).
				ndes is the total particle (neutrals + ions) content of the species whose neutral species has index isfeedback. This is controlled through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2).
				private_flux_puff is the particle flow of species isfeedback through the private flux region boundary. This is controlled through particle input of neutrals species isfeedback through the private flux boundaris (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2). 
				All but the first of these feedback schemes ("nesepm") can also be run though an Eirene neutral gas puff. In that case, one should set an appropriate gas puffing stratum in the Eirene input file input.dat, as well as in the b2.neutrals.parameters file. The code will assume, unless told otherwise through the use of "eirene_nesepm_istra", that the first stratum of type 'C' found in b2.neutrals.parameters is the stratum used for the feedback. If "eirene_nesepm_istra" is set to a positive number, the code will consider the feedback stratum to be the stratum in the "eirene_nesepm_istra"-th position in b2.neutrals.parameters.
			', """0.0"""),
   
      'eirene_nesepm_istra' : ('Physics', 'integer', '
				The 20 switches above are all feedback switches and require that b2stbc_feedback.ne.0 (See Run section for details) or that lfeedback=.true. in b2.boundary.parameters. The feedback is done as a boundary condition and is under-relaxed using the b2stbc_...._alpha switches (See Numerics section for details).
				fheycore is the radial electron heat flow entering the core boundary.
				fhiycore is the radial ion heat flow entering the core boundary.
				fchycore is the radial current entering the core boundary. fnaycore is the radial flux of species "isfeedback" entering the core boundary.
				If fhiycore_kinetic_energy.eq.1, the parallel kinetic energy flux is counted as part of the ion energy flux.
				For double-null cases, the f..ycore variables contain the total flow through both core boundaries taken together. The core boundaries are identified by the coreregno and coreregn2 switches (see Geometry section).
				The other seven switches are density feedback switches: nesepm is the outer midplane separatrix electron density. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is controlled through particle input of main plasma species isfeedback through the core boundary (See Geometry section for the core boundary indices coreregno and coreregn2).
				nesepm_sol is the outer midplane separatrix electron density, but
				this time controlled through a gas puff outside the SOL region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the SOL North boundary (See Geometry section for the SOL North boundary index solregno). If nesepm_overshoot.gt.1.0, the gas puff is turned off when the midplane separatrix density reaches nesepm*nesepm_overshoot. Minimum and maximum values of the feedback gas puff can be set using b2stbc_nesepm_minpuff and b2stbc_nesepm_maxpuff
				nepedm_sol is similar to nesepm_sol but the feedback is exerted on the electron density at the top of the pedestal, along the outer midplane, at radial position b2stbc_iyped. ndes_sol is the total particle content from the homonuclear sequence of species 'isfeedback' over the entire simulation domain.
				It is governed, like nesepm_sol, by nesepm_overshoot and nesepm_alpha and corresponds to a SOL boundary feedback. volrec_sol is the total particle source due to volume recombination coming from Eirene. Its feedback is governed by volrec_overshoot and volrec_alpha and volrec_beta parameters (See Numerics section for the latter two). nesepm_pfr is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the PFR region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the PFR South boundary indices pfrregno1 and pfrregno2).
				ndes is the total particle (neutrals + ions) content of the species whose neutral species has index isfeedback. This is controlled through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2).
				private_flux_puff is the particle flow of species isfeedback through the private flux region boundary. This is controlled through particle input of neutrals species isfeedback through the private flux boundaris (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2). 
				All but the first of these feedback schemes ("nesepm") can also be run though an Eirene neutral gas puff. In that case, one should set an appropriate gas puffing stratum in the Eirene input file input.dat, as well as in the b2.neutrals.parameters file. The code will assume, unless told otherwise through the use of "eirene_nesepm_istra", that the first stratum of type 'C' found in b2.neutrals.parameters is the stratum used for the feedback. If "eirene_nesepm_istra" is set to a positive number, the code will consider the feedback stratum to be the stratum in the "eirene_nesepm_istra"-th position in b2.neutrals.parameters.
			', """-1"""),
   
      'b2stbc_pfrregno1' : ('Geometry', 'integer', '
				pfrregno1 is the boundary index of the first half of the private flux region boundary on which feedback is being applied (through b2stbc_ndes or b2stbc_private_flux_puff) in the input files b2ah.dat and b2mn.dat. pfrregno2 is the second half of the same private flux region. For a standard single null, the pair should be (0,2). For a standard double-null, the lower private flux region is labelled with the pair (0,5), and the upper private flux region with the pair (2,3). One can use only one private flux region by setting pfrregno1.eq.pfrregno2.
			', """0"""),
   
      'b2stbc_pfrregno2' : ('Geometry', 'integer', '
				pfrregno1 is the boundary index of the first half of the private flux region boundary on which feedback is being applied (through b2stbc_ndes or b2stbc_private_flux_puff) in the input files b2ah.dat and b2mn.dat. pfrregno2 is the second half of the same private flux region. For a standard single null, the pair should be (0,2). For a standard double-null, the lower private flux region is labelled with the pair (0,5), and the upper private flux region with the pair (2,3). One can use only one private flux region by setting pfrregno1.eq.pfrregno2.
			', """2"""),
   
      'b2stbc_she0ep' : ('Numerics', 'real', '
				Small level sources introduced in all cells.
			', """1.0e-36"""),
   
      'b2stbc_shi0ep' : ('Numerics', 'real', '
				Small level sources introduced in all cells.
			', """1.0e-36"""),
   
      'b2stbc_sna0ep' : ('Numerics', 'real', '
				Small level sources introduced in all cells.
			', """1.0e-36"""),
   
      'b2stbc_type13_fac' : ('Numerics', 'real', '
				Additional feedback strength adjustment parameters for BCCON=13 boundary condition, density adjusted to match a specific flux.
				The density is adjusted by a factor of:
				(1.0_R8+CONPAR(IS,IB,2)*(DFS-FS)/ (abs(DFS)+abs(FS)+abs(type13_norm)+abs(NAS*type13_fac)))
				where FS is the current particle flux, DFS is the desired particle flux, and NAS the current volume-averaged density. The desired flux DFS is computed as
				CONPAR(IS,IB,1)+CONPAR(IS,IB,3)
				where the first number is provided directly by the user in b2.boundary.parameters and the second is internally set to correspond to the re-entry of ionised neutrals that have crossed into the core for cases run with Eirene where eirene_ionising_core is activated.
				See also the description of 'eirene_ionising_core'.
			', """1.0"""),
   
      'b2stbc_type13_norm' : ('Numerics', 'real', '
				Additional feedback strength adjustment parameters for BCCON=13 boundary condition, density adjusted to match a specific flux.
				The density is adjusted by a factor of:
				(1.0_R8+CONPAR(IS,IB,2)*(DFS-FS)/ (abs(DFS)+abs(FS)+abs(type13_norm)+abs(NAS*type13_fac)))
				where FS is the current particle flux, DFS is the desired particle flux, and NAS the current volume-averaged density. The desired flux DFS is computed as
				CONPAR(IS,IB,1)+CONPAR(IS,IB,3)
				where the first number is provided directly by the user in b2.boundary.parameters and the second is internally set to correspond to the re-entry of ionised neutrals that have crossed into the core for cases run with Eirene where eirene_ionising_core is activated.
				See also the description of 'eirene_ionising_core'.
			', """1.0e15"""),
   
      'b2stbc_type13_ref' : ('Physics', 'integer', '
				These switches are associated with the boundary condition of type 13, 16, 17, 20 or 21 for particle flux, or electron and ion energy fluxes, i.e. constant density or temperature giving a prescribed flux through a radial surface, located type13_ref or type16_ref radial steps away from the boundary of the computational domain, respectively, and applied type20_ref steps away. See code and description in b2cdcn for details.
				Type 21 also applies to the electric potential boundary condition.
				It scales the feedback strength according to the value of the variable on the ring type21_ref steps inside.
				When type16_ref.gt.1, then the position where the core flux tallies are computed moves along with the boundary condition.
				If type16_kinetic_energy.eq.1, then the parallel kinetic energy flux is included in the ion heat flux component of type 16 and 17 boundary conditions.
			', """1"""),
   
      'b2stbc_type16_kinetic_energy' : ('Physics', 'integer', '
				These switches are associated with the boundary condition of type 13, 16, 17, 20 or 21 for particle flux, or electron and ion energy fluxes, i.e. constant density or temperature giving a prescribed flux through a radial surface, located type13_ref or type16_ref radial steps away from the boundary of the computational domain, respectively, and applied type20_ref steps away. See code and description in b2cdcn for details.
				Type 21 also applies to the electric potential boundary condition.
				It scales the feedback strength according to the value of the variable on the ring type21_ref steps inside.
				When type16_ref.gt.1, then the position where the core flux tallies are computed moves along with the boundary condition.
				If type16_kinetic_energy.eq.1, then the parallel kinetic energy flux is included in the ion heat flux component of type 16 and 17 boundary conditions.
			', """0"""),
   
      'b2stbc_type16_ref' : ('Physics', 'integer', '
				These switches are associated with the boundary condition of type 13, 16, 17, 20 or 21 for particle flux, or electron and ion energy fluxes, i.e. constant density or temperature giving a prescribed flux through a radial surface, located type13_ref or type16_ref radial steps away from the boundary of the computational domain, respectively, and applied type20_ref steps away. See code and description in b2cdcn for details.
				Type 21 also applies to the electric potential boundary condition.
				It scales the feedback strength according to the value of the variable on the ring type21_ref steps inside.
				When type16_ref.gt.1, then the position where the core flux tallies are computed moves along with the boundary condition.
				If type16_kinetic_energy.eq.1, then the parallel kinetic energy flux is included in the ion heat flux component of type 16 and 17 boundary conditions.
			', """1"""),
   
      'b2stbc_type20_ref' : ('Physics', 'integer', '
				These switches are associated with the boundary condition of type 13, 16, 17, 20 or 21 for particle flux, or electron and ion energy fluxes, i.e. constant density or temperature giving a prescribed flux through a radial surface, located type13_ref or type16_ref radial steps away from the boundary of the computational domain, respectively, and applied type20_ref steps away. See code and description in b2cdcn for details.
				Type 21 also applies to the electric potential boundary condition.
				It scales the feedback strength according to the value of the variable on the ring type21_ref steps inside.
				When type16_ref.gt.1, then the position where the core flux tallies are computed moves along with the boundary condition.
				If type16_kinetic_energy.eq.1, then the parallel kinetic energy flux is included in the ion heat flux component of type 16 and 17 boundary conditions.
			', """1"""),
   
      'b2stbc_type21_ref' : ('Physics', 'integer', '
				These switches are associated with the boundary condition of type 13, 16, 17, 20 or 21 for particle flux, or electron and ion energy fluxes, i.e. constant density or temperature giving a prescribed flux through a radial surface, located type13_ref or type16_ref radial steps away from the boundary of the computational domain, respectively, and applied type20_ref steps away. See code and description in b2cdcn for details.
				Type 21 also applies to the electric potential boundary condition.
				It scales the feedback strength according to the value of the variable on the ring type21_ref steps inside.
				When type16_ref.gt.1, then the position where the core flux tallies are computed moves along with the boundary condition.
				If type16_kinetic_energy.eq.1, then the parallel kinetic energy flux is included in the ion heat flux component of type 16 and 17 boundary conditions.
			', """1"""),
   
      'b2stbr_alpha' : ('Physics', 'real', '
				Sputtering model switches. See the code in b2stbr and the b2mod_sputter module for specific implementation details and references.
				The default values represent the case of Graphite plates. Sput_src is the atomic number of the plasma species which causes chemical sputtering.
				Sput_dst (when .ge.0) is the species index of the destination species produced by physical sputtering, chemical sputtering and/or RES. If either of the latter two processes are included, the production chemical sputtering and RES rate calculations provided in the code assume that sput_dst points to a Carbon species.
				Sput_dst2 and sput_dst3 (when .ge.0) represent other species produced by wall interactions for mixed materials scenarios.
				Sput_frac_flag is the switch to turn on mixed materials scenarios (when sput_frac_flag.eq.1).
				Plate_model.eq.0 means the 0-D time-independent plate heating model while plate_model.eq.1 indicates the 1-D time-dependent plate heating treatment. Plate_model.eq.2 gives acces to a 2-D time-dependent model.
				Plate_option chooses the initialisation of the plate temperature profile. If plate_option.eq.1, the profile is set to the constant given in plate_temp. If plate_option.eq.2, the profile is computed to be the 0-D equilibrium profile. If plate_option.eq.3, the profile is read from results of the previous run.
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
				The switch sputter_energy_on turns on the energy contribution from the sputtered particles (physical and chemical).
				If sputter_energy_on.eq.0, the particles are sputtered cold, with no energy contribution to the ion heat equation. If sputter_energy_on.ne.0 (default), the chemically sputtered particles are re-introduced into the plasma with the thermal energy corresponding to the surface temperature of the material, while physically sputtered particles are re-introduced with the TRIM-calculated energy sputtering yield (if the TRIM model is used).
				Therm_evap turns on thermal evaporation when .gt.0.0 and is a multiplier to the thermal evaporation rate.
				Redep_alpha is the multiplier to the reduction of the sputtering yield due to prompt redeposition. The promptly redeposited species is counted as eroded-then-deposited species.
			', """0.25"""),
   
      'b2stbr_plate_model' : ('Physics', 'integer', '
				Sputtering model switches. See the code in b2stbr and the b2mod_sputter module for specific implementation details and references.
				The default values represent the case of Graphite plates. Sput_src is the atomic number of the plasma species which causes chemical sputtering.
				Sput_dst (when .ge.0) is the species index of the destination species produced by physical sputtering, chemical sputtering and/or RES. If either of the latter two processes are included, the production chemical sputtering and RES rate calculations provided in the code assume that sput_dst points to a Carbon species.
				Sput_dst2 and sput_dst3 (when .ge.0) represent other species produced by wall interactions for mixed materials scenarios.
				Sput_frac_flag is the switch to turn on mixed materials scenarios (when sput_frac_flag.eq.1).
				Plate_model.eq.0 means the 0-D time-independent plate heating model while plate_model.eq.1 indicates the 1-D time-dependent plate heating treatment. Plate_model.eq.2 gives acces to a 2-D time-dependent model.
				Plate_option chooses the initialisation of the plate temperature profile. If plate_option.eq.1, the profile is set to the constant given in plate_temp. If plate_option.eq.2, the profile is computed to be the 0-D equilibrium profile. If plate_option.eq.3, the profile is read from results of the previous run.
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
				The switch sputter_energy_on turns on the energy contribution from the sputtered particles (physical and chemical).
				If sputter_energy_on.eq.0, the particles are sputtered cold, with no energy contribution to the ion heat equation. If sputter_energy_on.ne.0 (default), the chemically sputtered particles are re-introduced into the plasma with the thermal energy corresponding to the surface temperature of the material, while physically sputtered particles are re-introduced with the TRIM-calculated energy sputtering yield (if the TRIM model is used).
				Therm_evap turns on thermal evaporation when .gt.0.0 and is a multiplier to the thermal evaporation rate.
				Redep_alpha is the multiplier to the reduction of the sputtering yield due to prompt redeposition. The promptly redeposited species is counted as eroded-then-deposited species.
			', """0"""),
   
      'b2stbr_plate_option' : ('Physics', 'integer', '
				Sputtering model switches. See the code in b2stbr and the b2mod_sputter module for specific implementation details and references.
				The default values represent the case of Graphite plates. Sput_src is the atomic number of the plasma species which causes chemical sputtering.
				Sput_dst (when .ge.0) is the species index of the destination species produced by physical sputtering, chemical sputtering and/or RES. If either of the latter two processes are included, the production chemical sputtering and RES rate calculations provided in the code assume that sput_dst points to a Carbon species.
				Sput_dst2 and sput_dst3 (when .ge.0) represent other species produced by wall interactions for mixed materials scenarios.
				Sput_frac_flag is the switch to turn on mixed materials scenarios (when sput_frac_flag.eq.1).
				Plate_model.eq.0 means the 0-D time-independent plate heating model while plate_model.eq.1 indicates the 1-D time-dependent plate heating treatment. Plate_model.eq.2 gives acces to a 2-D time-dependent model.
				Plate_option chooses the initialisation of the plate temperature profile. If plate_option.eq.1, the profile is set to the constant given in plate_temp. If plate_option.eq.2, the profile is computed to be the 0-D equilibrium profile. If plate_option.eq.3, the profile is read from results of the previous run.
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
				The switch sputter_energy_on turns on the energy contribution from the sputtered particles (physical and chemical).
				If sputter_energy_on.eq.0, the particles are sputtered cold, with no energy contribution to the ion heat equation. If sputter_energy_on.ne.0 (default), the chemically sputtered particles are re-introduced into the plasma with the thermal energy corresponding to the surface temperature of the material, while physically sputtered particles are re-introduced with the TRIM-calculated energy sputtering yield (if the TRIM model is used).
				Therm_evap turns on thermal evaporation when .gt.0.0 and is a multiplier to the thermal evaporation rate.
				Redep_alpha is the multiplier to the reduction of the sputtering yield due to prompt redeposition. The promptly redeposited species is counted as eroded-then-deposited species.
			', """3"""),
   
      'b2stbr_plate_temp' : ('Physics', 'real', '
				Sputtering model switches. See the code in b2stbr and the b2mod_sputter module for specific implementation details and references.
				The default values represent the case of Graphite plates. Sput_src is the atomic number of the plasma species which causes chemical sputtering.
				Sput_dst (when .ge.0) is the species index of the destination species produced by physical sputtering, chemical sputtering and/or RES. If either of the latter two processes are included, the production chemical sputtering and RES rate calculations provided in the code assume that sput_dst points to a Carbon species.
				Sput_dst2 and sput_dst3 (when .ge.0) represent other species produced by wall interactions for mixed materials scenarios.
				Sput_frac_flag is the switch to turn on mixed materials scenarios (when sput_frac_flag.eq.1).
				Plate_model.eq.0 means the 0-D time-independent plate heating model while plate_model.eq.1 indicates the 1-D time-dependent plate heating treatment. Plate_model.eq.2 gives acces to a 2-D time-dependent model.
				Plate_option chooses the initialisation of the plate temperature profile. If plate_option.eq.1, the profile is set to the constant given in plate_temp. If plate_option.eq.2, the profile is computed to be the 0-D equilibrium profile. If plate_option.eq.3, the profile is read from results of the previous run.
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
				The switch sputter_energy_on turns on the energy contribution from the sputtered particles (physical and chemical).
				If sputter_energy_on.eq.0, the particles are sputtered cold, with no energy contribution to the ion heat equation. If sputter_energy_on.ne.0 (default), the chemically sputtered particles are re-introduced into the plasma with the thermal energy corresponding to the surface temperature of the material, while physically sputtered particles are re-introduced with the TRIM-calculated energy sputtering yield (if the TRIM model is used).
				Therm_evap turns on thermal evaporation when .gt.0.0 and is a multiplier to the thermal evaporation rate.
				Redep_alpha is the multiplier to the reduction of the sputtering yield due to prompt redeposition. The promptly redeposited species is counted as eroded-then-deposited species.
			', """300.0"""),
   
      'b2stbr_plate_thick' : ('Physics', 'real', '
				Sputtering model switches. See the code in b2stbr and the b2mod_sputter module for specific implementation details and references.
				The default values represent the case of Graphite plates. Sput_src is the atomic number of the plasma species which causes chemical sputtering.
				Sput_dst (when .ge.0) is the species index of the destination species produced by physical sputtering, chemical sputtering and/or RES. If either of the latter two processes are included, the production chemical sputtering and RES rate calculations provided in the code assume that sput_dst points to a Carbon species.
				Sput_dst2 and sput_dst3 (when .ge.0) represent other species produced by wall interactions for mixed materials scenarios.
				Sput_frac_flag is the switch to turn on mixed materials scenarios (when sput_frac_flag.eq.1).
				Plate_model.eq.0 means the 0-D time-independent plate heating model while plate_model.eq.1 indicates the 1-D time-dependent plate heating treatment. Plate_model.eq.2 gives acces to a 2-D time-dependent model.
				Plate_option chooses the initialisation of the plate temperature profile. If plate_option.eq.1, the profile is set to the constant given in plate_temp. If plate_option.eq.2, the profile is computed to be the 0-D equilibrium profile. If plate_option.eq.3, the profile is read from results of the previous run.
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
				The switch sputter_energy_on turns on the energy contribution from the sputtered particles (physical and chemical).
				If sputter_energy_on.eq.0, the particles are sputtered cold, with no energy contribution to the ion heat equation. If sputter_energy_on.ne.0 (default), the chemically sputtered particles are re-introduced into the plasma with the thermal energy corresponding to the surface temperature of the material, while physically sputtered particles are re-introduced with the TRIM-calculated energy sputtering yield (if the TRIM model is used).
				Therm_evap turns on thermal evaporation when .gt.0.0 and is a multiplier to the thermal evaporation rate.
				Redep_alpha is the multiplier to the reduction of the sputtering yield due to prompt redeposition. The promptly redeposited species is counted as eroded-then-deposited species.
			', """0.00"""),
   
      'b2stbr_redep_alpha' : ('Physics', 'real', '
				Sputtering model switches. See the code in b2stbr and the b2mod_sputter module for specific implementation details and references.
				The default values represent the case of Graphite plates. Sput_src is the atomic number of the plasma species which causes chemical sputtering.
				Sput_dst (when .ge.0) is the species index of the destination species produced by physical sputtering, chemical sputtering and/or RES. If either of the latter two processes are included, the production chemical sputtering and RES rate calculations provided in the code assume that sput_dst points to a Carbon species.
				Sput_dst2 and sput_dst3 (when .ge.0) represent other species produced by wall interactions for mixed materials scenarios.
				Sput_frac_flag is the switch to turn on mixed materials scenarios (when sput_frac_flag.eq.1).
				Plate_model.eq.0 means the 0-D time-independent plate heating model while plate_model.eq.1 indicates the 1-D time-dependent plate heating treatment. Plate_model.eq.2 gives acces to a 2-D time-dependent model.
				Plate_option chooses the initialisation of the plate temperature profile. If plate_option.eq.1, the profile is set to the constant given in plate_temp. If plate_option.eq.2, the profile is computed to be the 0-D equilibrium profile. If plate_option.eq.3, the profile is read from results of the previous run.
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
				The switch sputter_energy_on turns on the energy contribution from the sputtered particles (physical and chemical).
				If sputter_energy_on.eq.0, the particles are sputtered cold, with no energy contribution to the ion heat equation. If sputter_energy_on.ne.0 (default), the chemically sputtered particles are re-introduced into the plasma with the thermal energy corresponding to the surface temperature of the material, while physically sputtered particles are re-introduced with the TRIM-calculated energy sputtering yield (if the TRIM model is used).
				Therm_evap turns on thermal evaporation when .gt.0.0 and is a multiplier to the thermal evaporation rate.
				Redep_alpha is the multiplier to the reduction of the sputtering yield due to prompt redeposition. The promptly redeposited species is counted as eroded-then-deposited species.
			', """0.00"""),
   
      'b2stbr_sput_chem_model' : ('Physics', 'integer', '
				Sputtering model switches. See the code in b2stbr and the b2mod_sputter module for specific implementation details and references.
				The default values represent the case of Graphite plates. Sput_src is the atomic number of the plasma species which causes chemical sputtering.
				Sput_dst (when .ge.0) is the species index of the destination species produced by physical sputtering, chemical sputtering and/or RES. If either of the latter two processes are included, the production chemical sputtering and RES rate calculations provided in the code assume that sput_dst points to a Carbon species.
				Sput_dst2 and sput_dst3 (when .ge.0) represent other species produced by wall interactions for mixed materials scenarios.
				Sput_frac_flag is the switch to turn on mixed materials scenarios (when sput_frac_flag.eq.1).
				Plate_model.eq.0 means the 0-D time-independent plate heating model while plate_model.eq.1 indicates the 1-D time-dependent plate heating treatment. Plate_model.eq.2 gives acces to a 2-D time-dependent model.
				Plate_option chooses the initialisation of the plate temperature profile. If plate_option.eq.1, the profile is set to the constant given in plate_temp. If plate_option.eq.2, the profile is computed to be the 0-D equilibrium profile. If plate_option.eq.3, the profile is read from results of the previous run.
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
				The switch sputter_energy_on turns on the energy contribution from the sputtered particles (physical and chemical).
				If sputter_energy_on.eq.0, the particles are sputtered cold, with no energy contribution to the ion heat equation. If sputter_energy_on.ne.0 (default), the chemically sputtered particles are re-introduced into the plasma with the thermal energy corresponding to the surface temperature of the material, while physically sputtered particles are re-introduced with the TRIM-calculated energy sputtering yield (if the TRIM model is used).
				Therm_evap turns on thermal evaporation when .gt.0.0 and is a multiplier to the thermal evaporation rate.
				Redep_alpha is the multiplier to the reduction of the sputtering yield due to prompt redeposition. The promptly redeposited species is counted as eroded-then-deposited species.
			', """0"""),
   
      'b2stbr_sput_chem_cutoff_alpha' : ('Physics', 'real', '
				Sputtering model switches. See the code in b2stbr and the b2mod_sputter module for specific implementation details and references.
				The default values represent the case of Graphite plates. Sput_src is the atomic number of the plasma species which causes chemical sputtering.
				Sput_dst (when .ge.0) is the species index of the destination species produced by physical sputtering, chemical sputtering and/or RES. If either of the latter two processes are included, the production chemical sputtering and RES rate calculations provided in the code assume that sput_dst points to a Carbon species.
				Sput_dst2 and sput_dst3 (when .ge.0) represent other species produced by wall interactions for mixed materials scenarios.
				Sput_frac_flag is the switch to turn on mixed materials scenarios (when sput_frac_flag.eq.1).
				Plate_model.eq.0 means the 0-D time-independent plate heating model while plate_model.eq.1 indicates the 1-D time-dependent plate heating treatment. Plate_model.eq.2 gives acces to a 2-D time-dependent model.
				Plate_option chooses the initialisation of the plate temperature profile. If plate_option.eq.1, the profile is set to the constant given in plate_temp. If plate_option.eq.2, the profile is computed to be the 0-D equilibrium profile. If plate_option.eq.3, the profile is read from results of the previous run.
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
				The switch sputter_energy_on turns on the energy contribution from the sputtered particles (physical and chemical).
				If sputter_energy_on.eq.0, the particles are sputtered cold, with no energy contribution to the ion heat equation. If sputter_energy_on.ne.0 (default), the chemically sputtered particles are re-introduced into the plasma with the thermal energy corresponding to the surface temperature of the material, while physically sputtered particles are re-introduced with the TRIM-calculated energy sputtering yield (if the TRIM model is used).
				Therm_evap turns on thermal evaporation when .gt.0.0 and is a multiplier to the thermal evaporation rate.
				Redep_alpha is the multiplier to the reduction of the sputtering yield due to prompt redeposition. The promptly redeposited species is counted as eroded-then-deposited species.
			', """1.0"""),
   
      'b2stbr_sput_chem_cutoff_beta' : ('Physics', 'real', '
				Sputtering model switches. See the code in b2stbr and the b2mod_sputter module for specific implementation details and references.
				The default values represent the case of Graphite plates. Sput_src is the atomic number of the plasma species which causes chemical sputtering.
				Sput_dst (when .ge.0) is the species index of the destination species produced by physical sputtering, chemical sputtering and/or RES. If either of the latter two processes are included, the production chemical sputtering and RES rate calculations provided in the code assume that sput_dst points to a Carbon species.
				Sput_dst2 and sput_dst3 (when .ge.0) represent other species produced by wall interactions for mixed materials scenarios.
				Sput_frac_flag is the switch to turn on mixed materials scenarios (when sput_frac_flag.eq.1).
				Plate_model.eq.0 means the 0-D time-independent plate heating model while plate_model.eq.1 indicates the 1-D time-dependent plate heating treatment. Plate_model.eq.2 gives acces to a 2-D time-dependent model.
				Plate_option chooses the initialisation of the plate temperature profile. If plate_option.eq.1, the profile is set to the constant given in plate_temp. If plate_option.eq.2, the profile is computed to be the 0-D equilibrium profile. If plate_option.eq.3, the profile is read from results of the previous run.
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
				The switch sputter_energy_on turns on the energy contribution from the sputtered particles (physical and chemical).
				If sputter_energy_on.eq.0, the particles are sputtered cold, with no energy contribution to the ion heat equation. If sputter_energy_on.ne.0 (default), the chemically sputtered particles are re-introduced into the plasma with the thermal energy corresponding to the surface temperature of the material, while physically sputtered particles are re-introduced with the TRIM-calculated energy sputtering yield (if the TRIM model is used).
				Therm_evap turns on thermal evaporation when .gt.0.0 and is a multiplier to the thermal evaporation rate.
				Redep_alpha is the multiplier to the reduction of the sputtering yield due to prompt redeposition. The promptly redeposited species is counted as eroded-then-deposited species.
			', """3.0"""),
   
      'b2stbr_sput_dst' : ('Physics', 'integer', '
				Sputtering model switches. See the code in b2stbr and the b2mod_sputter module for specific implementation details and references.
				The default values represent the case of Graphite plates. Sput_src is the atomic number of the plasma species which causes chemical sputtering.
				Sput_dst (when .ge.0) is the species index of the destination species produced by physical sputtering, chemical sputtering and/or RES. If either of the latter two processes are included, the production chemical sputtering and RES rate calculations provided in the code assume that sput_dst points to a Carbon species.
				Sput_dst2 and sput_dst3 (when .ge.0) represent other species produced by wall interactions for mixed materials scenarios.
				Sput_frac_flag is the switch to turn on mixed materials scenarios (when sput_frac_flag.eq.1).
				Plate_model.eq.0 means the 0-D time-independent plate heating model while plate_model.eq.1 indicates the 1-D time-dependent plate heating treatment. Plate_model.eq.2 gives acces to a 2-D time-dependent model.
				Plate_option chooses the initialisation of the plate temperature profile. If plate_option.eq.1, the profile is set to the constant given in plate_temp. If plate_option.eq.2, the profile is computed to be the 0-D equilibrium profile. If plate_option.eq.3, the profile is read from results of the previous run.
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
				The switch sputter_energy_on turns on the energy contribution from the sputtered particles (physical and chemical).
				If sputter_energy_on.eq.0, the particles are sputtered cold, with no energy contribution to the ion heat equation. If sputter_energy_on.ne.0 (default), the chemically sputtered particles are re-introduced into the plasma with the thermal energy corresponding to the surface temperature of the material, while physically sputtered particles are re-introduced with the TRIM-calculated energy sputtering yield (if the TRIM model is used).
				Therm_evap turns on thermal evaporation when .gt.0.0 and is a multiplier to the thermal evaporation rate.
				Redep_alpha is the multiplier to the reduction of the sputtering yield due to prompt redeposition. The promptly redeposited species is counted as eroded-then-deposited species.
			', """-1"""),
   
      'b2stbr_sput_dst2' : ('Physics', 'integer', '
				Sputtering model switches. See the code in b2stbr and the b2mod_sputter module for specific implementation details and references.
				The default values represent the case of Graphite plates. Sput_src is the atomic number of the plasma species which causes chemical sputtering.
				Sput_dst (when .ge.0) is the species index of the destination species produced by physical sputtering, chemical sputtering and/or RES. If either of the latter two processes are included, the production chemical sputtering and RES rate calculations provided in the code assume that sput_dst points to a Carbon species.
				Sput_dst2 and sput_dst3 (when .ge.0) represent other species produced by wall interactions for mixed materials scenarios.
				Sput_frac_flag is the switch to turn on mixed materials scenarios (when sput_frac_flag.eq.1).
				Plate_model.eq.0 means the 0-D time-independent plate heating model while plate_model.eq.1 indicates the 1-D time-dependent plate heating treatment. Plate_model.eq.2 gives acces to a 2-D time-dependent model.
				Plate_option chooses the initialisation of the plate temperature profile. If plate_option.eq.1, the profile is set to the constant given in plate_temp. If plate_option.eq.2, the profile is computed to be the 0-D equilibrium profile. If plate_option.eq.3, the profile is read from results of the previous run.
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
				The switch sputter_energy_on turns on the energy contribution from the sputtered particles (physical and chemical).
				If sputter_energy_on.eq.0, the particles are sputtered cold, with no energy contribution to the ion heat equation. If sputter_energy_on.ne.0 (default), the chemically sputtered particles are re-introduced into the plasma with the thermal energy corresponding to the surface temperature of the material, while physically sputtered particles are re-introduced with the TRIM-calculated energy sputtering yield (if the TRIM model is used).
				Therm_evap turns on thermal evaporation when .gt.0.0 and is a multiplier to the thermal evaporation rate.
				Redep_alpha is the multiplier to the reduction of the sputtering yield due to prompt redeposition. The promptly redeposited species is counted as eroded-then-deposited species.
			', """-1"""),
   
      'b2stbr_sput_dst3' : ('Physics', 'integer', '
				Sputtering model switches. See the code in b2stbr and the b2mod_sputter module for specific implementation details and references.
				The default values represent the case of Graphite plates. Sput_src is the atomic number of the plasma species which causes chemical sputtering.
				Sput_dst (when .ge.0) is the species index of the destination species produced by physical sputtering, chemical sputtering and/or RES. If either of the latter two processes are included, the production chemical sputtering and RES rate calculations provided in the code assume that sput_dst points to a Carbon species.
				Sput_dst2 and sput_dst3 (when .ge.0) represent other species produced by wall interactions for mixed materials scenarios.
				Sput_frac_flag is the switch to turn on mixed materials scenarios (when sput_frac_flag.eq.1).
				Plate_model.eq.0 means the 0-D time-independent plate heating model while plate_model.eq.1 indicates the 1-D time-dependent plate heating treatment. Plate_model.eq.2 gives acces to a 2-D time-dependent model.
				Plate_option chooses the initialisation of the plate temperature profile. If plate_option.eq.1, the profile is set to the constant given in plate_temp. If plate_option.eq.2, the profile is computed to be the 0-D equilibrium profile. If plate_option.eq.3, the profile is read from results of the previous run.
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
				The switch sputter_energy_on turns on the energy contribution from the sputtered particles (physical and chemical).
				If sputter_energy_on.eq.0, the particles are sputtered cold, with no energy contribution to the ion heat equation. If sputter_energy_on.ne.0 (default), the chemically sputtered particles are re-introduced into the plasma with the thermal energy corresponding to the surface temperature of the material, while physically sputtered particles are re-introduced with the TRIM-calculated energy sputtering yield (if the TRIM model is used).
				Therm_evap turns on thermal evaporation when .gt.0.0 and is a multiplier to the thermal evaporation rate.
				Redep_alpha is the multiplier to the reduction of the sputtering yield due to prompt redeposition. The promptly redeposited species is counted as eroded-then-deposited species.
			', """-1"""),
   
      'b2stbr_sput_frc' : ('Physics', 'real', '
				Sputtering model switches. See the code in b2stbr and the b2mod_sputter module for specific implementation details and references.
				The default values represent the case of Graphite plates. Sput_src is the atomic number of the plasma species which causes chemical sputtering.
				Sput_dst (when .ge.0) is the species index of the destination species produced by physical sputtering, chemical sputtering and/or RES. If either of the latter two processes are included, the production chemical sputtering and RES rate calculations provided in the code assume that sput_dst points to a Carbon species.
				Sput_dst2 and sput_dst3 (when .ge.0) represent other species produced by wall interactions for mixed materials scenarios.
				Sput_frac_flag is the switch to turn on mixed materials scenarios (when sput_frac_flag.eq.1).
				Plate_model.eq.0 means the 0-D time-independent plate heating model while plate_model.eq.1 indicates the 1-D time-dependent plate heating treatment. Plate_model.eq.2 gives acces to a 2-D time-dependent model.
				Plate_option chooses the initialisation of the plate temperature profile. If plate_option.eq.1, the profile is set to the constant given in plate_temp. If plate_option.eq.2, the profile is computed to be the 0-D equilibrium profile. If plate_option.eq.3, the profile is read from results of the previous run.
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
				The switch sputter_energy_on turns on the energy contribution from the sputtered particles (physical and chemical).
				If sputter_energy_on.eq.0, the particles are sputtered cold, with no energy contribution to the ion heat equation. If sputter_energy_on.ne.0 (default), the chemically sputtered particles are re-introduced into the plasma with the thermal energy corresponding to the surface temperature of the material, while physically sputtered particles are re-introduced with the TRIM-calculated energy sputtering yield (if the TRIM model is used).
				Therm_evap turns on thermal evaporation when .gt.0.0 and is a multiplier to the thermal evaporation rate.
				Redep_alpha is the multiplier to the reduction of the sputtering yield due to prompt redeposition. The promptly redeposited species is counted as eroded-then-deposited species.
			', """0.0"""),
   
      'b2stbr_sput_mixed_alpha' : ('Physics', 'real', '
				Sputtering model switches. See the code in b2stbr and the b2mod_sputter module for specific implementation details and references.
				The default values represent the case of Graphite plates. Sput_src is the atomic number of the plasma species which causes chemical sputtering.
				Sput_dst (when .ge.0) is the species index of the destination species produced by physical sputtering, chemical sputtering and/or RES. If either of the latter two processes are included, the production chemical sputtering and RES rate calculations provided in the code assume that sput_dst points to a Carbon species.
				Sput_dst2 and sput_dst3 (when .ge.0) represent other species produced by wall interactions for mixed materials scenarios.
				Sput_frac_flag is the switch to turn on mixed materials scenarios (when sput_frac_flag.eq.1).
				Plate_model.eq.0 means the 0-D time-independent plate heating model while plate_model.eq.1 indicates the 1-D time-dependent plate heating treatment. Plate_model.eq.2 gives acces to a 2-D time-dependent model.
				Plate_option chooses the initialisation of the plate temperature profile. If plate_option.eq.1, the profile is set to the constant given in plate_temp. If plate_option.eq.2, the profile is computed to be the 0-D equilibrium profile. If plate_option.eq.3, the profile is read from results of the previous run.
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
				The switch sputter_energy_on turns on the energy contribution from the sputtered particles (physical and chemical).
				If sputter_energy_on.eq.0, the particles are sputtered cold, with no energy contribution to the ion heat equation. If sputter_energy_on.ne.0 (default), the chemically sputtered particles are re-introduced into the plasma with the thermal energy corresponding to the surface temperature of the material, while physically sputtered particles are re-introduced with the TRIM-calculated energy sputtering yield (if the TRIM model is used).
				Therm_evap turns on thermal evaporation when .gt.0.0 and is a multiplier to the thermal evaporation rate.
				Redep_alpha is the multiplier to the reduction of the sputtering yield due to prompt redeposition. The promptly redeposited species is counted as eroded-then-deposited species.
			', """1.0"""),
   
      'b2stbr_sput_mixed_beta' : ('Physics', 'real', '
				Sputtering model switches. See the code in b2stbr and the b2mod_sputter module for specific implementation details and references.
				The default values represent the case of Graphite plates. Sput_src is the atomic number of the plasma species which causes chemical sputtering.
				Sput_dst (when .ge.0) is the species index of the destination species produced by physical sputtering, chemical sputtering and/or RES. If either of the latter two processes are included, the production chemical sputtering and RES rate calculations provided in the code assume that sput_dst points to a Carbon species.
				Sput_dst2 and sput_dst3 (when .ge.0) represent other species produced by wall interactions for mixed materials scenarios.
				Sput_frac_flag is the switch to turn on mixed materials scenarios (when sput_frac_flag.eq.1).
				Plate_model.eq.0 means the 0-D time-independent plate heating model while plate_model.eq.1 indicates the 1-D time-dependent plate heating treatment. Plate_model.eq.2 gives acces to a 2-D time-dependent model.
				Plate_option chooses the initialisation of the plate temperature profile. If plate_option.eq.1, the profile is set to the constant given in plate_temp. If plate_option.eq.2, the profile is computed to be the 0-D equilibrium profile. If plate_option.eq.3, the profile is read from results of the previous run.
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
				The switch sputter_energy_on turns on the energy contribution from the sputtered particles (physical and chemical).
				If sputter_energy_on.eq.0, the particles are sputtered cold, with no energy contribution to the ion heat equation. If sputter_energy_on.ne.0 (default), the chemically sputtered particles are re-introduced into the plasma with the thermal energy corresponding to the surface temperature of the material, while physically sputtered particles are re-introduced with the TRIM-calculated energy sputtering yield (if the TRIM model is used).
				Therm_evap turns on thermal evaporation when .gt.0.0 and is a multiplier to the thermal evaporation rate.
				Redep_alpha is the multiplier to the reduction of the sputtering yield due to prompt redeposition. The promptly redeposited species is counted as eroded-then-deposited species.
			', """1.0"""),
   
      'b2stbr_sput_phys' : ('Physics', 'real', '
				Sputtering model switches. See the code in b2stbr and the b2mod_sputter module for specific implementation details and references.
				The default values represent the case of Graphite plates. Sput_src is the atomic number of the plasma species which causes chemical sputtering.
				Sput_dst (when .ge.0) is the species index of the destination species produced by physical sputtering, chemical sputtering and/or RES. If either of the latter two processes are included, the production chemical sputtering and RES rate calculations provided in the code assume that sput_dst points to a Carbon species.
				Sput_dst2 and sput_dst3 (when .ge.0) represent other species produced by wall interactions for mixed materials scenarios.
				Sput_frac_flag is the switch to turn on mixed materials scenarios (when sput_frac_flag.eq.1).
				Plate_model.eq.0 means the 0-D time-independent plate heating model while plate_model.eq.1 indicates the 1-D time-dependent plate heating treatment. Plate_model.eq.2 gives acces to a 2-D time-dependent model.
				Plate_option chooses the initialisation of the plate temperature profile. If plate_option.eq.1, the profile is set to the constant given in plate_temp. If plate_option.eq.2, the profile is computed to be the 0-D equilibrium profile. If plate_option.eq.3, the profile is read from results of the previous run.
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
				The switch sputter_energy_on turns on the energy contribution from the sputtered particles (physical and chemical).
				If sputter_energy_on.eq.0, the particles are sputtered cold, with no energy contribution to the ion heat equation. If sputter_energy_on.ne.0 (default), the chemically sputtered particles are re-introduced into the plasma with the thermal energy corresponding to the surface temperature of the material, while physically sputtered particles are re-introduced with the TRIM-calculated energy sputtering yield (if the TRIM model is used).
				Therm_evap turns on thermal evaporation when .gt.0.0 and is a multiplier to the thermal evaporation rate.
				Redep_alpha is the multiplier to the reduction of the sputtering yield due to prompt redeposition. The promptly redeposited species is counted as eroded-then-deposited species.
			', """0.0"""),
   
      'b2stbr_sput_phys_col' : ('Physics', 'integer', '
				Sputtering model switches. See the code in b2stbr and the b2mod_sputter module for specific implementation details and references.
				The default values represent the case of Graphite plates. Sput_src is the atomic number of the plasma species which causes chemical sputtering.
				Sput_dst (when .ge.0) is the species index of the destination species produced by physical sputtering, chemical sputtering and/or RES. If either of the latter two processes are included, the production chemical sputtering and RES rate calculations provided in the code assume that sput_dst points to a Carbon species.
				Sput_dst2 and sput_dst3 (when .ge.0) represent other species produced by wall interactions for mixed materials scenarios.
				Sput_frac_flag is the switch to turn on mixed materials scenarios (when sput_frac_flag.eq.1).
				Plate_model.eq.0 means the 0-D time-independent plate heating model while plate_model.eq.1 indicates the 1-D time-dependent plate heating treatment. Plate_model.eq.2 gives acces to a 2-D time-dependent model.
				Plate_option chooses the initialisation of the plate temperature profile. If plate_option.eq.1, the profile is set to the constant given in plate_temp. If plate_option.eq.2, the profile is computed to be the 0-D equilibrium profile. If plate_option.eq.3, the profile is read from results of the previous run.
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
				The switch sputter_energy_on turns on the energy contribution from the sputtered particles (physical and chemical).
				If sputter_energy_on.eq.0, the particles are sputtered cold, with no energy contribution to the ion heat equation. If sputter_energy_on.ne.0 (default), the chemically sputtered particles are re-introduced into the plasma with the thermal energy corresponding to the surface temperature of the material, while physically sputtered particles are re-introduced with the TRIM-calculated energy sputtering yield (if the TRIM model is used).
				Therm_evap turns on thermal evaporation when .gt.0.0 and is a multiplier to the thermal evaporation rate.
				Redep_alpha is the multiplier to the reduction of the sputtering yield due to prompt redeposition. The promptly redeposited species is counted as eroded-then-deposited species.
			', """3"""),
   
      'b2stbr_sput_phys_model' : ('Physics', 'integer', '
				Sputtering model switches. See the code in b2stbr and the b2mod_sputter module for specific implementation details and references.
				The default values represent the case of Graphite plates. Sput_src is the atomic number of the plasma species which causes chemical sputtering.
				Sput_dst (when .ge.0) is the species index of the destination species produced by physical sputtering, chemical sputtering and/or RES. If either of the latter two processes are included, the production chemical sputtering and RES rate calculations provided in the code assume that sput_dst points to a Carbon species.
				Sput_dst2 and sput_dst3 (when .ge.0) represent other species produced by wall interactions for mixed materials scenarios.
				Sput_frac_flag is the switch to turn on mixed materials scenarios (when sput_frac_flag.eq.1).
				Plate_model.eq.0 means the 0-D time-independent plate heating model while plate_model.eq.1 indicates the 1-D time-dependent plate heating treatment. Plate_model.eq.2 gives acces to a 2-D time-dependent model.
				Plate_option chooses the initialisation of the plate temperature profile. If plate_option.eq.1, the profile is set to the constant given in plate_temp. If plate_option.eq.2, the profile is computed to be the 0-D equilibrium profile. If plate_option.eq.3, the profile is read from results of the previous run.
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
				The switch sputter_energy_on turns on the energy contribution from the sputtered particles (physical and chemical).
				If sputter_energy_on.eq.0, the particles are sputtered cold, with no energy contribution to the ion heat equation. If sputter_energy_on.ne.0 (default), the chemically sputtered particles are re-introduced into the plasma with the thermal energy corresponding to the surface temperature of the material, while physically sputtered particles are re-introduced with the TRIM-calculated energy sputtering yield (if the TRIM model is used).
				Therm_evap turns on thermal evaporation when .gt.0.0 and is a multiplier to the thermal evaporation rate.
				Redep_alpha is the multiplier to the reduction of the sputtering yield due to prompt redeposition. The promptly redeposited species is counted as eroded-then-deposited species.
			', """1"""),
   
      'b2stbr_sput_res' : ('Physics', 'real', '
				Sputtering model switches. See the code in b2stbr and the b2mod_sputter module for specific implementation details and references.
				The default values represent the case of Graphite plates. Sput_src is the atomic number of the plasma species which causes chemical sputtering.
				Sput_dst (when .ge.0) is the species index of the destination species produced by physical sputtering, chemical sputtering and/or RES. If either of the latter two processes are included, the production chemical sputtering and RES rate calculations provided in the code assume that sput_dst points to a Carbon species.
				Sput_dst2 and sput_dst3 (when .ge.0) represent other species produced by wall interactions for mixed materials scenarios.
				Sput_frac_flag is the switch to turn on mixed materials scenarios (when sput_frac_flag.eq.1).
				Plate_model.eq.0 means the 0-D time-independent plate heating model while plate_model.eq.1 indicates the 1-D time-dependent plate heating treatment. Plate_model.eq.2 gives acces to a 2-D time-dependent model.
				Plate_option chooses the initialisation of the plate temperature profile. If plate_option.eq.1, the profile is set to the constant given in plate_temp. If plate_option.eq.2, the profile is computed to be the 0-D equilibrium profile. If plate_option.eq.3, the profile is read from results of the previous run.
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
				The switch sputter_energy_on turns on the energy contribution from the sputtered particles (physical and chemical).
				If sputter_energy_on.eq.0, the particles are sputtered cold, with no energy contribution to the ion heat equation. If sputter_energy_on.ne.0 (default), the chemically sputtered particles are re-introduced into the plasma with the thermal energy corresponding to the surface temperature of the material, while physically sputtered particles are re-introduced with the TRIM-calculated energy sputtering yield (if the TRIM model is used).
				Therm_evap turns on thermal evaporation when .gt.0.0 and is a multiplier to the thermal evaporation rate.
				Redep_alpha is the multiplier to the reduction of the sputtering yield due to prompt redeposition. The promptly redeposited species is counted as eroded-then-deposited species.
			', """0.0"""),
   
      'b2stbr_sput_src' : ('Physics', 'integer', '
				Sputtering model switches. See the code in b2stbr and the b2mod_sputter module for specific implementation details and references.
				The default values represent the case of Graphite plates. Sput_src is the atomic number of the plasma species which causes chemical sputtering.
				Sput_dst (when .ge.0) is the species index of the destination species produced by physical sputtering, chemical sputtering and/or RES. If either of the latter two processes are included, the production chemical sputtering and RES rate calculations provided in the code assume that sput_dst points to a Carbon species.
				Sput_dst2 and sput_dst3 (when .ge.0) represent other species produced by wall interactions for mixed materials scenarios.
				Sput_frac_flag is the switch to turn on mixed materials scenarios (when sput_frac_flag.eq.1).
				Plate_model.eq.0 means the 0-D time-independent plate heating model while plate_model.eq.1 indicates the 1-D time-dependent plate heating treatment. Plate_model.eq.2 gives acces to a 2-D time-dependent model.
				Plate_option chooses the initialisation of the plate temperature profile. If plate_option.eq.1, the profile is set to the constant given in plate_temp. If plate_option.eq.2, the profile is computed to be the 0-D equilibrium profile. If plate_option.eq.3, the profile is read from results of the previous run.
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
				The switch sputter_energy_on turns on the energy contribution from the sputtered particles (physical and chemical).
				If sputter_energy_on.eq.0, the particles are sputtered cold, with no energy contribution to the ion heat equation. If sputter_energy_on.ne.0 (default), the chemically sputtered particles are re-introduced into the plasma with the thermal energy corresponding to the surface temperature of the material, while physically sputtered particles are re-introduced with the TRIM-calculated energy sputtering yield (if the TRIM model is used).
				Therm_evap turns on thermal evaporation when .gt.0.0 and is a multiplier to the thermal evaporation rate.
				Redep_alpha is the multiplier to the reduction of the sputtering yield due to prompt redeposition. The promptly redeposited species is counted as eroded-then-deposited species.
			', """1"""),
   
      'b2stbr_sputter_energy_on' : ('Physics', 'integer', '
				Sputtering model switches. See the code in b2stbr and the b2mod_sputter module for specific implementation details and references.
				The default values represent the case of Graphite plates. Sput_src is the atomic number of the plasma species which causes chemical sputtering.
				Sput_dst (when .ge.0) is the species index of the destination species produced by physical sputtering, chemical sputtering and/or RES. If either of the latter two processes are included, the production chemical sputtering and RES rate calculations provided in the code assume that sput_dst points to a Carbon species.
				Sput_dst2 and sput_dst3 (when .ge.0) represent other species produced by wall interactions for mixed materials scenarios.
				Sput_frac_flag is the switch to turn on mixed materials scenarios (when sput_frac_flag.eq.1).
				Plate_model.eq.0 means the 0-D time-independent plate heating model while plate_model.eq.1 indicates the 1-D time-dependent plate heating treatment. Plate_model.eq.2 gives acces to a 2-D time-dependent model.
				Plate_option chooses the initialisation of the plate temperature profile. If plate_option.eq.1, the profile is set to the constant given in plate_temp. If plate_option.eq.2, the profile is computed to be the 0-D equilibrium profile. If plate_option.eq.3, the profile is read from results of the previous run.
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
				The switch sputter_energy_on turns on the energy contribution from the sputtered particles (physical and chemical).
				If sputter_energy_on.eq.0, the particles are sputtered cold, with no energy contribution to the ion heat equation. If sputter_energy_on.ne.0 (default), the chemically sputtered particles are re-introduced into the plasma with the thermal energy corresponding to the surface temperature of the material, while physically sputtered particles are re-introduced with the TRIM-calculated energy sputtering yield (if the TRIM model is used).
				Therm_evap turns on thermal evaporation when .gt.0.0 and is a multiplier to the thermal evaporation rate.
				Redep_alpha is the multiplier to the reduction of the sputtering yield due to prompt redeposition. The promptly redeposited species is counted as eroded-then-deposited species.
			', """1"""),
   
      'b2stbr_therm_evap' : ('Physics', 'real', '
				Sputtering model switches. See the code in b2stbr and the b2mod_sputter module for specific implementation details and references.
				The default values represent the case of Graphite plates. Sput_src is the atomic number of the plasma species which causes chemical sputtering.
				Sput_dst (when .ge.0) is the species index of the destination species produced by physical sputtering, chemical sputtering and/or RES. If either of the latter two processes are included, the production chemical sputtering and RES rate calculations provided in the code assume that sput_dst points to a Carbon species.
				Sput_dst2 and sput_dst3 (when .ge.0) represent other species produced by wall interactions for mixed materials scenarios.
				Sput_frac_flag is the switch to turn on mixed materials scenarios (when sput_frac_flag.eq.1).
				Plate_model.eq.0 means the 0-D time-independent plate heating model while plate_model.eq.1 indicates the 1-D time-dependent plate heating treatment. Plate_model.eq.2 gives acces to a 2-D time-dependent model.
				Plate_option chooses the initialisation of the plate temperature profile. If plate_option.eq.1, the profile is set to the constant given in plate_temp. If plate_option.eq.2, the profile is computed to be the 0-D equilibrium profile. If plate_option.eq.3, the profile is read from results of the previous run.
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
				The switch sputter_energy_on turns on the energy contribution from the sputtered particles (physical and chemical).
				If sputter_energy_on.eq.0, the particles are sputtered cold, with no energy contribution to the ion heat equation. If sputter_energy_on.ne.0 (default), the chemically sputtered particles are re-introduced into the plasma with the thermal energy corresponding to the surface temperature of the material, while physically sputtered particles are re-introduced with the TRIM-calculated energy sputtering yield (if the TRIM model is used).
				Therm_evap turns on thermal evaporation when .gt.0.0 and is a multiplier to the thermal evaporation rate.
				Redep_alpha is the multiplier to the reduction of the sputtering yield due to prompt redeposition. The promptly redeposited species is counted as eroded-then-deposited species.
			', """0.0"""),
   
      'b2stbr_sput_frac_flag' : ('Physics', 'integer', '
				Sputtering model switches. See the code in b2stbr and the b2mod_sputter module for specific implementation details and references.
				The default values represent the case of Graphite plates. Sput_src is the atomic number of the plasma species which causes chemical sputtering.
				Sput_dst (when .ge.0) is the species index of the destination species produced by physical sputtering, chemical sputtering and/or RES. If either of the latter two processes are included, the production chemical sputtering and RES rate calculations provided in the code assume that sput_dst points to a Carbon species.
				Sput_dst2 and sput_dst3 (when .ge.0) represent other species produced by wall interactions for mixed materials scenarios.
				Sput_frac_flag is the switch to turn on mixed materials scenarios (when sput_frac_flag.eq.1).
				Plate_model.eq.0 means the 0-D time-independent plate heating model while plate_model.eq.1 indicates the 1-D time-dependent plate heating treatment. Plate_model.eq.2 gives acces to a 2-D time-dependent model.
				Plate_option chooses the initialisation of the plate temperature profile. If plate_option.eq.1, the profile is set to the constant given in plate_temp. If plate_option.eq.2, the profile is computed to be the 0-D equilibrium profile. If plate_option.eq.3, the profile is read from results of the previous run.
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
				The switch sputter_energy_on turns on the energy contribution from the sputtered particles (physical and chemical).
				If sputter_energy_on.eq.0, the particles are sputtered cold, with no energy contribution to the ion heat equation. If sputter_energy_on.ne.0 (default), the chemically sputtered particles are re-introduced into the plasma with the thermal energy corresponding to the surface temperature of the material, while physically sputtered particles are re-introduced with the TRIM-calculated energy sputtering yield (if the TRIM model is used).
				Therm_evap turns on thermal evaporation when .gt.0.0 and is a multiplier to the thermal evaporation rate.
				Redep_alpha is the multiplier to the reduction of the sputtering yield due to prompt redeposition. The promptly redeposited species is counted as eroded-then-deposited species.
			', """0"""),
   
      'b2stbr_b2wall_netcdf' : ('Output', 'integer', '
				If tallies_netcdf.ne.0, the file 'b2tallies.nc' is created, which contains the regional tallies in CDF format.
				If b2wall_netcdf.ne.0, the file 'b2wall.nc' is created, which contains the wall tallies in CDF format [written every b2wall_netcdf "main calls"].
			', """0"""),
   
      'tallies_netcdf' : ('Output', 'integer', '
				If tallies_netcdf.ne.0, the file 'b2tallies.nc' is created, which contains the regional tallies in CDF format.
				If b2wall_netcdf.ne.0, the file 'b2wall.nc' is created, which contains the wall tallies in CDF format [written every b2wall_netcdf "main calls"].
			', """0"""),
   
      'b2stbr_refl_model' : ('Physics', 'integer', '
				Reflection model switches. If the recycling coefficients (particle and energy) are set to zero, then the code attempts to use, for surfaces in contact with walls, the TRIM reflection data for particle and energy reflection coefficients, when refl_model.eq.1. If refl_model.eq.0, an empirical formula is used instead. The model switch is subservient to reflection_on.ne.0. If reflection_on.eq.0, then no reflection is used.
				If reflection_on.eq.1 (default), then the incident species is reflected unchanged. Otherwise, the reflected flux is of the associated neutral species to the incident particles.
			', """1"""),
   
      'b2stbr_reflection_on' : ('Physics', 'integer', '
				Reflection model switches. If the recycling coefficients (particle and energy) are set to zero, then the code attempts to use, for surfaces in contact with walls, the TRIM reflection data for particle and energy reflection coefficients, when refl_model.eq.1. If refl_model.eq.0, an empirical formula is used instead. The model switch is subservient to reflection_on.ne.0. If reflection_on.eq.0, then no reflection is used.
				If reflection_on.eq.1 (default), then the incident species is reflected unchanged. Otherwise, the reflected flux is of the associated neutral species to the incident particles.
			', """1"""),
   
      'b2stel_rg0' : ('Numerics', 'real', '
				Damping coefficient applied to the atomic physics sources.
			', """1.0"""),
   
      'b2stel_rg1' : ('Numerics', 'real', '
				Damping coefficient applied to the atomic physics sources.
			', """1.0"""),
   
      'b2stel_rxm0' : ('Numerics', 'real', '
				Damping coefficient applied to the atomic physics sources.
			', """0.0"""),
   
      'b2stel_rxm1' : ('Numerics', 'real', '
				Damping coefficient applied to the atomic physics sources.
			', """0.0"""),
   
      'b2stel_rxm2' : ('Numerics', 'real', '
				Damping coefficient applied to the atomic physics sources.
			', """0.0"""),
   
      'b2stel_rxm3' : ('Numerics', 'real', '
				Damping coefficient applied to the atomic physics sources.
			', """0.0"""),
   
      'b2stel_rxm4' : ('Numerics', 'real', '
				Damping coefficient applied to the atomic physics sources.
			', """0.0"""),
   
      'b2tanml_anomalous' : ('Physics', 'real', '
				Real parameter which determines anomalous current.
				Both b2tfhe_anomalous and b2tanml_anomalous point to the same switch (backward compatibility with SOLPS5.2): b2tfhe_anomalous is checked first and only if it is not found is b2tanml_anomalous looked for.
				If b2tfhe_anomalous is 0 then anomalous current is switched off otherwise anomalous current is switched on, and the numerical value of b2tfhe_anomalous acts as a multiplier to the anomalous electrical conductivity and thermo-electric coefficients provided.
			', """1.0"""),
   
      'b2tfhe_anomalous' : ('Physics', 'real', '
				Real parameter which determines anomalous current.
				Both b2tfhe_anomalous and b2tanml_anomalous point to the same switch (backward compatibility with SOLPS5.2): b2tfhe_anomalous is checked first and only if it is not found is b2tanml_anomalous looked for.
				If b2tfhe_anomalous is 0 then anomalous current is switched off otherwise anomalous current is switched on, and the numerical value of b2tfhe_anomalous acts as a multiplier to the anomalous electrical conductivity and thermo-electric coefficients provided.
			', """1.0"""),
   
      'b2tfhe_hybr2' : ('Numerics', 'integer', '
				Switches to toggle between the standard 5.0 hybrid scheme (no_hybr.eq.0) and the old 4.0 upwind scheme (no_hybr.eq.1).
				These apply separately to the electron heat, ion heat and particle conservation equations.
				If hybr2.ne.0, then a mixed scheme is used where only the conductivity is computed according to the 4.0 scheme.
			', """0"""),
   
      'b2tfhe_no_hybr' : ('Numerics', 'integer', '
				Switches to toggle between the standard 5.0 hybrid scheme (no_hybr.eq.0) and the old 4.0 upwind scheme (no_hybr.eq.1).
				These apply separately to the electron heat, ion heat and particle conservation equations.
				If hybr2.ne.0, then a mixed scheme is used where only the conductivity is computed according to the 4.0 scheme.
			', """0"""),
   
      'b2tfhi_hybr2' : ('Numerics', 'integer', '
				Switches to toggle between the standard 5.0 hybrid scheme (no_hybr.eq.0) and the old 4.0 upwind scheme (no_hybr.eq.1).
				These apply separately to the electron heat, ion heat and particle conservation equations.
				If hybr2.ne.0, then a mixed scheme is used where only the conductivity is computed according to the 4.0 scheme.
			', """0"""),
   
      'b2tfhi_no_hybr' : ('Numerics', 'integer', '
				Switches to toggle between the standard 5.0 hybrid scheme (no_hybr.eq.0) and the old 4.0 upwind scheme (no_hybr.eq.1).
				These apply separately to the electron heat, ion heat and particle conservation equations.
				If hybr2.ne.0, then a mixed scheme is used where only the conductivity is computed according to the 4.0 scheme.
			', """0"""),
   
      'b2tfnb_no_hybr' : ('Numerics', 'integer', '
				Switches to toggle between the standard 5.0 hybrid scheme (no_hybr.eq.0) and the old 4.0 upwind scheme (no_hybr.eq.1).
				These apply separately to the electron heat, ion heat and particle conservation equations.
				If hybr2.ne.0, then a mixed scheme is used where only the conductivity is computed according to the 4.0 scheme.
			', """0"""),
   
      'b2tfhe_upwind' : ('Numerics', 'real', '
				If upwind.ne.0, then the SOLPS4 upwind scheme in b2tfhe_ and b2tfhi_ to obtain the heat fluxes.
			', """0.0"""),
   
      'b2tfhi_upwind' : ('Numerics', 'real', '
				If upwind.ne.0, then the SOLPS4 upwind scheme in b2tfhe_ and b2tfhi_ to obtain the heat fluxes.
			', """0.0"""),
   
      'b2tfnb_alpha' : ('Physics', 'real', '
				Parameters for the flux limit to the convective neutral flow.
				Alpha is a multiplier to the classical flux limit value.
				The larger alpha is, the weaker the flux limit is.
				Gamma is the exponent used in the flux-limiting formula.
				The smaller gamma is, the stronger the flux limit is.
				If alpha.eq.0, no flux limit is applied.
				flux_limit_min_ti specifies the minimum ti to be used (in eV).
			', """0.0"""),
   
      'b2tfnb_gamma' : ('Physics', 'real', '
				Parameters for the flux limit to the convective neutral flow.
				Alpha is a multiplier to the classical flux limit value.
				The larger alpha is, the weaker the flux limit is.
				Gamma is the exponent used in the flux-limiting formula.
				The smaller gamma is, the stronger the flux limit is.
				If alpha.eq.0, no flux limit is applied.
				flux_limit_min_ti specifies the minimum ti to be used (in eV).
			', """2.0"""),
   
      'b2tfnb_flux_limit_min_ti' : ('Physics', 'real', '
				Parameters for the flux limit to the convective neutral flow.
				Alpha is a multiplier to the classical flux limit value.
				The larger alpha is, the weaker the flux limit is.
				Gamma is the exponent used in the flux-limiting formula.
				The smaller gamma is, the stronger the flux limit is.
				If alpha.eq.0, no flux limit is applied.
				flux_limit_min_ti specifies the minimum ti to be used (in eV).
			', """0.0"""),
   
      'b2tlc0_alpha' : ('Physics', 'real', '
				Parameters for the flux limit to dpa0 - pressure driven neutral diffusion.
				Alpha is a multiplier to the classical flux limit value.
				Gamma is the exponent used in the flux-limiting formula.
				If alpha.eq.0, no flux limit is applied.
			', """0.0"""),
   
      'b2tlc0_gamma' : ('Physics', 'real', '
				Parameters for the flux limit to dpa0 - pressure driven neutral diffusion.
				Alpha is a multiplier to the classical flux limit value.
				Gamma is the exponent used in the flux-limiting formula.
				If alpha.eq.0, no flux limit is applied.
			', """2.0"""),
   
      'b2tlh0_alpha' : ('Physics', 'real', '
				Parameters for the flux limit to the heat conductivity of the neutrals. Alpha is a multiplier to the classical flux limit value.
				The larger alpha is, the weaker the flux limit is.
				Gamma is the exponent used in the flux-limiting formula.
				The smaller gamma is, the stronger the flux limit is.
				If alpha.eq.0, no flux limit is applied.
				flux_limit_min_ti specifies the minimum ti to be used (in eV).
			', """0.0"""),
   
      'b2tlh0_gamma' : ('Physics', 'real', '
				Parameters for the flux limit to the heat conductivity of the neutrals. Alpha is a multiplier to the classical flux limit value.
				The larger alpha is, the weaker the flux limit is.
				Gamma is the exponent used in the flux-limiting formula.
				The smaller gamma is, the stronger the flux limit is.
				If alpha.eq.0, no flux limit is applied.
				flux_limit_min_ti specifies the minimum ti to be used (in eV).
			', """2.0"""),
   
      'b2tlh0_flux_limit_min_ti' : ('Physics', 'real', '
				Parameters for the flux limit to the heat conductivity of the neutrals. Alpha is a multiplier to the classical flux limit value.
				The larger alpha is, the weaker the flux limit is.
				Gamma is the exponent used in the flux-limiting formula.
				The smaller gamma is, the stronger the flux limit is.
				If alpha.eq.0, no flux limit is applied.
				flux_limit_min_ti specifies the minimum ti to be used (in eV).
			', """0.0"""),
   
      'b2tlnl_ee' : ('Physics', 'integer', '
				If lambda is positive, the Coulomb logarithm is set to lambda.
				If lambda is negative, then abs(lambda) is the lower bound to be used when computing the Coulomb logarithm according to the NRL formulae.
				The computation of the Coulomb logarithm takes place in b2tlnl.
				The default formula is to use the Braginskii formulation, which will give the same answer for electron-electron (ee), electron-ion (ei), and ion-ion (ii) collisions. Respectively, non-default values of '1', '2' and '3' for b2tlnl_ee, _ei, and _ii, respectively, make use of the calculation according to Wesson.
			', """0"""),
   
      'b2tlnl_ei' : ('Physics', 'integer', '
				If lambda is positive, the Coulomb logarithm is set to lambda.
				If lambda is negative, then abs(lambda) is the lower bound to be used when computing the Coulomb logarithm according to the NRL formulae.
				The computation of the Coulomb logarithm takes place in b2tlnl.
				The default formula is to use the Braginskii formulation, which will give the same answer for electron-electron (ee), electron-ion (ei), and ion-ion (ii) collisions. Respectively, non-default values of '1', '2' and '3' for b2tlnl_ee, _ei, and _ii, respectively, make use of the calculation according to Wesson.
			', """0"""),
   
      'b2tlnl_ii' : ('Physics', 'integer', '
				If lambda is positive, the Coulomb logarithm is set to lambda.
				If lambda is negative, then abs(lambda) is the lower bound to be used when computing the Coulomb logarithm according to the NRL formulae.
				The computation of the Coulomb logarithm takes place in b2tlnl.
				The default formula is to use the Braginskii formulation, which will give the same answer for electron-electron (ee), electron-ion (ei), and ion-ion (ii) collisions. Respectively, non-default values of '1', '2' and '3' for b2tlnl_ee, _ei, and _ii, respectively, make use of the calculation according to Wesson.
			', """0"""),
   
      'b2trcl_lambda' : ('Physics', 'real', '
				If lambda is positive, the Coulomb logarithm is set to lambda.
				If lambda is negative, then abs(lambda) is the lower bound to be used when computing the Coulomb logarithm according to the NRL formulae.
				The computation of the Coulomb logarithm takes place in b2tlnl.
				The default formula is to use the Braginskii formulation, which will give the same answer for electron-electron (ee), electron-ion (ei), and ion-ion (ii) collisions. Respectively, non-default values of '1', '2' and '3' for b2tlnl_ee, _ei, and _ii, respectively, make use of the calculation according to Wesson.
			', """-0.5"""),
   
      'b2tqna_ballooning' : ('Physics', 'real', '
				Ballooning model switches. If ballooning.ne.0, then all transport coefficients in cell (i) are rescaled by a factor of ballooning_rescale*abs(bb_ref/bb(i))**ballooning .
				The default value for bb_ref is the arithmetic average of the total magnetic field strength over the entire computational domain.
			', """0.0"""),
   
      'b2tqna_ballooning_rescale' : ('Physics', 'real', '
				Ballooning model switches. If ballooning.ne.0, then all transport coefficients in cell (i) are rescaled by a factor of ballooning_rescale*abs(bb_ref/bb(i))**ballooning .
				The default value for bb_ref is the arithmetic average of the total magnetic field strength over the entire computational domain.
			', """1.0"""),
   
      'b2tqna_bb_ref' : ('Physics', 'real', '
				Ballooning model switches. If ballooning.ne.0, then all transport coefficients in cell (i) are rescaled by a factor of ballooning_rescale*abs(bb_ref/bb(i))**ballooning .
				The default value for bb_ref is the arithmetic average of the total magnetic field strength over the entire computational domain.
			', """See description"""),
   
      'b2tqna_max_df0' : ('Physics', 'integer', '
				Upper and lower limits of the diffusivity coefficients df0 computed in b2tqna for each species.
			', """1e30"""),
   
      'b2tqna_min_df0' : ('Physics', 'real', '
				Upper and lower limits of the diffusivity coefficients df0 computed in b2tqna for each species.
			', """0.0"""),
   
      'b2tqna_user_transport' : ('Physics', 'integer', '
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
			', """0"""),
   
      'set_transport_eta' : ('Physics', 'real', '
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
			', """2.0"""),
   
      'set_transport_eta_alpha' : ('Physics', 'real', '
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
			', """0.5"""),
   
      'set_transport_eta_floor' : ('Physics', 'real', '
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
			', """0.1"""),
   
      'set_transport_eta_ceiling' : ('Physics', 'real', '
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
			', """10.0"""),
   
      'set_transport_ixref' : ('Physics', 'integer', '
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
			', """See description"""),
   
      'set_transport_iyref' : ('Physics', 'integer', '
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
			', """See description"""),
   
      'set_transport_required_te_gradient' : ('Physics', 'real', '
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
			', """5.0e4"""),
   
      'b2ux5p_mult_solvdim' : ('Numerics', 'integer', '
				Multipliers to the number of non-zero elements in the solution matrix for workspace arrays in the matrix solver.
			', """15"""),
   
      'b2ux5p_mult_solvdim1' : ('Numerics', 'integer', '
				Multipliers to the number of non-zero elements in the solution matrix for workspace arrays in the matrix solver.
			', """10"""),
   
      'eirene_na_max' : ('Numerics', 'integer', '
				Upper and lower bounds used when writing out data for Eirene.
			', """1e30"""),
   
      'eirene_na_min' : ('Numerics', 'real', '
				Upper and lower bounds used when writing out data for Eirene.
			', """0.0"""),
   
      'eirene_te_max' : ('Numerics', 'integer', '
				Upper and lower bounds used when writing out data for Eirene.
			', """1e30"""),
   
      'eirene_te_min' : ('Numerics', 'real', '
				Upper and lower bounds used when writing out data for Eirene.
			', """0.0"""),
   
      'eirene_ti_max' : ('Numerics', 'integer', '
				Upper and lower bounds used when writing out data for Eirene.
			', """1e30"""),
   
      'eirene_ti_min' : ('Numerics', 'real', '
				Upper and lower bounds used when writing out data for Eirene.
			', """0.0"""),
   
      'eirene_ua_max' : ('Numerics', 'real', '
				Upper and lower bounds used when writing out data for Eirene.
			', """+c"""),
   
      'eirene_ua_min' : ('Numerics', 'real', '
				Upper and lower bounds used when writing out data for Eirene.
			', """-c"""),
   
      'eirene_savef30' : ('Output', 'integer', '
				For coupled runs, the code will create two files named fort.30 and fort.31, containing the plasma geometry and plasma state, respectively, for use by Eirene. This happens irrespective of the setting of the two switches above. If however, the user wishes to obtain these files for a non-coupled run, then these two switches can be set to 1 and the files will then be produced at the end of the run. If savef31.lt.0, then a fort.31.###### file is produced after every B2.5 time step. Additionally, if savef31.ne.0, the fort.31 file will be updated before every Eirene call for coupled runs.
			', """0"""),
   
      'eirene_savef31' : ('Output', 'integer', '
				For coupled runs, the code will create two files named fort.30 and fort.31, containing the plasma geometry and plasma state, respectively, for use by Eirene. This happens irrespective of the setting of the two switches above. If however, the user wishes to obtain these files for a non-coupled run, then these two switches can be set to 1 and the files will then be produced at the end of the run. If savef31.lt.0, then a fort.31.###### file is produced after every B2.5 time step. Additionally, if savef31.ne.0, the fort.31 file will be updated before every Eirene call for coupled runs.
			', """0"""),
   
      'heatdiff1D_linlog' : ('Numerics', 'integer', '
				Parameters related to solving the temperature equation for the target plate elements in depth. If linlog.eq.1, a linear subdividing of the plate element is used. If linlog.eq.2, a logarithmic subdividing is used, with the surface layer being ratio times thinner than the last layer in the bulk.
				ratio must be larger than 1.
			', """1"""),
   
      'heatdiff1D_ratio' : ('Numerics', 'real', '
				Parameters related to solving the temperature equation for the target plate elements in depth. If linlog.eq.1, a linear subdividing of the plate element is used. If linlog.eq.2, a logarithmic subdividing is used, with the surface layer being ratio times thinner than the last layer in the bulk.
				ratio must be larger than 1.
			', """100.0"""),
   
      'label' : ('', 'String', 'specifies, on the next line, a label for the run', """None"""),
   
      'ank_tracing' : ('Output', 'integer', '
				If ank_tracing.ge.1, additional tracing output from Andrei Kukushkin is produced, in files to be found in the tracing/ directory inside the run directory. The traces will be written every ank_tracing iteration.	
			', """0"""),
   
      'b2agfs_Bt_adjust' : ('Geometry', 'integer', '
				Bt_adjust - integer.
				If the mesh is offset (See b2agfs_xoffset, b2agfs_yoffset below) and Bt_adjust.eq.1, then the magnetic field is recomputed, keeping the pitch constant but changing the toroidal field magnitude according to Bt = Bt0/R. To be used in b2ag.dat.
			', """0"""),
   
      'b2agfs_Bt_rescale' : ('Geometry', 'real', '
				Bt_rescale - real*8.
				The magnetic field will be multiplied by Bt_rescale. All components of the field are scaled together. To be used in b2ag.dat.
			', """1.0"""),
   
      'b2agfs_Bt_reversal' : ('Geometry', 'integer', '
				Bt_reversal - integer.
				If Bt_reversal.eq.1, then the sign of the toroidal field component only is reversed. The sign convention used is that a positive toroidal field leads to a Bx(grad(B)) direction pointing down, so B is out of the page when looking at the usual view of the poloidal plane with the center line on the left.
				To be used in b2ag.dat.
			', """0"""),
   
      'b2agfs_geom_match_dist' : ('Geometry', 'real', '
				Distance used as the matching criterion when reading the geometry file.
			', """1.0e-6"""),
   
      'b2agfs_geometry' : ('Geometry', 'string', '
				local_sonnet - character string.
				local_sonnet is the file name of the geometry file to be read.
				The file will be looked for in the run directory, in the ../baserun directory and in $SOLPSTOP/data/meshes. To be used in b2ag.dat.
			', """upgrade.geometry"""),
   
      'b2agfs_min_pitch' : ('Geometry', 'real', '
				Minimum allowed value for the pitch angle (in degrees) at the plates.
			', """1.0"""),
   
      'b2agfs_nncut' : ('Geometry', 'integer', '
				Number of topological cuts in geometry. Needed only to force a different value from the one computed automatically by b2ag.
			', """See description (integer)"""),
   
      'b2agfs_periodic_bc' : ('Geometry', 'integer', '
				periodic_bc - integer.
				periodic_bc specifies if this is either an island or limiter geometry.
				If periodic_bc.eq.1 then island/limiter treatment is turned on.
				We differentiate between the two case through nncut:
				 nncut.eq.0 = limiter case
				 nncut.ge.1 = island divertor case (there should be nncut islands then)
				The case periodic_bc.eq.-1 is used to remove tranverse physics in 1-D cases.
				If periodic_bc.eq.0 then we have the usual treatment. No other values are currently allowed. To be used in b2ag.dat.
			', """0"""),
   
      'b2agfs_pit_rescale' : ('Geometry', 'real', '
				pit_rescale - real*8.
				The magnetic field line pitch will be multiplied by pit_rescale.
				This means that the poloidal field component is multiplied by pit_rescale, while the toroidal field component is left unchanged. To reverse the plasma current direction, set pit_rescale to -1.0.
				The sign convention used is that a positive poloidal field points in the direction of increasing <ix>. Be mindful however that, when inverting the sign of the poloidal magnetic field, you are also inverting the direction of the parallel velocity. You will then need to use the 'b2mndr_inverse_ua' switch to correct for that.
				To be used in b2ag.dat.
			', """1.0"""),
   
      'b2agmt_1d_width' : ('Geometry', 'real', '
				For 1-D cases, gives the width of the domain (in m) in the third (toroidal) dimension.
			', """1.0"""),
   
      'b2agmx_pbs_from_basis_mesh' : ('Geometry', 'integer', '
				If pbs_from_basis_mesh.eq.0, the pbs array is computed from values on the actual working mesh (old treatment).
				If pbs_from_basis_mesh.eq.1, the pbs array is computed from values on the (possibly) finer basis mesh from the geometry file and the contributions from each basis cell are added to obtain the value on the working mesh.
				In both cases, mind the value of 'b2news_area_fix', which should be also declared in b2ag.dat if the non-default behaviour is wanted.
			', """1"""),
   
      'b2agsi_isymm' : ('Geometry', 'integer', '
				isymm - integer.
				isymm specifies the type of symmetry of the geometry: isymm.eq.0
				implies a slab geometry, isymm.eq.1.or.isymm.eq.2 imply rotational symmetry about the crx=0 axis, and isymm.eq.3.or.isymm.eq.4
				indicate rotational symmetry about the cry=0 axis.
				Other values are not allowed.
				isymm.eq.1.or.isymm.eq.3 mean a toroidal geometry case, i.e. with a toroidal (out-of-plane) magnetic field component.
				isymm.eq.2.or.isymm.eq.4 mean a cylindrical geometry case, i.e.
				no toroidal magnetic field component.
				To be used in b2ag.dat.
			', """1"""),
   
      'b2aidr_read_b2fstate' : ('Run', 'integer', '
				If read_b2fstate.ne.0, b2aidr will read an existing b2fstate file and append to it a flat state description for additional new species being introduced in the run.
			', """0"""),
   
      'b2ardr_fix_cx' : ('Atomic Physics', 'integer', '
				It is used to "correct" the CX data
				 0 => do not fix
				 1 => only fix H if CX data is < 1e-40 [default]
				 2 => fix if CX data is < 1e-40
				 3 => fix H
				 4 => fix all
				At the moment the only species with CX data in ADAS is C. Be careful with options that use the fit formula other than for H. 
				See the comments in ratstr.F for the origin of the fit formula used to "fix" the CX data.
			', """1"""),
   
      'b2ardr_fix_recomb' : ('Atomic Physics', 'integer', '
				When changed from 0, and if the ADAS option is in use, then uses the PRB file to add the contribution arising from is-->is-1 processes.
				This term includes the Bremsstrahlung.
				The default option ('0') only contains the Bremsstrahlung for the is-->is-1 process.
				This option should be used with the 'b2stel_fix_recomb_energy' option b2mn.dat set to '1'. See 'Physics' section.
				*** Use with caution! ***
			', """0"""),
   
      'b2ardr_no_weisheit' : ('Atomic Physics', 'integer', '
				When set to 1, disables the correction of the hydrogen atomic rate data with the Weisheit data using ratwei. *** Use with caution! ***
			', """0"""),
   
      'b2ardr_no_smoothing' : ('Numerics', 'integer', '
				When set to 1, disables the tail smoothing for of rate coefficients to represent the effect of a power-law tail on the distribution function. It has been added for compatibility with SOLPS4.3
			', """0"""),
   
      'b2mndr_astra' : ('Run', 'integer', '
				Turns on coupling with the ASTRA core transport code if non-zero.
				To be used, the code must be compiled with the -DASTRA option.
			', """0"""),
   
      'b2mndr_atomic_physics_rescale' : ('Physics', 'integer', '
				If atomic_physics_rescale is not 0, then the code will rescale the rates stored in b2frates according to the multipliers given in the b2.atomic_physics_rescale.parameters inputfile before making use of them.
			', """0"""),
   
      'b2mndr_b2time' : ('Output', 'integer', '
				Specifies the number of timesteps between writes of the time-dependent file. If b2time.gt.0, always writes out on the last timestep.
			', """1"""),
   
      'b2mndr_cdfmovietim' : ('Output', 'real', '
				Another option for movie output. Give the real-time interval between movie frames.
			', """0.0"""),
   
      'b2mndr_coronal_model' : ('Physics', 'integer', '
				Turns on the coronal model if coronal.ne.0. I.e., the reaction rates of all reactions are made density-independent, and the value computed at the lowest density (given in b2ar.dat) is used.
			', """0"""),
   
      'b2mndr_cpu' : ('Run', 'real', '
				CPU limit. If cpu.eq.0.0, no CPU limit is enforced. Otherwise, the code stops smoothly after it has been running for at least 'cpu' CPU seconds.
			', """0.0"""),
   
      'b2mndr_density_rescale' : ('Run', 'real', '
				Multiplier of all densities on the first timestep.
			', """1.0"""),
   
      'b2mndr_dtim' : ('Run', 'real', '
				Timestep (in seconds).
			', """1.0"""),
   
      'b2mndr_eirene' : ('Run', 'integer', '
				Turns on coupling with the Eirene Monte-Carlo neutral code if non-zero.
				To be used, the code must be compiled with the -DB25_EIRENE option.
			', """0"""),
   
      'b2mndr_elapsed' : ('Run', 'integer', '
				Elapsed time limit. Is elapsed.eq.0.0, no time limit is enforced.
				Otherwise, the code stops smoothly after is has been running for at least 'elapsed' wall clock seconds.
			', """0"""),
   
      'b2mndr_etim' : ('Run', 'real', '
				etim specifies the end time. Only active if etim > stim.
			', """0.0"""),
   
      'b2mndr_hz' : ('Physics', 'real', '
				hz has been introduced into the new form of the parallel momentum balance equation.
				If fac_hz = 0.0 then hz = 1 and old form of equations is used.
				If fac_hz = 1.0 then new form of equations is used.
			', """0.0"""),
   
      'b2mndr_inverse_ua' : ('Output', 'integer', '
				If inverse_ua.eq.1, the code will produce a 'b2fstati_with-ua' file that contains the same plasma information, but with the opposite sign convention for the parallel velocity. The run will then proceed with the new velocities with their sign inverted.
			', """0"""),
   
      'b2mndr_ismain' : ('Run', 'integer', '
				ismain identifies the index of the main plasma species. 
				It must hold that ismain is not a neutral species.
			', """1"""),
   
      'b2mndr_mvinc' : ('Output', 'integer', '
				Specifies the number of timesteps between movie output. If greater than 1 and the last timestep does not correspond to a planned frame, an extra endstate frame is added.
			', """1"""),
   
      'b2mndr_mvnum' : ('Output', 'integer', '
				Specifies the maximum number of instances at which movie data will be output.
			', """0"""),
   
      'b2mndr_na_min' : ('Numerics', 'real', '
				Minimal density maintained in all cells for all species.
				It must be true that na_min is smaller than na_new, as well as any of the initial densities provided in b2ai.dat.
				This switch replaces 'b2mndr_na0eps' from SOLPS5.x.
			', """1.0e4"""),
   
      'b2mndr_na_new' : ('Numerics', 'real', '
				Initial density put in all cells for all new species if not overwritten by initial state file.
				This switch replaces 'b2mndr_na0eps' from SOLPS5.x.
			', """1.0e14"""),
   
      'b2mndr_ntim' : ('Run', 'integer', '
				Number of timesteps desired in this run. If ntim.eq.0, the code simply reads the input file and creates the b2fplasma and b2fstate files corresponding to the present plasma state.
			', """1"""),
   
      'b2mndr_plasmatim' : ('Output', 'real', '
				Another option for plasma state file output. Give the real-time interval between succesive write-ups of plasmastate files, in addition to the ones written at regular CPU intervals.
			', """0.0"""),
   
      'b2mndr_rescale_neutrals' : ('Run', 'real', '
				Multiplier to the neutral density on the first timestep.
			', """1.0"""),
   
      'b2mndr_rescale_neutrals_sources' : ('Run', 'real', '
				Multiplier to the neutral sources (either computed by Eirene or the corresponding rate coefficients).
			', """1.0"""),
   
      'b2mndr_savecpu' : ('Run', 'real', '
				CPU time interval after with save files plasmastate.xxxx are written.
				These can be used, in conjunction with the b2co.exe instruction, to recover a crashed run.
			', """3600.0"""),
   
      'b2mndr_stim' : ('Run', 'real', '
				stim specifies the initial time --- default 0.
				If set to a positive or zero value, this overwrites the time value read from b2fstati.
				If set to a negative value, the run continues from the time read in b2fstati.
			', """0.0"""),
   
      'b2mndr_tally' : ('Output', 'integer', '
				Specifies the number of timesteps between writes of tallies.
				If tally.gt.0, always writes out on the last timestep.
			', """1"""),
   
      'b2mndr_trantim' : ('Output', 'real', '
				Produces a numbered 'tran' file every trantim real-time seconds.
				An endstate file is written if it falls between scheduled write-up times.
				Only available within the -DJET environment.
			', """0.0"""),
   
      'b2mndt_density_control' : ('Run', 'integer', '
				Feedback on the total heavy particle density. If density_control.ne.0, the sum of all densities is kept constant.
			', """0"""),
   
      'b2mndt_moitlv' : ('Output', 'integer', '
				Controls detailed monitoring output. moitlv.eq.-1 means no output, moitlv.eq.0 means output once per timestep, moitlv.eq.1 means output once per nstg0 iteration, moitlv.eq.2 means output once per nstg1 iteration and moitlv.eq.3 means output once per nstg2 iteration. See 'b2mndr_nstg?' description in Run section for more details.
			', """-1"""),
   
      'b2mndt_moqtlv' : ('Output', 'integer', '
				Controls quick trace output. moqtlv.eq.-1 means no output, moqtlv.eq.0 means output once per timestep, moqtlv.eq.1 means output once per nstg0 iteration, moqtlv.eq.2 means output once per nstg1 iteration and moqtlv.eq.3 means output once per nstg2 iteration. See 'b2mndr_nstg?' description in Run section for more details.
			', """3"""),
   
      'b2mndt_ntim_step_out' : ('Numerics', 'integer', '
				When set to a value of 'K', residuals at each K-th step will be written in b2ftrace. It helps to avoid a huge b2ftrace files during long time run.
			', """1"""),
   
      'b2mndt_rxf' : ('Numerics', 'real', '
				Main under-relaxation parameter.
			', """0.5"""),
   
      'b2mndt_style' : ('Numerics', 'integer', '
				When set to '1', all important variables will be calculated for the first step.
				This avoids a jump of residuals when continuing the run.
			', """0"""),
   
      'b2mndt_use_b2srst' : ('Numerics', 'integer', '
				Switches off the stabilization of the source coefficients.
			', """1"""),
   
      'b2mwqt_style' : ('Output', 'integer', '
				NOT FOUND!
			', """1"""),
   
      'b2mwti_ismain0' : ('Output', 'integer', '
				Index of the species used to create the 'dp3d?.last10' diagnostic files.
				Defaults to the neutral species associated with ismain. If no such species is declared, the default will be set to ismain. Is expected to either correspond to a neutral species or to ismain.
				If ismain is also defaulted, then will be 0.
			', """0"""),
   
      'b2mwti_jxa' : ('Geometry', 'integer', '
				Cell index, on the basis mesh, of the outer midplane. Default value depends on geometry:
				Single-null : jxa=rightcut1(1)-(rightcut1(1)-leftcut1(1))/4, i.e. three quarters of the way between the two cuts. Double-null : jxa=(rightcut1(1)+rightcut1(2))/2, i.e. halfway between the two outer cuts.
				Straight geometry : jxa=3*nx/4
			', """See description"""),
   
      'b2mwti_jxi' : ('Geometry', 'integer', '
				Cell index, on the basis mesh, of the inner midplane. Default value depends on geometry:
				Single-null : jxi=leftcut1(1)+(rightcut1(1)-leftcut1(1))/4, i.e. one quarter of the way between the two cuts. Double-null : jxi=(rightcut1(1)+rightcut1(2))/2, i.e. halfway between the two inner cuts.
				Straight geometry : jxi=nx/4
			', """See description"""),
   
      'b2mwti_target_offset' : ('Output', 'integer', '
				The diagnostic values from b2time.nc use guard cell values if target_offset.eq.0, and values from the neighbouring real cell if target_offset.eq.1. Fluxes are not affected.
			', """1"""),
   
      'b2news_area_fix' : ('Numerics', 'integer', '
				When area_fix.eq.0, recovers old SOLPS5.0 behaviour.
				If area_fix.ge.1, then certain computations of poloidal velocities are done by dividing flows by the area normal to the flux tube as opposed to the area of contact.
				If area_fix.ge.2, then additionally this treatment is used for the parallel contact area used in determining plasma flux limiters.
				If area_fix.ge.3, then additionally this treatment is used for all parallel contact areas.
			', """3"""),
   
      'b2news_BoRiS' : ('Physics', 'real', '
				The poloidal convective heat flux contains a prefactor of (3/2+BoRiS). The default gives us the internal energy equation. The value BoRiS = 1.0 gives us the total energy equation.
				Only for use to benchmark with codes using the total energy equation. When used, the meaning of fhe and fhi changes from internal energy fluxes to total energy fluxes.
			', """0.0"""),
   
      'b2news_coriolis' : ('Physics', 'integer', '
				If coriolis.ne.0, the Coriolis force terms will be included in the solution of the momentum equations.
			', """0"""),
   
      'b2news_do_2nd_b2npco_call' : ('Numerics', 'integer', '
				If do_2nd_b2npco_call.eq.1, perform a second call to the density equation solve to improve particle balance, as done in SOLPS4.
			', """0"""),
   
      'b2news_ExB' : ('Physics', 'real', '
				Real parameter which multiplies ExB flows. If b2news_ExB.eq.0 and b2news_facExB_start.eq.0 then ExB flows are switched off. If b2news_ExB is non-zero, then ExB flows are multiplied by that constant throughout the run.
				See also Run section on switches b2news_facExB_... for more details. A spatial fac_ExB profile is also possible, see Numerics section for details.
			', """0.0"""),
   
      'b2news_guard_flows' : ('Numerics', 'integer', '
				If guard_flows.eq.0, flows between neighbouring guard cells are blocked.
				If guard_flows.eq.1, flows between neighbouring guard cells are kept.
				If guard_flows.eq.2, particle flows between neighbouring guard cells are blocked for density equation and the incorrect corner values are replaced by interpolated values. It is recommended 2.
			', """2"""),
   
      'b2news_ncallout' : ('Output', 'integer', '
				If the iteration number is equal to ncallout, then several output files 'b2ne_npmo', 'b2ne_xppb', 'b2ne_npco', 'b2ne+nppo' which detail the convergence behaviour and residuals.
			', """-1"""),
   
      'b2news_no_b2sral_call' : ('Numerics', 'integer', '
				If no_b2sral_call.eq.0, add an additional call to recompute the source in b2news_ to reproduce the behaviour from SOLPS4.
			', """1"""),
   
      'b2news_no_solve' : ('Run', 'integer', '
				If no_solve.eq.1, then the code is run without actually solving any equations. All secondary and dependent data is computed.
				The nstg(0:2) array is overwritten to '1's.
				The simulation time will not be updated.
				The code will compute fluxes, sources, transport coefficients, etc...
				'ntim' times but not update the basic plasma quantities. Additionally, if no_solve is set to a negative value, then only some equations are solved (simulation time and nstg arrays will behave normally).
				no_solve.eq.-1 will activate the parallel momentum equations only.
				no_solve.eq.-2 will activate the density equations only. no_solve.eq.-4 will activate the potential equation only. (Active only if poteq.eq.1, otherwise, the behaviour dictated by the poteq setting applies).
				no_solve.eq.-8 will activate the heat equations only.
				These can be combined. For example, no_solve.eq.-3 will activate the parallel momentum and particle conservation equations.
				If the no_solve switch requires an equation not to be solved, the settings in the corresponding solvexx arrays from b2.numerics.parameters are moot.
				The latter are reserved for fine-tuning numerical diagnostics.
			', """0"""),
   
      'b2news_poteq' : ('Numerics', 'integer', '
				If poteq.eq.0, the potential equation is jumped over and not solved.
				If poteq.eq.2, the potential is set to 3.1*Te/qe as per SOLPS4.0.
				If poteq.eq.1, the potential equation is solved according to the no_solve switch settings.
				If poteq.ne.1, then 'b2tfhe_no_current'must be set to '1'.
			', """1"""),
   
      'b2news_potok' : ('Numerics', 'real', '
				Target residual for the potential equation.
			', """1.0e-2"""),
   
      'b2news_ramp_slow' : ('Numerics', 'integer', '
				If ramp_slow.eq.0 (default), the ExB and diamagnetic drifts multipliers are ramped on each call of b2news, otherwise they are only changed on the first call of the nstg loop on the timestep.
			', """0"""),
   
      'b2news_recalculate_contributions' : ('Numerics', 'integer', '
				If recalculate_contributions.eq.0, turns off recomputation of sources when wrong_flow flag is active.
			', """1"""),
   
      'b2news_re_eval_prtls_fluxes' : ('Numerics', 'integer', '
				If re_eval_prtls_fluxes.eq.1, the particle fluxes are recomputed at the end of b2news_. This is necessary for rescaling of the Eirene sources during coupled runs, so this switch is superceded by use_eirene, and also needed to reproduce SOLPS4 runs.
			', """0"""),
   
      'b2news_vis' : ('Physics', 'real', '
				Alternative name of the variable in the code is fac_vis_scalar
			', """0.0"""),
   
      'b2npco_rxg' : ('Numerics', 'real', '
				rxg specifies a special under-relaxation parameter. A term of the form "abs(residual)/rxg" is added to the diagonal of the matrix of the correction equation, with the effect of limiting the computed correction. rxg is dimensionless and of order unity; smaller values of rxg imply stronger damping.
			', """1.0"""),
   
      'b2npht_rxg' : ('Numerics', 'real', '
				rxg specifies a special under-relaxation parameter. A term of the form "abs(residual)/rxg" is added to the diagonal of the matrix of the correction equation, with the effect of limiting the computed correction. rxg is dimensionless and of order unity; smaller values of rxg imply stronger damping.
			', """1.0"""),
   
      'b2npht_style' : ('Numerics', 'integer', '
				When set to '1', SPb's form of the program b2sihs_ is called.
				It is recommended '1'.
			', """1"""),
   
      'b2nph9_style' : ('Numerics', 'integer', '
				When set to '1', SPb's form of the program b2sihs_ is called.
				It is recommended '1'.
			', """1"""),
   
      'b2npmo_b2sifr_' : ('Physics', 'integer', '
				When set to '1', the new correct form of the friction force is used.
				The value '0' corresponds to the old SOLPS5.0 treatment.
			', """1"""),
   
      'b2npmo_modvis' : ('Physics', 'integer', '
				When set to '1', the new correct form of viscosity is used. It is important for runs with drifts. It is recommended '1'.
				The value '0' corresponds to the old SOLPS5.0 treatment.
			', """1"""),
   
      'b2npmo_rxg' : ('Numerics', 'real', '
				Normalisation factor for the parallel momentum equation.
			', """1.0e6"""),
   
      'b2npp7_style' : ('Numerics', 'integer', '
				When set to '1', SPb's form of the program b2usp7_ is called.
				It is recommended '1'.
			', """1"""),
   
      'b2nxdv_style' : ('Numerics', 'integer', '
				When set to '1', the total friction force cancel is not calculated at the guard boundary cells.
				It is recommended '1'.
			', """1"""),
   
      'b2nxfc_style' : ('Numerics', 'integer', '
				style specifies the precise form of interpolation used in the computation of flcb and cvcb. When set to '1', SPb's form of the transport terms in the momentum correction equation is used.
				It is recommended '1'.
			', """1"""),
   
      'b2nxfx_style' : ('Numerics', 'integer', '
				When set to '1', SPb's form of an expression that occurs in the electron-atom thermal force is used.
				It is recommended '1'.
			', """1"""),
   
      'b2sdia_facgt' : ('Physics', 'real', '
				Multiplier of the contribution to electron and ion heat sources from divergence of the gradTxB heat flux. That contribution is also multiplied by facdrift. This term is no longer needed as it has been transferred from being a source to being included in the flows.
			', """0.0"""),
   
      'b2sicf_phm0' : ('Physics', 'real', '
				Multiplier of the centrifugal force term.
				It is recommended '1.0'.
				The value '0.0' corresponds to the old SOLPS5.0 treatment.
			', """1.0"""),
   
      'b2sicf_phm1' : ('Physics', 'real', '
				Multiplier of the centrifugal force correction term due to linearization.
				It is recommended '1.0'.
				The value '0.0' corresponds to the old SOLPS5.0 treatment.
			', """1.0"""),
   
      'b2sifr_phm0' : ('Physics', 'real', '
				Multiplier of the friction term between charged species.
			', """1.0"""),
   
      'b2sifr_phm1' : ('Physics', 'real', '
				Multiplier of the ehxp term in the thermal force term.
			', """1.0"""),
   
      'b2sifr_phm2' : ('Physics', 'real', '
				Multiplier of the electron thermal gradient term in the thermal force term.
			', """1.0"""),
   
      'b2sigp_style' : ('Numerics', 'integer', '
				When set to '1', SPb's form of the pressure gradient term on the right hand of the momentum balance equation is used.
				It is recommended '1'.
			', """1"""),
   
      'b2sihs_istyle_Joule_heating' : ('Physics', 'integer', '
				When set to '1', there is no radial contribution in Joule heating because there are no physical reasons to take it into account.
				The value '0' corresponds to the old SOLPS5.0 treatment.
			', """1"""),
   
      'b2sihs_phm0' : ('Physics', 'real', '
				Multiplier of the contribution to electron heat sources from divergence(ue,ve).
			', """1.0"""),
   
      'b2sihs_phm1' : ('Physics', 'real', '
				Multiplier of the contribution to ion heat sources from divergence(ua,va).
				This term is superseded by the BoRiS switch if invoked.
			', """1.0"""),
   
      'b2sihs_phm2' : ('Physics', 'real', '
				Multiplier of the contribution to ion heat sources from viscous heating.
				This term is superseded by the BoRiS switch if invoked.
			', """1.0"""),
   
      'b2sihs_phm3' : ('Physics', 'real', '
				Multiplier of the contribution to electron heat sources from Joule heating (electron-ion friction).
			', """1.0"""),
   
      'b2sihs_phm4' : ('Physics', 'real', '
				Multiplier of the contribution to ion heat sources from atom-atom friction.
				This term is superseded by the BoRiS switch if invoked.
			', """1.0"""),
   
      'b2sihs_phm5' : ('Physics', 'real', '
				Multiplier of the contribution to electron heat sources from divergence of the electrical drift. That contribution is also multiplied by facExB.
			', """1.0"""),
   
      'b2sihs_phm6' : ('Physics', 'real', '
				Multiplier of the contribution to ion heat sources from divergence of the electrical drift. That contribution is also multiplied by facExB.
			', """1.0"""),
   
      'b2sihs_phm7' : ('Physics', 'real', '
				Multiplier of the contribution to heat sources from friction due to diamagnetic velocities. Normally already included in 'phm3' term above.
			', """0.0"""),
   
      'b2sihs_style' : ('Numerics', 'integer', '
				style determines the form of the strange electron-atom energy transfer term.
			', """0"""),
   
      'b2sqel_artificial_radiation' : ('Physics', 'real', '
				If art_rad.ne.0, then an artificial radiation loss term is added to the electron cooling rate. Art_rad represents the percent fraction of impurities in the plasma.
			', """0.0"""),
   
      'b2sqel_phm0' : ('Physics', 'real', '
				Multiplier to the ionisation rate coefficient.
			', """1.0"""),
   
      'b2sqel_phm1' : ('Physics', 'real', '
				Multiplier to the recombination rate coefficient.
			', """1.0"""),
   
      'b2sqel_phm2' : ('Physics', 'real', '
				Multiplier to the heat loss rate coefficient.
			', """1.0"""),
   
      'b2sral_inputfile' : ('Run', 'integer', '
				Profiles file indicator. If b2sral_inputfile.eq.1, then the code looks for the file b2.sources.profile in which it expects to find the 'profile' namelist.
				This namelist will contain profiles of sources measured from the location (ixref,iyref) (default is outer midplane separatrix), which is set with the 'set_transport_i[xy]ref' switches.
			', """0"""),
   
      'b2sral_style' : ('Physics', 'integer', '
				When set to '0', in the expression of the electron particle flux (fne) the particle flux with drift terms is used and temporary drift velocities on the first call are calculated. When set to '1' or '2', the particle flux without drift terms is used in fne.
				It is recommended '2'.
			', """2"""),
   
      'b2srsm_diagno' : ('Output', 'integer', '
				Controls level of output in b2srsm. If diagno.ge.2, output will be given on every call. If diagno.eq.1, output will be given on main calls only.
			', """0"""),
   
      'b2srsm_enable' : ('Numerics', 'integer', '
				If enable.ne.0, then the sources for particle, parallel momentum, electron and ion heat are rescaled, for non-boundary cells, if the local timestep exceeds the physics timescale implied by those sources.
			', """0"""),
   
      'b2stbc_bcpot_16_step' : ('Numerics', 'integer', '
				Frequency (in number of calls to b2stbc_phys) at which the constant value of the potential at the boundaries where BCPOT=16 is applied will be recomputed.
			', """50"""),
   
      'b2stbc_cbc' : ('Run', 'real', '
				Multiplier to the ExB velocity for sheath boundary conditions in b2stbc_spb and BCMOM=13 case of b2stbc_phys.
			', """1.0"""),
   
      'b2stbc_diagno' : ('Output', 'integer', '
				Controls level of output in b2stbc and subservient routines.
				Level 1 (diagno.ge.1) output includes wrong_flow warnings, transport coefficients at the (nx/2,ny) basis mesh position, the solution found for the given heat flux at constant temperature bc, and all feedback diagnostics.
				Level 2 output (diagno.ge.2) includes the integral current correction, the boundary sources on the first call, excessive sound speeds, and the iterative progress to the given heat flux at constant temperature bc. 
				Level 3 output (diagno.ge.3) includes the boundary sources on each call, and the boundary.prt file listing all boundary cells.
			', """0"""),
   
      'b2stbc_fchy_dia' : ('Numerics', 'real', '
				Multiplier to the neoclassical current and diamagnetic heat flux convective boundary conditions, also multiplied by facdrift.
				Allows use b2stbc_integral_current is fchy_dia.eq.0, forbids it otherwise.
			', """1.0"""),
   
      'b2stbc_fchy_dia_coreonly' : ('Numerics', 'integer', '
				If fchy_dia_coreonly.eq.1, the neoclassical current and diamagnetic heat flux convective boundary conditions are only applied on the core boundary.
				If fchy_dia_coreonly.eq.0, those are applied to all boundaries, including PFR, North SOL edge and diverted island center boundary.
			', """1"""),
   
      'b2stbc_feedback' : ('Run', 'integer', '
				If feedback.eq.1, turns on feedback mode for the boundary conditions.
				See Physics section for more details. Equivalent to LFEEDBACK=.true. in the b2.boundary.parameters namelist.
			', """0"""),
   
      'b2stbc_fix_fch_in_fhe_sheath' : ('Numerics', 'integer', '
				If fix_fch_in_fhe_sheath.eq.0, then the wrong (old) implementation of the FCH contribution to FHE used;
				If fix_fch_in_fhe_sheath.eq.1, then the wrong (second) implementation of the FCH contribution to FHE used;
				If fix_fch_in_fhe_sheath.eq.2, then the correct implementation of the FCH contribution to FHE used;
			', """2"""),
   
      'b2stbc_integral_current' : ('Numerics', 'real', '
				If integral_current.gt.0, corrects current sources so that there be no surface current at the North and South edges of the edge plasma.
				The value of integral_current multiplies the correction term added to the current source.
				This setting is incompatible with the normal use of diamagnetic drift terms (facdrift.gt.0.0 .and. b2stbc_fchy_dia.ne.0.0) or neoclassical boundary conditions (b2stbc_neoclassical.gt.0.0).
			', """0.0"""),
   
      'b2stbc_istyle_cur_contr_on_S_and_N' : ('Numerics', 'integer', '
				When set to '2', SPB's form of adding currents on the South core boundary is included by using BCPOT=12, and on the SOuth PFR and North boundaries by using BCPOT=13. It is recommended '2', in conjunction with the BCPOT=12 and BCPOT=13 settings, respectively.
				When set to '1', SPb's form of adding currents on South and North boundaries is done explicitly in addition to other existing boundary conditions for the potential equation.
				The old 5.0 calculation is recovered by using the value '0'.
			', """2"""),
   
      'b2stbc_istyle_fchi' : ('Numerics', 'integer', '
				If '1', explicitly use the expression (bx*cs*na) of particle flux (fna) from boundary condition instead of fna.
			', """0"""),
   
      'b2stbc_ncallfeedback' : ('Run', 'integer', '
				Timestep index after which the feedback in b2stbc is activated.
			', """0"""),
   
      'b2stbc_neoclassical' : ('Numerics', 'real', '
				Real parameter which establishes boundary conditions for radial component of the current for North and South boundaries when these lie on closed flux surfaces.
				If b2stbc_neoclassical is 0 then the radial component of the current is zero.
				If b2stbc_neoclassical is not 0 the radial component of the current is given by the neoclassical value. b2stbc_neoclassical is superseded if facdrift.ne.0.
				This cannot be used in conjunction with b2stbc_integral_current below.
			', """0.0"""),
   
      'b2stbc_secmodel' : ('Physics', 'integer', '
				If secmodel.eq.1, then the secondary electron emission coefficient at the plates is computed locally according to a kinetic model, otherwise the default values of cbsch(7,ireg) and/or gammae are used.
			', """0"""),
   
      'b2stbc_sheath_drift_fix' : ('Numerics', 'integer', '
				If sheath_drift_fix.eq.0, then the drift velocity used in the sheath boundary conditions is the sum of diamagnetic and ExB contributions (old, but likely wrong, treatment). If sheath_drift_fix.eq.1, then the drift velocity used in the sheath boundary conditions is the ExB velocity only (recommended).
			', """1"""),
   
      'b2stbc_solregno' : ('Geometry', 'integer', '
				solregno is the boundary index of the SOL North boundary in the input files b2ah.dat and b2mn.dat. For a standard single-null case, solregno is 3. For a standard double-null case, solregno for the outer SOL North boundary would be 7.
			', """3"""),
   
      'b2stbm_impgyro_mod' : ('Numerics', 'integer', '
				Specifies the frequency (in units of full b2 timesteps) at which an externally coupled code providing additional source (for instance a kinetic treatment of trace impurity ions such as IMPGYRO) should be called.
			', """0"""),
   
      'b2stbm_linearisation' : ('Numerics', 'real', '
				Same as above, but applied to the sources coming for an externally coupled code providing plasma sources, for instance a kinetic treatment of trace impurity ions. 'b2stbm_linearization' is an alias for this switch.
			', """1.0"""),
   
      'b2stbr_core_sources_rescale' : ('Run', 'real', '
				Multiplier to the totally ionised species sources at the core boundary.
			', """1.0"""),
   
      'b2stbr_eir_src_nhist' : ('Numerics', 'integer', '
				If b2stbr_eir_src_nhist.gt.1, then Eirene sources are accumulated and a moving average is computed. Note that only one of b2stbr_eir_src_nhist, eirene_neutr_avg, or eirene_underrelax may be nonzero.
			', """1"""),
   
      'b2stbr_first_flight' : ('Run', 'integer', '
				If first_flight.ne.0, turns on the first flight model. See Physics section for additional details.
			', """0"""),
   
      'b2stbr_first_flight_dl' : ('Numerics', 'real', '
				Step length (in meters) for computing the first flight model chords.
			', """0.001"""),
   
      'b2stbr_first_flight_no_of_flights' : ('Numerics', 'integer', '
				Number of chords started from each start point in the first flight model.
			', """9"""),
   
      'b2stbr_first_flight_no_of_start_points' : ('Geometry', 'integer', '
				When the first flight model is turned on, this number must be greater than or equal to the number of boundary cells on the mesh.
				Only in cases with special geometries (i.e. limiters, islands, ...) need it be increased beyond the default value above. This variable is only used within the first flight module.
			', """2*(nx+2)+2*max(nncut,1)*(ny+2)"""),
   
      'b2stbr_first_flight_table_size' : ('Numerics', 'integer', '
				Workspace size given to the first flight table.
			', """200000"""),
   
      'b2stbr_output' : ('Output', 'integer', '
				Output flag for the first_flight model. If output.ge.1, the files start, end, and fort.88 are created, which contain information about the chords used in the model.
			', """0"""),
   
      'b2stbr_potential_at_guard_cell' : ('Numerics', 'integer', '
				If potential_at_guard_cell.eq.1, the electric potential used for the computation of the incident energy for sputtering yields is taken as the value in the guard cell. If potential_at_guard_cell.eq.0, the value from the neighbouring real cell is used instead.
			', """1"""),
   
      'b2stbr_bas_recycled_neutrals_contr' : ('Physics', 'real', '
				Introduced for nulling recycling energy when it is zero.
			', """1.0"""),
   
      'b2stcx_rg0' : ('Numerics', 'real', '
				(rg0 for numerical stabilisation; needs experiments.)
			', """1.0"""),
   
      'b2stcx_styl0' : ('Numerics', 'integer', '
				Specifies the type of linearisation used in the charge exchange momentum source term.
			', """0"""),
   
      'b2stel_fix_recomb_energy' : ('Physics', 'integer', '
				If changed to 1, then the recombination energy (rpi) is added to the electron energy for each recombination. This should only be used if the is-->is-1 energy terms have been included in the electron cooling rates (as done by setting the switch 'b2ardr_fix_recomb' in b2ar.dat to a non-zero value and recalculating b2frates).
				See 'Atomic Physics' section.
				*** Use with caution! ***
			', """0"""),
   
      'b2stel_phm0' : ('Physics', 'real', '
				Multiplier of the recombination contribution to the electron cooling rate (if ADPAK rates are not used because those are already included). Assumes all recombination is three-body.
			', """0.0"""),
   
      'b2stel_styl0' : ('Numerics', 'integer', '
				Specifies the type of linearisation used in the charge exchange momentum source term.
			', """0"""),
   
      'b2tfcc_xfac' : ('Numerics', 'real', '
				Multiplier to the pressure force term.
			', """1.0"""),
   
      'b2tfhe_alfTeEh' : ('Physics', 'real', '
				When set to '0.0', the old form of the electron heat flux calculation is used.
				It is recommended to use 1.0.
			', """0.0"""),
   
      'b2tfhe_conduction_only' : ('Physics', 'integer', '
				When conduction_only.eq.1, convective heat transfer terms are turned off. Only to be used when benchmarking against pure conduction cases.
			', """0"""),
   
      'b2tfhe_fch_pTe' : ('Physics', 'real', '
				When set to '1.0', the new form of the electron heat flux calculation is used.
				It is recommended to use 1.0.
			', """1.0"""),
   
      'b2tfhe_lim_flux' : ('Physics', 'integer', '
				If '0', flux limit is not applied directly to the electron heat flux but is applied through transport coefficients if 'b2trcl_conductive_limit' is '1'.
				It is recommended '0'.
			', """1"""),
   
      'b2tfhe_mdf' : ('Numerics', 'integer', '
				If '1', Spb's new form of calculating electron heat flux is used.
				It is recommended '1' for runs with drifts.
			', """0"""),
   
      'b2tfhe_neutral' : ('Physics', 'real', '
				Real parameter which multiplies ion-neutral current.
				If b2tfhe_neutral is 0 then ion-neutral current is switched off otherwise ion-neutral current is switched on.
			', """0.0"""),
   
      'b2tfhe_no_current' : ('Numerics', 'integer', '
				If no_current.eq.1, all currents are set to zero. The setting no_current.eq.1 must be used if the potential equation is not explicitly solved for, i.e. for b2news_poteq.ne.1.
			', """0"""),
   
      'b2tfhe_vis_par' : ('Physics', 'real', '
				Real parameter which multiplies current driven by parallel viscosity. 
				If b2tfhe_vis_par is 0 then viscosity-driven current is switched off otherwise viscosity-driven current is switched on.
			', """0.0"""),
   
      'b2tfhe_vis_per' : ('Numerics', 'real', '
				If '1.0', the electric potential equation is solved by the subroutine b2npp7 using a 7-point stencil.
				The value '1.0' is recommended for runs with drifts when perpendicular viscosity and corresponding perpendicular viscosity current is taken into account.
			', """0.0"""),
   
      'b2tfhe_vis_q' : ('Physics', 'real', '
				Real parameter which multiplies current driven by heat viscosity effects.
			', """1.0"""),
   
      'b2tfhi_lim_flux' : ('Physics', 'integer', '
				If '0', flux limit is not applied directly to the ion heat flux but is applied through transport coefficients if 'b2trcl_conductive_limit' is '1'.
				It is recommended '0'.
			', """1"""),
   
      'b2tfhi_mdf' : ('Numerics', 'integer', '
				If '1', Spb's new form of calculating ion heat flux is used.
				It is recommended '1' for runs with drifts.
			', """0"""),
   
      'b2tfnb_anomalous_core_only' : ('Physics', 'integer', '
				No description found.
			', """0"""),
   
      'b2tfnb_drift_style' : ('Numerics', 'integer', '
				When set to '0', drift velocities are calculated in cell centers. When set to '1', drift velocities are calculated in cell faces.
				It is recommended '1'.
			', """1"""),
   
      'b2tfnb_fnb_nodrift_style' : ('Numerics', 'integer', '
				When set to '1', SPb's form of calculating no drift part of the particle fluxes is used.
				It is recommended '1'.
			', """1"""),
   
      'b2tfnb_mdf' : ('Numerics', 'integer', '
				If '1', Spb's new form of calculating particle flux is used.
				It is recommended '1' for runs with drifts.
			', """0"""),
   
      'b2tfnb_PSch' : ('Physics', 'real', '
				Multiplier to the Pfirsch-Schlueter flows.
			', """1.0"""),
   
      'b2tfnb_xfrhie' : ('Numerics', 'real', '
				Multiplier to the Rhie and Chow upwind correction.
			', """1.0"""),
   
      'b2tfnb_xfrhiehz' : ('Numerics', 'real', '
				Multiplier to the Rhie and Chow upwind correction in particle flux which is passed to parallel balance momentum equation with drifts.
			', """1.0"""),
   
      'b2tfnb_ycur' : ('Physics', 'real', '
				Ycur is a multiplier to the parallel viscosity, ion inertial and anomalous currents to the ion radial flows (particle and energy).
			', """1.0"""),
   
      'b2tlh0_flux_limit_style' : ('Numerics', 'integer', '
				If '0', use the SOLPS5.0 scheme for neutral heat conductivity flux limits.
				If '1', Spb's form to calculate parallel and perpendicular neutral heat conductivity flux limit (does not preserve symmetry, kept for backward compatibility reasons).
				If '2', modifies the Spb treatment for the flux limits to be applied on the transport coefficients directly.
				It is recommended '2'.
			', """2"""),
   
      'b2tlh0_hcimx_flag' : ('Numerics', 'integer', '
				When set to -1, only the gradient to the left/bottom is used to compute the conductive neutral flux limits.
				When set to 0, only the gradient to the left/bottom is used to compute the conductive neutral flux limits, except when these do not exist (the other face value is used).
			', """1"""),
   
      'b2tlmv_style' : ('Physics', 'integer', '
				if style = 0 then
				 it is applied the origin flux limit to the viscosity
				else
				 it is applied the SPb flux limit to the viscosity
			', """1"""),
   
      'b2tqca_model' : ('Physics', 'integer', '
				If model.eq.1, use the Balescu formulation from SOLPS5.0 classical parallel ion heat diffusivity.
				If model.eq.2, use the older Braginskii SOLPS4.0 model.
				If model.eq.3, it is as model.eq.1 but without factor 4/3 which is applied to cvsahz for main ions in b2tral.F.
				It is recommended '3'.
			', """3"""),
   
      'b2tqca_phm0' : ('Physics', 'real', '
				Multiplier for the classical parallel viscosity.
			', """1.0"""),
   
      'b2tqce_model' : ('Physics', 'integer', '
				If model.eq.1, use the fitted Balescu formulation from SOLPS5.0 classical parallel electron heat diffusivity.
				If model.eq.2, use the older Braginskii SOLPS4.0 model.
				If model.eq.3, use the 21-moment Balescu results.
			', """1"""),
   
      'b2tqce_fke_Zhdanov' : ('Physics', 'integer', '
				When set to '1', Zhdanov's expression is used in the electron thermal conductivity. It is recommended to use 'b2tqce_fke_Zhdanov' '1'.
				This switch is only active if, simultaneously, one has b2tqce_model.eq.1 and b2tfhe_fch_pTe.eq.1.0.
			', """1"""),
   
      'b2tqna_diagno' : ('Output', 'integer', '
				If diagno.gt.0, outputs details of the calculations of neutral transport coefficients when using the new_df0 model.
				See switch b2tqna_new_df0 for more details.
			', """0"""),
   
      'b2tqna_divsol_rescale' : ('Physics', 'integer', '
				Scaling factor for all ion and electron transport coefficients inside divertor SOL regions.
			', """1.0"""),
   
      'b2tqna_inputfile' : ('Run', 'integer', '
				Profiles file indicator. If b2tqna_inputfile.eq.1, then the code looks for the file b2.transport.inputfile, in which it expects to find the transport namelist.
				This namelist will contain profiles of sources transport parameters measured from the location (ixref,iyref) (default is outer midplane separatrix), which is set with the 'set_transport_i[xy]ref' switches.
			', """0"""),
   
      'b2tqna_ixref' : ('Physics', 'integer', '
				Poloidal index (on the basis mesh) of the reference surface for the flux-scaled transport model. The default value is the outer midplane, computed as such (see b2mwti_jxa in Geometry section or set_transport_ixref below):
				Single-null : ixref=rightcut1(1)-(rightcut1(1)-leftcut1(1))/4. Double-null : ixref=(rightcut1(1)+rightcut1(2))/2.
				Straight geometry : ixref=3*nx/4.
				The flux-scaled transport model is used in conjunction with scaling factors listed in column (7) of the transport coefficients description in input files b2ah.dat and b2mn.dat.
			', """See description"""),
   
      'b2tqna_model_sig' : ('Physics', 'integer', '
				If '1', use constant density in core region to calculate anomalous conductivity sig0=dfsig*qe*ne(nmdpl,-1), nmdpl - number of midplane cell.
				If '0', use sig0=dfsig*qe*ne(x,y)
			', """0"""),
   
      'b2tqna_new_df0' : ('Physics', 'integer', '
				When new_df0.eq.1, the neutral diffusivity is computed according to the local charge-exchange, ionisation and elastic collision rates, instead of the standard form with constant cross-sections.
			', """0"""),
   
      'b2tqna_pfr_rescale' : ('Physics', 'real', '
				Scaling factor for all ion and electron transport coefficients inside private flux regions.
			', """1.0"""),
   
      'b2tral_mode' : ('Numerics', 'integer', '
				Switch to choose between various interpolation schemes for transport coefficients (Does not apply to pinch velocities vla or to the temperature-driven electric conductivity alf).
				mode.eq.-1: harmonic averaging
				mode.eq.0 : geometric averaging
				mode.eq.1 : arithmetic averaging (SOLPS5.0 formulation)
				mode.eq.2 : arithmetic averaging (SOLPS4.0 formulation)
			', """1"""),
   
      'b2trcl_conductive_limit' : ('Numerics', 'integer', '
				When set to '1', flux limit of the parallel electron and ion heat fluxes is applied to transport coefficients.
				It is recommended '1'. If 'b2trcl_conductive_limit' '0' then the keys 'b2tfhe_lim_flux' and 'b2tfhi_lim_flux' must be '0'.
			', """0"""),
   
      'b2trcl_core_cond_limit' : ('Numerics', 'integer', '
				If core_cond_limit.eq.0, then the heat flux limit due to chvemx is not applied in the core.
			', """0"""),
   
      'b2trcl_cvsa_mltpl' : ('Numerics', 'real', '
				Artificial coefficient providing faster convergence to the neoclassical electric field but giving a distortion of the flows in the SOL as a side-effect.
				Can be applied <1 during the convergence and turned off for the final stage of calculations.
				Use with caution.
			', """1.0"""),
   
      'b2trcl_lluciani' : ('Physics', 'integer', '
				If lluciani.ne.0, then transport coefficients on cells belonging to  closed field lines are modified according to the Luciani model.
				If lluciani.eq.1, the standard connection length formulation is used.
				If lluciani.eq.2, the old SOLPS4.0 formulation is used for backward compatibility.
				If lluciani.eq.3, Spb's new form Luciani's coefficient.
			', """3"""),
   
      'b2trcl_lthf21' : ('Physics', 'integer', '
				If lthf21.ne.0, then the heat transfer model is modified according to the 21-moment approach. This should only be used for multi-fluid runs.
			', """0"""),
   
      'b2trcl_lvis21' : ('Physics', 'integer', '
				If lvis21.ne.0, then the viscosities are modified according to the 21-moment approach. This should only be used for multi-fluid runs. This switch should not be used along with 'b2tfhe_vis_par' to avoid double-counting of classical viscosity effects.
			', """0"""),
   
      'b2treq_phm0' : ('Physics', 'real', '
				Multiplier to the temperature equipartition term.
			', """1.0"""),
   
      'b2trno_csig_an_style' : ('Physics', 'integer', '
				If '1', the anomalous contributions in the parallel direction to the electrical conductivity csig and the thermo-electric coefficient calf are zeroed out.
			', """1"""),
   
      'b2trno_flux_limit_to_dpa' : ('Numerics', 'integer', '
				If '1', flux limit to neutrals contribution to dpa0 - the diffusion coefficient is applied in b2tlc0.F. It is recommended '1'.
				b2tlc0.F has the flux limit parameters alpha and gamma which are given by 'b2tlc0_alpha' and 'b2tlc0_gamma'. 'b2tfnb_alpha' and 'b2tlc0_alpha' cannot be different from zero simultaneously.
				'b2tfnb_alpha' gives another form of flux limit which is applied to the whole particle flux.
			', """1"""),
   
      'b2trno_pol_anom_scale' : ('Physics', 'real', '
				If pol_anom_scale.ne.1, the poloidal anomalous transport coefficients are scaled by the number. To get the same treatment as setting the old switch (radial_only) to 1, set the new switch to 0.0.
				This multiplication is to only take place for charged species.
			', """1.0"""),
   
      'b2upht_stylec' : ('Numerics', 'integer', '
				(stylec is a numerical switch, needs experiments)
			', """0"""),
   
      'b2usmo_cfc0' : ('Numerics', 'real', '
				Linearisation constant.
			', """1.0"""),
   
      'b2ux5p_acpar' : ('Numerics', 'real', '
				Paremeter needed for iluter matrix solver.
			', """8.0"""),
   
      'b2ux5p_cpu' : ('Output', 'integer', '
				If cpu.gt.0, prints out the time spent in the matrix solver.
			', """0"""),
   
      'b2ux5p_mult_nonzero' : ('Numerics', 'integer', '
				Number of expected non-zero matrix elements per matrix row.
			', """10"""),
   
      'b2ux5p_nltrsol' : ('Output', 'integer', '
				Output flag for the iluter matrix solver. Larger numbers mean increasing output level.
			', """2"""),
   
      'b2ux5p_style' : ('Numerics', 'integer', '
				Choose the type of matrix solver. Style.eq.0 = iluter, Style.eq.1 = 5-pt stencil, Style.eq.2 = MA28. NOTE: Only style.eq.2 will give good results.
				Other values are NOT recommended!
			', """2"""),
   
      'b2ux7p_nltrsol' : ('Output', 'integer', '
				Output flag for the iluter matrix solver. Larger numbers mean increasing output level.
			', """0"""),
   
      'b2ux7p_style' : ('Numerics', 'integer', '
				Choose the type of matrix solver. Style.eq.0 = iluter, Style.eq.1 = 5-pt stencil, Style.eq.2 = MA28copy. Style.eq.3 = SDRV from YSMP
				NOTE: Only style.eq.3 will give good results.
				Other values are NOT recommended!
			', """3"""),
   
      'b2ux9p_nltrsol' : ('Output', 'integer', '
				Output flag for the iluter matrix solver. Larger numbers mean increasing output level.
			', """0"""),
   
      'b2ux9p_style' : ('Numerics', 'integer', '
				Choose the type of matrix solver. Style.eq.0 = iluter, Style.eq.1 = 5-pt stencil, Style.eq.2 = MA28copy. NOTE: Only style.eq.2 will give good results.
				Other values are NOT recommended!
			', """2"""),
   
      'b2xzdd_zero_dead_and_core' : ('Numerics', 'integer', '
				If 1 then zero passed sources in dead regions,
				If 2 zero passed sources in dead regions and core boundary cells
				If 0 then SKIP
			', """1"""),
   
      'b2yrdr_ns' : ('Output', 'integer', '
				New number of species desired when reading a new atomic rates file using b2yr.exe. Must be specified within b2yr.dat.
				To be used for checking atomic rates after bundling and before any plasma state files have been created or converted, i.e. when the number of species in the atomic rates file b2frates does not match the number of species declared in the run parameters file b2fpardf.
			', """ns"""),
   
      'b2ytdr_ndepth1' : ('Run', 'integer', '
				New resolution of target depth desired when creating a new initial state file using b2yt.exe. Must be specified within b2yt.dat.
			', """ndepth_nml"""),
   
      'b2ytdr_non_commensurate' : ('Run', 'integer', '
				When set to 1, b2yt will attempt to interpolate a plasma solution and create new input files for a new grid which is not commensurate to the original grid, but still has the same topology.
			', """0"""),
   
      'b2ytdr_ns' : ('Run', 'integer', '
				New number of species desired when creating a new initial state file using b2yt.exe. Must be specified within b2yt.dat.
			', """ns"""),
   
      'b2ytdr_rescale_neutrals' : ('Run', 'real', '
				Rescaling of neutral densities by rescale_neutrals when creating a new initial state file using b2yt.exe. Must be specified within b2yt.dat.
			', """1.0"""),
   
      'eirene_ank_mods' : ('Numerics', 'integer', '
				If ank_mods.ne.0, then uses an additional scheme to ensure particle balance as the B2 solution evolves, due to the internal iteration scheme, away from the plasma background on which the Eirene sources were originally computed at the beginning of the time-step. The user is referred to the text in $SOLPSTOP/doc/Source_Scaling_in_B2.pdf for a full description of the method used.
			', """0"""),
   
      'eirene_dpc_fix' : ('Numerics', 'integer', '
				If dpc_fix.eq.1, then uses the true particle source from the stratum. If dpc_fix.eq.2, sets this particle source to zero.
				The equivalent of the old behaviour is dpc_fix.eq.0 and is wrong!
			', """1"""),
   
      'eirene_extrap' : ('Numerics', 'integer', '
				If eirene_extrap.eq.1, then guard cell plasma parameter values are calculated from the neighbouring real cell values.
				If eirene_extrap.eq.0, the guard cell values are used unchanged.
			', """1"""),
   
      'eirene_ionising_core' : ('Physics', 'integer', '
				If <> 0 then recycles the neutral flux having crossed the core boundary within Eirene as ions. The recycling is surface-averaged, and neutrals come back as fully-stripped ions.
				'eirene_ionizing_core' is an alias for this switch.
				If the value = 1, then the flux is added by direct modification of the sources in the guard cells --- this will only work if a standard flux boundary condition is applied at that boundary.
				If the value is < 0, then the absolute value specifies which boundary in b2.boundary.parameters is to be used. This will only work for the new type 13 boundary condition.
			', """0"""),
   
      'eirene_fixuub' : ('Numerics', 'integer', '
				Switch for toggling between conversion rules for velocities between B2.5 and Eirene.
				If fixuub.eq.0, the velocity passed to Eirene is face-centered and computed from the fluxes at the cell faces.
				If fixuub.eq.1, the velocity passed to Eirene is cell-centered and computed from the fluxes at the cell faces.
				If fixuub.eq.2, the velocity passed to Eirene is cell-centered and computed as the cell-centered parallel velocity from B2.5 multiplied by the pitch angle.
			', """0"""),
   
      'eirene_format' : ('Output', 'string', '
				This switch is to be provided within b2yt.dat to indicate to the b2yt converter the format of the original Eirene input.dat file to be modified. The accepted values are (case-insensitive):
				'old' for input files from SOLPS4.0 and SOLPS5.0 runs using "old" Eirene_96
				'new' for input files from SOLPS4.0 and SOLPS5.0 runs using "new" Eirene_99
				'facelift' for input files from SOLPS5.1 runs
				'juelich' for input files from Juelich Eirene versions (2008 and younger)
				'iter' for input files from SOLPS4.2/4.3 and SOLPS-ITER runs
			', """iter"""),
   
      'eirene_lhalpha' : ('Physics', 'integer', '
				If 0 then no calculation of halpha in wneutral, otherwise halpha is calculated
			', """1"""),
   
      'eirene_lvib' : ('Physics', 'integer', '
				If 0 then the sigadd4 (molecular ions) and sigadd5 (negative ions) contributions to the halpha in wneutral are not included, otherwise they are
			', """0"""),
   
      'eirene_mc_linearisation' : ('Numerics', 'integer', '
				Specifies the type of linearisation used in the sources derived from the Monte-Carlo neutrals. If linearisation.eq.0, all sources are fed to the constant term, if linearisation.eq.1, positive terms go in the constant term, and negative terms in the proportional term. 'eirene_mc_linearization' is an alias for this switch.
			', """1"""),
   
      'eirene_mc_output_style' : ('Output', 'integer', '
				If non-zero, prints sources computed by Eirene. If greater than 1, prints them on every use of the recycling sources, not just when they are computed.
			', """1"""),
   
      'eirene_neutr_avg' : ('Numerics', 'integer', '
				If eirene_neutr_avg.gt.0, then Eirene sources are accumulated and averaged until eirene_neutr_avg+1 steps, at which point the averaging process is reset. Note that only one of b2stbr_eir_src_nhist, eirene_neutr_avg, or eirene_underrelax may be nonzero.
			', """0"""),
   
      'eirene_print_minmax' : ('Numerics', 'integer', '
				Print min and max values of te, ti, na & ua
			', """0"""),
   
      'eirene_repeat_first_call' : ('Physics', 'integer', '
				If > 0 then repeats the first call to eirene in eirene_mc so many times.
				Useful if a density feedback gas puff is being used because the flux passed to Eirene on its first call is ignored (instead the value in the Eirene input file is used).
			', """1"""),
   
      'eirene_underrelax' : ('Numerics', 'integer', '
				If eirene_underrelax.gt.0, then an underrelaxation scheme is used for the Eirene sources, with an underrelaxation ratio of 1/eirene_underrelax.
				Note that only one of b2stbr_eir_src_nhist, eirene_neutr_avg, or eirene_underrelax may be nonzero.
			', """0"""),
   
      'eirene_use_recyceir' : ('Physics', 'integer', '
				If > 0 use recyceir (non species dependent) to specify the recycling* coefficients, else if 0 use recyc (species dependent).
			', """1"""),
   
      'ma28_nwrite' : ('Output', 'integer', '
				If nwrite.gt.0, prints the content of the sparse matrix in the b2_matrix file, for the first nwrite calls.
			', """0"""),
   
      'neoclassical_ic' : ('Physics', 'integer', '
				..set the contribution ic in NEOART
				  0 --- classical particle flux
				  1 --- banana plateau contribution
				  2 --- Pfirsch-Schlueter contribution
				  3 --- both banana and PS
				  4 --- all contributions
				  mind that B2 already calculates the classical transport !
				  avoid double transport, 0+4 for cross checks only !
			', """3"""),
   
      'solps_version' : ('Output', 'string', '
				This switch is to be provided within b2yt.dat to indicate to the b2yt converter the format of the original fort.44 file to be modified. The accepted values are (case-insensitive):
				'4.3' for a fort.44 file produced from SOLPS4.3 runs
				'5.0' for a fort.44 file produced from SOLPS5.0 runs
				'5.1' for a fort.44 file produced from SOLPS5.1 runs
				'5.2' for a fort.44 file produced from SOLPS5.2 runs
				'iter' for input files from SOLPS-ITER runs (no conversion necessary)
			', """iter"""),
   
}
