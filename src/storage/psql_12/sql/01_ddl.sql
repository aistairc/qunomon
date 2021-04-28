--
-- PostgreSQL database dump
--

-- Dumped from database version 12.5
-- Dumped by pg_dump version 12.5

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: M_DataType; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public."M_DataType" (
    id integer NOT NULL,
    name character varying
);


ALTER TABLE public."M_DataType" OWNER TO "user";

--
-- Name: M_DataType_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE public."M_DataType_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."M_DataType_id_seq" OWNER TO "user";

--
-- Name: M_DataType_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE public."M_DataType_id_seq" OWNED BY public."M_DataType".id;


--
-- Name: M_Downloadable_Template; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public."M_Downloadable_Template" (
    id integer NOT NULL,
    name character varying NOT NULL,
    description character varying,
    test_runner_id integer
);


ALTER TABLE public."M_Downloadable_Template" OWNER TO "user";

--
-- Name: M_Downloadable_Template_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE public."M_Downloadable_Template_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."M_Downloadable_Template_id_seq" OWNER TO "user";

--
-- Name: M_Downloadable_Template_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE public."M_Downloadable_Template_id_seq" OWNED BY public."M_Downloadable_Template".id;


--
-- Name: M_FileSystem; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public."M_FileSystem" (
    id integer NOT NULL,
    name character varying
);


ALTER TABLE public."M_FileSystem" OWNER TO "user";

--
-- Name: M_FileSystem_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE public."M_FileSystem_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."M_FileSystem_id_seq" OWNER TO "user";

--
-- Name: M_FileSystem_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE public."M_FileSystem_id_seq" OWNED BY public."M_FileSystem".id;


--
-- Name: M_Format; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public."M_Format" (
    id integer NOT NULL,
    format_ character varying,
    resource_type_id integer
);


ALTER TABLE public."M_Format" OWNER TO "user";

--
-- Name: M_Format_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE public."M_Format_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."M_Format_id_seq" OWNER TO "user";

--
-- Name: M_Format_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE public."M_Format_id_seq" OWNED BY public."M_Format".id;


--
-- Name: M_GraphTemplate; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public."M_GraphTemplate" (
    id integer NOT NULL,
    name character varying NOT NULL,
    description character varying,
    test_runner_id integer,
    resource_type_id integer
);


ALTER TABLE public."M_GraphTemplate" OWNER TO "user";

--
-- Name: M_GraphTemplate_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE public."M_GraphTemplate_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."M_GraphTemplate_id_seq" OWNER TO "user";

--
-- Name: M_GraphTemplate_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE public."M_GraphTemplate_id_seq" OWNED BY public."M_GraphTemplate".id;


--
-- Name: M_Inventory; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public."M_Inventory" (
    id integer NOT NULL,
    name character varying NOT NULL,
    file_path character varying NOT NULL,
    description character varying,
    delete_flag boolean,
    schema character varying,
    creation_datetime timestamp without time zone,
    update_datetime timestamp without time zone,
    ml_component_id integer,
    type_id integer,
    file_system_id integer
);


ALTER TABLE public."M_Inventory" OWNER TO "user";

--
-- Name: M_Inventory_Format; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public."M_Inventory_Format" (
    id integer NOT NULL,
    inventory_id integer,
    format_id integer
);


ALTER TABLE public."M_Inventory_Format" OWNER TO "user";

--
-- Name: M_Inventory_Format_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE public."M_Inventory_Format_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."M_Inventory_Format_id_seq" OWNER TO "user";

--
-- Name: M_Inventory_Format_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE public."M_Inventory_Format_id_seq" OWNED BY public."M_Inventory_Format".id;


--
-- Name: M_Inventory_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE public."M_Inventory_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."M_Inventory_id_seq" OWNER TO "user";

--
-- Name: M_Inventory_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE public."M_Inventory_id_seq" OWNED BY public."M_Inventory".id;


--
-- Name: M_MLComponent; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public."M_MLComponent" (
    id integer NOT NULL,
    name character varying NOT NULL,
    description character varying NOT NULL,
    problem_domain character varying NOT NULL,
    delete_flag boolean,
    org_id character varying,
    ml_framework_id integer
);


ALTER TABLE public."M_MLComponent" OWNER TO "user";

--
-- Name: M_MLComponent_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE public."M_MLComponent_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."M_MLComponent_id_seq" OWNER TO "user";

--
-- Name: M_MLComponent_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE public."M_MLComponent_id_seq" OWNED BY public."M_MLComponent".id;


--
-- Name: M_MLFrameworkMapper; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public."M_MLFrameworkMapper" (
    id integer NOT NULL,
    name character varying
);


ALTER TABLE public."M_MLFrameworkMapper" OWNER TO "user";

--
-- Name: M_MLFrameworkMapper_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE public."M_MLFrameworkMapper_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."M_MLFrameworkMapper_id_seq" OWNER TO "user";

--
-- Name: M_MLFrameworkMapper_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE public."M_MLFrameworkMapper_id_seq" OWNED BY public."M_MLFrameworkMapper".id;


--
-- Name: M_Organization; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public."M_Organization" (
    id character varying NOT NULL,
    name character varying NOT NULL
);


ALTER TABLE public."M_Organization" OWNER TO "user";

--
-- Name: M_Quality_Dimension; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public."M_Quality_Dimension" (
    id integer NOT NULL,
    name character varying NOT NULL
);


ALTER TABLE public."M_Quality_Dimension" OWNER TO "user";

