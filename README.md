# mirai

my qq bot

## Linux配置mirai

- ##### 安装java环境

  ```bash
  sudo apt update
  sudo apt install openjdk-11-jdk
  ```

- ##### 下载Mirai Console Loader

  去github下载<a href='https://github.com/iTXTech/mirai-console-loader/releases'>最新版本的加载器</a>，然后到服务器上解压，我用的版本的是1.0.5。

  ```bash
  wget https://github.com/iTXTech/mirai-console-loader/releases/download/v1.0.5/mcl-1.0.5.zip
  mkdir mcl
  unzip -q mcl-1.0.5.zip -d ./mcl
  chmod -R a+x .
  ```

- ##### 启动

  `./mcl` 会自动下载核心组件，如果出现链接超时报错，多下几次就行了

  运行  `./mcl --update-package net.mamoe:mirai-api-http --channel stable --type plugin` 下载最新版的mirai-api-http插件

  再次执行`./mcl`就会开始自动下载插件

- ##### mirai-api-http配置

  `vim ./config/net.mamoe.mirai-api-http/setting.yml`修改默认的setting，把authKey改了，enableWebsocket设置为true，:wq保存退出

  再次运行.`/mcl`之后可以使用`login qq password` 登录

- ##### 自动登录

  运行`vim ./config/Console/AutoLogin.yml`修改`account`(qq账号)以及`value`(密码)，:wq保存退出

  再次运行`./mcl`即可自动登录

参考自https://angelica.moe/index.php/2021/02/17/linux-install-mirai-robot/