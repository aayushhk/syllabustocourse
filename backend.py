import asyncio
from duckduckgo_search import AsyncDDGS, DDGS
from duckduckgo_search import exceptions
import openai



async def webai(query: str, custom_prompt: str) -> str:
    # Perform synchronous text search using DDGS
    search_results = DDGS().text(query, max_results=6)
    
    for result in search_results:
        print("---------------------------")
        print(f"Title: {result['title']}")
        print(f"Link: {result['href']}")
        print(f"Snippet: {result['body']}")
        

    # Combine snippets from the search results for the chat prompt
    combined_snippets = "\n".join(result['title'] for result in search_results).join(result['body'] for result in search_results)
    print(combined_snippets)
    
    
    # Use the custom prompt and format it with search results
    chat_input = custom_prompt.format(search_snippets=combined_snippets)

    # Perform asynchronous chat using AsyncDDGS
    async with AsyncDDGS() as ddgs:
        results = await ddgs.achat(chat_input)
    
    return results


async def ai(idea_prompt: str) -> str:
    chat_input = idea_prompt

    try:
        # Perform asynchronous chat using AsyncDDGS
        async with AsyncDDGS() as ddgs:
            results = await ddgs.achat(chat_input)
    
    except exceptions.DuckDuckGoSearchException as e:
        print(f"DuckDuckGo search failed with error: {str(e)}. Falling back to ChatGPT.")
        
        # Fall back to OpenAI's ChatGPT API
        results = await chatgpt_fallback(chat_input)
    
    return results

async def chatgpt_fallback(chat_input: str) -> str:
    openai.api_key = st.secrets["openai_apikey"]  # Replace with your OpenAI API key

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Be a intresting assistant"},
            {"role": "user", "content": chat_input},
        ]
    )
    return response.choices[0].message.content

async def web(query: str) -> str:
    # Perform synchronous text search using DDGS
    search_results = DDGS().text(query, max_results=6)
    
    for result in search_results:
        print("---------------------------")
        print(f"Title: {result['title']}")
        print(f"Link: {result['href']}")
        print(f"Snippet: {result['body']}")
        

    # Combine snippets from the search results for the chat prompt
    
    
    return search_results
