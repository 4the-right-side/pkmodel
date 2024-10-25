import pytest
import numpy as np
import numpy.testing as npt

@pytest.mark.parametrize(
    "t, expected",
    [
        #t < start_h
        (
            0.5,
            0,
        ),
        #t > stop_h
        (
            101,
            0,
        ),
        #t == stop_h == n*(freq_h)
        (
            100,
            1.0, #Value of X given in the args_dict
        ),
        #hours_after_dosing = duration frac
        (
            6,
            1, #unusual, presumably because of floats
        ),
        #hours_after_dosing > duration frac
        (
            7,
            0,
        ),
        #hours_after_dosing < duration frac
        (
            5.3,
            1,
        ),
        #hours_after_dosing < duration frac
        (
            10.3,
            1,
        ),
    ]
)
def test_dose_outputs(t, expected):
    """Tests that the dose output by a given t value is that expected"""
    import pkmodel as pk
    model = pk.Protocol(args_dict = {
                'name': 'model1',
                'Q_p1': 1.0,
                'V_c': 1.0,
                'V_p1': 1.0,
                'CL': 1.0,
                'X': 1.0,
                'ka': 0,
                'Dosing_Type': 'Bolus'
            },)
    #This function's inputs have been checked in the previous section
    model.add_dose_t_tophat_params(5,100,1,5)
    print(model)
    npt.assert_equal(model.dose(t), expected)
