--
-- PostgreSQL database dump
--

\restrict oTqihj6lL3q8Jv46xIrFie5JjGqc77nb5E2duKLn6VnazuQbJ7dTpuaAVmBvAm6

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
-- Name: tasks; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tasks (
    id integer NOT NULL,
    title character varying NOT NULL,
    description text,
    status public.taskstatus,
    creator_id integer,
    assignee_id integer,
    assigned_by_id integer,
    created_at timestamp with time zone DEFAULT now(),
    assigned_at timestamp with time zone,
    started_at timestamp with time zone,
    completed_at timestamp with time zone,
    result_note text
);


ALTER TABLE public.tasks OWNER TO postgres;

--
-- Name: tasks_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tasks_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tasks_id_seq OWNER TO postgres;

--
-- Name: tasks_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tasks_id_seq OWNED BY public.tasks.id;


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
-- Name: work_notes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.work_notes (
    id integer NOT NULL,
    type public.notetype NOT NULL,
    title character varying NOT NULL,
    content text,
    user_id integer NOT NULL,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone,
    extra_data text
);


ALTER TABLE public.work_notes OWNER TO postgres;

--
-- Name: work_notes_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.work_notes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.work_notes_id_seq OWNER TO postgres;

--
-- Name: work_notes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.work_notes_id_seq OWNED BY public.work_notes.id;


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
    created_at timestamp with time zone DEFAULT now()
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
-- Name: policies id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.policies ALTER COLUMN id SET DEFAULT nextval('public.policies_id_seq'::regclass);


--
-- Name: tasks id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tasks ALTER COLUMN id SET DEFAULT nextval('public.tasks_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Name: work_notes id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.work_notes ALTER COLUMN id SET DEFAULT nextval('public.work_notes_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: tenant_1; Owner: postgres
--

ALTER TABLE ONLY tenant_1.users ALTER COLUMN id SET DEFAULT nextval('tenant_1.users_id_seq'::regclass);


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
-- Data for Name: tasks; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tasks (id, title, description, status, creator_id, assignee_id, assigned_by_id, created_at, assigned_at, started_at, completed_at, result_note) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, username, hashed_password, full_name, role, village_id, created_at) FROM stdin;
\.


--
-- Data for Name: work_notes; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.work_notes (id, type, title, content, user_id, created_at, updated_at, extra_data) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: tenant_1; Owner: postgres
--

COPY tenant_1.users (id, username, hashed_password, full_name, role, village_id, created_at) FROM stdin;
1	admin	$2b$12$bqSF6UWv3EeEMTJZBRC34.NqkTuoJUtJCCsQFxlYXufEUIM2vEM5C	系统管理员	admin	1	2026-04-24 08:12:44.437456+00
2	zlb	$2b$12$GKFEQ013lnH1ivYb6kgG3uSCcofX/SCyxTsACF51v2F7VMYDKctHO	周连兵	staff	1	2026-04-25 01:50:53.355235+00
\.


--
-- Name: policies_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.policies_id_seq', 1, false);


--
-- Name: tasks_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tasks_id_seq', 1, false);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 1, false);


--
-- Name: work_notes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.work_notes_id_seq', 1, false);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: tenant_1; Owner: postgres
--

SELECT pg_catalog.setval('tenant_1.users_id_seq', 2, true);


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
-- Name: tasks tasks_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: work_notes work_notes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.work_notes
    ADD CONSTRAINT work_notes_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: tenant_1; Owner: postgres
--

ALTER TABLE ONLY tenant_1.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: ix_policies_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_policies_id ON public.policies USING btree (id);


--
-- Name: ix_tasks_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_tasks_id ON public.tasks USING btree (id);


--
-- Name: ix_users_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_users_id ON public.users USING btree (id);


--
-- Name: ix_users_username; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_users_username ON public.users USING btree (username);


--
-- Name: ix_work_notes_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_work_notes_id ON public.work_notes USING btree (id);


--
-- Name: ix_users_id; Type: INDEX; Schema: tenant_1; Owner: postgres
--

CREATE INDEX ix_users_id ON tenant_1.users USING btree (id);


--
-- Name: ix_users_username; Type: INDEX; Schema: tenant_1; Owner: postgres
--

CREATE UNIQUE INDEX ix_users_username ON tenant_1.users USING btree (username);


--
-- Name: tasks tasks_assigned_by_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_assigned_by_id_fkey FOREIGN KEY (assigned_by_id) REFERENCES public.users(id);


--
-- Name: tasks tasks_assignee_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_assignee_id_fkey FOREIGN KEY (assignee_id) REFERENCES public.users(id);


--
-- Name: tasks tasks_creator_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_creator_id_fkey FOREIGN KEY (creator_id) REFERENCES public.users(id);


--
-- Name: work_notes work_notes_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.work_notes
    ADD CONSTRAINT work_notes_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- PostgreSQL database dump complete
--

\unrestrict oTqihj6lL3q8Jv46xIrFie5JjGqc77nb5E2duKLn6VnazuQbJ7dTpuaAVmBvAm6

