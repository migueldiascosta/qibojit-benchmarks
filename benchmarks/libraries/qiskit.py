from benchmarks.libraries import abstract


class Qiskit(abstract.AbstractBackend):

    def __init__(self, max_qubits=0):
        import qiskit
        from qiskit.providers.aer import StatevectorSimulator
        self.name = "qiskit"
        self.__version__ = qiskit.__version__
        self.precision = "double"
        self.max_qubits = max_qubits
        self.simulator = StatevectorSimulator(
            fusion_enable=max_qubits > 0,
            fusion_max_qubit=max_qubits,
            fusion_threshold=1
            )

    def from_qasm(self, qasm):
        from qiskit import QuantumCircuit
        # TODO: Consider using `circ = transpile(circ, simulator)`
        return QuantumCircuit.from_qasm_str(qasm)

    def __call__(self, circuit):
        result = self.simulator.run(circuit).result()
        return result.get_statevector(circuit)

    def get_precision(self):
        return self.precision

    def set_precision(self, precision):
        from qiskit.providers.aer import StatevectorSimulator
        self.precision = precision
        self.options["precision"] = precision
        self.simulator = StatevectorSimulator(**self.options)

    def get_device(self):
        return None


class QiskitGpu(Qiskit):

    def __init__(self, max_qubits=0):
        from qiskit.providers.aer import StatevectorSimulator
        super().__init__(max_qubits)
        self.name = "qiskit-gpu"
        self.simulator = StatevectorSimulator(
            device="GPU",
            fusion_enable=max_qubits > 0,
            fusion_max_qubit=max_qubits,
            fusion_threshold=1
            )
