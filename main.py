import numpy as np
import matplotlib.pyplot as plt

# Set the number of simulations
n_simulations = 1000000

# Set the polling data (mean and standard deviation)
# Using the average of the three polls
ND_mean = (34.0 + 36.5 + 35.0) / 3
SYRIZA_mean = (33.0 + 29.5 + 30.0) / 3
PASOK_mean = (9.0 + 10.3 + 10.5) / 3
KKE_mean = (6.0 + 6.8 + 7.5) / 3
EL_mean = (4.8 + 3.7 + 3.5) / 3
MeRA25_mean = (3.8 + 3.7 + 4.0) / 3

# Define the max vote percentages
ND_max = 38
SYRIZA_max = 34
PASOK_max = 10
KKE_max = 7
EL_max = 5
MeRA25_max = 5

# Assuming a 3% margin of error for all parties
margin_of_error = 3

# Set the proportion of undecided voters
undecided = 0.12

# Define party labels
party_labels = np.array(['ND', 'SYRIZA', 'PASOK', 'KKE', 'EL', 'MeRA25'])
left_wing = np.array([False, True, False, True, False, True])
right_wing = np.array([True, False, False, False, True, False])

# Initial values for the while loop
rerun_election = True
while rerun_election:
    # Run the Monte Carlo simulations
    ND_votes = np.random.normal(ND_mean, margin_of_error, n_simulations)
    SYRIZA_votes = np.random.normal(SYRIZA_mean, margin_of_error, n_simulations)
    PASOK_votes = np.random.normal(PASOK_mean, margin_of_error, n_simulations)
    KKE_votes = np.random.normal(KKE_mean, margin_of_error, n_simulations)
    EL_votes = np.random.normal(EL_mean, margin_of_error, n_simulations)
    MeRA25_votes = np.random.normal(MeRA25_mean, margin_of_error, n_simulations)

    # Cap the votes at the max percentages
    ND_votes = np.minimum(ND_votes, ND_max)
    SYRIZA_votes = np.minimum(SYRIZA_votes, SYRIZA_max)
    PASOK_votes = np.minimum(PASOK_votes, PASOK_max)
    KKE_votes = np.minimum(KKE_votes, KKE_max)
    EL_votes = np.minimum(EL_votes, EL_max)
    MeRA25_votes = np.minimum(MeRA25_votes, MeRA25_max)

    # Stack the votes
    votes = np.stack([ND_votes, SYRIZA_votes, PASOK_votes, KKE_votes, EL_votes, MeRA25_votes], axis=0)

    # Define the reputation scores for each party
    ND_reputation = 60  # Change these values based on your own assessment
    SYRIZA_reputation = 50
    PASOK_reputation = 40
    KKE_reputation = 45
    EL_reputation = 35
    MeRA25_reputation = 55

    # Define the standard deviation for the noise
    noise_std_dev = 5  # Change this value based on how much randomness you want to introduce

    reputation_scores = np.array(
        [ND_reputation, SYRIZA_reputation, PASOK_reputation, KKE_reputation, EL_reputation, MeRA25_reputation])

    # Add noise to the reputation scores
    reputation_scores = reputation_scores + np.random.normal(0, noise_std_dev, size=reputation_scores.shape)

    # Ensure the reputation scores are not less than zero
    reputation_scores = np.maximum(reputation_scores, 0)

    # Distribute undecided votes proportionally to the reputation scores
    undecided_votes = np.random.uniform(0, 1, n_simulations) * undecided
    votes = votes + (undecided_votes * (reputation_scores[:, np.newaxis] / np.sum(reputation_scores)))

    # If any party hits their max, trigger a re-election
    if np.any(votes >= np.array([ND_max, SYRIZA_max, PASOK_max, KKE_max, EL_max, MeRA25_max])[:, np.newaxis]):
        # Sum the votes of left-wing and right-wing parties
        left_votes = np.sum(votes[left_wing], axis=0)
        right_votes = np.sum(votes[right_wing], axis=0)

        # Reassign the votes to the left and right wing
        votes = np.stack([right_votes, left_votes], axis=0)
        party_labels = np.array(['Right Wing', 'Left Wing'])

        # Break the loop
        rerun_election = False
    else:
        # If no party hit their max, break the loop
        rerun_election = False

    # Calculate the vote percentages
    vote_percentages = votes / np.sum(votes, axis=0)

    # Calculate the mean and standard deviation of the vote percentages
    vote_percentage_means = np.mean(vote_percentages, axis=1)
    vote_percentage_stds = np.std(vote_percentages, axis=1)

    # Plot the results
    plt.figure(figsize=(10, 6))
    for i, party_label in enumerate(party_labels):
        plt.hist(vote_percentages[i], bins=100, alpha=0.6,
                 label=f'{party_label} (mean = {vote_percentage_means[i]:.2f}, std = {vote_percentage_stds[i]:.2f})')
    plt.legend()
    plt.xlabel('Vote Percentage')
    plt.ylabel('Frequency')
    plt.title('Monte Carlo Simulation of Election Results')
    plt.show()