# 矩阵分析及其应用

讨论 $\mathbb C^{m\times n}$ 中矩阵序列与矩阵级数的收敛性，以及方阵函数 $f(\bm A)$ 的定义与计算，判据最终都归结为谱半径 $\rho(\bm A)$

## 矩阵序列

### 矩阵序列的极限
- 设有矩阵序列 $\{\bm A^{(k)}\}$，其中
    $$\bm A^{(k)}=(a_{ij}^{(k)})_{m\times n}\in\mathbb C^{m\times n}\qquad(k=1,2,\cdots)$$
    若当 $k\rightarrow\infty$ 时每个元素都有极限 $a_{ij}^{(k)}\rightarrow a_{ij}$，则称 $\{\bm A^{(k)}\}$ **收敛**，并称 $\bm A=(a_{ij})$ 为它的**极限**，记为
    $$\lim_{k\rightarrow\infty}\bm A^{(k)}=\bm A\qquad\text{或}\qquad\bm A^{(k)}\rightarrow\bm A$$
    不收敛的矩阵序列称为**发散**，矩阵序列的收敛**等价于 $mn$ 个元素数列同时收敛**
- 极限的运算性质
    - 线性性：若 $\bm A^{(k)}\rightarrow\bm A$，$\bm B^{(k)}\rightarrow\bm B$，则 $\lim_{k\rightarrow\infty}(\alpha\bm A^{(k)}+\beta\bm B^{(k)})=\alpha\bm A+\beta\bm B$
    - 乘法：若 $\bm A^{(k)}\rightarrow\bm A_{m\times n}$，$\bm B^{(k)}\rightarrow\bm B_{n\times l}$，则 $\lim_{k\rightarrow\infty}\bm A^{(k)}\bm B^{(k)}=\bm A\bm B$
    - 求逆：若 $\bm A^{(k)},\bm A$ 都可逆且 $\bm A^{(k)}\rightarrow\bm A$，则 $(\bm A^{(k)})^{-1}\rightarrow\bm A^{-1}$
- 定理3.1（用范数刻画极限）：设 $\bm A^{(k)}\in\mathbb C^{m\times n}$，$\Vert * \Vert$ 是 $\mathbb C^{m\times n}$ 上的**任何一种**矩阵范数，则
    $$\bm A^{(k)}\rightarrow\bm A\iff\Vert\bm A^{(k)}-\bm A\Vert\rightarrow 0$$
    特别地
    $$\bm A^{(k)}\rightarrow\bm O\iff\Vert\bm A^{(k)}\Vert\rightarrow 0$$
    这只是范数等价性的直接推论，检验极限时**任选一种范数**即可

### 收敛矩阵
- 定义3.2：若存在常数 $M>0$，使对任意 $k$ 都有
    $$\vert a_{ij}^{(k)}\vert<M\qquad(i=1,2,\cdots,m;\ j=1,2,\cdots,n)$$
    则称矩阵序列 $\{\bm A^{(k)}\}$ **有界**
- 定义3.3：设 $\bm A$ 为方阵，若当 $k\rightarrow\infty$ 时 $\bm A^{k}\rightarrow\bm O$，则称 $\bm A$ 为**收敛矩阵**
- 定理3.2（收敛矩阵的判据）：$\bm A$ 为收敛矩阵 $\iff\rho(\bm A)<1$
    - 充分性：由 Jordan 标准形 $\bm A=\bm P\bm J\bm P^{-1}$ 得 $\bm A^{k}=\bm P\bm J^{k}\bm P^{-1}$，其中
        $$\bm J^{k}=\mathrm{diag}\left(\bm J_{1}^{k}(\lambda_{1}),\bm J_{2}^{k}(\lambda_{2}),\cdots,\bm J_{s}^{k}(\lambda_{s})\right)$$
        而 $\bm J_{i}^{k}(\lambda_{i})$ 的元素为 $C_{k}^{l}\lambda_{i}^{k-l}$（$l=0,1,\cdots,m_{i}-1$，$C_{k}^{l}$ 为组合数，并规定 $C_{k}^{l}=0(l>k)$），$\rho(\bm A)<1$ 时 $\vert\lambda_{i}\vert<1$，故 $C_{k}^{l}\lambda_{i}^{k-l}\rightarrow 0$，从而 $\bm A^{k}\rightarrow\bm O$
    - 必要性：$\bm A^{k}\rightarrow\bm O\implies\bm J^{k}\rightarrow\bm O\implies\bm J_{i}^{k}(\lambda_{i})\rightarrow\bm O\implies\vert\lambda_{i}\vert<1$，即 $\rho(\bm A)<1$
