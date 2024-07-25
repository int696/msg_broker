def control_f(operator, column, status=0):
    f = operator.get_energy_storage_system()['F']
    settings = operator.get_setting()
    if settings['f_min_3'] >= f >= settings['f_max_1']:
        print(f'Останов эксперимента operator.update_control_signal({column}, {status})')
        operator.update_control_signal(column, status)
