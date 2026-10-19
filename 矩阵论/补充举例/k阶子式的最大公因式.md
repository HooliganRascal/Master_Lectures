# k阶子式的最大公因式
---
下面逐点说明，并把之前当作结论用的地方补上论证。

---

## 1. 为什么 $D_{k}=d_{1}d_{2}\cdots d_{k}$

设
$$
B(\lambda)=\lambda I-A.
$$
对 $B(\lambda)$ 作初等行、列变换，可化为 Smith 标准形
$$
\operatorname{diag}(d_{1}(\lambda),\dots,d_{n}(\lambda)),
\qquad d_{1}\mid d_{2}\mid\cdots\mid d_{n}.
$$
记 $D_{k}(\lambda)$ 为 $B(\lambda)$ 的所有 $k$ 阶子式的首一最大公因式，称为 $k$ 阶行列式因子。初等行、列变换不改变各阶子式的最大公因式，所以可对 Smith 标准形计算。

在对角矩阵
$$
\operatorname{diag}(d_{1},\dots,d_{n})
$$
中，一个非零的 $k$ 阶子式，必是取某 $k$ 个对角元相乘：
$$
d_{i_{1}}d_{i_{2}}\cdots d_{i_{k}},
\qquad i_{1} < \cdots < i_{k}.
$$
由于整除链
$$
d_{1}\mid d_{2}\mid\cdots\mid d_{n},
$$
有
$$
d_{1}d_{2}\cdots d_{k} \mid d_{i_{1}}d_{i_{2}}\cdots d_{i_{k}},
$$
因为 $i_{j}\ge j$，所以 $d_{j}\mid d_{i_{j}}$。

另一方面，取前 $k$ 行前 $k$ 列，得到的 $k$ 阶子式正好是
$$
d_{1}d_{2}\cdots d_{k}.
$$
因此所有 $k$ 阶子式的最大公因式就是
$$
D_{k}=d_{1}d_{2}\cdots d_{k}.
$$
于是
$$
d_{k}=\frac{D_{k}}{D_{k-1}}.
$$
这就是不变因子与行列式因子的关系。

---

## 2. 初等因子组与 Jordan 块的对应

在代数闭域（如 $\mathbb C$）上讨论。先看单个 Jordan 块
$$
J_{e}(\lambda_{0})=
\begin{pmatrix}
\lambda_{0}&1&&\\
&\lambda_{0}&\ddots&\\
&&\ddots&1\\
&&&\lambda_{0}
\end{pmatrix}.
$$
其特征矩阵为
$$
\lambda I-J_{e}(\lambda_{0})=
\begin{pmatrix}
\lambda-\lambda_{0}&-1&&\\
&\lambda-\lambda_{0}&\ddots&\\
&&\ddots&-1\\
&&&\lambda-\lambda_{0}
\end{pmatrix}.
$$
对于 $k < e$，存在 $k$ 阶子式等于 $\pm1$，因为
> 对 Jordan 块
> $$
> J_{e}(\lambda_{0})=
> \begin{pmatrix}
> \lambda_{0}&1&&\\
> &\lambda_{0}&\ddots&\\
> &&\ddots&1\\
> &&&\lambda_{0}
> \end{pmatrix},
> $$
> 其特征矩阵
> $$
> B(\lambda)=\lambda I-J_{e}(\lambda_{0})
> $$
> 的非零元素只有两类：
> 
> - 对角元：$B_{ii}=\lambda-\lambda_{0}$；
> - 超对角元：$B_{i,i+1}=-1$；
> - 其余为 $0$。
> 
> 现在取 $1\le k < e$。选取 $B(\lambda)$ 的
> 
> $$
> \text{行 }1,2,\dots,k,\qquad
> \text{列 }2,3,\dots,k+1
> $$
> 
> 组成的 $k$ 阶子矩阵。由于 $k+1\le e$，这些行列都合法。这个子矩阵形如
> 
> $$
> \begin{pmatrix}
> -1&0&\cdots&0\\
> \lambda-\lambda_{0}&-1&\ddots&\vdots\\
> 0&\lambda-\lambda_{0}&\ddots&0\\
> \vdots&&\ddots&-1\\
> 0&\cdots&0&\lambda-\lambda_{0}&-1
> \end{pmatrix}
> $$
> 
> 更准确地说，它是下三角矩阵，主对角线全是 $-1$，次对角线是 $\lambda-\lambda_{0}$，上三角全为 $0$。因此其行列式为
> 
> $$
> (-1)^k=\pm 1.
> $$
> 
> 所以对每个 $k < e$，都存在一个 $k$ 阶子式等于 $\pm1$。
> 
> 于是 $k$ 阶行列式因子 $D_{k}$ 作为所有 $k$ 阶子式的首一最大公因式，必然为
> 
> $$
> D_{k}=1,\qquad k < e.
> $$
> 
> 而
> $$
> D_{e}=\det(\lambda I-J_{e}(\lambda_{0}))
> =(\lambda-\lambda_{0})^e.
> $$
> 
> 因此该 Jordan 块的不变因子为
> 
> $$
> \underbrace{1,\dots,1}_{e-1\text{ 个}},
> (\lambda-\lambda_{0})^e,
> $$
> 
> 所以它的初等因子组只有一个元素：
> 
> $$
> \{(\lambda-\lambda_{0})^e\}.
> $$
> 
> 这就是“一个 $e$ 阶 Jordan 块对应一个初等因子 $(\lambda-\lambda_{0})^e$”的关键论证。选取行 $1,\dots,k$、列 $2,\dots,k+1$ 的目的，就是专门取到那些 $-1$ 的超对角元，从而避开变量 $\lambda-\lambda_{0}$，得到非零常数子式。

