CREATE TABLE "gates" (
  "id" int PRIMARY KEY,
  "type" varchar,
  "count" int
);

CREATE TABLE "vehicles" (
  "id" int PRIMARY KEY,
  "licensePlate" varchar,
  "type" varchar,
  "status" varchar,
  "createdAt" datetime
);

CREATE TABLE "queue" (
  "id" int PRIMARY KEY,
  "vehicleId" int,
  "gateId" int,
  "calledAt" datetime,
  "status" varchar
);

ALTER TABLE "queue" ADD FOREIGN KEY ("vehicleId") REFERENCES "vehicles" ("id");

ALTER TABLE "queue" ADD FOREIGN KEY ("gateId") REFERENCES "gates" ("id");
