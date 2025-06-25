!workspace "Complex C4 Example" "A comprehensive C4 model"
!define structurizr.groupSeparator /

!model
    !person admin "Administrator" "Manages the system"
    !person user "End User" "Uses the web and mobile apps"

    !softwareSystem ecommerce "E-Commerce System" "Handles online sales and inventory"

    group "Frontend"
        container webapp "Web Application" "JavaScript / React" "Allows users to browse and buy products"
        container mobileapp "Mobile App" "Kotlin / Swift" "Mobile version of the store"
    endgroup

    group "Backend"
        container apigateway "API Gateway" "Nginx / Node.js" "Routes requests to backend services"
        container backend "Backend Service" "Java / Spring Boot" "Handles business logic and orders"
        container database "Database" "PostgreSQL" "Stores data"
        container cache "Cache" "Redis" "Speeds up reads"
    endgroup

    group "Monitoring"
        container prometheus "Prometheus" "Monitoring"
        container grafana "Grafana" "Dashboard"
    endgroup

    !person_support support "Support Agent" "Helps users with issues"
    container crm "CRM Tool" "Salesforce" "Handles customer support"

    !rel user -> webapp "Uses"
    !rel user -> mobileapp "Uses"
    !rel webapp -> apigateway "Calls"
    !rel mobileapp -> apigateway "Calls"
    !rel apigateway -> backend "Routes to"
    !rel backend -> database "Reads from/Writes to"
    !rel backend -> cache "Reads from/Writes to"
    !rel backend -> crm "Updates customer profile"
    !rel support -> crm "Uses"
    !rel prometheus -> backend "Scrapes metrics from"
    !rel grafana -> prometheus "Queries metrics"

    !impliedRelationships true

    !tags webapp "Web"
    !tags mobileapp "Mobile"
    !tags database "Database"
    !tags backend "BusinessLogic"

!deployment
    deploymentEnvironment "Production" {
        node web_server "Web Server" "Nginx" {
            containerInstance webapp
        }
        node app_server "Application Server" "Docker Host" {
            containerInstance apigateway
            containerInstance backend
        }
        node db_server "Database Server" {
            containerInstance database
        }
        node cache_node "Cache Node" {
            containerInstance cache
        }
        node monitoring "Monitoring Stack" {
            containerInstance prometheus
            containerInstance grafana
        }
    }

!views
    systemContext ecommerce "System Context" {
        include *
        autolayout lr
    }

    container ecommerce "Containers" {
        include *
        autolayout lr
    }

    component backend "Backend Components" {
        component orderComponent "Order Component" "Handles orders"
        component paymentComponent "Payment Component" "Handles payments"
        component inventoryComponent "Inventory Component" "Manages stock"

        !rel orderComponent -> paymentComponent "Uses"
        !rel orderComponent -> inventoryComponent "Checks stock"

        !rel backend -> orderComponent "Delegates to"
        !rel backend -> paymentComponent "Delegates to"
        !rel backend -> inventoryComponent "Delegates to"

        autolayout lr
    }

    deployment ecommerce "Production Deployment" {
        include *
        autolayout lr
    }

    dynamic ecommerce "User Interaction" {
        user -> webapp "Browse items"
        webapp -> apigateway "GET /items"
        apigateway -> backend "GET /items"
        backend -> cache "Check cache"
        backend -> database "Fetch items"
        backend -> cache "Update cache"
        backend -> apigateway "Return items"
        apigateway -> webapp "Return items"
        webapp -> user "Display items"
    }

    filtered systemContext "Only Frontend" {
        include element.tag==Web
    }

!perspectives
    security {
        element backend "Must use TLS, only internal access"
        element database "Encrypted at rest"
        element apigateway "Rate-limited and authenticated"
    }

!styles
    element "Web" {
        background #1168bd
        color #ffffff
        shape RoundedBox
    }

    element "Database" {
        shape Cylinder
        background #ffcc00
    }

    element "BusinessLogic" {
        shape Hexagon
        background #28a745
    }

    relationship default {
        thickness 2
        color #707070
    }

!documentation
    workspace {
        title "E-Commerce Architecture"
        overview "This model represents a full-stack e-commerce system."
    }

    system ecommerce {
        context "This system allows users to browse and purchase items online."
    }

!decisions
    decision "Use PostgreSQL" "Using relational DB for transactional integrity" {
        status Approved
        date 2024-03-15
    }

    decision "Containerization" "Deploy backend as Docker containers" {
        status Approved
        date 2024-04-01
    }
