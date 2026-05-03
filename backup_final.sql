--
-- PostgreSQL database dump
--

\restrict Mk7WsHXKYMWTclRUKXgH1WjbHPqvclIfgpfcruIfYf3iFrWGFHbgX5xEyBgPfvT

-- Dumped from database version 17.9
-- Dumped by pg_dump version 17.9

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: tenant_1; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA tenant_1;


ALTER SCHEMA tenant_1 OWNER TO postgres;

--
-- Name: appstatus; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.appstatus AS ENUM (
    'PENDING',
    'APPROVED',
    'REJECTED'
);


ALTER TYPE public.appstatus OWNER TO postgres;

--
-- Name: notetype; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.notetype AS ENUM (
    'VEHICLE',
    'ENGINEERING',
    'LABOR',
    'OTHER',
    'MEMO'
);


ALTER TYPE public.notetype OWNER TO postgres;

--
-- Name: taskstatus; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.taskstatus AS ENUM (
    'PENDING',
    'ASSIGNED',
    'IN_PROGRESS',
    'COMPLETED',
    'CANCELLED'
);


ALTER TYPE public.taskstatus OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO postgres;

--
-- Name: policies; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.policies (
    id integer NOT NULL,
    title character varying NOT NULL,
    content text,
    category character varying,
    published_at timestamp with time zone,
    created_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.policies OWNER TO postgres;

--
-- Name: policies_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.policies_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.policies_id_seq OWNER TO postgres;

--
-- Name: policies_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.policies_id_seq OWNED BY public.policies.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying NOT NULL,
    hashed_password character varying NOT NULL,
    full_name character varying,
    role character varying,
    village_id integer NOT NULL,
    created_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: applications; Type: TABLE; Schema: tenant_1; Owner: postgres
--

CREATE TABLE tenant_1.applications (
    id integer NOT NULL,
    user_id integer,
    type character varying(50) NOT NULL,
    content text NOT NULL,
    status character varying(20) DEFAULT 'pending'::character varying,
    admin_reply text,
    created_at timestamp without time zone DEFAULT now(),
    CONSTRAINT applications_status_check CHECK (((status)::text = ANY ((ARRAY['pending'::character varying, 'approved'::character varying, 'rejected'::character varying])::text[])))
);


ALTER TABLE tenant_1.applications OWNER TO postgres;

--
-- Name: applications_id_seq; Type: SEQUENCE; Schema: tenant_1; Owner: postgres
--

CREATE SEQUENCE tenant_1.applications_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE tenant_1.applications_id_seq OWNER TO postgres;

--
-- Name: applications_id_seq; Type: SEQUENCE OWNED BY; Schema: tenant_1; Owner: postgres
--

ALTER SEQUENCE tenant_1.applications_id_seq OWNED BY tenant_1.applications.id;


--
-- Name: consultations; Type: TABLE; Schema: tenant_1; Owner: postgres
--

CREATE TABLE tenant_1.consultations (
    id integer NOT NULL,
    user_id integer,
    question text NOT NULL,
    answer text,
    status character varying(20) DEFAULT 'pending'::character varying,
    created_at timestamp without time zone DEFAULT now(),
    CONSTRAINT consultations_status_check CHECK (((status)::text = ANY (ARRAY[('pending'::character varying)::text, ('answered'::character varying)::text])))
);


ALTER TABLE tenant_1.consultations OWNER TO postgres;

--
-- Name: consultations_id_seq; Type: SEQUENCE; Schema: tenant_1; Owner: postgres
--

CREATE SEQUENCE tenant_1.consultations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE tenant_1.consultations_id_seq OWNER TO postgres;

--
-- Name: consultations_id_seq; Type: SEQUENCE OWNED BY; Schema: tenant_1; Owner: postgres
--

ALTER SEQUENCE tenant_1.consultations_id_seq OWNED BY tenant_1.consultations.id;


--
-- Name: guides; Type: TABLE; Schema: tenant_1; Owner: postgres
--

CREATE TABLE tenant_1.guides (
    id integer NOT NULL,
    title character varying(200) NOT NULL,
    content text NOT NULL,
    "order" integer DEFAULT 0,
    created_at timestamp without time zone DEFAULT now()
);


ALTER TABLE tenant_1.guides OWNER TO postgres;

--
-- Name: guides_id_seq; Type: SEQUENCE; Schema: tenant_1; Owner: postgres
--

CREATE SEQUENCE tenant_1.guides_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE tenant_1.guides_id_seq OWNER TO postgres;

--
-- Name: guides_id_seq; Type: SEQUENCE OWNED BY; Schema: tenant_1; Owner: postgres
--

ALTER SEQUENCE tenant_1.guides_id_seq OWNED BY tenant_1.guides.id;


--
-- Name: memorials; Type: TABLE; Schema: tenant_1; Owner: postgres
--

CREATE TABLE tenant_1.memorials (
    id integer NOT NULL,
    title character varying(200) NOT NULL,
    content text NOT NULL,
    happened_at timestamp without time zone,
    images jsonb DEFAULT '[]'::jsonb,
    created_at timestamp without time zone DEFAULT now()
);


ALTER TABLE tenant_1.memorials OWNER TO postgres;

--
-- Name: memorials_id_seq; Type: SEQUENCE; Schema: tenant_1; Owner: postgres
--

CREATE SEQUENCE tenant_1.memorials_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE tenant_1.memorials_id_seq OWNER TO postgres;

--
-- Name: memorials_id_seq; Type: SEQUENCE OWNED BY; Schema: tenant_1; Owner: postgres
--

ALTER SEQUENCE tenant_1.memorials_id_seq OWNED BY tenant_1.memorials.id;


--
-- Name: notices; Type: TABLE; Schema: tenant_1; Owner: postgres
--

CREATE TABLE tenant_1.notices (
    id integer NOT NULL,
    title character varying(200) NOT NULL,
    content text NOT NULL,
    is_top boolean DEFAULT false,
    published_at timestamp without time zone DEFAULT now(),
    created_at timestamp without time zone DEFAULT now()
);


ALTER TABLE tenant_1.notices OWNER TO postgres;

--
-- Name: notices_id_seq; Type: SEQUENCE; Schema: tenant_1; Owner: postgres
--

CREATE SEQUENCE tenant_1.notices_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE tenant_1.notices_id_seq OWNER TO postgres;

--
-- Name: notices_id_seq; Type: SEQUENCE OWNED BY; Schema: tenant_1; Owner: postgres
--

ALTER SEQUENCE tenant_1.notices_id_seq OWNED BY tenant_1.notices.id;


--
-- Name: policies; Type: TABLE; Schema: tenant_1; Owner: postgres
--

CREATE TABLE tenant_1.policies (
    id integer NOT NULL,
    title character varying(200) NOT NULL,
    content text NOT NULL,
    category character varying(100),
    published_at timestamp without time zone DEFAULT now(),
    created_at timestamp without time zone DEFAULT now()
);


ALTER TABLE tenant_1.policies OWNER TO postgres;

--
-- Name: policies_id_seq; Type: SEQUENCE; Schema: tenant_1; Owner: postgres
--

CREATE SEQUENCE tenant_1.policies_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE tenant_1.policies_id_seq OWNER TO postgres;

--
-- Name: policies_id_seq; Type: SEQUENCE OWNED BY; Schema: tenant_1; Owner: postgres
--

ALTER SEQUENCE tenant_1.policies_id_seq OWNED BY tenant_1.policies.id;


--
-- Name: task_assignments; Type: TABLE; Schema: tenant_1; Owner: postgres
--

CREATE TABLE tenant_1.task_assignments (
    id integer NOT NULL,
    task_id integer NOT NULL,
    user_id integer NOT NULL,
    status character varying(20) DEFAULT 'pending'::character varying NOT NULL,
    feedback text,
    assigned_at timestamp with time zone DEFAULT now(),
    started_at timestamp with time zone,
    completed_at timestamp with time zone,
    updated_at timestamp with time zone DEFAULT now()
);


ALTER TABLE tenant_1.task_assignments OWNER TO postgres;

--
-- Name: task_assignments_id_seq; Type: SEQUENCE; Schema: tenant_1; Owner: postgres
--

CREATE SEQUENCE tenant_1.task_assignments_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE tenant_1.task_assignments_id_seq OWNER TO postgres;

--
-- Name: task_assignments_id_seq; Type: SEQUENCE OWNED BY; Schema: tenant_1; Owner: postgres
--

ALTER SEQUENCE tenant_1.task_assignments_id_seq OWNED BY tenant_1.task_assignments.id;


--
-- Name: task_attachments; Type: TABLE; Schema: tenant_1; Owner: postgres
--

CREATE TABLE tenant_1.task_attachments (
    id integer NOT NULL,
    task_id integer NOT NULL,
    filename character varying(255) NOT NULL,
    file_path character varying(500) NOT NULL,
    file_size integer,
    mime_type character varying(100),
    uploaded_by integer,
    created_at timestamp with time zone DEFAULT now()
);


ALTER TABLE tenant_1.task_attachments OWNER TO postgres;

--
-- Name: task_attachments_id_seq; Type: SEQUENCE; Schema: tenant_1; Owner: postgres
--

CREATE SEQUENCE tenant_1.task_attachments_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE tenant_1.task_attachments_id_seq OWNER TO postgres;

--
-- Name: task_attachments_id_seq; Type: SEQUENCE OWNED BY; Schema: tenant_1; Owner: postgres
--

ALTER SEQUENCE tenant_1.task_attachments_id_seq OWNED BY tenant_1.task_attachments.id;


--
-- Name: tasks; Type: TABLE; Schema: tenant_1; Owner: postgres
--

CREATE TABLE tenant_1.tasks (
    id integer NOT NULL,
    title character varying NOT NULL,
    description text,
    priority character varying(20) DEFAULT 'medium'::character varying,
    due_date character varying(50),
    extra_data jsonb DEFAULT '{}'::jsonb,
    status character varying(20) DEFAULT 'pending'::character varying,
    creator_id integer NOT NULL,
    created_at timestamp with time zone DEFAULT now(),
    assigned_by_id integer,
    assigned_at timestamp with time zone,
    started_at timestamp with time zone,
    completed_at timestamp with time zone,
    result_note text,
    assignee_ids json DEFAULT '[]'::json
);


ALTER TABLE tenant_1.tasks OWNER TO postgres;

--
-- Name: tasks_id_seq; Type: SEQUENCE; Schema: tenant_1; Owner: postgres
--

CREATE SEQUENCE tenant_1.tasks_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE tenant_1.tasks_id_seq OWNER TO postgres;

--
-- Name: tasks_id_seq; Type: SEQUENCE OWNED BY; Schema: tenant_1; Owner: postgres
--

ALTER SEQUENCE tenant_1.tasks_id_seq OWNED BY tenant_1.tasks.id;


--
-- Name: users; Type: TABLE; Schema: tenant_1; Owner: postgres
--

CREATE TABLE tenant_1.users (
    id integer NOT NULL,
    username character varying NOT NULL,
    hashed_password character varying NOT NULL,
    full_name character varying,
    role character varying,
    village_id integer NOT NULL,
    created_at timestamp with time zone DEFAULT now(),
    real_name character varying(50),
    phone character varying(20),
    is_active boolean DEFAULT true
);


ALTER TABLE tenant_1.users OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: tenant_1; Owner: postgres
--

CREATE SEQUENCE tenant_1.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE tenant_1.users_id_seq OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: tenant_1; Owner: postgres
--

ALTER SEQUENCE tenant_1.users_id_seq OWNED BY tenant_1.users.id;


--
-- Name: work_notes; Type: TABLE; Schema: tenant_1; Owner: postgres
--

CREATE TABLE tenant_1.work_notes (
    id integer NOT NULL,
    type character varying(50) NOT NULL,
    title character varying NOT NULL,
    content text,
    user_id integer NOT NULL,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone
);


ALTER TABLE tenant_1.work_notes OWNER TO postgres;

--
-- Name: work_notes_id_seq; Type: SEQUENCE; Schema: tenant_1; Owner: postgres
--

CREATE SEQUENCE tenant_1.work_notes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE tenant_1.work_notes_id_seq OWNER TO postgres;

--
-- Name: work_notes_id_seq; Type: SEQUENCE OWNED BY; Schema: tenant_1; Owner: postgres
--

ALTER SEQUENCE tenant_1.work_notes_id_seq OWNED BY tenant_1.work_notes.id;


--
-- Name: policies id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.policies ALTER COLUMN id SET DEFAULT nextval('public.policies_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Name: applications id; Type: DEFAULT; Schema: tenant_1; Owner: postgres
--

ALTER TABLE ONLY tenant_1.applications ALTER COLUMN id SET DEFAULT nextval('tenant_1.applications_id_seq'::regclass);


--
-- Name: consultations id; Type: DEFAULT; Schema: tenant_1; Owner: postgres
--

ALTER TABLE ONLY tenant_1.consultations ALTER COLUMN id SET DEFAULT nextval('tenant_1.consultations_id_seq'::regclass);


--
-- Name: guides id; Type: DEFAULT; Schema: tenant_1; Owner: postgres
--

ALTER TABLE ONLY tenant_1.guides ALTER COLUMN id SET DEFAULT nextval('tenant_1.guides_id_seq'::regclass);


--
-- Name: memorials id; Type: DEFAULT; Schema: tenant_1; Owner: postgres
--

ALTER TABLE ONLY tenant_1.memorials ALTER COLUMN id SET DEFAULT nextval('tenant_1.memorials_id_seq'::regclass);


--
-- Name: notices id; Type: DEFAULT; Schema: tenant_1; Owner: postgres
--

ALTER TABLE ONLY tenant_1.notices ALTER COLUMN id SET DEFAULT nextval('tenant_1.notices_id_seq'::regclass);


--
-- Name: policies id; Type: DEFAULT; Schema: tenant_1; Owner: postgres
--

ALTER TABLE ONLY tenant_1.policies ALTER COLUMN id SET DEFAULT nextval('tenant_1.policies_id_seq'::regclass);


--
-- Name: task_assignments id; Type: DEFAULT; Schema: tenant_1; Owner: postgres
--

ALTER TABLE ONLY tenant_1.task_assignments ALTER COLUMN id SET DEFAULT nextval('tenant_1.task_assignments_id_seq'::regclass);


--
-- Name: task_attachments id; Type: DEFAULT; Schema: tenant_1; Owner: postgres
--

ALTER TABLE ONLY tenant_1.task_attachments ALTER COLUMN id SET DEFAULT nextval('tenant_1.task_attachments_id_seq'::regclass);


--
-- Name: tasks id; Type: DEFAULT; Schema: tenant_1; Owner: postgres
--

ALTER TABLE ONLY tenant_1.tasks ALTER COLUMN id SET DEFAULT nextval('tenant_1.tasks_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: tenant_1; Owner: postgres
--

ALTER TABLE ONLY tenant_1.users ALTER COLUMN id SET DEFAULT nextval('tenant_1.users_id_seq'::regclass);


--
-- Name: work_notes id; Type: DEFAULT; Schema: tenant_1; Owner: postgres
--

ALTER TABLE ONLY tenant_1.work_notes ALTER COLUMN id SET DEFAULT nextval('tenant_1.work_notes_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.alembic_version (version_num) FROM stdin;
c82f19a6beba
\.


--
-- Data for Name: policies; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.policies (id, title, content, category, published_at, created_at) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, username, hashed_password, full_name, role, village_id, created_at) FROM stdin;
\.


--
-- Data for Name: applications; Type: TABLE DATA; Schema: tenant_1; Owner: postgres
--

COPY tenant_1.applications (id, user_id, type, content, status, admin_reply, created_at) FROM stdin;
1	1	subsidy	2	pending	\N	2026-05-02 08:05:36.229185
2	1	building	2	pending	\N	2026-05-02 08:05:44.684021
4	1	other	2	rejected	2	2026-05-02 08:05:57.26808
3	1	employment	2	approved		2026-05-02 08:05:50.924885
\.


--
-- Data for Name: consultations; Type: TABLE DATA; Schema: tenant_1; Owner: postgres
--

COPY tenant_1.consultations (id, user_id, question, answer, status, created_at) FROM stdin;
1	1	f	d	answered	2026-05-02 07:49:53.87813
\.


--
-- Data for Name: guides; Type: TABLE DATA; Schema: tenant_1; Owner: postgres
--

COPY tenant_1.guides (id, title, content, "order", created_at) FROM stdin;
3	服务指南	服务指南	0	2026-05-01 10:19:50.054603
\.


--
-- Data for Name: memorials; Type: TABLE DATA; Schema: tenant_1; Owner: postgres
--

COPY tenant_1.memorials (id, title, content, happened_at, images, created_at) FROM stdin;
8	人居环境整治与美丽乡村建设	近年来，北荡村坚持生态优先、绿色发展，全面推进农村人居环境整治提升行动，打造“水清、岸绿、路净、村美”的水乡风貌。系统治理黑臭水体，修建污水管网9220米、污水处理站3座，实现生活污水集中处理、达标排放。全面推行河长制、湖长制、林长制，加强高邮湖岸线保护，清理乱搭乱建、乱堆乱放、乱采乱挖，修复湿地生态，守护碧水蓝天。实施道路硬化、村庄绿化、庭院美化、路灯亮化工程，新建、改扩建村组道路，修建排灌干渠，改造老旧房屋，建设休闲广场、文化活动中心、村级卫生室，公共服务设施不断完善。依托高邮湖生态资源，联动周边村庄发展乡村旅游，打造采摘园、垂钓点、农家乐，吸引城市游客前来观光休闲，拓宽增收渠道。通过持续整治与建设，北荡村村容村貌焕然一新，生态环境明显改善，群众幸福感、获得感显著提升，先后获评市级文明村、人居环境整治示范村，成为水乡大地上宜居宜业宜游的美丽乡村样板。	2021-01-01 17:22:01	[]	2026-05-01 09:27:08.657676
6	渔民上岸安置与就业帮扶	北荡村是传统渔业村，世代渔民以船为家、以渔为生，生产生活条件艰苦，抗风险能力弱。2019年起，按照上级渔民上岸安居工程部署，北荡村全面推进渔民转产转业、集中安置工作，高标准建设渔民新村，配套住房、教育、医疗、养老等公共服务设施，让世代水上人家实现“陆上安家、稳定生活”梦想。针对上岸渔民普遍存在的就业难、收入不稳问题，村里同步建设绒毛玩具扶贫车间，就近吸纳渔民就业，实现“家门口上班、顾家增收两不误”。推行劳务经纪人制度，党员干部带头逐户走访、宣讲政策、对接岗位，累计帮助56名上岸渔民实现稳定就业。对困难家庭、重病家庭、单亲家庭精准帮扶，落实低保、医保、助学、助残等政策，解决后顾之忧。通过安居、就业、帮扶三位一体推进，上岸渔民实现“搬得出、稳得住、能致富”，生产生活面貌发生根本性改变。	2019-05-01 17:22:01	[]	2026-05-01 09:25:15.334555
5	年芡实产业崛起与合作社发展	北荡村地处高邮湖西岸，河网密布、水土丰沃，历史上以传统种植、零散养殖为主，经济效益偏低。2018年起，村“两委”立足水乡资源禀赋，把芡实产业作为富民强村主导产业，大力推进土地流转，引导农户以土地入股、劳务务工等方式加入合作社。成立天长市千秋芡实经济专业合作社，统一品种、统一技术、统一收购、统一销售，规模化发展芡实种植，累计承包河湖滩涂及水田32300亩，形成连片化、标准化种植基地。同步完善基础设施，修建“四好农村路”，水泥路直通田头水边，彻底改变“人挑肩扛、运输困难”历史，解决芡实采收、运输、销售“最后一公里”难题。芡实产业带动全村脱贫户及普通农户稳定增收，户均年收入增加2—3万元，小小芡实成为名副其实的“金豆豆”，北荡村也成为远近闻名的芡实专业村、产业致富村。	2018-01-01 17:22:01	[]	2026-05-01 09:24:04.646187
7	村“两委”换届与治理体系重塑	2021年底，北荡村举行党组织换届选举，一批有担当、有能力、群众信任的村干部进入村“两委”班子，为村级发展注入新鲜血液。新班子上任后，坚持党建引领、民主治村、阳光村务，从整顿作风、规范制度、理清账目入手，全面加强基层治理。严格执行“四议两公开”制度，每月定期召开村务监督例会，及时公开村务、财务、资产资源及重大事项，保障村民知情权、参与权、监督权。深入开展“我为群众办实事”，聚焦群众急难愁盼，解决道路破损、灌溉不畅、环境脏乱、邻里矛盾等一批历史遗留问题，干群关系显著改善，凝聚力、向心力明显增强。以党建促产业、以治理保发展，先后成立渔业养殖、芡实种植、果蔬种植三大专业合作社，发展特色种养9600多亩，推动北荡村从“薄弱村”向“产业强村”跨越。此次换届成为北荡村发展转折点，为乡村振兴注入强劲组织动力。	2021-09-01 17:22:01	[]	2026-05-01 09:26:34.212408
9	高邮湖退养还湖生态保护行动	2026 年，北荡村坚决贯彻上级关于高邮湖生态保护与高质量发展部署，全面推进退养还湖、生态修复专项行动，筑牢高邮湖西岸生态屏障。按照统一规划，对辖区内高邮湖水域围网养殖、圈圩养殖进行有序清退，逐户开展政策宣讲、调查摸底、协议签订，做好养殖设施拆除、水面恢复、生态修复等工作，累计完成退养面积数千亩，恢复湖泊自然水面，提升行洪调蓄能力，同步实施岸线整治、湿地修复、水生植物种植等工程，加强水质监测与日常管护，严厉打击非法捕捞、违规排污等行为，推动湖区水质持续改善，生物多样性逐步恢复。坚持退养不退民、转产能致富，统筹推进渔民转产就业、技能培训、社会保障等工作，引导群众向特色种植、乡村旅游、劳务输出等产业转型，实现生态保护与民生保障双赢。此次退养还湖行动，标志着北荡村从 “靠湖吃湖” 向 “护湖养湖” 转变，为水乡绿色低碳发展和乡村全面振兴奠定坚实生态基础。	2026-01-01 17:22:01	[]	2026-05-01 09:27:51.582915
4	“三资”改革与集体资产盘活	2017年，北荡村集体资产长期闲置、资源利用低效、村务管理不透明等问题突出，制约集体经济发展。为破解发展瓶颈，村“两委”在市、镇纪委和“三资办”指导下，全面开展集体资产清产核资，建立台账、厘清账目、公开公示，彻底扭转“家底不清、账实不符”局面。同年7月，张行林场52亩老旧林木通过农村产权交易平台公开竞价，底价14.68万元，经28次线上竞价，最终以16.8万元成交，比私下交易高出10.8万元。随后，废旧林地整理后对外发包，一次性收取20年租金28万元；外圩300亩滩涂水面及老村部、旧校舍等资产陆续挂牌租赁，年增收17.6万元。通过规范交易、阳光操作，沉睡资源转化为稳定收益，村级集体经济实现突破性增长，为后续产业发展、基础设施建设和民生改善奠定坚实基础。	2017-01-01 00:00:00	[]	2026-05-01 09:23:20.039654
\.


--
-- Data for Name: notices; Type: TABLE DATA; Schema: tenant_1; Owner: postgres
--

COPY tenant_1.notices (id, title, content, is_top, published_at, created_at) FROM stdin;
2	通知	通知	f	2026-05-01 10:03:11.794929	2026-05-01 10:03:11.794929
\.


--
-- Data for Name: policies; Type: TABLE DATA; Schema: tenant_1; Owner: postgres
--

COPY tenant_1.policies (id, title, content, category, published_at, created_at) FROM stdin;
2	政务公开	政务公开	政务公开	2026-05-01 08:35:40.47947	2026-05-01 08:35:40.47947
\.


--
-- Data for Name: task_assignments; Type: TABLE DATA; Schema: tenant_1; Owner: postgres
--

COPY tenant_1.task_assignments (id, task_id, user_id, status, feedback, assigned_at, started_at, completed_at, updated_at) FROM stdin;
\.


--
-- Data for Name: task_attachments; Type: TABLE DATA; Schema: tenant_1; Owner: postgres
--

COPY tenant_1.task_attachments (id, task_id, filename, file_path, file_size, mime_type, uploaded_by, created_at) FROM stdin;
\.


--
-- Data for Name: tasks; Type: TABLE DATA; Schema: tenant_1; Owner: postgres
--

COPY tenant_1.tasks (id, title, description, priority, due_date, extra_data, status, creator_id, created_at, assigned_by_id, assigned_at, started_at, completed_at, result_note, assignee_ids) FROM stdin;
15	ss	s's	medium	2015-12-31T16:00:00.000Z	{"assignee_ids": [2]}	pending	1	2026-05-01 08:31:38.20166+00	\N	\N	\N	\N	\N	[]
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: tenant_1; Owner: postgres
--

COPY tenant_1.users (id, username, hashed_password, full_name, role, village_id, created_at, real_name, phone, is_active) FROM stdin;
3	yyl	$2b$12$QkhUZTjFNh8pRDWcnODzcObhshBpPA.bIR3zAq0soMt.r0X1ejAai	杨玉良	staff	1	2026-04-27 09:24:26.753872+00		\N	t
2	zlb	$2b$12$W3IRXYPpmVL/zKXVs92neOxHxlCJqz/Bq.iMlGGdTNW2irwXTu6vm	周连兵	staff	1	2026-04-25 01:50:53.355235+00		\N	t
1	admin	$2b$12$P3yad./JSbW2Ver6oT0t9.yB/lxrWuYCTcW8tmdnr.sB7GXmXn8nu	系统管理员	admin	1	2026-04-24 08:12:44.437456+00		\N	t
7	m	$2b$12$J.OdCaLs..xNaquhGa6Ij.VX1Jdpf4o5Ab1xZz9vGdj0rORjar9Te	\N	villager	1	2026-05-01 10:48:52.072379+00	m	\N	t
10	mm	$2b$12$vQu85kY7cgGkC3nq9Y/BLeyiONsYCbSv0Hnftt/LNeWj8/C.s7Wgy	\N	villager	1	2026-05-02 07:32:05.697267+00	mm	\N	t
\.


--
-- Data for Name: work_notes; Type: TABLE DATA; Schema: tenant_1; Owner: postgres
--

COPY tenant_1.work_notes (id, type, title, content, user_id, created_at, updated_at) FROM stdin;
\.


--
-- Name: policies_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.policies_id_seq', 1, false);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 1, false);


--
-- Name: applications_id_seq; Type: SEQUENCE SET; Schema: tenant_1; Owner: postgres
--

SELECT pg_catalog.setval('tenant_1.applications_id_seq', 4, true);


--
-- Name: consultations_id_seq; Type: SEQUENCE SET; Schema: tenant_1; Owner: postgres
--

SELECT pg_catalog.setval('tenant_1.consultations_id_seq', 1, true);


--
-- Name: guides_id_seq; Type: SEQUENCE SET; Schema: tenant_1; Owner: postgres
--

SELECT pg_catalog.setval('tenant_1.guides_id_seq', 3, true);


--
-- Name: memorials_id_seq; Type: SEQUENCE SET; Schema: tenant_1; Owner: postgres
--

SELECT pg_catalog.setval('tenant_1.memorials_id_seq', 9, true);


--
-- Name: notices_id_seq; Type: SEQUENCE SET; Schema: tenant_1; Owner: postgres
--

SELECT pg_catalog.setval('tenant_1.notices_id_seq', 2, true);


--
-- Name: policies_id_seq; Type: SEQUENCE SET; Schema: tenant_1; Owner: postgres
--

SELECT pg_catalog.setval('tenant_1.policies_id_seq', 2, true);


--
-- Name: task_assignments_id_seq; Type: SEQUENCE SET; Schema: tenant_1; Owner: postgres
--

SELECT pg_catalog.setval('tenant_1.task_assignments_id_seq', 1, true);


--
-- Name: task_attachments_id_seq; Type: SEQUENCE SET; Schema: tenant_1; Owner: postgres
--

SELECT pg_catalog.setval('tenant_1.task_attachments_id_seq', 1, false);


--
-- Name: tasks_id_seq; Type: SEQUENCE SET; Schema: tenant_1; Owner: postgres
--

SELECT pg_catalog.setval('tenant_1.tasks_id_seq', 15, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: tenant_1; Owner: postgres
--

SELECT pg_catalog.setval('tenant_1.users_id_seq', 10, true);


--
-- Name: work_notes_id_seq; Type: SEQUENCE SET; Schema: tenant_1; Owner: postgres
--

SELECT pg_catalog.setval('tenant_1.work_notes_id_seq', 5, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: policies policies_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.policies
    ADD CONSTRAINT policies_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: applications applications_pkey; Type: CONSTRAINT; Schema: tenant_1; Owner: postgres
--

ALTER TABLE ONLY tenant_1.applications
    ADD CONSTRAINT applications_pkey PRIMARY KEY (id);


--
-- Name: consultations consultations_pkey; Type: CONSTRAINT; Schema: tenant_1; Owner: postgres
--

ALTER TABLE ONLY tenant_1.consultations
    ADD CONSTRAINT consultations_pkey PRIMARY KEY (id);


--
-- Name: guides guides_pkey; Type: CONSTRAINT; Schema: tenant_1; Owner: postgres
--

ALTER TABLE ONLY tenant_1.guides
    ADD CONSTRAINT guides_pkey PRIMARY KEY (id);


--
-- Name: memorials memorials_pkey; Type: CONSTRAINT; Schema: tenant_1; Owner: postgres
--

ALTER TABLE ONLY tenant_1.memorials
    ADD CONSTRAINT memorials_pkey PRIMARY KEY (id);


--
-- Name: notices notices_pkey; Type: CONSTRAINT; Schema: tenant_1; Owner: postgres
--

ALTER TABLE ONLY tenant_1.notices
    ADD CONSTRAINT notices_pkey PRIMARY KEY (id);


--
-- Name: policies policies_pkey; Type: CONSTRAINT; Schema: tenant_1; Owner: postgres
--

ALTER TABLE ONLY tenant_1.policies
    ADD CONSTRAINT policies_pkey PRIMARY KEY (id);


--
-- Name: task_assignments task_assignments_pkey; Type: CONSTRAINT; Schema: tenant_1; Owner: postgres
--

ALTER TABLE ONLY tenant_1.task_assignments
    ADD CONSTRAINT task_assignments_pkey PRIMARY KEY (id);


--
-- Name: task_attachments task_attachments_pkey; Type: CONSTRAINT; Schema: tenant_1; Owner: postgres
--

ALTER TABLE ONLY tenant_1.task_attachments
    ADD CONSTRAINT task_attachments_pkey PRIMARY KEY (id);


--
-- Name: tasks tasks_pkey; Type: CONSTRAINT; Schema: tenant_1; Owner: postgres
--

ALTER TABLE ONLY tenant_1.tasks
    ADD CONSTRAINT tasks_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: tenant_1; Owner: postgres
--

ALTER TABLE ONLY tenant_1.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: work_notes work_notes_pkey; Type: CONSTRAINT; Schema: tenant_1; Owner: postgres
--

ALTER TABLE ONLY tenant_1.work_notes
    ADD CONSTRAINT work_notes_pkey PRIMARY KEY (id);


--
-- Name: ix_policies_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_policies_id ON public.policies USING btree (id);


--
-- Name: ix_users_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_users_id ON public.users USING btree (id);


--
-- Name: ix_users_username; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_users_username ON public.users USING btree (username);


--
-- Name: idx_applications_status; Type: INDEX; Schema: tenant_1; Owner: postgres
--

CREATE INDEX idx_applications_status ON tenant_1.applications USING btree (status);


--
-- Name: idx_applications_user_id; Type: INDEX; Schema: tenant_1; Owner: postgres
--

CREATE INDEX idx_applications_user_id ON tenant_1.applications USING btree (user_id);


--
-- Name: idx_consultations_status; Type: INDEX; Schema: tenant_1; Owner: postgres
--

CREATE INDEX idx_consultations_status ON tenant_1.consultations USING btree (status);


--
-- Name: idx_consultations_user_id; Type: INDEX; Schema: tenant_1; Owner: postgres
--

CREATE INDEX idx_consultations_user_id ON tenant_1.consultations USING btree (user_id);


--
-- Name: idx_memorials_happened_at; Type: INDEX; Schema: tenant_1; Owner: postgres
--

CREATE INDEX idx_memorials_happened_at ON tenant_1.memorials USING btree (happened_at);


--
-- Name: idx_notices_is_top; Type: INDEX; Schema: tenant_1; Owner: postgres
--

CREATE INDEX idx_notices_is_top ON tenant_1.notices USING btree (is_top);


--
-- Name: idx_task_assignments_task; Type: INDEX; Schema: tenant_1; Owner: postgres
--

CREATE INDEX idx_task_assignments_task ON tenant_1.task_assignments USING btree (task_id);


--
-- Name: idx_task_assignments_user; Type: INDEX; Schema: tenant_1; Owner: postgres
--

CREATE INDEX idx_task_assignments_user ON tenant_1.task_assignments USING btree (user_id);


--
-- Name: idx_task_attachments_task; Type: INDEX; Schema: tenant_1; Owner: postgres
--

CREATE INDEX idx_task_attachments_task ON tenant_1.task_attachments USING btree (task_id);


--
-- Name: ix_tasks_id; Type: INDEX; Schema: tenant_1; Owner: postgres
--

CREATE INDEX ix_tasks_id ON tenant_1.tasks USING btree (id);


--
-- Name: ix_users_id; Type: INDEX; Schema: tenant_1; Owner: postgres
--

CREATE INDEX ix_users_id ON tenant_1.users USING btree (id);


--
-- Name: ix_users_username; Type: INDEX; Schema: tenant_1; Owner: postgres
--

CREATE UNIQUE INDEX ix_users_username ON tenant_1.users USING btree (username);


--
-- Name: applications applications_user_id_fkey; Type: FK CONSTRAINT; Schema: tenant_1; Owner: postgres
--

ALTER TABLE ONLY tenant_1.applications
    ADD CONSTRAINT applications_user_id_fkey FOREIGN KEY (user_id) REFERENCES tenant_1.users(id) ON DELETE CASCADE;


--
-- Name: consultations consultations_user_id_fkey; Type: FK CONSTRAINT; Schema: tenant_1; Owner: postgres
--

ALTER TABLE ONLY tenant_1.consultations
    ADD CONSTRAINT consultations_user_id_fkey FOREIGN KEY (user_id) REFERENCES tenant_1.users(id) ON DELETE CASCADE;


--
-- Name: task_assignments task_assignments_task_id_fkey; Type: FK CONSTRAINT; Schema: tenant_1; Owner: postgres
--

ALTER TABLE ONLY tenant_1.task_assignments
    ADD CONSTRAINT task_assignments_task_id_fkey FOREIGN KEY (task_id) REFERENCES tenant_1.tasks(id) ON DELETE CASCADE;


--
-- Name: task_assignments task_assignments_user_id_fkey; Type: FK CONSTRAINT; Schema: tenant_1; Owner: postgres
--

ALTER TABLE ONLY tenant_1.task_assignments
    ADD CONSTRAINT task_assignments_user_id_fkey FOREIGN KEY (user_id) REFERENCES tenant_1.users(id) ON DELETE CASCADE;


--
-- Name: task_attachments task_attachments_task_id_fkey; Type: FK CONSTRAINT; Schema: tenant_1; Owner: postgres
--

ALTER TABLE ONLY tenant_1.task_attachments
    ADD CONSTRAINT task_attachments_task_id_fkey FOREIGN KEY (task_id) REFERENCES tenant_1.tasks(id) ON DELETE CASCADE;


--
-- Name: task_attachments task_attachments_uploaded_by_fkey; Type: FK CONSTRAINT; Schema: tenant_1; Owner: postgres
--

ALTER TABLE ONLY tenant_1.task_attachments
    ADD CONSTRAINT task_attachments_uploaded_by_fkey FOREIGN KEY (uploaded_by) REFERENCES tenant_1.users(id);


--
-- Name: tasks tasks_assigned_by_id_fkey; Type: FK CONSTRAINT; Schema: tenant_1; Owner: postgres
--

ALTER TABLE ONLY tenant_1.tasks
    ADD CONSTRAINT tasks_assigned_by_id_fkey FOREIGN KEY (assigned_by_id) REFERENCES tenant_1.users(id);


--
-- Name: tasks tasks_creator_id_fkey; Type: FK CONSTRAINT; Schema: tenant_1; Owner: postgres
--

ALTER TABLE ONLY tenant_1.tasks
    ADD CONSTRAINT tasks_creator_id_fkey FOREIGN KEY (creator_id) REFERENCES tenant_1.users(id);


--
-- PostgreSQL database dump complete
--

\unrestrict Mk7WsHXKYMWTclRUKXgH1WjbHPqvclIfgpfcruIfYf3iFrWGFHbgX5xEyBgPfvT

