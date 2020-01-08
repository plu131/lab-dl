"""
파라미터 최적화 알고리즘 6) Nesterov's Accelerated Gradient
    모멘텀(momentum) 알고리즘을 좀 더 적극적으로 활용한 알고리즘
    Momentum: v = m * v - lr * dL/dW
    -> W = W + v = W - lr * dL/dW + m * v
                 = W - lr * dL/dW + m * (m * v - lr * dL/dW)
                 = W + m**2 * v - (1 + m) * lr * dL/dW
    모멘텀 알고리즘에서 이전 학습에서 계산된 모멘텀(v) 항을 새로 업데이트된 모멘텀으로 대신하여,
    결과적으로는 모멘텀 상수 제곱(m**2)에 의한 파라미터 변화와 모멘텀 상수(1+m)와 학습률(lr)에 의한 파라미터 변화를
    모두 반영하도록 하는 알고리즘
"""
import matplotlib.pyplot as plt
import numpy as np

from ch06.ex01_matplot3d import fn, fn_derivative


class Nesterov:
    def __init__(self, lr=0.01, m=0.9):
        self.lr = lr
        self.m = m
        self.v = dict()

    def update(self, params, grads):
        if not self.v:
            for key in params:
                self.v[key] = np.zeros_like(params[key])
        for key in params:
            self.v[key] = self.m * self.v[key] - self.lr * grads[key]
            params[key] += self.m**2 * self.v[key] - (1 + self.m) * self.lr * grads[key]


if __name__ == '__main__':
    nesterov = Nesterov(lr=0.1, m=0.9)

    params = {'x': -7., 'y': 2.}
    gradients = {'x': 0, 'y': 0}
    x_history = []
    y_history = []

    for _ in range(30):
        x_history.append(params['x'])
        y_history.append(params['y'])
        gradients['x'], gradients['y'] = fn_derivative(params['x'], params['y'])
        nesterov.update(params, gradients)

    for x, y in zip(x_history, y_history):
        print(f'({x}, {y})')

    x = np.linspace(-10, 10, 2000)
    y = np.linspace(-5, 5, 1000)
    X, Y = np.meshgrid(x, y)
    Z = fn(X, Y)

    mask = Z > 8
    Z[mask] = 0

    plt.contour(X, Y, Z, 10)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.axis('equal')

    plt.plot(x_history, y_history, 'o-', color='red')
    plt.show()
