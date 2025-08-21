--
-- PostgreSQL database dump
--

-- Dumped from database version 17.5
-- Dumped by pg_dump version 17.5

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

ALTER TABLE IF EXISTS ONLY public.users_user_permissions DROP CONSTRAINT IF EXISTS users_user_permissions_customuser_id_efdb305c_fk_users_id;
ALTER TABLE IF EXISTS ONLY public.users_user_permissions DROP CONSTRAINT IF EXISTS users_user_permissio_permission_id_6d08dcd2_fk_auth_perm;
ALTER TABLE IF EXISTS ONLY public.users DROP CONSTRAINT IF EXISTS users_profile_image_id_c982913d_fk_images_id;
ALTER TABLE IF EXISTS ONLY public.users_groups DROP CONSTRAINT IF EXISTS users_groups_group_id_2f3517aa_fk_auth_group_id;
ALTER TABLE IF EXISTS ONLY public.users_groups DROP CONSTRAINT IF EXISTS users_groups_customuser_id_4bd991a9_fk_users_id;
ALTER TABLE IF EXISTS ONLY public.token_blacklist_outstandingtoken DROP CONSTRAINT IF EXISTS token_blacklist_outstandingtoken_user_id_83bc629a_fk_users_id;
ALTER TABLE IF EXISTS ONLY public.token_blacklist_blacklistedtoken DROP CONSTRAINT IF EXISTS token_blacklist_blacklistedtoken_token_id_3cc7fe56_fk;
ALTER TABLE IF EXISTS ONLY public.schedules_idolschedule DROP CONSTRAINT IF EXISTS schedules_idolschedule_manager_id_df5f9580_fk_users_id;
ALTER TABLE IF EXISTS ONLY public.schedules_idolschedule DROP CONSTRAINT IF EXISTS schedules_idolschedule_idol_id_10a5653b_fk_idols_idol_id;
ALTER TABLE IF EXISTS ONLY public.schedules_groupschedule DROP CONSTRAINT IF EXISTS schedules_groupschedule_group_id_6726ed67_fk_groups_group_id;
ALTER TABLE IF EXISTS ONLY public.schedules_groupschedule DROP CONSTRAINT IF EXISTS schedules_groupschedule_author_id_d766b309_fk_users_id;
ALTER TABLE IF EXISTS ONLY public.idols_idolmanager DROP CONSTRAINT IF EXISTS idols_idolmanager_user_id_eadf5023_fk_users_id;
ALTER TABLE IF EXISTS ONLY public.idols_idolmanager DROP CONSTRAINT IF EXISTS idols_idolmanager_idol_id_d90ac253_fk_idols_idol_id;
ALTER TABLE IF EXISTS ONLY public.idols_idol DROP CONSTRAINT IF EXISTS idols_idol_user_id_a83e7273_fk_users_id;
ALTER TABLE IF EXISTS ONLY public.idols_idol DROP CONSTRAINT IF EXISTS idols_idol_group_id_51b47c95_fk_groups_group_id;
ALTER TABLE IF EXISTS ONLY public.groups_group DROP CONSTRAINT IF EXISTS groups_group_manager_id_fca03aad_fk_users_id;
ALTER TABLE IF EXISTS ONLY public.groups_group DROP CONSTRAINT IF EXISTS groups_group_logo_image_id_1b1a6ae0_fk_images_id;
ALTER TABLE IF EXISTS ONLY public.django_celery_beat_periodictask DROP CONSTRAINT IF EXISTS django_celery_beat_p_solar_id_a87ce72c_fk_django_ce;
ALTER TABLE IF EXISTS ONLY public.django_celery_beat_periodictask DROP CONSTRAINT IF EXISTS django_celery_beat_p_interval_id_a8ca27da_fk_django_ce;
ALTER TABLE IF EXISTS ONLY public.django_celery_beat_periodictask DROP CONSTRAINT IF EXISTS django_celery_beat_p_crontab_id_d3cba168_fk_django_ce;
ALTER TABLE IF EXISTS ONLY public.django_celery_beat_periodictask DROP CONSTRAINT IF EXISTS django_celery_beat_p_clocked_id_47a69f82_fk_django_ce;
ALTER TABLE IF EXISTS ONLY public.django_admin_log DROP CONSTRAINT IF EXISTS django_admin_log_user_id_c564eba6_fk_users_id;
ALTER TABLE IF EXISTS ONLY public.django_admin_log DROP CONSTRAINT IF EXISTS django_admin_log_content_type_id_c4bce8eb_fk_django_co;
ALTER TABLE IF EXISTS ONLY public.chat_rooms DROP CONSTRAINT IF EXISTS chat_rooms_last_message_id_c7b015c5_fk_chat_messages_id;
ALTER TABLE IF EXISTS ONLY public.chat_participants DROP CONSTRAINT IF EXISTS chat_participants_user_id_283c72d9_fk_users_id;
ALTER TABLE IF EXISTS ONLY public.chat_participants DROP CONSTRAINT IF EXISTS chat_participants_room_id_f90551d5_fk_chat_rooms_id;
ALTER TABLE IF EXISTS ONLY public.chat_messages DROP CONSTRAINT IF EXISTS chat_messages_sender_id_cd95a334_fk_users_id;
ALTER TABLE IF EXISTS ONLY public.chat_messages DROP CONSTRAINT IF EXISTS chat_messages_room_id_5bc95345_fk_chat_rooms_id;
ALTER TABLE IF EXISTS ONLY public.bookmarks_idolbookmark DROP CONSTRAINT IF EXISTS bookmarks_idolbookmark_user_id_02df2733_fk_users_id;
ALTER TABLE IF EXISTS ONLY public.bookmarks_idolbookmark DROP CONSTRAINT IF EXISTS bookmarks_idolbookmark_idol_id_c8d5506a_fk_idols_idol_id;
ALTER TABLE IF EXISTS ONLY public.bookmarks_groupbookmark DROP CONSTRAINT IF EXISTS bookmarks_groupbookmark_user_id_254f0112_fk_users_id;
ALTER TABLE IF EXISTS ONLY public.bookmarks_groupbookmark DROP CONSTRAINT IF EXISTS bookmarks_groupbookmark_group_id_fdc8be21_fk_groups_group_id;
ALTER TABLE IF EXISTS ONLY public.auth_permission DROP CONSTRAINT IF EXISTS auth_permission_content_type_id_2f476e4b_fk_django_co;
ALTER TABLE IF EXISTS ONLY public.auth_group_permissions DROP CONSTRAINT IF EXISTS auth_group_permissions_group_id_b120cbf9_fk_auth_group_id;
ALTER TABLE IF EXISTS ONLY public.auth_group_permissions DROP CONSTRAINT IF EXISTS auth_group_permissio_permission_id_84c5c92e_fk_auth_perm;
ALTER TABLE IF EXISTS ONLY public.alarms_alarm DROP CONSTRAINT IF EXISTS alarms_alarm_user_id_2555e580_fk_users_id;
ALTER TABLE IF EXISTS ONLY public.alarms_alarm DROP CONSTRAINT IF EXISTS alarms_alarm_idol_schedule_id_869129c3_fk_schedules;
ALTER TABLE IF EXISTS ONLY public.alarms_alarm DROP CONSTRAINT IF EXISTS alarms_alarm_group_schedule_id_14176631_fk_schedules;
DROP INDEX IF EXISTS public.users_user_permissions_permission_id_6d08dcd2;
DROP INDEX IF EXISTS public.users_user_permissions_customuser_id_efdb305c;
DROP INDEX IF EXISTS public.users_profile_image_id_c982913d;
DROP INDEX IF EXISTS public.users_nickname_70097a59_like;
DROP INDEX IF EXISTS public.users_groups_group_id_2f3517aa;
DROP INDEX IF EXISTS public.users_groups_customuser_id_4bd991a9;
DROP INDEX IF EXISTS public.users_email_0ea73cca_like;
DROP INDEX IF EXISTS public.token_blacklist_outstandingtoken_user_id_83bc629a;
DROP INDEX IF EXISTS public.token_blacklist_outstandingtoken_jti_hex_d9bdf6f7_like;
DROP INDEX IF EXISTS public.schedules_idolschedule_manager_id_df5f9580;
DROP INDEX IF EXISTS public.schedules_idolschedule_idol_id_10a5653b;
DROP INDEX IF EXISTS public.schedules_groupschedule_group_id_6726ed67;
DROP INDEX IF EXISTS public.schedules_groupschedule_author_id_d766b309;
DROP INDEX IF EXISTS public.idols_idolmanager_user_id_eadf5023;
DROP INDEX IF EXISTS public.idols_idolmanager_idol_id_d90ac253;
DROP INDEX IF EXISTS public.idols_idol_name_deab205c_like;
DROP INDEX IF EXISTS public.idols_idol_group_id_51b47c95;
DROP INDEX IF EXISTS public.groups_group_name_e9c7da84_like;
DROP INDEX IF EXISTS public.groups_group_manager_id_fca03aad;
DROP INDEX IF EXISTS public.groups_group_logo_image_id_1b1a6ae0;
DROP INDEX IF EXISTS public.django_session_session_key_c0390e0f_like;
DROP INDEX IF EXISTS public.django_session_expire_date_a5c62663;
DROP INDEX IF EXISTS public.django_celery_beat_periodictask_solar_id_a87ce72c;
DROP INDEX IF EXISTS public.django_celery_beat_periodictask_name_265a36b7_like;
DROP INDEX IF EXISTS public.django_celery_beat_periodictask_interval_id_a8ca27da;
DROP INDEX IF EXISTS public.django_celery_beat_periodictask_crontab_id_d3cba168;
DROP INDEX IF EXISTS public.django_celery_beat_periodictask_clocked_id_47a69f82;
DROP INDEX IF EXISTS public.django_admin_log_user_id_c564eba6;
DROP INDEX IF EXISTS public.django_admin_log_content_type_id_c4bce8eb;
DROP INDEX IF EXISTS public.chat_rooms_last_message_id_c7b015c5;
DROP INDEX IF EXISTS public.chat_participants_user_id_283c72d9;
DROP INDEX IF EXISTS public.chat_participants_room_id_f90551d5;
DROP INDEX IF EXISTS public.chat_messages_sender_id_cd95a334;
DROP INDEX IF EXISTS public.chat_messages_room_id_5bc95345;
DROP INDEX IF EXISTS public.bookmarks_idolbookmark_user_id_02df2733;
DROP INDEX IF EXISTS public.bookmarks_idolbookmark_idol_id_c8d5506a;
DROP INDEX IF EXISTS public.bookmarks_groupbookmark_user_id_254f0112;
DROP INDEX IF EXISTS public.bookmarks_groupbookmark_group_id_fdc8be21;
DROP INDEX IF EXISTS public.auth_permission_content_type_id_2f476e4b;
DROP INDEX IF EXISTS public.auth_group_permissions_permission_id_84c5c92e;
DROP INDEX IF EXISTS public.auth_group_permissions_group_id_b120cbf9;
DROP INDEX IF EXISTS public.auth_group_name_a6ea08ec_like;
DROP INDEX IF EXISTS public.alarms_alarm_user_id_2555e580;
DROP INDEX IF EXISTS public.alarms_alarm_idol_schedule_id_869129c3;
DROP INDEX IF EXISTS public.alarms_alarm_group_schedule_id_14176631;
ALTER TABLE IF EXISTS ONLY public.users_user_permissions DROP CONSTRAINT IF EXISTS users_user_permissions_pkey;
ALTER TABLE IF EXISTS ONLY public.users_user_permissions DROP CONSTRAINT IF EXISTS users_user_permissions_customuser_id_permission_2b4e4e39_uniq;
ALTER TABLE IF EXISTS ONLY public.users DROP CONSTRAINT IF EXISTS users_pkey;
ALTER TABLE IF EXISTS ONLY public.users DROP CONSTRAINT IF EXISTS users_nickname_key;
ALTER TABLE IF EXISTS ONLY public.users_groups DROP CONSTRAINT IF EXISTS users_groups_pkey;
ALTER TABLE IF EXISTS ONLY public.users_groups DROP CONSTRAINT IF EXISTS users_groups_customuser_id_group_id_927de924_uniq;
ALTER TABLE IF EXISTS ONLY public.users DROP CONSTRAINT IF EXISTS users_email_key;
ALTER TABLE IF EXISTS ONLY public.token_blacklist_outstandingtoken DROP CONSTRAINT IF EXISTS token_blacklist_outstandingtoken_pkey;
ALTER TABLE IF EXISTS ONLY public.token_blacklist_outstandingtoken DROP CONSTRAINT IF EXISTS token_blacklist_outstandingtoken_jti_hex_d9bdf6f7_uniq;
ALTER TABLE IF EXISTS ONLY public.token_blacklist_blacklistedtoken DROP CONSTRAINT IF EXISTS token_blacklist_blacklistedtoken_token_id_key;
ALTER TABLE IF EXISTS ONLY public.token_blacklist_blacklistedtoken DROP CONSTRAINT IF EXISTS token_blacklist_blacklistedtoken_pkey;
ALTER TABLE IF EXISTS ONLY public.schedules_idolschedule DROP CONSTRAINT IF EXISTS schedules_idolschedule_pkey;
ALTER TABLE IF EXISTS ONLY public.schedules_groupschedule DROP CONSTRAINT IF EXISTS schedules_groupschedule_pkey;
ALTER TABLE IF EXISTS ONLY public.images DROP CONSTRAINT IF EXISTS images_pkey;
ALTER TABLE IF EXISTS ONLY public.idols_idolmanager DROP CONSTRAINT IF EXISTS idols_idolmanager_user_id_idol_id_ae9eefaa_uniq;
ALTER TABLE IF EXISTS ONLY public.idols_idolmanager DROP CONSTRAINT IF EXISTS idols_idolmanager_pkey;
ALTER TABLE IF EXISTS ONLY public.idols_idol DROP CONSTRAINT IF EXISTS idols_idol_user_id_key;
ALTER TABLE IF EXISTS ONLY public.idols_idol DROP CONSTRAINT IF EXISTS idols_idol_pkey;
ALTER TABLE IF EXISTS ONLY public.idols_idol DROP CONSTRAINT IF EXISTS idols_idol_name_key;
ALTER TABLE IF EXISTS ONLY public.groups_group DROP CONSTRAINT IF EXISTS groups_group_pkey;
ALTER TABLE IF EXISTS ONLY public.groups_group DROP CONSTRAINT IF EXISTS groups_group_name_key;
ALTER TABLE IF EXISTS ONLY public.django_session DROP CONSTRAINT IF EXISTS django_session_pkey;
ALTER TABLE IF EXISTS ONLY public.django_migrations DROP CONSTRAINT IF EXISTS django_migrations_pkey;
ALTER TABLE IF EXISTS ONLY public.django_content_type DROP CONSTRAINT IF EXISTS django_content_type_pkey;
ALTER TABLE IF EXISTS ONLY public.django_content_type DROP CONSTRAINT IF EXISTS django_content_type_app_label_model_76bd3d3b_uniq;
ALTER TABLE IF EXISTS ONLY public.django_celery_beat_solarschedule DROP CONSTRAINT IF EXISTS django_celery_beat_solarschedule_pkey;
ALTER TABLE IF EXISTS ONLY public.django_celery_beat_solarschedule DROP CONSTRAINT IF EXISTS django_celery_beat_solar_event_latitude_longitude_ba64999a_uniq;
ALTER TABLE IF EXISTS ONLY public.django_celery_beat_periodictasks DROP CONSTRAINT IF EXISTS django_celery_beat_periodictasks_pkey;
ALTER TABLE IF EXISTS ONLY public.django_celery_beat_periodictask DROP CONSTRAINT IF EXISTS django_celery_beat_periodictask_pkey;
ALTER TABLE IF EXISTS ONLY public.django_celery_beat_periodictask DROP CONSTRAINT IF EXISTS django_celery_beat_periodictask_name_key;
ALTER TABLE IF EXISTS ONLY public.django_celery_beat_intervalschedule DROP CONSTRAINT IF EXISTS django_celery_beat_intervalschedule_pkey;
ALTER TABLE IF EXISTS ONLY public.django_celery_beat_crontabschedule DROP CONSTRAINT IF EXISTS django_celery_beat_crontabschedule_pkey;
ALTER TABLE IF EXISTS ONLY public.django_celery_beat_clockedschedule DROP CONSTRAINT IF EXISTS django_celery_beat_clockedschedule_pkey;
ALTER TABLE IF EXISTS ONLY public.django_admin_log DROP CONSTRAINT IF EXISTS django_admin_log_pkey;
ALTER TABLE IF EXISTS ONLY public.chat_rooms DROP CONSTRAINT IF EXISTS chat_rooms_pkey;
ALTER TABLE IF EXISTS ONLY public.chat_participants DROP CONSTRAINT IF EXISTS chat_participants_room_id_user_id_a1fd9483_uniq;
ALTER TABLE IF EXISTS ONLY public.chat_participants DROP CONSTRAINT IF EXISTS chat_participants_pkey;
ALTER TABLE IF EXISTS ONLY public.chat_messages DROP CONSTRAINT IF EXISTS chat_messages_pkey;
ALTER TABLE IF EXISTS ONLY public.bookmarks_idolbookmark DROP CONSTRAINT IF EXISTS bookmarks_idolbookmark_user_id_idol_id_0bc3676d_uniq;
ALTER TABLE IF EXISTS ONLY public.bookmarks_idolbookmark DROP CONSTRAINT IF EXISTS bookmarks_idolbookmark_pkey;
ALTER TABLE IF EXISTS ONLY public.bookmarks_groupbookmark DROP CONSTRAINT IF EXISTS bookmarks_groupbookmark_user_id_group_id_0a8e9d44_uniq;
ALTER TABLE IF EXISTS ONLY public.bookmarks_groupbookmark DROP CONSTRAINT IF EXISTS bookmarks_groupbookmark_pkey;
ALTER TABLE IF EXISTS ONLY public.auth_permission DROP CONSTRAINT IF EXISTS auth_permission_pkey;
ALTER TABLE IF EXISTS ONLY public.auth_permission DROP CONSTRAINT IF EXISTS auth_permission_content_type_id_codename_01ab375a_uniq;
ALTER TABLE IF EXISTS ONLY public.auth_group DROP CONSTRAINT IF EXISTS auth_group_pkey;
ALTER TABLE IF EXISTS ONLY public.auth_group_permissions DROP CONSTRAINT IF EXISTS auth_group_permissions_pkey;
ALTER TABLE IF EXISTS ONLY public.auth_group_permissions DROP CONSTRAINT IF EXISTS auth_group_permissions_group_id_permission_id_0cd325b0_uniq;
ALTER TABLE IF EXISTS ONLY public.auth_group DROP CONSTRAINT IF EXISTS auth_group_name_key;
ALTER TABLE IF EXISTS ONLY public.alarms_alarm DROP CONSTRAINT IF EXISTS alarms_alarm_pkey;
DROP TABLE IF EXISTS public.users_user_permissions;
DROP TABLE IF EXISTS public.users_groups;
DROP TABLE IF EXISTS public.users;
DROP TABLE IF EXISTS public.token_blacklist_outstandingtoken;
DROP TABLE IF EXISTS public.token_blacklist_blacklistedtoken;
DROP TABLE IF EXISTS public.schedules_idolschedule;
DROP TABLE IF EXISTS public.schedules_groupschedule;
DROP TABLE IF EXISTS public.images;
DROP TABLE IF EXISTS public.idols_idolmanager;
DROP TABLE IF EXISTS public.idols_idol;
DROP TABLE IF EXISTS public.groups_group;
DROP TABLE IF EXISTS public.django_session;
DROP TABLE IF EXISTS public.django_migrations;
DROP TABLE IF EXISTS public.django_content_type;
DROP TABLE IF EXISTS public.django_celery_beat_solarschedule;
DROP TABLE IF EXISTS public.django_celery_beat_periodictasks;
DROP TABLE IF EXISTS public.django_celery_beat_periodictask;
DROP TABLE IF EXISTS public.django_celery_beat_intervalschedule;
DROP TABLE IF EXISTS public.django_celery_beat_crontabschedule;
DROP TABLE IF EXISTS public.django_celery_beat_clockedschedule;
DROP TABLE IF EXISTS public.django_admin_log;
DROP TABLE IF EXISTS public.chat_rooms;
DROP TABLE IF EXISTS public.chat_participants;
DROP TABLE IF EXISTS public.chat_messages;
DROP TABLE IF EXISTS public.bookmarks_idolbookmark;
DROP TABLE IF EXISTS public.bookmarks_groupbookmark;
DROP TABLE IF EXISTS public.auth_permission;
DROP TABLE IF EXISTS public.auth_group_permissions;
DROP TABLE IF EXISTS public.auth_group;
DROP TABLE IF EXISTS public.alarms_alarm;
SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alarms_alarm; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.alarms_alarm (
    id bigint NOT NULL,
    message character varying(255) NOT NULL,
    is_read boolean NOT NULL,
    scheduled_time timestamp with time zone NOT NULL,
    created_at timestamp with time zone NOT NULL,
    group_schedule_id bigint,
    idol_schedule_id bigint,
    user_id bigint NOT NULL
);