- 定理3.3（充分条件）：只要**有一种**矩阵范数使 $\Vert\bm A\Vert<1$，就有 $\bm A^{k}\rightarrow\bm O\ (k\rightarrow\infty)$，这由 $\rho(\bm A)\leq\Vert\bm A\Vert$ 立得，该条件**不是必要的**
- 例：判断 $\bm A=\begin{bmatrix}0.5&0.3\\0.2&0.5\end{bmatrix}$ 是否为收敛矩阵
    - 特征多项式 $\varphi(\lambda)=(\lambda-0.5)^{2}-0.06$，特征值为 $0.5\pm\sqrt{0.06}$，故
        $$\rho(\bm A)=0.5+\sqrt{0.06}\approx 0.745<1$$
    - 所以 $\bm A$ 是收敛矩阵

## 矩阵级数

### 矩阵级数的概念
- 定义3.4：由矩阵序列 $\{\bm A^{(k)}\}$ 构成的无穷和称为**矩阵级数**，记为
    $$\sum_{k=0}^{\infty}\bm A^{(k)}=\bm A^{(0)}+\bm A^{(1)}+\cdots+\bm A^{(k)}+\cdots$$
- 定义3.5：称
    $$\bm S^{(N)}=\sum_{k=0}^{N}\bm A^{(k)}$$
    为矩阵级数的**部分和**，若部分和矩阵序列 $\{\bm S^{(N)}\}$ 收敛于 $\bm S$，则称矩阵级数**收敛**且和为 $\bm S$，不收敛的称为**发散**，矩阵级数的收敛**等价于 $mn$ 个元素级数都收敛**
- 定义3.6：若 $\sum_{k=0}^{\infty}\bm A^{(k)}$ 中的 $mn$ 个数项级数都**绝对收敛**，则称该矩阵级数**绝对收敛**
- 例：设
    $$\bm A^{(k)}=\begin{bmatrix}\frac{1}{2^{k}}&\frac{\pi}{3\cdot4^{k}}\\0&\frac{1}{k(k+1)}\end{bmatrix}\qquad(k=1,2,\cdots)$$
    求 $\sum_{k=1}^{\infty}\bm A^{(k)}$ 的收敛性，部分和为
    $$\bm S^{(N)}=\begin{bmatrix}1-\left(\frac{1}{2}\right)^{N}&\frac{\pi}{9}\left[1-\left(\frac{1}{4}\right)^{N}\right]\\0&\frac{N}{1+N}\end{bmatrix}$$
    于是
    $$\bm S=\lim_{N\rightarrow\infty}\bm S^{(N)}=\begin{bmatrix}1&\frac{\pi}{9}\\0&1\end{bmatrix}$$
    所以该矩阵级数收敛

### 矩阵级数的性质
- 性质1：绝对收敛的矩阵级数一定收敛，且任意调换项的次序后仍然收敛，其和不变
- 性质2：$\sum_{k=0}^{\infty}\bm A^{(k)}$ 绝对收敛 $\iff$ 正项级数 $\sum_{k=0}^{\infty}\Vert\bm A^{(k)}\Vert$ 收敛，其中 $\Vert * \Vert$ 为任何一种矩阵范数，这使矩阵级数的判敛**可以转化为范数级数**
- 性质3：若 $\sum_{k=0}^{\infty}\bm A^{(k)}$ 收敛（或绝对收敛），则对与 $k$ 无关的 $\bm P,\bm Q$，$\sum_{k=0}^{\infty}\bm P\bm A^{(k)}\bm Q$ 也收敛（或绝对收敛），且
    $$\sum_{k=0}^{\infty}\bm P\bm A^{(k)}\bm Q=\bm P\left(\sum_{k=0}^{\infty}\bm A^{(k)}\right)\bm Q$$
