# 使用官方的Python基础镜像
FROM python:3.11-slim-buster

# 设置工作目录
WORKDIR /app

# 将当前目录的内容复制到工作目录中
ADD . /app

# 安装项目需要的库
RUN pip install flet
RUN pip install openai

# 设置端口
EXPOSE ${PORT}, 7860

# 运行app.py当容器启动时
CMD ["python", "main.py"]