import numpy as np
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import matrix
import sys
import os

# 頂点バッファオブジェクトのメモリにデータを書き込む
position = np.array([[-1.0, -1.0, -1.0],
                     [ 1.0, -1.0, -1.0],
                     [ 1.0, -1.0,  1.0],
                     [-1.0, -1.0,  1.0],
                     [-1.0,  1.0, -1.0],
                     [ 1.0,  1.0, -1.0],
                     [ 1.0,  1.0,  1.0],
                     [-1.0,  1.0,  1.0]])

# 頂点バッファオブジェクトのメモリにデータを書き込む
edge =np.array([[0, 1],
               [1,2],
               [2,3],
               [3,0],
               [0,4],
               [1,5],
               [2,6],
               [3,7],
               [4,5],
               [5,6],
               [6,7],
               [7,4]])

class Render:

    def __init__(self, name="GL render"):

        self.gl2Program = None
        self.program = None
        self.projectionMatrixLocation = None
        self.projectionMatrix = None
        self.vertbuffer = None
        self.fragbuffer = None
        self.vertShaderPath = "simple.vert"
        self.fragShaderPath = "simple.frag"
        glutInit()
        glutInitDisplayMode(GLUT_RGB)
        glutCreateWindow(name)
        glutDisplayFunc(self.display)

    # 初期化
    def init(self):
        # 背景色
        glClearColor(1.0, 1.0, 1.0, 1.0)


        with open(self.vertShaderPath, "r") as f:
            vertShaderData = f.read()

        with open(self.fragShaderPath, "r") as f:
            fragShaderData = f.read()

        # シェーダオブジェクトの作成
        vertShader = glCreateShader(GL_VERTEX_SHADER)
        fragShader = glCreateShader(GL_FRAGMENT_SHADER)

        # シェーダのソースプログラムの読み込み
        glShaderSource(vertShader, vertShaderData)
        glShaderSource(fragShader, fragShaderData)
        
        # バーテックスシェーダのソースプログラムのコンパイル
        glCompileShader(vertShader)
        compiled = glGetShaderiv(vertShader, GL_COMPILE_STATUS)
        if compiled == GL_FALSE:
            print("in cimpiled error")
            strInfoLog = glGetShaderInfoLog(vertShader)
            print("Compilation failure for "  + " shader:\n" + str(strInfoLog))

        # フラグメントシェーダのソースプログラムのコンパイル
        glCompileShader(fragShader)
        compiled = glGetShaderiv(fragShader, GL_COMPILE_STATUS)
        if compiled == GL_FALSE:
            print("in cimpiled error")
            strInfoLog = glGetShaderInfoLog(fragShader)
            print("Compilation failure for "  + " shader:\n" + str(strInfoLog))

        # プログラムオブジェクトの作成
        self.gl2Program = glCreateProgram()

        # シェーダオブジェクトのシェーダプログラムへの登録
        glAttachShader(self.gl2Program, vertShader)
        glAttachShader(self.gl2Program, fragShader)


        # attribute 変数 position の index を 0 に指定する。
        glBindAttribLocation(self.gl2Program, 0, "position")

        # シェーダプログラムのリンク
        glLinkProgram(self.gl2Program)
        linked = glGetProgramiv(self.gl2Program, GL_LINK_STATUS)
        if linked == GL_FALSE:
            print("Link error.")
            strInfoLog = printProgramInfoLog(self.gl2Program)
            return

        # シェーダオブジェクトのデタッチ
        glDetachShader(self.gl2Program, vertShader)
        glDetachShader(self.gl2Program, fragShader)
        # シェーダオブジェクトの削除
        glDeleteShader(vertShader)
        glDeleteShader(fragShader)

        # 視野変換行列を求める
        temp0 = matrix.lookAt(4.0, 5.0, 6.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

        # 透視投影変換行列を求める 
        temp1 = matrix.cameraMatrix(30.0, 1.0, 7.0, 11.0)

        # 視野変換行列と投影変換行列の積を projectionMatrix に入れる
        self.projectionMatrix = matrix.multiplyMatrix(temp0, temp1)

        # uniform 変数 projectionMatrix の場所を得る
        self.projectionMatrixLocation = glGetUniformLocation(self.gl2Program, "projectionMatrix")

        # 頂点バッファオブジェクトを２つ作る
        self.vertbuffer = glGenBuffers(1)
        self.fragbuffer = glGenBuffers(1)

        # 頂点バッファオブジェクトに８頂点分のメモリ領域を確保する 
        glBindBuffer(GL_ARRAY_BUFFER, self.vertbuffer)
        glBufferData(GL_ARRAY_BUFFER, position, GL_STATIC_DRAW)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.fragbuffer)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, edge.astype(np.int32), GL_STATIC_DRAW)

        # 頂点バッファオブジェクトを解放する 
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)

        # 頂点バッファオブジェクトを解放する
        glBindBuffer(GL_ARRAY_BUFFER, 0)

    # 画面表示
    def display(self):
        # 画面クリア
        glClear(GL_COLOR_BUFFER_BIT)

        # シェーダプログラムを適用する
        glUseProgram(self.gl2Program)

        # uniform 変数 projectionMatrix に行列を設定する
        glUniformMatrix4fv(self.projectionMatrixLocation, 1, GL_FALSE, self.projectionMatrix)

        # index が 0 の attribute 変数に頂点情報を対応付ける
        glEnableVertexAttribArray(0)

        # 頂点バッファオブジェクトとして vertbuffer を指定する
        glBindBuffer(GL_ARRAY_BUFFER, self.vertbuffer)

        # 頂点情報の格納場所と書式を指定する
        glVertexAttribPointer(0, 3, GL_DOUBLE, GL_FALSE, 0, None)

        # 頂点バッファオブジェクトの指標として fragbuffer を指定する
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.fragbuffer)

        # 図形を描く 
        glDrawElements(GL_LINES, 24, GL_UNSIGNED_INT, None)

        # 頂点バッファオブジェクトを解放する
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

        # index が 0 の attribute 変数の頂点情報との対応付けを解除する
        glDisableVertexAttribArray(0)

        glutSwapBuffers()
        
    def mainloop(self):
        glutMainLoop()

        
# メインプログラム
def main():
    render = Render(sys.argv[0])
    render.init()
    render.mainloop()


if __name__ == '__main__':
    main()