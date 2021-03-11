# https://www.python.org/dev/peps/pep-0396/
# https://stackoverflow.com/questions/458550/standard-way-to-embed-version-into-python-package
# version as tuple for simple comparisons
VERSION = (1, 0, 2)
# string created from tuple to avoid inconsistency
__version__ = ".".join([str(x) for x in VERSION])
