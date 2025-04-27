
# Architecture diagram


```mermaid
graph LR
    

    User[/用户/]:::process --> LoadBalance(Load Balancer):::process
    LoadBalance --> ECS(ECS Cluster):::process
    ECS -.->|耗时较长任务| Lambda(Lambda):::process
    Lambda -- save result --> S3[(S3)]:::storage
    Lambda -- update status, write result url to db --> DynamoDB[(DynamoDB)]:::storage
```


# time sequence diagram 

```mermaid
sequenceDiagram
    participant User
    participant HTTPServer
    participant Lambda
    participant S3
    participant DynamoDB
    User->>HTTPServer: Submit a job
    HTTPServer->>DynamoDB: Store job information
    HTTPServer->>Lambda: Transfer the job for execution
    Lambda->>Lambda: Execute the job for N seconds
    Lambda->>S3: Write result files
    Lambda->>DynamoDB: Update job status        
```





# 改进

- lambda 最多执行15分钟，这是aws 的限制， 如果渲染时间很长， 不建议使用
- 把 yaml 拆分成多个 小的 yaml 模板，然后用 aws sam 打包 。 
- 可以考虑用 aws step function
- 可以考虑 分别 CI/CD : lambda 和 主程序
- 考虑使用 UpdatePolicy ,DeletionPolicy 