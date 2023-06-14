"""A Steamship package for prompt-based text generation.

This package provides a simple template for building a prompt-based API service.

To run:

1. Run `pip install steamship termcolor`
2. Run `ship login`
3. Run `python api.py`

To deploy and get a public API and web demo:

1. Run `echo steamship >> requirements.txt`
2. Run `echo termcolor >> requirements.txt`
3. Run `ship deploy`

To learn more about advanced uses of Steamship, read our docs at: https://docs.steamship.com/packages/using.html.
"""
import inspect

from steamship import check_environment, RuntimeEnvironments, Steamship
from steamship.invocable import post, PackageService
from termcolor import colored


class PromptPackage(PackageService):
    # Modify this to customize behavior to match your needs.
    PROMPT = """
         I want you to act as a household plant expert. 
         Please provide a paragraph of comprehensive background information such as latin name and
         country of origin about a {plant}. 
         Then, provide 3 bullet points under 50 words about light, water and humidity for a {plant}.
         Then, add a last sentence in informal tone that is an encouragement for taking care of house plants.
             """

    # When this package is deployed, this annotation tells Steamship
    # to expose an endpoint that accepts HTTP POST requests for the
    # `/generate` request path.
    # See README.md for more information about deployment.
    @post("generate")
    def generate(self, plant: str) -> str:
        """Generate text from prompt parameters."""
        llm_config = {
            # Controls length of generated output.
            "max_words": 300,
            # Controls randomness of output (range: 0.0-1.0).
            "temperature": 0.8
        }
        prompt_args = {"plant": plant}

        llm = self.client.use_plugin("gpt-3", config=llm_config)
        return llm.generate(self.PROMPT, prompt_args)


if __name__ == "__main__":
    print(colored("Generate plant information with GPT-3\n", attrs=['bold']))

    # This helper provides runtime API key prompting, etc.
    check_environment(RuntimeEnvironments.REPLIT)

    with Steamship.temporary_workspace() as client:
        prompt = PromptPackage(client)

        print(colored("What is the name of your plant?", 'green'))

        try_again = True
        while try_again:
            kwargs = {}
            for parameter in inspect.signature(prompt.generate).parameters:
                kwargs[parameter] = input(
                    colored(f'{parameter.capitalize()}: ', 'green'))

            print(colored("Generating...", 'green'))

            # This is the prompt-based generation call
            print(f'{prompt.generate(**kwargs)}\n')

            try_again = input(colored("Generate another (y/n)? ",
                                      'green')).lower().strip() == 'y'
            print()
