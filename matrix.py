import math


def lookAt(ex, ey, ez,
           tx, ty, tz,
           ux, uy, uz):

    matrix = [0] * 16

    tx = ex - tx
    ty = ey - ty
    tz = ez - tz
    l = math.sqrt(tx * tx + ty * ty + tz * tz);
    matrix[ 2] = tx / l
    matrix[ 6] = ty / l
    matrix[10] = tz / l


    tx = uy * matrix[10] - uz * matrix[ 6]
    ty = uz * matrix[ 2] - ux * matrix[10]
    tz = ux * matrix[ 6] - uy * matrix[ 2]
    l = math.sqrt(tx * tx + ty * ty + tz * tz)
    matrix[ 0] = tx / l
    matrix[ 4] = ty / l
    matrix[ 8] = tz / l

    matrix[ 1] = matrix[ 6] * matrix[ 8] - matrix[10] * matrix[ 4]
    matrix[ 5] = matrix[10] * matrix[ 0] - matrix[ 2] * matrix[ 8]
    matrix[ 9] = matrix[ 2] * matrix[ 4] - matrix[ 6] * matrix[ 0]

    matrix[12] = -(ex * matrix[ 0] + ey * matrix[ 4] + ez * matrix[ 8])
    matrix[13] = -(ex * matrix[ 1] + ey * matrix[ 5] + ez * matrix[ 9])
    matrix[14] = -(ex * matrix[ 2] + ey * matrix[ 6] + ez * matrix[10])

    matrix[ 3] = matrix[ 7] = matrix[11] = 0.0
    matrix[15] = 1.0

    return matrix

#  画角から透視投影変換行列を求める
def cameraMatrix(fovy, aspect, near, far):

    matrix = [0] * 16
    f = 1.0 / math.tan(fovy * 0.5 * 3.141593 / 180.0)
    dz = far - near

    matrix[ 0] = f / aspect
    matrix[ 5] = f
    matrix[10] = -(far + near) / dz
    matrix[11] = -1.0
    matrix[14] = -2.0 * far * near / dz

    return matrix

# 行列 m0 と m1 の積を求める
def multiplyMatrix(m0, m1):
    matrix = [0] * 16

    for i in range(16):
        j = i & ~3
        k = i & 3
    
        matrix[i] = m0[j + 0] * m1[ 0 + k] + m0[j + 1] * m1[ 4 + k] + m0[j + 2] * m1[ 8 + k] + m0[j + 3] * m1[12 + k]

    return matrix