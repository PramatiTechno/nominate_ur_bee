import sys
from fabric import Connection, task
from invoke import Responder
from fabric.config import Config

PROJECT_NAME = "nominate-your-bee"
PROJECT_PATH = "/var/www/{}".format(PROJECT_NAME)
REPO_URL = ""

def get_connection(ctx):
    try:
        with Connection(ctx.host, ctx.user, connect_kwargs=ctx.connect_kwargs) as conn:
            return conn
    except Exception as e:
        return None

@task
def development(ctx):
    ctx.user = "ubuntu"
    ctx.host = "172.17.10.110"
    ctx.connect_kwargs.key_filename = "/home/akhilesh/Documents/rpx_machine.pem"

# check if file exists in directory(list)
def exists(file, dir):
    return file in dir


# git tasks
@task
def pull(ctx, branch="deploy"):
    # check if ctx is Connection object or Context object
    # if Connection object then calling method from program
    # else calling directly from terminal
    if isinstance(ctx, Connection):
        conn = ctx
    else:
        conn = get_connection(ctx)

    with conn.cd(PROJECT_PATH):
        conn.run("git pull origin {}".format(branch))


@task
def checkout(ctx, branch=None):
    if branch is None:
        sys.exit("branch name is not specified")
    print("branch-name: {}".format(branch))
    if isinstance(ctx, Connection):
        conn = ctx
    else:
        conn = get_connection(ctx)
    with conn.cd(PROJECT_PATH):
        conn.run("git checkout {branch}".format(branch=branch))


@task
def clone(ctx):
    if isinstance(ctx, Connection):
        conn = ctx
    else:
        conn = get_connection(ctx)

    ls_result = conn.run("ls").stdout
    ls_result = ls_result.split("\n")
    if exists(PROJECT_NAME, ls_result):
        print("project already exists")
        return
    conn.run("git clone {} {}".format(REPO_URL, PROJECT_NAME))

@task
def migrate(ctx):
    if isinstance(ctx, Connection):
        conn = ctx
    else:
        conn = get_connection(ctx)
    with conn.cd(PROJECT_PATH):
        conn.run("./venv/bin/python3.6 manage.py migrate")


# supervisor tasks
@task
def start(ctx):
    if isinstance(ctx, Connection):
        conn = ctx
    else:
        conn = get_connection(ctx)
    conn.sudo("supervisorctl start all")


@task
def restart(ctx):
    if isinstance(ctx, Connection):
        conn = ctx
    else:
        conn = get_connection(ctx)
    print("restarting supervisor...")
    conn.sudo("supervisorctl restart all")

@task
def stop(ctx):
    if isinstance(ctx, Connection):
        conn = ctx
    else:
        conn = get_connection(ctx)
    conn.sudo("supervisorctl stop all")


@task
def status(ctx):
    if isinstance(ctx, Connection):
        conn = ctx
    else:
        conn = get_connection(ctx)
    conn.sudo("supervisorctl status")


# deploy task
@task
def deploy(ctx):
    conn = get_connection(ctx)
    if conn is None:
        sys.exit("Failed to get connection")
    clone(conn)
    with conn.cd(PROJECT_PATH):
        print("checkout to deploy branch...")
        checkout(conn, branch="deploy")
        print("pulling latest code from deploy branch...")
        pull(conn)
        print("migrating database....")
        migrate(conn)
        print("restarting the supervisor...")
        restart(conn)