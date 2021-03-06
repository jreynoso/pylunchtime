# pylunchtime

Lambda triggered by API requests to fetch lunch options.

## Requirements

- AWS CLI already configured with appropriate S3 and Lambda permissions.
- [Python 3 installed](https://www.python.org/downloads/).
- Terraform.io account, for remote state management.

## Local development

- Create and activate your virtual environment (recommended).
- Install project requirements:

```bash
$ pip install -r requirements-dev.txt
```

### Testing

Run the unit tests:

```bash
$ pytest
```

Run tests with coverage:

```bash
$ pytest --cov-report=term-missing --cov-report=xml --cov=app
```


## Deploy lambda infrastructure

This deployment depends on hosting the remote state in terraform.io.
Make sure to first set your specific `locals`, including aws config, a build number, and terraform.io configuration in `main.tf`, then:

- cd to `./terraform`
- plan changes:
  ```bash 
  $ terraform plan
  ```
- if it looks good, apply the plan:
  ```bash 
  $ terraform apply
  ```


## Build lambda code changes
Run the `build` script with a build number:

```bash
$ ./scripts/build.sh <build_num>
```

## Deploy lambda code changes
After building, run the `deploy` script with a build number:

```bash
$ ./scripts/deploy.sh <build_num>
```

Note: make sure to set your account id, region, and artifact bucket in the deploy script.