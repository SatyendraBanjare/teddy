import json
from markdown_to_json.vendor import CommonMark
from markdown_to_json.markdown_to_json import Renderer, CMarkASTNester

file = open("PROJECTS.md","r")
ast = CommonMark.DocParser().parse(file.read())
lol = CMarkASTNester().nest(ast)
res = Renderer().stringify_dict(lol)
print(json.dumps(res,indent=4))


