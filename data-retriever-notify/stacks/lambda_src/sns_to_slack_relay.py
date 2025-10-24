import json, os, urllib.request, boto3

secrets = boto3.client("secretsmanager")

def _get_webhook():
    """Fetch Slack webhook from Secrets Manager."""
    secret_name = os.environ["SLACK_SECRET_NAME"]
    resp = secrets.get_secret_value(SecretId=secret_name)
    s = resp.get("SecretString")
    j = json.loads(s) if s and s.startswith("{") else {"WEBHOOK_URL": s}
    return j["WEBHOOK_URL"]

WEBHOOK_URL = None

def post_to_slack(payload):
    global WEBHOOK_URL
    if WEBHOOK_URL is None:
        WEBHOOK_URL = _get_webhook()
    req = urllib.request.Request(
        WEBHOOK_URL,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    urllib.request.urlopen(req)

def format_console_link(region, cluster_arn, task_arn):
    """Generate direct link to ECS task in AWS console."""
    return f"https://{region}.console.aws.amazon.com/ecs/v2/clusters/{cluster_arn.split('/')[-1]}/tasks/{task_arn.split('/')[-1]}/details"

def lambda_handler(event, context):
    for record in event.get("Records", []):
        msg = record["Sns"]["Message"]
        try:
            detail = json.loads(msg).get("detail", {})
        except Exception:
            detail = {}

        region = os.environ.get("AWS_REGION", "us-east-1")
        cluster_arn = detail.get("clusterArn", "N/A")
        task_arn = detail.get("taskArn", "N/A")
        last_status = detail.get("lastStatus", "N/A")
        stopped_reason = detail.get("stoppedReason", "N/A")
        containers = detail.get("containers", [])
        first = containers[0] if containers else {}
        exit_code = first.get("exitCode", -1)
        reason = first.get("reason", "N/A")

        is_success = (exit_code == 0)
        title = "Data Retriever Succeeded" if is_success else "Data Retriever Failed"
        color = "#36a64f" if is_success else "#ff0000"

        text = "\n".join([
            f"*Task:* `{task_arn}`",
            f"*Status:* `{last_status}`",
            f"*Exit Code:* `{exit_code}`",
            f"*Reason:* `{reason}`",
            f"*Stopped Reason:* `{stopped_reason}`",
            f"*Console:* {format_console_link(region, cluster_arn, task_arn)}",
        ])

        payload = {"attachments": [{"color": color, "title": title, "text": text}]}
        post_to_slack(payload)

    return {"ok": True}