--
-- Name: alarms_alarm_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.alarms_alarm ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.alarms_alarm_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(150) NOT NULL
);


--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.auth_group ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.auth_group_permissions (
    id bigint NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.auth_group_permissions ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.auth_permission ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: bookmarks_groupbookmark; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.bookmarks_groupbookmark (
    id bigint NOT NULL,
    created_at timestamp with time zone NOT NULL,
    group_id bigint NOT NULL,
    user_id bigint NOT NULL
);


--
-- Name: bookmarks_groupbookmark_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.bookmarks_groupbookmark ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.bookmarks_groupbookmark_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: bookmarks_idolbookmark; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.bookmarks_idolbookmark (
    id bigint NOT NULL,
    created_at timestamp with time zone NOT NULL,
    idol_id bigint NOT NULL,
    user_id bigint NOT NULL
);


--
-- Name: bookmarks_idolbookmark_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.bookmarks_idolbookmark ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.bookmarks_idolbookmark_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: chat_messages; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.chat_messages (
    id bigint NOT NULL,
    content character varying(2083) NOT NULL,
    sent_at timestamp with time zone NOT NULL,
    sender_id bigint NOT NULL,
    room_id bigint NOT NULL
);


--
-- Name: chat_messages_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.chat_messages ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.chat_messages_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: chat_participants; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.chat_participants (
    id bigint NOT NULL,
    joined_at timestamp with time zone NOT NULL,
    user_id bigint NOT NULL,
    room_id bigint NOT NULL
);


--
-- Name: chat_participants_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.chat_participants ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.chat_participants_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: chat_rooms; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.chat_rooms (
    id bigint NOT NULL,
    room_name character varying(255),
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    last_message_id bigint
);


--
-- Name: chat_rooms_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.chat_rooms ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.chat_rooms_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id bigint NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.django_admin_log ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_admin_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_celery_beat_clockedschedule; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.django_celery_beat_clockedschedule (
    id integer NOT NULL,
    clocked_time timestamp with time zone NOT NULL
);


--
-- Name: django_celery_beat_clockedschedule_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.django_celery_beat_clockedschedule ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_celery_beat_clockedschedule_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_celery_beat_crontabschedule; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.django_celery_beat_crontabschedule (
    id integer NOT NULL,
    minute character varying(240) NOT NULL,
    hour character varying(96) NOT NULL,
    day_of_week character varying(64) NOT NULL,
    day_of_month character varying(124) NOT NULL,
    month_of_year character varying(64) NOT NULL,
    timezone character varying(63) NOT NULL
);


--
-- Name: django_celery_beat_crontabschedule_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.django_celery_beat_crontabschedule ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_celery_beat_crontabschedule_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_celery_beat_intervalschedule; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.django_celery_beat_intervalschedule (
    id integer NOT NULL,
    every integer NOT NULL,
    period character varying(24) NOT NULL
);


--
-- Name: django_celery_beat_intervalschedule_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.django_celery_beat_intervalschedule ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_celery_beat_intervalschedule_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_celery_beat_periodictask; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.django_celery_beat_periodictask (
    id integer NOT NULL,
    name character varying(200) NOT NULL,
    task character varying(200) NOT NULL,
    args text NOT NULL,
    kwargs text NOT NULL,
    queue character varying(200),
    exchange character varying(200),
    routing_key character varying(200),
    expires timestamp with time zone,
    enabled boolean NOT NULL,
    last_run_at timestamp with time zone,
    total_run_count integer NOT NULL,
    date_changed timestamp with time zone NOT NULL,
    description text NOT NULL,
    crontab_id integer,
    interval_id integer,
    solar_id integer,
    one_off boolean NOT NULL,
    start_time timestamp with time zone,
    priority integer,
    headers text NOT NULL,
    clocked_id integer,
    expire_seconds integer,
    CONSTRAINT django_celery_beat_periodictask_expire_seconds_check CHECK ((expire_seconds >= 0)),
    CONSTRAINT django_celery_beat_periodictask_priority_check CHECK ((priority >= 0)),
    CONSTRAINT django_celery_beat_periodictask_total_run_count_check CHECK ((total_run_count >= 0))
);


--
-- Name: django_celery_beat_periodictask_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.django_celery_beat_periodictask ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_celery_beat_periodictask_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_celery_beat_periodictasks; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.django_celery_beat_periodictasks (
    ident smallint NOT NULL,
    last_update timestamp with time zone NOT NULL
);


--
-- Name: django_celery_beat_solarschedule; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.django_celery_beat_solarschedule (
    id integer NOT NULL,
    event character varying(24) NOT NULL,
    latitude numeric(9,6) NOT NULL,
    longitude numeric(9,6) NOT NULL
);


--
-- Name: django_celery_beat_solarschedule_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.django_celery_beat_solarschedule ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_celery_beat_solarschedule_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.django_content_type ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_content_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.django_migrations (
    id bigint NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.django_migrations ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


--
-- Name: groups_group; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.groups_group (
    id bigint NOT NULL,
    name character varying(50) NOT NULL,
    debut_date date NOT NULL,
    agency character varying(100) NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    logo_image_id bigint,
    manager_id bigint
);


--
-- Name: groups_group_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.groups_group ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.groups_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: idols_idol; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.idols_idol (
    id bigint NOT NULL,
    name character varying(100) NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    group_id bigint,
    user_id bigint NOT NULL
);


--
-- Name: idols_idol_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.idols_idol ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.idols_idol_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: idols_idolmanager; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.idols_idolmanager (
    id bigint NOT NULL,
    idol_id bigint NOT NULL,
    user_id bigint NOT NULL
);


--
-- Name: idols_idolmanager_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.idols_idolmanager ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.idols_idolmanager_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: images; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.images (
    id bigint NOT NULL,
    image_file character varying(100),
    url character varying(2048),
    file_size integer,
    created_at timestamp with time zone NOT NULL
);


--
-- Name: images_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.images ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.images_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: schedules_groupschedule; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.schedules_groupschedule (
    id bigint NOT NULL,
    start_time timestamp with time zone NOT NULL,
    end_time timestamp with time zone NOT NULL,
    location character varying(5000) NOT NULL,
    description character varying(5000) NOT NULL,
    is_public boolean NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    author_id bigint,
    group_id bigint NOT NULL
);


--
-- Name: schedules_groupschedule_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.schedules_groupschedule ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.schedules_groupschedule_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: schedules_idolschedule; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.schedules_idolschedule (
    id bigint NOT NULL,
    title character varying(100) NOT NULL,
    start_time timestamp with time zone NOT NULL,
    end_time timestamp with time zone NOT NULL,
    location character varying(5000) NOT NULL,
    description character varying(5000) NOT NULL,
    is_public boolean NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    idol_id bigint NOT NULL,
    manager_id bigint
);


--
-- Name: schedules_idolschedule_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.schedules_idolschedule ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.schedules_idolschedule_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: token_blacklist_blacklistedtoken; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.token_blacklist_blacklistedtoken (
    id bigint NOT NULL,
    blacklisted_at timestamp with time zone NOT NULL,
    token_id bigint NOT NULL
);


--
-- Name: token_blacklist_blacklistedtoken_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.token_blacklist_blacklistedtoken ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.token_blacklist_blacklistedtoken_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: token_blacklist_outstandingtoken; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.token_blacklist_outstandingtoken (
    id bigint NOT NULL,
    token text NOT NULL,
    created_at timestamp with time zone,
    expires_at timestamp with time zone NOT NULL,
    user_id bigint,
    jti character varying(255) NOT NULL
);


--
-- Name: token_blacklist_outstandingtoken_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.token_blacklist_outstandingtoken ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.token_blacklist_outstandingtoken_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: users; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.users (
    id bigint NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    first_name character varying(150) NOT NULL,
    last_name character varying(150) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL,
    email character varying(254) NOT NULL,
    nickname character varying(20) NOT NULL,
    role character varying(10) NOT NULL,
    social_provider character varying(30),
    social_id character varying(255),
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    profile_image_id bigint
);


--
-- Name: users_groups; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.users_groups (
    id bigint NOT NULL,
    customuser_id bigint NOT NULL,
    group_id integer NOT NULL
);


--
-- Name: users_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.users_groups ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.users_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.users ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: users_user_permissions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.users_user_permissions (
    id bigint NOT NULL,
    customuser_id bigint NOT NULL,
    permission_id integer NOT NULL
);


--
-- Name: users_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.users_user_permissions ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.users_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Data for Name: alarms_alarm; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.alarms_alarm (id, message, is_read, scheduled_time, created_at, group_schedule_id, idol_schedule_id, user_id) FROM stdin;
\.


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.auth_group (id, name) FROM stdin;
\.


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add log entry	1	add_logentry
2	Can change log entry	1	change_logentry
3	Can delete log entry	1	delete_logentry
4	Can view log entry	1	view_logentry
5	Can add permission	2	add_permission
6	Can change permission	2	change_permission
7	Can delete permission	2	delete_permission
8	Can view permission	2	view_permission
9	Can add group	3	add_group
10	Can change group	3	change_group
11	Can delete group	3	delete_group
12	Can view group	3	view_group
13	Can add content type	4	add_contenttype
14	Can change content type	4	change_contenttype
15	Can delete content type	4	delete_contenttype
16	Can view content type	4	view_contenttype
17	Can add session	5	add_session
18	Can change session	5	change_session
19	Can delete session	5	delete_session
20	Can view session	5	view_session
21	Can add Blacklisted Token	6	add_blacklistedtoken
22	Can change Blacklisted Token	6	change_blacklistedtoken
23	Can delete Blacklisted Token	6	delete_blacklistedtoken
24	Can view Blacklisted Token	6	view_blacklistedtoken
25	Can add Outstanding Token	7	add_outstandingtoken
26	Can change Outstanding Token	7	change_outstandingtoken
27	Can delete Outstanding Token	7	delete_outstandingtoken
28	Can view Outstanding Token	7	view_outstandingtoken
29	Can add crontab	8	add_crontabschedule
30	Can change crontab	8	change_crontabschedule
31	Can delete crontab	8	delete_crontabschedule
32	Can view crontab	8	view_crontabschedule
33	Can add interval	9	add_intervalschedule
34	Can change interval	9	change_intervalschedule
35	Can delete interval	9	delete_intervalschedule
36	Can view interval	9	view_intervalschedule
37	Can add periodic task	10	add_periodictask
38	Can change periodic task	10	change_periodictask
39	Can delete periodic task	10	delete_periodictask
40	Can view periodic task	10	view_periodictask
41	Can add periodic task track	11	add_periodictasks
42	Can change periodic task track	11	change_periodictasks
43	Can delete periodic task track	11	delete_periodictasks
44	Can view periodic task track	11	view_periodictasks
45	Can add solar event	12	add_solarschedule
46	Can change solar event	12	change_solarschedule
47	Can delete solar event	12	delete_solarschedule
48	Can view solar event	12	view_solarschedule
49	Can add clocked	13	add_clockedschedule
50	Can change clocked	13	change_clockedschedule
51	Can delete clocked	13	delete_clockedschedule
52	Can view clocked	13	view_clockedschedule
53	Can add 이미지	14	add_image
54	Can change 이미지	14	change_image
55	Can delete 이미지	14	delete_image
56	Can view 이미지	14	view_image
57	Can add 사용자	15	add_customuser
58	Can change 사용자	15	change_customuser
59	Can delete 사용자	15	delete_customuser
60	Can view 사용자	15	view_customuser
61	Can add 그룹	16	add_group
62	Can change 그룹	16	change_group
63	Can delete 그룹	16	delete_group
64	Can view 그룹	16	view_group
65	Can add 아이돌 매니저	17	add_idolmanager
66	Can change 아이돌 매니저	17	change_idolmanager
67	Can delete 아이돌 매니저	17	delete_idolmanager
68	Can view 아이돌 매니저	17	view_idolmanager
69	Can add 아이돌	18	add_idol
70	Can change 아이돌	18	change_idol
71	Can delete 아이돌	18	delete_idol
72	Can view 아이돌	18	view_idol
73	Can add 채팅 메시지	19	add_chatmessage
74	Can change 채팅 메시지	19	change_chatmessage
75	Can delete 채팅 메시지	19	delete_chatmessage
76	Can view 채팅 메시지	19	view_chatmessage
77	Can add 채팅방 참여자	20	add_chatparticipant
78	Can change 채팅방 참여자	20	change_chatparticipant
79	Can delete 채팅방 참여자	20	delete_chatparticipant
80	Can view 채팅방 참여자	20	view_chatparticipant
81	Can add 채팅방	21	add_chatroom
82	Can change 채팅방	21	change_chatroom
83	Can delete 채팅방	21	delete_chatroom
84	Can view 채팅방	21	view_chatroom
85	Can add 그룹 즐겨찾기	22	add_groupbookmark
86	Can change 그룹 즐겨찾기	22	change_groupbookmark
87	Can delete 그룹 즐겨찾기	22	delete_groupbookmark
88	Can view 그룹 즐겨찾기	22	view_groupbookmark
89	Can add 아이돌 즐겨찾기	23	add_idolbookmark
90	Can change 아이돌 즐겨찾기	23	change_idolbookmark
91	Can delete 아이돌 즐겨찾기	23	delete_idolbookmark
92	Can view 아이돌 즐겨찾기	23	view_idolbookmark
93	Can add alarm	24	add_alarm
94	Can change alarm	24	change_alarm
95	Can delete alarm	24	delete_alarm
96	Can view alarm	24	view_alarm
97	Can add 그룹 스케줄	25	add_groupschedule
98	Can change 그룹 스케줄	25	change_groupschedule
99	Can delete 그룹 스케줄	25	delete_groupschedule
100	Can view 그룹 스케줄	25	view_groupschedule
101	Can add 아이돌 스케줄	26	add_idolschedule
102	Can change 아이돌 스케줄	26	change_idolschedule
103	Can delete 아이돌 스케줄	26	delete_idolschedule
104	Can view 아이돌 스케줄	26	view_idolschedule
\.


--
-- Data for Name: bookmarks_groupbookmark; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.bookmarks_groupbookmark (id, created_at, group_id, user_id) FROM stdin;
\.


--
-- Data for Name: bookmarks_idolbookmark; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.bookmarks_idolbookmark (id, created_at, idol_id, user_id) FROM stdin;
\.


--
-- Data for Name: chat_messages; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.chat_messages (id, content, sent_at, sender_id, room_id) FROM stdin;
\.


--
-- Data for Name: chat_participants; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.chat_participants (id, joined_at, user_id, room_id) FROM stdin;
\.


--
-- Data for Name: chat_rooms; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.chat_rooms (id, room_name, created_at, updated_at, last_message_id) FROM stdin;
\.


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
\.


--
-- Data for Name: django_celery_beat_clockedschedule; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.django_celery_beat_clockedschedule (id, clocked_time) FROM stdin;
\.


--
-- Data for Name: django_celery_beat_crontabschedule; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.django_celery_beat_crontabschedule (id, minute, hour, day_of_week, day_of_month, month_of_year, timezone) FROM stdin;
\.


--
-- Data for Name: django_celery_beat_intervalschedule; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.django_celery_beat_intervalschedule (id, every, period) FROM stdin;
\.


--
-- Data for Name: django_celery_beat_periodictask; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.django_celery_beat_periodictask (id, name, task, args, kwargs, queue, exchange, routing_key, expires, enabled, last_run_at, total_run_count, date_changed, description, crontab_id, interval_id, solar_id, one_off, start_time, priority, headers, clocked_id, expire_seconds) FROM stdin;
\.


--
-- Data for Name: django_celery_beat_periodictasks; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.django_celery_beat_periodictasks (ident, last_update) FROM stdin;
\.


--
-- Data for Name: django_celery_beat_solarschedule; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.django_celery_beat_solarschedule (id, event, latitude, longitude) FROM stdin;
\.


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.django_content_type (id, app_label, model) FROM stdin;
1	admin	logentry
2	auth	permission
3	auth	group
4	contenttypes	contenttype
5	sessions	session
6	token_blacklist	blacklistedtoken
7	token_blacklist	outstandingtoken
8	django_celery_beat	crontabschedule
9	django_celery_beat	intervalschedule
10	django_celery_beat	periodictask
11	django_celery_beat	periodictasks
12	django_celery_beat	solarschedule
13	django_celery_beat	clockedschedule
14	users	image
15	users	customuser
16	groups	group
17	idols	idolmanager
18	idols	idol
19	chats	chatmessage
20	chats	chatparticipant
21	chats	chatroom
22	bookmarks	groupbookmark
23	bookmarks	idolbookmark
24	alarms	alarm
25	schedules	groupschedule
26	schedules	idolschedule
\.


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2025-08-20 04:50:18.763526+09
2	contenttypes	0002_remove_content_type_name	2025-08-20 04:50:18.767107+09
3	auth	0001_initial	2025-08-20 04:50:18.79197+09
4	auth	0002_alter_permission_name_max_length	2025-08-20 04:50:18.795735+09
5	auth	0003_alter_user_email_max_length	2025-08-20 04:50:18.79847+09
6	auth	0004_alter_user_username_opts	2025-08-20 04:50:18.800796+09
7	auth	0005_alter_user_last_login_null	2025-08-20 04:50:18.803184+09
8	auth	0006_require_contenttypes_0002	2025-08-20 04:50:18.803775+09
9	auth	0007_alter_validators_add_error_messages	2025-08-20 04:50:18.806281+09
10	auth	0008_alter_user_username_max_length	2025-08-20 04:50:18.808986+09
11	auth	0009_alter_user_last_name_max_length	2025-08-20 04:50:18.81193+09
12	auth	0010_alter_group_name_max_length	2025-08-20 04:50:18.81682+09
13	auth	0011_update_proxy_permissions	2025-08-20 04:50:18.819425+09
14	auth	0012_alter_user_first_name_max_length	2025-08-20 04:50:18.821688+09
15	users	0001_initial	2025-08-20 04:50:18.855398+09
16	admin	0001_initial	2025-08-20 04:50:18.868693+09
17	admin	0002_logentry_remove_auto_add	2025-08-20 04:50:18.872803+09
18	admin	0003_logentry_add_action_flag_choices	2025-08-20 04:50:18.877209+09
19	schedules	0001_initial	2025-08-20 04:50:18.885744+09
20	alarms	0001_initial	2025-08-20 04:50:18.889202+09
21	alarms	0002_initial	2025-08-20 04:50:18.896004+09
22	alarms	0003_initial	2025-08-20 04:50:18.903831+09
23	groups	0001_initial	2025-08-20 04:50:18.909287+09
24	idols	0001_initial	2025-08-20 04:50:18.920066+09
25	bookmarks	0001_initial	2025-08-20 04:50:18.926504+09
26	bookmarks	0002_initial	2025-08-20 04:50:18.931317+09
27	bookmarks	0003_initial	2025-08-20 04:50:18.971309+09
28	chats	0001_initial	2025-08-20 04:50:18.982301+09
29	chats	0002_initial	2025-08-20 04:50:19.030901+09
30	django_celery_beat	0001_initial	2025-08-20 04:50:19.051139+09
31	django_celery_beat	0002_auto_20161118_0346	2025-08-20 04:50:19.059203+09
32	django_celery_beat	0003_auto_20161209_0049	2025-08-20 04:50:19.064346+09
33	django_celery_beat	0004_auto_20170221_0000	2025-08-20 04:50:19.06625+09
34	django_celery_beat	0005_add_solarschedule_events_choices	2025-08-20 04:50:19.068182+09
35	django_celery_beat	0006_auto_20180322_0932	2025-08-20 04:50:19.090056+09
36	django_celery_beat	0007_auto_20180521_0826	2025-08-20 04:50:19.100897+09
37	django_celery_beat	0008_auto_20180914_1922	2025-08-20 04:50:19.124716+09
38	django_celery_beat	0006_auto_20180210_1226	2025-08-20 04:50:19.137175+09
39	django_celery_beat	0006_periodictask_priority	2025-08-20 04:50:19.143114+09
40	django_celery_beat	0009_periodictask_headers	2025-08-20 04:50:19.149251+09
41	django_celery_beat	0010_auto_20190429_0326	2025-08-20 04:50:19.274697+09
42	django_celery_beat	0011_auto_20190508_0153	2025-08-20 04:50:19.285103+09
43	django_celery_beat	0012_periodictask_expire_seconds	2025-08-20 04:50:19.291333+09
44	django_celery_beat	0013_auto_20200609_0727	2025-08-20 04:50:19.297919+09
45	django_celery_beat	0014_remove_clockedschedule_enabled	2025-08-20 04:50:19.3006+09
46	django_celery_beat	0015_edit_solarschedule_events_choices	2025-08-20 04:50:19.30293+09
47	django_celery_beat	0016_alter_crontabschedule_timezone	2025-08-20 04:50:19.309094+09
48	django_celery_beat	0017_alter_crontabschedule_month_of_year	2025-08-20 04:50:19.31423+09
49	django_celery_beat	0018_improve_crontab_helptext	2025-08-20 04:50:19.319176+09
50	django_celery_beat	0019_alter_periodictasks_options	2025-08-20 04:50:19.320545+09
51	groups	0002_initial	2025-08-20 04:50:19.338499+09
52	idols	0002_initial	2025-08-20 04:50:19.377378+09
53	schedules	0002_initial	2025-08-20 04:50:19.439743+09
54	sessions	0001_initial	2025-08-20 04:50:19.446799+09
55	token_blacklist	0001_initial	2025-08-20 04:50:19.475921+09
56	token_blacklist	0002_outstandingtoken_jti_hex	2025-08-20 04:50:19.48487+09
57	token_blacklist	0003_auto_20171017_2007	2025-08-20 04:50:19.500701+09
58	token_blacklist	0004_auto_20171017_2013	2025-08-20 04:50:19.515262+09
59	token_blacklist	0005_remove_outstandingtoken_jti	2025-08-20 04:50:19.523864+09
60	token_blacklist	0006_auto_20171017_2113	2025-08-20 04:50:19.534384+09
61	token_blacklist	0007_auto_20171017_2214	2025-08-20 04:50:19.558053+09
62	token_blacklist	0008_migrate_to_bigautofield	2025-08-20 04:50:19.591551+09
63	token_blacklist	0010_fix_migrate_to_bigautofield	2025-08-20 04:50:19.61066+09
64	token_blacklist	0011_linearizes_history	2025-08-20 04:50:19.612163+09
65	token_blacklist	0012_alter_outstandingtoken_user	2025-08-20 04:50:19.620967+09
66	token_blacklist	0013_alter_blacklistedtoken_options_and_more	2025-08-20 04:50:19.632046+09
\.


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
\.


--
-- Data for Name: groups_group; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.groups_group (id, name, debut_date, agency, created_at, updated_at, logo_image_id, manager_id) FROM stdin;
\.


--
-- Data for Name: idols_idol; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.idols_idol (id, name, created_at, updated_at, group_id, user_id) FROM stdin;
\.


--
-- Data for Name: idols_idolmanager; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.idols_idolmanager (id, idol_id, user_id) FROM stdin;
\.


--
-- Data for Name: images; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.images (id, image_file, url, file_size, created_at) FROM stdin;
\.


--
-- Data for Name: schedules_groupschedule; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.schedules_groupschedule (id, start_time, end_time, location, description, is_public, created_at, updated_at, author_id, group_id) FROM stdin;
\.


--
-- Data for Name: schedules_idolschedule; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.schedules_idolschedule (id, title, start_time, end_time, location, description, is_public, created_at, updated_at, idol_id, manager_id) FROM stdin;
\.


--
-- Data for Name: token_blacklist_blacklistedtoken; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.token_blacklist_blacklistedtoken (id, blacklisted_at, token_id) FROM stdin;
\.


--
-- Data for Name: token_blacklist_outstandingtoken; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.token_blacklist_outstandingtoken (id, token, created_at, expires_at, user_id, jti) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.users (id, password, last_login, is_superuser, first_name, last_name, is_staff, is_active, date_joined, email, nickname, role, social_provider, social_id, created_at, updated_at, profile_image_id) FROM stdin;
\.


--
-- Data for Name: users_groups; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.users_groups (id, customuser_id, group_id) FROM stdin;
\.


--
-- Data for Name: users_user_permissions; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.users_user_permissions (id, customuser_id, permission_id) FROM stdin;
\.


--
-- Name: alarms_alarm_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.alarms_alarm_id_seq', 1, false);


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 104, true);


--
-- Name: bookmarks_groupbookmark_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.bookmarks_groupbookmark_id_seq', 1, false);


--
-- Name: bookmarks_idolbookmark_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.bookmarks_idolbookmark_id_seq', 1, false);


--
-- Name: chat_messages_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.chat_messages_id_seq', 1, false);


--
-- Name: chat_participants_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.chat_participants_id_seq', 1, false);


--
-- Name: chat_rooms_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.chat_rooms_id_seq', 1, false);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 1, false);


--
-- Name: django_celery_beat_clockedschedule_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.django_celery_beat_clockedschedule_id_seq', 1, false);


--
-- Name: django_celery_beat_crontabschedule_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.django_celery_beat_crontabschedule_id_seq', 1, false);


--
-- Name: django_celery_beat_intervalschedule_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.django_celery_beat_intervalschedule_id_seq', 1, false);


--
-- Name: django_celery_beat_periodictask_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.django_celery_beat_periodictask_id_seq', 1, false);


--
-- Name: django_celery_beat_solarschedule_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.django_celery_beat_solarschedule_id_seq', 1, false);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 26, true);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 66, true);


--
-- Name: groups_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.groups_group_id_seq', 1, false);


--
-- Name: idols_idol_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.idols_idol_id_seq', 1, false);


--
-- Name: idols_idolmanager_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.idols_idolmanager_id_seq', 1, false);


--
-- Name: images_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.images_id_seq', 1, false);


--
-- Name: schedules_groupschedule_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.schedules_groupschedule_id_seq', 1, false);


--
-- Name: schedules_idolschedule_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.schedules_idolschedule_id_seq', 1, false);


--
-- Name: token_blacklist_blacklistedtoken_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.token_blacklist_blacklistedtoken_id_seq', 1, false);


--
-- Name: token_blacklist_outstandingtoken_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.token_blacklist_outstandingtoken_id_seq', 1, false);


--
-- Name: users_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.users_groups_id_seq', 1, false);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.users_id_seq', 1, false);


