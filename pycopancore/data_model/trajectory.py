
"""
TODO:
- add auto-generated "id" field and optional "name" and "description" fields to all entity types in base
- add set_state(State) to ModelLogics 
"""

class Trajectory (dict):

    def __init__(self,*arg,**kw):
        super(Trajectory, self).__init__(*arg, **kw)
        
    def export_JSON(
            self,
            filename="./%T.json.gz",  # see below for pattern definition
            hierarchy=".%V[%I][%t]",  # see below for pattern definition
            ):
        """
        
        Pattern tokens:
        %T: entity type or process taxon class name (e.g., 'World', 'SocialSystem', 'Culture')
        %V: variable codename (e.g. 'land_carbon')
        %R: variable readable name (e.g., 'land carbon')
        %I: instance id (e.g. '1', 'c2', 'USA', ...)
        %N: instance name (e.g. 'European Union')
        %t: time point (in years)
        
        Restrictions:
        - Each of %T and %t must occur in either filename_pattern or hierarchy
        - Exactly one of %V and $R must occur in either filename_pattern or hierarchy  
        - If %T occurs in hierarchy, exactly one of %I and $N must occur in hierarchy as well  
        - %T cannot come after any of %V, %R, %I, or %N and cannot be occur in brackets
        
        So the default filename="./%T.json.gz" and hierarchy=".%V[%I][%t]" gives files like these:
            ./Cell.json.gz: gzipped file containing { 
                'metadata': {
                    'scope': {
                        'type': 'Cell'
                    }, 
                    'hierarchy': ['variable', 'instance', 'time'],
                    'levels': {
                        'instance': ['c1', 'c2', ...],
                        'time': [2000.0, 2001.0, 2001.0, ...],
                    },
                    'variables': {
                        'land_carbon': { 'name': 'land carbon', 'description': '...', 'unit': 'GtC', ... },
                        'population': { ... },
                        ...
                    }
                },
                'data': {
                    'land_carbon': [[123.4, 234.5, ...], [345.6, 456.7, ...], ...],
                    'population': [[...], [...], ...],
                    ...
                }
            }
            ./SocialSystem.json: { ... }
            
        An alternative specification of filename="./%T.%V/%I.json" and hierarchy="[%t]" would give:
            ./Cell.land_carbon/c1.json: {
                'metadata': {
                    'scope': {
                        'type': 'Cell',
                        'variable': 'land_carbon'
                    }, 
                    'hierarchy': ['time'],
                    'levels': { 'time': [2000.0, 2001.0, 2001.0, ...] },
                    'variables': { 'land_carbon': { ... } }
                },
                'data': [123.4, 234.5, ...]
            }
            ./Cell.land_carbon/c2.json: { ... }
            ...
            
        An alternative specification of filename="./all.json" and hierarchy=".%T.%N.%R.%t" would give:
            ./all.json: {
                'metadata': { 
                    'hierarchy': ['type', 'instance', 'variable',' time'], 
                    'variables': { ... } 
                },
                'data': {
                    'Cell': {
                        'cell 1': {
                            'land carbon': {
                                '2000.0': 123.4,
                                '2001.0-': 234.5,
                                '2001.0+': 345.6,
                                ...
                            },
                            'population': { ... }
                            ...
                        },
                        ...
                    },
                    'SocialSystem': { ... },
                    ...
                }
            }
        """
        pass
        
    @classmethod
    def from_JSON_import(
            filename,  # can use the same pattern as above
            model=None
            ):
        """
        hierarchy is inferred from metadata
        if model is not None, dict keys are replaced by their corresponding 
        instance and Variable objects
        """
        pass
        
    def get_state(self, t):
        """
        returns a State object
        """
        pass


class State (dict):
    """just like Trajectory, just without any time dimension"""

    def __init__(self,*arg,**kw):
        super(State, self).__init__(*arg, **kw)
        
    def export_JSON(
            self,
            filename="./%T.json.gz",
            hierarchy=".%V[%I]",
            ):
        pass
        
    @classmethod
    def from_JSON_import(
            filename,
            model=None
            ):
        pass
