# Subreddit Map

Used by `scripts/fetch.py` to auto-detect relevant subreddits from the category keyword.

---

## Category to Subreddit Mapping

| Category Keyword | Subreddits |
|---|---|
| devops | r/devops, r/sysadmin, r/aws, r/kubernetes, r/docker |
| observability | r/devops, r/sysadmin, r/dataengineering, r/CloudArchitects |
| monitoring | r/devops, r/sysadmin, r/networking, r/aws |
| analytics | r/analytics, r/dataengineering, r/datascience, r/BusinessIntelligence |
| b2b | r/startups, r/entrepreneur, r/SaaS, r/smallbusiness |
| saas | r/SaaS, r/startups, r/entrepreneur, r/microsaas |
| developer | r/programming, r/webdev, r/ExperiencedDevs, r/devops |
| developer tools | r/programming, r/webdev, r/devops, r/ExperiencedDevs |
| api | r/webdev, r/programming, r/devops, r/node |
| security | r/netsec, r/cybersecurity, r/devops, r/sysadmin |
| data | r/dataengineering, r/datascience, r/analytics, r/BusinessIntelligence |
| database | r/dataengineering, r/Database, r/PostgreSQL, r/learnprogramming |
| auth | r/webdev, r/programming, r/netsec, r/node |
| payments | r/webdev, r/programming, r/entrepreneur, r/ecommerce |
| ecommerce | r/ecommerce, r/entrepreneur, r/shopify, r/startups |
| marketing | r/marketing, r/digital_marketing, r/entrepreneur, r/startups |
| crm | r/sales, r/salesforce, r/entrepreneur, r/smallbusiness |
| sales | r/sales, r/entrepreneur, r/startups, r/smallbusiness |
| hr | r/humanresources, r/remotework, r/startups, r/smallbusiness |
| finance | r/personalfinance, r/accounting, r/startups, r/smallbusiness |
| healthcare | r/healthIT, r/medicine, r/startups, r/technology |
| ai | r/MachineLearning, r/artificial, r/ChatGPT, r/learnmachinelearning |
| ml | r/MachineLearning, r/learnmachinelearning, r/datascience, r/artificial |
| llm | r/MachineLearning, r/artificial, r/ChatGPT, r/LocalLLaMA |

---

## Fallback (no category match)

If no keywords match: use `r/programming`, `r/webdev`, `r/technology`, `r/startups`, `r/entrepreneur`.

---

## Inference from Competitor Names

If competitor names are provided but no category:

| Competitor keyword | Inferred subreddits |
|---|---|
| data, log, metric, monitor, trace | observability subreddits |
| pay, stripe, billing | payments subreddits |
| db, sql, postgres, mongo | database subreddits |

---

## Cap: 8 subreddits maximum per run

Too many subreddits increases noise and request count. Cap at 8, prioritizing the highest-specificity match.
