## 基于智谱AI GLM-4模型的支持并发、多语言、滑动窗口的知识图谱生成工具

## Showcase

以下是使用该工具在`--input test.pdf --split --update --window 3 -p 20`条件下生成的图谱
![非常复杂的图谱](https://github.com/Helio609/zhipuai_kg_generator/blob/main/knowledge_graph.png)

## Usage
```bash
usage: main.py [-h] [-i INPUT] [-o OUTPUT] [-s] [-w WINDOW] [-m MODEL] [-p PARALLEL] [-l LANGUAGE] [-u]

options:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Input file path, support pure text file and pdf
  -o OUTPUT, --output OUTPUT
                        Output graphviz file name
  -s, --split           Split content, default to true
  -w WINDOW, --window WINDOW
                        A sliding window to control the number of sentences to be processed at a time
  -m MODEL, --model MODEL
                        The model used to generate the KG
  -p PARALLEL, --parallel PARALLEL
                        The max worker in thread pool
  -l LANGUAGE, --language LANGUAGE
  -u, --update          Render in real time when nodes or edges changed
```

- `-i, --input`: 输入文件路径，支持纯文本文件和PDF。（必需）
- `-o, --output`: 输出的Graphviz文件名，默认为"knowledge_graph"。
- `-s, --split`: 是否分割内容，默认为真。
- `-w, --window`: 控制每次处理的句子数量的滑动窗口，类型为整数，默认为0。
- `-m, --model`: 用于生成知识图谱的模型，默认为"glm-4"。
- `-p, --parallel`: 线程池中的最大工作线程数，类型为整数，默认为1。
- `-l, --language`: 使用的语言，默认为"中文"。
- `-u, --update`: 当节点或边变化时实时渲染。
