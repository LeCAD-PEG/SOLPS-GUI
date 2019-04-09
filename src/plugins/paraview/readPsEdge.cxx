/**
*-------------------------------------------------------------------------------
*   @file     readPsEdge.cxx
*   @Author   Dejan Penko, University of Ljubljana
*   @brief    This is the C++ file of the ParaView ReadUALEdge file for
*             handling data fields.
*   DESCRIPTION
*   This file provides C++ routines for reading the plasma state out of
*   edge_profiles, edge_sources and edge_transport IDSs.
*
*   Currently the included data fields are:
*       - grid geometry from any of the above IDSs;
*       - plasma state:
*           ~ edge_profiles:
*               - electrons:
*                   - temperature;
*                   - density;
*                   - density_fast;
*                   - pressure;
*                   - pressure_fast_perpendicular;
*                   - velocity:     @note: only for IMAS version <= 3.15.0
*                       - radial;
*                       - diamagnetic;
*                       - parallel;
*                       - poloidal;
*                       - toroidal;
*                   - distribution_function;
*               - ion:
*                   - temperature;
*                   - density;
*                   - density_fast;
*                   - pressure;
*                   - pressure_fast_perpendicular;
*                   - velocity:     @note: only for IMAS version <= 3.15.0
*                       - radial;
*                       - diamagnetic;
*                       - parallel;
*                       - poloidal;
*                       - toroidal;
*                   - distribution_function;
*           ~ edge_sources:
*               - electrons:
*                   - particles
*                   - energy
*               - ion:
*                   - particles
*                   - energy
*           ~ edge_transport:
*               - electrons:
*                   - particles:
*                       - d
*                       - v
*                       - flux
*                       - flux_limiter
*                   - energy:
*                       - d
*                       - v
*                       - flux
*                       - flux_limiter
*               - ion:
*                   - particles:
*                       - d
*                       - v
*                       - flux
*                       - flux_limiter
*                   - energy:
*                       - d
*                       - v
*                       - flux
*                       - flux_limiter
*
*-------------------------------------------------------------------------------
*/

#include "readPsEdge.h"
#include "VTKIDSutility.h"
#include "VTKIDSutilityTemplateClasses.cxx"
#include <UALClasses.h>
#include <vtkSmartPointer.h>
#include <fstream>
#include <iostream>
#include <string>

#define PLUGIN_IMAS_VERSION_DIGIT IMAS_VERSION_DIGIT

using namespace std;
using namespace IdsNs;

