
import os,glob
import subprocess
from pprint import pprint

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
      logging.FileHandler(os.path.splitext(__file__)[0]+".log"), 
      logging.StreamHandler()
    ]
)

def PrettyPrint(val):
  return pprint.format(val)


def FindNotebooks(dir):
  ret=glob.glob(f"{dir}/**/*.ipynb",recursive=True)
  ret=[it for it in ret if not "checkpoints" in it]
  ret=[it for it in ret if not os.path.basename(it).startswith("99")]
  return ret

# this is needed for some demos
if True:
  import bokeh
  bokeh.sampledata.download(progress=False)

# find notebooks
notebooks=FindNotebooks("examples")

v=[]
N=len(notebooks)
for I, notebook in enumerate(notebooks):
  logging.info(f"# [{I}/{N}] jupyter nbconvert --to html --execute {notebook} ")
  result = subprocess.run(["jupyter", "nbconvert", "--to", "html", "--execute", os.path.basename(notebook)], 
                          capture_output=True, 
                          text=True, 
                          cwd=os.path.dirname(notebook))
  body="\n".join([result.stdout.rstrip(),result.stderr.rstrip()])
  d=dict(notebook=notebook, returncode=result.returncode,body=body)
  v.append(d)
  if result.returncode!=0:  logging.info(PrettyPrint(d))

v=list(sorted(v, key=lambda d: d["returncode"]))

errors=[it for it in v if it["returncode"]!=0]

logging.info("# //////////////////// Errors {len(errors)}")
for it in errors:
  logging.info(it)





