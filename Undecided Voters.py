import numpy as np

# Define the weights for each characteristic
unifier_weight = 1.0
integrity_weight = 1.5  # Weighs more than other characteristics
accountability_weight = 1.0
# ... Add more weights for other characteristics

# Define the scores for each party on each characteristic
ND_unifier_score = 60
ND_integrity_score = 70
ND_accountability_score = 50
# ... Add more scores for other characteristics

SYRIZA_unifier_score = 50
SYRIZA_integrity_score = 60
SYRIZA_accountability_score = 40
# ... Add more scores for other characteristics

# ... Repeat for other parties

# Calculate the reputation scores by multiplying each characteristic score by its weight and summing up
ND_reputation = unifier_weight * ND_unifier_score + integrity_weight * ND_integrity_score + accountability_weight * ND_accountability_score # + ...
SYRIZA_reputation = unifier_weight * SYRIZA_unifier_score + integrity_weight * SYRIZA_integrity_score + accountability_weight * SYRIZA_accountability_score # + ...
# ... Repeat for other parties

# Calculate the total reputation scores for all parties
total_reputation = ND_reputation + SYRIZA_reputation # + ...

# Define the poll results
poll_results = {
    'ND': 35.0,
    'SYRIZA': 30.0,
    'Undecided': 10.0
}

# Calculate the final results
final_results = {}
for party, result in poll_results.items():
    if party == 'Undecided':
        continue
    reputation = ND_reputation if party == 'ND' else SYRIZA_reputation  # update this line to fetch the correct reputation for each party
    final_results[party] = result + poll_results['Undecided'] * (reputation / total_reputation) + np.random.normal(0, 1)

# Print the final results
for party, result in final_results.items():
    print(f"{party}: {result}%")
