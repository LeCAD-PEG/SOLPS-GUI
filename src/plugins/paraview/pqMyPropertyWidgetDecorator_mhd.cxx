/*=========================================================================

   Program: ParaView
   Module:    $RCSfile$

   Copyright (c) 2005,2006 Sandia Corporation, Kitware Inc.
   All rights reserved.

   ParaView is a free software; you can redistribute it and/or modify it
   under the terms of the ParaView license version 1.2.

   See License_v1.2.txt for the full ParaView license.
   A copy of this license can be obtained by contacting
   Kitware Inc.
   28 Corporate Drive
   Clifton Park, NY 12065
   USA

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
``AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE AUTHORS OR
CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

========================================================================*/

/*
* This source file specifies the behaviour of the mhdSourceID widget
* in relation to the LoadIDS widget.
*/

#include "pqMyPropertyWidgetDecorator_mhd.h"
#include "pqCoreUtilities.h"
#include "pqPropertyWidget.h"
#include "vtkCommand.h"
#include "vtkSMProperty.h"
#include "vtkSMProxy.h"
#include "vtkSMStringVectorProperty.h"
#include "vtkSMUncheckedPropertyHelper.h"
#include "ReadUALEdge.h"
#include "pqPropertyLinks.h"

//-----------------------------------------------------------------------------
pqMyPropertyWidgetDecorator_mhd::pqMyPropertyWidgetDecorator_mhd(
    vtkPVXMLElement* config, pqPropertyWidget* parentObject)
    : Superclass(config, parentObject)
{
    vtkSMProxy* proxy = parentObject->proxy();
    vtkSMProperty* prop_IDSLoad = proxy? proxy->GetProperty("LoadIDS") : NULL;
    if (!prop_IDSLoad)
    {
        qDebug("Could not locate property named 'LoadIDS'. "
        "pqMyPropertyWidgetDecorator_mhd will have no effect.");
        return;
    }

    this->ObservedObject1 = prop_IDSLoad;
    this->ObserverId1 = pqCoreUtilities::connect(
        prop_IDSLoad, vtkCommand::UncheckedPropertyModifiedEvent,
        this, SIGNAL(visibilityChanged()));

    vtkSMProperty* prop_IDSPlasmaStateSource =
        proxy? proxy->GetProperty("IDSPlasmaStateSource") : NULL;
    if (!prop_IDSPlasmaStateSource)
    {
        qDebug("Could not locate property named 'IDSPlasmaStateSource'. "
        "pqMyPropertyWidgetDecorator_mhd will have no effect.");
        return;
    }

    this->ObservedObject2 = prop_IDSPlasmaStateSource;
    this->ObserverId2 = pqCoreUtilities::connect(
        prop_IDSPlasmaStateSource, vtkCommand::UncheckedPropertyModifiedEvent,
        this, SIGNAL(visibilityChanged()));
}

//-----------------------------------------------------------------------------
pqMyPropertyWidgetDecorator_mhd::
    ~pqMyPropertyWidgetDecorator_mhd()
{
    if (this->ObservedObject1 && this->ObserverId1)
    {
        this->ObservedObject1->RemoveObserver(this->ObserverId1);
    }
    if (this->ObservedObject2 && this->ObserverId2)
    {
        this->ObservedObject2->RemoveObserver(this->ObserverId2);
    }
}

//-----------------------------------------------------------------------------
bool pqMyPropertyWidgetDecorator_mhd::
    canShowWidget( bool show_advanced ) const
{
    pqPropertyWidget* parentObject = this->parentWidget();
    vtkSMProxy* proxy = parentObject->proxy();
    vtkSMProperty* prop_IDSLoad = proxy? proxy->GetProperty("LoadIDS") : NULL;

    vtkSMProperty* prop_IDSPlasmaStateSource =
        proxy? proxy->GetProperty("IDSPlasmaStateSource") : NULL;

    // If 'IDSLoad' and 'IDSPlasmaStateSource' widgets are found
    if (prop_IDSLoad && prop_IDSPlasmaStateSource)
    {
        // Get value selected in the 'IDSLoad' widget
        const char* ids_value1 =
            vtkSMUncheckedPropertyHelper(prop_IDSLoad).GetAsString();
        // Get value selected in the 'IDSPlasmaStateSource' widget
        const char* ids_value2 =
            vtkSMUncheckedPropertyHelper(prop_IDSPlasmaStateSource).GetAsString();

        // If 'mhd' is found in any of the two widgets ('LoadIDS' and
        // IDSPlasmaStateSource), then proceed to show the 'mhdSourceID'
        // widget (in advanced options only)
        // Note: If the string is not found then value -1 is returned and
        // std::string::npos == -1
        if ((std::string(ids_value1).find( "mhd" ) != std::string::npos) ||
             (std::string(ids_value2).find( "mhd" ) != std::string::npos))
        {
            // Do nothing and continue the process of showing the
            // 'mhdSourceID' widget
        }else
        {
            // Return false (the widget 'mhdSourceID' won't be
            // displayed)
            return false;
        }

        vtkSMProperty* prop_mhdSourceID =
            proxy? proxy->GetProperty("mhdSourceID") : NULL;
        vtkSMStringVectorProperty* prop_mhdSourceID_strVec =
            dynamic_cast<vtkSMStringVectorProperty*>(proxy->
            GetProperty("mhdSourceID"));

        int mhd_source_int;
        if (prop_mhdSourceID)
        {
            // Getting integer currently in "mhdSourceID" checkbox
            // to string
            // std::clog << "---prop_mhdSourceID Printself---: " << std::endl;
            // prop_mhdSourceID->PrintSelf(std::clog, vtkIndent());
            mhd_source_int =
                vtkSMPropertyHelper(prop_mhdSourceID).GetAsInt();
        }
        return this->Superclass::canShowWidget(show_advanced);
    }
}
