import numpy as np
import matplotlib.pyplot as plt

# ---------- 数据 ----------
# 1. 修改了 x 的范围为 -3.14 到 3.14
x = np.linspace(-3.14, 3.14, 20000)
x = x[x != 0]

y1 = x**2 * np.sin(1 / x)
y2 = 2 * x * np.sin(1 / x) - np.cos(1 / x)

# ---------- 深色主题 ----------
plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(10, 6), facecolor='#1e1e1e')
ax.set_facecolor('#1e1e1e')

# ---------- 曲线（用普通文本作为图例）----------
ax.plot(x, y2, color='#4fc3f7', linewidth=1.5,
        label='y2 = 2x·sin(1/x) - cos(1/x)')
ax.plot(x, y1, color='#ff9800', linewidth=1.5,
        label='y1 = x²·sin(1/x)')

# ---------- 图例设置 ----------
ax.legend(loc='upper right', facecolor='#2e2e2e', edgecolor='#888',
          labelcolor='#eee', fontsize=12)

# ---------- 坐标轴穿过原点 ----------
ax.spines['left'].set_position('zero')
ax.spines['bottom'].set_position('zero')
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.spines['left'].set_color('#888')
ax.spines['bottom'].set_color('#888')

# ---------- 刻度与范围限制 ----------
ax.tick_params(colors='#bbb', labelsize=11)

# 2. 限制 X 轴范围为 -3.14 到 3.14
ax.set_xlim(-3.14, 3.14)

# 3. 限制 Y 轴范围为 -2 到 2，并固定刻度
ax.set_ylim(-2, 2)
ax.set_yticks([-2,  0,  2])

# ---------- 轴标签（普通斜体文本）----------
ax.text(1.02, 0.5, 'x', transform=ax.transAxes,
        fontsize=20, color='#eee', ha='left', va='center', fontstyle='italic')
ax.text(0.5, 1.02, 'y', transform=ax.transAxes,
        fontsize=20, color='#eee', ha='center', va='bottom', fontstyle='italic')

plt.tight_layout()

# ---------- 保存 / 显示 ----------
plt.savefig('plot_oscillation.svg', facecolor='#1e1e1e', bbox_inches='tight')
plt.show()
