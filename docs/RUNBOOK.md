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
3. Run the service: `python backend/app.py`
4. Access the service: `http://localhost:5000`

![Local Development Setup](https://i.imgur.com/4KqfzRr.png)

#### 3. Deployment Procedure
**Step-by-Step Deployment:**
1. **Build the Docker image**: `docker build -t salary-predictor .`
2. **Push the image to the registry**: `docker push <registry-url>/salary-predictor:latest`
3. **Deploy to Kubernetes**: `kubectl apply -f deployment.yaml`
4. **Verify deployment**: `kubectl get pods`

```yml
# deployment.yaml
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
        image: <registry-url>/salary-predictor:latest
        ports:
        - containerPort: 5000
```

![Deployment Architecture](https://i.imgur.com/8KqfzRr.png)

#### 4. Rollback Procedure
**Step-by-Step Rollback:**
1. **Identify the previous version**: `kubectl get deployments -o yaml | grep image`
2. **Update the deployment**: `kubectl set image deployment/salary-predictor salary-predictor=<registry-url>/salary-predictor:<previous-version>`
3. **Verify rollback**: `kubectl get pods`

#### 5. Common Failure Modes and Remediation
* **Failure Mode 1: Service Unavailable**
	+ Symptoms: 503 Service Unavailable error
	+ Remediation: Check the service logs for errors, restart the service if necessary
* **Failure Mode 2: High Latency**
	+ Symptoms: Average response time exceeds 500ms
	+ Remediation: Check the service logs for errors, optimize the service for performance if necessary

#### 6. Monitoring and Alerting Checklist
* **Metrics to Monitor:**
	+ Request latency
	+ Request throughput
	+ Error rate
* **Alerting Thresholds:**
	+ Latency: 500ms (average response time)
	+ Throughput: 100 requests per second
	+ Error rate: 1%

![Monitoring Dashboard](https://i.imgur.com/6KqfzRr.png)

#### 7. On-Call Escalation Path
* **Primary On-Call:**
	+ Name: John Doe
	+ Email: [john.doe@example.com](mailto:john.doe@example.com)
	+ Phone: 123-456-7890
* **Secondary On-Call:**
	+ Name: Jane Doe
	+ Email: [jane.doe@example.com](mailto:jane.doe@example.com)
	+ Phone: 987-654-3210

![On-Call Escalation Path](https://i.imgur.com/7KqfzRr.png)