- 性质4（乘积）：若两个矩阵级数都绝对收敛，其和分别为 $\bm A$ 与 $\bm B$，则按项相乘所得的级数
    $$\bm S_{3}:\ \sum_{k=0}^{\infty}\left(\sum_{i=0}^{k}\bm A^{(i)}\bm B^{(k-i)}\right)$$
    也绝对收敛，且和为 $\bm A\bm B$，即矩阵级数可以像数项级数一样做 **Cauchy 乘积**

### 矩阵幂级数
- 定理3.4（Neumann 级数）：方阵 $\bm A$ 的幂级数
    $$\sum_{k=0}^{\infty}\bm A^{k}=\bm I+\bm A+\bm A^{2}+\cdots+\bm A^{k}+\cdots$$
    收敛 $\iff$ $\bm A$ 为收敛矩阵，且收敛时
    $$\sum_{k=0}^{\infty}\bm A^{k}=(\bm I-\bm A)^{-1}$$
    - 证明要点：由 $\left(\bm I+\bm A+\cdots+\bm A^{k}\right)(\bm I-\bm A)=\bm I-\bm A^{k+1}$ 得
        $$\bm I+\bm A+\cdots+\bm A^{k}=(\bm I-\bm A)^{-1}-\bm A^{k+1}(\bm I-\bm A)^{-1}$$
        再由 $\bm A^{k+1}\rightarrow\bm O$ 即得结论，这也说明 $\rho(\bm A)<1$ 时 $\bm I-\bm A$ 必可逆
- 定理3.5（截断误差）：若方阵 $\bm A$ 对某一矩阵范数满足 $\Vert\bm A\Vert<1$，则对任何非负整数 $k$，用 $\bm I+\bm A+\cdots+\bm A^{k}$ 近似 $(\bm I-\bm A)^{-1}$ 的误差满足
    $$\Vert(\bm I-\bm A)^{-1}-(\bm I+\bm A+\cdots+\bm A^{k})\Vert\leq\frac{\Vert\bm A\Vert^{k+1}}{1-\Vert\bm A\Vert}$$
- 定理3.6（矩阵幂级数的收敛性）：设幂级数 $f(z)=\sum_{k=0}^{\infty}c_{k}z^{k}$ 的收敛半径为 $r$，则
    $$
    \begin{aligned}
    &\rho(\bm A)<r\implies\sum_{k=0}^{\infty}c_{k}\bm A^{k}\ \text{绝对收敛}\\
    &\rho(\bm A)>r\implies\sum_{k=0}^{\infty}c_{k}\bm A^{k}\ \text{发散}
    \end{aligned}
    $$
    判据只看谱半径，与所用的矩阵范数无关，$\rho(\bm A)=r$ 的情形不在此定理范围内
    - 证明要点：取 $\varepsilon>0$ 使 $\rho(\bm A)+\varepsilon<r$，存在范数使 $\Vert\bm A\Vert\leq\rho(\bm A)+\varepsilon$，从而
        $$\Vert c_{k}\bm A^{k}\Vert\leq\vert c_{k}\vert\left(\rho(\bm A)+\varepsilon\right)^{k}$$
        由比较判别法得绝对收敛；发散的情形由 Jordan 标准形的对角元 $\sum_{k=0}^{\infty}c_{k}\lambda_{i}^{k}$ 看出
- 推论：若幂级数在整个复平面上收敛（$r=+\infty$），则对任何方阵 $\bm A$，$\sum_{k=0}^{\infty}c_{k}\bm A^{k}$ 都绝对收敛
- 例：设 $\bm A=\begin{bmatrix}0.5&0.2\\0.3&1\end{bmatrix}$，讨论 $\sum_{k=0}^{\infty}\frac{k}{2^{k}}\bm A^{k}$ 的收敛性
    - 系数的收敛半径
        $$r=\lim_{k\rightarrow\infty}\left\vert\frac{c_{k}}{c_{k+1}}\right\vert=\lim_{k\rightarrow\infty}\frac{2k}{k+1}=2$$
    - 又 $\bm A$ 的列和范数 $\Vert\bm A\Vert_{1}=1.2<2$，由 $\rho(\bm A)\leq\Vert\bm A\Vert_{1}$ 得 $\rho(\bm A)<2=r$，故该矩阵级数绝对收敛

