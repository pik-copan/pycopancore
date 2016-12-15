Experiments
===========

Due to stochastic model components, experiments will generally fall into these categories:

Individual runs for specific parameters and initial conditions
--------------------------------------------------------------

*   output:

    *   sequence of event times, types, and event parameters (e.g. which node, link was active etc.)



    *   time series of all dynamic and derived model variables





Monte-Carlo simulations for specific parameters and initial conditions
----------------------------------------------------------------------

*   parameter: ensemble size



*   output: aggregate statistical information about the above, including

    *   time series and asymptotic values of

        *   means, standard deviations, skewnesses



        *   0th, 5th, 10th, 25th, 50th, 75th, 90th, 95th and 100th percentiles







Monte-Carlo simulations for specific parameters but varying initial conditions
------------------------------------------------------------------------------

*   parameters:

    *   ensemble size



    *   distribution of initial conditions





*   output: as above



*   analyses:

    *   dependence of output on initial condition



    *   Basin Stability, survivability



    *   topology of management options (method: one experiment for each essential management option)





Monte-Carlo simulations with varying parameters and initial conditions
----------------------------------------------------------------------

*   parameters:

    *   meta-ensemble size (no. of different parameter combinations)



    *   ensemble size (no. of different initial conditions)w





*   output: as above



*   analyses:

    *   dependence of output on

        *   parameters



        *   combination of parameters and initial conditions