--
-- Name: users_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.users_user_permissions_id_seq', 1, false);


--
-- Name: alarms_alarm alarms_alarm_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.alarms_alarm
    ADD CONSTRAINT alarms_alarm_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission auth_permission_content_type_id_codename_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- Name: auth_permission auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: bookmarks_groupbookmark bookmarks_groupbookmark_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.bookmarks_groupbookmark
    ADD CONSTRAINT bookmarks_groupbookmark_pkey PRIMARY KEY (id);


--
-- Name: bookmarks_groupbookmark bookmarks_groupbookmark_user_id_group_id_0a8e9d44_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.bookmarks_groupbookmark
    ADD CONSTRAINT bookmarks_groupbookmark_user_id_group_id_0a8e9d44_uniq UNIQUE (user_id, group_id);


--
-- Name: bookmarks_idolbookmark bookmarks_idolbookmark_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.bookmarks_idolbookmark
    ADD CONSTRAINT bookmarks_idolbookmark_pkey PRIMARY KEY (id);


--
-- Name: bookmarks_idolbookmark bookmarks_idolbookmark_user_id_idol_id_0bc3676d_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.bookmarks_idolbookmark
    ADD CONSTRAINT bookmarks_idolbookmark_user_id_idol_id_0bc3676d_uniq UNIQUE (user_id, idol_id);


