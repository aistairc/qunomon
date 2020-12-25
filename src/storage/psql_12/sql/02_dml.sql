pg_dump: warning: there are circular foreign-key constraints on this table:
pg_dump:   T_TestDescription
pg_dump: You might not be able to restore the dump without using --disable-triggers or temporarily dropping the constraints.
pg_dump: Consider using a full dump instead of a --data-only dump to avoid this problem.
--
-- PostgreSQL database dump
--

-- Dumped from database version 12.3
-- Dumped by pg_dump version 12.3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'SJIS';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: M_DataType; Type: TABLE DATA; Schema: public; Owner: user
--

INSERT INTO public."M_DataType" (id, name) VALUES (1, 'dataset');
INSERT INTO public."M_DataType" (id, name) VALUES (2, 'model');
INSERT INTO public."M_DataType" (id, name) VALUES (3, 'attribute set');


--
-- Data for Name: M_TestRunner; Type: TABLE DATA; Schema: public; Owner: user
--

-- INSERT INTO public."M_TestRunner" (id, name, description, author, email, version, quality, landing_page) VALUES (1, 'acc_check_1.0.py', 'eval_acc_check_by_tfmodel_1.0', 'John Smith', 'John_Smith@aaa.com', '1', 'https://airc.aist.go.jp/aiqm/quality/internal/学習の正確性', 'https://aithub.com/acc_check/1.0');
-- INSERT INTO public."M_TestRunner" (id, name, description, author, email, version, quality, landing_page) VALUES (2, 'adversarial_example_acc_test_1.0.py', 'eval_adversarial_example_acc_test_by_tfmodel_1.0', 'John Smith', 'John_Smith@aaa.com', '1', 'https://airc.aist.go.jp/aiqm/quality/internal/学習の安定性', 'https://aithub.com/adversarial_example_acc_test/1.0');
-- INSERT INTO public."M_TestRunner" (id, name, description, author, email, version, quality, landing_page) VALUES (3, 'dev_hello_world', 'dev_hello_world_0.1', 'John Smith', 'John_Smith@aaa.com', '0.1', 'https://airc.aist.go.jp/aiqm/quality/internal/学習の安定性', 'https://aithub.com/dev_hello_world/');


--
-- Data for Name: M_Downloadable_Template; Type: TABLE DATA; Schema: public; Owner: user
--

-- INSERT INTO public."M_Downloadable_Template" (id, name, path, description, test_runner_id) VALUES (1, 'log.txt', '/aa/bb/cc/log.txt', 'log data', 1);
-- INSERT INTO public."M_Downloadable_Template" (id, name, path, description, test_runner_id) VALUES (2, 'log.txt', '/aa/bb/cc/log.txt', 'log data', 2);
-- INSERT INTO public."M_Downloadable_Template" (id, name, path, description, test_runner_id) VALUES (3, 'log.txt', '/usr/local/qai/downloads/1/log.txt', 'log data', 3);
-- INSERT INTO public."M_Downloadable_Template" (id, name, path, description, test_runner_id) VALUES (4, 'adversarial_samples', '/usr/local/qai/downloads/2/adversarial_samples.zip', 'log data', 3);
-- INSERT INTO public."M_Downloadable_Template" (id, name, path, description, test_runner_id) VALUES (5, 'adversarial_samples', '/usr/local/qai/downloads/3/ait.log', 'log data', 3);


--
-- Data for Name: M_FileSystem; Type: TABLE DATA; Schema: public; Owner: user
--

INSERT INTO public."M_FileSystem" (id, name) VALUES (1, 'UNIX_FILE_SYSTEM');
INSERT INTO public."M_FileSystem" (id, name) VALUES (2, 'WINDOWS_FILE');


--
-- Data for Name: M_ResourceType; Type: TABLE DATA; Schema: public; Owner: user
--

INSERT INTO public."M_ResourceType" (id, type) VALUES (1, 'text');
INSERT INTO public."M_ResourceType" (id, type) VALUES (2, 'picture');
INSERT INTO public."M_ResourceType" (id, type) VALUES (3, 'table');
INSERT INTO public."M_ResourceType" (id, type) VALUES (4, 'binary');


--
-- Data for Name: M_Format; Type: TABLE DATA; Schema: public; Owner: user
--

