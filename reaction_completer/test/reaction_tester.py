import re
from unittest import TestCase

from reaction_completer.driver import balance_recipe


def simple_parse(composition_string):
    """
    Parse compact composition strings such as:

    '''
    1.0--D:1.0+C:1.0+O:3.0;
    2.0--Fe:2.0+O:3.0?
    D:K,Na;E:O,H<
    Na+&K+
    '''

    Rules:
    1. Whitespaces will be ignored.
    2. The entire string is formatted as:
        "COMPOSITIONS ? SUBSTITUTIONS < ADDITIVES"
    3. COMPOSITIONS is separated into components using semicolon ";"
    4. Each component can have an optional prefix "amount--"
    5. Each component will contain a list of elements separated by "+"
    6. Each element has an optional postfix ":amount"
    7. Substitutions are made by parts separated by semicolon ";"
    8. Each substitution is "Var:value1,value2..."
    9. Additives are separated by and "&"
    """
    composition_string = re.sub(r'\s', '', composition_string)

    additives = []
    if '<' in composition_string:
        composition_string, additives_string = composition_string.split('<')
        additives = additives_string.split('&')

    elements_vars = {}
    if '?' in composition_string:
        composition_string, elements_vars_string = composition_string.split('?')
        for element_var in elements_vars_string.split(';'):
            element, values = element_var.split(':')
            elements_vars[element] = values.split(',')

    compositions = composition_string.split(';')
    material_composition = []
    for composition in compositions:
        parts = composition.split('--', maxsplit=1)
        if len(parts) == 1:
            comp_amount, elements = '1.0', parts[0]
        else:
            comp_amount, elements = parts
        elements_dict = {}
        for pair in elements.split('+'):
            parts = pair.split(':', maxsplit=1)
            if len(parts) == 1:
                element, amount = parts[0], '1.0'
            else:
                element, amount = parts
            elements_dict[element] = amount
        material_composition.append({
            'amount': comp_amount,
            'elements': elements_dict
        })
    return material_composition, elements_vars, additives


def make_material(data):
    material_formula, material_string, composition_string = data
    composition, elements_vars, additives = simple_parse(composition_string)
    return {
        'material_formula': material_formula,
        'material_string': material_string,
        'composition': composition,
        'elements_vars': elements_vars,
        'additives': additives,
    }


def make_materials(data):
    return [make_material(x) for x in data]


class TestReaction(TestCase):
    def balance_equation(self, precursors, targets, text=None):
        return balance_recipe(
            make_materials(precursors),
            make_materials(targets),
            text)

    @staticmethod
    def _parse_equation(eq):
        parts = re.split(r'\s*;\s*', eq)
        left, right = parts[0].split(' == ')
        left = set(re.split(r'\s\+\s', left))
        right = set(re.split(r'\s\+\s', right))

        if len(parts) > 1:
            substitutions = set(re.split(r'\s*,\s*', parts[1]))
        else:
            substitutions = set()

        if len(parts) > 2:
            additives = parts[2:]
        else:
            additives = set()

        return left, right, substitutions, additives

    def assertReactionsEqual(self, reactions, reactions_correct_strings):
        reactions = sorted([self._parse_equation(x[3]) for x in reactions])
        reactions_correct = sorted([self._parse_equation(x) for x in reactions_correct_strings])

        return self.assertListEqual(reactions, reactions_correct)
