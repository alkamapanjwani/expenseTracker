--
-- PostgreSQL database dump
--

-- Dumped from database version 14.9
-- Dumped by pg_dump version 14.9

-- Started on 2023-08-26 21:26:19

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
-- TOC entry 212 (class 1259 OID 16414)
-- Name: expense_head; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.expense_head (
    expense_head_id integer NOT NULL,
    expense_head_name character varying NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.expense_head OWNER TO postgres;

--
-- TOC entry 211 (class 1259 OID 16413)
-- Name: expense_head_expense_head_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.expense_head ALTER COLUMN expense_head_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.expense_head_expense_head_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 216 (class 1259 OID 16440)
-- Name: expense_list; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.expense_list (
    expense_list_id integer NOT NULL,
    amount numeric NOT NULL,
    comment character varying,
    income_head_id integer NOT NULL,
    expense_head_id integer NOT NULL,
    user_id integer NOT NULL,
    created_timestamp timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


ALTER TABLE public.expense_list OWNER TO postgres;

--
-- TOC entry 215 (class 1259 OID 16439)
-- Name: expense_list_expense_list_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.expense_list ALTER COLUMN expense_list_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.expense_list_expense_list_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 214 (class 1259 OID 16427)
-- Name: income_head; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.income_head (
    income_head_id integer NOT NULL,
    income_head_name character varying NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.income_head OWNER TO postgres;

--
-- TOC entry 213 (class 1259 OID 16426)
-- Name: income_head_income_head_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.income_head ALTER COLUMN income_head_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.income_head_income_head_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 210 (class 1259 OID 16406)
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    user_id integer NOT NULL,
    username character varying NOT NULL,
    full_name character varying NOT NULL,
    password character varying NOT NULL
);


ALTER TABLE public.users OWNER TO postgres;

--
-- TOC entry 209 (class 1259 OID 16405)
-- Name: user_user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.users ALTER COLUMN user_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.user_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 3183 (class 2606 OID 16420)
-- Name: expense_head expense_head_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.expense_head
    ADD CONSTRAINT expense_head_pkey PRIMARY KEY (expense_head_id);


--
-- TOC entry 3187 (class 2606 OID 16447)
-- Name: expense_list expense_list_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.expense_list
    ADD CONSTRAINT expense_list_pkey PRIMARY KEY (expense_list_id);


--
-- TOC entry 3185 (class 2606 OID 16433)
-- Name: income_head income_head_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.income_head
    ADD CONSTRAINT income_head_pkey PRIMARY KEY (income_head_id);


--
-- TOC entry 3181 (class 2606 OID 16412)
-- Name: users user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT user_pkey PRIMARY KEY (user_id);


--
-- TOC entry 3192 (class 2606 OID 16458)
-- Name: expense_list fk_expense_head_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.expense_list
    ADD CONSTRAINT fk_expense_head_id FOREIGN KEY (expense_head_id) REFERENCES public.expense_head(expense_head_id);


--
-- TOC entry 3191 (class 2606 OID 16453)
-- Name: expense_list fk_income_head_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.expense_list
    ADD CONSTRAINT fk_income_head_id FOREIGN KEY (income_head_id) REFERENCES public.income_head(income_head_id);


--
-- TOC entry 3188 (class 2606 OID 16421)
-- Name: expense_head fk_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.expense_head
    ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- TOC entry 3189 (class 2606 OID 16434)
-- Name: income_head fk_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.income_head
    ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- TOC entry 3190 (class 2606 OID 16448)
-- Name: expense_list fk_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.expense_list
    ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES public.users(user_id);


-- Completed on 2023-08-26 21:26:20

--
-- PostgreSQL database dump complete
--