/**
*   Fill predefined vtkUnstructuredGrid (should already contain n-dimensional
*   geometry ) with plasma state data found in the specified IDS.
*
*   @param UG                       vtkUnstructuredGrid to be filled with
*                                   data fields
*   @param UG_db                    Base type of IDS data structure (IdsNs::IDS)
*   @param UG_gridSubset_index      Grid subset index of which data corresponds
*                                   to the current vtkUnstructuredGrid
*   @param UG_num_gridSubset_el     Number of elements of the relevant grid
*                                   subset
*   @param UG_LoadIDS_string        String containing name of the IDS of which
*                                   data fields are to be added to
*                                   vtkUnstructuredGrid
*   @param UG_ggd_slice_index       Array index of the ggd(:) array of
*                                   structures node
*   @param UG_EdgeSourcesSourceID   Array index of the source(:) array of
*                                   structures node (relevant only to
*                                   edge_sources IDS)
*   @param UG_EdgeTransportModelID  Array index of the model(:) array of
*                                   structures node (relevant only to
*                                   edge_transport IDS)
*/
template <typename IDS1>
void readPsEdge::setUnstructuredGridDataFields(
    vtkSmartPointer<vtkUnstructuredGrid> UG,
    IDS1 & UG_db,
    int UG_gridSubset_index,
    int UG_num_gridSubset_el,
    std::string UG_LoadIDS_string,
    int UG_ggd_slice_index,
    int UG_EdgeSourcesSourceID,
    int UG_EdgeTransportModelID)
{
//   @note   Below  is a variant of 'setUnstructuredGridDataFields_IMAS' routine,
//           made specifically for IMAS 3.15.1 due many issues with IMAS 3.15.1
//           ( while with IMAS 3.15.0 it works great).
//           It includes also full code of 'setAllDataFields_edge_profiles',
//           'setAllDataFields_edge_sources' and 'setAllDataFields_edge_profiles'
//           routines. For some strange reason those routines doesn't work with
//           IMAS 3.15.1 (the plugin freezes etc.).
#if IMAS_VERSION_DIGIT >= 3151
    // Object declaration for readPsEdge routines

    // For "edge_profiles" selection in "Load IDS" text box
    if( UG_LoadIDS_string.find( "edge_profiles" ) != std::string::npos)
    {

        VTKIDSutility vtkids_obj_ep;
        VTKIDSutilityTemplateClasses vtkids_obj_ep_template;
        // Set default value
        int num_IDStarget_gridSubsets = 0;

        // Assigning values - Electrons

        // Assign values found in Electrons Temperature array of structures
        // node to grid subsets objects
        num_IDStarget_gridSubsets = UG_db._edge_profiles
            .ggd(UG_ggd_slice_index).electrons.temperature.extent(0);
        for (int n = 0; n < num_IDStarget_gridSubsets; n++)
        {

            vtkids_obj_ep_template.VTK_IDS_Val2UnstrGrid_GenericGridScalar(
                "Electron Temperature",
                UG,
                UG_db._edge_profiles.ggd(UG_ggd_slice_index).electrons.temperature(n),
                UG_gridSubset_index,
                UG_num_gridSubset_el );

        }
        // Assign values found in Electrons Density array of structures node to
        // grid subsets objects
        num_IDStarget_gridSubsets = UG_db._edge_profiles
            .ggd(UG_ggd_slice_index).electrons.density.extent(0);
        for (int n = 0; n < num_IDStarget_gridSubsets; n++)
        {
            vtkids_obj_ep_template.VTK_IDS_Val2UnstrGrid_GenericGridScalar(
                "Electron Density",
                UG,
                UG_db._edge_profiles.ggd(UG_ggd_slice_index).electrons.density(n),
                UG_gridSubset_index,
                UG_num_gridSubset_el );
        }

        // Assign values found in Electrons Density_Fast array of structures
        // node to grid subsets objects
        num_IDStarget_gridSubsets = UG_db._edge_profiles
            .ggd(UG_ggd_slice_index).electrons.density_fast.extent(0);
        for (int n = 0; n < num_IDStarget_gridSubsets; n++)
        {
            vtkids_obj_ep_template.VTK_IDS_Val2UnstrGrid_GenericGridScalar(
                "Electron Density_Fast",
                UG,
                UG_db._edge_profiles.ggd(UG_ggd_slice_index).electrons
                    .density_fast(n),
                UG_gridSubset_index,
                UG_num_gridSubset_el );
        }

        // Assign values found in Electrons Pressure array of structures node to
        // grid subsets objects
        num_IDStarget_gridSubsets = UG_db._edge_profiles.ggd(UG_ggd_slice_index)
            .electrons.pressure.extent(0);
        for (int n = 0; n < num_IDStarget_gridSubsets; n++)
        {
            vtkids_obj_ep_template.VTK_IDS_Val2UnstrGrid_GenericGridScalar(
                "Electron Pressure",
                UG,
                UG_db._edge_profiles.ggd(UG_ggd_slice_index).electrons
                    .pressure(n),
                UG_gridSubset_index,
                UG_num_gridSubset_el );
        }

        // Assign values found in Electrons Pressure_Fast_Perpendicular array of
        // structures node to grid subsets objects
        num_IDStarget_gridSubsets = UG_db._edge_profiles.ggd(UG_ggd_slice_index).electrons
            .pressure_fast_perpendicular.extent(0);
        for (int n = 0; n < num_IDStarget_gridSubsets; n++)
        {
            vtkids_obj_ep_template.VTK_IDS_Val2UnstrGrid_GenericGridScalar(
                "Electron Pressure_Fast_Perpendicular",
                UG,
                UG_db._edge_profiles.ggd(UG_ggd_slice_index).electrons
                    .pressure_fast_perpendicular(n),
                UG_gridSubset_index,
                UG_num_gridSubset_el );
        }

        // Assign values found in Electrons Pressure_Fast_Parallel array of
        // structures  node to grid subsets objects
        num_IDStarget_gridSubsets = UG_db._edge_profiles
            .ggd(UG_ggd_slice_index).electrons.pressure_fast_parallel.extent(0);
        for (int n = 0; n < num_IDStarget_gridSubsets; n++)
        {
            vtkids_obj_ep_template.VTK_IDS_Val2UnstrGrid_GenericGridScalar(
                "Electron Pressure_Fast_Parallel",
                UG,
                UG_db._edge_profiles.ggd(UG_ggd_slice_index).electrons
                    .pressure_fast_parallel(n),
                UG_gridSubset_index,
                UG_num_gridSubset_el );
        }

        // In IMAS 3.15.0 and older versions the .velocity IDS data structure is
        // simple structure node, while in 3.15.1 it was changed to array
        // of structures node
    #if IMAS_VERSION_DIGIT >= 3170
        // Reading Electron velocity ( GenericGridVectorComponents data structure
        // type )
        num_IDStarget_gridSubsets = UG_db._edge_profiles.ggd(UG_ggd_slice_index)
            .electrons.velocity.extent(0);
        // Assign values found in Electrons Velocity array of structures
        // node - Radial simple structure node to grid subsets objects
        for (int n = 0; n < num_IDStarget_gridSubsets; n++)
        {
            vtkids_obj_ep_template.VTK_IDS_Val2UnstrGrid_GenericGridVectorComponents(
                "Electron Velocity - Radial",
                UG,
                UG_db._edge_profiles.ggd(UG_ggd_slice_index).electrons.velocity(n),
                "radial",
                UG_gridSubset_index,
                UG_num_gridSubset_el );
        }

        // Assign values found in Electrons Velocity array of structures
        // node - Diamagnetic simple structure node to grid subsets objects
        for (int n = 0; n < num_IDStarget_gridSubsets; n++)
        {
            vtkids_obj_ep_template.VTK_IDS_Val2UnstrGrid_GenericGridVectorComponents(
                "Electron Velocity - Diamagnetic",
                UG,
                UG_db._edge_profiles.ggd(UG_ggd_slice_index).electrons.velocity(n),
                "diamagnetic",
                UG_gridSubset_index,
                UG_num_gridSubset_el );
        }

        // Assign values found in Electrons Velocity array of structures
        // node - Parallel simple structure node to grid subsets objects
        for (int n = 0; n < num_IDStarget_gridSubsets; n++)
        {
            vtkids_obj_ep_template.VTK_IDS_Val2UnstrGrid_GenericGridVectorComponents(
                "Electron Velocity - Parallel",
                UG,
                UG_db._edge_profiles.ggd(UG_ggd_slice_index).electrons.velocity(n),
                "parallel",
                UG_gridSubset_index,
                UG_num_gridSubset_el );
        }

        // Assign values found in Electrons Velocity array of structures
        // node - Poloidal simple structure node to grid subsets objects
        for (int n = 0; n < num_IDStarget_gridSubsets; n++)
        {
            vtkids_obj_ep_template.VTK_IDS_Val2UnstrGrid_GenericGridVectorComponents(
                "Electron Velocity - Poloidal",
                UG,
                UG_db._edge_profiles.ggd(UG_ggd_slice_index).electrons.velocity(n),
                "poloidal",
                UG_gridSubset_index,
                UG_num_gridSubset_el );
        }

        // Assign values found in Electrons Velocity array of structures
        // node - Toroidal simple structure node to grid subsets objects
        for (int n = 0; n < num_IDStarget_gridSubsets; n++)
        {
            vtkids_obj_ep_template.VTK_IDS_Val2UnstrGrid_GenericGridVectorComponents(
                "Electron Velocity - Toroidal",
                UG,
                UG_db._edge_profiles.ggd(UG_ggd_slice_index).electrons.velocity(n),
                "toroidal",
                UG_gridSubset_index,
                UG_num_gridSubset_el );
        }
    #endif

        // Assign values found in Electrons Distribution Function array of
        // structures node to grid subsets objects
        num_IDStarget_gridSubsets = UG_db._edge_profiles
            .ggd(UG_ggd_slice_index).electrons.distribution_function.extent(0);
        for (int n = 0; n < num_IDStarget_gridSubsets; n++)
        {
            vtkids_obj_ep_template.VTK_IDS_Val2UnstrGrid_GenericGridScalar(
                "Electron Distribution Function",
                UG,
                UG_db._edge_profiles.ggd(UG_ggd_slice_index).electrons
                    .distribution_function(n),
                UG_gridSubset_index,
                UG_num_gridSubset_el );
        }

        // Assign values found in Ion substructure to grid subsets
        // objects (2D cells)
        int num_ion_species = UG_db._edge_profiles
            .ggd(UG_ggd_slice_index).ion.extent(0);

        // Set empty string for holding the ion species label
        std::string ion_label = "";

        for( int k = 0; k < num_ion_species; k++)
        {
            std::string ion_array_label;
            // Set ion species label
            // Search in ion(:).label and ion(:).state(0).label
            if (UG_db._edge_profiles.ggd(UG_ggd_slice_index).ion(k).label.empty())
            {
                if (UG_db._edge_profiles.ggd(UG_ggd_slice_index).ion(k).state.extent(0) > 0
                    && !UG_db._edge_profiles.ggd(UG_ggd_slice_index).ion(k).state(0).label.empty())
                {
                    ion_label = UG_db._edge_profiles
                        .ggd(UG_ggd_slice_index).ion(k).state(0).label;
                }
            }
            else
            {
                ion_label = UG_db._edge_profiles.
                    ggd(UG_ggd_slice_index).ion(k).label;
            }

            // Assign values found in Ion Temperature array of structures
            // node to grid subsets objects
            // Set data field label
            ion_array_label = vtkids_obj_ep.VTK_IDS_SetIonQuantityLabel(
                "Temperature", k, ion_label );
            num_IDStarget_gridSubsets = UG_db._edge_profiles
                .ggd(UG_ggd_slice_index).ion(k).temperature.extent(0);
            for (int n = 0; n < num_IDStarget_gridSubsets; n++)
            {
                vtkids_obj_ep_template.VTK_IDS_Val2UnstrGrid_GenericGridScalar(
                    ion_array_label,
                    UG,
                    UG_db._edge_profiles.
                        ggd(UG_ggd_slice_index).ion(k).temperature(n),
                    UG_gridSubset_index,
                    UG_num_gridSubset_el );
            }

            // Assign values found in Ion Density array of structures
            // node to grid subsets objects
            // Set data field label
            ion_array_label = vtkids_obj_ep.VTK_IDS_SetIonQuantityLabel(
                "Density", k, ion_label );
            num_IDStarget_gridSubsets = UG_db._edge_profiles
                .ggd(UG_ggd_slice_index).ion(k).density.extent(0);
            for (int n = 0; n < num_IDStarget_gridSubsets; n++)
            {
                vtkids_obj_ep_template.VTK_IDS_Val2UnstrGrid_GenericGridScalar(
                    ion_array_label,
                    UG,
                    UG_db._edge_profiles.ggd(UG_ggd_slice_index).ion(k)
                        .density(n),
                    UG_gridSubset_index,
                    UG_num_gridSubset_el );
            }

            // Assign values found in Ion Density_Fast array of structures
            // node to grid subsets objects
            // Set data field label
            ion_array_label = vtkids_obj_ep.VTK_IDS_SetIonQuantityLabel(
                "Density_Fast", k, ion_label );
            num_IDStarget_gridSubsets = UG_db._edge_profiles
                .ggd(UG_ggd_slice_index).ion(k).density_fast.extent(0);
            for (int n = 0; n < num_IDStarget_gridSubsets; n++)
            {
                vtkids_obj_ep_template.VTK_IDS_Val2UnstrGrid_GenericGridScalar(
                    ion_array_label,
                    UG,
                    UG_db._edge_profiles.ggd(UG_ggd_slice_index).ion(k)
                        .density_fast(n),
                    UG_gridSubset_index,
                    UG_num_gridSubset_el );
            }

            // Assign values found in Ion Pressure array of structures
            // node to grid subsets objects
            // Set data field label
            ion_array_label = vtkids_obj_ep.VTK_IDS_SetIonQuantityLabel(
                "Pressure", k, ion_label );
            num_IDStarget_gridSubsets = UG_db._edge_profiles
                .ggd(UG_ggd_slice_index).ion(k).pressure.extent(0);
            for (int n = 0; n < num_IDStarget_gridSubsets; n++)
            {
                vtkids_obj_ep_template.VTK_IDS_Val2UnstrGrid_GenericGridScalar(
                    ion_array_label,
                    UG,
                    UG_db._edge_profiles.ggd(UG_ggd_slice_index).ion(k)
                        .pressure(n),
                    UG_gridSubset_index,
                    UG_num_gridSubset_el );
            }

            // Assign values found in Ion Pressure - Fast Perpendicular array of
            // structures node to grid subsets objects
            // Set data field label
            ion_array_label = vtkids_obj_ep.VTK_IDS_SetIonQuantityLabel(
                "Pressure - Fast Perpendicular", k, ion_label );
            num_IDStarget_gridSubsets = UG_db._edge_profiles
                .ggd(UG_ggd_slice_index).ion(k).pressure_fast_perpendicular
                .extent(0);
            for (int n = 0; n < num_IDStarget_gridSubsets; n++)
            {
                vtkids_obj_ep_template.VTK_IDS_Val2UnstrGrid_GenericGridScalar(
                    ion_array_label,
                    UG,
                    UG_db._edge_profiles.ggd(UG_ggd_slice_index).ion(k)
                        .pressure_fast_perpendicular(n),
                    UG_gridSubset_index,
                    UG_num_gridSubset_el );
            }

            // Assign values found in Ion Pressure - Fast Parallel array of
            // structures node to grid subsets objects
            // Set data field label
            ion_array_label = vtkids_obj_ep.VTK_IDS_SetIonQuantityLabel(
                "Pressure - Fast Parallel", k, ion_label );
            num_IDStarget_gridSubsets = UG_db._edge_profiles
                .ggd(UG_ggd_slice_index).ion(k).pressure_fast_parallel.extent(0);
            for (int n = 0; n < num_IDStarget_gridSubsets; n++)
            {
                vtkids_obj_ep_template.VTK_IDS_Val2UnstrGrid_GenericGridScalar(
                    ion_array_label,
                    UG,
                    UG_db._edge_profiles.ggd(UG_ggd_slice_index).ion(k)
                        .pressure_fast_parallel(n),
                    UG_gridSubset_index,
                    UG_num_gridSubset_el );
            }

        // In IMAS 3.15.0 and older versions the .velocity IDS data structure is
        // simple structure node, while in 3.6.4 it was changed to array
        // of structures node
    #if IMAS_VERSION_DIGIT >= 3170
            // Reading Ion velocity ( GenericGridVectorComponents data structure
            // type )
            num_IDStarget_gridSubsets = UG_db._edge_profiles
                .ggd(UG_ggd_slice_index).ion(k).velocity.extent(0);
            // Assign values found in Ion Velocity array of structures
            // node - Radial simple structure node to grid subsets objects
            // Set data field label
            ion_array_label = vtkids_obj_ep.VTK_IDS_SetIonQuantityLabel(
                "Velocity - Radial", k, ion_label );
            for (int n = 0; n < num_IDStarget_gridSubsets; n++)
            {
                vtkids_obj_ep_template.VTK_IDS_Val2UnstrGrid_GenericGridVectorComponents(
                    ion_array_label,
                    UG,
                    UG_db._edge_profiles.ggd(UG_ggd_slice_index).ion(k)
                        .velocity(n),
                    "radial",
                    UG_gridSubset_index,
                    UG_num_gridSubset_el );
            }

            // Assign values found in Ion Velocity array of structures
            // node - Diamagnetic simple structure node to grid subsets objects
            // Set data field label
            ion_array_label = vtkids_obj_ep.VTK_IDS_SetIonQuantityLabel(
                "Velocity - Diamagnetic", k, ion_label );
            for (int n = 0; n < num_IDStarget_gridSubsets; n++)
            {
                vtkids_obj_ep_template.VTK_IDS_Val2UnstrGrid_GenericGridVectorComponents(
                    ion_array_label,
                    UG,
                    UG_db._edge_profiles.ggd(UG_ggd_slice_index).ion(k)
                        .velocity(n),
                    "diamagnetic",
                    UG_gridSubset_index,
                    UG_num_gridSubset_el );
            }

            // Assign values found in Ion Velocity array of structures
            // node - Parallel simple structure node to grid subsets objects
            // Set data field label
            ion_array_label = vtkids_obj_ep.VTK_IDS_SetIonQuantityLabel(
                "Velocity - Parallel", k, ion_label );
            for (int n = 0; n < num_IDStarget_gridSubsets; n++)
            {
                vtkids_obj_ep_template.VTK_IDS_Val2UnstrGrid_GenericGridVectorComponents(
                    ion_array_label,
                    UG,
                    UG_db._edge_profiles.ggd(UG_ggd_slice_index).ion(k)
                        .velocity(n),
                    "parallel",
                    UG_gridSubset_index,
                    UG_num_gridSubset_el );
            }

            // Assign values found in Ion Velocity array of structures
            // node - Poloidal simple structure node to grid subsets objects
            // Set data field label
            ion_array_label = vtkids_obj_ep.VTK_IDS_SetIonQuantityLabel(
                "Velocity - Poloidal", k, ion_label );
            for (int n = 0; n < num_IDStarget_gridSubsets; n++)
            {
                vtkids_obj_ep_template.VTK_IDS_Val2UnstrGrid_GenericGridVectorComponents(
                    ion_array_label,
                    UG,
                    UG_db._edge_profiles.ggd(UG_ggd_slice_index).ion(k)
                        .velocity(n),
                    "poloidal",
                    UG_gridSubset_index,
                    UG_num_gridSubset_el );
            }

            // Assign values found in Ion Velocity array of structures
            // node - Toroidal simple structure node to grid subsets objects
            // Set data field label
            ion_array_label = vtkids_obj_ep.VTK_IDS_SetIonQuantityLabel(
                "Velocity - Toroidal", k, ion_label );
            for (int n = 0; n < num_IDStarget_gridSubsets; n++)
            {
                vtkids_obj_ep_template.VTK_IDS_Val2UnstrGrid_GenericGridVectorComponents(
                    ion_array_label,
                    UG,
                    UG_db._edge_profiles.ggd(UG_ggd_slice_index).ion(k)
                        .velocity(n),
                    "toroidal",
                    UG_gridSubset_index,
                    UG_num_gridSubset_el );
            }
    #endif

            // Assign values found in Ion Energy Density Kinetic array of
            // structures node to grid subsets objects
            // Set data field label
            ion_array_label = vtkids_obj_ep.VTK_IDS_SetIonQuantityLabel(
                "Energy Density Kinetic", k, ion_label );
            num_IDStarget_gridSubsets = UG_db._edge_profiles
                .ggd(UG_ggd_slice_index).ion(k).energy_density_kinetic.extent(0);
            for (int n = 0; n < num_IDStarget_gridSubsets; n++)
            {
                vtkids_obj_ep_template.VTK_IDS_Val2UnstrGrid_GenericGridScalar(
                    ion_array_label,
                    UG,
                    UG_db._edge_profiles.ggd(UG_ggd_slice_index).ion(k)
                        .energy_density_kinetic(n),
                    UG_gridSubset_index,
                    UG_num_gridSubset_el );
            }
        }
    // For "edge_sources" selection in "Load IDS" text box
    }else if( UG_LoadIDS_string.find( "edge_sources" ) !=
        std::string::npos )
    {

        // Check if the SourceID is fine
        if ( UG_EdgeSourcesSourceID > UG_db._edge_sources.source.extent(0))
        {

            vtkOutputWindowDisplayWarningText("Warning! The set Source ID is out"
                " of bounds. \n");
            return;
        }

        VTKIDSutility vtkids_obj_ep;
        VTKIDSutilityTemplateClasses vtkids_obj_ep_template;
        // Set default value
        int num_IDStarget_gridSubsets = 0;

        // Assigning values - Electrons

        // Assign values found in Electrons Particles array of structures node to
        // grid subsets objects
        num_IDStarget_gridSubsets = UG_db._edge_sources
            .source(UG_EdgeSourcesSourceID).ggd(UG_ggd_slice_index)
            .electrons.particles.extent(0);
        for (int n = 0; n < num_IDStarget_gridSubsets; n++)
        {
            vtkids_obj_ep_template.VTK_IDS_Val2UnstrGrid_GenericGridScalar(
                "Electron Particles",
                UG,
                UG_db._edge_sources.source(UG_EdgeSourcesSourceID)
                    .ggd(UG_ggd_slice_index).electrons.particles(n),
                UG_gridSubset_index,
                UG_num_gridSubset_el );
        }

        // Assign values found in Electrons Energy array of structures node to
        // grid subsets objects
        num_IDStarget_gridSubsets = UG_db._edge_sources
            .source(UG_EdgeSourcesSourceID).ggd(UG_ggd_slice_index)
            .electrons.energy.extent(0);
        for (int n = 0; n < num_IDStarget_gridSubsets; n++)
        {
            vtkids_obj_ep_template.VTK_IDS_Val2UnstrGrid_GenericGridScalar(
                "Electron Energy",
                UG,
                UG_db._edge_sources.source(UG_EdgeSourcesSourceID)
                    .ggd(UG_ggd_slice_index).electrons.energy(n),
                UG_gridSubset_index,
                UG_num_gridSubset_el );
        }

        // Assign values found in Ion substructure to grid subsets
        // objects (2D cells)
        int num_ion_species = UG_db._edge_sources
            .source(UG_EdgeSourcesSourceID).ggd(UG_ggd_slice_index).ion
            .extent(0);
        for( int k = 0; k < num_ion_species; k++)
        {
            // Set ion specie label
            std::string ion_label= UG_db._edge_sources
                .source(UG_EdgeSourcesSourceID).ggd(UG_ggd_slice_index)
                .ion(k).label;
            std::string ion_array_label;

            // Assign values found in Ion Particles array of structures
            // node to grid subsets objects
            // Set data field label
            ion_array_label = vtkids_obj_ep.VTK_IDS_SetIonQuantityLabel(
                "Particles", k, ion_label );
            num_IDStarget_gridSubsets = UG_db._edge_sources
                .source(UG_EdgeSourcesSourceID).ggd(UG_ggd_slice_index)
                .ion(k).particles.extent(0);
            for (int n = 0; n < num_IDStarget_gridSubsets; n++)
            {
                vtkids_obj_ep_template.VTK_IDS_Val2UnstrGrid_GenericGridScalar(
                    ion_array_label,
                    UG,
                    UG_db._edge_sources.source(UG_EdgeSourcesSourceID)
                        .ggd(UG_ggd_slice_index).ion(k).particles(n),
                    UG_gridSubset_index,
                    UG_num_gridSubset_el );
            }


            // Assign values found in Ion Energy array of structures
            // node to grid subsets objects
            // Set data field label
            ion_array_label = vtkids_obj_ep.VTK_IDS_SetIonQuantityLabel(
                "Energy", k, ion_label );
            num_IDStarget_gridSubsets =UG_db._edge_sources
                .source(UG_EdgeSourcesSourceID).ggd(UG_ggd_slice_index)
                .ion(k).energy.extent(0);
            for (int n = 0; n < num_IDStarget_gridSubsets; n++)
            {
                vtkids_obj_ep_template.VTK_IDS_Val2UnstrGrid_GenericGridScalar(
                    ion_array_label,
                    UG,
                    UG_db._edge_sources.source(UG_EdgeSourcesSourceID)
                        .ggd(UG_ggd_slice_index).ion(k).energy(n),
                    UG_gridSubset_index,
                    UG_num_gridSubset_el );
            }
        }
    // For "edge_transport" selection in "Load IDS" text box
    }else if( UG_LoadIDS_string.find( "edge_transport" ) !=
        std::string::npos )
    {

        // Check if the ModelID is fine
        if ( UG_EdgeTransportModelID > UG_db._edge_transport.model.extent(0))
        {

            vtkOutputWindowDisplayWarningText("Warning! The set Model ID is out"
                " of bounds. \n");
            return;
        }

        VTKIDSutility vtkids_obj_ep;
        VTKIDSutilityTemplateClasses vtkids_obj_ep_template;

        // Set default value
        int num_IDStarget_gridSubsets = 0;

        // Assigning values - Electrons

        // Assign values found in Electrons Particles - Effective Diffusivity (d)
        // array of structures node to grid subsets objects
        num_IDStarget_gridSubsets =
            UG_db._edge_transport.model(UG_EdgeTransportModelID)
            .ggd(UG_ggd_slice_index).electrons.particles.d.extent(0);
        for (int n = 0; n < num_IDStarget_gridSubsets; n++)
        {
            vtkids_obj_ep_template.VTK_IDS_Val2UnstrGrid_GenericGridScalar(
                "Electron Particles - Effective Diffusivity",
                UG,
                UG_db._edge_transport.model(UG_EdgeTransportModelID)
                    .ggd(UG_ggd_slice_index).electrons.particles.d(n),
                UG_gridSubset_index,
                UG_num_gridSubset_el);
        }

        // Assign values found in Electrons Particles - Effective Convection (v)
        // array of structures node to grid subsets objects
        num_IDStarget_gridSubsets =
            UG_db._edge_transport.model(UG_EdgeTransportModelID)
            .ggd(UG_ggd_slice_index).electrons.particles.v.extent(0);
        for (int n = 0; n < num_IDStarget_gridSubsets; n++)
        {
            vtkids_obj_ep_template.VTK_IDS_Val2UnstrGrid_GenericGridScalar(
                "Electron Particles - Effective Convection",
                UG,
                UG_db._edge_transport.model(UG_EdgeTransportModelID)
                    .ggd(UG_ggd_slice_index).electrons.particles.v(n),
                UG_gridSubset_index,
                UG_num_gridSubset_el);
        }

        // Assign values found in Electrons Particles - Flux array of structures
        // node to grid subsets objects
        num_IDStarget_gridSubsets =
            UG_db._edge_transport.model(UG_EdgeTransportModelID)
            .ggd(UG_ggd_slice_index).electrons.particles.flux.extent(0);
        for (int n = 0; n < num_IDStarget_gridSubsets; n++)
        {
            vtkids_obj_ep_template.VTK_IDS_Val2UnstrGrid_GenericGridScalar(
                "Electron Particles - Flux",
                UG,
                UG_db._edge_transport.model(UG_EdgeTransportModelID)
                    .ggd(UG_ggd_slice_index).electrons.particles.flux(n),
                UG_gridSubset_index,
                UG_num_gridSubset_el);
        }

        // Assign values found in Electrons Particles - Flux Limiter array of
        // structures node to grid subsets objects
        num_IDStarget_gridSubsets =
            UG_db._edge_transport.model(UG_EdgeTransportModelID)
            .ggd(UG_ggd_slice_index).electrons.particles.flux_limiter.extent(0);
        for (int n = 0; n < num_IDStarget_gridSubsets; n++)
        {
            vtkids_obj_ep_template.VTK_IDS_Val2UnstrGrid_GenericGridScalar(
                "Electron Particles - Flux Limiter",
                UG,
                UG_db._edge_transport.model(UG_EdgeTransportModelID)
                    .ggd(UG_ggd_slice_index).electrons.particles.flux_limiter(n),
                UG_gridSubset_index,
                UG_num_gridSubset_el);
        }

        // Assign values found in Electrons Energy - Effective Diffusivity (d)
        // array of structures node to grid subsets objects
        num_IDStarget_gridSubsets =
            UG_db._edge_transport.model(UG_EdgeTransportModelID)
            .ggd(UG_ggd_slice_index).electrons.energy.d.extent(0);
        for (int n = 0; n < num_IDStarget_gridSubsets; n++)
        {
            vtkids_obj_ep_template.VTK_IDS_Val2UnstrGrid_GenericGridScalar(
                "Electron Energy - Effective Diffusivity",
                UG,
                UG_db._edge_transport.model(UG_EdgeTransportModelID)
                    .ggd(UG_ggd_slice_index).electrons.energy.d(n),
                UG_gridSubset_index,
                UG_num_gridSubset_el);
        }

        // Assign values found in Electrons Energy - Effective convection (d)
        // array of structures node to grid subsets objects
        num_IDStarget_gridSubsets =
            UG_db._edge_transport.model(UG_EdgeTransportModelID)
            .ggd(UG_ggd_slice_index).electrons.energy.v.extent(0);
        for (int n = 0; n < num_IDStarget_gridSubsets; n++)
        {
            vtkids_obj_ep_template.VTK_IDS_Val2UnstrGrid_GenericGridScalar(
                "Electron Energy - Effective Convection",
                UG,
                UG_db._edge_transport.model(UG_EdgeTransportModelID)
                    .ggd(UG_ggd_slice_index).electrons.energy.v(n),
                UG_gridSubset_index,
                UG_num_gridSubset_el);
        }


        // Assign values found in Electrons Energy - Flux array of structures
        // node to grid subsets objects
        num_IDStarget_gridSubsets =
            UG_db._edge_transport.model(UG_EdgeTransportModelID)
            .ggd(UG_ggd_slice_index).electrons.energy.flux.extent(0);
        for (int n = 0; n < num_IDStarget_gridSubsets; n++)
        {
            vtkids_obj_ep_template.VTK_IDS_Val2UnstrGrid_GenericGridScalar(
                "Electron Energy - Flux",
                UG,
                UG_db._edge_transport.model(UG_EdgeTransportModelID)
                    .ggd(UG_ggd_slice_index).electrons.energy.flux(n),
                UG_gridSubset_index,
                UG_num_gridSubset_el);
        }

        // Assign values found in Electrons Energy - Flux Limiter array of
        // structures node to grid subsets objects
        num_IDStarget_gridSubsets =
            UG_db._edge_transport.model(UG_EdgeTransportModelID)
            .ggd(UG_ggd_slice_index).electrons.energy.flux_limiter.extent(0);
        for (int n = 0; n < num_IDStarget_gridSubsets; n++)
        {
            vtkids_obj_ep_template.VTK_IDS_Val2UnstrGrid_GenericGridScalar(
                "Electron Energy - Flux Limiter",
                UG,
                UG_db._edge_transport.model(UG_EdgeTransportModelID)
                    .ggd(UG_ggd_slice_index).electrons.energy.flux_limiter(n),
                UG_gridSubset_index,
                UG_num_gridSubset_el);
        }

        // Assign values found in Ion substructure to grid subsets
        // objects (2D cells)
        int num_ion_species =
            UG_db._edge_transport.model(UG_EdgeTransportModelID)
            .ggd(UG_ggd_slice_index).ion.extent(0);
        for( int k = 0; k < num_ion_species; k++)
        {
            // Set ion specie label
            std::string ion_label= UG_db._edge_transport
                .model(UG_EdgeTransportModelID).ggd(UG_ggd_slice_index)
                .ion(k).label;
            std::string ion_array_label;

            // Assign values found in Ion Particles - Effective Diffusivity (d)
            // array of structures node to grid subsets objects
            // Set data field label
            ion_array_label = vtkids_obj_ep.VTK_IDS_SetIonQuantityLabel(
                "Particles - Effective Diffusivity", k, ion_label );
            num_IDStarget_gridSubsets =
                UG_db._edge_transport.model(UG_EdgeTransportModelID)
                    .ggd(UG_ggd_slice_index).ion(k).particles.d.extent(0);
            for (int n = 0; n < num_IDStarget_gridSubsets; n++)
            {
                vtkids_obj_ep_template.VTK_IDS_Val2UnstrGrid_GenericGridScalar(
                    ion_array_label,
                    UG,
                    UG_db._edge_transport.model(UG_EdgeTransportModelID)
                        .ggd(UG_ggd_slice_index).ion(k).particles.d(n),
                    UG_gridSubset_index,
                    UG_num_gridSubset_el);
            }

            // Assign values found in Ion Particles - Effective Convection (v)
            // array of structures node to grid subsets objects
            // Set data field label
            ion_array_label = vtkids_obj_ep.VTK_IDS_SetIonQuantityLabel(
                "Particles - Effective Convection", k, ion_label );
            num_IDStarget_gridSubsets =
                UG_db._edge_transport.model(UG_EdgeTransportModelID)
                    .ggd(UG_ggd_slice_index).ion(k).particles.v.extent(0);
            for (int n = 0; n < num_IDStarget_gridSubsets; n++)
            {
                vtkids_obj_ep_template.VTK_IDS_Val2UnstrGrid_GenericGridScalar(
                    ion_array_label,
                    UG,
                    UG_db._edge_transport.model(UG_EdgeTransportModelID)
                        .ggd(UG_ggd_slice_index).ion(k).particles.v(n),
                    UG_gridSubset_index,
                    UG_num_gridSubset_el);
            }


            // Assign values found in Ion Particles - Flux array of structures
            // node to grid subsets objects
            // Set data field label
            ion_array_label = vtkids_obj_ep.VTK_IDS_SetIonQuantityLabel(
                "Particles - Flux", k, ion_label );
            num_IDStarget_gridSubsets =
                UG_db._edge_transport.model(UG_EdgeTransportModelID)
                    .ggd(UG_ggd_slice_index).ion(k).particles.flux.extent(0);
            for (int n = 0; n < num_IDStarget_gridSubsets; n++)
            {
                vtkids_obj_ep_template.VTK_IDS_Val2UnstrGrid_GenericGridScalar(
                    ion_array_label,
                    UG,
                    UG_db._edge_transport.model(UG_EdgeTransportModelID)
                        .ggd(UG_ggd_slice_index).ion(k).particles.flux(n),
                    UG_gridSubset_index,
                    UG_num_gridSubset_el);
            }

            // Assign values found in Ion Particles - Flux Limiter array of
            // structures node to grid subsets objects
            // Set data field label
            ion_array_label = vtkids_obj_ep.VTK_IDS_SetIonQuantityLabel(
                "Particles - Flux Limiter", k, ion_label );
            num_IDStarget_gridSubsets =
                UG_db._edge_transport.model(UG_EdgeTransportModelID)
                    .ggd(UG_ggd_slice_index).ion(k).particles.flux_limiter
                    .extent(0);
            for (int n = 0; n < num_IDStarget_gridSubsets; n++)
            {
                vtkids_obj_ep_template.VTK_IDS_Val2UnstrGrid_GenericGridScalar(
                    ion_array_label,
                    UG,
                    UG_db._edge_transport.model(UG_EdgeTransportModelID)
                        .ggd(UG_ggd_slice_index).ion(k).particles.flux_limiter(n),
                    UG_gridSubset_index,
                    UG_num_gridSubset_el);
            }

            // Assign values found in Ion Energy - Effective Diffusivity (d)
            // array of structures node to grid subsets objects
            // Set data field label
            ion_array_label = vtkids_obj_ep.VTK_IDS_SetIonQuantityLabel(
                "Energy - Effective Diffusivity", k, ion_label );
            num_IDStarget_gridSubsets =
                UG_db._edge_transport.model(UG_EdgeTransportModelID)
                    .ggd(UG_ggd_slice_index).ion(k).energy.d.extent(0);
            for (int n = 0; n < num_IDStarget_gridSubsets; n++)
            {
                vtkids_obj_ep_template.VTK_IDS_Val2UnstrGrid_GenericGridScalar(
                    ion_array_label,
                    UG,
                    UG_db._edge_transport.model(UG_EdgeTransportModelID)
                        .ggd(UG_ggd_slice_index).ion(k).energy.d(n),
                    UG_gridSubset_index,
                    UG_num_gridSubset_el);
            }

            // Assign values found in Ion Energy - Effective Convection (v)
            // array of structures node to grid subsets objects
            // Set data field label
            ion_array_label = vtkids_obj_ep.VTK_IDS_SetIonQuantityLabel(
                "Energy - Effective Convection", k, ion_label );
            num_IDStarget_gridSubsets =
                UG_db._edge_transport.model(UG_EdgeTransportModelID)
                    .ggd(UG_ggd_slice_index).ion(k).energy.v.extent(0);
            for (int n = 0; n < num_IDStarget_gridSubsets; n++)
            {
                vtkids_obj_ep_template.VTK_IDS_Val2UnstrGrid_GenericGridScalar(
                    ion_array_label,
                    UG,
                    UG_db._edge_transport.model(UG_EdgeTransportModelID)
                        .ggd(UG_ggd_slice_index).ion(k).energy.v(n),
                    UG_gridSubset_index,
                    UG_num_gridSubset_el);
            }


            // Assign values found in Ion Energy - Flux array of structures
            // node to grid subsets objects
            // Set data field label
            ion_array_label = vtkids_obj_ep.VTK_IDS_SetIonQuantityLabel(
                "Energy - Flux", k, ion_label );
            num_IDStarget_gridSubsets =
                UG_db._edge_transport.model(UG_EdgeTransportModelID)
                    .ggd(UG_ggd_slice_index).ion(k).energy.flux.extent(0);
            for (int n = 0; n < num_IDStarget_gridSubsets; n++)
            {
                vtkids_obj_ep_template.VTK_IDS_Val2UnstrGrid_GenericGridScalar(
                    ion_array_label,
                    UG,
                    UG_db._edge_transport.model(UG_EdgeTransportModelID)
                        .ggd(UG_ggd_slice_index).ion(k).energy.flux(n),
                    UG_gridSubset_index,
                    UG_num_gridSubset_el);
            }

            // Assign values found in Ion Energy - Flux Limiter array of
            // structures node to grid subsets objects
            // Set data field label
            ion_array_label = vtkids_obj_ep.VTK_IDS_SetIonQuantityLabel(
                "Energy - Flux Limiter ", k, ion_label );
            num_IDStarget_gridSubsets =
                UG_db._edge_transport.model(UG_EdgeTransportModelID)
                    .ggd(UG_ggd_slice_index).ion(k).energy.flux_limiter
                    .extent(0);
            for (int n = 0; n < num_IDStarget_gridSubsets; n++)
            {
                vtkids_obj_ep_template.VTK_IDS_Val2UnstrGrid_GenericGridScalar(
                    ion_array_label,
                    UG,
                    UG_db._edge_transport.model(UG_EdgeTransportModelID)
                        .ggd(UG_ggd_slice_index).ion(k).energy.flux_limiter(n),
                    UG_gridSubset_index,
                    UG_num_gridSubset_el);
            }
        }
    }

#else   // Working for IMAS modules of versions lower than 3.15.1

    // For "edge_profiles" selection in "Load IDS" text box
    if( UG_LoadIDS_string.find( "edge_profiles" ) != std::string::npos)
    {
        // Using readPsEdge function
        setAllDataFields_edge_profiles(
            UG,
            UG_db._edge_profiles.ggd(UG_ggd_slice_index),
            UG_gridSubset_index,
            UG_num_gridSubset_el);
    // For "edge_sources" selection in "Load IDS" text box
    }else if( UG_LoadIDS_string.find( "edge_sources" ) !=
        std::string::npos )
    {
        // Assigning values (2D cells)
        // Using readPsEdge function
        setAllDataFields_edge_sources(
            UG,
            UG_db._edge_sources.source(UG_EdgeSourcesSourceID).
                ggd(UG_ggd_slice_index),
            UG_gridSubset_index,
            UG_num_gridSubset_el);
    // For "edge_transport" selection in "Load IDS" text box
    }else if( UG_LoadIDS_string.find( "edge_transport" ) !=
        std::string::npos )
    {
        // Assigning values (2D cells)
        // Using readPsEdge function
        setAllDataFields_edge_transport(
            UG,
            UG_db._edge_transport.model(UG_EdgeTransportModelID).
                ggd(UG_ggd_slice_index),
            UG_gridSubset_index,
            UG_num_gridSubset_el);
    }
#endif
}


