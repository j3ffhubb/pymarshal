"""

"""

import importlib
import inspect
import yaml

from pymarshal.util.init_args import init_args
from pymarshal.json import *


__all__ = [
    'DocString',
]


class DocStringArg:
    def __init__(
        self,
        name,
        desc,
        type,
        subtypes=None,
        required=True,
        default=None,
        docstring=None,
        hide=False,
    ):
        """
        desc: >
            Represents an argument to the constructor of a method or
            function.  Normally you should use DocStringArg.factory instead.
        args:
            -   name: name
                desc: The name of the argument
                type: str
            -   name: type
                desc: The type of the argument
                type: str
            -   name: desc
                desc: A description of the argument
                type: str
            -   name: subtypes
                desc: >
                    If @type is a list, dict or other data structure,
                    the contained objects should be of this type.
                    This should be a list of one item for lists, or a list
                    of 2 items for a dict.  More than 2 items is not
                    supported.
                type: list
                required: false
            -   name: required
                desc: >
                    True if this is a mandatory argument, False if it
                    has a default value.  If False, @default should be
                    set appropriately.
                type: bool
                required: false
                default: true
            -   name: default
                desc: >
                    The default value for this argument.  This is ignored
                    if @required == True
                required: false
            -   name: docstring
                desc: >
                    A docstring instance for the constructor used by @type
            -   name: hide
                desc: >
                    Don't display this argument to the user.  Useful for
                    not showing arguments that are excluded from marshalling.
                    Note that this is only a hint to the client that will
                    render the JSON, the argument will still be sent
                required: false
                default: false
        returns:
            desc: A DocStringArg instance with recursively populated
                  @docstring attributes for child arguments
            type: mpwdga.util.docstring.DocStringArg
        """
        self.name = type_assert(name, str)
        self.desc = type_assert(desc, str)
        self.type = type_assert(type, str)
        self.subtypes = type_assert_iter(
            subtypes,
            str,
            allow_none=True,
        )
        self.required = type_assert(
            required,
            bool,
        )
        self.default = default
        self.docstring = type_assert(
            docstring,
            DocString,
            allow_none=True,
        )
        self.hide = type_assert(hide, bool)

    @staticmethod
    def factory(
        name,
        desc,
        type,
        subtypes=None,
        required=True,
        default=None,
        ctor=None,
        hide=False,
    ):
        """
        desc: >
            Creates a DocStringArg and recursively includes child
            docstrings if they are not JSON types.
        args:
            -   name: type
                desc: The type of the argument
                type: str
            -   name: desc
                desc: A description of the argument
                type: str
            -   name: subtypes
                desc: >
                    If @type is a list, dict or other data structure,
                    the contained objects should be of this type.
                    This should be a list of one item for lists, or a list
                    of 2 items for a dict.  More than 2 items is not
                    supported.
                type: list
                required: false
            -   name: required
                desc: >
                    True if this is a mandatory argument, False if it
                    has a default value.  If False, @default should be
                    set appropriately.
                type: bool
            -   name: default
                desc: >
                    The default value for this argument.  This is ignored
                    if @required == True
            -   name: ctor
                desc: >
                    Only use if @type is a class instance and not a JSON type
                    The constructor that the JSON object will be
                    unmarshalled to.  Either the Class.__init__, or a
                    factory function or factory static method.
                    Use the full path: module.submodule.Class.__init__
                type: str-or-None
                required: false
            -   name: hide
                desc: >
                    Don't display this argument to the user.  Useful for
                    not showing arguments that are excluded from marshalling.
                    Note that this is only a hint to the client that will
                    render the JSON, the argument will still be sent
                required: false
                type: bool
                default: false
        returns:
            desc: A DocStringArg instance with recursively populated
                  @docstring attributes for child arguments
            type: mpwdga.util.docstring.DocStringArg
        """
        if ctor:
            type_assert(ctor, str)
            module_name, cls_name, method_name = ctor.rsplit('.', 2)
            module = importlib.import_module(module_name)
            cls = getattr(module, cls_name)
            method = getattr(cls, method_name)
            docstring = DocString.from_ctor(method)
        else:
            docstring = None

        return DocStringArg(
            name,
            desc,
            type,
            subtypes,
            required,
            default,
            docstring=docstring,
            hide=hide,
        )


class DocStringRaise:
    def __init__(
        self,
        desc,
        type,
    ):
        """
        desc: >
            Provides information about the exceptions that a
            function or method can raise.
        args:
            -   name: desc
                desc: >
                    Provides a description of what conditions will cause
                    this exception to be raised
                type: str
            -   name: type
                desc: The type of exception raised
                type: str
        """
        self.desc = type_assert(desc, str)
        self.type = type_assert(type, str)


class DocStringReturn:
    def __init__(
        self,
        desc,
        type,
        subtypes=None,
    ):
        """
        desc: >
            Provides information about the exceptions that a
            function or method can raise.
        args:
            -   name: desc
                desc: >
                    Provides a description of what conditions will cause
                    this exception to be raised
                type: str
            -   name: type
                desc: The type of exception raised
                type: str
            -   name: subtypes
                desc: >
                    If @type is a list, dict or other data structure,
                    the contained objects should be of this type.
                    This should be a list of one item for lists, or a list
                    of 2 items for a dict.  More than 2 items is not
                    supported.
                type: list
                required: false
        """
        self.desc = type_assert(desc, str)
        self.type = type_assert(type, str)
        self.subtypes = type_assert_iter(
            subtypes,
            str,
            allow_none=True,
        )
        assert (
            subtypes is None
            or
            len(subtypes) in (1, 2)
        ), subtypes


class DocString:
    def __init__(
        self,
        desc,
        args=None,
        raises=None,
        returns=None,
    ):
        """
        desc: >
            Represents a function or method docstring.  To be parsed
            from docstrings using YAML or JSON.
        args:
            -   name: desc
                desc: A description of the function or method
                type: str
            -   name: args
                desc: The arguments passed to the function or method
                type: list
                subtypes: [mpwdga.util.docstring.DocStringArg]
                required: false
            -   name: raises
                desc: The Exceptions that this function or method can raise
                type: list
                subtypes: [mpwdga.util.docstring.DocStringRaise]
                required: false
            -   name: returns
                desc: The return value (if any) from the function or method
                type: mpwdga.util.docstring.DocStringReturn
                required: false
        """
        self.desc = type_assert(desc, str)
        self.args = type_assert_iter(
            args,
            DocStringArg,
            allow_none=True,
            ctor=DocStringArg.factory,
        )
        self.raises = type_assert_iter(
            raises,
            DocStringRaise,
            allow_none=True,
        )
        self.returns = type_assert(
            returns,
            DocStringReturn,
            allow_none=True,
        )

    @staticmethod
    def from_ctor(
        ctor,
    ):
        """
        desc: >
            Turns a class constructor into an instance of DocString.
            Pass in either Class.__init__, a factory function,
            or factory static method.
        args:
            -   name: ctor
                desc: The constructor method or function to use for
                generating a DocString instance
                type: function-or-method
        raises:
            -   type: AssertionError
                desc: When ctor does not have a docstring
        """
        docstring = inspect.getdoc(ctor)
        assert docstring is not None, "No docstring for {}".format(ctor)
        obj = yaml.load(docstring)
        return unmarshal_json(obj, DocString)
