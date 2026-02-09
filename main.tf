terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0.2"
    }
  }
}

provider "docker" {
  host = "npipe:////./pipe/docker_engine"
}


# --- Réseau ---
resource "docker_network" "project_network" {
  name   = "my_project_network"
  driver = "bridge"
}

# --- Service Auth ---
resource "docker_image" "auth_image" {
  name         = "auth-service-image"
  build {
    context    = "${path.cwd}/auth_service"
  }
}

resource "docker_container" "auth" {
  name  = "auth-service"
  image = docker_image.auth_image.name

  env = [
    "SERVICE_NAME=auth",
    "ARTICLE_SERVICE_URL=http://article-service:5001/article_page"
  ]

  ports {
    internal = 5000
    external = 5000
  }

  networks_advanced {
    name = docker_network.project_network.name
  }

  depends_on = [
    docker_container.article
  ]
}

# --- Service Article ---
resource "docker_image" "article_image" {
  name = "article-service-image"
  build {
    context = "${path.cwd}/article_service"
  }
}

resource "docker_container" "article" {
  name  = "article-service"
  image = docker_image.article_image.name

  env = [
    "SERVICE_NAME=article"
  ]

  ports {
    internal = 5001
    external = 5001
  }

  networks_advanced {
    name = docker_network.project_network.name
  }
}

# --- Service Banque ---
resource "docker_image" "banque_image" {
  name = "banque-service-image"
  build {
    context = "${path.cwd}/banque_service"
  }
}

resource "docker_container" "banque" {
  name  = "banque-service"
  image = docker_image.banque_image.name

  env = [
    "SERVICE_NAME=banque"
  ]

  ports {
    internal = 5003
    external = 5003
  }

  networks_advanced {
    name = docker_network.project_network.name
  }
}

# --- Service Panier / Gateway Front ---
resource "docker_image" "panier_image" {
  name = "panier-service-image"
  build {
    context = "${path.cwd}/gateway_front"
  }
}

resource "docker_container" "panier" {
  name  = "panier-service"
  image = docker_image.panier_image.name

  env = [
    "SERVICE_NAME=panier"
  ]

  ports {
    internal = 5002
    external = 5002
  }

  networks_advanced {
    name = docker_network.project_network.name
  }
}
