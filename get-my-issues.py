from dotenv import load_dotenv
import os
from jira import JIRA

# Construct the hyperlink using OSC 8 escape sequences
def get_hyperlink(url, text):
    return f"\033]8;;{url}\033\\{text}\033]8;;\033\\"

load_dotenv()

JIRA_SERVER = os.getenv('JIRA_SERVER')
JIRA_USERNAME = os.getenv('JIRA_USERNAME')
JIRA_API_TOKEN = os.getenv('JIRA_API_TOKEN')

jira = JIRA(server=JIRA_SERVER, basic_auth=(JIRA_USERNAME, JIRA_API_TOKEN))

myself = jira.myself()
print(f"Logged in as: {myself['displayName']} ({myself['emailAddress']})")

jql_query = 'assignee = currentUser() ORDER BY priority DESC'

issues = jira.search_issues(jql_query)

key_width = 15
status_width = 15

for issue in issues:
    key = get_hyperlink(issue.permalink(), issue.key).ljust(key_width)
    summary = issue.fields.summary
    status = f"{issue.fields.status.name}".ljust(status_width)
    print(f"{key}: {status} {summary}")

