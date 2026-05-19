import time
from router.input_router import route_input
from router.state import state
from chat.chat_agent import chat_response
from router.task_router import run_task


def main():
    print("=" * 70)
    print("   MULTI-AGENT ORCHESTRATION FRAMEWORK (LangChain)")
    print("   Intelligent Routing + Chat + Multi-Agent Tasks")
    print("=" * 70)
    print("Type 'exit' to quit | 'clear' to reset session\n")

    while True:
        try:
            user_input = input("\n🗣️ you: ").strip()

            if not user_input:
                continue

            if user_input.lower() == "exit":
                print("\n👋 Goodbye!")
                break

            if user_input.lower() == "clear":
                state.chat_history.clear()
                state.pending_task = None
                print("\n🧹 Session state cleared!")
                continue

            # ROUTING DECISION
            decision = route_input(user_input, state)
            print(f"[ROUTER] → {decision['mode']}")

            start_time = time.time()


            # CHAT MODE
            if decision["mode"] == "CHAT":
                reply = chat_response(user_input, state)
                print("\n🤖", reply)
                continue

            
            # CLARIFY MODE
            if decision["mode"] == "CLARIFY":
                state.pending_task = {
                    "original_query": user_input
                }
                print("\n🤖", decision["question"])
                continue

            # RESUME MODE
            if decision["mode"] == "RESUME":
                if not state.pending_task:
                    print("\n⚠️ No pending task to resume.")
                    continue

                merged_query = (
                    state.pending_task["original_query"]
                    + " "
                    + user_input
                )
                state.pending_task = None  

                new_decision = route_input(merged_query, state)
                print(f"[ROUTER] → {new_decision['mode']}")
                print("\n🤖 Processing...")

                output = run_task(
                    merged_query,
                    new_decision["mode"]
                )

                elapsed = time.time() - start_time
                print("\n🤖 Agent:")
                print(output)
                print(f"\nResponse in ({elapsed:.1f}s)")
                continue

            # COMPLEX TASK EXECUTION
            print("\n🤖 Processing...")
            output = run_task(
                user_input,
                decision["mode"]
            )

            # If agent asks a follow-up question, pause workflow
            if decision["mode"] == "COMPLEX_TASK" and output.strip().endswith("?"):
                state.pending_task = {
                    "original_query": user_input
                }
                print("\n🤖", output)
                continue

            elapsed = time.time() - start_time
            print("\n🤖 Agent:")
            print(output)
            print(f"\nResponse in ({elapsed:.1f}s)")

        except KeyboardInterrupt:
            print("\n\n👋 Interrupted. Goodbye!")
            break

        except Exception as e:
        # CRITICAL FIX: RESET STATE ON ERROR
            state.pending_task = None
            print(f"\n❌ System error: {e}")
            print("🛑 Task aborted. Please try again.\n")


if __name__ == "__main__":
    main()
