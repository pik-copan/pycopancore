"""Register hooks for the run inside a runner."""

# This file is part of pycopancore.
#
# Copyright (C) 2016-2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# Contact: core@pik-potsdam.de
# License: BSD 2-clause license

#
# Imports
#
from enum import Enum, unique

#
# Specific Error Definition
#


class HookRegistrationError(BaseException):
    """Dummy docstring"""
    # TODO: missing class docstring
    pass


class HooksError(BaseException):
    """Dummy docstring"""
    # TODO: missing class docstring
    pass

#
# Definition of class _AbstractRunner
#


class Hooks(object):
    """Class managing the hooks that are called before, during and after a run."""

    # class variables
    _pre_hooks = {}
    """dict of hooks that are executed before the run

    keys: None or Entity class or Taxon class

    values: list of functions
    """
    _mid_hooks = {}
    """dict of hooks that are executed every time the run is halted for a step or an event

    keys: None or Entity class or Taxon class

    values: list of functions
    """
    _post_hooks = {}
    """dict of hooks that are executed after the run

    keys: None or Entity class or Taxon class

    values: list of functions
    """

    tmp = []  # TODO: to be deleted again, just for testing purposes

    @unique
    class Types(Enum):
        """Defines the three hook types: pre, mid, post"""
        pre = 1
        mid = 2
        post = 3

    @classmethod
    def register_hook(cls, type, hook, theclass=None):
        """Register a hook.
        Parameters
        ==========

        type: HookTypes member
            Specifies the type of the hook.

        hook: function
            The function to be called.
            arguments: instance of the corresponding enitity or taxon, time when called
        """
        assert type in cls.Types, "please give a type from {}.HookTypes".format(
            cls.__qualname__)
        cls.tmp.append(theclass)
        if type is cls.Types.pre:
            hooks = cls._pre_hooks
        elif type is cls.Types.mid:
            hooks = cls._mid_hooks
        elif type is cls.Types.post:
            hooks = cls._post_hooks
        else:
            # if the Code ends up here, there is an error in the implementation because
            # cls.HookTypes has been extended but there is no registration done
            # here
            raise HooksError("unknown hook type")

        if theclass in hooks:
            if hook in hooks[theclass]:
                raise HookRegistrationError(
                    "already registered hook: {!r}".format(hook))
            hooks[theclass].append(hook)
        else:
            hooks[theclass] = [hook]

    @classmethod
    def unregister_hook(cls, type, hook, theclass=None,
                        error_if_not_registered=True):
        """Register a hook.
        Parameters
        ==========

        type: HookTypes member
            Specifies the type of the hook.

        hook: function
            The function to be removed.

        Errors
        ======
        raises HookRegistrationError when hook is not listed as registered
        """
        assert type in cls.Types, "please give a type from {}.HookTypes".format(
            cls.__qualname__)
        cls.tmp.append(theclass)
        if type is cls.Types.pre:
            hooks = cls._pre_hooks
        elif type is cls.Types.mid:
            hooks = cls._mid_hooks
        elif type is cls.Types.post:
            hooks = cls._post_hooks
        else:
            # if the Code ends up here, there is an error in the implementation because
            # cls.HookTypes has been extended but there is no registration done
            # here
            raise HooksError("unknown hook type")
        try:
            if theclass not in hooks:
                raise ValueError("class has no hook registered")
            hooks[theclass].remove(hook)
        except ValueError:
            if error_if_not_registered:
                raise HookRegistrationError(
                    "hook is not listed as registered, so it cannot be unregistered")
            # else: ignore quietly

    @classmethod
    def execute_hooks(cls, type, model, t):
        """Dummy docstring"""
        # TODO: Missing method docstring
        assert type in cls.Types, "please give a type from {}.HookTypes".format(
            cls.__qualname__)
        if type is cls.Types.pre:
            hooks = cls._pre_hooks
        elif type is cls.Types.mid:
            hooks = cls._mid_hooks
        elif type is cls.Types.post:
            hooks = cls._post_hooks
        else:
            # if the Code ends up here, there is an error in the implementation because
            # cls.HookTypes has been extended but there is no registration done
            # here
            raise HooksError("unknown hook type")

        if hooks:
            if None in hooks:
                # go throught all hooks that don't have an entity or taxon
                # associated with it
                for hook in hooks[None]:
                    hook(t)
            # look for the correct components fitting to each hook_class
            # and then run the hook for each instance
            for component in model.entity_types + model.process_taxa:
                for hook_class in hooks:
                    if issubclass(component, hook_class):
                        for instance in component.instances:
                            for hook in hooks[hook_class]:
                                hook(instance, t)

    def __new__(cls, *args, **kwargs):
        """raises an error because this class should not be instantiated"""
        raise HooksError("This class should not be instantiated.")
