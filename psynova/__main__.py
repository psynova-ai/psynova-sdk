#!python

from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich import print as rprint

from .client import PsynovaClient


def interactive():
    console = Console()

    console.print("\n[bold cyan]✨ Welcome to [bold magenta]Psynova[/bold magenta] ✨[/bold cyan]")
    console.print("[bold blue]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/bold blue]")
    console.print("[bold magenta]  ╔═╗╔═╗╦ ╦╔╗╔╔═╗╦  ╦╔═╗  [/bold magenta]")
    console.print("[bold magenta]  ╠═╝╚═╗╚╦╝║║║║ ║╚╗╔╝╠═╣  [/bold magenta]") 
    console.print("[bold magenta]  ╩  ╚═╝ ╩ ╝╚╝╚═╝ ╚╝ ╩ ╩  [/bold magenta]")
    console.print("[bold blue]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/bold blue]")
    console.print("[cyan]🤖 The Next-Gen AI Agent Framework[/cyan]")
    console.print("[dim italic]Empowering developers to create, manage and interact[/dim italic]")
    console.print("[dim italic]with AI agents through an elegant API interface[/dim italic]\n")

    # Get private key
    private_key = Prompt.ask("[yellow]Please enter your private key[/yellow]")
    
    try:
        client = PsynovaClient(private_key)
        console.print("[green]Successfully connected![/green]\n")
    except Exception as e:
        console.print(f"[red]Error connecting: {str(e)}[/red]")
        return

    while True:
        console.print("\n[bold cyan]Available options:[/bold cyan]")
        console.print("1. Create new agent")
        console.print("2. List existing agents") 
        console.print("3. Exit")

        choice = Prompt.ask("\nSelect an option", choices=["1", "2", "3"])

        if choice == "1":
            name = Prompt.ask("\n[yellow]Enter agent name[/yellow]")
            version_id = int(Prompt.ask("[yellow]List of version IDs:\n1 - 3.1 405B Instruct Turbo\n2 - 3.3 70B Instruct Turbo\n3 - 3.1 70B Instruct Turbo\n18 - QwQ-32B-Preview\n19 - 2.5 Coder 32B Instruct Expert\n20 - Qwen 2 Instruct (72B)\n21 - Instruct (27B)\n22 - Instruct (9B)\n23 - Instruct (2B)\n27 - Chat (67B)\n30 - Typhoon 1.5X 70B-awq\n31 - Nemotron 70B\nEnter version ID (example: 1)[/yellow]"))

            try:
                agent_id = client.create_agent(name=name, version_id=version_id)
                console.print(f"\n[green]Successfully created agent with ID: {agent_id}[/green]")
                
                if Confirm.ask("\nWould you like to chat with this agent?"):
                    chat_with_agent(client, agent_id, console)
            
            except Exception as e:
                console.print(f"[red]Error creating agent: {str(e)}[/red]")

        elif choice == "2":
            try:
                agents = client.list_agents()
                
                if not agents or len(agents) == 0:
                    console.print("\n[yellow]No agents found[/yellow]")
                    continue
                    
                console.print("\n[bold cyan]Your agents:[/bold cyan]")
                for agent in agents:
                    console.print(agent)
                    console.print(f"ID: {agent['id']} | Name: {agent['name']} | Status: {agent['status']}")
                
                if Confirm.ask("\nWould you like to chat with an agent?"):
                    agent_id = int(Prompt.ask("[yellow]Enter agent ID[/yellow]"))
                    chat_with_agent(client, agent_id, console)
                    
            except Exception as e:
                console.print(f"[red]Error listing agents: {str(e)}[/red]")

        else:
            console.print("\n[blue]Goodbye![/blue]")
            break


def chat_with_agent(client, agent_id, console):
    console.print(f"\n[bold green]Starting chat with agent {agent_id}[/bold green]")
    console.print("Type 'exit' to end the chat\n")
    
    while True:
        message = Prompt.ask("[bold cyan]You[/bold cyan]")
        
        if message.lower() == 'exit':
            break
            
        try:
            response = client.chat(agent_id, message=message)
            console.print(f"[bold purple]Agent[/bold purple]: {response}")
        except Exception as e:
            console.print(f"[red]Error in chat: {str(e)}[/red]")
            break


def main():
    interactive()

if __name__ == "__main__":
    main()

