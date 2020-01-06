Process-type "Step"
===================

A process of type *step*
represents things that occur at singular discrete time-points
which are regularly distributed in time.

Its specification consists of two parts:

- A specification of *when* the event occurs next depending on the current model time.

- A specification of *what* happens every time the event occurs,
  including which variables are then changed in what way,
  which may also contain stochastic components.