/* Main function used to fully read plasma state from the edge_profiles IDS
* and set the data properly to specified vtkUnstructuredGrid
* @param inputVtkUnstructuredGrid   Input vtkUnstructuredGrid to fill
* @param loc_ggd            \b edge_profiles_time_slice ggd IDS data structure
* @param gridSubset_index   Grid subset index of the corresponding grid subset
*                           to the vtkUnstructuredGrid
* @param num_gridSubset_el  Number of grid subset elements forming the grid
*                           subset
*/
template< typename EP1 >
void readPsEdge::setAllDataFields_edge_profiles(
    vtkSmartPointer<vtkUnstructuredGrid> inputVtkUnstructuredGrid,
    EP1 loc_ggd,
    int gridSubset_index,
    int num_gridSubset_el)
{
    VTKIDSutility vtkids_obj_ep;
    VTKIDSutilityTemplateClasses vtkids_obj_ep_template;

    // Set default value
    int num_IDStarget_gridSubsets = 0;

    // Assigning values - Electrons

    // Assign values found in Electrons Temperature array of structures node to
    // grid subsets objects
    num_IDStarget_gridSubsets = loc_ggd.electrons.temperature.extent(0);
    for (int n = 0; n < num_IDStarget_gridSubsets; n++)
    {
        vtkids_obj_ep_template.VTK_IDS_Val2UnstrGrid_GenericGridScalar(
            "Electron Temperature",
            inputVtkUnstructuredGrid,
            loc_ggd.electrons.temperature(n),
            gridSubset_index,
            num_gridSubset_el );
    }

    // Assign values found in Electrons Density array of structures node to
    // grid subsets objects
    num_IDStarget_gridSubsets = loc_ggd.electrons.density.extent(0);
    for (int n = 0; n < num_IDStarget_gridSubsets; n++)
    {
        vtkids_obj_ep_template.VTK_IDS_Val2UnstrGrid_GenericGridScalar(
            "Electron Density",
            inputVtkUnstructuredGrid,
            loc_ggd.electrons.density(n),
            gridSubset_index,
            num_gridSubset_el );
    }

    // Assign values found in Electrons Density_Fast array of structures node to
    // grid subsets objects
    num_IDStarget_gridSubsets = loc_ggd.electrons.density_fast.extent(0);
    for (int n = 0; n < num_IDStarget_gridSubsets; n++)
    {
        vtkids_obj_ep_template.VTK_IDS_Val2UnstrGrid_GenericGridScalar(
            "Electron Density_Fast",
            inputVtkUnstructuredGrid,
            loc_ggd.electrons.density_fast(n),
            gridSubset_index,
            num_gridSubset_el );
    }

    // Assign values found in Electrons Pressure array of structures node to
    // grid subsets objects
    num_IDStarget_gridSubsets = loc_ggd.electrons.pressure.extent(0);
    for (int n = 0; n < num_IDStarget_gridSubsets; n++)
    {
        vtkids_obj_ep_template.VTK_IDS_Val2UnstrGrid_GenericGridScalar(
            "Electron Pressure",
            inputVtkUnstructuredGrid,
            loc_ggd.electrons.pressure(n),
            gridSubset_index,
            num_gridSubset_el );
    }

    // Assign values found in Electrons Pressure_Fast_Perpendicular array of
    // structures node to grid subsets objects
    num_IDStarget_gridSubsets =
        loc_ggd.electrons.pressure_fast_perpendicular.extent(0);
    for (int n = 0; n < num_IDStarget_gridSubsets; n++)
    {
        vtkids_obj_ep_template.VTK_IDS_Val2UnstrGrid_GenericGridScalar(
            "Electron Pressure_Fast_Perpendicular",
            inputVtkUnstructuredGrid,
            loc_ggd.electrons.pressure_fast_perpendicular(n),
            gridSubset_index,
            num_gridSubset_el );
    }

    // Assign values found in Electrons Pressure_Fast_Parallel array of
    // structures  node to grid subsets objects
    num_IDStarget_gridSubsets =
        loc_ggd.electrons.pressure_fast_parallel.extent(0);
    for (int n = 0; n < num_IDStarget_gridSubsets; n++)
    {
        vtkids_obj_ep_template.VTK_IDS_Val2UnstrGrid_GenericGridScalar(
            "Electron Pressure_Fast_Parallel",
            inputVtkUnstructuredGrid,
            loc_ggd.electrons.pressure_fast_parallel(n),
            gridSubset_index,
            num_gridSubset_el );
    }

    // In IMAS 3.15.0 and older versions the .velocity IDS data structure is
    // simple structure node, while in 3.6.4 it was changed to array
    // of structures node
#if IMAS_VERSION_DIGIT >= 3150
    // Reading Electron velocity ( GenericGridVectorComponents data structure
    // type )
    num_IDStarget_gridSubsets = loc_ggd.electrons.velocity.extent(0);
    // Assign values found in Electrons Velocity array of structures
    // node - Radial simple structure node to grid subsets objects
    for (int n = 0; n < num_IDStarget_gridSubsets; n++)
    {
        vtkids_obj_ep_template.VTK_IDS_Val2UnstrGrid_GenericGridVectorComponents(
            "Electron Velocity - Radial",
            inputVtkUnstructuredGrid,
            loc_ggd.electrons.velocity(n),
            "radial",
            gridSubset_index,
            num_gridSubset_el );
    }

    // Assign values found in Electrons Velocity array of structures
    // node - Diamagnetic simple structure node to grid subsets objects
    for (int n = 0; n < num_IDStarget_gridSubsets; n++)
    {
        vtkids_obj_ep_template.VTK_IDS_Val2UnstrGrid_GenericGridVectorComponents(
            "Electron Velocity - Diamagnetic",
            inputVtkUnstructuredGrid,
            loc_ggd.electrons.velocity(n),
            "diamagnetic",
            gridSubset_index,
            num_gridSubset_el );
    }

    // Assign values found in Electrons Velocity array of structures
    // node - Parallel simple structure node to grid subsets objects
    for (int n = 0; n < num_IDStarget_gridSubsets; n++)
    {
        vtkids_obj_ep_template.VTK_IDS_Val2UnstrGrid_GenericGridVectorComponents(
            "Electron Velocity - Parallel",
            inputVtkUnstructuredGrid,
            loc_ggd.electrons.velocity(n),
            "parallel",
            gridSubset_index,
            num_gridSubset_el );
    }

    // Assign values found in Electrons Velocity array of structures
    // node - Poloidal simple structure node to grid subsets objects
    for (int n = 0; n < num_IDStarget_gridSubsets; n++)
    {
        vtkids_obj_ep_template.VTK_IDS_Val2UnstrGrid_GenericGridVectorComponents(
            "Electron Velocity - Poloidal",
            inputVtkUnstructuredGrid,
            loc_ggd.electrons.velocity(n),
            "poloidal",
            gridSubset_index,
            num_gridSubset_el );
    }

    // Assign values found in Electrons Velocity array of structures
    // node - Toroidal simple structure node to grid subsets objects
    for (int n = 0; n < num_IDStarget_gridSubsets; n++)
    {
        vtkids_obj_ep_template.VTK_IDS_Val2UnstrGrid_GenericGridVectorComponents(
            "Electron Velocity - Toroidal",
            inputVtkUnstructuredGrid,
            loc_ggd.electrons.velocity(n),
            "toroidal",
            gridSubset_index,
            num_gridSubset_el );
    }
#endif

    // Assign values found in Electrons Distribution Function array of structures
    // node to grid subsets objects
    num_IDStarget_gridSubsets =
        loc_ggd.electrons.distribution_function.extent(0);
    for (int n = 0; n < num_IDStarget_gridSubsets; n++)
    {
        vtkids_obj_ep_template.VTK_IDS_Val2UnstrGrid_GenericGridScalar(
            "Electron Distribution Function",
            inputVtkUnstructuredGrid,
            loc_ggd.electrons.distribution_function(n),
            gridSubset_index,
            num_gridSubset_el );
    }

    // Assign values found in Ion substructure to grid subsets
    // objects (2D cells)
    int num_ion_species = loc_ggd.ion.extent(0);
    for( int k = 0; k < num_ion_species; k++)
    {
        // Set ion specie label
        std::string ion_label= loc_ggd.ion(k).label;
        std::string ion_array_label;

        // Assign values found in Ion Temperature array of structures
        // node to grid subsets objects
        // Set data field label
        ion_array_label = vtkids_obj_ep.VTK_IDS_SetIonQuantityLabel(
            "Temperature", k, ion_label );
        num_IDStarget_gridSubsets =
            loc_ggd.ion(k).temperature.extent(0);
        for (int n = 0; n < num_IDStarget_gridSubsets; n++)
        {
            vtkids_obj_ep_template.VTK_IDS_Val2UnstrGrid_GenericGridScalar(
                ion_array_label,
                inputVtkUnstructuredGrid,
                loc_ggd.ion(k).temperature(n),
                gridSubset_index,
                num_gridSubset_el );
        }

        // Assign values found in Ion Density array of structures
        // node to grid subsets objects
        // Set data field label
        ion_array_label = vtkids_obj_ep.VTK_IDS_SetIonQuantityLabel(
            "Density", k, ion_label );
        num_IDStarget_gridSubsets =
            loc_ggd.ion(k).density.extent(0);
        for (int n = 0; n < num_IDStarget_gridSubsets; n++)
        {
            vtkids_obj_ep_template.VTK_IDS_Val2UnstrGrid_GenericGridScalar(
                ion_array_label,
                inputVtkUnstructuredGrid,
                loc_ggd.ion(k).density(n),
                gridSubset_index,
                num_gridSubset_el );
        }

        // Assign values found in Ion Density_Fast array of structures
        // node to grid subsets objects
        // Set data field label
        ion_array_label = vtkids_obj_ep.VTK_IDS_SetIonQuantityLabel(
            "Density_Fast", k, ion_label );
        num_IDStarget_gridSubsets =
            loc_ggd.ion(k).density_fast.extent(0);
        for (int n = 0; n < num_IDStarget_gridSubsets; n++)
        {
            vtkids_obj_ep_template.VTK_IDS_Val2UnstrGrid_GenericGridScalar(
                ion_array_label,
                inputVtkUnstructuredGrid,
                loc_ggd.ion(k).density_fast(n),
                gridSubset_index,
                num_gridSubset_el );
        }

        // Assign values found in Ion Pressure array of structures
        // node to grid subsets objects
        // Set data field label
        ion_array_label = vtkids_obj_ep.VTK_IDS_SetIonQuantityLabel(
            "Pressure", k, ion_label );
        num_IDStarget_gridSubsets =
            loc_ggd.ion(k).pressure.extent(0);
        for (int n = 0; n < num_IDStarget_gridSubsets; n++)
        {
            vtkids_obj_ep_template.VTK_IDS_Val2UnstrGrid_GenericGridScalar(
                ion_array_label,
                inputVtkUnstructuredGrid,
                loc_ggd.ion(k).pressure(n),
                gridSubset_index,
                num_gridSubset_el );
        }

        // Assign values found in Ion Pressure - Fast Perpendicular array of
        // structures node to grid subsets objects
        // Set data field label
        ion_array_label = vtkids_obj_ep.VTK_IDS_SetIonQuantityLabel(
            "Pressure - Fast Perpendicular", k, ion_label );
        num_IDStarget_gridSubsets =
            loc_ggd.ion(k).pressure_fast_perpendicular.extent(0);
        for (int n = 0; n < num_IDStarget_gridSubsets; n++)
        {
            vtkids_obj_ep_template.VTK_IDS_Val2UnstrGrid_GenericGridScalar(
                ion_array_label,
                inputVtkUnstructuredGrid,
                loc_ggd.ion(k).pressure_fast_perpendicular(n),
                gridSubset_index,
                num_gridSubset_el );
        }

        // Assign values found in Ion Pressure - Fast Parallel array of
        // structures node to grid subsets objects
        // Set data field label
        ion_array_label = vtkids_obj_ep.VTK_IDS_SetIonQuantityLabel(
            "Pressure - Fast Parallel", k, ion_label );
        num_IDStarget_gridSubsets =
            loc_ggd.ion(k).pressure_fast_parallel.extent(0);
        for (int n = 0; n < num_IDStarget_gridSubsets; n++)
        {
            vtkids_obj_ep_template.VTK_IDS_Val2UnstrGrid_GenericGridScalar(
                ion_array_label,
                inputVtkUnstructuredGrid,
                loc_ggd.ion(k).pressure_fast_parallel(n),
                gridSubset_index,
                num_gridSubset_el );
        }

    // In IMAS 3.15.0 and older versions the .velocity IDS data structure is
    // simple structure node, while in 3.6.4 it was changed to array
    // of structures node
#if IMAS_VERSION_DIGIT >= 3150
        // Reading Ion velocity ( GenericGridVectorComponents data structure
        // type )
        num_IDStarget_gridSubsets = loc_ggd.ion(k).velocity.extent(0);
        // Assign values found in Ion Velocity array of structures
        // node - Radial simple structure node to grid subsets objects
        // Set data field label
        ion_array_label = vtkids_obj_ep.VTK_IDS_SetIonQuantityLabel(
            "Velocity - Radial", k, ion_label );
        for (int n = 0; n < num_IDStarget_gridSubsets; n++)
        {
            vtkids_obj_ep_template.VTK_IDS_Val2UnstrGrid_GenericGridVectorComponents(
                ion_array_label,
                inputVtkUnstructuredGrid,
                loc_ggd.ion(k).velocity(n),
                "radial",
                gridSubset_index,
                num_gridSubset_el );
        }

        // Assign values found in Ion Velocity array of structures
        // node - Diamagnetic simple structure node to grid subsets objects
        // Set data field label
        ion_array_label = vtkids_obj_ep.VTK_IDS_SetIonQuantityLabel(
            "Velocity - Diamagnetic", k, ion_label );
        for (int n = 0; n < num_IDStarget_gridSubsets; n++)
        {
            vtkids_obj_ep_template.VTK_IDS_Val2UnstrGrid_GenericGridVectorComponents(
                ion_array_label,
                inputVtkUnstructuredGrid,
                loc_ggd.ion(k).velocity(n),
                "diamagnetic",
                gridSubset_index,
                num_gridSubset_el );
        }

        // Assign values found in Ion Velocity array of structures
        // node - Parallel simple structure node to grid subsets objects
        // Set data field label
        ion_array_label = vtkids_obj_ep.VTK_IDS_SetIonQuantityLabel(
            "Velocity - Parallel", k, ion_label );
        for (int n = 0; n < num_IDStarget_gridSubsets; n++)
        {
            vtkids_obj_ep_template.VTK_IDS_Val2UnstrGrid_GenericGridVectorComponents(
                ion_array_label,
                inputVtkUnstructuredGrid,
                loc_ggd.ion(k).velocity(n),
                "parallel",
                gridSubset_index,
                num_gridSubset_el );
        }

        // Assign values found in Ion Velocity array of structures
        // node - Poloidal simple structure node to grid subsets objects
        // Set data field label
        ion_array_label = vtkids_obj_ep.VTK_IDS_SetIonQuantityLabel(
            "Velocity - Poloidal", k, ion_label );
        for (int n = 0; n < num_IDStarget_gridSubsets; n++)
        {
            vtkids_obj_ep_template.VTK_IDS_Val2UnstrGrid_GenericGridVectorComponents(
                ion_array_label,
                inputVtkUnstructuredGrid,
                loc_ggd.ion(k).velocity(n),
                "poloidal",
                gridSubset_index,
                num_gridSubset_el );
        }

        // Assign values found in Ion Velocity array of structures
        // node - Toroidal simple structure node to grid subsets objects
        // Set data field label
        ion_array_label = vtkids_obj_ep.VTK_IDS_SetIonQuantityLabel(
            "Velocity - Toroidal", k, ion_label );
        for (int n = 0; n < num_IDStarget_gridSubsets; n++)
        {
            vtkids_obj_ep_template.VTK_IDS_Val2UnstrGrid_GenericGridVectorComponents(
                ion_array_label,
                inputVtkUnstructuredGrid,
                loc_ggd.ion(k).velocity(n),
                "toroidal",
                gridSubset_index,
                num_gridSubset_el );
        }
#endif

        // Assign values found in Ion Energy Density Kinetic array of structures
        // node to grid subsets objects
        // Set data field label
        ion_array_label = vtkids_obj_ep.VTK_IDS_SetIonQuantityLabel(
            "Energy Density Kinetic", k, ion_label );
        num_IDStarget_gridSubsets =
            loc_ggd.ion(k).energy_density_kinetic.extent(0);
        for (int n = 0; n < num_IDStarget_gridSubsets; n++)
        {
            vtkids_obj_ep_template.VTK_IDS_Val2UnstrGrid_GenericGridScalar(
                ion_array_label,
                inputVtkUnstructuredGrid,
                loc_ggd.ion(k).energy_density_kinetic(n),
                gridSubset_index,
                num_gridSubset_el );
        }
    }
}

