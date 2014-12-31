from __future__ import print_function, unicode_literals, division
from importlib import import_module


class Config(dict):

    """A class for storing configuration parameters. """

    EXPECTED_VARS = ['OPENNLP_BIN',
                     'OPENNLP_MODEL',
                     ]

    def from_object(self, module_name):
        """Load a configuration from a module name.

        :module_name: The name of the module where the parameters are defined.
        """
        m = import_module(module_name)

        for var in self.EXPECTED_VARS:
            if hasattr(m, var):
                self[var] = getattr(m, var)


config = Config()
