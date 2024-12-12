from algo_tester import AlgorithmTester
from argument_generator import ArgumentGenerator

# Example Algorithm: Sort a list
# We will use Python's built-in sort for demonstration, but you can replace this with any function.
def my_algorithm(arr):
    # Example: A simple sort for demonstration
    return sorted(arr)

if __name__ == "__main__":
    # Initialize the classes
    tester = AlgorithmTester()
    gen = ArgumentGenerator(seed=42)  # seed for reproducibility

    # 1. Correctness Testing
    # Define some test cases. Each test case is a tuple ((args...), expected_output).
    # Here, `args` will be a single list argument for my_algorithm, and we specify what we expect after sorting.
    test_cases = [
        ([3, 1, 2], [1, 2, 3]),
        ([5, 3, 5, 2], [2, 3, 5, 5]),
        ([], []),
        ([10, 9, 8, 8, 9], [8, 8, 9, 9, 10]),
    ]

    print("=== Testing Correctness ===")
    tester.test_correctness(my_algorithm, test_cases)

    # 2. Complexity Estimation
    # We want to measure how runtime scales as we increase input size.
    # We'll assume our algorithm is O(n log n) since it's a sort, but let's see what the tester estimates.

    # Prepare a range of input sizes
    input_sizes = [100, 200, 400, 800, 1600]

    # Define an argument generator function compatible with estimate_complexity:
    # This function takes an input size n and returns a tuple of arguments for the function.
    # Since my_algorithm takes a single list, we'll generate a list of length n.
    def list_args_generator(n):
        # We'll just generate a random list of integers of length n
        return gen.generate_int_list(n=n, min_val=0, max_val=1000, unique=False)

    print("\n=== Estimating Complexity ===")
    tester = AlgorithmTester()
    best_fit, fig = tester.estimate_complexity(my_algorithm, generate_plot=True)
    print("Estimated Complexity:", best_fit)
    # Save figure
    fig.savefig("complexity_plot.png")