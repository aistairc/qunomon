
--
-- Data for Name: M_Setting; Type: TABLE DATA; Schema: public; Owner: user
--

INSERT INTO public."M_Setting" (key, value) VALUES ('backend_entry_point', 'https://127.0.0.1/qai-testbed/api/0.0.1');
INSERT INTO public."M_Setting" (key, value) VALUES ('ip_entry_point', 'http://ip:6000/qai-ip/api/0.0.1');
INSERT INTO public."M_Setting" (key, value) VALUES ('mount_src_path', 'testbed_mount_volume_src');
INSERT INTO public."M_Setting" (key, value) VALUES ('mount_dst_path', '/testbed_mount_volume_dst');
INSERT INTO public."M_Setting" (key, value) VALUES ('airflow_entry_point', 'http://airflow:8080');
INSERT INTO public."M_Setting" (key, value) VALUES ('docker_repository_url', 'registry:5500');
INSERT INTO public."M_Setting" (key, value) VALUES ('airflow_mount_volume_path', '/testbed_mount_volume_dst');
INSERT INTO public."M_Setting" (key, value) VALUES ('report_resource_limit', '20');
INSERT INTO public."M_Setting" (key, value) VALUES ('aithub_url', 'https://ait-hub.pj.aist.go.jp/ait-hub/api/0.0.1');
INSERT INTO public."M_Setting" (key, value) VALUES ('docker_host_name', '380582692320.dkr.ecr.ap-northeast-1.amazonaws.com');
INSERT INTO public."M_Setting" (key, value) VALUES ('aithub_linkage_flag', '1');
INSERT INTO public."M_Setting" (key, value) VALUES ('local_create_user_account', 'local_developer');
INSERT INTO public."M_Setting" (key, value) VALUES ('local_create_user_name', 'ローカル開発者');
INSERT INTO public."M_Setting" (key, value) VALUES ('airc_create_user_account', 'airc_developer');
INSERT INTO public."M_Setting" (key, value) VALUES ('airc_create_user_name', 'airc開発者');
INSERT INTO public."M_Setting" (key, value) VALUES ('guideline_schema_files_path', '/work/files/guideline_schema/');


