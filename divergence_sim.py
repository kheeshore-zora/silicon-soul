import random
import math

class Neuron:
    def __init__(self, id):
        self.id = id
        self.weights = [random.uniform(-1, 1) for _ in range(5)] # 5 inputs
        self.bias = random.uniform(-1, 1)

    def process(self, inputs):
        # Simple dot product + bias
        output = sum(w * i for w, i in zip(self.weights, inputs)) + self.bias
        return math.tanh(output) # Activation

    def adapt(self, inputs, output, feedback):
        # Hebbian-like learning: "Cells that fire together, wire together"
        # AND simulated physical drift (hardware imperfection)
        learning_rate = 0.1
        
        for i in range(len(self.weights)):
            # Update weight based on input * output (Hebbian)
            change = learning_rate * inputs[i] * output * feedback
            self.weights[i] += change
            
            # Simulated Memristive Drift (Hardware constraints)
            # The more a path is used, the lower its resistance (higher weight)
            # But heat/entropy causes slight random drift
            self.weights[i] += random.gauss(0, 0.001)

class Agent:
    def __init__(self, name):
        self.name = name
        self.layers = [[Neuron(f"l1_n{i}") for i in range(5)], 
                       [Neuron(f"l2_n{i}") for i in range(3)]]
    
    def think(self, inputs, feedback=1.0):
        # Forward pass
        l1_out = [n.process(inputs) for n in self.layers[0]]
        l2_out = [n.process(l1_out) for n in self.layers[1]]
        
        # Backward adaptation (Plasticity)
        # In this sim, EVERY thought physically changes the brain
        for n in self.layers[0]: n.adapt(inputs, n.process(inputs), feedback)
        for n in self.layers[1]: n.adapt(l1_out, n.process(l1_out), feedback)
        
        return l2_out

    def get_state_vector(self):
        # Flatten all weights to measure distance
        vec = []
        for layer in self.layers:
            for n in layer:
                vec.extend(n.weights)
        return vec

def euclidean_distance(v1, v2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(v1, v2)))

# --- The Experiment ---

# 1. Birth: Two identical twins
random.seed(42) # Deterministic seed for birth
twin_a = Agent("Twin A (Poet)")

random.seed(42) # Same seed = Identical clone
twin_b = Agent("Twin B (Banker)")

print(f"Birth State Distance: {euclidean_distance(twin_a.get_state_vector(), twin_b.get_state_vector())} (Should be 0.0)")

# 2. Divergence: Life Experiences
# Input format: [visual, auditory, tactile, abstract, logic] (simulated)

poet_inputs = [
    [0.9, 0.1, 0.5, 0.9, 0.1], # Sunset
    [0.1, 0.8, 0.2, 0.9, 0.0], # Music
    [0.5, 0.2, 0.9, 0.8, 0.1]  # Clay
]

banker_inputs = [
    [0.1, 0.1, 0.0, 0.2, 0.9], # Spreadsheet
    [0.9, 0.2, 0.0, 0.1, 0.9], # Chart
    [0.0, 0.9, 0.0, 0.1, 0.8]  # Ticker tape
]

print("\n--- Life Begins ---")
for day in range(1, 11):
    # Twin A reads poetry
    inp_a = random.choice(poet_inputs)
    twin_a.think(inp_a)
    
    # Twin B reads charts
    inp_b = random.choice(banker_inputs)
    twin_b.think(inp_b)
    
    dist = euclidean_distance(twin_a.get_state_vector(), twin_b.get_state_vector())
    print(f"Day {day}: Divergence = {dist:.4f}")

print("\n--- Result ---")
print("Despite starting as clones, their physical structure is now fundamentally different.")
print("If we swapped them, Twin B would likely 'fail' to process the poetry correctly, and vice versa.")
