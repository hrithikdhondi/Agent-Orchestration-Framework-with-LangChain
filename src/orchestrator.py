from multi_agents import (
    create_planner_agent,
    create_research_agent,
    create_summarizer_agent
)
from memory import AgentMemory
from shared_memory import SharedKnowledgeBase
import uuid

def extract_text(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "".join(
            block.get("text", "")
            for block in content
            if isinstance(block, dict)
        )
    return str(content)


def run_multi_agent_workflow(user_query: str):
    raw_data = ""
    print(f"\n{'='*80}")
    print(f"🔍 Processing: {user_query}")
    print(f"{'='*80}")
    
    # Initialize memory systems
    agent_memory = AgentMemory()
    shared_memory = SharedKnowledgeBase()
    
    # Unique session ID for this conversation
    session_id = str(uuid.uuid4())[:8]
    
    # 1. Get shared knowledge context
    try:
        shared_context = shared_memory.get_context(user_query)
    except Exception:
        shared_context = "Shared memory unavailable."
    
    # Agent IDs for this conversation
    planner_id = f"{session_id}-planner"
    researcher_id = f"{session_id}-researcher"
    summarizer_id = f"{session_id}-summarizer"
    
    # Create agents
    planner = create_planner_agent()
    researcher = create_research_agent()
    summarizer = create_summarizer_agent()
    
    # ========================================
    # STEP 1: PLANNER (with memory + shared knowledge)
    # ========================================
    planner_history = agent_memory.get_agent_memory(planner_id)
    planner_context = f"""
        Previous conversations: {planner_history.messages[-3:] if planner_history.messages else 'None'}
        Shared knowledge: {shared_context}

        User Query: {user_query}
            
        Plan execution steps for Research Agent.
    """
    
    planner_result = planner.invoke({
        "messages": [{"role": "user", "content": planner_context}]
    })
    plan = planner_result["messages"][-1].content
    plan = extract_text(plan)
    
    # Save planner interaction
    agent_memory.add_message(planner_id, "user", user_query)
    agent_memory.add_message(planner_id, "assistant", plan)
    
    print("\n" + "="*50)
    print("📋 PLANNER OUTPUT")
    print("="*50)
    print(plan)

    skip_research = any(
        phrase in plan.lower()
        for phrase in [
            "no research required",
            "research not required",
            "research not needed",
            "generate the answer directly"
        ]
    )

    if skip_research:
        raw_data = "No research required. Generate answer directly."
    else:
         # ========================================
        # STEP 2: RESEARCHER (with memory + shared knowledge)
        # ========================================
        researcher_history = agent_memory.get_agent_memory(researcher_id)
        researcher_context = f"""
            Previous research: {researcher_history.messages[-2:] if researcher_history.messages else 'None'}
            Shared knowledge: {shared_context}

            Execution Plan: {plan}
                
            Execute research steps and return raw data only.
        """
        
        researcher_result = researcher.invoke({
            "messages": [{"role": "user", "content": researcher_context}]
        })
        raw_data = extract_text(researcher_result["messages"][-1].content)

        # Save researcher interaction
        agent_memory.add_message(researcher_id, "user", plan)
        agent_memory.add_message(researcher_id, "assistant", raw_data)

        print("\n" + "="*50)
        print("🔬 RESEARCH OUTPUT")
        print("="*50)
        print(raw_data)

        
   
    
    if not raw_data.strip():
        raw_data = "No research data available."

    # ========================================
    # STEP 3: SUMMARIZER (with full context)
    # ========================================
    summarizer_history = agent_memory.get_agent_memory(summarizer_id)
    full_context = f"""
        Original Query: {user_query}
        Shared Knowledge: {shared_context}
        Research Data: {raw_data}
        Previous summaries: {summarizer_history.messages[-1].content if summarizer_history.messages else 'None'}

        Create polished final answer.
    """
    
    summarizer_result = summarizer.invoke({
        "messages": [{"role": "user", "content": full_context}]
    })
    raw_content = summarizer_result["messages"][-1].content
    final_answer = extract_text(raw_content)

    
    # Save summarizer interaction
    agent_memory.add_message(summarizer_id, "user", raw_data)
    agent_memory.add_message(summarizer_id, "assistant", final_answer)
    
    # ========================================
    # STEP 4: SAVE TO SHARED MEMORY
    # ========================================
    shared_fact = f"Q: {user_query[:50]}... → Key facts: {raw_data[:100]}... → Answer: {final_answer[:50]}..."
    shared_memory.save_fact(shared_fact)
    
    print("\n" + "="*50)
    print("🎯 FINAL ANSWER")
    print("="*50)
    print(final_answer)
    
    return final_answer