--
-- Name: M_Quality_Dimension_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE public."M_Quality_Dimension_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."M_Quality_Dimension_id_seq" OWNER TO "user";

--
-- Name: M_Quality_Dimension_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE public."M_Quality_Dimension_id_seq" OWNED BY public."M_Quality_Dimension".id;


--
-- Name: M_Quality_Measurement; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public."M_Quality_Measurement" (
    id integer NOT NULL,
    name character varying NOT NULL,
    description character varying NOT NULL,
    type character varying NOT NULL,
    min_value double precision,
    max_value double precision,
    structure_id integer,
    quality_dimension_id integer,
    test_runner_id integer
);


ALTER TABLE public."M_Quality_Measurement" OWNER TO "user";

--
-- Name: M_Quality_Measurement_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE public."M_Quality_Measurement_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."M_Quality_Measurement_id_seq" OWNER TO "user";

--
-- Name: M_Quality_Measurement_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE public."M_Quality_Measurement_id_seq" OWNED BY public."M_Quality_Measurement".id;


--
-- Name: M_RelationalOperator; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public."M_RelationalOperator" (
    id integer NOT NULL,
    expression character varying NOT NULL,
    description character varying NOT NULL
);


ALTER TABLE public."M_RelationalOperator" OWNER TO "user";

--
-- Name: M_RelationalOperator_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE public."M_RelationalOperator_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."M_RelationalOperator_id_seq" OWNER TO "user";

--
-- Name: M_RelationalOperator_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE public."M_RelationalOperator_id_seq" OWNED BY public."M_RelationalOperator".id;


--
-- Name: M_ResourceType; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public."M_ResourceType" (
    id integer NOT NULL,
    type character varying NOT NULL
);


ALTER TABLE public."M_ResourceType" OWNER TO "user";

--
-- Name: M_ResourceType_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE public."M_ResourceType_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."M_ResourceType_id_seq" OWNER TO "user";

--
-- Name: M_ResourceType_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE public."M_ResourceType_id_seq" OWNED BY public."M_ResourceType".id;


--
-- Name: M_Setting; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public."M_Setting" (
    key character varying NOT NULL,
    value character varying
);


ALTER TABLE public."M_Setting" OWNER TO "user";

--
-- Name: M_Structure; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public."M_Structure" (
    id integer NOT NULL,
    structure character varying
);


ALTER TABLE public."M_Structure" OWNER TO "user";

--
-- Name: M_Structure_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE public."M_Structure_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."M_Structure_id_seq" OWNER TO "user";

--
-- Name: M_Structure_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE public."M_Structure_id_seq" OWNED BY public."M_Structure".id;


--
-- Name: M_Tag; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public."M_Tag" (
    id integer NOT NULL,
    name character varying NOT NULL,
    type character varying NOT NULL
);


ALTER TABLE public."M_Tag" OWNER TO "user";

--
-- Name: M_Tag_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE public."M_Tag_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."M_Tag_id_seq" OWNER TO "user";

--
-- Name: M_Tag_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE public."M_Tag_id_seq" OWNED BY public."M_Tag".id;


--
-- Name: M_TestInventoryTemplate; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public."M_TestInventoryTemplate" (
    id_ integer NOT NULL,
    name character varying NOT NULL,
    description character varying,
    schema character varying,
    test_runner_id integer,
    type_id integer
);


ALTER TABLE public."M_TestInventoryTemplate" OWNER TO "user";

--
-- Name: M_TestInventoryTemplateTag; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public."M_TestInventoryTemplateTag" (
    id_ integer NOT NULL,
    inventory_template_id integer,
    tag_id integer
);


ALTER TABLE public."M_TestInventoryTemplateTag" OWNER TO "user";

--
-- Name: M_TestInventoryTemplateTag_id__seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE public."M_TestInventoryTemplateTag_id__seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."M_TestInventoryTemplateTag_id__seq" OWNER TO "user";

--
-- Name: M_TestInventoryTemplateTag_id__seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE public."M_TestInventoryTemplateTag_id__seq" OWNED BY public."M_TestInventoryTemplateTag".id_;


--
-- Name: M_TestInventoryTemplate_Format; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public."M_TestInventoryTemplate_Format" (
    id integer NOT NULL,
    inventory_template_id integer,
    format_id integer
);


ALTER TABLE public."M_TestInventoryTemplate_Format" OWNER TO "user";

--
-- Name: M_TestInventoryTemplate_Format_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE public."M_TestInventoryTemplate_Format_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."M_TestInventoryTemplate_Format_id_seq" OWNER TO "user";

--
-- Name: M_TestInventoryTemplate_Format_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE public."M_TestInventoryTemplate_Format_id_seq" OWNED BY public."M_TestInventoryTemplate_Format".id;


--
-- Name: M_TestInventoryTemplate_id__seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE public."M_TestInventoryTemplate_id__seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."M_TestInventoryTemplate_id__seq" OWNER TO "user";

--
-- Name: M_TestInventoryTemplate_id__seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE public."M_TestInventoryTemplate_id__seq" OWNED BY public."M_TestInventoryTemplate".id_;


--
-- Name: M_TestRunner; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public."M_TestRunner" (
    id integer NOT NULL,
    name character varying NOT NULL,
    description character varying,
    author character varying,
    email character varying,
    version character varying,
    quality character varying NOT NULL,
    landing_page character varying NOT NULL
);


ALTER TABLE public."M_TestRunner" OWNER TO "user";

