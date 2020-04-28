locals {
  product = "pylunchtime"

  api_token        = "your-google-places-api-token-here"
  artifact_bucket  = "dispassion-ops-lambda-us-west-2"
  aws_access_key   = "your-key-here"
  aws_account_id   = "your-account-id-here"
  aws_region       = "us-west-2"
  aws_secret_key   = "your-secret-here"
  build_number     = 0
}

terraform {
  required_version = "~> 0.12"
  backend "remote" {
    organization = "dispassionproject"

    workspaces {
      name = "lunchtime"
    }
  }
}

provider "aws" {
  region     = local.aws_region
  access_key = local.aws_access_key
  secret_key = local.aws_secret_key
}

###lambda
resource "aws_lambda_function" "lambda" {
  s3_bucket = local.artifact_bucket
  s3_key    = "${local.product}/${local.product}-${local.build_number}.zip"

  function_name = local.product
  handler       = "app.handler.lambda_handler"
  memory_size   = 256
  role          = aws_iam_role.lambda-role.arn
  runtime       = "python3.7"
  timeout       = 30

  environment {
    variables = {
      "API_TOKEN": local.api_token
    }
  }

  tags = {
    BuildNumber = local.build_number
    Product     = local.product
    Terraform   = true
  }

}

resource "aws_lambda_permission" "allow-trigger" {
  statement_id  = "AllowTrigger"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda.function_name
  principal     = "apigateway.amazonaws.com"
}


