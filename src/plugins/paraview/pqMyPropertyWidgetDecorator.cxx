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
#include "pqMyPropertyWidgetDecorator.h"

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
pqMyPropertyWidgetDecorator::pqMyPropertyWidgetDecorator(
    vtkPVXMLElement* config, pqPropertyWidget* parentObject)
    : Superclass(config, parentObject)
{
    vtkSMProxy* proxy = parentObject->proxy();
    vtkSMProperty* prop = proxy? proxy->GetProperty("CPOLoad") : NULL;
    if (!prop)
    {
        qDebug("Could not locate property named 'CPOLoad'. "
        "pqMyPropertyWidgetDecorator will have no effect.");
        return;
    }

    this->ObservedObject = prop;
    this->ObserverId = pqCoreUtilities::connect(
        prop, vtkCommand::UncheckedPropertyModifiedEvent,
        this, SIGNAL(visibilityChanged()));

    vtkSMProperty* prop_user = proxy? proxy->GetProperty("User") : NULL;
    this->ObserverId = pqCoreUtilities::connect(
        prop_user, vtkCommand::UncheckedPropertyModifiedEvent,
        this, SIGNAL(visibilityChanged()));


    vtkSMProperty* prop_list = proxy? proxy->GetProperty("ShotRunList") : NULL;
}

//-----------------------------------------------------------------------------
pqMyPropertyWidgetDecorator::~pqMyPropertyWidgetDecorator()
{
    if (this->ObservedObject && this->ObserverId)
    {
        this->ObservedObject->RemoveObserver(this->ObserverId);
    }
}

//-----------------------------------------------------------------------------
bool pqMyPropertyWidgetDecorator::canShowWidget(bool show_advanced) const
{
    pqPropertyWidget* parentObject = this->parentWidget();
    vtkSMProxy* proxy = parentObject->proxy();
    vtkSMProperty* prop = proxy? proxy->GetProperty("CPOLoad") : NULL;
    if (prop)
    {
        double value = vtkSMUncheckedPropertyHelper(prop).GetAsInt();
        if (value ==0)
        {
            return false;
        }
    }

    // Extracting available Shot/Runs from the user, defined in the 
    // "User" text box, and adding them to the Shot/Run list 
    vtkSMProperty* prop_user = proxy? proxy->GetProperty("User") : NULL;
    vtkSMStringVectorProperty* prop_user_strVec = 
        dynamic_cast<vtkSMStringVectorProperty*>(proxy->GetProperty("User"));
    std::vector<std::string> UserShotRunList;

    vtkSMProperty* prop_list = proxy? proxy->GetProperty("ShotRunList") : NULL;

    const char *user;
    if(prop_user)
    {
        // Getting text currently in"User" checkbox to string
        std::clog << "---prop_user Printself---: " << std::endl;
        prop_user->PrintSelf(std::clog, vtkIndent());
        user = vtkSMUncheckedPropertyHelper(prop_user).GetAsString();
    }
    if(prop_list)
    {
        // Getting text currently in"User" checkbox to string
        std::clog << "---prop_list Printself---: " << std::endl;
        prop_list->PrintSelf(std::clog, vtkIndent());
    }

    // Getting the users $HOME directory 
    std::string cmd = "echo ~" + string(user);
    char buffer[128];
    std::string homedir = "";
    FILE* pipe = popen(cmd.c_str(), "r");

    if (!pipe) std::clog << "popen() failed!" << std::endl;
    try
    {
        while (!feof(pipe)) 
        {
            if (fgets(buffer, 128, pipe) != NULL)
                homedir += buffer;
        }
    } catch (...)
    {
        pclose(pipe);
        throw;
    }
    pclose(pipe);

    // Example of userIMASShotRunDir: 
    // /home/ITER/penkod/public/imasdb/solps-iter/3/0
    std::string userIMASShotRunDir = homedir + "/public/imasdb/solps-iter/3/0";
    userIMASShotRunDir.erase(std::remove(userIMASShotRunDir.begin(), 
        userIMASShotRunDir.end(), '\n'), userIMASShotRunDir.end());
    UserShotRunList = findShotRun(userIMASShotRunDir, string(user));

    vtkSMProperty* prop_SHlist = proxy? proxy->GetProperty(
        "ShotRunList") : NULL;
    if (!prop_SHlist)
    {
        qDebug("Could not locate property named 'ShotRunList'. "
        "pqMyPropertyWidgetDecorator will have no effect.");
    } 
    else if (prop_SHlist)
    {
        vtkSMStringVectorProperty* prop_SHlist_strVec = 
            dynamic_cast<vtkSMStringVectorProperty*>(proxy->GetProperty(
            "ShotRunList"));
        for(int i = 0; i < UserShotRunList.size(); i++)
        {
            // Filling the Shot/Run List
            prop_SHlist_strVec->SetElement(i, UserShotRunList[i].c_str());
        }
        proxy->UpdatePropertyInformation(prop_SHlist_strVec);
        proxy->UpdateSelfAndAllInputs();
    }
    return this->Superclass::canShowWidget(show_advanced);
}
