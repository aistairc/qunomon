# 削除

本章では、登録したMLComponents, Inventories, TestDescriptionsの各項目の削除手順について解説します。

## TestDescriptionsの削除

TestDescriptions一覧画面から削除対象の「delete」列に表示されたごみ箱アイコンを押下すると、削除できます。

![0101](01/01.png)

## Inventoriesの削除

Inventories一覧画面から削除対象の「delete」列に表示されたごみ箱アイコンを押下すると、削除できます。

![0201](02/01.png)

## MLComponentsの削除

MLComponents一覧画面から削除対象の「delete」列に表示されたごみ箱アイコンを押下すると、削除できます。

削除対象のMLComponent内にTestDescriptionやInventoryが存在すると削除できません。予め関連付けられたTestDescriptionやInventoryを削除したうえで再実行ください。

![0301](03/01.png)

## ガイドラインの削除

Guidelines一覧画面から削除対象の「delete」列に表示されたごみ箱アイコンを押下すると、削除できます。

![0401](04/01.png)

## AITのアンインストール

インストール済みAITリスト画面から「AIT Uninstall」ボタンを押下すると当該AITをアンインストールできます。

評価の再実行性や証跡の管理のため、当該AITが関連付けられたTestDescriptionが一つでもあればアンインストールを実行できません。（TD Using Status列にて、TD unusedとなっていれば削除可能といえます。）

本当に不要な場合は、当該AITを使用するすべてのTestDescriptionを削除した後に、アンインストール操作を再実行ください。

![0501](05/01.png)