--
-- Name: chat_messages chat_messages_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.chat_messages
    ADD CONSTRAINT chat_messages_pkey PRIMARY KEY (id);


--
-- Name: chat_participants chat_participants_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.chat_participants
    ADD CONSTRAINT chat_participants_pkey PRIMARY KEY (id);


--
-- Name: chat_participants chat_participants_room_id_user_id_a1fd9483_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.chat_participants
    ADD CONSTRAINT chat_participants_room_id_user_id_a1fd9483_uniq UNIQUE (room_id, user_id);


--
-- Name: chat_rooms chat_rooms_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.chat_rooms
    ADD CONSTRAINT chat_rooms_pkey PRIMARY KEY (id);


--
-- Name: django_admin_log django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_celery_beat_clockedschedule django_celery_beat_clockedschedule_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_celery_beat_clockedschedule
    ADD CONSTRAINT django_celery_beat_clockedschedule_pkey PRIMARY KEY (id);


--
-- Name: django_celery_beat_crontabschedule django_celery_beat_crontabschedule_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_celery_beat_crontabschedule
    ADD CONSTRAINT django_celery_beat_crontabschedule_pkey PRIMARY KEY (id);


--
-- Name: django_celery_beat_intervalschedule django_celery_beat_intervalschedule_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_celery_beat_intervalschedule
    ADD CONSTRAINT django_celery_beat_intervalschedule_pkey PRIMARY KEY (id);


