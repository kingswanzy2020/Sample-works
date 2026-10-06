vault {
  address = "http://vault:8200"
}

auto_auth {
  method "token_file" {
    config = {
      token_file_path = "/token/agent-token"
    }
  }
}

template {
  destination = "/secrets/database_url"
  perms       = "0644"
  contents    = <<EOT
{{ with secret "database/creds/app" }}postgresql://{{ .Data.username }}:{{ .Data.password }}@db:5432/app{{ end }}
EOT
}
