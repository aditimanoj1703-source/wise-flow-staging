# Learning Schedule: SQL, PostgreSQL & Vertica

An 8-week, self-paced schedule to go from SQL fundamentals to working
proficiency in PostgreSQL and Vertica. Assumes roughly 5-7 hours/week
(~1 hour on weekdays, longer sessions on weekends). Adjust pace as needed.

## How this is organized

- **Weeks 1-2**: Core SQL fundamentals (portable across databases)
- **Weeks 3-5**: PostgreSQL — setup, features, performance, administration
- **Weeks 6-7**: Vertica — columnar/MPP concepts, architecture, migration from Postgres knowledge
- **Week 8**: Applied project + review

---

## Week 1 — SQL Fundamentals I

| Day | Topic | Practice |
|-----|-------|----------|
| Mon | SELECT, WHERE, ORDER BY, LIMIT | Query a sample dataset (e.g. `pagila` or `dvdrental`) |
| Tue | Filtering: `IN`, `BETWEEN`, `LIKE`, `NULL` handling | Write 10 filter queries |
| Wed | Aggregate functions: `COUNT`, `SUM`, `AVG`, `MIN`, `MAX` | Build summary reports |
| Thu | `GROUP BY` and `HAVING` | Group sales/orders by category |
| Fri | Joins: `INNER`, `LEFT`, `RIGHT`, `FULL` | Join 3+ related tables |
| Sat/Sun | Review + exercises (e.g. SQLZoo, LeetCode SQL easy set) | 8-10 problems |

## Week 2 — SQL Fundamentals II

| Day | Topic | Practice |
|-----|-------|----------|
| Mon | Subqueries (scalar, correlated, `EXISTS`) | Rewrite joins as subqueries and vice versa |
| Tue | Common Table Expressions (`WITH`) | Refactor nested subqueries into CTEs |
| Wed | Window functions: `ROW_NUMBER`, `RANK`, `LAG`/`LEAD` | Running totals, top-N per group |
| Thu | Set operations: `UNION`, `INTERSECT`, `EXCEPT`; `CASE` expressions | Combine and reshape result sets |
| Fri | Data modeling basics: normalization, keys, constraints | Sketch a small ER diagram |
| Sat/Sun | Mixed review problems (medium difficulty) | 8-10 problems |

## Week 3 — PostgreSQL Foundations

| Day | Topic | Practice |
|-----|-------|----------|
| Mon | Install PostgreSQL locally (or Docker), `psql` basics | Create a database, connect via `psql` |
| Tue | Data types (`numeric`, `text`, `jsonb`, `array`, `uuid`, `timestamptz`) | Design a table using varied types |
| Wed | DDL: `CREATE TABLE`, constraints, `ALTER TABLE` | Build a small schema (3-5 tables) |
| Thu | DML: `INSERT`, `UPDATE`, `DELETE`, `UPSERT` (`ON CONFLICT`) | Load sample data, practice upserts |
| Fri | Indexes: B-tree, unique, partial, expression indexes | Add indexes and compare query plans |
| Sat/Sun | Project: model a small app's schema end-to-end | Users/orders/products style schema |

## Week 4 — PostgreSQL Deep Dive

| Day | Topic | Practice |
|-----|-------|----------|
| Mon | `EXPLAIN` / `EXPLAIN ANALYZE`, query planning | Diagnose a slow query |
| Tue | Transactions, isolation levels, locking | Simulate concurrent updates |
| Wed | Views, materialized views | Create a reporting view |
| Thu | Stored procedures & functions (PL/pgSQL) | Write a simple function/trigger |
| Fri | `jsonb` querying, full-text search basics | Query semi-structured data |
| Sat/Sun | Practice: optimize 3-5 slow queries from your project | Use `EXPLAIN ANALYZE` throughout |

## Week 5 — PostgreSQL Administration & Performance

| Day | Topic | Practice |
|-----|-------|----------|
| Mon | Roles, permissions, `GRANT`/`REVOKE` | Set up read-only vs. admin roles |
| Tue | Backup/restore (`pg_dump`, `pg_restore`), replication basics | Practice a dump/restore cycle |
| Wed | Partitioning (range/list/hash) | Partition a large table |
| Thu | `VACUUM`, `ANALYZE`, autovacuum tuning | Inspect bloat, run manual vacuum |
| Fri | Connection pooling (PgBouncer), config tuning basics | Read through `postgresql.conf` key settings |
| Sat/Sun | Review + PostgreSQL certification-style quiz | Self-test on weeks 3-5 |

## Week 6 — Vertica Foundations

| Day | Topic | Practice |
|-----|-------|----------|
| Mon | Vertica overview: columnar storage vs. row storage (vs. Postgres) | Read architecture overview docs |
| Tue | MPP architecture: nodes, segmentation, projections | Diagram how a query is distributed |
| Wed | Projections: superprojections, buddy projections, design | Create a custom projection |
| Thu | Loading data: `COPY`, batch loading, flex tables | Bulk load a CSV dataset |
| Fri | SQL dialect differences from Postgres (functions, syntax quirks) | Port 5 queries from Postgres to Vertica |
| Sat/Sun | Practice: rebuild your Week 3 schema in Vertica | Compare DDL/behavior differences |

## Week 7 — Vertica Performance & Operations

| Day | Topic | Practice |
|-----|-------|----------|
| Mon | Query optimization: `EXPLAIN`, profiling queries | Analyze a query plan |
| Tue | Encoding & compression strategies | Apply encoding types to columns |
| Wed | Partitioning and segmentation strategy | Partition a fact table |
| Thu | Workload management, resource pools | Read about resource pool tuning |
| Fri | Database Designer tool, `DBD` recommendations | Run designer on sample workload |
| Sat/Sun | Review: compare Postgres vs. Vertica decision points | Write notes on when to use which |

## Week 8 — Applied Project & Review

| Day | Focus |
|-----|-------|
| Mon-Tue | Pick a dataset (e.g. sales, logs); load into both Postgres and Vertica |
| Wed-Thu | Write the same 10-15 analytical queries against both; compare plans and performance |
| Fri | Document key differences (use cases, performance, tooling) in a short write-up |
| Sat/Sun | Final review: redo hardest exercises from weeks 1-7, fill gaps |

---

## Suggested Resources

- **SQL practice**: SQLZoo, Mode SQL Tutorial, LeetCode/HackerRank SQL tracks
- **PostgreSQL**: official docs (postgresql.org/docs), "PostgreSQL Exercises" (pgexercises.com), *PostgreSQL: Up and Running*
- **Vertica**: official Vertica documentation (docs.vertica.com), Vertica Academy free courses
- **Sample datasets**: `dvdrental`/`pagila` (Postgres), any public CSV dataset for bulk-load practice

## Tracking Progress

Check off each week as you complete it:

- [ ] Week 1 — SQL Fundamentals I
- [ ] Week 2 — SQL Fundamentals II
- [ ] Week 3 — PostgreSQL Foundations
- [ ] Week 4 — PostgreSQL Deep Dive
- [ ] Week 5 — PostgreSQL Administration & Performance
- [ ] Week 6 — Vertica Foundations
- [ ] Week 7 — Vertica Performance & Operations
- [ ] Week 8 — Applied Project & Review
