Dimensions
==========

Time, events
------------

*   Time is essentially continuous



*   Some processes are represented in continuous time via differential equations



*   Some processes are represented as discontinuous
    *steps*
    or
    *events *

    *   Steps and events may happen at any time (not only on a fixed regular time grid)



    *   If a step or event happens at
        *t*
        , we distinguish between the system state at time
        *t–*
        , just before the step or event, and at time
        *t+*
        , right after the step or event



    *   The distinction between steps and events is not completely sharp. Steps are rather meant to represent either regularly occurring things (e.g., sunrise) or discretizations of actually continuous-time processes (e.g. via a difference equation) and typically involve few stochasticity, whereas events are rather meant to represent irregularly occurring things (e.g. birth or death of a node, link, or coalition, merger or split of a coalition, rewiring of a node, imitation of one agent by another, arrival of a large perturbation such as an economic crisis, etc.) and may involve a lot of stochasticity in both their timing and consequences.





Space
-----

Spatial resolution
~~~~~~~~~~~~~~~~~~

*   Space is essentially continuous



*   Basic space geometry is two-dimensional

    *   one periodic dimension
        *x*
        (“longitude”, going from 0 to
        360
        )



    *   one nonperiodic dimension
        *y*
        (“latitude”, going from –90 to 90)





*   Some types of model entities (e.g. humans) are located at arbitrary
    *points*




*   Some types of model entities (e.g. patches of land or ocean) are located at
    *individual grid cells*
    of a formally regular lon/lat
    grid



*   Some types of model entities (e.g. societies) are located at
    *connected sets of grid cells*
    called
    *territories*



Fixed spatial heterogeneity
~~~~~~~~~~~~~~~~~~~~~~~~~~~

*   Fixed aspects of spatial heterogeneity are represented by parameters or distributions at the
    *grid level*
    , all points within a grid cell are similar



*   Grid cells may (but need not) differ in

    *   area
        (constant in the first version, but may depend on latitude in later versions when Earth system submodels are coupled)



    *   type of terrain
        (initially all is land, later some cells may be ocean, even later distinctions like plain/mountainous etc may be made)



    *   solar insolation (
        initially constant
        )



    *   basic soil quality



    *   Potential biomass productivity



    *   basic availability of fossil resources and water (if hydrology is deemed essential)



    *   surface temperature





Other physical dimensions
-------------------------

(Not to be confused with individual variables. They are listed later!)


Each variable will have an explicit physical dimension and unit in order to facilitate

*   estimation of parameters and initial conditions from data



*   comparison of results with data



*   later coupling to other models




Basic dimensions (and units) that will probably occur are

*   Human population (discrete, humans)



*   Carbon (gigatons)



*   Energy (gigajoules)



*   Power: energy / time (gigajoules / s)



*   Temperature



*   Money (
    time-independent “coins”? “unskilled working hours”?
    )



*   Produced goods
    / Capital
    (
    nevertheless in monetary units to make aggregation possible
    )



*   Utility/wellbeing (not to be confused with money, unit “utils”)


