def compare_quantitative (guess_val, secret_val, label):
    ratio = secret_val/guess_val
    if ratio <0.9: return f"{label}: ⏫ should be higher"
    elif ratio <1.1:  return f"{label}: approximately right!"
    else: return f"{label}: ⏬ should be lower"

def compare_qualitative(guess_val, secret_val, label):
    if guess_val == secret_val: return f"{label}: RIGHT!"
    else: return f"{label}: wrong :( "

def get_value(country, label):
    pass