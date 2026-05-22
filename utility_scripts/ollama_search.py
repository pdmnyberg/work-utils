from pydantic import BaseModel, TypeAdapter

from pydantic_ai import Agent, FunctionToolset, RunContext
from pydantic_ai.models.ollama import OllamaModel
from pydantic_ai.providers.ollama import OllamaProvider
from pydantic_ai.output import NativeOutput
import requests
import functools
from bs4 import BeautifulSoup

search_toolset = FunctionToolset(
    instructions=(
        "Always use the search tool or the url fetching tool before answering factual questions. "
        "Investigate the topic and give a list of facts with url references to the source of the information. "
        "Include a list of open questions if that could improve the understanding if answered. "
        "Open questions must always be possible to understand without additional context."
        "Always recall previous facts to avoid repeating already known facts."
        "Do not include previous facts in your response."
    ),
)

class SearchResultEntry(BaseModel):
    url: str
    hitTitle: str
    hitSummary: str
    searchCategory: str


class SearchResult(BaseModel):
    hits: list[SearchResultEntry]


class Fact(BaseModel):
    description: str
    url: str


class Knowledge(BaseModel):
    facts: list[Fact]
    open_questions: list[str]


DepsType = list[Fact]
OutputType = Knowledge


@search_toolset.tool_plain(docstring_format="google", require_parameter_descriptions=True)
def find_at_nbis(search: str) -> SearchResult:
    """Returns structured information about the NBIS organization

    Args:
        search: short topical sentence with what you are looking for
    """
    base_url = "https://nbis.se"
    try:
        print(f"Searching: {search}")
        params = {
            "q": search
        }
        response = requests.get(f"{base_url}/results/", params=params)
        response.raise_for_status()
        result = SearchResult.model_validate(response.json())
        for hit in result.hits:
            hit.url = f"{base_url}/{hit.url}"
        return result
    except requests.exceptions.HTTPError as e:
        return "Failed to get search result."


@search_toolset.tool_plain(docstring_format="google", require_parameter_descriptions=True)
def get_text_from_url(url: str) -> str:
    """Returns the text content from a web page URL

    Args:
        url: a url from which to fetch text
    """
    try:
        print(f"Fetching: {url}")
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, features="html.parser")
        return soup.get_text()
    except requests.exceptions.HTTPError as e:
        return "Failed to get url result."


@search_toolset.tool(docstring_format="google", require_parameter_descriptions=True)
def recall_previous_knowledge(ctx: RunContext[DepsType]) -> list[Fact]:
    """Recall current facts about the topic at hand
    
    Args:
        ctx: The AI context for this run
    """

    print("Recalling knowledge.")
    return ctx.deps


@functools.cache
def get_agent():
    print("Creating agent.")
    model = OllamaModel(
        "qwen3.6",
        provider=OllamaProvider(base_url='http://localhost:11434/v1'),
    )
    return Agent(
        model,
        toolsets=[search_toolset],
        output_type=NativeOutput(OutputType),
        deps_type=DepsType
    )


def find_out_more(question: str, facts: list[Fact], secondary_question: str):
    agent = get_agent()
    request = (
        question
        if question == secondary_question
        else f"Answer the question '{secondary_question}' with a response that fits the original question '{question}'."
    )
    print(f"Request: {request}")
    result = agent.run_sync(request, deps=facts)
    return result.output


def print_result(result):
    result_adapter = TypeAdapter(OutputType)
    print(result_adapter.dump_json(result, indent=2).decode(encoding="utf-8"))


def iterative_understanding(question: str, max_iterations: int | None = None):
    open_questions: list[str] = [question]
    facts: list[Fact] = []
    
    iterations = 0
    while len(open_questions) > 0 and (max_iterations is None or iterations < max_iterations):
        next_open_questions = []
        for open_question in open_questions:
            result = find_out_more(question, facts, open_question)
            print_result(result)
            next_open_questions.extend(result.open_questions)
            facts.extend(result.facts)
        open_questions = next_open_questions
        iterations = iterations + 1
    return Knowledge(facts=facts, open_questions=open_questions)


result = iterative_understanding(
    "What does Mattias Nyberg do at NBIS? Include the most relevant open question.",
    max_iterations=2
)
print_result(result)