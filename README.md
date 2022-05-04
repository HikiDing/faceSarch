# 用来排解无聊的晚上
# ROBOMASTER 中维动力战队杀人神奇
# 用于直面天灵盖的神奇代码


使用google的mediapipe，进行脸部处理，然后获取天灵盖^
想用就自己装库吧
基于ROS1，构建代码。

facesearch中接收图片节点为：/send_pic
            发布串口消息为：/uart_send
            主要发布3个参数：yaw，pitch，distance
可以添加接收串口部分