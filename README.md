## Kindledxpush

注：本项目从[blahgeek][1]处fork过来

增加的功能有：日志中记录推送文档中文标题而不是asian

然后就是写了以下关于这个过程的部分细节，详见[wiki][2]

---

在国内，Kindle DX 3G的推送并不是免费的。这里的不是免费指的是：

- 通过发送邮件至`@kindle.com`或者使用`Send To Kindle`浏览器插件，将个人文档自动发送至Kindle，是收费的
- 但是，通过以上两种方式能将文档发送至Amazon管理页面上的`Kindle Library`，在那上面手动点击`Deliver`是可以免费推送的

所以，这个程序的功能就是自动将页面上的文档发送至Kindle，可以使用crontab每十分钟运行一次。

使用前需要新建一个`config.py`，包含以下内容：

    EMAIL = "xxx@gmail.com"  # 你的用户名
    PASSWORD = "xxxxxx"      # 你的密码
    DEVICE = "xxxxxx"        # 你的设备ID
    COUNT = 15               # 一次要检查投递的文档，默认是15（一页），第一次如果有很多要投递，请设大一些或者给直接精确数值

最后一个设备ID，需要在网页上查看。进入`Your Kindle Library`，选择一个文档，点击Action-Deliver，在出现的窗口中审查元素（查看源代码）。

![](./src/push_button.png)

相应选项的value即设备ID. 

![](./src/device_id.png)


[1]: https://github.com/blahgeek/kindledxpush
[2]: https://github.com/lord63/kindledxpush/wiki

