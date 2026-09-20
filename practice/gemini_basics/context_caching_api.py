import os
import time
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types


# ==== SETUP ====

env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(env_path)

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=api_key)

# Use the same model for cache creation and generation
model = "models/gemini-3.5-flash-lite"


# ==== LARGE DOCUMENT CONTEXT ====

print("\n==== LARGE DOCUMENT CONTEXT ====")

documentation = """
Gemini API Developer Documentation

Authentication:
Applications authenticate with the Gemini API using an API key.
API keys should be stored securely and should not be committed
to source control.

Generate Content:
The GenerateContent API accepts content and returns generated
model output. The selected model determines capabilities,
context limits, latency and pricing.

Context Caching:
Context caching allows a large body of content to be reused
across multiple requests. This is useful when the same
documentation, transcripts, codebases, policies or reference
material are queried repeatedly.

Explicit Caching:
An application can explicitly create a cached-content resource
and reference that cache in subsequent generation requests.

Cache TTL:
Cached content has a time-to-live. Once the TTL expires,
the cache is no longer available.

Token Usage:
Applications should inspect usage metadata to understand
input tokens, output tokens, total tokens and cached tokens.

Production:
Applications should keep API keys outside source code,
handle API errors, respect rate limits and monitor token usage.

Model Selection:
Flash-Lite models are intended for high-throughput and
cost-sensitive workloads.

Tools:
Depending on the model and configuration, Gemini can use
tools such as function calling and grounding.

Safety:
Model output should be validated before being used in
sensitive or automated workflows.
"""

# Repeat the documentation to create a large reusable context
large_text_context = documentation * 20

print(f"Context characters: {len(large_text_context):,}")


# ==== TOKEN COUNT ====

print("\n==== CONTEXT TOKEN COUNT ====")

try:
    token_count = client.models.count_tokens(
        model=model,
        contents=large_text_context,
    )

    context_tokens = token_count.total_tokens

    print(f"Context tokens: {context_tokens:,}")

except Exception as e:
    print("\n==== TOKEN COUNT ERROR ====")
    print(type(e).__name__)
    print(e)
    raise


# ==== CREATE CONTEXT CACHE ====

print("\n==== CREATING CONTEXT CACHE ====")

cache = None

try:
    cache = client.caches.create(
        model=model,
        config=types.CreateCachedContentConfig(
            contents=[large_text_context],
            ttl="300s",
            display_name="gemini_docs_demo_cache",
        ),
    )

    print("Cache created successfully!")
    print(f"Cache Name: {cache.name}")
    print("Cache TTL: 300 seconds")

except Exception as e:
    print("\n==== CACHE CREATION ERROR ====")
    print(type(e).__name__)
    print(e)

    # Handle Free Tier cached-storage limitation
    if "TotalCachedContentStorageTokensPerModelFreeTier" in str(e):

        print("\n==== FREE TIER CACHE LIMIT ====")
        print("Explicit context caching is unavailable")
        print("for this project on the current Free Tier.")

        print(f"Requested cached tokens: {context_tokens:,}")
        print("Available cached storage tokens: 0")

        print("\nNo sleep/retry will fix this quota.")
        print("Continuing with normal generation...")

    else:
        print("\n==== UNEXPECTED CACHE ERROR ====")
        raise


# ==== CACHE SUCCESS PATH ====