--
-- Name: M_TestRunnerParamTemplate; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public."M_TestRunnerParamTemplate" (
    id_ integer NOT NULL,
    name character varying NOT NULL,
    value_type character varying NOT NULL,
    description character varying NOT NULL,
    default_value character varying,
    min_value double precision,
    max_value double precision,
    test_runner_id integer
);


ALTER TABLE public."M_TestRunnerParamTemplate" OWNER TO "user";

--
-- Name: M_TestRunnerParamTemplate_id__seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE public."M_TestRunnerParamTemplate_id__seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."M_TestRunnerParamTemplate_id__seq" OWNER TO "user";

--
-- Name: M_TestRunnerParamTemplate_id__seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE public."M_TestRunnerParamTemplate_id__seq" OWNED BY public."M_TestRunnerParamTemplate".id_;


--
-- Name: M_TestRunnerReference; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public."M_TestRunnerReference" (
    id integer NOT NULL,
    reference character varying NOT NULL,
    test_runner_id integer
);


ALTER TABLE public."M_TestRunnerReference" OWNER TO "user";

--
-- Name: M_TestRunnerReference_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE public."M_TestRunnerReference_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."M_TestRunnerReference_id_seq" OWNER TO "user";

--
-- Name: M_TestRunnerReference_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE public."M_TestRunnerReference_id_seq" OWNED BY public."M_TestRunnerReference".id;


--
-- Name: M_TestRunner_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE public."M_TestRunner_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."M_TestRunner_id_seq" OWNER TO "user";

--
-- Name: M_TestRunner_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE public."M_TestRunner_id_seq" OWNED BY public."M_TestRunner".id;


--
-- Name: T_Download; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public."T_Download" (
    id integer NOT NULL,
    path character varying NOT NULL
);


ALTER TABLE public."T_Download" OWNER TO "user";

--
-- Name: T_Download_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE public."T_Download_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."T_Download_id_seq" OWNER TO "user";

--
-- Name: T_Download_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE public."T_Download_id_seq" OWNED BY public."T_Download".id;


--
-- Name: T_Downloadable_Data; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public."T_Downloadable_Data" (
    id integer NOT NULL,
    download_address character varying NOT NULL,
    file_name character varying NOT NULL,
    run_id integer,
    downloadable_template_id integer,
    download_id integer
);


ALTER TABLE public."T_Downloadable_Data" OWNER TO "user";

--
-- Name: T_Downloadable_Data_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE public."T_Downloadable_Data_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."T_Downloadable_Data_id_seq" OWNER TO "user";

--
-- Name: T_Downloadable_Data_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE public."T_Downloadable_Data_id_seq" OWNED BY public."T_Downloadable_Data".id;


--
-- Name: T_Graph; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public."T_Graph" (
    id integer NOT NULL,
    report_required boolean NOT NULL,
    graph_address character varying NOT NULL,
    report_index integer NOT NULL,
    report_name character varying NOT NULL,
    file_name character varying NOT NULL,
    graph_template_id integer,
    run_id integer,
    download_id integer
);


ALTER TABLE public."T_Graph" OWNER TO "user";

--
-- Name: T_Graph_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE public."T_Graph_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."T_Graph_id_seq" OWNER TO "user";

--
-- Name: T_Graph_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE public."T_Graph_id_seq" OWNED BY public."T_Graph".id;


--
-- Name: T_Inventory_TestDescription; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public."T_Inventory_TestDescription" (
    id integer NOT NULL,
    inventory_id integer,
    template_inventory_id integer,
    test_description_id integer
);


ALTER TABLE public."T_Inventory_TestDescription" OWNER TO "user";

--
-- Name: T_Inventory_TestDescription_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE public."T_Inventory_TestDescription_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."T_Inventory_TestDescription_id_seq" OWNER TO "user";

--
-- Name: T_Inventory_TestDescription_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE public."T_Inventory_TestDescription_id_seq" OWNED BY public."T_Inventory_TestDescription".id;


--
-- Name: T_Job; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public."T_Job" (
    id integer NOT NULL,
    status character varying NOT NULL,
    result character varying NOT NULL,
    result_detail character varying NOT NULL,
    creation_datetime timestamp without time zone,
    test_id integer
);


ALTER TABLE public."T_Job" OWNER TO "user";

--
-- Name: T_Job_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE public."T_Job_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."T_Job_id_seq" OWNER TO "user";

--
-- Name: T_Job_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE public."T_Job_id_seq" OWNED BY public."T_Job".id;


--
-- Name: T_Operand; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public."T_Operand" (
    id integer NOT NULL,
    value character varying NOT NULL,
    enable boolean,
    quality_measurement_id integer,
    test_description_id integer,
    relational_operator_id integer
);


ALTER TABLE public."T_Operand" OWNER TO "user";

--
-- Name: T_Operand_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE public."T_Operand_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."T_Operand_id_seq" OWNER TO "user";

--
-- Name: T_Operand_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE public."T_Operand_id_seq" OWNED BY public."T_Operand".id;


--
-- Name: T_Run; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public."T_Run" (
    id integer NOT NULL,
    status character varying NOT NULL,
    result character varying,
    result_detail character varying,
    cpu_brand character varying,
    cpu_arch character varying,
    cpu_clocks character varying,
    cpu_cores character varying,
    memory_capacity character varying,
    launch_datetime timestamp without time zone,
    done_datetime timestamp without time zone,
    execution_date character varying,
    ait_output_file character varying,
    log_file character varying,
    test_description_id integer,
    error_code character varying,
    job_id integer
);


