#!/usr/bin/env python

import click
import os, json, subprocess
from markdown_to_json.vendor import CommonMark
from markdown_to_json.markdown_to_json import Renderer, CMarkASTNester
from git import Repo

git_ssh_prefix = "git@github.com:SatyendraBanjare/"

projects_path = "/home/satyendra/projects"
teddy_path = "/home/satyendra/projects/teddy"
project_config = open(os.path.join(teddy_path, "PROJECTS.md"),"r")

# config for notes repo
notes_repo_path = "/home/satyendra/notes/"
COMMIT_MSG = "Notes Updated"

def extract_json(fileName):
    ast = CommonMark.DocParser().parse(fileName.read())
    nestedAst = CMarkASTNester().nest(ast)
    orderdDict = Renderer().stringify_dict(nestedAst)
    return json.loads(json.dumps(orderdDict,indent=4))

# WIP repos
wip_repos = extract_json(project_config)['WIP']

# Projects directory list
dir_list = os.listdir(projects_path)

def count_todo():
    count = 0
    for repo in wip_repos:
        if repo in dir_list:
            filePath = os.path.join(projects_path, repo, "README.md")
            fileName = open(filePath,"r")
            count+=len(extract_json(fileName)['TODO'])
    return count

def intialize_wip_repos():
    for repo in wip_repos:
        if repo not in dir_list:
            dirPath = os.path.join(projects_path, repo)
            clone_url = git_ssh_prefix + repo
            Repo.clone_from(clone_url,dirPath)
        else:
            print("Repository " + repo +" already exists.")

def sync_notes():
    try:
        repo = Repo(notes_repo_path)
        repo.git.add(notes_repo_path)
        repo.git.add(update=True)
        repo.index.commit(COMMIT_MSG)
        origin = repo.remote(name='origin')
        origin.push()
        print("Notes successfully synced")
    except:
        print('Some error occured while pushing the code')    

def publish_links():
    open(notes_repo_path + "index.md",'w').write("")
    index_file = open(notes_repo_path + "index.md",'a')
    index_file.write("# My notes \n")
    index_file.write("-------------------------------\n\n")
    dir_list = os.listdir(notes_repo_path)
    for dir_name in dir_list :
        if os.path.isdir(os.path.join(notes_repo_path,dir_name)) and dir_name != '.git':
            index_file.write("### "+dir_name+"\n")
            for note in os.listdir(os.path.join(notes_repo_path,dir_name)):
                index_file.write("- ["+note+"](./"+dir_name+"/"+note+")\n")
            index_file.write("\n<br><br>\n\n")

    index_file.write("\n-------------------------------\n\n")

    for file_name in dir_list :
        if not os.path.isdir(os.path.join(notes_repo_path,file_name)) and file_name != 'index.md':
            index_file.write("- ["+file_name+"](./"+file_name+")\n")

def list_project_containers():
    bashCmd = ["docker", "ps","-a", "--format","{ \"IMAGE\":\"{{.Image}}\", \"NAME\":\"{{.Names}}\" ,\"STATUS\":\"{{.Status}}\" }"]
    process = subprocess.Popen(bashCmd, stdout=subprocess.PIPE)
    output, error = process.communicate()
    if(not error):
        containers = output.decode("utf-8").strip().splitlines()
        print(containers)
        for container in containers :
            data = json.loads(container)
            print(data)

def create_and_publish_container(projectname):
    print("Hello")

#######################################################
# Commands 
#######################################################

@click.group()
def cli():
    pass

@cli.command('initrepos', short_help='initialize with the WIP repos in PROJECTS.md')  
def intirepos():
    click.echo(intialize_wip_repos())

@cli.command('sync', short_help='sync the notes repo')  
def sync():
    click.echo(sync_notes())

@cli.command('todo', short_help='count To-Do items in README.md of WIP projects')  
def todo():
    click.echo(count_todo())

@cli.command('publish', short_help='publish to index.md of notes repo')  
def publish():
    click.echo(publish_links())

@cli.command('create',short_help='Create docker container for the given project name')  
@click.argument('projectname')
def create(projectname):
    """
    PROJECTNAME is the name of the project to be build
    and its container published, must be present in [projects_path]
    """
    if(projectname in dir_list):
        click.echo(create_and_publish_container(projectname))
    else:
        print("Given project does not exist!!\nClone it first in "+projects_path)

@cli.command('list_containers', short_help='list docker containers')  
def list_containers():
    click.echo(list_project_containers())

if __name__ == '__main__':
    cli()