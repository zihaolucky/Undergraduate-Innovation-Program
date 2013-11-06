crawler_zhihu
=====================

这是一个基于Scrapy的用于抓取知乎帖子内容的工具。

该工具主要是抓取单一问题页面内的发帖人、回帖人以及其二级评论人的ID，并将结果保存在 `record.txt` 中。后者可以导入 `gephi` 并生成网络图。

我们可以用Social Network Analysis的方法去研究和评价该帖子所形成的网络结构，这个结构（链接）主要是通过SNS用户间的“评论”产生的。如此一来，我们便可以做一些基础性的研究，包括节点的中心度、网络中的社团以及节点可达性等。

这部分的知识是我们从Coursera的 [Social Network Analysis](https://www.coursera.org/course/sna) 中学习到的，非常感谢MOOC!

                                                                                        2013-11-6


#####Released Note:

  `2011-11-06` 更新了 `zhihu` ，添加了此前漏了的主题节点。

 `2011-11-04` 发布了第一版的 `zhihu`，用于抓取单一页面的内容。
