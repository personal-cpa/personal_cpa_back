variable "password" {
  type = string
  default = "TO_BE_FILLED"
}

variable "user" {
  type = string
  default = "application_user"
}

variable "port" {
  type = string
  default = "3306"
}

variable "database" {
  type = string
  default = "personal_cpa"
}

env "local" {
  url = "mysql://${var.user}:${var.password}@localhost:${var.port}/${var.database}"
  dir = "file://migrations"
}

env "prod" {
  url = "mysql://${var.user}:${var.password}@endpoint:${var.port}/${var.database}"
  dir = "file://migrations"
}