回到 $k$ 阶子式和 Jordan 块的关系，所以
$$
D_{k}=1,\qquad k < e.
$$
而
$$
D_{e}=\det(\lambda I-J_{e}(\lambda_{0}))
=(\lambda-\lambda_{0})^e.
$$
因此该 Jordan 块的不变因子为
$$
\underbrace{1,\dots,1}_{e-1\text{ 个}},
(\lambda-\lambda_{0})^e.
$$
所以它的初等因子组只有一个元素：
$$
\{(\lambda-\lambda_{0})^e\}.
$$
也就是说，一个 $e$ 阶 Jordan 块恰好贡献一个初等因子 $(\lambda-\lambda_{0})^e$。

再看块对角矩阵
$$
J=\operatorname{diag}(J_{e_{1}}(\lambda_{1}),\dots,J_{e_{t}}(\lambda_{t})).
$$
其特征矩阵也是块对角：
$$
\lambda I-J=
\operatorname{diag}\bigl(\lambda I-J_{e_{1}}(\lambda_{1}),\dots,
\lambda I-J_{e_{t}}(\lambda_{t})\bigr).
$$
Smith 标准形有一个标准性质：块对角矩阵的初等因子组，等于各块的初等因子组按重数取并。理由是：对每个不可约多项式 $p(\lambda)$，各块不变因子中 $p$ 的指数序列在直和下会合并排序；排序不改变指数多重集，所以非平凡幂的多重集就是各块的并。于是整体初等因子组为
$$
\{(\lambda-\lambda_{1})^{e_{1}},\dots,(\lambda-\lambda_{t})^{e_{t}}\}.
$$
因此每个初等因子 $(\lambda-\lambda_{0})^e$ 对应一个 $e$ 阶 Jordan 块。

反过来，给定初等因子组
$$
\{(\lambda-\lambda_{1})^{e_{1}},\dots,(\lambda-\lambda_{t})^{e_{t}}\},
$$
取直和
$$
\operatorname{diag}(J_{e_{1}}(\lambda_{1}),\dots,J_{e_{t}}(\lambda_{t})),
$$
它的初等因子组正好就是给定的这一组。而初等因子组是相似完全不变量，所以任何具有这组初等因子的矩阵都相似于这个直和。这就是 Jordan 标准形。

所以对应关系是：

$$
\boxed{
(\lambda-\lambda_{0})^e
\quad\longleftrightarrow\quad
J_{e}(\lambda_{0})
}
$$

按重数一一对应。若同一特征值出现多个初等因子，就对应多个相应阶数的 Jordan 块。

---

## 3. Jordan 块排列不同，最小多项式会不同吗？

不会。Jordan 块的排列不同，只是把直和项交换顺序。例如
$$
A=J_{2}(0)\oplus J_{1}(0),
\qquad
B=J_{1}(0)\oplus J_{2}(0).
$$
它们只是块排列不同，实际上存在置换矩阵 $P$ 使
$$
B=P^{-1}AP,
$$
所以 $A$ 与 $B$ 相似。相似矩阵有相同的最小多项式、特征多项式、初等因子组。

最小多项式公式为
$$
m_{A}(\lambda)
=
\operatorname{lcm}\{\text{所有初等因子}\}.
$$
对于上面的例子，初等因子组都是
$$
\{\lambda,\lambda^2\},
$$
因此
$$
m_{A}(\lambda)=m_{B}(\lambda)
=\operatorname{lcm}(\lambda,\lambda^2)
=\lambda^2.
$$
最小公倍式与顺序无关，所以块怎么排列都不影响最小多项式。

但要区分：如果改变的不是“排列”，而是初等因子组本身，例如把
$$
J_{2}(0)\oplus J_{1}(0)
$$
换成
$$
J_{3}(0),
$$
那最小多项式会从 $\lambda^2$ 变成 $\lambda^3$。这不是排列变化，而是 Jordan 块的多重集变了。

---

## 总结

1. Smith 标准形为 $\operatorname{diag}(d_{1},\dots,d_{n})$ 时，
   $$
   D_{k}=d_{1}d_{2}\cdots d_{k},
   $$
   因为所有 $k$ 阶子式都被 $d_{1}\cdots d_{k}$ 整除，且 $d_{1}\cdots d_{k}$ 本身就是一个 $k$ 阶子式。

2. 单个 $e$ 阶 Jordan 块 $J_{e}(\lambda_{0})$ 的初等因子正是 $(\lambda-\lambda_{0})^e$。块对角矩阵的初等因子组是各块初等因子组按重数取并，所以初等因子与 Jordan 块一一对应。

3. Jordan 块排列不同不影响最小多项式；最小多项式是
   $$
   m_{A}=\operatorname{lcm}\{\text{初等因子}\},
   $$
   只依赖于初等因子组的多重集，与块的排列顺序无关。
