import os
import random
import re
import math

# Configuration
GEN_SIZE = 10
GENERATIONS = 20
BASE_DESIGN = os.path.expanduser("~/repos/silicon-soul/hardware/plastic_neuron.v")

class HardwareSim:
    """
    Simulates the logic described in the Verilog file using Python.
    This bridges the gap since we don't have a Verilog compiler installed.
    """
    def __init__(self, verilog_code):
        self.code = verilog_code
        self.weight = 0
        self.learning_rate = 0
        self.operator = '*' # Default inference op
        self.learn_op = '+' # Default learn op
        self.parse_config()

    def parse_config(self):
        """Extracts 'hardware' parameters from the text file."""
        # 1. Parse Initial Weight
        # Look for: weight <= 16'd1000;
        w_match = re.search(r"weight <= \d+'d(\d+);", self.code)
        if w_match: self.weight = int(w_match.group(1))
        else: self.weight = 1000 # Fallback

        # 2. Parse Learning Rate
        # Look for: parameter LEARNING_RATE = 16'd10;
        lr_match = re.search(r"parameter LEARNING_RATE = \d+'d(\d+);", self.code)
        if lr_match: self.learning_rate = int(lr_match.group(1))
        else: self.learning_rate = 10

        # 3. Parse Logic Operators (Mutation detection)
        # Inference: output_signal <= ... input_signal * weight
        if "input_signal + weight" in self.code: self.operator = '+'
        elif "input_signal - weight" in self.code: self.operator = '-'
        else: self.operator = '*'

        # Learning: weight <= weight + LEARNING_RATE
        if "weight - LEARNING_RATE" in self.code and "weight + LEARNING_RATE" not in self.code:
            self.learn_op = '-' # It learned to forget?

    def run_cycle(self, input_val, feedback_val, cycles=10):
        """Runs the neuron for N cycles."""
        results = []
        for _ in range(cycles):
            # Hardware Inference
            if self.operator == '*': output = input_val * self.weight
            elif self.operator == '+': output = input_val + self.weight
            elif self.operator == '-': output = input_val - self.weight
            else: output = 0
            
            results.append(output)

            # Hardware Plasticity (Hebbian)
            # If input > 0 and feedback > 0: weight += LR
            if input_val > 0 and feedback_val > 0:
                if self.learn_op == '+': self.weight += self.learning_rate
                elif self.learn_op == '-': self.weight -= self.learning_rate
        
        return results

class EvolutionEngine:
    def __init__(self, base_design):
        self.base_design = base_design
        with open(base_design, 'r') as f:
            self.dna = f.read()

    def mutate(self, code):
        """Mutates parameters and logic operators."""
        lines = code.split('\n')
        new_lines = []
        for line in lines:
            # Skip comments
            if line.strip().startswith('//'): 
                new_lines.append(line)
                continue

            # 5% Mutation Rate
            if random.random() < 0.05:
                # Mutate Operators
                if '*' in line: line = line.replace('*', random.choice(['+', '-']))
                elif '+' in line and "weight" in line: line = line.replace('+', '-') # Flip learning direction
                
                # Mutate Constants
                match = re.search(r"(\d+)'d(\d+)", line)
                if match:
                    width, val = match.groups()
                    new_val = max(1, int(val) + random.randint(-50, 50))
                    line = re.sub(r"\d+'d\d+", f"{width}'d{new_val}", line)
            
            new_lines.append(line)
        return '\n'.join(new_lines)

    def evaluate_fitness(self, sim):
        """
        Task: Dynamic Target Seeking (Harder)
        The chip must handle varied inputs, not just a static '10'.
        
        Input: [10, 5, 20]
        Target Output: Input * 2000
        
        This forces the chip to evolve a MULTIPLIER, not an ADDER.
        (10+2000 != 10*2000, but 10*2000 == 20000)
        """
        test_inputs = [10, 5, 20]
        total_error = 0
        
        for input_val in test_inputs:
            target_output = input_val * 2000 # The "Function" we want it to learn
            
            # Run for 10 cycles per input
            outputs = sim.run_cycle(input_val, 1, cycles=10)
            final_output = outputs[-1]
            
            total_error += abs(target_output - final_output)
        
        # Fitness: Higher is better. 
        if total_error == 0: return 1000
        return 100000 / (total_error + 1)

    def run(self):
        print(f"🌌 Silicon Evolution: Task 'Target Seeking' initiated.")
        current_best_dna = self.dna
        
        for g in range(1, GENERATIONS + 1):
            population = []
            
            for i in range(GEN_SIZE):
                mutant_dna = self.mutate(current_best_dna)
                sim = HardwareSim(mutant_dna)
                fitness = self.evaluate_fitness(sim)
                population.append((fitness, mutant_dna, sim))
            
            # Selection
            population.sort(key=lambda x: x[0], reverse=True)
            best_fitness, best_dna, best_sim = population[0]
            
            print(f"Gen {g}: Best Fitness = {best_fitness:.4f} | W:{best_sim.weight} LR:{best_sim.learning_rate} Op:{best_sim.operator}")
            
            # Evolution
            current_best_dna = best_dna
            
            # Save Survivor
            if g % 5 == 0:
                with open(os.path.expanduser(f"~/repos/silicon-soul/hardware/survivor_gen{g}.v"), 'w') as f:
                    f.write(best_dna)

if __name__ == "__main__":
    engine = EvolutionEngine(BASE_DESIGN)
    engine.run()
