# 待完成
1. 去掉外部资源使用, 角色使用一个大蓝方块表示, 陷阱采用小蓝方块表示, 敌人使用红色方块表示
2. 使用fps控制帧率
3. 修正bug: 寻路方向的问题: 可能是player本体的实际位置和第一个寻路位置存在差距
4. 总结寻路是怎么实现的, 总结到OneNote上面

#  笔记
NOTE: 如果直接用self.old_rect = self.rect python实际上是让old_rect 和 rect指向同一个rect, 所以需要使用方法self.old_rect = self.rect.copy()
[] 不等于 0, 空列表不等于0

draw方法只有在group里面才有吗
# 程序构思