--
-- Name: django_celery_beat_periodictask django_celery_beat_periodictask_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_celery_beat_periodictask
    ADD CONSTRAINT django_celery_beat_periodictask_name_key UNIQUE (name);


--
-- Name: django_celery_beat_periodictask django_celery_beat_periodictask_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_celery_beat_periodictask
    ADD CONSTRAINT django_celery_beat_periodictask_pkey PRIMARY KEY (id);


--
-- Name: django_celery_beat_periodictasks django_celery_beat_periodictasks_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_celery_beat_periodictasks
    ADD CONSTRAINT django_celery_beat_periodictasks_pkey PRIMARY KEY (ident);


--
-- Name: django_celery_beat_solarschedule django_celery_beat_solar_event_latitude_longitude_ba64999a_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_celery_beat_solarschedule
    ADD CONSTRAINT django_celery_beat_solar_event_latitude_longitude_ba64999a_uniq UNIQUE (event, latitude, longitude);


--
-- Name: django_celery_beat_solarschedule django_celery_beat_solarschedule_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_celery_beat_solarschedule
    ADD CONSTRAINT django_celery_beat_solarschedule_pkey PRIMARY KEY (id);


--
-- Name: django_content_type django_content_type_app_label_model_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: groups_group groups_group_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.groups_group
    ADD CONSTRAINT groups_group_name_key UNIQUE (name);