ALTER TABLE public."T_Run" OWNER TO "user";

--
-- Name: T_Run_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE public."T_Run_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."T_Run_id_seq" OWNER TO "user";

--
-- Name: T_Run_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE public."T_Run_id_seq" OWNED BY public."T_Run".id;


--
-- Name: T_Test; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public."T_Test" (
    id integer NOT NULL,
    report_url character varying,
    job_id integer,
    ml_component_id integer
);


ALTER TABLE public."T_Test" OWNER TO "user";

--
-- Name: T_TestDescription; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public."T_TestDescription" (
    id integer NOT NULL,
    name character varying NOT NULL,
    creation_datetime timestamp without time zone,
    update_datetime timestamp without time zone,
    opinion character varying NOT NULL,
    delete_flag boolean,
    value_target boolean,
    star boolean,
    test_id integer,
    quality_dimension_id integer,
    test_runner_id integer,
    parent_id integer,
    run_id integer
);


ALTER TABLE public."T_TestDescription" OWNER TO "user";

--
-- Name: T_TestDescription_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE public."T_TestDescription_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."T_TestDescription_id_seq" OWNER TO "user";

--
-- Name: T_TestDescription_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE public."T_TestDescription_id_seq" OWNED BY public."T_TestDescription".id;


--
-- Name: T_TestRunnerParam; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public."T_TestRunnerParam" (
    id integer NOT NULL,
    value character varying,
    test_runner_param_template_id integer,
    test_description_id integer
);


ALTER TABLE public."T_TestRunnerParam" OWNER TO "user";

--
-- Name: T_TestRunnerParam_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE public."T_TestRunnerParam_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."T_TestRunnerParam_id_seq" OWNER TO "user";

--
-- Name: T_TestRunnerParam_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE public."T_TestRunnerParam_id_seq" OWNED BY public."T_TestRunnerParam".id;


--
-- Name: T_Test_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE public."T_Test_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."T_Test_id_seq" OWNER TO "user";

--
-- Name: T_Test_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE public."T_Test_id_seq" OWNED BY public."T_Test".id;


--
-- Name: M_DataType id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."M_DataType" ALTER COLUMN id SET DEFAULT nextval('public."M_DataType_id_seq"'::regclass);


--
-- Name: M_Downloadable_Template id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."M_Downloadable_Template" ALTER COLUMN id SET DEFAULT nextval('public."M_Downloadable_Template_id_seq"'::regclass);


--
-- Name: M_FileSystem id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."M_FileSystem" ALTER COLUMN id SET DEFAULT nextval('public."M_FileSystem_id_seq"'::regclass);


--
-- Name: M_Format id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."M_Format" ALTER COLUMN id SET DEFAULT nextval('public."M_Format_id_seq"'::regclass);


--
-- Name: M_GraphTemplate id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."M_GraphTemplate" ALTER COLUMN id SET DEFAULT nextval('public."M_GraphTemplate_id_seq"'::regclass);


--
-- Name: M_Inventory id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."M_Inventory" ALTER COLUMN id SET DEFAULT nextval('public."M_Inventory_id_seq"'::regclass);


--
-- Name: M_Inventory_Format id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."M_Inventory_Format" ALTER COLUMN id SET DEFAULT nextval('public."M_Inventory_Format_id_seq"'::regclass);


--
-- Name: M_MLComponent id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."M_MLComponent" ALTER COLUMN id SET DEFAULT nextval('public."M_MLComponent_id_seq"'::regclass);


--
-- Name: M_MLFrameworkMapper id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."M_MLFrameworkMapper" ALTER COLUMN id SET DEFAULT nextval('public."M_MLFrameworkMapper_id_seq"'::regclass);


--
-- Name: M_Quality_Dimension id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."M_Quality_Dimension" ALTER COLUMN id SET DEFAULT nextval('public."M_Quality_Dimension_id_seq"'::regclass);


--
-- Name: M_Quality_Measurement id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."M_Quality_Measurement" ALTER COLUMN id SET DEFAULT nextval('public."M_Quality_Measurement_id_seq"'::regclass);


--
-- Name: M_RelationalOperator id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."M_RelationalOperator" ALTER COLUMN id SET DEFAULT nextval('public."M_RelationalOperator_id_seq"'::regclass);


--
-- Name: M_ResourceType id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."M_ResourceType" ALTER COLUMN id SET DEFAULT nextval('public."M_ResourceType_id_seq"'::regclass);


--
-- Name: M_Structure id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."M_Structure" ALTER COLUMN id SET DEFAULT nextval('public."M_Structure_id_seq"'::regclass);


--
-- Name: M_Tag id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."M_Tag" ALTER COLUMN id SET DEFAULT nextval('public."M_Tag_id_seq"'::regclass);


--
-- Name: M_TestInventoryTemplate id_; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."M_TestInventoryTemplate" ALTER COLUMN id_ SET DEFAULT nextval('public."M_TestInventoryTemplate_id__seq"'::regclass);


--
-- Name: M_TestInventoryTemplateTag id_; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."M_TestInventoryTemplateTag" ALTER COLUMN id_ SET DEFAULT nextval('public."M_TestInventoryTemplateTag_id__seq"'::regclass);


--
-- Name: M_TestInventoryTemplate_Format id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."M_TestInventoryTemplate_Format" ALTER COLUMN id SET DEFAULT nextval('public."M_TestInventoryTemplate_Format_id_seq"'::regclass);


