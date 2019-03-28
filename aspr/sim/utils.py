import logging

# Specify logging settings
logging.basicConfig(
    format='%(levelname)s: aspr - %(name)s : %(message)s')
logging_level_dict = {0: logging.WARNING, 1: logging.INFO, 2: logging.DEBUG}

def _setup_logger(cls, verbose=0):
    """Configures and returns logger instance.
    This function takes a class instance (which must have a `name` attribute)
    and a verbosity level as parameters and returns a connfigured logger
    instance with the appropriate level set.
    Parameters
    ----------
    cls : object
        Class instance with attribute `name` (e.g. Scenario, GreedyDecisionModel)
    verbose: int
        Verbosity level. Values can be 0, 1, or 2, with 0 being the least
        verbose and 2 being the most verbose.
    Returns
    -------
    logger : logging.Logger
        Configured logger
    Allows classes to each have their own seperate loggers in order to
    allow for varying levels of verbosity. 
    setup_logger() helps streamline this process.
    """
    if not hasattr(cls, 'name'):
        raise AttributeError('Input must have a "name" attribute.')
    # Set up logger
    if verbose not in logging_level_dict:
        raise KeyError('Verbose option {} for {} not valid. '
                       'Valid options are {}.'.format(
                           verbose, cls.name, logging_level_dict.keys()))
    logger = logging.getLogger(cls.name)
    logger.setLevel(logging_level_dict[verbose])

    return logger