import subprocess as sp

from flask_restful import Resource


# TODO make async
def deploy(image):
    print(f'This is Dry Run! Deploying image: {image}...')

    org = "default-org"
    deployment = image[image.rfind('/') + 1:]
    vars_file_path = "../terraform/generated/vars.tfvars"
    template_file_path = f"../terraform/templates/ecs/{org}-{deployment}.json.tpl"
    def_template_file_path = "../terraform/templates/ecs/default-org-container.json.tpl"

    params = set_params(image, org, deployment, template_file_path)

    write_variables(params, vars_file_path)

    write_template_file(template_file_path, def_template_file_path)
    print(f'Starting to run init')
    init_out = run_terraform_init(vars_file_path)
    print(f'Starting to run plan')
    plan_out = run_terraform_plan(vars_file_path, image)

    return {'task': f'plan executed for{image}',
            'init_output': f'{init_out}',
            'plan_output': f'{plan_out}',
            'execution': 'To apply plan run {curl -XPOST  -H \'Content-Type: application/json\' http://host:5000//api/v1/deployment/deploy/<string:image>} -d \'{"apply": "true"}\''}


def write_template_file(template_file_path, def_template_file_path):
    with open(def_template_file_path, "r") as defTmpl:
        template_data = defTmpl.read()
    defTmpl.close()

    with open(template_file_path, "a") as tmpl:
        tmpl.seek(0)
        tmpl.truncate()
        tmpl.write(template_data)
    tmpl.close()


def set_params(image, org, deployment, template_file_path):
    params = f"""
app_image=\"{image}\"
organization=\"{org}\"
deployment=\"{deployment}\"
template_file=\"{template_file_path}\"
"""
    return params


def write_variables(params, vars_file_path):
    with open(vars_file_path, "a") as fvars:
        fvars.seek(0)
        fvars.truncate()
        fvars.write(params)
    fvars.close()


def run_terraform_plan(vars_file_path, image):
    cmd = f"terraform plan -out={image}_run.plan -var-file={vars_file_path} ../terraform/"
    return run_process_and_print(cmd)


def run_process_and_print(cmd):
    child = sp.Popen(cmd, stdout=sp.PIPE)
    (out_stream, err_stream) = child.communicate()
    rc = child.returncode
    if not rc == 0:
        if not err_stream:
            err_stream = b"empty"
        print(f"Error running {cmd}: {err_stream.decode('ANSI')}")
        print(f"output: {out_stream.decode('ANSI')}")
        return f"Error running {cmd}: {err_stream.decode('ANSI')}" + f"output: {out_stream.decode('ANSI')}"
    # # output = stream_data.decode('utf-8')
    # sys.stdout.write(stream_data.decode('ASCII'))
    print(out_stream.decode('ANSI'))
    return out_stream


def run_terraform_init(vars_file_path):
    cmd = f"terraform init -var-file={vars_file_path} ../terraform/"
    return run_process_and_print(cmd)


def get_deployment(image):
    return {'Deployment': f'{image}'}


def delete_deployment(image):
    vars_file_path = "../terraform/generated/vars.tfvars"
    print("starting to destroy deployment {image}")
    cmd = f"terraform destroy -var-file={vars_file_path} -auto-approve ../terraform/"
    return {"delete_deployment": f" output: {run_process_and_print(cmd)}"}


def apply(image):
    print("Applying deployment {image}")
    cmd = f"terraform apply -out={image}_run.plan"
    return {"Apply deployment": f" output: {run_process_and_print(cmd)}"}


class Deployment(Resource):



    def get(self, image):
        return get_deployment(image)

    def put(self, image):
        return deploy(image)

    def post(self, image):
        return apply(image)

    def delete(self, image):
        return delete_deployment(image)
