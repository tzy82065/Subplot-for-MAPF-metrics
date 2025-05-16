import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl

mpl.rcParams['font.family'] = 'serif'
mpl.rcParams['font.serif'] = ['Times new roman']
mpl.rcParams['font.weight'] = 'bold'
plt.rcParams['mathtext.default'] = 'regular'

# 地图名称列表
map_names = ['empty-32-32', 'random-32-32-20', 'room-64-64-8',
             'warehouse-10-20-10-2-2', 'den520d']

# 创建子图并调整位置
fig, axs = plt.subplots(3, 5, figsize=(20, 10))
plt.subplots_adjust(top=0.85, bottom=0.12, left=0.08, right=0.98,
                    wspace=0.25, hspace=0.35)

# 读取数据
df_cbs = pd.read_csv('success_rate/cbs.csv', index_col=0)
df_pibt = pd.read_csv('success_rate/pibt.csv', index_col=0)

for col, map_name in enumerate(map_names):
    # 成功率图
    agent_nums = [int(x) for x in df_pibt.columns]
    show_ticks = agent_nums[1::2]

    cbs_data = df_cbs.loc[map_name]
    pibt_data = df_pibt.loc[map_name]

    l1 = axs[0, col].plot(agent_nums, cbs_data.values, marker='o',
                          color='sandybrown', linewidth=3, markersize=5)
    l2 = axs[0, col].plot(agent_nums, pibt_data.values, marker='o',
                          color='cornflowerblue', linewidth=3, markersize=5)
    # 设置成功率图的y轴范围
    axs[0, col].set_ylim(-0.05, 1.05)
    axs[0, col].set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])

    # SOC gap图
    df_soc = pd.read_csv(f'soc/{map_name}_cost_ratios.csv', index_col=0)
    for col_name in df_soc.columns:
        axs[1, col].scatter([int(col_name)] * len(df_soc[col_name].dropna()),
                            df_soc[col_name].dropna(),
                            alpha=0.3, color='lightcoral', s=18)
    means = df_soc.mean()
    l3 = axs[1, col].plot(means.index.astype(int), means.values,
                          color='firebrick', linewidth=3)
    # 设置SOC图的y轴范围
    axs[1, col].set_ylim(0.95, 1.6)

    # Makespan gap图
    df_makespan = pd.read_csv(f'makespan/{map_name}_makespan_ratios.csv', index_col=0)
    for col_name in df_makespan.columns:
        axs[2, col].scatter([int(col_name)] * len(df_makespan[col_name].dropna()),
                            df_makespan[col_name].dropna(),
                            alpha=0.3, color='limegreen', s=18)
    means = df_makespan.mean()
    l4 = axs[2, col].plot(means.index.astype(int), means.values,
                          color='forestgreen', linewidth=3)
    # 设置Makespan图的y轴范围
    axs[2, col].set_ylim(0.95, 1.6)

    for col, map_name in enumerate(map_names):
        # 设置每列的标题（移到循环开始处）
        map_labels = {
            'empty-32-32': 'empty-32-32',
            'random-32-32-20': 'random-32-32-20',
            'room-64-64-8': 'room-64-64-8',
            'warehouse-10-20-10-2-2': 'warehouse-10-20-10-2-2',
            'den520d': 'den520d'
        }
        # 将set_xlabel改为set_title，应用到第一行的子图上
        axs[0, col].set_title(map_labels[map_name], size=20, family='Times New Roman', pad=12)
    '''
    # 设置每列的标题
    map_labels = {
        'empty-32-32': 'empty-32-32',
        'random-32-32-20': 'random-32-32-20',
        'room-64-64-8': 'room-64-64-8',
        'warehouse-10-20-10-2-2': 'warehouse-10-20-10-2-2',
        'den520d': 'den520d'
    }
    # axs[2, col].set_xlabel(map_labels[map_name], size=20, family='Times New Roman', labelpad=12)
    '''

    # 设置每行的格式
    for row in range(3):
        axs[row, col].tick_params(labelsize=16)
        axs[row, col].spines['top'].set_linewidth(2)
        axs[row, col].spines['right'].set_linewidth(2)
        axs[row, col].spines['bottom'].set_linewidth(2)
        axs[row, col].spines['left'].set_linewidth(2)
        axs[row, col].set_xlim(0, 105)
        axs[row, col].set_xticks(show_ticks)

        # 只给最左边的子图添加y轴标签
        if col == 0:
            if row == 0:
                axs[row, col].set_ylabel('Success Rate', size=20)
            elif row == 1:
                axs[row, col].set_ylabel('Sum of Cost/LB', size=20)
            else:
                axs[row, col].set_ylabel('Makespan/LB', size=20)

# 添加总图例
fig.legend([l1[0], l2[0], l3[0], l4[0]],
           ['CBS$_{T}$', 'PIBT$_{T}$', 'Average SOC/LB', 'Average Makespan/LB'],
           loc='upper center', bbox_to_anchor=(0.5, 0.95),
           ncol=4, fontsize=20, frameon=False)

fig.text(0.5, 0.02, 'Number of agents: |A|', ha='center', va='center',
         family='Times New Roman', size=20)


plt.show()