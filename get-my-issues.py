from dotenv import load_dotenv
import os
from jira import JIRA

# Construct the hyperlink using OSC 8 escape sequences
def get_hyperlink(url, text):
    return f"\033]8;;{url}\033\\{text}\033]8;;\033\\"


# Load environment variables
load_dotenv()
JIRA_SERVER = os.getenv('JIRA_SERVER')
JIRA_USERNAME = os.getenv('JIRA_USERNAME')
JIRA_API_TOKEN = os.getenv('JIRA_API_TOKEN')


# Log in to Jira
jira = JIRA(server=JIRA_SERVER, basic_auth=(JIRA_USERNAME, JIRA_API_TOKEN))
myself = jira.myself()
print(f"Logged in as: {myself['displayName']} ({myself['emailAddress']})")


# Query issues assigned to user
jql_query = 'assignee = currentUser() ORDER BY priority DESC'
issues = jira.search_issues(jql_query, maxResults=1000)


# Order issues by status name
status_order = {
    "BACKLOG": 0,
    "TO DO": 1,
    "IN PROGRESS": 2,
    "MERGED": 3,
    "QA": 4,
    "DONE": 5,
    "REJECTED": 6
}
issues = sorted(issues, key=lambda issue: status_order.get(issue.fields.status.name.upper(), 100))


# Pretty print result
key_width = 15
status_width = 15

for issue in issues:
    key = get_hyperlink(issue.permalink(), issue.key).ljust(key_width)
    summary = issue.fields.summary
    status = f"{issue.fields.status.name}".ljust(status_width)
    print(f"{key}: {status} {summary}")