INSERT INTO public."M_Format" (id, format_, resource_type_id) VALUES (1, 'png', 2);
INSERT INTO public."M_Format" (id, format_, resource_type_id) VALUES (2, 'jpg', 2);
INSERT INTO public."M_Format" (id, format_, resource_type_id) VALUES (3, 'jpeg', 2);
INSERT INTO public."M_Format" (id, format_, resource_type_id) VALUES (4, 'jpe', 2);
INSERT INTO public."M_Format" (id, format_, resource_type_id) VALUES (5, 'tif', 2);
INSERT INTO public."M_Format" (id, format_, resource_type_id) VALUES (6, 'tiff', 2);
INSERT INTO public."M_Format" (id, format_, resource_type_id) VALUES (7, 'bmp', 2);
INSERT INTO public."M_Format" (id, format_, resource_type_id) VALUES (8, 'csv', 3);
INSERT INTO public."M_Format" (id, format_, resource_type_id) VALUES (9, 'tsv', 3);
INSERT INTO public."M_Format" (id, format_, resource_type_id) VALUES (10, 'onnx', 4);
INSERT INTO public."M_Format" (id, format_, resource_type_id) VALUES (11, 'txt', 1);
INSERT INTO public."M_Format" (id, format_, resource_type_id) VALUES (12, 'text', 1);
INSERT INTO public."M_Format" (id, format_, resource_type_id) VALUES (13, 'json', 1);
INSERT INTO public."M_Format" (id, format_, resource_type_id) VALUES (14, 'xml', 1);
INSERT INTO public."M_Format" (id, format_, resource_type_id) VALUES (15, 'md', 1);
INSERT INTO public."M_Format" (id, format_, resource_type_id) VALUES (16, 'h5', 4);
INSERT INTO public."M_Format" (id, format_, resource_type_id) VALUES (17, 'zip', 4);
INSERT INTO public."M_Format" (id, format_, resource_type_id) VALUES (18, 'gz', 4);
INSERT INTO public."M_Format" (id, format_, resource_type_id) VALUES (19, '7z', 4);
INSERT INTO public."M_Format" (id, format_, resource_type_id) VALUES (20, 'dump', 4);
INSERT INTO public."M_Format" (id, format_, resource_type_id) VALUES (21, 'dmp', 4);
INSERT INTO public."M_Format" (id, format_, resource_type_id) VALUES (22, 'bin', 4);
INSERT INTO public."M_Format" (id, format_, resource_type_id) VALUES (23, 'dat', 4);
INSERT INTO public."M_Format" (id, format_, resource_type_id) VALUES (24, 'data', 4);
INSERT INTO public."M_Format" (id, format_, resource_type_id) VALUES (25, '*', 4);


--
-- Data for Name: M_GraphTemplate; Type: TABLE DATA; Schema: public; Owner: user
--

-- INSERT INTO public."M_GraphTemplate" (id, type, name, path, description, test_runner_id) VALUES (1, 'picture', 'log.png', '/aa/bb/cc/log.png', 'one image', 1);
-- INSERT INTO public."M_GraphTemplate" (id, type, name, path, description, test_runner_id) VALUES (2, 'picture', 'log.png', '/aa/bb/cc/log.png', 'one image', 1);
-- INSERT INTO public."M_GraphTemplate" (id, type, name, path, description, test_runner_id) VALUES (3, 'table', 'distribution_graph', 'aa/bb/cc/distribution_graph.png', 'image', 1);
-- INSERT INTO public."M_GraphTemplate" (id, type, name, path, description, test_runner_id) VALUES (4, 'table', 'acc.csv', './acc.csv', 'acc csv', 3);
-- INSERT INTO public."M_GraphTemplate" (id, type, name, path, description, test_runner_id) VALUES (5, 'picture', 'acc.png', './acc.png', 'acc image', 3);
-- INSERT INTO public."M_GraphTemplate" (id, type, name, path, description, test_runner_id) VALUES (6, 'picture', 'images.png', './images.png', 'image', 3);
-- INSERT INTO public."M_GraphTemplate" (id, type, name, path, description, test_runner_id) VALUES (7, 'table', 'Incorrect_data.csv', './Incorrect_data.csv', 'incorrect data csv', 3);

--
-- Data for Name: M_MLFrameworkMapper; Type: TABLE DATA; Schema: public; Owner: user
--

