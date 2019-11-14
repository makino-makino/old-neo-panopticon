# neo-panopticon
すべてのユーザが監視し合うことによって生み出される、とっても平和なSNS

## 起動
以下のコマンドの実行で、起動ができる。


### 初回

```sh
$ git clone https://github.com/akakou/neo-panopticon
$ cd neo-panopticon
$ sudo docker-compose up -d --build
$
$ # しばらく時間をおいて
$ sudo docker-compose run api rails db:create && rails db:migrate RAILS_ENV=development
```

### 2回目以降

```sh
$ git clone https://github.com/akakou/neo-panopticon
$ cd neo-panopticon
$ sudo docker-compose up 
```

App（Nuxt.js）: http://localhost:3001  
API（Ruby on Rails）: http://localhost:3000 
