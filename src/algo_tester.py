import time
import math
import statistics

class AlgorithmTester:
    """
    A class that can test both correctness of a function and estimate its big-O runtime complexity.
    """
    def __init__(self):
        pass

    def test_correctness(self, func, test_cases, comparator=None):
        """
        Tests the correctness of a function against provided test cases.

        Parameters:
        - func: The function to test. It should accept arguments as specified in test cases.
        - test_cases: A list of tuples of the form ((args...), expected_output)
        - comparator: An optional custom comparator function that takes (result, expected) and returns True/False.

        Prints a report of which tests passed and which failed.
        """
        if comparator is None:
            comparator = lambda result, expected: result == expected

        all_passed = True
        for i, case in enumerate(test_cases):
            args, expected = case
            if not isinstance(args, tuple):
                args = (args,)
            try:
                result = func(*args)
                if comparator(result, expected):
                    print(f"Test case {i+1}: PASS")
                else:
                    print(f"Test case {i+1}: FAIL - Expected {expected}, got {result}")
                    all_passed = False
            except Exception as e:
                print(f"Test case {i+1}: FAIL - Exception occurred: {e}")
                all_passed = False

        if all_passed:
            print("All test cases passed!")
        else:
            print("Some test cases failed.")

    def estimate_complexity(self, func, input_sizes, args_generator, num_runs=5):
        """
        Estimate the complexity of a function by measuring how the runtime scales with input size.
        
        Parameters:
        - func: The function whose complexity we want to estimate.
        - input_sizes: A list of input sizes (e.g., [100, 200, 400, ...]).
        - args_generator: A callable that takes an input size and returns a tuple of arguments 
                          for the function.
        - num_runs: How many times to run each measurement for averaging.

        Returns:
        - A string representing the best guess of the complexity class from a predefined set.
        """

        # Extended set of complexities to attempt:
        complexity_functions = {
            "O(1)":        lambda n: 1,
            "O(log n)":    lambda n: math.log(n) if n > 1 else 0,
            "O(√n)":       lambda n: math.sqrt(n),
            "O(n)":        lambda n: n,
            "O(n log n)":  lambda n: n * math.log(n) if n > 1 else 0,
            "O(n²)":       lambda n: n**2,
            "O(n³)":       lambda n: n**3,
            "O(2^n)":      lambda n: 2**n if n < 30 else float('inf'),  # limited to smaller n due to large values
        }

        times = []
        # Run the function for each input size and measure time
        for n in input_sizes:
            run_times = []
            # Generate arguments using the provided generator
            args = args_generator(n)
            for _ in range(num_runs):
                start = time.perf_counter()
                func(*args)
                end = time.perf_counter()
                run_times.append(end - start)
            avg_time = statistics.mean(run_times)
            times.append(avg_time)

        # Attempt to fit times to complexity forms using a least squares approach
        best_fit = None
        best_error = float("inf")

        for label, f_complex in complexity_functions.items():
            f_values = [f_complex(n) for n in input_sizes]

            # If all f_values are zero (degenerate case)
            if all(v == 0 for v in f_values):
                c = sum(times) / len(times) if times else 0
                error = sum((t - c)**2 for t in times)
            else:
                # Filter out infinite or NaN values (for large n in O(2^n))
                valid_pairs = [(t, fv) for t, fv in zip(times, f_values) if math.isfinite(fv) and fv != 0]
                if not valid_pairs:
                    continue
                t_vals, fv_vals = zip(*valid_pairs)

                numerator = sum(t * fv for t, fv in zip(t_vals, fv_vals))
                denominator = sum(fv * fv for fv in fv_vals)
                if denominator == 0:
                    continue
                c = numerator / denominator

                # Compute error
                error = sum((t - c * fv)**2 for t, fv in zip(t_vals, fv_vals))

            if error < best_error:
                best_error = error
                best_fit = label

        return best_fit
