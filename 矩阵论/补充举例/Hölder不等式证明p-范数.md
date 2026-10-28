# Hölder 不等式证明 $p-$ 范数

设 $x=(x_{1},\dots,x_{n})\in\mathbb R^n$（或 $\mathbb C^n$），对 $1\le p<\infty$ 定义  
$$
\|x\|_p=\left(\sum_{i=1}^n |x_{i}|^p\right)^{1/p}.
$$
下面证明它是范数。记共轭指数 $q=\frac{p}{p-1}$（当 $p>1$ 时），满足
$$
\frac1p+\frac1q=1.
$$
Hölder 不等式为
$$
\sum_{i=1}^n |a_{i} b_{i}|
\le \left(\sum_{i=1}^n |a_{i}|^p\right)^{1/p}
   \left(\sum_{i=1}^n |b_{i}|^q\right)^{1/q}.
$$

## 1. 非负性与正定性
显然
$$
\|x\|_p=\left(\sum_{i=1}^n |x_{i}|^p\right)^{1/p}\ge 0.
$$
若 $\|x\|_p=0$，则
$$
\sum_{i=1}^n |x_{i}|^p=0,
$$
所以每个 $|x_{i}|^p=0$，从而 $x_{i}=0$，即 $x=0$。反之若 $x=0$，显然 $\|x\|_p=0$。因此
$$
\|x\|_p\ge 0,\qquad \|x\|_p=0\iff x=0.
$$

## 2. 齐次性
对任意标量 $\alpha$，
$$
\|\alpha x\|_p
=\left(\sum_{i=1}^n |\alpha x_{i}|^p\right)^{1/p}
=\left(|\alpha|^p\sum_{i=1}^n |x_{i}|^p\right)^{1/p}
=|\alpha|\left(\sum_{i=1}^n |x_{i}|^p\right)^{1/p}
=|\alpha|\|x\|_p.
$$
所以 $p$-范数具有绝对齐次性。

## 3. 三角不等式
先考虑 $p>1$。令 $z=x+y$，即 $z_{i}=x_{i}+y_{i}$。有
$$
\|x+y\|_p^p
=\sum_{i=1}^n |z_{i}|^p
=\sum_{i=1}^n |z_{i}|\,|z_{i}|^{p-1}
\le \sum_{i=1}^n |x_{i}|\,|z_{i}|^{p-1}
+\sum_{i=1}^n |y_{i}|\,|z_{i}|^{p-1}.
$$
对右端第一项使用 Hölder 不等式，取
$$
a_{i}=|x_{i}|,\qquad b_{i}=|z_{i}|^{p-1}.
$$
因为 $q=\frac{p}{p-1}$，所以
$$
(b_{i})^q=|z_{i}|^{(p-1)q}=|z_{i}|^p.
$$
于是
$$
\sum_{i=1}^n |x_{i}|\,|z_{i}|^{p-1}
\le
\left(\sum_{i=1}^n |x_{i}|^p\right)^{1/p}
\left(\sum_{i=1}^n |z_{i}|^p\right)^{1/q}
=
\|x\|_p\,\|z\|_p^{p/q}.
$$
又因为
$$
\frac{p}{q}=p-1,
$$
故
$$
\sum_{i=1}^n |x_{i}|\,|z_{i}|^{p-1}
\le \|x\|_p\,\|z\|_p^{p-1}.
$$
同理，
$$
\sum_{i=1}^n |y_{i}|\,|z_{i}|^{p-1}
\le \|y\|_p\,\|z\|_p^{p-1}.
$$
因此
$$
\|x+y\|_p^p
\le
\bigl(\|x\|_p+\|y\|_p\bigr)\|x+y\|_p^{p-1}.
$$
若 $\|x+y\|_p=0$，则三角不等式显然成立。若 $\|x+y\|_p>0$，两边除以 $\|x+y\|_p^{p-1}$，得到
$$
\|x+y\|_p
\le
\|x\|_p+\|y\|_p.
$$
这就是三角不等式。

当 $p=1$ 时，
$$
\|x+y\|_{1}
=\sum_{i=1}^n |x_{i}+y_{i}|
\le
\sum_{i=1}^n |x_{i}|+\sum_{i=1}^n |y_{i}|
=\|x\|_{1}+\|y\|_{1},
$$
三角不等式直接成立。

