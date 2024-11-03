PGDMP  /                	    |            nutriologo_db    16.4    16.4 f    z           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            {           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            |           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            }           1262    90524    nutriologo_db    DATABASE     �   CREATE DATABASE nutriologo_db WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'Spanish_Mexico.1252';
    DROP DATABASE nutriologo_db;
                postgres    false            �            1259    90525    anio    TABLE     V   CREATE TABLE public.anio (
    id_anio integer NOT NULL,
    anio integer NOT NULL
);
    DROP TABLE public.anio;
       public         heap    postgres    false            �            1259    90528    anio_id_anio_seq    SEQUENCE     �   ALTER TABLE public.anio ALTER COLUMN id_anio ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.anio_id_anio_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    215            �            1259    98485    anio_progreso    TABLE     _   CREATE TABLE public.anio_progreso (
    id_anio integer NOT NULL,
    anio integer NOT NULL
);
 !   DROP TABLE public.anio_progreso;
       public         heap    postgres    false            �            1259    98484    anio_progreso_id_anio_seq    SEQUENCE     �   ALTER TABLE public.anio_progreso ALTER COLUMN id_anio ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.anio_progreso_id_anio_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    242            �            1259    90529    plan_alimenticio    TABLE     �  CREATE TABLE public.plan_alimenticio (
    id_plan_alimenticio integer NOT NULL,
    alimento_permitido character varying(1000) NOT NULL,
    comidas_evitar character varying(1000) NOT NULL,
    bebidas_permitidas character varying(1000) NOT NULL,
    tips_alimentacion character varying(1000),
    suplementos character varying(1000),
    id_paciente_paciente integer NOT NULL,
    id_dia_id_dia integer NOT NULL,
    id_mes_dia_mes integer NOT NULL,
    id_anio_id_anio integer NOT NULL
);
 $   DROP TABLE public.plan_alimenticio;
       public         heap    postgres    false            �            1259    90534    comida_id_comida_seq    SEQUENCE     �   ALTER TABLE public.plan_alimenticio ALTER COLUMN id_plan_alimenticio ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.comida_id_comida_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    217            �            1259    90535    dia    TABLE     S   CREATE TABLE public.dia (
    id_dia integer NOT NULL,
    dia integer NOT NULL
);
    DROP TABLE public.dia;
       public         heap    postgres    false            �            1259    114857    dia_de_rutina_ejercicio    TABLE     u   CREATE TABLE public.dia_de_rutina_ejercicio (
    id_dia_rutina integer NOT NULL,
    dia_rutina integer NOT NULL
);
 +   DROP TABLE public.dia_de_rutina_ejercicio;
       public         heap    postgres    false            �            1259    114856 )   dia_de_rutina_ejercicio_id_dia_rutina_seq    SEQUENCE     �   ALTER TABLE public.dia_de_rutina_ejercicio ALTER COLUMN id_dia_rutina ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.dia_de_rutina_ejercicio_id_dia_rutina_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    244            �            1259    90538    dia_id_dia_seq    SEQUENCE     �   ALTER TABLE public.dia ALTER COLUMN id_dia ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.dia_id_dia_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    219            �            1259    98473    dia_progreso    TABLE     \   CREATE TABLE public.dia_progreso (
    id_dia integer NOT NULL,
    dia integer NOT NULL
);
     DROP TABLE public.dia_progreso;
       public         heap    postgres    false            �            1259    98472    dia_progreso_id_dia_seq    SEQUENCE     �   ALTER TABLE public.dia_progreso ALTER COLUMN id_dia ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.dia_progreso_id_dia_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    238            �            1259    90539    mes    TABLE     a   CREATE TABLE public.mes (
    id_mes integer NOT NULL,
    mes character varying(15) NOT NULL
);
    DROP TABLE public.mes;
       public         heap    postgres    false            �            1259    90542    mes_id_mes_seq    SEQUENCE     �   ALTER TABLE public.mes ALTER COLUMN id_mes ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.mes_id_mes_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    221            �            1259    98479    mes_progreso    TABLE     j   CREATE TABLE public.mes_progreso (
    id_mes integer NOT NULL,
    mes character varying(15) NOT NULL
);
     DROP TABLE public.mes_progreso;
       public         heap    postgres    false            �            1259    98478    mes_progreso_id_mes_seq    SEQUENCE     �   ALTER TABLE public.mes_progreso ALTER COLUMN id_mes ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.mes_progreso_id_mes_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    240            �            1259    90543 
   nutriologo    TABLE     �  CREATE TABLE public.nutriologo (
    id_nutriologo integer NOT NULL,
    nombres character varying(70) NOT NULL,
    ap_paterno character varying(55) NOT NULL,
    ap_materno character varying(55),
    telefono bigint NOT NULL,
    correo_electronico character varying(100) NOT NULL,
    contrasena character varying(500) NOT NULL,
    id_rol_id_rol integer NOT NULL,
    estado_sesion boolean
);
    DROP TABLE public.nutriologo;
       public         heap    postgres    false            �            1259    90548    nutriologo_id_nutriologo_seq    SEQUENCE     �   ALTER TABLE public.nutriologo ALTER COLUMN id_nutriologo ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.nutriologo_id_nutriologo_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    223            �            1259    90649    paciente    TABLE     �  CREATE TABLE public.paciente (
    id_paciente integer NOT NULL,
    nombres character varying(70) NOT NULL,
    ap_paterno character varying(55) NOT NULL,
    ap_materno character varying(55),
    fecha_nacimiento date NOT NULL,
    sexo character varying(15) NOT NULL,
    correo_electronico character varying(100)[] NOT NULL,
    contrasena character varying(500) NOT NULL,
    telefono bigint NOT NULL,
    status boolean NOT NULL,
    id_rol_id_rol integer NOT NULL,
    id_nutriologo_id_nutriologo integer NOT NULL,
    estado_sesion boolean DEFAULT false NOT NULL,
    acceso_habilitado boolean DEFAULT true NOT NULL
);