--
-- Name: M_TestRunner id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."M_TestRunner" ALTER COLUMN id SET DEFAULT nextval('public."M_TestRunner_id_seq"'::regclass);


--
-- Name: M_TestRunnerParamTemplate id_; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."M_TestRunnerParamTemplate" ALTER COLUMN id_ SET DEFAULT nextval('public."M_TestRunnerParamTemplate_id__seq"'::regclass);


--
-- Name: M_TestRunnerReference id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."M_TestRunnerReference" ALTER COLUMN id SET DEFAULT nextval('public."M_TestRunnerReference_id_seq"'::regclass);


--
-- Name: T_Download id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."T_Download" ALTER COLUMN id SET DEFAULT nextval('public."T_Download_id_seq"'::regclass);


--
-- Name: T_Downloadable_Data id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."T_Downloadable_Data" ALTER COLUMN id SET DEFAULT nextval('public."T_Downloadable_Data_id_seq"'::regclass);


--
-- Name: T_Graph id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."T_Graph" ALTER COLUMN id SET DEFAULT nextval('public."T_Graph_id_seq"'::regclass);


--
-- Name: T_Inventory_TestDescription id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."T_Inventory_TestDescription" ALTER COLUMN id SET DEFAULT nextval('public."T_Inventory_TestDescription_id_seq"'::regclass);


--
-- Name: T_Job id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."T_Job" ALTER COLUMN id SET DEFAULT nextval('public."T_Job_id_seq"'::regclass);


--
-- Name: T_Operand id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."T_Operand" ALTER COLUMN id SET DEFAULT nextval('public."T_Operand_id_seq"'::regclass);


--
-- Name: T_Run id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."T_Run" ALTER COLUMN id SET DEFAULT nextval('public."T_Run_id_seq"'::regclass);


--
-- Name: T_Test id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."T_Test" ALTER COLUMN id SET DEFAULT nextval('public."T_Test_id_seq"'::regclass);


--
-- Name: T_TestDescription id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."T_TestDescription" ALTER COLUMN id SET DEFAULT nextval('public."T_TestDescription_id_seq"'::regclass);


--
-- Name: T_TestRunnerParam id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."T_TestRunnerParam" ALTER COLUMN id SET DEFAULT nextval('public."T_TestRunnerParam_id_seq"'::regclass);


--
-- Name: M_DataType M_DataType_name_key; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."M_DataType"
    ADD CONSTRAINT "M_DataType_name_key" UNIQUE (name);


--
-- Name: M_DataType M_DataType_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."M_DataType"
    ADD CONSTRAINT "M_DataType_pkey" PRIMARY KEY (id);


--
-- Name: M_Downloadable_Template M_Downloadable_Template_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."M_Downloadable_Template"
    ADD CONSTRAINT "M_Downloadable_Template_pkey" PRIMARY KEY (id);


--
-- Name: M_FileSystem M_FileSystem_name_key; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."M_FileSystem"
    ADD CONSTRAINT "M_FileSystem_name_key" UNIQUE (name);


--
-- Name: M_FileSystem M_FileSystem_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."M_FileSystem"
    ADD CONSTRAINT "M_FileSystem_pkey" PRIMARY KEY (id);


--
-- Name: M_Format M_Format_format__key; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."M_Format"
    ADD CONSTRAINT "M_Format_format__key" UNIQUE (format_);


--
-- Name: M_Format M_Format_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."M_Format"
    ADD CONSTRAINT "M_Format_pkey" PRIMARY KEY (id);


--
-- Name: M_GraphTemplate M_GraphTemplate_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."M_GraphTemplate"
    ADD CONSTRAINT "M_GraphTemplate_pkey" PRIMARY KEY (id);


--
-- Name: M_Inventory_Format M_Inventory_Format_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."M_Inventory_Format"
    ADD CONSTRAINT "M_Inventory_Format_pkey" PRIMARY KEY (id);


--
-- Name: M_Inventory M_Inventory_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."M_Inventory"
    ADD CONSTRAINT "M_Inventory_pkey" PRIMARY KEY (id);


--
-- Name: M_MLComponent M_MLComponent_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."M_MLComponent"
    ADD CONSTRAINT "M_MLComponent_pkey" PRIMARY KEY (id);


--
-- Name: M_MLFrameworkMapper M_MLFrameworkMapper_name_key; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."M_MLFrameworkMapper"
    ADD CONSTRAINT "M_MLFrameworkMapper_name_key" UNIQUE (name);


--
-- Name: M_MLFrameworkMapper M_MLFrameworkMapper_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."M_MLFrameworkMapper"
    ADD CONSTRAINT "M_MLFrameworkMapper_pkey" PRIMARY KEY (id);


--
-- Name: M_Organization M_Organization_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."M_Organization"
    ADD CONSTRAINT "M_Organization_pkey" PRIMARY KEY (id);


--
-- Name: M_Quality_Dimension M_Quality_Dimension_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."M_Quality_Dimension"
    ADD CONSTRAINT "M_Quality_Dimension_pkey" PRIMARY KEY (id);


--
-- Name: M_Quality_Measurement M_Quality_Measurement_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."M_Quality_Measurement"
    ADD CONSTRAINT "M_Quality_Measurement_pkey" PRIMARY KEY (id);


