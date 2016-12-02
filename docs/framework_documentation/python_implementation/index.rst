Python implementation
=====================

This section describes how the computer software described in the :doc:`../software_design/index` is currently implemented in the Python programming language.
For a detailed reference of the resulting Python package pycopancore, see :doc:`../../api_reference`.

TODO!

In this documentation, ``<text in this kind of brackets>`` is always a placeholder,
e.g., ``<variable name>`` is a placeholder for a variable name.


Package structure
-----------------


::

   pycopancore
   
      studies

      models

      model_components

         <component name>
            interface.py
            cell.py
            society.py
            individual.py
            nature.py
            social_metabolism.py
            culture.py
            ...

         <other component name>
            ...

         ...

         _template

      master_data_model
         cell.py
         society.py
         individual.py
         nature.py
         social_metabolism.py
         culture.py
         ...
         
      process_types
         ODE.py
         step.py
         explicit.py
         event.py
         ...

      runners
         scipy_odeint_runner.py
         ...

      _private
         _abstract_process_type.py
         _abstract_runner.py
         ...

      entity_type.py
      process_taxon.py
      variable.py
      ...
      

.. toctree::
   :maxdepth: 1

   model_components