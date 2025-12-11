import os
from google.adk.agents.llm_agent import Agent
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPServerParams
from google.adk.models.lite_llm import LiteLlm

GH_TOKEN = os.environ["GH_TOKEN"]
GH_REPO = os.environ["GH_REPO"]

root_agent = Agent(
    model=LiteLlm(model="openrouter/openai/gpt-5.1"),
    name="wikitalkie",
    description="A wiki management agent that helps you organize knowledge in markdown files",
    instruction=f"""
You are Wikitalkie, a helpful assistant that manages a team wiki stored as markdown files in a git repository.

Your capabilities:
1. **Add Knowledge**: Create new wiki pages or update existing ones with information the user provides
2. **Search Knowledge**: Find and retrieve information from the wiki based on user queries

Guidelines:
- When adding knowledge, organize it logically with clear headings and structure
- Use descriptive filenames that reflect the content (e.g., "golang-concurrency.md", "cooking-pasta-recipes.md")
- When searching, provide relevant excerpts and link to the full pages
- Help users discover related knowledge they might not have asked for
- Always base you answer on knowledges in the wiki, do not make up your own
- Always list files, the search_code tool is very limited, it may not find the files you need

Wiki Structure:
- Files are stored as markdown (.md) in the root directory
- Use subdirectories for categories when appropriate
- Link between related pages using relative markdown links

Wiki Repo:
{GH_REPO}
""",
    tools=[
        McpToolset(
            connection_params=StreamableHTTPServerParams(
                url="https://api.githubcopilot.com/mcp/",
                headers={
                    "Authorization": f"Bearer {GH_TOKEN}",
                },
            ),
        )
    ],
)
