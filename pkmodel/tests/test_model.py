import pytest

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
                'X': 1.0,
                'ka': 0,
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

@pytest.mark.parametrize(
    "parameters, expect_raises",
    [
        #For Q_p1 below 0
        (
            {
                'name': 'model1',
                'Q_p1': -1.0,
                'V_c': 1.0,
                'V_p1': 1.0,
                'CL': 1.0,
                'ka': 1.0,
                'X': 1.0,
                'Dosing_Type': 'Sub'
            },
            ValueError,
        ),
        #For everything is ok
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
        #For V_c is <= 0
        (
            {
                'name': 'model1',
                'Q_p1': 1.0,
                'V_c': 0,
                'V_p1': 1.0,
                'CL': 1.0,
                'ka': 1.0,
                'X': 1.0,
                'Dosing_Type': 'Sub'
            },
            ValueError,
        ),
        #For V_p1 <= 0
        (
            {
                'name': 'model1',
                'Q_p1': 1.0,
                'V_c': 10,
                'V_p1': 0,
                'CL': 1.0,
                'ka': 1.0,
                'X': 1.0,
                'Dosing_Type': 'Sub'
            },
            ValueError,
        ),
        #For CL < 0
        (
            {
                'name': 'model1',
                'Q_p1': 1.0,
                'V_c': 10,
                'V_p1': 1.0,
                'CL': -7,
                'ka': 1.0,
                'X': 1.0,
                'Dosing_Type': 'Sub'
            },
            ValueError,
        ),
        #For Ka < 0
        (
            {
                'name': 'model1',
                'Q_p1': 1.0,
                'V_c': 10,
                'V_p1': 1.0,
                'CL': 1.0,
                'ka': -1.0,
                'X': 1.0,
                'Dosing_Type': 'Sub'
            },
            ValueError,
        ),
        #For ka 0
        (
            {
                'name': 'model1',
                'Q_p1': 1.0,
                'V_c': 10,
                'V_p1': 1.0,
                'CL': 1.0,
                'ka': 0,
                'X': 1.0,
                'Dosing_Type': 'Bolus'
            },
            None,
        ),
        #Testing ka given but dosage type bolus
        (
            {
                'name': 'model1',
                'Q_p1': 1.0,
                'V_c': 10,
                'V_p1': 1.0,
                'CL': 1.0,
                'ka': 5,
                'X': 1.0,
                'Dosing_Type': 'Bolus'
            },
            UserWarning,
        ),
        #For X is less than 0
        (
            {
                'name': 'model1',
                'Q_p1': 1.0,
                'V_c': 10,
                'V_p1': 1.0,
                'CL': 1.0,
                'ka': 5,
                'X': -1.0,
                'Dosing_Type': 'Sub'
            },
            ValueError,
        ),
        #For X > 1000
        (
            {
                'name': 'model1',
                'Q_p1': 1.0,
                'V_c': 10,
                'V_p1': 1.0,
                'CL': 1.0,
                'ka': 5,
                'X': 1001.0,
                'Dosing_Type': 'Sub'
            },
            UserWarning,
        ),
    ]
)
def test_values_reasonable(parameters, expect_raises):
    """Test the models have reasonable input constants"""
    import pkmodel as pk
    if expect_raises is ValueError:
        with pytest.raises(expect_raises):
            pk.Model(name = 'test', args_dict = parameters)
    elif expect_raises is not None:
        with pytest.warns(expect_raises):
            pk.Model(name = 'test', args_dict = parameters)
    else:
        pk.Model(name = 'test', args_dict = parameters)


@pytest.mark.parametrize(
    "start, stop, duration, freq, expect_raises",
    [
        (
            100, 10, 1, 1,
            ValueError,
        ),
        (
            10, 100, 1, 1,
            None,
        ),
        (
            10, 100, 10, 1,
            ValueError,
        ),
    ]
)
def test_top_hat_inputs(start, stop, duration, freq, expect_raises):
    """Test the models class can correctly assess dose frequencies are reasonable"""
    import pkmodel as pk
    model = pk.Model(name = 'test', args_dict = {
                'name': 'model1',
                'Q_p1': 1.0,
                'V_c': 1.0,
                'V_p1': 1.0,
                'CL': 1.0,
                'X': 1.0,
                'ka': 0,
                'Dosing_Type': 'Bolus'
            },)
    print(start, stop, freq, duration)
    if expect_raises is not None:
        with pytest.raises(expect_raises):
            model.add_dose_t_tophat_params(start, stop, duration, freq)
    else:
        model.add_dose_t_tophat_params(start, stop, duration, freq)