--
-- PostgreSQL database dump
--

-- Dumped from database version 15.3 (Ubuntu 15.3-1.pgdg18.04+1)
-- Dumped by pg_dump version 15.3 (Ubuntu 15.3-1.pgdg18.04+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: code_access; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.code_access (
    id integer NOT NULL,
    code character varying(32),
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.code_access OWNER TO postgres;

--
-- Name: code_access_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.code_access_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.code_access_id_seq OWNER TO postgres;

--
-- Name: code_access_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.code_access_id_seq OWNED BY public.code_access.id;


--
-- Name: detections; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.detections (
    id character varying(32) NOT NULL,
    latitude character varying(32),
    longitude character varying(32),
    confidance character varying(32),
    wide character varying(32),
    image character varying(128),
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.detections OWNER TO postgres;

--
-- Name: code_access id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.code_access ALTER COLUMN id SET DEFAULT nextval('public.code_access_id_seq'::regclass);


--
-- Data for Name: code_access; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.code_access (id, code, created_at) FROM stdin;
1	E41211739	2023-11-17 10:53:07.965531+07
\.


--
-- Data for Name: detections; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.detections (id, latitude, longitude, confidance, wide, image, created_at) FROM stdin;
\.


--
-- Name: code_access_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.code_access_id_seq', 1, true);


--
-- Name: code_access code_access_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.code_access
    ADD CONSTRAINT code_access_pkey PRIMARY KEY (id);


--
-- Name: detections detections_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.detections
    ADD CONSTRAINT detections_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

