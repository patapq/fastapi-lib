# fastapi-lib
Run raw python app
```
cd app/ 
python3 -m venv myenv
source myenv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Deploy GitLab Runner to Minikube using the Helm Chart

```
helm repo add gitlab https://charts.gitlab.io
helm repo update gitlab
helm install --namespace do-5-libcor gitlab-runner -f values.yaml gitlab/gitlab-runner
```
