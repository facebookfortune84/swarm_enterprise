from crewai import Task, Crew, Process
from agents.engineering_team import EngineeringTeam

team = EngineeringTeam()
dev = team.developer()
reviewer = team.critic()

def run_software_factory(user_prompt, stack):
    # Step 1: Coding Task
    task_coding = Task(
        description=f"Create a high-scale {stack} application for: {user_prompt}. Write all core files to the /output directory.",
        agent=dev,
        expected_output="All source code files written to disk."
    )

    # Step 2: Critique & Self-Healing Task
    task_review = Task(
        description="Read the files in /output. Validate them against the SOP. If errors are found, use the write_file tool to provide a REJECTION_REPORT.md and force the developer to fix them.",
        agent=reviewer,
        context=[task_coding],
        expected_output="A final validation report confirming the app is production-ready."
    )

    # Execution
    factory_crew = Crew(
        agents=[dev, reviewer],
        tasks=[task_coding, task_review],
        process=Process.sequential
    )
    
    return factory_crew.kickoff()

if __name__ == "__main__":
    # Example Vibe Command
    run_software_factory(
        "A multi-tenant SaaS for managing AI agents with Stripe billing and a React dashboard",
        "FastAPI, PostgreSQL, React, Docker"
    )