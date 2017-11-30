Process-type "Event"
====================

A process of type *event*
represents things that occur at singular discrete time-points
which are typically irregularly and often randomly distributed in time.

Its specification consists of two parts:

- A specification of *when* the event occurs,
  either stochastically with a constant or state- and time-dependent probability rate,
  or by specifying when it happens next depending on the current model time.

- A specification of *what* happens every time the event occurs,
  including which variables are then changed in what way,
  which may also contain stochastic components.
