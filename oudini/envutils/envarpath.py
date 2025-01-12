#! python3
import  copy
import  logging
from    pathlib import Path
import  os
from    typing import Union


class EnvarPath:
    """
    System-independant class for convenient manipulation of the PATH environment variable.
    """
    PATH_ENVAR_NAME = 'PATH'

    def __init__(self):
        """
        Constructor
        """
        self._logger = logging.getLogger("%s-%s" %(__name__, type(self).__name__))
        self._path   = ""

    @classmethod
    def from_environ(cls):
        """
            Create an envutils.Path object from the PATH variable in the current environment.
        :return:
        """

        obj = cls()
        obj._path = os.environ[EnvarPath.PATH_ENVAR_NAME]

        obj._logger.debug("Created instance - PATH = '%s'" % (obj._path))
        return obj

    def append(self,
               i_item : Union[str, Path]):
        """
        TODO
        :param i_item:
        :return:
        """
        self._logger.debug("Appended: '%s'" % (str(i_item)))
        return self._concatenate(i_format = "{path_str}{separator}{item}",
                                 i_item   = str(i_item))

    def prepend(self,
                i_item : Union[str, Path, 'EnvarPath']):
        """
        TODO
        :param i_item:
        :return:
        """
        self._logger.debug("Prepended: '%s'" % (str(i_item)))
        return self._concatenate(i_format = "{item}{separator}{path_str}",
                                 i_item   = str(i_item))

    def __str__(self):
        """
        :return: PATH, as a string
        """
        return self._path

    def _concatenate(self,
                     i_format : str,
                     i_item   : Union[str, Path, 'EnvarPath']):
        """
        
        :param i_format: 
        :param i_item: 
        :return: 
        """
        assert isinstance(i_format, str)
        assert isinstance(i_item, str)  or\
               isinstance(i_item, Path) or\
               isinstance(i_item, EnvarPath)

        if (self._path):
            self._path = i_format.format(separator = os.pathsep,
                                         item      = str(i_item),
                                         path_str  = self._path)
        else:
            self._path = str(i_item)

        return self


    def join(self,
             *argv,
             i_add_to_end : bool = True):
        p = copy.deepcopy(self)

        for arg in argv:
            if i_add_to_end:
                p.append(arg)
            else:
                p.prepend(arg)

        return p

