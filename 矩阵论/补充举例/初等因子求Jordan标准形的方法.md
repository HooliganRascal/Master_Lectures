# 初等因子求Jordan标准形的方法
---
下面按“从 $\lambda I-A$ 到不变因子，再到初等因子，再到 Jordan 块/最小多项式”的逻辑说明。

---

## 1. 从多项式矩阵 $\lambda I-A$ 得到不变因子

给定 $A\in F^{n\times n}$，构造多项式矩阵
$$
B(\lambda)=\lambda I-A\in F[\lambda]^{n\times n}.
$$
对它作初等行、列变换（交换、乘非零常数、加多项式倍），可化为 Smith 标准形
$$
B(\lambda)\sim \operatorname{diag}(d_{1}(\lambda),\dots,d_{n}(\lambda)),
$$
其中 $d_{i}$ 首一，且
$$
d_{1}\mid d_{2}\mid\cdots\mid d_{n}.
$$
这些 $d_{i}(\lambda)$ 就是 $A$ 的**不变因子**。

等价地用行列式因子计算：令 $D_{k}(\lambda)$ 为 $B(\lambda)$ 的所有 $k$ 阶子式的首一最大公因式，$D_{0}=1$。则
$$
d_{k}(\lambda)=\frac{D_{k}(\lambda)}{D_{k-1}(\lambda)},\qquad k=1,\dots,n.
$$
并且
$$
D_{k}=d_{1}d_{2}\cdots d_{k},\qquad
D_{n}=\det(\lambda I-A)=\chi_{A}(\lambda).
$$
详细推导见[k阶子式的最大公因式](k阶子式的最大公因式.md)，所以
$$
\prod_{i=1}^n d_{i}(\lambda)=\chi_{A}(\lambda).
$$

---

## 2. 从不变因子得到初等因子组

把每个不变因子分解成不可约多项式的幂：
$$
d_{i}(\lambda)=\prod_{j} p_{j}(\lambda)^{e_{ij}}.
$$
把所有非平凡的幂
$$
p_{j}(\lambda)^{e_{ij}}\qquad (e_{ij}>0)
$$
收集起来，按重数计入，得到的就是**初等因子组**。注意：同一个不可约因子在不同 $d_{i}$ 中的幂要分别作为初等因子，不要先合并。

在代数闭域（如 $\mathbb C$）上，不可约因子都是一次的，所以初等因子形如
$$
(\lambda-\lambda_{0})^e.
$$
每个这样的初等因子[对应一个 $e\times e$ 的 Jordan 块](k阶子式的最大公因式.md)
$$
J_{e}(\lambda_{0}).
$$
因此初等因子组与 Jordan 标准形的 Jordan 块一一对应。

---

## 3. 为什么初等因子的“幂次相加”等于 $n$

对于 $n\times n$ 矩阵，所有初等因子的次数之和等于
$$
\sum_{i} \deg d_{i}(\lambda)
=\deg\prod_{i} d_{i}(\lambda)
=\deg \chi_{A}(\lambda)
=n.
$$
从 Jordan 标准形看更直观：若
$$
J=\operatorname{diag}(J_{e_{1}}(\lambda_{1}),\dots,J_{e_{t}}(\lambda_{t})),
$$
则初等因子组是
$$
\{(\lambda-\lambda_{1})^{e_{1}},\dots,(\lambda-\lambda_{t})^{e_{t}}\},
$$
而每个初等因子的指数 $e_{i}$ 正是对应 Jordan 块的阶数，所以
$$
e_{1}+\cdots+e_{t}=n.
$$
若固定一个特征值 $\lambda_{0}$，则所有形如 $(\lambda-\lambda_{0})^e$ 的初等因子的指数和，等于该特征值的代数重数；所有特征值再相加就是 $n$。

---

## 4. 与最小多项式的关系

矩阵 $A$ 的最小多项式 $m_{A}(\lambda)$ 等于所有初等因子的最小公倍式：
$$
m_{A}(\lambda)=\operatorname{lcm}\{\text{所有初等因子}\}.
$$
也就是说，对每个特征值 $\lambda_{0}$，取该特征值对应的初等因子中**最高幂次**：
$$
m_{A}(\lambda)=\prod_{\lambda_{0}}(\lambda-\lambda_{0})^{\max e},
$$
其中最大值取遍所有 $(\lambda-\lambda_{0})^e$。

在不变因子框架中，
$$
m_{A}(\lambda)=d_{n}(\lambda),
$$
即最后一个（最大）不变因子。因为 $d_{1}\mid\cdots\mid d_{n}$，所以 $d_{n}$ 含有每个不可约因子的最高幂。

对比：
- 特征多项式：每个特征值取初等因子指数之**和**；
- 最小多项式：每个特征值取初等因子指数之**最大值**。

---

## 5. 块对角矩阵的最小多项式

若
$$
A=\operatorname{diag}(A_{1},\dots,A_{s}),
$$
则
$$
m_{A}(\lambda)=\operatorname{lcm}\bigl(m_{A_{1}}(\lambda),\dots,m_{A_{s}}(\lambda)\bigr).
$$
原因是：多项式 $p(\lambda)$ 零化 $A$，即 $p(A)=0$，当且仅当它对每个块都有 $p(A_{i})=0$。因此最小零化多项式就是各块最小多项式的最小公倍式。

对 Jordan 标准形
$$
J=\operatorname{diag}(J_{e_{1}}(\lambda_{1}),\dots,J_{e_{t}}(\lambda_{t})),
$$
有
$$
m_{J}(\lambda)
=\operatorname{lcm}\bigl((\lambda-\lambda_{1})^{e_{1}},\dots,(\lambda-\lambda_{t})^{e_{t}}\bigr)
=\prod_{\lambda_{0}}(\lambda-\lambda_{0})^{\max_{\lambda_{i}=\lambda_{0}} e_{i}}.
$$
而整体初等因子组正是各 Jordan 块初等因子的并集，所以
$$
m_{J}=\operatorname{lcm}\{\text{整体初等因子组}\}.
$$

注意一般不是乘积，而是最小公倍式。例如
$$
J=\operatorname{diag}(J_{1}(0),J_{2}(0)).
$$
初等因子为 $\lambda,\lambda^2$，总次数 $1+2=3$，所以矩阵是 $3\times3$；但
$$
m_{J}=\operatorname{lcm}(\lambda,\lambda^2)=\lambda^2,
$$
不是 $\lambda^3$。特征多项式才是 $\lambda^3$。

---

## 总结

- $\lambda I-A$ 的 Smith 标准形对角元给出不变因子 $d_{1}\mid\cdots\mid d_{n}$。
- 分解各 $d_{i}$ 成不可约幂，收集起来得到初等因子组。
- 初等因子总次数满足
  $$
  \sum \deg(\text{初等因子})=\sum_{i}\deg d_{i}=n.
  $$
- 每个初等因子 $(\lambda-\lambda_{0})^e$ 对应一个 $e$ 阶 Jordan 块。
- 最小多项式
  $$
  m_{A}=d_{n}=\operatorname{lcm}\{\text{初等因子组}\}.
  $$
- 块对角矩阵
  $$
  m_{\operatorname{diag}(A_{1},\dots,A_{s})}
  =\operatorname{lcm}(m_{A_{1}},\dots,m_{A_{s}}).
  $$
- 特征多项式取初等因子指数的“和”，最小多项式取每个特征值对应指数的“最大值”。
