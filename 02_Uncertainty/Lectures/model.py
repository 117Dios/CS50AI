from pomegranate.distributions import Categorical, ConditionalCategorical
from pomegranate.bayesian_network import BayesianNetwork

# Define distributions
rain = Categorical([[0.7, 0.2, 0.1]])  # "none", "light", "heavy"

maintenance = ConditionalCategorical([
    [[0.4, 0.6], [0.2, 0.8], [0.1, 0.9]]  # P(yes, no | rain)
])

train = ConditionalCategorical([
    [  # P(on time, delayed | rain, maintenance)
        [[0.8, 0.2], [0.9, 0.1]],  # rain = none
        [[0.6, 0.4], [0.7, 0.3]],  # rain = light
        [[0.4, 0.6], [0.5, 0.5]]   # rain = heavy
    ]
])

appointment = ConditionalCategorical([
    [[0.9, 0.1], [0.6, 0.4]]  # P(attend, miss | train)
])

# Build the Bayesian Network
model = BayesianNetwork(
    distributions=[rain, maintenance, train, appointment],
    edges=[
        (rain, maintenance),
        (rain, train),
        (maintenance, train),
        (train, appointment)
    ]
)