import numpy as np

def calculate_total_tolerance(matrix, upper_tolerance, lower_tolerance):
    """
    Calculate total tolerance for a matrix with upper and lower bounds.
    
    Parameters:
    matrix: 2D array of floating point values
    upper_tolerance: 2D array of upper tolerance values (same shape as matrix)
    lower_tolerance: 2D array of lower tolerance values (same shape as matrix)
    
    Returns:
    dict: Contains nominal_total, upper_total, lower_total, and tolerance_range
    """
    
    # Convert to numpy arrays for easier manipulation
    matrix = np.array(matrix)
    upper_tolerance = np.array(upper_tolerance)
    lower_tolerance = np.array(lower_tolerance)
    
    # Calculate upper and lower bounds
    upper_matrix = matrix + upper_tolerance
    lower_matrix = matrix - lower_tolerance
    
    # Function to calculate parallel combination for a row
    def parallel_combination(row):
        # Handle zero or negative values by setting them to a small positive value
        row = np.where(row <= 0, 1e-12, row)
        # Calculate 1/((1/c1) + (1/c2) + ... + (1/cn))
        reciprocal_sum = np.sum(1.0 / row)
        return 1.0 / reciprocal_sum
    
    # Calculate parallel combination for each row
    nominal_parallel = np.array([parallel_combination(row) for row in matrix])
    upper_parallel = np.array([parallel_combination(row) for row in upper_matrix])
    lower_parallel = np.array([parallel_combination(row) for row in lower_matrix])
    
    # Sum the rows to get total
    nominal_total = np.sum(nominal_parallel)
    upper_total = np.sum(upper_parallel)
    lower_total = np.sum(lower_parallel)
    
    # Calculate tolerance range
    upper_tolerance_total = upper_total - nominal_total
    lower_tolerance_total = nominal_total - lower_total
    
    return {
        'nominal_total': nominal_total,
        'upper_total': upper_total,
        'lower_total': lower_total,
        'upper_tolerance_total': upper_tolerance_total,
        'lower_tolerance_total': lower_tolerance_total,
        'tolerance_range': upper_tolerance_total + lower_tolerance_total
    }

def print_results(results):
    """Print the results in a formatted way"""
    print(f"Nominal Total: {results['nominal_total']:.6f}")
    print(f"Upper Total: {results['upper_total']:.6f}")
    print(f"Lower Total: {results['lower_total']:.6f}")
    print(f"Upper Tolerance: +{results['upper_tolerance_total']:.6f}")
    print(f"Lower Tolerance: -{results['lower_tolerance_total']:.6f}")
    print(f"Total Tolerance Range: {results['tolerance_range']:.6f}")

# Example usage
if __name__ == "__main__":
    # Example matrix (3x4)
    matrix = [
        [10.0, 20.0, 30.0, 40.0],
        [15.0, 25.0, 35.0, 45.0],
        [12.0, 22.0, 32.0, 42.0]
    ]
    
    # Upper tolerances
    upper_tolerance = [
        [0.5, 1.0, 1.5, 2.0],
        [0.8, 1.2, 1.7, 2.2],
        [0.6, 1.1, 1.6, 2.1]
    ]
    
    # Lower tolerances
    lower_tolerance = [
        [0.5, 1.0, 1.5, 2.0],
        [0.8, 1.2, 1.7, 2.2],
        [0.6, 1.1, 1.6, 2.1]
    ]
    
    print("Matrix:")
    for row in matrix:
        print(row)
    
    print("\nUpper Tolerances:")
    for row in upper_tolerance:
        print(row)
    
    print("\nLower Tolerances:")
    for row in lower_tolerance:
        print(row)
    
    print("\nCalculating total tolerance...")
    results = calculate_total_tolerance(matrix, upper_tolerance, lower_tolerance)
    print_results(results)
    
    # Show intermediate calculations
    print("\nIntermediate calculations:")
    matrix_np = np.array(matrix)
    for i, row in enumerate(matrix_np):
        # Calculate parallel combination for this row
        reciprocal_sum = np.sum(1.0 / row)
        parallel_result = 1.0 / reciprocal_sum
        print(f"Row {i+1}: {row} -> Parallel combination: {parallel_result:.6f}")
