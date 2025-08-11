from qiskit import QuantumCircuit
from utils import * # type: ignore
import numpy as np


## Benchmark circuit names
Benchmarks = ["10_sqn",
              "10_sym9",
              "11_sym9",
              "11_wim",
              "11_z4",
              "12_cycle10",
              "12_rd84",
              "12_sym9",
              "13_dist",
              "13_radd",
              "13_root",
              "14_clip",
              "14_cm42a",
              "14_cm85a",
              "15_co14",
              "15_misex1",
              "15_sqrt7",
              "16_inc",
              "16_ising",
              "16_mlp4"]


def InteractionMatrix (qasm_file_path):
    # Load the circuit
    qc = QuantumCircuit.from_qasm_file(qasm_file_path)
    num_qubits = qc.num_qubits

    # Initialize the interaction matrix F
    F = np.zeros((num_qubits, num_qubits), dtype=int)

    # Count two-qubit gates and populate the interaction matrix
    two_qubit_gate_count = 0

    for instruction in qc.data:

        qubits = instruction.qubits

        if len(qubits) == 2:
            qubit_indices = [qubit._index for qubit in qubits]
            i, j = qubit_indices
            if (i != j):
                two_qubit_gate_count += 1  
                F[i, j] += 1
                F[j, i] += 1

    print(f"Loaded circuit '{qasm_file_path}' with {num_qubits} qubits and {two_qubit_gate_count} two-qubit gates.")

    return F


k = 0

for bench in Benchmarks:

    input_file_path = "../circuits/" + bench + ".qasm"

    output_file_path = "../inter/" + bench + ".csv"

    SaveMatrix_csv(InteractionMatrix(input_file_path), output_file_path)

    k += 1

print(f"Succesfully loaded {k} circuits")
