import json

with open("edited_country_data.json", "r", encoding="utf-8") as f:
    File = json.load(f)

Quantity_labels = ["population", "area"]
Quality_labels = ["name", "subregion", "landlocked"]
def compare_quantitative (guess_val, secret_val, label):
    ratio = (secret_val)/(guess_val)
    if ratio <0.9: return f"{label}: ⏫ should be higher"
    elif ratio <1.1:  return f"{label}: approximately right!"
    else: return f"{label}: ⏬ should be lower"

def compare_qualitative(guess_val, secret_val, label):
    if guess_val == secret_val: return f"{label}: RIGHT!"
    else: return f"{label}: wrong :( "

def get_value(id, label):
    return(File[id][label])


def id(country):
    for i in range(len(File["data"])):
        if i["name"] == country:
            return i

def compare(guess, secret):
    secret_id = id(secret)
    guess_id = id(guess)
    for label in Quality_labels:
        guess_val = get_value(label, guess_id)
        secret_val = get_value(label, secret_id)
        compare_qualitative(guess_val, secret_val, label)
    for label in Quantity_labels:
        guess_val = get_value(label, guess_id)
        secret_val = get_value( label, secret_id)
        compare_quantitative(guess_val, secret_val, label)