综上，对 $1\le p<\infty$，向量的 $p$-范数
$$
\|x\|_p=\left(\sum_{i=1}^n |x_{i}|^p\right)^{1/p}
$$
满足非负性、正定性、齐次性和三角不等式，因此是一种范数。

## 补充：Hölder 不等式的证明
下面给出有限维离散形式的 Hölder 不等式证明；一般测度形式证明完全相同，只需把求和换成积分。

设 $1 < p < \infty$，共轭指数 $q=\frac{p}{p-1}$，即
$$
\frac1p+\frac1q=1.
$$
Hölder 不等式为
$$
\sum_{i=1}^n |a_{i} b_{i}|
\le
\left(\sum_{i=1}^n |a_{i}|^p\right)^{1/p}
\left(\sum_{i=1}^n |b_{i}|^q\right)^{1/q}.
$$

### 第一步：Young 不等式
对任意 $u,v\ge 0$，有
$$
uv\le \frac{u^p}{p}+\frac{v^q}{q}.
$$
证明如下。由加权 AM-GM 不等式，
$$
u v=(u^p)^{1/p}(v^q)^{1/q}
\le \frac1p u^p+\frac1q v^q.
$$
因为 $\frac1p+\frac1q=1$。这就是 Young 不等式。

### 第二步：归一化
记
$$
A=\left(\sum_{i=1}^n |a_{i}|^p\right)^{1/p},\qquad
B=\left(\sum_{i=1}^n |b_{i}|^q\right)^{1/q}.
$$
若 $A=0$ 或 $B=0$，则对应的 $a$ 或 $b$ 为零向量，Hölder 不等式显然成立。以下设 $A,B>0$。

令
$$
x_{i}=\frac{|a_{i}|}{A},\qquad y_{i}=\frac{|b_{i}|}{B}.
$$
则
$$
\sum_{i=1}^n x_{i}^p
=
\frac{\sum_{i} |a_{i}|^p}{A^p}=1,
\qquad
\sum_{i=1}^n y_{i}^q
=
\frac{\sum_{i} |b_{i}|^q}{B^q}=1.
$$

### 第三步：逐项使用 Young 不等式
对每个 $i$，由 Young 不等式，
$$
x_{i} y_{i}\le \frac{x_{i}^p}{p}+\frac{y_{i}^q}{q}.
$$
对 $i=1,\dots,n$ 求和，得
$$
\sum_{i=1}^n x_{i} y_{i}
\le
\frac1p\sum_{i=1}^n x_{i}^p
+
\frac1q\sum_{i=1}^n y_{i}^q
=
\frac1p+\frac1q
=1.
$$
代回 $x_{i},y_{i}$，得到
$$
\sum_{i=1}^n \frac{|a_{i}|}{A}\frac{|b_{i}|}{B}\le 1,
$$
即
$$
\sum_{i=1}^n |a_{i} b_{i}|
\le
AB
=
\left(\sum_{i=1}^n |a_{i}|^p\right)^{1/p}
\left(\sum_{i=1}^n |b_{i}|^q\right)^{1/q}.
$$
这就是 Hölder 不等式。

### 边界情形
当 $p=1$ 时，$q=\infty$，Hölder 不等式为
$$
\sum_{i=1}^n |a_{i} b_{i}|
\le
\left(\sum_{i=1}^n |a_{i}|\right)\max_{1\le i\le n}|b_{i}|,
$$
这是显然的。类似地可处理 $p=\infty$。

### 等号条件
在 $p,q\in(1,\infty)$ 且 $A,B>0$ 时，等号成立当且仅当存在常数 $c>0$，使得
$$
|a_{i}|^p=c\,|b_{i}|^q,\qquad i=1,\dots,n.
$$
等价地，序列 $(|a_{i}|^p)$ 与 $(|b_{i}|^q)$ 成比例。

一般测度形式的 Hölder 不等式
$$
\int |fg|\,d\mu
\le
\left(\int |f|^p\,d\mu\right)^{1/p}
\left(\int |g|^q\,d\mu\right)^{1/q}
$$
也可用完全相同的 Young 不等式加归一化方法证明。
