# Jordan标准形两种求法的关系
---

对于一个矩阵 $\bm A$，其特征多项式可以写成：

$$
\det(\lambda\bm I-\bm A) = \prod_{i=1}^{s}(\lambda-\lambda_{i})^{m_{i}},\qquad\sum_{i}^{s}m_{i} = n
$$

按照从小到大的顺序排列其实就是 Smith 标准形的写法：

$$
\varphi(\lambda) = 
(\lambda-\lambda_{1})(\lambda-\lambda_{1})\cdots
(\lambda-\lambda_{s})(\lambda-\lambda_{s})\cdots(\lambda-\lambda_{s})
$$

回到因式分解，我们展开每一个 $\lambda_{i}$ 对应的**核链**，首先有：

$$
\forall \bm v
((\lambda_{i}\bm I-\bm A)^{k}\bm v = 0)
\implies
((\lambda_{i}\bm I-\bm A)^{k+1}\bm v = 0)
$$

另一方面：

$$
\exists \bm w
((\lambda_{i}\bm I-\bm A)^{k+1}\bm w = 0)
\implies
((\lambda_{i}\bm I-\bm A)^{k}\bm w = 0)
$$

因此

$$
\ker(\lambda_{i}\bm I-\bm A)^{k}\subset\ker(\lambda_{i}\bm I-\bm A)^{k+1}
$$

注意，同一特征值的所有 Jordan 块的阶数和就是这个特征值的代数重数！

## 核链求解
首先：
$$
m_{i}=r_{i1}+r_{i2}+\cdots+r_{is_{i}},
$$

其中 $r_{ij}$ 是各个 Jordan 块的大小。单个 Jordan 块的大小一般小于或等于 $m_{i}$。

---

特征多项式因式分解为

$$
\chi_{A}(x)=\prod_{i} (x-\lambda_{i})^{m_{i}}.
$$

由互素分解得到根子空间直和：

$$
V=\bigoplus_{i} V_{i},\qquad 
V_{i}=\ker\big((A-\lambda_{i} I)^{m_{i}}\big),
$$

并且

$$
\dim V_{i}=m_{i}.
$$

在 $V_{i}$ 上，

$$
A|_{V_{i}}=\lambda_{i} I+N_{i},\qquad 
N_{i}=(A-\lambda_{i} I)|_{V_{i}},
$$

其中 $N_{i}$ 是幂零算子：

$$
N_{i}^{m_{i}}=0.
$$

注意：这里 $N_{i}^{m_{i}}=0$ 只说明幂零指数不超过 $m_{i}$，不说明 $m_{i}$ 就是一个 Jordan 块的阶数。

---

### 下一步：分析幂零算子 $N_{i}$ 的核链

对固定的 $\lambda_{i}$，计算

$$
d_{i,t}=\dim\ker N_{i}^t
=\dim\ker\big((A-\lambda_{i} I)^t\big),
\qquad t=1,2,\dots
$$

直到

$$
d_{i,r_{i}}=m_{i},
$$

其中 $r_{i}$ 是最小的正整数使 $d_{i,r_{i}}=m_{i}$。这个 $r_{i}$ 就是 $\lambda_{i}$ 对应的**最大 Jordan 块的阶数**，也就是 $N_{i}$ 的幂零指数。

然后：

$$
d_{i,1}=\dim\ker(A-\lambda_{i} I)
$$

是 $\lambda_{i}$ 对应的 **Jordan 块个数**，也就是几何重数。

更一般地，阶数至少为 $t$ 的 Jordan 块个数为

$$
b_{i,t}=d_{i,t}-d_{i,t-1},
\qquad d_{i,0}=0.
$$

因此阶数恰好为 $t$ 的 Jordan 块个数为

$$
c_{i,t}=b_{i,t}-b_{i,t+1}
=2d_{i,t}-d_{i,t-1}-d_{i,t+1}.
$$

于是 $\lambda_{i}$ 对应的 Jordan 块结构为：

$$
\underbrace{J_{1}(\lambda_{i})\oplus\cdots\oplus J_{1}(\lambda_{i})}_{c_{i,1}\text{ 个}}
\oplus
\underbrace{J_{2}(\lambda_{i})\oplus\cdots\oplus J_{2}(\lambda_{i})}_{c_{i,2}\text{ 个}}
\oplus\cdots
\oplus
\underbrace{J_{r_{i}}(\lambda_{i})\oplus\cdots\oplus J_{r_{i}}(\lambda_{i})}_{c_{i,r_{i}}\text{ 个}}.
$$

把所有 $\lambda_{i}$ 拼起来，就得到

$$
A\sim
\bigoplus_{i}
\left(
\bigoplus_{t=1}^{r_{i}} J_{t}(\lambda_{i})^{\oplus c_{i,t}}
\right).
$$

这就是 Jordan 标准型。

---

### 关键点

