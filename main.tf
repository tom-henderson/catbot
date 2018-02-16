variable "region" {
  default = "ap-southeast-2"
}

provider "aws" {
  region = "${var.region}"
}

module "catbot" {
  source      = "github.com/tom-henderson/terraform-modules//slash-command"
  name        = "catbot"
  region      = "${var.region}"
  source_code = "catbot.zip"
  module_name = "catbot"

  ssm_parameters = ["catbot_slash_command_token"]

  environment_variables = {
    token_parameter = "catbot_slash_command_token"
  }
}

output "command_url" {
  value = "${module.catbot.slash_command_invocation_url}"
}
