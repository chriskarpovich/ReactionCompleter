# Exceptions indicating the reaction completer has an error
#
__author__ = 'Haoyan Huo'
__maintainer__ = 'Haoyan Huo'
__email__ = 'haoyan.huo@lbl.gov'


class FormulaException(Exception):
    """
    A chemical formula cannot be parsed.
    """
    print('FormulaException')
    pass


class CannotBalance(Exception):
    """
    A general exception suggesting that reaction completer
    is unable to create a valid reaction
    """
    print('CannotBalance')
    pass


class TooFewPrecursors(CannotBalance):
    """
    Too few precursors cannot be balanced.
    """
    print('TooFewPrecursors')
    pass


class TooManyPrecursors(CannotBalance):
    """
    Too many precursors cannot be balanced. For example:

    Ba + O + BaO + TiO2 == ? == BaTiO3
    """
    print('TooManyPrecursors')
    pass


class StupidRecipe(CannotBalance):
    """
    Exception shows that the recipe is not meaningful for parsing.
    List of possible reasons:

    1. Target equals precursors: BaTiO3 == BaTiO3
    2. Target only has less than three elements: 2H + O == H2O

    """
    print('StupidRecipe')
    pass


class ExpressionPrintException(CannotBalance):
    """
    A math formula cannot be printed.
    """
    print('ExpressionPrintException')
    pass
