import os
import random
import re
import subprocess

# Configuration
GEN_SIZE = 5        # Number of mutated chips per generation
GENERATIONS = 10    # How many evolutionary cycles to run
BASE_DESIGN = os.path.expanduser("~/repos/silicon-soul/hardware/plastic_neuron.v")
MUTATION_RATE = 0.05

class EvolutionEngine:
    def __init__(self, base_design):
        self.base_design = base_design
        with open(base_design, 'r') as f:
            self.dna = f.read()
        self.generation = 0

    def mutate(self, code, rate):
        """Randomly alters logic to simulate hardware variation."""
        lines = code.split('\n')
        new_lines = []
        for line in lines:
            if line.strip().startswith('//') or 'module' in line:
                new_lines.append(line)
                continue
            
            if random.random() < rate:
                # Logic Flips
                if '+' in line: line = line.replace('+', random.choice(['-', '*', '+']))
                elif '-' in line: line = line.replace('-', random.choice(['+', '*', '-']))
                elif '>' in line: line = line.replace('>', '<')
                elif '<' in line: line = line.replace('<', '>')
                
                # Parameter Drift
                match = re.search(r"(\d+)'d(\d+)", line)
                if match:
                    width, val = match.groups()
                    new_val = max(0, int(val) + random.randint(-5, 5))
                    line = re.sub(r"\d+'d\d+", f"{width}'d{new_val}", line)
            
            new_lines.append(line)
        return '\n'.join(new_lines)

    def evaluate(self, code):
        """
        Simulates the chip's performance.
        In a real scenario, this would run a Verilog testbench.
        Here, we simulate 'fitness' based on logic integrity.
        """
        # 1. Syntax Check (Does it compile?)
        if "syntax error" in code.lower(): return 0
        
        # 2. Functional Score (Simulated)
        # We want the chip to learn.
        # Ideally, we check if 'weight' converges to a target.
        score = 100
        
        # Penalty for breaking core learning logic
        if "weight <= weight + LEARNING_RATE" not in code and "weight <= weight - LEARNING_RATE" not in code:
            score -= 50 # It forgot how to learn
            
        # Penalty for breaking inference
        if "output_signal <=" not in code:
            score -= 90 # It's brain dead
            
        return max(0, score + random.randint(-10, 10)) # Add noise for realism

    def run(self):
        print(f"🌌 Silicon Evolution Initiated: {GENERATIONS} generations")
        current_best_dna = self.dna
        
        for g in range(1, GENERATIONS + 1):
            print(f"\n--- Generation {g} ---")
            population = []
            
            # Create mutants
            for i in range(GEN_SIZE):
                mutant_dna = self.mutate(current_best_dna, MUTATION_RATE)
                fitness = self.evaluate(mutant_dna)
                population.append((fitness, mutant_dna))
                # print(f"  Chip {i}: Fitness = {fitness}")
            
            # Survival of the Fittest
            population.sort(key=lambda x: x[0], reverse=True)
            best_fitness, best_dna = population[0]
            
            print(f"  🏆 Survivor Fitness: {best_fitness}")
            
            # Evolution: The best becomes the parent for the next generation
            if best_fitness > 0:
                current_best_dna = best_dna
                
                # Save the champion
                filename = os.path.expanduser(f"~/repos/silicon-soul/hardware/plastic_neuron_gen{g}.v")
                with open(filename, 'w') as f:
                    f.write(best_dna)
            else:
                print("  💀 Extinction Event: All mutants failed.")
                break

if __name__ == "__main__":
    engine = EvolutionEngine(BASE_DESIGN)
    engine.run()
