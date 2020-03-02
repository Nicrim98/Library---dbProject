--
-- PostgreSQL database dump
--

-- Dumped from database version 12.1
-- Dumped by pg_dump version 12.1

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
-- Name: autorzy; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.autorzy (
    id_autora bigint NOT NULL,
    imie character varying(30) NOT NULL,
    nazwisko character varying(30) NOT NULL
);


ALTER TABLE public.autorzy OWNER TO postgres;

--
-- Name: autorzy_id_autora_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.autorzy_id_autora_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.autorzy_id_autora_seq OWNER TO postgres;

--
-- Name: autorzy_id_autora_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.autorzy_id_autora_seq OWNED BY public.autorzy.id_autora;


--
-- Name: czytelnicy; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.czytelnicy (
    id_czytelnika bigint NOT NULL,
    imie character varying(30) NOT NULL,
    nazwisko character varying(30) NOT NULL,
    pesel character varying(11) NOT NULL,
    data_urodzenia date NOT NULL
);


ALTER TABLE public.czytelnicy OWNER TO postgres;

--
-- Name: czytelnicy_id_czytelnika_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.czytelnicy_id_czytelnika_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.czytelnicy_id_czytelnika_seq OWNER TO postgres;

--
-- Name: czytelnicy_id_czytelnika_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.czytelnicy_id_czytelnika_seq OWNED BY public.czytelnicy.id_czytelnika;


--
-- Name: kategorie; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.kategorie (
    id_kategorii bigint NOT NULL,
    nazwa character varying(30) NOT NULL
);


ALTER TABLE public.kategorie OWNER TO postgres;

--
-- Name: kategorie_id_kategorii_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.kategorie_id_kategorii_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.kategorie_id_kategorii_seq OWNER TO postgres;

--
-- Name: kategorie_id_kategorii_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.kategorie_id_kategorii_seq OWNED BY public.kategorie.id_kategorii;


--
-- Name: ksiazki; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ksiazki (
    id_ksiazki bigint NOT NULL,
    id_kategorii integer,
    tytul character varying(30) NOT NULL,
    id_autora integer,
    rok_wydania integer
);


ALTER TABLE public.ksiazki OWNER TO postgres;

--
-- Name: ksiazki_id_ksiazki_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.ksiazki_id_ksiazki_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.ksiazki_id_ksiazki_seq OWNER TO postgres;

--
-- Name: ksiazki_id_ksiazki_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.ksiazki_id_ksiazki_seq OWNED BY public.ksiazki.id_ksiazki;


--
-- Name: wypozyczenia; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.wypozyczenia (
    id_wypozyczenia bigint NOT NULL,
    id_czytelnika integer,
    id_ksiazki integer,
    tytul character varying(30) NOT NULL,
    data_wypozyczenia date NOT NULL,
    data_oddania date NOT NULL
);


ALTER TABLE public.wypozyczenia OWNER TO postgres;

--
-- Name: wypozyczenia_id_wypozyczenia_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.wypozyczenia_id_wypozyczenia_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.wypozyczenia_id_wypozyczenia_seq OWNER TO postgres;

--
-- Name: wypozyczenia_id_wypozyczenia_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.wypozyczenia_id_wypozyczenia_seq OWNED BY public.wypozyczenia.id_wypozyczenia;


--
-- Name: autorzy id_autora; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.autorzy ALTER COLUMN id_autora SET DEFAULT nextval('public.autorzy_id_autora_seq'::regclass);


--
-- Name: czytelnicy id_czytelnika; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.czytelnicy ALTER COLUMN id_czytelnika SET DEFAULT nextval('public.czytelnicy_id_czytelnika_seq'::regclass);


--
-- Name: kategorie id_kategorii; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.kategorie ALTER COLUMN id_kategorii SET DEFAULT nextval('public.kategorie_id_kategorii_seq'::regclass);


--
-- Name: ksiazki id_ksiazki; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ksiazki ALTER COLUMN id_ksiazki SET DEFAULT nextval('public.ksiazki_id_ksiazki_seq'::regclass);


--
-- Name: wypozyczenia id_wypozyczenia; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.wypozyczenia ALTER COLUMN id_wypozyczenia SET DEFAULT nextval('public.wypozyczenia_id_wypozyczenia_seq'::regclass);


--
-- Name: autorzy autorzy_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.autorzy
    ADD CONSTRAINT autorzy_pkey PRIMARY KEY (id_autora);


--
-- Name: czytelnicy czytelnicy_pesel_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.czytelnicy
    ADD CONSTRAINT czytelnicy_pesel_key UNIQUE (pesel);


--
-- Name: czytelnicy czytelnicy_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.czytelnicy
    ADD CONSTRAINT czytelnicy_pkey PRIMARY KEY (id_czytelnika);


--
-- Name: kategorie kategorie_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.kategorie
    ADD CONSTRAINT kategorie_pkey PRIMARY KEY (id_kategorii);


--
-- Name: ksiazki ksiazki_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ksiazki
    ADD CONSTRAINT ksiazki_pkey PRIMARY KEY (id_ksiazki);


--
-- Name: wypozyczenia wypozyczenia_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.wypozyczenia
    ADD CONSTRAINT wypozyczenia_pkey PRIMARY KEY (id_wypozyczenia);


--
-- Name: ksiazki ksiazki_id_autora_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ksiazki
    ADD CONSTRAINT ksiazki_id_autora_fkey FOREIGN KEY (id_autora) REFERENCES public.autorzy(id_autora) ON DELETE CASCADE;


--
-- Name: ksiazki ksiazki_id_kategorii_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ksiazki
    ADD CONSTRAINT ksiazki_id_kategorii_fkey FOREIGN KEY (id_kategorii) REFERENCES public.kategorie(id_kategorii) ON DELETE CASCADE;


--
-- Name: wypozyczenia wypozyczenia_id_czytelnika_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.wypozyczenia
    ADD CONSTRAINT wypozyczenia_id_czytelnika_fkey FOREIGN KEY (id_czytelnika) REFERENCES public.czytelnicy(id_czytelnika) ON DELETE CASCADE;


--
-- Name: wypozyczenia wypozyczenia_id_ksiazki_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.wypozyczenia
    ADD CONSTRAINT wypozyczenia_id_ksiazki_fkey FOREIGN KEY (id_ksiazki) REFERENCES public.ksiazki(id_ksiazki) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