- $m_{i}=\dim V_{i}$ 是 $\lambda_{i}$ 对应所有 Jordan 块的**总大小**；
- $r_{i}$ 才是最大 Jordan 块的阶数；
- 单块阶数由核链维数 $d_{i,t}$ 的增量决定；
- 仅由特征多项式只能知道 $m_{i}$，不能知道块怎么分；必须利用 $A$ 计算核空间维数，或者用最小多项式、$\operatorname{rank}(A-\lambda_{i} I)^t$ 等信息。

例如：

$$
A=\begin{pmatrix}
\lambda&1&0\\
0&\lambda&0\\
0&0&\lambda
\end{pmatrix}
=J_{2}(\lambda)\oplus J_{1}(\lambda).
$$

这里

$$
m=3,\qquad 
d_{1}=\dim\ker(A-\lambda I)=2,\qquad
d_{2}=\dim\ker((A-\lambda I)^2)=3.
$$

所以：

- 块总数 $d_{1}=2$；
- 最大块阶数 $r=2$；
- 阶数恰好 $2$ 的块数：
  $$
  c_{2}=d_{2}-d_{1}=1;
  $$
- 阶数恰好 $1$ 的块数：
  $$
  c_{1}=d_{1}-c_{2}=1.
  $$

因此是 $J_{2}(\lambda)\oplus J_{1}(\lambda)$，而不是一个 $3$ 阶块。

---

要得到 Jordan 标准型，下一步是在每个 $V_{i}$ 上对幂零算子 $N_{i}=A-\lambda_{i} I$ 计算核链维数，从而确定各阶 Jordan 块的个数。

## 和 Smith 标准型的关系

两者本质上是同一件事的两种“读法”：  
- **根子空间 + 核链**：先按特征值把空间拆成局部块，再在每个局部用 $A-\lambda I$ 的幂零核链测出 Jordan 块大小。  
- **Smith 标准型 + 不变因子/初等因子**：直接对 $\lambda$-矩阵 $xI-A$ 做多项式初等变换，一次性读出所有初等因子；每个初等因子 $(x-\lambda)^e$ 就对应一个 $e$ 阶 Jordan 块 $J_{e}(\lambda)$。
- 不变因子不过就是相似矩阵的那个对角线上始终不变的玩意儿，**本质还是矩阵相似**！

---

### 1. Smith 标准型给出的就是块阶数

设
$$
xI-A
$$
的 Smith 标准型为
$$
\operatorname{diag}(1,\dots,1,\Delta_{1}(x),\dots,\Delta_{s}(x)),
$$
其中
$$
\Delta_{1}\mid \Delta_{2}\mid\cdots\mid \Delta_{s}
$$
是不变因子。把每个 $\Delta_{k}$ 分解成不可约幂：
$$
\Delta_{k}(x)=\prod_\lambda (x-\lambda)^{e_{k,\lambda}}.
$$
这些 $(x-\lambda)^{e_{k,\lambda}}$（$e_{k,\lambda}>0$）就是**初等因子**。  
每个初等因子
$$
(x-\lambda)^e
$$
对应一个 Jordan 块
$$
J_{e}(\lambda).
$$
所以 Smith 方法直接告诉你：对每个 $\lambda$，有哪些阶数的 Jordan 块，各多少个。

---

### 2. 固定 $\lambda$：核链维数就是初等因子指数的“统计量”

固定特征值 $\lambda$，令
$$
n_{t}=\dim\ker(A-\lambda I)^t.
$$
在根子空间方法中，你算的就是这个核链。

在 Smith 方法中，令
$$
e_{k}=v_\lambda(\Delta_{k})
$$
表示不变因子 $\Delta_{k}$ 中 $(x-\lambda)$ 的指数。因为
$$
\Delta_{1}\mid\Delta_{2}\mid\cdots\mid\Delta_{s},
$$
所以
$$
e_{1}\le e_{2}\le\cdots\le e_{s}.
$$
这些非零的 $e_{k}$ 正是 $\lambda$ 对应的初等因子指数，也就是 Jordan 块阶数。

两种信息满足公式
$$
n_{t}=\sum_{k}\min(t,e_{k}).
$$
因此
$$
n_{t}-n_{t-1}
=\#\{k:e_{k}\ge t\}
=\text{阶数至少为 }t\text{ 的 Jordan 块个数}.
$$
于是阶数恰好为 $t$ 的块数为
$$
c_{t}=(n_{t}-n_{t-1})-(n_{t+1}-n_{t})
=2n_{t}-n_{t-1}-n_{t+1}.
$$
而 $c_{t}$ 正是初等因子 $(x-\lambda)^t$ 出现的次数。  
所以：

> **根子空间方法中由核链维数算出的 $c_{t}$，就是 Smith 方法中初等因子 $(x-\lambda)^t$ 的重数。**

两者完全一致。

---

### 3. $m_{i}$ 在 Smith 方法里是什么？

