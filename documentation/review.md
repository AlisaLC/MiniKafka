### Review Documentation

#### 1. Introduction
This is the retro documentation for the MiniKafka Project for the course "Systems 
Analysis & Design" at Sharif University of Technology, Fall 1402. This document will
contain the information reviewing the whole project goal and purpose.

#### 2. Team Members


- Ali Salesi
- Soroush Sherafat
- Amirhossein Barati
- Arad Maleki

#### 2. Overview
The main goal of the MiniKafka project is to build a Message Queue that supports
high-throughput, fault-tolerant handling of messages across distributed systems. 
By offering client code in both Python and Go, MiniKafka ensures a broad accessibility 
for developers working in different programming environments. The project emphasizes
simplicity in deployment and scalability, allowing systems to efficiently process and 
manage large volumes of messages. In the next sections, we will explain the architectural 
overview of the components of the project in details.

#### 3. Architecture Overview
MiniKafka's architecture is designed to be lightweight and modular, consisting of 
several key components:


- Client Code: Available in Python and Go, allowing applications to produce and consume
messages seamlessly.
- Gateway: Acts as the communication facilitator between clients and the MiniKafka ecosystem,
specifically with Zookeeper, to manage cluster metadata and broker coordination.
- Zookeeper: Utilized for managing and coordinating the MiniKafka brokers, ensuring high 
availability and fault tolerance within the message queuing system.
- Brokers: The backbone of the MiniKafka system, responsible for the storage, replication,
and retrieval of messages, thereby fulfilling the project's primary objective of efficient
message queuing.

#### 4. Design Principles
The design of MiniKafka is guided by several core principles:

- Simplicity: Aiming to reduce the complexity inherent in distributed messaging systems, 
MiniKafka emphasizes ease of use and straightforward deployment.
- Scalability: With a modular architecture, MiniKafka can scale horizontally, adding more 
brokers to the system as needed to increase throughput and storage capacity.
- Fault Tolerance: Ensuring the reliability of message processing and storage, even in the 
face of system failures.

#### 5. Consensus and Replication
To maintain consistency across the distributed system, MiniKafka employs a hashring algorithm
for consensus among brokers. This approach efficiently maps data to brokers, facilitating 
balanced load distribution and streamlined data lookup.

For replication and fault tolerance, MiniKafka introduces a novel strategy by organizing brokers
in a chain, akin to a circular linked list. Each broker in the chain holds a copy of the messages
from the previous broker, creating a redundant storage mechanism that enhances data durability. 
This design ensures that, should any single broker fail, there is no loss of data, as the subsequent
broker in the chain holds a replica of the lost messages. This replication strategy serves two primary
functions:

- Data Redundancy: By storing copies of messages across multiple brokers, MiniKafka safeguards against
data loss, a critical feature for ensuring the reliability of the messaging system.
- Fault Recovery: In the event of a broker failure, the system can automatically recover by rerouting
message traffic to the next broker in the chain, minimizing downtime and maintaining continuous operation.

#### 6. Additional Tools 
This section delves into the core aspects of MiniKafka's operational capabilities, including the CI/CD 
pipeline, monitoring, and logging mechanisms.

- CI/CD Pipeline:
MiniKafka incorporates a Continuous Integration and Continuous Deployment (CI/CD) pipeline 
leveraging GitHub Actions. This automated pipeline facilitates the seamless integration of new code 
contributions, ensuring that every change is automatically built and tested before being merged into 
the main codebase. Furthermore, the CI/CD process enables the automated deployment of the latest version 
of MiniKafka, ensuring that users always have access to the most recent features and fixes. This approach
significantly reduces the potential for human error during deployment and accelerates the development 
cycle.
- Monitoring and Logging: For comprehensive system monitoring, MiniKafka utilizes Prometheus and Grafana. 
Prometheus is responsible for collecting and storing metrics related to the performance and health of the 
MiniKafka system. Grafana, in turn, provides a powerful visualization platform, allowing users to create 
dashboards that display these metrics in real-time. This setup offers insights into various aspects of the
system, including but not limited to:
    - Throughput: Measures the rate at which messages are produced and consumed within the system.
    - Latency: Tracks the time taken for messages to be processed and delivered to consumers.
    - System Health: Monitors the status of individual components within the MiniKafka architecture, 
  including brokers and the gateway.

#### 7. Limitations
While MiniKafka offers functionalities designed to meet the needs of most messaging system users, 
it is important to acknowledge the project's current limitations. One significant limitation identified 
is the system's untested resilience against the simultaneous failure of two or more nodes. Preliminary 
analysis suggests that such an event could potentially lead to a data leak within the system, as the 
chain replication model may not adequately cover the redundancy needed to prevent data loss in this 
scenario. This limitation highlights an area for future research and development, aiming to enhance the
fault tolerance of MiniKafka further.

#### 8. Conclusion

The project is a step forward in creating an easy-to-use, effective, and scalable way to 
manage messages, With features like automatic code updates, thorough monitoring with Prometheus
and Grafana, and a smart way to keep data safe.
