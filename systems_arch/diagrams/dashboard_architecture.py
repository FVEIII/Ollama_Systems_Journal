from diagrams import Diagram, Cluster
from diagrams.aws.network import APIGateway
from diagrams.onprem.compute import Server
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.client import User

# Output location for the PNG
OUTPUT_PATH = "systems_arch/diagrams/analytics_dashboard_architecture"

with Diagram(
    name="Analytics Dashboard Architecture",
    filename=OUTPUT_PATH,
    outformat="png",
    show=False,
    direction="LR",  # Left-to-right layout
):
    # External client
    browser = User("Browser")

    # Edge Layer
    with Cluster("Edge Layer"):
        gateway = APIGateway("API Gateway (ADR-001)")

    # Services Layer (vertically aligned)
    with Cluster("Services Layer"):
        users = Server("Users Service")
        analytics = Server("Analytics Service")

    # Data Layer (perfect vertical alignment)
    with Cluster("Data Layer"):
        cache = Redis("Redis Cache (ADR-003)")
        db_primary = PostgreSQL("Postgres - Primary (ADR-002)")
        db_replica = PostgreSQL("Postgres - Replica (ADR-002)")

    # Connections (clean order, minimal crossovers)
    browser >> gateway
    gateway >> users
    gateway >> analytics

    analytics >> cache
    analytics >> db_replica
    analytics >> db_primary

    users >> db_primary