--
-- Name: M_RelationalOperator M_RelationalOperator_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."M_RelationalOperator"
    ADD CONSTRAINT "M_RelationalOperator_pkey" PRIMARY KEY (id);


--
-- Name: M_ResourceType M_ResourceType_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."M_ResourceType"
    ADD CONSTRAINT "M_ResourceType_pkey" PRIMARY KEY (id);


--
-- Name: M_Setting M_Setting_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."M_Setting"
    ADD CONSTRAINT "M_Setting_pkey" PRIMARY KEY (key);


--
-- Name: M_Structure M_Structure_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."M_Structure"
    ADD CONSTRAINT "M_Structure_pkey" PRIMARY KEY (id);


--
-- Name: M_Structure M_Structure_structure_key; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."M_Structure"
    ADD CONSTRAINT "M_Structure_structure_key" UNIQUE (structure);


--
-- Name: M_Tag M_Tag_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."M_Tag"
    ADD CONSTRAINT "M_Tag_pkey" PRIMARY KEY (id);


--
-- Name: M_TestInventoryTemplateTag M_TestInventoryTemplateTag_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."M_TestInventoryTemplateTag"
    ADD CONSTRAINT "M_TestInventoryTemplateTag_pkey" PRIMARY KEY (id_);


--
-- Name: M_TestInventoryTemplate_Format M_TestInventoryTemplate_Format_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."M_TestInventoryTemplate_Format"
    ADD CONSTRAINT "M_TestInventoryTemplate_Format_pkey" PRIMARY KEY (id);


--
-- Name: M_TestInventoryTemplate M_TestInventoryTemplate_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."M_TestInventoryTemplate"
    ADD CONSTRAINT "M_TestInventoryTemplate_pkey" PRIMARY KEY (id_);


--
-- Name: M_TestRunnerParamTemplate M_TestRunnerParamTemplate_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."M_TestRunnerParamTemplate"
    ADD CONSTRAINT "M_TestRunnerParamTemplate_pkey" PRIMARY KEY (id_);


--
-- Name: M_TestRunnerReference M_TestRunnerReference_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."M_TestRunnerReference"
    ADD CONSTRAINT "M_TestRunnerReference_pkey" PRIMARY KEY (id);


--
-- Name: M_TestRunner M_TestRunner_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."M_TestRunner"
    ADD CONSTRAINT "M_TestRunner_pkey" PRIMARY KEY (id);


--
-- Name: T_Download T_Download_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."T_Download"
    ADD CONSTRAINT "T_Download_pkey" PRIMARY KEY (id);


--
-- Name: T_Downloadable_Data T_Downloadable_Data_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."T_Downloadable_Data"
    ADD CONSTRAINT "T_Downloadable_Data_pkey" PRIMARY KEY (id);


--
-- Name: T_Graph T_Graph_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."T_Graph"
    ADD CONSTRAINT "T_Graph_pkey" PRIMARY KEY (id);


--
-- Name: T_Inventory_TestDescription T_Inventory_TestDescription_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."T_Inventory_TestDescription"
    ADD CONSTRAINT "T_Inventory_TestDescription_pkey" PRIMARY KEY (id);


--
-- Name: T_Job T_Job_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."T_Job"
    ADD CONSTRAINT "T_Job_pkey" PRIMARY KEY (id);


--
-- Name: T_Operand T_Operand_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."T_Operand"
    ADD CONSTRAINT "T_Operand_pkey" PRIMARY KEY (id);


--
-- Name: T_Run T_Run_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."T_Run"
    ADD CONSTRAINT "T_Run_pkey" PRIMARY KEY (id);


--
-- Name: T_TestDescription T_TestDescription_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."T_TestDescription"
    ADD CONSTRAINT "T_TestDescription_pkey" PRIMARY KEY (id);


--
-- Name: T_TestRunnerParam T_TestRunnerParam_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."T_TestRunnerParam"
    ADD CONSTRAINT "T_TestRunnerParam_pkey" PRIMARY KEY (id);


--
-- Name: T_Test T_Test_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."T_Test"
    ADD CONSTRAINT "T_Test_pkey" PRIMARY KEY (id);


--
-- Name: M_Downloadable_Template M_Downloadable_Template_test_runner_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."M_Downloadable_Template"
    ADD CONSTRAINT "M_Downloadable_Template_test_runner_id_fkey" FOREIGN KEY (test_runner_id) REFERENCES public."M_TestRunner"(id);


--
-- Name: M_Format M_Format_resource_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."M_Format"
    ADD CONSTRAINT "M_Format_resource_type_id_fkey" FOREIGN KEY (resource_type_id) REFERENCES public."M_ResourceType"(id);


--
-- Name: M_GraphTemplate M_GraphTemplate_resource_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."M_GraphTemplate"
    ADD CONSTRAINT "M_GraphTemplate_resource_type_id_fkey" FOREIGN KEY (resource_type_id) REFERENCES public."M_ResourceType"(id);


--
-- Name: M_GraphTemplate M_GraphTemplate_test_runner_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."M_GraphTemplate"
    ADD CONSTRAINT "M_GraphTemplate_test_runner_id_fkey" FOREIGN KEY (test_runner_id) REFERENCES public."M_TestRunner"(id);


--
-- Name: M_Inventory_Format M_Inventory_Format_format_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."M_Inventory_Format"
    ADD CONSTRAINT "M_Inventory_Format_format_id_fkey" FOREIGN KEY (format_id) REFERENCES public."M_Format"(id);


