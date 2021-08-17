+++
title = "Bind DLZ and Postgres - Part 2"
template = "page.html"
date = 2014-01-21T04:12:33Z
[taxonomies]
tags = ["dns", "bind", "postgres"]
[extra]
mathjax = "tex-mml"
+++

Recently, thanks to my once again playing [EVE Online][eve], I have had the opportunity to talk to some people who deal with a lot of my interest subjects as their day job. This has allowed me to learn a lot about many different subjects.

One thing that came up recently (when I commented that my DNS server had fallen over) was that SQL backed DNS was stupid... except when there was some requirement for it to be updated by non-technical users. Now, given that is a large part of the reason I moved to using SQL backed DNS in the first place, I enquired about how to get around the various issues when using SQL backed DNS.

<!-- more -->

As it turns out, the way to get around most of the deficiencies is to simply not publish the real master server, and only publish slave servers.

Now, I really liked this idea, as I very quickly assessed that this could let me get rid of another 2 servers if I could find some other service to hos my slave DNS servers.
I hit up Google and I found a well reviewed service and signed up for it. (I will refrain from posting about it here until I have had a chance to properly use it and see how it goes one way or the other.)

In my last last post on the subject of SQL backed DNS, I comment that XFR and SQL backed DNS is a bad idea. The reason for this being a bad idea is because the authors of DLZ were after instant update DNS and master-&gt;slave replication is not an instant thing.

My goal with using SQL backed DNS is not the instant update the DLZ is looking for however, it is as I want a simple well documented interface to create web front end for managing DNS.

Using XFR with SQL backed DNS still allows me to have this simple, well documented interface to the zone data (the SQL database) and it additionally gives me the speed and robust stability of a stock DNS server.

## Technical Bit ##

So that enough on the why, lets get onto the how.

Since my last article on the subject I made some slight changes to the database schema I was using - In particular, moved all of the SOA information into the Zone table, and added proper database relations between all of the tables in the schema.

Ok, so lets start with the schema I am using

### Zone ###
```sql
CREATE SEQUENCE dns_zone_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

CREATE TABLE dns_zone (
    id integer DEFAULT nextval('dns_zone_id_seq'::regclass) NOT NULL,
    zone character varying(255) NOT NULL,
    primary_ns character varying(255) NOT NULL,
    contact character varying(255) NOT NULL,
    serial bigint NOT NULL,
    refresh integer NOT NULL,
    retry integer NOT NULL,
    expire integer NOT NULL,
    minimum integer NOT NULL,
    ttl integer DEFAULT 1200 NOT NULL
);

ALTER TABLE ONLY dns_zone
    ADD CONSTRAINT dns_zone_pkey PRIMARY KEY (id);

ALTER TABLE ONLY dns_zone
    ADD CONSTRAINT dns_zone_zone_key UNIQUE (zone);
```

### Record ###
```sql
CREATE SEQUENCE dns_record_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

CREATE TABLE dns_record (
    id integer DEFAULT nextval('dns_record_id_seq'::regclass) NOT NULL,
    zone_id integer NOT NULL,
    host character varying(255) DEFAULT '@'::character varying NOT NULL,
    ttl integer NOT NULL,
    type character varying(255) NOT NULL,
    mx_priority integer,
    data character varying(255) NOT NULL
);

ALTER TABLE ONLY dns_record
    ADD CONSTRAINT dns_record_pkey PRIMARY KEY (id);

CREATE INDEX dns_record_host_idx ON dns_record USING btree (host);


ALTER TABLE ONLY dns_record
    ADD CONSTRAINT dns_record_zone_id_fkey FOREIGN KEY (zone_id) REFERENCES dns_zone(id) ON UPDATE CASCADE ON DELETE CASCADE;
```

### Xfr ###
```sql
CREATE SEQUENCE dns_xfr_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

CREATE TABLE dns_xfr (
    id integer DEFAULT nextval('dns_xfr_id_seq'::regclass) NOT NULL,
    zone_id integer NOT NULL,
    client character varying(255) NOT NULL
);

ALTER TABLE ONLY dns_xfr
    ADD CONSTRAINT dns_xfr_pkey PRIMARY KEY (id);

ALTER TABLE ONLY dns_xfr
    ADD CONSTRAINT dns_xfr_zone_id_fkey FOREIGN KEY (zone_id) REFERENCES dns_zone(id) ON UPDATE CASCADE ON DELETE CASCADE;
```

### Bind9 Config ###
And then the Bind9 DLZ config, and yes, all those escape characters are strictly necessary.

```
dlz "postgres zone" {
    database "postgres 2
    {host=127.0.0.1 port=5432 dbname=bind user=bind password=__YOU_PASSWORD__}
    {SELECT \"zone\" FROM \"dns_zone\" WHERE \"zone\" = '$zone$'}
    {SELECT \"r\".\"ttl\", \"r\".\"type\", \"r\".\"mx_priority\", CASE WHEN lower(\"r\".\"type\")='txt' THEN '\"' || \"r\".\"data\" || '\"' ELSE \"r\".\"data\" END AS \"data\" FROM \"dns_record\" AS \"r\" LEFT JOIN \"dns_zone\" AS \"z\" ON \"r\".\"zone_id\" = \"z\".\"id\" WHERE lower(\"z\".\"zone\") = '$zone$' AND lower(\"r\".\"host\") = '$record$' and lower(\"r\".\"type\") <> 'ns'}
    {SELECT \"z\".\"ttl\", 'SOA' AS \"type\", \"z\".\"primary_ns\", \"z\".\"contact\", \"z\".\"serial\", \"z\".\"refresh\", \"z\".\"retry\", \"z\".\"expire\", \"z\".\"minimum\" FROM \"dns_zone\" AS \"z\" WHERE lower(\"z\".\"zone\") = '$zone$' UNION SELECT \"r\".\"ttl\", \"r\".\"type\", \"r\".\"data\", null, null, null, null, null, null FROM \"dns_record\" AS \"r\" LEFT JOIN \"dns_zone\" AS \"z\" ON \"r\".\"zone_id\" = \"z\".\"id\" WHERE lower(\"z\".\"zone\") = '$zone$' AND lower(\"r\".\"type\") = 'ns' ORDER BY \"type\" DESC}
    {SELECT \"r\".\"ttl\", \"r\".\"type\", \"r\".\"host\", \"r\".\"mx_priority\", \"r\".\"data\", null, null, null, null FROM \"dns_record\" AS \"r\" LEFT JOIN \"dns_zone\" AS \"z\" ON \"r\".\"zone_id\" = \"z\".\"id\" WHERE lower(\"z\".\"zone\") = '$zone$'}
    {SELECT 1 FROM \"dns_xfr\" AS \"x\" LEFT JOIN \"dns_zone\" AS \"z\" ON \"x\".\"zone_id\" = \"z\".\"id\" WHERE lower(\"z\".\"zone\") = '$zone$' AND lower(\"x\".\"client\") = '$client$'}";
};
```

[eve]: http://www.eveonline.com/ "EVE Online"