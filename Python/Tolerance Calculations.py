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
    upper_matrix = matrix + upper_tolerance * matrix
    lower_matrix = matrix - lower_tolerance * matrix

    # Function to calculate parallel combination for an array
    def parallel_combination(arr):
        # Handle zero or negative values by setting them to a small positive value
        arr = np.where(arr <= 0, 1e-12, arr)
        # Calculate 1/((1/c1) + (1/c2) + ... + (1/cn))
        reciprocal_sum = np.sum(1.0 / arr)
        return 1.0 / reciprocal_sum

    # Sum each row first to get 1xRows arrays
    nominal_row_sums = np.sum(matrix, axis=1)
    upper_row_sums = np.sum(upper_matrix, axis=1)
    lower_row_sums = np.sum(lower_matrix, axis=1)

    # Apply parallel combination to the row sums
    nominal_total = parallel_combination(nominal_row_sums)
    upper_total = parallel_combination(upper_row_sums)
    lower_total = parallel_combination(lower_row_sums)

    # Calculate tolerance range
    upper_tolerance_total = np.abs(upper_total / nominal_total - 1) * 100
    lower_tolerance_total = np.abs(lower_total / nominal_total - 1) * 100

    return {
        "nominal_total": nominal_total,
        "upper_total": upper_total,
        "lower_total": lower_total,
        "upper_tolerance_total": upper_tolerance_total,
        "lower_tolerance_total": lower_tolerance_total,
        "tolerance_range": upper_tolerance_total + lower_tolerance_total,
    }


def print_results(results):
    """Print the results in a formatted way"""
    print(f"Nominal Total: {results['nominal_total']:.6f}")
    print(f"Upper Total: {results['upper_total']:.6f}")
    print(f"Lower Total: {results['lower_total']:.6f}")
    print(f"Upper Tolerance: +{results['upper_tolerance_total']:.6f} %")
    print(f"Lower Tolerance: -{results['lower_tolerance_total']:.6f} %")
    print(f"Total Tolerance Range: {results['tolerance_range']:.6f} %")


# Example usage
if __name__ == "__main__":
    # Example matrix (3x4)
    matrix = [
            [1, 2, 3,],
            [3, 2, 1,],
            [4, 5, 6,],
            [6, 5, 4,],
            ]
    # Upper tolerances
    upper_tolerance = [
            [0.01, 0.05, 0.001,],
            [0.01, 0.05, 0.001,],
            [0.01, 0.05, 0.001,],
            [0.01, 0.05, 0.001,],
            ]
    # Lower tolerances
    lower_tolerance = [
            [0.01, 0.05, 0.001,],
            [0.01, 0.05, 0.001,],
            [0.01, 0.05, 0.001,],
            [0.01, 0.05, 0.001,],
            ]

  #  print("Matrix:")
  #  for row in matrix:
  #      print(row)

  #  print("\nUpper Tolerances:")
  #  for row in upper_tolerance:
  #      print(row)

  #  print("\nLower Tolerances:")
  #  for row in lower_tolerance:
  #      print(row)

    print("\nCalculating total tolerance...")
    results = calculate_total_tolerance(matrix, upper_tolerance, lower_tolerance)
    print_results(results)

    # Show intermediate calculations
   # print("\nIntermediate calculations:")
   # matrix_np = np.array(matrix)
   # upper_np = np.array(upper_tolerance)
   # lower_np = np.array(lower_tolerance)

   # print("Row sums:")
   # for i, row in enumerate(matrix_np):
   #     row_sum = np.sum(row)
   #     upper_sum = np.sum(row + upper_np[i])
   #     lower_sum = np.sum(row - lower_np[i])
   #     print(
   #         f"Row {i + 1}: {row} -> Sum: {row_sum:.6f} (Upper: {upper_sum:.6f}, Lower: {lower_sum:.6f})"
   #     )

   # # Calculate the row sums
   # nominal_row_sums = np.sum(matrix_np, axis=1)
   # upper_row_sums = np.sum(matrix_np + upper_np, axis=1)
   # lower_row_sums = np.sum(matrix_np - lower_np, axis=1)

   # print(f"\nRow sums array: {nominal_row_sums}")
   # print(f"Upper row sums: {upper_row_sums}")
   # print(f"Lower row sums: {lower_row_sums}")

   # # Show parallel combination calculation
   # reciprocal_sum = np.sum(1.0 / nominal_row_sums)
   # print("\nParallel combination of row sums:")
   # print(
   #     f"1/({' + '.join([f'1/{val:.6f}' for val in nominal_row_sums])}) = 1/{reciprocal_sum:.6f} = {results['nominal_total']:.6f}"
   # )