--
-- Name: groups_group groups_group_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.groups_group
    ADD CONSTRAINT groups_group_pkey PRIMARY KEY (id);


--
-- Name: idols_idol idols_idol_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.idols_idol
    ADD CONSTRAINT idols_idol_name_key UNIQUE (name);


--
-- Name: idols_idol idols_idol_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.idols_idol
    ADD CONSTRAINT idols_idol_pkey PRIMARY KEY (id);


--
-- Name: idols_idol idols_idol_user_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.idols_idol
    ADD CONSTRAINT idols_idol_user_id_key UNIQUE (user_id);


--
-- Name: idols_idolmanager idols_idolmanager_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.idols_idolmanager
    ADD CONSTRAINT idols_idolmanager_pkey PRIMARY KEY (id);


--
-- Name: idols_idolmanager idols_idolmanager_user_id_idol_id_ae9eefaa_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.idols_idolmanager
    ADD CONSTRAINT idols_idolmanager_user_id_idol_id_ae9eefaa_uniq UNIQUE (user_id, idol_id);


--
-- Name: images images_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.images
    ADD CONSTRAINT images_pkey PRIMARY KEY (id);


--
-- Name: schedules_groupschedule schedules_groupschedule_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.schedules_groupschedule
    ADD CONSTRAINT schedules_groupschedule_pkey PRIMARY KEY (id);


--
-- Name: schedules_idolschedule schedules_idolschedule_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.schedules_idolschedule
    ADD CONSTRAINT schedules_idolschedule_pkey PRIMARY KEY (id);


