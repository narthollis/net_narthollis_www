---
title: Net Narthollis - Bind9 DLZ - PostgreSQL style!
sitename: Net Narthollis
---
Well i have recently setup Bind with PostgreSQL DLZ - that is, dynamically loaded zones - or loading zones on the fly from a PostgreSQL database.

The point of this post is more of a reminder to myself, there is plenty of information about Bind9 DLZ's out there. Especially at the [official Bind DLZ site](http://bind-dlz.sourceforge.net/ "http://bind-dlz.sourceforge.net/").

So first of all lets start of with the SQL.

This first file contains all of the actual DNS records, and in a 'best use' scenario is the only table you will need.
~~~~.sql
CREATE TABLE dns_record (
    id integer NOT NULL,
    zone character varying(255) NOT NULL,
    ttl integer NOT NULL,
    type character varying(255) NOT NULL,
    host character varying(255) DEFAULT '@'::character varying NOT NULL,
    mx_priority integer,
    data text,
    primary_ns character varying(255),
    resp_contact character varying(255),
    serial bigint,
    refresh integer,
    retry integer,
    expire integer,
    minimum integer
);

CREATE SEQUENCE dns_record_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;

ALTER TABLE dns_record ALTER COLUMN id SET DEFAULT nextval('dns_record_id_seq'::regclass);

ALTER TABLE ONLY dns_record ADD CONSTRAINT dns_record_pkey PRIMARY KEY (id);
CREATE INDEX dns_record_host_idx ON dns_record USING btree (host);
CREATE INDEX dns_record_type_idx ON dns_record USING btree (type);
CREATE INDEX dns_record_zone_idx ON dns_record USING btree (zone);
~~~~

This other table is only needed if you intend to use zone transfers, which when using DLZ are something of a no-no, but as I don't presently have the resources to run a second Bind DLZ to be my secondary DNS server, I am left with little choice.

~~~~.sql

CREATE TABLE dns_xfr (
    zone character varying(255) NOT NULL,
    client character varying(255) NOT NULL
);

CREATE INDEX dns_xfr_client_idx ON dns_xfr USING btree (client);
CREATE INDEX dns_xfr_zone_idx ON dns_xfr USING btree (zone);
~~~~

Ok, now if you don't have a need for zone transfers, You really shoul use the first configuration here

No Zone Transfers
~~~~.plain
dlz "Postgres Zone" {
       database "postgres 2
       {host=127.0.0.1 port=5432 dbname=bind user=bind}
       {SELECT zone FROM dns_record WHERE zone = '%zone%'}
       {SELECT ttl, type, mx_priority, case when lower(type)='txt' then '\"' || data || '\"' else data end AS data FROM dns_record WHERE zone = '%zone%' AND host = '%record%' AND type <> 'SOA' AND type <> 'NS'}
       {SELECT ttl, type, data, resp_contact, serial, refresh, retry, expire, minimum FROM dns_record WHERE zone = '%zone%' AND (type = 'SOA' OR type='NS')}
       {SELECT ttl, type, host, mx_priority, case when lower(type)='txt' then '\"' || data || '\"' else data end AS data, resp_contact, serial, refresh, retry, expire, minimum FROM dns_record WHERE zone = '%zone%' AND type <> 'SOA' AND type <> 'NS'}
       {SELECT zone FROM dns_xfr where zone='%zone%' AND client = '%client%'}";
};
~~~~

If you really do need to support zone transfers, here is the configuration to use.
~~~~.plain
dlz "Postgres Zone" {
        database "postgres 2
        {host=127.0.0.1 port=5432 dbname=bind user=bind}
        {SELECT zone FROM dns_record WHERE zone = '%zone%'}
        {SELECT ttl, type, mx_priority, CASE WHEN LOWER(type)='txt' THEN '\"' || data || '\"' WHEN LOWER(type)='soa' THEN data || ' ' || resp_contact || ' ' || serial || ' ' || refresh || ' ' || retry || ' ' || expire || ' ' || minimum else data end from dns_record where zone = '%zone%' and host = '%record%'}
        {}
        {select ttl, type, host, mx_priority, case when lower(type)='txt' then '\"' || data || '\"' else data end, resp_contact, serial, refresh, retry, expire, minimum from dns_record where zone = '%zone%'}
        {SELECT zone FROM dns_xfr where zone='%zone%' AND client = '%client%'}";
};
~~~~

Well best of luck if you do decide to use this!