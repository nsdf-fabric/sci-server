
import os,glob
import subprocess
from pprint import pprint

# this is needed for some demos
if True:
  import bokeh
  bokeh.sampledata.download(progress=False)

notebooks=glob.glob("examples/**/*.ipynb",recursive=True)
notebooks=[it for it in notebooks if not "checkpoints" in it]
notebooks=[it for it in notebooks if not os.path.basename(it).startswith("99")]

v=[]
N=len(notebooks)
for I, notebook in enumerate(notebooks):
  print(f"# [{I}/{N}] jupyter nbconvert --to html --execute {notebook} ")
  result = subprocess.run(["jupyter", "nbconvert", "--to", "html", "--execute", os.path.basename(notebook)], 
                          capture_output=True, 
                          text=True, 
                          cwd=os.path.dirname(notebook))
  body="\n".join([result.stdout.rstrip(),result.stderr.rstrip()])
  d=dict(notebook=notebook, returncode=result.returncode,body=body)
  v.append(d)
  if result.returncode!=0:  pprint(d)

v=list(sorted(v, key=lambda d: d["returncode"]))

errors=[it for it in v if it["returncode"]!=0]
print(f"# //////////////////// Errors {len(errors)}")
pprint(errors)




