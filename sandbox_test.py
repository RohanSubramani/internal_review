from inspect_ai import Task, task, eval
from inspect_ai.dataset import Sample
from inspect_ai.solver import use_tools, generate
from inspect_ai.tool import ToolError, tool
from inspect_ai.util import sandbox

# Step 1: Define the Tool
@tool
def list_files():
    async def execute(dir: str):
        """List the files in a directory."""
        result = await sandbox().exec(["ls", dir])
        if result.success:
            return result.stdout
        else:
            raise ToolError(result.stderr)
    return execute

# Step 2: Define the Dataset
dataset = [
    Sample(
        input='What files are present in the directory?',
        target="file1.txt",
        files={
            "file1.txt": "This is file 1 content.",
            "file2.txt": "This is file 2 content.",
        },
    )
]

# Step 3: Define the Task
@task
def custom_eval():
    return Task(
        dataset=dataset,
        solver=[
            use_tools([list_files()]),
            generate()
        ],
        sandbox="docker",  # Specify Docker as the sandbox environment
    )

# Step 4: Run the Evaluation
if __name__ == "__main__":
    eval("custom_eval")
