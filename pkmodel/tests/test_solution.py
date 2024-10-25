# import unittest
# import pkmodel as pk
import pytest

from os.path import isfile
import numpy as np

def test_solve():
    import pkmodel as pk
    model = {
                'name': 'model1',
                'Q_p1': 1.0,
                'V_c': 1.0,
                'V_p1': 1.0,
                'CL': 1.0,
                'X': 1.0,
                'ka': 0,
                'Dosing_Type': 'Bolus'
            }
    t_eval = np.linspace( 0 ,10 ,10000)
    y0 = np.array([0.0, 0, 0])
    sol = pk.Solution(args_dict = model, t_eval= t_eval , y0 = y0)
    sol.define_peripheral_compartments(1)
    sol.solve()
    assert isfile("model1.npz") == True

def test_plot():
    import pkmodel as pk
    model = {
                'name': 'model1',
                'Q_p1': 1.0,
                'V_c': 1.0,
                'V_p1': 1.0,
                'CL': 1.0,
                'X': 1.0,
                'ka': 0,
                'Dosing_Type': 'Bolus'
            }
    t_eval = np.linspace( 0 ,10 ,10000)
    y0 = np.array([0.0, 0, 0])
    sol = pk.Solution(args_dict = model, t_eval= t_eval , y0 = y0)
    sol.define_peripheral_compartments(1)
    sol.solve()
    sol.Plot()
    assert isfile("model1.png") == True

