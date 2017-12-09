# Generated with create-addmenu.xslt
# xsltproc create-addmenu.xslt solps-input.xml &gt; ../../solps-gui/src/widgets/b2menu.py

b2mn_menu = {
# Category : ( parameter, type, default, description )
#         or ( parametergroup, 'paramgroup', [(name, type, default, description)...], description)
  
  'Run': [ '',
  
      ( 'b2mndr_id', 'switchgroup', [
        
               ('b2mndr_run_number', 'integer', '1000',''''''), 
        
               ('b2mndr_shot_number', 'integer', '0',''''''), 
        
               ('b2mndr_device', 'string', '$(DEVICE)',''''''), 
        
               ('b2mndr_user', 'string', '$(USER)',''''''), 
        ],
         """
					These switches server as identification for the simulation. They can be inherited from SOLPS-GUI:
					Run number : The number of the run.
					Shot number : Shot number identifying the run. Defaults to the last number found in shotnumber.history, or 0 if the file is not found.
					Device : The device where the simulation was run.
					User : The user who ran the simulation.
				"""),
         ( 'b2aidr_read_b2fstate', 'integer', '0', """
					If read_b2fstate.ne.0, b2aidr will read an existing b2fstate file and append to it a flat state description for additional new species being introduced in the run.
				"""),
      
         ( 'b2mndr_ntim', 'integer', '1', """
					Number of timesteps desired in this run. If ntim.eq.0, the code simply reads the input file and creates the b2fplasma and b2fstate files corresponding to the present plasma state.
				"""),
      
         ( 'b2mndr_dtim', 'real', '1.0', """
					Timestep (in seconds).
				"""),
      
      ( 'b2mndr_d*', 'switchgroup', [
        
               ('b2mndr_delta_max', 'real', '0.0',''''''), 
        
               ('b2mndr_delta_min', 'real', '0.0',''''''), 
        
               ('b2mndr_dt_change_dec', 'real', '1.0',''''''), 
        
               ('b2mndr_dt_change_inc', 'real', '1.0',''''''), 
        
               ('b2mndr_dt_max', 'real', '1.0e+01',''''''), 
        
               ('b2mndr_dt_min', 'real', '1.0e-30',''''''), 
        ],
         """
					One of the dynamic timestep control parameters. Only active if both delta_max and delta_min are nonzero. The timestep is increased by a factor dt_change_inc or decreased by a factor dt_change_dec, within the bounds [dt_min, dt_max], according to whether the largest instantaneous change in all equations is smaller than delta_min or larger than delta_max, respectively.
				"""),
         ( 'b2mndr_stim', 'real', '0.0', """
					stim specifies the initial time --- default 0.
					If set to a positive or zero value, this overwrites the time value read from b2fstati.
					If set to a negative value, the run continues from the time read in b2fstati. In that case, the tracing data is appended to the existing files, otherwise the tracing files are overwritten.
				"""),
      
         ( 'b2mndr_etim', 'real', '0.0', """
					etim specifies the end time. Only active if etim &gt; stim.
				"""),
      
      ( 'b2mndt_nstg.', 'switchgroup', [
        
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
					See 'Numerics' section for details.
				"""),
         ( 'b2news_no_solve', 'integer', '0', """
					If no_solve.eq.1, then the code is run without actually solving any equations. All secondary and dependent data is computed.
					The nstg(0:2) array is overwritten to '1's. The simulation time will not be updated. The code will compute fluxes, sources, transport coefficients, etc...
					'ntim' times but not update the basic plasma quantities. Additionally, if no_solve is set to a negative value, then only some equations are solved (simulation time and nstg arrays will behave normally).
					no_solve.eq.-1 will activate the parallel momentum equations only.
					no_solve.eq.-2 will activate the density equations only. no_solve.eq.-4 will activate the potential equation only. (Active only if poteq.eq.1, otherwise, the behaviour dictated by the poteq setting applies).
					no_solve.eq.-8 will activate the heat equations only. These can be combined. For example, no_solve.eq.-3 will activate the parallel momentum and particle conservation equations.
					If the no_solve switch requires an equation not to be solved, the settings in the corresponding solvexx arrays from b2.numerics.parameters are moot.
					The latter are reserved for fine-tuning numerical diagnostics.
				"""),
      
         ( 'b2mndr_cpu', 'real', '0.0', """
					CPU limit. If cpu.eq.0.0, no CPU limit is enforced. Otherwise, the code stops smoothly after it has been running for at least 'cpu' CPU seconds.
				"""),
      
         ( 'b2mndr_elapsed', 'real', '0.0', """
					Elapsed time limit. Is elapsed.eq.0.0, no time limit is enforced.
					Otherwise, the code stops smoothly after is has been running for at least 'elapsed' wall clock seconds.
				"""),
      
         ( 'b2mndr_savecpu', 'real', '3600.0', """
					CPU time interval after which save files plasmastate.xxxx are written.
					These can be used, in conjunction with the b2co.exe instruction, to recover a crashed run.
				"""),
      
         ( 'b2mndr_ismain', 'real', '1', """
					ismain identifies the index of the main plasma species.
					It must hold that ismain is not a neutral species.
				"""),
      
      ( 'b2news_facdrift*', 'switchgroup', [
        
               ('b2news_facdrift_dec', 'real', '0.0',''''''), 
        
               ('b2news_facdrift_inc', 'real', '1.0',''''''), 
        
               ('b2news_facdrift_start', 'real', '0.0',''''''), 
        
               ('b2news_facdrift_target', 'real', '0.0',''''''), 
        ],
         """
					Ramping parameters for facdrift, which multiplies the diamagnetic terms as well as the ion inertia current. The code is started on the first time step with facdrift=facdrift_start. If facdrift_target.ne.facdrift_start, then, on each time step, facdrift is multiplied by facdrift_inc. If the code does not converge on the timestep, facdrift is decreased by facdrift_dec. A facdrift profile is also possible, see Numerics section for details.
					The ion-neutral friction current requires either facdrift or fac_ExB to be turned on as well.
				"""),
      ( 'b2news_facExB_*', 'switchgroup', [
        
               ('b2news_facExB_dec', 'real', '0.0',''''''), 
        
               ('b2news_facExB_inc', 'real', '1.0',''''''), 
        
               ('b2news_facExB_start', 'real', '0.0',''''''), 
        
               ('b2news_facExB_target', 'real', '0.0',''''''), 
        ],
         """
					Ramping parameters for facExB, which multiplies the ExB terms. Same treatment as above for facdrift.
				"""),
      ( 'b2news_facvis_*', 'switchgroup', [
        
               ('b2news_facvis_dec', 'real', '0.0',''''''), 
        
               ('b2news_facvis_inc', 'real', '1.0',''''''), 
        
               ('b2news_facvis_start', 'real', '0.0',''''''), 
        
               ('b2news_facvis_target', 'real', '0.0',''''''), 
        ],
         """
					Ramping parameters for facvis, which multiplies the drift viscosity terms. Same treatment as above for facdrift.
				"""),
      ( 'b2srdt_*_namelist', 'switchgroup', [
        
               ('b2stbc_boundary_namelist', 'integer', '0',''''''), 
        
               ('b2stbr_neutrals_namelist', 'integer', '0',''''''), 
        
               ('b2srdt_numerics_namelist', 'integer', '0',''''''), 
        
               ('b2tqna_transport_namelist', 'integer', '0',''''''), 
        ],
         """
					Namelist file indicators. If xxx_namelist.eq.1, then the code looks for the file b2.xxx.parameters, in which it expects to find the xxx namelist.
				"""),
         ( 'b2sral_inputfile', '', '0', """
					Profiles file indicator. If b2sral_inputfile.eq.1, then the code looks for the file b2.sources.profile in which it expects to find the 'profile' namelist.
					This namelist will contain profiles of sources measured from the location (ixref,iyref) (default is outer midplane separatrix), which is set with the 'set_transport_i[xy]ref' switches.
				"""),
      
         ( 'b2tqna_inputfile', 'integer', '0', """
					Profiles file indicator. If b2tqna_inputfile.eq.1, then the code looks for the file b2.transport.inputfile, in which it expects to find the transport namelist.
					This namelist will contain profiles of sources transport parameters measured from the location (ixref,iyref) (default is outer midplane separatrix), which is set with the 'set_transport_i[xy]ref' switches.
				"""),
      
         ( 'b2mndr_eirene', 'integer', '0', """
					Turns on coupling with the Eirene Monte-Carlo neutral code if nonzero.
					To be used, the code must be compiled with the -DB25_EIRENE option.
				"""),
      
         ( 'b2mndr_astra', 'integer', '0', """
					Turns on coupling with the ASTRA core transport code if nonzero.
					To be used, the code must be compiled with the -DASTRA option.
				"""),
      
         ( 'b2mndr_rescale_neutrals_sources', 'real', '1.0', """
					Multiplier to the neutral sources (either computed by Eirene or the corresponding rate coefficients).
				"""),
      
         ( 'b2mndr_rescale_neutrals', 'real', '1.0', """
					Multiplier to the neutral density on the first timestep.
				"""),
      
         ( 'b2mndr_density_rescale', 'real', '1.0', """
					Multiplier of all densities on the first timestep.
				"""),
      
         ( 'b2stbr_core_sources_rescale', 'real', '1.0', """
					Multiplier to the totally ionised species sources at the core boundary.
				"""),
      
         ( 'b2mndt_density_control', 'integer', '0', """
					Feedback on the total heavy particle density. If density_control.ne.0, the sum of all densities is kept constant.
				"""),
      
         ( 'b2stbc_feedback', 'integer', '0', """
					If feedback.eq.1, turns on feedback mode for the boundary conditions.
					See Physics section for more details. Equivalent to LFEEDBACK=.true. in the b2.boundary.parameters namelist.
				"""),
      
         ( 'b2stbc_ncallfeedback', 'integer', '0', """
					Timestep index after which the feedback in b2stbc is activated.
				"""),
      
         ( 'b2stbr_first_flight', 'integer', '0', """
					If first_flight.ne.0, turns on the first flight model. See Physics section for additional details.
				"""),
      
         ( 'b2ytdr_ns', 'integer', 'ns', """
					New number of species desired when creating a new initial state file using b2yt.exe. Must be specified within b2yt.dat.
				"""),
      
         ( 'b2ytdr_ndepth1', 'integer', 'ndepth_nml', """
					New resolution of target depth desired when creating a new initial state file using b2yt.exe. Must be specified within b2yt.dat.
				"""),
      
         ( 'b2ytdr_rescale_neutrals', 'real', '1.0', """
					Rescaling of neutral densities by rescale_neutrals when creating a new initial state file using b2yt.exe. Must be specified within b2yt.dat.
				"""),
      
         ( 'b2ytdr_non_commensurate', 'integer', '0', """
					When set to 1, b2yt will attempt to interpolate a plasma solution and create new input files for a new grid which is not commensurate to the original grid, but still has the same topology.
					Must be specified within b2yt.dat.
				"""),
      
   ],

  'Output': [ '',
  
         ( 'b2mndr_b2time', 'integer', '1', """
					Specifies the number of timesteps between writes of the b2time.nc time-dependent file. If b2time.gt.0, always writes out on the last timestep. If b2mndr_stim.lt.0, data from the current run is appended to the existing b2time.nc file, otherwise the file is overwritten.
				"""),
      
         ( 'b2mndr_tally', 'integer', '1', """
					Specifies the number of timesteps between writes of tallies. If tally.gt.0, always writes out on the last timestep.
				"""),
      
         ( 'b2mndt_moitlv', 'integer', '-1', """
					Controls detailed monitoring output. moitlv.eq.-1 means no output, moitlv.eq.0 means output once per timestep, moitlv.eq.1 means output once per nstg0 iteration, moitlv.eq.2 means output once per nstg1 iteration and moitlv.eq.3 means output once per nstg2 iteration. See 'b2mndr_nstg?' description in Run section for more details.
				"""),
      
         ( 'b2mndt_moqtlv', 'integer', '3', """
					Controls quick trace output. moqtlv.eq.-1 means no output, moqtlv.eq.0 means output once per timestep, moqtlv.eq.1 means output once per nstg0 iteration, moqtlv.eq.2 means output once per nstg1 iteration and moqtlv.eq.3 means output once per nstg2 iteration. See 'b2mndr_nstg?' description in Run section for more details.
				"""),
      
         ( 'b2mndr_mvnum', 'integer', '0', """
					Specifies the maximum number of instances at which movie data will be output.
				"""),
      
         ( 'b2mndr_mvinc', 'integer', '1', """
					Specifies the number of timesteps between movie output. If greater than 1 and the last timestep does not correspond to a planned frame, an extra endstate frame is added.
				"""),
      
         ( 'b2mndr_plasnum', 'integer', '0', """
					Specifies the maximum number of instances at which extra writes of b2fplasmf.xxxx will occur.
				"""),
      
         ( 'b2mndr_plasinc', 'integer', '1', """
					Specifies the number of timesteps between b2fplasmf.xxxx writes.
				"""),
      
         ( 'b2mndr_cdfmovietim', 'real', '0.0', """
					Another option for movie output. Give the real-time interval between movie frames.
				"""),
      
         ( 'b2mndr_ntim_save', 'integer', '0', """
					Another option for plasma state file output. Give the number of B2.5 full interations between succesive write-ups of plasmastate files, in addition to the ones written at regular CPU intervals. Should be used, at the exclusion of other plasmastate write-up frequency settings, in conjunction with the Leuven Monte-Carlo averaging scheme.
				"""),
      
         ( 'b2mndt_av', 'integer', '0', """
					If b2mndt_av.gt.0, turns on computation of running averages.
				"""),
      
         ( 'b2mndt_av_continue', 'integer', '1', """
					If b2mndt_av_continue.gt.0, continuously perform running averages.
				"""),
      
         ( 'b2mndt_av_ntim_batch', 'integer', '500', """
					If ntim_batch.gt.0, number of iterations used to compute batch averages.
				"""),
      
         ( 'b2mndt_av_ntim_run', 'integer', '1000', """
					If ntim_run.gt.0, number of iterations used for writing running averages.
				"""),
      
         ( 'b2mndt_av_batch_all', 'integer', '0', """
					If b2mndt_av_batch_all.gt.0, produces standard output for batch averages.
				"""),
      
         ( 'b2mndr_plasmatim', 'real', '0.0', """
					Another option for plasma state file output. Give the real-time interval between succesive write-ups of plasmastate files, in addition to the ones written at regular CPU intervals.
				"""),
      
         ( 'b2wdat_iout', 'integer', '0', """
					If iout.eq.1, a large set of *.dat output files will be produced containing the values of a variety of code quantities.
					If iout.eq.4, a more select set of output files will be produced, which usually suffices for everyday analysis.
					For more detailed debugging analysis, one should instead use "procedure_name"_iout.eq.1.
					The files and their content are fully described in the Output_description.pdf file in the SOLPSTOP/doc directory.
				"""),
      
         ( 'b2wdat_append', 'integer', '0', """
					If append.eq.1, the *.dat output files are appended upon every write, instead of being rewritten every time.
				"""),
      
         ( 'b2mndr_old_style', 'integer', '0', """
					If old_style.gt.0, old-fashioned (SOLPS4 style) output is added at the end of the b2mn.prt file.
				"""),
      
         ( 'b2mndr_av_read', 'integer', '0', """
					If ird_aver.gt.0, the averaged solution is read from the b2faveri file and written in the b2favere file at the end of the run.
				"""),
      
      ( 'b2mndr_*', 'switchgroup', [
        
               ('b2mndr_na_eps', 'real', '1.0e19',''''''), 
        
               ('b2mndr_po_eps', 'real', '1.0e+1',''''''), 
        
               ('b2mndr_te_eps', 'real', '1.0e+1',''''''), 
        
               ('b2mndr_ti_eps', 'real', '1.0e+1',''''''), 
        
               ('b2mndr_ua_eps', 'real', '1.0e+4',''''''), 
        ],
         """
					The five switches above are safeguards numbers for when printing changes after a time-step. The change is computed as: deltaX = abs((X(t)-X(t-1))/(X(t)+X_eps))
				"""),
         ( 'b2mndr_trantim', 'real', '0.0', """
					Produces a numbered 'tran' file every trantim real-time seconds. An endstate file is written if it falls between scheduled write-up times. Only available within the -DJET environment.
				"""),
      
         ( 'b2mwti_target_offset', 'integer', '1', """
					The diagnostic values from b2time.nc use guard cell values if target_offset.eq.0, and values from the neighbouring real cell if target_offset.eq.1. Fluxes are not affected.
				"""),
      
         ( 'b2mwti_2dwrite', 'integer', '0', """
					Controls additional output to b2time.nc.  If eq 1 then a few 2d arrays (ne, Te, Ti) are written with each write to b2time.nc. If eq 2 then fluxes, po, kinetic energy, and fluid particle and energy source terms are also included (e.g., rsana, rsahi, rqrad).
				"""),
      
         ( 'b2mwti_ismain0', 'integer', '0', """
					Index of the species used to create the 'dp3d?.last10' diagnostic files.
					Defaults to the neutral species associated with ismain. If no such species is declared, the default will be set to ismain. Is expected to either correspond to a neutral species or to ismain.
					If ismain is also defaulted, then will be 0.
				"""),
      
         ( 'b2mwqt_style', 'integer', '1', """
					Specifies the amount of data that is written out to b2ftrace. See the manual (Section on b2yq) for full details.
				"""),
      
      ( 'b2stbr_*_netcdf', 'switchgroup', [
        
               ('tallies_netcdf', 'integer', '0',''''''), 
        
               ('b2stbr_b2wall_netcdf', 'integer', '0',''''''), 
        
               ('balance_netcdf', 'integer', '0',''''''), 
        
               ('balance_average', 'integer', '0',''''''), 
        ],
         """
					If tallies_netcdf.ne.0, the file 'b2tallies.nc' is created, which contains the regional tallies in CDF format. If b2mndr_stim.lt.0, data from the current run is appended to the existing b2tallies.nc file, otherwise the file is overwritten.
					If b2wall_netcdf.ne.0, the file 'b2wall.nc' is created, which contains the wall tallies in CDF format [written every b2wall_netcdf 'main calls']. If b2mndr_stim.lt.0, data from the current run is appended to the existing b2wall.nc file, otherwise the file is overwritten.
					If balance_netcdf.ne.0, the file 'balance.nc' is created, which contains all of the arrays required by the balance post-processing routines, in CDF format.
					If balance_average.ne.0, the balance arrays are averaged over all b2mndr_ntim timesteps.
				"""),
         ( 'ank_tracing', 'integer', '0', """
					If ank_tracing.ge.1, additional tracing output from Andrei Kukushkin is produced, in files to be found in the tracing/ directory inside the run directory. The traces will be written every ank_tracing iteration. If b2mndr_stim.lt.0, data from the current run is appended to the existing files, otherwise the files are overwritten.
				"""),
      
         ( 'b2stbc_diagno', 'integer', '0', """
					Controls level of output in b2stbc and subservient routines.
					Level 1 (diagno.ge.1) output includes wrong_flow warnings, transport coefficients at the (nx/2,ny) basis mesh position, the solution found for the given heat flux at constant temperature bc, and all feedback diagnostics.
					Level 2 output (diagno.ge.2) includes the integral current correction, the boundary sources on the first call, excessive sound speeds, and the iterative progress to the given heat flux at constant temperature bc.
					Level 3 output (diagno.ge.3) includes the boundary sources on each call, and the boundary.prt file listing all boundary cells.
				"""),
      
         ( 'b2stbr_output', 'integer', '0', """
					Output flag for the first_flight model. If output.ge.1, the files start, end, and fort.88 are created, which contain information about the chords used in the model.
				"""),
      
         ( 'b2npmo_vlct_diagno', 'integer', '1', """
                   Output flag to control diagnostics related to use of ion_vlct_restrict switch.
				   If vlct_diagno.eq.0, the velocity restrictions are applied silently.
				   If vlct_diagno.eq.1 (default), the user only gets a count of how many times the velocity restriction has been applied for each species, if any.
				   If vlct_diagno.eq.2, the user gets the full details of where and how large the applied velocity restriction was, if any.
				"""),
      
      ( 'eirene_savef3*', 'switchgroup', [
        
               ('eirene_savef30', 'integer', '0',''''''), 
        
               ('eirene_savef31', 'integer', '0',''''''), 
        ],
         """
					For coupled runs, the code will create two files named fort.30 and fort.31, containing the plasma geometry and plasma state, respectively, for use by Eirene. This happens irrespective of the setting of the two switches above. If however, the user wishes to obtain these files for a non-coupled run, then these two switches can be set to 1 and the files will then be produced at the end of the run. If savef31.lt.0, then a fort.31.###### file is produced after every B2.5 time step. Additionally, if savef31.ne.0, the fort.31 file will be updated before every Eirene call for coupled runs.
				"""),
         ( 'b2mndr_inverse_ua', 'integer', '0', """
					If inverse_ua.eq.1, the code will produce a 'b2fstati_with-ua' file that contains the same plasma information, but with the opposite sign convention for the parallel velocity. The run will then proceed with the new velocities with their sign inverted.
				"""),
      
         ( 'b2yrdr_ns', 'integer', 'ns', """
					New number of species desired when reading a new atomic rates file using b2yr.exe. Must be specified within b2yr.dat.
					To be used for checking atomic rates after bundling and before any plasma state files have been created or converted, i.e. when the number of species in the atomic rates file b2frates does not match the number of species declared in the run parameters file b2fpardf.
				"""),
      
         ( 'b2srsm_diagno', 'integer', '0', """
					Controls level of output in b2srsm. If diagno.ge.2, output will be given on every call. If diagno.eq.1, output will be given on main calls only.
				"""),
      
         ( 'b2ux5p_cpu', 'integer', '0', """
					If cpu.gt.0, prints out the time spent in the matrix solver.
				"""),
      
      ( 'b2ux*', 'switchgroup', [
        
               ('b2ux5p_nltrsol', 'integer', '2',''''''), 
        
               ('b2ux7p_nltrsol', 'integer', '0',''''''), 
        
               ('b2ux9p_nltrsol', 'integer', '0',''''''), 
        ],
         """
					Output flag for the iluter matrix solver. Larger numbers mean increasing output level.
				"""),
         ( 'eirene_mc_output_style', 'integer', '1', """
					If nonzero, prints sources computed by Eirene. If greater than 1, prints them on every use of the recycling sources, not just when they are computed.
				"""),
      
         ( 'ma28_nwrite', 'integer', '0', """
					If nwrite.gt.0, prints the content of the sparse matrix in the b2_matrix file, for the first nwrite calls.
				"""),
      
         ( 'b2news_ncallout', 'integer', '-1', """
					If the iteration number is equal to ncallout, then several output files 'b2ne_npmo', 'b2ne_xppb', 'b2ne_npco', 'b2ne+nppo' which detail the convergence behaviour and residuals.
				"""),
      
         ( 'b2tqna_diagno', 'integer', '0', """
					If diagno.gt.0, outputs details of the calculations of neutral transport coefficients when using the new_df0 model. See switch b2tqna_new_df0 for more details.
				"""),
      
      ( 'b2mndr_idout.', 'switchgroup', [
        
               ('b2mndr_idout0', '', 'pgnl;pgmm;pzmm',''''''), 
        
               ('b2mndr_idout1', '', 'pzmm',''''''), 
        ],
         """
					idout0 and idout1 specify the desired selection of output segments; idout0 for output before the calculation and idout1 for output at the conclusion of the calculation. The generic description of either of these 'idout' variables follows. idout specifies the desired selection of output segments for printed and graphical output. Associated with each segment is a four-character word, which is identified on the printed output. (The same word may be associated with several segments.) A particular segment will be produced only if its associated word has a match, as defined by the routine strmas, in idout.
				"""),
         ( 'eirene_format', 'string', 'iter', """
					This switch is to be provided within b2yt.dat to indicate to the b2yt converter the format of the original Eirene input.dat file to be modified. The accepted values are (case-insensitive):
					'old' for input files from SOLPS4.0 and SOLPS5.0 runs using 'old' Eirene_96
					'new' for input files from SOLPS4.0 and SOLPS5.0 runs using 'new' Eirene_99
					'facelift' for input files from SOLPS5.1 runs
					'juelich' for input files from Juelich Eirene versions (2008 and younger)
					'iter' for input files from SOLPS4.2/4.3 and SOLPS-ITER runs
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

  'Physics': [ '',
  
         ( 'b2siav_addvis', 'real', '0.0', """
					Multiplier to heat flux contribution to divergence of viscosity tensor in the momentum equation.
				"""),
      
         ( 'b2siav_addvis1', 'real', '1.0', """
					When not equal to '0.0', adds contribution to divergence of viscosity tensor coming from x-variations in B.
				"""),
      
         ( 'b2siav_style_qip', 'integer', '0', """
					If style_qip.eq.1, adds a classical ion heat conductivity term to the heat flux used to compute the heat viscosity current (see manual for full details).
				"""),
      
         ( 'b2npmo_b2sifr_', 'integer', '1', """
					If b2sigp_style is set to '2', this switch has no effect.
					When set to '1', the new correct form of the friction force is used, applicable for non-hydrogenic plasmas or hydrogenic mixtures.
					The value '0' corresponds to the old SOLPS5.0 treatment.
				"""),
      
         ( 'b2sihs_istyle_Joule_heating', 'integer', '1', """
					When set to '1', there is no radial contribution in Joule heating because there are no physical reasons to take it into account.
					The value '0' corresponds to the old SOLPS5.0 treatment.
				"""),
      
         ( 'b2sian_phm0', 'real', '1.0', """
					Multiplier to the parallel momentum source term associated with the anomalous current. It is recommended '1.0'.
					The value '0.0' corresponds to the old SOLPS5.0 treatment.
				"""),
      
         ( 'b2sicf_phm0', 'real', '1.0', """
					Multiplier of the centrifugal force term. It is recommended '1.0'.
					The value '0.0' corresponds to the old SOLPS5.0 treatment.
				"""),
      
         ( 'b2sicf_phm1', 'real', '1.0', """
					Multiplier of the centrifugal force correction term due to linearization.
					It is recommended '1.0'.
					The value '0.0' corresponds to the old SOLPS5.0 treatment.
				"""),
      
      ( 'b2t*_anomalous', 'switchgroup', [
        
               ('b2tfhe_anomalous', 'real', '1.0',''''''), 
        
               ('b2tanml_anomalous', 'real', '1.0',''''''), 
        ],
         """
					Real parameter which determines anomalous current.
					Both b2tfhe_anomalous and b2tanml_anomalous point to the same switch (backward compatibility with SOLPS5.2): b2tfhe_anomalous is checked first and only if it is not found is b2tanml_anomalous looked for.
					If b2tfhe_anomalous is 0 then anomalous current is switched off otherwise anomalous current is switched on, and the numerical value of b2tfhe_anomalous acts as a multiplier to the anomalous electrical conductivity and thermo-electric coefficients provided.
				"""),
         ( 'b2news_ExB', 'real', '0.0', """
					Real parameter which multiplies ExB flows. If b2news_ExB.eq.0 and b2news_facExB_start.eq.0 then ExB flows are switched off. If b2news_ExB is nonzero, then ExB flows are multiplied by that constant throughout the run.
					See also Run section on switches b2news_facExB_... for more details. A spatial fac_ExB profile is also possible, see Numerics section for details.
				"""),
      
         ( 'b2tiner_inert', 'real', '1.0', """
					Real parameter which multiplies the ion inertial current.
				"""),
      
         ( 'b2tfhe_dia_cur', 'real', '1.0', """
					Real parameter which multiplies the diamagnetic current.
				"""),
      
         ( 'b2tfhe_vdia_par', 'real', '1.0', """
					Real parameter which multiplies the convective heat flux due to grad B-drift of guiding centers in non-modified heat fluxes of electrons and ions.
				"""),
      
         ( 'b2tfhe_neutral', 'real', '0.0', """
					Real parameter which multiplies the ion-neutral current.
					If b2tfhe_neutral is 0 then the ion-neutral current is switched off otherwise the ion-neutral current is switched on.
					The ion-neutral current also requires either the diamagnetic or ExB drifts to be turned on as well.
				"""),
      
         ( 'b2tinnt_fchin_in_core', 'integer', '0', """
					Integer switch to turn off or on the ion-neutral current in the core region (applies to coupled runs only). This is recommended in cases where the neutral densities are very low in the core region and the ion-neutral current is likely to vary widely from one iteration to the next as a result of Monte-Carlo noise.
					If fchin_in_core.eq.0 (default), then fchin is set to zero in the core.
					If fchin_in_core.eq.1, then fchin is unchanged.
				"""),
      
         ( 'b2tfhe_PSch', 'real', '1.0', """
					Real parameter which multiplies the Pfirsch-Schlueter electron heat flux and conductivity.
				"""),
      
         ( 'b2tfhe_vis_par', 'real', '0.0', """
					Real parameter which multiplies the current driven by parallel viscosity.
					If b2tfhe_vis_par is 0 then the viscosity-driven current is switched off otherwise the viscosity-driven current is switched on.
				"""),
      
         ( 'b2tfhe_vis_q', 'real', '1.0', """
					Real parameter which multiplies the current driven by heat viscosity effects.
				"""),
      
         ( 'b2tfhe_stochastic', 'real', '0.0', """
					Real parameter which turns on stochastic current.
					If b2tfhe_stochastic is 0 then stochastic current is switched off otherwise stochastic current is switched on.
				"""),
      
         ( 'b2tstch_delta', 'real', '0.0', """
					Width of the stochastic current layer (in meters), measured from the separatrix inward, along the poloidal index ixref (given by b2tqna_ixref).
					If b2tfhe_stochastic.ne.0, then b2tstch_delta must be greater than zero.
				"""),
      
         ( 'b2tstch_sig', 'real', '1.0', """
					Multiplier to the magnetic field line stochastic diffusion coefficient, describing the stochastic conductivity.
				"""),
      
         ( 'b2trno_con_e_stochastic', 'real', '1.0', """
					Multiplier to the stochastic conductivity.
				"""),
      
         ( 'b2trcl_lluciani', 'integer', '3', """
					If lluciani.ne.0, then transport coefficients on cells belonging to closed field lines are modified according to the Luciani model.
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
      
         ( 'b2sqel_artificial_radiation', 'real', '0.0', """
					If art_rad.ne.0, then an artificial radiation loss term is added to the electron cooling rate. Art_rad represents the percent fraction of impurities in the plasma.
				"""),
      
      ( 'b2stbc_*', 'switchgroup', [
        
               ('b2stbc_fheycore', 'real', '0.0',''''''), 
        
               ('b2stbc_fhiycore', 'real', '0.0',''''''), 
        
               ('b2stbc_fhiycore_kinetic_energy', 'integer', '0',''''''), 
        
               ('b2stbc_fchycore', 'real', '-1.0e30',''''''), 
        
               ('b2stbc_fnaycore', 'real', '-1.0e30',''''''), 
        
               ('b2stbc_isfeedback', 'integer', '0',''''''), 
        
               ('b2stbc_iyped', 'real', 'jsep/2',''''''), 
        
               ('b2stbc_ndes', 'real', '0.0',''''''), 
        
               ('b2stbc_ndes_sol', 'real', '0.0',''''''), 
        
               ('b2stbc_nepedm_sol', 'real', '0.0',''''''), 
        
               ('b2stbc_nesepm', 'real', '0.0',''''''), 
        
               ('b2stbc_nesepm_overshoot', 'real', '0.0',''''''), 
        
               ('b2stbc_nesepm_pfr', 'real', '0.0',''''''), 
        
               ('b2stbc_nesepm_sol', 'real', '0.0',''''''), 
        
               ('b2stbc_private_flux_puff', 'real', '0.0',''''''), 
        
               ('b2stbc_volrec', 'real', '0.0',''''''), 
        
               ('b2stbc_volrec_overshoot', 'real', '0.0',''''''), 
        
               ('b2stbc_nesepm_minpuff', 'real', '0.0',''''''), 
        
               ('b2stbc_nesepm_maxpuff', 'real', '0.0',''''''), 
        
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
					nesepm_sol is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the SOL region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the SOL North boundary (See Geometry section for the SOL North boundary index solregno). If nesepm_overshoot.gt.1.0, the gas puff is turned off when the midplane separatrix density reaches nesepm*nesepm_overshoot. Minimum and maximum values of the feedback gas puff can be set using b2stbc_nesepm_minpuff and b2stbc_nesepm_maxpuff
					nepedm_sol is similar to nesepm_sol but the feedback is exerted on the electron density at the top of the pedestal, along the outer midplane, at radial position b2stbc_iyped. ndes_sol is the total particle content from the homonuclear sequence of species 'isfeedback' over the entire simulation domain.
					It is governed, like nesepm_sol, by nesepm_overshoot and nesepm_alpha and corresponds to a SOL boundary feedback. volrec_sol is the total particle source due to volume recombination coming from Eirene. Its feedback is governed by volrec_overshoot and volrec_alpha and volrec_beta parameters (See Numerics section for the latter two). nesepm_pfr is the outer midplane separatrix electron density, but this time controlled through a gas puff outside the PFR region. (See b2mwti_jxa switch in Geometry section for setting of midplane position). This is done through particle input of neutrals species isfeedback through the private flux boundaries (See Geometry section for the PFR South boundary indices pfrregno1 and pfrregno2).
					ndes is the total particle (neutrals + ions) content of the species whose neutral species has index isfeedback. This is controlled through particle input of neutrals species isfeedback through the
					private flux boundaries (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2). private_flux_puff is the particle flow of species isfeedback through the private flux region boundary. This is controlled through particle input of neutrals species isfeedback through the private flux boundaris (See Geometry section for the private flux region boundary indices pfrregno1 and pfrregno2).
					All but the first of these feedback schemes ("nesepm") can also be run though an Eirene neutral gas puff. In that case, one should set an appropriate gas puffing stratum in the Eirene input file input.dat, as well as in the b2.neutrals.parameters file. The code will assume, unless told otherwise through the use of "eirene_nesepm_istra", that the first stratum of type 'C' found in b2.neutrals.parameters is the stratum used for the feedback. If "eirene_nesepm_istra" is set to a positive number, the code will consider the feedback stratum to be the stratum in the "eirene_nesepm_istra"-th position in b2.neutrals.parameters.
				"""),
      ( 'b2stbc_type13..21*', 'switchgroup', [
        
               ('b2stbc_type13_ref', 'integer', '1',''''''), 
        
               ('b2stbc_type16_ref', 'integer', '1',''''''), 
        
               ('b2stbc_type20_ref', 'integer', '1',''''''), 
        
               ('b2stbc_type21_ref', 'integer', '1',''''''), 
        
               ('b2stbc_type16_kinetic_energy', 'integer', '0',''''''), 
        ],
         """
					These switches are associated with the boundary condition of type 13, 16, 17, 20 or 21 for particle flux, or electron and ion energy fluxes, i.e. constant density or temperature giving a prescribed flux through a radial surface, located type13_ref or type16_ref radial steps away from the boundary of the computational domain, respectively, and applied type20_ref steps away. See code and description in b2cdcn for details.
					Type 21 also applies to the electric potential boundary condition.
					It scales the feedback strength according to the value of the variable on the ring type21_ref steps inside.
					When type16_ref.gt.1, then the position where the core flux tallies are computed moves along with the boundary condition.
					If type16_kinetic_energy.eq.1, then the parallel kinetic energy flux is included in the ion heat flux component of type 16 and 17 boundary conditions.
				"""),
         ( 'b2stbc_secmodel', 'integer', '0', """
					If secmodel.eq.1, then the secondary electron emission coefficient at the plates is computed locally according to a kinetic model, otherwise the default values of cbsch(7,ireg) and/or gammae are used.
				"""),
      
      ( 'b2stbr_sputtering...', 'switchgroup', [
        
               ('b2stbr_plate_model', 'integer', '0',''''''), 
        
               ('b2stbr_plate_option', 'integer', '3',''''''), 
        
               ('b2stbr_sput_chem_model', 'integer', '0',''''''), 
        
               ('b2stbr_sput_chem_cutoff_alpha', 'real', '1.0',''''''), 
        
               ('b2stbr_sput_chem_cutoff_beta', 'real', '3.0',''''''), 
        
               ('b2stbr_sput_mixed_alpha', 'real', '1.0',''''''), 
        
               ('b2stbr_sput_mixed_beta', 'real', '1.0',''''''), 
        
               ('b2stbr_sput_phys_model', 'integer', '1',''''''), 
        
               ('b2stbr_sputter_energy_on', 'integer', '1',''''''), 
        
               ('b2stbr_sput_res', 'real', '0.0',''''''), 
        
               ('b2stbr_therm_evap', 'real', '0.0',''''''), 
        
               ('b2stbr_sput_dst', 'integer', '-1',''''''), 
        
               ('b2stbr_sput_dst2', 'integer', '-1',''''''), 
        
               ('b2stbr_sput_dst3', 'integer', '-1',''''''), 
        
               ('b2stbr_sput_frac_flag', 'integer', '0',''''''), 
        
               ('b2stbr_sput_frc', 'real', '0.0',''''''), 
        
               ('b2stbr_sput_phys', 'real', '0.0',''''''), 
        
               ('b2stbr_sput_src', 'integer', '1',''''''), 
        
               ('b2stbr_sput_phys_col', 'integer', '3',''''''), 
        
               ('b2stbr_alpha', 'real', '0.25',''''''), 
        
               ('b2stbr_plate_temp', 'real', '300.0',''''''), 
        
               ('b2stbr_plate_thick', 'real', '0.00',''''''), 
        
               ('b2stbr_redep_alpha', 'real', '0.00',''''''), 
        ],
         """
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
					For neutrals species, we add a factor of α*na*vbar to the particle flux to the plate (used to compute chemical and RES sputtering), where vbar is the average neutral particle speed.
					Sput_phys turns on physical sputtering when sput_phys.gt.0.0 and contains a (real) multiplier for the physical sputtering rate looked up in the TRIM tables. It is superseded by the phys_sput array in b2.neutrals.parameters if the latter is used.
					sput_phys_col indicates which column to use in the TRIM table; the default (3) corresponds to 30 degrees incidence. The columns are for
					  0 15 30 45 55 65 75 80 85
					degrees. This angle is also used in the empirical formula. Plate_temp is the temperature (in Kelvin) of the COOLED end of the divertor plates. The surface temperature is computed self-consistently (using a 1-D description) according to the incident heat fluxes from the plasma. The plate is assumed to have a thickness of plate_thick, measured in meters. When plate_thick.eq.0 (default), the plate surface temperature is assumed to be the same as plate_temp. Sput_res turns on radiation enhanced sublimation (RES) when .gt.0.0 and is a multiplier to the RES rate.
					The switch sputter_energy_on turns on the energy contribution from the sputtered particles (physical and chemical). If sputter_energy_on.eq.0, the particles are sputtered cold, with no energy contribution to the ion heat equation.
					If sputter_energy_on.ne.0 (default), the chemically sputtered particles are re-introduced into the plasma with the thermal energy corresponding to the surface temperature of the material, while physically sputtered particles are re-introduced with the TRIM-calculated energy sputtering yield (if the TRIM model is used).
					Therm_evap turns on thermal evaporation when .gt.0.0 and is a multiplier to the thermal evaporation rate.
					Redep_alpha is the multiplier to the reduction of the sputtering yield due to prompt redeposition. The promptly redeposited species is counted as eroded-then-deposited species.
				"""),
      ( 'b2stbr_refl*', 'switchgroup', [
        
               ('b2stbr_refl_model', 'integer', '1',''''''), 
        
               ('b2stbr_reflection_on', 'integer', '1',''''''), 
        ],
         """
					Reflection model switches. If the recycling coefficients (particle and energy) are set to zero, then the code attempts to use, for surfaces in contact with walls, the TRIM reflection data for particle and energy reflection coefficients, when refl_model.eq.1. If refl_model.eq.0, an empirical formula is used instead. The model switch is subservient to reflection_on.ne.0. If reflection_on.eq.0, then no reflection is used.
					If reflection_on.eq.1 (default), then the incident species is reflected unchanged. Otherwise, the reflected flux is of the associated neutral species to the incident particles.
				"""),
         ( 'b2mndr_coronal_model', 'integer', '0', """
					Turns on the coronal model if coronal.ne.0. I.e., the reaction rates of all reactions are made density-independent, and the value computed at the lowest density (given in b2ar.dat) is used.
				"""),
      
         ( 'b2mndr_hz', 'real', '0.0', """
					hz has been introduced into the new form of the parallel momentum balance equation. If fac_hz = 0.0 then hz = 1 and old form of equations is used. If fac_hz = 1.0 then new form of equations is used.
				"""),
      
         ( 'b2stbr_bas_recycled_neutrals_contr', 'real', '1.0', """
					Introduced for nulling recycling energy when it is zero.
				"""),
      
         ( 'b2tfhe_alfTeEh', 'real', '0.0', """
					When set to '0.0', the old form of the electron heat flux calculation is used. It is recommended to use 1.0.
				"""),
      
         ( 'b2tfhe_fch_pTe', 'real', '1.0', """
					When set to '1.0', the new form of the electron heat flux calculation is used. It is recommended to use 1.0.
				"""),
      
         ( 'b2tfnb_xcur', 'real', '0.0', """
					Xcur is a multiplier to the parallel viscosity, perpendicular viscosity, heat viscosity, ion inertial and anomalous current contributions to the ion poloidal flows (particle and energy).
				"""),
      
         ( 'b2tfnb_ycur', 'real', '1.0', """
					Ycur is a multiplier to the parallel viscosity, perpendicular viscosity, heat viscosity, ion inertial and anomalous current contributions to the ion radial flows (particle and energy).
				"""),
      
         ( 'b2tfnb_vis_per', 'real', '0.0', """
				    vis_per is a multiplier to the perpendicular viscosity current contributions to the ion poloidal flows (particle and energy). Subservient to b2tfnb_xcur and b2tfnb_ycur.
				"""),
      
         ( 'b2tfnb_vis_q', 'real', '1.0', """
					vis_q is a multiplier to the heat viscosity current contributions to the ion poloidal flows (particle and energy). Subservient to b2tfnb_xcur and b2tfnb_ycur.
				"""),
      
         ( 'b2tqce_fke_Zhdanov', 'integer', '1', """
					When set to '1', Zhdanov's expression is used in the electron thermal conductivity. It is recommended to use 'b2tqce_fke_Zhdanov' '1'.
					This switch is only active if, simultaneously, one has b2tqce_model.eq.1 and b2tfhe_fch_pTe.eq.1.0.
				"""),
      
         ( 'b2tqna_ixref', 'integer', 'See description (integer)', """
					Poloidal index (on the basis mesh) of the reference surface for the flux-scaled transport model. The default value is the outer midplane, computed as such (see b2mwti_jxa in Geometry section or set_transport_ixref below):
					Single-null : ixref=rightcut1(1)-(rightcut1(1)-leftcut1(1))/4.
					Double-null : ixref=(rightcut1(1)+rightcut1(2))/2. Straight geometry : ixref=3*nx/4.
					The flux-scaled transport model is used in conjunction with scaling factors listed in column (7) of the transport coefficients description in input files b2ah.dat and b2mn.dat.
				"""),
      
      ( 'b2tqna_user_transport...', 'switchgroup', [
        
               ('b2tqna_user_transport', 'integer', '0',''''''), 
        
               ('set_transport_eta', 'real', '2.0',''''''), 
        
               ('set_transport_eta_alpha', 'real', '0.5',''''''), 
        
               ('set_transport_eta_floor', 'real', '0.1',''''''), 
        
               ('set_transport_eta_ceiling', 'real', '10.0',''''''), 
        
               ('set_transport_ixref', 'integer', 'See description (integer)',''''''), 
        
               ('set_transport_iyref', 'integer', 'See description (integer)',''''''), 
        
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
      ( 'b2tqna_m*', 'switchgroup', [
        
               ('b2tqna_max_df0', 'real', '1e30',''''''), 
        
               ('b2tqna_min_df0', 'real', '0.0',''''''), 
        ],
         """
					Upper and lower limits of the diffusivity coefficients df0 computed in b2tqna for each species.
				"""),
         ( 'b2tqna_new_df0', 'integer', '0', """
					When new_df0.eq.1, the neutral diffusivity is computed according to the local charge exchange, ionisation and elastic collision rates, instead of the standard form with constant cross-sections.
				"""),
      
      ( 'b2tqna_ballooning', 'switchgroup', [
        
               ('b2tqna_ballooning', 'real', '0.0',''''''), 
        
               ('b2tqna_ballooning_rescale', 'real', '1.0',''''''), 
        
               ('b2tqna_bb_ref', 'real', 'See description (real)',''''''), 
        ],
         """
					Ballooning model switches. If ballooning.ne.0, then all transport coefficients in cell (i) are rescaled by a factor of ballooning_rescale*abs(bb_ref/bb(i))**ballooning .
					The default value for bb_ref is the arithmetic average of the total magnetic field strength over the entire computational domain.
				"""),
         ( 'b2tqna_pfr_rescale', 'real', '1.0', """
					Scaling factor for all ion and electron transport coefficients inside private flux regions.
				"""),
      
         ( 'b2tqna_divsol_rescale', 'real', '1.0', """
					Scaling factor for all ion and electron transport coefficients inside divertor SOL regions.
				"""),
      
         ( 'b2sifr_phm0', 'real', '1.0', """
					Multiplier of the friction term between charged species (only ions in case b2sigp_style.eq.2).
				"""),
      
         ( 'b2sifr_phm1', 'real', '1.0', """
					If b2sigp_style.eq.2, multiplier to the friction force term between electrons and ions.
					Otherwise, multiplier of the ehxp term in the older expression for the thermal force.
				"""),
      
         ( 'b2sifr_phm2', 'real', '1.0', """
					Multiplier of the electron thermal gradient term in the thermal force term and parallel current
				"""),
      
         ( 'b2sifr_phm3', 'real', '1.0', """
					Multiplier of the ion thermal gradient term in the thermal force term.
				"""),
      
      ( 'b2sifr_limth*', 'switchgroup', [
        
               ('b2sifr_limthee', 'real', '0.3',''''''), 
        
               ('b2sifr_limthii', 'real', '0.3',''''''), 
        ],
         """
					Parameters for the computation of the thermal force term.
				"""),
      ( 'b2trcl_cth*', 'switchgroup', [
        
               ('b2trcl_cthe', 'real', '0.0',''''''), 
        
               ('b2trcl_cthi', 'real', '2.65',''''''), 
        ],
         """
					Parameters for the computation of the thermal force term.
				"""),
      ( 'b2tlnl_*', 'switchgroup', [
        
               ('b2trcl_lambda', 'real', '-5.0',''''''), 
        
               ('b2tlnl_ee', 'integer', '0',''''''), 
        
               ('b2tlnl_ei', 'integer', '0',''''''), 
        
               ('b2tlnl_ii', 'integer', '0',''''''), 
        ],
         """
					If lambda is positive, the Coulomb logarithm is set to lambda.
					If lambda is negative, then abs(lambda) is the lower bound to be used when computing the Coulomb logarithm according to the NRL formulae.
					The computation of the Coulomb logarithm takes place in b2tlnl.
					The default formula is to use the Braginskii formulation, which will give the same answer for electron-electron (ee), electron-ion (ei), and ion-ion (ii) collisions. Respectively, non-default values of '1', '2' and '3' for b2tlnl_ee, _ei, and _ii, respectively, make use of the calculation according to Wesson.
				"""),
         ( 'b2tfnb_PSch', 'real', '1.0', """
					Multiplier to the Pfirsch-Schlueter flows.
				"""),
      
         ( 'b2news_BoRiS', 'real', '0.0', """
					The poloidal convective heat flux contains a prefactor of (3/2+BoRiS). The default gives us the internal energy equation. The value BoRiS = 1.0 gives us the total energy equation.
					Only for use to benchmark with codes using the total energy equation. When used, the meaning of fhe and fhi changes from internal energy fluxes to total energy fluxes.
				"""),
      
         ( 'b2tfhe_conduction_only', 'integer', '0', """
					When conduction_only.eq.1, convective heat transfer terms are turned off. Only to be used when benchmarking against pure conduction cases.
				"""),
      
      ( 'b2tfnb_flux...', 'switchgroup', [
        
               ('b2tfnb_alpha', 'real', '0.0',''''''), 
        
               ('b2tfnb_gamma', 'real', '2.0',''''''), 
        
               ('b2tfnb_flux_limit_min_ti', 'real', '0.0',''''''), 
        ],
         """
					Parameters for the flux limit to the convective neutral flow.
					Alpha is a multiplier to the classical flux limit value.
					The larger α is, the weaker the flux limit is.
					Γ is the exponent used in the flux-limiting formula.
					The smaller γ is, the stronger the flux limit is.
					If alpha.eq.0, no flux limit is applied.
					flux_limit_min_ti specifies the minimum ti to be used (in eV).
				"""),
      ( 'b2tlc0_*', 'switchgroup', [
        
               ('b2tlc0_alpha', 'real', '0.0',''''''), 
        
               ('b2tlc0_gamma', 'real', '2.0',''''''), 
        ],
         """
					Parameters for the flux limit to dpa0 - pressure driven neutral diffusion.
					Alpha is a multiplier to the classical flux limit value.
					Γ is the exponent used in the flux-limiting formula. If alpha.eq.0, no flux limit is applied.
				"""),
      ( 'b2tlh0_*', 'switchgroup', [
        
               ('b2tlh0_alpha', 'real', '0.0',''''''), 
        
               ('b2tlh0_gamma', 'real', '2.0',''''''), 
        
               ('b2tlh0_flux_limit_min_ti', 'real', '0.0',''''''), 
        ],
         """
					Parameters for the flux limit to the heat conductivity of the neutrals. Alpha is a multiplier to the classical flux limit value.
					The larger α is, the weaker the flux limit is.
					Γ is the exponent used in the flux-limiting formula.
					The smaller γ is, the stronger the flux limit is.
					If alpha.eq.0, no flux limit is applied.
					flux_limit_min_ti specifies the minimum ti to be used (in eV).
				"""),
         ( 'b2tlmv_style', 'integer', '1', """
					if style = 0 then it is applied the origin flux limit to the viscosity else it is applied the SPb flux limit to the viscosity
				"""),
      
         ( 'b2sihs_phm0', 'real', '1.0', """
					Multiplier of the contribution to electron heat sources from divergence(ue,ve). This term is superseded by the BoRiS switch if invoked.
				"""),
      
         ( 'b2sihs_phm1', 'real', '1.0', """
					Multiplier of the contribution to ion heat sources from divergence(ua,va). This term is superseded by the BoRiS switch if invoked.
				"""),
      
         ( 'b2sihs_phm2', 'real', '1.0', """
					Multiplier of the contribution to ion heat sources from viscous heating due to poloidal velocity differences. This term is superseded by the BoRiS switch if invoked.
				"""),
      
         ( 'b2sihs_phm3', 'real', '1.0', """
					Multiplier of the contribution to electron heat sources from Joule heating (electron-ion friction).
				"""),
      
         ( 'b2sihs_phm4', 'real', '1.0', """
					Multiplier of the contribution to ion heat sources from atom-atom friction. This term is superseded by the BoRiS switch if invoked.
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
      
         ( 'b2sihs_phm8', 'real', '1.0', """
					Multiplier of the contribution to heat sources from viscous heating due to radial velocity differences. This term is only included when using b2nph9_style.eq.1 or b2npht_style.eq.1 (defaults). This term is superseded by the BoRiS switch if invoked.
				"""),
      
         ( 'b2sdia_facgt', 'real', '0.0', """
					Multiplier of the contribution to electron and ion heat sources from divergence of the gradTxB heat flux. That contribution is also multiplied by facdrift. This term is no longer needed as it has been transferred from being a source to being included in the flows.
				"""),
      
         ( 'b2sral_style', 'integer', '2', """
					When set to '0' or '2', the code calls the standard b2stbc routine, which uses the particle flux with drift terms included in the expression of the electron particle flux (fne). When set to '1', the code calls the b2stbc_spb routine instead, which uses the particle flux without drift terms in fne. It is recommended '2'.
				"""),
      
      ( 'b2sqcx_phm.', 'switchgroup', [
        
               ('b2sqcx_styl0', 'integer', '0',''''''), 
        
               ('b2sqcx_phm0', 'real', '1.0',''''''), 
        ],
         """
					phm0 : Multiplier to the charge exchange rate coefficient. Subservient to styl0: only used if styl0.eq.0 or is.lt.2. If styl0.ne.0, the charge exchange rate coefficients for species of index 2 and above are set to zero.
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
      
         ( 'b2stel_phm0', 'real', '0.0', """
					Multiplier of the recombination contribution to the electron cooling rate (if ADPAK rates are not used because those are already included). Assumes all recombination is three-body.
				"""),
      
         ( 'b2tfhe_lim_flux', 'integer', '0', """
					If '0', flux limit is not applied directly to the electron heat flux but is applied through transport coefficients if 'b2trcl_conductive_limit' is '1'. It is recommended '0'.
				"""),
      
         ( 'b2tfhi_lim_flux', 'integer', '1', """
					If '0', flux limit is not applied directly to the ion heat flux but is applied through transport coefficients if 'b2trcl_conductive_limit' is '1'. It is recommended '0'.
				"""),
      
         ( 'b2treq_phm0', 'real', '1.0', """
					Multiplier to the temperature equipartition term.
				"""),
      
         ( 'b2tqca_phm0', 'real', '1.0', """
					Multiplier for the classical parallel viscosity.
				"""),
      
         ( 'b2tqca_model', 'integer', '1', """
					If model.eq.1, use the Balescu formulation from SOLPS5.2 classical parallel ion heat diffusivity.
					If model.eq.2, use the older Braginskii SOLPS4.0 model.
					Note: old option model.eq.3 removed, replaced with model.eq.1., but numerical treatment w.r.t. factor 4/3 according to old model.eq.3.
				"""),
      
         ( 'b2tqce_model', 'integer', '1', """
					If model.eq.1, use the fitted Balescu formulation from SOLPS5.0 classical parallel electron heat diffusivity.
					If model.eq.2, use the older Braginskii SOLPS4.0 model.
					If model.eq.3, use the 21-moment Balescu results.
				"""),
      
         ( 'b2tqna_model_sig', 'integer', '0', """
					If '1', use constant density in core region to calculate anomalous conductivity sig0=dfsig*qe*ne(nmdpl,-1), nmdpl - number of midplane cell. If '0', use sig0=dfsig*qe*ne(x,y)
				"""),
      
         ( 'b2trno_csig_an_style', 'integer', '1', """
					If '1', the anomalous contributions in the parallel direction to the electrical conductivity csig and the thermo-electric coefficient calf are zeroed out.
				"""),
      
         ( 'b2trno_pol_anom_scale', 'real', '1.0', """
					If pol_anom_scale.ne.1, the poloidal anomalous transport coefficients are scaled by the number. To get the same treatment as setting the old switch (radial_only) to 1, set the new switch to 0.0.
					This multiplication is to only take place for charged species.
				"""),
      
         ( 'eirene_lhalpha', 'integer', '1', """
					If 0 then no calculation of halpha in wneutral, otherwise halpha is calculated
				"""),
      
         ( 'eirene_lvib', 'integer', '0', """
					If 0 then the sigadd4 (molecular ions) and sigadd5 (negative ions) contributions to the halpha in wneutral are not included, otherwise they are
				"""),
      
         ( 'eirene_repeat_first_call', 'integer', '1', """
					If &gt; 0 then repeats the first call to eirene in eirene_mc so many times.
					Useful if a density feedback gas puff is being used because the flux passed to Eirene on its first call is ignored (instead the value in the Eirene input file is used).
				"""),
      
         ( 'eirene_use_recyceir', 'integer', '1', """
					If &gt; 0 use recyceir (non species dependent) to specify the recycling* coefficients, else if 0 use recyc (species dependent).
				"""),
      
         ( 'eirene_ionising_core', 'integer', '0', """
					If &lt;&gt; 0 then recycles the neutral flux having crossed the core boundary within Eirene as ions. The recycling is surface-averaged, and neutrals come back as fully-stripped ions.
					'eirene_ionizing_core' is an alias for this switch.
					If the value = 1, then the flux is added by direct modification of the sources in the guard cells --- this will only work if a standard flux boundary condition is applied at that boundary.
					If the value is &lt; 0, then the absolute value specifies which boundary in b2.boundary.parameters is to be used. This will only work for the type 13 boundary condition.
				"""),
      
         ( 'eirene_background', 'integer', '1', """
					If eirene_background.eq.0, the ion velocities passed to Eirene to be used for the collisions are based on grad-B and ExB drifts (vadia + vaecrb).
					If eirene_background.eq.1, these velocities contain the full diamagnetic and ExB drifts (wadia + vaecrb).
					Note: recycling fluxes are always computed based on grad-B and ExB drifts only (and are not affected by this switch), because diamagnetic drift flows largely close within the sheath.
				"""),
      
         ( 'eirene_sheath_pot', 'integer', '1', """
					If eirene_sheath_pot.eq.1, the sheath potential drop as computed by B2.5 (i.e. including effects of parallel currents, secondary electron emission, etc.) is passed to EIRENE to compute ion acceleration in the sheath.
					If eirene_sheath_pot.eq.0, the sheath potential drop is
					recomputed by EIRENE, usually assuming zero current and secondary
					electron emission.
				"""),
      
         ( 'b2stel_fix_recomb_energy', 'integer', '0', """
					If changed to 1, then the recombination energy (rpi) is added to the electron energy for each recombination. This should only be used if the is--&gt;is-1 energy terms have been included in the electron cooling rates (as done by setting the switch 'b2ardr_fix_recomb' in b2ar.dat to a non-zero value and recalculating b2frates).
					See 'Atomic Physics' section.
					*** Use with caution! ***
				"""),
      
         ( 'b2mndr_atomic_physics_rescale', 'integer', '0', """
					If atomic_physics_rescale is not 0, then the code will rescale the rates stored in b2frates according to the multipliers given in the b2.atomic_physics_rescale.parameters inputfile before making use of them.
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

  'Atomic Physics': [ '',
  
         ( 'b2ardr_fix_cx', 'integer', '1', """
					It is used to 'correct' the CX data
					0 =&gt; do not fix
					1 =&gt; only fix H if CX data is &lt; 1e-40 [default]
					2 =&gt; fix if CX data is &lt; 1e-40
					3 =&gt; fix H
					4 =&gt; fix all
					At the moment the only species with CX data in ADAS is C. Be careful with options that use the fit formula other than for H.
					See the comments in ratstr.F for the origin of the fit formula used to 'fix' the CX data.
				"""),
      
         ( 'b2ardr_no_weisheit', 'integer', '0', """
					When set to 1, disables the correction of the hydrogen atomic rate data with the Weisheit data using ratwei.
					*** Use with caution! ***
				"""),
      
         ( 'b2ardr_no_smoothing', 'integer', '0', """
					When set to 1, disables the tail smoothing for of rate coefficients to represent the effect of a power-law tail on the distribution function. It has been added for compatibility with SOLPS4.3
				"""),
      
         ( 'b2ardr_fix_recomb', 'integer', '0', """
					When changed from 0, and if the ADAS option is in use, then uses the PRB file to add the contribution arising from is--&gt;is-1 processes.
					This term includes the bremsstrahlung.
					The default option ('0') only contains the bremsstrahlung for the is--&gt;is-1 process.
					This option should be used with the 'b2stel_fix_recomb_energy' option b2mn.dat set to '1'. See 'Physics' section.
					*** Use with caution! ***
				"""),
      
      ( 'b2ardr_rtn.', 'switchgroup', [
        
               ('b2ardr_rtnt', 'integer', '40',''''''), 
        
               ('b2ardr_rtnn', 'integer', '16',''''''), 
        ],
         """
					The number of intervals in the discretisation of the density (rtnn) and temperature (rtnt) ranges for the atomic physics tables.
				"""),
      ( 'b2mndr_dpc_mod_rates_*_hot*', 'switchgroup', [
        
               ('b2mndr_dpc_mod_rates_ne_hot_frac', 'real', '0.0',''''''), 
        
               ('b2mndr_dpc_mod_rates_te_hot', 'real', '0.0',''''''), 
        ],
         """
					Modify the atomic rates by including a hot electron population of temperature te_hot (in eV) and a population faction ne_hot_frac.
					Still experimental.
				"""),
   ],

  'Geometry': [ '',
  
         ( 'b2agfs_geometry', '', 'upgrade.geometry', """
					local_sonnet - character string.
					local_sonnet is the file name of the geometry file to be read.
					The file will be looked for in the run directory, in the ../baserun directory and in $SOLPSTOP/data/meshes. To be used in b2ag.dat.
				"""),
      
         ( 'b2mwti_jxa', '', 'See description (integer)', """
					jxa - integer.
					Cell index, on the basis mesh, of the outer midplane. Default value depends on geometry:
					Single-null : jxa=rightcut1(1)-(rightcut1(1)-leftcut1(1))/4, i.e. three quarters of the way between the two cuts.
					Double-null : jxa=(rightcut1(1)+rightcut1(2))/2, i.e. halfway between the two outer cuts. Straight geometry : jxa=3*nx/4
				"""),
      
         ( 'b2mwti_jxi', 'integer', 'See description (integer)', """
					Cell index, on the basis mesh, of the inner midplane. Default value depends on geometry:
					Single-null : jxi=leftcut1(1)+(rightcut1(1)-leftcut1(1))/4, i.e. one quarter of the way between the two cuts. Double-null : jxi=(leftcut1(1)+leftcut1(2))/2, i.e. halfway between the two inner cuts.
					Straight geometry : jxi=nx/4
				"""),
      
         ( 'b2agmx_pbs_from_basis_mesh', 'integer', '1', """
					If pbs_from_basis_mesh.eq.0, the pbs array is computed from values on the actual working mesh (old treatment).
					If pbs_from_basis_mesh.eq.1, the pbs array is computed from values on the (possibly) finer basis mesh from the geometry file and the contributions from each basis cell are added to obtain the value on the working mesh.
					In both cases, mind the value of 'b2news_area_fix', which should be also declared in b2ag.dat if the non-default behaviour is wanted.
				"""),
      
         ( 'b2agdr_redef_pbs', 'integer', '1', """
					When b2agdr_redef_pbs.eq.1, geometrical quantities are adjusted so as to ensure that the poloidal flux between two flux surfaces remains constant.
				"""),
      
         ( 'b2mndr_redef_pbs', 'integer', '0', """
					Obsolete. Should use b2agdr_redef_pbs instead.
				"""),
      
         ( 'b2agfs_periodic_bc', 'integer', '0', """
					periodic_bc - integer.
					periodic_bc specifies if this is either an island or limiter geometry.
					If periodic_bc.eq.1 then island/limiter treatment is turned on. We differentiate between the two case through nncut:
					nncut.eq.0 = limiter case
					nncut.ge.1 = island divertor case (there should be nncut islands then)
					The case periodic_bc.eq.-1 is used to remove tranverse physics in 1-D cases.
					If periodic_bc.eq.0 then we have the usual treatment. No other values are currently allowed. To be used in b2ag.dat.
				"""),
      
         ( 'b2agsi_isymm', 'integer', '1', """
					isymm - integer.
					isymm specifies the type of symmetry of the geometry: isymm.eq.0 implies a slab geometry,
					isymm.eq.1.or.isymm.eq.2 imply rotational symmetry about the crx=0 axis, and isymm.eq.3.or.isymm.eq.4 indicate rotational symmetry about the cry=0 axis.
					Other values are not allowed.
					isymm.eq.1.or.isymm.eq.3 mean a toroidal geometry case, i.e. with a toroidal (out-of-plane) magnetic field component.
					isymm.eq.2.or.isymm.eq.4 mean a cylindrical geometry case, i.e. no toroidal magnetic field component. To be used in b2ag.dat.
				"""),
      
      ( 'b2stbc_coreregn*', 'switchgroup', [
        
               ('b2stbc_coreregno', 'integer', '1',''''''), 
        
               ('b2stbc_coreregn2', 'integer', '4',''''''), 
        ],
         """
					coreregno, coreregn2 - integers. coreregno is the boundary index of the core boundary in the input files b2ah.dat and b2mn.dat. For a standard single-null case, coreregno is 1. For a straight geometry or limiter case, it is likely that coreregno need be set to 0, depending on the actual geometry details.
					coreregn2 is the boundary index of the second core boundary in case of a double-null geometry, and is not used otherwise.
				"""),
      ( 'b2stbc_pfrregno*', 'switchgroup', [
        
               ('b2stbc_pfrregno1', 'integer', '0',''''''), 
        
               ('b2stbc_pfrregno2', 'integer', '2',''''''), 
        ],
         """
					pfrregno1, pfrregno2 - integers.
					pfrregno1 is the boundary index of the first half of the private flux region boundary on which feedback is being applied (through b2stbc_ndes or b2stbc_private_flux_puff) in the input files b2ah.dat and b2mn.dat. pfrregno2 is the second half of the same private flux region. For a standard single null, the pair should be (0,2). For a standard double-null, the lower private flux region is labelled with the pair (0,5), and the upper private flux region with the pair (2,3). One can use only one private flux region by setting pfrregno1.eq.pfrregno2.
				"""),
         ( 'b2stbc_solregno', 'integer', '3', """
					solregno - integer.
					solregno is the boundary index of the SOL North boundary in the input files b2ah.dat and b2mn.dat. For a standard single-null case, solregno is 3. For a standard double-null case, solregno for the outer SOL North boundary would be 7.
				"""),
      
         ( 'b2agmt_1d_width', 'real', '1.0', """
					For 1-D cases, gives the width of the domain (in m) in the third (toroidal) dimension.
				"""),
      
         ( 'b2stbr_first_flight_no_of_start_points', 'integer', '2*(nx+2)+2*max(nncut,1)*(ny+2)', """
					When the first flight model is turned on, this number must be greater than or equal to the num
					ber of boundary cells on the mesh. Only in cases with special geometries (i.e. limiters, islands, ...) need it be increased beyond the default value above. This variable is only used within the first flight module.
				"""),
      
         ( 'b2agfs_geom_match_dist', 'real', '1.0e-6', """
					Distance used as the matching criterion when reading the geometry file.
				"""),
      
         ( 'b2agfs_Bt_adjust', 'integer', '0', """
					Bt_adjust - integer.
					If the mesh is offset (See b2agfs_xoffset, b2agfs_yoffset below) and Bt_adjust.eq.1, then the magnetic field is recomputed, keeping the pitch constant but changing the toroidal field magnitude according to Bt = Bt0/R. To be used in b2ag.dat.
				"""),
      
         ( 'b2agfs_Bt_rescale', 'real', '1.0', """
					Bt_rescale - real*8.
					The magnetic field will be multiplied by Bt_rescale. All components of the field are scaled together. To be used in b2ag.dat.
				"""),
      
         ( 'b2agfs_pit_rescale', 'real', '1.0', """
					pit_rescale - real*8.
					The magnetic field line pitch will be multiplied by pit_rescale.
					This means that the poloidal field component is multiplied by pit_rescale, while the toroidal field component is left unchanged. To reverse the plasma current direction, set pit_rescale to -1.0.
					The sign convention used is that a positive poloidal field points in the direction of increasing &lt;ix&gt;. Be mindful however that, when inverting the sign of the poloidal magnetic field, you are also inverting the direction of the parallel velocity. You will then need to use the 'b2mndr_inverse_ua' switch to correct for that. To be used in b2ag.dat.
				"""),
      
         ( 'b2agfs_Bt_reversal', 'integer', '0', """
					Bt_reversal - integer. If Bt_reversal.eq.1, then the sign of the toroidal field component only is reversed. The sign convention used is that a positive toroidal field leads to a Bx(grad(B)) direction pointing down, so B is out of the page when looking at the usual view of the poloidal plane with the center line on the left. To be used in b2ag.dat.
				"""),
      
         ( 'b2agfs_min_pitch', 'real', '1.0', """
					Minimum allowed value for the pitch angle (in degrees) at the plates.
				"""),
      
      ( 'b2agfs_.offset', 'switchgroup', [
        
               ('b2agfs_xoffset', 'real', '0.0',''''''), 
        
               ('b2agfs_yoffset', 'real', '0.0',''''''), 
        ],
         """
					xoffset, yoffset - real*8.
					xoffset and yoffset are offsets of the basis mesh in the x- and y-direction respectively. The mesh will be translated by (xoffset,yoffset) if any of the two is non-zero from its position given in the local_sonnet (See 'b2agfs_geometry' above) file.
					To be used in b2ag.dat.
				"""),
      ( 'b2agfs_.rescale', 'switchgroup', [
        
               ('b2agfs_xrescale', 'real', '1.0',''''''), 
        
               ('b2agfs_yrescale', 'real', '1.0',''''''), 
        ],
         """
					yrescale - real*8.
					Rescaling factors of the x- and y- coordinates of the basis mesh.
					To be used in b2ag.dat.
				"""),
         ( 'b2agfs_nncut', 'integer', 'See description (integer)', """
					Number of topological cuts in geometry. Needed only to force a different value from the one computed automatically by b2ag.
				"""),
      
      ( 'b2agfs_*cut', 'switchgroup', [
        
               ('b2agfs_leftcut', 'integer', 'See description (integer)',''''''), 
        
               ('b2agfs_rightcut', 'integer', 'See description (integer)',''''''), 
        
               ('b2agfs_bottomcut', 'integer', 'See description (integer)',''''''), 
        
               ('b2agfs_topcut', 'integer', 'See description (integer)',''''''), 
        ],
         """
					Parameters describing the position and extent of the first topological cut, i.e. corresponding to the first X-point. Needed only to force different values from the ones computed automatically by b2ag.
					leftcut is the poloidal index of cells directly to the RIGHT of the left branch of the cut.
					rightcut is the poloidal index of cells directly to the RIGHT of the right branch of the cut.
					bottomcut is the radial index of cells directly below the cut.
					topcut is the radial index of cells directly above the cut.
				"""),
      ( 'b2agfs_*cut2', 'switchgroup', [
        
               ('b2agfs_leftcut2', 'integer', 'See description (integer)',''''''), 
        
               ('b2agfs_rightcut2', 'integer', 'See description (integer)',''''''), 
        
               ('b2agfs_bottomcut2', 'integer', 'See description (integer)',''''''), 
        
               ('b2agfs_topcut2', 'integer', 'See description (integer)',''''''), 
        ],
         """
					Parameters describing the position and extent of the second topological cut, i.e. corresponding to the second X-point. Needed only to force different values from the ones computed automatically by b2ag.
					leftcut2 is the poloidal index of cells directly to the RIGHT of the left branch of the second cut.
					rightcut2 is the poloidal index of cells directly to the RIGHT of the right branch of the second cut.
					bottomcut is the radial index of cells directly below the second cut.
					topcut is the radial index of cells directly above the second cut.
				"""),
      ( 'b2agdr_n.iso.', 'switchgroup', [
        
               ('b2agdr_nxiso1', 'integer', '-2',''''''), 
        
               ('b2agdr_nxiso2', 'integer', '-2',''''''), 
        
               ('b2agdr_nyiso1', 'integer', '-2',''''''), 
        
               ('b2agdr_nyiso2', 'integer', '-2',''''''), 
        ],
         """
					Range of an optional isolated region to be included in the geometry.
					The isolated region will extend over the cell range spanned by (nxiso1:nxiso2,nyiso1:nyiso2).
					If only some of the four coordinates are given, the region is made to extent from the given coordinates to the end of the grid.
					Neighbourhood arrays and region indices are automatically adjusted.
				"""),
   ],

  'Atomic Physics': [ '',
  
         ( 'b2ardr_fix_cx', 'integer', '1', """
					It is used to 'correct' the CX data
					0 =&gt; do not fix
					1 =&gt; only fix H if CX data is &lt; 1e-40 [default]
					2 =&gt; fix if CX data is &lt; 1e-40
					3 =&gt; fix H
					4 =&gt; fix all
					At the moment the only species with CX data in ADAS is C. Be careful with options that use the fit formula other than for H.
					See the comments in ratstr.F for the origin of the fit formula used to 'fix' the CX data.
				"""),
      
         ( 'b2ardr_no_weisheit', 'integer', '0', """
					When set to 1, disables the correction of the hydrogen atomic rate data with the Weisheit data using ratwei.
					*** Use with caution! ***
				"""),
      
         ( 'b2ardr_no_smoothing', 'integer', '0', """
					When set to 1, disables the tail smoothing for of rate coefficients to represent the effect of a power-law tail on the distribution function. It has been added for compatibility with SOLPS4.3
				"""),
      
         ( 'b2ardr_fix_recomb', 'integer', '0', """
					When changed from 0, and if the ADAS option is in use, then uses the PRB file to add the contribution arising from is--&gt;is-1 processes.
					This term includes the bremsstrahlung.
					The default option ('0') only contains the bremsstrahlung for the is--&gt;is-1 process.
					This option should be used with the 'b2stel_fix_recomb_energy' option b2mn.dat set to '1'. See 'Physics' section.
					*** Use with caution! ***
				"""),
      
      ( 'b2ardr_rtn.', 'switchgroup', [
        
               ('b2ardr_rtnt', 'integer', '40',''''''), 
        
               ('b2ardr_rtnn', 'integer', '16',''''''), 
        ],
         """
					The number of intervals in the discretisation of the density (rtnn) and temperature (rtnt) ranges for the atomic physics tables.
				"""),
      ( 'b2mndr_dpc_mod_rates_*_hot*', 'switchgroup', [
        
               ('b2mndr_dpc_mod_rates_ne_hot_frac', 'real', '0.0',''''''), 
        
               ('b2mndr_dpc_mod_rates_te_hot', 'real', '0.0',''''''), 
        ],
         """
					Modify the atomic rates by including a hot electron population of temperature te_hot (in eV) and a population faction ne_hot_frac.
					Still experimental.
				"""),
   ],

  'b2ai params': [ 'namelist',
  
         ( 'dimens', 'None', 'None', """
					the number of charge states
				"""),
      
         ( 'label', 'None', 'None', """a label"""),
      
         ( 'specs', 'None', 'None', """
					atomic charge, nuclear charge, atomic mass and atomic charge squared for each charge stateminimum atomic charge of the stage, maximum atomic charge of the stage, nuclear charge, and atomic mass; this data should match that given in b2ah.dat
				"""),
      
         ( 'naini', 'None', 'None', """
					initial densities for each of the charge states, in m^-3
				"""),
      
         ( 'ttini', 'None', 'None', """
					initial ion and electron temperatures, in eV
				"""),
      
   ],

  'b2ah params': [ 'namelist',
  
         ( 'dimens', '', 'None', """
					the number of charge states
				"""),
      
         ( 'label', '', 'None', """
					specifies, on the next line, a label for the run
				"""),
      
         ( 'b2cmpa', '', 'None', """
					specifies a block of basic parameters.
				"""),
      
         ( 'b2cmpb', '', 'None', """
					specifies a block of boundary conditions
				"""),
      
         ( 'b2cmpt', '', 'None', """
					specifies a block of transport coefficients
				"""),
      
         ( 'specs', '', '', """
					atomic charge, nuclear charge, atomic mass and atomic charge squared; this data should match that given in b2ai.dat. Starting with code version 01.001.024, an alternative means of describing the plasma species and filling out the b2cmpa block is provided, in order to allow for bundling of charge states, when running cases with high-Z species. The relevant description is then minimum atomic charge of the stage, maximum atomic charge of the stage, nuclear charge, and atomic mass; this data should match that given in b2ai.dat The code can accept indifferently both types of input and makes the appropriate self-consistency checks. It is not permitted to bundle neutral and ionized species together.
				"""),
      
         ( 'cbregs', '', 'None', """
					specifies the number of regions where boundary conditions will be specified the 'south' boundary is broken into three pieces with one quarter of the cells in the first region, half ofthe cells in the second, and the remaining quarter in the third region (inner target private flux, core, outerprivate flux). This is geometry-dependent information the code will check against the mesh connectivity and return an error if the two do not match the 'north', 'west' and 'east' are not broken up, and correspond to the SOL boundary, inner target andouter target, respectively. For double-null cases, the north boundary should be split into two sections
				"""),
      
         ( 'region', '', 'None', """
					one block for each of the regions containing; the immediately following line being the region dentifier
				"""),
      
         ( 'cbsna', '', 'None', """
					boundary conditions for density (1 line per species)
				"""),
      
         ( 'cbsmo', '', 'None', """
					boundary conditions for parallel momentum (1 line per species)
				"""),
      
         ( 'cbshi', '', 'None', """
					ion/neutral (or "atomic") temperature/energy boundary condition (1 line per species)
				"""),
      
         ( 'cbshe', '', 'None', """
					electron temperature/heat flux boundary condition
				"""),
      
         ( 'cbsch', '', 'None', """
					boundary condition for the electric potential equation
				"""),
      
         ( 'cbrec', '', 'None', """
					recycling coefficients (1 line per species)
				"""),
      
         ( 'cbmsa', '', 'None', """
					[unused]
				"""),
      
         ( 'cbmsb', '', 'None', """
					[unused] (1 line per species)
				"""),
      
   ],

  'b2ag params': [ 'namelist',
  
         ( 'dimens', 'None', 'None', """
					specifies the size of the grid first pair is NX &amp; NY of the grid you want to produce second pair is the size of the grid that was originally created each needs to be an integer multiple of the corresponding entry of the first pair. Note that for double-null cases, the interior guard cells corresponding to the top divertor boundaries should not be multiplied.
				"""),
      
         ( 'param', 'None', 'None', """
					at least 100 additional numbers, of which only the first is relevant for us -1.0 read the mesh data using the "simplified" Carre format -2.0 read the mesh data using the Sonnet format
				"""),
      
   ],

  'b2.neutrals.parameters': [ 'namelist',
  
         ( 'NSTRAI', 'integer', '0', """
					Number of neutral sources, or 'strata'. Must not be larger than DEF_NSTRA from $(SOLPSTOP)/include(.local)/DIMENSIONS.F file.
					Need not include the time-dependent stratum. If a time-dependent stratum is used, is incremented internally as needed. The incremented value is referred to as NSTRAT below.
				"""),
      
         ( 'RCPOS', 'integer array of length (NSTRAT)', '-2', """
					Position in the B2 grid of the of strata. Similar use as BCPOS from /BOUNDARY/ namelist.
				"""),
      
         ( 'RCSTART', 'integer array of length (NSTRAT)', '-2', """
					Start coordinate on the B2 grid the strata. Similar use as BCSTART from /BOUNDARY/ namelist.
				"""),
      
         ( 'RCEND', 'integer array of length (NSTRAT)', '-2', """
					End coordinate on the B2 grid of the strata. Similar use as BCEND from /BOUNDARY/ namelist.
				"""),
      
         ( 'RC_LIST_SIZE', 'integer array of length (NSTRAT)', '0', """
					Contains the size of the recycling boundary lists. Similar use as BC_LIST_SIZE from /BOUNDARY/ namelist.
				"""),
      
         ( 'RC_LIST_X', 'integer array of length (2*(NXD+NYD),NSTRAT)', '-2', """
					Contains the X-coordinate of the cells where recycling boundaries are applied. Similar use as BC_LIST_X from /BOUNDARY/ namelist.
				"""),
      
         ( 'RC_LIST_Y', 'integer array of length (2*(NXD+NYD),NSTRAT)', '-2', """
					Contains the Y-coordinate of the cells where recycling boundaries are applied. Similar use as BC_LIST_Y from /BOUNDARY/ namelist.
				"""),
      
         ( 'TARGSP', 'integer array of size (NSTRAT,NTRACK)', 'b2stbr_sput_dst', """
					Identifies the base material(s) of this stratum wall. The number corresponds to the B2 species index produced by sputtering. Check b2cdci for details. If the bulk species is not sputtered, should contain -1.
				"""),
      
         ( 'CHEMSP', 'logical array of length NSTRAT', '.false.', """
					Indicates whether chemical sputtering is allowed from this wall stratum.
				"""),
      
         ( 'RECYC', 'real*8 array of size (0:NS-1,NSTRAT)', '', """
					Stores the particle recycling coefficients of species (is) on stratum (istra). Defaults to 1.0 for non-carbon species and 0.0 for carbon species. Particles recycle into the neutral species associated to their homonuclear sequence.
					Applies to B2 neutral fluid species.
					Also multiplies Eirene recycling fluxes if 'eirene_use_recyceir' is set to 0 (see b2cdci for details).
				"""),
      
         ( 'MRECYC', 'real*8 array of size (0:NS-1,NSTRAT)', '0.0', """
					Stores the parallel momentum recycling coefficients of species (is) on stratum (istra). The parallel momentum is carried back by the recycled neutrals. Applies only to B2 neutral fluid species.
				"""),
      
         ( 'ERECYC', 'real*8 array of size (0:NS-1,NSTRAT)', '', """
					Stores the energy recycling coefficients of species (is) on stratum (istra). Defaults to 0.3 for non-carbon species and 0.0 for carbon species. The energy is carried back by the recycled neutrals.
					Applies only to B2 neutral fluid species.
				"""),
      
         ( 'RCION', 'real*8 array of size (0:NS-1,NSTRAT)', '0.0', """
					Stores the particle-into-ion recycling coefficients of species (is) on stratum (istra). Particles recycle into the next ionised species associated to their homonuclear sequence. Applies only to B2 neutral fluid species.
				"""),
      
         ( 'RECYCEIR', 'real*8 array of size (NSTRAT)', '1.0', """
					Multiplier to the Eirene recycling fluxes from stratum (istra). Only used if 'eirene_use_recyceir' is set to 1 (default).
				"""),
      
         ( 'USERFLUXPARM', 'real*8 array of size (NSTRAT,2)', '0', """
					The element (istra,1) contains the strength of constant gas puff strata (type 'C') for Eirene in particles/second.
				"""),
      
         ( 'CRCSTRA', 'character*1 array of length (NSTRAT)', ' ', """
					Contains the type of stratum for Eirene. Possible options include:
					'N','S','W','E' - topological mesh boundaries (same use as BCCHAR in /BOUNDARY/ namelist)
					'V' - volume recombination source (related RCPOS, RCSTART, RCEND and RC_LIST variables are ignored).
					'C' - constant or feedback gas puff source (related RCPOS, RCSTART, RCEND and RC_LIST variables are ignored). Gas puffs for B2 fluid neutrals are handled via b2.boundary.parameters. Unless specified otherwise by use of 'eirene_nesepm_istra', it is the first 'C' stratum that is used for feedback puff schemes. See b2cdci for details.
					'T' - time-dependent source for Eirene (related RCPOS, RCSTART, RCEND and RC_LIST variables are ignored). Long-lived Eirene neutrals are stored in this stratum. See EIRENE_STEP_DT below.
				"""),
      
         ( 'RF_NEUT', 'real*8 array of size (4)', '1.0', """
					Relaxation parameters multiplying the Eirene particle, parallel momentum, electron energy and ion energy sources respectively before use in B2.
				"""),
      
         ( 'PHYS_SPUT', 'real*8 array of size (0:NS-1,NSTRAT)', '0.0', """
					Stores the physical sputtering multiplier for B2 species (is) sputtering on the wall of stratum (istra). Must be non-zero for physical sputtering to occur. Only applies if using B2 fluid neutral model.
				"""),
      
         ( 'CHEM_SPUT', 'real*8 array of size (0:NS-1,NSTRAT)', '0.0', """
					Stores the chemical sputtering multiplier for B2 species (is) sputtering on the wall of stratum (istra). Must be non-zero for chemical sputtering to occur. Only applies if using B2 fluid neutral model.
				"""),
      
         ( 'EIRENE_STEP_CPU', 'real*8', '', """
					Length of CPU time devoted to Eirene calls after the first one (in s). Defaults to the value given in input.dat.
				"""),
      
         ( 'EIRENE_STEP_DT', 'real*8', '1.0e-3', """
					Physical time (in s) the Eirene particles are to be followed before being passed to the time-dependent stratum.
				"""),
      
         ( 'EIRENE_MOD', 'integer', '1', """
					Frequency of Eirene calls. Eirene is called every EIRENE_MOD full B2 iterations.
				"""),
      
         ( 'VOLRECSTART', 'real*8 array of size (NSTRAT)', '1.e21', """
					Initial volume recombination rate from stratum (istra) to be used for the volume recombination scaling regulation algorithm. Rendered obsolete by 'eirene_dpc_fix'.
				"""),
      
         ( 'VOLRECINC', 'real*8', '', """
					Maximum rate of increase of the volume recombination source strength. The volume recombination regulation scaling scheme is activated if VOLRECINC is neither 0 nor 1.
					Rendered obsolete by 'eirene_dpc_fix'.
				"""),
      
         ( 'VOLRECWT', 'real*8', '0.1', """
					Weight of new volume recombination strength relative to that of previous iteration in the volume recombination regulation scaling scheme.
					Rendered obsolete by 'eirene_dpc_fix'.
				"""),
      
         ( 'SPECIES_START', 'integer array of size (NSTRAT)', '0', """
					Specifies the index of the first B2 species involved in stratum (istra).
				"""),
      
         ( 'SPECIES_END', 'integer array of size (NSTRAT)', 'ns-1', """
					Specifies the index of the last B2 species involved in stratum (istra).
				"""),
      
         ( 'NEUTRALS_FILENAME', 'character*256', 'b2.neutrals.parameters', """
					Name of the next file to use for reading a new /NEUTRALS/ namelist.
				"""),
      
         ( 'NEUTRALS_TIME_MOD', 'real*8', '0.0', """
					When the B2 run simulation time, in seconds, modulo(NEUTRALS_TIME_MOD), exceeds NEUTRALS_TIME_SWITCH, reads the new namelist from NEUTRALS_FILENAME. Also switches to the new namelist if the ELM count (here time/NEUTRALS_TIME_MOD) changes. Only active if NEUTRALS_TIME_MOD is greater than 0.
				"""),
      
         ( 'NEUTRALS_TIME_SWITCH', 'real*8', '0.0', """
					Time (in seconds) within an ELM cycle after which a new NEUTRALS namelist is read.
				"""),
      
         ( 'L_NEUTRAD', 'integer', '0', """
					If l_neutrad &gt;= 0, then the radiated power due to the neutrals atoms is taken directly from the Eirene calculation, instead of being recomputed by B2.
				"""),
      
         ( 'L_NEUTFLUX', 'integer', '', """
					If l_neutflux &gt;=0, then correct treatment of the incident fluxes in B2 and b2plot; if &lt;0, then old (approximate) treatment
				"""),
      
         ( 'LSTRASCL', 'integer array of size (NSTRAT,0:natm)', '', """
					Indicates with which Eirene atomic species to scale the Eirene stratum (istra) (0 means no scaling, default). Atomic species 0 stands for electrons.
				"""),
      
         ( 'B2EATCR', 'integer array of size (0:NS-1)', 'ordering of the B2 isonuclear sequences', """
					Contains the index of the Eirene atomic species corresponding to the B2 species (is).
				"""),
      
         ( 'B2ESPCR', 'integer array of size (0:NS-1)', 'ordering of the B2 isonuclear sequences', """
					Contains the isonuclear sequence index of the B2 species (is).
				"""),
      
         ( 'EB2ATCR', 'integer array of size (NATM)', 'first B2 species of each isonuclear sequence', """
					Contains the index of the B2 neutral fluid species corresponding to the Eirene atomic species (iatm).
				"""),
      
         ( 'EB2SPCR', 'integer array of size (NSPECIES)', 'first B2 species of each isonuclear sequence', """
					Contains the index of the first B2 fluid for each species.
				"""),
      
         ( 'LATMSCL', 'integer array of size (NATM)', 'assuming one-to-one match between Eirene and B2.5 atomic species', """
					Contains the index of the B2.5 isonuclear sequence with which the Eirene atomic species (IATM) should be scaled.
				"""),
      
         ( 'LMOLSCL', 'integer array of size (NMOL)', '0', """
					Contains the index of the Eirene atomic species with which the Eirene molecular species (IMOL) should be scaled.
				"""),
      
         ( 'MLCMP', 'integer array of size (NATM,NMOL)', '0', """
					Contains the number of atoms from Eirene atomic species IATM within each molecule of Eirene molecular species IMOL.
				"""),
      
         ( 'LIONSCL', 'integer array of size (NION)', '0', """
					Contains the index of the Eirene atomic species with which the Eirene test ion species (IION) should be scaled.
				"""),
      
         ( 'LCNS', 'integer array of size (NSTS)', '0', """
					Contains the indices of Eirene non-standard surfaces (block 3A in input.dat) corresponding to core boundaries.
				"""),
      
         ( 'LTNS', 'integer array of size (NSTS)', '0', """
					Contains the indices of Eirene non-standard surfaces (block 3A in input.dat) corresponding to target boundaries.
				"""),
      
         ( 'LSNS', 'integer array of size (NSTRAT*NSRFS)', '0', """
					Contains the indices of Eirene surfaces related to the recycling sources.
				"""),
      
         ( 'KSNS', 'integer array of size (NSTRAT)', '0', """
					Contains the number of Eirene surfaces for each Eirene recycling stratum.
				"""),
      
         ( 'GPFC', 'real*8 array of size (NATM,NSTRAT)', '0.0', """
					Specifies the fraction of Eirene atomic species (iatm) in one particle puffed from stratum (istra).
				"""),
      
         ( 'DBG_EIR_MC', 'integer', '0', """
					Debug output control for eirene_mc routine. See code for usage.
				"""),
      
         ( 'DEBUG_FLAGS', 'integer array of size (100)', '0', """
					Non-zero elements yield additional print-out data for debugging B2-Eirene coupling. See code for specific uses. Many slots still available for user-specific needs.
				"""),
      
         ( 'NEUT_SCL_LIM', 'real*8', '2.0', """
					Maximum number by which Eirene neutral sources may be scaled in either direction within the ank-mods scheme. See explaining text in $SOLPSTOP/doc/Source_Scaling_in_B2.pdf for details.
				"""),
      
         ( 'TRACK_INDEX', 'integer array of size (0:NS-1)', '1 for species spud_dst, 0 for other', """
					Specifies the mixed material species index related to B2 species (is).
				"""),
      
         ( 'TRACK_CHEM_SPUT', 'logical array of size (NTRACK)', '', """
					Indicates whether mixed material species (itrack) participates in chemical sputtering. Defaults to .true. for first tracked species if sput_dst is carbon, and to .false. for all other cases.
				"""),
      
         ( 'CHEMICAL_EROSION_REDEP_FAC', 'real*8', '1.0', """
					Multiplier to the chemical sputtering coefficient of carbon for computing the rate used for redeposited carbon.
				"""),
      
         ( 'CHEMICAL_EROSION_BE_FAC', 'logical', '.false.', """
					Indicates whether the presence of beryllium is to impact on the chemical sputtering yield of carbon.
				"""),
      
         ( 'CHEMICAL_EROSION_BE_FAC_A', 'real*8', '0.2', """
					The chemical sputtering yield of carbon is multiplied by
					(1.0-C/2*(tanh((frac-A)/B)-tanh((-A)/B)))
					where frac is the fractional content of Be in the surface layer material.
				"""),
      
         ( 'CHEMICAL_EROSION_BE_FAC_B', 'real*8', '0.05', """
					See above.
				"""),
      
         ( 'CHEMICAL_EROSION_BE_FAC_C', 'real*8', '0.9', """
					See above.
				"""),
      
         ( 'N_SPCSRF', 'integer', '0', """
					Number of special surfaces groups for diagnostics.
				"""),
      
         ( 'L_SPCSRF', 'integer array of length (NLIM+NSTS)', '0', """
					List of surface segments (non-default standard surfaces [NDSS] or additional surfaces in Eirene notation) included in the groups. Negative numbers correspond to NDSS.
				"""),
      
         ( 'SPS_ID', 'character*8 array of length (N_SPCSRF)', '', """
					Labels of groups of special surfaces.
				"""),
      
         ( 'I_SPCSRF', 'integer array of length (N_SPCSRF)', '0', """
					Index of the first Eirene surface belonging to a special surface group in the L_SPCSRF list.
				"""),
      
         ( 'J_SPCSRF', 'integer array of length (N_SPCSRF)', '0', """
					Index of the last Eirene surface belonging to a special surface group in the L_SPCSRF list.
				"""),
      
         ( 'SPS_ABSR', 'real*8 array of length (N_SPCSRF)', '-1.0', """
					Particle absorption on the surface. If positive, will supercede the setting from the Eirene input file: RECYCT = 1-SPS_ABSR. Ignored if negative.
				"""),
      
         ( 'SPS_TRNO', 'real*8 array of length (N_SPCSRF)', '-1.0', """
					Surface transparency in positive direction. If positive, will supercede the setting from the Eirene input file: TRANSP(1,) = SPS_TRNO. Ignored if negative.
				"""),
      
         ( 'SPS_TRNI', 'real*8 array of length (N_SPCSRF)', '-1.0', """
					Surface transparency in negative direction. If positive, will supercede the setting from the Eirene input file: TRANSP(2,) = SPS_TRNI. If negative, the setting from SPS_TRNO is used.
				"""),
      
         ( 'SPS_MTRI', 'real*8 array of length (N_SPCSRF)', '0', """
					Surface material in Eirene notation (e.g., 1206 for C). If positive, will supercede the setting from the Eirene input file: ZNML = SPS_MTRI. Ignored if negative.
				"""),
      
         ( 'SPS_MTRL', 'character*8 array of length (N_SPCSRF)', '', """
					Surface material in human notation (e.g., 'C').
				"""),
      
         ( 'SPS_TMPR', 'real*8 array of length (N_SPCSRF)', '1.e15', """
					Surface temperature (in eV). If set larger to 1.e10, will be ignored. Otherwise, will supercede the setting from the Eirene input file: EWALL = SPS_TMPR.
				"""),
      
         ( 'SPS_SPPH', 'real*8 array of length (N_SPCSRF)', '-1.0', """
					Fudge factor for physical sputtering. If positive, will supercede the setting from the Eirene input file: RECYCS = SPS_SPPH. Ignored if negative.
				"""),
      
         ( 'SPS_SPCH', 'real*8 array of length (N_SPCSRF)', '-1.0', """
					Fudge factor for chemical sputtering. If positive, will supercede the setting from the Eirene input file: RECYCC = SPS_SPCH. Ignored if negative.
				"""),
      
         ( 'SPS_SGRP', 'integer array of length (N_SPCSRF)', '-1', """
					Sputtered particle species flag for chemical sputtering. If positive, will supercede the setting from the Eirene input file: ISRC = SPS_SGRP. Ignored if negative.
				"""),
      
         ( 'WRITE_NML_NEUT', 'logical', '.true.', """
					If .true. (default), writes the content of the namelist to stdout after it has been read.
				"""),
      
         ( 'TIME_DEP_PUFF', 'logical array of length (NSTRAT)', '.false. for all strata', """
					Indicates whether a stratum is a time-dependent gas puff. Should only be .true. for strata defined as gas puffs.
				"""),
      
         ( 'NGPDATA', 'integer data of size (NSTRAT)', '0', """
					Number of points over which the time profile of the strength of gas puff (istra) is given. Defaults to 0. Current maximum value is 100.
				"""),
      
         ( 'GPDATA', 'real*8 data of size (NGPDATA,2,NSTRAT)', '0.0', """
					For (i,ik,istra) in (1:NGPDATA(istra),1:2,1:NSTRAT),
					GPDATA(i,1,istra) contains the time point (i) for stratum (istra) (in s).
					GPDATA(i,2,istra) contains the gas puff strength of stratum (istra) at time point (i) (in particles/s).
					The gas puff strength before the first time point is given by USERFLUXPARM(istra,1).
					The gas puff strength after the last time point is given by the GPDATA value of the last time point.
					Otherwise, the gas puff strength is linearly interpolated from the given data.
				"""),
      
         ( 'CHEMICAL_SPUTTER_YIELD', 'real*8 array of size (0:NLIM+NSTS)', '0.0', """
					Passed to Eirene. Chemical sputter yield of wall surface (ilim).
				"""),
      
         ( 'FCHAR_CHEMICAL', 'real*8', '0', """
					Nuclear charge of atomic species causing the sputtering. Default means no chemical sputtering.
				"""),
      
         ( 'IGASS_CHEMICAL', 'integer', '0', """
					Passed to Eirene. Eirene atomic species index of the sputtered particle. If igass_chemical &gt; natmi, the data from chemical_sputter_yield is not used and the yield from the Eirene surface blocks is used instead.
				"""),
      
         ( 'ITSPUT_CHEMICAL', 'integer', '0', """
					Passed to Eirene. Eirene type index of the sputtered particle. Atoms = 1, Ions = 4. Defaults to 0, meaning 1 eV atom chemical sputtering.
				"""),
      
         ( 'ISSPUT_CHEMICAL', 'integer', '0', """
					Passed to Eirene. Mass*100 + nuclear charge of the sputtered particle. Defaults to 0, internally changed to 1206 = carbon.
				"""),
      
   ],

  'b2.wall_save.parameters': [ 'namelist',
  
         ( 'NDEPTH_NML', 'integer', '1', """
					Dimension NDEPTH used for the arrays within this namelist. Represents the number of depth layer discretising the wall elements for the wall model. If using the 0-D model or the time-independent 1-D model, will contain 1 (default). Should not exceed the value of the parameter NDEPTH declared in b2mod_wall.F.
				"""),
      
         ( 'IMAPX', 'integer array of size (NWALL)', '', """
					Indicates the (ix) position in the grid of wall element (iwall). Default ordering of the wall elements proceeds clockwise in physical space from the lower left corner.
				"""),
      
         ( 'IMAPY', 'integer array of size (NWALL)', '', """
					Indicates the (iy) position in the grid of wall element (iwall). Default ordering of the wall elements proceeds clockwise in physical space from the lower left corner.
				"""),
      
         ( 'XYMAP', 'integer array of size (-1:NX,-1:NY)', '', """
					XYMAP(ix,iy) contains the wall index (iwall) of the wall element located a grid locaion (ix,iy). If there is no wall element at this position, contains 0.
					Default ordering of the wall elements proceeds clockwise in physical space from the lower left corner.
				"""),
      
         ( 'SURFACE_MATERIAL_NAME', 'character*6 of size (NWALL)', 'C', """
					Contains the filename from which to extract the surface material properties for wall element (iwall). The files are to be found in $(SOLPSTOP)/data(.local)/Surface_properties/.
				"""),
      
         ( 'COATING_MATERIAL_NAME', 'character*6 of size (NWALL)', ' ', """
					Contains the filename from which to extract the bulk material properties of the eventual coating for wall element (iwall).
				"""),
      
         ( 'BULK_MATERIAL_NAME', 'character*6 of size (NWALL)', 'C', """
					Contains the filename from which to extract the bulk material properties for wall element (iwall). The files are to be found in $(SOLPSTOP)/data(.local)/Bulk_properties/.
				"""),
      
         ( 'LAYER_ALLOYS', 'character*6 of size (NALLOYS)', '', """
					Contains the filename from which to extract the material properties for alloy (nalloy) which may be present in mixed materials deposited layers. Not yet operational. The files are to be found in $(SOLPSTOP)/data(.local)/Bulk_properties/ and $(SOLPSTOP)/data(.local)/Surface_properties/.
				"""),
      
         ( 'TARGET_TEMP', 'real*8 array of size (NWALL,NDEPTH)', '', """
					Contains the temperature (in Kelvin) of wall element (iwall) at depth layer (idepth).
					If plate_option.eq.1, will be set to backplate_temp(iwall).
					If plate_option.eq.2 and empty, will be set to equilibrium 1-D profile deduced from plasma incoming fluxes.
					If plate-option.eq.3, must be set.
				"""),
      
         ( 'INERTIAL_COOLING', 'logical array of size (NWALL)', '.false.', """
					Indicates whether wall element (iwall) is inertially cooled instead of actively cooled.
				"""),
      
         ( 'BACKPLATE_TEMP', 'real*8 array of size (NWALL)', 'b2stbr_plate_temp', """
					Contains the temperature (in Kelvin) maintained by cooling at the back end of wall element (iwall).
				"""),
      
         ( 'PLATE_THICKNESS', 'real*8 array of size (NWALL)', 'b2stbr_plate_thick', """
					Contains the thickness (in meters) of wall element (iwall).
				"""),
      
         ( 'COATING_THICKNESS', 'real*8 array of size (NWALL)', '0', """
					Contains the thickness (in meters) of the eventual coating on wall element (iwall).
				"""),
      
         ( 'PLATE_TIME_FACTOR', 'real*8 array of size (NWALL)', '1.0', """
					Multiplier to the time for the equations for temperature and composition evolution of wall element (iwall).
				"""),
      
         ( 'DEPOSITION', 'real*8 array of size (NWALL, NTRACK)', '0.0', """
					Contains the amount of deposited material (in atoms) from species (itrack) onto wall element (iwall).
				"""),
      
         ( 'EROSION', 'real*8 array of size(NWALL, NTRACK)', '0.0', """
					Contains the amount of eroded material (in atoms) of species (itrack) from wall element(iwall).
				"""),
      
         ( 'CHEMICAL_SPUTTERING', 'real*8 array of size (NWALL,0:NS-1)', '0.0', """
					Contains the chemical sputter yield of 'sput_dst' or 'sput_dst_bulk' species on wall element (iwall) caused by B2 species (is).
				"""),
      
         ( 'PHYSICAL_SPUTTERING', 'real*8 array of size (NWALL,0:NS-1)', '0.0', """
					Contains the physical sputter yield of 'sput_dst' or 'sput_dst_bulk' species on wall element (iwall) caused by B2 species (is).
				"""),
      
         ( 'PHYSICAL_SPUTTERING_ENERGY', 'real*8 array of size (NWALL,0:NS-1)', '0.0', """
					Contains the fraction of returned energy carried by sputtered particles of species 'sput_dst' or 'sput_dst_bulk' species from wall element (iwall) caused by B2 species (is).
				"""),
      
         ( 'RES_SPUTTERING', 'real*8 array of size (NWALL,0:NS-1)', '0.0', """
					Contains the RES sputter yield of 'sput_dst' or 'sput_dst_bulk' species on wall element (iwall) caused by B2 species (is).
				"""),
      
         ( 'THERMAL_EVAPORATION', 'real*8 array of size(NWALL,0:NS-1)', '0.0', """
					Contains the rate of thermal evaporation of species (is) (in particles/second) from wall element (iwall).
				"""),
      
         ( 'BACKSCATTERING', 'real*8 array of size (NWALL,0:NS-1)', '0.0', """
					Contains the backscattering fraction for incoming B2 species (is) onto wall element (iwall).
				"""),
      
         ( 'BACKSCATTERING_ENERGY', 'real*8 array of size (NWALL,0:NS-1)', '0.0', """
					Contains the backscattered energy fraction for incoming B2 species (is) onto wall element (iwall).
				"""),
      
         ( 'PLATE_TIME', 'real*8 array of size (NWALL)', '0.0', """
					Indicates how much simulation time has elapsed for wall element (iwall) (in seconds).
				"""),
      
         ( 'PLATE_AREA', 'real*8 array of size (NWALL)', '', """
					Indicates the wall area (in square meters) for wall element (iwall). Defaults to the area computed from the B2 grid information.
				"""),
      
         ( 'MONOLAYER_DEPOSITION', 'real*8 array of size (NWALL,NTRACK)', '0.0', """
					Contains the amount of deposited material (in monolayers) from species (itrack) onto wall element (iwall).
				"""),
      
         ( 'MONOLAYER_EROSION', 'real*8 array of size (NWALL,NTRACK)', '0.0', """
					Contains the amount of eroded material (in monolayers) of species (itrack) from wall element (iwall).
				"""),
      
         ( 'LAYER_NCONSTITUENTS', 'integer array of size (NWALL)', '1', """
					Indicates the number of elemental constituents within the surface layer of wall element (NWALL).
				"""),
      
         ( 'LAYER_NZCONSTITUENTS', 'integer array of size (NWALL,6+NTRACK)', '', """
					Contains the atomic numbers Z of the various elements present within the surface layer of wall element (iwall). Defaults to 6 for the first value, 0 otherwise.
				"""),
      
         ( 'LAYER_NRELCONSTITUENTS', 'real*8 array of size (NWALL,6+NTRACK)', '', """
					Contains the relative atomic abundances of the various elements present within the surface layer of wall element (iwall). Defaults to 1.0 for the first value, 0.0 otherwise.
				"""),
      
   ],

  'b2md.dat': [ 'namelist',
  
         ( 'EXP', 'character*128', 'NOT_SET', """
					Name of the experiment being modelled.
				"""),
      
         ( 'SHOT', 'integer', '', """
					Shot number identifying the run. Defaults to the last number found in shotnumber.history, or 0 if the file is not found.
				"""),
      
         ( 'TIME', 'real*8', '0.0', """
					Time point of the experimental shot being simulated.
				"""),
      
         ( 'COMMENT', 'character*128', 'NOT_SET', """
					Label for the run.
				"""),
      
         ( 'TIMEDEP', 'logical', '', """
					If .true. (default), saves data from b2time.nc.
				"""),
      
         ( 'SNAPSHOT', 'logical', '', """
					If .true. (default), saves data from b2fplasma.
				"""),
      
         ( 'TALLIES', 'logical', '', """
					If .true. (default), saves data from b2tallies.nc.
				"""),
      
         ( 'MOVIES', 'logical', '', """
					If .true. (default), saves data from b2movies.nc.
				"""),
      
         ( 'OVERWRITE_SHOTNUMBER', 'integer', '', """
					Indicate the shot number to overwrite (to be used only when updating an already saved run with 'resave_mds' script).
					Defaults to the last number found in shotnumber.history, or 0 if the file is not found.
				"""),
      
   ],

  'b2.boundary.parameters': [ 'namelist',
  
         ( 'NBC', 'integer', '0', """Number of boundary segments."""),
      
         ( 'BCCHAR', 'character*1 array of length (NBC)', ' ', """
					Specifies the nature of the boundary segment
					N = 'North' boundary
					S = 'South' boundary
					W = 'West' boundary
					E = 'East' boundary
					X = 'X' boundary used for specifying a fixed value on a row of cells
					Y = 'Y' boundary used for specifying a fixed value on a column of cells
				"""),
      
         ( 'CONPAR', 'real*8 array of size (0:NS-1,NBC,3)', '0.0', """
					Contains parameters helping to define the boundary conditions for the continuity equation of species (is). See description of BCCON below for details.
				"""),
      
         ( 'MOMPAR', 'real*8 array of size (0:NS-1,NBC,2)', '0.0', """
					Contains parameters helping to define the boundary conditions for the parallel momentum equation of species (is). See description of BCMOM below for details.
				"""),
      
         ( 'ENEPAR', 'real*8 array of size (NBC,2)', '0.0', """
					Contains parameters helping to define the boundary conditions for the electron energy equation. See description of BCENE below for details.
				"""),
      
         ( 'ENIPAR', 'real*8 array of size (NBC,2)', '0.0', """
					Contains parameters helping to define the boundary conditions for the ion energy equation. See description of BCENI below for details.
				"""),
      
         ( 'POTPAR', 'real*8 array of size (NBC,2)', '0.0', """
					Contains parameters helping to define the boundary conditions for the potential equation. See description of BCPOT below for details.
				"""),
      
         ( 'BCPOS', 'integer array, length (NBC)', '-2', """
					For North, South or X boundary conditions, it specifies the row index; for West, East and Y boundary conditions, it specifies the column index.
				"""),
      
         ( 'BCSTART', 'integer array, length (NBC)', '-2', """
					For North, South or X boundary conditions, it specifies the start column index; for West, East and Y boundary conditions, it specifies the start row index.
				"""),
      
         ( 'BCEND', 'integer array, length (NBC)', '-2', """
					For North, South X boundary conditions, it specifies the end column index; for West, East and Y boundary conditions, it specifies the end row index.
				"""),
      
         ( 'BC_LIST_SIZE', 'integer array of length (NBC)', '0', """
					Contains the size of the list of cells where a boundary condition is applied.
				"""),
      
         ( 'BC_LIST_X', 'integer array of length (2*(NXD+NYD),NBC)', '-2', """
					Contains the X-coordinate of the cells where boundaries conditions are applied.
				"""),
      
         ( 'BC_LIST_Y', 'integer array of length (2*(NXD+NYD),NBC)', '-2', """
					Contains the Y-coordinate of the cells where boundaries conditions are applied.
				"""),
      
         ( 'BCCON', 'integer array, length (0:NS-1,NBC)', '', """
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
						10 : leakage option for density, recommended for cases with drifts, CONPAR(,,1) specifies the leakage factor, α in Γ<sub>loss</sub> = α C<sub>s</sub> n<sub>a</sub>
						11 : particle flux feedback boundary condition, CONPAR(,,1) not used, derived from CBSNA(0,IS,IREG). The species used must be declared using the 'b2stbc_isfeedback' switch.
						12 : particle density feedback boundary condition, as above, CONPAR(,,1) not used, derived from CBSNA(0,IS,IREG). The species used must be declared using the 'b2stbc_isfeedback' switch.
						13 : particle density to achieve specified total flux,
							CONPAR(,,1) is the specified flux crossing the flux surface 'b2stbc_type13_ref' steps away from the boundary,
							CONPAR(,,2) is the strength of the feedback,
							CONPAR(,,3), when running with Eirene and the 'ionising core' switch is used, is set internally to match the re-entering flux of ionised neutrals that crossed the core boundary (one must then have 'ionising_core'.eq.-IB where IB is the boundary index).
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
				"""),
      
         ( 'BCMOM', 'integer array, length NS * NBC', '', """
					Specifying the type of parallel momentum or velocity boundary condition for each segment and species (fastest varying index is species); makes use of MOMPAR to specify additional information, as indicated
						 0 : default, no boundary condition is applied
						 1 : prescribe the value of the parallel velocity, MOMPAR(,,1) specifies the parallel velocity in m.s<sup>-1</sup>
						 2 : prescribe the gradient of the parallel velocity, MOMPAR(,,1) specifies the parallel velocity gradient in s<sup>-1</sup>
						 3 : sheath conditions, Mach number as input,
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
						17 : leakage option for parallel momentum, MOMPAR(,,1) specifies the leakage factor, α in Γ<sub>loss</sub> = α C<sub>s,a</sub> m<sub>a</sub> n<sub>a</sub> u<sub>a</sub>
				"""),
      
         ( 'BCENE', 'integer array, length NBC', '', """
					Specifying the type of electron energy or temperature boundary condition for each segment; makes use of ENEPAR to specify additional information, as indicated
						 0 : default, no boundary condition is applied
						 1 : prescribe the value of the electron temperature, ENEPAR(,1) specifies the temperature in eV
						 2 : prescribe the gradient of the electron temperature, ENEPAR(,1) specifies the temperature gradient in eV.m<sup>-1</sup>
						 3 : sheath conditions, electron energy transmission, ENEPAR(,1) specifies an additional contribution to the energy transmission coefficient in addition to that of the potential difference [the sound speed used depends on settings of MOMPAR(,ISMAIN,2)]
						 4 : prescribe the value of the electron temperature, weakly a mixed boundary condition, ENEPAR(,1) specifies the temperature in eV and ENEPAR(,2) specifies the 'strength' of the boundary condition
						 5 : prescribe the electron energy flux per unit area, ENEPAR(,1) specifies the energy flux density in W.m<sup>-2</sup>
						 6 : prescribe the total electron energy flux for a constant electron temperature, ENEPAR(,1) specifies the energy flux in W (no longer supported, use types [16] or [17] instead)
						 7 : prescribe the electron temperature as a function of other plasma parameters [not yet available]
						 8 : prescribe the total electron heat flux with constant flux density, ENEPAR(,1) specifies the energy flux in W
						 9 : prescribe the decay length for the electron temperature, ENEPAR(,1) specifies the decay length in m (can also use type [19] instead)
						 10 : feedback option for core, ENEPAR(,1) not used, derived from cbshe(0,coreregno)
						 11 : not used
						 12 : sheath conditions, electron energy transmission coefficient, ENEPAR(,1) specifies an energy transmission factor, delta<sub>e</sub> in Q<sub>e</sub> = delta<sub>e</sub> Γ<sub>e</sub> T<sub>e</sub>
						 13 : prescribe the electron energy flux per unit area proportional to temperature, ENEPAR(,1) specifies the energy flux density per temperature in W.m<sup>-2</sup>.J<sup>-1</sup> (the temperature here in J)
						 14 : leakage option for electron energy, ENEPAR(,1) specifies the leakage factor, α in Γ<sub>loss</sub> = α C<sub>s</sub>, collective n<sub>e</sub> T<sub>e</sub>
						 15 : sheath boundary condition, from b2stbc_spb, recommended when using drifts (see Section C.6.4 of manual for details). Linked to using BCCON=14 for all ion species.
						 16 : Feedback boundary condition with constant temperature, ENEPAR(,1) specifies the power flux in W across the flux surface with index 'b2stbc_type16_ref' (default=-1), ENEPAR(,2) should be something like 0.1 and specifies the strength of the feedback. Also see type [17] below. Available if bcene_16_style=0 (default). If bcene_16_style=1, integrated electron heat flux with constant electron temperature, summed over all core boundaries with BCENE=16.
						 17 : Feedback boundary condition with constant shared temperature for both electrons and ions, with ENEPAR(,1) + ENIPAR(,1) giving the total power flux in W across the flux surface with index 'b2stbc_type16_ref' (default=-1), ENEPAR(,2) should be something like 0.1 and specifies the strength of the feedback. Replaces [16] for high densities and large values of 'b2stbc_type16_ref'.
						 18 : Fractional drop condition. Not yet working.
						 19 : same as [9] but to be used when simultaneously setting BCCON=1 on the same boundary.
						 20 : Feedback boundary condition with constant temperature, as per type [16] but with 'type20_' switches and a different feedback scheme.
						 21 : constant temperature feedback scaled by temperature on the ring bc_type21_ref away
						  	ENEPAR(,1) specifies the desired electron temperature in eV.
						    ENEPAR(,2) is the strength of the feedback
						 22 : radial leakage condition for the electron temperature. ENEPAR(,1) specifies the leakage velocity in units of the electron thermal velocity. A temperature gradient such that the diffusive flux is set to match this leakage is imposed.
				"""),
      
         ( 'BCENI', 'integer array, length NBC', '', """
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
						12 : sheath conditions, ion energy transmission coefficient, ENIPAR(,1) specifies an energy transmission factor, delta<sub>i</sub> in Q<sub>i</sub> = delta<sub>i</sub> T<sub>i</sub> sum<sub>a</sub> Γ<sub>a</sub>
						13 : prescribe the ion energy flux per unit area proportional to temperature, ENIPAR(,1) specifies the energy flux density per temperature in W.m<sup>-2</sup>.J<sup>-1</sup> (the temperature here in J)
						14 : leakage option for ion energy, ENIPAR(,1) specifies the leakage factor, α in Γ<sub>loss</sub> = α C<sub>s</sub>T<sub>i</sub>
						15 : sheath boundary condition, from b2stbc_spb, recommended when using drifts (see Section C.6.5 of manual for details). Linked to using BCCON=14 for all ion species.
						16 : Feedback boundary condition with constant temperature, ENIPAR(,1) specifies the power flux in W across the flux surface with index 'b2stbc_type16_ref' (default=-1), ENIPAR(,2) should be something like 0.1 and specifies the strength of the feedback. Also see type [17] below. Available if bceni_16_style=0 (default). If bceni_16_style=1, integrated ion heat flux with constant ion temperature, summed over all core boundaries with BCENI=16.
							ENIPAR(,1) specifies the power flux in W
						17 : Feedback boundary condition with constant shared temperature for both electrons and ions, see BCENE=17 above for description.
						18 : Fractional drop condition. Not yet working.
						19 : same as [9] but to be used when simultaneously setting BCCON=1 on the same boundary.
						20 : Feedback boundary condition with constant temperature, as per type [16] but with 'type20_' switches and a different feedback scheme.
						21 : from b2stbc_spb
						22 : Radial leakage condition for the ion temperature. ENIPAR(,1) specifies the leakage velocity in units of the collective ion thermal velocity. A temperature gradient such that the diffusive flux is set to match this leakage is imposed.
						23 : Prescribe the poloidally averaged value of the ion temperature and introduce a poloidal variation as close as possible to neoclassical solution. It is recommended to use this boundary condition together with corresponding condition on ion density (BCCON=21,22,23). The average is taken over all core boundaries with BCENI=23. ENIPAR(,1) specifies the temperature in eV
						24 : Feedback boundary condition with prescribed total ion flux, constant poloidally averaged ion temperature and a poloidal variation as close as possible to neoclassical solution. It is recommended to use this boundary condition together with corresponding condition on ion density (BCCON=21,22,23). The flux is summed over all core boundaries with BCENI=24. ENIPAR(,1) specifies the energy flux in W
						25 : Constant temperature feedback scaled by temperature on the ring bc_type21_ref away. ENIPAR(,1) specifies the desired ion temperature in eV. ENIPAR(,2) is the strength of the feedback
						26 : Prescribe the poloidally averaged value of the ion temperature and introduce a poloidal variation in a simplified manner. This boundary condition is suitable for any plasma composition (i.e. when BCENI=23 fails). It is recommended to use this boundary condition together with corresponding condition on ion density (BCCON = 25,26,27). The average is taken over all core boundaries with BCENI=26. ENIPAR(,1) specifies the temperature in eV
						27 : Feedback boundary condition with prescribed total ion heat flux, constant poloidally averaged ion temperature and a poloidal variation in a simplified manner. This boundary condition is suitable for any plasma composition (i.e. when BCENI=24 fails). It is recommended to use this boundary condition together with corresponding condition on ion density (BCCON = 25,26,27). The flux is summed over all core boundaries with BCENI=27. ENIPAR(,1) specifies the energy flux in W
				"""),
      
         ( 'BCPOT', 'integer array, length NBC', '', """
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
				"""),
      
         ( 'GAMMAI', 'real*8', '1.0', """
					Adiabatic coefficient multiplying the ion temperature when computing the plasma sound speed.
				"""),
      
         ( 'GAMMAE', 'real*8', '0.5', """
					Secondary electron emission coefficient.
				"""),
      
         ( 'LBNDUSR', 'logical', '.false.', """
					If .true. will also call Bas' boundary condition routine after the end of the physics boundary condition routine (governed by the data from b2ah.dat and b2mn.dat).
				"""),
      
         ( 'LFEEDBACK', 'logical', '.false.', """
					Indicates whether a feedback scheme is used. Obsolete. Superceded by 'b2stbc_feedback'.
				"""),
      
         ( 'NNISO', 'integer', '0', """
					Number of dead (or isolated) regions.
				"""),
      
         ( 'NIISO', 'real*8 array of size (0:NS-1)', '', """
					Density of species (is) in (m-3) to impose in isolated regions.
				"""),
      
         ( 'TEISO', 'real*8', '1.0', """
					Electron temperature (in eV) to impose in isolated regions.
				"""),
      
         ( 'TIISO', 'real*8', '1.0', """
					Ion temperature (in eV) to impose in isolated regions.
				"""),
      
         ( 'PHIISO', 'real*8', '0.0', """
					Electric potential (in V) to impose in isolated regions.
				"""),
      
         ( 'NXISO1', 'integer array of size NNISO', '-2', """
					Column number of bottom left corner of the dead region (iiso).
				"""),
      
         ( 'NXISO2', 'integer array of size NNISO', '-2', """
					Column number of top right corner of the dead region (iiso).
				"""),
      
         ( 'NYISO1', 'integer array of size NNISO', '-2', """
					Row number of bottom left corner of the dead region (iiso).
				"""),
      
         ( 'NYISO2', 'integer array of size NNISO', '-2', """
					Row number of top right corner of the dead region (iiso).
				"""),
      
         ( 'BOUNDARY_FILENAME', 'character*256', 'b2.boundary.parameters', """
					Name of the next file to use for reading a new /BOUNDARY/ namelist.
				"""),
      
         ( 'BOUNDARY_TIME_MOD', 'real*8', '0.0', """
					When the B2 run simulation time, in seconds, modulo(BOUNDARY_TIME_MOD), exceeds BOUNDARY_TIME_SWITCH, reads the new namelist from BOUNDARY_FILENAME. Also switches to the new namelist as the ELM count (here time/BOUNDARY_TIME_MOD) changes.
					Only active if BOUNDARY_TIME_MOD is greater than 0.
				"""),
      
         ( 'BOUNDARY_TIME_SWITCH', 'real*8', '0.0', """
					Time (in seconds) within an ELM cycle after which a new /BOUNDARY/ namelist is read.
				"""),
      
         ( 'LCBS', 'integer array of size (NBC)', '', """
					Indices of the core boundary segments in B2 for passing to EIRENE. Defaults to the list of 'S' boundaries in regions 1 and 5.
				"""),
      
         ( 'WRITE_NML_BND', 'logical', '.true.', """
					If .true. (default), writes the content of the namelist to stdout after it has been read.
				"""),
      
   ],

  'b2.feedback_save.parameters': [ 'namelist',
  
         ( 'SAVED_CBSHE_CORE', 'real*8', '0.0', """
					Last value used for the core electron energy radial flux feedback.
				"""),
      
         ( 'SAVED_CBSHI_CORE', 'real*8', '0.0', """
					Last value used for the core ion energy radial flux feedback.
				"""),
      
         ( 'SAVED_CBSNA_CORE', 'real*8', '0.0', """
					Last value used for the core particle radial flux feedback. Corresponds to 'isfeedback' B2 species.
				"""),
      
         ( 'SAVED_CBSCH_CORE', 'real*8', '0.0', """
					Last value used for the core radial electric current feedback.
				"""),
      
         ( 'SAVED_CBSNA_PFR1', 'real*8', '0.0', """
					Last value used for the radial inner PFR boundary flux feedback. Corresponds to 'isfeedback' B2 species.
				"""),
      
         ( 'SAVED_CBSNA_PFR2', 'real*8', '0.0', """
					Last value used for the radial outer PFR boundary flux feedback. Corresponds to 'isfeedback' B2 species.
				"""),
      
         ( 'SAVED_CBSNA_SOL', 'real*8', '0.0', """
					Last value used for the radial particle flux feedback in the SOL. Corresponds to 'isfeedback' B2 species.
				"""),
      
   ],

  'b2.feedback_control.parameters': [ 'namelist',
  
         ( 'VACUUM_COMMUNICATION', 'Integer', '0', """
					If &gt; 0, allows for a
					communication of particle fluxes across vacuum regions. This option only applies to neutrals. The density boundary condition is based on the difference between the average pressure and the local pressure.
				"""),
      
         ( 'VACUUM_COMMUNICATION_NREG', 'Integer array of size (NVAC)', '0', """
					Number of communicating vacuum regions.
				"""),
      
         ( 'VACUUM_COMMUNICATION_METHOD', 'Integer array of size (NVAC)', '0', """
					Option for resorbing the pressure difference.
						1: Try to set a flux. Corr = (beta*ave_pressure - pressure)/temp * alpha
						2: Try to set a density based on pressure equality.
					Corr = α * beta * pressure / Ti
				"""),
      
         ( 'VACUUM_COMMUNICATION_IY', 'Integer array of size (NVACREG,NVAC)', '-2', """
					Radial index of the ring on which the neutral pressure is computed for region IREG.
				"""),
      
         ( 'VACUUM_COMMUNICATION_IX1', 'Integer array of size (NVACREG,NVAC)', '-2', """
					Poloidal lower bound of the range over which the neutral pressure is computed for region IREG.
				"""),
      
         ( 'VACUUM_COMMUNICATION_IX2', 'Integer array of size (NVACREG,NVAC)', '-2', """
					Poloidal upper bound of the range over which the neutral pressure is computed for region IREG.
				"""),
      
         ( 'VACUUM_COMMUNICATION_ALPHA', 'Real*8 array of size (0:NSPECIES-1,NVAC)', '0.0', """
					Parameter for setting the pressure correction. See above.
				"""),
      
         ( 'VACUUM_COMMINICATION_BETA', 'Real*8 array of size (0:NSPECIES-1,NVAC)', '1.0', """
					Parameter for setting the pressure correction. See above.
				"""),
      
         ( 'NA_FEEDBACK_TARGET', 'Real*8 array of size (0:NSPECIES-1)', '0.0', """
					Sets the target density of species (ISPECIES) for the feedback scheme.
				"""),
      
         ( 'NA_FEEDBACK_TIME', 'Real*8 array of size (0:NSPECIES-1)', '0.0', """
					Sets the time of reference (in s) for the feedback of species (ISPECIES).
				"""),
      
         ( 'NA_FEEDBACK_CHOICE', 'Integer array of size (0:NSPECIES-1)', '0', """
					Choice of quantity on which the feedback is computed:
						0: no action
						1: local species density (averaged over the rectangle of cells[IX1:IX2,IY1:IY2]). Summed over all charge states of that species.
						2: local electron density (averaged over the rectangle of cells[IX1:IX2,IY1:IY2]).
						3: outer midplane separatrix electron density.
						4: total particle content for that species.
						5: total ion content for that species (not including neutrals).
						6: neutral particle flux through the core boundary.
						7: relative average concentration of this species at the separatrix.
				"""),
      
         ( 'NA_FEEDBACK_OPTION', 'Integer array of size (0:NSPECIES-1)', '0', """
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
				"""),
      
         ( 'NA_FEEDBACK_ACTUATOR', 'Integer array of size (0:NSPECIES-1)', '0', """
					Choice for the actuator used for the feedback.
					0: no action
					1: gas puff via boundary condition
					2: rescale na
					3: core boundary flux condition
				"""),
      
         ( 'NA_FEEDBACK_ALPHA', 'Real*8 array of size (0:NSPECIES-1)', '0.001', """
					Factor by which the rescaling is slowed. Rescaling factor is :
					Option 1: (1 + α*target/current) / (1 + alpha)
					Option 3: 2**(tanh(log(x)/beta)*log(alpha)/log(2))
					Options 4 and 5: Corresponds to parameter F
				"""),
      
         ( 'NA_FEEDBACK_BETA', 'Real*8 array of size (0:NSPECIES-1)', '1.0', """
					Factor by which the rescaling is slowed. See above. Options 4 and 5: Corresponds to parameter V (ffb_rtvn)
				"""),
      
         ( 'NA_FEEDBACK_CONST', 'Real*8 array of size (0:NSPECIES-1)', '0.0', """
					Options 4 and 5: Corresponds to parameter C. If negative, C is
						computed as the initial total particle content of the sequence.
				"""),
      
         ( 'NA_FEEDBACK_IX1', 'Integer array of size (0:NSPECIES-1)', '-2', """
					Lower poloidal bound for the region of which the density is being averaged.
				"""),
      
         ( 'NA_FEEDBACK_IX2', 'Integer array of size (0:NSPECIES-1)', '-2', """
					Upper poloidal bound for the region of which the density is being averaged.
				"""),
      
         ( 'NA_FEEDBACK_IY1', 'Integer array of size (0:NSPECIES-1)', '-2', """
					Lower radial bound for the region of which the density is being averaged.
				"""),
      
         ( 'NA_FEEDBACK_IY2', 'Integer array of size (0:NSPECIES-1)', '-2', """
					Upper poloidal bound for the region of which the density is being averaged.
				"""),
      
         ( 'NA_FEEDBACK_IB', 'Integer array of size (0:NSPECIES-1)', '-1', """
					Index of boundary condition through which the feedback is being applied.
				"""),
      
         ( 'NA_FEEDBACK_PUFF_MIN', 'Real*8 array of size (0:NSPECIES-1)', '0.0', """
					Minimum gas puff being applied.
				"""),
      
         ( 'NA_FEEDBACK_PUFF_MAX', 'Real*8 array of size (0:NSPECIES-1)', '0.0', """
					Maximum gas puff being applied.
				"""),
      
         ( 'NA_FEEDBACK_OVERSHOOT', 'Real*8 array of size (0:NSPECIES-1)', '0.0', """
					If the density is larger than target*overshoot, the gas puff is turned off.
				"""),
      
   ],

  'b2.transport.inputfile': [ 'namelist',
  
         ( 'NDATA', 'integer array of size (NKIND_DATA,NCOEF,0:NS)', '0', """
					Number of points over which the source profile of (kind_data,kind_coef,is) is defined. Should not exceed NY+2.
					If KIND_DATA=1, the data is expressed as a profiles in physical distance from the separatrix (in metres).
					If KIND_DATA=2, the data is expressed as a profile in flux distance from the separatrix (not yet available).
				"""),
      
         ( 'TDATA', 'real*8 data of size (3,NY+2,NKIND_COEFF,0:NS)', '0.0', """
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
				"""),
      
         ( 'ADDSPEC', 'integer array of size (NS,NKIND_COEFF,0:NS)', '-5', """
					If ADDSPEC(is,ikind,spec).ge.0, then the transport coefficient profile of type (ikind) from species (spec) is also used for species with index ADDSPEC(is,ikind,spec).
				"""),
      
         ( 'TRANSPORT_FILENAME', 'character*256', 'b2.transport.inputfile', """
					Name of the next file to use for reading a new /TRANSPORT/ namelist.
				"""),
      
         ( 'TRANSPORT_TIME_MOD', 'real*8', '0.0', """
					When the B2 run simulation time, in seconds, modulo(TRANSPORT_TIME_MOD),exceeds TRANSPORT_TIME_SWITCH, reads the new namelist from TRANSPORT_FILENAME. Also switches to the new namelist if the ELM count (here time/TRANSPORT_TIME_MOD) changes. Only active if TRANSPORT_TIME_MOD is greater than 0.
				"""),
      
         ( 'TRANSPORT_TIME_SWITCH', 'real*8', '0.0', """
					Time (in seconds) within an ELM cycle after which a new /TRANSPORT/ namelist is read.
				"""),
      
         ( 'REGION_FLAGS', 'logical array of size (NREG,NKIND_COEFF)', '.true.', """
					If region_flags(ireg,ikind) is .true. (default), then the transport parameters profiles for region (ireg) and kind (ikind) are used.
				"""),
      
         ( 'NO_PFLUX', 'logical', '.false.', """
					If .true., transport coefficients profiles are not implemented in the private flux regions.
				"""),
      
         ( 'NO_DIV', 'logical', '.false.', """
					If .true., transport coefficients profiles are not implemented in the divertor regions.
				"""),
      
         ( 'POLOIDAL_SCALING', 'logical array of size (10)', '.false.', """
					If .true., then the transport coefficients profiles from the current b2.transport.inputfile are increased by a factor of 1.0+Gaussian where Gaussian is a Gaussian profile in the poloidal direction of amplitude SCALING_STRENGTH extending from SCALING_IX_BEGIN to SCALING_IX_END inclusively. The profile has a decay length of SCALING_WIDTH (in units of the number of poloidal cells).
				"""),
      
         ( 'SCALING_STRENGTH', 'real*8 array of size 10', '0', """
					See above.
				"""),
      
         ( 'SCALING_WIDTH', 'real*8 array of size 10', '1/3 interval', """
					See above. Defaults to about 1/3 of the interval over which the scaling is to be done.
				"""),
      
         ( 'SCALING_IX_BEGIN', 'integer array of size 10', '-2', """
					See above.
				"""),
      
         ( 'SCALING_IX_END', 'integer array of size 10', '-2', """
					See above.
				"""),
      
         ( 'ELM_TIME_BEGIN', 'real*8', '0.0', """
					Time (in seconds) modulo ELM_TIME_PERIOD at which the ELM phase begins and the ELM data must be used.
				"""),
      
         ( 'ELM_TIME_END', 'real*8', '0.0', """
					Time (in seconds) modulo ELM_TIME_PERIOD at which the ELM phase ends and the ELM data is no longer used.
				"""),
      
         ( 'ELM_TIME_PERIOD', 'real*8', '0.0', """
					Indicates the real frequency of simulated ELMs. See above for usage.
					If zero, no ELM profiles are used.
				"""),
      
         ( 'ELM_IX_BEGIN', 'integer', '-2', """
					Poloidal position at which the ELM profile starts to be applied.
				"""),
      
         ( 'ELM_IX_END', 'integer', '-2', """
					Poloidal position at which the ELM profile ends being applied.
				"""),
      
   ],

  'b2.neutrals_save.parameters': [ 'namelist',
  
         ( 'SAVED_VOLREC', 'real*8 array of size (NSTRAT)', '0.0', """
					Contains the last value of the strength of volume recombination sources from stratum (istra).
				"""),
      
   ],

  'b2.numerics.parameters': [ 'namelist',
  
         ( 'DTCO', 'real*8 array of size (0:NS-1,0:NREG)', '1.0', """
					Multiplier to the time used in solving the continuity equation of species (is) in region (ireg).
				"""),
      
         ( 'DTMO', 'real*8 array of size (0:NS-1,0:NREG)', '1.0', """
					Multiplier to the time used in solving the parallel momentum equation of species (is) in region (ireg).
				"""),
      
         ( 'DTEE', 'real*8 array of size (0:NREG)', '1.0', """
					Multiplier to the time used in solving the electron heat equation in region (ireg).
				"""),
      
         ( 'DTEI', 'real*8 array of size (0:NREG)', '1.0', """
					Multiplier to the time used in solving the ion heat equation in region (ireg).
				"""),
      
         ( 'SOLVECO', 'logical array of size (0:NS-1,0:NREG)', '.true.', """
					Indicates whether the continuity equation for species (is) is to be solved in region (ireg). Subservient to 'no_solve' switch.
				"""),
      
         ( 'SOLVEMO', 'logical array of size (0:NS-1,0:NREG)', '.true.', """
					Indicates whether the parallel momentum equation for species (is) is to be solved in region (ireg). Subservient to 'no_solve' switch.
				"""),
      
         ( 'SOLVEPO', 'logical array of size (0:NREG)', '.true.', """
					Indicates whether the potential energy equation is to be solved in region (ireg). Subservient to 'no_solve' switch.
				"""),
      
         ( 'SOLVEEE', 'logical array of size (0:NREG)', '.true.', """
					Indicates whether the electron energy equation is to be solved in region (ireg). Subservient to 'no_solve' switch.
				"""),
      
         ( 'SOLVEEI', 'logical array of size (0:NREG)', '.true.', """
					Indicates whether the ion energy equation is to be solved in region (ireg). Subservient to 'no_solve' switch.
				"""),
      
         ( 'TIME_FACTOR_REQUIRED', 'real*8', '0.1', """
					Minimum time scale of evolution allowed for all equations. Only active is 'b2srsm_enable' is set to 1.
				"""),
      
         ( 'CORE_DT_SUPPRESSION', 'real*8', '1.0', """
					De-multiplier to the timestep in the core. Only active if less than 1. Should be larger than 0. Applies fully to the innermost core ring of cells (IY .eq. -1). See CORE_DT_FACTOR for further use.
				"""),
      
         ( 'CORE_DT_FACTOR', 'real*8', '1.0', """
					Multiplier to the timestep in the core. Only active is less than 1. Should be larger than 0. Multiplies each successive core ring of cells (increasing IY) by CORE_DT_FACTOR, until the local time step multiplier is equal to 1.
				"""),
      
         ( 'NUMERICS_FILENAME', 'character*256', 'b2.numerics.namelist', """
					Name of the next file to use for reading a new /NUMERICS/ namelist.
				"""),
      
         ( 'NUMERICS_TIME_MOD', 'real*8', '0.0', """
					When the B2 run simulation time, in seconds, modulo(NUMERICS_TIME_MOD), exceeds NUMERICS_TIME_SWITCH, reads the new namelist from NUMERICS_FILENAME. Also switches to the new namelist as the ELM count (here time/NUMERICS_TIME_MOD) changes. Only active if NUMERICS_TIME_MOD is greater than 0.
				"""),
      
         ( 'NUMERICS_TIME_SWITCH', 'real*8', '0.0', """
					Time (in seconds) within an ELM cycle after which a new /NUMERICS/ namelist is read.
				"""),
      
         ( 'WRITE_NML_NUM', 'logical', '.true.', """
					If .true. (default), writes the content of the namelist to stdout after it has been read.
				"""),
      
   ],

  'b2.transport_models_save.parameters': [ 'namelist',
  
         ( 'ETA_HCE_MULT', 'real*8 array of size (-1:NY)', '1.0', """
					Used by the user specified set_transport_eta transport model. See code for details.
				"""),
      
   ],

  'b2.neutrals.parameters': [ 'namelist',
  
         ( 'NSTRAI', 'integer', '0', """
					Number of neutral sources, or 'strata'. Must not be larger than DEF_NSTRA from $(SOLPSTOP)/include(.local)/DIMENSIONS.F file.
					Need not include the time-dependent stratum. If a time-dependent stratum is used, is incremented internally as needed. The incremented value is referred to as NSTRAT below.
				"""),
      
         ( 'RCPOS', 'integer array of length (NSTRAT)', '-2', """
					Position in the B2 grid of the of strata. Similar use as BCPOS from /BOUNDARY/ namelist.
				"""),
      
         ( 'RCSTART', 'integer array of length (NSTRAT)', '-2', """
					Start coordinate on the B2 grid the strata. Similar use as BCSTART from /BOUNDARY/ namelist.
				"""),
      
         ( 'RCEND', 'integer array of length (NSTRAT)', '-2', """
					End coordinate on the B2 grid of the strata. Similar use as BCEND from /BOUNDARY/ namelist.
				"""),
      
         ( 'RC_LIST_SIZE', 'integer array of length (NSTRAT)', '0', """
					Contains the size of the recycling boundary lists. Similar use as BC_LIST_SIZE from /BOUNDARY/ namelist.
				"""),
      
         ( 'RC_LIST_X', 'integer array of length (2*(NXD+NYD),NSTRAT)', '-2', """
					Contains the X-coordinate of the cells where recycling boundaries are applied. Similar use as BC_LIST_X from /BOUNDARY/ namelist.
				"""),
      
         ( 'RC_LIST_Y', 'integer array of length (2*(NXD+NYD),NSTRAT)', '-2', """
					Contains the Y-coordinate of the cells where recycling boundaries are applied. Similar use as BC_LIST_Y from /BOUNDARY/ namelist.
				"""),
      
         ( 'TARGSP', 'integer array of size (NSTRAT,NTRACK)', 'b2stbr_sput_dst', """
					Identifies the base material(s) of this stratum wall. The number corresponds to the B2 species index produced by sputtering. Check b2cdci for details. If the bulk species is not sputtered, should contain -1.
				"""),
      
         ( 'CHEMSP', 'logical array of length NSTRAT', '.false.', """
					Indicates whether chemical sputtering is allowed from this wall stratum.
				"""),
      
         ( 'RECYC', 'real*8 array of size (0:NS-1,NSTRAT)', '', """
					Stores the particle recycling coefficients of species (is) on stratum (istra). Defaults to 1.0 for non-carbon species and 0.0 for carbon species. Particles recycle into the neutral species associated to their homonuclear sequence.
					Applies to B2 neutral fluid species.
					Also multiplies Eirene recycling fluxes if 'eirene_use_recyceir' is set to 0 (see b2cdci for details).
				"""),
      
         ( 'MRECYC', 'real*8 array of size (0:NS-1,NSTRAT)', '0.0', """
					Stores the parallel momentum recycling coefficients of species (is) on stratum (istra). The parallel momentum is carried back by the recycled neutrals. Applies only to B2 neutral fluid species.
				"""),
      
         ( 'ERECYC', 'real*8 array of size (0:NS-1,NSTRAT)', '', """
					Stores the energy recycling coefficients of species (is) on stratum (istra). Defaults to 0.3 for non-carbon species and 0.0 for carbon species. The energy is carried back by the recycled neutrals.
					Applies only to B2 neutral fluid species.
				"""),
      
         ( 'RCION', 'real*8 array of size (0:NS-1,NSTRAT)', '0.0', """
					Stores the particle-into-ion recycling coefficients of species (is) on stratum (istra). Particles recycle into the next ionised species associated to their homonuclear sequence. Applies only to B2 neutral fluid species.
				"""),
      
         ( 'RECYCEIR', 'real*8 array of size (NSTRAT)', '1.0', """
					Multiplier to the Eirene recycling fluxes from stratum (istra). Only used if 'eirene_use_recyceir' is set to 1 (default).
				"""),
      
         ( 'USERFLUXPARM', 'real*8 array of size (NSTRAT,2)', '0', """
					The element (istra,1) contains the strength of constant gas puff strata (type 'C') for Eirene in particles/second.
				"""),
      
         ( 'CRCSTRA', 'character*1 array of length (NSTRAT)', ' ', """
					Contains the type of stratum for Eirene. Possible options include:
					'N','S','W','E' - topological mesh boundaries (same use as BCCHAR in /BOUNDARY/ namelist)
					'V' - volume recombination source (related RCPOS, RCSTART, RCEND and RC_LIST variables are ignored).
					'C' - constant or feedback gas puff source (related RCPOS, RCSTART, RCEND and RC_LIST variables are ignored). Gas puffs for B2 fluid neutrals are handled via b2.boundary.parameters. Unless specified otherwise by use of 'eirene_nesepm_istra', it is the first 'C' stratum that is used for feedback puff schemes. See b2cdci for details.
					'T' - time-dependent source for Eirene (related RCPOS, RCSTART, RCEND and RC_LIST variables are ignored). Long-lived Eirene neutrals are stored in this stratum. See EIRENE_STEP_DT below.
				"""),
      
         ( 'RF_NEUT', 'real*8 array of size (4)', '1.0', """
					Relaxation parameters multiplying the Eirene particle, parallel momentum, electron energy and ion energy sources respectively before use in B2.
				"""),
      
         ( 'PHYS_SPUT', 'real*8 array of size (0:NS-1,NSTRAT)', '0.0', """
					Stores the physical sputtering multiplier for B2 species (is) sputtering on the wall of stratum (istra). Must be non-zero for physical sputtering to occur. Only applies if using B2 fluid neutral model.
				"""),
      
         ( 'CHEM_SPUT', 'real*8 array of size (0:NS-1,NSTRAT)', '0.0', """
					Stores the chemical sputtering multiplier for B2 species (is) sputtering on the wall of stratum (istra). Must be non-zero for chemical sputtering to occur. Only applies if using B2 fluid neutral model.
				"""),
      
         ( 'EIRENE_STEP_CPU', 'real*8', '', """
					Length of CPU time devoted to Eirene calls after the first one (in s). Defaults to the value given in input.dat.
				"""),
      
         ( 'EIRENE_STEP_DT', 'real*8', '1.0e-3', """
					Physical time (in s) the Eirene particles are to be followed before being passed to the time-dependent stratum.
				"""),
      
         ( 'EIRENE_MOD', 'integer', '1', """
					Frequency of Eirene calls. Eirene is called every EIRENE_MOD full B2 iterations.
				"""),
      
         ( 'VOLRECSTART', 'real*8 array of size (NSTRAT)', '1.e21', """
					Initial volume recombination rate from stratum (istra) to be used for the volume recombination scaling regulation algorithm. Rendered obsolete by 'eirene_dpc_fix'.
				"""),
      
         ( 'VOLRECINC', 'real*8', '', """
					Maximum rate of increase of the volume recombination source strength. The volume recombination regulation scaling scheme is activated if VOLRECINC is neither 0 nor 1.
					Rendered obsolete by 'eirene_dpc_fix'.
				"""),
      
         ( 'VOLRECWT', 'real*8', '0.1', """
					Weight of new volume recombination strength relative to that of previous iteration in the volume recombination regulation scaling scheme.
					Rendered obsolete by 'eirene_dpc_fix'.
				"""),
      
         ( 'SPECIES_START', 'integer array of size (NSTRAT)', '0', """
					Specifies the index of the first B2 species involved in stratum (istra).
				"""),
      
         ( 'SPECIES_END', 'integer array of size (NSTRAT)', 'ns-1', """
					Specifies the index of the last B2 species involved in stratum (istra).
				"""),
      
         ( 'NEUTRALS_FILENAME', 'character*256', 'b2.neutrals.parameters', """
					Name of the next file to use for reading a new /NEUTRALS/ namelist.
				"""),
      
         ( 'NEUTRALS_TIME_MOD', 'real*8', '0.0', """
					When the B2 run simulation time, in seconds, modulo(NEUTRALS_TIME_MOD), exceeds NEUTRALS_TIME_SWITCH, reads the new namelist from NEUTRALS_FILENAME. Also switches to the new namelist if the ELM count (here time/NEUTRALS_TIME_MOD) changes. Only active if NEUTRALS_TIME_MOD is greater than 0.
				"""),
      
         ( 'NEUTRALS_TIME_SWITCH', 'real*8', '0.0', """
					Time (in seconds) within an ELM cycle after which a new NEUTRALS namelist is read.
				"""),
      
         ( 'L_NEUTRAD', 'integer', '0', """
					If l_neutrad &gt;= 0, then the radiated power due to the neutrals atoms is taken directly from the Eirene calculation, instead of being recomputed by B2.
				"""),
      
         ( 'L_NEUTFLUX', 'integer', '', """
					If l_neutflux &gt;=0, then correct treatment of the incident fluxes in B2 and b2plot; if &lt;0, then old (approximate) treatment
				"""),
      
         ( 'LSTRASCL', 'integer array of size (NSTRAT,0:natm)', '', """
					Indicates with which Eirene atomic species to scale the Eirene stratum (istra) (0 means no scaling, default). Atomic species 0 stands for electrons.
				"""),
      
         ( 'B2EATCR', 'integer array of size (0:NS-1)', 'ordering of the B2 isonuclear sequences', """
					Contains the index of the Eirene atomic species corresponding to the B2 species (is).
				"""),
      
         ( 'B2ESPCR', 'integer array of size (0:NS-1)', 'ordering of the B2 isonuclear sequences', """
					Contains the isonuclear sequence index of the B2 species (is).
				"""),
      
         ( 'EB2ATCR', 'integer array of size (NATM)', 'first B2 species of each isonuclear sequence', """
					Contains the index of the B2 neutral fluid species corresponding to the Eirene atomic species (iatm).
				"""),
      
         ( 'EB2SPCR', 'integer array of size (NSPECIES)', 'first B2 species of each isonuclear sequence', """
					Contains the index of the first B2 fluid for each species.
				"""),
      
         ( 'LATMSCL', 'integer array of size (NATM)', 'assuming one-to-one match between Eirene and B2.5 atomic species', """
					Contains the index of the B2.5 isonuclear sequence with which the Eirene atomic species (IATM) should be scaled.
				"""),
      
         ( 'LMOLSCL', 'integer array of size (NMOL)', '0', """
					Contains the index of the Eirene atomic species with which the Eirene molecular species (IMOL) should be scaled.
				"""),
      
         ( 'MLCMP', 'integer array of size (NATM,NMOL)', '0', """
					Contains the number of atoms from Eirene atomic species IATM within each molecule of Eirene molecular species IMOL.
				"""),
      
         ( 'LIONSCL', 'integer array of size (NION)', '0', """
					Contains the index of the Eirene atomic species with which the Eirene test ion species (IION) should be scaled.
				"""),
      
         ( 'LCNS', 'integer array of size (NSTS)', '0', """
					Contains the indices of Eirene non-standard surfaces (block 3A in input.dat) corresponding to core boundaries.
				"""),
      
         ( 'LTNS', 'integer array of size (NSTS)', '0', """
					Contains the indices of Eirene non-standard surfaces (block 3A in input.dat) corresponding to target boundaries.
				"""),
      
         ( 'LSNS', 'integer array of size (NSTRAT*NSRFS)', '0', """
					Contains the indices of Eirene surfaces related to the recycling sources.
				"""),
      
         ( 'KSNS', 'integer array of size (NSTRAT)', '0', """
					Contains the number of Eirene surfaces for each Eirene recycling stratum.
				"""),
      
         ( 'GPFC', 'real*8 array of size (NATM,NSTRAT)', '0.0', """
					Specifies the fraction of Eirene atomic species (iatm) in one particle puffed from stratum (istra).
				"""),
      
         ( 'DBG_EIR_MC', 'integer', '0', """
					Debug output control for eirene_mc routine. See code for usage.
				"""),
      
         ( 'DEBUG_FLAGS', 'integer array of size (100)', '0', """
					Non-zero elements yield additional print-out data for debugging B2-Eirene coupling. See code for specific uses. Many slots still available for user-specific needs.
				"""),
      
         ( 'NEUT_SCL_LIM', 'real*8', '2.0', """
					Maximum number by which Eirene neutral sources may be scaled in either direction within the ank-mods scheme. See explaining text in $SOLPSTOP/doc/Source_Scaling_in_B2.pdf for details.
				"""),
      
         ( 'TRACK_INDEX', 'integer array of size (0:NS-1)', '1 for species spud_dst, 0 for other', """
					Specifies the mixed material species index related to B2 species (is).
				"""),
      
         ( 'TRACK_CHEM_SPUT', 'logical array of size (NTRACK)', '', """
					Indicates whether mixed material species (itrack) participates in chemical sputtering. Defaults to .true. for first tracked species if sput_dst is carbon, and to .false. for all other cases.
				"""),
      
         ( 'CHEMICAL_EROSION_REDEP_FAC', 'real*8', '1.0', """
					Multiplier to the chemical sputtering coefficient of carbon for computing the rate used for redeposited carbon.
				"""),
      
         ( 'CHEMICAL_EROSION_BE_FAC', 'logical', '.false.', """
					Indicates whether the presence of beryllium is to impact on the chemical sputtering yield of carbon.
				"""),
      
         ( 'CHEMICAL_EROSION_BE_FAC_A', 'real*8', '0.2', """
					The chemical sputtering yield of carbon is multiplied by
					(1.0-C/2*(tanh((frac-A)/B)-tanh((-A)/B)))
					where frac is the fractional content of Be in the surface layer material.
				"""),
      
         ( 'CHEMICAL_EROSION_BE_FAC_B', 'real*8', '0.05', """
					See above.
				"""),
      
         ( 'CHEMICAL_EROSION_BE_FAC_C', 'real*8', '0.9', """
					See above.
				"""),
      
         ( 'N_SPCSRF', 'integer', '0', """
					Number of special surfaces groups for diagnostics.
				"""),
      
         ( 'L_SPCSRF', 'integer array of length (NLIM+NSTS)', '0', """
					List of surface segments (non-default standard surfaces [NDSS] or additional surfaces in Eirene notation) included in the groups. Negative numbers correspond to NDSS.
				"""),
      
         ( 'SPS_ID', 'character*8 array of length (N_SPCSRF)', '', """
					Labels of groups of special surfaces.
				"""),
      
         ( 'I_SPCSRF', 'integer array of length (N_SPCSRF)', '0', """
					Index of the first Eirene surface belonging to a special surface group in the L_SPCSRF list.
				"""),
      
         ( 'J_SPCSRF', 'integer array of length (N_SPCSRF)', '0', """
					Index of the last Eirene surface belonging to a special surface group in the L_SPCSRF list.
				"""),
      
         ( 'SPS_ABSR', 'real*8 array of length (N_SPCSRF)', '-1.0', """
					Particle absorption on the surface. If positive, will supercede the setting from the Eirene input file: RECYCT = 1-SPS_ABSR. Ignored if negative.
				"""),
      
         ( 'SPS_TRNO', 'real*8 array of length (N_SPCSRF)', '-1.0', """
					Surface transparency in positive direction. If positive, will supercede the setting from the Eirene input file: TRANSP(1,) = SPS_TRNO. Ignored if negative.
				"""),
      
         ( 'SPS_TRNI', 'real*8 array of length (N_SPCSRF)', '-1.0', """
					Surface transparency in negative direction. If positive, will supercede the setting from the Eirene input file: TRANSP(2,) = SPS_TRNI. If negative, the setting from SPS_TRNO is used.
				"""),
      
         ( 'SPS_MTRI', 'real*8 array of length (N_SPCSRF)', '0', """
					Surface material in Eirene notation (e.g., 1206 for C). If positive, will supercede the setting from the Eirene input file: ZNML = SPS_MTRI. Ignored if negative.
				"""),
      
         ( 'SPS_MTRL', 'character*8 array of length (N_SPCSRF)', '', """
					Surface material in human notation (e.g., 'C').
				"""),
      
         ( 'SPS_TMPR', 'real*8 array of length (N_SPCSRF)', '1.e15', """
					Surface temperature (in eV). If set larger to 1.e10, will be ignored. Otherwise, will supercede the setting from the Eirene input file: EWALL = SPS_TMPR.
				"""),
      
         ( 'SPS_SPPH', 'real*8 array of length (N_SPCSRF)', '-1.0', """
					Fudge factor for physical sputtering. If positive, will supercede the setting from the Eirene input file: RECYCS = SPS_SPPH. Ignored if negative.
				"""),
      
         ( 'SPS_SPCH', 'real*8 array of length (N_SPCSRF)', '-1.0', """
					Fudge factor for chemical sputtering. If positive, will supercede the setting from the Eirene input file: RECYCC = SPS_SPCH. Ignored if negative.
				"""),
      
         ( 'SPS_SGRP', 'integer array of length (N_SPCSRF)', '-1', """
					Sputtered particle species flag for chemical sputtering. If positive, will supercede the setting from the Eirene input file: ISRC = SPS_SGRP. Ignored if negative.
				"""),
      
         ( 'WRITE_NML_NEUT', 'logical', '.true.', """
					If .true. (default), writes the content of the namelist to stdout after it has been read.
				"""),
      
         ( 'TIME_DEP_PUFF', 'logical array of length (NSTRAT)', '.false. for all strata', """
					Indicates whether a stratum is a time-dependent gas puff. Should only be .true. for strata defined as gas puffs.
				"""),
      
         ( 'NGPDATA', 'integer data of size (NSTRAT)', '0', """
					Number of points over which the time profile of the strength of gas puff (istra) is given. Defaults to 0. Current maximum value is 100.
				"""),
      
         ( 'GPDATA', 'real*8 data of size (NGPDATA,2,NSTRAT)', '0.0', """
					For (i,ik,istra) in (1:NGPDATA(istra),1:2,1:NSTRAT),
					GPDATA(i,1,istra) contains the time point (i) for stratum (istra) (in s).
					GPDATA(i,2,istra) contains the gas puff strength of stratum (istra) at time point (i) (in particles/s).
					The gas puff strength before the first time point is given by USERFLUXPARM(istra,1).
					The gas puff strength after the last time point is given by the GPDATA value of the last time point.
					Otherwise, the gas puff strength is linearly interpolated from the given data.
				"""),
      
         ( 'CHEMICAL_SPUTTER_YIELD', 'real*8 array of size (0:NLIM+NSTS)', '0.0', """
					Passed to Eirene. Chemical sputter yield of wall surface (ilim).
				"""),
      
         ( 'FCHAR_CHEMICAL', 'real*8', '0', """
					Nuclear charge of atomic species causing the sputtering. Default means no chemical sputtering.
				"""),
      
         ( 'IGASS_CHEMICAL', 'integer', '0', """
					Passed to Eirene. Eirene atomic species index of the sputtered particle. If igass_chemical &gt; natmi, the data from chemical_sputter_yield is not used and the yield from the Eirene surface blocks is used instead.
				"""),
      
         ( 'ITSPUT_CHEMICAL', 'integer', '0', """
					Passed to Eirene. Eirene type index of the sputtered particle. Atoms = 1, Ions = 4. Defaults to 0, meaning 1 eV atom chemical sputtering.
				"""),
      
         ( 'ISSPUT_CHEMICAL', 'integer', '0', """
					Passed to Eirene. Mass*100 + nuclear charge of the sputtered particle. Defaults to 0, internally changed to 1206 = carbon.
				"""),
      
   ],

  'b2.transport.parameters': [ 'namelist',
  
      ( 'FLAG*', 'switchgroup', [
        
               ('FLAG_DNA', 'integer', '','''
						Transport model flag for density-driven diffusion.
					'''), 
        
               ('FLAG_DPA', 'integer', '','''
						Transport model flag for pressure-driven dffusion.
					'''), 
        
               ('FLAG_VLA', 'integer', '','''
						Transport model flag for pinch velocity.
					'''), 
        
               ('FLAG_VSA', 'integer', '','''
						Transport model flag for viscosity.
					'''), 
        
               ('FLAG_HCI', 'integer', '','''
						Transport model flag for ion heat diffusivity.
					'''), 
        
               ('FLAG_HCE', 'integer', '','''
						Transport model flag for electron heat diffusivity.
					'''), 
        
               ('FLAG_SIG', 'integer', '','''
						Transport model flag for field-driven current radial conductivity.
					'''), 
        
               ('FLAG_ALF', 'integer', '','''
						Transport model flag for temperature-driven current radial conductivity.
					'''), 
        ],
         """
					All flags follow:
					FLAG=0: Use model from b2ah.dat and b2mn.dat. Default.
					FLAG=1: Constant, value set to PARM.
					FLAG=2: 1/N model, multiplied by PARM.
					FLAG=3: Bohm model, multiplied by PARM.
					FLAG=4: flux-scaled model, multiplied by PARM.
				"""),
         ( 'PARM_DNA', 'real*8 array of size (0:NS-1)', '', """
					Parameter for the density-driven particle diffusion coefficient for species (is).
				"""),
      
         ( 'PARM_DPA', 'real*8 array of size (0:NS-1)', '', """
					Parameter for the pressure-driven particle diffusion coefficient for species (is).
				"""),
      
         ( 'PARM_VLA', 'real*8 array of size (0:NS-1)', '', """
					Parameter for the anomalous radial pinch velocity for species (is).
				"""),
      
         ( 'PARM_VSA', 'real*8 array of size (0:NS-1)', '', """
					Parameter for the viscosity for species (is).
				"""),
      
         ( 'PARM_HCI', 'real*8 array of size (0:NS-1)', '', """
					Parameter for the heat diffusivity coefficient for species (is).
				"""),
      
         ( 'PARM_HCE', 'real*8', '', """
					Parameter for the electron heat diffusivity coefficient.
				"""),
      
         ( 'PARM_SIG', 'real*8', '', """
					Parameter for the anomalous radial field-driven current conductivity.
				"""),
      
         ( 'PARM_ALF', 'real*8', '', """
					Parameter for the anomalous radial temperature-driven current conductivity.
				"""),
      
         ( 'TRANSPORT_FILENAME', 'character*256', 'b2.transport.parameters', """
					Name of the next file to use for reading a new /TRANSPORT/ namelist.
				"""),
      
         ( 'TRANSPORT_TIME_MOD', 'real*8', '0.0', """
					When the B2 run simulation time, in seconds, modulo(TRANSPORT_TIME_MOD), exceeds TRANSPORT_TIME_SWITCH, reads the new namelist from TRANSPORT_FILENAME. Also switches to the new namelist if the ELM count (here time/TRANSPORT_TIME_MOD) changes.
					Only active if TRANSPORT_TIME_MOD is greater than 0.
				"""),
      
         ( 'TRANSPORT_TIME_SWITCH', 'real*8', '0.0', """
					Time (in seconds) within an ELM cycle after which a new /TRANSPORT/ namelist is read.
				"""),
      
      ( 'CFL*', 'switchgroup', [
        
               ('CFLME', 'real*8', 'Default inherited from b2mn.dat','''
						Multiplier to the electron heat flux limit.
					'''), 
        
               ('CFLMI', 'real*8', 'Default inherited from b2mn.dat','''
						Multiplier to the ion heat flux limit.
					'''), 
        
               ('CFLMV', 'real*8', 'Default inherited from b2mn.dat','''
						Multiplier to the viscous heat flux limit.
					'''), 
        
               ('CFLAL', 'real*8', 'Default inherited from b2mn.dat','''
						Multiplier to the thermo-electric coefficient flux limit.
					'''), 
        
               ('CFLAB', 'real*8', 'Default inherited from b2mn.dat','''
						Multiplier to the friction force flux limit.
					'''), 
        ],
         """
					For all flux limit multipliers, setting them to zero turns off the corresponding flux limiter.
				"""),
         ( 'WRITE_NML_TRANSP', 'logical', '.true.', """
					If .true. (default), writes the content of the namelist to stdout after it has been read.
				"""),
      
      ( '*_CNV', 'switchgroup', [
        
               ('VOUT_CNV', 'real*8 array of size (0:NS-1)', '0.0','''
						Value of the "blob" convection velocity for species (is) at the outer grid edge (in m/s).
					'''), 
        
               ('PW0_CNV', 'real*8 array of size (0:NS-1)', '1.0','''
						Exponent in radial profile of the "blob" velocity for species (is).
					'''), 
        
               ('PW1_CNV', 'real*8 array of size (0:NS-1)', '5.0','''
						First exponent in poloidal profile of the "blob" velocity for species (is).
					'''), 
        
               ('PW2_CNV', 'real*8 array of size (0:NS-1)', '2.0','''
						Second exponent in a poloidal profile of the "blob" velocity for species (is).
					'''), 
        ],
         """
					The four *_CNV parameters are only activated if 'b2tqna_user_transport' is set to '6'.
				"""),
   ],

  'b2.atomic_physics_rescale.parameters': [ 'namelist',
  
         ( 'RESCALE_SA', 'real*8 array of size(0:NS-1)', '1.0', """
					Scaling factors for rtsa: ionisation rates of species (is).
				"""),
      
         ( 'RESCALE_RA', 'real*8 array of size(0:NS-1)', '1.0', """
					Scaling factors for rtra: recombination rates of species (is).
				"""),
      
         ( 'RESCALE_QA', 'real*8 array of size(0:NS-1)', '1.0', """
					Scaling factors for rtqa: electron cooling rates of species (is).
				"""),
      
         ( 'RESCALE_CX', 'real*8 array of size(0:NS-1)', '1.0', """
					Scaling factors for rtcx: charge exchange rates of species (is).
				"""),
      
         ( 'RESCALE_RD', 'real*8 array of size(0:NS-1)', '1.0', """
					Scaling factors for rtrd: line radiation rates of species (is).
				"""),
      
         ( 'RESCALE_BR', 'real*8 array of size(0:NS-1)', '1.0', """
					Scaling factors for rtbr: bremsstrahlung radiation rates of species (is).
				"""),
      
   ],

  'b2.user.parameters': [ 'namelist',
  
         ( 'LHETRGTS', 'integer array of size (NLIM)', 'Eirene recycling target surfaces defined in the LTNS array', """
					List of surface indices (EIRENE notation) which are used for calculation of helium enrichment.
				"""),
      
         ( 'LPFRB_I', 'integer', '0', """
					B2 x-cell index corresponding to the first edge of the bypass between the inner and outer divertor (inner divertor, edge closest to target). If non-positive, counted backwards from the X-point location in the lower PFR, from the inner upper target in the upper PFR, from the lower outer target in the outer SOL, and from the inner upper target in the inner SOL.
				"""),
      
         ( 'LPFRB_O', 'integer', '0', """
					B2 x-cell index corresponding to the first edge of the bypass between the inner and outer divertor (outer divertor, edge closest to target). If non-positive, counted backwards from the outer lower target in the lower PFR, from the lower outer target in the outer SOL, from the upper outer target in the upper PFR, and from the inner upper target in the inner SOL.
				"""),
      
         ( 'LPFRT_I', 'integer', '0', """
					B2 x-cell index corresponding to the second edge of the bypass between the inner and outer divertor (inner side, edge furthest to target). If non-positive, counted backwards from the X-point location in the PFR, from the outer target in the outer SOL for a SN, from the top targets in the SOL for a DN.
				"""),
      
         ( 'LPFRT_O', 'integer', '0', """
					B2 x-cell index corresponding to the second edge of the bypass between the inner and outer divertor (outer divertor, edge furthest to target). If non-positive, counted backwards from the X-point location in the PFR, from the outer target in the outer SOL for a SN, from the top targets in the SOL for a DN.
				"""),
      
         ( 'J_HE_AT', 'integer', '', """
					Species index of the helium atoms in Eirene. The code attempts to find a match by default.
				"""),
      
         ( 'J_NE_AT', 'integer', '', """
					Species index of the neon atoms in Eirene. The code attempts to find a match by default.
				"""),
      
         ( 'J_H_AT', 'integer', '', """
					Species index of the hydrogen atoms in Eirene. The code attempts to find a match by default.
				"""),
      
         ( 'L_H_MOL', 'integer array of size (NMOL)', '', """
					Number of hydrogen nuclei for molecules in Eirene. The code attempts to find a match by default.
				"""),
      
         ( 'FUSION_POWER', 'real*8', '0.0', """
					Fusion power occuring in core (including neutrons, in Megawatts).
				"""),
      
         ( 'SPMP_HE_TO_D', 'real*8', '1.0', """
					Ratio of He to DT pumping speeds (typically, 0.8).
				"""),
      
         ( 'LPFRS_PMP', 'integer', '0', """
					Location of the pump. 0 no pump at all (default), 1 - lower PFR, 2 - outer SOL, 3 - upper PFR, 4 - inner SOL
				"""),
      
         ( 'NPFRGRP', 'integer', '0', """
					Actual number of surface groups for PFR flows.
				"""),
      
         ( 'LPFRGRP', 'integer array of size (NLIM)', '', """
					List of surface segments for PFR flows.
				"""),
      
         ( 'IPFRGRP', 'integer array of size (NPFRGRP)', '0', """
					First positions in this list for each group.
				"""),
      
         ( 'JPFRGRP', 'integer array of size (NPFRGRP)', '0', """
					Last positions in this list for each group.
				"""),
      
         ( 'GPFRGRP', 'character*8 array of size (NPFRGRP)', ' ', """
					Labels for surface groups for PFR flows.
				"""),
      
         ( 'NNTRGRP', 'integer', '', """
					Actual number of surface groups for neutral data.
				"""),
      
         ( 'LNTRGRP', 'integer array of size (NLIM)', '', """
					List of surface segments for neutral data.
				"""),
      
         ( 'INTRGRP', 'integer array of size (NNTRGRP)', '', """
					First positions in this list for each group.
				"""),
      
         ( 'JNTRGRP', 'integer array of size (NNTRGRP)', '', """
					Last positions in this list for each group.
				"""),
      
         ( 'GNTRGRP', 'character*8 array of size (NNTRGRP)', '', """
					Labels for the neutral data surface groups.
				"""),
      
         ( 'SPMP_NOM', 'real*8', '0.0', """
					Nominal pumping speed.
				"""),
      
         ( 'FILEDATA', 'logical array of size 10', '.true.', """
					Switches to turn on/off the tracing files controlled by the ank_tracing switch. The files are defined in b2mod_diag, in order, starting with element 2 of the filedata array: test.trc, residuals.trc, sources.trc, blnn.trc, blne.trc, integral.trc, user.trc, blnm.trc, sepdata.trc.
					If there is no b2.user.parameters file present, the flag for user.trc is set to .false..
					If the tracing files are to be appended but a reading error occurs when opening them, the corresponding filedata element is overwritten to .false..
				"""),
      
         ( 'USER_FILENAME', 'character*80', 'b2.user.parameters', """
					Filename where /USER/ namelist is stored.
				"""),
      
   ],

  'b2.sources.profile': [ 'namelist',
  
         ( 'NSDATA', 'integer array of size (NKIND_DATA,NKIND_SOURCE,0:NS)', '0', """
					Number of points over which the source profile of (kind_data,kind_source,is) is defined. Should not exceed NY+2.
						If KIND_DATA=1, the data is expressed as a profile in physical distance from the separatrix (in metres) along the outer midplane.
						The user can change this default reference location by use of the 'set_transport_i[xy]ref' switches.
						If KIND_DATA=2, the data is expressed as a profile in flux distance from the separatrix (not yet available).
				"""),
      
         ( 'SDATA', 'real*8 data of size (2,NY+2,NKIND_SOURCE,0:NS)', '0.0', """
					For (i,ir,ik,is) in (1:2,1:NY+2,1:NKIND_SOURCE,0:NS),
					SDATA(1,ir,:,:) contains the radial location of the profile point (ir).
					SDATA(2,ir,:,:) contains the source profile value at point (ir).
					KIND_SOURCE=1 means particle source of species (is) (in particles/m3)
					KIND_SOURCE=2 means parallel momentum source for species (is) (in kg.m/s/m3)
					KIND_SOURCE=3 means electron heat source (in Watts/m3)
					KIND_SOURCE=4 means ion heat source (in Watts/m3)
					KIND_SOURCE=5 means electric charge source (in Coulombs/m3)
					KIND_SOURCE=6 means non-ambipolar electron particle source (in e/m3)
				"""),
      
         ( 'NXDATA', 'integer array of size (NKIND_DATA,NKIND_SOURCE,0:NS)', '', """
					Number of points over which the axial profile of (kind_data,kind_source,is) is defined. Should not exceed NX+2. Defaults to 0.
					If KIND_DATA=1, the data is expressed as a profile in physical distance, here connection length, rescaled from 0.0 to 1.0.
					For closed field lines, the reference location for the zero of distance is set by use of the 'set_transport_i[xy]ref' switches.
					If KIND_DATA=2, the data is expressed as a profile in (ix) cell index, again normalized from 0.0 to 1.0 to match the [0:nx-1] interval.
				"""),
      
         ( 'XDATA', 'real*8 data of size (2,NY+2,NKIND_SOURCE,0:NS)', '1.0', """
					Multiplier to the poloidal source profile in the axial direction. Same convention for KIND_SOURCE as above.
				"""),
      
         ( 'DIVHEAT', 'real*8', '0.0', """
					Additional divertor ion heat source (in Watts/m3)
				"""),
      
         ( 'SOURCES_FILENAME', 'character*256', 'b2.sources.profile', """
					Name of the next file to use for reading a new /PROFILE/ namelist. Quantities not present in the new file will be inherited from the old one.
				"""),
      
         ( 'SOURCES_TIME_MOD', 'real*8', '0.0', """
					When the B2 run simulation time, in seconds, modulo(SOURCES_TIME_MOD),exceeds SOURCES_TIME_SWITCH, reads the new namelist from SOURCES_FILENAME. Also switches to the new namelist if the ELM count (here time/SOURCES_TIME_MOD) changes. Only active if SOURCES_TIME_MOD is greater than 0.
				"""),
      
         ( 'SOURCES_TIME_SWITCH', 'real*8', '0.0', """
					Time (in seconds) within an ELM cycle after which a new /PROFILE/ namelist is read.
				"""),
      
   ],


}



