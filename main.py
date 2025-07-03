import os
import argparse
from code_to_run_file import code_to_run
from transformers import AutoModelForCausalLM, AutoTokenizer

def named_args():
    parser = argparse.ArgumentParser(
        description="This program is used to run the eval testing code for the models",
        usage="%(prog)s --is_server False --cuda_device 0,1",
        prog="main.py",
        add_help=True,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument("-s", "--is_server", metavar='', required=True, help="Please enter if the code is running in server or not as Boolean value")
    parser.add_argument("-c", "--cuda_device", metavar='', required=True, help="Please enter the cuda devices as a string")

    return parser.parse_args()

if __name__ == "__main__":
    args=named_args()
    
    if args.is_server.lower() not in ["true", "false"]:
        raise ValueError("is_server must be either 'True' or 'False'")
    
    is_server = args.is_server.lower() == "true"
    cuda_device = args.cuda_device # or "0,1" or "0,1,2" etc.

    os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"
    os.environ["CUDA_VISIBLE_DEVICES"] = cuda_device

    checkpoint = "Qwen/Qwen2.5-Coder-7B-Instruct"

    if is_server:
        tokenizer = AutoTokenizer.from_pretrained(
            checkpoint,
            cache_dir=f"/external-raid/scratch/SIT/akarsh_sit/{checkpoint}",
            trust_remote_code=True,
        )
        model = AutoModelForCausalLM.from_pretrained(
            checkpoint, 
            device_map="auto",
            cache_dir=f"/external-raid/scratch/SIT/akarsh_sit/{checkpoint}",
            trust_remote_code=True,
        )
    else:
        tokenizer = AutoTokenizer.from_pretrained(
            checkpoint,
            trust_remote_code=True,
        )
        model = AutoModelForCausalLM.from_pretrained(
            checkpoint, 
            device_map="auto",
            trust_remote_code=True,
        )

    code_to_run(model, tokenizer)