/* Main function used to fully read plasma state from the edge_sources IDS
* and set the data properly to specified vtkUnstructuredGrid
* @param inputVtkUnstructuredGrid   Input vtkUnstructuredGrid to fill
* @param loc_ggd            \b edge_profiles_time_slice ggd IDS data structure
* @param gridSubset_index   Grid subset index of the corresponding grid subset
*                           to the vtkUnstructuredGrid
* @param num_gridSubset_el  Number of grid subset elements forming the grid
*                           subset
*/
template< typename ES1 >
void readPsEdge::setAllDataFields_edge_sources(
    vtkSmartPointer<vtkUnstructuredGrid> inputVtkUnstructuredGrid,
    ES1 loc_ggd,
    int gridSubset_index,
    int num_gridSubset_el)
{
    VTKIDSutility vtkids_obj_ep;
    VTKIDSutilityTemplateClasses vtkids_obj_ep_template;

    // Set default value
    int num_IDStarget_gridSubsets = 0;

    // Assigning values - Electrons

    // Assign values found in Electrons Particles array of structures node to
    // grid subsets objects
    num_IDStarget_gridSubsets = loc_ggd.electrons.particles.extent(0);
    for (int n = 0; n < num_IDStarget_gridSubsets; n++)
    {
        vtkids_obj_ep_template.VTK_IDS_Val2UnstrGrid_GenericGridScalar(
            "Electron Particles",
            inputVtkUnstructuredGrid,
            loc_ggd.electrons.particles(n),
            gridSubset_index,
            num_gridSubset_el );
    }

    // Assign values found in Electrons Energy array of structures node to
    // grid subsets objects
    num_IDStarget_gridSubsets = loc_ggd.electrons.energy.extent(0);
    for (int n = 0; n < num_IDStarget_gridSubsets; n++)
    {
        vtkids_obj_ep_template.VTK_IDS_Val2UnstrGrid_GenericGridScalar(
            "Electron Energy",
            inputVtkUnstructuredGrid,
            loc_ggd.electrons.energy(n),
            gridSubset_index,
            num_gridSubset_el );
    }

    // Assign values found in Ion substructure to grid subsets
    // objects (2D cells)
    int num_ion_species = loc_ggd.ion.extent(0);
    for( int k = 0; k < num_ion_species; k++)
    {
        // Set ion specie label
        std::string ion_label= loc_ggd.ion(k).label;
        std::string ion_array_label;

        // Assign values found in Ion Particles array of structures
        // node to grid subsets objects
        // Set data field label
        ion_array_label = vtkids_obj_ep.VTK_IDS_SetIonQuantityLabel(
            "Particles", k, ion_label );
        num_IDStarget_gridSubsets =
            loc_ggd.ion(k).particles.extent(0);
        for (int n = 0; n < num_IDStarget_gridSubsets; n++)
        {
            vtkids_obj_ep_template.VTK_IDS_Val2UnstrGrid_GenericGridScalar(
                ion_array_label,
                inputVtkUnstructuredGrid,
                loc_ggd.ion(k).particles(n),
                gridSubset_index,
                num_gridSubset_el );
        }


        // Assign values found in Ion Energy array of structures
        // node to grid subsets objects
        // Set data field label
        ion_array_label = vtkids_obj_ep.VTK_IDS_SetIonQuantityLabel(
            "Energy", k, ion_label );
        num_IDStarget_gridSubsets =
            loc_ggd.ion(k).energy.extent(0);
        for (int n = 0; n < num_IDStarget_gridSubsets; n++)
        {
            vtkids_obj_ep_template.VTK_IDS_Val2UnstrGrid_GenericGridScalar(
                ion_array_label,
                inputVtkUnstructuredGrid,
                loc_ggd.ion(k).energy(n),
                gridSubset_index,
                num_gridSubset_el );
        }
    }
}

