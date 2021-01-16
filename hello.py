#!/usr/bin/env python

import click

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

@cli.command('todo', short_help='count To-Do items')  
def todo():
    click.echo('todo')

if __name__ == '__main__':
    cli()