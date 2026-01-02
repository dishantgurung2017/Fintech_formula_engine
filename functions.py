def delinquency_count(inputs):
    return 2

def debt_to_income(inputs):
    return inputs['debt'] / inputs['income']

def discount(inputs):
    if inputs['employment_type'] == 'MNC':
        return 100
    else: return 0
