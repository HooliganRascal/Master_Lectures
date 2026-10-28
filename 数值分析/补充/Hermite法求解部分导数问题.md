# Hermite 法求解部分导数问题

核心是：**把普通 Lagrange 插值部分 $L_{n}(x)$ 和只修正 $x_{k}$ 处导数的修正项分开求导**。设

$$
L_{n}(x)=\sum_{i=0}^n f(x_{i})l_{i}(x),
\qquad
l_{i}(x)=\prod_{j\ne i}\frac{x-x_{j}}{x_{i}-x_{j}},
$$

其中 $l_{i}(x_{j})=\delta_{ij}$。设给定的切线条件为

$$
H'_{n+1}(x_{k})=m_{k}
$$

（若要求与原函数切线相同，就取 $m_{k}=f'(x_{k})$）。按第二种构造：

$$
H_{n+1}(x)
=L_{n}(x)+C_{k}(x-x_{k})l_{k}(x).
$$

先看函数值条件：因为

$$
l_{k}(x_{i})=0\quad(i\ne k),\qquad (x_{k}-x_{k})l_{k}(x_{k})=0,
$$

所以修正项在所有节点 $x_{i}$ 处都为零，因此

$$
H_{n+1}(x_{i})=L_{n}(x_{i})=f(x_{i}),
$$

函数值条件自动满足。修正项只用来调整 $x_{k}$ 处的导数。

对 $H_{n+1}$ 求导：

$$
H'_{n+1}(x)
=L_{n}'(x)+C_{k}\bigl[l_{k}(x)+(x-x_{k})l_{k}'(x)\bigr].
$$

在 $x=x_{k}$ 处，利用 $l_{k}(x_{k})=1$，有

$$
H'_{n+1}(x_{k})
=L_{n}'(x_{k})+C_{k}.
$$

于是由切线条件 $H'_{n+1}(x_{k})=m_{k}$ 得

$$
\boxed{C_{k}=m_{k}-L_{n}'(x_{k})}.
$$

代回即得

$$
\boxed{
H_{n+1}(x)
=L_{n}(x)+\bigl[m_{k}-L_{n}'(x_{k})\bigr](x-x_{k})l_{k}(x)
}
$$

或者写成你给出的显式形式：

$$
\boxed{
H_{n+1}(x)
=L_{n}(x)+\bigl[m_{k}-L_{n}'(x_{k})\bigr]
\frac{\prod_{j=0}^n(x-x_{j})}
{\prod_{j\ne k}(x_{k}-x_{j})}
}
$$

因为

$$
(x-x_{k})l_{k}(x)
=
\frac{\prod_{j=0}^n(x-x_{j})}
{\prod_{j\ne k}(x_{k}-x_{j})}.
$$

如果想把 $L_{n}'(x_{k})$ 完全展开，则为

$$
L_{n}'(x_{k})
=
f(x_{k})\sum_{j\ne k}\frac1{x_{k}-x_{j}}
+
\sum_{i\ne k}f(x_{i})
\frac{\prod_{j\ne i,k}(x_{k}-x_{j})}
{\prod_{j\ne i}(x_{i}-x_{j})}.
$$

因此

$$
\boxed{
C_{k}
=
m_{k}-
\left[
f(x_{k})\sum_{j\ne k}\frac1{x_{k}-x_{j}}
+
\sum_{i\ne k}f(x_{i})
\frac{\prod_{j\ne i,k}(x_{k}-x_{j})}
{\prod_{j\ne i}(x_{i}-x_{j})}
\right].
}
$$

所以“拆分求解”的意思就是：

$$
H_{n+1}=L_{n}+\text{修正项},
$$

其中 $L_{n}$ 已满足所有函数值条件；修正项在所有节点为零，因此不破坏函数值条件。求导后在 $x_{k}$ 处，修正项的导数贡献恰好是 $C_{k}$，于是用

$$
H'_{n+1}(x_{k})=L_{n}'(x_{k})+C_{k}=m_{k}
$$

即可解出 $C_{k}$。

注意：这个简单显式公式适用于**只有一个额外导数条件**的情形。若有多个节点同时要求指定导数，一般不能仍用 $n+1$ 次多项式只加一个 $C_{k}$；需要提高插值多项式次数或建立更高次的 Hermite 型插值。
