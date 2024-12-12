import time
import math
import statistics
import matplotlib

matplotlib.use('Agg')  # Use a non-interactive backend

import matplotlib.pyplot as plt

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

    def estimate_complexity(self, func, input_sizes=None, args_generator=None, num_runs=5, generate_plot=False):
        """
        Estimate the complexity of a function by measuring how the runtime scales with input size.
        
        Parameters:
        - func: The function whose complexity we want to estimate.
        - input_sizes: A list of input sizes (e.g., [100, 200, 400, ...]). If None, uses a default set.
        - args_generator: A callable that takes an input size and returns a tuple of arguments 
                          for the function.
        - num_runs: How many times to run each measurement for averaging.
        - generate_plot: If True, also generate a plot comparing actual runtimes vs. best-fit complexity.
        
        Returns:
        - best_fit (str) if generate_plot=False
        - (best_fit (str), fig (matplotlib figure)) if generate_plot=True
        """

        if input_sizes is None:
            # Default set of input sizes
            input_sizes = [100, 200, 400, 800, 1600]

        # Provide a default args_generator if none is given
        if args_generator is None:
            # Default: generate a list of integers of size n
            def default_args_generator(n):
                return ([0]*n,)
            args_generator = default_args_generator

        complexity_functions = {
            "O(1)":        lambda n: 1,
            "O(log n)":    lambda n: math.log(n) if n > 1 else 0,
            "O(√n)":       lambda n: math.sqrt(n),
            "O(n)":        lambda n: n,
            "O(n log n)":  lambda n: n * math.log(n) if n > 1 else 0,
            "O(n²)":       lambda n: n**2,
            "O(n³)":       lambda n: n**3,
            "O(2^n)":      lambda n: 2**n if n < 30 else float('inf'),  # limited due to large values
        }

        times = []
        # Measure runtime for each input size
        for n in input_sizes:
            run_times = []
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
        best_c = None
        best_func = None

        for label, f_complex in complexity_functions.items():
            f_values = [f_complex(n) for n in input_sizes]

            # If all f_values are zero (degenerate case)
            if all(v == 0 for v in f_values):
                c = sum(times) / len(times) if times else 0
                error = sum((t - c)**2 for t in times)
            else:
                # Filter out infinite or NaN values (for large n in O(2^n))
                valid_pairs = [(t, fv) for t, fv in zip(times, f_values) 
                               if math.isfinite(fv) and fv != 0]
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
                best_c = c if 'c' in locals() else None
                best_func = f_complex

        if not generate_plot:
            return best_fit
        else:
            # Generate a plot of the runtimes and the best fit line
            fig, ax = plt.subplots()

            # Plot measured times
            ax.scatter(input_sizes, times, color='blue', label='Measured Times')

            # Plot best fit complexity line
            if best_fit is not None and best_func is not None and best_c is not None:
                fitted_values = [best_c * best_func(n) for n in input_sizes]
                ax.plot(input_sizes, fitted_values, color='red', label=f'Best Fit: {best_fit}')

            ax.set_xlabel('Input Size (n)')
            ax.set_ylabel('Time (seconds)')
            ax.set_title('Runtime vs. Input Size')
            ax.legend()
            ax.grid(True)

            # Return best_fit and fig
            return best_fit, fig
