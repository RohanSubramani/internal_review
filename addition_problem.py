from inspect_ai import Task, eval, task
from inspect_ai.dataset import Sample
from inspect_ai.scorer import includes, match
from inspect_ai.solver import (
    generate, system_message, use_tools
)
from inspect_ai.tool import tool
from inspect_ai.util import subprocess
from inspect_ai.solver import self_critique

@tool
def add():
    async def execute(x: int, y: int):
        """
        Add two numbers.

        Args:
            x (int): First number to add.
            y (int): Second number to add.

        Returns:
            The sum of the two numbers.
        """
        return x + y

    return execute

@task
def addition_problem():
    return Task(
        dataset=[Sample(
            input="What is 1 + 1?",
            target=["2","2.0"]
        ),
        Sample(
            input="What is 12+(-65)?",
            target=["-53","-53.0"]
        )],
        solver=[
            use_tools(add()),
            generate(),
            self_critique()
        ],
        scorer=match(numeric=True)
    )