INSERT INTO public."M_MLFrameworkMapper" (id, name) VALUES (1, 'Tensorflow-2.3');


--
-- Data for Name: M_Organization; Type: TABLE DATA; Schema: public; Owner: user
--

INSERT INTO public."M_Organization" (id, name) VALUES ('dep-a', '部署A');
INSERT INTO public."M_Organization" (id, name) VALUES ('dep-b', '部署B');
INSERT INTO public."M_Organization" (id, name) VALUES ('dep-c', '部署C');


--
-- Data for Name: M_MLComponent; Type: TABLE DATA; Schema: public; Owner: user
--

-- INSERT INTO public."M_MLComponent" (id, name, description, problem_domain, org_id, ml_framework_id) VALUES (1, 'A社住宅価格予測-機械学習コンポーネント', 'A社の住宅価格を予測する機械学習コンポーネント', '重回帰分析', 'dep-a', 1);
-- INSERT INTO public."M_MLComponent" (id, name, description, problem_domain, org_id, ml_framework_id) VALUES (2, 'B社文字認識-機械学習コンポーネント', 'B社の文字を認識する機械学習コンポーネント', '画像分類', 'dep-a', 1);
-- INSERT INTO public."M_MLComponent" (id, name, description, problem_domain, org_id, ml_framework_id) VALUES (3, 'C社ゴルフスコア読取-機械学習コンポーネント', 'C社のスコア表枠組み、文字を認識する機械学習コンポーネント', 'レイアウト認識、画像分類', 'dep-a', 1);


--
-- Data for Name: M_Inventory; Type: TABLE DATA; Schema: public; Owner: user
--

-- INSERT INTO public."M_Inventory" (id, name, type, file_system, file_path, description, delete_flag, schema, creation_datetime, update_datetime, ml_component_id) VALUES (1, 'TestDataset_0818', 'dataset', 'UNIX_FILE_SYSTEM', '\usr\local\airflow\ip\dummyInventory\test.csv', '0818用のデータセット', false, 'http://yann.lecun.com/exdb/mnist/', '2020-09-30 10:06:11.896638', '2020-09-30 10:06:11.896638', 1);
-- INSERT INTO public."M_Inventory" (id, name, type, file_system, file_path, description, delete_flag, schema, creation_datetime, update_datetime, ml_component_id) VALUES (2, 'TrainedModel_0907', 'model', 'UNIX_FILE_SYSTEM', '\usr\local\airflow\ip\dummyInventory\test.csv', '0918用のデータセット', false, 'http://yann.lecun.com/exdb/mnist/', '2020-09-30 10:06:11.898639', '2020-09-30 10:06:11.898639', 1);
-- INSERT INTO public."M_Inventory" (id, name, type, file_system, file_path, description, delete_flag, schema, creation_datetime, update_datetime, ml_component_id) VALUES (3, 'TestDataset_0918', 'dataset', 'UNIX_FILE_SYSTEM', '\usr\local\airflow\ip\dummyInventory\test.csv', '0907用のモデル', false, 'https://support.hdfgroup.org/HDF5/doc/index.html', '2020-09-30 10:06:11.898639', '2020-09-30 10:06:11.898639', 1);
-- INSERT INTO public."M_Inventory" (id, name, type, file_system, file_path, description, delete_flag, schema, creation_datetime, update_datetime, ml_component_id) VALUES (4, 'TestDataset_1002', 'dataset', 'UNIX_FILE_SYSTEM', '\usr\local\airflow\ip\dummyInventory\test.csv', '1007用のモデル', false, 'https://support.hdfgroup.org/HDF5/doc/index.html', '2020-09-30 10:06:11.900237', '2020-09-30 10:06:11.900237', 1);
-- INSERT INTO public."M_Inventory" (id, name, type, file_system, file_path, description, delete_flag, schema, creation_datetime, update_datetime, ml_component_id) VALUES (5, 'DUMMY1_ONNX', 'model', 'WINDOWS_FILE', '\usr\local\airflow\ip\dummyInventory\test.csv', '開発用ダミーデータ', false, 'http://www.kasai.fm/wiki/rfc4180jp', '2020-09-30 10:06:11.900237', '2020-09-30 10:06:11.900237', 1);
-- INSERT INTO public."M_Inventory" (id, name, type, file_system, file_path, description, delete_flag, schema, creation_datetime, update_datetime, ml_component_id) VALUES (6, 'DUMMY2_ONNX', 'model', 'WINDOWS_FILE', '\usr\local\airflow\ip\dummyInventory\test.csv', '開発用ダミーデータ', false, 'http://www.kasai.fm/wiki/rfc4180jp', '2020-09-30 10:06:11.901233', '2020-09-30 10:06:11.901233', 1);


