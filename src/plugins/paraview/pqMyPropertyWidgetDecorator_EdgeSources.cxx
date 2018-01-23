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
* This source file specifies the behaviour of the EdgeSourcesSource widget
* in relation to the LoadIDS widget.
*/

#include "pqMyPropertyWidgetDecorator_EdgeSources.h"
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
pqMyPropertyWidgetDecorator_EdgeSources::pqMyPropertyWidgetDecorator_EdgeSources(
    vtkPVXMLElement* config, pqPropertyWidget* parentObject)
    : Superclass(config, parentObject)
{
    vtkSMProxy* proxy = parentObject->proxy();
    vtkSMProperty* prop_IDSLoad = proxy? proxy->GetProperty("LoadIDS") : NULL;
    if (!prop_IDSLoad)
    {
        qDebug("Could not locate property named 'LoadIDS'. "
        "pqMyPropertyWidgetDecorator_EdgeSources will have no effect.");
        return;
    }

    this->ObservedObject = prop_IDSLoad;
    this->ObserverId = pqCoreUtilities::connect(
        prop_IDSLoad, vtkCommand::UncheckedPropertyModifiedEvent,
        this, SIGNAL(visibilityChanged()));
}

//-----------------------------------------------------------------------------
pqMyPropertyWidgetDecorator_EdgeSources::
    ~pqMyPropertyWidgetDecorator_EdgeSources()
{
    if (this->ObservedObject && this->ObserverId)
    {
        this->ObservedObject->RemoveObserver(this->ObserverId);
    }
}

//-----------------------------------------------------------------------------
bool pqMyPropertyWidgetDecorator_EdgeSources::
    canShowWidget( bool show_advanced ) const
{
    pqPropertyWidget* parentObject = this->parentWidget();
    vtkSMProxy* proxy = parentObject->proxy();
    vtkSMProperty* prop_IDSLoad = proxy? proxy->GetProperty("LoadIDS") : NULL;

    if (prop_IDSLoad)
    {
        const char* ids_value =
            vtkSMUncheckedPropertyHelper(prop_IDSLoad).GetAsString();
        if (std::string(ids_value).find( "edge_sources" ) == std::string::npos)
        {
            return false;
        }
    }

    vtkSMProperty* prop_EdgeSourcesSource =
        proxy? proxy->GetProperty("EdgeSourcesSource") : NULL;
    vtkSMStringVectorProperty* prop_EdgeSourcesSource_strVec =
        dynamic_cast<vtkSMStringVectorProperty*>(proxy->
        GetProperty("EdgeSourcesSource"));

    int EdgeSources_source_int;
    if (prop_EdgeSourcesSource)
    {
        // Getting integer currently in"EdgeSourcesSource" checkbox to string
        // std::clog << "---prop_EdgeSourcesSource Printself---: " << std::endl;
        // prop_EdgeSourcesSource->PrintSelf(std::clog, vtkIndent());
        EdgeSources_source_int =
            vtkSMPropertyHelper(prop_EdgeSourcesSource).GetAsInt();
    }
    if (prop_IDSLoad)
    {
        // Getting text currently in"User" checkbox to string
        // std::clog << "---prop_IDSLoad Printself---: " << std::endl;
        // prop_IDSLoad->PrintSelf(std::clog, vtkIndent());
    }
    return this->Superclass::canShowWidget(show_advanced);
}
