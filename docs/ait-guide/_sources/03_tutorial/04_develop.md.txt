# Develop

## edit my_ait.ipynb

* edit and run.
* if run success, result output `{AIT_ROOT}\local_qai\mnt\ip\job_result\1\1` and prepare deploy.

### my_ait.ipynb of structure

|#|area name|cell num|description|edit or not|
|---|---|---|---|---|
| 1|flags set|1|setting of launch jupyter or ait flag.|no edit|
| 2|ait-sdk install|1|Use only jupyter launch.<br>find ait-sdk and install.|no edit|
| 3|create requirements and pip install|3|Use only jupyter launch.<br>create requirements.txt.<br>And install by requirements.txt.|should edit(second cell, you set use modules.)|
| 4|import|2|you should write use import modules.<br>but bottom lines do not edit.|should edit(first cell, you import your moduel.)|
| 5|create manifest|1|Use only jupyter launch.<br>create ait.manifest.json.|should edit|
| 6|create input|1|Use only jupyter launch.<br>create ait.input.json.|should edit|
| 7|initialize|1|this cell is initialize for ait progress.|no edit|
| 8|functions|N|you defined measures, resources, downloads in ait.manifesit.json. <br>Define any functions to add these.|should edit|
| 9|main|1|Read the data set or model and calls the function defined in `functions-area`.|should edit|
|10|entrypoint|1|Call the main function.|no edit|
|11|license attribute set|1|Use only notebook launch.<br>Setting attribute for license.|should edit|
|12|prepare deploy|1|Use only notebook launch.<br>Convert to python programs and create dag.py.|no edit|

### #3 area: create requirements and pip install

* This section is for generating the requirements.txt.

* example
    * install for tensoflow 2.3.0
    ```py
        requirements_generator = AITRequirementsGenerator()
        requirements_generator.add_package('tensorflow', '2.3.0')
    ```

