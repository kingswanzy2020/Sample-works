# Data inventory, RPO and RTO

**RPO (Recovery Point Objective):** maximum acceptable data loss, measured in time.
**RTO (Recovery Time Objective):** maximum acceptable time to restore service.

Pick targets from **business impact**, then choose the strategy that meets them. Don't work backwards from the tool.

| Data store | What's in it | Can it be recreated? | Cost of 1h downtime | Cost of 1h data loss | RPO target | RTO target | Strategy | Measured RPO | Measured RTO |
|------------|--------------|----------------------|---------------------|----------------------|------------|------------|----------|--------------|--------------|
| Postgres `app` | items | No | | | | | | | |
| Terraform state (project 01) | infra mapping | Partially (import) | | | | | S3 versioning | | |
| Secrets (project 05) | credentials | Rotatable | | | | | | | |
| Grafana dashboards (project 04) | dashboards | Yes (provisioned from git) | | | | | git | | |
| Container images | app builds | Yes (rebuild from git) | | | | | registry + git | | |

## Who agreed to these numbers?

>