## 矩阵函数

### 矩阵函数的定义与初等矩阵函数
- 定义3.7：设一元函数 $f(z)$ 能展开为幂级数
    $$f(z)=\sum_{k=0}^{\infty}c_{k}z^{k}\qquad(\vert z\vert<r)$$
    其中 $r>0$ 为收敛半径，当方阵 $\bm A$ 的谱半径满足 $\rho(\bm A)<r$ 时，称收敛的矩阵幂级数之和为**矩阵函数**，记为
    $$f(\bm A)=\sum_{k=0}^{\infty}c_{k}\bm A^{k}$$
- 收敛半径为 $+\infty$ 的初等函数对任何方阵都有定义
    $$\mathrm e^{\bm A}=\bm I+\frac{\bm A}{1!}+\frac{\bm A^{2}}{2!}+\frac{\bm A^{3}}{3!}+\cdots$$
    $$\sin\bm A=\bm A-\frac{\bm A^{3}}{3!}+\frac{\bm A^{5}}{5!}-\cdots$$
    $$\cos\bm A=\bm I-\frac{\bm A^{2}}{2!}+\frac{\bm A^{4}}{4!}-\cdots$$
- 由幂级数推得的恒等式
    $$\mathrm e^{\mathrm i\bm A}=\cos\bm A+\mathrm i\sin\bm A$$
    $$\cos\bm A=\frac{1}{2}\left(\mathrm e^{\mathrm i\bm A}+\mathrm e^{-\mathrm i\bm A}\right)\qquad \sin\bm A=\frac{1}{2\mathrm i}\left(\mathrm e^{\mathrm i\bm A}-\mathrm e^{-\mathrm i\bm A}\right)$$
    $$\cos(-\bm A)=\cos\bm A\qquad \sin(-\bm A)=-\sin\bm A$$
- 一般情况下
    $$\mathrm e^{\bm A}\mathrm e^{\bm B}\neq\mathrm e^{\bm B}\mathrm e^{\bm A}\neq\mathrm e^{\bm A+\bm B}$$
    例如取 $\bm A=\begin{bmatrix}1&1\\0&0\end{bmatrix}$，$\bm B=\begin{bmatrix}1&-1\\0&0\end{bmatrix}$，则 $\bm A^{2}=\bm A,\bm B^{2}=\bm B$，有
    $$\mathrm e^{\bm A}=\bm I+(\mathrm e-1)\bm A\qquad \mathrm e^{\bm B}=\bm I+(\mathrm e-1)\bm B$$
    而 $\bm A+\bm B=\begin{bmatrix}2&0\\0&0\end{bmatrix}$，可算得
    $$
    \mathrm e^{\bm A}\mathrm e^{\bm B}=\begin{bmatrix}\mathrm e^{2}&-(\mathrm e-1)^{2}\\0&1\end{bmatrix}\qquad
    \mathrm e^{\bm B}\mathrm e^{\bm A}=\begin{bmatrix}\mathrm e^{2}&(\mathrm e-1)^{2}\\0&1\end{bmatrix}\qquad
    \mathrm e^{\bm A+\bm B}=\begin{bmatrix}\mathrm e^{2}&0\\0&1\end{bmatrix}
    $$
    三者互不相等，原因是 $\bm A\bm B\neq\bm B\bm A$
- 定理3.7：若 $\bm A\bm B=\bm B\bm A$，则
    $$\mathrm e^{\bm A}\mathrm e^{\bm B}=\mathrm e^{\bm B}\mathrm e^{\bm A}=\mathrm e^{\bm A+\bm B}$$
    - 证明依赖性质4（绝对收敛级数的 Cauchy 乘积）以及 $\bm A\bm B=\bm B\bm A$
    - 推论1：$\mathrm e^{\bm A}\mathrm e^{-\bm A}=\mathrm e^{-\bm A}\mathrm e^{\bm A}=\bm I$，即 $(\mathrm e^{\bm A})^{-1}=\mathrm e^{-\bm A}$
    - 推论2：对整数 $m$，$(\mathrm e^{\bm A})^{m}=\mathrm e^{m\bm A}$
