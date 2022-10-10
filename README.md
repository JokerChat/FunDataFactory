![png](https://img.shields.io/badge/Python-3.9-green)
![png](https://img.shields.io/badge/vue-2.0-green)
![png](https://img.shields.io/badge/FastApi-green)

### 🎉 技术栈

- [x] 🎨 FastApi(毛坯房中的毛坯房，异步web框架)
- [x] 🎶 SQLAlchemy(你可以看到很多sqlalchemy同步的用法) 
- [x] 🏐 Gunicorn(内含uvicorn，部署服务)
- [x] 🎲 Nginx(反向代理)

### 🏅️ 特约赞助商
[ 😁 pity项目，快点我](https://github.com/wuranxu/pity)（ **说明:** 本项目一部分代码借鉴`pity`项目，当然README介绍文档也是😅希望无敌哥看到之后不会`打我`向pity项目Respect😉）

### ⚽ 前端地址

[😈 快点我](https://github.com/JokerChat/FunDataFactoryWeb)
![](http://static.fangfun.xyz/picture/WX20221007-105728%402x.png)


## ☕ 说明

这是一个内部落地大半年的数据工厂，作为子公司测试团队落地的第一个测试平台，且内部反馈较好~具备完整`开发手册`虽然手册讲得不是很好，但是我觉得可以从中学到`测试平台的思路`

废话少讲，快D过黎体验吧！靓仔靓女们~

 为什么会有数据工厂的概念？这里引用柴佬的话语
> 为什么会有数据工厂的概念？大家可以类比一下数据仓库，本身不做产出，只做收集，你可以认为接口测试平台里面的场景链路就是数据工厂里面的一个卡片事务，但这是职责方向不同，数据工厂面向的是数据产出，只需要单个或者少量入参就封装好了大量的写事务，接口平台你需要手动录入，串联上下文 context，或者流量录制，总之你要自己去编写链路，数据工厂本身是一个调用方（理解什么是工厂），本质上它是做一个调度，管理，执行的地方。好比如果你要赋能其他业务线或者开发线，你去要开发新增一个优惠券去自测一下，开发说太麻烦了，链路很长，你这个时候封装一个事务卡片在工厂里，给开发自己去点击这个卡片，他肯定也会乐意，如果是接口自动化平台，难不成你丢给他这么大个平台，说你去找一下我这个场景链路（他压根不想看），所以，工厂的后续优化方向，肯定是怎么更好的去让其他业务线使用，不要看到底层链路细节，只管造数用来测试即可

[在线体验 😎](http://www.fangfun.xyz/)

<details open="open">
<summary>🌙 已有功能</summary>

| 功能点            | 状态  |
|:---------------|:----|
| 脚本项目与平台服务解耦  🔥  | ✅  |
| 在线展示测试脚本 🔥      | ✅   |
| 美观的数据报表 🔥       | ✅   |
| http、rpc、get调用 🔥         | ✅   |
| git webhooks同步项目🤤           | ✅   |

</details>

<details>
<summary>平台预览</summary>

#### 🍦 数据报表

![image-20221007112933614](http://static.fangfun.xyz//picture/202210071129659.png)

#### 场景列表

![image-20221007113206729](http://static.fangfun.xyz//picture/202210071132768.png)

#### 运行日志

![image-20221007113225969](http://static.fangfun.xyz//picture/202210071132010.png)

#### 用户管理

![image-20221007113242061](http://static.fangfun.xyz//picture/202210071132097.png)

#### 项目管理

![image-20221007113253424](http://static.fangfun.xyz//picture/202210071132459.png)

</details>

## ✉ 相关文档

[介绍文档](https://www.yuque.com/joker-bo9zn/hp2cg3/aaxdlk)

[使用文档](https://www.yuque.com/joker-bo9zn/hp2cg3/ultb8c)

[部署文档](https://www.yuque.com/joker-bo9zn/hp2cg3/metxph)

## 😊 开发参考文章

[开发文档-公众号](https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzI2MjU0Mzg4MA==&action=getalbum&album_id=2379389965001687041)

[开发文档-掘金](https://juejin.cn/column/7102023541570142216)

[开发文档-语雀](https://www.yuque.com/joker-bo9zn/hp2cg3)

### 😢 关于FunLine数据工厂

FunLine前身：公司以前的内部造数平台（fastapi）将造数脚本进行api化，然后用fastapi自带的swagger文档进行请求，没有web页面，不太方便，加上写造数脚本相当于写成了一个接口，对于不太熟悉fastapi的同学debug起来及其困难···

使用`Python`+`FastApi`+`Vue`开发，将平台与造数脚本进行解耦，采用apidoc生成脚本入参出参数据，生成web界面，动态导包作为核心执行方法~

FunLine的宗旨：专注于测试脚本的测试工具，用于业务测试提效···

FunLine命名缘由：fun有趣的意思，line流水线般造数据，结合起来就如某土康的流水线一样，想造什么就造什么FunLine~

### 服务器部署
我们只需要在服务器上`git clone`，下载项目并以项目中的dockerfile文件构建镜像
1. 新建server目录
```shell
mkdir /server
cd /server
# 用来目录挂载
mkdir logs
# 用来目录挂载
mkdir keys
```
**备注:** keys目录上传刚才本地创建的公钥和私钥，这里我用的是`FinalShell`软件进行上传，如果不需要ssh拉取git项目，可以忽略创建keys目录


2. 在server目录git clone项目
```shell
cd /server
git clone https://github.com/JokerChat/FunDataFactory.git 
git clone git clone https://github.com/JokerChat/FunDataFactory.git
```
3. 分别执行构建镜像
```shell
cd /server/FunDataFactory
docker build -t fun:v1 .
cd /server/FunDataFactoryWeb
docker build -t fun_web:v1 .
```
4. 创建并启动容器
```shell
# 后端服务启动
# 如果不需要ssh拉取git项目，可以忽略挂载keys目录
docker run -itd -p 8080:8080 -v /server/logs:/fun/logs -v /server/keys:/fun/app/commons/settings/keys fun:v1

# 前端服务启动
docker run -itd -p 80:80 fun_web:v1
```
**备注:** 记得开放相关的端口，前端的`.env.production`目录记得更换对应的后端api端口

![img](http://static.fangfun.xyz//picture/202210071311540.png)

启动成功后，浏览器访问`http://119.91.144.214`，`119.91.144.214`为服务器的ip地址

5. Nginx转发代理(非必须)

如果已经申请了域名，可以给机器配上个域名，这样子就不用每次直接`ip+端口`访问，方便很多，如果没有申请域名，可忽略第5步···
```
worker_processes  1;
events {
    worker_connections  1024;
}

http {
    include       mime.types;
    default_type  application/octet-stream;
    sendfile        on;
    keepalive_timeout  65;
    server {
        listen       80;
        server_name  fangfun.xyz;
        location / {
          proxy_set_header   X-Real-IP $remote_addr;
        	proxy_set_header   Host      $http_host;
        	proxy_pass         http://0.0.0.0:81;
        }
        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   html;
        }
    }
	server {  
    		listen 80;
    		server_name api.fangfun.xyz;
    		location / {
        		proxy_set_header   X-Real-IP $remote_addr;
        		proxy_set_header   Host      $http_host;
        		proxy_pass         http://0.0.0.0:8080;
    }
}
}
```
这里的`fangfun.xyz`直接映射到了本地的`81`端口即为前端服务，
`api.fangfun.xyz`为二级域名，直接映射到了本地的`8080`端口即为后端服务

**备注:**前端镜像启动时，映射宿主机的端口为`81`

```shell
# 前端服务启动
docker run -itd -p 81:80 fun_web:v1
```

6. 配置rancher流水线(非必须)

可自己搭建个rancher玩玩，配合rancher流水线进行自动化部署项目···有兴趣的小伙伴可找我交流交流，互相学习一波

![img](http://static.fangfun.xyz//picture/202210071311455.png)

### 📞 作者介绍

    大家好，我是笋货，一个乐于分享、热爱生活，喜欢捣鼓各类测试工具的点点点工程师，目前就职于广州某传统行业公司。
    
    一个爱玩、爱学习、各类运动样样都‘精通’的韭5后。
    
    个人技术公众号: `笋货测试笔记`，欢迎大家关注我，掌握最新测试知识。

![](http://static.fangfun.xyz//picture/202210071152661.png)

### ❤️ 平台初心

因为自己本身就是一名业务测试，深感业务测试的痛点···一直思考🤔如何进行测试提效？接口自动化？接口测试平台？jmeter脚本？数据工厂？我选择了后者，后来公司内部也落地了，证明当初的想法是对的···为什么要开源呢？因为自己乐于分享，乐于交流，乐于学习，在开源的同时，相当于把之前的东西重新写了一遍，温故而知新！！！首先，在这里最感谢的一个人就是无敌哥！！！数据工厂的一些思路都是他给我指路，亿分感谢！另一个人当然就是溜达哥啦，fastapi有什么不懂的，我都请教他，每次溜达哥都能提供出解决思路，万分感谢！最后要感谢的是leader-小凤姐，提供`舞台`让我`show time`感谢一路陪我走过来的各位，衷心感谢！！！

人啊，总得不断学习，不断进步，路漫漫其修远兮···

我相信FunLine可以给你们带来测试效率上的提升！！！项目里面的代码虽谈不上优雅，但可以给你学习`fastapi`带来一定的借鉴作用。

### 💪 落地效果

数据工厂在公司内部已经落地了大半年，稳定运行，平台上的测试脚本提供于开发、产品、测试使用，大大提高测试效率···

### 😊 已有功能

+ [x] 🔥 git webhook 同步项目
- [x] 🀄 在线展示测试脚本
* [x] 🚴 丰富的调用方式（http、rpc、get调用）
- [x] 💎 美观的数据报表

## 🙋 待开发的功能

- [ ] 🤡 在线包管理

* [ ] 🐭 结合接口自动化执行脚本

- [ ] 🌽 等等等等

### 赞助

如果您觉得这个项目对你`有所帮助`，可以请我吃包魔法士哦~或者帮忙点个star，让我创作更有动力！！！谢谢大家啦！

![image-20221007132527912](http://static.fangfun.xyz//picture/202210071325959.png)

### 🏅️ 官方合作赞助商（排名不分先后）
- 无敌哥
- 老虎哥
- 晴天
- 迷龙
- 大月亮的小伙伴

## 🎨 微信交流群
这里我建了一个微信交流群，有兴趣的小伙伴们可以加我个人微信: `JIE664616581`，我拉你到群聊或者扫码进群学习交流~

![image-20221010144240622](http://static.fangfun.xyz//picture/202210101442452.png)