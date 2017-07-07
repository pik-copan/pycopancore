Step by step tutorial
=====================

The following instructive step by step tutorial will guide the reader from
a starting point, a fairy tale, to the conception of a model component, its
implementation and the building of a operational model.

Starting point: a fairy tale
----------------------------
Once upon a time in a place far away seven dwarfs lived together in a cave.
Winter had come and they could not leave their cave to collect food. They grew
older and were to die, either from age or from hunger.

Their beards grew longer and the only thing giving them a glimpse of hope in
their pitiful lives was an old story of a beautiful princess that would arrive
some day and save them from their misery. When Snow White finally arrived they
discovered she tricked them, ate half of their food supplies and left them
to die.

Entities and process taxa
-------------------------
In order to conceptualize a model from this story, we follow the procedure
described in :doc:`model component developers <./model_component_developers>`,
:doc:`model composers <./model_composers>`, and
:doc:`model end users <./model_end_users>`.

At first, we identify the necessary entities and process taxa. We model the
seven dwarfs as ``Individuals`` in the CORE:framework, because they are
well-distinguishable entities which possess attributes as age, beard length etc.
We model the cave as a ``Cell``. In our model component, we neither need the
``Culture`` nor the ``Social Metabolism`` nor the ``Nature`` taxon. This also
applies to the ``Society`` entity.

The CORE:framework is modular in the sense that various model components can be
combined. Hence, we can use classes of the ``base`` package, as we will later
do when using the ``Culture`` class of the ``base`` package.

We will continue by investigating the processes that determine our model.

Processes
---------
There are various ways to start conceptualizing and implementing our model.
In this tutorial we start by considering the processes involved in our fairy
tale . There are four of them (which for the instructiveness of this tutorial
are the :doc:`four processes <../framework_documentation/process_types_index>`
provided by the CORE:framework):

- Aging, a ``Step`` process
- Eating, an ``ODE`` process
- Beard growing, an ``Explicit`` process
- Snow White arrival, an ``Event`` process

These four processes completely determine the dynamics of the model for our
story. It makes sense to assign the first three processes (aging, eating and
beard growing) to each dwarf (``Individual``).

Although aging is a continuous process in the actual world, we think of it as
as a ``STEP`` process which changes the variable age(year). Because eating
happens more often than having birthday, we model eating as an ``ODE`` process.
Beard growing is modeled as an ...
The arrival of Snow White is modeled as an event process, because she does not
have any attributes in our story and solely changes attributes of other entities.



The aging process
-----------------
Each dwarf needs
.. Following the processes specified above, each dwarf needs the following
variables:
- age
- beard length

.. For reasons which will become clear later, each dwarf also needs:
- beard growth parameter and
- eating parameter

Thus, the instantiation method of ``Individual`` looks like this:

::

    def __init__(self,
                 *,
                 age = 0,
                 **kwargs):
        """Initialize an instance of dwarf."""
        super().__init__(**kwargs)

        self.age = age



The dwarf's age is set to zero unless specified differently.
.. A new dwarf has a beard length of zero unless specified differently. The beard growth parameter
determines how fast the beard of the instantiated dwarf grows. The eating
parameter determines how much the dwarf eats.

Methods of dwarf:

The class ``Individual`` needs a function which will determine the aging
process. We also include dying from age, which is a Bernoulli process with
probability p = age/100.
::

    def aging(self):
        """Make dwarf have birthday."""
        self.age = self.age + 1
        if self.age/100 >= np.random.random():
            print("Dwarf died from age.")
            self.deactivate()



.. ::

..    def beard_growing(self):
        """Grow beard of dwarf in explicit manner."""
        self.beard_length = (self.beard_length
                             + self.beard_growth_parameter
                             * self.age
                             )

For a ``Step`` process, we need a timing function which returns the point of
time when the process shoulf be executed the next time:

::

    def step_timing(self, t):
        """Let one year pass."""
        return t + 1


Now, we can define the ageing process:

::

    processes = [
        Step("aging", [I.Individual.age], [step_timing, aging])
    ]




Cell's attributes and methods
-----------------------------

.. ::

..    def __init__(self,
                 *,
                 stock=100,
                 **kwargs):
        """Initialize an instance of Cell."""
        super().__init__(**kwargs)
        self.stock = stock


.. methods:

.. ::

..    def snow_white_arrival(self):
        """Calculate snow white's arrival."""
        return np.random.exponential(18.)

..    def snow_white_eating(self):
        """Party hard."""
        I.Cell.stock = I.Cell.stock / 2.

.. process:

.. ::

..    processes = [
        Event("snow_white",
              [I.Cell.stock],
              ["time", snow_white_arrival, snow_white_eating]
              )
    ]


Interface file
--------------
Why which variable?

Model file
----------
Put base and seven dwarfs together
acquaintance network needed.

Run file
--------
