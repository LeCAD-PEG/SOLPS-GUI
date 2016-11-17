# Generated with create-addmenu.xslt
# xsltproc create-addmenu.xslt solps-input.xml > ../../solps-gui/src/widgets/b2menu.py
b2mn_menu = {
# Category : ( parameter, type, default, description )
#         or ( parametergroup, 'paramgroup', [(name, type, default, description)...], description)
  
  'Run': [
  
         ( 'b2aidr_read_b2fstate', 'integer', '0', """
				If read_b2fstate.ne.0, b2aidr will read an existing b2fstate file and append to it a flat state description for additional new species being introduced in the run.
			"""),
      
         ( 'b2mndr_astra', 'integer', '0', """
				Turns on coupling with the ASTRA core transport code if non-zero.
				To be used, the code must be compiled with the -DASTRA option.
			"""),
      
         ( 'b2mndr_cpu', 'real', '0.0', """
				CPU limit. If cpu.eq.0.0, no CPU limit is enforced. Otherwise, the code stops smoothly after it has been running for at least 'cpu' CPU seconds.
			"""),
      
         ( 'b2mndr_density_rescale', 'real', '1.0', """
				Multiplier of all densities on the first timestep.
			"""),
      
      ( 'b2mndr_d*', 'paramgroup', [
        
               ('b2mndr_delta_max', 'real', '0.0',''''''), 
        
               ('b2mndr_delta_min', 'real', '0.0',''''''), 
        
               ('b2mndr_dt_change_dec', 'real', '1.0',''''''), 
        
               ('b2mndr_dt_change_inc', 'real', '1.0',''''''), 
        
               ('b2mndr_dt_max', 'real', '1.0e+01',''''''), 
        
               ('b2mndr_dt_min', 'real', '1.0e-30',''''''), 
        ],
         """
				One of the dynamic timestep control parameters. Only active if both delta_max and delta_min are non-zero. The timestep is increased by a factor dt_change_inc or decreased by a factor dt_change_dec, within the bounds [dt_min, dt_max], according to whether the largest instantaneous change in all equations is smaller than delta_min or larger than delta_max, respectively.
			"""),
         ( 'b2mndr_dtim', 'real', '1.0', """
				Timestep (in seconds).
			"""),
      
         ( 'b2mndr_eirene', 'integer', '0', """
				Turns on coupling with the Eirene Monte-Carlo neutral code if non-zero.
				To be used, the code must be compiled with the -DB25_EIRENE option.
			"""),
      
         ( 'b2mndr_elapsed', 'integer', '0', """
				Elapsed time limit. Is elapsed.eq.0.0, no time limit is enforced.
				Otherwise, the code stops smoothly after is has been running for at least 'elapsed' wall clock seconds.
			"""),
      
         ( 'b2mndr_etim', 'real', '0.0', """
				etim specifies the end time. Only active if etim > stim.
			"""),
      
         ( 'b2mndr_ismain', 'integer', '1', """
				ismain identifies the index of the main plasma species. 
				It must hold that ismain is not a neutral species.
			"""),
      
         ( 'b2mndr_ntim', 'integer', '1', """
				Number of timesteps desired in this run. If ntim.eq.0, the code simply reads the input file and creates the b2fplasma and b2fstate files corresponding to the present plasma state.
			"""),
      
         ( 'b2mndr_rescale_neutrals', 'real', '1.0', """
				Multiplier to the neutral density on the first timestep.
			"""),
      
         ( 'b2mndr_rescale_neutrals_sources', 'real', '1.0', """
				Multiplier to the neutral sources (either computed by Eirene or the corresponding rate coefficients).
			"""),
      
         ( 'b2mndr_savecpu', 'real', '3600.0', """
				CPU time interval after with save files plasmastate.xxxx are written.
				These can be used, in conjunction with the b2co.exe instruction, to recover a crashed run.
			"""),
      
         ( 'b2mndr_stim', 'real', '0.0', """
				stim specifies the initial time --- default 0.
				If set to a positive or zero value, this overwrites the time value read from b2fstati.
				If set to a negative value, the run continues from the time read in b2fstati.
			"""),
      
         ( 'b2mndt_density_control', 'integer', '0', """
				Feedback on the total heavy particle density. If density_control.ne.0, the sum of all densities is kept constant.
			"""),
      
      ( 'b2mndt_nstg.', 'paramgroup', [
        
               ('b2mndt_nstg0', 'integer', '1',''''''), 
        
               ('b2mndt_nstg1', 'integer', '1',''''''), 
        
               ('b2mndt_nstg2', 'integer', '1',''''''), 
        ],
         """
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
			"""),
      ( 'b2news_facdrift*', 'paramgroup', [
        
               ('b2news_facdrift_dec', 'real', '0.0',''''''), 
        
               ('b2news_facdrift_inc', 'real', '1.0',''''''), 
        
               ('b2news_facdrift_start', 'real', '0.0',''''''), 
        
               ('b2news_facdrift_target', 'real', '0.0',''''''), 
        ],
         """
				Ramping parameters for facdrift, which multiplies the diamagnetic terms. The code is started on the first time step with facdrift=facdrift_start. If facdrift_target.ne.facdrift_start, then, on each time step, facdrift is multiplied by facdrift_inc. If the code does not converge on the timestep, facdrift is decreased by facdrift_dec. A facdrift profile is also possible, see Numerics section for details.
			"""),
      ( 'b2news_facExB_*', 'paramgroup', [
        
               ('b2news_facExB_dec', 'real', '0.0',''''''), 
        
               ('b2news_facExB_inc', 'real', '1.0',''''''), 
        
               ('b2news_facExB_start', 'real', '0.0',''''''), 
        
               ('b2news_facExB_target', 'real', '0.0',''''''), 
        ],
         """
				Ramping parameters for facExB, which multiplies the ExB terms. Same treatment as above for facdrift.
			"""),
      ( 'b2news_facvis_*', 'paramgroup', [
        
               ('b2news_facvis_dec', 'real', '0.0',''''''), 
        
               ('b2news_facvis_inc', 'real', '1.0',''''''), 
        
               ('b2news_facvis_start', 'real', '0.0',''''''), 
        
               ('b2news_facvis_target', 'real', '0.0',''''''), 
        ],
         """
				Ramping parameters for facvis, which multiplies the drift viscosity terms. Same treatment as above for facdrift.
			"""),
         ( 'b2news_no_solve', 'integer', '0', """
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
			"""),
      
         ( 'b2sral_inputfile', 'integer', '0', """
				Profiles file indicator. If b2sral_inputfile.eq.1, then the code looks for the file b2.sources.profile in which it expects to find the 'profile' namelist.
				This namelist will contain profiles of sources measured from the location (ixref,iyref) (default is outer midplane separatrix), which is set with the 'set_transport_i[xy]ref' switches.
			"""),
      
      ( 'b2srdt_*_namelist', 'paramgroup', [
        
               ('b2srdt_numerics_namelist', 'integer', '0',''''''), 
        
               ('b2stbc_boundary_namelist', 'integer', '0',''''''), 
        
               ('b2stbr_neutrals_namelist', 'integer', '0',''''''), 
        
               ('b2tqna_transport_namelist', 'integer', '0',''''''), 
        ],
         """
				Namelist file indicators. If xxx_namelist.eq.1, then the code looks for the file b2.xxx.parameters, in which it expects to find the xxx namelist.
			"""),
         ( 'b2stbc_cbc', 'real', '1.0', """
				Multiplier to the ExB velocity for sheath boundary conditions in b2stbc_spb and BCMOM=13 case of b2stbc_phys.
			"""),
      
         ( 'b2stbc_feedback', 'integer', '0', """
				If feedback.eq.1, turns on feedback mode for the boundary conditions.
				See Physics section for more details. Equivalent to LFEEDBACK=.true. in the b2.boundary.parameters namelist.
			"""),
      
         ( 'b2stbc_ncallfeedback', 'integer', '0', """
				Timestep index after which the feedback in b2stbc is activated.
			"""),
      
         ( 'b2stbr_core_sources_rescale', 'real', '1.0', """
				Multiplier to the totally ionised species sources at the core boundary.
			"""),
      
         ( 'b2stbr_first_flight', 'integer', '0', """
				If first_flight.ne.0, turns on the first flight model. See Physics section for additional details.
			"""),
      
         ( 'b2tqna_inputfile', 'integer', '0', """
				Profiles file indicator. If b2tqna_inputfile.eq.1, then the code looks for the file b2.transport.inputfile, in which it expects to find the transport namelist.
				This namelist will contain profiles of sources transport parameters measured from the location (ixref,iyref) (default is outer midplane separatrix), which is set with the 'set_transport_i[xy]ref' switches.
			"""),
      
         ( 'b2ytdr_ndepth1', 'integer', 'ndepth_nml', """
				New resolution of target depth desired when creating a new initial state file using b2yt.exe. Must be specified within b2yt.dat.
			"""),
      
         ( 'b2ytdr_non_commensurate', 'integer', '0', """
				When set to 1, b2yt will attempt to interpolate a plasma solution and create new input files for a new grid which is not commensurate to the original grid, but still has the same topology.
			"""),
      
         ( 'b2ytdr_ns', 'integer', 'ns', """
				New number of species desired when creating a new initial state file using b2yt.exe. Must be specified within b2yt.dat.
			"""),
      
         ( 'b2ytdr_rescale_neutrals', 'real', '1.0', """
				Rescaling of neutral densities by rescale_neutrals when creating a new initial state file using b2yt.exe. Must be specified within b2yt.dat.
			"""),
      
   ],

  'Output': [
  
         ( 'ank_tracing', 'integer', '0', """
				If ank_tracing.ge.1, additional tracing output from Andrei Kukushkin is produced, in files to be found in the tracing/ directory inside the run directory. The traces will be written every ank_tracing iteration.	
			"""),
      
         ( 'b2mndr_b2time', 'integer', '1', """
				Specifies the number of timesteps between writes of the time-dependent file. If b2time.gt.0, always writes out on the last timestep.
			"""),
      
         ( 'b2mndr_cdfmovietim', 'real', '0.0', """
				Another option for movie output. Give the real-time interval between movie frames.
			"""),
      
      ( 'b2mndr_idout.', 'paramgroup', [
        
               ('b2mndr_idout0', 'string', 'pgnl;pgmm;pzmm',''''''), 
        
               ('b2mndr_idout1', 'string', 'pzmm',''''''), 
        ],
         """
				idout0 and idout1 specify the desired selection of output segments; idout0 for output before the calculation and idout1 for output at the conclusion of the calculation. The generic description of either of these 'idout' variables follows. idout specifies the desired selection of output segments for printed and graphical output. Associated with each segment is a four-character word, which is identified on the printed output. (The same word may be associated with several segments.) A particular segment will be produced only if its associated word has a match, as defined by the routine strmas, in idout.
			"""),
         ( 'b2mndr_inverse_ua', 'integer', '0', """
				If inverse_ua.eq.1, the code will produce a 'b2fstati_with-ua' file that contains the same plasma information, but with the opposite sign convention for the parallel velocity. The run will then proceed with the new velocities with their sign inverted.
			"""),
      
         ( 'b2mndr_mvinc', 'integer', '1', """
				Specifies the number of timesteps between movie output. If greater than 1 and the last timestep does not correspond to a planned frame, an extra endstate frame is added.
			"""),
      
         ( 'b2mndr_mvnum', 'integer', '0', """
				Specifies the maximum number of instances at which movie data will be output.
			"""),
      
      ( 'b2mndr_*_eps', 'paramgroup', [
        
               ('b2mndr_na_eps', 'real', '1.0e19',''''''), 
        
               ('b2mndr_po_eps', 'real', '1.0e+1',''''''), 
        
               ('b2mndr_te_eps', 'real', '1.0e+1',''''''), 
        
               ('b2mndr_ti_eps', 'real', '1.0e+1',''''''), 
        
               ('b2mndr_ua_eps', 'real', '1.0e+4',''''''), 
        ],
         """
					The five switches above are safeguards numbers for when printing changes after a time-step. The change is computed as:
					deltaX = abs((X(t)-X(t-1))/(X(t)+X_eps))
			"""),
         ( 'b2mndr_plasmatim', 'real', '0.0', """
				Another option for plasma state file output. Give the real-time interval between succesive write-ups of plasmastate files, in addition to the ones written at regular CPU intervals.
			"""),
      
         ( 'b2mndr_tally', 'integer', '1', """
				Specifies the number of timesteps between writes of tallies.
				If tally.gt.0, always writes out on the last timestep.
			"""),
      
         ( 'b2mndr_trantim', 'real', '0.0', """
				Produces a numbered 'tran' file every trantim real-time seconds.
				An endstate file is written if it falls between scheduled write-up times.
				Only available within the -DJET environment.
			"""),
      
         ( 'b2mndt_moitlv', 'integer', '-1', """
				Controls detailed monitoring output. moitlv.eq.-1 means no output, moitlv.eq.0 means output once per timestep, moitlv.eq.1 means output once per nstg0 iteration, moitlv.eq.2 means output once per nstg1 iteration and moitlv.eq.3 means output once per nstg2 iteration. See 'b2mndr_nstg?' description in Run section for more details.
			"""),
      
         ( 'b2mndt_moqtlv', 'integer', '3', """
				Controls quick trace output. moqtlv.eq.-1 means no output, moqtlv.eq.0 means output once per timestep, moqtlv.eq.1 means output once per nstg0 iteration, moqtlv.eq.2 means output once per nstg1 iteration and moqtlv.eq.3 means output once per nstg2 iteration. See 'b2mndr_nstg?' description in Run section for more details.
			"""),
      
         ( 'b2mwqt_style', 'integer', '1', """
				NOT FOUND!
			"""),
      
         ( 'b2mwti_ismain0', 'integer', '0', """
				Index of the species used to create the 'dp3d?.last10' diagnostic files.
				Defaults to the neutral species associated with ismain. If no such species is declared, the default will be set to ismain. Is expected to either correspond to a neutral species or to ismain.
				If ismain is also defaulted, then will be 0.
			"""),
      
         ( 'b2mwti_target_offset', 'integer', '1', """
				The diagnostic values from b2time.nc use guard cell values if target_offset.eq.0, and values from the neighbouring real cell if target_offset.eq.1. Fluxes are not affected.
			"""),
      
         ( 'b2news_ncallout', 'integer', '-1', """
				If the iteration number is equal to ncallout, then several output files 'b2ne_npmo', 'b2ne_xppb', 'b2ne_npco', 'b2ne+nppo' which detail the convergence behaviour and residuals.
			"""),
      
         ( 'b2srsm_diagno', 'integer', '0', """
				Controls level of output in b2srsm. If diagno.ge.2, output will be given on every call. If diagno.eq.1, output will be given on main calls only.
			"""),
      
         ( 'b2stbc_diagno', 'integer', '0', """
				Controls level of output in b2stbc and subservient routines.
				Level 1 (diagno.ge.1) output includes wrong_flow warnings, transport coefficients at the (nx/2,ny) basis mesh position, the solution found for the given heat flux at constant temperature bc, and all feedback diagnostics.
				Level 2 output (diagno.ge.2) includes the integral current correction, the boundary sources on the first call, excessive sound speeds, and the iterative progress to the given heat flux at constant temperature bc. 
				Level 3 output (diagno.ge.3) includes the boundary sources on each call, and the boundary.prt file listing all boundary cells.
			"""),
      
      ( 'b2stbr_*_netcdf', 'paramgroup', [
        
               ('b2stbr_b2wall_netcdf', 'integer', '0',''''''), 
        
               ('tallies_netcdf', 'integer', '0',''''''), 
        ],
         """
				If tallies_netcdf.ne.0, the file 'b2tallies.nc' is created, which contains the regional tallies in CDF format.
				If b2wall_netcdf.ne.0, the file 'b2wall.nc' is created, which contains the wall tallies in CDF format [written every b2wall_netcdf "main calls"].
			"""),
         ( 'b2stbr_output', 'integer', '0', """
				Output flag for the first_flight model. If output.ge.1, the files start, end, and fort.88 are created, which contain information about the chords used in the model.
			"""),
      
         ( 'b2tqna_diagno', 'integer', '0', """
				If diagno.gt.0, outputs details of the calculations of neutral transport coefficients when using the new_df0 model.
				See switch b2tqna_new_df0 for more details.
			"""),
      
         ( 'b2ux5p_cpu', 'integer', '0', """
				If cpu.gt.0, prints out the time spent in the matrix solver.
			"""),
      
         ( 'b2ux5p_nltrsol', 'integer', '2', """
				Output flag for the iluter matrix solver. Larger numbers mean increasing output level.
			"""),
      
         ( 'b2ux7p_nltrsol', 'integer', '0', """
				Output flag for the iluter matrix solver. Larger numbers mean increasing output level.
			"""),
      
         ( 'b2ux9p_nltrsol', 'integer', '0', """
				Output flag for the iluter matrix solver. Larger numbers mean increasing output level.
			"""),
      
         ( 'b2yrdr_ns', 'integer', 'ns', """
				New number of species desired when reading a new atomic rates file using b2yr.exe. Must be specified within b2yr.dat.
				To be used for checking atomic rates after bundling and before any plasma state files have been created or converted, i.e. when the number of species in the atomic rates file b2frates does not match the number of species declared in the run parameters file b2fpardf.
			"""),
      
         ( 'eirene_format', 'string', 'iter', """
				This switch is to be provided within b2yt.dat to indicate to the b2yt converter the format of the original Eirene input.dat file to be modified. The accepted values are (case-insensitive):
				'old' for input files from SOLPS4.0 and SOLPS5.0 runs using "old" Eirene_96
				'new' for input files from SOLPS4.0 and SOLPS5.0 runs using "new" Eirene_99
				'facelift' for input files from SOLPS5.1 runs
				'juelich' for input files from Juelich Eirene versions (2008 and younger)
				'iter' for input files from SOLPS4.2/4.3 and SOLPS-ITER runs
			"""),
      
         ( 'eirene_mc_output_style', 'integer', '1', """
				If non-zero, prints sources computed by Eirene. If greater than 1, prints them on every use of the recycling sources, not just when they are computed.
			"""),
      
      ( 'eirene_savef3.', 'paramgroup', [
        
               ('eirene_savef30', 'integer', '0',''''''), 
        
               ('eirene_savef31', 'integer', '0',''''''), 
        ],
         """
				For coupled runs, the code will create two files named fort.30 and fort.31, containing the plasma geometry and plasma state, respectively, for use by Eirene. This happens irrespective of the setting of the two switches above. If however, the user wishes to obtain these files for a non-coupled run, then these two switches can be set to 1 and the files will then be produced at the end of the run. If savef31.lt.0, then a fort.31.###### file is produced after every B2.5 time step. Additionally, if savef31.ne.0, the fort.31 file will be updated before every Eirene call for coupled runs.
			"""),
         ( 'ma28_nwrite', 'integer', '0', """
				If nwrite.gt.0, prints the content of the sparse matrix in the b2_matrix file, for the first nwrite calls.
			"""),
      
         ( 'solps_version', 'string', 'iter', """
				This switch is to be provided within b2yt.dat to indicate to the b2yt converter the format of the original fort.44 file to be modified. The accepted values are (case-insensitive):
				'4.3' for a fort.44 file produced from SOLPS4.3 runs
				'5.0' for a fort.44 file produced from SOLPS5.0 runs
				'5.1' for a fort.44 file produced from SOLPS5.1 runs
				'5.2' for a fort.44 file produced from SOLPS5.2 runs
				'iter' for input files from SOLPS-ITER runs (no conversion necessary)
			"""),
      
   ],

  'Physics': [
  
         ( 'b2mndr_atomic_physics_rescale', 'integer', '0', """
				If atomic_physics_rescale is not 0, then the code will rescale the rates stored in b2frates according to the multipliers given in the b2.atomic_physics_rescale.parameters inputfile before making use of them.
			"""),
      
         ( 'b2mndr_coronal_model', 'integer', '0', """
				Turns on the coronal model if coronal.ne.0. I.e., the reaction rates of all reactions are made density-independent, and the value computed at the lowest density (given in b2ar.dat) is used.
			"""),
      
         ( 'b2mndr_hz', 'real', '0.0', """
				hz has been introduced into the new form of the parallel momentum balance equation.
				If fac_hz = 0.0 then hz = 1 and old form of equations is used.
				If fac_hz = 1.0 then new form of equations is used.
			"""),
      
         ( 'b2news_BoRiS', 'real', '0.0', """
				The poloidal convective heat flux contains a prefactor of (3/2+BoRiS). The default gives us the internal energy equation. The value BoRiS = 1.0 gives us the total energy equation.
				Only for use to benchmark with codes using the total energy equation. When used, the meaning of fhe and fhi changes from internal energy fluxes to total energy fluxes.
			"""),
      
         ( 'b2news_coriolis', 'integer', '0', """
				If coriolis.ne.0, the Coriolis force terms will be included in the solution of the momentum equations.
			"""),
      
         ( 'b2news_ExB', 'real', '0.0', """
				Real parameter which multiplies ExB flows. If b2news_ExB.eq.0 and b2news_facExB_start.eq.0 then ExB flows are switched off. If b2news_ExB is non-zero, then ExB flows are multiplied by that constant throughout the run.
				See also Run section on switches b2news_facExB_... for more details. A spatial fac_ExB profile is also possible, see Numerics section for details.
			"""),
      
         ( 'b2news_vis', 'real', '0.0', """
				Alternative name of the variable in the code is fac_vis_scalar
			"""),
      
         ( 'b2npmo_b2sifr_', 'integer', '1', """
				When set to '1', the new correct form of the friction force is used.
				The value '0' corresponds to the old SOLPS5.0 treatment.
			"""),
      
         ( 'b2npmo_modvis', 'integer', '1', """
				When set to '1', the new correct form of viscosity is used. It is important for runs with drifts. It is recommended '1'.
				The value '0' corresponds to the old SOLPS5.0 treatment.
			"""),
      
         ( 'b2sdia_facgt', 'real', '0.0', """
				Multiplier of the contribution to electron and ion heat sources from divergence of the gradTxB heat flux. That contribution is also multiplied by facdrift. This term is no longer needed as it has been transferred from being a source to being included in the flows.
			"""),
      
         ( 'b2sicf_phm0', 'real', '1.0', """
				Multiplier of the centrifugal force term.
				It is recommended '1.0'.
				The value '0.0' corresponds to the old SOLPS5.0 treatment.
			"""),
      
         ( 'b2sicf_phm1', 'real', '1.0', """
				Multiplier of the centrifugal force correction term due to linearization.
				It is recommended '1.0'.
				The value '0.0' corresponds to the old SOLPS5.0 treatment.
			"""),
      
      ( 'b2sifr_*th*', 'paramgroup', [
        
               ('b2sifr_limthee', 'real', '0.3',''''''), 
        
               ('b2sifr_limthii', 'real', '0.3',''''''), 
        
               ('b2sifr_phm1', 'real', '1.0',''''''), 
        
               ('b2trcl_cthe', 'real', '0.0',''''''), 
        
               ('b2trcl_cthi', 'real', '2.65',''''''), 
        ],
         """
				Parameters for the computation of the thermal force term.
			"""),
         ( 'b2sifr_phm0', 'real', '1.0', """
				Multiplier of the friction term between charged species.
			"""),
      
         ( 'b2sifr_phm1', 'real', '1.0', """
				Multiplier of the ehxp term in the thermal force term.
			"""),
      
         ( 'b2sifr_phm2', 'real', '1.0', """
				Multiplier of the electron thermal gradient term in the thermal force term.
			"""),
      
         ( 'b2sihs_istyle_Joule_heating', 'integer', '1', """
				When set to '1', there is no radial contribution in Joule heating because there are no physical reasons to take it into account.
				The value '0' corresponds to the old SOLPS5.0 treatment.
			"""),
      
         ( 'b2sihs_phm0', 'real', '1.0', """
				Multiplier of the contribution to electron heat sources from divergence(ue,ve).
			"""),
      
         ( 'b2sihs_phm1', 'real', '1.0', """
				Multiplier of the contribution to ion heat sources from divergence(ua,va).
				This term is superseded by the BoRiS switch if invoked.
			"""),
      
         ( 'b2sihs_phm2', 'real', '1.0', """
				Multiplier of the contribution to ion heat sources from viscous heating.
				This term is superseded by the BoRiS switch if invoked.
			"""),
      
         ( 'b2sihs_phm3', 'real', '1.0', """
				Multiplier of the contribution to electron heat sources from Joule heating (electron-ion friction).
			"""),
      
         ( 'b2sihs_phm4', 'real', '1.0', """
				Multiplier of the contribution to ion heat sources from atom-atom friction.
				This term is superseded by the BoRiS switch if invoked.
			"""),
      
         ( 'b2sihs_phm5', 'real', '1.0', """
				Multiplier of the contribution to electron heat sources from divergence of the electrical drift. That contribution is also multiplied by facExB.
			"""),
      
         ( 'b2sihs_phm6', 'real', '1.0', """
				Multiplier of the contribution to ion heat sources from divergence of the electrical drift. That contribution is also multiplied by facExB.
			"""),
      
         ( 'b2sihs_phm7', 'real', '0.0', """
				Multiplier of the contribution to heat sources from friction due to diamagnetic velocities. Normally already included in 'phm3' term above.
			"""),
      
      ( 'b2sqcx_phm.', 'paramgroup', [
        
               ('b2sqcx_phm0', 'real', '1.0',''''''), 
        
               ('b2sqcx_styl0', 'integer', '0',''''''), 
        ],
         """
				phm0 : Multiplier to the charge-exchange rate coefficient. Subservient to styl0: only used if styl0.eq.0 or is.lt.2. If styl0.ne.0, the charge-exchange rate coefficients for species of index 2 and above are set to zero.
			"""),
         ( 'b2sqel_artificial_radiation', 'real', '0.0', """
				If art_rad.ne.0, then an artificial radiation loss term is added to the electron cooling rate. Art_rad represents the percent fraction of impurities in the plasma.
			"""),
      
         ( 'b2sqel_phm0', 'real', '1.0', """
				Multiplier to the ionisation rate coefficient.
			"""),
      
         ( 'b2sqel_phm1', 'real', '1.0', """
				Multiplier to the recombination rate coefficient.
			"""),
      
         ( 'b2sqel_phm2', 'real', '1.0', """
				Multiplier to the heat loss rate coefficient.
			"""),
      
         ( 'b2sral_style', 'integer', '2', """
				When set to '0', in the expression of the electron particle flux (fne) the particle flux with drift terms is used and temporary drift velocities on the first call are calculated. When set to '1' or '2', the particle flux without drift terms is used in fne.
				It is recommended '2'.
			"""),
      
      ( 'b2stbc_feedback*', 'paramgroup', [
        
               ('b2stbc_fchycore', 'real', '-1.0e30',''''''), 
        
               ('b2stbc_fheycore', 'real', '0.0',''''''), 
        
               ('b2stbc_fhiycore', 'real', '0.0',''''''), 
        
               ('b2stbc_fhiycore_kinetic_energy', 'integer', '0',''''''), 
        
               ('b2stbc_fnaycore', 'real', '-1.0e30',''''''), 
        
               ('b2stbc_isfeedback', 'integer', '0',''''''), 
        
               ('b2stbc_iyped', 'integer', 'jsep/2',''''''), 
        
               ('b2stbc_ndes', 'real', '0.0',''''''), 
        
               ('b2stbc_ndes_sol', 'real', '0.0',''''''), 
        
               ('b2stbc_nepedm_sol', 'real', '0.0',''''''), 
        
               ('b2stbc_nesepm', 'real', '0.0',''''''), 
        
               ('b2stbc_nesepm_overshoot', 'real', '0.0',''''''), 
        
               ('b2stbc_nesepm_minpuff', 'real', '0.0',''''''), 
        
               ('b2stbc_nesepm_maxpuff', 'real', '0.0',''''''), 
        
               ('b2stbc_nesepm_pfr', 'real', '0.0',''''''), 
        
               ('b2stbc_nesepm_sol', 'real', '0.0',''''''), 
        
               ('b2stbc_private_flux_puff', 'real', '0.0',''''''), 
        
               ('b2stbc_volrec', 'real', '0.0',''''''), 
        
               ('b2stbc_volrec_overshoot', 'real', '0.0',''''''), 
        
               ('eirene_nesepm_istra', 'integer', '-1',''''''), 
        ],
         """
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
			"""),
         ( 'b2stbc_secmodel', 'integer', '0', """
				If secmodel.eq.1, then the secondary electron emission coefficient at the plates is computed locally according to a kinetic model, otherwise the default values of cbsch(7,ireg) and/or gammae are used.
			"""),
      
      ( 'b2stbc_type13..21*', 'paramgroup', [
        
               ('b2stbc_type13_ref', 'integer', '1',''''''), 
        
               ('b2stbc_type16_kinetic_energy', 'integer', '0',''''''), 
        
               ('b2stbc_type16_ref', 'integer', '1',''''''), 
        
               ('b2stbc_type20_ref', 'integer', '1',''''''), 
        
               ('b2stbc_type21_ref', 'integer', '1',''''''), 
        ],
         """
				These switches are associated with the boundary condition of type 13, 16, 17, 20 or 21 for particle flux, or electron and ion energy fluxes, i.e. constant density or temperature giving a prescribed flux through a radial surface, located type13_ref or type16_ref radial steps away from the boundary of the computational domain, respectively, and applied type20_ref steps away. See code and description in b2cdcn for details.
				Type 21 also applies to the electric potential boundary condition.
				It scales the feedback strength according to the value of the variable on the ring type21_ref steps inside.
				When type16_ref.gt.1, then the position where the core flux tallies are computed moves along with the boundary condition.
				If type16_kinetic_energy.eq.1, then the parallel kinetic energy flux is included in the ion heat flux component of type 16 and 17 boundary conditions.
			"""),
      ( 'b2stbr_sputtering...', 'paramgroup', [
        
               ('b2stbr_alpha', 'real', '0.25',''''''), 
        
               ('b2stbr_plate_model', 'integer', '0',''''''), 
        
               ('b2stbr_plate_option', 'integer', '3',''''''), 
        
               ('b2stbr_plate_temp', 'real', '300.0',''''''), 
        
               ('b2stbr_plate_thick', 'real', '0.00',''''''), 
        
               ('b2stbr_redep_alpha', 'real', '0.00',''''''), 
        
               ('b2stbr_sput_chem_model', 'integer', '0',''''''), 
        
               ('b2stbr_sput_chem_cutoff_alpha', 'real', '1.0',''''''), 
        
               ('b2stbr_sput_chem_cutoff_beta', 'real', '3.0',''''''), 
        
               ('b2stbr_sput_dst', 'integer', '-1',''''''), 
        
               ('b2stbr_sput_dst2', 'integer', '-1',''''''), 
        
               ('b2stbr_sput_dst3', 'integer', '-1',''''''), 
        
               ('b2stbr_sput_frc', 'real', '0.0',''''''), 
        
               ('b2stbr_sput_mixed_alpha', 'real', '1.0',''''''), 
        
               ('b2stbr_sput_mixed_beta', 'real', '1.0',''''''), 
        
               ('b2stbr_sput_phys', 'real', '0.0',''''''), 
        
               ('b2stbr_sput_phys_col', 'integer', '3',''''''), 
        
               ('b2stbr_sput_phys_model', 'integer', '1',''''''), 
        
               ('b2stbr_sput_res', 'real', '0.0',''''''), 
        
               ('b2stbr_sput_src', 'integer', '1',''''''), 
        
               ('b2stbr_sputter_energy_on', 'integer', '1',''''''), 
        
               ('b2stbr_therm_evap', 'real', '0.0',''''''), 
        
               ('b2stbr_sput_frac_flag', 'integer', '0',''''''), 
        ],
         """
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
			"""),
      ( 'b2stbr_refl*', 'paramgroup', [
        
               ('b2stbr_refl_model', 'integer', '1',''''''), 
        
               ('b2stbr_reflection_on', 'integer', '1',''''''), 
        ],
         """
				Reflection model switches. If the recycling coefficients (particle and energy) are set to zero, then the code attempts to use, for surfaces in contact with walls, the TRIM reflection data for particle and energy reflection coefficients, when refl_model.eq.1. If refl_model.eq.0, an empirical formula is used instead. The model switch is subservient to reflection_on.ne.0. If reflection_on.eq.0, then no reflection is used.
				If reflection_on.eq.1 (default), then the incident species is reflected unchanged. Otherwise, the reflected flux is of the associated neutral species to the incident particles.
			"""),
         ( 'b2stbr_bas_recycled_neutrals_contr', 'real', '1.0', """
				Introduced for nulling recycling energy when it is zero.
			"""),
      
         ( 'b2stel_fix_recomb_energy', 'integer', '0', """
				If changed to 1, then the recombination energy (rpi) is added to the electron energy for each recombination. This should only be used if the is-->is-1 energy terms have been included in the electron cooling rates (as done by setting the switch 'b2ardr_fix_recomb' in b2ar.dat to a non-zero value and recalculating b2frates).
				See 'Atomic Physics' section.
				*** Use with caution! ***
			"""),
      
         ( 'b2stel_phm0', 'real', '0.0', """
				Multiplier of the recombination contribution to the electron cooling rate (if ADPAK rates are not used because those are already included). Assumes all recombination is three-body.
			"""),
      
      ( 'b2t*_anomalous', 'paramgroup', [
        
               ('b2tanml_anomalous', 'real', '1.0',''''''), 
        
               ('b2tfhe_anomalous', 'real', '1.0',''''''), 
        ],
         """
				Real parameter which determines anomalous current.
				Both b2tfhe_anomalous and b2tanml_anomalous point to the same switch (backward compatibility with SOLPS5.2): b2tfhe_anomalous is checked first and only if it is not found is b2tanml_anomalous looked for.
				If b2tfhe_anomalous is 0 then anomalous current is switched off otherwise anomalous current is switched on, and the numerical value of b2tfhe_anomalous acts as a multiplier to the anomalous electrical conductivity and thermo-electric coefficients provided.
			"""),
         ( 'b2tfhe_alfTeEh', 'real', '0.0', """
				When set to '0.0', the old form of the electron heat flux calculation is used.
				It is recommended to use 1.0.
			"""),
      
         ( 'b2tfhe_conduction_only', 'integer', '0', """
				When conduction_only.eq.1, convective heat transfer terms are turned off. Only to be used when benchmarking against pure conduction cases.
			"""),
      
         ( 'b2tfhe_fch_pTe', 'real', '1.0', """
				When set to '1.0', the new form of the electron heat flux calculation is used.
				It is recommended to use 1.0.
			"""),
      
         ( 'b2tfhe_lim_flux', 'integer', '1', """
				If '0', flux limit is not applied directly to the electron heat flux but is applied through transport coefficients if 'b2trcl_conductive_limit' is '1'.
				It is recommended '0'.
			"""),
      
         ( 'b2tfhe_neutral', 'real', '0.0', """
				Real parameter which multiplies ion-neutral current.
				If b2tfhe_neutral is 0 then ion-neutral current is switched off otherwise ion-neutral current is switched on.
			"""),
      
         ( 'b2tfhe_vis_par', 'real', '0.0', """
				Real parameter which multiplies current driven by parallel viscosity. 
				If b2tfhe_vis_par is 0 then viscosity-driven current is switched off otherwise viscosity-driven current is switched on.
			"""),
      
         ( 'b2tfhe_vis_q', 'real', '1.0', """
				Real parameter which multiplies current driven by heat viscosity effects.
			"""),
      
         ( 'b2tfhi_lim_flux', 'integer', '1', """
				If '0', flux limit is not applied directly to the ion heat flux but is applied through transport coefficients if 'b2trcl_conductive_limit' is '1'.
				It is recommended '0'.
			"""),
      
      ( 'b2tfnb_flux...', 'paramgroup', [
        
               ('b2tfnb_alpha', 'real', '0.0',''''''), 
        
               ('b2tfnb_gamma', 'real', '2.0',''''''), 
        
               ('b2tfnb_flux_limit_min_ti', 'real', '0.0',''''''), 
        ],
         """
				Parameters for the flux limit to the convective neutral flow.
				Alpha is a multiplier to the classical flux limit value.
				The larger alpha is, the weaker the flux limit is.
				Gamma is the exponent used in the flux-limiting formula.
				The smaller gamma is, the stronger the flux limit is.
				If alpha.eq.0, no flux limit is applied.
				flux_limit_min_ti specifies the minimum ti to be used (in eV).
			"""),
         ( 'b2tfnb_anomalous_core_only', 'integer', '0', """
				No description found.
			"""),
      
         ( 'b2tfnb_PSch', 'real', '1.0', """
				Multiplier to the Pfirsch-Schlueter flows.
			"""),
      
         ( 'b2tfnb_ycur', 'real', '1.0', """
				Ycur is a multiplier to the parallel viscosity, ion inertial and anomalous currents to the ion radial flows (particle and energy).
			"""),
      
      ( 'b2tlc0_*', 'paramgroup', [
        
               ('b2tlc0_alpha', 'real', '0.0',''''''), 
        
               ('b2tlc0_gamma', 'real', '2.0',''''''), 
        ],
         """
				Parameters for the flux limit to dpa0 - pressure driven neutral diffusion.
				Alpha is a multiplier to the classical flux limit value.
				Gamma is the exponent used in the flux-limiting formula.
				If alpha.eq.0, no flux limit is applied.
			"""),
      ( 'b2tlh0_*', 'paramgroup', [
        
               ('b2tlh0_alpha', 'real', '0.0',''''''), 
        
               ('b2tlh0_gamma', 'real', '2.0',''''''), 
        
               ('b2tlh0_flux_limit_min_ti', 'real', '0.0',''''''), 
        ],
         """
				Parameters for the flux limit to the heat conductivity of the neutrals. Alpha is a multiplier to the classical flux limit value.
				The larger alpha is, the weaker the flux limit is.
				Gamma is the exponent used in the flux-limiting formula.
				The smaller gamma is, the stronger the flux limit is.
				If alpha.eq.0, no flux limit is applied.
				flux_limit_min_ti specifies the minimum ti to be used (in eV).
			"""),
         ( 'b2tlmv_style', 'integer', '1', """
				if style = 0 then
				 it is applied the origin flux limit to the viscosity
				else
				 it is applied the SPb flux limit to the viscosity
			"""),
      
      ( 'b2tlnl_*', 'paramgroup', [
        
               ('b2tlnl_ee', 'integer', '0',''''''), 
        
               ('b2tlnl_ei', 'integer', '0',''''''), 
        
               ('b2tlnl_ii', 'integer', '0',''''''), 
        
               ('b2trcl_lambda', 'real', '-0.5',''''''), 
        ],
         """
				If lambda is positive, the Coulomb logarithm is set to lambda.
				If lambda is negative, then abs(lambda) is the lower bound to be used when computing the Coulomb logarithm according to the NRL formulae.
				The computation of the Coulomb logarithm takes place in b2tlnl.
				The default formula is to use the Braginskii formulation, which will give the same answer for electron-electron (ee), electron-ion (ei), and ion-ion (ii) collisions. Respectively, non-default values of '1', '2' and '3' for b2tlnl_ee, _ei, and _ii, respectively, make use of the calculation according to Wesson.
			"""),
         ( 'b2tqca_model', 'integer', '3', """
				If model.eq.1, use the Balescu formulation from SOLPS5.0 classical parallel ion heat diffusivity.
				If model.eq.2, use the older Braginskii SOLPS4.0 model.
				If model.eq.3, it is as model.eq.1 but without factor 4/3 which is applied to cvsahz for main ions in b2tral.F.
				It is recommended '3'.
			"""),
      
         ( 'b2tqca_phm0', 'real', '1.0', """
				Multiplier for the classical parallel viscosity.
			"""),
      
         ( 'b2tqce_model', 'integer', '1', """
				If model.eq.1, use the fitted Balescu formulation from SOLPS5.0 classical parallel electron heat diffusivity.
				If model.eq.2, use the older Braginskii SOLPS4.0 model.
				If model.eq.3, use the 21-moment Balescu results.
			"""),
      
         ( 'b2tqce_fke_Zhdanov', 'integer', '1', """
				When set to '1', Zhdanov's expression is used in the electron thermal conductivity. It is recommended to use 'b2tqce_fke_Zhdanov' '1'.
				This switch is only active if, simultaneously, one has b2tqce_model.eq.1 and b2tfhe_fch_pTe.eq.1.0.
			"""),
      
      ( 'b2tqna_ballooning*', 'paramgroup', [
        
               ('b2tqna_ballooning', 'real', '0.0',''''''), 
        
               ('b2tqna_ballooning_rescale', 'real', '1.0',''''''), 
        
               ('b2tqna_bb_ref', 'real', 'See description',''''''), 
        ],
         """
				Ballooning model switches. If ballooning.ne.0, then all transport coefficients in cell (i) are rescaled by a factor of ballooning_rescale*abs(bb_ref/bb(i))**ballooning .
				The default value for bb_ref is the arithmetic average of the total magnetic field strength over the entire computational domain.
			"""),
         ( 'b2tqna_divsol_rescale', 'integer', '1.0', """
				Scaling factor for all ion and electron transport coefficients inside divertor SOL regions.
			"""),
      
         ( 'b2tqna_ixref', 'integer', 'See description', """
				Poloidal index (on the basis mesh) of the reference surface for the flux-scaled transport model. The default value is the outer midplane, computed as such (see b2mwti_jxa in Geometry section or set_transport_ixref below):
				Single-null : ixref=rightcut1(1)-(rightcut1(1)-leftcut1(1))/4. Double-null : ixref=(rightcut1(1)+rightcut1(2))/2.
				Straight geometry : ixref=3*nx/4.
				The flux-scaled transport model is used in conjunction with scaling factors listed in column (7) of the transport coefficients description in input files b2ah.dat and b2mn.dat.
			"""),
      
      ( 'b2tqna_*_df0', 'paramgroup', [
        
               ('b2tqna_max_df0', 'integer', '1e30',''''''), 
        
               ('b2tqna_min_df0', 'real', '0.0',''''''), 
        ],
         """
				Upper and lower limits of the diffusivity coefficients df0 computed in b2tqna for each species.
			"""),
         ( 'b2tqna_model_sig', 'integer', '0', """
				If '1', use constant density in core region to calculate anomalous conductivity sig0=dfsig*qe*ne(nmdpl,-1), nmdpl - number of midplane cell.
				If '0', use sig0=dfsig*qe*ne(x,y)
			"""),
      
         ( 'b2tqna_new_df0', 'integer', '0', """
				When new_df0.eq.1, the neutral diffusivity is computed according to the local charge-exchange, ionisation and elastic collision rates, instead of the standard form with constant cross-sections.
			"""),
      
         ( 'b2tqna_pfr_rescale', 'real', '1.0', """
				Scaling factor for all ion and electron transport coefficients inside private flux regions.
			"""),
      
      ( 'b2tqna_user_transport...', 'paramgroup', [
        
               ('b2tqna_user_transport', 'integer', '0',''''''), 
        
               ('set_transport_eta', 'real', '2.0',''''''), 
        
               ('set_transport_eta_alpha', 'real', '0.5',''''''), 
        
               ('set_transport_eta_floor', 'real', '0.1',''''''), 
        
               ('set_transport_eta_ceiling', 'real', '10.0',''''''), 
        
               ('set_transport_ixref', 'integer', 'See description',''''''), 
        
               ('set_transport_iyref', 'integer', 'See description',''''''), 
        
               ('set_transport_required_te_gradient', 'real', '5.0e4',''''''), 
        ],
         """
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
			"""),
         ( 'b2trcl_lluciani', 'integer', '3', """
				If lluciani.ne.0, then transport coefficients on cells belonging to  closed field lines are modified according to the Luciani model.
				If lluciani.eq.1, the standard connection length formulation is used.
				If lluciani.eq.2, the old SOLPS4.0 formulation is used for backward compatibility.
				If lluciani.eq.3, Spb's new form Luciani's coefficient.
			"""),
      
         ( 'b2trcl_lthf21', 'integer', '0', """
				If lthf21.ne.0, then the heat transfer model is modified according to the 21-moment approach. This should only be used for multi-fluid runs.
			"""),
      
         ( 'b2trcl_lvis21', 'integer', '0', """
				If lvis21.ne.0, then the viscosities are modified according to the 21-moment approach. This should only be used for multi-fluid runs. This switch should not be used along with 'b2tfhe_vis_par' to avoid double-counting of classical viscosity effects.
			"""),
      
         ( 'b2treq_phm0', 'real', '1.0', """
				Multiplier to the temperature equipartition term.
			"""),
      
         ( 'b2trno_csig_an_style', 'integer', '1', """
				If '1', the anomalous contributions in the parallel direction to the electrical conductivity csig and the thermo-electric coefficient calf are zeroed out.
			"""),
      
         ( 'b2trno_pol_anom_scale', 'real', '1.0', """
				If pol_anom_scale.ne.1, the poloidal anomalous transport coefficients are scaled by the number. To get the same treatment as setting the old switch (radial_only) to 1, set the new switch to 0.0.
				This multiplication is to only take place for charged species.
			"""),
      
         ( 'eirene_ionising_core', 'integer', '0', """
				If <> 0 then recycles the neutral flux having crossed the core boundary within Eirene as ions. The recycling is surface-averaged, and neutrals come back as fully-stripped ions.
				'eirene_ionizing_core' is an alias for this switch.
				If the value = 1, then the flux is added by direct modification of the sources in the guard cells --- this will only work if a standard flux boundary condition is applied at that boundary.
				If the value is < 0, then the absolute value specifies which boundary in b2.boundary.parameters is to be used. This will only work for the new type 13 boundary condition.
			"""),
      
         ( 'eirene_lhalpha', 'integer', '1', """
				If 0 then no calculation of halpha in wneutral, otherwise halpha is calculated
			"""),
      
         ( 'eirene_lvib', 'integer', '0', """
				If 0 then the sigadd4 (molecular ions) and sigadd5 (negative ions) contributions to the halpha in wneutral are not included, otherwise they are
			"""),
      
         ( 'eirene_repeat_first_call', 'integer', '1', """
				If > 0 then repeats the first call to eirene in eirene_mc so many times.
				Useful if a density feedback gas puff is being used because the flux passed to Eirene on its first call is ignored (instead the value in the Eirene input file is used).
			"""),
      
         ( 'eirene_use_recyceir', 'integer', '1', """
				If > 0 use recyceir (non species dependent) to specify the recycling* coefficients, else if 0 use recyc (species dependent).
			"""),
      
         ( 'neoclassical_ic', 'integer', '3', """
				..set the contribution ic in NEOART
				  0 --- classical particle flux
				  1 --- banana plateau contribution
				  2 --- Pfirsch-Schlueter contribution
				  3 --- both banana and PS
				  4 --- all contributions
				  mind that B2 already calculates the classical transport !
				  avoid double transport, 0+4 for cross checks only !
			"""),
      
   ],

  'Atomic Physics': [
  
         ( 'b2ardr_fix_cx', 'integer', '1', """
				It is used to "correct" the CX data
				 0 => do not fix
				 1 => only fix H if CX data is < 1e-40 [default]
				 2 => fix if CX data is < 1e-40
				 3 => fix H
				 4 => fix all
				At the moment the only species with CX data in ADAS is C. Be careful with options that use the fit formula other than for H. 
				See the comments in ratstr.F for the origin of the fit formula used to "fix" the CX data.
			"""),
      
         ( 'b2ardr_fix_recomb', 'integer', '0', """
				When changed from 0, and if the ADAS option is in use, then uses the PRB file to add the contribution arising from is-->is-1 processes.
				This term includes the Bremsstrahlung.
				The default option ('0') only contains the Bremsstrahlung for the is-->is-1 process.
				This option should be used with the 'b2stel_fix_recomb_energy' option b2mn.dat set to '1'. See 'Physics' section.
				*** Use with caution! ***
			"""),
      
         ( 'b2ardr_no_weisheit', 'integer', '0', """
				When set to 1, disables the correction of the hydrogen atomic rate data with the Weisheit data using ratwei. *** Use with caution! ***
			"""),
      
      ( 'b2ardr_rtn.', 'paramgroup', [
        
               ('b2ardr_rtnt', 'integer', '40',''''''), 
        
               ('b2ardr_rtnn', 'integer', '16',''''''), 
        ],
         """
				The number of intervals in the discretisation of the density (rtnn) and temperature (rtnt) ranges for the atomic physics tables.
			"""),
   ],

  'Geometry': [
  
      ( 'b2agdr_n.iso.', 'paramgroup', [
        
               ('b2agdr_nxiso1', 'integer', '-2',''''''), 
        
               ('b2agdr_nxiso2', 'integer', '-2',''''''), 
        
               ('b2agdr_nyiso1', 'integer', '-2',''''''), 
        
               ('b2agdr_nyiso2', 'integer', '-2',''''''), 
        ],
         """
				Range of an optional isolated region to be included in the geometry. 
				The isolated region will extend over the cell range spanned by (nxiso1:nxiso2,nyiso1:nyiso2).
				If only some of the four coordinates are given, the region is made to extent from the given coordinates to the end of the grid. Neighbourhood arrays and region indices are automatically adjusted.
			"""),
      ( 'b2agfs_*cut', 'paramgroup', [
        
               ('b2agfs_leftcut', 'integer', 'See description (integer)','''
					leftcut is the poloidal index of cells directly to the RIGHT of the left branch of the cut.
				'''), 
        
               ('b2agfs_rightcut', 'integer', 'See description (integer)','''
					rightcut is the poloidal index of cells directly to the RIGHT of the right branch of the cut.
				'''), 
        
               ('b2agfs_bottomcut', 'integer', 'See description (integer)','''
					bottomcut is the radial index of cells directly below the cut.
				'''), 
        
               ('b2agfs_topcut', 'integer', 'See description (integer)','''
					topcut is the radial index of cells directly above the cut.
				'''), 
        ],
         """
				Parameters describing the position and extent of the first topological cut, i.e. corresponding to the first X-point. Needed only to force different values from the ones computed automatically by b2ag.
			"""),
      ( 'b2agfs_*cut2', 'paramgroup', [
        
               ('b2agfs_leftcut2', 'integer', 'See description (integer)','''
					leftcut2 is the poloidal index of cells directly to the RIGHT of the left branch of the second cut.
				'''), 
        
               ('b2agfs_rightcut2', 'integer', 'See description (integer)','''
					rightcut2 is the poloidal index of cells directly to the RIGHT of the right branch of the second cut.
				'''), 
        
               ('b2agfs_bottomcut2', 'integer', 'See description (integer)','''
					bottomcut2 is the radial index of cells directly below the second cut.
				'''), 
        
               ('b2agfs_topcut2', 'integer', 'See description (integer)','''
					topcut2 is the radial index of cells directly above the second cut.
				'''), 
        ],
         """
				Parameters describing the position and extent of the second topological cut, i.e. corresponding to the second X-point. Needed only to force different values from the ones computed automatically by b2ag.		
			"""),
         ( 'b2agfs_Bt_adjust', 'integer', '0', """
				Bt_adjust - integer.
				If the mesh is offset (See b2agfs_xoffset, b2agfs_yoffset below) and Bt_adjust.eq.1, then the magnetic field is recomputed, keeping the pitch constant but changing the toroidal field magnitude according to Bt = Bt0/R. To be used in b2ag.dat.
			"""),
      
         ( 'b2agfs_Bt_rescale', 'real', '1.0', """
				Bt_rescale - real*8.
				The magnetic field will be multiplied by Bt_rescale. All components of the field are scaled together. To be used in b2ag.dat.
			"""),
      
         ( 'b2agfs_Bt_reversal', 'integer', '0', """
				Bt_reversal - integer.
				If Bt_reversal.eq.1, then the sign of the toroidal field component only is reversed. The sign convention used is that a positive toroidal field leads to a Bx(grad(B)) direction pointing down, so B is out of the page when looking at the usual view of the poloidal plane with the center line on the left.
				To be used in b2ag.dat.
			"""),
      
         ( 'b2agfs_geom_match_dist', 'real', '1.0e-6', """
				Distance used as the matching criterion when reading the geometry file.
			"""),
      
         ( 'b2agfs_geometry', 'string', 'upgrade.geometry', """
				local_sonnet - character string.
				local_sonnet is the file name of the geometry file to be read.
				The file will be looked for in the run directory, in the ../baserun directory and in $SOLPSTOP/data/meshes. To be used in b2ag.dat.
			"""),
      
         ( 'b2agfs_min_pitch', 'real', '1.0', """
				Minimum allowed value for the pitch angle (in degrees) at the plates.
			"""),
      
         ( 'b2agfs_nncut', 'integer', 'See description (integer)', """
				Number of topological cuts in geometry. Needed only to force a different value from the one computed automatically by b2ag.
			"""),
      
         ( 'b2agfs_periodic_bc', 'integer', '0', """
				periodic_bc - integer.
				periodic_bc specifies if this is either an island or limiter geometry.
				If periodic_bc.eq.1 then island/limiter treatment is turned on.
				We differentiate between the two case through nncut:
				 nncut.eq.0 = limiter case
				 nncut.ge.1 = island divertor case (there should be nncut islands then)
				The case periodic_bc.eq.-1 is used to remove tranverse physics in 1-D cases.
				If periodic_bc.eq.0 then we have the usual treatment. No other values are currently allowed. To be used in b2ag.dat.
			"""),
      
         ( 'b2agfs_pit_rescale', 'real', '1.0', """
				pit_rescale - real*8.
				The magnetic field line pitch will be multiplied by pit_rescale.
				This means that the poloidal field component is multiplied by pit_rescale, while the toroidal field component is left unchanged. To reverse the plasma current direction, set pit_rescale to -1.0.
				The sign convention used is that a positive poloidal field points in the direction of increasing <ix>. Be mindful however that, when inverting the sign of the poloidal magnetic field, you are also inverting the direction of the parallel velocity. You will then need to use the 'b2mndr_inverse_ua' switch to correct for that.
				To be used in b2ag.dat.
			"""),
      
      ( 'b2agfs_.offset', 'paramgroup', [
        
               ('b2agfs_xoffset', 'real*8', '0.0',''''''), 
        
               ('b2agfs_yoffset', 'real*8', '0.0',''''''), 
        ],
         """
				xoffset and yoffset are offsets of the basis mesh in the x- and y-direction respectively. The mesh will be translated by (xoffset,yoffset) if any of the two is non-zero from its position given in the local_sonnet (See 'b2agfs_geometry' above) file.
				To be used in b2ag.dat.
			"""),
      ( 'b2agfs_.rescale', 'paramgroup', [
        
               ('b2agfs_xrescale', 'real*8', '1.0',''''''), 
        
               ('b2agfs_yrescale', 'real*8', '1.0',''''''), 
        ],
         """
				yrescale - real*8.
				Rescaling factors of the x- and y- coordinates of the basis mesh.
				To be used in b2ag.dat.
			"""),
         ( 'b2agmt_1d_width', 'real', '1.0', """
				For 1-D cases, gives the width of the domain (in m) in the third (toroidal) dimension.
			"""),
      
         ( 'b2agmx_pbs_from_basis_mesh', 'integer', '1', """
				If pbs_from_basis_mesh.eq.0, the pbs array is computed from values on the actual working mesh (old treatment).
				If pbs_from_basis_mesh.eq.1, the pbs array is computed from values on the (possibly) finer basis mesh from the geometry file and the contributions from each basis cell are added to obtain the value on the working mesh.
				In both cases, mind the value of 'b2news_area_fix', which should be also declared in b2ag.dat if the non-default behaviour is wanted.
			"""),
      
         ( 'b2agsi_isymm', 'integer', '1', """
				isymm - integer.
				isymm specifies the type of symmetry of the geometry: isymm.eq.0
				implies a slab geometry, isymm.eq.1.or.isymm.eq.2 imply rotational symmetry about the crx=0 axis, and isymm.eq.3.or.isymm.eq.4
				indicate rotational symmetry about the cry=0 axis.
				Other values are not allowed.
				isymm.eq.1.or.isymm.eq.3 mean a toroidal geometry case, i.e. with a toroidal (out-of-plane) magnetic field component.
				isymm.eq.2.or.isymm.eq.4 mean a cylindrical geometry case, i.e.
				no toroidal magnetic field component.
				To be used in b2ag.dat.
			"""),
      
         ( 'b2mwti_jxa', 'integer', 'See description', """
				Cell index, on the basis mesh, of the outer midplane. Default value depends on geometry:
				Single-null : jxa=rightcut1(1)-(rightcut1(1)-leftcut1(1))/4, i.e. three quarters of the way between the two cuts. Double-null : jxa=(rightcut1(1)+rightcut1(2))/2, i.e. halfway between the two outer cuts.
				Straight geometry : jxa=3*nx/4
			"""),
      
         ( 'b2mwti_jxi', 'integer', 'See description', """
				Cell index, on the basis mesh, of the inner midplane. Default value depends on geometry:
				Single-null : jxi=leftcut1(1)+(rightcut1(1)-leftcut1(1))/4, i.e. one quarter of the way between the two cuts. Double-null : jxi=(rightcut1(1)+rightcut1(2))/2, i.e. halfway between the two inner cuts.
				Straight geometry : jxi=nx/4
			"""),
      
      ( 'b2stbc_coreregn*', 'paramgroup', [
        
               ('b2stbc_coreregno', '', 'integer',''''''), 
        
               ('b2stbc_coreregn2', '', 'integer',''''''), 
        ],
         """
				coreregno is the boundary index of the core boundary in the input files b2ah.dat and b2mn.dat. For a standard single-null case, coreregno is 1. For a straight geometry or limiter case, it is likely that coreregno need be set to 0, depending on the actual geometry details.
				coreregn2 is the boundary index of the second core boundary in case of a double-null geometry, and is not used otherwise.
			"""),
      ( 'b2stbc_pfrregno.', 'paramgroup', [
        
               ('b2stbc_pfrregno1', 'integer', '0',''''''), 
        
               ('b2stbc_pfrregno2', 'integer', '2',''''''), 
        ],
         """
				pfrregno1 is the boundary index of the first half of the private flux region boundary on which feedback is being applied (through b2stbc_ndes or b2stbc_private_flux_puff) in the input files b2ah.dat and b2mn.dat. pfrregno2 is the second half of the same private flux region. For a standard single null, the pair should be (0,2). For a standard double-null, the lower private flux region is labelled with the pair (0,5), and the upper private flux region with the pair (2,3). One can use only one private flux region by setting pfrregno1.eq.pfrregno2.
			"""),
         ( 'b2stbc_solregno', 'integer', '3', """
				solregno is the boundary index of the SOL North boundary in the input files b2ah.dat and b2mn.dat. For a standard single-null case, solregno is 3. For a standard double-null case, solregno for the outer SOL North boundary would be 7.
			"""),
      
         ( 'b2stbr_first_flight_no_of_start_points', 'integer', '2*(nx+2)+2*max(nncut,1)*(ny+2)', """
				When the first flight model is turned on, this number must be greater than or equal to the number of boundary cells on the mesh.
				Only in cases with special geometries (i.e. limiters, islands, ...) need it be increased beyond the default value above. This variable is only used within the first flight module.
			"""),
      
   ],

  'Atomic Physics': [
  
         ( 'b2ardr_fix_cx', 'integer', '1', """
				It is used to "correct" the CX data
				 0 => do not fix
				 1 => only fix H if CX data is < 1e-40 [default]
				 2 => fix if CX data is < 1e-40
				 3 => fix H
				 4 => fix all
				At the moment the only species with CX data in ADAS is C. Be careful with options that use the fit formula other than for H. 
				See the comments in ratstr.F for the origin of the fit formula used to "fix" the CX data.
			"""),
      
         ( 'b2ardr_fix_recomb', 'integer', '0', """
				When changed from 0, and if the ADAS option is in use, then uses the PRB file to add the contribution arising from is-->is-1 processes.
				This term includes the Bremsstrahlung.
				The default option ('0') only contains the Bremsstrahlung for the is-->is-1 process.
				This option should be used with the 'b2stel_fix_recomb_energy' option b2mn.dat set to '1'. See 'Physics' section.
				*** Use with caution! ***
			"""),
      
         ( 'b2ardr_no_weisheit', 'integer', '0', """
				When set to 1, disables the correction of the hydrogen atomic rate data with the Weisheit data using ratwei. *** Use with caution! ***
			"""),
      
      ( 'b2ardr_rtn.', 'paramgroup', [
        
               ('b2ardr_rtnt', 'integer', '40',''''''), 
        
               ('b2ardr_rtnn', 'integer', '16',''''''), 
        ],
         """
				The number of intervals in the discretisation of the density (rtnn) and temperature (rtnt) ranges for the atomic physics tables.
			"""),
   ],
   
}
