variable "region" {
  default = "ap-southeast-2"
}

provider "aws" {
  region = "${var.region}"
}

module "catbot" {
  source      = "slash_command"
  name        = "catbot"
  region      = "${var.region}"
  source_code = "catbot.zip"
}

output "command_url" {
  value = "${module.catbot.command_url}"
}