特征多项式
$$
\chi_{A}(x)=\det(xI-A)=\prod_{i} (x-\lambda_{i})^{m_{i}}.
$$
在 Smith 标准型中，
$$
\det(xI-A)=\prod_{k} \Delta_{k}(x)
$$
（忽略常数）。因此对固定 $\lambda_{i}$，
$$
m_{i}=v_{\lambda_{i}}(\det(xI-A))
=\sum_{k} e_{k,\lambda_{i}}.
$$
也就是说：

- $m_{i}$ 是 $\lambda_{i}$ 对应的**所有 Jordan 块阶数之和**；
- 单个 Jordan 块的阶数是某个 $e_{k,\lambda_{i}}$；
- 所以 $m_{i}$ 一般不是单个块阶数。

例如
$$
A=J_{2}(\lambda)\oplus J_{1}(\lambda).
$$
特征多项式是
$$
(x-\lambda)^3,
$$
所以 $m=3$。但 Smith 标准型给出
$$
\operatorname{diag}(1,x-\lambda,(x-\lambda)^2),
$$
初等因子是
$$
(x-\lambda),\quad (x-\lambda)^2,
$$
对应两个块：
$$
J_{1}(\lambda),\quad J_{2}(\lambda).
$$
这里 $m=1+2=3$，不是某个块的阶数。

---

### 4. 和根子空间分解的对应

你在根子空间方法中做的是：
$$
V=\bigoplus_{i} V_{i},\qquad 
V_{i}=\ker\big((A-\lambda_{i} I)^{m_{i}}\big).
$$
在模语言下，这相当于把 $K[x]$-模
$$
V\cong K[x]/(\Delta_{1})\oplus\cdots\oplus K[x]/(\Delta_{s})
$$
按不同 $\lambda_{i}$ 用中国剩余定理拆开。  
拆开后，$V_{i}$ 正好汇集了所有含 $(x-\lambda_{i})$ 的初等因子，且
$$
\dim V_{i}=m_{i}=\sum_{k} e_{k,\lambda_{i}}.
$$
然后在每个 $V_{i}$ 上，对幂零算子
$$
N_{i}=(A-\lambda_{i} I)|_{V_{i}}
$$
做循环子空间分解，得到的循环子空间维数就是那些 $e_{k,\lambda_{i}}$，每个给一个 Jordan 块 $J_{e_{k,\lambda_{i}}}(\lambda_{i})$。

所以两条路线是：

$$
\text{根子空间 + 核链}
\quad\Longleftrightarrow\quad
\text{先按 }\lambda\text{ 局部化，再读局部初等因子},
$$
$$
\text{Smith 标准型 + 初等因子}
\quad\Longleftrightarrow\quad
\text{先整体求不变因子，再 CRT 分解成初等因子}.
$$
最后得到的初等因子集合完全相同，因此 Jordan 标准型相同。

---

### 5. 一句话总结

Smith 标准型中的初等因子 $(x-\lambda)^e$ 的指数 $e$，就是根子空间方法中通过核链维数
$$
n_{t}=\dim\ker(A-\lambda I)^t
$$
确定出来的 Jordan 块阶数；初等因子 $(x-\lambda)^e$ 的重数就是阶数为 $e$ 的 Jordan 块个数。  
$m_{i}$ 在两边都只是 $\lambda_{i}$ 对应的所有块阶数之和，即代数重数，不是单个块的阶数。

## Smith 标准形的最后一项

对于 $n$ 阶方阵 $A$，考虑特征矩阵
$$
xI-A
$$
的 Smith 标准型。若其非零不变因子为
$$
d_{1}(x)\mid d_{2}(x)\mid\cdots\mid d_{s}(x),
$$
其中 $d_{s}(x)$ 是**最大的不变因子**（整除链末端），则
$$
\boxed{d_{s}(x)=m_{A}(x)}
$$
即 $d_{s}(x)$ 就是 $A$ 的最小多项式。

同时：
$$
\chi_{A}(x)=\det(xI-A)=\prod_{k=1}^s d_{k}(x)
$$
（忽略常数因子），而最小多项式是最小次数首一多项式使 $m_{A}(A)=0$。

等价地，若把 Smith 标准型写成
$$
\operatorname{diag}(1,\dots,1,d_{1}(x),\dots,d_{s}(x)),
$$
则最后一个对角元 $d_{s}(x)$ 就是最小多项式；前面那些 $1$ 不影响。

例如
$$
A=J_{2}(\lambda)\oplus J_{1}(\lambda).
$$
特征矩阵的 Smith 标准型为
$$
\operatorname{diag}(1,\;x-\lambda,\;(x-\lambda)^2).
$$
最大不变因子是
$$
(x-\lambda)^2,
$$
而 $A$ 的最小多项式确实是 $(x-\lambda)^2$。特征多项式是
$$
(x-\lambda)^3,
$$
等于所有不变因子的乘积。

所以结论是：

$$
\boxed{\text{Smith 标准型中最大的不变因子 }d_{s}(x)\text{ 就是 }A\text{ 的最小多项式。}}
$$

注意这里说的是 $xI-A$ 的 Smith 标准型中**最后一个非零不变因子**，也就是整除链中最大的那个。
