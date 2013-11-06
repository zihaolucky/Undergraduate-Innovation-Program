crawler_zhihu
=====================

这是一个基于Scrapy的用于抓取知乎帖子内容的工具。

该工具主要是抓取单一问题页面内的发帖人、回帖人以及其二级评论人的ID，并将结果保存在 `record.txt` 中。后者可以导入 `gephi` 并生成网络图。

我们可以用Social Network Analysis的方法去研究和评价该帖子所形成的网络结构，这个结构（链接）主要是通过SNS用户间的“评论”产生的。如此一来，我们便可以做一些基础性的研究，包括节点的中心度、网络中的社团以及节点可达性等。

                                                                                        2013-11-6


Released Note:
1. `network#1` 是由第一版的crawler抓取所得的效果。

2. `network#2` 是由第二版的crawler抓取相同页面得到的结果。注意到这两幅图的上色方式是不同的。后者是按相同的modularity进行着色。

![zhihu](https://f.cloud.github.com/assets/4514568/1464359/ae45f7f4-4545-11e3-8390-dc96f1b8fe4f.png)