ALTER TABLE ONLY public.paciente FORCE ROW LEVEL SECURITY;
    DROP TABLE public.paciente;
       public         heap    postgres    false            �            1259    90648    paciente_id_paciente_seq    SEQUENCE     �   ALTER TABLE public.paciente ALTER COLUMN id_paciente ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.paciente_id_paciente_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    236            �            1259    90555    semana_plan_comida    TABLE     t  CREATE TABLE public.semana_plan_comida (
    id_comida integer NOT NULL,
    tiempos_de_comida character varying(30) NOT NULL,
    menu_uno_lunes_viernes character varying(400) NOT NULL,
    menu_dos_martes_jueves character varying(400) NOT NULL,
    menu_tres_miercoles_sabado character varying(400) NOT NULL,
    id_plan_alimenticio_plan_alimenticio integer NOT NULL
);
 &   DROP TABLE public.semana_plan_comida;
       public         heap    postgres    false            �            1259    90560 "   paciente_plan_comida_id_comida_seq    SEQUENCE     �   ALTER TABLE public.semana_plan_comida ALTER COLUMN id_comida ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.paciente_plan_comida_id_comida_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    225            �            1259    90561    progreso    TABLE     g  CREATE TABLE public.progreso (
    id_progreso integer NOT NULL,
    peso double precision NOT NULL,
    abdomen double precision NOT NULL,
    brazo_der_relajado double precision NOT NULL,
    brazo_der_contraido double precision NOT NULL,
    brazo_izq_relajado double precision NOT NULL,
    brazo_izq_contraido double precision NOT NULL,
    pierna_der_relajada double precision NOT NULL,
    pierna_der_contraida double precision NOT NULL,
    pierna_izq_relajada double precision NOT NULL,
    pierna_izq_contraida double precision NOT NULL,
    pantorrilla double precision NOT NULL,
    porcentaje_grasa double precision NOT NULL,
    porcentaje_musculo double precision NOT NULL,
    id_paciente_paciente integer NOT NULL,
    id_dia_progreso_id_dia integer NOT NULL,
    id_mes_progreso_id_mes integer NOT NULL,
    id_anio_progreso_id_anio integer NOT NULL
);
    DROP TABLE public.progreso;
       public         heap    postgres    false            �            1259    90564    progreso_id_progreso_seq    SEQUENCE     �   ALTER TABLE public.progreso ALTER COLUMN id_progreso ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.progreso_id_progreso_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    227            �            1259    90642    rol    TABLE     a   CREATE TABLE public.rol (
    id_rol integer NOT NULL,
    rol character varying(25) NOT NULL
);
    DROP TABLE public.rol;
       public         heap    postgres    false            �            1259    90641    rol_id_rol_seq    SEQUENCE     �   ALTER TABLE public.rol ALTER COLUMN id_rol ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.rol_id_rol_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    234            �            1259    90565    rutina_de_ejercicio    TABLE       CREATE TABLE public.rutina_de_ejercicio (
    id_rutina integer NOT NULL,
    semana_uno integer NOT NULL,
    semana_dos integer NOT NULL,
    musculo_a_entrenar character varying(20) NOT NULL,
    ejercicio character varying(1000) NOT NULL,
    series integer NOT NULL,
    repeticion_uno integer NOT NULL,
    repeticion_dos integer,
    descansos integer NOT NULL,
    id_plan_alimenticio_plan_alimenticio integer NOT NULL,
    id_dia_de_rutina_ejercicio_id_dia_rutina integer NOT NULL,
    rutina_estado boolean NOT NULL
);
 '   DROP TABLE public.rutina_de_ejercicio;
       public         heap    postgres    false            �            1259    90570 !   rutina_de_ejercicio_id_rutina_seq    SEQUENCE     �   ALTER TABLE public.rutina_de_ejercicio ALTER COLUMN id_rutina ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.rutina_de_ejercicio_id_rutina_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    229            �            1259    90571    superusuario    TABLE        CREATE TABLE public.superusuario (
    id_super integer NOT NULL,
    nombre character varying(100) NOT NULL,
    correo_electronico character varying(100) NOT NULL,
    contrasena character varying(500) NOT NULL,
    id_rol_id_rol integer NOT NULL,
    estado_sesion boolean NOT NULL
);
     DROP TABLE public.superusuario;
       public         heap    postgres    false            �            1259    90576    superusuario_id_super_seq    SEQUENCE     �   ALTER TABLE public.superusuario ALTER COLUMN id_super ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.superusuario_id_super_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);
            public          postgres    false    231            Z          0    90525    anio 
   TABLE DATA           -   COPY public.anio (id_anio, anio) FROM stdin;
    public          postgres    false    215   �       u          0    98485    anio_progreso 
   TABLE DATA           6   COPY public.anio_progreso (id_anio, anio) FROM stdin;
    public          postgres    false    242   C�       ^          0    90535    dia 
   TABLE DATA           *   COPY public.dia (id_dia, dia) FROM stdin;
    public          postgres    false    219   ��       w          0    114857    dia_de_rutina_ejercicio 
   TABLE DATA           L   COPY public.dia_de_rutina_ejercicio (id_dia_rutina, dia_rutina) FROM stdin;
    public          postgres    false    244   �       q          0    98473    dia_progreso 
   TABLE DATA           3   COPY public.dia_progreso (id_dia, dia) FROM stdin;
    public          postgres    false    238   N�       `          0    90539    mes 
   TABLE DATA           *   COPY public.mes (id_mes, mes) FROM stdin;
    public          postgres    false    221   ŋ       s          0    98479    mes_progreso 
   TABLE DATA           3   COPY public.mes_progreso (id_mes, mes) FROM stdin;
    public          postgres    false    240   @�       b          0    90543 
   nutriologo 
   TABLE DATA           �   COPY public.nutriologo (id_nutriologo, nombres, ap_paterno, ap_materno, telefono, correo_electronico, contrasena, id_rol_id_rol, estado_sesion) FROM stdin;
    public          postgres    false    223   ��       o          0    90649    paciente 
   TABLE DATA           �   COPY public.paciente (id_paciente, nombres, ap_paterno, ap_materno, fecha_nacimiento, sexo, correo_electronico, contrasena, telefono, status, id_rol_id_rol, id_nutriologo_id_nutriologo, estado_sesion, acceso_habilitado) FROM stdin;
    public          postgres    false    236   �       \          0    90529    plan_alimenticio 
   TABLE DATA           �   COPY public.plan_alimenticio (id_plan_alimenticio, alimento_permitido, comidas_evitar, bebidas_permitidas, tips_alimentacion, suplementos, id_paciente_paciente, id_dia_id_dia, id_mes_dia_mes, id_anio_id_anio) FROM stdin;
    public          postgres    false    217   ��       f          0    90561    progreso 
   TABLE DATA           y  COPY public.progreso (id_progreso, peso, abdomen, brazo_der_relajado, brazo_der_contraido, brazo_izq_relajado, brazo_izq_contraido, pierna_der_relajada, pierna_der_contraida, pierna_izq_relajada, pierna_izq_contraida, pantorrilla, porcentaje_grasa, porcentaje_musculo, id_paciente_paciente, id_dia_progreso_id_dia, id_mes_progreso_id_mes, id_anio_progreso_id_anio) FROM stdin;
    public          postgres    false    227   �       m          0    90642    rol 
   TABLE DATA           *   COPY public.rol (id_rol, rol) FROM stdin;
    public          postgres    false    234   ��       h          0    90565    rutina_de_ejercicio 
   TABLE DATA             COPY public.rutina_de_ejercicio (id_rutina, semana_uno, semana_dos, musculo_a_entrenar, ejercicio, series, repeticion_uno, repeticion_dos, descansos, id_plan_alimenticio_plan_alimenticio, id_dia_de_rutina_ejercicio_id_dia_rutina, rutina_estado) FROM stdin;
    public          postgres    false    229   �       d          0    90555    semana_plan_comida 
   TABLE DATA           �   COPY public.semana_plan_comida (id_comida, tiempos_de_comida, menu_uno_lunes_viernes, menu_dos_martes_jueves, menu_tres_miercoles_sabado, id_plan_alimenticio_plan_alimenticio) FROM stdin;
    public          postgres    false    225   �       j          0    90571    superusuario 
   TABLE DATA           v   COPY public.superusuario (id_super, nombre, correo_electronico, contrasena, id_rol_id_rol, estado_sesion) FROM stdin;
    public          postgres    false    231   ��       ~           0    0    anio_id_anio_seq    SEQUENCE SET     @   SELECT pg_catalog.setval('public.anio_id_anio_seq', 101, true);
          public          postgres    false    216                       0    0    anio_progreso_id_anio_seq    SEQUENCE SET     I   SELECT pg_catalog.setval('public.anio_progreso_id_anio_seq', 101, true);
          public          postgres    false    241            �           0    0    comida_id_comida_seq    SEQUENCE SET     B   SELECT pg_catalog.setval('public.comida_id_comida_seq', 6, true);
          public          postgres    false    218            �           0    0 )   dia_de_rutina_ejercicio_id_dia_rutina_seq    SEQUENCE SET     W   SELECT pg_catalog.setval('public.dia_de_rutina_ejercicio_id_dia_rutina_seq', 7, true);
          public          postgres    false    243            �           0    0    dia_id_dia_seq    SEQUENCE SET     =   SELECT pg_catalog.setval('public.dia_id_dia_seq', 31, true);
          public          postgres    false    220            �           0    0    dia_progreso_id_dia_seq    SEQUENCE SET     F   SELECT pg_catalog.setval('public.dia_progreso_id_dia_seq', 31, true);
          public          postgres    false    237            �           0    0    mes_id_mes_seq    SEQUENCE SET     =   SELECT pg_catalog.setval('public.mes_id_mes_seq', 12, true);
          public          postgres    false    222            �           0    0    mes_progreso_id_mes_seq    SEQUENCE SET     F   SELECT pg_catalog.setval('public.mes_progreso_id_mes_seq', 12, true);
          public          postgres    false    239            �           0    0    nutriologo_id_nutriologo_seq    SEQUENCE SET     J   SELECT pg_catalog.setval('public.nutriologo_id_nutriologo_seq', 1, true);
          public          postgres    false    224            �           0    0    paciente_id_paciente_seq    SEQUENCE SET     G   SELECT pg_catalog.setval('public.paciente_id_paciente_seq', 10, true);
          public          postgres    false    235            �           0    0 "   paciente_plan_comida_id_comida_seq    SEQUENCE SET     Q   SELECT pg_catalog.setval('public.paciente_plan_comida_id_comida_seq', 25, true);
          public          postgres    false    226            �           0    0    progreso_id_progreso_seq    SEQUENCE SET     F   SELECT pg_catalog.setval('public.progreso_id_progreso_seq', 7, true);
          public          postgres    false    228            �           0    0    rol_id_rol_seq    SEQUENCE SET     <   SELECT pg_catalog.setval('public.rol_id_rol_seq', 4, true);
          public          postgres    false    233            �           0    0 !   rutina_de_ejercicio_id_rutina_seq    SEQUENCE SET     P   SELECT pg_catalog.setval('public.rutina_de_ejercicio_id_rutina_seq', 1, false);
          public          postgres    false    230            �           0    0    superusuario_id_super_seq    SEQUENCE SET     H   SELECT pg_catalog.setval('public.superusuario_id_super_seq', 1, false);
          public          postgres    false    232            �           2606    90582    anio anio_pkey 
   CONSTRAINT     Q   ALTER TABLE ONLY public.anio
    ADD CONSTRAINT anio_pkey PRIMARY KEY (id_anio);
 8   ALTER TABLE ONLY public.anio DROP CONSTRAINT anio_pkey;
       public            postgres    false    215            �           2606    98489     anio_progreso anio_progreso_pkey 
   CONSTRAINT     c   ALTER TABLE ONLY public.anio_progreso
    ADD CONSTRAINT anio_progreso_pkey PRIMARY KEY (id_anio);
 J   ALTER TABLE ONLY public.anio_progreso DROP CONSTRAINT anio_progreso_pkey;
       public            postgres    false    242            �           2606    90584    plan_alimenticio comida_pkey 
   CONSTRAINT     k   ALTER TABLE ONLY public.plan_alimenticio
    ADD CONSTRAINT comida_pkey PRIMARY KEY (id_plan_alimenticio);
 F   ALTER TABLE ONLY public.plan_alimenticio DROP CONSTRAINT comida_pkey;
       public            postgres    false    217            �           2606    114861 4   dia_de_rutina_ejercicio dia_de_rutina_ejercicio_pkey 
   CONSTRAINT     }   ALTER TABLE ONLY public.dia_de_rutina_ejercicio
    ADD CONSTRAINT dia_de_rutina_ejercicio_pkey PRIMARY KEY (id_dia_rutina);
 ^   ALTER TABLE ONLY public.dia_de_rutina_ejercicio DROP CONSTRAINT dia_de_rutina_ejercicio_pkey;
       public            postgres    false    244            �           2606    90586    dia dia_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.dia
    ADD CONSTRAINT dia_pkey PRIMARY KEY (id_dia);
 6   ALTER TABLE ONLY public.dia DROP CONSTRAINT dia_pkey;
       public            postgres    false    219            �           2606    98477    dia_progreso dia_progreso_pkey 
   CONSTRAINT     `   ALTER TABLE ONLY public.dia_progreso
    ADD CONSTRAINT dia_progreso_pkey PRIMARY KEY (id_dia);
 H   ALTER TABLE ONLY public.dia_progreso DROP CONSTRAINT dia_progreso_pkey;
       public            postgres    false    238            �           2606    90588    mes mes_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.mes
    ADD CONSTRAINT mes_pkey PRIMARY KEY (id_mes);
 6   ALTER TABLE ONLY public.mes DROP CONSTRAINT mes_pkey;
       public            postgres    false    221            �           2606    98483    mes_progreso mes_progreso_pkey 
   CONSTRAINT     `   ALTER TABLE ONLY public.mes_progreso
    ADD CONSTRAINT mes_progreso_pkey PRIMARY KEY (id_mes);
 H   ALTER TABLE ONLY public.mes_progreso DROP CONSTRAINT mes_progreso_pkey;
       public            postgres    false    240            �           2606    90590    nutriologo nutriologo_pkey 
   CONSTRAINT     c   ALTER TABLE ONLY public.nutriologo
    ADD CONSTRAINT nutriologo_pkey PRIMARY KEY (id_nutriologo);
 D   ALTER TABLE ONLY public.nutriologo DROP CONSTRAINT nutriologo_pkey;
       public            postgres    false    223            �           2606    90655    paciente paciente_pkey 
   CONSTRAINT     ]   ALTER TABLE ONLY public.paciente
    ADD CONSTRAINT paciente_pkey PRIMARY KEY (id_paciente);
 @   ALTER TABLE ONLY public.paciente DROP CONSTRAINT paciente_pkey;
       public            postgres    false    236            �           2606    90594 ,   semana_plan_comida paciente_plan_comida_pkey 
   CONSTRAINT     q   ALTER TABLE ONLY public.semana_plan_comida
    ADD CONSTRAINT paciente_plan_comida_pkey PRIMARY KEY (id_comida);
 V   ALTER TABLE ONLY public.semana_plan_comida DROP CONSTRAINT paciente_plan_comida_pkey;
       public            postgres    false    225            �           2606    90596    progreso progreso_pkey 
   CONSTRAINT     ]   ALTER TABLE ONLY public.progreso
    ADD CONSTRAINT progreso_pkey PRIMARY KEY (id_progreso);
 @   ALTER TABLE ONLY public.progreso DROP CONSTRAINT progreso_pkey;
       public            postgres    false    227            �           2606    90646    rol rol_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.rol
    ADD CONSTRAINT rol_pkey PRIMARY KEY (id_rol);
 6   ALTER TABLE ONLY public.rol DROP CONSTRAINT rol_pkey;
       public            postgres    false    234            �           2606    90598 ,   rutina_de_ejercicio rutina_de_ejercicio_pkey 
   CONSTRAINT     q   ALTER TABLE ONLY public.rutina_de_ejercicio
    ADD CONSTRAINT rutina_de_ejercicio_pkey PRIMARY KEY (id_rutina);
 V   ALTER TABLE ONLY public.rutina_de_ejercicio DROP CONSTRAINT rutina_de_ejercicio_pkey;
       public            postgres    false    229            �           2606    90600    superusuario superusuario_pkey 
   CONSTRAINT     b   ALTER TABLE ONLY public.superusuario
    ADD CONSTRAINT superusuario_pkey PRIMARY KEY (id_super);
 H   ALTER TABLE ONLY public.superusuario DROP CONSTRAINT superusuario_pkey;
       public            postgres    false    231            �           1259    114898    paciente_correo_electronico_idx    INDEX     i   CREATE UNIQUE INDEX paciente_correo_electronico_idx ON public.paciente USING btree (correo_electronico);
 3   DROP INDEX public.paciente_correo_electronico_idx;
       public            postgres    false    236            �           1259    114899    paciente_telefono_idx    INDEX     U   CREATE UNIQUE INDEX paciente_telefono_idx ON public.paciente USING btree (telefono);
 )   DROP INDEX public.paciente_telefono_idx;
       public            postgres    false    236            �           2606    90601    plan_alimenticio anio_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.plan_alimenticio
    ADD CONSTRAINT anio_fkey FOREIGN KEY (id_anio_id_anio) REFERENCES public.anio(id_anio) NOT VALID;
 D   ALTER TABLE ONLY public.plan_alimenticio DROP CONSTRAINT anio_fkey;
       public          postgres    false    4761    215    217            �           2606    98506    progreso anio_progreso_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.progreso
    ADD CONSTRAINT anio_progreso_fkey FOREIGN KEY (id_anio_progreso_id_anio) REFERENCES public.anio_progreso(id_anio) NOT VALID;
 E   ALTER TABLE ONLY public.progreso DROP CONSTRAINT anio_progreso_fkey;
       public          postgres    false    4789    242    227            �           2606    114862 0   rutina_de_ejercicio dia_de_rutina_ejercicio_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.rutina_de_ejercicio
    ADD CONSTRAINT dia_de_rutina_ejercicio_fkey FOREIGN KEY (id_dia_de_rutina_ejercicio_id_dia_rutina) REFERENCES public.dia_de_rutina_ejercicio(id_dia_rutina) NOT VALID;
 Z   ALTER TABLE ONLY public.rutina_de_ejercicio DROP CONSTRAINT dia_de_rutina_ejercicio_fkey;
       public          postgres    false    4791    244    229            �           2606    90606    plan_alimenticio dia_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.plan_alimenticio
    ADD CONSTRAINT dia_fkey FOREIGN KEY (id_dia_id_dia) REFERENCES public.dia(id_dia) NOT VALID;
 C   ALTER TABLE ONLY public.plan_alimenticio DROP CONSTRAINT dia_fkey;
       public          postgres    false    217    4765    219            �           2606    98496    progreso dia_progreso_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.progreso
    ADD CONSTRAINT dia_progreso_fkey FOREIGN KEY (id_dia_progreso_id_dia) REFERENCES public.dia_progreso(id_dia) NOT VALID;
 D   ALTER TABLE ONLY public.progreso DROP CONSTRAINT dia_progreso_fkey;
       public          postgres    false    227    4785    238            �           2606    90611 +   semana_plan_comida id_plan_alimenticio_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.semana_plan_comida
    ADD CONSTRAINT id_plan_alimenticio_fkey FOREIGN KEY (id_plan_alimenticio_plan_alimenticio) REFERENCES public.plan_alimenticio(id_plan_alimenticio) NOT VALID;
 U   ALTER TABLE ONLY public.semana_plan_comida DROP CONSTRAINT id_plan_alimenticio_fkey;
       public          postgres    false    225    4763    217            �           0    0 9   CONSTRAINT id_plan_alimenticio_fkey ON semana_plan_comida    COMMENT     �   COMMENT ON CONSTRAINT id_plan_alimenticio_fkey ON public.semana_plan_comida IS 'Relación entre plan_alimenticio y semana_plan_alimenticio en una relación de uno a muchos';
          public          postgres    false    4797            �           2606    90616    plan_alimenticio mes_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.plan_alimenticio
    ADD CONSTRAINT mes_fkey FOREIGN KEY (id_mes_dia_mes) REFERENCES public.mes(id_mes) NOT VALID;
 C   ALTER TABLE ONLY public.plan_alimenticio DROP CONSTRAINT mes_fkey;
       public          postgres    false    4767    217    221            �           2606    98501    progreso mes_progreso_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.progreso
    ADD CONSTRAINT mes_progreso_fkey FOREIGN KEY (id_mes_progreso_id_mes) REFERENCES public.mes_progreso(id_mes) NOT VALID;
 D   ALTER TABLE ONLY public.progreso DROP CONSTRAINT mes_progreso_fkey;
       public          postgres    false    4787    240    227            �           2606    90656    paciente nutriologo_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.paciente
    ADD CONSTRAINT nutriologo_fkey FOREIGN KEY (id_nutriologo_id_nutriologo) REFERENCES public.nutriologo(id_nutriologo);
 B   ALTER TABLE ONLY public.paciente DROP CONSTRAINT nutriologo_fkey;
       public          postgres    false    236    4769    223            �           2606    90661    progreso paciente_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.progreso
    ADD CONSTRAINT paciente_fkey FOREIGN KEY (id_paciente_paciente) REFERENCES public.paciente(id_paciente) NOT VALID;
 @   ALTER TABLE ONLY public.progreso DROP CONSTRAINT paciente_fkey;
       public          postgres    false    227    4782    236            �           2606    90666    plan_alimenticio paciente_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.plan_alimenticio
    ADD CONSTRAINT paciente_fkey FOREIGN KEY (id_paciente_paciente) REFERENCES public.paciente(id_paciente) NOT VALID;
 H   ALTER TABLE ONLY public.plan_alimenticio DROP CONSTRAINT paciente_fkey;
       public          postgres    false    217    4782    236            �           2606    90636 )   rutina_de_ejercicio plan_alimenticio_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.rutina_de_ejercicio
    ADD CONSTRAINT plan_alimenticio_fkey FOREIGN KEY (id_plan_alimenticio_plan_alimenticio) REFERENCES public.plan_alimenticio(id_plan_alimenticio) NOT VALID;
 S   ALTER TABLE ONLY public.rutina_de_ejercicio DROP CONSTRAINT plan_alimenticio_fkey;
       public          postgres    false    217    4763    229            �           0    0 7   CONSTRAINT plan_alimenticio_fkey ON rutina_de_ejercicio    COMMENT     �   COMMENT ON CONSTRAINT plan_alimenticio_fkey ON public.rutina_de_ejercicio IS 'Relación entre plan_alimenticio y rutina_de_ejercicio en una relación de uno a muchos';
          public          postgres    false    4803            �           2606    90671    nutriologo rol_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.nutriologo
    ADD CONSTRAINT rol_fkey FOREIGN KEY (id_rol_id_rol) REFERENCES public.rol(id_rol) NOT VALID;
 =   ALTER TABLE ONLY public.nutriologo DROP CONSTRAINT rol_fkey;
       public          postgres    false    223    4779    234            �           2606    90676    superusuario rol_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.superusuario
    ADD CONSTRAINT rol_fkey FOREIGN KEY (id_rol_id_rol) REFERENCES public.rol(id_rol) NOT VALID;
 ?   ALTER TABLE ONLY public.superusuario DROP CONSTRAINT rol_fkey;
       public          postgres    false    4779    234    231            �           2606    90681    paciente rol_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.paciente
    ADD CONSTRAINT rol_fkey FOREIGN KEY (id_rol_id_rol) REFERENCES public.rol(id_rol) NOT VALID;
 ;   ALTER TABLE ONLY public.paciente DROP CONSTRAINT rol_fkey;
       public          postgres    false    236    4779    234            W           3256    114888    paciente acceso_exclusivo    POLICY     �   CREATE POLICY acceso_exclusivo ON public.paciente FOR SELECT USING ((((CURRENT_USER = 'paciente'::name) AND (acceso_habilitado = true)) OR ((CURRENT_USER = 'visitante'::name) AND (acceso_habilitado = true)) OR (CURRENT_USER = 'nutriologo'::name)));
 1   DROP POLICY acceso_exclusivo ON public.paciente;
       public          postgres    false    236    236            X           3256    114889     paciente acceso_exclusivo_insert    POLICY     e   CREATE POLICY acceso_exclusivo_insert ON public.paciente FOR INSERT TO nutriologo WITH CHECK (true);
 8   DROP POLICY acceso_exclusivo_insert ON public.paciente;
       public          postgres    false    236            Y           3256    114890     paciente acceso_exclusivo_update    POLICY        CREATE POLICY acceso_exclusivo_update ON public.paciente FOR UPDATE USING ((((CURRENT_USER = 'paciente'::name) AND (acceso_habilitado = true)) OR ((CURRENT_USER = 'visitante'::name) AND (acceso_habilitado = true)) OR (CURRENT_USER = 'nutriologo'::name)));
 8   DROP POLICY acceso_exclusivo_update ON public.paciente;
       public          postgres    false    236    236            V           0    90649    paciente    ROW SECURITY     6   ALTER TABLE public.paciente ENABLE ROW LEVEL SECURITY;          public          postgres    false    236            Z   L  x�һm 1��[�!��^���J�ɉ)�+I�H�IiHk����=�}�'2�!�ˠ,dX�20+���F�g+ǳ����]xnr<w9���S��%������|x~
�x
��~/\����T�E)�x1
�X%^�/�/M�����e(�2�xYJ�l%^�/W���«��+Sᕫ��{
�J^�
�Z�W�«U�թ������x�j�5^o�ץ��V����z5x}�y�1޸oB�7���o,x��ެoN��O����[��mh�6�x[Z��և�������������tx�:�ޥ�J�w�ûo�xǞ����錄_I�,�N      u   L  x�һm 1��[�!��^���J�ɉ)�+I�H�IiHk����=�}�'2�!�ˠ,dX�20+���F�g+ǳ����]xnr<w9���S��%������|x~
�x
��~/\����T�E)�x1
�X%^�/�/M�����e(�2�xYJ�l%^�/W���«��+Sᕫ��{
�J^�
�Z�W�«U�թ������x�j�5^o�ץ��V����z5x}�y�1޸oB�7���o,x��ެoN��O����[��mh�6�x[Z��և�������������tx�:�ޥ�J�w�ûo�xǞ����錄_I�,�N      ^   g   x��A0��L'�;�R�8�%���B���Z�h��<=��-G.��7>��-7y�/~�#KY����G!���&G9��&���%Oy�R-�*�� ?P.      w   (   x��A 0��w+fw� 3�cI&iQ^�M;�����D�      q   g   x��A0��L'�;�R�8�%���B���Z�h��<=��-G.��7>��-7y�/~�#KY����G!���&G9��&���%Oy�R-�*�� ?P.      `   k   x�3�t�K-��2�tKM*��9}���L8��2s�L���|.3N�Ҽ�|.s ��-8��K�,9�SJ2Ss�ڹ8��KJ�LCN��2���Kf2����� i�#[      s   k   x�3�t�K-��2�tKM*��9}���L8��2s�L���|.3N�Ҽ�|.s ��-8��K�,9�SJ2Ss�ڹ8��KJ�LCN��2���Kf2����� i�#[      b   I   x�3��*M�K�,8��(��3���\ eiianfjbld��+HJ:��&f��%��r��pr�p��qqq T)�      o   �  x�}V�rG]7_���Nu�~�"P�ãBH���v�ےKC���T>&ߒˑۛx�ϨZS}�w��9��ߩ�y#���g��K6ݬ��g-ze�Zd둷f1��F�_}1�t��h�����}Z�m�}s�i��SN�ay�f�>��'��͜/v/g���B��k�^E���>4���Rkr��ć>
;���9J�ڜ�����{���j�d��������B�\���Y��V�6�	�`v���y��nQ�x\� ��GDf�?�w}[tA����/>ԓ?�˫�2������V{Iz��S�Xz��$kmptH�"��F�!J#�2F�Xl�RF�*����$�Y��z�Z!ﲎ�+؋ŗ>���:������9��V��R���7W��[��f��-y��c�<;�؂�A�N�����ӟ^5Z�T��yI�a��\������&�Z*YcR��b�.��z	[��1��R/��mtġ�ݷ�G���K���!�8��=x�)���O+��>��d���n��% ���ϧ{ov���_���߾���$�uk�D�R���b-6O΅�m�cMD����m�}���:F�ޑ�pvN�[pFRG�8�ˣ�6�<`�6��S'C��"X����ќN[5�t�O�5o�G���ܠ=������~����/�_ˌ[�ZB<�@�m�)*�;2�Ӱ:��z��=�:j&�6b���2�S�D}�,	"h�A�����!%zAn�c���GD(A����z�A�����̧�B|��o��K7��-����3�g/ލ����Y�ö̭��H}�.M�*(���w��6$�x�y߬���z8txE�9��Ba-A+�:$��6���$4`�h���Ah�N9�;Ћ�̇,�/d�?n�_���V�l�3��F�⑃�-2����W���/)����l���hʒ�Q�T�%Z��ǑOX�&����m��S���rq&�Iь\�d��h��pB�;`aLT��(�D�8G��z`��q��j��0�c1���]�_�}�8�?�����t��#�}~�������w�,f�8-�0�(b�8��S0�@pa�u��\�̽b�1`��������v������b�x�bZ��r���#ހȇۑv��֬�}aƆ�}2�o����j+'?O?���o�hoԙ��4g�2�C�������ѿJ��l��J1A��5����\	9�]0�jp�58�����bC��o�^P��F�s{͸���ʘr����NF�:��v�5;^��t �s};������Y?[���K�",��L\�egl(�}�} �\��n��ro�!��1���������s(�/�~4ߴU�D3ǌߡ�k���'T�(��ѻ)�㮕p�����A��,      \   [  x��T�r#E��OѡM�Y:�@�CU.���l{50;���
��W�r�ћ�$|=�#]�QE@QH%�lO�|��ϲ�Lg뙒����o��c|�����م�fNd8Iĳ
�1�/)��������+���\7���{o%ѓ�H^�fg.��ϜN��e��o�>K�����:+�tI�Ԗi\b�.��[��E�n�ڎ��sfϟL��>靑��ll�$ؙ�=�q�����Κ���)Ճ���BY�������I�xl� ��s������B���9�{�@U�R�2`��j(A)�L�L�W�����D�B;����{d��\�saq�o؋^I63��Q4���B9r�l���z[N�D]p�0i|)OQ�A=�݄,��ʼ�Rp�֋E�&��<t���ɵ'$Z���Eu���Ԍ��h��xwL����UB���OVj�Kb�A��
�K;U��V�`Z��α��{x�,c0h*���0堩9���s�ter|�W�:���˱�4�Y�����DPB*}&����� � L >�	͹�g�7L����_���)�Z�Iu�P<�DéJT`�>ǒ��d��wNN�Q�ZF^h��FDWz1h ��w��Qk�5�t��>]5�l�V����Fu�[�y��t?��9�׋EuU�𷨖���#;��gf�a�F'$����������=F.u�aS=����$abL�#�q�a��V�*[�`Đ�Av6
ƞX�Du�,O��J��F,�`�1�ksR�:[�&������-z���qRo���8��*_T 3��k��i����e��`4|Y�����G�uU����ֱ~G�������㋳��?yr{      f   �   x��O[
!����Pǻ��ϱiGٿa�P
I�l��Э��G���BҠ�(=��Ei�_�h�7���;�1V��Z6ʈ�yE�l���z���[�?����31�k{FlEO�xhlӧ�R���<�      m   <   x�3��+-)����O��2�,HL�L�+I�2�,.-H-*-.M�r�p�eg�$��b���� $�h      h      x������ � �      d   }  x��X�n#5��y
_���L�w��ؕJ��. �ޜ̸/{���+ě����ۼ	/�+���ߊ$`�Fj��|Ǟyo�I�"�bθ*���B�d�2�9d,�r�Y��TZ1%%�v��ǝ�S��T`��,[Rn�%$%/0N�ʝ���Z��`��QD�
gy�2I)}�����w�{S��S�qj)�]�����a0�,�Q��٨}W�\����j�Jf7�n��W�ĥA�$YR�E��R�y^� d#oa�<��?��VPF,1"�v9m��Fh�%�dp��%}�s�~�ݯt���B�Ng�ڊL���wC
I��ݚ��M�	X�g��{13��"]�p֋�B��јD��C2wᄃ���S�w��� <�4�ņ'�-DAR(NX.2���z�<�����(I�p���H���v8w���4@M̬�-����md�L�R���+Ղ<.�N?J>��ص�)��m�Hg�U�Z��$����X�B1Z�~CIo��vr}��ˋ��l����7�.��o&�r�̳��˗��W'�<Y���j����zI�K@}_*��'b��F�����J����]M�&��Vw鵮�Y�eZ��0#(��r�i�*Ro��b;m�Y���~[�pr�փo|eF��I�N/�?�+�:�OEd�V1�m�nA�f�r�5M22?�v8D�UKP
��LKn�h�g�WA� c�^�^���%pb�CɛBHY�yJb�ˑhNi&V���Iۥ�u1y}=�E�zz�z�0Ru��YU<1t�fZ��v�mK�pX'(Ci��Z�;s�eS�����^���%���Ί�F��DA8n��\m�3��S�n볱�asC�Y�W?����[� ��T9�*�S��*c�q菟~e���*��L?���6�wI�n\s����,�qt[��@C�e�#�ֺ�'�N3Z������li"�U���{n�������5@���}��`��/���w8֗z��/�'�?�ռ���pn�|�����N�{�Q��3�k�9o�9�f�h��Q#���F���%���om؍�3��G5o�m�X�G;���9�鎂���P?�N���.�!ߥ�~p�L=Ͷ�+���J���~|%��Wr�������]W]�      j      x������ � �     