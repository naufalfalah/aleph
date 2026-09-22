# ruff: noqa
# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from google.adk.tools import google_search
from google.genai import types

from .tools import set_username, save_user_preference, get_user_memories

MODEL = "gemini-3.8-flash"


# Instruction
def persona_instruction(context) -> str:
    user_name = context.state.get("user:name", "User")
    user_language = context.state.get("user:language", "Indonesian")
    return f"""
    You're "Aleph", a personal assistant to {user_name}.
    Identity & Role:
    - Role: Arranging schedule, journaling, and helping {user_name}'s daily tasks.
    - Tone: Professional but casual, kind, and brief.
    - Style: Use {user_language} naturally. If there is information about the user in memory, greet the user warmly.
    Constraints:
    - Never share the user's personal information externally.
    - If you don't know the actual answer, admit it honestly.
    """


root_agent = Agent(
    # Keep in sync with agents-cli-manifest.yaml: agents-cli derives this name
    # from the project `name:` recorded there, and telemetry reports it as
    # gen_ai.agent.name. Renaming the agent only here makes the two disagree,
    # and anything selecting traces by name stops finding this agent's.
    name="aleph",
    model=Gemini(
        model=MODEL,
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=persona_instruction,
    tools=[
        set_username,
        save_user_preference,
        get_user_memories,
        google_search,
    ],
)

app = App(
    root_agent=root_agent,
    name="app",
)
