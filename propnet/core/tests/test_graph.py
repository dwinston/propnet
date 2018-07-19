import unittest
from propnet.core.graph import Graph, SymbolPath
from propnet.core.materials import Material
from propnet.core.symbols import Symbol
from propnet.core.models import AbstractModel
from propnet.core.quantity import Quantity

from propnet.symbols import DEFAULT_SYMBOLS

class GraphTest(unittest.TestCase):

    @staticmethod
    def generate_canonical_symbols():
        """
        Returns a set of Symbol objects used in testing.
        Returns: (dict<str, Symbol>)
        """
        A = Symbol('A', ['A'], ['A'], units=[1.0, []], shape=[1])
        B = Symbol('B', ['B'], ['B'], units=[1.0, []], shape=[1])
        C = Symbol('C', ['C'], ['C'], units=[1.0, []], shape=[1])
        D = Symbol('D', ['D'], ['D'], units=[1.0, []], shape=[1])
        G = Symbol('G', ['G'], ['G'], units=[1.0, []], shape=[1])
        F = Symbol('F', ['F'], ['F'], units=[1.0, []], shape=[1])
        return {
            'A': A,
            'B': B,
            'C': C,
            'D': D,
            'G': G,
            'F': F
        }

    @staticmethod
    def generate_canonical_models(c_symbols):
        """
        Returns a set of Model objects used in testing.
        Returns: (dict<str, Model>)
        """

        class Model1 (AbstractModel):
            def __init__(self, symbol_types=None):
                AbstractModel.__init__(self, metadata=
                    { 'title': 'model1', 'tags': [], 'references': [], 'description': '',
                      'symbol_mapping': {'A': 'A',
                                         'B': 'B',
                                         'C': 'C'
                                        },
                      'connections': [{'inputs': ['A'],
                                       'outputs': ['B', 'C']
                                      }],
                      'equations': ['B-2*A', 'C-3*A']
                    },
                    symbol_types=symbol_types)

        class Model2 (AbstractModel):
            def __init__(self, symbol_types=None):
                AbstractModel.__init__(self, metadata=
                    { 'title': 'model2', 'tags': [], 'references': [], 'description': '',
                      'symbol_mapping': {'A': 'A',
                                         'G': 'G'
                                        },
                      'connections': [{'inputs': ['A'],
                                       'outputs': ['G']
                                      }],
                      'equations': ['G-5*A']
                    },
                    symbol_types=symbol_types)

        class Model3 (AbstractModel):
            def __init__(self, symbol_types=None):
                AbstractModel.__init__(self, metadata=
                    { 'title': 'model3', 'tags': [], 'references': [], 'description': '',
                      'symbol_mapping': {'B': 'B',
                                         'F': 'F'
                                        },
                      'connections': [{'inputs': ['B'],
                                       'outputs': ['F']
                                      }],
                      'equations': ['F-7*B']
                    },
                    symbol_types=symbol_types)

        class Model4 (AbstractModel):
            def __init__(self, symbol_types=None):
                AbstractModel.__init__(self, metadata=
                    { 'title': 'model4', 'tags': [], 'references': [], 'description': '',
                      'symbol_mapping': {'D': 'D',
                                         'B': 'B',
                                         'C': 'C'
                                        },
                      'connections': [{'inputs': ['B', 'C'],
                                       'outputs': ['D']
                                      }],
                      'equations': ['D-B*C*11']
                    },
                    symbol_types=symbol_types)

        class Model5 (AbstractModel):
            def __init__(self, symbol_types=None):
                AbstractModel.__init__(self, metadata=
                    { 'title': 'model5', 'tags': [], 'references': [], 'description': '',
                      'symbol_mapping': {'C': 'C',
                                         'G': 'G',
                                         'D': 'D'
                                        },
                      'connections': [{'inputs': ['C', 'G'],
                                       'outputs': ['D']
                                      }],
                      'equations': ['D-C*G*13']
                    },
                    symbol_types=symbol_types)

        class Model6 (AbstractModel):
            def __init__(self, symbol_types=None):
                AbstractModel.__init__(self, metadata=
                    { 'title': 'model6', 'tags': [], 'references': [], 'description': '',
                      'symbol_mapping': {'A': 'A',
                                         'F': 'F',
                                         'D': 'D'
                                        },
                      'connections': [{'inputs': ['F', 'D'],
                                       'outputs': ['A']
                                      }],
                      'equations': ['A-F*D*17']
                    },
                    symbol_types=symbol_types)

        models = [Model1(c_symbols), Model2(c_symbols), Model3(c_symbols),
                  Model4(c_symbols), Model5(c_symbols), Model6(c_symbols)]
        return {x.title: x for x in models}

    @staticmethod
    def generate_canonical_material(c_symbols):
        """
        Generates a Material with appropriately attached Quantities.
        Args:
            c_symbols: (dict<str, Symbol>) dictionary of defined materials.
        Returns:
            (Material) material with properties loaded.
        """
        q1 = Quantity(c_symbols['A'], 19)
        q2 = Quantity(c_symbols['A'], 23)
        m = Material()
        m.add_quantity(q1)
        m.add_quantity(q2)
        return m

    def test_graph_setup(self):
        """
        Tests the outcome of constructing the canonical graph.
        """
        symbols = GraphTest.generate_canonical_symbols()
        models = GraphTest.generate_canonical_models(symbols)
        g = Graph(models=models, symbol_types=symbols)
        st_c = {x for x in symbols.values()}
        st_g = g.get_symbol_types()
        m_c = {x for x in models.values()}
        m_g = g.get_models()
        self.assertTrue(st_c == st_g,
                        'Canonical constructed graph does not have the right Symbol objects.')
        self.assertTrue(m_c == m_g,
                        'Canonical constructed graph does not have the right Model objects.')
        for m in models.values():
            for d in m.type_connections:
                for s in d['inputs']:
                    self.assertTrue(symbols[s] in g._input_to_model.keys(),
                                    "Canonical constructed graph does not have an edge from input: " + s +
                                    " to model: " + m.name)
                    self.assertTrue(m in g._input_to_model[s],
                                    "Canonical constructed graph does not have an edge from input: " + s +
                                    " to model: " + m.name)
                for s in d['outputs']:
                    self.assertTrue(symbols[s] in g._output_to_model.keys(),
                                    "Canonical constructed graph does not have an edge from input: " + s +
                                    " to model: " + m.name)
                    self.assertTrue(m in g._output_to_model[s],
                                    "Canonical constructed graph does not have an edge from input: " + s +
                                    " to model: " + m.name)

    def test_model_add_remove(self):
        """
        Tests the outcome of adding and removing a model from the canonical graph.
        """
        symbols = GraphTest.generate_canonical_symbols()
        models = GraphTest.generate_canonical_models(symbols)
        g = Graph(models=models, symbol_types=symbols)
        g.remove_models({models['model6'].name: models['model6']})
        self.assertTrue(models['model6'] not in g.get_models(),
                        "Model was unsuccessfully removed from the graph.")
        for s in g._input_to_model.values():
            self.assertTrue(models['model6'] not in s,
                            "Model was unsuccessfully removed from the graph.")
        for s in g._output_to_model.values():
            self.assertTrue(models['model6'] not in s,
                            "Model was unsuccessfully removed from the graph.")
        m6 = models['model6']
        del models['model6']
        for m in models.values():
            self.assertTrue(m in g.get_models(),
                            "Too many models were removed.")
        g.update_models({'Model6': m6})
        self.assertTrue(m6 in g.get_models(),
                        "Model was unsuccessfully added to the graph.")
        self.assertTrue(m6 in g._input_to_model[symbols['D']],
                        "Model was unsuccessfully added to the graph.")
        self.assertTrue(m6 in g._input_to_model[symbols['F']],
                        "Model was unsuccessfully added to the graph.")
        self.assertTrue(m6 in g._output_to_model[symbols['A']],
                        "Model was unsuccessfully added to the graph.")

    def test_symbol_add_remove(self):
        """
        Tests the outcome of adding and removing a Symbol from the canonical graph.
        """
        symbols = GraphTest.generate_canonical_symbols()
        models = GraphTest.generate_canonical_models(symbols)
        g = Graph(models=models, symbol_types=symbols)
        g.remove_symbol_types({'F': symbols['F']})
        self.assertTrue(symbols['F'] not in g.get_symbol_types(),
                        "Symbol was not properly removed.")
        self.assertTrue(symbols['F'] not in g._input_to_model.keys(),
                        "Symbol was not properly removed.")
        self.assertTrue(symbols['F'] not in g._output_to_model.keys(),
                        "Symbol was not properly removed.")
        self.assertTrue(models['model3'] not in g.get_models(),
                        "Removing symbol did not remove a model using that symbol.")
        self.assertTrue(models['model6'] not in g.get_models(),
                        "Removing symbol did not remove a model using that symbol.")
        g.update_symbol_types({'F': symbols['F']})
        self.assertTrue(symbols['F'] in g.get_symbol_types(),
                       "Symbol was not properly added.")

    def test_evaluate(self):
        """
        Tests the evaluation algorithm on a non-cyclic graph.
        The canonical graph and the canonical material are used for this test.
        """
        symbols = GraphTest.generate_canonical_symbols()
        models = GraphTest.generate_canonical_models(symbols)
        material = GraphTest.generate_canonical_material(symbols)
        del models['model6']
        g = Graph(symbol_types=symbols, models=models)
        material_derived = g.evaluate(material)

        expected_quantities = [
            Quantity(symbols['A'], 19),
            Quantity(symbols['A'], 23),
            Quantity(symbols['B'], 38),
            Quantity(symbols['B'], 46),
            Quantity(symbols['C'], 57),
            Quantity(symbols['C'], 69),
            Quantity(symbols['G'], 95),
            Quantity(symbols['G'], 115),
            Quantity(symbols['F'], 266),
            Quantity(symbols['F'], 322),
            Quantity(symbols['D'], 23826),
            Quantity(symbols['D'], 28842),
            Quantity(symbols['D'], 34914),
            Quantity(symbols['D'], 70395),
            Quantity(symbols['D'], 85215),
            Quantity(symbols['D'], 103155),
        ]

        self.assertTrue(material == GraphTest.generate_canonical_material(symbols),
                        "evaluate() mutated the original material argument.")

        derived_quantities = material_derived.get_quantities()
        self.assertTrue(len(expected_quantities) == len(derived_quantities),
                        "Evaluate did not correctly derive outputs.")
        for q in expected_quantities:
            self.assertTrue(q in material_derived._symbol_to_quantity[q.symbol],
                            "Evaluate failed to derive all outputs.")
            self.assertTrue(q in derived_quantities)

    def test_evaluate_cyclic(self):
        """
        Tests the evaluation algorithm on a cyclic graph.
        The canonical graph and the canonical material are used for this test.
        """
        symbols = GraphTest.generate_canonical_symbols()
        models = GraphTest.generate_canonical_models(symbols)
        material = GraphTest.generate_canonical_material(symbols)
        g = Graph(symbol_types=symbols, models=models)
        material_derived = g.evaluate(material)

        expected_quantities = [
            # Starting
            Quantity(symbols['A'], 19),
            Quantity(symbols['A'], 23),

            # Derives -1 (M1)
            Quantity(symbols['B'], 38),
            Quantity(symbols['B'], 46),
            Quantity(symbols['C'], 57),
            Quantity(symbols['C'], 69),
            # Derives -2 (M3, M1)
            Quantity(symbols['F'], 266),
            Quantity(symbols['F'], 322),
            # Derives -2 (M4, M1)
            Quantity(symbols['D'], 23826),
            Quantity(symbols['D'], 28842),
            Quantity(symbols['D'], 34914),
            # Derives -3 (M6, M3, M4, M1)
            Quantity(symbols['A'], 107741172),
            Quantity(symbols['A'], 130423524),
            Quantity(symbols['A'], 157881108),
            Quantity(symbols['A'], 191119236),
            # Derivable outputs include Derives -4 and Derives -5

            # Derives -1 (M2)
            Quantity(symbols['G'], 95),
            Quantity(symbols['G'], 115),
            # Derives -2 (M5, M1, M2)
            Quantity(symbols['D'], 70395),
            Quantity(symbols['D'], 85215),
            Quantity(symbols['D'], 103155),
            # Derives -3 (M6, M5, M1, M2)
            Quantity(symbols['A'], 318326190),
            Quantity(symbols['A'], 385342230),
            Quantity(symbols['A'], 466466910),
            Quantity(symbols['A'], 564670470),
            # Any derivable outputs are then snubbed.

            # Derives -4 (M2, M6, M3, M4, M1)
            Quantity(symbols['G'], 538705860),
            Quantity(symbols['G'], 652117620),
            Quantity(symbols['G'], 789405540),
            Quantity(symbols['G'], 955596180),
            # Derives -5 (M5, M2, M6, M3, M4, M1)
            # (57 & 69)
            Quantity(symbols['D'], 399181042260),
            Quantity(symbols['D'], 483219156420),
            Quantity(symbols['D'], 584949505140),
            Quantity(symbols['D'], 708096769380),
            Quantity(symbols['D'], 857169773460)
        ]

        self.assertTrue(material == GraphTest.generate_canonical_material(symbols),
                        "evaluate() mutated the original material argument.")

        derived_quantities = material_derived.get_quantities()
        self.assertTrue(len(expected_quantities) == len(derived_quantities),
                        "Evaluate did not correctly derive outputs.")
        for q in expected_quantities:
            self.assertTrue(q in material_derived._symbol_to_quantity[q.symbol],
                            "Evaluate failed to derive all outputs.")
            self.assertTrue(q in derived_quantities)

    def test_evaluate_constraints(self):
        """
        Tests the evaluation algorithm on a non-cyclic graph involving constraints.
        The canonical graph and the canonical material are used for this test.
        """
        class Model4 (AbstractModel):
            def __init__(self, symbol_types=None):
                AbstractModel.__init__(self, metadata=
                    { 'title': 'model4', 'tags': [], 'references': [], 'description': '',
                      'symbol_mapping': {'D': 'D',
                                         'B': 'B',
                                         'C': 'C',
                                         'G': 'G'
                                        },
                      'connections': [{'inputs': ['B', 'C'],
                                       'outputs': ['D']
                                      }],
                      'equations': ['D-B*C*11']
                    },
                    symbol_types=symbol_types)

            @property
            def constraint_symbols(self):
                return ['G']

            def check_constraints(self, constraint_inputs):
                return constraint_inputs['G'] == 0

        symbols = GraphTest.generate_canonical_symbols()
        models = GraphTest.generate_canonical_models(symbols)
        models['model4'] = Model4(symbol_types=symbols)
        del models['model6']
        material = GraphTest.generate_canonical_material(symbols)
        g = Graph(symbol_types=symbols, models=models)
        material_derived = g.evaluate(material)

        expected_quantities = [
            Quantity(symbols['A'], 19),
            Quantity(symbols['A'], 23),
            Quantity(symbols['B'], 38),
            Quantity(symbols['B'], 46),
            Quantity(symbols['C'], 57),
            Quantity(symbols['C'], 69),
            Quantity(symbols['G'], 95),
            Quantity(symbols['G'], 115),
            Quantity(symbols['F'], 266),
            Quantity(symbols['F'], 322),
            Quantity(symbols['D'], 70395),
            Quantity(symbols['D'], 85215),
            Quantity(symbols['D'], 103155)
        ]

        self.assertTrue(material == GraphTest.generate_canonical_material(symbols),
                        "evaluate() mutated the original material argument.")

        derived_quantities = material_derived.get_quantities()
        self.assertTrue(len(expected_quantities) == len(derived_quantities),
                        "Evaluate did not correctly derive outputs.")
        for q in expected_quantities:
            self.assertTrue(q in material_derived._symbol_to_quantity[q.symbol],
                            "Evaluate failed to derive all outputs.")
            self.assertTrue(q in derived_quantities)

    def test_evaluate_constraints_cyclic(self):
        """
        Tests the evaluation algorithm on a cyclic graph involving constraints.
        The canonical graph and the canonical material are used for this test.
        """
        class Model4 (AbstractModel):
            def __init__(self, symbol_types=None):
                AbstractModel.__init__(self, metadata=
                    { 'title': 'model4', 'tags': [], 'references': [], 'description': '',
                      'symbol_mapping': {'D': 'D',
                                         'B': 'B',
                                         'C': 'C',
                                         'G': 'G'
                                        },
                      'connections': [{'inputs': ['B', 'C'],
                                       'outputs': ['D']
                                      }],
                      'equations': ['D-B*C*11']
                    },
                    symbol_types=symbol_types)

            @property
            def constraint_symbols(self):
                return ['G']

            def check_constraints(self, constraint_inputs):
                return constraint_inputs['G'] == 0

        symbols = GraphTest.generate_canonical_symbols()
        models = GraphTest.generate_canonical_models(symbols)
        models['model4'] = Model4(symbol_types=symbols)
        material = GraphTest.generate_canonical_material(symbols)
        g = Graph(symbol_types=symbols, models=models)
        material_derived = g.evaluate(material)

        expected_quantities = [
            Quantity(symbols['A'], 19),
            Quantity(symbols['A'], 23),
            Quantity(symbols['B'], 38),
            Quantity(symbols['B'], 46),
            Quantity(symbols['C'], 57),
            Quantity(symbols['C'], 69),
            Quantity(symbols['G'], 95),
            Quantity(symbols['G'], 115),
            Quantity(symbols['F'], 266),
            Quantity(symbols['F'], 322),
            Quantity(symbols['D'], 70395),
            Quantity(symbols['D'], 85215),
            Quantity(symbols['D'], 103155),
            Quantity(symbols['A'], 318326190),
            Quantity(symbols['A'], 385342230),
            Quantity(symbols['A'], 466466910),
            Quantity(symbols['A'], 564670470)
        ]

        self.assertTrue(material == GraphTest.generate_canonical_material(symbols),
                        "evaluate() mutated the original material argument.")

        derived_quantities = material_derived.get_quantities()
        self.assertTrue(len(expected_quantities) == len(derived_quantities),
                        "Evaluate did not correctly derive outputs.")
        for q in expected_quantities:
            self.assertTrue(q in material_derived._symbol_to_quantity[q.symbol],
                            "Evaluate failed to derive all outputs.")
            self.assertTrue(q in derived_quantities)

    def test_evaluate_single_material_degenerate_property(self):
        """
        Graph has one material on it: mat1
            mat1 has trivial degenerate properties relative permittivity and relative permeability
                2 experimental relative permittivity measurements
                2 experimental relative permeability measurements
        Determines if TestGraph1 is correctly evaluated using the evaluate method.
        We expect 4 refractive_index properties to be calculated as the following:
            sqrt(3), sqrt(5), sqrt(6), sqrt(10)
        """
        # Setup
        propnet = Graph()
        mat1 = Material()
        mat1.add_quantity(Quantity(DEFAULT_SYMBOLS['relative_permeability'], 1))
        mat1.add_quantity(Quantity(DEFAULT_SYMBOLS['relative_permeability'], 2))
        mat1.add_quantity(Quantity(DEFAULT_SYMBOLS['relative_permittivity'], 3))
        mat1.add_quantity(Quantity(DEFAULT_SYMBOLS['relative_permittivity'], 5))

        mat1_derived = propnet.evaluate(mat1)

        # Expected outputs
        s_outputs = []
        s_outputs.append(Quantity('relative_permeability', 1))
        s_outputs.append(Quantity('relative_permeability', 2))
        s_outputs.append(Quantity('relative_permittivity', 3))
        s_outputs.append(Quantity('relative_permittivity', 5))
        s_outputs.append(Quantity('refractive_index', 3 ** 0.5))
        s_outputs.append(Quantity('refractive_index', 5 ** 0.5))
        s_outputs.append(Quantity('refractive_index', 6 ** 0.5))
        s_outputs.append(Quantity('refractive_index', 10 ** 0.5))

        st_outputs = []
        st_outputs.append(DEFAULT_SYMBOLS['relative_permeability'])
        st_outputs.append(DEFAULT_SYMBOLS['relative_permittivity'])
        st_outputs.append(DEFAULT_SYMBOLS['refractive_index'])

        # Test
        for q_expected in s_outputs:
            q = None
            for q_derived in mat1_derived._symbol_to_quantity[q_expected.symbol]:
                if q_derived == q_expected:
                    q = q_derived
            self.assertTrue(q is not None,
                            "Quantity missing from evaluate.")

    def test_symbol_expansion(self):
        """
        Tests the Symbol Expansion algorithm on a non-cyclic graph.
        The canonical graph and the canonical material are used for this test.
        """
        symbols = GraphTest.generate_canonical_symbols()
        models = GraphTest.generate_canonical_models(symbols)
        material = GraphTest.generate_canonical_material(symbols)
        del models['model6']
        g = Graph(symbol_types=symbols, models=models)

        ts = []
        ans = []

        ts.append(g.calculable_properties({symbols['A']}))
        ans.append({x for x in symbols.values() if x is not symbols['A']})

        ts.append(g.calculable_properties({symbols['B']}))
        ans.append({symbols['F']})

        ts.append(g.calculable_properties({symbols['C']}))
        ans.append(set())

        ts.append(g.calculable_properties({symbols['C'], symbols['G']}))
        ans.append({symbols['D']})

        ts.append(g.calculable_properties({symbols['B'], symbols['C']}))
        ans.append({symbols['D'], symbols['F']})

        for i in range(0, len(ts)):
            self.assertTrue(ts[i] == ans[i],
                            "Symbol Expansion failed: test - " + str(i))

    def test_symbol_expansion_cyclic(self):
        """
        Tests the Symbol Expansion algorithm on a cyclic graph.
        The canonical graph and the canonical material are used for this test.
        """
        symbols = GraphTest.generate_canonical_symbols()
        models = GraphTest.generate_canonical_models(symbols)
        material = GraphTest.generate_canonical_material(symbols)
        g = Graph(symbol_types=symbols, models=models)

        ts = []
        ans = []

        ts.append(g.calculable_properties({symbols['A']}))
        ans.append({x for x in symbols.values() if x is not symbols['A']})

        ts.append(g.calculable_properties({symbols['B']}))
        ans.append({symbols['F']})

        ts.append(g.calculable_properties({symbols['C']}))
        ans.append(set())

        ts.append(g.calculable_properties({symbols['C'], symbols['G']}))
        ans.append({symbols['D']})

        ts.append(g.calculable_properties({symbols['B'], symbols['C']}))
        ans.append({x for x in symbols.values() if x is not symbols['B'] and x is not symbols['C']})

        for i in range(0, len(ts)):
            self.assertTrue(ts[i] == ans[i],
                            "Symbol Expansion failed: test - " + str(i))

    def test_symbol_expansion_constraints(self):
        """
        Tests the Symbol Expansion algorithm on a non-cyclic graph with constraints.
        The canonical graph and the canonical material are used for this test.
        """
        class Model4 (AbstractModel):
            def __init__(self, symbol_types=None):
                AbstractModel.__init__(self, metadata=
                    { 'title': 'model4', 'tags': [], 'references': [], 'description': '',
                      'symbol_mapping': {'D': 'D',
                                         'B': 'B',
                                         'C': 'C',
                                         'G': 'G'
                                        },
                      'connections': [{'inputs': ['B', 'C'],
                                       'outputs': ['D']
                                      }],
                      'equations': ['D-B*C*11']
                    },
                    symbol_types=symbol_types)

            @property
            def constraint_symbols(self):
                return ['G']

            def check_constraints(self, constraint_inputs):
                return constraint_inputs['G'] == 0

        symbols = GraphTest.generate_canonical_symbols()
        models = GraphTest.generate_canonical_models(symbols)
        models['model4'] = Model4(symbol_types=symbols)
        del models['model6']
        material = GraphTest.generate_canonical_material(symbols)
        g = Graph(symbol_types=symbols, models=models)

        ts = []
        ans = []

        ts.append(g.calculable_properties({symbols['A']}))
        ans.append({x for x in symbols.values() if x is not symbols['A']})

        ts.append(g.calculable_properties({symbols['B']}))
        ans.append({symbols['F']})

        ts.append(g.calculable_properties({symbols['C']}))
        ans.append(set())

        ts.append(g.calculable_properties({symbols['C'], symbols['G']}))
        ans.append({symbols['D']})

        ts.append(g.calculable_properties({symbols['B'], symbols['C']}))
        ans.append({symbols['F']})

        for i in range(0, len(ts)):
            self.assertEqual(ts[i], ans[i],
                             "Symbol Expansion failed: test - " + str(i))

    def test_symbol_expansion_cyclic_constraints(self):
        """
        Tests the Symbol Expansion algorithm on a cyclic graph with constraints.
        The canonical graph and the canonical material are used for this test.
        """
        class Model4 (AbstractModel):
            def __init__(self, symbol_types=None):
                AbstractModel.__init__(self, metadata=
                    { 'title': 'model4', 'tags': [], 'references': [], 'description': '',
                      'symbol_mapping': {'D': 'D',
                                         'B': 'B',
                                         'C': 'C',
                                         'G': 'G'
                                        },
                      'connections': [{'inputs': ['B', 'C'],
                                       'outputs': ['D']
                                      }],
                      'equations': ['D-B*C*11']
                    },
                    symbol_types=symbol_types)

            @property
            def constraint_symbols(self):
                return ['G']

            def check_constraints(self, constraint_inputs):
                return constraint_inputs['G'] == 0

        symbols = GraphTest.generate_canonical_symbols()
        models = GraphTest.generate_canonical_models(symbols)
        models['model4'] = Model4(symbol_types=symbols)
        material = GraphTest.generate_canonical_material(symbols)
        g = Graph(symbol_types=symbols, models=models)

        ts = []
        ans = []

        ts.append(g.calculable_properties({symbols['A']}))
        ans.append({x for x in symbols.values() if x is not symbols['A']})

        ts.append(g.calculable_properties({symbols['B']}))
        ans.append({symbols['F']})

        ts.append(g.calculable_properties({symbols['C']}))
        ans.append(set())

        ts.append(g.calculable_properties({symbols['C'], symbols['G']}))
        ans.append({symbols['D']})

        ts.append(g.calculable_properties({symbols['B'], symbols['C']}))
        ans.append({symbols['F']})

        for i in range(0, len(ts)):
            self.assertEqual(ts[i], ans[i],
                             "Symbol Expansion failed: test - " + str(i))

    def test_symbol_ancestry(self):
        """
        Tests the Symbol Ancestry algorithm on a non-cyclic graph.
        The canonical graph and the canonical material are used for this test.
        """
        symbols = GraphTest.generate_canonical_symbols()
        models = GraphTest.generate_canonical_models(symbols)
        material = GraphTest.generate_canonical_material(symbols)
        del models['model6']
        g = Graph(symbol_types=symbols, models=models)

        out1 = g.required_inputs_for_property(symbols['F'])

        self.assertTrue(out1.head.m is None and out1.head.parent is None and
                        out1.head.inputs == {symbols['F']} and len(out1.head.children) == 1,
                        "Tree head not properly defined.")
        self.assertTrue(out1.head.children[0].m == models['model3'] and
                        out1.head.children[0].inputs == {symbols['B']} and
                        out1.head.children[0].parent is out1.head and
                        len(out1.head.children[0].children) == 1,
                        "Tree branch improperly formed.")
        self.assertTrue(out1.head.children[0].children[0].m == models['model1'] and
                        out1.head.children[0].children[0].inputs == {symbols['A']} and
                        out1.head.children[0].children[0].parent is out1.head.children[0] and
                        len(out1.head.children[0].children) == 1 and
                        len(out1.head.children[0].children[0].children) == 0,
                        "Tree branch improperly formed.")

        out2 = g.required_inputs_for_property(symbols['D'])
        self.assertTrue(out2.head.m is None and out2.head.parent is None and
                        out2.head.inputs == {symbols['D']} and len(out2.head.children) == 2,
                        "Tree head not properly defined.")
        m_map = {x.m: x for x in out2.head.children}
        self.assertTrue(m_map[models['model4']].inputs == {symbols['B'], symbols['C']} and
                        m_map[models['model4']].parent is out2.head,
                        "Tree branch improperly formed.")
        self.assertTrue(m_map[models['model5']].inputs == {symbols['C'], symbols['G']} and
                        m_map[models['model5']].parent is out2.head and
                        len(m_map[models['model5']].children) == 2,
                        "Tree branch improperly formed.")
        m_map_1 = {x.m: x for x in m_map[models['model4']].children}
        m_map_2 = {x.m: x for x in m_map[models['model5']].children}
        self.assertTrue(m_map_1[models['model1']].inputs == {symbols['A']} and
                        m_map_1[models['model1']].parent is m_map[models['model4']] and
                        m_map_1[models['model1']].children == [],
                        "Tree branch improperly formed.")
        self.assertTrue(m_map_2[models['model1']].inputs == {symbols['G'], symbols['A']} and
                        m_map_2[models['model1']].parent is m_map[models['model5']] and
                        len(m_map_2[models['model1']].children) == 1 and
                        m_map_2[models['model1']].children[0].parent is m_map_2[models['model1']] and
                        m_map_2[models['model1']].children[0].children == [] and
                        m_map_2[models['model1']].children[0].inputs == {symbols['A']},
                        "Tree branch improperly formed.")
        self.assertTrue(m_map_2[models['model2']].inputs == {symbols['C'], symbols['A']} and
                        m_map_2[models['model2']].parent is m_map[models['model5']] and
                        len(m_map_2[models['model2']].children) == 1 and
                        m_map_2[models['model2']].children[0].parent is m_map_2[models['model2']] and
                        m_map_2[models['model2']].children[0].children == [] and
                        m_map_2[models['model2']].children[0].inputs == {symbols['A']},
                        "Tree branch improperly formed.")

    def test_symbol_ancestry_cyclic(self):
        """
        Tests the Symbol Ancestry algorithm on a cyclic graph.
        The canonical graph and the canonical material are used for this test.
        """
        symbols = GraphTest.generate_canonical_symbols()
        models = GraphTest.generate_canonical_models(symbols)
        material = GraphTest.generate_canonical_material(symbols)
        g = Graph(symbol_types=symbols, models=models)

        out1 = g.required_inputs_for_property(symbols['F'])

        self.assertTrue(out1.head.m is None and out1.head.parent is None and
                        out1.head.inputs == {symbols['F']} and len(out1.head.children) == 1,
                        "Tree head not properly defined.")
        self.assertTrue(out1.head.children[0].m == models['model3'] and
                        out1.head.children[0].inputs == {symbols['B']} and
                        out1.head.children[0].parent is out1.head and
                        len(out1.head.children[0].children) == 1,
                        "Tree branch improperly formed.")
        self.assertTrue(out1.head.children[0].children[0].m == models['model1'] and
                        out1.head.children[0].children[0].inputs == {symbols['A']} and
                        out1.head.children[0].children[0].parent is out1.head.children[0] and
                        len(out1.head.children[0].children) == 1 and
                        len(out1.head.children[0].children[0].children) == 0,
                        "Tree branch improperly formed.")

        out2 = g.required_inputs_for_property(symbols['D'])
        self.assertTrue(out2.head.m is None and out2.head.parent is None and
                        out2.head.inputs == {symbols['D']} and len(out2.head.children) == 2,
                        "Tree head not properly defined.")
        m_map = {x.m: x for x in out2.head.children}
        self.assertTrue(m_map[models['model4']].inputs == {symbols['B'], symbols['C']} and
                        m_map[models['model4']].parent is out2.head,
                        "Tree branch improperly formed.")
        self.assertTrue(m_map[models['model5']].inputs == {symbols['C'], symbols['G']} and
                        m_map[models['model5']].parent is out2.head and
                        len(m_map[models['model5']].children) == 2,
                        "Tree branch improperly formed.")
        m_map_1 = {x.m: x for x in m_map[models['model4']].children}
        m_map_2 = {x.m: x for x in m_map[models['model5']].children}
        self.assertTrue(m_map_1[models['model1']].inputs == {symbols['A']} and
                        m_map_1[models['model1']].parent is m_map[models['model4']] and
                        m_map_1[models['model1']].children == [],
                        "Tree branch improperly formed.")
        self.assertTrue(m_map_2[models['model1']].inputs == {symbols['G'], symbols['A']} and
                        m_map_2[models['model1']].parent is m_map[models['model5']] and
                        len(m_map_2[models['model1']].children) == 1 and
                        m_map_2[models['model1']].children[0].parent is m_map_2[models['model1']] and
                        m_map_2[models['model1']].children[0].children == [] and
                        m_map_2[models['model1']].children[0].inputs == {symbols['A']},
                        "Tree branch improperly formed.")
        self.assertTrue(m_map_2[models['model2']].inputs == {symbols['C'], symbols['A']} and
                        m_map_2[models['model2']].parent is m_map[models['model5']] and
                        len(m_map_2[models['model2']].children) == 1 and
                        m_map_2[models['model2']].children[0].parent is m_map_2[models['model2']] and
                        m_map_2[models['model2']].children[0].children == [] and
                        m_map_2[models['model2']].children[0].inputs == {symbols['A']},
                        "Tree branch improperly formed.")

    def test_symbol_ancestry_constraint(self):
        """
        Tests the Symbol Ancestry algorithm on a non-cyclic graph with constraints.
        The canonical graph and the canonical material are used for this test.
        """
        class Model4 (AbstractModel):
            def __init__(self, symbol_types=None):
                AbstractModel.__init__(self, metadata=
                    { 'title': 'model4', 'tags': [], 'references': [], 'description': '',
                      'symbol_mapping': {'D': 'D',
                                         'B': 'B',
                                         'C': 'C',
                                         'G': 'G'
                                        },
                      'connections': [{'inputs': ['B', 'C'],
                                       'outputs': ['D']
                                      }],
                      'equations': ['D-B*C*11']
                    },
                    symbol_types=symbol_types)

            @property
            def constraint_symbols(self):
                return ['G']

            def check_constraints(self, constraint_inputs):
                return constraint_inputs['G'] == 0

        symbols = GraphTest.generate_canonical_symbols()
        models = GraphTest.generate_canonical_models(symbols)
        models['model4'] = Model4(symbol_types=symbols)
        del models['model6']
        g = Graph(symbol_types=symbols, models=models)

        out1 = g.required_inputs_for_property(symbols['F'])

        self.assertTrue(out1.head.m is None and out1.head.parent is None and
                        out1.head.inputs == {symbols['F']} and len(out1.head.children) == 1,
                        "Tree head not properly defined.")
        self.assertTrue(out1.head.children[0].m == models['model3'] and
                        out1.head.children[0].inputs == {symbols['B']} and
                        out1.head.children[0].parent is out1.head and
                        len(out1.head.children[0].children) == 1,
                        "Tree branch improperly formed.")
        self.assertTrue(out1.head.children[0].children[0].m == models['model1'] and
                        out1.head.children[0].children[0].inputs == {symbols['A']} and
                        out1.head.children[0].children[0].parent is out1.head.children[0] and
                        len(out1.head.children[0].children) == 1 and
                        len(out1.head.children[0].children[0].children) == 0,
                        "Tree branch improperly formed.")

        out2 = g.required_inputs_for_property(symbols['D'])
        self.assertTrue(out2.head.m is None and out2.head.parent is None and
                        out2.head.inputs == {symbols['D']} and len(out2.head.children) == 2,
                        "Tree head not properly defined.")
        m_map = {x.m: x for x in out2.head.children}
        self.assertTrue(m_map[models['model4']].inputs == {symbols['B'], symbols['C'], symbols['G']} and
                        m_map[models['model4']].parent is out2.head,
                        "Tree branch improperly formed.")
        self.assertTrue(m_map[models['model5']].inputs == {symbols['C'], symbols['G']} and
                        m_map[models['model5']].parent is out2.head and
                        len(m_map[models['model5']].children) == 2,
                        "Tree branch improperly formed.")
        m_map_2 = {x.m: x for x in m_map[models['model5']].children}
        self.assertTrue(m_map_2[models['model1']].inputs == {symbols['G'], symbols['A']} and
                        m_map_2[models['model1']].parent is m_map[models['model5']] and
                        len(m_map_2[models['model1']].children) == 1 and
                        m_map_2[models['model1']].children[0].parent is m_map_2[models['model1']] and
                        m_map_2[models['model1']].children[0].children == [] and
                        m_map_2[models['model1']].children[0].inputs == {symbols['A']},
                        "Tree branch improperly formed.")
        self.assertTrue(m_map_2[models['model2']].inputs == {symbols['C'], symbols['A']} and
                        m_map_2[models['model2']].parent is m_map[models['model5']] and
                        len(m_map_2[models['model2']].children) == 1 and
                        m_map_2[models['model2']].children[0].parent is m_map_2[models['model2']] and
                        m_map_2[models['model2']].children[0].children == [] and
                        m_map_2[models['model2']].children[0].inputs == {symbols['A']},
                        "Tree branch improperly formed.")

        m_map_1 = {x.m: x for x in m_map[models['model4']].children}
        self.assertTrue(m_map_1[models['model1']].inputs == {symbols['G'], symbols['A']} and
                        m_map_1[models['model1']].parent is m_map[models['model4']] and
                        len(m_map_1[models['model1']].children) == 1 and
                        m_map_1[models['model1']].children[0].parent is m_map_1[models['model1']] and
                        m_map_1[models['model1']].children[0].children == [] and
                        m_map_1[models['model1']].children[0].inputs == {symbols['A']},
                        "Tree branch improperly formed.")
        self.assertTrue(m_map_1[models['model2']].inputs == {symbols['B'], symbols['C'], symbols['A']} and
                        m_map_1[models['model2']].parent is m_map[models['model4']] and
                        len(m_map_1[models['model2']].children) == 1 and
                        m_map_1[models['model2']].children[0].parent is m_map_1[models['model2']] and
                        m_map_1[models['model2']].children[0].children == [] and
                        m_map_1[models['model2']].children[0].inputs == {symbols['A']},
                        "Tree branch improperly formed.")

    def test_symbol_ancestry_cyclic_constraint(self):
        """
        Tests the Symbol Ancestry algorithm on a cyclic graph with constraints.
        The canonical graph and the canonical material are used for this test.
        """
        class Model4 (AbstractModel):
            def __init__(self, symbol_types=None):
                AbstractModel.__init__(self, metadata=
                    { 'title': 'model4', 'tags': [], 'references': [], 'description': '',
                      'symbol_mapping': {'D': 'D',
                                         'B': 'B',
                                         'C': 'C',
                                         'G': 'G'
                                        },
                      'connections': [{'inputs': ['B', 'C'],
                                       'outputs': ['D']
                                      }],
                      'equations': ['D-B*C*11']
                    },
                    symbol_types=symbol_types)

            @property
            def constraint_symbols(self):
                return ['G']

            def check_constraints(self, constraint_inputs):
                return constraint_inputs['G'] == 0

        symbols = GraphTest.generate_canonical_symbols()
        models = GraphTest.generate_canonical_models(symbols)
        models['model4'] = Model4(symbol_types=symbols)
        g = Graph(symbol_types=symbols, models=models)

        out1 = g.required_inputs_for_property(symbols['F'])

        self.assertTrue(out1.head.m is None and out1.head.parent is None and
                        out1.head.inputs == {symbols['F']} and len(out1.head.children) == 1,
                        "Tree head not properly defined.")
        self.assertTrue(out1.head.children[0].m == models['model3'] and
                        out1.head.children[0].inputs == {symbols['B']} and
                        out1.head.children[0].parent is out1.head and
                        len(out1.head.children[0].children) == 1,
                        "Tree branch improperly formed.")
        self.assertTrue(out1.head.children[0].children[0].m == models['model1'] and
                        out1.head.children[0].children[0].inputs == {symbols['A']} and
                        out1.head.children[0].children[0].parent is out1.head.children[0] and
                        len(out1.head.children[0].children) == 1 and
                        len(out1.head.children[0].children[0].children) == 0,
                        "Tree branch improperly formed.")

        out2 = g.required_inputs_for_property(symbols['D'])
        self.assertTrue(out2.head.m is None and out2.head.parent is None and
                        out2.head.inputs == {symbols['D']} and len(out2.head.children) == 2,
                        "Tree head not properly defined.")
        m_map = {x.m: x for x in out2.head.children}
        self.assertTrue(m_map[models['model4']].inputs == {symbols['B'], symbols['C'], symbols['G']} and
                        m_map[models['model4']].parent is out2.head,
                        "Tree branch improperly formed.")
        self.assertTrue(m_map[models['model5']].inputs == {symbols['C'], symbols['G']} and
                        m_map[models['model5']].parent is out2.head and
                        len(m_map[models['model5']].children) == 2,
                        "Tree branch improperly formed.")
        m_map_2 = {x.m: x for x in m_map[models['model5']].children}
        self.assertTrue(m_map_2[models['model1']].inputs == {symbols['G'], symbols['A']} and
                        m_map_2[models['model1']].parent is m_map[models['model5']] and
                        len(m_map_2[models['model1']].children) == 1 and
                        m_map_2[models['model1']].children[0].parent is m_map_2[models['model1']] and
                        m_map_2[models['model1']].children[0].children == [] and
                        m_map_2[models['model1']].children[0].inputs == {symbols['A']},
                        "Tree branch improperly formed.")
        self.assertTrue(m_map_2[models['model2']].inputs == {symbols['C'], symbols['A']} and
                        m_map_2[models['model2']].parent is m_map[models['model5']] and
                        len(m_map_2[models['model2']].children) == 1 and
                        m_map_2[models['model2']].children[0].parent is m_map_2[models['model2']] and
                        m_map_2[models['model2']].children[0].children == [] and
                        m_map_2[models['model2']].children[0].inputs == {symbols['A']},
                        "Tree branch improperly formed.")

        m_map_1 = {x.m: x for x in m_map[models['model4']].children}
        self.assertTrue(m_map_1[models['model1']].inputs == {symbols['G'], symbols['A']} and
                        m_map_1[models['model1']].parent is m_map[models['model4']] and
                        len(m_map_1[models['model1']].children) == 1 and
                        m_map_1[models['model1']].children[0].parent is m_map_1[models['model1']] and
                        m_map_1[models['model1']].children[0].children == [] and
                        m_map_1[models['model1']].children[0].inputs == {symbols['A']},
                        "Tree branch improperly formed.")
        self.assertTrue(m_map_1[models['model2']].inputs == {symbols['B'], symbols['C'], symbols['A']} and
                        m_map_1[models['model2']].parent is m_map[models['model4']] and
                        len(m_map_1[models['model2']].children) == 1 and
                        m_map_1[models['model2']].children[0].parent is m_map_1[models['model2']] and
                        m_map_1[models['model2']].children[0].children == [] and
                        m_map_1[models['model2']].children[0].inputs == {symbols['A']},
                        "Tree branch improperly formed.")

    def test_get_path(self):
        """
        Tests the ability to generate all paths from one symbol to another.
        """
        symbols = GraphTest.generate_canonical_symbols()
        models = GraphTest.generate_canonical_models(symbols)
        material = GraphTest.generate_canonical_material(symbols)
        del models['model6']
        g = Graph(symbol_types=symbols, models=models)

        paths_1 = g.get_paths(symbols['A'], symbols['F'])
        paths_2 = g.get_paths(symbols['A'], symbols['D'])

        ans_1 = [SymbolPath({symbols['A']}, [models['model1'], models['model3']])]
        ans_2 = [
                    SymbolPath({symbols['A'], symbols['C']}, [models['model2'], models['model5']]),
                    SymbolPath({symbols['A'], symbols['G']}, [models['model1'], models['model5']]),
                    SymbolPath({symbols['A']}, [models['model1'], models['model4']]),
                    SymbolPath({symbols['A']}, [models['model1'], models['model2'], models['model5']]),
                    SymbolPath({symbols['A']}, [models['model2'], models['model1'], models['model5']])
                ]
        self.assertTrue(len(paths_1) == len(ans_1),
                        "Incorrect paths generated.")
        self.assertTrue(len(paths_2) == len(ans_2),
                        "Incorrect paths generated.")
        for i in paths_1:
            self.assertTrue(i in ans_1,
                            "Incorrect paths generated.")
        for i in paths_2:
            self.assertTrue(i in ans_2,
                            "Incorrect paths generated.")

    def test_get_path_constraint(self):
        """
        Tests the ability to generate all paths from one symbol to another with constraints.
        """
        class Model4 (AbstractModel):
            def __init__(self, symbol_types=None):
                AbstractModel.__init__(self, metadata=
                    { 'title': 'model4', 'tags': [], 'references': [], 'description': '',
                      'symbol_mapping': {'D': 'D',
                                         'B': 'B',
                                         'C': 'C',
                                         'G': 'G'
                                        },
                      'connections': [{'inputs': ['B', 'C'],
                                       'outputs': ['D']
                                      }],
                      'equations': ['D-B*C*11']
                    },
                    symbol_types=symbol_types)

            @property
            def constraint_symbols(self):
                return ['G']

            def check_constraints(self, constraint_inputs):
                return constraint_inputs['G'] == 0

        symbols = GraphTest.generate_canonical_symbols()
        models = GraphTest.generate_canonical_models(symbols)
        models['model4'] = Model4(symbol_types=symbols)
        del models['model6']
        g = Graph(symbol_types=symbols, models=models)

        paths_1 = g.get_paths(symbols['A'], symbols['F'])
        paths_2 = g.get_paths(symbols['A'], symbols['D'])

        ans_1 = [SymbolPath({symbols['A']}, [models['model1'], models['model3']])]

        ans_2 = [
            SymbolPath({symbols['A'], symbols['C']}, [models['model2'], models['model5']]),
            SymbolPath({symbols['A'], symbols['G']}, [models['model1'], models['model5']]),
            SymbolPath({symbols['A'], symbols['C'], symbols['B']}, [models['model2'], models['model4']]),
            SymbolPath({symbols['A'], symbols['G']}, [models['model1'], models['model4']]),
            SymbolPath({symbols['A']}, [models['model1'], models['model2'], models['model5']]),
            SymbolPath({symbols['A']}, [models['model2'], models['model1'], models['model5']]),
            SymbolPath({symbols['A']}, [models['model1'], models['model2'], models['model4']]),
            SymbolPath({symbols['A']}, [models['model2'], models['model1'], models['model4']])
        ]

        self.assertTrue(len(paths_1) == len(ans_1),
                        "Incorrect paths generated.")
        self.assertTrue(len(paths_2) == len(ans_2),
                        "Incorrect paths generated.")
        for i in paths_1:
            self.assertTrue(i in ans_1,
                            "Incorrect paths generated.")
        for i in paths_2:
            self.assertTrue(i in ans_2,
                            "Incorrect paths generated.")
