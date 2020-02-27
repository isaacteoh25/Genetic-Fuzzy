import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

class Fuzzy:
    def __init__ (self, ES, AD):
        self.AD = AD
        self.ES = ES

    def fuzzy_output (self):
        EvolutionaryProcess = ctrl.Antecedent(np.arange(0, 3.05, 0.02), 'ES')
        averageDiversity = ctrl.Antecedent(np.arange(0, 1.05, 0.1), 'AD')
        mutation = ctrl.Consequent(np.arange(0, 0.205, 0.01), 'mutation')

        # Auto-membership function population is possible with .automf(3, 5, or 7)
        # EvolutionaryProcess.automf(3)
        # averageDiversity.automf(3)
        EvolutionaryProcess ['low'] = fuzz.trapmf(EvolutionaryProcess.universe, [0, 0, 0.5, 1])
        EvolutionaryProcess ['medium'] = fuzz.trimf(EvolutionaryProcess.universe, [0.8, 1.4, 2])
        EvolutionaryProcess ['high'] = fuzz.trapmf(EvolutionaryProcess.universe, [1.8, 2.4, 3, 3])
        averageDiversity ['low'] = fuzz.trapmf(averageDiversity.universe, [0, 0, 0.1,0.3])
        averageDiversity ['medium'] = fuzz.trimf(averageDiversity.universe, [0.2, 0.4, 0.6])
        averageDiversity ['high'] = fuzz.trapmf(averageDiversity.universe, [0.4, 0.7, 1, 1])

        # Custom membership functions can be built interactively with a familiar,
        # Pythonic API
        # mutation['lower'] = fuzz.trapmf(mutation.universe, [0, 0, 0.01, 0.02])
        # mutation['low'] = fuzz.trimf(mutation.universe, [0.01, 0.03, 0.05])
        # mutation['medium'] = fuzz.trimf(mutation.universe, [0.04, 0.06, 0.08])
        # mutation['high'] = fuzz.trimf(mutation.universe, [0.07, 0.09, 0.12])
        # mutation['higher'] = fuzz.trapmf(mutation.universe, [0.1, 0.15, 0.2, 0.2])

        mutation['lower'] = fuzz.trapmf(mutation.universe, [0, 0, 0.05, 0.1])
        mutation['low'] = fuzz.trimf(mutation.universe, [0.08, 0.1, 0.12])
        mutation['medium'] = fuzz.trimf(mutation.universe, [0.11, 0.13, 0.15])
        mutation['high'] = fuzz.trimf(mutation.universe, [0.14, 0.16, 0.18])
        mutation['higher'] = fuzz.trapmf(mutation.universe, [0.17, 0.18, 0.2, 0.2])
        # EvolutionaryProcess.view()
        # averageDiversity.view()
        # mutation.view()

        rule1 = ctrl.Rule(EvolutionaryProcess['high'], mutation['low'])
        rule2 = ctrl.Rule(EvolutionaryProcess['medium'] | averageDiversity['medium'], mutation['medium'])
        rule3 = ctrl.Rule(EvolutionaryProcess['medium'] | averageDiversity['low'], mutation['high'])
        rule4 = ctrl.Rule(EvolutionaryProcess['medium'] | averageDiversity['high'], mutation['low'])
        rule5 = ctrl.Rule(EvolutionaryProcess['low'] | averageDiversity['low'], mutation['lower'])
        rule6 = ctrl.Rule(EvolutionaryProcess['low'] | averageDiversity['medium'], mutation['medium'])
        rule7 = ctrl.Rule(EvolutionaryProcess['low'] | averageDiversity['high'], mutation['high'])
        rule1.view()

        tipping_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7])
        tipping = ctrl.ControlSystemSimulation(tipping_ctrl)
        # Pass inputs to  ControlSystem using Antecedent labels with Pythonic API
        # Note: if you like passing many inputs all at once, use .inputs(dict_of_data)
        # tipping.input['ES'] = 1.0074484670015589
        # tipping.input['AD'] = 0.5

        tipping.input['ES'] = self.ES
        tipping.input['AD'] = self.AD
        # Crunch the numbers
        tipping.compute()
        print(tipping.output['mutation'])
        # mutation.view(sim=tipping)

        return tipping.output['mutation']