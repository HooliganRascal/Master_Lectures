# 最小多项式和Jordan标准形的关系
---
是的，**矩阵 $A$ 的最小多项式等于其所有 Jordan 块的最小多项式的首一最小公倍式（lcm）**。更准确地说：

若
$$
A\sim \operatorname{diag}(J_{m_{1}}(\lambda_{1}),\dots,J_{m_{t}}(\lambda_{t})),
$$
其中
$$
J_{m}(\lambda)=
\begin{pmatrix}
\lambda&1&&\\
&\ddots&\ddots&\\
&&\ddots&1\\
&&&\lambda
\end{pmatrix}_{m\times m},
$$
则每个 Jordan 块的最小多项式为
$$
\mu_{J_{m}(\lambda)}(x)=(x-\lambda)^m.
$$
于是
$$
\mu_{A}(x)=\operatorname{lcm}\bigl(\mu_{J_{m_{1}}(\lambda_{1})},\dots,\mu_{J_{m_{t}}(\lambda_{t})}\bigr).
$$

等价地，按特征值合并：对每个特征值 $\lambda$，看它在 Jordan 标准形中对应的**最大 Jordan 块的阶数**，记为 $r_\lambda$，则
$$
\mu_{A}(x)=\prod_{\lambda}(x-\lambda)^{r_\lambda}.
$$
也就是说，同一特征值的不同 Jordan 块，在最小多项式中只取**最高次幂**，不是把各块次数相加。

---

### 为什么是最小公倍式？

块对角矩阵的多项式作用为
$$
p(A)=\operatorname{diag}\bigl(p(J_{m_{1}}(\lambda_{1})),\dots,p(J_{m_{t}}(\lambda_{t}))\bigr).
$$
所以
$$
p(A)=0
\iff p(J_{m_{i}}(\lambda_{i}))=0\quad \forall i.
$$
而
$$
p(J_{m}(\lambda))=0
\iff (x-\lambda)^m\mid p(x).
$$
因此 $p$ 必须同时是所有 $(x-\lambda_{i})^{m_{i}}$ 的倍数，最小的这种首一多项式正是它们的最小公倍式。

---

### 例子

设
$$
A\sim \operatorname{diag}\bigl(J_{2}(1),\,J_{3}(1),\,J_{1}(2)\bigr).
$$
各 Jordan 块的最小多项式分别是
$$
(x-1)^2,\qquad (x-1)^3,\qquad (x-2).
$$
所以
$$
\mu_{A}(x)=\operatorname{lcm}\bigl((x-1)^2,(x-1)^3,(x-2)\bigr)
=(x-1)^3(x-2).
$$
注意特征多项式是
$$
\chi_{A}(x)=(x-1)^{2+3}(x-2)=(x-1)^5(x-2),
$$
但最小多项式只取同一特征值的**最大块阶数**。

---

### 常见误区

- **不是把各 Jordan 块的最小多项式直接相乘**。同一特征值要取最高次幂，即 lcm。
- 如果只有一个 Jordan 块 $J_{m}(\lambda)$，那么
  $$
  \mu_{A}(x)=\chi_{A}(x)=(x-\lambda)^m.
  $$
- 如果 $A$ 可对角化，则所有 Jordan 块都是 $1$ 阶，所以
  $$
  \mu_{A}(x)=\prod_{\lambda\in\sigma(A)}(x-\lambda),
  $$
  即最小多项式无重根。

所以你的说法是对的：  
$$
\boxed{\mu_{A}=\operatorname{lcm}\{\mu_{J}:J\text{ 是 }A\text{ 的 Jordan 块}\}}
$$
首一化意义下成立。
