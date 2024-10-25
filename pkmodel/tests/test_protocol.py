import pytest
import numpy as np
import numpy.testing as npt

@pytest.mark.parametrize(
    "t, expected, expect_raises",
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
        #hours_after_dosing >= duration frequency
        (
            6,
            0,
        ),
    ]
)
def test_dose_outputs(t, expected):
    """Tests that the dose output by a given t value is that expected"""
    import pkmodel as pk
    #How is this called later? 
    #Is there any point at which the args_dict is fed to the model class, 
    # or can this be bypassed for the protocol class?
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
    model.add_dose_t_tophat_params(10,100,1,5)
    npt.assert_equal(model.dose(t), expected)