--
-- Data for Name: M_Inventory_Format; Type: TABLE DATA; Schema: public; Owner: user
--

-- INSERT INTO public."M_Inventory_Format" (id, inventory_id, format_id) VALUES (1, 1, 4);
-- INSERT INTO public."M_Inventory_Format" (id, inventory_id, format_id) VALUES (2, 2, 4);
-- INSERT INTO public."M_Inventory_Format" (id, inventory_id, format_id) VALUES (3, 3, 6);
-- INSERT INTO public."M_Inventory_Format" (id, inventory_id, format_id) VALUES (4, 4, 6);
-- INSERT INTO public."M_Inventory_Format" (id, inventory_id, format_id) VALUES (5, 5, 4);


--
-- Data for Name: M_Tag; Type: TABLE DATA; Schema: public; Owner: user
--

-- INSERT INTO public."M_Tag" (id, name, type) VALUES (1, 'CSV', 'INVENTORY');
-- INSERT INTO public."M_Tag" (id, name, type) VALUES (2, 'TF_MODEL', 'INVENTORY');
-- INSERT INTO public."M_Tag" (id, name, type) VALUES (3, 'ZIP', 'INVENTORY');



--
-- Data for Name: M_Quality_Dimension; Type: TABLE DATA; Schema: public; Owner: user
--

INSERT INTO public."M_Quality_Dimension" (id, name) VALUES (1, 'Completeness_of_problem_domain_analysis');
INSERT INTO public."M_Quality_Dimension" (id, name) VALUES (2, 'Coverage_for_distinguished_problem_cases');
INSERT INTO public."M_Quality_Dimension" (id, name) VALUES (3, 'Diversity_of_test_data');
INSERT INTO public."M_Quality_Dimension" (id, name) VALUES (4, 'Distribution_of_training_data');
INSERT INTO public."M_Quality_Dimension" (id, name) VALUES (5, 'Accuracy_of_trained_model');
INSERT INTO public."M_Quality_Dimension" (id, name) VALUES (6, 'Robustness_of_trained_model');
INSERT INTO public."M_Quality_Dimension" (id, name) VALUES (7, 'Stability_Maintainability_of_quality');
INSERT INTO public."M_Quality_Dimension" (id, name) VALUES (8, 'Dependability_of_underlying_software');


--
-- Data for Name: M_Structure; Type: TABLE DATA; Schema: public; Owner: user
--

INSERT INTO public."M_Structure" (id, structure) VALUES (1, 'single');


--
-- Data for Name: M_Quality_Measurement; Type: TABLE DATA; Schema: public; Owner: user
--

-- INSERT INTO public."M_Quality_Measurement" (id, name, description, type, structure_id, quality_dimension_id, test_runner_id) VALUES (1, '学習モデルの精度計測', '学習モデルの正確性評価指標', 'float', 1, 5, 1);
-- INSERT INTO public."M_Quality_Measurement" (id, name, description, type, structure_id, quality_dimension_id, test_runner_id) VALUES (2, '学習モデルの敵対的サンプル安定性計測', '学習モデルの安定性評価指標', 'float', 1, 6, 2);
-- INSERT INTO public."M_Quality_Measurement" (id, name, description, type, structure_id, quality_dimension_id, test_runner_id) VALUES (3, '学習モデルの敵対的サンプル安定性計測2', '学習モデルの安定性評価指標', 'float', 1, 6, 3);


--
-- Data for Name: M_RelationalOperator; Type: TABLE DATA; Schema: public; Owner: user
--

INSERT INTO public."M_RelationalOperator" (id, expression, description) VALUES (1, '==', '値が等しければTrue');
INSERT INTO public."M_RelationalOperator" (id, expression, description) VALUES (2, '!=', '値が等しくなければTrue');
INSERT INTO public."M_RelationalOperator" (id, expression, description) VALUES (3, '>', '値が大きければTrue');
INSERT INTO public."M_RelationalOperator" (id, expression, description) VALUES (4, '<', '値が小さければTrue');
INSERT INTO public."M_RelationalOperator" (id, expression, description) VALUES (5, '>=', '値が同じか大きければTrue');
INSERT INTO public."M_RelationalOperator" (id, expression, description) VALUES (6, '<=', '値が同じか小さければTrue');


