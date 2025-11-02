import os
from dotenv import load_dotenv
from orchestrator.workflow_engine import WorkflowEngine
from orchestrator.prompt_tester import PromptTester
import json


class InteractiveConsole:
    """Interactive console for multi-agent system"""

    def __init__(self):
        load_dotenv()

        if not os.getenv('ANTHROPIC_API_KEY'):
            print("Error: ANTHROPIC_API_KEY not found in environment")
            exit(1)

        self.engine = WorkflowEngine()
        self.tester = PromptTester()
        self.current_input = {}

    def start(self):
        """Start interactive session"""
        print("\n" + "="*70)
        print("MULTI-AGENT CONSULTANT INTELLIGENCE SYSTEM")
        print("Interactive Mode")
        print("="*70 + "\n")

        self.engine.initialize_agents()

        print("\nSystem ready. Type 'help' for commands.\n")

        while True:
            try:
                command = input(">>> ").strip().lower()

                if command == 'help':
                    self.show_help()
                elif command == 'quit' or command == 'exit':
                    print("\nGoodbye!\n")
                    break
                elif command == 'input':
                    self.set_input()
                elif command == 'analyze':
                    self.run_analysis()
                elif command == 'test':
                    self.run_ab_test()
                elif command == 'config':
                    self.show_config()
                elif command == 'history':
                    self.show_history()
                elif command.startswith('load'):
                    self.load_document(command)
                elif command == 'clear':
                    self.current_input = {}
                    print("Input cleared.\n")
                else:
                    print(f"Unknown command: {command}")
                    print("Type 'help' for available commands.\n")

            except KeyboardInterrupt:
                print("\n\nInterrupted. Type 'quit' to exit.\n")
            except Exception as e:
                print(f"\nError: {str(e)}\n")

    def show_help(self):
        """Display available commands"""
        help_text = """
AVAILABLE COMMANDS:

Analysis Commands:
  input      - Enter document and context interactively
  load <file>- Load document from file
  analyze    - Run full multi-agent analysis
  clear      - Clear current input

Testing Commands:
  test       - Run A/B test on prompt variants
  config     - Show current agent configuration

Utility Commands:
  history    - Show recent analysis results
  help       - Show this help message
  quit/exit  - Exit interactive mode

"""
        print(help_text)

    def set_input(self):
        """Interactively set input document and context"""
        print("\n" + "-"*70)
        print("DOCUMENT INPUT")
        print("-"*70)
        print("Enter your document text (press Ctrl+D or Ctrl+Z when done):")
        print()

        lines = []
        try:
            while True:
                line = input()
                lines.append(line)
        except EOFError:
            pass

        self.current_input['document'] = '\n'.join(lines)

        print("\n" + "-"*70)
        print("CONTEXT (optional)")
        print("-"*70)
        print("Enter context (press Ctrl+D or Ctrl+Z when done, or just press Enter to skip):")
        print()

        lines = []
        try:
            while True:
                line = input()
                if not line and not lines:  # Empty first line = skip
                    break
                lines.append(line)
        except EOFError:
            pass

        if lines:
            self.current_input['context'] = '\n'.join(lines)

        print("\n✓ Input saved")
        print(f"  Document: {len(self.current_input['document'])} characters")
        if 'context' in self.current_input:
            print(f"  Context: {len(self.current_input['context'])} characters")
        print()

    def load_document(self, command):
        """Load document from file"""
        parts = command.split()
        if len(parts) < 2:
            print("Usage: load <filename>")
            return

        filename = parts[1]

        try:
            with open(filename, 'r') as f:
                self.current_input['document'] = f.read()

            print(f"\n✓ Loaded {filename}")
            print(f"  Document: {len(self.current_input['document'])} characters\n")

        except FileNotFoundError:
            print(f"\nError: File not found: {filename}\n")
        except Exception as e:
            print(f"\nError loading file: {str(e)}\n")

    def run_analysis(self):
        """Run full multi-agent analysis"""
        if not self.current_input.get('document'):
            print("\nError: No document loaded. Use 'input' or 'load' first.\n")
            return

        print("\nStarting analysis...\n")

        result = self.engine.execute_workflow(self.current_input)

        if result['success']:
            # Save output
            brief_path = self.engine.save_output(result)

            # Display brief
            print("\n" + "="*70)
            print("ANALYSIS COMPLETE")
            print("="*70 + "\n")

            with open(brief_path, 'r') as f:
                print(f.read())

            # Show individual agent insights
            self.show_agent_details(result)

        else:
            print(f"\n✗ Analysis failed: {result.get('error', 'Unknown error')}\n")

    def show_agent_details(self, result):
        """Show detailed agent outputs"""
        print("\n" + "="*70)
        print("DETAILED AGENT OUTPUTS")
        print("="*70 + "\n")

        response = input("View detailed agent outputs? (y/n): ").strip().lower()

        if response == 'y':
            for agent_name, agent_result in result['phase1_results'].items():
                if agent_result['success']:
                    print(f"\n{'-'*70}")
                    print(f"{agent_name.upper().replace('_', ' ')}")
                    print(f"{'-'*70}")

                    output = agent_result['output']
                    for key, value in output.items():
                        if not key.startswith('_') and key != 'raw_response':
                            print(f"\n{key.replace('_', ' ').title()}:")
                            print(f"  {value}")

                    print()

    def run_ab_test(self):
        """Run A/B test on prompt variants"""
        if not self.current_input.get('document'):
            print("\nError: No document loaded. Use 'input' or 'load' first.\n")
            return

        print("\n" + "-"*70)
        print("A/B TESTING MODE")
        print("-"*70)
        print("\nAvailable agents to test:")
        print("  1. strategic_analyst")
        print("  2. audience_evaluator")
        print()

        choice = input("Select agent (1 or 2): ").strip()

        agent_map = {
            '1': 'strategic_analyst',
            '2': 'audience_evaluator'
        }

        agent_name = agent_map.get(choice)

        if not agent_name:
            print("\nInvalid choice.\n")
            return

        iterations = input("Number of iterations per variant (default 3): ").strip()
        iterations = int(iterations) if iterations.isdigit() else 3

        print(f"\nRunning A/B test on {agent_name} with {iterations} iterations per variant...")
        print("This may take several minutes...\n")

        results = self.tester.run_ab_test(
            agent_name=agent_name,
            input_data=self.current_input,
            iterations=iterations
        )

        # Save results
        self.tester.save_test_results(results)

        # Display summary
        print("\n" + "="*70)
        print("TEST COMPLETE")
        print("="*70 + "\n")

        print(f"Winner: {results['winner']['variant_name']}")
        print(f"Composite Score: {results['winner']['composite_score']:.3f}\n")

        print("All Scores:")
        for variant_id, score in results['winner']['all_scores'].items():
            print(f"  {variant_id}: {score:.3f}")

        print()

    def show_config(self):
        """Display current configuration"""
        print("\n" + "="*70)
        print("CURRENT CONFIGURATION")
        print("="*70 + "\n")

        for agent_name, config in self.engine.config['agents'].items():
            print(f"{agent_name}:")
            print(f"  Model: {config['parameters']['model']}")
            print(f"  Temperature: {config['parameters']['temperature']}")
            print(f"  Max Tokens: {config['parameters']['max_tokens']}")
            print()

    def show_history(self):
        """Show recent analysis history"""
        import glob

        output_files = sorted(glob.glob('outputs/analysis_*_brief.txt'), reverse=True)

        if not output_files:
            print("\nNo analysis history found.\n")
            return

        print("\n" + "="*70)
        print("RECENT ANALYSES")
        print("="*70 + "\n")

        for i, filepath in enumerate(output_files[:5], 1):
            filename = os.path.basename(filepath)
            timestamp = filename.replace('analysis_', '').replace('_brief.txt', '')

            # Format timestamp
            date_part = timestamp[:8]
            time_part = timestamp[9:]
            formatted = f"{date_part[:4]}-{date_part[4:6]}-{date_part[6:8]} {time_part[:2]}:{time_part[2:4]}:{time_part[4:6]}"

            print(f"{i}. {formatted}")
            print(f"   File: {filepath}")
            print()

        choice = input("View an analysis? (1-5 or Enter to skip): ").strip()

        if choice.isdigit() and 1 <= int(choice) <= min(5, len(output_files)):
            filepath = output_files[int(choice) - 1]

            print("\n" + "="*70)
            with open(filepath, 'r') as f:
                print(f.read())
            print("="*70 + "\n")


def main():
    console = InteractiveConsole()
    console.start()


if __name__ == "__main__":
    main()
