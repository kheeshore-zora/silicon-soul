import re
import random
import os

class BitstreamMutator:
    """
    Simulates hardware evolution by randomly mutating Verilog code.
    In a real FPGA context, this would operate on the binary .bit file.
    Here, we operate on the source logic gates to simulate 'rewiring'.
    """
    
    def __init__(self, verilog_path):
        self.path = verilog_path
        with open(self.path, 'r') as f:
            self.original_code = f.read()
        self.current_code = self.original_code

    def mutate(self, mutation_rate=0.05):
        """
        Randomly alters non-critical logic operations.
        - Changes '+' to '-' or '*' (Arithmetic mutation)
        - Changes '>' to '<' (Comparator mutation)
        - Changes constants slightly (Parameter drift)
        """
        print(f"🧬 Mutating {self.path} with rate {mutation_rate}...")
        
        lines = self.current_code.split('\n')
        new_lines = []
        
        for line in lines:
            # Skip comments and module definitions (don't break the file structure)
            if line.strip().startswith('//') or 'module' in line or 'endmodule' in line:
                new_lines.append(line)
                continue
                
            # Mutation Logic
            if random.random() < mutation_rate:
                # 1. Flip Arithmetic
                if '+' in line:
                    line = line.replace('+', random.choice(['-', '*', '+'])) # 33% chance to change
                    print(f"  -> Mutated Arithmetic: {line.strip()}")
                elif '-' in line:
                    line = line.replace('-', random.choice(['+', '*', '-']))
                    print(f"  -> Mutated Arithmetic: {line.strip()}")
                    
                # 2. Flip Comparators
                if '>' in line:
                    line = line.replace('>', '<')
                    print(f"  -> Mutated Comparator: {line.strip()}")
                elif '<' in line:
                    line = line.replace('<', '>')
                    print(f"  -> Mutated Comparator: {line.strip()}")
                    
                # 3. Parameter Drift (Simulating atomic drift)
                # Finds numbers like 16'd10 and tweaks them
                match = re.search(r"(\d+)'d(\d+)", line)
                if match:
                    width, val = match.groups()
                    new_val = int(val) + random.randint(-2, 2) # Drift by +/- 2
                    new_val = max(0, new_val) # Keep positive
                    line = re.sub(r"\d+'d\d+", f"{width}'d{new_val}", line)
                    print(f"  -> Mutated Parameter: {line.strip()}")

            new_lines.append(line)
            
        self.current_code = '\n'.join(new_lines)
        return self.current_code

    def save(self, output_path):
        with open(output_path, 'w') as f:
            f.write(self.current_code)
        print(f"💾 Saved mutated bitstream to {output_path}")

# --- Test Run ---
if __name__ == "__main__":
    base_path = os.path.expanduser("~/repos/silicon-soul/hardware/plastic_neuron.v")
    mutator = BitstreamMutator(base_path)
    
    # Evolve generation 1
    mutator.mutate(mutation_rate=0.1)
    mutator.save(os.path.expanduser("~/repos/silicon-soul/hardware/plastic_neuron_gen1.v"))
