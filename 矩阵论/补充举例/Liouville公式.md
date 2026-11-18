# Liouville's 公式

在矩阵论和微分方程中通常被称为**刘维尔公式（Liouville's formula）**，也称**阿贝尔-雅可比-刘维尔恒等式**。它正是回答“变系数微分方程能否用行列式求解”的关键。

## 📜 恒等式的核心：从矩阵导数到行列式

你提到的“积分矩阵的导数等于系数矩阵乘积分矩阵本身”，即基本矩阵 $\Phi(t)$ 满足：
$$ \Phi'(t) = A(t)\Phi(t) $$

**雅可比公式（Jacobi's formula）** 是证明的基石，它给出了**任意**可微矩阵 $M(t)$ 行列式的导数法则：
$$ \frac{d}{dt}\det M(t) = \operatorname{tr}\left(\operatorname{adj}(M(t)) \cdot M'(t)\right) $$
其中 $\operatorname{adj}(M)$ 是 $M$ 的伴随矩阵。

当 $M(t)$ 可逆时，利用 $M^{-1} = \operatorname{adj}(M)/\det(M)$，公式可化为更简洁的形式：
$$ (\det M)' = \det(M) \cdot \operatorname{tr}(M^{-1}M') $$

## 🔗 推导：连接两者

将 $M(t)$ 替换为基本矩阵 $\Phi(t)$。由于基本矩阵由线性无关的解构成，其行列式恒不为零，因此总是可逆的。代入 $\Phi' = A\Phi$：
$$ (\det \Phi)' = \det(\Phi) \cdot \operatorname{tr}(\Phi^{-1} \cdot A\Phi) = \det(\Phi) \cdot \operatorname{tr}(A) $$

这里用到了迹的循环性质 $\operatorname{tr}(\Phi^{-1}A\Phi) = \operatorname{tr}(A)$。由此得到**刘维尔公式**的微分形式：
$$ \frac{d}{dt}\det\Phi(t) = \operatorname{tr}(A(t)) \cdot \det\Phi(t) $$

## ✅ 最终表达式与适用范围

这是一个关于 $\det\Phi(t)$ 的一阶线性齐次方程，解出即得**积分形式**：
$$ \det\Phi(t) = \det\Phi(t_{0}) \cdot \exp\left( \int_{t_{0}}^{t} \operatorname{tr}(A(s)) \, ds \right) $$

**这个行列式表达式完全适用于变系数微分方程**。它的美妙之处在于，无论系数矩阵 $A(t)$ 如何随 $t$ 变化，基本矩阵的行列式（即朗斯基行列式）的演化**只由系数矩阵的迹 $\operatorname{tr}(A(t))$ 的积分决定**。这为研究解的整体行为（如解的线性相关性、稳定性）提供了一个极其有力的工具，无需解出完整的矩阵 $\Phi(t)$。
