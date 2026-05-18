# Worked Examples

This file provides 3 worked examples showing how the skill interprets different types of job posts. The agent reads this file to calibrate its analysis quality.

---

## Example 1: High Signal, High ICP Fit

### Input

**Product brief:** "Metabase — open-source BI tool that lets non-technical teams query data and build dashboards without SQL. Target: Series A–C startups with growing data teams."

**ICP description:** "B2B SaaS companies, 50–500 employees, Series A–C, have at least 2 data engineers, use modern data stack (dbt, Snowflake, BigQuery), need self-serve analytics for business teams."

**Job post:**
```json
{
  "company_name": "Acme Analytics",
  "job_title": "Senior Data Platform Engineer",
  "location": "Remote, US",
  "seniority": "Senior / IC",
  "team_or_function": "Data Platform / Infra",
  "job_description_text": "We're looking for a Senior Data Platform Engineer to own our analytics infrastructure. You'll build a self-serve analytics layer so product managers and business leads can access metrics without pinging the data team. Responsibilities: own ETL pipelines and dbt transformations, optimize query performance for our BI tools, partner with 6+ internal teams to define metrics, and ensure data reliability for executive dashboards. Requirements: 5+ years with modern data stack (Snowflake, dbt, Airflow), experience building self-serve data products, strong SQL. We are a Series B company with 120 employees scaling rapidly."
}
```

### Expected Output

**Summary:**
- Headline: "Staffing data infra to unblock self-serve analytics for non-technical teams"
- Overall score: 87
- Signal strength: 9 (explicit analytics pain + modern data stack + building self-serve layer)
- Urgency: 8 (partnering with 6+ teams suggests backlog, "scaling rapidly")
- ICP fit: 9 (Series B, 120 employees, dbt + Snowflake, self-serve analytics need)
- Stage guess: Scaling post-PMF
- Buy-vs-build: Hybrid (buy-and-build)
  - _Reasoning: building infrastructure + likely to buy BI tooling_

**Primary pain:** "Data team is a bottleneck for business teams needing metrics access. PMs and leads are blocked by ad-hoc data requests."

**Evidence cited:** "product managers and business leads can access metrics without pinging the data team", "partner with 6+ internal teams"

**Outreach angle:** "Reduce ad-hoc data fire drills — lead with how Metabase gives PMs self-serve dashboards so the data team stops being a ticket queue."

---

## Example 2: Low Signal, Generic Post

### Input

**Product brief:** "Ramp — sales onboarding platform for B2B SaaS. Helps VP Sales cut new-rep ramp time."

**ICP description:** "B2B SaaS, 100–1000 employees, at least 10 sales reps, hiring SDRs/AEs, series B+."

**Job post:**
```json
{
  "company_name": "CoolStartup Inc",
  "job_title": "Full Stack Engineer",
  "location": "San Francisco, CA",
  "seniority": "Mid-level / IC",
  "team_or_function": "Engineering",
  "job_description_text": "We're looking for a rockstar full-stack engineer who loves building cool things. You'll work on our product using React, Node.js, and PostgreSQL. Must be a team player who thrives in a fast-paced startup environment. We offer competitive salary, equity, unlimited PTO, and weekly team lunches. Come join our amazing culture!"
}
```

### Expected Output

**Summary:**
- Headline: "Generic engineering hire with no relevant GTM or sales signals"
- Overall score: 16
- Signal strength: 1 (no sales, onboarding, or GTM signals; engineering role unrelated to product area)
- Urgency: 2 (no urgency language, exploratory tone)
- ICP fit: 2 (no company size, no sales team indicators, no relevant function)
- Stage guess: Unknown (no indicators)
- Buy-vs-build: Unknown

**Primary pain:** None identified. Post is too generic to infer operational pain relevant to sales onboarding.

**Note to user:** "This post contains minimal signal for your ICP. The role is a general engineering hire with no references to sales operations, onboarding, or GTM infrastructure. Recommend skipping."

---

## Example 3: Decent Pain, Out-of-ICP

### Input

**Product brief:** "Datadog — monitoring and observability platform for cloud-native applications. Target: tech companies running Kubernetes in production."

**ICP description:** "Cloud-native tech companies, 200+ engineers, running Kubernetes/containers, multi-cloud, Series C+ or public."

**Job post:**
```json
{
  "company_name": "MedSecure Health Systems",
  "job_title": "Director of Cloud Infrastructure",
  "location": "Chicago, IL",
  "seniority": "Director / Leadership",
  "team_or_function": "IT Infrastructure",
  "job_description_text": "MedSecure Health Systems is seeking a Director of Cloud Infrastructure to lead our cloud migration initiative. You will oversee the transition of 200+ on-premise applications to AWS, build container orchestration capabilities, and establish monitoring and observability practices from scratch. Manage a team of 8 infrastructure engineers. Requirements: 10+ years in infrastructure, experience with AWS, Terraform, container orchestration (Kubernetes preferred), HIPAA compliance expertise required. We are a 2,000-employee healthcare technology company."
}
```

### Expected Output

**Summary:**
- Headline: "Healthcare company building cloud infra and observability from scratch"
- Overall score: 62
- Signal strength: 8 (Director-level, building observability from scratch, Kubernetes, AWS migration)
- Urgency: 7 (200+ app migration, building from scratch, leadership hire)
- ICP fit: 3 (healthcare, not cloud-native tech company; on-prem migrating to cloud, not cloud-native)
- Stage guess: Mature / Enterprise
- Buy-vs-build: Leaning buy
  - _Reasoning: "establish monitoring and observability practices from scratch" suggests they need to adopt tooling_

**Primary pain:** "No monitoring or observability stack exists. Migrating 200+ on-prem apps to AWS with zero cloud-native visibility."

**Evidence cited:** "establish monitoring and observability practices from scratch", "transition of 200+ on-premise applications to AWS"

**ICP flag:** ⚠️ Outside core ICP — healthcare vertical, on-prem migrating (not cloud-native). Pain is real and product-relevant, but company profile does not match ideal customer profile. Consider deprioritizing unless healthcare is an expansion segment.

**Outreach angle:** "If pursued: lead with migration observability — reference the 200-app migration and offer a proof-of-value on the first 10 apps moved to AWS."
