resource "kubernetes_deployment" "fastapi" {
  metadata {
    name = "fastapi"
    labels = {
      App = "FastAPI"
    }
  }

  spec {
    replicas = 1
    selector {
      match_labels = {
        App = "FastAPI"
      }
    }
    template {
      metadata {
        labels = {
          App = "FastAPI"
        }
      }
      spec {
        container {
          image = var.ecr_url
          name  = "fastapi"

          port {
            container_port = 80
          }

          resources {
            limits = {
              cpu    = "1"
              memory = "2048Mi"
            }
            requests = {
              cpu    = "250m"
              memory = "256Mi"
            }
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "fastapi" {
  metadata {
    name = "fastapi"
  }
  spec {
    selector = {
      App = kubernetes_deployment.fastapi.spec.0.template.0.metadata[0].labels.App
    }
    port {
      port        = 80
      target_port = 80
    }

    type = "LoadBalancer"
  }
}
output "lb_ip" {
  value = kubernetes_service.fastapi.status.0.load_balancer.0.ingress.0.hostname
}