- 当 $\bm A\bm B=\bm B\bm A$ 时，三角恒等式对矩阵也成立
    $$\cos(\bm A+\bm B)=\cos\bm A\cos\bm B-\sin\bm A\sin\bm B$$
    $$\sin(\bm A+\bm B)=\sin\bm A\cos\bm B+\cos\bm A\sin\bm B$$
    $$\cos2\bm A=\cos^{2}\bm A-\sin^{2}\bm A\qquad \sin2\bm A=2\sin\bm A\cos\bm A$$
- 例：$f(z)=\frac{1}{1-z}=\sum_{k=0}^{\infty}z^{k}(\vert z\vert<1)$，当 $\rho(\bm A)<1$ 时
    $$f(\bm A)=\sum_{k=0}^{\infty}\bm A^{k}=(\bm I-\bm A)^{-1}$$
    这正是定理3.4

### 待定系数法
- 设 $\bm A$ 的特征多项式为 $\varphi(\lambda)=\det(\lambda\bm I-\bm A)$，称满足
    $$\left(\mu(\bm A)=\bm O\right)\wedge\left(\mu(\lambda)\mid\varphi(\lambda)\right)$$
    的首一多项式 $\mu(\lambda)$ 为 $\bm A$ 的**最小多项式**，其次数为 $m$（$1\leq m\leq n$）
- 设 $\mu(\lambda)$ 的互异零点为 $\lambda_{1},\lambda_{2},\cdots,\lambda_{s}$，重数为 $r_{1},r_{2},\cdots,r_{s}$，则 $r_{1}+\cdots+r_{s}=m$，且
    $$\mu^{(l)}(\lambda_{i})=0\qquad(l=0,1,\cdots,r_{i}-1;\ i=1,2,\cdots,s)$$
- 由带余除法，把 $f$ 写成
    $$f(z)=\sum_{k=0}^{\infty}c_{k}z^{k}=\mu(z)g(z)+r(z)$$
    其中 $\deg r<m$ 或 $r(z)=0$，由 $\mu(\bm A)=\bm O$ 得
    $$f(\bm A)=\sum_{k=0}^{\infty}c_{k}\bm A^{k}=r(\bm A)$$
    而 $r(z)$ 由 **Hermite 条件**
    $$f^{(l)}(\lambda_{i})=r^{(l)}(\lambda_{i})\qquad(l=0,1,\cdots,r_{i}-1;\ i=1,2,\cdots,s)$$
    唯一确定，这共 $m$ 个条件，恰好定出 $r$ 的 $m$ 个系数
- 这正是**待定系数法**，它表明 $f(\bm A)$ 只依赖 $f$ 及其各阶导数在谱 $\sigma(\bm A)$ 上的值
- 算法
    - 求最小多项式 $\mu(\lambda)$，若只知道特征多项式 $\varphi(\lambda)$，用 $\varphi$ 代替 $\mu$ 也成立，只是 $r$ 的次数更高
    - 设 $r(\lambda)=a_{m-1}\lambda^{m-1}+\cdots+a_{1}\lambda+a_{0}$，用上述 $m$ 个条件解出系数
    - 计算 $r(\bm A)$
- 例：$\bm A=\begin{bmatrix}1&0\\1&2\end{bmatrix}$，$\varphi(\lambda)=(\lambda-1)(\lambda-2)$，取 $r(\lambda)=a\lambda+b$
    - 由 $f(1)=\mathrm e=a+b$、$f(2)=\mathrm e^{2}=2a+b$ 得 $a=\mathrm e^{2}-\mathrm e$，$b=2\mathrm e-\mathrm e^{2}$，于是
        $$\mathrm e^{\bm A}=(\mathrm e^{2}-\mathrm e)\bm A+(2\mathrm e-\mathrm e^{2})\bm I=\begin{bmatrix}\mathrm e&0\\\mathrm e^{2}-\mathrm e&\mathrm e^{2}\end{bmatrix}$$
    - 对 $f(\lambda)=\mathrm e^{t\lambda}$ 同理得
        $$\mathrm e^{t\bm A}=\begin{bmatrix}\mathrm e^{t}&0\\\mathrm e^{2t}-\mathrm e^{t}&\mathrm e^{2t}\end{bmatrix}$$
