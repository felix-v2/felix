# Like-for-like (as close as possible, warts and all) copies of the src functions used in the original C implementation of StandardNet6Areas.
# There are surely far more Pythonic implementations (e.g. numpy) than those below, but we ignore them
# in order to keep the translated Python version as close as possible to the original C implementation.

import numpy as np
from numpy.typing import NDArray
import random
import math
# from multiprocessing import Pool

BaseType = np.float64
VectorType = NDArray[BaseType]
bVectorType = NDArray[np.int32]


def Get_Vector(z: int) -> VectorType:
    """
    Create a vector of length z
    """
    return np.zeros(z, dtype=BaseType)


def Get_Random_Vector(n: int) -> VectorType:
    """
    A new function for unit tests; not in the original C implementation
    """
    return np.random.rand(n)


def Get_bVector(z: int) -> bVectorType:
    """
    Creates a binary vector of length z
    """
    return np.zeros(z, dtype=np.int32)


def Clear_Vector(v: VectorType) -> None:
    """
    Zeros all values of the vector
    """
    v.fill(0.0)


def Clear_bVector(v: bVectorType) -> None:
    """
    Zeros all values of the binary vector
    """
    v.fill(0)


# See todos below: where we do assignment to numpy arrays (vectors, e.g. J) we need to make sure
# we mutate the original sliced J that is passed in! Check how to do this with numpy

# @todo init_gauss_kern seems to result in J having only a handful of non-zero values. Same issue as below?
# @todo J is not being updated with the random values - is it referenceing the original self.J that is passed down?

# this is like init_gaussian_kernels
# creates the (0,0) kernel at the start of the slice
# then copies it to the end of the area_connection's section of J
def add_all_kernels_for_area_connection(vector_slice: VectorType, cells_per_area: int, area_connection_id: int):
    # add the array of 4 synaptic values for the area-area connection, to the start of the slice
    for x in range(cells_per_area):
        for y in range(cells_per_area):
            vector_slice[y*cells_per_area+x] = area_connection_id

    # copy this to the other 4 sections of the vector slice, representing the section of the vector for this area-area connection
    n = cells_per_area*cells_per_area
    for i in range(1, n):
        vector_slice[i*n:(i+1)*n] = vector_slice[:n]


def MUTATE_VECTOR():
    """
    For illustrative purposes only - not used in the model. This is a simplified version of how
    J is referenced and mutated in the flow `init() -> init_patchy_gauss_kern() -> init_gaussian_kernel()`.

    1. self.init_patchy_gauss_kern(... , self.J[start:end], ...)
    2.   init_gauss_kernel(..., J, ...)
    3.     J[y * mx + x:y * mx + x + 1] = ampl * math.exp(-h)

    (A) at level 1, if we pass down a single element, the downstream logic breaks because it tries to
      index the element itself e.g. J[index] -> 0.0. Therefore we have to pass down a single-element 
      slice of self.J - `J[index:index+1]` -> [0.0].

    (B) however, at level 3, we need to mutate the original J in memory - but we can only mutate values within the index range of the passed slice.
        Therefore if we pass down the single element from index i as a slice, we can't do anything with the elements i+1, i+2, ..., i+n 
        Therefore we need to pass down a sliced *range* of J corresponding to the section of J that is apportioned to the specific area-area connection
        E.g. for the area connection (0,0), we should pass to init_patchy_gauss_kern: J[0:390625]

    Example: 6 areas, each area has 2 cells, 4 synapses. Each area-area connection has 4*4 synapses, 16.
    36 area-connections
    Each area-connection has 16 synapses
    J = [ 1*16 | 2*16 | ... | 36*16 ] - 576 total network synapses, 16 for each of the 36 "area connections"
    """
    areas = 6
    area_connections = areas*areas  # 36
    cells_per_area = 2
    synapses_per_area = cells_per_area*cells_per_area  # 4
    synapses_per_area_connection = synapses_per_area*synapses_per_area  # 16
    total_network_synapses = area_connections * \
        synapses_per_area_connection  # 36*16 = 576

    # this original vector should be mutated directly by the downstream func
    vector = Get_Vector(total_network_synapses)

    # for each of the 36 area connections
    for i in range(area_connections):
        vector_start = synapses_per_area_connection * i
        vector_end = vector_start + synapses_per_area_connection
        print(
            f"Area connection [{i+1}/{area_connections}]: adding synapse data to J at ({vector_start}, {vector_end})"),

        # the vector slice below represents the start-end positions in J of the synapses for *this* area connection
        add_all_kernels_for_area_connection(
            vector[vector_start:vector_end], cells_per_area, i+1)

    return vector


