## 选择多进程的原因：

虽然由于爬虫属于IO密集型计算是使用多线程比较好，但是：

（1）由于 Python 中 GIL 的原因, 对于计算密集型任务, Python 下比较好的方式是使用多进程, 这样可以非常有效的使用 		 CPU 资源。当然同一时间执行的进程数量取决于你电脑的 CPU 核心数.。

（2）python 中的多线程其实并不是真正的多线程，并不能做到充分利用多核 CPU 资源。因此选择多进程进行爬虫。

##### （3）重点：由爬取不同的url产生的任务序列可以使用多进程的方式充分提高爬取速度。

（4）在python环境下，多进程稍稍比多线程好实现好理解一点。

## 

## 任务分配问题（多进程核心原理）

多进程爬虫的任务分配，和多线程一样，通过队列进行分配，先在主进程中将任务push到队列中，多进程启动后，每个进程都尝试从队列里获取任务，这里的任务，在实际应用中可能就是一个需要爬取的url

## 参考资料

[用代理池分布式爬取B站所有用户信息 - 知乎](https://zhuanlan.zhihu.com/p/46289663)

[b站(bilibili)注册用户数量总共有多少?如何通过uid搜索用户名? - 尺码通](https://www.chimatong.com/bzwj/202012/16-26977.html)

[利用Python爬取B站千万级数据，并对其进行简单的分析 - 哔哩哔哩](https://www.bilibili.com/read/cv1928650/)

[CPU-bound(计算密集型) 和I/O bound(I/O密集型)_轻锋的专栏-CSDN博客](https://blog.csdn.net/q_l_s/article/details/51538039)
