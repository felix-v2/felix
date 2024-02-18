# Like-for-like (as close as possible, warts and all) copies of the src functions used in the original C implementation of StandardNet6Areas.
# There are surely far more Pythonic implementations (e.g. numpy) than those below, but we ignore them
# in order to keep the translated Python version as close as possible to the original C implementation.

from multiprocessing import Pool
import numpy as np
from numpy.typing import NDArray
import random

VectorType = NDArray[np.float64]
bVectorType = NDArray[np.bool_]


def Get_Vector(z: int) -> VectorType:
    """
    Create a vector of length z
    """
    return np.zeros(z, dtype=np.float64)


def Get_Random_Vector(n: int) -> VectorType:
    return np.random.rand(n)


def Get_bVector(z: int) -> bVectorType:
    """
    Creates a binary vector of length z
    """
    return np.zeros(z, dtype=np.int32)


def Clear_Vector(z: int, v: VectorType) -> None:
    """
    Zeros all values of the vector
    """
    v.fill(0.0)


def Clear_bVector(z: int, v: bVectorType) -> None:
    """
    Zeros all values of the binary vector
    """
    v.fill(0)


def bbSkalar(n: int, v1: bVectorType, v2: bVectorType):
    """
    Calculates the dot product of two binary vectors v1 and v2 up to index n.

    It starts a parallel loop using OpenMP (#pragma omp parallel for) to distribute the iterations of the loop across multiple threads. 
    The loop is scheduled statically, meaning iterations are evenly distributed among threads. 
    The loop is shared across threads (shared(n,v1,v2)) while the loop variable i is private to each thread (private(i)).

    Replace with: numpy.dot (numexpr for parallelisation)?
    """
    result = 0

    def process_chunk(i):
        nonlocal result
        for index in range(i[0], i[1]):
            if v1[index] and v2[index]:
                result += 1

    chunk_size = n // 4  # Number of chunks for multiprocessing
    chunks = [(i * chunk_size, (i + 1) * chunk_size) for i in range(4)]
    chunks[-1] = (chunks[-1][0], n)  # Adjust last chunk

    with Pool(processes=4) as pool:
        pool.map(process_chunk, chunks)

    return result


def bSkalar(n: int, v1: VectorType, v2: bVectorType):
    """
    Calculates the dot product of a numeric vector v1 and a boolean vector v2 up to index n.

    Parallelised in the same manner as bbSkalar.
    """
    result = 0.0

    def process_chunk(chunk):
        chunk_sum = 0.0
        for i in chunk:
            if v2[i]:
                chunk_sum += v1[i]
        return chunk_sum

    chunk_size = n // 4  # Number of chunks for multiprocessing
    chunks = [(i * chunk_size, (i + 1) * chunk_size) for i in range(4)]
    chunks[-1] = (chunks[-1][0], n)  # Adjust last chunk

    with Pool(processes=4) as pool:
        chunk_sums = pool.map(process_chunk, chunks)

    return sum(chunk_sums)


def bSum(n: int, v: bVectorType):
    """
    Calculates the sum of elements in a binary vector in parallel using OpenMP, where each thread handles a 
    portion of the vector elements. The sum is computed using a reduction operation to efficiently combine 
    partial sums from different threads.

    Replace with: numpy.sum (numexpr for parallelisation)?
    """
    def process_chunk(chunk):
        chunk_sum = 0
        for i in chunk:
            if v[i]:
                chunk_sum += 1
        return chunk_sum

    chunk_size = n // 4  # Number of chunks for multiprocessing
    chunks = [(i * chunk_size, (i + 1) * chunk_size) for i in range(4)]
    chunks[-1] = (chunks[-1][0], n)  # Adjust last chunk

    with Pool(processes=4) as pool:
        chunk_sums = pool.map(process_chunk, chunks)

    return sum(chunk_sums)


def Sum(n: int, v: VectorType):
    """
    Calculates the sum of elements in a vector in parallel using OpenMP, where each thread handles a 
    portion of the vector elements. The sum is computed using a reduction operation to efficiently combine 
    partial sums from different threads.

    Replace with: numpy.sum (numexpr for parallelisation)?
    """
    def process_chunk(chunk):
        chunk_sum = 0
        for i in chunk:
            if v[i]:
                chunk_sum += v[i]
        return chunk_sum

    chunk_size = n // 4  # Number of chunks for multiprocessing
    chunks = [(i * chunk_size, (i + 1) * chunk_size) for i in range(4)]
    chunks[-1] = (chunks[-1][0], n)  # Adjust last chunk

    with Pool(processes=4) as pool:
        chunk_sums = pool.map(process_chunk, chunks)

    return sum(chunk_sums)


def Max_Elem(n: int, v: VectorType) -> float:
    """
    Finds the maximum element in a given vector v of length n.

    Replace with: max(v) ?
    """
    if n <= 0:
        print("dimension <= 0 in Max_Elem()")
        return None

    result = v[0]  # Initialize result to the first element of the vector
    for i in range(1, n):
        if v[i] > result:
            result = v[i]

    return result


def Fire(n: int, vektor: np.ndarray, teta, dest=None) -> bVectorType:
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


def leaky_integrate(tau: float, obj: float, expr: float, step_size: float) -> float:
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
    x, y = input_matrix.shape
    kx, ky = kernel.shape
    left = -(kx - 1) // 2
    right = kx // 2
    upper = -(ky - 1) // 2
    lower = ky // 2

    for i in range(y):  # Iterate over rows
        for j in range(x):  # Iterate over columns
            h = 0.0
            for k in range(upper, lower + 1):  # Iterate over kernel rows
                for l in range(left, right + 1):  # Iterate over kernel columns
                    h += kernel[k + (ky - 1) // 2, l + (kx - 1) // 2] * \
                        input_matrix[(i + k) % y, (j + l) % x]
            out[i * x + j] = h

    return out


def equal_noise() -> float:
    """
    Generates a random floating-point number in the range [0, 1)
    """
    return random.random()


def bool_noise(p: float) -> bool:
    """
    Generates a random boolean value with a probability p. The generated boolean value is true with probability p and 
    false with probability 1-p. The randomness is achieved by generating a random floating-point value in the 
    range [0, 1) and comparing it to the given probability p
    """
    return random.random() <= p