--
-- Data for Name: M_Setting; Type: TABLE DATA; Schema: public; Owner: user
--

INSERT INTO public."M_Setting" (key, value) VALUES ('backend_entry_point', 'http://127.0.0.1:8888/qai-testbed/api/0.0.1');
INSERT INTO public."M_Setting" (key, value) VALUES ('ip_entry_point', 'http://ip:6000/qai-ip/api/0.0.1');
INSERT INTO public."M_Setting" (key, value) VALUES ('mount_src_path', 'testbed_mount_volume_src');
INSERT INTO public."M_Setting" (key, value) VALUES ('mount_dst_path', '/testbed_mount_volume_dst');
INSERT INTO public."M_Setting" (key, value) VALUES ('airflow_entry_point', 'http://airflow:8080');
INSERT INTO public."M_Setting" (key, value) VALUES ('docker_repository_url', 'registry:5500');
INSERT INTO public."M_Setting" (key, value) VALUES ('airflow_mount_volume_path', '/testbed_mount_volume_dst');
INSERT INTO public."M_Setting" (key, value) VALUES ('report_resource_limit', '20');


--
-- Data for Name: M_TestInventoryTemplate; Type: TABLE DATA; Schema: public; Owner: user
--

-- INSERT INTO public."M_TestInventoryTemplate" (id_, name, type_, description, schema, test_runner_id) VALUES (1, 'TestDataSet', 'dataset', '28x28のpng', 'http://yann.lecun.com/exdb/mnist/', 1);
-- INSERT INTO public."M_TestInventoryTemplate" (id_, name, type_, description, schema, test_runner_id) VALUES (2, 'TrainedModel', 'model', 'ONNXファイル', 'https://onnx.ai/about.html', 1);
-- INSERT INTO public."M_TestInventoryTemplate" (id_, name, type_, description, schema, test_runner_id) VALUES (3, 'TestMetaDataSet', 'dataset', 'jpg, jpeg', 'http://yann.lecun.com/exdb/mnist/', 2);
-- INSERT INTO public."M_TestInventoryTemplate" (id_, name, type_, description, schema, test_runner_id) VALUES (4, 'TestDataSet', 'dataset', 'csv, tsv', 'http://yann.lecun.com/exdb/mnist/', 2);
-- INSERT INTO public."M_TestInventoryTemplate" (id_, name, type_, description, schema, test_runner_id) VALUES (5, 'TrainedModel', 'model', 'ONNXファイル', 'https://onnx.ai/about.html', 2);
-- INSERT INTO public."M_TestInventoryTemplate" (id_, name, type_, description, schema, test_runner_id) VALUES (6, 'TrainedModel', 'model', 'ONNXファイル', 'https://onnx.ai/about.html', 3);


--
-- Data for Name: M_TestInventoryTemplateTag; Type: TABLE DATA; Schema: public; Owner: user
--

-- INSERT INTO public."M_TestInventoryTemplateTag" (id_, inventory_template_id, tag_id) VALUES (1, 1, 1);
-- INSERT INTO public."M_TestInventoryTemplateTag" (id_, inventory_template_id, tag_id) VALUES (2, 2, 2);
-- INSERT INTO public."M_TestInventoryTemplateTag" (id_, inventory_template_id, tag_id) VALUES (3, 3, 1);
-- INSERT INTO public."M_TestInventoryTemplateTag" (id_, inventory_template_id, tag_id) VALUES (4, 4, 3);
-- INSERT INTO public."M_TestInventoryTemplateTag" (id_, inventory_template_id, tag_id) VALUES (5, 5, 2);
-- INSERT INTO public."M_TestInventoryTemplateTag" (id_, inventory_template_id, tag_id) VALUES (6, 6, 2);


--
-- Data for Name: M_TestInventoryTemplate_Format; Type: TABLE DATA; Schema: public; Owner: user
--

