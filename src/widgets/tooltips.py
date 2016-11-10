# Generated with create-tooltips.xslt
b2mn_tooltips = {
   
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
						CPU limit. If cpu.eq.0.0, no CPU limit is enforced. Otherwise, the code stops smoothly after it has been running for at least 'cpu' CPU seconds.
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
   
'b2mndr_mvnum' : """
						Specifies the maximum number of instances at which movie data will be output.
					""",
   
'b2mndr_na_min' : """
						Minimal density maintained in all cells for all species.
						It must be true that na_min is smaller than na_new, as well as any of the initial densities provided in b2ai.dat.
						This switch replaces 'b2mndr_na0eps' from SOLPS5.x.
					""",
   
'b2mndr_na_new' : """
						Initial density put in all cells for all new species if not overwritten by initial state file.
						This switch replaces 'b2mndr_na0eps' from SOLPS5.x.
					""",
   
'b2mndr_ntim' : """
						Number of timesteps desired in this run. If ntim.eq.0, the code simply reads the input file and creates the b2fplasma and b2fstate files corresponding to the present plasma state.
					""",
   
'b2mndr_plasmatim' : """
						Another option for plasma state file output. Give the real-time interval between succesive write-ups of plasmastate files, in addition to the ones written at regular CPU intervals.
					""",
   
'b2mndr_rescale_neutrals' : """
						Multiplier to the neutral density on the first timestep.
					""",
   
'b2mndr_rescale_neutrals_sources' : """
						Multiplier to the neutral sources (either computed by Eirene or the corresponding rate coefficients).
					""",
   
'b2mndr_savecpu' : """
						CPU time interval after with save files plasmastate.xxxx are written.
						These can be used, in conjunction with the b2co.exe instruction, to recover a crashed run.
					""",
   
'b2mndr_stim' : """
						stim specifies the initial time --- default 0.
						If set to a positive or zero value, this overwrites the time value read from b2fstati.
						If set to a negative value, the run continues from the time read in b2fstati.
					""",
   
'b2mndr_tally' : """
						Specifies the number of timesteps between writes of tallies.
						If tally.gt.0, always writes out on the last timestep.
					""",
   
'b2mndr_trantim' : """
						Produces a numbered 'tran' file every trantim real-time seconds.
						An endstate file is written if it falls between scheduled write-up times.
						Only available within the -DJET environment.
					""",
   
'b2mndt_density_control' : """
						Feedback on the total heavy particle density. If density_control.ne.0, the sum of all densities is kept constant.
					""",
   
'b2mndt_moitlv' : """
						Controls detailed monitoring output. moitlv.eq.-1 means no output, moitlv.eq.0 means output once per timestep, moitlv.eq.1 means output once per nstg0 iteration, moitlv.eq.2 means output once per nstg1 iteration and moitlv.eq.3 means output once per nstg2 iteration. See 'b2mndr_nstg?' description in Run section for more details.
					""",
   
'b2mndt_moqtlv' : """
						Controls quick trace output. moqtlv.eq.-1 means no output, moqtlv.eq.0 means output once per timestep, moqtlv.eq.1 means output once per nstg0 iteration, moqtlv.eq.2 means output once per nstg1 iteration and moqtlv.eq.3 means output once per nstg2 iteration. See 'b2mndr_nstg?' description in Run section for more details.
					""",
   
'b2mndt_ntim_step_out' : """
						When set to a value of 'K', residuals at each K-th step will be written in b2ftrace. It helps to avoid a huge b2ftrace files during long time run.
					""",
   
'b2mndt_rxf' : """
						Main under-relaxation parameter.
					""",
   
'b2mndt_style' : """
						When set to '1', all important variables will be calculated for the first step.
						This avoids a jump of residuals when continuing the run.
					""",
   
'b2mndt_use_b2srst' : """
						Switches off the stabilization of the source coefficients.
					""",
   
'b2mwqt_style' : """
						NOT FOUND!
					""",
   
'b2mwti_ismain0' : """
						Index of the species used to create the 'dp3d?.last10' diagnostic files.
						Defaults to the neutral species associated with ismain. If no such species is declared, the default will be set to ismain. Is expected to either correspond to a neutral species or to ismain.
						If ismain is also defaulted, then will be 0.
					""",
   
'b2mwti_jxa' : """
						Cell index, on the basis mesh, of the outer midplane. Default value depends on geometry:
						Single-null : jxa=rightcut1(1)-(rightcut1(1)-leftcut1(1))/4, i.e. three quarters of the way between the two cuts. Double-null : jxa=(rightcut1(1)+rightcut1(2))/2, i.e. halfway between the two outer cuts.
						Straight geometry : jxa=3*nx/4
					""",
   
'b2mwti_jxi' : """
						Cell index, on the basis mesh, of the inner midplane. Default value depends on geometry:
						Single-null : jxi=leftcut1(1)+(rightcut1(1)-leftcut1(1))/4, i.e. one quarter of the way between the two cuts. Double-null : jxi=(rightcut1(1)+rightcut1(2))/2, i.e. halfway between the two inner cuts.
						Straight geometry : jxi=nx/4
					""",
   
'b2mwti_target_offset' : """
						The diagnostic values from b2time.nc use guard cell values if target_offset.eq.0, and values from the neighbouring real cell if target_offset.eq.1. Fluxes are not affected.
					""",
   
'b2news_area_fix' : """
						When area_fix.eq.0, recovers old SOLPS5.0 behaviour.
						If area_fix.ge.1, then certain computations of poloidal velocities are done by dividing flows by the area normal to the flux tube as opposed to the area of contact.
						If area_fix.ge.2, then additionally this treatment is used for the parallel contact area used in determining plasma flux limiters.
						If area_fix.ge.3, then additionally this treatment is used for all parallel contact areas.
					""",
   
'b2news_BoRiS' : """
						The poloidal convective heat flux contains a prefactor of (3/2+BoRiS). The default gives us the internal energy equation. The value BoRiS = 1.0 gives us the total energy equation.
						Only for use to benchmark with codes using the total energy equation. When used, the meaning of fhe and fhi changes from internal energy fluxes to total energy fluxes.
					""",
   
'b2news_coriolis' : """
						If coriolis.ne.0, the Coriolis force terms will be included in the solution of the momentum equations.
					""",
   
'b2news_do_2nd_b2npco_call' : """
						If do_2nd_b2npco_call.eq.1, perform a second call to the density equation solve to improve particle balance, as done in SOLPS4.
					""",
   
'b2news_ExB' : """
						Real parameter which multiplies ExB flows. If b2news_ExB.eq.0 and b2news_facExB_start.eq.0 then ExB flows are switched off. If b2news_ExB is non-zero, then ExB flows are multiplied by that constant throughout the run.
						See also Run section on switches b2news_facExB_... for more details. A spatial fac_ExB profile is also possible, see Numerics section for details.
					""",
   
'b2news_guard_flows' : """
						If guard_flows.eq.0, flows between neighbouring guard cells are blocked.
						If guard_flows.eq.1, flows between neighbouring guard cells are kept.
						If guard_flows.eq.2, particle flows between neighbouring guard cells are blocked for density equation and the incorrect corner values are replaced by interpolated values. It is recommended 2.
					""",
   
'b2news_ncallout' : """
						If the iteration number is equal to ncallout, then several output files 'b2ne_npmo', 'b2ne_xppb', 'b2ne_npco', 'b2ne+nppo' which detail the convergence behaviour and residuals.
					""",
   
'b2news_no_b2sral_call' : """
						If no_b2sral_call.eq.0, add an additional call to recompute the source in b2news_ to reproduce the behaviour from SOLPS4.
					""",
   
'b2news_no_solve' : """
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
					""",
   
'b2news_poteq' : """
						If poteq.eq.0, the potential equation is jumped over and not solved.
						If poteq.eq.2, the potential is set to 3.1*Te/qe as per SOLPS4.0.
						If poteq.eq.1, the potential equation is solved according to the no_solve switch settings.
						If poteq.ne.1, then 'b2tfhe_no_current'must be set to '1'.
					""",
   
'b2news_potok' : """
						Target residual for the potential equation.
					""",
   
'b2news_ramp_slow' : """
						If ramp_slow.eq.0 (default), the ExB and diamagnetic drifts multipliers are ramped on each call of b2news, otherwise they are only changed on the first call of the nstg loop on the timestep.
					""",
   
'b2news_recalculate_contributions' : """
						If recalculate_contributions.eq.0, turns off recomputation of sources when wrong_flow flag is active.
					""",
   
'b2news_re_eval_prtls_fluxes' : """
						If re_eval_prtls_fluxes.eq.1, the particle fluxes are recomputed at the end of b2news_. This is necessary for rescaling of the Eirene sources during coupled runs, so this switch is superceded by use_eirene, and also needed to reproduce SOLPS4 runs.
					""",
   
'b2news_vis' : """
						Alternative name of the variable in the code is fac_vis_scalar
					""",
   
'b2npco_rxg' : """
						rxg specifies a special under-relaxation parameter. A term of the form "abs(residual)/rxg" is added to the diagonal of the matrix of the correction equation, with the effect of limiting the computed correction. rxg is dimensionless and of order unity; smaller values of rxg imply stronger damping.
					""",
   
'b2npht_rxg' : """
						rxg specifies a special under-relaxation parameter. A term of the form "abs(residual)/rxg" is added to the diagonal of the matrix of the correction equation, with the effect of limiting the computed correction. rxg is dimensionless and of order unity; smaller values of rxg imply stronger damping.
					""",
   
'b2npht_style' : """
						When set to '1', SPb's form of the program b2sihs_ is called.
						It is recommended '1'.
					""",
   
'b2nph9_style' : """
						When set to '1', SPb's form of the program b2sihs_ is called.
						It is recommended '1'.
					""",
   
'b2npmo_b2sifr_' : """
						When set to '1', the new correct form of the friction force is used.
						The value '0' corresponds to the old SOLPS5.0 treatment.
					""",
   
'b2npmo_modvis' : """
						When set to '1', the new correct form of viscosity is used. It is important for runs with drifts. It is recommended '1'.
						The value '0' corresponds to the old SOLPS5.0 treatment.
					""",
   
'b2npmo_rxg' : """
						Normalisation factor for the parallel momentum equation.
					""",
   
'b2npp7_style' : """
						When set to '1', SPb's form of the program b2usp7_ is called.
						It is recommended '1'.
					""",
   
'b2nxdv_style' : """
						When set to '1', the total friction force cancel is not calculated at the guard boundary cells.
						It is recommended '1'.
					""",
   
'b2nxfc_style' : """
						style specifies the precise form of interpolation used in the computation of flcb and cvcb. When set to '1', SPb's form of the transport terms in the momentum correction equation is used.
						It is recommended '1'.
					""",
   
'b2nxfx_style' : """
						When set to '1', SPb's form of an expression that occurs in the electron-atom thermal force is used.
						It is recommended '1'.
					""",
   
'b2sdia_facgt' : """
						Multiplier of the contribution to electron and ion heat sources from divergence of the gradTxB heat flux. That contribution is also multiplied by facdrift. This term is no longer needed as it has been transferred from being a source to being included in the flows.
					""",
   
'b2sicf_phm0' : """
						Multiplier of the centrifugal force term.
						It is recommended '1.0'.
						The value '0.0' corresponds to the old SOLPS5.0 treatment.
					""",
   
'b2sicf_phm1' : """
						Multiplier of the centrifugal force correction term due to linearization.
						It is recommended '1.0'.
						The value '0.0' corresponds to the old SOLPS5.0 treatment.
					""",
   
'b2sifr_phm0' : """
						Multiplier of the friction term between charged species.
					""",
   
'b2sifr_phm1' : """
						Multiplier of the ehxp term in the thermal force term.
					""",
   
'b2sifr_phm2' : """
						Multiplier of the electron thermal gradient term in the thermal force term.
					""",
   
'b2sigp_style' : """
						When set to '1', SPb's form of the pressure gradient term on the right hand of the momentum balance equation is used.
						It is recommended '1'.
					""",
   
'b2sihs_istyle_Joule_heating' : """
						When set to '1', there is no radial contribution in Joule heating because there are no physical reasons to take it into account.
						The value '0' corresponds to the old SOLPS5.0 treatment.
					""",
   
'b2sihs_phm0' : """
						Multiplier of the contribution to electron heat sources from divergence(ue,ve).
					""",
   
'b2sihs_phm1' : """
						Multiplier of the contribution to ion heat sources from divergence(ua,va).
						This term is superseded by the BoRiS switch if invoked.
					""",
   
'b2sihs_phm2' : """
						Multiplier of the contribution to ion heat sources from viscous heating.
						This term is superseded by the BoRiS switch if invoked.
					""",
   
'b2sihs_phm3' : """
						Multiplier of the contribution to electron heat sources from Joule heating (electron-ion friction).
					""",
   
'b2sihs_phm4' : """
						Multiplier of the contribution to ion heat sources from atom-atom friction.
						This term is superseded by the BoRiS switch if invoked.
					""",
   
'b2sihs_phm5' : """
						Multiplier of the contribution to electron heat sources from divergence of the electrical drift. That contribution is also multiplied by facExB.
					""",
   
'b2sihs_phm6' : """
						Multiplier of the contribution to ion heat sources from divergence of the electrical drift. That contribution is also multiplied by facExB.
					""",
   
'b2sihs_phm7' : """
						Multiplier of the contribution to heat sources from friction due to diamagnetic velocities. Normally already included in 'phm3' term above.
					""",
   
'b2sihs_style' : """
						style determines the form of the strange electron-atom energy transfer term.
					""",
   
'b2sqel_artificial_radiation' : """
						If art_rad.ne.0, then an artificial radiation loss term is added to the electron cooling rate. Art_rad represents the percent fraction of impurities in the plasma.
					""",
   
'b2sqel_phm0' : """
						Multiplier to the ionisation rate coefficient.
					""",
   
'b2sqel_phm1' : """
						Multiplier to the recombination rate coefficient.
					""",
   
'b2sqel_phm2' : """
						Multiplier to the heat loss rate coefficient.
					""",
   
'b2sral_inputfile' : """
						Profiles file indicator. If b2sral_inputfile.eq.1, then the code looks for the file b2.sources.profile in which it expects to find the 'profile' namelist.
						This namelist will contain profiles of sources measured from the location (ixref,iyref) (default is outer midplane separatrix), which is set with the 'set_transport_i[xy]ref' switches.
					""",
   
'b2sral_style' : """
						When set to '0', in the expression of the electron particle flux (fne) the particle flux with drift terms is used and temporary drift velocities on the first call are calculated. When set to '1' or '2', the particle flux without drift terms is used in fne.
						It is recommended '2'.
					""",
   
'b2srsm_diagno' : """
						Controls level of output in b2srsm. If diagno.ge.2, output will be given on every call. If diagno.eq.1, output will be given on main calls only.
					""",
   
'b2srsm_enable' : """
						If enable.ne.0, then the sources for particle, parallel momentum, electron and ion heat are rescaled, for non-boundary cells, if the local timestep exceeds the physics timescale implied by those sources.
					""",
   
'b2stbc_bcpot_16_step' : """
						Frequency (in number of calls to b2stbc_phys) at which the constant value of the potential at the boundaries where BCPOT=16 is applied will be recomputed.
					""",
   
'b2stbc_cbc' : """
						Multiplier to the ExB velocity for sheath boundary conditions in b2stbc_spb and BCMOM=13 case of b2stbc_phys.
					""",
   
'b2stbc_diagno' : """
						Controls level of output in b2stbc and subservient routines.
						Level 1 (diagno.ge.1) output includes wrong_flow warnings, transport coefficients at the (nx/2,ny) basis mesh position, the solution found for the given heat flux at constant temperature bc, and all feedback diagnostics.
						Level 2 output (diagno.ge.2) includes the integral current correction, the boundary sources on the first call, excessive sound speeds, and the iterative progress to the given heat flux at constant temperature bc. 
						Level 3 output (diagno.ge.3) includes the boundary sources on each call, and the boundary.prt file listing all boundary cells.
					""",
   
'b2stbc_fchy_dia' : """
						Multiplier to the neoclassical current and diamagnetic heat flux convective boundary conditions, also multiplied by facdrift.
						Allows use b2stbc_integral_current is fchy_dia.eq.0, forbids it otherwise.
					""",
   
'b2stbc_fchy_dia_coreonly' : """
						If fchy_dia_coreonly.eq.1, the neoclassical current and diamagnetic heat flux convective boundary conditions are only applied on the core boundary.
						If fchy_dia_coreonly.eq.0, those are applied to all boundaries, including PFR, North SOL edge and diverted island center boundary.
					""",
   
'b2stbc_feedback' : """
						If feedback.eq.1, turns on feedback mode for the boundary conditions.
						See Physics section for more details. Equivalent to LFEEDBACK=.true. in the b2.boundary.parameters namelist.
					""",
   
'b2stbc_fix_fch_in_fhe_sheath' : """
						If fix_fch_in_fhe_sheath.eq.0, then the wrong (old) implementation of the FCH contribution to FHE used;
						If fix_fch_in_fhe_sheath.eq.1, then the wrong (second) implementation of the FCH contribution to FHE used;
						If fix_fch_in_fhe_sheath.eq.2, then the correct implementation of the FCH contribution to FHE used;
					""",
   
'b2stbc_integral_current' : """
						If integral_current.gt.0, corrects current sources so that there be no surface current at the North and South edges of the edge plasma.
						The value of integral_current multiplies the correction term added to the current source.
						This setting is incompatible with the normal use of diamagnetic drift terms (facdrift.gt.0.0 .and. b2stbc_fchy_dia.ne.0.0) or neoclassical boundary conditions (b2stbc_neoclassical.gt.0.0).
					""",
   
'b2stbc_istyle_cur_contr_on_S_and_N' : """
						When set to '2', SPB's form of adding currents on the South core boundary is included by using BCPOT=12, and on the SOuth PFR and North boundaries by using BCPOT=13. It is recommended '2', in conjunction with the BCPOT=12 and BCPOT=13 settings, respectively.
						When set to '1', SPb's form of adding currents on South and North boundaries is done explicitly in addition to other existing boundary conditions for the potential equation.
						The old 5.0 calculation is recovered by using the value '0'.
					""",
   
'b2stbc_istyle_fchi' : """
						If '1', explicitly use the expression (bx*cs*na) of particle flux (fna) from boundary condition instead of fna.
					""",
   
'b2stbc_ncallfeedback' : """
						Timestep index after which the feedback in b2stbc is activated.
					""",
   
'b2stbc_neoclassical' : """
						Real parameter which establishes boundary conditions for radial component of the current for North and South boundaries when these lie on closed flux surfaces.
						If b2stbc_neoclassical is 0 then the radial component of the current is zero.
						If b2stbc_neoclassical is not 0 the radial component of the current is given by the neoclassical value. b2stbc_neoclassical is superseded if facdrift.ne.0.
						This cannot be used in conjunction with b2stbc_integral_current below.
					""",
   
'b2stbc_secmodel' : """
						If secmodel.eq.1, then the secondary electron emission coefficient at the plates is computed locally according to a kinetic model, otherwise the default values of cbsch(7,ireg) and/or gammae are used.
					""",
   
'b2stbc_sheath_drift_fix' : """
						If sheath_drift_fix.eq.0, then the drift velocity used in the sheath boundary conditions is the sum of diamagnetic and ExB contributions (old, but likely wrong, treatment). If sheath_drift_fix.eq.1, then the drift velocity used in the sheath boundary conditions is the ExB velocity only (recommended).
					""",
   
'b2stbc_solregno' : """
						solregno is the boundary index of the SOL North boundary in the input files b2ah.dat and b2mn.dat. For a standard single-null case, solregno is 3. For a standard double-null case, solregno for the outer SOL North boundary would be 7.
					""",
   
'b2stbm_impgyro_mod' : """
						Specifies the frequency (in units of full b2 timesteps) at which an externally coupled code providing additional source (for instance a kinetic treatment of trace impurity ions such as IMPGYRO) should be called.
					""",
   
'b2stbm_linearisation' : """
						Same as above, but applied to the sources coming for an externally coupled code providing plasma sources, for instance a kinetic treatment of trace impurity ions. 'b2stbm_linearization' is an alias for this switch.
					""",
   
'b2stbr_core_sources_rescale' : """
						Multiplier to the totally ionised species sources at the core boundary.
					""",
   
'b2stbr_eir_src_nhist' : """
						If b2stbr_eir_src_nhist.gt.1, then Eirene sources are accumulated and a moving average is computed. Note that only one of b2stbr_eir_src_nhist, eirene_neutr_avg, or eirene_underrelax may be nonzero.
					""",
   
'b2stbr_first_flight' : """
						If first_flight.ne.0, turns on the first flight model. See Physics section for additional details.
					""",
   
'b2stbr_first_flight_dl' : """
						Step length (in meters) for computing the first flight model chords.
					""",
   
'b2stbr_first_flight_no_of_flights' : """
						Number of chords started from each start point in the first flight model.
					""",
   
'b2stbr_first_flight_no_of_start_points' : """
						When the first flight model is turned on, this number must be greater than or equal to the number of boundary cells on the mesh.
						Only in cases with special geometries (i.e. limiters, islands, ...) need it be increased beyond the default value above. This variable is only used within the first flight module.
					""",
   
'b2stbr_first_flight_table_size' : """
						Workspace size given to the first flight table.
					""",
   
'b2stbr_output' : """
						Output flag for the first_flight model. If output.ge.1, the files start, end, and fort.88 are created, which contain information about the chords used in the model.
					""",
   
'b2stbr_potential_at_guard_cell' : """
						If potential_at_guard_cell.eq.1, the electric potential used for the computation of the incident energy for sputtering yields is taken as the value in the guard cell. If potential_at_guard_cell.eq.0, the value from the neighbouring real cell is used instead.
					""",
   
'b2stbr_bas_recycled_neutrals_contr' : """
						Introduced for nulling recycling energy when it is zero.
					""",
   
'b2stcx_rg0' : """
						(rg0 for numerical stabilisation; needs experiments.)
					""",
   
'b2stcx_styl0' : """
						Specifies the type of linearisation used in the charge exchange momentum source term.
					""",
   
'b2stel_fix_recomb_energy' : """
						If changed to 1, then the recombination energy (rpi) is added to the electron energy for each recombination. This should only be used if the is-->is-1 energy terms have been included in the electron cooling rates (as done by setting the switch 'b2ardr_fix_recomb' in b2ar.dat to a non-zero value and recalculating b2frates).
						See 'Atomic Physics' section.
						*** Use with caution! ***
					""",
   
'b2stel_phm0' : """
						Multiplier of the recombination contribution to the electron cooling rate (if ADPAK rates are not used because those are already included). Assumes all recombination is three-body.
					""",
   
'b2stel_styl0' : """
						Specifies the type of linearisation used in the charge exchange momentum source term.
					""",
   
'b2tfcc_xfac' : """
						Multiplier to the pressure force term.
					""",
   
'b2tfhe_alfTeEh' : """
						When set to '0.0', the old form of the electron heat flux calculation is used.
						It is recommended to use 1.0.
					""",
   
'b2tfhe_conduction_only' : """
						When conduction_only.eq.1, convective heat transfer terms are turned off. Only to be used when benchmarking against pure conduction cases.
					""",
   
'b2tfhe_fch_pTe' : """
						When set to '1.0', the new form of the electron heat flux calculation is used.
						It is recommended to use 1.0.
					""",
   
'b2tfhe_lim_flux' : """
						If '0', flux limit is not applied directly to the electron heat flux but is applied through transport coefficients if 'b2trcl_conductive_limit' is '1'.
						It is recommended '0'.
					""",
   
'b2tfhe_mdf' : """
						If '1', Spb's new form of calculating electron heat flux is used.
						It is recommended '1' for runs with drifts.
					""",
   
'b2tfhe_neutral' : """
						Real parameter which multiplies ion-neutral current.
						If b2tfhe_neutral is 0 then ion-neutral current is switched off otherwise ion-neutral current is switched on.
					""",
   
'b2tfhe_no_current' : """
						If no_current.eq.1, all currents are set to zero. The setting no_current.eq.1 must be used if the potential equation is not explicitly solved for, i.e. for b2news_poteq.ne.1.
					""",
   
'b2tfhe_vis_par' : """
						Real parameter which multiplies current driven by parallel viscosity. 
						If b2tfhe_vis_par is 0 then viscosity-driven current is switched off otherwise viscosity-driven current is switched on.
					""",
   
'b2tfhe_vis_per' : """
						If '1.0', the electric potential equation is solved by the subroutine b2npp7 using a 7-point stencil.
						The value '1.0' is recommended for runs with drifts when perpendicular viscosity and corresponding perpendicular viscosity current is taken into account.
					""",
   
'b2tfhe_vis_q' : """
						Real parameter which multiplies current driven by heat viscosity effects.
					""",
   
'b2tfhi_lim_flux' : """
						If '0', flux limit is not applied directly to the ion heat flux but is applied through transport coefficients if 'b2trcl_conductive_limit' is '1'.
						It is recommended '0'.
					""",
   
'b2tfhi_mdf' : """
						If '1', Spb's new form of calculating ion heat flux is used.
						It is recommended '1' for runs with drifts.
					""",
   
'b2tfnb_anomalous_core_only' : """
						No description found.
					""",
   
'b2tfnb_drift_style' : """
						When set to '0', drift velocities are calculated in cell centers. When set to '1', drift velocities are calculated in cell faces.
						It is recommended '1'.
					""",
   
'b2tfnb_fnb_nodrift_style' : """
						When set to '1', SPb's form of calculating no drift part of the particle fluxes is used.
						It is recommended '1'.
					""",
   
'b2tfnb_mdf' : """
						If '1', Spb's new form of calculating particle flux is used.
						It is recommended '1' for runs with drifts.
					""",
   
'b2tfnb_PSch' : """
						Multiplier to the Pfirsch-Schlueter flows.
					""",
   
'b2tfnb_xfrhie' : """
						Multiplier to the Rhie and Chow upwind correction.
					""",
   
'b2tfnb_xfrhiehz' : """
						Multiplier to the Rhie and Chow upwind correction in particle flux which is passed to parallel balance momentum equation with drifts.
					""",
   
'b2tfnb_ycur' : """
						Ycur is a multiplier to the parallel viscosity, ion inertial and anomalous currents to the ion radial flows (particle and energy).
					""",
   
'b2tlh0_flux_limit_style' : """
						If '0', use the SOLPS5.0 scheme for neutral heat conductivity flux limits.
						If '1', Spb's form to calculate parallel and perpendicular neutral heat conductivity flux limit (does not preserve symmetry, kept for backward compatibility reasons).
						If '2', modifies the Spb treatment for the flux limits to be applied on the transport coefficients directly.
						It is recommended '2'.
					""",
   
'b2tlh0_hcimx_flag' : """
						When set to -1, only the gradient to the left/bottom is used to compute the conductive neutral flux limits.
						When set to 0, only the gradient to the left/bottom is used to compute the conductive neutral flux limits, except when these do not exist (the other face value is used).
					""",
   
'b2tlmv_style' : """
						if style = 0 then
						 it is applied the origin flux limit to the viscosity
						else
						 it is applied the SPb flux limit to the viscosity
					""",
   
'b2tqca_model' : """
						If model.eq.1, use the Balescu formulation from SOLPS5.0 classical parallel ion heat diffusivity.
						If model.eq.2, use the older Braginskii SOLPS4.0 model.
						If model.eq.3, it is as model.eq.1 but without factor 4/3 which is applied to cvsahz for main ions in b2tral.F.
						It is recommended '3'.
					""",
   
'b2tqca_phm0' : """
						Multiplier for the classical parallel viscosity.
					""",
   
'b2tqce_model' : """
						If model.eq.1, use the fitted Balescu formulation from SOLPS5.0 classical parallel electron heat diffusivity.
						If model.eq.2, use the older Braginskii SOLPS4.0 model.
						If model.eq.3, use the 21-moment Balescu results.
					""",
   
'b2tqce_fke_Zhdanov' : """
						When set to '1', Zhdanov's expression is used in the electron thermal conductivity. It is recommended to use 'b2tqce_fke_Zhdanov' '1'.
						This switch is only active if, simultaneously, one has b2tqce_model.eq.1 and b2tfhe_fch_pTe.eq.1.0.
					""",
   
'b2tqna_diagno' : """
						If diagno.gt.0, outputs details of the calculations of neutral transport coefficients when using the new_df0 model.
						See switch b2tqna_new_df0 for more details.
					""",
   
'b2tqna_divsol_rescale' : """
						Scaling factor for all ion and electron transport coefficients inside divertor SOL regions.
					""",
   
'b2tqna_inputfile' : """
						Profiles file indicator. If b2tqna_inputfile.eq.1, then the code looks for the file b2.transport.inputfile, in which it expects to find the transport namelist.
						This namelist will contain profiles of sources transport parameters measured from the location (ixref,iyref) (default is outer midplane separatrix), which is set with the 'set_transport_i[xy]ref' switches.
					""",
   
'b2tqna_ixref' : """
						Poloidal index (on the basis mesh) of the reference surface for the flux-scaled transport model. The default value is the outer midplane, computed as such (see b2mwti_jxa in Geometry section or set_transport_ixref below):
						Single-null : ixref=rightcut1(1)-(rightcut1(1)-leftcut1(1))/4. Double-null : ixref=(rightcut1(1)+rightcut1(2))/2.
						Straight geometry : ixref=3*nx/4.
						The flux-scaled transport model is used in conjunction with scaling factors listed in column (7) of the transport coefficients description in input files b2ah.dat and b2mn.dat.
					""",
   
'b2tqna_model_sig' : """
						If '1', use constant density in core region to calculate anomalous conductivity sig0=dfsig*qe*ne(nmdpl,-1), nmdpl - number of midplane cell.
						If '0', use sig0=dfsig*qe*ne(x,y)
					""",
   
'b2tqna_new_df0' : """
						When new_df0.eq.1, the neutral diffusivity is computed according to the local charge-exchange, ionisation and elastic collision rates, instead of the standard form with constant cross-sections.
					""",
   
'b2tqna_pfr_rescale' : """
						Scaling factor for all ion and electron transport coefficients inside private flux regions.
					""",
   
'b2tral_mode' : """
						Switch to choose between various interpolation schemes for transport coefficients (Does not apply to pinch velocities vla or to the temperature-driven electric conductivity alf).
						mode.eq.-1: harmonic averaging
						mode.eq.0 : geometric averaging
						mode.eq.1 : arithmetic averaging (SOLPS5.0 formulation)
						mode.eq.2 : arithmetic averaging (SOLPS4.0 formulation)
					""",
   
'b2trcl_conductive_limit' : """
						When set to '1', flux limit of the parallel electron and ion heat fluxes is applied to transport coefficients.
						It is recommended '1'. If 'b2trcl_conductive_limit' '0' then the keys 'b2tfhe_lim_flux' and 'b2tfhi_lim_flux' must be '0'.
					""",
   
'b2trcl_core_cond_limit' : """
						If core_cond_limit.eq.0, then the heat flux limit due to chvemx is not applied in the core.
					""",
   
'b2trcl_cvsa_mltpl' : """
						Artificial coefficient providing faster convergence to the neoclassical electric field but giving a distortion of the flows in the SOL as a side-effect.
						Can be applied <1 during the convergence and turned off for the final stage of calculations.
						Use with caution.
					""",
   
'b2trcl_lluciani' : """
						If lluciani.ne.0, then transport coefficients on cells belonging to  closed field lines are modified according to the Luciani model.
						If lluciani.eq.1, the standard connection length formulation is used.
						If lluciani.eq.2, the old SOLPS4.0 formulation is used for backward compatibility.
						If lluciani.eq.3, Spb's new form Luciani's coefficient.
					""",
   
'b2trcl_lthf21' : """
						If lthf21.ne.0, then the heat transfer model is modified according to the 21-moment approach. This should only be used for multi-fluid runs.
					""",
   
'b2trcl_lvis21' : """
						If lvis21.ne.0, then the viscosities are modified according to the 21-moment approach. This should only be used for multi-fluid runs. This switch should not be used along with 'b2tfhe_vis_par' to avoid double-counting of classical viscosity effects.
					""",
   
'b2treq_phm0' : """
						Multiplier to the temperature equipartition term.
					""",
   
'b2trno_csig_an_style' : """
						If '1', the anomalous contributions in the parallel direction to the electrical conductivity csig and the thermo-electric coefficient calf are zeroed out.
					""",
   
'b2trno_flux_limit_to_dpa' : """
						If '1', flux limit to neutrals contribution to dpa0 - the diffusion coefficient is applied in b2tlc0.F. It is recommended '1'.
						b2tlc0.F has the flux limit parameters alpha and gamma which are given by 'b2tlc0_alpha' and 'b2tlc0_gamma'. 'b2tfnb_alpha' and 'b2tlc0_alpha' cannot be different from zero simultaneously.
						'b2tfnb_alpha' gives another form of flux limit which is applied to the whole particle flux.
					""",
   
'b2trno_pol_anom_scale' : """
						If pol_anom_scale.ne.1, the poloidal anomalous transport coefficients are scaled by the number. To get the same treatment as setting the old switch (radial_only) to 1, set the new switch to 0.0.
						This multiplication is to only take place for charged species.
					""",
   
'b2upht_stylec' : """
						(stylec is a numerical switch, needs experiments)
					""",
   
'b2usmo_cfc0' : """
						Linearisation constant.
					""",
   
'b2ux5p_acpar' : """
						Paremeter needed for iluter matrix solver.
					""",
   
'b2ux5p_cpu' : """
						If cpu.gt.0, prints out the time spent in the matrix solver.
					""",
   
'b2ux5p_mult_nonzero' : """
						Number of expected non-zero matrix elements per matrix row.
					""",
   
'b2ux5p_nltrsol' : """
						Output flag for the iluter matrix solver. Larger numbers mean increasing output level.
					""",
   
'b2ux5p_style' : """
						Choose the type of matrix solver. Style.eq.0 = iluter, Style.eq.1 = 5-pt stencil, Style.eq.2 = MA28. NOTE: Only style.eq.2 will give good results.
						Other values are NOT recommended!
					""",
   
'b2ux7p_nltrsol' : """
						Output flag for the iluter matrix solver. Larger numbers mean increasing output level.
					""",
   
'b2ux7p_style' : """
						Choose the type of matrix solver. Style.eq.0 = iluter, Style.eq.1 = 5-pt stencil, Style.eq.2 = MA28copy. Style.eq.3 = SDRV from YSMP
						NOTE: Only style.eq.3 will give good results.
						Other values are NOT recommended!
					""",
   
'b2ux9p_nltrsol' : """
						Output flag for the iluter matrix solver. Larger numbers mean increasing output level.
					""",
   
'b2ux9p_style' : """
						Choose the type of matrix solver. Style.eq.0 = iluter, Style.eq.1 = 5-pt stencil, Style.eq.2 = MA28copy. NOTE: Only style.eq.2 will give good results.
						Other values are NOT recommended!
					""",
   
'b2xzdd_zero_dead_and_core' : """
						If 1 then zero passed sources in dead regions,
						If 2 zero passed sources in dead regions and core boundary cells
						If 0 then SKIP
					""",
   
'b2yrdr_ns' : """
						New number of species desired when reading a new atomic rates file using b2yr.exe. Must be specified within b2yr.dat.
						To be used for checking atomic rates after bundling and before any plasma state files have been created or converted, i.e. when the number of species in the atomic rates file b2frates does not match the number of species declared in the run parameters file b2fpardf.
					""",
   
'b2ytdr_ndepth1' : """
						New resolution of target depth desired when creating a new initial state file using b2yt.exe. Must be specified within b2yt.dat.
					""",
   
'b2ytdr_non_commensurate' : """
						When set to 1, b2yt will attempt to interpolate a plasma solution and create new input files for a new grid which is not commensurate to the original grid, but still has the same topology.
					""",
   
'b2ytdr_ns' : """
						New number of species desired when creating a new initial state file using b2yt.exe. Must be specified within b2yt.dat.
					""",
   
'b2ytdr_rescale_neutrals' : """
						Rescaling of neutral densities by rescale_neutrals when creating a new initial state file using b2yt.exe. Must be specified within b2yt.dat.
					""",
   
'eirene_ank_mods' : """
						If ank_mods.ne.0, then uses an additional scheme to ensure particle balance as the B2 solution evolves, due to the internal iteration scheme, away from the plasma background on which the Eirene sources were originally computed at the beginning of the time-step. The user is referred to the text in $SOLPSTOP/doc/Source_Scaling_in_B2.pdf for a full description of the method used.
					""",
   
'eirene_dpc_fix' : """
						If dpc_fix.eq.1, then uses the true particle source from the stratum. If dpc_fix.eq.2, sets this particle source to zero.
						The equivalent of the old behaviour is dpc_fix.eq.0 and is wrong!
					""",
   
'eirene_extrap' : """
						If eirene_extrap.eq.1, then guard cell plasma parameter values are calculated from the neighbouring real cell values.
						If eirene_extrap.eq.0, the guard cell values are used unchanged.
					""",
   
'eirene_ionising_core' : """
						If <> 0 then recycles the neutral flux having crossed the core boundary within Eirene as ions. The recycling is surface-averaged, and neutrals come back as fully-stripped ions.
						'eirene_ionizing_core' is an alias for this switch.
						If the value = 1, then the flux is added by direct modification of the sources in the guard cells --- this will only work if a standard flux boundary condition is applied at that boundary.
						If the value is < 0, then the absolute value specifies which boundary in b2.boundary.parameters is to be used. This will only work for the new type 13 boundary condition.
					""",
   
'eirene_fixuub' : """
						Switch for toggling between conversion rules for velocities between B2.5 and Eirene.
						If fixuub.eq.0, the velocity passed to Eirene is face-centered and computed from the fluxes at the cell faces.
						If fixuub.eq.1, the velocity passed to Eirene is cell-centered and computed from the fluxes at the cell faces.
						If fixuub.eq.2, the velocity passed to Eirene is cell-centered and computed as the cell-centered parallel velocity from B2.5 multiplied by the pitch angle.
					""",
   
'eirene_format' : """
						This switch is to be provided within b2yt.dat to indicate to the b2yt converter the format of the original Eirene input.dat file to be modified. The accepted values are (case-insensitive):
						'old' for input files from SOLPS4.0 and SOLPS5.0 runs using "old" Eirene_96
						'new' for input files from SOLPS4.0 and SOLPS5.0 runs using "new" Eirene_99
						'facelift' for input files from SOLPS5.1 runs
						'juelich' for input files from Juelich Eirene versions (2008 and younger)
						'iter' for input files from SOLPS4.2/4.3 and SOLPS-ITER runs
					""",
   
'eirene_lhalpha' : """
						If 0 then no calculation of halpha in wneutral, otherwise halpha is calculated
					""",
   
'eirene_lvib' : """
						If 0 then the sigadd4 (molecular ions) and sigadd5 (negative ions) contributions to the halpha in wneutral are not included, otherwise they are
					""",
   
'eirene_mc_linearisation' : """
						Specifies the type of linearisation used in the sources derived from the Monte-Carlo neutrals. If linearisation.eq.0, all sources are fed to the constant term, if linearisation.eq.1, positive terms go in the constant term, and negative terms in the proportional term. 'eirene_mc_linearization' is an alias for this switch.
					""",
   
'eirene_mc_output_style' : """
						If non-zero, prints sources computed by Eirene. If greater than 1, prints them on every use of the recycling sources, not just when they are computed.
					""",
   
'eirene_neutr_avg' : """
						If eirene_neutr_avg.gt.0, then Eirene sources are accumulated and averaged until eirene_neutr_avg+1 steps, at which point the averaging process is reset. Note that only one of b2stbr_eir_src_nhist, eirene_neutr_avg, or eirene_underrelax may be nonzero.
					""",
   
'eirene_print_minmax' : """
						Print min and max values of te, ti, na & ua
					""",
   
'eirene_repeat_first_call' : """
						If > 0 then repeats the first call to eirene in eirene_mc so many times.
						Useful if a density feedback gas puff is being used because the flux passed to Eirene on its first call is ignored (instead the value in the Eirene input file is used).
					""",
   
'eirene_underrelax' : """
						If eirene_underrelax.gt.0, then an underrelaxation scheme is used for the Eirene sources, with an underrelaxation ratio of 1/eirene_underrelax.
						Note that only one of b2stbr_eir_src_nhist, eirene_neutr_avg, or eirene_underrelax may be nonzero.
					""",
   
'eirene_use_recyceir' : """
						If > 0 use recyceir (non species dependent) to specify the recycling* coefficients, else if 0 use recyc (species dependent).
					""",
   
'ma28_nwrite' : """
						If nwrite.gt.0, prints the content of the sparse matrix in the b2_matrix file, for the first nwrite calls.
					""",
   
'neoclassical_ic' : """
						..set the contribution ic in NEOART
						  0 --- classical particle flux
						  1 --- banana plateau contribution
						  2 --- Pfirsch-Schlueter contribution
						  3 --- both banana and PS
						  4 --- all contributions
						  mind that B2 already calculates the classical transport !
						  avoid double transport, 0+4 for cross checks only !
					""",
   
'solps_version' : """
						This switch is to be provided within b2yt.dat to indicate to the b2yt converter the format of the original fort.44 file to be modified. The accepted values are (case-insensitive):
						'4.3' for a fort.44 file produced from SOLPS4.3 runs
						'5.0' for a fort.44 file produced from SOLPS5.0 runs
						'5.1' for a fort.44 file produced from SOLPS5.1 runs
						'5.2' for a fort.44 file produced from SOLPS5.2 runs
						'iter' for input files from SOLPS-ITER runs (no conversion necessary)
					""",
   
}
