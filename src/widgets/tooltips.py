# Generated with create-tooltips.xslt
b2mn_tooltips = {
   
'b2mndr_ntim' : """
					Number of timesteps desired in this run. If ntim.eq.0, the code simply reads the input file and creates the b2fplasma and b2fstate files corresponding to the present plasma state. This parameter limits the number of time steps.
				""",
   
'b2mndr_dtim' : """
					Timestep (in seconds).
				""",
   
'b2mndt_nstg0' : """
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
				""",
   
'b2mndt_nstg1' : """
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
				""",
   
'b2mndt_nstg2' : """
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
				""",
   
'b2mndt_rxf' : """
					Main under-relaxation parameter.
				""",
   
'b2mndr_mvinc' : """
					Specifies the number of timesteps between movie output. If greater than 1 and the last timestep does not correspond to a planned frame, an extra endstate frame is added.
				""",
   
'b2mndr_mvnum' : """
					Specifies the maximum number of instances at which movie data will be output.
				""",
   
'b2mndr_b2time' : """
					Specifies the number of timesteps between writes of the time-dependent file. If b2time.gt.0, always writes out on the last timestep.
				""",
   
'b2mndr_na0eps' : """
					This switch from SOLPS5.x has been replaced with 'b2mndr_na_min' and 'b2mndr_na_new'.
					CHECK VALIDITY!!!
				""",
   
'b2mndr_na_min' : """
					Minimal density maintained in all cells for all species. It must be true that na_min is smaller than na_new, as well as any of the initial densities provided in b2ai.dat.
					This switch replaces 'b2mndr_na0eps' from SOLPS5.x.
				""",
   
'b2mndr_na_new' : """
					Minimal density maintained in all cells for all species. It must be true that na_min is smaller than na_new, as well as any of the initial densities provided in b2ai.dat.
					This switch replaces 'b2mndr_na0eps' from SOLPS5.x.
				""",
   
'b2mndr_savecpu' : """
					CPU time interval after with save files plasmastate.xxxx are written. These can be used, in conjunction with the b2co.exe instruction, to recover a crashed run.
					CHECK VALIDITY!!!(badly stated description)
				""",
   
'b2ux5p_nltrsol' : """
					Output flag for the iluter matrix solver. Larger numbers mean increasing output level.
				""",
   
'b2ux5p_style' : """
					Choose the type of matrix solver. Style.eq.0 = iluter, Style.eq.1 = 5-pt stencil, Style.eq.2 = MA28. NOTE: Only style.eq.2 will give good results.
					Other values are NOT recommended!
				""",
   
'b2stbc_sna0ep' : """
					Small level sources introduced in all cells.
				""",
   
'b2trcl_lluciani' : """
					If lluciani.ne.0, then transport coefficients on cells belonging to  closed field lines are modified according to the Luciani model.
					If lluciani.eq.1, the standard connection length formulation is used.
					If lluciani.eq.2, the old SOLPS4.0 formulation is used for backward compatibility.
					If lluciani.eq.3, Spb's new form Luciani's coefficient.
				""",
   
'b2news_potit' : """
					Maximum number of iterations in the potential equation.
					It must hold that potitmin < potit.

					CHECK VALIDITY!!! (I added a reserved symbol "less than" in the description value)
				""",
   
'b2news_potitmin' : """
					Minimum number of iterations in the potential equation.
					It must hold that potitmin < potit.
					
					CHECK VALIDITY!!! (I added a reserved symbol "less than" in the description value)
				""",
   
'b2news_potok' : """
					Target residual for the potential equation.
				""",
   
'b2trcl_lvis21' : """
					If lvis21.ne.0, then the viscosities are modified according to the 21-moment approach. This should only be used for multi-fluid runs. This switch should not be used along with 'b2tfhe_vis_par' to avoid double-counting of classical viscosity effects.
				""",
   
'b2trcl_lthf21' : """
					If lthf21.ne.0, then the heat transfer model is modified according to the 21-moment approach. This should only be used for multi-fluid runs.
				""",
   
'b2tfhe_neutral' : """
					Real parameter which multiplies ion-neutral current.
					If b2tfhe_neutral is 0 then ion-neutral current is switched off otherwise ion-neutral current is switched on.
				""",
   
'b2tfhe_vis_par' : """
					Real parameter which multiplies current driven by parallel viscosity. 
					If b2tfhe_vis_par is 0 then viscosity-driven current is switched off otherwise viscosity-driven current is switched on.
				""",
   
'b2news_facdrift_target' : """
					One of the ramping parameters for facdrift, which multiplies the diamagnetic terms.
					The code is started on the first time step with facdrift=facdrift_start.
					If facdrift_target.ne.facdrift_start, then, on each time step, facdrift is multiplied by facdrift_inc. If the code does not converge on the timestep, facdrift is decreased by facdrift_dec. A facdrift profile is also possible, see Numerics section for details.

					CHECK VALIDITY!!! (Description is not very specific)
				""",
   
'b2news_facdrift_dec' : """
					One of the ramping parameters for facdrift, which multiplies the diamagnetic terms.
					The code is started on the first time step with facdrift=facdrift_start.
					If facdrift_target.ne.facdrift_start, then, on each time step, facdrift is multiplied by facdrift_inc. If the code does not converge on the timestep, facdrift is decreased by facdrift_dec. A facdrift profile is also possible, see Numerics section for details.

					CHECK VALIDITY!!! (Description is not very specific)
				""",
   
'b2news_facdrift_inc' : """
					One of the ramping parameters for facdrift, which multiplies the diamagnetic terms.
					The code is started on the first time step with facdrift=facdrift_start.
					If facdrift_target.ne.facdrift_start, then, on each time step, facdrift is multiplied by facdrift_inc. If the code does not converge on the timestep, facdrift is decreased by facdrift_dec. A facdrift profile is also possible, see Numerics section for details.

					CHECK VALIDITY!!! (Description is not very specific)
				""",
   
'b2news_facdrift_start' : """
					One of the ramping parameters for facdrift, which multiplies the diamagnetic terms.
					The code is started on the first time step with facdrift=facdrift_start.
					If facdrift_target.ne.facdrift_start, then, on each time step, facdrift is multiplied by facdrift_inc. If the code does not converge on the timestep, facdrift is decreased by facdrift_dec. A facdrift profile is also possible, see Numerics section for details.

					CHECK VALIDITY!!! (Description is not very specific)
				""",
   
'b2news_facExB_target' : """
					One of the ramping parameters for facExB, which multiplies the ExB terms. Same treatment as for facdrift.

					CHECK VALIDITY!!! (I changed the description a bit
					)
				""",
   
'b2news_facExB_dec' : """
					One of the ramping parameters for facExB, which multiplies the ExB terms. Same treatment as for facdrift.

					CHECK VALIDITY!!! (I changed the description a bit
					)
				""",
   
'b2news_facExB_inc' : """
					One of the ramping parameters for facExB, which multiplies the ExB terms. Same treatment as for facdrift.

					CHECK VALIDITY!!! (I changed the description a bit
					)
				""",
   
'b2news_facExB_start' : """
					One of the ramping parameters for facExB, which multiplies the ExB terms. Same treatment as for facdrift.

					CHECK VALIDITY!!! (I changed the description a bit
					)
				""",
   
'b2stbc_fchy_dia_coreonly' : """
					If fchy_dia_coreonly.eq.1, the neoclassical current and diamagnetic heat flux convective boundary conditions are only applied on the core boundary.
					If fchy_dia_coreonly.eq.0, those are applied to all boundaries, including PFR, North SOL edge and diverted island center boundary.
				""",
   
'b2stbc_boundary_namelist' : """
					Namelist file indicators. If xxx_namelist.eq.1, then the code looks for the file b2.xxx.parameters, in which it expects to find the xxx namelist.
					If 'b2stbc_boundary_namelist' is set to 1 in b2mn.dat then the boundary conditions are read in fromb2.boundary.parameters instead of being taken from the file created by b2ah and possibly modified in b2mn.dat.

					CHECK VALIDITY!!! (I added 2 descriptions I found)
				""",
   
'b2srdt_numerics_namelist' : """
					Namelist file indicators. If xxx_namelist.eq.1, then the code looks for the file b2.xxx.parameters, in which it expects to find the xxx namelist.
				""",
   
'b2srdt_transport_namelist' : """
					Namelist file indicators. If xxx_namelist.eq.1, then the code looks for the file b2.xxx.parameters, in which it expects to find the xxx namelist.
				""",
   
'b2srdt_neutrals_namelist' : """
					Namelist file indicators. If xxx_namelist.eq.1, then the code looks for the file b2.xxx.parameters, in which it expects to find the xxx namelist.
				""",
   
'b2mwti_jxi' : """
					Cell index, on the basis mesh, of the inner midplane. Default value depends on geometry:
					Single-null : jxi=leftcut1(1)+(rightcut1(1)-leftcut1(1))/4, i.e. one quarter of the way between the two cuts.
					Double-null : jxi=(rightcut1(1)+rightcut1(2))/2, i.e. halfway between the two inner cuts.
					Straight geometry : jxi=nx/4
				""",
   
'b2mwti_jxa' : """
					Cell index, on the basis mesh, of the outer midplane. Default value depends on geometry:
					Single-null : jxa=rightcut1(1)-(rightcut1(1)-leftcut1(1))/4, i.e. three quarters of the way between the two cuts.
					Double-null : jxa=(rightcut1(1)+rightcut1(2))/2, i.e. halfway between the two outer cuts.
					Straight geometry : jxa=3*nx/4
				""",
   
'b2tlh0_alpha' : """
					One of the parameter for the flux limit to the heat conductivity of the neutrals.
					Alpha is a multiplier to the classical flux limit value.
					The larger alpha is, the weaker the flux limit is.
					The smaller gamma is, the stronger the flux limit is. If alpha.eq.0, no flux limit is applied.
				""",
   
'b2tlh0_gamma' : """
					One of the parameter for the flux limit to the heat conductivity of the neutrals.
					Gamma is the exponent used in the flux-limiting formula.
				""",
   
'b2tlh0_flux_limit_min_ti' : """
					One of the parameter for the flux limit to the heat conductivity of the neutrals.
					flux_limit_min_ti specifies the minimum ti to be used (in eV)
				""",
   
'b2mndr_eirene' : """
					Turns on coupling with the Eirene Monte-Carlo neutral code if non-zero.
					To be used, the code must be compiled with the -DB25_EIRENE option.
				""",
   
'b2stbc_feedback' : """
					If feedback.eq.1, turns on feedback mode for the boundary conditions.
					See Physics section for more details. Equivalent to LFEEDBACK=.true. in the b2.boundary.parameters namelist.
				""",
   
'b2stbc_nesepm_sol' : """
					One of the feedback switches and it requires that b2stbc_feedback.ne.0 or that lfeedback=.true. in b2.boundary.parameters. The feedback is done as a boundary condition and is under-relaxed using the* b2stbc_...._alpha switches.

					One of  the density feedback switches. nesepm is the outer midplane separatrix electron density. This is controlled through particle input of main plasma species isfeedback through the core boundary. nesepm_sol is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the SOL region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the SOL North boundary (See Geometry section for the SOL North boundary index solregno).

					CHECK VALIDITY!!! (I edited the text a bit. Still, it requires more editing.)
				""",
   
'b2stbc_diagno' : """
					Controls level of output in b2stbc and subservient routines.
					Level 1 (diagno.ge.1) output includes wrong_flow warnings, transport coefficients at the (nx/2,ny) basis mesh position, the solution found for the given heat flux at constant temperature bc, and all feedback diagnostics.
					Level 2 output (diagno.ge.2) includes the integral current correction, the boundary sources on the first call, excessive sound speeds, and the iterative progress to the given heat flux at constant temperature bc. 
					Level 3 output (diagno.ge.3) includes the boundary sources on each call, and the boundary.prt file listing all boundary cells.
				""",
   
'b2stbc_solregno' : """
					solregno is the boundary index of the SOL North boundary in the input files b2ah.dat and b2mn.dat. For a standard single-null case, solregno is 3. For a standard double-null case, solregno for the outer SOL North boundary would be 7.
				""",
   
'ank_tracing' : """
					If ank_tracing.ge.1, additional tracing output from Andrei Kukushkin is produced, in files to be found in the tracing/ directory inside the run directory. The traces will be written every ank_tracing iteration.	
				""",
   
'b2agfs_Bt_adjust' : """
					Bt_adjust - integer.
					If the mesh is offset (See b2agfs_xoffset, b2agfs_yoffset below) and Bt_adjust.eq.1, then the magnetic field is recomputed, keeping the pitch constant but changing the toroidal field magnitude according to Bt = Bt0/R. To be used in b2ag.dat.
				""",
   
'b2agfs_Bt_rescale' : """
					Bt_rescale - real*8.
					The magnetic field will be multiplied by Bt_rescale. All components of the field are scaled together. To be used in b2ag.dat.
				""",
   
'b2agfs_Bt_reversal' : """
					Bt_reversal - integer.
					If Bt_reversal.eq.1, then the sign of the toroidal field component only is reversed. The sign convention used is that a positive toroidal field leads to a Bx(grad(B)) direction pointing down, so B is out of the page when looking at the usual view of the poloidal plane with the center line on the left.
					To be used in b2ag.dat.
				""",
   
'b2agfs_geom_match_dist' : """
					Distance used as the matching criterion when reading the geometry file.
				""",
   
'b2agfs_geometry' : """
					local_sonnet - character string.
					local_sonnet is the file name of the geometry file to be read.
					The file will be looked for in the run directory, in the ../baserun directory and in $SOLPSTOP/data/meshes. To be used in b2ag.dat.

					CHECK VALIDITY!!! (type)
				""",
   
'b2agfs_min_pitch' : """
					Minimum allowed value for the pitch angle (in degrees) at the plates.
				""",
   
'b2agfs_nncut' : """
					Number of topological cuts in geometry. Needed only to force a different value from the one computed automatically by b2ag.
				""",
   
'b2agfs_periodic_bc' : """
					periodic_bc - integer.
					periodic_bc specifies if this is either an island or limiter geometry.
					If periodic_bc.eq.1 then island/limiter treatment is turned on.
					We differentiate between the two case through nncut:
					 nncut.eq.0 = limiter case
					 nncut.ge.1 = island divertor case (there should be nncut islands then)
					The case periodic_bc.eq.-1 is used to remove tranverse physics in 1-D cases.
					If periodic_bc.eq.0 then we have the usual treatment. No other values are currently allowed. To be used in b2ag.dat.
				""",
   
'b2agfs_pit_rescale' : """
					pit_rescale - real*8.
					The magnetic field line pitch will be multiplied by pit_rescale.
					This means that the poloidal field component is multiplied by pit_rescale, while the toroidal field component is left unchanged. To reverse the plasma current direction, set pit_rescale to -1.0.
					The sign convention used is that a positive poloidal field points in the direction of increasing <ix>. Be mindful however that, when inverting the sign of the poloidal magnetic field, you are also inverting the direction of the parallel velocity. You will then need to use the 'b2mndr_inverse_ua' switch to correct for that.
					To be used in b2ag.dat.
				""",
   
'b2agmt_1d_width' : """
					For 1-D cases, gives the width of the domain (in m) in the third (toroidal) dimension.
				""",
   
'b2agmx_pbs_from_basis_mesh' : """
					If pbs_from_basis_mesh.eq.0, the pbs array is computed from values on the actual working mesh (old treatment).
					If pbs_from_basis_mesh.eq.1, the pbs array is computed from values on the (possibly) finer basis mesh from the geometry file and the contributions from each basis cell are added to obtain the value on the working mesh.
					In both cases, mind the value of 'b2news_area_fix', which should be also declared in b2ag.dat if the non-default behaviour is wanted.
				""",
   
'b2agsi_isymm' : """
					isymm - integer.
					isymm specifies the type of symmetry of the geometry: isymm.eq.0
					implies a slab geometry, isymm.eq.1.or.isymm.eq.2 imply rotational symmetry about the crx=0 axis, and isymm.eq.3.or.isymm.eq.4
					indicate rotational symmetry about the cry=0 axis.
					Other values are not allowed.
					isymm.eq.1.or.isymm.eq.3 mean a toroidal geometry case, i.e. with a toroidal (out-of-plane) magnetic field component.
					isymm.eq.2.or.isymm.eq.4 mean a cylindrical geometry case, i.e.
					no toroidal magnetic field component.
					To be used in b2ag.dat.
				""",
   
'b2aidr_read_b2fstate' : """
					If read_b2fstate.ne.0, b2aidr will read an existing b2fstate file and append to it a flat state description for additional new species being introduced in the run.
				""",
   
'b2ardr_fix_cx' : """
					It is used to "correct" the CX data
					 0 => do not fix
					 1 => only fix H if CX data is < 1e-40 [default]
					 2 => fix if CX data is < 1e-40
					 3 => fix H
					 4 => fix all
					At the moment the only species with CX data in ADAS is C. Be careful with options that use the fit formula other than for H. 
					See the comments in ratstr.F for the origin of the fit formula used to "fix" the CX data.
				""",
   
'b2ardr_fix_recomb' : """
					When changed from 0, and if the ADAS option is in use, then uses the PRB file to add the contribution arising from is-->is-1 processes.
					This term includes the Bremsstrahlung.
					The default option ('0') only contains the Bremsstrahlung for the is-->is-1 process.
					This option should be used with the 'b2stel_fix_recomb_energy' option b2mn.dat set to '1'. See 'Physics' section.
					*** Use with caution! ***
				""",
   
'b2ardr_no_weisheit' : """
					When set to 1, disables the correction of the hydrogen atomic rate data with the Weisheit data using ratwei. *** Use with caution! ***
				""",
   
'b2ardr_no_smoothing' : """
					When set to 1, disables the tail smoothing for of rate coefficients to represent the effect of a power-law tail on the distribution function. It has been added for compatibility with SOLPS4.3
				""",
   
'b2mndr_astra' : """
					Turns on coupling with the ASTRA core transport code if non-zero.
					To be used, the code must be compiled with the -DASTRA option.
				""",
   
'b2mndr_atomic_physics_rescale' : """
					If atomic_physics_rescale is not 0, then the code will rescale the rates stored in b2frates according to the multipliers given in the b2.atomic_physics_rescale.parameters inputfile before making use of them.
				""",
   
'b2mndr_cdfmovietim' : """
					Another option for movie output. Give the real-time interval between movie frames.
				""",
   
'b2mndr_coronal_model' : """
					Turns on the coronal model if coronal.ne.0. I.e., the reaction rates of all reactions are made density-independent, and the value computed at the lowest density (given in b2ar.dat) is used.
				""",
   
'b2mndr_cpu' : """
					CPU limit. Is cpu.eq.0.0, no CPU limit is enforced. Otherwise, the code stops smoothly after it has been running for at least 'cpu' CPU seconds.
					CHECK VALIDITY!!!(changed "is" to "it")
				""",
   
'b2mndr_density_rescale' : """
					Multiplier of all densities on the first timestep.
				""",
   
'b2mndr_dtim' : """
					Timestep (in seconds).
				""",
   
'b2mndr_eirene' : """
					Turns on coupling with the Eirene Monte-Carlo neutral code if non-zero.
					To be used, the code must be compiled with the -DB25_EIRENE option.
				""",
   
'b2mndr_elapsed' : """
					Elapsed time limit. Is elapsed.eq.0.0, no time limit is enforced.
					Otherwise, the code stops smoothly after is has been running for at least 'elapsed' wall clock seconds.
				""",
   
'b2mndr_etim' : """
					etim specifies the end time. Only active if etim > stim.
				""",
   
'b2mndr_hz' : """
					hz has been introduced into the new form of the parallel momentum balance equation.
					If fac_hz = 0.0 then hz = 1 and old form of equations is used.
					If fac_hz = 1.0 then new form of equations is used.
				""",
   
'b2mndr_inverse_ua' : """
					If inverse_ua.eq.1, the code will produce a 'b2fstati_with-ua' file that contains the same plasma information, but with the opposite sign convention for the parallel velocity. The run will then proceed with the new velocities with their sign inverted.
				""",
   
'b2mndr_ismain' : """
					ismain identifies the index of the main plasma species. 
					It must hold that ismain is not a neutral species.
				""",
   
'b2mndr_mvinc' : """
					Specifies the number of timesteps between movie output. If greater than 1 and the last timestep does not correspond to a planned frame, an extra endstate frame is added.
				""",
   
}
