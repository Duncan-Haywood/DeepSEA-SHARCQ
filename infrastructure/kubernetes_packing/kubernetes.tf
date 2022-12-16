resource "kubernetes_deployment" "fastapi" {
  metadata {
    name = "fastapi"
    labels = {
      App = "FastAPI"
    }
  }

  spec {
    replicas = 2
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
          image = "nginx:1.7.8"
          name  = "fastapi"

          port {
            container_port = 80
          }

          resources {
            limits = {
              cpu    = "0.5"
              memory = "512Mi"
            }
            requests = {
              cpu    = "250m"
              memory = "50Mi"
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

