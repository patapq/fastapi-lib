ui = true

listener "tcp" {
  address     = "0.0.0.0:8201"
  tls_disable = 1
}

storage "file" {
  path = "/vault/file"
}

api_addr = "http://127.0.0.1:8201"

disable_mlock = "true"