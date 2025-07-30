import subprocess
import json
from pathlib import Path

base_dir = Path(__file__).parent
spass_output = base_dir / "spass_output"
spass_output.mkdir(exist_ok=True)


default_config = {
    "problemName": "StepFrames",
    "name": "{*StepFrames*}",
    "author": "{*Author*}",
    "description":"{*Output of SPASS python file*}",
}


def load_config():
    try:
        with open(base_dir/"config.json") as f:
            config = json.load(f)
    except FileNotFoundError as e:
        with open(base_dir/"config.json", "w") as f:
            json.dump(default_config, f, indent=4)
            config = default_config

    problemName = config.get("problemName","StepFrames")
    name = config.get("name","Person")
    author = config.get("author","Author")
    description = config.get("description","Output of SPASS python file")

    if problemName.strip()=="":
        problemName = "StepFrames"

    if name.strip()=="":
        name = "Person"

    if author.strip()=="":
        author = "Author"

    if description.strip()=="":
        description = "Output of SPASS python file"

    return {"problemName":problemName,"name":name,"author":author,"description":description}


def load_args():
    try:
        with open(base_dir/"args.txt","r") as f:
            data = [i.replace("\n","") for i in f.readlines() if "%" not in i]
        
        first_order = data[0]
        S = data[1]

        return first_order,S
    except FileNotFoundError as e:
        raise FileNotFoundError("args.txt file is missing")


def create_dfg_file(config,first_order,S):
    dfg_code = f"""begin_problem({config["problemName"]}).

    list_of_descriptions.
    name({config["name"]}).
    author({config["author"]}).
    status(unsatisfiable).
    description({config["description"]}).
    end_of_list.
    

    list_of_symbols.
        functions[(f,1)].
        predicates[(R,2),(S,2)].
    end_of_list.


    list_of_formulae(axioms).
        formula(forall([v], exists([w], equal(f(w), v))), 1).
        {first_order}
        {S}
    end_of_list.    


    list_of_formulae(conjectures).
    
    formula(forall([w,v],equiv(R(w,v),exists([w1],and(S(w,w1),equal(f(w1),v))))),4).
    formula(forall([w,v],equiv(S(w,v),exists([k],and(R(k,v),S(w,k))))),5).
    
    end_of_list.

    end_problem.
    """

    with open(spass_output/"spass.dfg", "w") as f:
        f.write(dfg_code)


def run_SPASS():
    SPASS_result = subprocess.run([base_dir/"spass39/SPASS", spass_output/"spass.dfg"], capture_output=True, text=True)

    print("OUTPUT:")
    print(SPASS_result.stdout)

    with open(spass_output/"output.txt","w") as f:
        f.write(SPASS_result.stdout)

    with open(spass_output/"error.txt","w") as f:
        f.write(SPASS_result.stderr)


config = load_config()
first_order,S = load_args()
create_dfg_file(config,first_order,S)
run_SPASS()
