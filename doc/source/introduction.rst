.. _introduction:

..  topic:: Abstract

    by *Xavier Bonnin* and *Richard Pitts*

    The design of the ITER divertor and estimates of the required fuelling
    throughput have relied for many years on simulations performed by use of
    the SOLPS plasma edge modelling tool, more specifically its versions 4.0,
    4.2 and 4.3. However, the SOLPS code base has been developed independently
    by other research groups among the ITER Members’ institutions, most notably
    in IPP-Garching (EU) and St. Petersburg (RF), leading ultimately to
    versions SOLPS5.0/5.1 and SOLPS5.2, respectively.

    While the developments at ITER on SOLPS4.x, in collaboration with FZ-Jülich
    (EU), have focused mainly on the physics of neutral transport, the work
    done in Garching has been devoted mostly to improving the physics
    capabilities of the plasma model and the St. Petersburg efforts have
    concentrated on improving the numerical solution of the drift terms and
    the electric potential equation. These various enhancements have now
    reached some maturity and it was decided at the IO in 2012 to devote
    resources to merging back these three code versions into a single package
    that would bring together all the advances from those branches of
    development. This began with a first Task Agreement between IO
    and F4E to couple the newest versions of the two main components of the
    SOLPS package (separate plasma fluid and neutral transport codes) to yield
    a new code version, named SOLPS-ITER. Subsequently, additional effort has
    been devoted to adding further refinements present in the various
    previous versions which were not all captured in the initial coupling
    exercise. The new code was released to the R&D community at a workshop
    organized at the ITER Headquarters on April 13th-17th, 2015.

    The ambition of the SOLPS-ITER effort is to make this last code version
    become the new standard used across the ITER Parties for modelling not
    only ITER, but any other tokamaks and linear plasma devices wherever
    applicable.
    In order to facilitate user adoption of SOLPS-ITER and migration from
    earlier versions, it has therefore been decided to include as part of
    the SOLPS- ITER package, a more user-friendly interface for some of the
    more tedious and error-prone tasks to ease the transition for users of
    older versions and provide additional added value and incentive for those
    switching to SOLPS-ITER. At the same time, SOLPS users, including those
    at the IO, have, over the years, expressed the desire for some
    run monitoring framework and more powerful graphical post-processing tools.
    The aim of Graphical User Interface (GUI) is to provide the software
    constituting this interface.

    The SOLPS GUI adds to the current SOLPS-ITER code suite a framework
    consisting of various tools aiming at improving the user’s experience,
    to accelerate and simplify run input set-up, and to increase the scientific
    usability of the *B2.5-Eirene* simulation results.

============
Introduction
============

The SOLPS GUI is a framework tailored specifically for SOLPS-ITER code
suite in a sense that code specifics are built-in the interface. Its design
allows users to extend functionality by coupling custom widgets prepared
for the SOLPS GUI. These custom widgets are in similar environments called
*actors* as they do act on some data depending on input received
and then they pass results further in a scientific workflow. Custom widgets
for SOLPS are operating in a similar fashion in a way that they receive and
send the signals to other widgets for further operation. In principle, no
programming is needed by users to create their own *Dashboard* for analysing
and controlling the SOLPS simulations. Graphical workflow "design" is done
with `Qt designer <http://doc.qt.io/qt-5/qtdesigner-manual.html>`_.
In contrast to scientific workflow engines such as
`Kepler <https://kepler-project.org>`_ here we are more oriented to
look-and-feel experience than to create a general purpose workflow engine.
That's why the widgets in SOLPS GUI are concentrated to have "nice"
input and output presentation while we don't care how "nicely" wires are
placed. "Wiring" is usually taking significant space in other workflow
engines where *actors* are "small" or unified size with separated or neglected
display output. SOLPS GUI is having vice-versa approach with widgets filling
up available *Dashboard* completely. There can be many widgets that trigger
part of the workflow, whereas there is just *play* used in *Kepler*.
SOLPS GUI **signal/slot** philosophy provided by
`Qt framework <http://www.qt.io/qt-framework/>`_ is similar to
input/output ports in *Kepler*, while the triggering is more explicit than
implicit. This means that it is usually just one trigger needed to start the
action with the assumption that all needed signals describing the action
already arrived beforehand.

Users are therefore encouraged to design their own *Dashboard* by redesigning
it to suit their needs. As the *Dashboard* is intended to be configured with
*Qt designer* this means that all action needs to be provided within the
widgets connected by signals. "Wiring" can be graphical too. GUI
is then saved in XML files and compiled on-the-fly at the GUI startup. Even
if providing limited set of "custom" widgets there can exist many different
*Dashboards* for running SOLPS simulations. The may differ on the analysis,
user's preference and maybe exchanged for reuse by others. Nice thing with
such *graphical programming* is not just adding functionality easily
but one can simply remove the unwanted custom widgets too.