# コンテナ・Kubernetes デモ

<walkthrough-tutorial-duration duration="9999"></walkthrough-tutorial-duration>

<!--
  br タグは読みやすく表示するために利用。
  これがないと、コマンド前後のマージンが微妙でコマンドと文章との対応がわかりにくい。
-->

## デモの流れ

* 事前準備
  * デモ前に環境の構築をしておいてください
* コンテナ デモ
* Kubernetes デモ
* GKE デモ

## 事前準備

<walkthrough-tutorial-duration duration="10"></walkthrough-tutorial-duration>

**必ずデモ前に実施してください。**

### プロジェクトの設定

デモで利用するプロジェクトを設定してください。

<walkthrough-project-setup></walkthrough-project-setup>

gcloud を設定してください。

```sh
gcloud config set project <walkthrough-project-id/>
```

### Terraform 実行

Terraformを実行してください。

```sh
export TF_VAR_project_id="<walkthrough-project-id/>"
cd terraform
terraform init
terraform apply
```

## コンテナ デモ

<walkthrough-tutorial-duration duration="20"></walkthrough-tutorial-duration>

コンテナに関するデモを実施します。

* コンテナ Hello world
* 「コンテナ = プロセス」の確認
* コンテナの隔離の確認
* Dockerfile によるイメージビルド
* Dockerfile によるランタイム アップデート
* イメージをレジストリに Push


## コンテナ Hello world

まずはコンテナを実行してみます。

Docker Hub にある [Hello-world](https://hub.docker.com/_/hello-world)というイメージを使います。

```sh
docker run -ti --rm hello-world
```

## 「コンテナ = プロセス」の確認

今のプロセスを確認します。
Docker Hub にある [Node.js](https://hub.docker.com/_/node)のイメージからコンテナを起動したときのプロセスを見てみます。

まず、コンテナ起動前の `node` プロセスを確認します。

```sh
ps a | grep node | grep -v grep
```
<br>

(別タブで) 次に node コンテナを起動します。

```sh
docker run -ti --rm node
```
<br>

再度ホスト側で `node` プロセスを確認します。

```sh
ps a | grep node | grep -v grep
```
<br>

このように、ホスト側からするとコンテナはただのプロセスであることが確認できます。

node コンテナから `Ctrl-D` で抜けてください。

## コンテナの隔離性の確認

ホスト (Cloud Shell) の OS やプロセスを確認してみます。

ホストのOS:

```sh
lsb_release -a
```
<br>

ホストのプロセス:

```sh
ps -A
```
<br>

CentOS のコンテナを起動します。

```sh
docker run -ti --rm centos
```
<br>

OS とプロセスを確認します。

```sh
cat /etc/centos-release
ps -A
```
<br>

ホストの Cloud Shell とは別の OS が起動していて、プロセスも隔離されていることがわかります。
ファイルシステムが隔離されていることも確認します。**(ホスト側で実行しないように)**

```sh
rm -rf --no-preserve-root /
```
<br>

`Ctrl-D` で抜けると、ホストの Cloud Shell は生きていることが確認できます。

## Dockerfile によるイメージビルド

<walkthrough-editor-open-file filePath="./sample-app/app/main.py">サンプルコードを開く</walkthrough-editor-open-file>

ローカルで実行します。

```sh
cd sample-app
python app/main.py
```
<br>

<walkthrough-editor-open-file filePath="./sample-app/Dockerfile">Dockerfileを開く</walkthrough-editor-open-file>

`Dockerfile` からコンテナイメージをビルドします。

```sh
docker build -t sample .
```
<br>

ビルドしたイメージからコンテナを起動します。

```sh
docker run -ti --rm sample
```
<br>


## Dockerfile によるランタイム アップデート

`main.py` を Python 3.10 向けに修正します。(`is_google_cloud_service`関数のコメントアウト、アンコメント)

Cloud Shell では実行できないことを確認します。(Python 3.9なので)

```sh
python -V
python app/main.py
```
<br>

`Dockerfile` のベースイメージを修正します。

```
FROM python:3.10
```
<br>

イメージをビルドします。

```sh
docker build -t sample:v2 .
```
<br>

コンテナを実行します。

```sh
docker run -ti --rm sample:v2
```

## イメージをレジストリに Push

コンテナイメージをレジストリにPushします。

```sh
docker tag sample:v2 gcr.io/<walkthrough-project-id/>/sample:v2
docker push gcr.io/<walkthrough-project-id/>/sample:v2
```
<br>

レジストリのイメージを指定してコンテナを起動します。

```sh
docker run -ti --rm gcr.io/<walkthrough-project-id/>/sample:v2
```
<br>


## Kubernetes デモ

* kubectl 紹介
* Deployment
* Service
* セルフヒーリング
* ローリング アップデート

## kubectl 紹介

Kubernetes には kubectl という CLI ツールがあります。

今回はGKEのKubernetesを使うので、gcloud コマンドで認証します。

```sh
gcloud container clusters get-credentials demo-cluster --region asia-northeast1
```
<br>

例えば、現在の Kubernetes ノード一覧を取得できます。

```sh
kubectl get nodes
```
<br>

## Deployment の宣言

このセクションでは Deployment を宣言して Pod が作成される様子を確認します。

作業前にDeploymentが存在しないことを確認します。

```sh
kubectl get deployment
```
<br>

また、Podが存在しないことを確認します。

```sh
kubectl get pods
```
<br>

<walkthrough-editor-open-file filePath="./container-demo/deployment.yaml">Deploymentを開く</walkthrough-editor-open-file>

Kubernetes に Deployment の宣言を適用します。

```sh
cd ..
kubectl apply -f deployment.yaml
```
<br>

Deployment一覧を確認します。

```sh
kubectl get deployments
```
<br>

Pod 一覧を確認します。

```sh
kubectl get pods --watch
```
<br>

## Service の宣言

このセクションでは Service を宣言して、Service により作成されたエンドポイントにアクセスします。

<walkthrough-editor-open-file filePath="./container-demo/service.yaml">serviceを開く</walkthrough-editor-open-file>

Service の宣言を Kubernetes に適用します。

```sh
kubectl apply -f service.yaml
```
<br>

Service が作成される様子を確認します。

```sh
kubectl get services --watch
```

## セルフヒーリング

このセクションでは Pod を手動で削除することで Deployment のセルフヒーリング機能を確認します。

Pod の様子を確認します。

```sh
kubectl get pods --watch
```
<br>

手動で Pod を削除します。

```sh
name=$(kubectl get pods -o jsonpath='{.items[0].metadata.name}')
kubectl delete pod $name
```
<br>

Deployment がすぐに新しい Pod を作り直す様子が確認できます。

## ローリングアップデート

このセクションでは　Deployment のローリングアップデート機能を確認します。

Deploymentの `NAME` 環境変数を書き換えます。

<walkthrough-editor-open-file filePath="./container-demo/deployment.yaml">Deploymentを編集する</walkthrough-editor-open-file>

Pod の様子を確認します。

```sh
kubectl get pods --watch
```
<br>

curl コマンドでレスポンスも確認します。

```sh
ip_address=$(kubectl get service hello -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
while :; do curl -s http://${ip_address}/; sleep 1; done
```
<br>

新しい Deployment の宣言を適用します。

```sh
kubectl apply -f deployment.yaml
```
<br>

1つずつ Pod が新しくなっていく様子が確認できます。

## GKE デモ

## Cloud Run デモ

## Well done!

以上でデモは終了です。

<walkthrough-conclusion-trophy/>