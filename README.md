# GitHub ↔ Jira Webhook Automation

Automatically create Jira tickets when new comments are made on GitHub issues using a lightweight Flask webhook listener.

---

## 🧪 Step-by-Step Setup

### ✅ Step 1: Configure GitHub Webhook

1. **Go to your GitHub repository** → **Settings** → **Webhooks**
2. **Click "Add Webhook"**
3. **Set Payload URL** to:  
http://<your-ec2-public-ip>:5000/createJira

text
4. **Set Content type** to:  
application/json

text
5. **Choose "Let me select individual events"**, then check:  
Issue comment

text
6. **Click "Add Webhook"**

---

### 💻 Step 2: Create the Flask Webhook Listener

Create a file named `webhook_listener.py`:

```
import requests
from requests.auth import HTTPBasicAuth
import json
from flask import Flask, request

app = Flask(name)

@app.route('/createJira', methods=['POST'])
def createJira():
data = request.get_json()
comment_text = data['comment']['body']

text
url = "https://<your-jira-domain>.atlassian.net/rest/api/3/issue"
API_TOKEN = "<your-api-token>"

auth = HTTPBasicAuth("<your-jira-email>", API_TOKEN)
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

payload = json.dumps({
    "fields": {
        "project": { "key": "AB" },
        "summary": "New GitHub Comment Triggered Ticket",
        "description": {
            "type": "doc",
            "version": 1,
            "content": [{
                "type": "paragraph",
                "content": [{ "type": "text", "text": comment_text }]
            }]
        },
        "issuetype": { "id": "10006" }
    }
})

response = requests.post(url, headers=headers, data=payload, auth=auth)
return json.dumps(json.loads(response.text), indent=4)
if name == 'main':
app.run(host='0.0.0.0', port=5000)
```
text

> **🔐 Important:** Store sensitive data like your Jira email and token in environment variables instead of hardcoding.

---

### ☁️ Step 3: Deploy Flask App on AWS EC2

1. **SSH into your EC2 instance**
2. **Install Python and Flask:**
sudo apt update
sudo apt install python3-pip -y
pip3 install Flask requests

text
3. **Run your Flask app:**
python3 webhook_listener.py

text
> **Make sure port 5000 is open in your EC2 Security Group**

---

### 🧪 Step 4: Test It!

1. **Go to your GitHub repo**
2. **Comment on any existing issue**
3. **A Jira ticket should be automatically created using the comment content**
4. **Check logs on EC2 to confirm**

---

## 🔐 Security Best Practices

- **Validate webhook signatures from GitHub**
- **Use environment variables or AWS Secrets Manager for sensitive data**
- **Avoid logging API keys or tokens**
- **Use HTTPS in production environments**

---

## 🧱 Future Improvements

- **Format Jira descriptions with markdown or rich text**
- **Add validation, error handling, and logging**
- **Integrate Slack or Discord notifications**
- **Containerize with Docker**
- **Deploy with GitHub Actions or Terraform**

---

## 🎯 Conclusion

This project showcases a practical DevOps integration that streamlines workflows between GitHub and Jira. With minimal infrastructure and code, you’ve automated an essential project management task.

DevOps isn't just about CI/CD — it's about reducing friction across your entire pipeline. This automation helps you get one step closer.

---

## 🙌 Contribute

Have ideas? Found a bug? Want to add OAuth or Slack notifications? PRs are welcome!  
Let’s build smarter DevOps together. 💡
