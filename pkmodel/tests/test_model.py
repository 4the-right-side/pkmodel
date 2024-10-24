import unittest
import pytest
import pkmodel as pk




def test_create(self):
    """
    Tests Model creation.
    """
    model = pk.Model()
    self.assertEqual(model.value, 42)

#Test models:
#Model1 - Sub, functional
#Model2 - Bolus, functional
#Model3 - Injection, functional
#Model4 - No 
@pytest.mark.parametrize(
    "parameters, expect_raises",
    [
        (
            {
                'name': 'model1',
                'Q_p1': 1.0,
                'V_c': 1.0,
                'V_p1': 1.0,
                'CL': 1.0,
                'ka': 1.0,
                'X': 1.0,
                'Dosing_Type': 'Injection'
            },
            ValueError,
        ),
        (
            {
                'name': 'model1',
                'Q_p1': 1.0,
                'V_c': 1.0,
                'V_p1': 1.0,
                'CL': 1.0,
                'ka': 1.0,
                'X': 1.0,
                'Dosing_Type': 'Sub'
            },
            None,
        ),
        (
            {
                'name': 'model1',
                'Q_p1': 1.0,
                'V_c': 1.0,
                'V_p1': 1.0,
                'CL': 1.0,
                'ka': 1.0,
                'X': 1.0,
                'Dosing_Type': 'Bolus'
            },
            None,
        ),
    ]
)
def test_dosing_type(parameters, expect_raises):
    """Test the models class can correctly assess dosing type"""
    print(parameters)
    print(expect_raises)
    import pkmodel as pk
    if expect_raises is not None:
        with pytest.raises(ValueError):
            pk.Model(name = 'test', args_dict = parameters)
    else:
        pk.Model(name = 'test', args_dict = parameters)
