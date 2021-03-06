# -*- coding: utf-8 -*-
# see LICENSE.rst

"""Setup Script."""

__all__ = [
    "__version__",
]


##############################################################################
# CODE
##############################################################################

# this indicates whether or not we are in the package's setup.py
try:
    _ASTROPY_SETUP_  # type: ignore
except NameError:
    # BUILT-IN
    import builtins

    builtins._ASTROPY_SETUP_ = False

try:
    # PROJECT-SPECIFIC
    from .version import version as __version__
except ImportError:
    __version__ = ""


if not _ASTROPY_SETUP_:  # noqa: F401
    # BUILT-IN
    import os
    from warnings import warn

    # THIRD PARTY
    from astropy.config.configuration import (
        ConfigurationDefaultMissingError,
        ConfigurationDefaultMissingWarning,
        update_default_config,
    )

    # Create the test function for self test
    from astropy.tests.runner import TestRunner

    test = TestRunner.make_test_runner_in(os.path.dirname(__file__))
    test.__test__ = False
    __all__ += ["test"]

    # add these here so we only need to cleanup the namespace at the end
    config_dir = None

    if not os.environ.get("ASTROPY_SKIP_CONFIG_UPDATE", False):
        config_dir = os.path.dirname(__file__)
        config_template = os.path.join(config_dir, __package__ + ".cfg")
        if os.path.isfile(config_template):
            try:
                update_default_config(
                    __package__,
                    config_dir,
                    version=__version__,
                )
            except TypeError as orig_error:
                try:
                    update_default_config(__package__, config_dir)
                except ConfigurationDefaultMissingError as e:
                    wmsg = (
                        e.args[0]
                        + " Cannot install default profile. If you are "
                        "importing from source, this is expected."
                    )
                    warn(ConfigurationDefaultMissingWarning(wmsg))
                    del e
                except Exception:
                    raise orig_error

# /if


##############################################################################
# END
