# algo_tester
Small library to automate generating valid Leetcode-style test cases and testing algorithms for runtime complexity.

---

## Installation

**Prerequisites:**  
- Python 3.6 or later
- `pip` (Python’s package manager)

**Recommended:** Use a virtual environment (e.g., `venv` or `conda`) to avoid conflicts with other packages on your system.

### Steps

1. **Clone the repository** (if you haven’t already):
   ```bash
   git clone https://github.com/yourusername/algo_tester.git
   cd algo_tester
   ```

2. **(Optional) Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install the package and its dependencies using `pip`:**
   ```bash
   python -m pip install .
   ```

   Using `python -m pip` ensures that `pip` corresponds to the same Python interpreter used to run your code, preventing environment mismatches.

4. **Verify installation:**
   ```bash
   python -c "from algo_tester.algo_tester import AlgorithmTester; print('Installation successful!')"
   ```

If the command above prints **"Installation successful!"** without errors, you’re ready to use `AlgorithmTester`.