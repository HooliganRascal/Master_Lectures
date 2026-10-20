# SOR收敛的必要条件和Ostrowski-Reich定理
---
下面按通常的 SOR 记号证明。设

$$
A=D-L-U,
$$

其中 $D=\operatorname{diag}(A)$，$L$ 为严格下三角部分，$U$ 为严格上三角部分。SOR 迭代矩阵为

$$
T_{\omega}=(D-\omega L)^{-1}\big((1-\omega)D+\omega U\big).
$$

有限维线性迭代 $x^{(k+1)}=T_{\omega} x^{(k)}+g$ 对任意初值收敛，当且仅当

$$
\rho(T_{\omega})<1.
$$

---

## 1. 必要性：若全局收敛，则 $0<\omega<2$

由 SOR 迭代矩阵行列式：

$$
\det T_{\omega}
=
\frac{\det\big((1-\omega)D+\omega U\big)}
{\det(D-\omega L)}.
$$

因为 $U$ 是严格上三角，所以 $(1-\omega)D+\omega U$ 是上三角矩阵，对角元为 $(1-\omega)D_{ii}$，故

$$
\det\big((1-\omega)D+\omega U\big)
=(1-\omega)^n\det D.
$$

又因为 $L$ 是严格下三角，$D-\omega L$ 是下三角矩阵，对角元为 $D_{ii}$，故

$$
\det(D-\omega L)=\det D.
$$

因此

$$
\det T_{\omega}=(1-\omega)^n.
$$

若迭代全局收敛，则 $\rho(T_{\omega})<1$。设 $T_{\omega}$ 的特征值为 $\lambda_{1},\dots,\lambda_{n}$，则

$$
|\det T_{\omega}|=\prod_{i=1}^n|\lambda_{i}|
\le \rho(T_{\omega})^n<1.
$$

于是

$$
|1-\omega|^n<1,
$$

即

$$
|1-\omega|<1.
$$

所以

$$
0<\omega<2.
$$

因此 $0<\omega<2$ 是 SOR 全局收敛的必要条件。

---

## 2. 充分性：若 $A$ 对称正定且 $0<\omega<2$，则 SOR 全局收敛

这是经典的 Ostrowski–Reich 定理。

因为 $A$ 对称正定，所以

$$
A=D-L-L^T,
$$

且 $D$ 正定。记

$$
M=D-\omega L.
$$

SOR 迭代矩阵为

$$
T_{\omega}=(D-\omega L)^{-1}\big((1-\omega)D+\omega L^T\big).
$$

先算恒等式：

$$
I-T_{\omega}
=
(D-\omega L)^{-1}A\cdot \omega.
$$

因为

$$
\begin{aligned}
I-T_{\omega}
&=(D-\omega L)^{-1}\Big[(D-\omega L)-\big((1-\omega)D+\omega L^T\big)\Big]\\
&=(D-\omega L)^{-1}\big[\omega D-\omega L-\omega L^T\big]\\
&=\omega(D-\omega L)^{-1}A.
\end{aligned}
$$

所以

$$
T_{\omega}=I-\omega(D-\omega L)^{-1}A.
$$

令 $M=D-\omega L$，则

$$
T_{\omega}=I-\omega M^{-1}A.
$$

考虑矩阵

$$
A-T_{\omega}^*AT_{\omega}.
$$

直接代入：

$$
\begin{aligned}
A-T_{\omega}^*AT_{\omega}
&=
A-\big(I-\omega A M^{-*}\big)A\big(I-\omega M^{-1}A\big)\\
&=\omega A M^{-*}\big(M^*+M-\omega A\big)M^{-1}A.
\end{aligned}
$$

而

$$
M^*+M-\omega A
=
(D-\omega L^T)+(D-\omega L)-\omega(D-L-L^T)
=(2-\omega)D.
$$

因此

$$
A-T_{\omega}^*AT_{\omega}
=
\omega(2-\omega)A M^{-*}D M^{-1}A.
$$

当 $0<\omega<2$ 时，$D$ 正定，且 $M$ 可逆，所以

$$
M^{-*}DM^{-1}
$$

正定。又 $A$ 正定，故

$$
A-T_{\omega}^*AT_{\omega}
$$

正定。

设 $\lambda$ 是 $T_{\omega}$ 的任一特征值，对应特征向量 $x\ne0$，即

$$
T_{\omega} x=\lambda x.
$$

因为 $A-T_{\omega}^*AT_{\omega}$ 正定，所以

$$
x^*(A-T_{\omega}^*AT_{\omega})x>0.
$$

但

$$
x^*(A-T_{\omega}^*AT_{\omega})x
=
x^*Ax-(T_{\omega} x)^*A(T_{\omega} x)
=
(1-|\lambda|^2)x^*Ax.
$$

由于 $A$ 正定，$x^*Ax>0$，于是

$$
1-|\lambda|^2>0.
$$

所以

$$
|\lambda|<1.
$$

这对 $T_{\omega}$ 的所有特征值都成立，因此

$$
\rho(T_{\omega})<1.
$$

于是对任意初始向量 $x^{(0)}$，误差满足

$$
e^{(k)}=T_{\omega}^k e^{(0)}\to 0,
$$

故 SOR 迭代全局收敛。

---

## 结论

- 若 $A$ 的主对角元全不为零，则 SOR 全局收敛的必要条件是  
  $$
  \boxed{0<\omega<2.}
  $$

- 若 $A$ 对称正定，且  
  $$
  \boxed{0<\omega<2,}
  $$
  则 SOR 迭代全局收敛，即  
  $$
  \boxed{\rho(T_{\omega})<1.}
  $$

实际上，对对称正定矩阵 $A$，SOR 收敛的充要条件正是

$$
\boxed{0<\omega<2.}
$$

即经典的 **Ostrowski–Reich 定理**。
