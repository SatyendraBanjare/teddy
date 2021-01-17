#!/usr/bin/env python

import click
import os, json
from markdown_to_json.vendor import CommonMark
from markdown_to_json.markdown_to_json import Renderer, CMarkASTNester
from git import Repo

projects_path = "/home/satyendra/projects"
project_config = open("PROJECTS.md","r")

git_ssh_prefix = "git@github.com:SatyendraBanjare/"

def extract_json(fileName):
    ast = CommonMark.DocParser().parse(fileName.read())
    nestedAst = CMarkASTNester().nest(ast)
    orderdDict = Renderer().stringify_dict(nestedAst)
    return json.loads(json.dumps(orderdDict,indent=4))

# WIP repos :
wip_repos = extract_json(project_config)['WIP']
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

@click.group()
def cli():
    pass

@cli.command('intirepos', short_help='initialize with the WIP repos in PROJECTS.md')  
def intirepos():
    click.echo(intialize_wip_repos())

@cli.command('sync', short_help='sync the NOTES repo')  
def sync():
    click.echo('Sync')

@cli.command('todo', short_help='count To-Do items in WIP projects')  
def todo():
    click.echo(count_todo())

if __name__ == '__main__':
    cli()