if cache:

    # ==== CACHE DETAILS ====

    print("\n==== CACHE DETAILS ====")

    try:
        cached_content = client.caches.get(
            name=cache.name
        )

        print(f"Cache Name:   {cached_content.name}")
        print(f"Display Name: {cached_content.display_name}")
        print(f"Created:      {cached_content.create_time}")
        print(f"Expires:      {cached_content.expire_time}")

    except Exception as e:
        print("\n==== CACHE DETAILS ERROR ====")
        print(type(e).__name__)
        print(e)


    # ==== QUERY USING CACHED CONTEXT ====

    print("\n==== QUERY USING CACHED CONTEXT ====")

    config = types.GenerateContentConfig(
        cached_content=cache.name
    )

    prompt = (
        "Summarize the primary guidelines mentioned "
        "in the cached Gemini API documentation."
    )

    try:
        start_time = time.perf_counter()

        response = client.models.generate_content(
            model=model,
            contents=prompt,
            config=config,
        )

        elapsed = time.perf_counter() - start_time

        print("\n==== CACHED RESPONSE ====")
        print(response.text)

        print("\n==== RESPONSE DETAILS ====")

        if response.candidates:
            candidate = response.candidates[0]
            print(f"Finish reason: {candidate.finish_reason}")

        print(f"Response time: {elapsed:.3f} seconds")

        print("\n==== TOKEN USAGE ====")

        if response.usage_metadata:
            usage = response.usage_metadata

            print(f"Input tokens:  {usage.prompt_token_count}")
            print(f"Output tokens: {usage.candidates_token_count}")
            print(f"Total tokens:   {usage.total_token_count}")

            cached_tokens = getattr(
                usage,
                "cached_content_token_count",
                None,
            )

            if cached_tokens is not None:
                print(f"Cached tokens: {cached_tokens}")

    except Exception as e:
        print("\n==== CACHED QUERY ERROR ====")
        print(type(e).__name__)
        print(e)


    # ==== WAIT BEFORE SECOND REQUEST ====

    print("\nWaiting 2 seconds before the next request...")
    time.sleep(2)


    # ==== SECOND QUERY USING SAME CACHE ====

    print("\n==== SECOND QUERY USING SAME CACHE ====")

    second_prompt = (
        "According to the cached documentation, what "
        "are the main recommendations for production applications?"
    )

    try:
        start_time = time.perf_counter()

        response2 = client.models.generate_content(
            model=model,
            contents=second_prompt,
            config=config,
        )

        elapsed = time.perf_counter() - start_time

        print("\n==== SECOND CACHED RESPONSE ====")
        print(response2.text)

        print("\n==== SECOND RESPONSE DETAILS ====")

        if response2.candidates:
            candidate = response2.candidates[0]
            print(f"Finish reason: {candidate.finish_reason}")

        print(f"Response time: {elapsed:.3f} seconds")

        print("\n==== SECOND TOKEN USAGE ====")

        if response2.usage_metadata:
            usage = response2.usage_metadata

            print(f"Input tokens:  {usage.prompt_token_count}")
            print(f"Output tokens: {usage.candidates_token_count}")
            print(f"Total tokens:   {usage.total_token_count}")

            cached_tokens = getattr(
                usage,
                "cached_content_token_count",
                None,
            )

            if cached_tokens is not None:
                print(f"Cached tokens: {cached_tokens}")

    except Exception as e:
        print("\n==== SECOND CACHED QUERY ERROR ====")
        print(type(e).__name__)
        print(e)


    # ==== DELETE CACHE ====

    print("\n==== CLEANING UP CACHE ====")

    try:
        client.caches.delete(name=cache.name)
        print("Cache deleted successfully!")

    except Exception as e:
        print("\n==== CACHE DELETE ERROR ====")
        print(type(e).__name__)
        print(e)


# ==== FREE TIER FALLBACK ====

else:

    print("\n==== NORMAL GENERATION FALLBACK ====")

    normal_prompt = f"""
Use the following documentation as reference.

--- DOCUMENTATION START ---

{large_text_context}

--- DOCUMENTATION END ---

Question:
Summarize the primary guidelines mentioned in the documentation.
"""

    try:
        start_time = time.perf_counter()

        response = client.models.generate_content(
            model=model,
            contents=normal_prompt,
        )

        elapsed = time.perf_counter() - start_time

        print("\n==== NORMAL RESPONSE ====")
        print(response.text)

        print("\n==== RESPONSE DETAILS ====")

        if response.candidates:
            candidate = response.candidates[0]
            print(f"Finish reason: {candidate.finish_reason}")

        print(f"Response time: {elapsed:.3f} seconds")

        print("\n==== TOKEN USAGE ====")

        if response.usage_metadata:
            usage = response.usage_metadata

            print(f"Input tokens:  {usage.prompt_token_count}")
            print(f"Output tokens: {usage.candidates_token_count}")
            print(f"Total tokens:   {usage.total_token_count}")

            cached_tokens = getattr(
                usage,
                "cached_content_token_count",
                None,
            )

            if cached_tokens is not None:
                print(f"Cached tokens: {cached_tokens}")

    except Exception as e:
        print("\n==== NORMAL GENERATION ERROR ====")
        print(type(e).__name__)
        print(e)


# ==== COMPLETE ====

print("\n==== DEMO COMPLETE ====")
