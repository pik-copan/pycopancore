Python implementation
=====================

This section describes how the computer software described in the :doc:`../software_design/index` is currently
implemented in the Python programming language.
For a detailed reference of the resulting Python package pycopancore, see :doc:`../../api_reference`.

Because it allows a comfortable mix of object-oriented and imperative programming,
is well-established in many scientific communities
and provides powerful tools for statistical analysis and data management and exchange,
we chose to implement the software in the standard **Python** programming language, using the current grammar version 3,
with the option to port it later to other Python variants like *Cython* or to other object-oriented languages such as C++ or Java.


Typographic conventions
-----------------------

In this documentation, ``<text in this kind of brackets>`` is always a placeholder,
e.g., ``<variable name>`` is a placeholder for a variable name.


Main package structure
----------------------

::

   pycopancore

      data_model
         master_data_model
            cell.py
            society.py
            individual.py
            nature.py
            social_metabolism.py
            culture.py
            ...
         dimensions.py
         dimensional_quantity.py
         variable.py
         ...

      model_components
         <component name>
            implementation
               cell.py
               society.py
               individual.py
               nature.py
               social_metabolism.py
               culture.py
            interface.py
            model.py
            ...
         <other component name>
            ...
         ...
         _template

      models
         <my_model>.py

      private
         _abstract_process.py
         _abstract_runner.py
         _abstract_entity_mixin.py
         _expressions.py
         ...

      process_types
         ODE.py
         step.py
         explicit.py
         event.py
         implicit.py

      runners
         scipy_odeint_runner.py
         ...
      ...


.. toctree::
   :maxdepth: 1

   model_components