def bbSkalar(n: int, v1: bVectorType, v2: bVectorType):
    """
    Calculates the dot product of two binary vectors v1 and v2 up to index n.

    It starts a parallel loop using OpenMP (#pragma omp parallel for) to distribute the iterations of the loop across multiple threads. 
    The loop is scheduled statically, meaning iterations are evenly distributed among threads. 
    The loop is shared across threads (shared(n,v1,v2)) while the loop variable i is private to each thread (private(i)).

    Replace with: numpy.dot (numexpr for parallelisation)?
    """
    return np.dot(v1, v2)
    # result = 0

    # def process_chunk(i):
    #     nonlocal result
    #     for index in range(i[0], i[1]):
    #         if v1[index] and v2[index]:
    #             result += 1

    # chunk_size = n // 4  # Number of chunks for multiprocessing
    # chunks = [(i * chunk_size, (i + 1) * chunk_size) for i in range(4)]
    # chunks[-1] = (chunks[-1][0], n)  # Adjust last chunk

    # with Pool(processes=4) as pool:
    #     pool.map(process_chunk, chunks)

    # return result


def bSkalar(n: int, v1: VectorType, v2: bVectorType):
    """
    Calculates the dot product of a numeric vector v1 and a boolean vector v2 up to index n.

    Parallelised in the same manner as bbSkalar.

    Replace with: numpy.dot (numexpr for parallelisation)?
    """
    return np.dot(v1, v2)
    # result = 0.0

    # def process_chunk(chunk):
    #     chunk_sum = 0.0
    #     for i in chunk:
    #         if v2[i]:
    #             chunk_sum += v1[i]
    #     return chunk_sum

    # chunk_size = n // 4  # Number of chunks for multiprocessing
    # chunks = [(i * chunk_size, (i + 1) * chunk_size) for i in range(4)]
    # chunks[-1] = (chunks[-1][0], n)  # Adjust last chunk

    # with Pool(processes=4) as pool:
    #     chunk_sums = pool.map(process_chunk, chunks)

    # return sum(chunk_sums)


def bSum(n: int, v: bVectorType):
    """
    Calculates the sum of elements in a binary vector in parallel (originally using OpenMP), where each thread handles a 
    portion of the vector elements. The sum is computed using a reduction operation to efficiently combine 
    partial sums from different threads.

    Replace with: numpy.sum (numexpr for parallelisation)?
    """
    return np.sum(v)
    # def process_chunk(chunk):
    #     chunk_sum = 0
    #     for i in chunk:
    #         if v[i]:
    #             chunk_sum += 1
    #     return chunk_sum

    # chunk_size = n // 4  # Number of chunks for multiprocessing
    # chunks = [(i * chunk_size, (i + 1) * chunk_size) for i in range(4)]
    # chunks[-1] = (chunks[-1][0], n)  # Adjust last chunk

    # with Pool(processes=4) as pool:
    #     chunk_sums = pool.map(process_chunk, chunks)

    # return sum(chunk_sums)


def Sum(n: int, v: VectorType):
    """
    Calculates the sum of elements in a vector in parallel (originally using OpenMP), where each thread handles a 
    portion of the vector elements. The sum is computed using a reduction operation to efficiently combine 
    partial sums from different threads.

    Replace with: numpy.sum (numexpr for parallelisation)?
    """
    return np.sum(v)
    # def process_chunk(chunk):
    #     chunk_sum = 0
    #     for i in chunk:
    #         if v[i]:
    #             chunk_sum += v[i]
    #     return chunk_sum

    # chunk_size = n // 4  # Number of chunks for multiprocessing
    # chunks = [(i * chunk_size, (i + 1) * chunk_size) for i in range(4)]
    # chunks[-1] = (chunks[-1][0], n)  # Adjust last chunk

    # with Pool(processes=4) as pool:
    #     chunk_sums = pool.map(process_chunk, chunks)

    # return sum(chunk_sums)