--
-- Name: token_blacklist_blacklistedtoken token_blacklist_blacklistedtoken_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.token_blacklist_blacklistedtoken
    ADD CONSTRAINT token_blacklist_blacklistedtoken_pkey PRIMARY KEY (id);


--
-- Name: token_blacklist_blacklistedtoken token_blacklist_blacklistedtoken_token_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.token_blacklist_blacklistedtoken
    ADD CONSTRAINT token_blacklist_blacklistedtoken_token_id_key UNIQUE (token_id);


--
-- Name: token_blacklist_outstandingtoken token_blacklist_outstandingtoken_jti_hex_d9bdf6f7_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.token_blacklist_outstandingtoken
    ADD CONSTRAINT token_blacklist_outstandingtoken_jti_hex_d9bdf6f7_uniq UNIQUE (jti);


--
-- Name: token_blacklist_outstandingtoken token_blacklist_outstandingtoken_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.token_blacklist_outstandingtoken
    ADD CONSTRAINT token_blacklist_outstandingtoken_pkey PRIMARY KEY (id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users_groups users_groups_customuser_id_group_id_927de924_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users_groups
    ADD CONSTRAINT users_groups_customuser_id_group_id_927de924_uniq UNIQUE (customuser_id, group_id);


--
-- Name: users_groups users_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users_groups
    ADD CONSTRAINT users_groups_pkey PRIMARY KEY (id);


--
-- Name: users users_nickname_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_nickname_key UNIQUE (nickname);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users_user_permissions users_user_permissions_customuser_id_permission_2b4e4e39_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users_user_permissions
    ADD CONSTRAINT users_user_permissions_customuser_id_permission_2b4e4e39_uniq UNIQUE (customuser_id, permission_id);


--
-- Name: users_user_permissions users_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users_user_permissions
    ADD CONSTRAINT users_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: alarms_alarm_group_schedule_id_14176631; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX alarms_alarm_group_schedule_id_14176631 ON public.alarms_alarm USING btree (group_schedule_id);


--
-- Name: alarms_alarm_idol_schedule_id_869129c3; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX alarms_alarm_idol_schedule_id_869129c3 ON public.alarms_alarm USING btree (idol_schedule_id);


--
-- Name: alarms_alarm_user_id_2555e580; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX alarms_alarm_user_id_2555e580 ON public.alarms_alarm USING btree (user_id);


--
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_group_id_b120cbf9; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_permission_id_84c5c92e; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_content_type_id_2f476e4b; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);


--
-- Name: bookmarks_groupbookmark_group_id_fdc8be21; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX bookmarks_groupbookmark_group_id_fdc8be21 ON public.bookmarks_groupbookmark USING btree (group_id);


--
-- Name: bookmarks_groupbookmark_user_id_254f0112; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX bookmarks_groupbookmark_user_id_254f0112 ON public.bookmarks_groupbookmark USING btree (user_id);


--
-- Name: bookmarks_idolbookmark_idol_id_c8d5506a; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX bookmarks_idolbookmark_idol_id_c8d5506a ON public.bookmarks_idolbookmark USING btree (idol_id);


--
-- Name: bookmarks_idolbookmark_user_id_02df2733; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX bookmarks_idolbookmark_user_id_02df2733 ON public.bookmarks_idolbookmark USING btree (user_id);


--
-- Name: chat_messages_room_id_5bc95345; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX chat_messages_room_id_5bc95345 ON public.chat_messages USING btree (room_id);


--
-- Name: chat_messages_sender_id_cd95a334; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX chat_messages_sender_id_cd95a334 ON public.chat_messages USING btree (sender_id);


--
-- Name: chat_participants_room_id_f90551d5; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX chat_participants_room_id_f90551d5 ON public.chat_participants USING btree (room_id);


--
-- Name: chat_participants_user_id_283c72d9; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX chat_participants_user_id_283c72d9 ON public.chat_participants USING btree (user_id);


--
-- Name: chat_rooms_last_message_id_c7b015c5; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX chat_rooms_last_message_id_c7b015c5 ON public.chat_rooms USING btree (last_message_id);


--
-- Name: django_admin_log_content_type_id_c4bce8eb; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_user_id_c564eba6; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);


--
-- Name: django_celery_beat_periodictask_clocked_id_47a69f82; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX django_celery_beat_periodictask_clocked_id_47a69f82 ON public.django_celery_beat_periodictask USING btree (clocked_id);


--
-- Name: django_celery_beat_periodictask_crontab_id_d3cba168; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX django_celery_beat_periodictask_crontab_id_d3cba168 ON public.django_celery_beat_periodictask USING btree (crontab_id);


--
-- Name: django_celery_beat_periodictask_interval_id_a8ca27da; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX django_celery_beat_periodictask_interval_id_a8ca27da ON public.django_celery_beat_periodictask USING btree (interval_id);


--
-- Name: django_celery_beat_periodictask_name_265a36b7_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX django_celery_beat_periodictask_name_265a36b7_like ON public.django_celery_beat_periodictask USING btree (name varchar_pattern_ops);


--
-- Name: django_celery_beat_periodictask_solar_id_a87ce72c; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX django_celery_beat_periodictask_solar_id_a87ce72c ON public.django_celery_beat_periodictask USING btree (solar_id);


--
-- Name: django_session_expire_date_a5c62663; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);


--
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: groups_group_logo_image_id_1b1a6ae0; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX groups_group_logo_image_id_1b1a6ae0 ON public.groups_group USING btree (logo_image_id);


--
-- Name: groups_group_manager_id_fca03aad; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX groups_group_manager_id_fca03aad ON public.groups_group USING btree (manager_id);


--
-- Name: groups_group_name_e9c7da84_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX groups_group_name_e9c7da84_like ON public.groups_group USING btree (name varchar_pattern_ops);


--
-- Name: idols_idol_group_id_51b47c95; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idols_idol_group_id_51b47c95 ON public.idols_idol USING btree (group_id);


--
-- Name: idols_idol_name_deab205c_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idols_idol_name_deab205c_like ON public.idols_idol USING btree (name varchar_pattern_ops);


--
-- Name: idols_idolmanager_idol_id_d90ac253; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idols_idolmanager_idol_id_d90ac253 ON public.idols_idolmanager USING btree (idol_id);


--
-- Name: idols_idolmanager_user_id_eadf5023; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idols_idolmanager_user_id_eadf5023 ON public.idols_idolmanager USING btree (user_id);


--
-- Name: schedules_groupschedule_author_id_d766b309; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX schedules_groupschedule_author_id_d766b309 ON public.schedules_groupschedule USING btree (author_id);


--
-- Name: schedules_groupschedule_group_id_6726ed67; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX schedules_groupschedule_group_id_6726ed67 ON public.schedules_groupschedule USING btree (group_id);


--
-- Name: schedules_idolschedule_idol_id_10a5653b; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX schedules_idolschedule_idol_id_10a5653b ON public.schedules_idolschedule USING btree (idol_id);


--
-- Name: schedules_idolschedule_manager_id_df5f9580; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX schedules_idolschedule_manager_id_df5f9580 ON public.schedules_idolschedule USING btree (manager_id);


--
-- Name: token_blacklist_outstandingtoken_jti_hex_d9bdf6f7_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX token_blacklist_outstandingtoken_jti_hex_d9bdf6f7_like ON public.token_blacklist_outstandingtoken USING btree (jti varchar_pattern_ops);


--
-- Name: token_blacklist_outstandingtoken_user_id_83bc629a; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX token_blacklist_outstandingtoken_user_id_83bc629a ON public.token_blacklist_outstandingtoken USING btree (user_id);


--
-- Name: users_email_0ea73cca_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX users_email_0ea73cca_like ON public.users USING btree (email varchar_pattern_ops);


--
-- Name: users_groups_customuser_id_4bd991a9; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX users_groups_customuser_id_4bd991a9 ON public.users_groups USING btree (customuser_id);


--
-- Name: users_groups_group_id_2f3517aa; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX users_groups_group_id_2f3517aa ON public.users_groups USING btree (group_id);


--
-- Name: users_nickname_70097a59_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX users_nickname_70097a59_like ON public.users USING btree (nickname varchar_pattern_ops);


--
-- Name: users_profile_image_id_c982913d; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX users_profile_image_id_c982913d ON public.users USING btree (profile_image_id);


--
-- Name: users_user_permissions_customuser_id_efdb305c; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX users_user_permissions_customuser_id_efdb305c ON public.users_user_permissions USING btree (customuser_id);


--
-- Name: users_user_permissions_permission_id_6d08dcd2; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX users_user_permissions_permission_id_6d08dcd2 ON public.users_user_permissions USING btree (permission_id);


