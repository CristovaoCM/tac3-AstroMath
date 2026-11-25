import subprocess
import sys
import os

def run_commands():
    
    os.makedirs("docs", exist_ok=True)
    
    base_cmd = [sys.executable, "-c", "import sys; from pylint.pyreverse.main import Run; Run(sys.argv[1:])"]
    
    
    commands = [
        base_cmd + ["-o", "mmd", "source/modules", "-S", "-k", "-p", "game", "-d", "docs"],
        base_cmd + ["-o", "puml", "source/modules", "-S", "-k", "-p", "game", "-d", "docs"]
    ]
    
    for cmd in commands:
      
        print(f"\n🚀 Running: pyreverse {' '.join(cmd[3:])}")
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,  
                text=True,            
                check=True            
            )
            print("✅ Sucesso: Diagrama gerado na pasta docs!")
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Error executing command")
            print(f"Exit Code: {e.returncode}")
            print(f"Error Message: {e.stderr}")
            print("Stopping automation due to error.")
            sys.exit(1)

if __name__ == "__main__":
    run_commands()