/* Main function used to fully read plasma state from the edge_sources IDS
* and set the data properly to specified vtkUnstructuredGrid
* @param inputVtkUnstructuredGrid   Input vtkUnstructuredGrid to fill
* @param loc_ggd            \b edge_profiles_time_slice ggd IDS data structure
* @param gridSubset_index   Grid subset index of the corresponding grid subset
*                           to the vtkUnstructuredGrid
* @param num_gridSubset_el  Number of grid subset elements forming the grid
*                           subset
*/
template< typename ET1 >
void readPsEdge::setAllDataFields_edge_transport(
    vtkSmartPointer<vtkUnstructuredGrid> inputVtkUnstructuredGrid,
    ET1 loc_ggd,
    int gridSubset_index,
    int num_gridSubset_el)
{
    VTKIDSutility vtkids_obj_ep;
    VTKIDSutilityTemplateClasses vtkids_obj_ep_template;

    // Set default value
    int num_IDStarget_gridSubsets = 0;

    // Assigning values - Electrons

    // Assign values found in Electrons Particles - Effective Diffusivity (d)
    // array of structures node to grid subsets objects
    num_IDStarget_gridSubsets = loc_ggd.electrons.particles.d.extent(0);
    for (int n = 0; n < num_IDStarget_gridSubsets; n++)
    {
        vtkids_obj_ep_template.VTK_IDS_Val2UnstrGrid_GenericGridScalar(
            "Electron Particles - Effective Diffusivity",
            inputVtkUnstructuredGrid,
            loc_ggd.electrons.particles.d(n),
            gridSubset_index,
            num_gridSubset_el );
    }

    // Assign values found in Electrons Particles - Effective Convection (v)
    // array of structures node to grid subsets objects
    num_IDStarget_gridSubsets = loc_ggd.electrons.particles.v.extent(0);
    for (int n = 0; n < num_IDStarget_gridSubsets; n++)
    {
        vtkids_obj_ep_template.VTK_IDS_Val2UnstrGrid_GenericGridScalar(
            "Electron Particles - Effective Convection",
            inputVtkUnstructuredGrid,
            loc_ggd.electrons.particles.v(n),
            gridSubset_index,
            num_gridSubset_el );
    }

    // Assign values found in Electrons Particles - Flux array of structures
    // node to grid subsets objects
    num_IDStarget_gridSubsets = loc_ggd.electrons.particles.flux.extent(0);
    for (int n = 0; n < num_IDStarget_gridSubsets; n++)
    {
        vtkids_obj_ep_template.VTK_IDS_Val2UnstrGrid_GenericGridScalar(
            "Electron Particles - Flux",
            inputVtkUnstructuredGrid,
            loc_ggd.electrons.particles.flux(n),
            gridSubset_index,
            num_gridSubset_el );
    }

    // Assign values found in Electrons Particles - Flux Limiter array of
    // structures node to grid subsets objects
    num_IDStarget_gridSubsets = loc_ggd.electrons.particles.flux_limiter.extent(0);
    for (int n = 0; n < num_IDStarget_gridSubsets; n++)
    {
        vtkids_obj_ep_template.VTK_IDS_Val2UnstrGrid_GenericGridScalar(
            "Electron Particles - Flux Limiter",
            inputVtkUnstructuredGrid,
            loc_ggd.electrons.particles.flux_limiter(n),
            gridSubset_index,
            num_gridSubset_el );
    }

    // Assign values found in Electrons Energy - Effective Diffusivity (d)
    // array of structures node to grid subsets objects
    num_IDStarget_gridSubsets = loc_ggd.electrons.energy.d.extent(0);
    for (int n = 0; n < num_IDStarget_gridSubsets; n++)
    {
        vtkids_obj_ep_template.VTK_IDS_Val2UnstrGrid_GenericGridScalar(
            "Electron Energy - Effective Diffusivity",
            inputVtkUnstructuredGrid,
            loc_ggd.electrons.energy.d(n),
            gridSubset_index,
            num_gridSubset_el );
    }

    // Assign values found in Electrons Energy - Effective convection (d)
    // array of structures node to grid subsets objects
    num_IDStarget_gridSubsets = loc_ggd.electrons.energy.v.extent(0);
    for (int n = 0; n < num_IDStarget_gridSubsets; n++)
    {
        vtkids_obj_ep_template.VTK_IDS_Val2UnstrGrid_GenericGridScalar(
            "Electron Energy - Effective Convection",
            inputVtkUnstructuredGrid,
            loc_ggd.electrons.energy.v(n),
            gridSubset_index,
            num_gridSubset_el );
    }


    // Assign values found in Electrons Energy - Flux array of structures
    // node to grid subsets objects
    num_IDStarget_gridSubsets = loc_ggd.electrons.energy.flux.extent(0);
    for (int n = 0; n < num_IDStarget_gridSubsets; n++)
    {
        vtkids_obj_ep_template.VTK_IDS_Val2UnstrGrid_GenericGridScalar(
            "Electron Energy - Flux",
            inputVtkUnstructuredGrid,
            loc_ggd.electrons.energy.flux(n),
            gridSubset_index,
            num_gridSubset_el );
    }

    // Assign values found in Electrons Energy - Flux Limiter array of
    // structures node to grid subsets objects
    num_IDStarget_gridSubsets = loc_ggd.electrons.energy.flux_limiter.extent(0);
    for (int n = 0; n < num_IDStarget_gridSubsets; n++)
    {
        vtkids_obj_ep_template.VTK_IDS_Val2UnstrGrid_GenericGridScalar(
            "Electron Energy - Flux Limiter",
            inputVtkUnstructuredGrid,
            loc_ggd.electrons.energy.flux_limiter(n),
            gridSubset_index,
            num_gridSubset_el );
    }

    // Assign values found in Ion substructure to grid subsets
    // objects (2D cells)
    int num_ion_species = loc_ggd.ion.extent(0);
    for( int k = 0; k < num_ion_species; k++)
    {
        // Set ion specie label
        std::string ion_label= loc_ggd.ion(k).label;
        std::string ion_array_label;

        // Assign values found in Ion Particles - Effective Diffusivity (d)
        // array of structures node to grid subsets objects
        // Set data field label
        ion_array_label = vtkids_obj_ep.VTK_IDS_SetIonQuantityLabel(
            "Particles - Effective Diffusivity", k, ion_label );
        num_IDStarget_gridSubsets =
            loc_ggd.ion(k).particles.d.extent(0);
        for (int n = 0; n < num_IDStarget_gridSubsets; n++)
        {
            vtkids_obj_ep_template.VTK_IDS_Val2UnstrGrid_GenericGridScalar(
                ion_array_label,
                inputVtkUnstructuredGrid,
                loc_ggd.ion(k).particles.d(n),
                gridSubset_index,
                num_gridSubset_el );
        }

        // Assign values found in Ion Particles - Effective Convection (v)
        // array of structures node to grid subsets objects
        // Set data field label
        ion_array_label = vtkids_obj_ep.VTK_IDS_SetIonQuantityLabel(
            "Particles - Effective Convection", k, ion_label );
        num_IDStarget_gridSubsets =
            loc_ggd.ion(k).particles.v.extent(0);
        for (int n = 0; n < num_IDStarget_gridSubsets; n++)
        {
            vtkids_obj_ep_template.VTK_IDS_Val2UnstrGrid_GenericGridScalar(
                ion_array_label,
                inputVtkUnstructuredGrid,
                loc_ggd.ion(k).particles.v(n),
                gridSubset_index,
                num_gridSubset_el );
        }


        // Assign values found in Ion Particles - Flux array of structures
        // node to grid subsets objects
        // Set data field label
        ion_array_label = vtkids_obj_ep.VTK_IDS_SetIonQuantityLabel(
            "Particles - Flux", k, ion_label );
        num_IDStarget_gridSubsets =
            loc_ggd.ion(k).particles.flux.extent(0);
        for (int n = 0; n < num_IDStarget_gridSubsets; n++)
        {
            vtkids_obj_ep_template.VTK_IDS_Val2UnstrGrid_GenericGridScalar(
                ion_array_label,
                inputVtkUnstructuredGrid,
                loc_ggd.ion(k).particles.flux(n),
                gridSubset_index,
                num_gridSubset_el );
        }

        // Assign values found in Ion Particles - Flux Limiter array of
        // structures node to grid subsets objects
        // Set data field label
        ion_array_label = vtkids_obj_ep.VTK_IDS_SetIonQuantityLabel(
            "Particles - Flux Limiter", k, ion_label );
        num_IDStarget_gridSubsets =
            loc_ggd.ion(k).particles.flux_limiter.extent(0);
        for (int n = 0; n < num_IDStarget_gridSubsets; n++)
        {
            vtkids_obj_ep_template.VTK_IDS_Val2UnstrGrid_GenericGridScalar(
                ion_array_label,
                inputVtkUnstructuredGrid,
                loc_ggd.ion(k).particles.flux_limiter(n),
                gridSubset_index,
                num_gridSubset_el );
        }

        // Assign values found in Ion Energy - Effective Diffusivity (d)
        // array of structures node to grid subsets objects
        // Set data field label
        ion_array_label = vtkids_obj_ep.VTK_IDS_SetIonQuantityLabel(
            "Energy - Effective Diffusivity", k, ion_label );
        num_IDStarget_gridSubsets =
            loc_ggd.ion(k).energy.d.extent(0);
        for (int n = 0; n < num_IDStarget_gridSubsets; n++)
        {
            vtkids_obj_ep_template.VTK_IDS_Val2UnstrGrid_GenericGridScalar(
                ion_array_label,
                inputVtkUnstructuredGrid,
                loc_ggd.ion(k).energy.d(n),
                gridSubset_index,
                num_gridSubset_el );
        }

        // Assign values found in Ion Energy - Effective Convection (v)
        // array of structures node to grid subsets objects
        // Set data field label
        ion_array_label = vtkids_obj_ep.VTK_IDS_SetIonQuantityLabel(
            "Energy - Effective Convection", k, ion_label );
        num_IDStarget_gridSubsets =
            loc_ggd.ion(k).energy.v.extent(0);
        for (int n = 0; n < num_IDStarget_gridSubsets; n++)
        {
            vtkids_obj_ep_template.VTK_IDS_Val2UnstrGrid_GenericGridScalar(
                ion_array_label,
                inputVtkUnstructuredGrid,
                loc_ggd.ion(k).energy.v(n),
                gridSubset_index,
                num_gridSubset_el );
        }


        // Assign values found in Ion Energy - Flux array of structures
        // node to grid subsets objects
        // Set data field label
        ion_array_label = vtkids_obj_ep.VTK_IDS_SetIonQuantityLabel(
            "Energy - Flux", k, ion_label );
        num_IDStarget_gridSubsets =
            loc_ggd.ion(k).energy.flux.extent(0);
        for (int n = 0; n < num_IDStarget_gridSubsets; n++)
        {
            vtkids_obj_ep_template.VTK_IDS_Val2UnstrGrid_GenericGridScalar(
                ion_array_label,
                inputVtkUnstructuredGrid,
                loc_ggd.ion(k).energy.flux(n),
                gridSubset_index,
                num_gridSubset_el );
        }

        // Assign values found in Ion Energy - Flux Limiter array of structures
        // node to grid subsets objects
        // Set data field label
        ion_array_label = vtkids_obj_ep.VTK_IDS_SetIonQuantityLabel(
            "Energy - Flux Limiter ", k, ion_label );
        num_IDStarget_gridSubsets =
            loc_ggd.ion(k).energy.flux_limiter.extent(0);
        for (int n = 0; n < num_IDStarget_gridSubsets; n++)
        {
            vtkids_obj_ep_template.VTK_IDS_Val2UnstrGrid_GenericGridScalar(
                ion_array_label,
                inputVtkUnstructuredGrid,
                loc_ggd.ion(k).energy.flux_limiter(n),
                gridSubset_index,
                num_gridSubset_el );
        }
    }
}
