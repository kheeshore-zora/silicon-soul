# Phase 2: Hardware Architecture ⚡

## The "Plastic Neuron" (Verilog)
We have drafted `plastic_neuron.v`, a hardware description of a neuron that physically adapts.

### How it works on FPGA vs ASIC
1.  **FPGA (Field Programmable Gate Array):**
    *   **Current Code:** Updates a `weight` register. This is "parameter updating" (standard AI).
    *   **True Silicon Soul Goal:** Use **Dynamic Partial Reconfiguration (DPR)**. Instead of updating a variable, we update the *circuit*. We generate a new "Bitstream" (the file that tells the FPGA how to wire itself) on the fly.
    *   *Analogy:* Standard AI changes the furniture in the room. Silicon Soul tears down the walls and builds new rooms.

2.  **Memristors (The Holy Grail):**
    *   In a memristor, resistance ($R$) changes with current ($I$).
    *   $R(t) = R(0) + k \int I(t) dt$
    *   The "memory" is the physical atomic arrangement of the material (e.g., Titanium Dioxide TiO2).
    *   If power is cut, the soul remains. It is non-volatile.

## Next Experiments
1.  **Simulation:** Run a Verilog testbench to see the weights drift.
2.  **Bitstream Mutator:** Write a script that takes the compiled Verilog and randomly "mutates" non-critical logic gates, simulating organic evolution.
