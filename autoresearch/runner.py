""" 
This file is the entry point for MLAgentBench.
"""

import argparse
import sys
from dotenv import load_dotenv
load_dotenv()
from autoresearch import LLM
from autoresearch.environment import Environment
from autoresearch.agents.agent import Agent, SimpleActionAgent, ReasoningActionAgent
from autoresearch.agents.agent_research import ResearchAgent

def run(agent_cls, args):
    with Environment(args) as env:

        print("=====================================")
        research_problem = env.research_problem
        print("Research problem: ", research_problem)

        agent = agent_cls(args, env)
        final_message = agent.run(env)

        print("=====================================")
        print("Final message: ", final_message)

    env.save("final")



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--research-problem", type=argparse.FileType("r"), required=True, help="research problem")
    parser.add_argument("--log-dir", type=str, default="./logs", help="log dir")
    parser.add_argument("--work-dir", type=str, default="./workspace", help="work dir")
    parser.add_argument("--max-steps", type=int, default=50, help="number of steps")
    parser.add_argument("--max-time", type=int, default=5* 60 * 60, help="max time")
    parser.add_argument("--device", type=int, default=0, help="device id")
    parser.add_argument("--python", type=str, default="python", help="python command")
    parser.add_argument("--resume", type=str, default=None, help="resume from a previous run")
    parser.add_argument("--resume-step", type=int, default=0, help="the step to resume from")

    # general agent configs
    parser.add_argument("--agent-type", type=str, default="ResearchAgent", help="agent type")
    parser.add_argument("--llm-name", type=str, default="claude-v1", help="llm name")
    parser.add_argument("--fast-llm-name", type=str, default="claude-v1", help="llm name")
    parser.add_argument("--edit-script-llm-name", type=str, default="claude-v1", help="llm name")
    parser.add_argument("--edit-script-llm-max-tokens", type=int, default=4000, help="llm max tokens")
    parser.add_argument("--agent-max-steps", type=int, default=50, help="max iterations for agent")

    # research agent configs
    parser.add_argument("--actions-remove-from-prompt", type=str, nargs='+', default=[], help="actions to remove in addition to the default ones: Read File, Write File, Append File, Retrieval from Research Log, Append Summary to Research Log, Python REPL, Edit Script Segment (AI)")
    parser.add_argument("--actions-add-to-prompt", type=str, nargs='+', default=[], help="actions to add")
    parser.add_argument("--retrieval", action="store_true", help="enable retrieval")
    parser.add_argument("--valid-format-entires", type=str, nargs='+', default=None, help="valid format entries")
    parser.add_argument("--max-steps-in-context", type=int, default=3, help="max steps in context")
    parser.add_argument("--max-observation-steps-in-context", type=int, default=3, help="max observation steps in context")
    parser.add_argument("--max-retries", type=int, default=5, help="max retries")

    args = parser.parse_args()
    print(vars(args), file=sys.stderr)
    if not args.retrieval or args.agent_type != "ResearchAgent":
        # should not use these actions when there is no retrieval
        args.actions_remove_from_prompt.extend(["Retrieval from Research Log", "Append Summary to Research Log", "Reflection"])
    LLM.FAST_MODEL = args.fast_llm_name
    run(getattr(sys.modules[__name__], args.agent_type), args)
    
