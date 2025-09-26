from prompt import user_goal_prompt
from typing import Optional, Any, Callable
import asyncio
import importlib

def initialize_model(google_api_key: str) -> Any:
    """Create and return the chat model instance lazily to avoid top-level imports."""
    try:
        genai_mod = importlib.import_module('langchain_google_genai')
        ChatGoogleGenerativeAI = getattr(genai_mod, 'ChatGoogleGenerativeAI')
    except Exception as e:
        raise RuntimeError(
            "Missing dependency: langchain-google-genai. Install requirements first."
        ) from e
    return ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=google_api_key)

async def setup_agent_with_tools(
    google_api_key: str,
    youtube_pipedream_url: str,
    drive_pipedream_url: Optional[str] = None,
    notion_pipedream_url: Optional[str] = None,
    progress_callback: Optional[Callable[[str], None]] = None
) -> Any:
    """
    Set up the agent with YouTube (mandatory) and optional Drive or Notion tools.
    """
    try:
        if progress_callback:
            progress_callback("Setting up agent with tools... ✅")
        
        # Initialize tools configuration with mandatory YouTube
        tools_config = {
            "youtube": {
                "url": youtube_pipedream_url,
                "transport": "streamable_http"
            }
        }

        # Add Drive if URL provided
        if drive_pipedream_url:
            tools_config["drive"] = {
                "url": drive_pipedream_url,
                "transport": "streamable_http"
            }
            if progress_callback:
                progress_callback("Added Google Drive integration... ✅")

        # Add Notion if URL provided
        if notion_pipedream_url:
            tools_config["notion"] = {
                "url": notion_pipedream_url,
                "transport": "streamable_http"
            }
            if progress_callback:
                progress_callback("Added Notion integration... ✅")

        if progress_callback:
            progress_callback("Initializing MCP client... ✅")
        # Initialize MCP client with configured tools
        try:
            mcp_mod = importlib.import_module('langchain_mcp_adapters.client')
            MultiServerMCPClient = getattr(mcp_mod, 'MultiServerMCPClient')
        except Exception as e:
            raise RuntimeError(
                "Missing dependency: langchain-mcp-adapters. Install requirements first."
            ) from e
        mcp_client = MultiServerMCPClient(tools_config)
        
        if progress_callback:
            progress_callback("Getting available tools... ✅")
        # Get all tools with graceful fallback
        try:
            tools = await mcp_client.get_tools()
        except Exception as e:
            if progress_callback:
                progress_callback("Failed to connect to one or more tools. Proceeding without external tools.")
            tools = []
            print(f"MCP tool discovery failed: {str(e)}")
        
        if progress_callback:
            progress_callback("Creating AI agent... ✅")
        # Create agent with initialized model
        mcp_orch_model = initialize_model(google_api_key)
        try:
            prebuilt_mod = importlib.import_module('langgraph.prebuilt')
            create_react_agent = getattr(prebuilt_mod, 'create_react_agent')
        except Exception as e:
            raise RuntimeError(
                "Missing dependency: langgraph. Install requirements first."
            ) from e
        agent = create_react_agent(mcp_orch_model, tools)
        
        if progress_callback:
            progress_callback("Setup complete! Starting to generate learning path... ✅")
        
        return agent
    except Exception as e:
        print(f"Error in setup_agent_with_tools: {str(e)}")
        raise

def run_agent_sync(
    google_api_key: str,
    youtube_pipedream_url: str,
    drive_pipedream_url: Optional[str] = None,
    notion_pipedream_url: Optional[str] = None,
    user_goal: str = "",
    progress_callback: Optional[Callable[[str], None]] = None
) -> dict:
    """
    Synchronous wrapper for running the agent.
    """
    async def _run():
        try:
            agent = await setup_agent_with_tools(
                google_api_key=google_api_key,
                youtube_pipedream_url=youtube_pipedream_url,
                drive_pipedream_url=drive_pipedream_url,
                notion_pipedream_url=notion_pipedream_url,
                progress_callback=progress_callback
            )
            
            # Combine user goal with prompt template
            learning_path_prompt = "User Goal: " + user_goal + "\n" + user_goal_prompt
            
            if progress_callback:
                progress_callback("Generating your learning path...")
            
            # Run the agent
            try:
                core_msgs_mod = importlib.import_module('langchain_core.messages')
                core_run_mod = importlib.import_module('langchain_core.runnables')
                HumanMessage = getattr(core_msgs_mod, 'HumanMessage')
                RunnableConfig = getattr(core_run_mod, 'RunnableConfig')
            except Exception as e:
                raise RuntimeError(
                    "Missing dependency: langchain-core. Install requirements first."
                ) from e
            cfg = RunnableConfig(recursion_limit=100)
            result = await agent.ainvoke({"messages": [HumanMessage(content=learning_path_prompt)]}, config=cfg)
            
            if progress_callback:
                progress_callback("Learning path generation complete!")
            
            return result
        except Exception as e:
            print(f"Error in _run: {str(e)}")
            raise

    # Run in new event loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(_run())
    finally:
        loop.close()
