#安装配置

##安装jshint

###安装最新稳定版Node
>- sudo add-apt-repository ppa:chris-lea/node.js
>- sudo update
>- sudo apt-get install nodejs

###安装jshint
>- sudo npm install jshint -g

##安装git_hook

###获取相关代码
>- mkdir ~/bin/
>- cd ~/bin/
>- git clone git@github.com:NanJingBoy/git_code_sniffer_hooks.git

###安装python相关依赖
>- sudo apt-get install python-setuptools
>- sudo easy_install pip
>- sudo pip install -r ~/bin/git_code_sniffer_hooks/requirements.txt

###配置
>- ln -s ~/bin/git_code_sniffer_hooks/pre-commit ~/workspace/test/.git/hooks/ （假设您的项目目录为~/workspace/test）

#说明
>- 执行git commit 时，如果代码格式有误会禁止提交，可将~/bin/git_code_sniffer_hooks/configs/default.cfg中commit节点下的REJECT_COMMIT设置为False以改变其行为