-- INSERT INTO public."M_TestInventoryTemplate_Format" (id, inventory_template_id, format_id) VALUES (1, 1, 1);
-- INSERT INTO public."M_TestInventoryTemplate_Format" (id, inventory_template_id, format_id) VALUES (2, 2, 6);
-- INSERT INTO public."M_TestInventoryTemplate_Format" (id, inventory_template_id, format_id) VALUES (3, 3, 2);
-- INSERT INTO public."M_TestInventoryTemplate_Format" (id, inventory_template_id, format_id) VALUES (4, 3, 3);
-- INSERT INTO public."M_TestInventoryTemplate_Format" (id, inventory_template_id, format_id) VALUES (5, 4, 4);
-- INSERT INTO public."M_TestInventoryTemplate_Format" (id, inventory_template_id, format_id) VALUES (6, 4, 5);
-- INSERT INTO public."M_TestInventoryTemplate_Format" (id, inventory_template_id, format_id) VALUES (7, 5, 6);
-- INSERT INTO public."M_TestInventoryTemplate_Format" (id, inventory_template_id, format_id) VALUES (8, 6, 6);


--
-- Data for Name: M_TestRunnerParamTemplate; Type: TABLE DATA; Schema: public; Owner: user
--

-- INSERT INTO public."M_TestRunnerParamTemplate" (id_, name, value_type, description, default_value, test_runner_id) VALUES (1, 'Threshold', 'float', '敵対的生成のずらし具合, \epsilon \in \{0.0, 1.0\', '0.5', 1);
-- INSERT INTO public."M_TestRunnerParamTemplate" (id_, name, value_type, description, default_value, test_runner_id) VALUES (2, 'Lower Limit', 'float', '敵対的生成のずらし具合, \epsilon \in \{0.0, 1.0\', '0.3', 1);
-- INSERT INTO public."M_TestRunnerParamTemplate" (id_, name, value_type, description, default_value, test_runner_id) VALUES (3, 'Upper Limit', 'float', '敵対的生成のずらし具合, \epsilon \in \{0.0, 1.0\', '1.0', 1);
-- INSERT INTO public."M_TestRunnerParamTemplate" (id_, name, value_type, description, default_value, test_runner_id) VALUES (4, 'select', 'string', 'select', '', 2);
-- INSERT INTO public."M_TestRunnerParamTemplate" (id_, name, value_type, description, default_value, test_runner_id) VALUES (5, 'nb_examples', 'int', '単純ベイズ分類器', '', 2);
-- INSERT INTO public."M_TestRunnerParamTemplate" (id_, name, value_type, description, default_value, test_runner_id) VALUES (6, 'balance_sampling', 'string', '母集団からユニットをランダムに選択する方法', '', 2);
-- INSERT INTO public."M_TestRunnerParamTemplate" (id_, name, value_type, description, default_value, test_runner_id) VALUES (7, 'test_mode', 'string', 'test_mode', '', 2);
-- INSERT INTO public."M_TestRunnerParamTemplate" (id_, name, value_type, description, default_value, test_runner_id) VALUES (8, 'attacks', 'string', 'attacks', '', 2);
-- INSERT INTO public."M_TestRunnerParamTemplate" (id_, name, value_type, description, default_value, test_runner_id) VALUES (9, 'robustness', 'string', 'ニューラルネットワークのトレーニング、評価、探索', '', 2);
-- INSERT INTO public."M_TestRunnerParamTemplate" (id_, name, value_type, description, default_value, test_runner_id) VALUES (10, 'detection', 'string', 'detection', '', 2);
-- INSERT INTO public."M_TestRunnerParamTemplate" (id_, name, value_type, description, default_value, test_runner_id) VALUES (11, 'Name', 'string', 'Name', '', 3);


--
-- Data for Name: M_TestRunnerReference; Type: TABLE DATA; Schema: public; Owner: user
--



--
-- Data for Name: T_Download; Type: TABLE DATA; Schema: public; Owner: user
--

-- INSERT INTO public."T_Download" (id, path) VALUES (1, 'C:\Windows\System32\nvidia-smi.1.pdf');


--
-- Data for Name: T_Job; Type: TABLE DATA; Schema: public; Owner: user
--



--
-- Data for Name: T_Run; Type: TABLE DATA; Schema: public; Owner: user
--



--
-- Data for Name: T_Downloadable_Data; Type: TABLE DATA; Schema: public; Owner: user
--



--
-- Data for Name: T_Graph; Type: TABLE DATA; Schema: public; Owner: user
--



--
-- Data for Name: T_Test; Type: TABLE DATA; Schema: public; Owner: user
--

-- INSERT INTO public."T_Test" (id, report_url, job_id, ml_component_id) VALUES (1, NULL, NULL, 1);


--
-- Data for Name: T_TestDescription; Type: TABLE DATA; Schema: public; Owner: user
--

-- INSERT INTO public."T_TestDescription" (id, name, creation_datetime, update_datetime, opinion, delete_flag, value_target, test_id, quality_dimension_id, test_runner_id, parent_id, run_id) VALUES (1, 'ACC_check_v1', '2020-09-30 10:06:11.916748', '2020-09-30 10:06:11.916748', '精度について問題なし。', false, true, 1, 5, 1, NULL, NULL);
-- INSERT INTO public."T_TestDescription" (id, name, creation_datetime, update_datetime, opinion, delete_flag, value_target, test_id, quality_dimension_id, test_runner_id, parent_id, run_id) VALUES (2, 'Adversarial Example ACC testing Test_v1', '2020-09-30 10:06:11.918747', '2020-09-30 10:06:11.918747', 'adversarial exampleにより、精度が悪化しているが、運用上悪意ある画像が入力される可能性がないため、指標を満たしていないが、本件問題なしとする。', false, true, 1, 6, 2, NULL, NULL);
-- INSERT INTO public."T_TestDescription" (id, name, creation_datetime, update_datetime, opinion, delete_flag, value_target, test_id, quality_dimension_id, test_runner_id, parent_id, run_id) VALUES (3, 'dag_test', '2020-09-30 10:06:11.919747', '2020-09-30 10:06:11.919747', '精度について問題なし。', false, true, 1, 6, 3, NULL, NULL);


--
-- Data for Name: T_Inventory_TestDescription; Type: TABLE DATA; Schema: public; Owner: user
--

-- INSERT INTO public."T_Inventory_TestDescription" (id, inventory_id, template_inventory_id, test_description_id) VALUES (1, 1, 1, 1);
-- INSERT INTO public."T_Inventory_TestDescription" (id, inventory_id, template_inventory_id, test_description_id) VALUES (2, 2, 2, 1);
-- INSERT INTO public."T_Inventory_TestDescription" (id, inventory_id, template_inventory_id, test_description_id) VALUES (3, 1, 3, 2);
-- INSERT INTO public."T_Inventory_TestDescription" (id, inventory_id, template_inventory_id, test_description_id) VALUES (4, 2, 4, 2);
-- INSERT INTO public."T_Inventory_TestDescription" (id, inventory_id, template_inventory_id, test_description_id) VALUES (5, 5, 5, 3);


--
-- Data for Name: T_Operand; Type: TABLE DATA; Schema: public; Owner: user
--

-- INSERT INTO public."T_Operand" (id, value, quality_measurement_id, test_description_id, relational_operator_id) VALUES (1, '80', 1, 1, 3);
-- INSERT INTO public."T_Operand" (id, value, quality_measurement_id, test_description_id, relational_operator_id) VALUES (2, '50', 2, 2, 4);
-- INSERT INTO public."T_Operand" (id, value, quality_measurement_id, test_description_id, relational_operator_id) VALUES (3, '10', 3, 3, 5);


--
-- Data for Name: T_TestRunnerParam; Type: TABLE DATA; Schema: public; Owner: user
--

-- INSERT INTO public."T_TestRunnerParam" (id, value, test_runner_param_template_id, test_description_id) VALUES (1, '0.5', 1, 1);
-- INSERT INTO public."T_TestRunnerParam" (id, value, test_runner_param_template_id, test_description_id) VALUES (2, '0.3', 2, 1);
-- INSERT INTO public."T_TestRunnerParam" (id, value, test_runner_param_template_id, test_description_id) VALUES (3, '1.0', 3, 2);
-- INSERT INTO public."T_TestRunnerParam" (id, value, test_runner_param_template_id, test_description_id) VALUES (4, NULL, 4, 2);
-- INSERT INTO public."T_TestRunnerParam" (id, value, test_runner_param_template_id, test_description_id) VALUES (5, '2000', 5, 2);
-- INSERT INTO public."T_TestRunnerParam" (id, value, test_runner_param_template_id, test_description_id) VALUES (6, '', 6, 2);
-- INSERT INTO public."T_TestRunnerParam" (id, value, test_runner_param_template_id, test_description_id) VALUES (7, NULL, 7, 2);
-- INSERT INTO public."T_TestRunnerParam" (id, value, test_runner_param_template_id, test_description_id) VALUES (8, 'FGSM?eps=0.1;', 8, 2);
-- INSERT INTO public."T_TestRunnerParam" (id, value, test_runner_param_template_id, test_description_id) VALUES (9, 'none;FeatureSqueezing?squeezer=bit_depth_1;', 9, 2);
-- INSERT INTO public."T_TestRunnerParam" (id, value, test_runner_param_template_id, test_description_id) VALUES (10, 'FeatureSqueezing?squeezers=bit_depth_1,median_filter_2_2&distance_measure=l1&fpr=0.05;', 10, 2);
-- INSERT INTO public."T_TestRunnerParam" (id, value, test_runner_param_template_id, test_description_id) VALUES (11, 'ODAIBA', 11, 3);


--
-- Name: M_DataType_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public."M_DataType_id_seq"', 3, true);


--
-- Name: M_Downloadable_Template_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public."M_Downloadable_Template_id_seq"', 1, true);


--
-- Name: M_FileSystem_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public."M_FileSystem_id_seq"', 2, true);


--
-- Name: M_Format_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public."M_Format_id_seq"', 25, true);


--
-- Name: M_GraphTemplate_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public."M_GraphTemplate_id_seq"', 1, true);


--
-- Name: M_Inventory_Format_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public."M_Inventory_Format_id_seq"', 1, true);



--
-- Name: M_Inventory_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public."M_Inventory_id_seq"', 1, true);


--
-- Name: M_MLComponent_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public."M_MLComponent_id_seq"', 1, true);


--
-- Name: M_MLFrameworkMapper_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public."M_MLFrameworkMapper_id_seq"', 1, true);


--
-- Name: M_Quality_Dimension_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public."M_Quality_Dimension_id_seq"', 8, true);


--
-- Name: M_Quality_Measurement_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public."M_Quality_Measurement_id_seq"', 1, true);


--
-- Name: M_RelationalOperator_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public."M_RelationalOperator_id_seq"', 6, true);


--
-- Name: M_ResourceType_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public."M_ResourceType_id_seq"', 4, true);


--
-- Name: M_Structure_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public."M_Structure_id_seq"', 1, true);


--
-- Name: M_Tag_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public."M_Tag_id_seq"', 1, true);


--
-- Name: M_TestInventoryTemplateTag_id__seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public."M_TestInventoryTemplateTag_id__seq"', 1, true);


--
-- Name: M_TestInventoryTemplate_Format_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public."M_TestInventoryTemplate_Format_id_seq"', 1, true);


--
-- Name: M_TestInventoryTemplate_id__seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public."M_TestInventoryTemplate_id__seq"', 1, true);


--
-- Name: M_TestRunnerParamTemplate_id__seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public."M_TestRunnerParamTemplate_id__seq"', 1, true);


--
-- Name: M_TestRunnerReference_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public."M_TestRunnerReference_id_seq"', 1, false);


--
-- Name: M_TestRunner_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public."M_TestRunner_id_seq"', 1, true);


--
-- Name: T_Download_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public."T_Download_id_seq"', 1, true);


--
-- Name: T_Downloadable_Data_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public."T_Downloadable_Data_id_seq"', 1, false);


--
-- Name: T_Graph_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public."T_Graph_id_seq"', 1, false);


--
-- Name: T_Inventory_TestDescription_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public."T_Inventory_TestDescription_id_seq"', 1, true);


--
-- Name: T_Job_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public."T_Job_id_seq"', 1, false);


--
-- Name: T_Operand_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public."T_Operand_id_seq"', 1, true);


--
-- Name: T_Run_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public."T_Run_id_seq"', 1, false);


--
-- Name: T_TestDescription_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public."T_TestDescription_id_seq"', 1, true);


--
-- Name: T_TestRunnerParam_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public."T_TestRunnerParam_id_seq"', 1, true);


--
-- Name: T_Test_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public."T_Test_id_seq"', 1, true);


--
-- PostgreSQL database dump complete
--

