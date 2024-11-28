from dotenv import load_dotenv
import os
from jira import JIRA

load_dotenv()

JIRA_SERVER = os.getenv('JIRA_SERVER')
JIRA_USERNAME = os.getenv('JIRA_USERNAME')
JIRA_API_TOKEN = os.getenv('JIRA_API_TOKEN')

jira = JIRA(server=JIRA_SERVER, basic_auth=(JIRA_USERNAME, JIRA_API_TOKEN))

myself = jira.myself()
print(f"Logged in as: {myself['displayName']} ({myself['emailAddress']})")

jql_query = 'assignee = currentUser() ORDER BY priority DESC'

issues = jira.search_issues(jql_query)

for issue in issues:
    print(f"{issue.key}: {issue.fields.summary} (Status: {issue.fields.status.name})")

