# This parameter denotes which biological system you would like to choose for analysis.
# This string can be a file name in two folders: data/networks and data/transitions. Other commands below will determine this is a file with a Boolean network or with transitions.
BIOLOGICAL_SYSTEM_NAME = "budding_yeast_manuscript"

# This parameter denotes the name of the command for analysis.
# If this is "Complete Transitions Generation", then it means that you are loading a Boolean network as an input, and you call methods to generate all transitions from this Boolean network. The name of the output is the name of the system with a suffix "complete".
# If this is "Analyze Transitions Structure", then it means that you are loading transitions, and you are checking the structure of transitions, such as the number of components and attractors.
# If this is "Strong Inhibition Inference", then it means that you are loading transitions, and you are checking if it can follow Strong Inhibition dynamics or not.
# If this is "Test Belief Propagation", then it means that you are loading no inputs, only fixed testcases of Belief Propagation will run.
COMMAND_NAME = "Strong Inhibition Inference"

# This parameter denotes if you would like to show whether the loading transitions can follow Strong Inhibition dynamics or not.
# This parameter can work only if COMMAND_NAME is "Strong Inhibition Inference".
SHOW_HAS_SOLUTION = True

# This parameter denotes if you would like to show whether the probabilities of green and red edges from all solutions based on Strong Inhibition dynamics or not.
# This parameter can work only if COMMAND_NAME is "Strong Inhibition Inference".
SHOW_REAL_EDGES_PROBABILITIES = True
