import numpy as np
from pomegranate.distributions import Categorical
from pomegranate.hmm import DenseHMM

# Stati e osservazioni
states = ["sun", "rain"]
observations = ["umbrella", "no umbrella"]

# Mapping osservazioni (opzionale)
obs_to_index = {obs: i for i, obs in enumerate(observations)}
index_to_state = {i: state for i, state in enumerate(states)}

# Distribuzioni di emissione (P(obs | state))
sun = Categorical(np.array([[0.2, 0.8]]))   # P(umbrella | sun), P(no umbrella | sun)
rain = Categorical(np.array([[0.9, 0.1]]))  # P(umbrella | rain), P(no umbrella | rain)

# Lista di distribuzioni, una per stato
emissions = [sun, rain]

# Matrice di transizione
transitions = np.array([
    [0.8, 0.2],  # sun → sun, sun → rain
    [0.3, 0.7]   # rain → sun, rain → rain
])

# Probabilità iniziali
starts = np.array([0.5, 0.5])

# Probabilità di uscita (facoltativa, può essere zero)
ends = np.array([0.0, 0.0])

# Costruzione del modello HMM
model = DenseHMM(
    distributions=emissions,
    edges=transitions,
    starts=starts,
    ends=ends
)
