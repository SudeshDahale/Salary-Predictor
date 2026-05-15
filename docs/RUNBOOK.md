### Operational Runbook for SudeshDahale/Salary-Predictor
#### 1. Service Overview and SLOs
The Salary-Predictor service is a Python-based application that provides salary prediction functionality. The service has three primary functions:
* `health`: Checks the service's health status
* `metadata`: Returns metadata about the service
* `predict`: Predicts salary based on input parameters

The service has the following Service Level Objectives (SLOs):
* Availability: 99.9%
* Latency: 500ms (average response time)
* Throughput: 100 requests per second

#### 2. Local Development Setup
To set up the service for local development:
1. Clone the repository: `git clone https://github.com/SudeshDahale/Salary-Predictor.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Run the service: `python app.py`
4. Access the service: `http://localhost:5000`

![Local Development Setup](https://i.imgur.com/6xWVxLQ.png)

#### 3. Deployment Procedure
The deployment procedure involves the following steps:
1. **Build**: Build the Docker image using the `Dockerfile`
```dockerfile
docker build -t salary-predictor .
```
2. **Push**: Push the image to the container registry
```dockerfile
docker tag salary-predictor:latest <registry-url>/salary-predictor:latest
docker push <registry-url>/salary-predictor:latest
```
3. **Deploy**: Deploy the service to the production environment using Kubernetes
```yml
kubectl apply -f deployment.yaml
```
4. **Verify**: Verify the service is running and accessible
```bash
kubectl get pods
kubectl logs -f <pod-name>
```

![Deployment Procedure](https://i.imgur.com/VL7xLpQ.png)

#### 4. Rollback Procedure
To rollback to a previous version:
1. **Identify**: Identify the previous version to rollback to
2. **Update**: Update the `deployment.yaml` file to reference the previous version
```yml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: salary-predictor
spec:
  replicas: 3
  selector:
    matchLabels:
      app: salary-predictor
  template:
    metadata:
      labels:
        app: salary-predictor
    spec:
      containers:
      - name: salary-predictor
        image: <registry-url>/salary-predictor:<previous-version>
        ports:
        - containerPort: 5000
```
3. **Apply**: Apply the updated `deployment.yaml` file
```bash
kubectl apply -f deployment.yaml
```
4. **Verify**: Verify the service is running and accessible

#### 5. Common Failure Modes and Remediation
The following are common failure modes and remediation steps:
* **Container crashes**: Restart the container
```bash
kubectl rollout restart deployment salary-predictor
```
* **Network issues**: Check the network configuration and restart the pod
```bash
kubectl delete pod <pod-name>
```
* **Database connection issues**: Check the database connection string and restart the pod
```bash
kubectl delete pod <pod-name>
```

#### 6. Monitoring and Alerting Checklist
The following are monitoring and alerting checks:
* **CPU usage**: Alert when CPU usage exceeds 80%
* **Memory usage**: Alert when memory usage exceeds 80%
* **Request latency**: Alert when average request latency exceeds 1s
* **Error rate**: Alert when error rate exceeds 5%

![Monitoring and Alerting Checklist](https://i.imgur.com/3xWVxLQ.png)

#### 7. On-call Escalation Path
The on-call escalation path is as follows:
1. **Primary on-call**: The primary on-call engineer is responsible for responding to alerts and resolving issues
2. **Secondary on-call**: The secondary on-call engineer is responsible for providing support to the primary on-call engineer
3. **Engineering team**: The engineering team is responsible for providing support and resolving complex issues

![On-call Escalation Path](https://i.imgur.com/6xWVxLQ.png)