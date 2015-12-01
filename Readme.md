## 使用说明

`git clone` 或者点击 *Download ZIP* 以下载本仓库。

Sample AI 可以在以下地址下载： <https://gist.github.com/abcdabcd987/d6d284227f5c5953c857>

Linux / OS X 用户可以直接使用下面命令运行：

```
$ g++ -std=c++11 -O2 -Wall sample_ai.cc -o sample_ai
$ ./main.py ./sample_ai ./sample_ai
```

Windows 用户请下载 Python 3 之后，用 `cmd` 打开，使用类似的方式运行。

本地评测结束后，在终端中会显示比赛结果以及中间的过程，这个结果在 `result.json` 中也保存了一份。另外，当前目录下会产生 `ai?_std???.log` 代表每个 AI 的 `stdin / stdout / stderr` 记录。

#Have Fun!