* AITRequirementsGenerator specification is [here](https://aistairc.github.io/qunomon/ait-sdk/ait_sdk.common.files.html#module-ait_sdk.common.files.ait_requirements_generator)


``` important:: ait-sdk will be added automatically by AITRequirementsGenerator.
```

### #4 area: import

* You need import packages.

### #5 area: create manifest

* This section is for generating the ait.manifest.json.

* ait.manifest.json holds the design meta-information for AIT.

* example
    * set AIT name
    ```py
        manifest_genenerator = AITManifestGenerator(current_dir)
        manifest_genenerator.set_ait_name('eval_mnist_acc_tf2.3')
    ```

* AITManifestGenerator specification is [here](https://aistairc.github.io/qunomon/ait-sdk/ait_sdk.common.files.html#module-ait_sdk.common.files.ait_manifest_generator)

### #6 area: create input

* This section is for generating the ait.input.json.

* ait.input.json holds the parameters needed to start AIT.

* example
    * set inventory
    ```py
        input_generator = AITInputGenerator(manifest_path)
        input_generator.add_ait_inventories(name='trained_model',
                                            value='trained_model/model_1.h5')
    ```

* AITInputGenerator specification is [here](https://aistairc.github.io/qunomon/ait-sdk/ait_sdk.common.files.html#module-ait_sdk.common.files.ait_input_generator)

* The argument `name` in `add_ait_inventories` and `set_ait_params` is linked to ait.manifest.json.

  * `add_ait_inventories` matches the `ieventories/name` in ait.manifest.json.

  * `set_ait_params` matches the `ieventories/parameters` in ait.manifest.json.

### #8 area: functions

#### output report/measures

* `@log(logger)` is need.

* `@measures(ait_output, 'AUC')` is need. `AUC` will change report/measures in ait.manifest.json.

``` important:: return value set 'AUC' measures at '@measures' automatically. so must return value(s).
```

* example

    ```py
    @log(logger)
    @measures(ait_output, 'AUC')
    def calc_auc(y_test, y_pred, multi_class: str, average: str) -> float:
        y_true = to_categorical(y_test)
        y_score = y_pred

        return roc_auc_score(y_true, y_score,
                            multi_class=multi_class,
                            average=average)
    ```


#### output report/resources

* `@log(logger)` is need.

* `@resources(ait_output, path_helper, 'ConfusionMatrixHeatmap')` is need. `ConfusionMatrixHeatmap` will change report/resources in ait.manifest.json.

``` important:: argument 'file_path' must define. because 'ConfusionMatrixHeatmap' filepath read from ait.input.json and set 'file_path' at '@resources'
```

* example

    ```py
    @log(logger)
    @resources(ait_output, path_helper, 'ConfusionMatrixHeatmap')
    def save_confusion_matrix_heatmap(y_test, y_pred, file_path: str=None) -> None:
        makedirs(str(Path(file_path).parent), exist_ok=True)

        y_pred = K.argmax(y_pred)

        labels = sorted(list(set(y_test)))
        cmx_data = confusion_matrix(y_test, y_pred, labels=labels)

        df_cmx = pd.DataFrame(cmx_data, index=labels, columns=labels)

        fig = plt.figure(dpi=100, figsize=(8,6))
        sn.heatmap(df_cmx, annot=True, fmt='g' ,square = True)
        ax = fig.add_subplot(1, 1, 1)
        ax.set_xlabel('Predicted class')
        ax.set_ylabel('Actual class')
        ax.set_title('Plot of Confusion Matrix')

        # save as png
        plt.savefig(file_path)
    ```


#### output downloads

* `@log(logger)` is need.

* `@downloads(ait_output, path_helper, 'ConfusionMatrixCSV')` is need. `ConfusionMatrixCSV` will change downloads in ait.manifest.json.

``` important:: argument 'file_path' must define. because 'ConfusionMatrixCSV' filepath read from ait.input.json and set 'file_path' at '@downloads'
```
* example

    ```py
    @log(logger)
    @downloads(ait_output, path_helper, 'ConfusionMatrixCSV')
    def save_confusion_matrix_csv(y_test, y_pred, file_path: str=None) -> None:
        makedirs(str(Path(file_path).parent), exist_ok=True)

        cmx_data = confusion_matrix(y_test, K.argmax(y_pred))
        logger.info(cmx_data)
        np.savetxt(file_path, cmx_data, fmt='%d', delimiter=',')
    ```


### #9 area: main

* read invenotries and call `area: functions`.

* `@log(logger)` is need.

* `@ait_main(ait_output, path_helper)` is need.

* example

    ```py
    @log(logger)
    @ait_main(ait_output, path_helper)
    def main() -> None:
        image_px_size = ait_input.get_method_param_value('image_px_size')

        # load MNIST image and label from inventory
        mnist = MNIST()
        X_test = mnist.load_image(ait_input.get_inventory_path('test_set_images'), image_px_size)
        y_test = mnist.load_label(ait_input.get_inventory_path('test_set_labels'))

        # preprocess normarize
        X_test_normalize = X_test / 255

        # load model
        model = tf.keras.models.load_model(ait_input.get_inventory_path('trained_model'))
        logger.info(get_summary_text(model))

        # predoction
        y_pred = model.predict(X_test_normalize)

        # Total accuracy evaluation value(measure)
        calc_acc_all(y_test=y_test, y_pred=y_pred)

        # Accuracy Rating by Class(measure)
        calc_acc_by_class(y_test=y_test, y_pred=y_pred)

        # Confusion matrix(CSV)
        save_confusion_matrix_csv(y_test=y_test, y_pred=y_pred)

        # Confusion matrix(PNG)
        save_confusion_matrix_heatmap(y_test=y_test, y_pred=y_pred)

        # ROC curve(PNG)
        save_roc_curve(y_test=y_test, y_pred=y_pred, 
                        n_classes=ait_input.get_method_param_value('class_count'))

        # AUC(measure)
        calc_auc(y_test=y_test, y_pred=y_pred,
                multi_class=ait_input.get_method_param_value('auc_multi_class'),
                average=ait_input.get_method_param_value('auc_average'))

        # NG predictions(PNG)
        save_ng_predicts(X_test=X_test, y_test=y_test, y_pred=y_pred, 
                        n_classes= int(ait_input.get_method_param_value('class_count')))

        # PredictionResult(CSV)
        save_prediction_result(y_test=y_test, y_pred=y_pred)

        # log(Text)
        move_log()
    ```

### #11 area: license attribute set

* This section sets the license attribute information for AIT.

* set `ait_owner` and `ait_creation_year`.