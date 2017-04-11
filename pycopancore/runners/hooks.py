"""Register hooks for the run inside a runner."""
# This file is part of pycopancore.
#
# Copyright (C) 2016 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

#
# Imports
#
from enum import Enum, unique

#
# Specific Error Definition
#

class HookRegistrationError(BaseException):
    pass

class HooksError(BaseException):
    pass

#
# Definition of class _AbstractRunner
#

class Hooks(object):
    """Class managing the hooks that are called before, during and after a run."""

    # class variables
    _pre_hooks = []
    """list of hooks that are executed before the run (in inverse order)"""
    _mid_hooks = []
    """list of hooks that are executed every time the run is halted for a step or an event"""
    _post_hooks = []
    """list of hooks that are executed after the run"""

    @unique
    class HookTypes(Enum):
        """Defines the three hook types: pre, mid, post"""
        pre = 1
        mid = 2
        post = 3

    @classmethod
    def register_hook(cls, type, hook):
        """Register a hook.
        Parameters
        ==========
        
        type: HookTypes member
            Specifies the type of the hook.
            
        hook: function
            The function to be called.  
            pre and post arguments: instance of the corresponding enitity or taxon
            mid arguments: instance of the corresponding enitity or taxon, time when called
        """
        assert type in cls.HookTypes, "please give a type from {}.HookTypes".format(cls.__qualname__)
        if type is cls.HookTypes.pre:
            cls._pre_hooks.append(hook)
        elif type is cls.HookTypes.mid:
            cls._mid_hooks.append(hook)
        elif type is cls.HookTypes.post:
            cls._post_hooks.append(hook)
        else:
            # if the Code ends up here, there is an error in the implementation because
            # cls.HookTypes has been extended but there is no registration done here
            raise HooksError("unknown hook type")

    @classmethod
    def unregister_hook(cls, type, hook):
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
        assert type in cls.HookTypes, "please give a type from {}.HookTypes".format(cls.__qualname__)
        try:
            if type is cls.HookTypes.pre:
                cls._pre_hooks.remove(hook)
            elif type is cls.HookTypes.mid:
                cls._mid_hooks.remove(hook)
            elif type is cls.HookTypes.post:
                cls._post_hooks.remove(hook)
            else:
                raise HooksError("unknown hook type")
        except ValueError:
            raise HookRegistrationError("hook is not listed as registered, so it cannot be unregistered")

    def __new__(cls, *args, **kwargs):
        """raises an error because this class should not be instantiated"""
        raise HooksError("This class should not be instantiated.")



