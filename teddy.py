#!/usr/bin/env python

import click
import os, json
from markdown_to_json.vendor import CommonMark
from markdown_to_json.markdown_to_json import Renderer, CMarkASTNester

projects_path = "/home/satyendra/projects"
project_config = open("PROJECTS.md","r")

def extract_json(fileName):
    ast = CommonMark.DocParser().parse(fileName.read())
    nestedAst = CMarkASTNester().nest(ast)
    orderdDict = Renderer().stringify_dict(nestedAst)
    return json.loads(json.dumps(orderdDict,indent=4))

json_str = extract_json(project_config)
print(json_str)
# WIP repos :
wip_repos = json_str['WIP']
dir_list = os.listdir(projects_path)
print(wip_repos)
print(dir_list)
for repo in wip_repos:
    if repo in dir_list:
        filePath = os.path.join(projects_path, repo, "README.md")
        fileName = open(filePath,"r")
        print(repo)
        print(extract_json(fileName))

var1 = 0

@click.group()
@click.option('--verbose/--no-verbose', default=False , help='print verbosely')
def cli(verbose):
    global var1 
    var1 = 10
    click.echo('Debug mode is %s' % ('on' if verbose else 'off'))

@cli.command('initialize', short_help='initize with the repos in PROJECTS.md')  
def intialize():
    click.echo(var1)

@cli.command('sync', short_help='sync the NOTES repo')  
def sync():
    click.echo('Sync')

@cli.command('todo', short_help='count To-Do items in WIP projects')  
def todo():
    click.echo('todo')

if __name__ == '__main__':
    cli()