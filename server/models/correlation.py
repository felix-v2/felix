from .util import VectorType

"""
Functions like correlate_2d_cyclic, from the original C implementation, 
which operate on one-dimensional arrays but perform computations 
equivalent to operations on two-dimensional arrays (matrices), 
are often called "flattened" or "linearized" versions of the corresponding 2D operations.

These functions are commonly used when efficiency or memory considerations favor a 
flattened representation of multidimensional data.

So for instance, The expression (y + i + k) % y computes the row index after applying cyclic 
boundary conditions. Similarly, (x + j + l) % x computes the column index after applying 
cyclic boundary conditions. These expressions ensure that when the convolution operation reaches
the boundaries of the 2D matrix, it wraps around to the opposite side, simulating a toroidal (cyclic) structure.

Such indexing expressions as (y + i + k) % y and (x + j + l) % x are specific to 2D matrix operations and 
won't directly translate to linearized vectors. When working with linearized vectors, we need to adjust the 
indexing logic to compute a single index that represents the position of the element in the vector.


Our specific use case means that we have linearised vectors, and we're correlating along both rows and columns 
of a 2D data structure represented as a 1D array. We therefore have to ensure that your 1D arrays are properly 
structured to represent the 2D data and that the indexing and boundary conditions are handled correctly.
"""


def Correlate_2d_cyclic_original_C(in_matrix, kern, x, y, kx, ky, out):
    """
    This doesn't work for 1d numpy arrays.
    """
    left = -((kx - 1) // 2)
    right = kx // 2
    upper = -((ky - 1) // 2)
    lower = ky // 2

    for i in range(y):  # rows
        ix = i * x
        for j in range(x):  # columns
            pkern = kern[ix + j]
            h = 0.0
            for k in range(upper, lower + 1):
                for l in range(left, right + 1):
                    in_index = ((i + k) % y) * x + ((j + l) % x)
                    kern_index = (k - upper) * kx + (l - left)
                    h += pkern[kern_index] * in_matrix[in_index]
            out[ix + j] = h
    return out


def Correlate_2d_cyclic_python(in_vector, kern, width, height, kernel_width, kernel_height, out_vector):
    """
    Performs a cyclic 2D correlation on a 2D data structure represented as a 1D array.
    The original C implementation, replicated in Correlate_2d_cyclic_original_C, doesn't work
    with our 1d numpy arrays
    """
    for i in range(height):
        for j in range(width):
            h = 0
            for k in range(-((kernel_height - 1) // 2), kernel_height // 2 + 1):
                for l in range(-((kernel_width - 1) // 2), kernel_width // 2 + 1):
                    index_in = ((i + k) % height) * width + (j + l) % width
                    index_kern = ((k + ((kernel_height - 1) // 2)) * kernel_width +
                                  (l + ((kernel_width - 1) // 2)))
                    h += kern[index_kern] * in_vector[index_in]
            out_vector[i * width + j] = h

    return out_vector


def Correlate_2d_Uni_cyclic(in_matrix: VectorType, kern: VectorType, x: int, y: int, kx: int, ky: int, out: VectorType):
    """
    This replicates the original C implementation, which does work for 1d numpy arrays.
    Performs a cyclic correlation operation between the input matrix and the uniform kernel, 
    taking into account the cyclic boundary conditions, and stores the result in the output matrix
    """
    left = -((kx - 1) // 2)
    right = kx // 2
    upper = -((ky - 1) // 2)
    lower = ky // 2

    pkern = kern.copy()

    for i in range(y):  # rows
        for j in range(x):  # columns
            h = 0.0
            for k in range(upper, lower + 1):
                for l in range(left, right + 1):
                    in_index = ((y + i + k) % y) * x + ((x + j + l) % x)
                    kern_index = (k - upper) * kx + (l - left)
                    h += pkern[kern_index] * in_matrix[in_index]
            out[i * x + j] = h
    return out