--
-- Name: M_Inventory_Format M_Inventory_Format_inventory_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."M_Inventory_Format"
    ADD CONSTRAINT "M_Inventory_Format_inventory_id_fkey" FOREIGN KEY (inventory_id) REFERENCES public."M_Inventory"(id);


--
-- Name: M_Inventory M_Inventory_file_system_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."M_Inventory"
    ADD CONSTRAINT "M_Inventory_file_system_id_fkey" FOREIGN KEY (file_system_id) REFERENCES public."M_FileSystem"(id);


--
-- Name: M_Inventory M_Inventory_ml_component_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."M_Inventory"
    ADD CONSTRAINT "M_Inventory_ml_component_id_fkey" FOREIGN KEY (ml_component_id) REFERENCES public."M_MLComponent"(id);


--
-- Name: M_Inventory M_Inventory_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."M_Inventory"
    ADD CONSTRAINT "M_Inventory_type_id_fkey" FOREIGN KEY (type_id) REFERENCES public."M_DataType"(id);


--
-- Name: M_MLComponent M_MLComponent_ml_framework_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."M_MLComponent"
    ADD CONSTRAINT "M_MLComponent_ml_framework_id_fkey" FOREIGN KEY (ml_framework_id) REFERENCES public."M_MLFrameworkMapper"(id);


--
-- Name: M_MLComponent M_MLComponent_org_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."M_MLComponent"
    ADD CONSTRAINT "M_MLComponent_org_id_fkey" FOREIGN KEY (org_id) REFERENCES public."M_Organization"(id);


--
-- Name: M_Quality_Measurement M_Quality_Measurement_quality_dimension_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."M_Quality_Measurement"
    ADD CONSTRAINT "M_Quality_Measurement_quality_dimension_id_fkey" FOREIGN KEY (quality_dimension_id) REFERENCES public."M_Quality_Dimension"(id);


--
-- Name: M_Quality_Measurement M_Quality_Measurement_structure_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."M_Quality_Measurement"
    ADD CONSTRAINT "M_Quality_Measurement_structure_id_fkey" FOREIGN KEY (structure_id) REFERENCES public."M_Structure"(id);


--
-- Name: M_Quality_Measurement M_Quality_Measurement_test_runner_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."M_Quality_Measurement"
    ADD CONSTRAINT "M_Quality_Measurement_test_runner_id_fkey" FOREIGN KEY (test_runner_id) REFERENCES public."M_TestRunner"(id);


--
-- Name: M_TestInventoryTemplateTag M_TestInventoryTemplateTag_inventory_template_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."M_TestInventoryTemplateTag"
    ADD CONSTRAINT "M_TestInventoryTemplateTag_inventory_template_id_fkey" FOREIGN KEY (inventory_template_id) REFERENCES public."M_TestInventoryTemplate"(id_);


--
-- Name: M_TestInventoryTemplateTag M_TestInventoryTemplateTag_tag_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."M_TestInventoryTemplateTag"
    ADD CONSTRAINT "M_TestInventoryTemplateTag_tag_id_fkey" FOREIGN KEY (tag_id) REFERENCES public."M_Tag"(id);


--
-- Name: M_TestInventoryTemplate_Format M_TestInventoryTemplate_Format_format_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."M_TestInventoryTemplate_Format"
    ADD CONSTRAINT "M_TestInventoryTemplate_Format_format_id_fkey" FOREIGN KEY (format_id) REFERENCES public."M_Format"(id);


--
-- Name: M_TestInventoryTemplate_Format M_TestInventoryTemplate_Format_inventory_template_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."M_TestInventoryTemplate_Format"
    ADD CONSTRAINT "M_TestInventoryTemplate_Format_inventory_template_id_fkey" FOREIGN KEY (inventory_template_id) REFERENCES public."M_TestInventoryTemplate"(id_);


--
-- Name: M_TestInventoryTemplate M_TestInventoryTemplate_test_runner_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."M_TestInventoryTemplate"
    ADD CONSTRAINT "M_TestInventoryTemplate_test_runner_id_fkey" FOREIGN KEY (test_runner_id) REFERENCES public."M_TestRunner"(id);


--
-- Name: M_TestInventoryTemplate M_TestInventoryTemplate_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."M_TestInventoryTemplate"
    ADD CONSTRAINT "M_TestInventoryTemplate_type_id_fkey" FOREIGN KEY (type_id) REFERENCES public."M_DataType"(id);


--
-- Name: M_TestRunnerParamTemplate M_TestRunnerParamTemplate_test_runner_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."M_TestRunnerParamTemplate"
    ADD CONSTRAINT "M_TestRunnerParamTemplate_test_runner_id_fkey" FOREIGN KEY (test_runner_id) REFERENCES public."M_TestRunner"(id);


--
-- Name: M_TestRunnerReference M_TestRunnerReference_test_runner_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."M_TestRunnerReference"
    ADD CONSTRAINT "M_TestRunnerReference_test_runner_id_fkey" FOREIGN KEY (test_runner_id) REFERENCES public."M_TestRunner"(id);


--
-- Name: T_Downloadable_Data T_Downloadable_Data_download_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."T_Downloadable_Data"
    ADD CONSTRAINT "T_Downloadable_Data_download_id_fkey" FOREIGN KEY (download_id) REFERENCES public."T_Download"(id);


--
-- Name: T_Downloadable_Data T_Downloadable_Data_downloadable_template_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."T_Downloadable_Data"
    ADD CONSTRAINT "T_Downloadable_Data_downloadable_template_id_fkey" FOREIGN KEY (downloadable_template_id) REFERENCES public."M_Downloadable_Template"(id);


