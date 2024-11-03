-- crear roles
CREATE ROLE paciente WITH 
    LOGIN 
    PASSWORD 'Y#8fL*5nV!q0G3z&xT9e'
    NOSUPERUSER 
    INHERIT 
    NOCREATEDB 
    NOCREATEROLE 
    NOREPLICATION;

CREATE ROLE visitante WITH 
    LOGIN 
    PASSWORD 'T!6rF@9gQ#x1V2b&zP8k' 
    NOSUPERUSER 
    INHERIT 
    NOCREATEDB 
    NOCREATEROLE 
    NOREPLICATION;	


CREATE ROLE nutriologo WITH 
    LOGIN 
    PASSWORD 'T!6ry@9g#@c1t2b&z#@k' 
    NOSUPERUSER 
    INHERIT 
    NOCREATEDB 
    NOCREATEROLE 
    NOREPLICATION;

	CREATE ROLE superusuario WITH 
    LOGIN 
    PASSWORD 'T6645697#5x1@#b@z48k' 
    NOSUPERUSER 
    INHERIT 
    NOCREATEDB 
    NOCREATEROLE 
    NOREPLICATION;

-- otorgar permisos de select en 4 tablas al rol visitante

-- otorgar permisos de select en 4 tablas al rol visitante

GRANT SELECT ON public.nutriologo TO visitante;

GRANT SELECT ON public.paciente TO visitante;

GRANT SELECT ON public.superusuario TO visitante;

GRANT SELECT ON public.rol TO visitante;


-- permisso para rol nutriologo
GRANT SELECT ON public.anio TO nutriologo;

GRANT SELECT ON public.dia TO nutriologo;

GRANT SELECT ON public.mes TO nutriologo;

GRANT SELECT ON public.anio_progreso TO nutriologo;

GRANT SELECT ON public.dia_progreso TO nutriologo;

GRANT SELECT ON public.mes_progreso TO nutriologo;

GRANT SELECT, UPDATE, INSERT ON public.nutriologo TO nutriologo;

GRANT SELECT, UPDATE, INSERT ON public.paciente TO nutriologo;

GRANT SELECT, UPDATE, INSERT ON public.plan_alimenticio TO nutriologo;

GRANT SELECT, UPDATE, INSERT ON public.progreso TO nutriologo;  

GRANT SELECT ON public.rol TO nutriologo;

GRANT SELECT, UPDATE, INSERT ON public.rutina_de_ejercicio TO nutriologo;

GRANT SELECT ON public.dia_de_rutina_ejercicio TO nutriologo;

GRANT SELECT, UPDATE, INSERT ON public.semana_plan_comida TO nutriologo;

GRANT SELECT ON public.superusuario TO nutriologo;

-- otorgar permisos de select y update en tablas al rol paciente

GRANT SELECT ON public.anio TO paciente;

GRANT SELECT ON public.dia TO paciente;

GRANT SELECT ON public.mes TO paciente;

GRANT SELECT ON public.anio_progreso TO paciente;

GRANT SELECT ON public.dia_progreso TO paciente;

GRANT SELECT ON public.mes_progreso TO paciente;

GRANT SELECT, UPDATE ON public.paciente TO paciente;  -- Solo SELECT y UPDATE para paciente

GRANT SELECT ON public.plan_alimenticio TO paciente;

GRANT SELECT ON public.progreso TO paciente;

GRANT SELECT ON public.rol TO paciente;

GRANT SELECT ON public.rutina_de_ejercicio TO paciente;

GRANT SELECT ON public.dia_de_rutina_ejercicio TO paciente;

GRANT SELECT ON public.semana_plan_comida TO paciente;

GRANT SELECT ON public.superusuario TO paciente;


-- mas permisos (registro de progresos cliente)



-- Crear indices unicos  

CREATE UNIQUE INDEX "paciente_correo_electronico_idx" ON "public"."paciente" USING BTREE ("correo_electronico");

CREATE UNIQUE INDEX "paciente_telefono_idx" ON "public"."paciente" USING BTREE ("telefono");

SELECT id, archivo FROM documento;



-- crear tabla de pdf

CREATE TABLE documento (
    id SERIAL PRIMARY KEY,
    archivo VARCHAR(255) NOT NULL
);



INSERT INTO documento (archivo) 
VALUES ('hey') 
RETURNING id;


-- permiso para pdf
GRANT SELECT, UPDATE, INSERT ON public.documento TO nutriologo;

GRANT USAGE, SELECT ON SEQUENCE documento_id_seq TO nutriologo;


-- nuevos
-- otorgar permisos de select en 4 tablas al rol visitante

GRANT SELECT ON public.nutriologo TO visitante;

GRANT SELECT ON public.paciente TO visitante;

GRANT SELECT ON public.superusuario TO visitante;

GRANT SELECT ON public.rol TO visitante;


-- permisso para rol nutriologo
GRANT SELECT ON public.anio TO nutriologo;

GRANT SELECT ON public.dia TO nutriologo;

GRANT SELECT ON public.mes TO nutriologo;

GRANT SELECT ON public.anio_progreso TO nutriologo;

GRANT SELECT ON public.dia_progreso TO nutriologo;

GRANT SELECT ON public.mes_progreso TO nutriologo;

GRANT SELECT, UPDATE, INSERT ON public.nutriologo TO nutriologo;

GRANT SELECT, UPDATE, INSERT ON public.paciente TO nutriologo;

GRANT SELECT, UPDATE, INSERT ON public.plan_alimenticio TO nutriologo;

GRANT SELECT, UPDATE, INSERT ON public.progreso TO nutriologo;  

GRANT SELECT ON public.rol TO nutriologo;

GRANT SELECT, UPDATE, INSERT ON public.rutina_de_ejercicio TO nutriologo;

GRANT SELECT ON public.dia_de_rutina_ejercicio TO nutriologo;

GRANT SELECT, UPDATE, INSERT ON public.semana_plan_comida TO nutriologo;

GRANT SELECT ON public.superusuario TO nutriologo;

-- otorgar permisos de select y update en tablas al rol paciente

GRANT SELECT ON public.anio TO paciente;

GRANT SELECT ON public.dia TO paciente;

GRANT SELECT ON public.mes TO paciente;

GRANT SELECT ON public.anio_progreso TO paciente;

GRANT SELECT ON public.dia_progreso TO paciente;

GRANT SELECT ON public.mes_progreso TO paciente;

GRANT SELECT, UPDATE ON public.paciente TO paciente;  -- Solo SELECT y UPDATE para paciente

GRANT SELECT ON public.plan_alimenticio TO paciente;

GRANT SELECT ON public.progreso TO paciente;

GRANT SELECT ON public.rol TO paciente;

GRANT SELECT ON public.rutina_de_ejercicio TO paciente;

GRANT SELECT ON public.dia_de_rutina_ejercicio TO paciente;

GRANT SELECT ON public.semana_plan_comida TO paciente;

GRANT SELECT ON public.superusuario TO paciente;


