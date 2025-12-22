from orchestrator import run_multi_agent_workflow
import time

def main():
    print("=" * 70)
    print("   MULTI-AGENT ORCHESTRATION FRAMEWORK (LangChain)")
    print("   Shared Memory + Per-Agent Memory Enabled")
    print("=" * 70)
    print("Type 'exit' to quit | 'clear' to reset memory\n")

    while True:
        try:
            query = input("\n🗣️ you: ").strip()

            if not query:
                continue
            if query.lower() == "exit":
                print("\n👋 Goodbye!")
                break
            if query.lower() == "clear":
                print("\n🧹 Memory cleared!")
                continue

            print("\n🤖 Agents thinking...")
            start_time = time.time()
            
            # Run multi-agent workflow (handles all memory automatically)
            result = run_multi_agent_workflow(query)
            
            elapsed = time.time() - start_time

            print(f"🤖 Agent: Response  ({elapsed:.1f}s)")
            print(result)
            print("\n" + "-"*70)

        except KeyboardInterrupt:
            print("\n\n👋 Interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ System error: {e}")
            print("🔄 Continuing...\n")

if __name__ == "__main__":
    main()