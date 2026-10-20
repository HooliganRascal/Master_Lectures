# 谱半径控制迭代格式的长期收敛速度与 Gelfand 公式
先把两个概念分开：

- **谱半径的定义**就是  
  $$
  \rho(\bm B)=\max_{i}|\lambda_{i}(\bm B)|.
  $$
  所以“谱半径是最大特征值模”不是 Gelfand 公式推导出来的，而是定义。

- **Gelfand 公式**说的是：对任意矩阵范数 $\|\cdot\|$，
  $$
  \boxed{\lim_{k\to\infty}\|\bm B^k\|^{1/k}=\rho(\bm B).}
  $$
  它把“矩阵幂的渐近增长率”和“最大特征值模”联系起来了。

---

## 1. 为什么渐近收敛速度由谱半径控制

迭代误差满足
$$
\bm e^{(k)}=\bm B^k\bm e^{(0)}.
$$
因此第 $k$ 步最坏误差由 $\|\bm B^k\|$ 控制：
$$
\sup_{\|\bm e^{(0)}\|=1}\|\bm e^{(k)}\|
=
\|\bm B^k\|.
$$
Gelfand 公式给出
$$
\|\bm B^k\|^{1/k}\to \rho(\bm B).
$$
也就是说，最坏误差的**几何平均每步衰减因子**趋于 $\rho(\bm B)$。更具体地，任意 $\varepsilon>0$，当 $k$ 足够大时，
$$
\|\bm B^k\|\lesssim (\rho(\bm B)+\varepsilon)^k.
$$
所以若 $\rho(\bm B)<1$，误差最终按大约 $\rho(\bm B)^k$ 的速度衰减；$\rho(\bm B)$ 越小，长期收敛越快。

但注意：这是**渐近、最坏情形**意义下的速度。**非正规矩阵可能一开始误差增大**，即 $\rho(\bm B)<1$ 但 $\|\bm B\|>1$。**长期指数速度仍由谱半径决定**。

---

## 2. Gelfand 公式为什么成立：下界和上界

令
$$
r=\rho(\bm B)=\max_{i}|\lambda_{i}(\bm B)|.
$$
要证明
$$
\lim_{k\to\infty}\|\bm B^k\|^{1/k}=r,
$$
就是证明
$$
r\le \liminf_{k\to\infty}\|\bm B^k\|^{1/k}
\le
\limsup_{k\to\infty}\|\bm B^k\|^{1/k}
\le r.
$$

### 下界：增长率不能小于最大特征值模

取一个最大模特征值 $\lambda$，$|\lambda|=r$，对应特征向量 $\bm v\neq0$：
$$
\bm B\bm v=\lambda\bm v.
$$
于是
$$
\bm B^k\bm v=\lambda^k\bm v.
$$
因此
$$
|\lambda|^k\|\bm v\|
=
\|\bm B^k\bm v\|
\le
\|\bm B^k\|\,\|\bm v\|.
$$
约掉 $\|\bm v\|$，得
$$
\|\bm B^k\|^{1/k}\ge |\lambda|=r.
$$
所以
$$
\liminf_{k\to\infty}\|\bm B^k\|^{1/k}\ge r.
$$
直观上：最大模特征方向上的分量每步乘以 $|\lambda|=r$，矩阵幂的范数不可能比这个增长得更慢。

### 上界：增长率不能大于最大特征值模

用 Jordan 标准形：
$$
\bm B=\bm S\bm J\bm S^{-1},
$$
其中每个 Jordan 块形如
$$
J_{i}=\lambda_{i}\bm I+\bm N_{i},\qquad \bm N_{i}^{\,m_{i}}=0.
$$
于是
$$
J_{i}^k
=
\sum_{j=0}^{m_{i}-1}\binom{k}{j}\lambda_{i}^{k-j}\bm N_{i}^j.
$$
因此 $\bm B^k$ 的元素最多按
$$
C k^{m-1}|\lambda_{i}|^k
$$
增长，而所有 $|\lambda_{i}|\le r$，所以存在常数 $C$ 使
$$
\|\bm B^k\|\le C k^{m-1}r^k.
$$
开 $k$ 次方：
$$
\|\bm B^k\|^{1/k}
\le
C^{1/k}k^{(m-1)/k}r
\to r.
$$
所以
$$
\limsup_{k\to\infty}\|\bm B^k\|^{1/k}\le r.
$$

下界和上界合起来：
$$
r\le \liminf \|\bm B^k\|^{1/k}
\le \limsup \|\bm B^k\|^{1/k}
\le r,
$$
故
$$
\boxed{\lim_{k\to\infty}\|\bm B^k\|^{1/k}=r=\rho(\bm B).}
$$

---

## 3. 关键点：不是 $\|\bm B\|=\rho(\bm B)$，而是 $\|\bm B^k\|^{1/k}\to\rho(\bm B)$

一般只有
$$
\rho(\bm B)\le \|\bm B\|.
$$
例如
$$
\bm B=
\begin{pmatrix}
0&M\\
0&0
\end{pmatrix},
\qquad
\rho(\bm B)=0,
$$
但
$$
\|\bm B\|_2=M.
$$
不过
$$
\bm B^2=0,
$$
所以
$$
\|\bm B^k\|^{1/k}\to0=\rho(\bm B).
$$
这正是 Gelfand 公式的含义：**单个矩阵的范数可能远大于谱半径，但矩阵幂的渐近几何增长率由谱半径控制。**

---

## 4. 关于“下界是后者，上界也是后者？”

不是循环。逻辑是：

- 下界：由最大模特征向量得到  
  $$
  \|\bm B^k\|^{1/k}\ge r,
  $$
  所以极限不可能小于 $r$。
- 上界：由 Jordan 标准形知道所有模态都被 $r^k$ 加上多项式因子控制，而多项式因子开 $k$ 次方趋于 $1$，所以  
  $$
  \|\bm B^k\|^{1/k}\lesssim r,
  $$
  所以极限不可能大于 $r$。

两边一夹，极限只能等于 $r$。因此 Gelfand 公式成立。

总结成一句话：

$$
\boxed{
\text{谱半径是最大特征值模；}
}\\
\boxed{
\text{Gelfand 公式说明矩阵幂范数的渐近几何增长率正好等于这个最大特征值模。}
}
$$

因此迭代误差 $\bm e^{(k)}=\bm B^k\bm e^{(0)}$ 的长期最坏收敛速度由 $\rho(\bm B)$ 控制，而不是由某一次矩阵范数 $\|\bm B\|$ 控制。