--
-- Name: alarms_alarm alarms_alarm_group_schedule_id_14176631_fk_schedules; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.alarms_alarm
    ADD CONSTRAINT alarms_alarm_group_schedule_id_14176631_fk_schedules FOREIGN KEY (group_schedule_id) REFERENCES public.schedules_groupschedule(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: alarms_alarm alarms_alarm_idol_schedule_id_869129c3_fk_schedules; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.alarms_alarm
    ADD CONSTRAINT alarms_alarm_idol_schedule_id_869129c3_fk_schedules FOREIGN KEY (idol_schedule_id) REFERENCES public.schedules_idolschedule(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: alarms_alarm alarms_alarm_user_id_2555e580_fk_users_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.alarms_alarm
    ADD CONSTRAINT alarms_alarm_user_id_2555e580_fk_users_id FOREIGN KEY (user_id) REFERENCES public.users(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: bookmarks_groupbookmark bookmarks_groupbookmark_group_id_fdc8be21_fk_groups_group_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.bookmarks_groupbookmark
    ADD CONSTRAINT bookmarks_groupbookmark_group_id_fdc8be21_fk_groups_group_id FOREIGN KEY (group_id) REFERENCES public.groups_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: bookmarks_groupbookmark bookmarks_groupbookmark_user_id_254f0112_fk_users_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.bookmarks_groupbookmark
    ADD CONSTRAINT bookmarks_groupbookmark_user_id_254f0112_fk_users_id FOREIGN KEY (user_id) REFERENCES public.users(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: bookmarks_idolbookmark bookmarks_idolbookmark_idol_id_c8d5506a_fk_idols_idol_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.bookmarks_idolbookmark
    ADD CONSTRAINT bookmarks_idolbookmark_idol_id_c8d5506a_fk_idols_idol_id FOREIGN KEY (idol_id) REFERENCES public.idols_idol(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: bookmarks_idolbookmark bookmarks_idolbookmark_user_id_02df2733_fk_users_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.bookmarks_idolbookmark
    ADD CONSTRAINT bookmarks_idolbookmark_user_id_02df2733_fk_users_id FOREIGN KEY (user_id) REFERENCES public.users(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: chat_messages chat_messages_room_id_5bc95345_fk_chat_rooms_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.chat_messages
    ADD CONSTRAINT chat_messages_room_id_5bc95345_fk_chat_rooms_id FOREIGN KEY (room_id) REFERENCES public.chat_rooms(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: chat_messages chat_messages_sender_id_cd95a334_fk_users_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.chat_messages
    ADD CONSTRAINT chat_messages_sender_id_cd95a334_fk_users_id FOREIGN KEY (sender_id) REFERENCES public.users(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: chat_participants chat_participants_room_id_f90551d5_fk_chat_rooms_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.chat_participants
    ADD CONSTRAINT chat_participants_room_id_f90551d5_fk_chat_rooms_id FOREIGN KEY (room_id) REFERENCES public.chat_rooms(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: chat_participants chat_participants_user_id_283c72d9_fk_users_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.chat_participants
    ADD CONSTRAINT chat_participants_user_id_283c72d9_fk_users_id FOREIGN KEY (user_id) REFERENCES public.users(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: chat_rooms chat_rooms_last_message_id_c7b015c5_fk_chat_messages_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.chat_rooms
    ADD CONSTRAINT chat_rooms_last_message_id_c7b015c5_fk_chat_messages_id FOREIGN KEY (last_message_id) REFERENCES public.chat_messages(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_content_type_id_c4bce8eb_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_user_id_c564eba6_fk_users_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_users_id FOREIGN KEY (user_id) REFERENCES public.users(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_celery_beat_periodictask django_celery_beat_p_clocked_id_47a69f82_fk_django_ce; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_celery_beat_periodictask
    ADD CONSTRAINT django_celery_beat_p_clocked_id_47a69f82_fk_django_ce FOREIGN KEY (clocked_id) REFERENCES public.django_celery_beat_clockedschedule(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_celery_beat_periodictask django_celery_beat_p_crontab_id_d3cba168_fk_django_ce; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_celery_beat_periodictask
    ADD CONSTRAINT django_celery_beat_p_crontab_id_d3cba168_fk_django_ce FOREIGN KEY (crontab_id) REFERENCES public.django_celery_beat_crontabschedule(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_celery_beat_periodictask django_celery_beat_p_interval_id_a8ca27da_fk_django_ce; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_celery_beat_periodictask
    ADD CONSTRAINT django_celery_beat_p_interval_id_a8ca27da_fk_django_ce FOREIGN KEY (interval_id) REFERENCES public.django_celery_beat_intervalschedule(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_celery_beat_periodictask django_celery_beat_p_solar_id_a87ce72c_fk_django_ce; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_celery_beat_periodictask
    ADD CONSTRAINT django_celery_beat_p_solar_id_a87ce72c_fk_django_ce FOREIGN KEY (solar_id) REFERENCES public.django_celery_beat_solarschedule(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: groups_group groups_group_logo_image_id_1b1a6ae0_fk_images_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.groups_group
    ADD CONSTRAINT groups_group_logo_image_id_1b1a6ae0_fk_images_id FOREIGN KEY (logo_image_id) REFERENCES public.images(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: groups_group groups_group_manager_id_fca03aad_fk_users_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.groups_group
    ADD CONSTRAINT groups_group_manager_id_fca03aad_fk_users_id FOREIGN KEY (manager_id) REFERENCES public.users(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: idols_idol idols_idol_group_id_51b47c95_fk_groups_group_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.idols_idol
    ADD CONSTRAINT idols_idol_group_id_51b47c95_fk_groups_group_id FOREIGN KEY (group_id) REFERENCES public.groups_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: idols_idol idols_idol_user_id_a83e7273_fk_users_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.idols_idol
    ADD CONSTRAINT idols_idol_user_id_a83e7273_fk_users_id FOREIGN KEY (user_id) REFERENCES public.users(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: idols_idolmanager idols_idolmanager_idol_id_d90ac253_fk_idols_idol_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.idols_idolmanager
    ADD CONSTRAINT idols_idolmanager_idol_id_d90ac253_fk_idols_idol_id FOREIGN KEY (idol_id) REFERENCES public.idols_idol(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: idols_idolmanager idols_idolmanager_user_id_eadf5023_fk_users_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.idols_idolmanager
    ADD CONSTRAINT idols_idolmanager_user_id_eadf5023_fk_users_id FOREIGN KEY (user_id) REFERENCES public.users(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: schedules_groupschedule schedules_groupschedule_author_id_d766b309_fk_users_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.schedules_groupschedule
    ADD CONSTRAINT schedules_groupschedule_author_id_d766b309_fk_users_id FOREIGN KEY (author_id) REFERENCES public.users(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: schedules_groupschedule schedules_groupschedule_group_id_6726ed67_fk_groups_group_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.schedules_groupschedule
    ADD CONSTRAINT schedules_groupschedule_group_id_6726ed67_fk_groups_group_id FOREIGN KEY (group_id) REFERENCES public.groups_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: schedules_idolschedule schedules_idolschedule_idol_id_10a5653b_fk_idols_idol_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.schedules_idolschedule
    ADD CONSTRAINT schedules_idolschedule_idol_id_10a5653b_fk_idols_idol_id FOREIGN KEY (idol_id) REFERENCES public.idols_idol(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: schedules_idolschedule schedules_idolschedule_manager_id_df5f9580_fk_users_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.schedules_idolschedule
    ADD CONSTRAINT schedules_idolschedule_manager_id_df5f9580_fk_users_id FOREIGN KEY (manager_id) REFERENCES public.users(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: token_blacklist_blacklistedtoken token_blacklist_blacklistedtoken_token_id_3cc7fe56_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.token_blacklist_blacklistedtoken
    ADD CONSTRAINT token_blacklist_blacklistedtoken_token_id_3cc7fe56_fk FOREIGN KEY (token_id) REFERENCES public.token_blacklist_outstandingtoken(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: token_blacklist_outstandingtoken token_blacklist_outstandingtoken_user_id_83bc629a_fk_users_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.token_blacklist_outstandingtoken
    ADD CONSTRAINT token_blacklist_outstandingtoken_user_id_83bc629a_fk_users_id FOREIGN KEY (user_id) REFERENCES public.users(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: users_groups users_groups_customuser_id_4bd991a9_fk_users_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users_groups
    ADD CONSTRAINT users_groups_customuser_id_4bd991a9_fk_users_id FOREIGN KEY (customuser_id) REFERENCES public.users(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: users_groups users_groups_group_id_2f3517aa_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users_groups
    ADD CONSTRAINT users_groups_group_id_2f3517aa_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: users users_profile_image_id_c982913d_fk_images_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_profile_image_id_c982913d_fk_images_id FOREIGN KEY (profile_image_id) REFERENCES public.images(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: users_user_permissions users_user_permissio_permission_id_6d08dcd2_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users_user_permissions
    ADD CONSTRAINT users_user_permissio_permission_id_6d08dcd2_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: users_user_permissions users_user_permissions_customuser_id_efdb305c_fk_users_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users_user_permissions
    ADD CONSTRAINT users_user_permissions_customuser_id_efdb305c_fk_users_id FOREIGN KEY (customuser_id) REFERENCES public.users(id) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--