- 例：若最小多项式比特征多项式次数低，可以用最小多项式减少待定系数，取 $\bm A=\begin{bmatrix}2&0&0\\1&1&1\\1&-1&3\end{bmatrix}$，则 $\varphi(\lambda)=(\lambda-2)^{3}$，但 $2\bm I-\bm A\neq\bm O$ 而 $(2\bm I-\bm A)^{2}=\bm O$，故最小多项式为 $\mu(\lambda)=(\lambda-2)^{2}$，只需 $r(\lambda)=a\lambda+b$
    - 对 $f(\lambda)=\sin\lambda t$，由 $f(2)=\sin2t=2a+b$、$f'(2)=t\cos2t=a$ 得
        $$r(\lambda)=t\cos(2t)\lambda+\sin2t-2t\cos(2t)$$
        于是
        $$\sin t\bm A=t\cos(2t)\bm A+\left(\sin2t-2t\cos(2t)\right)\bm I$$

### 数项级数求和法
- 设 $\bm A$ 的最小多项式（或特征多项式，取次数较低者）为
    $$\mu(\lambda)=\lambda^{m}+b_{1}\lambda^{m-1}+\cdots+b_{m-1}\lambda+b_{m}\qquad(1\leq m\leq n)$$
    由 $\mu(\bm A)=\bm O$ 得
    $$\bm A^{m}+b_{1}\bm A^{m-1}+\cdots+b_{m-1}\bm A+b_{m}\bm I=\bm O$$
    于是可以把高次幂逐次降为低次幂
    $$\bm A^{m+j}=k_{0}^{(j)}\bm I+k_{1}^{(j)}\bm A+\cdots+k_{m-1}^{(j)}\bm A^{m-1}\qquad(j=0,1,2,\cdots)$$
- 代入 $f(\bm A)=\sum_{k=0}^{\infty}c_{k}\bm A^{k}$ 并按 $\bm I,\bm A,\cdots,\bm A^{m-1}$ 合并同类项，原矩阵级数化为 $m$ 个**数项级数**，这 $m$ 个数项级数收敛，逐个求和即得 $f(\bm A)$
- 例：设
    $$\bm A=\begin{bmatrix}\pi&0&0&0\\0&-\pi&0&0\\0&0&0&1\\0&0&0&0\end{bmatrix}$$
    其特征多项式为 $\varphi(\lambda)=\lambda^{4}-\pi^{2}\lambda^{2}$，由 $\varphi(\bm A)=\bm O$ 得
    $$\bm A^{4}=\pi^{2}\bm A^{2}\qquad \bm A^{5}=\pi^{2}\bm A^{3}\qquad\cdots$$
    于是
    $$\sin\bm A=\bm A-\frac{1}{3!}\bm A^{3}+\frac{1}{5!}\bm A^{5}-\cdots=\bm A+\left(-\frac{1}{3!}+\frac{\pi^{2}}{5!}-\cdots\right)\bm A^{3}=\bm A-\frac{1}{\pi^{2}}\bm A^{3}$$

### Jordan 标准形法
- 设 $\bm A$ 的 Jordan 标准形为
    $$\bm P^{-1}\bm A\bm P=\bm J=\mathrm{diag}\left(\bm J_{1},\bm J_{2},\cdots,\bm J_{s}\right)$$
    则 $\bm A^{k}=\bm P\bm J^{k}\bm P^{-1}$，从而
    $$f(\bm A)=\sum_{k=0}^{\infty}c_{k}\bm A^{k}=\bm P\left(\sum_{k=0}^{\infty}c_{k}\bm J^{k}\right)\bm P^{-1}=\bm P\,\mathrm{diag}\left(f(\bm J_{1}),\cdots,f(\bm J_{s})\right)\bm P^{-1}$$
