### 作业发布、提交和下载

此项目是我自己开发用于班级作业提交，看见想用就可以拿去用。

数据库的连接在config.py文件里，记得修改。设计了四张表：students、teachers、jobs、cursors。

stu表存放的是学生的信息：学号姓名班级。tea表存放的是老师的信息：账号密码还有交的课……。

jobs表是创建的作业记录。cursors表存放的是学生的提交记录。

**因为个人目前不会前端，所以整个项目看起来很丑陋但是功能还是比较齐全**

因为用的flask框架，上传文件时要保存文件名中的中文的话，还得修改main/views.py中的129行的secure_filename()[方法](https://blog.csdn.net/qq_30490489/article/details/92000197?depth_1-utm_source=distribute.pc_relevant.none-task-blog-BlogCommendFromBaidu-2&utm_source=distribute.pc_relevant.none-task-blog-BlogCommendFromBaidu-2)