--
-- Name: T_Downloadable_Data T_Downloadable_Data_run_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."T_Downloadable_Data"
    ADD CONSTRAINT "T_Downloadable_Data_run_id_fkey" FOREIGN KEY (run_id) REFERENCES public."T_Run"(id);


--
-- Name: T_Graph T_Graph_download_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."T_Graph"
    ADD CONSTRAINT "T_Graph_download_id_fkey" FOREIGN KEY (download_id) REFERENCES public."T_Download"(id);


--
-- Name: T_Graph T_Graph_graph_template_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."T_Graph"
    ADD CONSTRAINT "T_Graph_graph_template_id_fkey" FOREIGN KEY (graph_template_id) REFERENCES public."M_GraphTemplate"(id);


--
-- Name: T_Graph T_Graph_run_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."T_Graph"
    ADD CONSTRAINT "T_Graph_run_id_fkey" FOREIGN KEY (run_id) REFERENCES public."T_Run"(id);


--
-- Name: T_Inventory_TestDescription T_Inventory_TestDescription_inventory_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."T_Inventory_TestDescription"
    ADD CONSTRAINT "T_Inventory_TestDescription_inventory_id_fkey" FOREIGN KEY (inventory_id) REFERENCES public."M_Inventory"(id);


--
-- Name: T_Inventory_TestDescription T_Inventory_TestDescription_template_inventory_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."T_Inventory_TestDescription"
    ADD CONSTRAINT "T_Inventory_TestDescription_template_inventory_id_fkey" FOREIGN KEY (template_inventory_id) REFERENCES public."M_TestInventoryTemplate"(id_);


--
-- Name: T_Inventory_TestDescription T_Inventory_TestDescription_test_description_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."T_Inventory_TestDescription"
    ADD CONSTRAINT "T_Inventory_TestDescription_test_description_id_fkey" FOREIGN KEY (test_description_id) REFERENCES public."T_TestDescription"(id);


--
-- Name: T_Operand T_Operand_quality_measurement_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."T_Operand"
    ADD CONSTRAINT "T_Operand_quality_measurement_id_fkey" FOREIGN KEY (quality_measurement_id) REFERENCES public."M_Quality_Measurement"(id);


--
-- Name: T_Operand T_Operand_relational_operator_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."T_Operand"
    ADD CONSTRAINT "T_Operand_relational_operator_id_fkey" FOREIGN KEY (relational_operator_id) REFERENCES public."M_RelationalOperator"(id);


--
-- Name: T_Operand T_Operand_test_description_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."T_Operand"
    ADD CONSTRAINT "T_Operand_test_description_id_fkey" FOREIGN KEY (test_description_id) REFERENCES public."T_TestDescription"(id);


--
-- Name: T_Run T_Run_job_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."T_Run"
    ADD CONSTRAINT "T_Run_job_id_fkey" FOREIGN KEY (job_id) REFERENCES public."T_Job"(id);


--
-- Name: T_TestDescription T_TestDescription_parent_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."T_TestDescription"
    ADD CONSTRAINT "T_TestDescription_parent_id_fkey" FOREIGN KEY (parent_id) REFERENCES public."T_TestDescription"(id);


--
-- Name: T_TestDescription T_TestDescription_quality_dimension_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."T_TestDescription"
    ADD CONSTRAINT "T_TestDescription_quality_dimension_id_fkey" FOREIGN KEY (quality_dimension_id) REFERENCES public."M_Quality_Dimension"(id);


--
-- Name: T_TestDescription T_TestDescription_run_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."T_TestDescription"
    ADD CONSTRAINT "T_TestDescription_run_id_fkey" FOREIGN KEY (run_id) REFERENCES public."T_Run"(id);


--
-- Name: T_TestDescription T_TestDescription_test_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."T_TestDescription"
    ADD CONSTRAINT "T_TestDescription_test_id_fkey" FOREIGN KEY (test_id) REFERENCES public."T_Test"(id);


--
-- Name: T_TestDescription T_TestDescription_test_runner_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."T_TestDescription"
    ADD CONSTRAINT "T_TestDescription_test_runner_id_fkey" FOREIGN KEY (test_runner_id) REFERENCES public."M_TestRunner"(id);


--
-- Name: T_TestRunnerParam T_TestRunnerParam_test_description_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."T_TestRunnerParam"
    ADD CONSTRAINT "T_TestRunnerParam_test_description_id_fkey" FOREIGN KEY (test_description_id) REFERENCES public."T_TestDescription"(id);


--
-- Name: T_TestRunnerParam T_TestRunnerParam_test_runner_param_template_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."T_TestRunnerParam"
    ADD CONSTRAINT "T_TestRunnerParam_test_runner_param_template_id_fkey" FOREIGN KEY (test_runner_param_template_id) REFERENCES public."M_TestRunnerParamTemplate"(id_);


--
-- Name: T_Test T_Test_job_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."T_Test"
    ADD CONSTRAINT "T_Test_job_id_fkey" FOREIGN KEY (job_id) REFERENCES public."T_Job"(id);


--
-- Name: T_Test T_Test_ml_component_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public."T_Test"
    ADD CONSTRAINT "T_Test_ml_component_id_fkey" FOREIGN KEY (ml_component_id) REFERENCES public."M_MLComponent"(id);


--
-- PostgreSQL database dump complete
--