- $f(\bm J_{i})$ 仍是上三角矩阵，其元素由 $f$ 在 $\lambda_{i}$ 处的各阶导数给出
    $$f(\bm J_{i})=\begin{bmatrix}f(\lambda_{i})&\frac{1}{1!}f'(\lambda_{i})&\cdots&\frac{1}{(m_{i}-1)!}f^{(m_{i}-1)}(\lambda_{i})\\&f(\lambda_{i})&\ddots&\vdots\\&&\ddots&\frac{1}{1!}f'(\lambda_{i})\\&&&f(\lambda_{i})\end{bmatrix}$$
- 特例：对 $\bm J_{i}=\begin{bmatrix}\lambda&1\\0&\lambda\end{bmatrix}$，有
    $$\mathrm e^{t\bm J_{i}}=\mathrm e^{\lambda t}\begin{bmatrix}1&t\\0&1\end{bmatrix}\qquad \sin(t\bm J_{i})=\begin{bmatrix}\sin\lambda t&t\cos\lambda t\\0&\sin\lambda t\end{bmatrix}$$
- 例：$\bm A=\begin{bmatrix}4&6&0\\-3&-5&0\\-3&-6&1\end{bmatrix}$，$\varphi(\lambda)=(\lambda+2)(\lambda-1)^{2}$，$\lambda=1$ 有两个线性无关的特征向量，故 $\bm A$ 可对角化
    $$\bm P=\begin{bmatrix}-1&-2&0\\1&1&0\\1&0&1\end{bmatrix}\qquad \bm J=\mathrm{diag}(-2,1,1)$$
    于是
    $$\mathrm e^{t\bm A}=\bm P\,\mathrm{diag}\left(\mathrm e^{-2t},\mathrm e^{t},\mathrm e^{t}\right)\bm P^{-1}$$

### 矩阵函数的另一定义
- 定义3.8：设 $\bm A$ 的 Jordan 标准形 $\bm P^{-1}\bm A\bm P=\mathrm{diag}(\bm J_{1},\cdots,\bm J_{s})$，其中 $\bm J_{i}$ 为 $m_{i}$ 阶、特征值为 $\lambda_{i}$ 的 Jordan 块，若 $f(z)$ 在 $\lambda_{i}$ 处具有直到 $m_{i}-1$ 阶的导数（$i=1,2,\cdots,s$），令
    $$f(\bm A)=\bm P\,\mathrm{diag}\left(f(\bm J_{1}),\cdots,f(\bm J_{s})\right)\bm P^{-1}$$
    其中 $f(\bm J_{i})$ 为 $f$ 及其各阶导数在 $\lambda_{i}$ 处构成的上三角矩阵，则称 $f(\bm A)$ 为对应于 $f(z)$ 的**矩阵函数**
- 定义3.8 只要求 $f$ 在谱上有足够高阶的导数，比定义3.7 更一般，而定义3.7 适用时两者一致，因为 $f(\bm A)$ 只依赖 $f$ 及其导数在谱上的值
- 例：$f(z)=\frac{1}{z}$，$\bm A$ 是四阶 Jordan 块
    $$\bm A=\begin{bmatrix}2&1&0&0\\0&2&1&0\\0&0&2&1\\0&0&0&2\end{bmatrix}$$
    由 $f^{(l)}(2)=(-1)^{l}l!/2^{l+1}$ 得
    $$f(\bm A)=\bm A^{-1}=\begin{bmatrix}\frac{1}{2}&-\frac{1}{4}&\frac{1}{8}&-\frac{1}{16}\\0&\frac{1}{2}&-\frac{1}{4}&\frac{1}{8}\\0&0&\frac{1}{2}&-\frac{1}{4}\\0&0&0&\frac{1}{2}\end{bmatrix}$$
- 例：$f(z)=\sqrt z$，$\bm A=\begin{bmatrix}1&1&0\\0&1&0\\0&0&2\end{bmatrix}$，则 $\bm J_{1}=\begin{bmatrix}1&1\\0&1\end{bmatrix}$，$\bm J_{2}=2$，由 $f'(1)=\frac{1}{2}$ 得
    $$f(\bm J_{1})=\begin{bmatrix}1&\frac{1}{2}\\0&1\end{bmatrix}\qquad f(\bm J_{2})=\sqrt2$$
    故
    $$f(\bm A)=\begin{bmatrix}1&\frac{1}{2}&0\\0&1&0\\0&0&\sqrt2\end{bmatrix}$$