def Max_Elem(v: VectorType) -> BaseType:
    """
    Finds the maximum element in a given vector v of length n.

    Replace with: max(v) ?
    """
    return max(v)
    # if n <= 0:
    #     print("dimension <= 0 in Max_Elem()")
    #     return None

    # result = v[0]  # Initialize result to the first element of the vector
    # for i in range(1, n):
    #     if v[i] > result:
    #         result = v[i]

    # return result


def Fire(n: int, vektor: VectorType, teta: BaseType, dest: bVectorType = None) -> bVectorType:
    """
    "Classifies" each element in the input vector vektor based on whether it exceeds the threshold 
    value teta, and returns a binary array indicating the result of this classification
    """
    def FIRE(pot):
        return 1 if pot > 0.0 else 0

    if dest is None:
        dest = Get_bVector(n)
        if dest is None:
            return None

    for i in range(n):
        dest[i] = FIRE(vektor[i] - teta)

    return dest


def leaky_integrate(tau: BaseType, obj: BaseType, expr: BaseType, step_size: BaseType) -> BaseType:
    """
    Represents a leaky integration process.
    Updates a variable obj over time based on an expression expr and a time constant tau
    """
    if tau:
        obj += (expr - obj) * (step_size / tau)
    else:
        obj = expr
    return obj


def Correlate_2d_cyclic(input_matrix: np.ndarray, kernel: np.ndarray, out: np.ndarray) -> np.ndarray:
    """
    Performs a cyclic correlation operation between the input matrix and the kernel matrix, 
    taking into account the cyclic boundary conditions, and stores the result in the output matrix
    """
    x, y = input_matrix.shape
    kx, ky = kernel.shape

    for i in range(y):  # Iterate over rows
        for j in range(x):  # Iterate over columns
            left = -(kx - 1) // 2
            right = kx // 2
            upper = -(ky - 1) // 2
            lower = ky // 2

            h = 0.0
            for k in range(upper, lower + 1):  # Iterate over kernel rows
                for l in range(left, right + 1):  # Iterate over kernel columns
                    pkern = kernel[(k + (ky - 1) // 2), (l + (kx - 1) // 2)]
                    h += pkern * input_matrix[(i + k) % y, (j + l) % x]

            out[i, j] = h

    return out


def Correlate_2d_Uni_cyclic(input_matrix: np.ndarray, kernel: np.ndarray, out: np.ndarray) -> np.ndarray:
    """
    Performs a cyclic correlation operation between the input matrix and the uniform kernel, 
    taking into account the cyclic boundary conditions, and stores the result in the output matrix
    """
    y, x = input_matrix.shape
    ky, kx = kernel.shape
    oy, ox = out.shape

    left = -(kx - 1) // 2
    right = kx // 2
    upper = -(ky - 1) // 2
    lower = ky // 2

    for i in range(oy):  # Iterate over rows of out
        for j in range(ox):  # Iterate over columns of out
            h = 0.0
            for k in range(upper, lower + 1):  # Iterate over kernel rows
                for l in range(left, right + 1):  # Iterate over kernel columns
                    h += kernel[k + (ky - 1) // 2, l + (kx - 1) // 2] * \
                        input_matrix[(i + k) % oy, (j + l) % ox]

            out[i, j] = h

    return out


def equal_noise() -> BaseType:
    """
    Generates a random floating-point number in the range [0, 1)
    """
    return random.random()


def bool_noise(p: BaseType) -> bool:
    """
    Generates a random boolean value with a probability p. The generated boolean value is true with probability p and 
    false with probability 1-p
    """
    return random.random() <= p


def SIGMOID(x: BaseType):
    """
    Computes the sigmoid activation value for the input _x, which squashes the input values into the range [0, 1], 
    (suitable for modeling probabilities -- firing rates in neural nets)

    Replace with: tensorflow.sig ?
    """
    return 1.0 / (1.0 + math.exp(-2.0 * x))


def RAMP(x: BaseType):
    """
    Activation function (for excitatory cells)
    Essentially clips the input x to the range [0.0, 1.0]. If the input is outside this range, it is clamped to the nearest boundary value (0.0 or 1.0)
    """
    return max(0.0, min(1.0, x))


def TLIN(x: BaseType):
    """
    Activation functions (for inhibitory neurons)
    Introduces a threshold, and if the input exceeds the threshold, it allows the input to pass through unchanged; otherwise, it returns zero
    """
    return x if x > 0 else 0
